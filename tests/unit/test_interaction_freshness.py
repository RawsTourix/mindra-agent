"""Проверки episode/decision-window freshness без wall-clock semantics."""

from dataclasses import replace
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    AvailabilityError,
    Available,
    BranchId,
    CompositionRevision,
    DecisionWindowId,
    EpisodeId,
    FreshnessMode,
    LineageId,
    LogicalTime,
    ReadSpec,
    RunId,
    RuntimeBoundaryId,
    SchemaRevision,
    StateEntry,
    StateEnvelope,
    StateFieldSpec,
    StateKey,
    StatePath,
    StateProjection,
    StateProvenance,
    StateRevision,
    StateSchema,
    ValueContract,
)
from mindra.runtime import build_cognitive_state, build_state_projection

KEY = StateKey[int](StatePath.from_dotted("observation.current"))


def _time(*, episode: int = 3, window: int = 4) -> LogicalTime:
    return LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
        episode_id=EpisodeId(UUID(int=episode)),
        decision_window_id=DecisionWindowId(UUID(int=window)),
    )


def _projection(
    *, produced_at: LogicalTime, current: LogicalTime, mode: FreshnessMode
) -> StateProjection:
    schema = StateSchema(
        SchemaRevision.initial(),
        (
            cast(
                StateFieldSpec[object],
                StateFieldSpec(
                    key=KEY,
                    owner=RuntimeBoundaryId("runtime.interaction_ingress"),
                    value_contract=ValueContract(int),
                ),
            ),
        ),
    )
    state = build_cognitive_state(
        schema=schema,
        envelope=StateEnvelope(
            schema_revision=schema.revision,
            state_revision=StateRevision.initial(),
            parent_state_revision=None,
            lineage_id=LineageId(UUID(int=5)),
            branch_id=BranchId(UUID(int=6)),
            agent_revision_id=AgentRevisionId(UUID(int=7)),
            logical_time=current,
            composition_revision=CompositionRevision.initial(),
        ),
        entries={
            KEY.path: StateEntry(
                availability=Available(9),
                provenance=StateProvenance(
                    producer=RuntimeBoundaryId("runtime.interaction_ingress"),
                    base_state_revision=StateRevision.initial(),
                    logical_time=produced_at,
                ),
            )
        },
    )
    return build_state_projection(
        base_state=state,
        read_specs=(
            cast(
                ReadSpec[object],
                ReadSpec(
                    key=KEY,
                    required=True,
                    allowed_availability=frozenset({Available}),
                    freshness=mode,
                ),
            ),
        ),
        logical_time=current,
    )


def test_current_decision_window_accepts_matching_context() -> None:
    current = _time()

    assert _projection(
        produced_at=current,
        current=current,
        mode=FreshnessMode.CURRENT_DECISION_WINDOW,
    ).read(KEY).availability == Available(9)


@pytest.mark.parametrize(
    "produced_at",
    [
        replace(_time(), run_id=RunId(UUID(int=10))),
        replace(_time(), agent_session_id=AgentSessionId(UUID(int=20))),
        replace(_time(), episode_id=EpisodeId(UUID(int=30))),
        _time(window=40),
    ],
)
def test_current_decision_window_rejects_temporal_mismatch(
    produced_at: LogicalTime,
) -> None:
    projection = _projection(
        produced_at=produced_at,
        current=_time(),
        mode=FreshnessMode.CURRENT_DECISION_WINDOW,
    )

    with pytest.raises(AvailabilityError, match="decision window"):
        projection.read(KEY)


def test_current_episode_allows_another_window_in_same_episode() -> None:
    projection = _projection(
        produced_at=_time(window=40),
        current=_time(window=41),
        mode=FreshnessMode.CURRENT_EPISODE,
    )

    assert projection.read(KEY).availability == Available(9)


def test_current_episode_rejects_another_episode() -> None:
    projection = _projection(
        produced_at=_time(episode=30, window=40),
        current=_time(episode=31, window=41),
        mode=FreshnessMode.CURRENT_EPISODE,
    )

    with pytest.raises(AvailabilityError, match="episode"):
        projection.read(KEY)


@pytest.mark.parametrize(
    "mode",
    [FreshnessMode.CURRENT_DECISION_WINDOW, FreshnessMode.CURRENT_EPISODE],
)
def test_interaction_freshness_fails_closed_without_required_scope(
    mode: FreshnessMode,
) -> None:
    incomplete = LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
    )
    projection = _projection(produced_at=incomplete, current=incomplete, mode=mode)

    with pytest.raises(AvailabilityError):
        projection.read(KEY)
