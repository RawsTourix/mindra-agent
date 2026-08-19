"""Immutable hierarchical logical time Core Kernel."""

from dataclasses import dataclass
from uuid import UUID

from mindra.contracts.identity import (
    AgentSessionId,
    CognitiveCycleId,
    DecisionWindowId,
    EpisodeId,
    RunId,
    WaveId,
)


@dataclass(frozen=True, slots=True)
class LogicalTime:
    """Causal temporal envelope без wall-clock metadata."""

    run_id: RunId
    agent_session_id: AgentSessionId
    episode_id: EpisodeId | None = None
    decision_window_id: DecisionWindowId | None = None
    cognitive_cycle_id: CognitiveCycleId | None = None
    wave_id: WaveId | None = None

    def __post_init__(self) -> None:
        required_ids = (self.run_id, self.agent_session_id)
        if any(not isinstance(identity, UUID) for identity in required_ids):
            raise TypeError("Обязательные temporal identities должны быть UUID")

        optional_ids = (
            self.episode_id,
            self.decision_window_id,
            self.cognitive_cycle_id,
            self.wave_id,
        )
        if any(
            identity is not None and not isinstance(identity, UUID) for identity in optional_ids
        ):
            raise TypeError("Optional temporal identities должны быть UUID или None")

        hierarchy = (
            (self.decision_window_id, self.episode_id, "decision_window_id", "episode_id"),
            (
                self.cognitive_cycle_id,
                self.decision_window_id,
                "cognitive_cycle_id",
                "decision_window_id",
            ),
            (self.wave_id, self.cognitive_cycle_id, "wave_id", "cognitive_cycle_id"),
        )
        for child, parent, child_name, parent_name in hierarchy:
            if child is not None and parent is None:
                raise ValueError(f"{child_name} требует заданный {parent_name}")


TemporalContext = LogicalTime

__all__ = ["LogicalTime", "TemporalContext"]
