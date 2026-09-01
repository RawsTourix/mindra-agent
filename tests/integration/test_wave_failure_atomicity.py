"""Integration checks wave module/commit failure atomicity."""

from dataclasses import replace
from uuid import UUID

from mindra.contracts import (
    Available,
    CognitiveState,
    CommitAttemptedEvent,
    ExecutionPhase,
    LogicalTime,
    ModuleAttemptFinishedEvent,
    ModuleAttemptId,
    ModuleAttemptOutcome,
    ModuleComputeRequest,
    ModuleComputeResult,
    ModuleDescriptor,
    ModuleId,
    PrivateStateSnapshot,
    StateSchema,
)
from mindra.runtime import (
    CognitiveScheduler,
    CommitCoordinator,
    CommitResult,
    CycleExecutionOutcome,
    DeterministicIdFactory,
    InMemoryEvidenceRecorder,
    ModuleAttemptExecutionRequest,
    ModuleAttemptRecord,
    PrivateStateStore,
    SequentialWaveExecutor,
)
from tests.scheduler_support import SchedulerTestContext, make_scheduler_context, module_for


class RecordingCommitCoordinator(CommitCoordinator):
    """Test-only coordinator, считающий фактические commit calls."""

    __slots__ = ("calls",)

    def __init__(
        self,
        *,
        schema: StateSchema,
        descriptors: tuple[ModuleDescriptor, ...],
        private_store: PrivateStateStore,
        id_factory: DeterministicIdFactory,
    ) -> None:
        super().__init__(
            schema=schema,
            descriptors=descriptors,
            private_store=private_store,
            id_factory=id_factory,
        )
        self.calls = 0

    def commit(
        self,
        *,
        current_state: CognitiveState,
        results: tuple[ModuleComputeResult, ...],
        logical_time: LogicalTime,
        phase: ExecutionPhase = ExecutionPhase.COGNITIVE_CYCLE,
    ) -> CommitResult:
        self.calls += 1
        return super().commit(
            current_state=current_state,
            results=results,
            logical_time=logical_time,
            phase=phase,
        )


def _recording_scheduler(
    context: SchedulerTestContext,
) -> tuple[
    CognitiveScheduler,
    RecordingCommitCoordinator,
    DeterministicIdFactory,
    InMemoryEvidenceRecorder,
]:
    commit_factory = DeterministicIdFactory(UUID(int=501), "binding-commit")
    coordinator = RecordingCommitCoordinator(
        schema=context.schema,
        descriptors=context.descriptors,
        private_store=context.store,
        id_factory=commit_factory,
    )
    recorder = InMemoryEvidenceRecorder()
    scheduler = CognitiveScheduler(
        plan=context.plan,
        modules=context.modules,
        private_store=context.store,
        commit_coordinator=coordinator,
        wave_executor=SequentialWaveExecutor(),
        evidence_recorder=recorder,
        id_factory=DeterministicIdFactory(UUID(int=502), "binding-runtime"),
    )
    return scheduler, coordinator, commit_factory, recorder


def test_module_failure_discards_successful_sibling_and_preserves_earlier_wave() -> None:
    context = make_scheduler_context()
    gamma = module_for(context, "gamma")

    def fail(_request: ModuleComputeRequest) -> ModuleComputeResult:
        raise RuntimeError("beta failed")

    beta = module_for(context, "beta")
    beta.set_compute(fail)

    result = context.scheduler.run_cycle(
        current_state=context.state,
        cycle_time=context.cycle_time,
    )

    assert result.outcome is CycleExecutionOutcome.FAILED
    assert result.completed_waves == 1
    assert result.state.envelope.state_revision.value == 1
    assert result.state.read(context.keys["alpha"]).availability == Available(2)
    assert result.state.read(context.keys["beta"]).availability == Available(2)
    assert result.state.read(context.keys["gamma"]).availability == Available(3)
    assert len(gamma.requests) == 1
    private = context.store.snapshot_for(ModuleId("scheduler.alpha"))
    assert isinstance(private, PrivateStateSnapshot)
    assert private.value == 11
    assert not any(
        event.kind.value == "commit_attempted"
        and event.logical_time.wave_id == beta.requests[0].context.logical_time.wave_id
        for event in context.recorder.snapshot()
    )


def test_commit_failure_publishes_no_current_wave_effect() -> None:
    context = make_scheduler_context()
    beta = module_for(context, "beta")
    original = beta.compute_function

    def malformed(request: ModuleComputeRequest) -> ModuleComputeResult:
        result = original(request)
        write = result.state_update.writes[0]
        bad_provenance = replace(write.provenance, logical_time=context.previous_cycle_time)
        return replace(
            result,
            state_update=replace(
                result.state_update,
                writes=(replace(write, provenance=bad_provenance),),
            ),
        )

    beta.set_compute(malformed)
    result = context.scheduler.run_cycle(
        current_state=context.state,
        cycle_time=context.cycle_time,
    )

    assert result.outcome is CycleExecutionOutcome.FAILED
    assert result.completed_waves == 1
    assert result.state.envelope.state_revision.value == 1
    kinds = [event.kind.value for event in context.recorder.snapshot()]
    assert kinds[-3:] == ["commit_attempted", "commit_failed", "cycle_failed"]
    assert result.failure is not None
    assert result.failure.error_type == "CommitValidationError"
    assert "logical_time" in result.failure.message


