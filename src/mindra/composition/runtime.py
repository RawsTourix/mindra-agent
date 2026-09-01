"""Narrow facade одной fully assembled kernel composition."""

from collections.abc import Mapping
from dataclasses import dataclass
from re import compile as compile_pattern
from types import MappingProxyType
from uuid import UUID

from mindra.composition.profile import KernelProfile
from mindra.contracts import (
    CognitiveCycleId,
    CognitiveState,
    CompositionError,
    DecisionContext,
    ExecutionPhase,
    IdFactory,
    InterventionError,
    LogicalTime,
    ModuleDescriptor,
    ProfileId,
    SchemaRevision,
    StateInterventionSpec,
    TraceEventEnvelope,
)
from mindra.contracts.identity import AgentRevisionId
from mindra.contracts.revisions import CompositionRevision
from mindra.runtime import (
    CognitiveScheduler,
    CycleExecutionResult,
    ExecutionPlan,
    InMemoryEvidenceRecorder,
    InterventionGateway,
    InterventionResult,
    LifecycleCoordinator,
    LifecycleExecutionResult,
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
        "_cycle_active",
        "_evidence_recorder",
        "_id_factory",
        "_intervention_gateway",
        "_lifecycle_active",
        "_lifecycle_coordinators",
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
    _intervention_gateway: InterventionGateway
    _cycle_active: bool
    _lifecycle_active: bool
    _lifecycle_coordinators: Mapping[ExecutionPhase, LifecycleCoordinator]

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
        self._cycle_active = True
        try:
            result = self._scheduler.run_cycle(current_state=self._state, cycle_time=cycle_time)
        finally:
            self._cycle_active = False
        self._state = result.state
        return result

    def run_cycle_in(self, context: DecisionContext) -> CycleExecutionResult:
        """Исполнить cycle в заданном caller DecisionContext с runtime-owned ID."""
        self._validate_decision_context(context)
        cycle_time = LogicalTime(
            run_id=context.run_id,
            agent_session_id=context.agent_session_id,
            episode_id=context.episode_id,
            decision_window_id=context.decision_window_id,
            cognitive_cycle_id=self._id_factory.new_id(CognitiveCycleId),
            wave_id=None,
        )
        self._cycle_active = True
        try:
            result = self._scheduler.run_cycle(
                current_state=self._state,
                cycle_time=cycle_time,
            )
        finally:
            self._cycle_active = False
        self._state = result.state
        return result

    def run_lifecycle(
        self,
        phase: ExecutionPhase,
        context: DecisionContext,
    ) -> LifecycleExecutionResult:
        """Исполнить wired стандартную non-cycle phase."""
        if not isinstance(phase, ExecutionPhase):
            raise TypeError("phase должен быть ExecutionPhase")
        if phase is ExecutionPhase.COGNITIVE_CYCLE:
            raise CompositionError("run_lifecycle запрещает COGNITIVE_CYCLE")
        self._validate_decision_context(context)
        coordinator = self._lifecycle_coordinators.get(phase)
        if coordinator is None:
            raise CompositionError(f"Lifecycle phase не wired: {phase.value}")
        phase_time = LogicalTime(
            run_id=context.run_id,
            agent_session_id=context.agent_session_id,
            episode_id=context.episode_id,
            decision_window_id=context.decision_window_id,
            cognitive_cycle_id=None,
            wave_id=None,
        )
        self._lifecycle_active = True
        try:
            result = coordinator.run(current_state=self._state, phase_time=phase_time)
        finally:
            self._lifecycle_active = False
        self._state = result.state
        return result

    def apply_intervention(self, spec: StateInterventionSpec, /) -> InterventionResult:
        """Применить one-shot public treatment только at between-cycle boundary."""
        if not isinstance(spec, StateInterventionSpec):
            raise TypeError("spec должен быть StateInterventionSpec")
        if self._cycle_active or self._lifecycle_active:
            raise InterventionError(
                "Intervention запрещена во время active cognitive cycle или lifecycle phase"
            )
        logical_time = LogicalTime(
            run_id=self._root_time.run_id,
            agent_session_id=self._root_time.agent_session_id,
            episode_id=self._root_time.episode_id,
            decision_window_id=self._root_time.decision_window_id,
            cognitive_cycle_id=None,
            wave_id=None,
        )
        result = self._intervention_gateway.apply(
            current_state=self._state,
            spec=spec,
            logical_time=logical_time,
        )
        self._state = result.state
        return result

    def _validate_decision_context(self, context: DecisionContext) -> None:
        if not isinstance(context, DecisionContext):
            raise TypeError("context должен быть DecisionContext")
        if context.run_id != self._root_time.run_id:
            raise CompositionError("DecisionContext run_id не совпадает с runtime root")
        if context.agent_session_id != self._root_time.agent_session_id:
            raise CompositionError(
                "DecisionContext agent_session_id не совпадает с runtime session"
            )
        state_time = self._state.envelope.logical_time
        if state_time.episode_id != context.episode_id:
            raise CompositionError("DecisionContext episode_id не совпадает с current state")
        if state_time.decision_window_id != context.decision_window_id:
            raise CompositionError(
                "DecisionContext decision_window_id не совпадает с current state"
            )


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
    intervention_gateway: InterventionGateway,
    lifecycle_coordinators: Mapping[ExecutionPhase, LifecycleCoordinator] | None = None,
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
    runtime._intervention_gateway = intervention_gateway
    runtime._cycle_active = False
    runtime._lifecycle_active = False
    coordinators = {} if lifecycle_coordinators is None else dict(lifecycle_coordinators)
    for phase, coordinator in coordinators.items():
        if not isinstance(phase, ExecutionPhase):
            raise TypeError("lifecycle_coordinators keys должны быть ExecutionPhase")
        if not isinstance(coordinator, LifecycleCoordinator):
            raise TypeError("lifecycle_coordinators values должны быть LifecycleCoordinator")
        if phase is ExecutionPhase.COGNITIVE_CYCLE or coordinator.phase is not phase:
            raise CompositionError("Lifecycle coordinator mapping не совпадает с plan phase")
        coordinator._assert_kernel_binding(
            private_store=private_store,
            composition_revision=composition.composition_revision,
            schema_revision=composition.schema_revision,
        )
    runtime._lifecycle_coordinators = MappingProxyType(coordinators)
    return runtime


__all__ = ["CompositionMetadata", "KernelRuntime"]
