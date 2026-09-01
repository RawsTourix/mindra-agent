"""Доступные Agent контракты взаимодействия с Environment."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from uuid import UUID

from mindra.contracts.identity import (
    ActionCommitId,
    EnvironmentTransitionId,
    EpisodeId,
    ExternalTaskId,
    ObservationId,
)

type AgentVisibleScalar = bool | int | float | str | None
type AgentVisibleValue = AgentVisibleScalar | tuple[AgentVisibleScalar, ...]


def _validate_label(value: object, field_name: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{field_name} должен быть строкой")
    if not value or any(character.isspace() or not character.isprintable() for character in value):
        raise ValueError(f"{field_name} должен быть непустым whitespace-free token")


def _validate_revision(value: object, field_name: str) -> None:
    if type(value) is not int:
        raise TypeError(f"{field_name} должен быть целым числом")
    if value < 0:
        raise ValueError(f"{field_name} не может быть отрицательным")


def _validate_boolean(value: object, field_name: str) -> None:
    if type(value) is not bool:
        raise TypeError(f"{field_name} должен быть bool")


def _validate_scalar(value: object, field_name: str) -> None:
    if value is None:
        return
    if type(value) not in {bool, int, float, str}:
        raise TypeError(f"{field_name} должен содержать только agent-visible scalar")
    if isinstance(value, float) and not isfinite(value):
        raise ValueError(f"{field_name} не может содержать не-конечный float")


def _validate_value(value: object, field_name: str) -> None:
    if type(value) is tuple:
        for item in value:
            _validate_scalar(item, field_name)
        return
    _validate_scalar(value, field_name)


def _validate_fields(fields: object, field_name: str) -> None:
    if type(fields) is not tuple:
        raise TypeError(f"{field_name} должен быть tuple AgentVisibleField")
    names: set[str] = set()
    for field in fields:
        if type(field) is not AgentVisibleField:
            raise TypeError(f"{field_name} должен содержать AgentVisibleField")
        if field.name in names:
            raise ValueError(f"{field_name} содержит duplicate field name: {field.name}")
        names.add(field.name)


def _validate_records(records: object, field_name: str) -> None:
    if type(records) is not tuple:
        raise TypeError(f"{field_name} должен быть tuple AgentVisibleRecord")
    if any(type(record) is not AgentVisibleRecord for record in records):
        raise TypeError(f"{field_name} должен содержать AgentVisibleRecord")


@dataclass(frozen=True, slots=True)
class AgentVisibleField:
    """Одно неизменяемое именованное поле открытой Environment-нагрузки."""

    name: str
    value: AgentVisibleValue

    def __post_init__(self) -> None:
        _validate_label(self.name, "name")
        _validate_value(self.value, "value")


@dataclass(frozen=True, slots=True)
class AgentVisibleRecord:
    """Типизированная открытая запись без универсального metadata-канала."""

    kind: str
    fields: tuple[AgentVisibleField, ...]

    def __post_init__(self) -> None:
        _validate_label(self.kind, "kind")
        _validate_fields(self.fields, "fields")


class Direction(Enum):
    """Каноническое направление по сторонам света MicroWorld v0.2."""

    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


@dataclass(frozen=True, slots=True)
class Move:
    """Переместиться в заданном направлении."""

    direction: Direction

    def __post_init__(self) -> None:
        if type(self.direction) is not Direction:
            raise TypeError("direction должен быть Direction")


@dataclass(frozen=True, slots=True)
class Interact:
    """Взаимодействовать в заданном направлении."""

    direction: Direction

    def __post_init__(self) -> None:
        if type(self.direction) is not Direction:
            raise TypeError("direction должен быть Direction")


@dataclass(frozen=True, slots=True)
class Pickup:
    """Поднять объект в заданном направлении."""

    direction: Direction

    def __post_init__(self) -> None:
        if type(self.direction) is not Direction:
            raise TypeError("direction должен быть Direction")


@dataclass(frozen=True, slots=True)
class Drop:
    """Положить объект в заданном направлении."""

    direction: Direction

    def __post_init__(self) -> None:
        if type(self.direction) is not Direction:
            raise TypeError("direction должен быть Direction")


@dataclass(frozen=True, slots=True)
class Wait:
    """Явное намерение дождаться следующего внешнего перехода."""


type EnvironmentAction = Move | Interact | Pickup | Drop | Wait

_ACTION_TYPES = (Move, Interact, Pickup, Drop, Wait)
_ACTION_KINDS = frozenset({"drop", "interact", "move", "pickup", "wait"})


def _validate_action(action: object) -> None:
    if type(action) not in _ACTION_TYPES:
        raise TypeError("action должен быть canonical EnvironmentAction")


@dataclass(frozen=True, slots=True)
class ActionCapabilityDescriptor:
    """Стабильная action-schema capability без динамической маски hidden state."""

    action_schema_revision: int
    supported_action_kinds: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_revision(self.action_schema_revision, "action_schema_revision")
        if type(self.supported_action_kinds) is not tuple:
            raise TypeError("supported_action_kinds должен быть tuple строк")
        if not self.supported_action_kinds:
            raise ValueError("supported_action_kinds не может быть пустым")
        if any(type(kind) is not str for kind in self.supported_action_kinds):
            raise TypeError("supported_action_kinds должен содержать строки")
        if any(kind not in _ACTION_KINDS for kind in self.supported_action_kinds):
            raise ValueError("supported_action_kinds содержит неизвестный action kind")
        if self.supported_action_kinds != tuple(sorted(set(self.supported_action_kinds))):
            raise ValueError("supported_action_kinds должен иметь canonical unique ordering")


@dataclass(frozen=True, slots=True)
class RawObservation:
    """Доступное Agent raw observation без исследовательского provenance."""

    observation_id: ObservationId
    observation_schema_revision: int
    records: tuple[AgentVisibleRecord, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.observation_id, UUID):
            raise TypeError("observation_id должен быть ObservationId")
        _validate_revision(self.observation_schema_revision, "observation_schema_revision")
        _validate_records(self.records, "records")


@dataclass(frozen=True, slots=True)
class ExternalTaskSpecification:
    """Намеренно раскрытая внешняя task specification, не внутренний Goal."""

    external_task_id: ExternalTaskId
    task_schema_revision: int
    task_kind: str
    parameters: tuple[AgentVisibleField, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.external_task_id, UUID):
            raise TypeError("external_task_id должен быть ExternalTaskId")
        _validate_revision(self.task_schema_revision, "task_schema_revision")
        _validate_label(self.task_kind, "task_kind")
        _validate_fields(self.parameters, "parameters")


class ExternalTaskFeedbackStatus(Enum):
    """Доступный Agent статус внешней задачи."""

    IN_PROGRESS = "in_progress"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class ExternalTaskFeedback:
    """Явно объявленный доступный Agent feedback внешней задачи."""

    external_task_id: ExternalTaskId
    feedback_schema_revision: int
    status: ExternalTaskFeedbackStatus
    events: tuple[AgentVisibleRecord, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.external_task_id, UUID):
            raise TypeError("external_task_id должен быть ExternalTaskId")
        _validate_revision(self.feedback_schema_revision, "feedback_schema_revision")
        if type(self.status) is not ExternalTaskFeedbackStatus:
            raise TypeError("status должен быть ExternalTaskFeedbackStatus")
        _validate_records(self.events, "events")


class AgentVisibleActionOutcomeStatus(Enum):
    """Узкий открытый статус эффекта без привилегированной причины."""

    EFFECT = "effect"
    NO_EFFECT = "no_effect"


@dataclass(frozen=True, slots=True)
class AgentVisibleActionOutcome:
    """Доступная Agent проекция последствия действия."""

    status: AgentVisibleActionOutcomeStatus
    events: tuple[AgentVisibleRecord, ...]

    def __post_init__(self) -> None:
        if type(self.status) is not AgentVisibleActionOutcomeStatus:
            raise TypeError("status должен быть AgentVisibleActionOutcomeStatus")
        _validate_records(self.events, "events")


@dataclass(frozen=True, slots=True)
class EnvironmentEpisodeControl:
    """Доступный только research/runtime reset control, не observation Agent."""

    world_manifest_ref: str | None
    generation_seed: int | None
    dynamics_seed: int | None
    task_seed: int | None
    full_observation: bool

    def __post_init__(self) -> None:
        if self.world_manifest_ref is not None:
            _validate_label(self.world_manifest_ref, "world_manifest_ref")
        for field_name in ("generation_seed", "dynamics_seed", "task_seed"):
            value = getattr(self, field_name)
            if value is not None and type(value) is not int:
                raise TypeError(f"{field_name} должен быть целым числом или None")
        _validate_boolean(self.full_observation, "full_observation")


@dataclass(frozen=True, slots=True)
class EpisodeStartRequest:
    """Принадлежащая runtime Episode identity и опциональный research reset control."""

    episode_id: EpisodeId
    control: EnvironmentEpisodeControl | None

    def __post_init__(self) -> None:
        if not isinstance(self.episode_id, UUID):
            raise TypeError("episode_id должен быть EpisodeId")
        if self.control is not None and type(self.control) is not EnvironmentEpisodeControl:
            raise TypeError("control должен быть EnvironmentEpisodeControl или None")


@dataclass(frozen=True, slots=True)
class EpisodeStartResult:
    """Успешный доступный Agent результат Environment reset."""

    raw_observation: RawObservation
    external_task: ExternalTaskSpecification | None
    external_feedback: ExternalTaskFeedback | None
    terminated: bool
    truncated: bool

    def __post_init__(self) -> None:
        if type(self.raw_observation) is not RawObservation:
            raise TypeError("raw_observation должен быть RawObservation")
        if (
            self.external_task is not None
            and type(self.external_task) is not ExternalTaskSpecification
        ):
            raise TypeError("external_task должен быть ExternalTaskSpecification или None")
        if (
            self.external_feedback is not None
            and type(self.external_feedback) is not ExternalTaskFeedback
        ):
            raise TypeError("external_feedback должен быть ExternalTaskFeedback или None")
        _validate_boolean(self.terminated, "terminated")
        _validate_boolean(self.truncated, "truncated")
        if self.terminated or self.truncated:
            raise ValueError("Successful Episode reset не может быть terminated или truncated")


@dataclass(frozen=True, slots=True)
class CommittedEnvironmentAction:
    """Минимальная направленная в Environment нагрузка после Action Commit."""

    action_commit_id: ActionCommitId
    action: EnvironmentAction

    def __post_init__(self) -> None:
        if not isinstance(self.action_commit_id, UUID):
            raise TypeError("action_commit_id должен быть ActionCommitId")
        _validate_action(self.action)


@dataclass(frozen=True, slots=True)
class EnvironmentTransitionRef:
    """Непрозрачная ссылка на authoritative Environment transition."""

    environment_transition_id: EnvironmentTransitionId

    def __post_init__(self) -> None:
        if not isinstance(self.environment_transition_id, UUID):
            raise TypeError("environment_transition_id должен быть EnvironmentTransitionId")


@dataclass(frozen=True, slots=True)
class EnvironmentTransitionReceipt:
    """Причинная связь ActionCommitId с опубликованным Environment transition."""

    action_commit_id: ActionCommitId
    transition: EnvironmentTransitionRef

    def __post_init__(self) -> None:
        if not isinstance(self.action_commit_id, UUID):
            raise TypeError("action_commit_id должен быть ActionCommitId")
        if type(self.transition) is not EnvironmentTransitionRef:
            raise TypeError("transition должен быть EnvironmentTransitionRef")


@dataclass(frozen=True, slots=True)
class InteractionResult:
    """Доступная Agent/execution проекция authoritative transition."""

    receipt: EnvironmentTransitionReceipt
    raw_observation: RawObservation
    external_feedback: ExternalTaskFeedback | None
    action_outcome: AgentVisibleActionOutcome | None
    terminated: bool
    truncated: bool

    def __post_init__(self) -> None:
        if type(self.receipt) is not EnvironmentTransitionReceipt:
            raise TypeError("receipt должен быть EnvironmentTransitionReceipt")
        if type(self.raw_observation) is not RawObservation:
            raise TypeError("raw_observation должен быть RawObservation")
        if (
            self.external_feedback is not None
            and type(self.external_feedback) is not ExternalTaskFeedback
        ):
            raise TypeError("external_feedback должен быть ExternalTaskFeedback или None")
        if (
            self.action_outcome is not None
            and type(self.action_outcome) is not AgentVisibleActionOutcome
        ):
            raise TypeError("action_outcome должен быть AgentVisibleActionOutcome или None")
        _validate_boolean(self.terminated, "terminated")
        _validate_boolean(self.truncated, "truncated")


__all__ = [
    "ActionCapabilityDescriptor",
    "AgentVisibleActionOutcome",
    "AgentVisibleActionOutcomeStatus",
    "AgentVisibleField",
    "AgentVisibleRecord",
    "AgentVisibleScalar",
    "AgentVisibleValue",
    "CommittedEnvironmentAction",
    "Direction",
    "Drop",
    "EnvironmentAction",
    "EnvironmentEpisodeControl",
    "EnvironmentTransitionReceipt",
    "EnvironmentTransitionRef",
    "EpisodeStartRequest",
    "EpisodeStartResult",
    "ExternalTaskFeedback",
    "ExternalTaskFeedbackStatus",
    "ExternalTaskSpecification",
    "Interact",
    "InteractionResult",
    "Move",
    "Pickup",
    "RawObservation",
    "Wait",
]
