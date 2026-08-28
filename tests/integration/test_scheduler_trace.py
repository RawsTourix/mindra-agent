"""Integration checks exact deterministic Scheduler O0 producer ordering."""

from uuid import UUID

from mindra.contracts import (
    CommitSucceededEvent,
    ModuleAttemptFinishedEvent,
    ModuleComputeRequest,
    ModuleComputeResult,
    ModuleId,
    PrivateStateProposal,
    PrivateStateSnapshot,
    StateRevisionCommittedEvent,
    StateUpdateProposal,
)
from mindra.runtime import (
    CognitiveScheduler,
    CommitCoordinator,
    DeterministicIdFactory,
    ExecutionPlanCompiler,
    InMemoryEvidenceRecorder,
    ModuleAttemptExecutionRequest,
    ModuleAttemptRecord,
    PrivateStateStore,
    SequentialWaveExecutor,
)
from tests.scheduler_support import TestModule, make_scheduler_context


def test_successful_cycle_emits_exact_canonical_structural_trace() -> None:
    context = make_scheduler_context()
    result = context.scheduler.run_cycle(
        current_state=context.state,
        cycle_time=context.cycle_time,
    )
    events = context.recorder.snapshot()

    assert [event.kind.value for event in events] == [
        "cycle_started",
        "wave_started",
        "module_attempt_started",
        "module_attempt_finished",
        "commit_attempted",
        "commit_succeeded",
        "state_revision_committed",
        "wave_started",
        "module_attempt_started",
        "module_attempt_started",
        "module_attempt_finished",
        "module_attempt_finished",
        "commit_attempted",
        "commit_succeeded",
        "state_revision_committed",
        "cycle_finished",
    ]
    assert all(event.physical_timestamp_ns is None for event in events)
    assert not {
        "composition_resolved",
        "plan_compiled",
        "intervention_applied",
    }.intersection(event.kind.value for event in events)

    successful = [
        event.payload for event in events if isinstance(event.payload, CommitSucceededEvent)
    ]
    committed = [
        event.payload for event in events if isinstance(event.payload, StateRevisionCommittedEvent)
    ]
    assert successful[-1].resulting_state_revision == result.state.envelope.state_revision
    assert successful[-1].private_revisions == ()
    assert committed[-1].commit_id == successful[-1].commit_id
    assert committed[-1].public_paths == successful[-1].public_paths


def test_finished_attempt_events_are_canonical_independent_of_executor_return_order() -> None:
    class ReverseExecutor:
        def execute(
            self,
            attempts: tuple[ModuleAttemptExecutionRequest, ...],
            /,
        ) -> tuple[ModuleAttemptRecord, ...]:
            sequential = SequentialWaveExecutor()
            return tuple(reversed(sequential.execute(attempts)))

    context = make_scheduler_context(wave_executor=ReverseExecutor())
    context.scheduler.run_cycle(current_state=context.state, cycle_time=context.cycle_time)
    finished = [
        event.payload.module_id.value
        for event in context.recorder.snapshot()
        if isinstance(event.payload, ModuleAttemptFinishedEvent)
    ]
    assert finished == ["scheduler.alpha", "scheduler.beta", "scheduler.gamma"]


def test_private_only_wave_commits_without_fake_public_revision_event() -> None:
    context = make_scheduler_context()
    descriptor = next(
        item for item in context.descriptors if item.module_id == ModuleId("scheduler.alpha")
    )

    def private_only(request: ModuleComputeRequest) -> ModuleComputeResult:
        assert isinstance(request.private_state, PrivateStateSnapshot)
        assert isinstance(request.private_state.value, int)
        return ModuleComputeResult(
            state_update=StateUpdateProposal(
                base_state_revision=request.context.base_state_revision,
                producer=descriptor.module_id,
                module_attempt_id=request.context.module_attempt_id,
                writes=(),
            ),
            private_state_update=PrivateStateProposal(
                module_id=descriptor.module_id,
                base_revision=request.private_state.revision,
                module_attempt_id=request.context.module_attempt_id,
                value=request.private_state.value + 1,
            ),
        )

    plan = ExecutionPlanCompiler(DeterministicIdFactory(UUID(int=400), "private-plan")).compile(
        (descriptor,),
        context.schema,
        composition_revision=context.plan.composition_revision,
        plan_revision=context.plan.revision,
    )
    store = PrivateStateStore((descriptor,), {descriptor.module_id: 10})
    coordinator = CommitCoordinator(
        schema=context.schema,
        descriptors=(descriptor,),
        private_store=store,
        id_factory=DeterministicIdFactory(UUID(int=401), "private-commit"),
    )
    recorder = InMemoryEvidenceRecorder()
    scheduler = CognitiveScheduler(
        plan=plan,
        modules=(TestModule(descriptor, private_only),),
        private_store=store,
        commit_coordinator=coordinator,
        wave_executor=SequentialWaveExecutor(),
        evidence_recorder=recorder,
        id_factory=DeterministicIdFactory(UUID(int=402), "private-runtime"),
    )

    result = scheduler.run_cycle(
        current_state=context.state,
        cycle_time=context.cycle_time,
    )

    assert result.state is context.state
    assert result.completed_waves == 1
    private = store.snapshot_for(descriptor.module_id)
    assert isinstance(private, PrivateStateSnapshot)
    assert private.value == 11
    assert [event.kind.value for event in recorder.snapshot()] == [
        "cycle_started",
        "wave_started",
        "module_attempt_started",
        "module_attempt_finished",
        "commit_attempted",
        "commit_succeeded",
        "cycle_finished",
    ]
    succeeded = next(
        event.payload
        for event in recorder.snapshot()
        if isinstance(event.payload, CommitSucceededEvent)
    )
    assert succeeded.public_paths == ()
    assert len(succeeded.private_revisions) == 1
