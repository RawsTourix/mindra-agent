"""Contract checks atomic runtime-boundary CognitiveState publication."""

from dataclasses import replace
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    Available,
    BoundaryStateUpdate,
    BoundaryStateWrite,
    BranchId,
    CognitiveState,
    CommitValidationError,
    CompositionRevision,
    DecisionWindowId,
    EpisodeId,
    LineageId,
    LogicalTime,
    MissingFieldError,
    ModuleAttemptId,
    RunId,
    RuntimeBoundaryId,
    SchemaError,
    SchemaRevision,
    StaleProposalError,
    StateEntry,
    StateEnvelope,
    StateFieldSpec,
    StateKey,
    StatePath,
    StateProvenance,
    StateRevision,
    StateSchema,
    UnauthorizedWriteError,
    ValueContract,
)
from mindra.runtime import (
    BoundaryCommitCoordinator,
    DeterministicIdFactory,
    build_cognitive_state,
)

BOUNDARY_A = RuntimeBoundaryId("runtime.interaction_ingress")
BOUNDARY_B = RuntimeBoundaryId("runtime.action_boundary")
OBSERVATION = StateKey[int](StatePath.from_dotted("observation.current"))
OUTCOME = StateKey[int](StatePath.from_dotted("interaction.outcome"))
CAPABILITY = StateKey[int](StatePath.from_dotted("action.capability"))


def _time(*, window: int = 4) -> LogicalTime:
    return LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
        episode_id=EpisodeId(UUID(int=3)),
        decision_window_id=DecisionWindowId(UUID(int=window)),
    )


def _schema() -> StateSchema:
    return StateSchema(
        SchemaRevision.initial(),
        tuple(
            cast(
                StateFieldSpec[object],
                StateFieldSpec(key, owner, ValueContract(int)),
            )
            for key, owner in (
                (OBSERVATION, BOUNDARY_A),
                (OUTCOME, BOUNDARY_A),
                (CAPABILITY, BOUNDARY_B),
            )
        ),
    )


def _state(schema: StateSchema) -> CognitiveState:
    logical_time = _time(window=3)
    return build_cognitive_state(
        schema=schema,
        envelope=StateEnvelope(
            schema_revision=schema.revision,
            state_revision=StateRevision.initial(),
            parent_state_revision=None,
            lineage_id=LineageId(UUID(int=5)),
            branch_id=BranchId(UUID(int=6)),
            agent_revision_id=AgentRevisionId(UUID(int=7)),
            logical_time=logical_time,
            composition_revision=CompositionRevision.initial(),
        ),
        entries={
            key.path: StateEntry(
                availability=Available(index),
                provenance=StateProvenance(
                    producer=owner,
                    base_state_revision=StateRevision.initial(),
                    logical_time=logical_time,
                ),
            )
            for index, (key, owner) in enumerate(
                (
                    (OBSERVATION, BOUNDARY_A),
                    (OUTCOME, BOUNDARY_A),
                    (CAPABILITY, BOUNDARY_B),
                ),
                start=1,
            )
        },
    )


def _write(
    key: StateKey[int],
    value: object,
    *,
    producer: RuntimeBoundaryId = BOUNDARY_A,
    logical_time: LogicalTime | None = None,
    base: StateRevision | None = None,
) -> BoundaryStateWrite[object]:
    return cast(
        BoundaryStateWrite[object],
        BoundaryStateWrite(
            key=key,
            availability=Available(value),
            provenance=StateProvenance(
                producer=producer,
                base_state_revision=base or StateRevision.initial(),
                logical_time=logical_time or _time(),
            ),
        ),
    )


def _coordinator(
    schema: StateSchema, factory: DeterministicIdFactory | None = None
) -> BoundaryCommitCoordinator:
    return BoundaryCommitCoordinator(
        schema=schema,
        id_factory=factory or DeterministicIdFactory(UUID(int=8), "boundary-commit"),
    )


