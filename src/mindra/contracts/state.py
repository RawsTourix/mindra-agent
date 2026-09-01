"""Immutable schema primitives канонического CognitiveState."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from re import compile as compile_pattern
from types import MappingProxyType
from typing import cast, overload
from uuid import UUID

from mindra.contracts.availability import Availability, Available, Stale, Unavailable, Unknown
from mindra.contracts.errors import (
    AvailabilityError,
    MissingFieldError,
    SchemaError,
    UndeclaredReadError,
)
from mindra.contracts.identity import (
    AgentRevisionId,
    BranchId,
    LineageId,
    ModuleId,
    RuntimeBoundaryId,
)
from mindra.contracts.provenance import StateProvenance
from mindra.contracts.revisions import CompositionRevision, SchemaRevision, StateRevision
from mindra.contracts.time import LogicalTime

_SEGMENT_PATTERN = compile_pattern(r"[a-z][a-z0-9_]*")


@dataclass(frozen=True, order=True, slots=True)
class StatePath:
    """Validated semantic path с canonical dotted representation."""

    segments: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.segments, tuple):
            raise TypeError("segments должен быть tuple строк")
        if not self.segments:
            raise ValueError("StatePath должен содержать хотя бы один segment")

        for segment in self.segments:
            if not isinstance(segment, str):
                raise TypeError("Каждый StatePath segment должен быть строкой")
            if _SEGMENT_PATTERN.fullmatch(segment) is None:
                raise ValueError(
                    "StatePath segment должен иметь canonical lowercase snake representation"
                )

    @classmethod
    def from_dotted(cls, value: str) -> StatePath:
        """Разобрать canonical dotted representation без неявной нормализации."""
        if not isinstance(value, str):
            raise TypeError("Dotted StatePath должен быть строкой")
        return cls(tuple(value.split(".")))

    @property
    def dotted(self) -> str:
        """Вернуть canonical dotted representation."""
        return ".".join(self.segments)

    def __str__(self) -> str:
        return self.dotted


@dataclass(frozen=True, slots=True)
class StateKey[ValueT]:
    """Typed handle canonical поля active state schema."""

    path: StatePath

    def __post_init__(self) -> None:
        if not isinstance(self.path, StatePath):
            raise TypeError("path должен быть StatePath")


def _is_snapshot_safe(value: object) -> bool:
    if value is None or type(value) in {bool, int, float, complex, str, bytes, range}:
        return True
    if isinstance(value, UUID):
        return True
    if isinstance(value, Enum):
        return _is_snapshot_safe(value.value)
    if isinstance(value, tuple | frozenset):
        return all(_is_snapshot_safe(item) for item in value)
    if isinstance(value, list | dict | set | bytearray):
        return False
    if is_dataclass(value) and not isinstance(value, type):
        parameters = getattr(type(value), "__dataclass_params__", None)
        if parameters is None or not parameters.frozen:
            return False
        return all(_is_snapshot_safe(getattr(value, field.name)) for field in fields(value))
    return False


@dataclass(frozen=True, slots=True)
class ValueContract[ValueT]:
    """Default contract immutable Python payload заданного runtime-типа."""

    value_type: type[ValueT]

    def __post_init__(self) -> None:
        if not isinstance(self.value_type, type):
            raise TypeError("value_type должен быть Python type")

    def validate(self, value: object) -> None:
        """Fail closed проверить runtime type и snapshot safety payload."""
        if not isinstance(value, self.value_type):
            raise SchemaError(
                f"Payload должен иметь тип {self.value_type.__qualname__}, "
                f"получен {type(value).__qualname__}"
            )
        if not _is_snapshot_safe(value):
            raise SchemaError("Payload не является snapshot-safe immutable value")

    def freeze(self, value: object) -> ValueT:
        """Проверить и вернуть уже immutable canonical payload."""
        self.validate(value)
        return cast(ValueT, value)


@dataclass(frozen=True, slots=True)
class StateFieldSpec[ValueT]:
    """Schema declaration поля с explicit semantic owner."""

    key: StateKey[ValueT]
    owner: ModuleId | RuntimeBoundaryId
    value_contract: ValueContract[ValueT]

    def __post_init__(self) -> None:
        if not isinstance(self.key, StateKey):
            raise TypeError("key должен быть StateKey")
        if not isinstance(self.owner, ModuleId | RuntimeBoundaryId):
            raise TypeError("owner должен быть explicit ModuleId или RuntimeBoundaryId")
        if not isinstance(self.value_contract, ValueContract):
            raise TypeError("value_contract должен быть ValueContract")


@dataclass(frozen=True, slots=True, init=False)
class StateSchema:
    """Compiled immutable registry canonical state fields."""

    revision: SchemaRevision
    _fields: Mapping[StatePath, StateFieldSpec[object]]

    def __init__(
        self,
        revision: SchemaRevision,
        field_specs: Iterable[StateFieldSpec[object]],
    ) -> None:
        if not isinstance(revision, SchemaRevision):
            raise TypeError("revision должен быть SchemaRevision")

        compiled: dict[StatePath, StateFieldSpec[object]] = {}
        for spec in field_specs:
            if not isinstance(spec, StateFieldSpec):
                raise TypeError("field_specs должен содержать StateFieldSpec")
            path = spec.key.path
            if path in compiled:
                raise SchemaError(f"Duplicate StatePath в schema: {path}")
            compiled[path] = spec

        object.__setattr__(self, "revision", revision)
        object.__setattr__(self, "_fields", MappingProxyType(compiled))

    @property
    def fields(self) -> Mapping[StatePath, StateFieldSpec[object]]:
        """Вернуть read-only mapping compiled fields."""
        return self._fields

    @overload
    def lookup[ValueT](self, key: StateKey[ValueT]) -> StateFieldSpec[ValueT]: ...

    @overload
    def lookup(self, key: StatePath) -> StateFieldSpec[object]: ...

    def lookup[ValueT](
        self, key: StateKey[ValueT] | StatePath
    ) -> StateFieldSpec[ValueT] | StateFieldSpec[object]:
        """Найти spec либо явно сообщить structural missing."""
        path = key.path if isinstance(key, StateKey) else key
        if not isinstance(path, StatePath):
            raise TypeError("lookup принимает StateKey или StatePath")
        try:
            spec = self._fields[path]
        except KeyError as error:
            raise MissingFieldError(f"StatePath отсутствует в active schema: {path}") from error
        return cast(StateFieldSpec[ValueT], spec)

    def __len__(self) -> int:
        return len(self._fields)


@dataclass(frozen=True, slots=True)
class StateEntry[ValueT]:
    """Immutable availability/value с causal provenance."""

    availability: Availability[ValueT]
    provenance: StateProvenance

    def __post_init__(self) -> None:
        if not isinstance(self.availability, Available | Unknown | Stale | Unavailable):
            raise TypeError("availability должна быть canonical Availability variant")
        if not isinstance(self.provenance, StateProvenance):
            raise TypeError("provenance должна быть StateProvenance")
        if isinstance(self.availability, Available | Stale) and not _is_snapshot_safe(
            self.availability.value
        ):
            raise SchemaError("StateEntry payload не является snapshot-safe immutable value")


@dataclass(frozen=True, slots=True)
class StateEnvelope:
    """Causal metadata immutable state snapshot без payload/store behavior."""

    schema_revision: SchemaRevision
    state_revision: StateRevision
    parent_state_revision: StateRevision | None
    lineage_id: LineageId
    branch_id: BranchId
    agent_revision_id: AgentRevisionId
    logical_time: LogicalTime
    composition_revision: CompositionRevision

    def __post_init__(self) -> None:
        if not isinstance(self.schema_revision, SchemaRevision):
            raise TypeError("schema_revision должен быть SchemaRevision")
        if not isinstance(self.state_revision, StateRevision):
            raise TypeError("state_revision должен быть StateRevision")
        if self.parent_state_revision is not None and not isinstance(
            self.parent_state_revision, StateRevision
        ):
            raise TypeError("parent_state_revision должен быть StateRevision или None")
        if not isinstance(self.lineage_id, UUID):
            raise TypeError("lineage_id должен быть LineageId")
        if not isinstance(self.branch_id, UUID):
            raise TypeError("branch_id должен быть BranchId")
        if not isinstance(self.agent_revision_id, UUID):
            raise TypeError("agent_revision_id должен быть AgentRevisionId")
        if not isinstance(self.logical_time, LogicalTime):
            raise TypeError("logical_time должен быть LogicalTime")
        if not isinstance(self.composition_revision, CompositionRevision):
            raise TypeError("composition_revision должен быть CompositionRevision")


class FreshnessMode(Enum):
    """Freshness semantics declared read dependency."""

    ANY_COMMITTED = "any_committed"
    CURRENT_CYCLE = "current_cycle"
    CURRENT_DECISION_WINDOW = "current_decision_window"
    CURRENT_EPISODE = "current_episode"


type AvailabilityVariant = (
    type[Available[object]] | type[Unknown] | type[Stale[object]] | type[Unavailable]
)

_AVAILABILITY_VARIANTS = (Available, Unknown, Stale, Unavailable)


@dataclass(frozen=True, slots=True)
class ReadSpec[ValueT]:
    """Typed declaration read dependency без выполнения projection read."""

    key: StateKey[ValueT]
    required: bool
    allowed_availability: frozenset[AvailabilityVariant]
    freshness: FreshnessMode

    def __post_init__(self) -> None:
        if not isinstance(self.key, StateKey):
            raise TypeError("key должен быть StateKey")
        if type(self.required) is not bool:
            raise TypeError("required должен быть bool")
        if not isinstance(self.allowed_availability, frozenset):
            raise TypeError("allowed_availability должен быть frozenset")
        if not self.allowed_availability:
            raise ValueError("allowed_availability не может быть пустым")
        if any(variant not in _AVAILABILITY_VARIANTS for variant in self.allowed_availability):
            raise ValueError("allowed_availability содержит неизвестный availability variant")
        if not isinstance(self.freshness, FreshnessMode):
            raise TypeError("freshness должен быть FreshnessMode")


def _freeze_entry(spec: StateFieldSpec[object], entry: StateEntry[object]) -> StateEntry[object]:
    """Применить schema ValueContract к payload перед публикацией snapshot."""
    availability = entry.availability
    if isinstance(availability, Available):
        frozen_availability: Availability[object] = Available(
            spec.value_contract.freeze(availability.value)
        )
    elif isinstance(availability, Stale):
        frozen_availability = Stale(
            value=spec.value_contract.freeze(availability.value),
            freshness=availability.freshness,
        )
    else:
        frozen_availability = availability
    return StateEntry(availability=frozen_availability, provenance=entry.provenance)


@dataclass(frozen=True, slots=True, init=False)
class CognitiveState:
    """Immutable-by-interface committed canonical state snapshot."""

    envelope: StateEnvelope
    _entries: Mapping[StatePath, StateEntry[object]]

    def __init__(
        self,
        *,
        schema: StateSchema,
        envelope: StateEnvelope,
        entries: Mapping[StatePath, StateEntry[object]],
    ) -> None:
        if not isinstance(schema, StateSchema):
            raise TypeError("schema должен быть StateSchema")
        if not isinstance(envelope, StateEnvelope):
            raise TypeError("envelope должен быть StateEnvelope")
        if not isinstance(entries, Mapping):
            raise TypeError("entries должен быть Mapping")
        if envelope.schema_revision != schema.revision:
            raise SchemaError("StateEnvelope и StateSchema имеют разные schema revision")

        frozen_entries: dict[StatePath, StateEntry[object]] = {}
        for path, entry in entries.items():
            if not isinstance(path, StatePath):
                raise TypeError("entries keys должны быть StatePath")
            if not isinstance(entry, StateEntry):
                raise TypeError("entries values должны быть StateEntry")
            spec = schema.lookup(path)
            frozen_entries[path] = _freeze_entry(spec, entry)

        object.__setattr__(self, "envelope", envelope)
        object.__setattr__(self, "_entries", MappingProxyType(frozen_entries))

    @property
    def entries(self) -> Mapping[StatePath, StateEntry[object]]:
        """Вернуть read-only mapping без выдачи mutable backing store."""
        return self._entries

    def read[ValueT](self, key: StateKey[ValueT]) -> StateEntry[ValueT]:
        """Прочитать canonical entry либо сообщить structural missing."""
        if not isinstance(key, StateKey):
            raise TypeError("key должен быть StateKey")
        try:
            entry = self._entries[key.path]
        except KeyError as error:
            raise MissingFieldError(
                f"StatePath отсутствует в committed CognitiveState: {key.path}"
            ) from error
        return cast(StateEntry[ValueT], entry)

    def __len__(self) -> int:
        return len(self._entries)


@dataclass(frozen=True, slots=True, init=False)
class StateProjection:
    """Узкий module-facing view только declared canonical reads."""

    _read_specs: Mapping[StatePath, ReadSpec[object]]
    _entries: Mapping[StatePath, StateEntry[object]]
    _logical_time: LogicalTime

    @classmethod
    def _from_runtime(
        cls,
        *,
        read_specs: Iterable[ReadSpec[object]],
        entries: Mapping[StatePath, StateEntry[object]],
        logical_time: LogicalTime,
    ) -> StateProjection:
        """Создать projection из подготовленных runtime данных."""
        if not isinstance(entries, Mapping):
            raise TypeError("entries должен быть Mapping")
        if not isinstance(logical_time, LogicalTime):
            raise TypeError("logical_time должен быть LogicalTime")

        declared: dict[StatePath, ReadSpec[object]] = {}
        for read_spec in read_specs:
            if not isinstance(read_spec, ReadSpec):
                raise TypeError("read_specs должен содержать ReadSpec")
            path = read_spec.key.path
            if path in declared:
                raise SchemaError(f"Duplicate ReadSpec для StatePath: {path}")
            declared[path] = read_spec

        projected_entries = {path: entry for path, entry in entries.items() if path in declared}
        projection = object.__new__(cls)
        object.__setattr__(projection, "_read_specs", MappingProxyType(declared))
        object.__setattr__(projection, "_entries", MappingProxyType(dict(projected_entries)))
        object.__setattr__(projection, "_logical_time", logical_time)
        return projection

    def read[ValueT](self, key: StateKey[ValueT]) -> StateEntry[ValueT]:
        """Прочитать declared entry с fail-closed availability/freshness checks."""
        if not isinstance(key, StateKey):
            raise TypeError("key должен быть StateKey")
        try:
            read_spec = self._read_specs[key.path]
        except KeyError as error:
            raise UndeclaredReadError(f"Read не объявлен для StatePath: {key.path}") from error

        try:
            entry = self._entries[key.path]
        except KeyError as error:
            raise MissingFieldError(
                f"StatePath отсутствует в committed CognitiveState: {key.path}"
            ) from error

        availability_type = type(entry.availability)
        if availability_type not in read_spec.allowed_availability:
            raise AvailabilityError(
                f"Availability {availability_type.__name__} запрещена для StatePath: {key.path}"
            )

        produced_at = entry.provenance.logical_time
        if read_spec.freshness is FreshnessMode.CURRENT_CYCLE:
            if self._logical_time.cognitive_cycle_id is None or any(
                produced != current
                for produced, current in (
                    (produced_at.run_id, self._logical_time.run_id),
                    (produced_at.agent_session_id, self._logical_time.agent_session_id),
                    (produced_at.episode_id, self._logical_time.episode_id),
                    (produced_at.decision_window_id, self._logical_time.decision_window_id),
                    (produced_at.cognitive_cycle_id, self._logical_time.cognitive_cycle_id),
                )
            ):
                raise AvailabilityError(
                    f"StatePath не произведён в текущем cognitive cycle: {key.path}"
                )
        elif read_spec.freshness is FreshnessMode.CURRENT_DECISION_WINDOW:
            if (
                self._logical_time.episode_id is None
                or self._logical_time.decision_window_id is None
                or any(
                    produced != current
                    for produced, current in (
                        (produced_at.run_id, self._logical_time.run_id),
                        (produced_at.agent_session_id, self._logical_time.agent_session_id),
                        (produced_at.episode_id, self._logical_time.episode_id),
                        (produced_at.decision_window_id, self._logical_time.decision_window_id),
                    )
                )
            ):
                raise AvailabilityError(
                    f"StatePath не произведён в текущем decision window: {key.path}"
                )
        elif read_spec.freshness is FreshnessMode.CURRENT_EPISODE:
            if self._logical_time.episode_id is None or any(
                produced != current
                for produced, current in (
                    (produced_at.run_id, self._logical_time.run_id),
                    (produced_at.agent_session_id, self._logical_time.agent_session_id),
                    (produced_at.episode_id, self._logical_time.episode_id),
                )
            ):
                raise AvailabilityError(f"StatePath не произведён в текущем episode: {key.path}")

        return cast(StateEntry[ValueT], entry)


__all__ = [
    "AvailabilityVariant",
    "CognitiveState",
    "FreshnessMode",
    "ReadSpec",
    "StateEntry",
    "StateEnvelope",
    "StateFieldSpec",
    "StateKey",
    "StatePath",
    "StateProjection",
    "StateSchema",
    "ValueContract",
]
