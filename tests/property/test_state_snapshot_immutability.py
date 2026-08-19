"""Property checks последовательных immutable state snapshots."""

from typing import cast
from uuid import UUID

from hypothesis import given
from hypothesis import strategies as st

from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    Available,
    BranchId,
    CompositionRevision,
    LineageId,
    LogicalTime,
    ModuleId,
    RunId,
    RuntimeBoundaryId,
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

KEY = StateKey[int](StatePath.from_dotted("synthetic.source.value"))
LOGICAL_TIME = LogicalTime(
    run_id=RunId(UUID(int=1)),
    agent_session_id=AgentSessionId(UUID(int=2)),
)


def _schema() -> StateSchema:
    spec = cast(
        StateFieldSpec[object],
        StateFieldSpec(
            key=KEY,
            owner=ModuleId("synthetic.source"),
            value_contract=ValueContract(int),
        ),
    )
    return StateSchema(SchemaRevision.initial(), (spec,))


def _envelope(revision: StateRevision, parent: StateRevision | None) -> StateEnvelope:
    return StateEnvelope(
        schema_revision=SchemaRevision.initial(),
        state_revision=revision,
        parent_state_revision=parent,
        lineage_id=LineageId(UUID(int=3)),
        branch_id=BranchId(UUID(int=4)),
        agent_revision_id=AgentRevisionId(UUID(int=5)),
        logical_time=LOGICAL_TIME,
        composition_revision=CompositionRevision.initial(),
    )


def _entry(value: int, revision: StateRevision) -> StateEntry[object]:
    return StateEntry(
        availability=Available(value),
        provenance=StateProvenance(
            producer=RuntimeBoundaryId("runtime.initialization"),
            base_state_revision=revision,
            logical_time=LOGICAL_TIME,
        ),
    )


@given(st.lists(st.integers(), min_size=1, max_size=20))
def test_snapshot_sequence_never_mutates_older_snapshots(values: list[int]) -> None:
    schema = _schema()
    revision = StateRevision.initial()
    state = build_cognitive_state(
        schema=schema,
        envelope=_envelope(revision, None),
        entries={KEY.path: _entry(values[0], revision)},
    )
    snapshots = [(state, values[0])]

    for value in values[1:]:
        next_revision = revision.next()
        state = copy_cognitive_state(
            base_state=state,
            schema=schema,
            envelope=_envelope(next_revision, revision),
            replacements={KEY.path: _entry(value, revision)},
        )
        revision = next_revision
        snapshots.append((state, value))

    assert [snapshot.read(KEY).availability for snapshot, _ in snapshots] == [
        Available(value) for _, value in snapshots
    ]


@given(st.integers(), st.integers())
def test_input_mapping_mutation_cannot_change_committed_state(
    committed_value: int, replacement_value: int
) -> None:
    revision = StateRevision.initial()
    source = {KEY.path: _entry(committed_value, revision)}
    state = build_cognitive_state(
        schema=_schema(),
        envelope=_envelope(revision, None),
        entries=source,
    )

    source[KEY.path] = _entry(replacement_value, revision)

    assert state.read(KEY).availability == Available(committed_value)
