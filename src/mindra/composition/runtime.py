"""Narrow facade одной fully assembled kernel composition."""

from dataclasses import dataclass
from re import compile as compile_pattern
from uuid import UUID

from mindra.composition.profile import KernelProfile
from mindra.contracts import (
    CognitiveCycleId,
    CognitiveState,
    IdFactory,
    LogicalTime,
    ModuleDescriptor,
    ProfileId,
    SchemaRevision,
    TraceEventEnvelope,
)
from mindra.contracts.identity import AgentRevisionId
from mindra.contracts.revisions import CompositionRevision
from mindra.runtime import (
    CognitiveScheduler,
    CycleExecutionResult,
    ExecutionPlan,
    InMemoryEvidenceRecorder,
    PrivateStateStore,
)

_FINGERPRINT_PATTERN = compile_pattern(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class CompositionMetadata:
    """Immutable structural metadata resolved active composition."""

    profile_id: ProfileId
    composition_revision: CompositionRevision
    schema_revision: SchemaRevision
    agent_revision_id: AgentRevisionId
    fingerprint: str
    descriptors: tuple[ModuleDescriptor, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.profile_id, ProfileId):
            raise TypeError("profile_id должен быть ProfileId")
        if not isinstance(self.composition_revision, CompositionRevision):
            raise TypeError("composition_revision должен быть CompositionRevision")
        if not isinstance(self.schema_revision, SchemaRevision):
            raise TypeError("schema_revision должен быть SchemaRevision")
        if not isinstance(self.agent_revision_id, UUID):
            raise TypeError("agent_revision_id должен быть AgentRevisionId")
        if (
            not isinstance(self.fingerprint, str)
            or _FINGERPRINT_PATTERN.fullmatch(self.fingerprint) is None
        ):
            raise ValueError("fingerprint должен быть lowercase SHA-256")
        if not isinstance(self.descriptors, tuple) or any(
            not isinstance(descriptor, ModuleDescriptor) for descriptor in self.descriptors
        ):
            raise TypeError("descriptors должен быть tuple ModuleDescriptor")
        canonical = tuple(sorted(self.descriptors, key=lambda item: item.module_id.value))
        if self.descriptors != canonical or len({item.module_id for item in canonical}) != len(
            canonical
        ):
            raise ValueError("descriptors должен иметь canonical unique ModuleId ordering")


class KernelRuntime:
    """Владелец current state и narrow no-argument cycle facade."""

    __slots__ = (
        "_composition",
        "_evidence_recorder",
        "_id_factory",
        "_plan",
        "_private_store",
        "_profile",
        "_root_time",
        "_scheduler",
        "_state",
    )

    _profile: KernelProfile
    _composition: CompositionMetadata
    _plan: ExecutionPlan
    _state: CognitiveState
    _private_store: PrivateStateStore
    _scheduler: CognitiveScheduler
    _evidence_recorder: InMemoryEvidenceRecorder
    _id_factory: IdFactory
    _root_time: LogicalTime

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise TypeError("KernelRuntime создаётся только CompositionRoot")

    @property
    def profile(self) -> KernelProfile:
        """Вернуть immutable source profile."""
        return self._profile

    @property
    def composition(self) -> CompositionMetadata:
        """Вернуть immutable resolved composition metadata."""
        return self._composition

    @property
    def plan(self) -> ExecutionPlan:
        """Вернуть active compiler-built execution plan."""
        return self._plan

    @property
    def state(self) -> CognitiveState:
        """Вернуть current committed public state."""
        return self._state

    def evidence_snapshot(self) -> tuple[TraceEventEnvelope, ...]:
        """Вернуть immutable structural evidence snapshot."""
        return self._evidence_recorder.snapshot()

    def run_cycle(self) -> CycleExecutionResult:
        """Создать новую cycle identity и исполнить active compiled plan."""
        cycle_time = LogicalTime(
            run_id=self._root_time.run_id,
            agent_session_id=self._root_time.agent_session_id,
            episode_id=self._root_time.episode_id,
            decision_window_id=self._root_time.decision_window_id,
            cognitive_cycle_id=self._id_factory.new_id(CognitiveCycleId),
            wave_id=None,
        )
        result = self._scheduler.run_cycle(current_state=self._state, cycle_time=cycle_time)
        self._state = result.state
        return result


def _build_kernel_runtime(
    *,
    profile: KernelProfile,
    composition: CompositionMetadata,
    plan: ExecutionPlan,
    state: CognitiveState,
    private_store: PrivateStateStore,
    scheduler: CognitiveScheduler,
    evidence_recorder: InMemoryEvidenceRecorder,
    id_factory: IdFactory,
    root_time: LogicalTime,
) -> KernelRuntime:
    """Internal construction после полного assembly/validation."""
    runtime = object.__new__(KernelRuntime)
    runtime._profile = profile
    runtime._composition = composition
    runtime._plan = plan
    runtime._state = state
    runtime._private_store = private_store
    runtime._scheduler = scheduler
    runtime._evidence_recorder = evidence_recorder
    runtime._id_factory = id_factory
    runtime._root_time = root_time
    return runtime


__all__ = ["CompositionMetadata", "KernelRuntime"]
