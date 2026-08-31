"""Контракты controlled public-state intervention Core Kernel."""

from dataclasses import dataclass
from uuid import UUID

from mindra.contracts.identity import BranchId, LineageId
from mindra.contracts.revisions import StateRevision
from mindra.contracts.state import StatePath


@dataclass(frozen=True, slots=True)
class StateInterventionWrite:
    """Ephemeral запрос one-shot override одного public state field."""

    path: StatePath
    value: object

    def __post_init__(self) -> None:
        if not isinstance(self.path, StatePath):
            raise TypeError("path должен быть StatePath")


@dataclass(frozen=True, slots=True)
class StateInterventionSpec:
    """Atomic intervention batch, привязанный к exact causal base."""

    base_state_revision: StateRevision
    base_lineage_id: LineageId
    base_branch_id: BranchId
    writes: tuple[StateInterventionWrite, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.base_lineage_id, UUID):
            raise TypeError("base_lineage_id должен быть LineageId")
        if not isinstance(self.base_branch_id, UUID):
            raise TypeError("base_branch_id должен быть BranchId")
        if not isinstance(self.writes, tuple):
            raise TypeError("writes должен быть tuple StateInterventionWrite")
        if not self.writes:
            raise ValueError("writes не может быть пустым")
        if any(not isinstance(write, StateInterventionWrite) for write in self.writes):
            raise TypeError("writes должен содержать StateInterventionWrite")

        paths = tuple(write.path for write in self.writes)
        if len(set(paths)) != len(paths):
            raise ValueError("writes не может содержать duplicate StatePath")
        object.__setattr__(
            self,
            "writes",
            tuple(sorted(self.writes, key=lambda item: item.path.dotted)),
        )


@dataclass(frozen=True, slots=True)
class InterventionPolicy:
    """Immutable exact-path allowlist research/control-plane interventions."""

    allowed_paths: tuple[StatePath, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.allowed_paths, tuple):
            raise TypeError("allowed_paths должен быть tuple StatePath")
        if any(not isinstance(path, StatePath) for path in self.allowed_paths):
            raise TypeError("allowed_paths должен содержать StatePath")
        if len(set(self.allowed_paths)) != len(self.allowed_paths):
            raise ValueError("allowed_paths не может содержать duplicate StatePath")
        object.__setattr__(
            self,
            "allowed_paths",
            tuple(sorted(self.allowed_paths, key=lambda item: item.dotted)),
        )

    @classmethod
    def disabled(cls) -> InterventionPolicy:
        """Создать policy, запрещающую все interventions."""
        return cls(())

    @classmethod
    def allowlist(cls, paths: tuple[StatePath, ...], /) -> InterventionPolicy:
        """Создать immutable exact-path allowlist."""
        return cls(paths)

    def allows(self, path: StatePath, /) -> bool:
        """Проверить exact membership без prefix/wildcard semantics."""
        if not isinstance(path, StatePath):
            raise TypeError("path должен быть StatePath")
        return path in self.allowed_paths


__all__ = ["InterventionPolicy", "StateInterventionSpec", "StateInterventionWrite"]
