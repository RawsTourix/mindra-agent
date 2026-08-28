"""Integration checks deterministic Scheduler wave execution."""

from dataclasses import replace
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentSessionId,
    Available,
    CognitiveCycleId,
    CommitValidationError,
    CompositionError,
    CompositionRevision,
    DecisionWindowId,
    EpisodeId,
    LogicalTime,
    ModuleAttemptStartedEvent,
    ModuleId,
    RunId,
    SchemaRevision,
    StateSchema,
    WaveId,
)
from mindra.runtime import (
    CognitiveScheduler,
    CommitCoordinator,
    CycleExecutionOutcome,
    DeterministicIdFactory,
    ExecutionPlanCompiler,
    InMemoryEvidenceRecorder,
    PrivateStateStore,
    SequentialWaveExecutor,
    build_cognitive_state,
)
from tests.scheduler_support import make_scheduler_context, module_for


def test_scheduler_executes_plan_waves_and_next_wave_sees_committed_state() -> None:
    context = make_scheduler_context()

    result = context.scheduler.run_cycle(
        current_state=context.state,
        cycle_time=context.cycle_time,
    )

    assert result.outcome is CycleExecutionOutcome.SUCCEEDED
    assert result.completed_waves == 2
    assert result.base_state_revision == context.state.envelope.state_revision
    assert result.state.envelope.state_revision.value == 2
    alpha = result.state.read(context.keys["alpha"]).availability
    beta = result.state.read(context.keys["beta"]).availability
    gamma = result.state.read(context.keys["gamma"]).availability
    assert isinstance(alpha, Available) and alpha.value == 2
    assert isinstance(beta, Available) and beta.value == 4
    assert isinstance(gamma, Available) and gamma.value == 6

    alpha_request = module_for(context, "alpha").requests[0]
    beta_request = module_for(context, "beta").requests[0]
    gamma_request = module_for(context, "gamma").requests[0]
    assert alpha_request.context.base_state_revision.value == 0
    assert beta_request.context.base_state_revision.value == 1
    assert gamma_request.context.base_state_revision == beta_request.context.base_state_revision
    assert beta_request.context.logical_time.cognitive_cycle_id == (
        context.cycle_time.cognitive_cycle_id
    )


def test_registration_order_does_not_change_plan_order() -> None:
    context = make_scheduler_context()
    assert tuple(module.descriptor.module_id.value for module in context.modules) == (
        "scheduler.gamma",
        "scheduler.alpha",
        "scheduler.beta",
    )

    context.scheduler.run_cycle(current_state=context.state, cycle_time=context.cycle_time)

    started = [
        event.payload.module_id.value
        for event in context.recorder.snapshot()
        if isinstance(event.payload, ModuleAttemptStartedEvent)
    ]
    assert started == ["scheduler.alpha", "scheduler.beta", "scheduler.gamma"]


def test_scheduler_rejects_missing_module_and_different_private_store() -> None:
    context = make_scheduler_context()
    with pytest.raises(CompositionError, match="missing"):
        CognitiveScheduler(
            plan=context.plan,
            modules=context.modules[:-1],
            private_store=context.store,
            commit_coordinator=context.coordinator,
            wave_executor=SequentialWaveExecutor(),
            evidence_recorder=InMemoryEvidenceRecorder(),
            id_factory=DeterministicIdFactory(UUID(int=200), "missing"),
        )

    other_store = PrivateStateStore(
        context.descriptors,
        {ModuleId("scheduler.alpha"): 10},
    )
    with pytest.raises(CommitValidationError, match="один PrivateStateStore"):
        CognitiveScheduler(
            plan=context.plan,
            modules=context.modules,
            private_store=other_store,
            commit_coordinator=context.coordinator,
            wave_executor=SequentialWaveExecutor(),
            evidence_recorder=InMemoryEvidenceRecorder(),
            id_factory=DeterministicIdFactory(UUID(int=201), "store"),
        )


