"""Integration-проверки KernelRuntime DecisionContext bridge."""

from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from typing import cast
from uuid import NAMESPACE_URL, UUID

import pytest

from mindra.composition import (
    CompositionRoot,
    KernelRuntime,
    build_reference_registry,
    load_kernel_profile,
)
from mindra.contracts import (
    AgentSessionId,
    CognitiveModule,
    CompositionError,
    DecisionContext,
    DecisionWindowId,
    EpisodeId,
    ExecutionPhase,
    InterventionError,
    RunId,
    StateInterventionSpec,
    StateInterventionWrite,
)
from mindra.runtime import (
    CommitCoordinator,
    DeterministicIdFactory,
    ExecutionPlanCompiler,
    LifecycleCoordinator,
    LifecycleExecutionOutcome,
    PrivateStateStore,
    SequentialWaveExecutor,
)
from tests.scheduler_support import TestModule


def _runtime(seed: str = "context-runtime") -> KernelRuntime:
    return CompositionRoot(
        registry=build_reference_registry(),
        id_factory=DeterministicIdFactory(NAMESPACE_URL, seed),
    ).build(load_kernel_profile(Path("configs/v0.1/reference.toml")))


def _context(runtime: KernelRuntime) -> DecisionContext:
    time = runtime.state.envelope.logical_time
    assert time.episode_id is not None
    assert time.decision_window_id is not None
    return DecisionContext(
        time.run_id,
        time.agent_session_id,
        time.episode_id,
        time.decision_window_id,
    )


def test_run_cycle_in_owns_distinct_cycle_ids_within_one_decision_window() -> None:
    runtime = _runtime()
    context = _context(runtime)

    first = runtime.run_cycle_in(context=context)
    second = runtime.run_cycle_in(context)

    assert first.cycle_time.cognitive_cycle_id is not None
    assert second.cycle_time.cognitive_cycle_id is not None
    assert first.cycle_time.cognitive_cycle_id != second.cycle_time.cognitive_cycle_id
    assert first.cycle_time.decision_window_id == second.cycle_time.decision_window_id
    assert runtime.state is second.state
    assert runtime.run_cycle().state.envelope.state_revision.value == 9


def test_run_cycle_in_rejects_each_context_mismatch() -> None:
    runtime = _runtime("mismatch")
    context = _context(runtime)
    mismatches = (
        ("run_id", replace(context, run_id=RunId(UUID(int=901)))),
        (
            "agent_session_id",
            replace(context, agent_session_id=AgentSessionId(UUID(int=902))),
        ),
        ("episode_id", replace(context, episode_id=EpisodeId(UUID(int=903)))),
        (
            "decision_window_id",
            replace(context, decision_window_id=DecisionWindowId(UUID(int=904))),
        ),
    )
    for field, mismatch in mismatches:
        with pytest.raises(CompositionError, match=field):
            runtime.run_cycle_in(mismatch)


def test_runtime_rejects_cycle_through_lifecycle_and_unwired_phase() -> None:
    runtime = _runtime("unwired")
    context = _context(runtime)
    with pytest.raises(CompositionError, match="COGNITIVE_CYCLE"):
        runtime.run_lifecycle(ExecutionPhase.COGNITIVE_CYCLE, context)
    with pytest.raises(CompositionError, match="wired"):
        runtime.run_lifecycle(ExecutionPhase.EPISODE_START, context)


def test_configured_lifecycle_phase_delegates_and_updates_current_state() -> None:
    runtime = _runtime("wired")
    source_id = next(
        item.module_id
        for item in runtime.composition.descriptors
        if item.module_id.value == "synthetic.source"
    )
    source = runtime._scheduler._modules[source_id]
    source_descriptor = replace(
        source.descriptor,
        phases=frozenset({ExecutionPhase.COGNITIVE_CYCLE, ExecutionPhase.EPISODE_START}),
    )
    descriptors = tuple(
        source_descriptor if item.module_id == source_id else item
        for item in runtime.composition.descriptors
    )
    schema = runtime._scheduler._commit_coordinator._schema
    factory = DeterministicIdFactory(NAMESPACE_URL, "wired-lifecycle")
    plan = ExecutionPlanCompiler(factory).compile(
        descriptors,
        schema,
        composition_revision=runtime.plan.composition_revision,
        plan_revision=runtime.plan.revision,
        phase=ExecutionPhase.EPISODE_START,
    )
    store = PrivateStateStore(descriptors, {})
    commit = CommitCoordinator(
        schema=schema,
        descriptors=descriptors,
        private_store=store,
        id_factory=factory,
    )
    participant = TestModule(source_descriptor, source.compute)
    coordinator = LifecycleCoordinator(
        plan=plan,
        modules=(cast(CognitiveModule, participant),),
        private_store=store,
        commit_coordinator=commit,
        wave_executor=SequentialWaveExecutor(),
        evidence_recorder=runtime._evidence_recorder,
        id_factory=factory,
    )
    runtime._lifecycle_coordinators = MappingProxyType({ExecutionPhase.EPISODE_START: coordinator})

    result = runtime.run_lifecycle(
        phase=ExecutionPhase.EPISODE_START,
        context=_context(runtime),
    )

    assert result.outcome is LifecycleExecutionOutcome.SUCCEEDED
    assert result.phase_time.cognitive_cycle_id is None
    assert result.phase_time.wave_id is None
    assert runtime.state is result.state
    assert result.state.envelope.state_revision.value == 1
    assert participant.requests[0].context.phase is ExecutionPhase.EPISODE_START


def test_intervention_guard_covers_active_lifecycle_execution() -> None:
    runtime = _runtime("active-lifecycle")
    state = runtime.state
    path = next(iter(state.entries))
    spec = StateInterventionSpec(
        state.envelope.state_revision,
        state.envelope.lineage_id,
        state.envelope.branch_id,
        (StateInterventionWrite(path, 1),),
    )
    runtime._lifecycle_active = True
    try:
        with pytest.raises(InterventionError, match="lifecycle phase"):
            runtime.apply_intervention(spec)
    finally:
        runtime._lifecycle_active = False
