"""Проверки immutable state schema/entry/envelope/read primitives."""

from collections.abc import MutableMapping
from dataclasses import FrozenInstanceError
from enum import Enum
from typing import cast
from uuid import UUID

import pytest

import mindra.composition as composition_module
import mindra.runtime as runtime_module
from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    Available,
    BranchId,
    CompositionRevision,
    FreshnessMode,
    LineageId,
    LogicalTime,
    MissingFieldError,
    ModuleId,
    ReadSpec,
    RunId,
    RuntimeBoundaryId,
    SchemaError,
    SchemaRevision,
    Stale,
    StateEntry,
    StateEnvelope,
    StateFieldSpec,
    StateKey,
    StatePath,
    StateProvenance,
    StateRevision,
    StateSchema,
    Unavailable,
    Unknown,
    ValueContract,
)


def _key() -> StateKey[int]:
    return StateKey(StatePath.from_dotted("synthetic.source.value"))


def _field_spec() -> StateFieldSpec[int]:
    return StateFieldSpec(
        key=_key(),
        owner=ModuleId("synthetic.source"),
        value_contract=ValueContract(int),
    )


def _logical_time() -> LogicalTime:
    return LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
    )


def _mutable_enum_value() -> list[int]:
    return [1]


class MutableStateEntryEnum(Enum):
    """Enum с mutable payload для проверки StateEntry boundary."""

    VALUE = _mutable_enum_value()


def test_schema_lookup_preserves_explicit_owner_and_contract() -> None:
    spec = _field_spec()
    schema = StateSchema(SchemaRevision.initial(), (spec,))

    found = schema.lookup(spec.key)

    assert found is spec
    assert found.owner == ModuleId("synthetic.source")
    assert found.value_contract.freeze(4) == 4
    assert schema.fields == {spec.key.path: spec}


def test_schema_rejects_duplicate_state_path() -> None:
    first = _field_spec()
    duplicate = StateFieldSpec(
        key=StateKey[int](first.key.path),
        owner=ModuleId("synthetic.other"),
        value_contract=ValueContract(int),
    )

    with pytest.raises(SchemaError, match="Duplicate StatePath"):
        StateSchema(SchemaRevision.initial(), (first, duplicate))


def test_schema_is_immutable_after_compile() -> None:
    spec = _field_spec()
    schema = StateSchema(SchemaRevision.initial(), (spec,))
    revision_attribute = "revision"

    with pytest.raises(TypeError):
        cast(MutableMapping[StatePath, StateFieldSpec[object]], schema.fields)[
            StatePath.from_dotted("synthetic.other.value")
        ] = cast(StateFieldSpec[object], spec)
    with pytest.raises(FrozenInstanceError):
        setattr(schema, revision_attribute, SchemaRevision(1))


def test_schema_lookup_reports_structural_missing() -> None:
    schema = StateSchema(SchemaRevision.initial(), (_field_spec(),))

    with pytest.raises(MissingFieldError, match="отсутствует в active schema"):
        schema.lookup(StatePath.from_dotted("synthetic.missing.value"))


def test_state_entry_and_envelope_are_immutable_value_objects() -> None:
    provenance = StateProvenance(
        producer=RuntimeBoundaryId("runtime.initialization"),
        base_state_revision=StateRevision.initial(),
        logical_time=_logical_time(),
    )
    entry = StateEntry(availability=Available(3), provenance=provenance)
    envelope = StateEnvelope(
        schema_revision=SchemaRevision.initial(),
        state_revision=StateRevision.initial(),
        parent_state_revision=None,
        lineage_id=LineageId(UUID(int=3)),
        branch_id=BranchId(UUID(int=4)),
        agent_revision_id=AgentRevisionId(UUID(int=5)),
        logical_time=_logical_time(),
        composition_revision=CompositionRevision.initial(),
    )
    provenance_attribute = "provenance"
    state_revision_attribute = "state_revision"

    assert entry.availability == Available(3)
    assert envelope.parent_state_revision is None
    with pytest.raises(FrozenInstanceError):
        setattr(entry, provenance_attribute, provenance)
    with pytest.raises(FrozenInstanceError):
        setattr(envelope, state_revision_attribute, StateRevision(1))


def test_state_entry_rejects_mutable_canonical_payload() -> None:
    provenance = StateProvenance(
        producer=RuntimeBoundaryId("runtime.initialization"),
        base_state_revision=StateRevision.initial(),
        logical_time=_logical_time(),
    )

    with pytest.raises(SchemaError, match="snapshot-safe"):
        StateEntry(availability=Available([1]), provenance=provenance)


def test_state_entry_rejects_enum_with_mutable_underlying_value() -> None:
    provenance = StateProvenance(
        producer=RuntimeBoundaryId("runtime.initialization"),
        base_state_revision=StateRevision.initial(),
        logical_time=_logical_time(),
    )

    with pytest.raises(SchemaError, match="snapshot-safe"):
        StateEntry(
            availability=Available(MutableStateEntryEnum.VALUE),
            provenance=provenance,
        )


def test_read_spec_declares_only_current_v01_freshness_modes() -> None:
    read = ReadSpec(
        key=_key(),
        required=True,
        allowed_availability=frozenset({Available, Unknown}),
        freshness=FreshnessMode.CURRENT_CYCLE,
    )

    assert read.allowed_availability == frozenset({Available, Unknown})
    assert {mode.name for mode in FreshnessMode} == {"ANY_COMMITTED", "CURRENT_CYCLE"}
    assert not hasattr(read, "read")


def test_read_spec_rejects_mutable_or_unknown_availability_set() -> None:
    with pytest.raises(TypeError):
        ReadSpec(
            key=_key(),
            required=True,
            allowed_availability=cast(frozenset[type[Available[object]]], {Available}),
            freshness=FreshnessMode.ANY_COMMITTED,
        )
    with pytest.raises(ValueError):
        ReadSpec(
            key=_key(),
            required=True,
            allowed_availability=cast(frozenset[type[Available[object]]], frozenset({object})),
            freshness=FreshnessMode.ANY_COMMITTED,
        )


def test_schema_primitives_have_no_runtime_or_composition_dependencies() -> None:
    assert not hasattr(runtime_module, "StateSchema")
    assert not hasattr(composition_module, "StateSchema")
    assert Stale not in {Available, Unknown, Unavailable}