@pytest.mark.parametrize(
    "cycle_time",
    [
        LogicalTime(
            run_id=RunId(UUID(int=1)),
            agent_session_id=AgentSessionId(UUID(int=2)),
            episode_id=EpisodeId(UUID(int=3)),
            decision_window_id=DecisionWindowId(UUID(int=4)),
        ),
        LogicalTime(
            run_id=RunId(UUID(int=99)),
            agent_session_id=AgentSessionId(UUID(int=2)),
            episode_id=EpisodeId(UUID(int=3)),
            decision_window_id=DecisionWindowId(UUID(int=4)),
            cognitive_cycle_id=CognitiveCycleId(UUID(int=11)),
        ),
        LogicalTime(
            run_id=RunId(UUID(int=1)),
            agent_session_id=AgentSessionId(UUID(int=2)),
            episode_id=EpisodeId(UUID(int=3)),
            decision_window_id=DecisionWindowId(UUID(int=4)),
            cognitive_cycle_id=CognitiveCycleId(UUID(int=11)),
            wave_id=WaveId(UUID(int=12)),
        ),
    ],
)
def test_cycle_preflight_rejects_invalid_temporal_context(cycle_time: LogicalTime) -> None:
    context = make_scheduler_context()
    with pytest.raises((ValueError, CommitValidationError)):
        context.scheduler.run_cycle(current_state=context.state, cycle_time=cycle_time)
    assert len(context.recorder) == 0


def test_cycle_preflight_rejects_schema_and_composition_revision_mismatch() -> None:
    context = make_scheduler_context()
    schema = StateSchema(
        SchemaRevision(context.plan.schema_revision.value + 1),
        tuple(context.schema.fields.values()),
    )
    bad_envelope = replace(
        context.state.envelope,
        schema_revision=schema.revision,
    )
    bad_state = build_cognitive_state(
        schema=schema,
        envelope=bad_envelope,
        entries=context.state.entries,
    )
    with pytest.raises(CommitValidationError, match="schema revision"):
        context.scheduler.run_cycle(
            current_state=bad_state,
            cycle_time=context.cycle_time,
        )

    composition_state = build_cognitive_state(
        schema=context.schema,
        envelope=replace(
            context.state.envelope,
            composition_revision=CompositionRevision(99),
        ),
        entries=context.state.entries,
    )
    with pytest.raises(CommitValidationError, match="composition revision"):
        context.scheduler.run_cycle(
            current_state=composition_state,
            cycle_time=context.cycle_time,
        )


def test_empty_plan_keeps_state_revision_across_distinct_caller_owned_cycles() -> None:
    context = make_scheduler_context()
    plan = ExecutionPlanCompiler(DeterministicIdFactory(UUID(int=300), "empty-plan")).compile(
        (),
        context.schema,
        composition_revision=context.plan.composition_revision,
        plan_revision=context.plan.revision,
    )
    store = PrivateStateStore((), {})
    coordinator = CommitCoordinator(
        schema=context.schema,
        descriptors=(),
        private_store=store,
        id_factory=DeterministicIdFactory(UUID(int=301), "empty-commit"),
    )
    recorder = InMemoryEvidenceRecorder()
    scheduler = CognitiveScheduler(
        plan=plan,
        modules=(),
        private_store=store,
        commit_coordinator=coordinator,
        wave_executor=SequentialWaveExecutor(),
        evidence_recorder=recorder,
        id_factory=DeterministicIdFactory(UUID(int=302), "empty-runtime"),
    )
    second_time = replace(
        context.cycle_time,
        cognitive_cycle_id=CognitiveCycleId(UUID(int=12)),
    )

    first = scheduler.run_cycle(current_state=context.state, cycle_time=context.cycle_time)
    second = scheduler.run_cycle(current_state=first.state, cycle_time=second_time)

    assert first.state is context.state
    assert second.state is context.state
    assert first.completed_waves == second.completed_waves == 0
    assert first.cycle_time.cognitive_cycle_id != second.cycle_time.cognitive_cycle_id
    assert [event.kind.value for event in recorder.snapshot()] == [
        "cycle_started",
        "cycle_finished",
        "cycle_started",
        "cycle_finished",
    ]
