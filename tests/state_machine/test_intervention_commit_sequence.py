"""State-machine sequence natural/intervention committed transitions."""

from pathlib import Path
from uuid import NAMESPACE_URL

import pytest

from mindra.composition import CompositionRoot, build_reference_registry, load_kernel_profile
from mindra.contracts import (
    CognitiveState,
    InterventionError,
    InterventionPolicy,
    StateInterventionSpec,
    StateInterventionWrite,
    StatePath,
)
from mindra.runtime import DeterministicIdFactory

SOURCE_PATH = StatePath.from_dotted("synthetic.source.value")


def _spec(state: CognitiveState, value: int) -> StateInterventionSpec:
    return StateInterventionSpec(
        state.envelope.state_revision,
        state.envelope.lineage_id,
        state.envelope.branch_id,
        (StateInterventionWrite(SOURCE_PATH, value),),
    )


def test_intervention_commit_sequence_rejects_stale_and_preserves_causal_state() -> None:
    runtime = CompositionRoot(
        registry=build_reference_registry(),
        id_factory=DeterministicIdFactory(NAMESPACE_URL, "intervention-sequence"),
        intervention_policy=InterventionPolicy.allowlist((SOURCE_PATH,)),
    ).build(load_kernel_profile(Path("configs/v0.1/reference.toml")))

    natural = runtime.run_cycle().state
    old_base_spec = _spec(natural, 7)
    first = runtime.apply_intervention(old_base_spec)
    assert first.state.envelope.state_revision == natural.envelope.state_revision.next()
    assert first.state.envelope.lineage_id != natural.envelope.lineage_id
    assert first.state.envelope.branch_id != natural.envelope.branch_id

    committed = runtime.state
    with pytest.raises(InterventionError):
        runtime.apply_intervention(old_base_spec)
    assert runtime.state is committed

    continued = runtime.run_cycle().state
    assert continued.envelope.lineage_id == first.state.envelope.lineage_id
    assert continued.envelope.branch_id == first.state.envelope.branch_id

    second = runtime.apply_intervention(_spec(continued, 11))
    assert second.state.envelope.state_revision == continued.envelope.state_revision.next()
    assert second.state.envelope.lineage_id != continued.envelope.lineage_id
    assert second.state.envelope.branch_id != continued.envelope.branch_id
