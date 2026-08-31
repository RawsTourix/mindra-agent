"""CompositionRoot initial state, plan, fingerprint и root evidence IS-13."""

from pathlib import Path
from uuid import NAMESPACE_URL

from mindra.composition import (
    CompositionRoot,
    KernelProfile,
    KernelRuntime,
    build_reference_registry,
    load_kernel_profile,
)
from mindra.contracts import (
    CompositionResolvedEvent,
    PlanCompiledEvent,
    ProfileId,
    RuntimeBoundaryId,
    Unknown,
)
from mindra.runtime import DeterministicIdFactory


def _build(profile: KernelProfile, *, seed: str = "composition") -> KernelRuntime:
    return CompositionRoot(
        registry=build_reference_registry(),
        id_factory=DeterministicIdFactory(NAMESPACE_URL, seed),
    ).build(profile)


def test_root_builds_schema_complete_revision_zero_state_and_exact_plan() -> None:
    runtime = _build(load_kernel_profile(Path("configs/v0.1/reference.toml")))

    assert tuple(path.dotted for path in runtime.state.entries) == (
        "synthetic.double.value",
        "synthetic.join.value",
        "synthetic.source.value",
        "synthetic.triple.value",
    )
    assert all(isinstance(entry.availability, Unknown) for entry in runtime.state.entries.values())
    assert all(
        entry.provenance.producer == RuntimeBoundaryId("composition.initial_state")
        for entry in runtime.state.entries.values()
    )
    envelope = runtime.state.envelope
    assert envelope.schema_revision.value == 0
    assert envelope.state_revision.value == 0
    assert envelope.parent_state_revision is None
    assert envelope.composition_revision.value == 0
    assert envelope.agent_revision_id == runtime.composition.agent_revision_id
    assert str(envelope.agent_revision_id) != runtime.composition.fingerprint
    assert envelope.logical_time.cognitive_cycle_id is None
    assert envelope.logical_time.wave_id is None

    assert tuple(
        tuple(module_id.value for module_id in wave.module_ids) for wave in runtime.plan.waves
    ) == (
        ("synthetic.source",),
        ("synthetic.double", "synthetic.triple"),
        ("synthetic.join",),
    )


def test_fingerprint_is_normalized_behavior_content() -> None:
    profile = load_kernel_profile(Path("configs/v0.1/reference.toml"))
    reversed_profile = KernelProfile(
        profile.schema, profile.profile_id, tuple(reversed(profile.modules))
    )
    renamed_profile = KernelProfile(profile.schema, ProfileId("renamed.profile"), profile.modules)
    source_changed = KernelProfile(
        profile.schema,
        profile.profile_id,
        tuple(
            type(item)(
                item.module_id,
                item.implementation_id,
                (("value", 3),) if item.module_id.value == "synthetic.source" else item.settings,
            )
            for item in profile.modules
        ),
    )

    first = _build(profile, seed="first").composition.fingerprint
    assert len(first) == 64 and first == first.lower()
    assert _build(reversed_profile, seed="second").composition.fingerprint == first
    assert _build(renamed_profile, seed="third").composition.fingerprint == first
    assert _build(source_changed, seed="fourth").composition.fingerprint != first


def test_root_evidence_exact_order_and_payload_mirrors_assembly() -> None:
    runtime = _build(load_kernel_profile(Path("configs/v0.1/reference.toml")))
    events = runtime.evidence_snapshot()

    assert tuple(event.kind.value for event in events) == (
        "composition_resolved",
        "plan_compiled",
    )
    assert all(event.physical_timestamp_ns is None for event in events)
    assert events[0].logical_time == runtime.state.envelope.logical_time
    composition = events[0].payload
    plan = events[1].payload
    assert isinstance(composition, CompositionResolvedEvent)
    assert composition.profile_id == runtime.profile.profile_id
    assert composition.composition_fingerprint == runtime.composition.fingerprint
    assert composition.agent_revision_id == runtime.composition.agent_revision_id
    assert isinstance(plan, PlanCompiledEvent)
    assert plan.plan_id == runtime.plan.plan_id
    assert plan.plan_fingerprint == runtime.plan.fingerprint.value
    assert plan.waves == tuple(
        type(plan.waves[0])(index=wave.index, module_ids=wave.module_ids)
        for wave in runtime.plan.waves
    )
