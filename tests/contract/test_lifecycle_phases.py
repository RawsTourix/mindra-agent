"""Contract-проверки стандартных lifecycle phases и plans."""

from dataclasses import fields, replace
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    CommitValidationError,
    DecisionContext,
    ExecutionPhase,
    ExecutionPlanError,
    LifecyclePhaseStartedEvent,
    LogicalTime,
    PlanCompiledEvent,
    PlanWaveTrace,
    TraceEventEnvelope,
)
from mindra.runtime import DeterministicIdFactory, ExecutionPlanCompiler
from tests.commit_support import make_context as make_commit_context
from tests.commit_support import result_for
from tests.lifecycle_support import make_lifecycle_context
from tests.scheduler_support import make_scheduler_context


def test_execution_phase_and_decision_context_have_exact_shape() -> None:
    assert tuple(ExecutionPhase) == (
        ExecutionPhase.COGNITIVE_CYCLE,
        ExecutionPhase.EPISODE_START,
        ExecutionPhase.POST_OUTCOME,
    )
    assert tuple(field.name for field in fields(DecisionContext)) == (
        "run_id",
        "agent_session_id",
        "episode_id",
        "decision_window_id",
    )
    context = make_scheduler_context().cycle_time
    assert context.episode_id is not None
    assert context.decision_window_id is not None
    decision = DecisionContext(
        context.run_id,
        context.agent_session_id,
        context.episode_id,
        context.decision_window_id,
    )
    assert decision.decision_window_id == context.decision_window_id


def test_compiler_default_preserves_cycle_and_explicit_phase_selects_subset() -> None:
    lifecycle = make_lifecycle_context()
    compiler = ExecutionPlanCompiler(DeterministicIdFactory(UUID(int=810), "phase-plan"))
    cycle = make_scheduler_context()
    default_cycle = compiler.compile(
        cycle.descriptors,
        cycle.schema,
        composition_revision=cycle.plan.composition_revision,
        plan_revision=cycle.plan.revision,
    )
    explicit_cycle = compiler.compile(
        cycle.descriptors,
        cycle.schema,
        composition_revision=cycle.plan.composition_revision,
        plan_revision=cycle.plan.revision,
        phase=ExecutionPhase.COGNITIVE_CYCLE,
    )

    explicit = compiler.compile(
        lifecycle.descriptors,
        lifecycle.base.schema,
        composition_revision=lifecycle.plan.composition_revision,
        plan_revision=lifecycle.plan.revision,
        phase=ExecutionPhase.POST_OUTCOME,
    )

    assert lifecycle.plan.phase is ExecutionPhase.EPISODE_START
    assert default_cycle.phase is ExecutionPhase.COGNITIVE_CYCLE
    assert default_cycle.fingerprint == explicit_cycle.fingerprint
    assert explicit.phase is ExecutionPhase.POST_OUTCOME
    assert lifecycle.plan.descriptors == explicit.descriptors
    assert lifecycle.plan.fingerprint != explicit.fingerprint
    assert tuple(item.module_id.value for item in explicit.descriptors) == ("scheduler.alpha",)


def test_non_cycle_current_cycle_read_is_rejected_and_empty_plan_is_valid() -> None:
    base = make_scheduler_context()
    beta = next(item for item in base.descriptors if item.module_id.value == "scheduler.beta")
    invalid = replace(beta, phases=frozenset({ExecutionPhase.EPISODE_START}))
    compiler = ExecutionPlanCompiler(DeterministicIdFactory(UUID(int=811), "invalid-plan"))
    with pytest.raises(ExecutionPlanError, match="CURRENT_CYCLE"):
        compiler.compile(
            (invalid,),
            base.schema,
            composition_revision=base.plan.composition_revision,
            plan_revision=base.plan.revision,
            phase=ExecutionPhase.EPISODE_START,
        )

    empty = compiler.compile(
        base.descriptors,
        base.schema,
        composition_revision=base.plan.composition_revision,
        plan_revision=base.plan.revision,
        phase=ExecutionPhase.POST_OUTCOME,
    )
    assert empty.descriptors == ()
    assert empty.dependencies == ()
    assert empty.waves == ()


def test_plan_compiled_event_accepts_lifecycle_phase() -> None:
    context = make_lifecycle_context()
    payload = PlanCompiledEvent(
        plan_id=context.plan.plan_id,
        plan_revision=context.plan.revision,
        composition_revision=context.plan.composition_revision,
        schema_revision=context.plan.schema_revision,
        phase=context.plan.phase,
        plan_fingerprint=context.plan.fingerprint.value,
        dependencies=(),
        waves=tuple(
            PlanWaveTrace(index=wave.index, module_ids=wave.module_ids)
            for wave in context.plan.waves
        ),
    )
    envelope = TraceEventEnvelope(context.phase_time, payload)
    assert isinstance(envelope.payload, PlanCompiledEvent)
    assert envelope.payload.phase is ExecutionPhase.EPISODE_START
    phase_payload = LifecyclePhaseStartedEvent(
        phase=context.plan.phase,
        base_state_revision=context.base.state.envelope.state_revision,
        plan_id=context.plan.plan_id,
        plan_revision=context.plan.revision,
        agent_revision_id=context.base.state.envelope.agent_revision_id,
    )
    with pytest.raises(ValueError, match="DecisionContext"):
        TraceEventEnvelope(
            LogicalTime(
                run_id=context.phase_time.run_id,
                agent_session_id=context.phase_time.agent_session_id,
            ),
            phase_payload,
        )


def test_invalid_phase_objects_fail_closed() -> None:
    context = make_lifecycle_context()
    with pytest.raises(TypeError, match="phase"):
        ExecutionPlanCompiler(DeterministicIdFactory(UUID(int=812), "bad-phase")).compile(
            context.plan.descriptors,
            context.base.schema,
            composition_revision=context.plan.composition_revision,
            plan_revision=context.plan.revision,
            phase=cast(ExecutionPhase, "episode_start"),
        )


def test_commit_rejects_producer_that_did_not_declare_current_phase() -> None:
    context = make_commit_context()
    with pytest.raises(CommitValidationError, match="episode_start"):
        context.coordinator.commit(
            current_state=context.state,
            results=(result_for(context, "gamma", public_value=4),),
            logical_time=context.logical_time,
            phase=ExecutionPhase.EPISODE_START,
        )
