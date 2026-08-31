"""Semantic determinism proof двух fresh canonical reference runs."""

from pathlib import Path
from uuid import NAMESPACE_URL

from mindra.composition import (
    CompositionRoot,
    KernelProfile,
    KernelRuntime,
    build_reference_registry,
    load_kernel_profile,
)
from mindra.contracts import Available, TraceEventKind
from mindra.reference import SYNTHETIC_JOIN_VALUE_KEY
from mindra.runtime import CycleExecutionOutcome, DeterministicIdFactory

PROFILE = Path("configs/v0.1/reference.toml")


def _fresh_run(profile: KernelProfile) -> KernelRuntime:
    runtime = CompositionRoot(
        registry=build_reference_registry(),
        id_factory=DeterministicIdFactory(
            NAMESPACE_URL,
            "mindra.v0_1.kernel_smoke",
            counter=0,
        ),
    ).build(profile)
    result = runtime.run_cycle()
    assert result.outcome is CycleExecutionOutcome.SUCCEEDED
    return runtime


def _plan_semantics(runtime: KernelRuntime) -> tuple[object, ...]:
    plan = runtime.plan
    return (
        plan.phase,
        plan.revision,
        plan.schema_revision,
        plan.composition_revision,
        plan.fingerprint,
        plan.dependencies,
        plan.waves,
    )


def _state_semantics(runtime: KernelRuntime) -> tuple[object, ...]:
    state = runtime.state
    payloads = tuple(
        (path, entry.availability)
        for path, entry in sorted(state.entries.items(), key=lambda item: item[0].dotted)
    )
    return (
        state.envelope.schema_revision,
        state.envelope.state_revision,
        state.envelope.composition_revision,
        payloads,
    )


def _logical_trace(runtime: KernelRuntime) -> tuple[tuple[object, ...], ...]:
    return tuple(
        (event.kind, event.logical_time, event.payload) for event in runtime.evidence_snapshot()
    )


def test_fresh_reference_runs_have_equal_plan_state_and_logical_trace() -> None:
    profile = load_kernel_profile(PROFILE)
    first = _fresh_run(profile)
    second = _fresh_run(profile)

    assert _plan_semantics(first) == _plan_semantics(second)
    assert _state_semantics(first) == _state_semantics(second)
    assert _logical_trace(first) == _logical_trace(second)

    availability = first.state.read(SYNTHETIC_JOIN_VALUE_KEY).availability
    assert isinstance(availability, Available)
    assert availability.value == 10

    kinds = tuple(event.kind for event in first.evidence_snapshot())
    assert kinds[:2] == (
        TraceEventKind.COMPOSITION_RESOLVED,
        TraceEventKind.PLAN_COMPILED,
    )
    assert kinds.count(TraceEventKind.CYCLE_STARTED) == 1
    assert kinds.count(TraceEventKind.CYCLE_FINISHED) == 1
    assert kinds.count(TraceEventKind.WAVE_STARTED) == 3
    assert TraceEventKind.COMMIT_FAILED not in kinds
    assert TraceEventKind.CYCLE_FAILED not in kinds
    assert TraceEventKind.INTERVENTION_APPLIED not in kinds
