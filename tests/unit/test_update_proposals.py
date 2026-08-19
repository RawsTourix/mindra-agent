"""Проверки immutable staged public/private proposals."""

from dataclasses import FrozenInstanceError
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
    ModuleAttemptId,
    ModuleId,
    PrivateStateProposal,
    PrivateStateRevision,
    PrivateStateSnapshot,
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
    StateUpdateProposal,
    StateWrite,
    ValueContract,
)
from mindra.runtime import build_cognitive_state


def _logical_time() -> LogicalTime:
    return LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
    )


def _key() -> StateKey[int]:
    return StateKey(StatePath.from_dotted("synthetic.module.value"))


def _provenance() -> StateProvenance:
    return StateProvenance(
        producer=ModuleId("synthetic.module"),
        base_state_revision=StateRevision.initial(),
        module_attempt_id=ModuleAttemptId(UUID(int=3)),
        logical_time=_logical_time(),
    )


def _write(value: int = 2) -> StateWrite[int]:
    return StateWrite(key=_key(), availability=Available(value), provenance=_provenance())


def _proposal(*writes: StateWrite[object]) -> StateUpdateProposal:
    return StateUpdateProposal(
        base_state_revision=StateRevision.initial(),
        producer=ModuleId("synthetic.module"),
        module_attempt_id=ModuleAttemptId(UUID(int=3)),
        writes=writes,
    )


def _base_state() -> CognitiveState:
    key = _key()
    schema = StateSchema(
        SchemaRevision.initial(),
        (
            cast(
                StateFieldSpec[object],
                StateFieldSpec(
                    key=key,
                    owner=ModuleId("synthetic.module"),
                    value_contract=ValueContract(int),
                ),
            ),
        ),
    )
    envelope = StateEnvelope(
        schema_revision=SchemaRevision.initial(),
        state_revision=StateRevision.initial(),
        parent_state_revision=None,
        lineage_id=LineageId(UUID(int=4)),
        branch_id=BranchId(UUID(int=5)),
        agent_revision_id=AgentRevisionId(UUID(int=6)),
        logical_time=_logical_time(),
        composition_revision=CompositionRevision.initial(),
    )
    return build_cognitive_state(
        schema=schema,
        envelope=envelope,
        entries={
            key.path: StateEntry(
                availability=Available(1),
                provenance=StateProvenance(
                    producer=RuntimeBoundaryId("runtime.initialization"),
                    base_state_revision=StateRevision.initial(),
                    logical_time=_logical_time(),
                ),
            )
        },
    )


def test_state_write_and_update_proposal_are_immutable() -> None:
    write = _write()
    proposal = _proposal(cast(StateWrite[object], write))
    availability_attribute = "availability"
    writes_attribute = "writes"

    with pytest.raises(FrozenInstanceError):
        setattr(write, availability_attribute, Available(4))
    with pytest.raises(FrozenInstanceError):
        setattr(proposal, writes_attribute, ())


def test_state_update_proposal_rejects_duplicate_write_path() -> None:
    first = cast(StateWrite[object], _write(2))
    second = cast(
        StateWrite[object],
        StateWrite(
            key=StateKey[int](_key().path),
            availability=Available(3),
            provenance=_provenance(),
        ),
    )

    with pytest.raises(SchemaError, match="Duplicate StatePath"):
        _proposal(first, second)


def test_proposal_creation_does_not_mutate_base_cognitive_state() -> None:
    base_state = _base_state()
    before = base_state.read(_key())

    proposal = _proposal(cast(StateWrite[object], _write(9)))

    assert proposal.writes[0].availability == Available(9)
    assert base_state.read(_key()) is before
    assert base_state.read(_key()).availability == Available(1)
    assert not hasattr(proposal, "commit")


def test_state_write_rejects_non_snapshot_safe_payload() -> None:
    with pytest.raises(SchemaError, match="snapshot-safe"):
        StateWrite(
            key=StateKey[list[int]](_key().path),
            availability=Available([1]),
            provenance=_provenance(),
        )


def test_private_snapshot_and_proposal_are_immutable_and_revision_pinned() -> None:
    module_id = ModuleId("synthetic.module")
    attempt_id = ModuleAttemptId(UUID(int=3))
    snapshot = PrivateStateSnapshot(
        module_id=module_id,
        revision=PrivateStateRevision(4),
        value=7,
    )
    proposal = PrivateStateProposal(
        module_id=module_id,
        base_revision=snapshot.revision,
        module_attempt_id=attempt_id,
        value=8,
    )

    assert proposal.base_revision == PrivateStateRevision(4)
    assert proposal.value == 8
    assert not hasattr(proposal, "commit")
    value_attribute = "value"
    with pytest.raises(FrozenInstanceError):
        setattr(snapshot, value_attribute, 10)
    with pytest.raises(FrozenInstanceError):
        setattr(proposal, value_attribute, 10)
