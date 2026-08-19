"""Property checks deterministic execution DAG decomposition."""

from itertools import permutations
from typing import cast
from uuid import UUID

from hypothesis import given
from hypothesis import strategies as st

from mindra.contracts import (
    Available,
    CompositionRevision,
    DeterminismMode,
    ExecutionPhase,
    ExecutionPlanRevision,
    ExecutionTraits,
    FreshnessMode,
    ImplementationId,
    ImplementationRevision,
    ModuleDescriptor,
    ModuleId,
    ModuleStatefulness,
    ReadSpec,
    SchemaRevision,
    StateFieldSpec,
    StateKey,
    StatePath,
    StateSchema,
    ValueContract,
)
from mindra.runtime import DeterministicIdFactory, ExecutionPlan, ExecutionPlanCompiler

NAMESPACE = UUID("1c7d7bf4-12ee-438d-ac8e-d4ff9a89355a")


def _key(name: str) -> StateKey[int]:
    return StateKey(StatePath.from_dotted(f"{name}.value"))


def _descriptor(name: str, predecessor: str | None) -> ModuleDescriptor:
    reads: tuple[ReadSpec[object], ...] = ()
    if predecessor is not None:
        reads = (
            cast(
                ReadSpec[object],
                ReadSpec(
                    key=_key(predecessor),
                    required=True,
                    allowed_availability=frozenset({Available}),
                    freshness=FreshnessMode.CURRENT_CYCLE,
                ),
            ),
        )
    return ModuleDescriptor(
        module_id=ModuleId(name),
        implementation_id=ImplementationId(f"reference.{name}.v1"),
        implementation_revision=ImplementationRevision("v1"),
        reads=reads,
        writes=(cast(StateKey[object], _key(name)),),
        private_state=None,
        phases=frozenset({ExecutionPhase.COGNITIVE_CYCLE}),
        traits=ExecutionTraits(
            statefulness=ModuleStatefulness.STATELESS,
            determinism=DeterminismMode.DETERMINISTIC,
        ),
    )


def _schema(names: tuple[str, ...]) -> StateSchema:
    return StateSchema(
        SchemaRevision.initial(),
        tuple(
            cast(
                StateFieldSpec[object],
                StateFieldSpec(
                    key=_key(name),
                    owner=ModuleId(name),
                    value_contract=ValueContract(int),
                ),
            )
            for name in names
        ),
    )


def _compile(descriptors: tuple[ModuleDescriptor, ...]) -> ExecutionPlan:
    return ExecutionPlanCompiler(DeterministicIdFactory(NAMESPACE, "property")).compile(
        descriptors,
        _schema(tuple(descriptor.module_id.value for descriptor in descriptors)),
        composition_revision=CompositionRevision.initial(),
        plan_revision=ExecutionPlanRevision.initial(),
    )


def test_every_permutation_has_identical_dependencies_waves_and_fingerprint() -> None:
    descriptors = (
        _descriptor("a", None),
        _descriptor("b", "a"),
        _descriptor("c", "a"),
        _descriptor("d", "b"),
    )
    expected = _compile(descriptors)

    for permutation in permutations(descriptors):
        actual = _compile(permutation)
        assert actual.dependencies == expected.dependencies
        assert actual.waves == expected.waves
        assert actual.fingerprint == expected.fingerprint


@given(st.integers(min_value=0, max_value=12))
def test_independent_modules_always_form_one_canonical_wave(module_count: int) -> None:
    names = tuple(f"module_{index:02d}" for index in reversed(range(module_count)))
    plan = _compile(tuple(_descriptor(name, None) for name in names))

    if not names:
        assert plan.waves == ()
    else:
        assert len(plan.waves) == 1
        assert plan.waves[0].module_ids == tuple(ModuleId(name) for name in sorted(names))
