"""Contract checks declared-read StateProjection boundary."""

from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    AvailabilityError,
    Available,
    BranchId,
    CognitiveCycleId,
    CognitiveState,
    CompositionRevision,
    DecisionWindowId,
    EpisodeId,
    FreshnessMetadata,
    FreshnessMode,
    LineageId,
    LogicalTime,
    MissingFieldError,
    ModuleId,
    ReadSpec,
    RunId,
    RuntimeBoundaryId,
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
    UndeclaredReadError,
    Unknown,
    ValueContract,
)
from mindra.runtime import build_cognitive_state, build_state_projection


def _key(name: str = "value") -> StateKey[int]:
    return StateKey(StatePath.from_dotted(f"synthetic.source.{name}"))


def _time(cycle: int, *, run: int = 1) -> LogicalTime:
    return LogicalTime(
        run_id=RunId(UUID(int=run)),
        agent_session_id=AgentSessionId(UUID(int=2)),
        episode_id=EpisodeId(UUID(int=3)),
        decision_window_id=DecisionWindowId(UUID(int=4)),
        cognitive_cycle_id=CognitiveCycleId(UUID(int=cycle)),
    )


def _schema(*keys: StateKey[int]) -> StateSchema:
    specs = tuple(
        cast(
            StateFieldSpec[object],
            StateFieldSpec(
                key=key,
                owner=ModuleId("synthetic.source"),
                value_contract=ValueContract(int),
            ),
        )
        for key in keys
    )
    return StateSchema(SchemaRevision.initial(), specs)


def _state(
    *,
    key: StateKey[int],
    availability: Available[int] | Unknown | Stale[int] | Unavailable,
    produced_cycle: int,
    current_cycle: int = 10,
    produced_run: int = 1,
    current_run: int = 1,
) -> CognitiveState:
    revision = StateRevision.initial()
    envelope = StateEnvelope(
        schema_revision=SchemaRevision.initial(),
        state_revision=revision,
        parent_state_revision=None,
        lineage_id=LineageId(UUID(int=5)),
        branch_id=BranchId(UUID(int=6)),
        agent_revision_id=AgentRevisionId(UUID(int=7)),
        logical_time=_time(current_cycle, run=current_run),
        composition_revision=CompositionRevision.initial(),
    )
    entry: StateEntry[object] = StateEntry(
        availability=availability,
        provenance=StateProvenance(
            producer=RuntimeBoundaryId("runtime.initialization"),
            base_state_revision=revision,
            logical_time=_time(produced_cycle, run=produced_run),
        ),
    )
    return build_cognitive_state(
        schema=_schema(key),
        envelope=envelope,
        entries={key.path: entry},
    )


def _read_spec(
    key: StateKey[int],
    *,
    allowed: frozenset[
        type[Available[object]] | type[Unknown] | type[Stale[object]] | type[Unavailable]
    ],
    freshness: FreshnessMode,
) -> ReadSpec[int]:
    return ReadSpec(
        key=key,
        required=True,
        allowed_availability=allowed,
        freshness=freshness,
    )


def test_projection_reads_declared_key_and_rejects_undeclared_key() -> None:
    key = _key()
    other = _key("other")
    state = _state(key=key, availability=Available(3), produced_cycle=10)
    projection = build_state_projection(
        base_state=state,
        read_specs=(
            cast(
                ReadSpec[object],
                _read_spec(
                    key,
                    allowed=frozenset({Available}),
                    freshness=FreshnessMode.ANY_COMMITTED,
                ),
            ),
        ),
    )

    assert projection.read(key).availability == Available(3)
    with pytest.raises(UndeclaredReadError):
        projection.read(other)


def test_projection_reports_missing_declared_key_structurally() -> None:
    key = _key()
    state = build_cognitive_state(
        schema=_schema(key),
        envelope=_state(key=key, availability=Unknown(), produced_cycle=10).envelope,
        entries={},
    )
    projection = build_state_projection(
        base_state=state,
        read_specs=(
            cast(
                ReadSpec[object],
                _read_spec(
                    key,
                    allowed=frozenset({Unknown}),
                    freshness=FreshnessMode.ANY_COMMITTED,
                ),
            ),
        ),
    )

    with pytest.raises(MissingFieldError):
        projection.read(key)


