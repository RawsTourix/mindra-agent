"""Проверки immutable module descriptor и execution traits v0.1."""

from dataclasses import FrozenInstanceError, fields
from typing import cast

import pytest

from mindra.contracts import (
    Available,
    DeterminismMode,
    ExecutionPhase,
    ExecutionTraits,
    FreshnessMode,
    ImplementationId,
    ImplementationRevision,
    ModuleDescriptor,
    ModuleId,
    ModuleStatefulness,
    PrivateStateContract,
    PrivateStateDescriptor,
    ReadSpec,
    SchemaError,
    StateKey,
    StatePath,
    ValueContract,
)


def _key(name: str = "input") -> StateKey[int]:
    return StateKey(StatePath.from_dotted(f"synthetic.module.{name}"))


def _read(key: StateKey[int]) -> ReadSpec[int]:
    return ReadSpec(
        key=key,
        required=True,
        allowed_availability=frozenset({Available}),
        freshness=FreshnessMode.ANY_COMMITTED,
    )


def _descriptor(
    *,
    reads: tuple[ReadSpec[object], ...] = (),
    writes: tuple[StateKey[object], ...] = (),
    private_state: PrivateStateDescriptor[object] | None = None,
    statefulness: ModuleStatefulness = ModuleStatefulness.STATELESS,
    phases: frozenset[ExecutionPhase] = frozenset({ExecutionPhase.COGNITIVE_CYCLE}),
) -> ModuleDescriptor:
    return ModuleDescriptor(
        module_id=ModuleId("synthetic.module"),
        implementation_id=ImplementationId("reference.synthetic_module.v1"),
        implementation_revision=ImplementationRevision("v1.0.0"),
        reads=reads,
        writes=writes,
        private_state=private_state,
        phases=phases,
        traits=ExecutionTraits(
            statefulness=statefulness,
            determinism=DeterminismMode.DETERMINISTIC,
        ),
    )


def test_implementation_revision_is_opaque_equality_only_value() -> None:
    revision = ImplementationRevision("abc123")

    assert revision == ImplementationRevision("abc123")
    assert not hasattr(revision, "next")
    assert "__lt__" not in vars(ImplementationRevision)


@pytest.mark.parametrize("value", ["", " v1", "v1 ", "v 1", "v1\n"])
def test_implementation_revision_rejects_invalid_token(value: str) -> None:
    with pytest.raises(ValueError):
        ImplementationRevision(value)


def test_descriptor_is_immutable_and_has_exact_minimum_shape() -> None:
    descriptor = _descriptor()

    assert {field.name for field in fields(ModuleDescriptor)} == {
        "module_id",
        "implementation_id",
        "implementation_revision",
        "reads",
        "writes",
        "private_state",
        "phases",
        "traits",
    }
    module_id_attribute = "module_id"
    with pytest.raises(FrozenInstanceError):
        setattr(descriptor, module_id_attribute, ModuleId("synthetic.other"))


def test_descriptor_rejects_duplicate_read_paths() -> None:
    key = _key()
    reads = (
        cast(ReadSpec[object], _read(key)),
        cast(ReadSpec[object], _read(StateKey[int](key.path))),
    )

    with pytest.raises(SchemaError, match="Duplicate read StatePath"):
        _descriptor(reads=reads)


def test_descriptor_rejects_duplicate_write_paths() -> None:
    key = _key("output")
    writes = (cast(StateKey[object], key), cast(StateKey[object], StateKey[int](key.path)))

    with pytest.raises(SchemaError, match="Duplicate write StatePath"):
        _descriptor(writes=writes)


def test_descriptor_rejects_empty_or_unsupported_phases() -> None:
    with pytest.raises(ValueError, match="phases"):
        _descriptor(phases=frozenset())
    with pytest.raises(ValueError, match="COGNITIVE_CYCLE"):
        _descriptor(phases=cast(frozenset[ExecutionPhase], frozenset({"future_phase"})))


def test_descriptor_enforces_statefulness_private_descriptor_consistency() -> None:
    contract = ValueContract(int)
    private = cast(
        PrivateStateDescriptor[object],
        PrivateStateDescriptor(contract),
    )

    assert isinstance(contract, PrivateStateContract)
    with pytest.raises(ValueError, match="statefulness"):
        _descriptor(private_state=private)
    with pytest.raises(ValueError, match="statefulness"):
        _descriptor(statefulness=ModuleStatefulness.STATEFUL)

    descriptor = _descriptor(
        private_state=private,
        statefulness=ModuleStatefulness.STATEFUL,
    )
    assert descriptor.private_state is private


def test_descriptor_allows_read_write_overlap() -> None:
    key = _key()
    descriptor = _descriptor(
        reads=(cast(ReadSpec[object], _read(key)),),
        writes=(cast(StateKey[object], key),),
    )

    assert descriptor.reads[0].key.path == descriptor.writes[0].path


def test_execution_traits_contain_only_v01_fields_and_values() -> None:
    assert {field.name for field in fields(ExecutionTraits)} == {"statefulness", "determinism"}
    assert {phase.name for phase in ExecutionPhase} == {"COGNITIVE_CYCLE"}
    assert {trait.name for trait in ModuleStatefulness} == {"STATELESS", "STATEFUL"}
    assert {mode.name for mode in DeterminismMode} == {"DETERMINISTIC", "STOCHASTIC"}
