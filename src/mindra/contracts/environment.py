"""Environment-дескрипторы и раздельные interaction/research capabilities."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable
from uuid import UUID

from mindra.contracts.identity import (
    ActionCommitId,
    EnvironmentSnapshotId,
    EnvironmentTransitionId,
    EpisodeId,
    WorldInstanceId,
)
from mindra.contracts.interaction import (
    ActionCapabilityDescriptor,
    CommittedEnvironmentAction,
    Drop,
    EnvironmentAction,
    EpisodeStartRequest,
    EpisodeStartResult,
    ExternalTaskFeedback,
    Interact,
    InteractionResult,
    Move,
    Pickup,
    Wait,
)


def _validate_label(value: object, field_name: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{field_name} должен быть строкой")
    if not value or any(character.isspace() or not character.isprintable() for character in value):
        raise ValueError(f"{field_name} должен быть непустым whitespace-free token")


def _validate_optional_label(value: object, field_name: str) -> None:
    if value is not None:
        _validate_label(value, field_name)


def _validate_optional_text(value: object, field_name: str) -> None:
    if value is None:
        return
    if type(value) is not str:
        raise TypeError(f"{field_name} должен быть строкой или None")
    if not value.strip() or any(not character.isprintable() for character in value):
        raise ValueError(f"{field_name} должен быть непустым printable text")


def _validate_revision(value: object, field_name: str) -> None:
    if type(value) is not int:
        raise TypeError(f"{field_name} должен быть целым числом")
    if value < 0:
        raise ValueError(f"{field_name} не может быть отрицательным")


def _validate_boolean(value: object, field_name: str) -> None:
    if type(value) is not bool:
        raise TypeError(f"{field_name} должен быть bool")


def _validate_optional_seed(value: object, field_name: str) -> None:
    if value is not None and type(value) is not int:
        raise TypeError(f"{field_name} должен быть целым числом или None")


@dataclass(frozen=True, slots=True)
class EnvironmentInteractionDescriptor:
    """Безопасный доступный Agent/execution Environment-дескриптор."""

    environment_family: str
    environment_semantic_version: str
    interaction_interface_revision: int
    observation_schema_revision: int
    task_schema_revision: int
    feedback_schema_revision: int
    action_capability: ActionCapabilityDescriptor

    def __post_init__(self) -> None:
        _validate_label(self.environment_family, "environment_family")
        _validate_label(self.environment_semantic_version, "environment_semantic_version")
        for field_name in (
            "interaction_interface_revision",
            "observation_schema_revision",
            "task_schema_revision",
            "feedback_schema_revision",
        ):
            _validate_revision(getattr(self, field_name), field_name)
        if type(self.action_capability) is not ActionCapabilityDescriptor:
            raise TypeError("action_capability должен быть ActionCapabilityDescriptor")


@dataclass(frozen=True, slots=True)
class EnvironmentDescriptor:
    """Привилегированный research-дескриптор identity Environment."""

    interaction: EnvironmentInteractionDescriptor
    engine_version: str
    generator_version: str
    task_family: str
    task_version: str
    distribution_id: str
    distribution_version: str
    world_instance_id: WorldInstanceId
    world_manifest_ref: str | None

    def __post_init__(self) -> None:
        if type(self.interaction) is not EnvironmentInteractionDescriptor:
            raise TypeError("interaction должен быть EnvironmentInteractionDescriptor")
        for field_name in (
            "engine_version",
            "generator_version",
            "task_family",
            "task_version",
            "distribution_id",
            "distribution_version",
        ):
            _validate_label(getattr(self, field_name), field_name)
        if not isinstance(self.world_instance_id, UUID):
            raise TypeError("world_instance_id должен быть WorldInstanceId")
        _validate_optional_label(self.world_manifest_ref, "world_manifest_ref")


@dataclass(frozen=True, slots=True)
class EnvironmentGenerationProvenance:
    """Доступный только research provenance настроенной генерации Environment."""

    generator_version: str
    world_manifest_ref: str | None
    generation_seed: int | None
    dynamics_seed: int | None
    task_seed: int | None

    def __post_init__(self) -> None:
        _validate_label(self.generator_version, "generator_version")
        _validate_optional_label(self.world_manifest_ref, "world_manifest_ref")
        for field_name in ("generation_seed", "dynamics_seed", "task_seed"):
            _validate_optional_seed(getattr(self, field_name), field_name)


@dataclass(frozen=True, slots=True)
class EnvironmentResearchView:
    """Привилегированный структурный вид без универсального hidden-state object."""

    descriptor: EnvironmentDescriptor
    hidden_state_ref: str
    generation: EnvironmentGenerationProvenance
    terminated: bool
    truncated: bool
    termination_reason: str | None

    def __post_init__(self) -> None:
        if type(self.descriptor) is not EnvironmentDescriptor:
            raise TypeError("descriptor должен быть EnvironmentDescriptor")
        _validate_label(self.hidden_state_ref, "hidden_state_ref")
        if type(self.generation) is not EnvironmentGenerationProvenance:
            raise TypeError("generation должен быть EnvironmentGenerationProvenance")
        _validate_boolean(self.terminated, "terminated")
        _validate_boolean(self.truncated, "truncated")
        _validate_optional_text(self.termination_reason, "termination_reason")


@dataclass(frozen=True, slots=True)
class EnvironmentSnapshotMetadata:
    """Неизменяемые metadata identity/совместимости snapshot без формата payload."""

    environment_snapshot_id: EnvironmentSnapshotId
    world_instance_id: WorldInstanceId
    snapshot_contract_revision: int
    parent_snapshot_id: EnvironmentSnapshotId | None
    environment: EnvironmentDescriptor

    def __post_init__(self) -> None:
        if not isinstance(self.environment_snapshot_id, UUID):
            raise TypeError("environment_snapshot_id должен быть EnvironmentSnapshotId")
        if not isinstance(self.world_instance_id, UUID):
            raise TypeError("world_instance_id должен быть WorldInstanceId")
        _validate_revision(self.snapshot_contract_revision, "snapshot_contract_revision")
        if self.parent_snapshot_id is not None and not isinstance(self.parent_snapshot_id, UUID):
            raise TypeError("parent_snapshot_id должен быть EnvironmentSnapshotId или None")
        if type(self.environment) is not EnvironmentDescriptor:
            raise TypeError("environment должен быть EnvironmentDescriptor")


@runtime_checkable
class EnvironmentSnapshot(Protocol):
    """Snapshot capability без преждевременно заданного serialization payload."""

    @property
    def metadata(self) -> EnvironmentSnapshotMetadata:
        """Вернуть immutable research metadata snapshot."""
        ...


class ResearchActionOutcomeStatus(Enum):
    """Привилегированная категория результата действия на уровне мира."""

    EFFECT = "effect"
    NO_EFFECT = "no_effect"
    STOCHASTIC_FAILURE = "stochastic_failure"


@dataclass(frozen=True, slots=True)
class EnvironmentResearchTransitionRecord:
    """Привилегированная causal Environment transition record без persistence ownership."""

    environment_transition_id: EnvironmentTransitionId
    episode_id: EpisodeId
    world_instance_id: WorldInstanceId
    action_commit_id: ActionCommitId
    action: EnvironmentAction
    pre_snapshot_id: EnvironmentSnapshotId | None
    post_snapshot_id: EnvironmentSnapshotId | None
    action_status: ResearchActionOutcomeStatus
    reason: str | None
    external_feedback: ExternalTaskFeedback | None
    terminated: bool
    truncated: bool
    termination_reason: str | None

    def __post_init__(self) -> None:
        for field_name in (
            "environment_transition_id",
            "episode_id",
            "world_instance_id",
            "action_commit_id",
        ):
            if not isinstance(getattr(self, field_name), UUID):
                raise TypeError(f"{field_name} должен быть соответствующей UUID identity")
        if type(self.action) not in (Move, Interact, Pickup, Drop, Wait):
            raise TypeError("action должен быть canonical EnvironmentAction")
        for field_name in ("pre_snapshot_id", "post_snapshot_id"):
            value = getattr(self, field_name)
            if value is not None and not isinstance(value, UUID):
                raise TypeError(f"{field_name} должен быть EnvironmentSnapshotId или None")
        if type(self.action_status) is not ResearchActionOutcomeStatus:
            raise TypeError("action_status должен быть ResearchActionOutcomeStatus")
        _validate_optional_text(self.reason, "reason")
        if (
            self.external_feedback is not None
            and type(self.external_feedback) is not ExternalTaskFeedback
        ):
            raise TypeError("external_feedback должен быть ExternalTaskFeedback или None")
        _validate_boolean(self.terminated, "terminated")
        _validate_boolean(self.truncated, "truncated")
        _validate_optional_text(self.termination_reason, "termination_reason")


@runtime_checkable
class EnvironmentInteraction(Protocol):
    """Узкая capability обычного взаимодействия Agent и Environment."""

    def describe_interaction(self) -> EnvironmentInteractionDescriptor:
        """Описать только safe interaction contract."""
        ...

    def reset(self, request: EpisodeStartRequest, /) -> EpisodeStartResult:
        """Начать Episode с caller-owned identity."""
        ...

    def apply_committed_action(
        self,
        action: CommittedEnvironmentAction,
        /,
    ) -> InteractionResult:
        """Применить уже committed semantic action."""
        ...


@runtime_checkable
class EnvironmentResearch(Protocol):
    """Отдельная привилегированная capability research control Environment."""

    def inspect(self) -> EnvironmentResearchView:
        """Получить privileged structural view."""
        ...

    def snapshot(self) -> EnvironmentSnapshot:
        """Получить immutable snapshot capability."""
        ...

    def restore(self, snapshot: EnvironmentSnapshot, /) -> None:
        """Восстановить state без natural Environment transition."""
        ...

    def clone(self) -> EnvironmentCapabilities:
        """Создать independent capability bundle текущего exact state."""
        ...

    def fork(self, snapshot: EnvironmentSnapshot, /) -> EnvironmentCapabilities:
        """Создать independent capability bundle от explicit snapshot."""
        ...

    def transition_records(self) -> tuple[EnvironmentResearchTransitionRecord, ...]:
        """Вернуть immutable structural transition record sequence."""
        ...


@dataclass(frozen=True, slots=True)
class EnvironmentCapabilities:
    """Только wiring-bundle раздельных interaction/research surfaces."""

    interaction: EnvironmentInteraction
    research: EnvironmentResearch

    def __post_init__(self) -> None:
        if not isinstance(self.interaction, EnvironmentInteraction):
            raise TypeError("interaction должен удовлетворять EnvironmentInteraction")
        if not isinstance(self.research, EnvironmentResearch):
            raise TypeError("research должен удовлетворять EnvironmentResearch")


__all__ = [
    "EnvironmentCapabilities",
    "EnvironmentDescriptor",
    "EnvironmentGenerationProvenance",
    "EnvironmentInteraction",
    "EnvironmentInteractionDescriptor",
    "EnvironmentResearch",
    "EnvironmentResearchTransitionRecord",
    "EnvironmentResearchView",
    "EnvironmentSnapshot",
    "EnvironmentSnapshotMetadata",
    "ResearchActionOutcomeStatus",
]