def test_forged_module_attempt_id_fails_before_commit_without_consuming_commit_id() -> None:
    context = make_scheduler_context()
    alpha = module_for(context, "alpha")
    original = alpha.compute_function
    forged_attempt_id = ModuleAttemptId(UUID(int=503))

    def forged(request: ModuleComputeRequest) -> ModuleComputeResult:
        result = original(request)
        write = result.state_update.writes[0]
        assert result.private_state_update is not None
        return replace(
            result,
            state_update=replace(
                result.state_update,
                module_attempt_id=forged_attempt_id,
                writes=(
                    replace(
                        write,
                        provenance=replace(
                            write.provenance,
                            module_attempt_id=forged_attempt_id,
                        ),
                    ),
                ),
            ),
            private_state_update=replace(
                result.private_state_update,
                module_attempt_id=forged_attempt_id,
            ),
        )

    alpha.set_compute(forged)
    private_before = context.store.snapshot_for(alpha.descriptor.module_id)
    scheduler, coordinator, commit_factory, recorder = _recording_scheduler(context)

    result = scheduler.run_cycle(current_state=context.state, cycle_time=context.cycle_time)

    assert result.outcome is CycleExecutionOutcome.FAILED
    assert result.completed_waves == 0
    assert result.state is context.state
    assert context.store.snapshot_for(alpha.descriptor.module_id) == private_before
    assert coordinator.calls == 0
    assert commit_factory.counter == 0
    finished = [
        event.payload
        for event in recorder.snapshot()
        if isinstance(event.payload, ModuleAttemptFinishedEvent)
    ]
    assert len(finished) == 1
    assert finished[0].module_attempt_id == alpha.requests[0].context.module_attempt_id
    assert finished[0].outcome is ModuleAttemptOutcome.SUCCEEDED
    assert not any(isinstance(event.payload, CommitAttemptedEvent) for event in recorder.snapshot())
    assert result.failure is not None
    assert result.failure.error_type == "WaveExecutionError"
    assert "Wave 0 module scheduler.alpha" in result.failure.message
    assert "state_update.module_attempt_id mismatch" in result.failure.message


def test_forged_producers_fail_in_canonical_order_before_current_wave_commit() -> None:
    context = make_scheduler_context()
    beta = module_for(context, "beta")
    gamma = module_for(context, "gamma")
    beta_behavior = beta.compute_function
    gamma_behavior = gamma.compute_function
    beta.set_compute(gamma_behavior)
    gamma.set_compute(beta_behavior)
    scheduler, coordinator, commit_factory, recorder = _recording_scheduler(context)

    result = scheduler.run_cycle(current_state=context.state, cycle_time=context.cycle_time)

    assert result.outcome is CycleExecutionOutcome.FAILED
    assert result.completed_waves == 1
    assert result.state.envelope.state_revision.value == 1
    assert result.state.read(context.keys["alpha"]).availability == Available(2)
    assert result.state.read(context.keys["beta"]).availability == Available(2)
    assert result.state.read(context.keys["gamma"]).availability == Available(3)
    private = context.store.snapshot_for(ModuleId("scheduler.alpha"))
    assert isinstance(private, PrivateStateSnapshot)
    assert private.value == 11
    assert coordinator.calls == 1
    assert commit_factory.counter == 1
    assert (
        sum(isinstance(event.payload, CommitAttemptedEvent) for event in recorder.snapshot()) == 1
    )
    assert result.failure is not None
    assert result.failure.error_type == "WaveExecutionError"
    assert "Wave 1 module scheduler.beta" in result.failure.message
    assert "state_update.producer mismatch" in result.failure.message
    assert "scheduler.gamma" in result.failure.message


def test_executor_missing_record_fails_closed_without_commit() -> None:
    class MissingRecordExecutor:
        def execute(
            self,
            attempts: tuple[ModuleAttemptExecutionRequest, ...],
            /,
        ) -> tuple[ModuleAttemptRecord, ...]:
            return SequentialWaveExecutor().execute(attempts)[:-1]

    context = make_scheduler_context(wave_executor=MissingRecordExecutor())
    result = context.scheduler.run_cycle(
        current_state=context.state,
        cycle_time=context.cycle_time,
    )

    assert result.outcome is CycleExecutionOutcome.FAILED
    assert result.completed_waves == 0
    assert result.state is context.state
    assert result.failure is not None
    assert result.failure.error_type == "WaveExecutionError"
    assert "missing/extra" in result.failure.message
    assert [event.kind.value for event in context.recorder.snapshot()] == [
        "cycle_started",
        "wave_started",
        "module_attempt_started",
        "cycle_failed",
    ]
