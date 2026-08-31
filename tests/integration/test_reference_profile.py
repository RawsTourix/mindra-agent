"""Full canonical reference profile vertical slice IS-15."""

from pathlib import Path
from uuid import NAMESPACE_URL

import pytest

from mindra.composition import CompositionRoot, build_reference_registry, load_kernel_profile
from mindra.contracts import (
    Available,
    InterventionError,
    StateInterventionSpec,
    StateInterventionWrite,
)
from mindra.reference import (
    SYNTHETIC_DOUBLE_VALUE_KEY,
    SYNTHETIC_JOIN_VALUE_KEY,
    SYNTHETIC_SOURCE_VALUE_KEY,
    SYNTHETIC_TRIPLE_VALUE_KEY,
)
from mindra.runtime import CycleExecutionOutcome, DeterministicIdFactory

PROFILE = Path("configs/v0.1/reference.toml")


def test_canonical_reference_profile_runs_one_exact_cycle() -> None:
    profile = load_kernel_profile(PROFILE)
    runtime = CompositionRoot(
        registry=build_reference_registry(),
        id_factory=DeterministicIdFactory(
            NAMESPACE_URL,
            "mindra.v0_1.kernel_smoke",
            counter=0,
        ),
    ).build(profile)

    assert tuple(
        tuple(module_id.value for module_id in wave.module_ids) for wave in runtime.plan.waves
    ) == (
        ("synthetic.source",),
        ("synthetic.double", "synthetic.triple"),
        ("synthetic.join",),
    )

    result = runtime.run_cycle()

    assert result.outcome is CycleExecutionOutcome.SUCCEEDED
    assert result.completed_waves == 3
    assert runtime.state is result.state
    assert runtime.state.envelope.state_revision.value == 3
    expected = (
        (SYNTHETIC_SOURCE_VALUE_KEY, 2),
        (SYNTHETIC_DOUBLE_VALUE_KEY, 4),
        (SYNTHETIC_TRIPLE_VALUE_KEY, 6),
        (SYNTHETIC_JOIN_VALUE_KEY, 10),
    )
    for key, value in expected:
        availability = runtime.state.read(key).availability
        assert isinstance(availability, Available)
        assert availability.value == value

    kinds = tuple(event.kind.value for event in runtime.evidence_snapshot())
    assert kinds[:2] == ("composition_resolved", "plan_compiled")
    assert kinds.count("cycle_started") == 1
    assert kinds.count("cycle_finished") == 1
    assert kinds.count("wave_started") == 3
    assert kinds.count("commit_attempted") == 3
    assert kinds.count("commit_succeeded") == 3
    assert kinds.count("state_revision_committed") == 3
    assert "commit_failed" not in kinds
    assert "cycle_failed" not in kinds
    assert "intervention_applied" not in kinds

    state = runtime.state
    disabled_spec = StateInterventionSpec(
        state.envelope.state_revision,
        state.envelope.lineage_id,
        state.envelope.branch_id,
        (StateInterventionWrite(SYNTHETIC_JOIN_VALUE_KEY.path, 11),),
    )
    with pytest.raises(InterventionError):
        runtime.apply_intervention(disabled_spec)
