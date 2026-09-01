"""Structural module API и staged proposal contracts Core Kernel."""

from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable
from uuid import UUID

from mindra.contracts.availability import Availability, Available, Stale, Unavailable, Unknown
from mindra.contracts.errors import SchemaError
from mindra.contracts.identity import ImplementationId, ModuleAttemptId, ModuleId
from mindra.contracts.provenance import StateProvenance
from mindra.contracts.revisions import PrivateStateRevision, StateRevision
from mindra.contracts.state import ReadSpec, StateEntry, StateKey, StateProjection
from mindra.contracts.time import LogicalTime


@dataclass(frozen=True, slots=True)
class ImplementationRevision:
    """Opaque equality-only token revision concrete implementation."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("ImplementationRevision value должен быть строкой")
        if not self.value or any(
            character.isspace() or not character.isprintable() for character in self.value
        ):
            raise ValueError("ImplementationRevision должен быть непустым opaque revision token")


class ExecutionPhase(Enum):
    """Стандартные execution phases kernel."""

    COGNITIVE_CYCLE = "cognitive_cycle"
    EPISODE_START = "episode_start"
    POST_OUTCOME = "post_outcome"


class ModuleStatefulness(Enum):
    """Declared presence causally relevant module-private state."""

    STATELESS = "stateless"
    STATEFUL = "stateful"


class DeterminismMode(Enum):
    """Declared deterministic behavior trait module implementation."""

    DETERMINISTIC = "deterministic"
    STOCHASTIC = "stochastic"


@dataclass(frozen=True, slots=True)
class ExecutionTraits:
    """Минимальные immutable execution traits v0.1."""

    statefulness: ModuleStatefulness
    determinism: DeterminismMode

    def __post_init__(self) -> None:
        if not isinstance(self.statefulness, ModuleStatefulness):
            raise TypeError("statefulness должен быть ModuleStatefulness")
        if not isinstance(self.determinism, DeterminismMode):
            raise TypeError("determinism должен быть DeterminismMode")


@runtime_checkable
class PrivateStateContract[ValueT](Protocol):
    """Structural validation/freeze contract private payload."""

    def validate(self, value: object) -> None:
        """Fail closed проверить private payload."""
        ...

    def freeze(self, value: object) -> ValueT:
        """Проверить и вернуть snapshot-safe private payload."""
        ...


@dataclass(frozen=True, slots=True)
class PrivateStateDescriptor[ValueT]:
    """Module-owned private-state contract без store/lifecycle behavior."""

    contract: PrivateStateContract[ValueT]

    def __post_init__(self) -> None:
        if not isinstance(self.contract, PrivateStateContract):
            raise TypeError("contract должен структурно удовлетворять PrivateStateContract")


@dataclass(frozen=True, slots=True)
class PrivateStateSnapshot[ValueT]:
    """Immutable committed snapshot own module-private state."""

    module_id: ModuleId
    revision: PrivateStateRevision
    value: ValueT

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        if not isinstance(self.revision, PrivateStateRevision):
            raise TypeError("revision должен быть PrivateStateRevision")


@dataclass(frozen=True, slots=True)
class PrivateStateProposal[ValueT]:
    """Staged private-state update относительно committed revision."""

    module_id: ModuleId
    base_revision: PrivateStateRevision
    module_attempt_id: ModuleAttemptId
    value: ValueT

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        if not isinstance(self.base_revision, PrivateStateRevision):
            raise TypeError("base_revision должен быть PrivateStateRevision")
        if not isinstance(self.module_attempt_id, UUID):
            raise TypeError("module_attempt_id должен быть ModuleAttemptId")


@dataclass(frozen=True, slots=True)
class ModuleExecutionContext:
    """Узкий causal context одного module attempt."""

    module_attempt_id: ModuleAttemptId
    base_state_revision: StateRevision
    logical_time: LogicalTime
    phase: ExecutionPhase

    def __post_init__(self) -> None:
        if not isinstance(self.module_attempt_id, UUID):
            raise TypeError("module_attempt_id должен быть ModuleAttemptId")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.logical_time, LogicalTime):
            raise TypeError("logical_time должен быть LogicalTime")
        if not isinstance(self.phase, ExecutionPhase):
            raise TypeError("phase должен быть ExecutionPhase")


@dataclass(frozen=True, slots=True)
class StateWrite[ValueT]:
    """Typed staged write canonical state без write/commit authority."""

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
class StateUpdateProposal:
    """Immutable uncommitted collection public state writes."""

    base_state_revision: StateRevision
    producer: ModuleId
    module_attempt_id: ModuleAttemptId
    writes: tuple[StateWrite[object], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.producer, ModuleId):
            raise TypeError("producer должен быть ModuleId")
        if not isinstance(self.module_attempt_id, UUID):
            raise TypeError("module_attempt_id должен быть ModuleAttemptId")
        if not isinstance(self.writes, tuple):
            raise TypeError("writes должен быть tuple StateWrite")

        paths = set()
        for write in self.writes:
            if not isinstance(write, StateWrite):
                raise TypeError("writes должен содержать StateWrite")
            if write.key.path in paths:
                raise SchemaError(f"Duplicate StatePath в proposal: {write.key.path}")
            paths.add(write.key.path)


@dataclass(frozen=True, slots=True)
class ModuleDescriptor:
    """Immutable declaration module dependencies, outputs и execution traits."""

    module_id: ModuleId
    implementation_id: ImplementationId
    implementation_revision: ImplementationRevision
    reads: tuple[ReadSpec[object], ...]
    writes: tuple[StateKey[object], ...]
    private_state: PrivateStateDescriptor[object] | None
    phases: frozenset[ExecutionPhase]
    traits: ExecutionTraits

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        if not isinstance(self.implementation_id, ImplementationId):
            raise TypeError("implementation_id должен быть ImplementationId")
        if not isinstance(self.implementation_revision, ImplementationRevision):
            raise TypeError("implementation_revision должен быть ImplementationRevision")
        if not isinstance(self.reads, tuple):
            raise TypeError("reads должен быть tuple ReadSpec")
        if not isinstance(self.writes, tuple):
            raise TypeError("writes должен быть tuple StateKey")
        if not isinstance(self.phases, frozenset):
            raise TypeError("phases должен быть frozenset ExecutionPhase")
        if not self.phases:
            raise ValueError("phases не может быть пустым")
        if any(not isinstance(phase, ExecutionPhase) for phase in self.phases):
            raise TypeError("phases должен содержать ExecutionPhase")
        if not isinstance(self.traits, ExecutionTraits):
            raise TypeError("traits должен быть ExecutionTraits")
        if self.private_state is not None and not isinstance(
            self.private_state, PrivateStateDescriptor
        ):
            raise TypeError("private_state должен быть PrivateStateDescriptor или None")

        read_paths = set()
        for read in self.reads:
            if not isinstance(read, ReadSpec):
                raise TypeError("reads должен содержать ReadSpec")
            if read.key.path in read_paths:
                raise SchemaError(f"Duplicate read StatePath: {read.key.path}")
            read_paths.add(read.key.path)

        write_paths = set()
        for write in self.writes:
            if not isinstance(write, StateKey):
                raise TypeError("writes должен содержать StateKey")
            if write.path in write_paths:
                raise SchemaError(f"Duplicate write StatePath: {write.path}")
            write_paths.add(write.path)

        is_stateful = self.traits.statefulness is ModuleStatefulness.STATEFUL
        if is_stateful != (self.private_state is not None):
            raise ValueError("statefulness и private_state descriptor не согласованы")


@dataclass(frozen=True, slots=True)
class ModuleComputeRequest:
    """Полный и узкий module-facing compute input v0.1."""

    state: StateProjection
    private_state: PrivateStateSnapshot[object] | Unavailable
    context: ModuleExecutionContext

    def __post_init__(self) -> None:
        if not isinstance(self.state, StateProjection):
            raise TypeError("state должен быть StateProjection")
        if not isinstance(self.private_state, PrivateStateSnapshot | Unavailable):
            raise TypeError("private_state должен быть own PrivateStateSnapshot или Unavailable")
        if not isinstance(self.context, ModuleExecutionContext):
            raise TypeError("context должен быть ModuleExecutionContext")


@dataclass(frozen=True, slots=True)
class ModuleComputeResult:
    """Только staged public/private effects module compute."""

    state_update: StateUpdateProposal
    private_state_update: PrivateStateProposal[object] | None

    def __post_init__(self) -> None:
        if not isinstance(self.state_update, StateUpdateProposal):
            raise TypeError("state_update должен быть StateUpdateProposal")
        if self.private_state_update is not None and not isinstance(
            self.private_state_update, PrivateStateProposal
        ):
            raise TypeError("private_state_update должен быть PrivateStateProposal или None")


@runtime_checkable
class CognitiveModule(Protocol):
    """Structural synchronous module compute contract Core Kernel v0.1."""

    descriptor: ModuleDescriptor

    def compute(self, request: ModuleComputeRequest) -> ModuleComputeResult:
        """Вычислить staged result без commit/store access."""
        ...


__all__ = [
    "CognitiveModule",
    "DeterminismMode",
    "ExecutionPhase",
    "ExecutionTraits",
    "ImplementationRevision",
    "ModuleComputeRequest",
    "ModuleComputeResult",
    "ModuleDescriptor",
    "ModuleExecutionContext",
    "ModuleStatefulness",
    "PrivateStateContract",
    "PrivateStateDescriptor",
    "PrivateStateProposal",
    "PrivateStateSnapshot",
    "StateUpdateProposal",
    "StateWrite",
]
