"""Типизированные causal и semantic identities Core Kernel."""

from dataclasses import dataclass
from re import compile as compile_pattern
from typing import NewType, Protocol, TypeVar
from uuid import UUID

RunId = NewType("RunId", UUID)
AgentSessionId = NewType("AgentSessionId", UUID)
EpisodeId = NewType("EpisodeId", UUID)
DecisionWindowId = NewType("DecisionWindowId", UUID)
CognitiveCycleId = NewType("CognitiveCycleId", UUID)
ExecutionPlanId = NewType("ExecutionPlanId", UUID)
WaveId = NewType("WaveId", UUID)
WaveAttemptId = NewType("WaveAttemptId", UUID)
ModuleAttemptId = NewType("ModuleAttemptId", UUID)
CommitId = NewType("CommitId", UUID)
InterventionId = NewType("InterventionId", UUID)
LineageId = NewType("LineageId", UUID)
BranchId = NewType("BranchId", UUID)
AgentRevisionId = NewType("AgentRevisionId", UUID)
ObservationId = NewType("ObservationId", UUID)
PerceptId = NewType("PerceptId", UUID)
ExternalTaskId = NewType("ExternalTaskId", UUID)
GoalProposalId = NewType("GoalProposalId", UUID)
GoalId = NewType("GoalId", UUID)
ActionIntentId = NewType("ActionIntentId", UUID)
AuthorizedActionId = NewType("AuthorizedActionId", UUID)
ActionCommitId = NewType("ActionCommitId", UUID)
DispatchId = NewType("DispatchId", UUID)
DispatchAttemptId = NewType("DispatchAttemptId", UUID)
EnvironmentTransitionId = NewType("EnvironmentTransitionId", UUID)
OutcomeId = NewType("OutcomeId", UUID)
ExperienceEventId = NewType("ExperienceEventId", UUID)
JournalId = NewType("JournalId", UUID)
EnvironmentSnapshotId = NewType("EnvironmentSnapshotId", UUID)
WorldInstanceId = NewType("WorldInstanceId", UUID)

IdentityT = TypeVar("IdentityT", bound=UUID, covariant=True)


class IdentityType(Protocol[IdentityT]):
    """Конструктор конкретного UUID identity-типа."""

    __name__: str

    def __call__(self, value: UUID, /) -> IdentityT:
        """Обернуть UUID в конкретный статический identity-тип."""
        ...


class IdFactory(Protocol):
    """Injected boundary создания causal UUID identities."""

    def new_id(self, identity_type: IdentityType[IdentityT], /) -> IdentityT:
        """Создать identity требуемого статического типа."""
        ...


_SEMANTIC_ID_PATTERN = compile_pattern(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*")


@dataclass(frozen=True, order=True, slots=True)
class _SemanticId:
    """Базовая immutable-форма canonical semantic string identity."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Значение semantic identity должно быть строкой")
        if _SEMANTIC_ID_PATTERN.fullmatch(self.value) is None:
            raise ValueError(
                "Semantic identity должна иметь canonical lowercase dotted/snake representation"
            )

    def __str__(self) -> str:
        return self.value


class ModuleId(_SemanticId):
    """Стабильная semantic identity модуля."""

    __slots__ = ()


class ImplementationId(_SemanticId):
    """Стабильная identity concrete implementation."""

    __slots__ = ()


class ProfileId(_SemanticId):
    """Стабильная identity configuration profile."""

    __slots__ = ()


class StateNamespace(_SemanticId):
    """Canonical namespace shared cognitive state."""

    __slots__ = ()


class RuntimeBoundaryId(_SemanticId):
    """Стабильная identity runtime boundary, публикующей state."""

    __slots__ = ()


__all__ = [
    "ActionCommitId",
    "ActionIntentId",
    "AgentRevisionId",
    "AgentSessionId",
    "AuthorizedActionId",
    "BranchId",
    "CognitiveCycleId",
    "CommitId",
    "DecisionWindowId",
    "DispatchAttemptId",
    "DispatchId",
    "EnvironmentSnapshotId",
    "EnvironmentTransitionId",
    "EpisodeId",
    "ExecutionPlanId",
    "ExperienceEventId",
    "ExternalTaskId",
    "GoalId",
    "GoalProposalId",
    "IdFactory",
    "IdentityType",
    "ImplementationId",
    "InterventionId",
    "JournalId",
    "LineageId",
    "ModuleAttemptId",
    "ModuleId",
    "ObservationId",
    "OutcomeId",
    "PerceptId",
    "ProfileId",
    "RunId",
    "RuntimeBoundaryId",
    "StateNamespace",
    "WaveAttemptId",
    "WaveId",
    "WorldInstanceId",
]
