"""Явная availability и freshness semantics Core Kernel."""

from dataclasses import dataclass

from mindra.contracts.revisions import StateRevision
from mindra.contracts.time import LogicalTime


@dataclass(frozen=True, slots=True)
class FreshnessMetadata:
    """Causal context последнего известного значения."""

    produced_at: LogicalTime
    based_on_state_revision: StateRevision

    def __post_init__(self) -> None:
        if not isinstance(self.produced_at, LogicalTime):
            raise TypeError("produced_at должен быть LogicalTime")
        if not isinstance(self.based_on_state_revision, StateRevision):
            raise TypeError("based_on_state_revision должен быть StateRevision")


@dataclass(frozen=True, slots=True)
class Available[ValueT]:
    """Применимое текущее значение."""

    value: ValueT


@dataclass(frozen=True, slots=True)
class Unknown:
    """Применимое, но неизвестное или ещё не вычисленное значение."""


@dataclass(frozen=True, slots=True)
class Stale[ValueT]:
    """Последнее известное значение с недостаточной freshness."""

    value: ValueT
    freshness: FreshnessMetadata

    def __post_init__(self) -> None:
        if not isinstance(self.freshness, FreshnessMetadata):
            raise TypeError("freshness должен быть FreshnessMetadata")


@dataclass(frozen=True, slots=True)
class Unavailable:
    """Неприменимая или намеренно недоступная capability/value."""


type Availability[ValueT] = Available[ValueT] | Unknown | Stale[ValueT] | Unavailable

__all__ = [
    "Availability",
    "Available",
    "FreshnessMetadata",
    "Stale",
    "Unavailable",
    "Unknown",
]
