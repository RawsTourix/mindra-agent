"""Runnable reference composition через narrow KernelRuntime facade."""

from dataclasses import replace
from pathlib import Path
from typing import cast
from uuid import NAMESPACE_URL

from mindra.composition import (
    CompositionRoot,
    ImplementationFactoryDescriptor,
    ImplementationRegistry,
    KernelRuntime,
    ModuleProfile,
    ResolvedModule,
    ResolvedStateField,
    build_reference_registry,
    load_kernel_profile,
)
from mindra.contracts import (
    Available,
    CognitiveModule,
    ImplementationId,
    ModuleComputeRequest,
    ModuleComputeResult,
    StateFieldSpec,
    StateKey,
    Unknown,
    ValueContract,
)
from mindra.reference import (
    SYNTHETIC_DOUBLE_VALUE_KEY,
    SYNTHETIC_JOIN_VALUE_KEY,
    SYNTHETIC_SOURCE_VALUE_KEY,
    SYNTHETIC_TRIPLE_VALUE_KEY,
    SyntheticJoinModule,
)
from mindra.runtime import CycleExecutionOutcome, DeterministicIdFactory


def _runtime() -> KernelRuntime:
    return CompositionRoot(
        registry=build_reference_registry(),
        id_factory=DeterministicIdFactory(NAMESPACE_URL, "runtime"),
    ).build(load_kernel_profile(Path("configs/v0.1/reference.toml")))


def _available_value(runtime: KernelRuntime, key: StateKey[int]) -> int:
    entry = runtime.state.read(key)
    assert isinstance(entry.availability, Available)
    assert type(entry.availability.value) is int
    return entry.availability.value


def test_reference_runtime_runs_two_cycles_with_pinned_outer_scopes() -> None:
    runtime = _runtime()
    initial_time = runtime.state.envelope.logical_time

    first = runtime.run_cycle()
    assert first.outcome is CycleExecutionOutcome.SUCCEEDED
    assert first.completed_waves == 3
    assert first.state.envelope.state_revision.value == 3
    assert runtime.state is first.state
    assert _available_value(runtime, SYNTHETIC_SOURCE_VALUE_KEY) == 2
    assert _available_value(runtime, SYNTHETIC_DOUBLE_VALUE_KEY) == 4
    assert _available_value(runtime, SYNTHETIC_TRIPLE_VALUE_KEY) == 6
    assert _available_value(runtime, SYNTHETIC_JOIN_VALUE_KEY) == 10

    second = runtime.run_cycle()
    assert second.outcome is CycleExecutionOutcome.SUCCEEDED
    assert second.state.envelope.state_revision.value == 6
    assert runtime.state is second.state
    assert first.cycle_time.cognitive_cycle_id != second.cycle_time.cognitive_cycle_id
    for field_name in ("run_id", "agent_session_id", "episode_id", "decision_window_id"):
        assert getattr(first.cycle_time, field_name) == getattr(second.cycle_time, field_name)
        assert getattr(first.cycle_time, field_name) == getattr(initial_time, field_name)


def test_runtime_public_surface_does_not_expose_internal_services() -> None:
    runtime = _runtime()

    assert not any(
        hasattr(runtime, name)
        for name in ("private_store", "commit_coordinator", "registry", "services", "modules")
    )
    assert callable(runtime.run_cycle)
    assert callable(runtime.evidence_snapshot)


def test_evidence_contains_root_events_before_scheduler_trace() -> None:
    runtime = _runtime()
    runtime.run_cycle()

    kinds = tuple(event.kind.value for event in runtime.evidence_snapshot())
    assert kinds[:3] == ("composition_resolved", "plan_compiled", "cycle_started")
    assert kinds[-1] == "cycle_finished"


class _FailingJoinModule:
    descriptor = replace(
        SyntheticJoinModule().descriptor,
        implementation_id=ImplementationId("test.failing_join.v1"),
    )

    def compute(self, request: ModuleComputeRequest) -> ModuleComputeResult:
        raise RuntimeError("expected later-wave failure")


def _build_failing_join(profile: ModuleProfile) -> ResolvedModule:
    assert profile.module_id == _FailingJoinModule.descriptor.module_id
    assert profile.implementation_id == _FailingJoinModule.descriptor.implementation_id
    assert profile.settings == ()
    return ResolvedModule(
        module=cast(CognitiveModule, _FailingJoinModule()),
        state_fields=(
            ResolvedStateField(
                spec=StateFieldSpec(
                    key=cast(StateKey[object], SYNTHETIC_JOIN_VALUE_KEY),
                    owner=_FailingJoinModule.descriptor.module_id,
                    value_contract=cast(ValueContract[object], ValueContract(int)),
                ),
                initial_availability=Unknown(),
            ),
        ),
        resolved_settings=(),
        initial_private_state=None,
    )


def test_failed_later_wave_preserves_earlier_commits_in_runtime_state() -> None:
    profile = load_kernel_profile(Path("configs/v0.1/reference.toml"))
    failing_profile = type(profile)(
        profile.schema,
        profile.profile_id,
        tuple(
            ModuleProfile(
                item.module_id,
                ImplementationId("test.failing_join.v1"),
                item.settings,
            )
            if item.module_id.value == "synthetic.join"
            else item
            for item in profile.modules
        ),
    )
    reference = build_reference_registry()
    registry = ImplementationRegistry(
        (
            reference.resolve(ImplementationId("reference.synthetic_source.v1")),
            reference.resolve(ImplementationId("reference.synthetic_double.v1")),
            reference.resolve(ImplementationId("reference.synthetic_triple.v1")),
            ImplementationFactoryDescriptor(
                ImplementationId("test.failing_join.v1"),
                _build_failing_join,
            ),
        )
    )
    runtime = CompositionRoot(
        registry=registry,
        id_factory=DeterministicIdFactory(NAMESPACE_URL, "failed-runtime"),
    ).build(failing_profile)

    result = runtime.run_cycle()

    assert result.outcome is CycleExecutionOutcome.FAILED
    assert result.completed_waves == 2
    assert result.state.envelope.state_revision.value == 2
    assert runtime.state is result.state
    assert _available_value(runtime, SYNTHETIC_SOURCE_VALUE_KEY) == 2
    assert _available_value(runtime, SYNTHETIC_DOUBLE_VALUE_KEY) == 4
    assert _available_value(runtime, SYNTHETIC_TRIPLE_VALUE_KEY) == 6
    assert isinstance(runtime.state.read(SYNTHETIC_JOIN_VALUE_KEY).availability, Unknown)
