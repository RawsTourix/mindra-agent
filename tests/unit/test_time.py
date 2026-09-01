"""Проверки immutable hierarchical logical time."""

from dataclasses import FrozenInstanceError
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentSessionId,
    CognitiveCycleId,
    DecisionWindowId,
    EpisodeId,
    LogicalTime,
    RunId,
    TemporalContext,
    WaveId,
)


def _uuid(value: int) -> UUID:
    return UUID(int=value)


def test_logical_time_carries_complete_hierarchy() -> None:
    logical_time = LogicalTime(
        run_id=RunId(_uuid(1)),
        agent_session_id=AgentSessionId(_uuid(2)),
        episode_id=EpisodeId(_uuid(3)),
        decision_window_id=DecisionWindowId(_uuid(4)),
        cognitive_cycle_id=CognitiveCycleId(_uuid(5)),
        wave_id=WaveId(_uuid(6)),
    )

    assert isinstance(logical_time, TemporalContext)
    assert logical_time.wave_id == WaveId(_uuid(6))
    assert not hasattr(logical_time, "timestamp")
    assert not hasattr(logical_time, "wall_clock")


def test_downstream_scopes_may_be_absent() -> None:
    logical_time = LogicalTime(
        run_id=RunId(_uuid(1)),
        agent_session_id=AgentSessionId(_uuid(2)),
    )

    assert logical_time.episode_id is None
    assert logical_time.decision_window_id is None
    assert logical_time.cognitive_cycle_id is None
    assert logical_time.wave_id is None


@pytest.mark.parametrize(
    "overrides",
    [
        {"decision_window_id": DecisionWindowId(_uuid(4))},
        {
            "episode_id": EpisodeId(_uuid(3)),
            "cognitive_cycle_id": CognitiveCycleId(_uuid(5)),
        },
    ],
)
def test_logical_time_rejects_hierarchy_gaps(overrides: dict[str, UUID]) -> None:
    with pytest.raises(ValueError):
        LogicalTime(
            run_id=RunId(_uuid(1)),
            agent_session_id=AgentSessionId(_uuid(2)),
            episode_id=cast(EpisodeId | None, overrides.get("episode_id")),
            decision_window_id=cast(DecisionWindowId | None, overrides.get("decision_window_id")),
            cognitive_cycle_id=cast(CognitiveCycleId | None, overrides.get("cognitive_cycle_id")),
            wave_id=cast(WaveId | None, overrides.get("wave_id")),
        )


def test_logical_time_is_frozen() -> None:
    logical_time = LogicalTime(
        run_id=RunId(_uuid(1)),
        agent_session_id=AgentSessionId(_uuid(2)),
    )
    episode_attribute = "episode_id"

    with pytest.raises(FrozenInstanceError):
        setattr(logical_time, episode_attribute, EpisodeId(_uuid(3)))


def test_logical_time_rejects_non_uuid_at_runtime() -> None:
    with pytest.raises(TypeError):
        LogicalTime(
            run_id=cast(RunId, "not-a-uuid"),
            agent_session_id=AgentSessionId(_uuid(2)),
        )
