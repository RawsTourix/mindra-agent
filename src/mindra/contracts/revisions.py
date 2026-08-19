"""Раздельные monotonic revision-типы Core Kernel."""

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, order=True, slots=True)
class _Revision:
    """Общая реализация без общего public revision-типа."""

    value: int

    def __post_init__(self) -> None:
        if type(self.value) is not int:
            raise TypeError("Значение revision должно быть целым числом")
        if self.value < 0:
            raise ValueError("Значение revision не может быть отрицательным")

    @classmethod
    def initial(cls) -> Self:
        """Вернуть начальную revision текущего semantic-типа."""
        return cls(0)

    def next(self) -> Self:
        """Вернуть следующую revision того же semantic-типа."""
        return type(self)(self.value + 1)


class SchemaRevision(_Revision):
    """Revision active state schema."""

    __slots__ = ()


class StateRevision(_Revision):
    """Revision committed public CognitiveState."""

    __slots__ = ()


class PrivateStateRevision(_Revision):
    """Revision module-private committed state."""

    __slots__ = ()


class ExecutionPlanRevision(_Revision):
    """Revision compiled execution plan."""

    __slots__ = ()


class CompositionRevision(_Revision):
    """Revision resolved composition."""

    __slots__ = ()


__all__ = [
    "CompositionRevision",
    "ExecutionPlanRevision",
    "PrivateStateRevision",
    "SchemaRevision",
    "StateRevision",
]
