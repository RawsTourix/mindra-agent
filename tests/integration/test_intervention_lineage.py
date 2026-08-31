"""Integration tests intervention composition/facade и lineage continuation."""

from dataclasses import fields
from pathlib import Path
from typing import cast
from uuid import NAMESPACE_URL

import pytest

from mindra.composition import (
    CompositionRoot,
    KernelRuntime,
    build_reference_registry,
    load_kernel_profile,
)
from mindra.contracts import (
    Available,
    CognitiveState,
    EvidenceRecorder,
    InterventionError,
    InterventionPolicy,
    LogicalTime,
    ModuleComputeRequest,
    StateInterventionSpec,
    StateInterventionWrite,
    StatePath,
    StateProjection,
    TraceEventEnvelope,
)
from mindra.runtime import (
    CognitiveScheduler,
    CycleExecutionResult,
    DeterministicIdFactory,
)

PROFILE = Path("configs/v0.1/reference.toml")
SOURCE_PATH = StatePath.from_dotted("synthetic.source.value")


def _runtime(*, enabled: bool, seed: str = "intervention-lineage") -> KernelRuntime:
    policy = InterventionPolicy.allowlist((SOURCE_PATH,)) if enabled else None
    return CompositionRoot(
        registry=build_reference_registry(),
        id_factory=DeterministicIdFactory(NAMESPACE_URL, seed),
        intervention_policy=policy,
    ).build(load_kernel_profile(PROFILE))


def _spec(runtime: KernelRuntime, value: int) -> StateInterventionSpec:
    state = runtime.state
    return StateInterventionSpec(
        state.envelope.state_revision,
        state.envelope.lineage_id,
        state.envelope.branch_id,
        (StateInterventionWrite(SOURCE_PATH, value),),
    )


def test_default_runtime_disabled_and_policy_does_not_change_fingerprint() -> None:
    disabled = _runtime(enabled=False, seed="same-composition")
    enabled = _runtime(enabled=True, seed="same-composition")

    assert disabled.composition.fingerprint == enabled.composition.fingerprint
    with pytest.raises(InterventionError):
        disabled.apply_intervention(_spec(disabled, 9))
    assert not hasattr(enabled, "intervention_gateway")
    assert not hasattr(enabled, "private_store")
    assert all("intervention" not in field.name for field in fields(ModuleComputeRequest))
    assert all("intervention" not in field.name for field in fields(StateProjection))


def test_facade_intervention_updates_state_and_next_cycle_continues_lineage() -> None:
    runtime = _runtime(enabled=True)
    base = runtime.state
    result = runtime.apply_intervention(_spec(runtime, 9))

    assert runtime.state is result.state
    assert base is not result.state
    treatment = result.state.entries[SOURCE_PATH].availability
    assert isinstance(treatment, Available)
    assert treatment.value == 9
    treatment_lineage = result.state.envelope.lineage_id
    treatment_branch = result.state.envelope.branch_id

    cycle = runtime.run_cycle()
    assert runtime.state is cycle.state
    assert cycle.state.envelope.lineage_id == treatment_lineage
    assert cycle.state.envelope.branch_id == treatment_branch


def test_failed_facade_intervention_preserves_exact_current_state() -> None:
    runtime = _runtime(enabled=True)
    current = runtime.state
    stale = StateInterventionSpec(
        current.envelope.state_revision.next(),
        current.envelope.lineage_id,
        current.envelope.branch_id,
        (StateInterventionWrite(SOURCE_PATH, 4),),
    )
    with pytest.raises(InterventionError):
        runtime.apply_intervention(stale)
    assert runtime.state is current


class _FailingRecorder:
    def record(self, event: TraceEventEnvelope, /) -> None:
        raise RuntimeError("evidence unavailable")


def test_facade_does_not_replace_state_when_evidence_recording_fails() -> None:
    runtime = _runtime(enabled=True, seed="facade-evidence-failure")
    current = runtime.state
    runtime._intervention_gateway._evidence_recorder = cast(EvidenceRecorder, _FailingRecorder())

    with pytest.raises(RuntimeError, match="evidence unavailable"):
        runtime.apply_intervention(_spec(runtime, 8))
    assert runtime.state is current


class _ThrowingScheduler:
    def run_cycle(
        self, *, current_state: CognitiveState, cycle_time: LogicalTime
    ) -> CycleExecutionResult:
        raise RuntimeError("scheduler infrastructure failed")


def test_cycle_active_resets_after_scheduler_exception() -> None:
    runtime = _runtime(enabled=True, seed="cycle-active-reset")
    runtime._scheduler = cast(CognitiveScheduler, _ThrowingScheduler())

    with pytest.raises(RuntimeError, match="scheduler infrastructure failed"):
        runtime.run_cycle()
    result = runtime.apply_intervention(_spec(runtime, 5))
    assert runtime.state is result.state


def test_active_cycle_rejects_reentrant_intervention() -> None:
    runtime = _runtime(enabled=True, seed="active-cycle-reject")
    current = runtime.state
    runtime._cycle_active = True
    try:
        with pytest.raises(InterventionError, match="active cognitive cycle"):
            runtime.apply_intervention(_spec(runtime, 3))
    finally:
        runtime._cycle_active = False
    assert runtime.state is current
