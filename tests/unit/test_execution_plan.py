"""Unit checks immutable execution plan compiler v0.1."""

from dataclasses import FrozenInstanceError, fields, replace
from typing import cast
from uuid import UUID

import pytest

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
from mindra.runtime import (
    DeterministicIdFactory,
    ExecutionDependency,
    ExecutionPlan,
    ExecutionPlanCompiler,
    ExecutionWave,
    PlanFingerprint,
)

NAMESPACE = UUID("9c582be5-97b0-449a-9694-472138275628")


def _key(owner: str, name: str = "value") -> StateKey[int]:
    return StateKey(StatePath.from_dotted(f"{owner}.{name}"))


def _read(
    key: StateKey[int],
    *,
    freshness: FreshnessMode = FreshnessMode.CURRENT_CYCLE,
    required: bool = True,
) -> ReadSpec[object]:
    return cast(
        ReadSpec[object],
        ReadSpec(
            key=key,
            required=required,
            allowed_availability=frozenset({Available}),
            freshness=freshness,
        ),
    )


def _descriptor(
    name: str,
    *,
    reads: tuple[ReadSpec[object], ...] = (),
    writes: tuple[StateKey[object], ...] = (),
    implementation_revision: str = "v1",
    determinism: DeterminismMode = DeterminismMode.DETERMINISTIC,
) -> ModuleDescriptor:
    return ModuleDescriptor(
        module_id=ModuleId(name),
        implementation_id=ImplementationId(f"reference.{name}.v1"),
        implementation_revision=ImplementationRevision(implementation_revision),
        reads=reads,
        writes=writes,
        private_state=None,
        phases=frozenset({ExecutionPhase.COGNITIVE_CYCLE}),
        traits=ExecutionTraits(
            statefulness=ModuleStatefulness.STATELESS,
            determinism=determinism,
        ),
    )


def _schema(*owners: str) -> StateSchema:
    specs = tuple(
        cast(
            StateFieldSpec[object],
            StateFieldSpec(
                key=_key(owner),
                owner=ModuleId(owner),
                value_contract=ValueContract(int),
            ),
        )
        for owner in owners
    )
    return StateSchema(SchemaRevision(7), specs)


def _compiler(seed: str = "plan") -> ExecutionPlanCompiler:
    return ExecutionPlanCompiler(DeterministicIdFactory(NAMESPACE, seed))


def _compile(
    descriptors: tuple[ModuleDescriptor, ...], schema: StateSchema, *, seed: str = "plan"
) -> ExecutionPlan:
    return _compiler(seed).compile(
        descriptors,
        schema,
        composition_revision=CompositionRevision(3),
        plan_revision=ExecutionPlanRevision(4),
    )


def test_linear_chain_has_one_module_per_wave() -> None:
    key_a, key_b, key_c = _key("a"), _key("b"), _key("c")
    descriptors = (
        _descriptor("a", writes=(cast(StateKey[object], key_a),)),
        _descriptor("b", reads=(_read(key_a),), writes=(cast(StateKey[object], key_b),)),
        _descriptor("c", reads=(_read(key_b),), writes=(cast(StateKey[object], key_c),)),
    )

    plan = _compile(descriptors, _schema("a", "b", "c"))

    assert tuple(wave.module_ids for wave in plan.waves) == (
        (ModuleId("a"),),
        (ModuleId("b"),),
        (ModuleId("c"),),
    )
    assert plan.dependencies == (
        ExecutionDependency(ModuleId("a"), ModuleId("b"), key_a.path),
        ExecutionDependency(ModuleId("b"), ModuleId("c"), key_b.path),
    )


def test_diamond_has_deterministic_fan_out_and_fan_in_waves() -> None:
    key_a, key_b, key_c = _key("a"), _key("b"), _key("c")
    descriptors = (
        _descriptor("a", writes=(cast(StateKey[object], key_a),)),
        _descriptor("b", reads=(_read(key_a),), writes=(cast(StateKey[object], key_b),)),
        _descriptor("c", reads=(_read(key_a),), writes=(cast(StateKey[object], key_c),)),
        _descriptor("d", reads=(_read(key_b), _read(key_c))),
    )

    plan = _compile(descriptors, _schema("a", "b", "c"))

    assert tuple(wave.module_ids for wave in plan.waves) == (
        (ModuleId("a"),),
        (ModuleId("b"), ModuleId("c")),
        (ModuleId("d"),),
    )


