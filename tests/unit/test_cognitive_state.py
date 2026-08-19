"""Проверки committed CognitiveState и copy-on-commit construction."""

from collections.abc import MutableMapping
from enum import Enum
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    Available,
    BranchId,
    CognitiveState,
    CompositionRevision,
    LineageId,
    LogicalTime,
    MissingFieldError,
    ModuleId,
    RunId,
    RuntimeBoundaryId,
    SchemaError,
    SchemaRevision,
    StateEntry,
    StateEnvelope,
    StateFieldSpec,
    StateKey,
    StatePath,
    StateProvenance,
    StateRevision,
    StateSchema,
    ValueContract,
)
from mindra.runtime import build_cognitive_state, copy_cognitive_state


class SafeEnum(Enum):
    """Snapshot-safe Enum regression fixture IS-04."""

    VALUE = ("safe", 1)


def _key() -> StateKey[int]:
    return StateKey(StatePath.from_dotted("synthetic.source.value"))


def _schema() -> StateSchema:
    spec: StateFieldSpec[object] = cast(
        StateFieldSpec[object],
        StateFieldSpec(
            key=_key(),
            owner=ModuleId("synthetic.source"),
            value_contract=ValueContract(int),
        ),
    )
    return StateSchema(SchemaRevision.initial(), (spec,))


def _logical_time() -> LogicalTime:
    return LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
    )


def _envelope(revision: StateRevision, parent: StateRevision | None) -> StateEnvelope:
    return StateEnvelope(
        schema_revision=SchemaRevision.initial(),
        state_revision=revision,
        parent_state_revision=parent,
        lineage_id=LineageId(UUID(int=3)),
        branch_id=BranchId(UUID(int=4)),
        agent_revision_id=AgentRevisionId(UUID(int=5)),
        logical_time=_logical_time(),
        composition_revision=CompositionRevision.initial(),
    )


def _entry(value: object, revision: StateRevision) -> StateEntry[object]:
    return StateEntry(
        availability=Available(value),
        provenance=StateProvenance(
            producer=RuntimeBoundaryId("runtime.initialization"),
            base_state_revision=revision,
            logical_time=_logical_time(),
        ),
    )


def test_cognitive_state_exposes_read_only_copied_mapping() -> None:
    key = _key()
    source = {key.path: _entry(3, StateRevision.initial())}
    state = build_cognitive_state(
        schema=_schema(),
        envelope=_envelope(StateRevision.initial(), None),
        entries=source,
    )

    source[key.path] = _entry(9, StateRevision.initial())

    assert state.read(key).availability == Available(3)
    assert state.entries[key.path].availability == Available(3)
    with pytest.raises(TypeError):
        cast(MutableMapping[StatePath, StateEntry[object]], state.entries)[key.path] = _entry(
            7, StateRevision.initial()
        )


def test_copy_on_commit_builds_new_snapshot_without_mutating_base() -> None:
    key = _key()
    base_revision = StateRevision.initial()
    base = build_cognitive_state(
        schema=_schema(),
        envelope=_envelope(base_revision, None),
        entries={key.path: _entry(2, base_revision)},
    )
    next_revision = base_revision.next()

    current = copy_cognitive_state(
        base_state=base,
        schema=_schema(),
        envelope=_envelope(next_revision, base_revision),
        replacements={key.path: _entry(4, base_revision)},
    )

    assert base.read(key).availability == Available(2)
    assert current.read(key).availability == Available(4)
    assert current.envelope.parent_state_revision == base_revision


def test_cognitive_state_reports_structural_missing() -> None:
    state = build_cognitive_state(
        schema=_schema(),
        envelope=_envelope(StateRevision.initial(), None),
        entries={},
    )

    with pytest.raises(MissingFieldError, match="committed CognitiveState"):
        state.read(_key())


def test_state_construction_applies_schema_value_contract() -> None:
    key = _key()

    with pytest.raises(SchemaError, match="Payload должен иметь тип int"):
        build_cognitive_state(
            schema=_schema(),
            envelope=_envelope(StateRevision.initial(), None),
            entries={key.path: _entry("wrong", StateRevision.initial())},
        )


def test_state_construction_rejects_mutable_and_nested_mutable_payload() -> None:
    revision = StateRevision.initial()
    provenance = StateProvenance(
        producer=RuntimeBoundaryId("runtime.initialization"),
        base_state_revision=revision,
        logical_time=_logical_time(),
    )

    with pytest.raises(SchemaError, match="snapshot-safe"):
        StateEntry(availability=Available([1]), provenance=provenance)
    with pytest.raises(SchemaError, match="snapshot-safe"):
        StateEntry(availability=Available(("unsafe", [1])), provenance=provenance)


def test_state_construction_preserves_safe_enum_correction() -> None:
    key = StateKey[SafeEnum](StatePath.from_dotted("synthetic.source.mode"))
    spec: StateFieldSpec[object] = cast(
        StateFieldSpec[object],
        StateFieldSpec(
            key=key,
            owner=ModuleId("synthetic.source"),
            value_contract=ValueContract(SafeEnum),
        ),
    )
    schema = StateSchema(SchemaRevision.initial(), (spec,))
    entry = _entry(SafeEnum.VALUE, StateRevision.initial())

    state = build_cognitive_state(
        schema=schema,
        envelope=_envelope(StateRevision.initial(), None),
        entries={key.path: entry},
    )

    assert state.read(key).availability == Available(SafeEnum.VALUE)
    assert isinstance(state, CognitiveState)
