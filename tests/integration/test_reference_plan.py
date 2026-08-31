"""Интеграционная проверка reference descriptors с existing planner."""

from itertools import permutations
from typing import cast
from uuid import UUID

from mindra.contracts import (
    CompositionRevision,
    ExecutionPlanRevision,
    ModuleDescriptor,
    ModuleId,
    SchemaRevision,
    StateFieldSpec,
    StateSchema,
    ValueContract,
)
from mindra.reference import (
    SYNTHETIC_DOUBLE_VALUE_KEY,
    SYNTHETIC_JOIN_VALUE_KEY,
    SYNTHETIC_SOURCE_VALUE_KEY,
    SYNTHETIC_TRIPLE_VALUE_KEY,
    SyntheticDoubleModule,
    SyntheticJoinModule,
    SyntheticSourceModule,
    SyntheticTripleModule,
)
from mindra.runtime import DeterministicIdFactory, ExecutionPlanCompiler

_EXPECTED_WAVES = (
    ("synthetic.source",),
    ("synthetic.double", "synthetic.triple"),
    ("synthetic.join",),
)


def _schema() -> StateSchema:
    fields = (
        (SYNTHETIC_SOURCE_VALUE_KEY, ModuleId("synthetic.source")),
        (SYNTHETIC_DOUBLE_VALUE_KEY, ModuleId("synthetic.double")),
        (SYNTHETIC_TRIPLE_VALUE_KEY, ModuleId("synthetic.triple")),
        (SYNTHETIC_JOIN_VALUE_KEY, ModuleId("synthetic.join")),
    )
    return StateSchema(
        SchemaRevision.initial(),
        tuple(
            cast(
                StateFieldSpec[object],
                StateFieldSpec(
                    key=key,
                    owner=owner,
                    value_contract=ValueContract(int),
                ),
            )
            for key, owner in fields
        ),
    )


def _descriptors() -> tuple[ModuleDescriptor, ...]:
    return (
        SyntheticSourceModule(value=2).descriptor,
        SyntheticDoubleModule().descriptor,
        SyntheticTripleModule().descriptor,
        SyntheticJoinModule().descriptor,
    )


def test_reference_graph_compiles_to_exact_waves_for_every_input_permutation() -> None:
    compiler = ExecutionPlanCompiler(DeterministicIdFactory(UUID(int=100), "reference-plan"))
    schema = _schema()

    for descriptor_order in permutations(_descriptors()):
        plan = compiler.compile(
            descriptor_order,
            schema,
            composition_revision=CompositionRevision.initial(),
            plan_revision=ExecutionPlanRevision.initial(),
        )
        assert (
            tuple(tuple(module_id.value for module_id in wave.module_ids) for wave in plan.waves)
            == _EXPECTED_WAVES
        )