def test_independent_modules_share_one_canonical_ordered_wave() -> None:
    descriptors = (_descriptor("zeta"), _descriptor("alpha"), _descriptor("middle"))

    plan = _compile(descriptors, _schema())

    assert plan.waves == (
        ExecutionWave(0, (ModuleId("alpha"), ModuleId("middle"), ModuleId("zeta"))),
    )
    assert tuple(descriptor.module_id for descriptor in plan.descriptors) == (
        ModuleId("alpha"),
        ModuleId("middle"),
        ModuleId("zeta"),
    )


def test_empty_descriptor_set_produces_deterministic_empty_plan() -> None:
    first = _compile((), _schema(), seed="first")
    second = _compiler("second").compile(
        (),
        _schema(),
        composition_revision=CompositionRevision(99),
        plan_revision=ExecutionPlanRevision(100),
    )

    assert first.descriptors == ()
    assert first.dependencies == ()
    assert first.waves == ()
    assert second.descriptors == ()
    assert second.dependencies == ()
    assert second.waves == ()
    assert first.fingerprint == second.fingerprint
    assert first.plan_id != second.plan_id


def test_plan_fingerprint_has_exact_lowercase_sha256_shape() -> None:
    fingerprint = _compile((_descriptor("alpha"),), _schema()).fingerprint

    assert len(fingerprint.value) == 64
    assert fingerprint.value == fingerprint.value.lower()
    assert set(fingerprint.value) <= set("0123456789abcdef")
    with pytest.raises(ValueError):
        PlanFingerprint("A" * 64)


def test_plan_values_are_frozen_and_have_exact_shape() -> None:
    plan = _compile((_descriptor("alpha"),), _schema())
    wave = plan.waves[0]
    dependency = ExecutionDependency(
        producer=ModuleId("alpha"),
        consumer=ModuleId("beta"),
        path=_key("alpha").path,
    )

    assert {field.name for field in fields(ExecutionPlan)} == {
        "plan_id",
        "revision",
        "fingerprint",
        "composition_revision",
        "schema_revision",
        "phase",
        "descriptors",
        "dependencies",
        "waves",
    }
    assert {field.name for field in fields(ExecutionWave)} == {"index", "module_ids"}
    assert {field.name for field in fields(ExecutionDependency)} == {
        "producer",
        "consumer",
        "path",
    }
    plan_attribute = "waves"
    wave_attribute = "index"
    dependency_attribute = "path"
    with pytest.raises(FrozenInstanceError):
        setattr(plan, plan_attribute, ())
    with pytest.raises(FrozenInstanceError):
        setattr(wave, wave_attribute, 1)
    with pytest.raises(FrozenInstanceError):
        setattr(dependency, dependency_attribute, _key("beta").path)


def test_plan_contains_metadata_not_concrete_runtime_objects() -> None:
    plan = _compile((_descriptor("alpha"),), _schema())

    assert not hasattr(plan, "modules")
    assert not hasattr(plan, "registry")
    assert not hasattr(plan, "config")
    assert not hasattr(plan, "composition_root")


@pytest.mark.parametrize(
    "change",
    [
        "implementation_revision",
        "read",
        "write",
        "freshness",
        "trait",
    ],
)
def test_semantic_descriptor_change_changes_fingerprint(change: str) -> None:
    key_a, key_b = _key("a"), _key("b")
    schema = _schema("a", "b")
    source = _descriptor("a", writes=(cast(StateKey[object], key_a),))
    consumer = _descriptor("consumer", reads=(_read(key_a),))
    base = (source, consumer)
    changed = base
    if change == "implementation_revision":
        changed = (
            replace(source, implementation_revision=ImplementationRevision("v2")),
            consumer,
        )
    elif change == "read":
        changed = (
            source,
            replace(
                consumer,
                reads=(
                    _read(key_a),
                    _read(key_b, freshness=FreshnessMode.ANY_COMMITTED, required=False),
                ),
            ),
        )
    elif change == "write":
        changed_source = _descriptor("b", writes=(cast(StateKey[object], key_b),))
        changed_consumer = replace(consumer, reads=(_read(key_b),))
        changed = (changed_source, changed_consumer)
    elif change == "freshness":
        changed = (
            source,
            replace(
                consumer,
                reads=(_read(key_a, freshness=FreshnessMode.ANY_COMMITTED),),
            ),
        )
    else:
        changed = (
            replace(
                source,
                traits=ExecutionTraits(
                    statefulness=ModuleStatefulness.STATELESS,
                    determinism=DeterminismMode.STOCHASTIC,
                ),
            ),
            consumer,
        )

    assert _compile(base, schema).fingerprint != _compile(changed, schema).fingerprint