def test_boundary_commit_publishes_normal_revision_with_explicit_provenance() -> None:
    schema = _schema()
    state = _state(schema)
    logical_time = _time()
    update = BoundaryStateUpdate(
        base_state_revision=state.envelope.state_revision,
        producer=BOUNDARY_A,
        writes=(_write(OBSERVATION, 10, logical_time=logical_time),),
    )

    result = _coordinator(schema).commit(
        current_state=state,
        update=update,
        logical_time=logical_time,
    )

    assert result.state is not state
    assert result.state.envelope.state_revision == StateRevision(1)
    assert result.state.envelope.parent_state_revision == StateRevision.initial()
    assert result.state.envelope.logical_time == logical_time
    entry = result.state.read(OBSERVATION)
    assert entry.availability == Available(10)
    assert entry.provenance.producer == BOUNDARY_A
    assert entry.provenance.base_state_revision == StateRevision.initial()
    assert entry.provenance.logical_time == logical_time
    assert result.record.producer == BOUNDARY_A
    assert result.record.public_paths == (OBSERVATION.path,)


def test_boundary_a_cannot_write_boundary_b_owned_field() -> None:
    schema = _schema()
    update = BoundaryStateUpdate(
        StateRevision.initial(),
        BOUNDARY_A,
        (_write(CAPABILITY, 10),),
    )

    with pytest.raises(UnauthorizedWriteError, match="owner"):
        _coordinator(schema).commit(
            current_state=_state(schema),
            update=update,
            logical_time=_time(),
        )


def test_stale_base_revision_is_rejected() -> None:
    schema = _schema()
    update = BoundaryStateUpdate(
        StateRevision(1),
        BOUNDARY_A,
        (_write(OBSERVATION, 10, base=StateRevision(1)),),
    )

    with pytest.raises(StaleProposalError):
        _coordinator(schema).commit(
            current_state=_state(schema),
            update=update,
            logical_time=_time(),
        )


def test_duplicate_and_missing_boundary_paths_are_rejected() -> None:
    write = _write(OBSERVATION, 10)
    with pytest.raises(SchemaError, match="Duplicate StatePath"):
        BoundaryStateUpdate(StateRevision.initial(), BOUNDARY_A, (write, write))

    missing = replace(
        write,
        key=StateKey[int](StatePath.from_dotted("observation.missing")),
    )
    update = BoundaryStateUpdate(StateRevision.initial(), BOUNDARY_A, (missing,))
    schema = _schema()
    with pytest.raises(MissingFieldError):
        _coordinator(schema).commit(
            current_state=_state(schema),
            update=update,
            logical_time=_time(),
        )


def test_invalid_payload_prevents_all_publication_and_identity_allocation() -> None:
    schema = _schema()
    state = _state(schema)
    factory = DeterministicIdFactory(UUID(int=9), "atomic-boundary")
    update = BoundaryStateUpdate(
        StateRevision.initial(),
        BOUNDARY_A,
        (_write(OBSERVATION, 10), _write(OUTCOME, "invalid")),
    )

    with pytest.raises(SchemaError, match="Payload должен иметь тип int"):
        _coordinator(schema, factory).commit(
            current_state=state,
            update=update,
            logical_time=_time(),
        )

    assert factory.counter == 0
    assert state.envelope.state_revision == StateRevision.initial()
    assert state.read(OBSERVATION).availability == Available(1)
    assert state.read(OUTCOME).availability == Available(2)


@pytest.mark.parametrize(
    "provenance",
    [
        StateProvenance(BOUNDARY_B, StateRevision.initial(), _time()),
        StateProvenance(BOUNDARY_A, StateRevision(1), _time()),
        StateProvenance(BOUNDARY_A, StateRevision.initial(), _time(window=40)),
        StateProvenance(
            BOUNDARY_A,
            StateRevision.initial(),
            _time(),
            module_attempt_id=ModuleAttemptId(UUID(int=60)),
        ),
    ],
)
def test_boundary_provenance_mismatch_is_rejected(provenance: StateProvenance) -> None:
    schema = _schema()
    write = replace(_write(OBSERVATION, 10), provenance=provenance)
    update = BoundaryStateUpdate(StateRevision.initial(), BOUNDARY_A, (write,))

    with pytest.raises(CommitValidationError):
        _coordinator(schema).commit(
            current_state=_state(schema),
            update=update,
            logical_time=_time(),
        )


def test_boundary_commit_rejects_incompatible_run_or_session() -> None:
    schema = _schema()
    state = _state(schema)
    invalid_time = replace(_time(), run_id=RunId(UUID(int=50)))
    update = BoundaryStateUpdate(
        StateRevision.initial(),
        BOUNDARY_A,
        (_write(OBSERVATION, 10, logical_time=invalid_time),),
    )

    with pytest.raises(CommitValidationError, match="run_id"):
        _coordinator(schema).commit(
            current_state=state,
            update=update,
            logical_time=invalid_time,
        )