@pytest.mark.parametrize("availability", [Unknown(), Unavailable()])
def test_projection_keeps_unknown_and_unavailable_distinct(
    availability: Unknown | Unavailable,
) -> None:
    key = _key()
    state = _state(key=key, availability=availability, produced_cycle=10)
    allowed = frozenset({type(availability)})
    projection = build_state_projection(
        base_state=state,
        read_specs=(
            cast(
                ReadSpec[object],
                _read_spec(
                    key,
                    allowed=cast(
                        frozenset[
                            type[Available[object]]
                            | type[Unknown]
                            | type[Stale[object]]
                            | type[Unavailable]
                        ],
                        allowed,
                    ),
                    freshness=FreshnessMode.ANY_COMMITTED,
                ),
            ),
        ),
    )

    assert type(projection.read(key).availability) is type(availability)


def test_projection_rejects_disallowed_availability() -> None:
    key = _key()
    state = _state(key=key, availability=Unavailable(), produced_cycle=10)
    projection = build_state_projection(
        base_state=state,
        read_specs=(
            cast(
                ReadSpec[object],
                _read_spec(
                    key,
                    allowed=frozenset({Available}),
                    freshness=FreshnessMode.ANY_COMMITTED,
                ),
            ),
        ),
    )

    with pytest.raises(AvailabilityError, match="Unavailable"):
        projection.read(key)


def test_current_cycle_accepts_current_and_rejects_previous_provenance() -> None:
    key = _key()
    read = cast(
        ReadSpec[object],
        _read_spec(
            key,
            allowed=frozenset({Available}),
            freshness=FreshnessMode.CURRENT_CYCLE,
        ),
    )
    current_state = _state(key=key, availability=Available(3), produced_cycle=10)
    previous_state = _state(key=key, availability=Available(3), produced_cycle=9)

    assert build_state_projection(base_state=current_state, read_specs=(read,)).read(
        key
    ).availability == Available(3)
    with pytest.raises(AvailabilityError, match="текущем cognitive cycle"):
        build_state_projection(base_state=previous_state, read_specs=(read,)).read(key)


def test_current_cycle_rejects_same_cycle_identity_from_other_run_context() -> None:
    key = _key()
    state = _state(
        key=key,
        availability=Available(3),
        produced_cycle=10,
        produced_run=8,
    )
    read = cast(
        ReadSpec[object],
        _read_spec(
            key,
            allowed=frozenset({Available}),
            freshness=FreshnessMode.CURRENT_CYCLE,
        ),
    )

    with pytest.raises(AvailabilityError, match="текущем cognitive cycle"):
        build_state_projection(base_state=state, read_specs=(read,)).read(key)


def test_any_committed_accepts_value_from_previous_cycle() -> None:
    key = _key()
    state = _state(key=key, availability=Available(3), produced_cycle=9)
    projection = build_state_projection(
        base_state=state,
        read_specs=(
            cast(
                ReadSpec[object],
                _read_spec(
                    key,
                    allowed=frozenset({Available}),
                    freshness=FreshnessMode.ANY_COMMITTED,
                ),
            ),
        ),
    )

    assert projection.read(key).availability == Available(3)


def test_stale_obeys_availability_and_current_cycle_checks() -> None:
    key = _key()
    stale = Stale(
        value=3,
        freshness=FreshnessMetadata(
            produced_at=_time(8),
            based_on_state_revision=StateRevision.initial(),
        ),
    )
    state = _state(key=key, availability=stale, produced_cycle=10)
    allowed_read = cast(
        ReadSpec[object],
        _read_spec(
            key,
            allowed=frozenset({Stale}),
            freshness=FreshnessMode.CURRENT_CYCLE,
        ),
    )

    assert isinstance(
        build_state_projection(base_state=state, read_specs=(allowed_read,)).read(key).availability,
        Stale,
    )


def test_projection_does_not_expose_full_state_or_mapping() -> None:
    key = _key()
    state = _state(key=key, availability=Available(3), produced_cycle=10)
    projection = build_state_projection(
        base_state=state,
        read_specs=(
            cast(
                ReadSpec[object],
                _read_spec(
                    key,
                    allowed=frozenset({Available}),
                    freshness=FreshnessMode.ANY_COMMITTED,
                ),
            ),
        ),
    )

    assert not hasattr(projection, "entries")
    assert not hasattr(projection, "envelope")
    assert not hasattr(projection, "state")
