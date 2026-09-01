"""Integration-проверки non-cycle LifecycleCoordinator."""

from dataclasses import replace

import pytest

from mindra.contracts import (
    Available,
    CompositionError,
    CycleFailedEvent,
    CycleFinishedEvent,
    CycleStartedEvent,
    ExecutionPhase,
    LifecyclePhaseFailedEvent,
    LifecyclePhaseFinishedEvent,
    LifecyclePhaseStartedEvent,
    ModuleComputeRequest,
    ModuleComputeResult,
    PrivateStateSnapshot,
)
from mindra.runtime import (
    CognitiveScheduler,
    DeterministicIdFactory,
    LifecycleCoordinator,
    LifecycleExecutionOutcome,
    ModuleAttemptExecutionRequest,
    SequentialWaveExecutor,
)
from tests.lifecycle_support import make_lifecycle_context


@pytest.mark.parametrize(
    "phase",
    [ExecutionPhase.EPISODE_START, ExecutionPhase.POST_OUTCOME],
)
def test_lifecycle_executes_exact_phase_subset_with_atomic_effects(
    phase: ExecutionPhase,
) -> None:
    context = make_lifecycle_context(phase)

    result = context.lifecycle.run(
        current_state=context.base.state,
        phase_time=context.phase_time,
    )

    assert result.outcome is LifecycleExecutionOutcome.SUCCEEDED
    assert result.phase is phase
    assert result.completed_waves == 1
    assert result.base_state_revision == context.base.state.envelope.state_revision
    assert result.state.envelope.state_revision.value == 1
    assert len(context.participant.requests) == 1
    request = context.participant.requests[0]
    assert request.context.phase is phase
    assert request.context.logical_time.cognitive_cycle_id is None
    assert request.context.logical_time.wave_id is not None
    public = result.state.read(context.base.keys["alpha"]).availability
    private = context.store.snapshot_for(context.participant.descriptor.module_id)
    assert isinstance(public, Available) and public.value == 2
    assert isinstance(private, PrivateStateSnapshot) and private.value == 11

    events = context.recorder.snapshot()
    assert isinstance(events[0].payload, LifecyclePhaseStartedEvent)
    assert isinstance(events[-1].payload, LifecyclePhaseFinishedEvent)
    assert not any(
        isinstance(event.payload, CycleStartedEvent | CycleFinishedEvent | CycleFailedEvent)
        for event in events
    )
    assert events[0].logical_time.cognitive_cycle_id is None
    assert events[0].logical_time.wave_id is None
    assert any(event.kind.value == "commit_succeeded" for event in events)
    assert tuple(event.kind.value for event in events) == (
        "lifecycle_phase_started",
        "wave_started",
        "module_attempt_started",
        "module_attempt_finished",
        "commit_attempted",
        "commit_succeeded",
        "state_revision_committed",
        "lifecycle_phase_finished",
    )


def test_current_wave_failure_publishes_no_public_or_private_effects() -> None:
    context = make_lifecycle_context()

    def fail(_request: ModuleComputeRequest) -> ModuleComputeResult:
        raise RuntimeError("expected lifecycle failure")

    context.participant.set_compute(fail)
    before_private = context.store.snapshot_for(context.participant.descriptor.module_id)
    result = context.lifecycle.run(
        current_state=context.base.state,
        phase_time=context.phase_time,
    )

    assert result.outcome is LifecycleExecutionOutcome.FAILED
    assert result.completed_waves == 0
    assert result.state is context.base.state
    assert context.store.snapshot_for(context.participant.descriptor.module_id) == before_private
    assert isinstance(context.recorder.snapshot()[-1].payload, LifecyclePhaseFailedEvent)
    assert not any(event.kind.value == "commit_attempted" for event in context.recorder.snapshot())


def test_commit_validation_failure_publishes_no_current_wave_effects() -> None:
    context = make_lifecycle_context()
    valid_compute = context.participant.compute_function

    def unauthorized(request: ModuleComputeRequest) -> ModuleComputeResult:
        result = valid_compute(request)
        proposal = result.state_update
        wrong_write = replace(proposal.writes[0], key=context.base.keys["beta"])
        return replace(
            result,
            state_update=replace(proposal, writes=(wrong_write,)),
        )

    context.participant.set_compute(unauthorized)
    before_private = context.store.snapshot_for(context.participant.descriptor.module_id)

    result = context.lifecycle.run(
        current_state=context.base.state,
        phase_time=context.phase_time,
    )

    assert result.outcome is LifecycleExecutionOutcome.FAILED
    assert result.state is context.base.state
    assert context.store.snapshot_for(context.participant.descriptor.module_id) == before_private
    assert tuple(event.kind.value for event in context.recorder.snapshot())[-2:] == (
        "commit_failed",
        "lifecycle_phase_failed",
    )


def test_coordinator_rejects_cycle_plan_and_executor_rejects_undeclared_phase() -> None:
    context = make_lifecycle_context()
    with pytest.raises(CompositionError, match="COGNITIVE_CYCLE"):
        LifecycleCoordinator(
            plan=context.base.plan,
            modules=context.base.modules,
            private_store=context.base.store,
            commit_coordinator=context.base.coordinator,
            wave_executor=SequentialWaveExecutor(),
            evidence_recorder=context.base.recorder,
            id_factory=DeterministicIdFactory(
                context.phase_time.run_id,
                "reject-cycle-plan",
            ),
        )
    with pytest.raises(CompositionError, match="COGNITIVE_CYCLE"):
        CognitiveScheduler(
            plan=context.plan,
            modules=(context.participant,),
            private_store=context.store,
            commit_coordinator=context.coordinator,
            wave_executor=SequentialWaveExecutor(),
            evidence_recorder=context.recorder,
            id_factory=DeterministicIdFactory(
                context.phase_time.run_id,
                "reject-lifecycle-plan",
            ),
        )

    context.lifecycle.run(
        current_state=context.base.state,
        phase_time=context.phase_time,
    )
    request = context.participant.requests[0]
    wrong = replace(
        request,
        context=replace(request.context, phase=ExecutionPhase.COGNITIVE_CYCLE),
    )
    with pytest.raises(ValueError, match="phase"):
        ModuleAttemptExecutionRequest(
            module_id=context.participant.descriptor.module_id,
            module=context.participant,
            compute_request=wrong,
        )
