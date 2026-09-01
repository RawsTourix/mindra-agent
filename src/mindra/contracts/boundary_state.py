"""Staged contracts публикации CognitiveState runtime boundary."""

from dataclasses import dataclass

from mindra.contracts.availability import Availability, Available, Stale, Unavailable, Unknown
from mindra.contracts.errors import SchemaError
from mindra.contracts.identity import RuntimeBoundaryId
from mindra.contracts.provenance import StateProvenance
from mindra.contracts.revisions import StateRevision
from mindra.contracts.state import StateEntry, StateKey


@dataclass(frozen=True, slots=True)
class BoundaryStateWrite[ValueT]:
    """Typed staged write runtime-owned canonical state."""

    key: StateKey[ValueT]
    availability: Availability[ValueT]
    provenance: StateProvenance

    def __post_init__(self) -> None:
        if not isinstance(self.key, StateKey):
            raise TypeError("key должен быть StateKey")
        if not isinstance(self.availability, Available | Unknown | Stale | Unavailable):
            raise TypeError("availability должна быть canonical Availability variant")
        if not isinstance(self.provenance, StateProvenance):
            raise TypeError("provenance должна быть StateProvenance")
        StateEntry(availability=self.availability, provenance=self.provenance)


@dataclass(frozen=True, slots=True)
class BoundaryStateUpdate:
    """Immutable runtime-boundary update относительно exact committed revision."""

    base_state_revision: StateRevision
    producer: RuntimeBoundaryId
    writes: tuple[BoundaryStateWrite[object], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.producer, RuntimeBoundaryId):
            raise TypeError("producer должен быть RuntimeBoundaryId")
        if not isinstance(self.writes, tuple):
            raise TypeError("writes должен быть tuple BoundaryStateWrite")
        if not self.writes:
            raise ValueError("BoundaryStateUpdate должен содержать хотя бы один write")

        paths = set()
        for write in self.writes:
            if not isinstance(write, BoundaryStateWrite):
                raise TypeError("writes должен содержать BoundaryStateWrite")
            if write.key.path in paths:
                raise SchemaError(f"Duplicate StatePath в boundary update: {write.key.path}")
            paths.add(write.key.path)


__all__ = ["BoundaryStateUpdate", "BoundaryStateWrite"]
