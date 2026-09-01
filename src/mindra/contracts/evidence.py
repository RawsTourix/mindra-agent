"""Immutable structural O0 evidence contracts Core Kernel."""

from dataclasses import dataclass
from enum import Enum
from re import compile as compile_pattern
from typing import Protocol, runtime_checkable
from uuid import UUID

from mindra.contracts.identity import (
    AgentRevisionId,
    BranchId,
    CommitId,
    ExecutionPlanId,
    ImplementationId,
    InterventionId,
    LineageId,
    ModuleAttemptId,
    ModuleId,
    ProfileId,
    WaveAttemptId,
)
from mindra.contracts.modules import (
    DeterminismMode,
    ExecutionPhase,
    ImplementationRevision,
    ModuleStatefulness,
)
from mindra.contracts.revisions import (
    CompositionRevision,
    ExecutionPlanRevision,
    PrivateStateRevision,
    SchemaRevision,
    StateRevision,
)
from mindra.contracts.state import StatePath
from mindra.contracts.time import LogicalTime

_FINGERPRINT_PATTERN = compile_pattern(r"[0-9a-f]{64}")


class TraceEventKind(Enum):
    """Exact structural event kinds Core Kernel v0.1."""

    COMPOSITION_RESOLVED = "composition_resolved"
    PLAN_COMPILED = "plan_compiled"
    CYCLE_STARTED = "cycle_started"
    WAVE_STARTED = "wave_started"
    MODULE_ATTEMPT_STARTED = "module_attempt_started"
    MODULE_ATTEMPT_FINISHED = "module_attempt_finished"
    COMMIT_ATTEMPTED = "commit_attempted"
    COMMIT_SUCCEEDED = "commit_succeeded"
    COMMIT_FAILED = "commit_failed"
    STATE_REVISION_COMMITTED = "state_revision_committed"
    INTERVENTION_APPLIED = "intervention_applied"
    CYCLE_FINISHED = "cycle_finished"
    CYCLE_FAILED = "cycle_failed"
    LIFECYCLE_PHASE_STARTED = "lifecycle_phase_started"
    LIFECYCLE_PHASE_FINISHED = "lifecycle_phase_finished"
    LIFECYCLE_PHASE_FAILED = "lifecycle_phase_failed"


class ModuleAttemptOutcome(Enum):
    """Фактический outcome завершившегося module attempt."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"


def _validate_printable_string(value: object, field_name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} должен быть строкой")
    if not value or not value.isprintable():
        raise ValueError(f"{field_name} должен быть непустой printable строкой")


def _validate_fingerprint(value: object, field_name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} должен быть строкой")
    if _FINGERPRINT_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{field_name} должен быть lowercase SHA-256 hex")


def _validate_uuid(value: object, field_name: str) -> None:
    if not isinstance(value, UUID):
        raise TypeError(f"{field_name} должен быть typed UUID identity")


def _validate_module_ids(
    value: object,
    field_name: str,
    *,
    non_empty: bool,
) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} должен быть tuple ModuleId")
    if non_empty and not value:
        raise ValueError(f"{field_name} не может быть пустым")
    if any(not isinstance(module_id, ModuleId) for module_id in value):
        raise TypeError(f"{field_name} должен содержать ModuleId")
    if value != tuple(sorted(set(value), key=lambda item: item.value)):
        raise ValueError(f"{field_name} должен иметь canonical unique ordering")


def _validate_attempt_ids(value: object, field_name: str) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} должен быть tuple ModuleAttemptId")
    if any(not isinstance(attempt_id, UUID) for attempt_id in value):
        raise TypeError(f"{field_name} должен содержать ModuleAttemptId")
    if len(set(value)) != len(value):
        raise ValueError(f"{field_name} не может содержать duplicate ModuleAttemptId")


def _validate_state_paths(
    value: object,
    field_name: str,
    *,
    non_empty: bool,
) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} должен быть tuple StatePath")
    if non_empty and not value:
        raise ValueError(f"{field_name} не может быть пустым")
    if any(not isinstance(path, StatePath) for path in value):
        raise TypeError(f"{field_name} должен содержать StatePath")
    if value != tuple(sorted(set(value), key=lambda item: item.dotted)):
        raise ValueError(f"{field_name} должен иметь canonical unique ordering")


@dataclass(frozen=True, slots=True)
class TraceFailure:
    """Snapshot-safe diagnostic failure без exception/traceback reference."""

    error_type: str
    message: str

    def __post_init__(self) -> None:
        _validate_printable_string(self.error_type, "error_type")
        _validate_printable_string(self.message, "message")

    @classmethod
    def from_exception(cls, error: BaseException) -> TraceFailure:
        """Скопировать только имя типа и printable diagnostic text exception."""
        if not isinstance(error, BaseException):
            raise TypeError("error должен быть BaseException")
        message = str(error) or "<empty message>"
        return cls(error_type=type(error).__name__, message=message)


@dataclass(frozen=True, slots=True)
class ResolvedModuleTrace:
    """Structural copy resolved module identity и execution traits."""

    module_id: ModuleId
    implementation_id: ImplementationId
    implementation_revision: ImplementationRevision
    statefulness: ModuleStatefulness
    determinism: DeterminismMode

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        if not isinstance(self.implementation_id, ImplementationId):
            raise TypeError("implementation_id должен быть ImplementationId")
        if not isinstance(self.implementation_revision, ImplementationRevision):
            raise TypeError("implementation_revision должен быть ImplementationRevision")
        if not isinstance(self.statefulness, ModuleStatefulness):
            raise TypeError("statefulness должен быть ModuleStatefulness")
        if not isinstance(self.determinism, DeterminismMode):
            raise TypeError("determinism должен быть DeterminismMode")


@dataclass(frozen=True, slots=True)
class PlanDependencyTrace:
    """Structural copy one plan dependency edge."""

    producer: ModuleId
    consumer: ModuleId
    path: StatePath

    def __post_init__(self) -> None:
        if not isinstance(self.producer, ModuleId):
            raise TypeError("producer должен быть ModuleId")
        if not isinstance(self.consumer, ModuleId):
            raise TypeError("consumer должен быть ModuleId")
        if not isinstance(self.path, StatePath):
            raise TypeError("path должен быть StatePath")


def _plan_dependency_key(dependency: PlanDependencyTrace) -> tuple[str, str, str]:
    return (
        dependency.producer.value,
        dependency.consumer.value,
        dependency.path.dotted,
    )


@dataclass(frozen=True, slots=True)
class PlanWaveTrace:
    """Structural copy canonical plan wave."""

    index: int
    module_ids: tuple[ModuleId, ...]

    def __post_init__(self) -> None:
        if type(self.index) is not int:
            raise TypeError("index должен быть целым числом")
        if self.index < 0:
            raise ValueError("index не может быть отрицательным")
        _validate_module_ids(self.module_ids, "module_ids", non_empty=True)


@dataclass(frozen=True, slots=True)
class PrivateRevisionTransitionTrace:
    """Immutable evidence representation committed private revision transition."""

    module_id: ModuleId
    before: PrivateStateRevision
    after: PrivateStateRevision

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        if not isinstance(self.before, PrivateStateRevision):
            raise TypeError("before должен быть PrivateStateRevision")
        if not isinstance(self.after, PrivateStateRevision):
            raise TypeError("after должен быть PrivateStateRevision")
        if self.after != self.before.next():
            raise ValueError("after должен быть ровно before.next()")


@dataclass(frozen=True, slots=True)
class CompositionResolvedEvent:
    """Structural evidence resolved composition без runtime object references."""

    profile_id: ProfileId
    composition_revision: CompositionRevision
    schema_revision: SchemaRevision
    agent_revision_id: AgentRevisionId
    composition_fingerprint: str
    modules: tuple[ResolvedModuleTrace, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.profile_id, ProfileId):
            raise TypeError("profile_id должен быть ProfileId")
        if not isinstance(self.composition_revision, CompositionRevision):
            raise TypeError("composition_revision должен быть CompositionRevision")
        if not isinstance(self.schema_revision, SchemaRevision):
            raise TypeError("schema_revision должен быть SchemaRevision")
        _validate_uuid(self.agent_revision_id, "agent_revision_id")
        _validate_fingerprint(self.composition_fingerprint, "composition_fingerprint")
        if not isinstance(self.modules, tuple):
            raise TypeError("modules должен быть tuple ResolvedModuleTrace")
        if any(not isinstance(module, ResolvedModuleTrace) for module in self.modules):
            raise TypeError("modules должен содержать ResolvedModuleTrace")
        module_ids = tuple(module.module_id for module in self.modules)
        if module_ids != tuple(sorted(set(module_ids), key=lambda item: item.value)):
            raise ValueError("modules должен иметь canonical unique ModuleId ordering")


@dataclass(frozen=True, slots=True)
class PlanCompiledEvent:
    """Structural evidence compiled immutable execution plan."""

    plan_id: ExecutionPlanId
    plan_revision: ExecutionPlanRevision
    composition_revision: CompositionRevision
    schema_revision: SchemaRevision
    phase: ExecutionPhase
    plan_fingerprint: str
    dependencies: tuple[PlanDependencyTrace, ...]
    waves: tuple[PlanWaveTrace, ...]

    def __post_init__(self) -> None:
        _validate_uuid(self.plan_id, "plan_id")
        if not isinstance(self.plan_revision, ExecutionPlanRevision):
            raise TypeError("plan_revision должен быть ExecutionPlanRevision")
        if not isinstance(self.composition_revision, CompositionRevision):
            raise TypeError("composition_revision должен быть CompositionRevision")
        if not isinstance(self.schema_revision, SchemaRevision):
            raise TypeError("schema_revision должен быть SchemaRevision")
        if not isinstance(self.phase, ExecutionPhase):
            raise TypeError("phase должен быть ExecutionPhase")
        _validate_fingerprint(self.plan_fingerprint, "plan_fingerprint")
        if not isinstance(self.dependencies, tuple) or any(
            not isinstance(dependency, PlanDependencyTrace) for dependency in self.dependencies
        ):
            raise TypeError("dependencies должен быть tuple PlanDependencyTrace")
        if self.dependencies != tuple(sorted(self.dependencies, key=_plan_dependency_key)):
            raise ValueError("dependencies должен иметь canonical ordering")
        if not isinstance(self.waves, tuple) or any(
            not isinstance(wave, PlanWaveTrace) for wave in self.waves
        ):
            raise TypeError("waves должен быть tuple PlanWaveTrace")
        if tuple(wave.index for wave in self.waves) != tuple(range(len(self.waves))):
            raise ValueError("wave indices должны идти с 0 без gaps")
        module_ids = tuple(module_id for wave in self.waves for module_id in wave.module_ids)
        if len(module_ids) != len(set(module_ids)):
            raise ValueError("ModuleId может входить максимум в одну plan wave")


@dataclass(frozen=True, slots=True)
class CycleStartedEvent:
    """Structural evidence начала cognitive cycle."""

    base_state_revision: StateRevision
    plan_id: ExecutionPlanId
    plan_revision: ExecutionPlanRevision
    agent_revision_id: AgentRevisionId

    def __post_init__(self) -> None:
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        _validate_uuid(self.plan_id, "plan_id")
        if not isinstance(self.plan_revision, ExecutionPlanRevision):
            raise TypeError("plan_revision должен быть ExecutionPlanRevision")
        _validate_uuid(self.agent_revision_id, "agent_revision_id")


@dataclass(frozen=True, slots=True)
class WaveStartedEvent:
    """Structural evidence начала one wave attempt."""

    wave_attempt_id: WaveAttemptId
    wave_index: int
    base_state_revision: StateRevision
    module_ids: tuple[ModuleId, ...]

    def __post_init__(self) -> None:
        _validate_uuid(self.wave_attempt_id, "wave_attempt_id")
        if type(self.wave_index) is not int:
            raise TypeError("wave_index должен быть целым числом")
        if self.wave_index < 0:
            raise ValueError("wave_index не может быть отрицательным")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        _validate_module_ids(self.module_ids, "module_ids", non_empty=True)


@dataclass(frozen=True, slots=True)
class ModuleAttemptStartedEvent:
    """Structural evidence фактически начатого module attempt."""

    wave_attempt_id: WaveAttemptId
    module_id: ModuleId
    module_attempt_id: ModuleAttemptId
    implementation_id: ImplementationId
    implementation_revision: ImplementationRevision
    base_state_revision: StateRevision
    base_private_revision: PrivateStateRevision | None

    def __post_init__(self) -> None:
        _validate_uuid(self.wave_attempt_id, "wave_attempt_id")
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        _validate_uuid(self.module_attempt_id, "module_attempt_id")
        if not isinstance(self.implementation_id, ImplementationId):
            raise TypeError("implementation_id должен быть ImplementationId")
        if not isinstance(self.implementation_revision, ImplementationRevision):
            raise TypeError("implementation_revision должен быть ImplementationRevision")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if self.base_private_revision is not None and not isinstance(
            self.base_private_revision, PrivateStateRevision
        ):
            raise TypeError("base_private_revision должен быть PrivateStateRevision или None")


@dataclass(frozen=True, slots=True)
class ModuleAttemptFinishedEvent:
    """Structural outcome module compute без O1/O2 payload values."""

    module_id: ModuleId
    module_attempt_id: ModuleAttemptId
    outcome: ModuleAttemptOutcome
    proposed_public_paths: tuple[StatePath, ...]
    private_update_proposed: bool
    failure: TraceFailure | None

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        _validate_uuid(self.module_attempt_id, "module_attempt_id")
        if not isinstance(self.outcome, ModuleAttemptOutcome):
            raise TypeError("outcome должен быть ModuleAttemptOutcome")
        _validate_state_paths(
            self.proposed_public_paths,
            "proposed_public_paths",
            non_empty=False,
        )
        if type(self.private_update_proposed) is not bool:
            raise TypeError("private_update_proposed должен быть bool")
        if self.outcome is ModuleAttemptOutcome.SUCCEEDED:
            if self.failure is not None:
                raise ValueError("Successful module attempt не может содержать failure")
        else:
            if not isinstance(self.failure, TraceFailure):
                raise ValueError("Failed module attempt требует TraceFailure")
            if self.proposed_public_paths or self.private_update_proposed:
                raise ValueError("Failed module attempt не может содержать proposal metadata")


@dataclass(frozen=True, slots=True)
class CommitAttemptedEvent:
    """Structural evidence фактически вызванной commit boundary."""

    wave_attempt_id: WaveAttemptId
    base_state_revision: StateRevision
    module_attempt_ids: tuple[ModuleAttemptId, ...]

    def __post_init__(self) -> None:
        _validate_uuid(self.wave_attempt_id, "wave_attempt_id")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        _validate_attempt_ids(self.module_attempt_ids, "module_attempt_ids")


@dataclass(frozen=True, slots=True)
class CommitSucceededEvent:
    """Structural copy successful commit result без runtime CommitRecord."""

    wave_attempt_id: WaveAttemptId
    commit_id: CommitId
    base_state_revision: StateRevision
    resulting_state_revision: StateRevision
    module_attempt_ids: tuple[ModuleAttemptId, ...]
    public_paths: tuple[StatePath, ...]
    private_revisions: tuple[PrivateRevisionTransitionTrace, ...]

    def __post_init__(self) -> None:
        _validate_uuid(self.wave_attempt_id, "wave_attempt_id")
        _validate_uuid(self.commit_id, "commit_id")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.resulting_state_revision, StateRevision):
            raise TypeError("resulting_state_revision должен быть StateRevision")
        _validate_attempt_ids(self.module_attempt_ids, "module_attempt_ids")
        _validate_state_paths(self.public_paths, "public_paths", non_empty=False)
        if not isinstance(self.private_revisions, tuple) or any(
            not isinstance(transition, PrivateRevisionTransitionTrace)
            for transition in self.private_revisions
        ):
            raise TypeError("private_revisions должен быть tuple PrivateRevisionTransitionTrace")
        module_ids = tuple(transition.module_id for transition in self.private_revisions)
        if module_ids != tuple(sorted(set(module_ids), key=lambda item: item.value)):
            raise ValueError("private_revisions должен иметь canonical unique ordering")
        expected_revision = (
            self.base_state_revision.next() if self.public_paths else self.base_state_revision
        )
        if self.resulting_state_revision != expected_revision:
            raise ValueError("resulting_state_revision не согласована с public_paths")


@dataclass(frozen=True, slots=True)
class CommitFailedEvent:
    """Structural evidence failed commit call, а не module compute failure."""

    wave_attempt_id: WaveAttemptId
    base_state_revision: StateRevision
    module_attempt_ids: tuple[ModuleAttemptId, ...]
    failure: TraceFailure

    def __post_init__(self) -> None:
        _validate_uuid(self.wave_attempt_id, "wave_attempt_id")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        _validate_attempt_ids(self.module_attempt_ids, "module_attempt_ids")
        if not isinstance(self.failure, TraceFailure):
            raise TypeError("failure должен быть TraceFailure")


@dataclass(frozen=True, slots=True)
class StateRevisionCommittedEvent:
    """Evidence фактического public state revision transition."""

    before: StateRevision
    after: StateRevision
    public_paths: tuple[StatePath, ...]
    lineage_id: LineageId
    branch_id: BranchId
    agent_revision_id: AgentRevisionId
    commit_id: CommitId | None
    intervention_id: InterventionId | None

    def __post_init__(self) -> None:
        if not isinstance(self.before, StateRevision):
            raise TypeError("before должен быть StateRevision")
        if not isinstance(self.after, StateRevision):
            raise TypeError("after должен быть StateRevision")
        if self.after != self.before.next():
            raise ValueError("after должен быть ровно before.next()")
        _validate_state_paths(self.public_paths, "public_paths", non_empty=True)
        _validate_uuid(self.lineage_id, "lineage_id")
        _validate_uuid(self.branch_id, "branch_id")
        _validate_uuid(self.agent_revision_id, "agent_revision_id")
        if self.commit_id is not None:
            _validate_uuid(self.commit_id, "commit_id")
        if self.intervention_id is not None:
            _validate_uuid(self.intervention_id, "intervention_id")
        if (self.commit_id is None) == (self.intervention_id is None):
            raise ValueError("Требуется ровно один origin: commit_id XOR intervention_id")


@dataclass(frozen=True, slots=True)
class InterventionAppliedEvent:
    """Structural contract future controlled public state intervention."""

    intervention_id: InterventionId
    base_state_revision: StateRevision
    resulting_state_revision: StateRevision
    target_paths: tuple[StatePath, ...]
    lineage_id: LineageId
    branch_id: BranchId

    def __post_init__(self) -> None:
        _validate_uuid(self.intervention_id, "intervention_id")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.resulting_state_revision, StateRevision):
            raise TypeError("resulting_state_revision должен быть StateRevision")
        if self.resulting_state_revision != self.base_state_revision.next():
            raise ValueError("resulting_state_revision должен быть ровно base.next()")
        _validate_state_paths(self.target_paths, "target_paths", non_empty=True)
        _validate_uuid(self.lineage_id, "lineage_id")
        _validate_uuid(self.branch_id, "branch_id")


@dataclass(frozen=True, slots=True)
class CycleFinishedEvent:
    """Structural evidence successful end cognitive cycle."""

    base_state_revision: StateRevision
    resulting_state_revision: StateRevision

    def __post_init__(self) -> None:
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.resulting_state_revision, StateRevision):
            raise TypeError("resulting_state_revision должен быть StateRevision")
        if self.resulting_state_revision < self.base_state_revision:
            raise ValueError("resulting_state_revision не может быть меньше base")


@dataclass(frozen=True, slots=True)
class CycleFailedEvent:
    """Structural evidence failed cycle без implicit rollback earlier waves."""

    base_state_revision: StateRevision
    current_state_revision: StateRevision
    failure: TraceFailure

    def __post_init__(self) -> None:
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.current_state_revision, StateRevision):
            raise TypeError("current_state_revision должен быть StateRevision")
        if self.current_state_revision < self.base_state_revision:
            raise ValueError("current_state_revision не может быть меньше base")
        if not isinstance(self.failure, TraceFailure):
            raise TypeError("failure должен быть TraceFailure")


def _validate_lifecycle_phase(phase: object) -> None:
    if phase not in (ExecutionPhase.EPISODE_START, ExecutionPhase.POST_OUTCOME):
        raise ValueError("Lifecycle event требует non-cycle ExecutionPhase")


@dataclass(frozen=True, slots=True)
class LifecyclePhaseStartedEvent:
    """Structural evidence начала стандартной lifecycle phase."""

    phase: ExecutionPhase
    base_state_revision: StateRevision
    plan_id: ExecutionPlanId
    plan_revision: ExecutionPlanRevision
    agent_revision_id: AgentRevisionId

    def __post_init__(self) -> None:
        _validate_lifecycle_phase(self.phase)
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        _validate_uuid(self.plan_id, "plan_id")
        if not isinstance(self.plan_revision, ExecutionPlanRevision):
            raise TypeError("plan_revision должен быть ExecutionPlanRevision")
        _validate_uuid(self.agent_revision_id, "agent_revision_id")


@dataclass(frozen=True, slots=True)
class LifecyclePhaseFinishedEvent:
    """Structural evidence успешного завершения lifecycle phase."""

    phase: ExecutionPhase
    base_state_revision: StateRevision
    resulting_state_revision: StateRevision

    def __post_init__(self) -> None:
        _validate_lifecycle_phase(self.phase)
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.resulting_state_revision, StateRevision):
            raise TypeError("resulting_state_revision должен быть StateRevision")
        if self.resulting_state_revision < self.base_state_revision:
            raise ValueError("resulting_state_revision не может быть меньше base")


@dataclass(frozen=True, slots=True)
class LifecyclePhaseFailedEvent:
    """Structural evidence ошибки lifecycle phase без rollback прошлых waves."""

    phase: ExecutionPhase
    base_state_revision: StateRevision
    current_state_revision: StateRevision
    failure: TraceFailure

    def __post_init__(self) -> None:
        _validate_lifecycle_phase(self.phase)
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.current_state_revision, StateRevision):
            raise TypeError("current_state_revision должен быть StateRevision")
        if self.current_state_revision < self.base_state_revision:
            raise ValueError("current_state_revision не может быть меньше base")
        if not isinstance(self.failure, TraceFailure):
            raise TypeError("failure должен быть TraceFailure")


type TraceEventPayload = (
    CompositionResolvedEvent
    | PlanCompiledEvent
    | CycleStartedEvent
    | WaveStartedEvent
    | ModuleAttemptStartedEvent
    | ModuleAttemptFinishedEvent
    | CommitAttemptedEvent
    | CommitSucceededEvent
    | CommitFailedEvent
    | StateRevisionCommittedEvent
    | InterventionAppliedEvent
    | CycleFinishedEvent
    | CycleFailedEvent
    | LifecyclePhaseStartedEvent
    | LifecyclePhaseFinishedEvent
    | LifecyclePhaseFailedEvent
)

_PAYLOAD_KIND: dict[type[object], TraceEventKind] = {
    CompositionResolvedEvent: TraceEventKind.COMPOSITION_RESOLVED,
    PlanCompiledEvent: TraceEventKind.PLAN_COMPILED,
    CycleStartedEvent: TraceEventKind.CYCLE_STARTED,
    WaveStartedEvent: TraceEventKind.WAVE_STARTED,
    ModuleAttemptStartedEvent: TraceEventKind.MODULE_ATTEMPT_STARTED,
    ModuleAttemptFinishedEvent: TraceEventKind.MODULE_ATTEMPT_FINISHED,
    CommitAttemptedEvent: TraceEventKind.COMMIT_ATTEMPTED,
    CommitSucceededEvent: TraceEventKind.COMMIT_SUCCEEDED,
    CommitFailedEvent: TraceEventKind.COMMIT_FAILED,
    StateRevisionCommittedEvent: TraceEventKind.STATE_REVISION_COMMITTED,
    InterventionAppliedEvent: TraceEventKind.INTERVENTION_APPLIED,
    CycleFinishedEvent: TraceEventKind.CYCLE_FINISHED,
    CycleFailedEvent: TraceEventKind.CYCLE_FAILED,
    LifecyclePhaseStartedEvent: TraceEventKind.LIFECYCLE_PHASE_STARTED,
    LifecyclePhaseFinishedEvent: TraceEventKind.LIFECYCLE_PHASE_FINISHED,
    LifecyclePhaseFailedEvent: TraceEventKind.LIFECYCLE_PHASE_FAILED,
}
_CYCLE_SCOPED_KINDS = {
    TraceEventKind.CYCLE_STARTED,
    TraceEventKind.CYCLE_FINISHED,
    TraceEventKind.CYCLE_FAILED,
}
_WAVE_SCOPED_KINDS = {
    TraceEventKind.WAVE_STARTED,
    TraceEventKind.MODULE_ATTEMPT_STARTED,
    TraceEventKind.MODULE_ATTEMPT_FINISHED,
    TraceEventKind.COMMIT_ATTEMPTED,
    TraceEventKind.COMMIT_SUCCEEDED,
    TraceEventKind.COMMIT_FAILED,
}
_LIFECYCLE_PHASE_KINDS = {
    TraceEventKind.LIFECYCLE_PHASE_STARTED,
    TraceEventKind.LIFECYCLE_PHASE_FINISHED,
    TraceEventKind.LIFECYCLE_PHASE_FAILED,
}


@dataclass(frozen=True, slots=True)
class TraceEventEnvelope:
    """Immutable causal envelope one typed O0 event."""

    logical_time: LogicalTime
    payload: TraceEventPayload
    physical_timestamp_ns: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.logical_time, LogicalTime):
            raise TypeError("logical_time должен быть LogicalTime")
        if type(self.payload) not in _PAYLOAD_KIND:
            raise TypeError("payload должен быть exact TraceEventPayload variant")
        if self.physical_timestamp_ns is not None:
            if type(self.physical_timestamp_ns) is not int:
                raise TypeError("physical_timestamp_ns должен быть целым числом или None")
            if self.physical_timestamp_ns < 0:
                raise ValueError("physical_timestamp_ns не может быть отрицательным")
        if self.kind in _CYCLE_SCOPED_KINDS and self.logical_time.cognitive_cycle_id is None:
            raise ValueError(f"{self.kind.value} требует cognitive_cycle_id")
        if self.kind in _WAVE_SCOPED_KINDS and self.logical_time.wave_id is None:
            raise ValueError(f"{self.kind.value} требует wave_id")
        if self.kind in _LIFECYCLE_PHASE_KINDS and (
            self.logical_time.episode_id is None
            or self.logical_time.decision_window_id is None
            or self.logical_time.cognitive_cycle_id is not None
            or self.logical_time.wave_id is not None
        ):
            raise ValueError(f"{self.kind.value} требует DecisionContext без cycle/wave identities")

    @property
    def kind(self) -> TraceEventKind:
        """Вывести exact kind из concrete typed payload."""
        return _PAYLOAD_KIND[type(self.payload)]


@runtime_checkable
class EvidenceRecorder(Protocol):
    """Однонаправленный passive sink уже построенных immutable events."""

    def record(self, event: TraceEventEnvelope, /) -> None:
        """Записать event без изменения cognition или payload."""
        ...


__all__ = [
    "CommitAttemptedEvent",
    "CommitFailedEvent",
    "CommitSucceededEvent",
    "CompositionResolvedEvent",
    "CycleFailedEvent",
    "CycleFinishedEvent",
    "CycleStartedEvent",
    "EvidenceRecorder",
    "InterventionAppliedEvent",
    "LifecyclePhaseFailedEvent",
    "LifecyclePhaseFinishedEvent",
    "LifecyclePhaseStartedEvent",
    "ModuleAttemptFinishedEvent",
    "ModuleAttemptOutcome",
    "ModuleAttemptStartedEvent",
    "PlanCompiledEvent",
    "PlanDependencyTrace",
    "PlanWaveTrace",
    "PrivateRevisionTransitionTrace",
    "ResolvedModuleTrace",
    "StateRevisionCommittedEvent",
    "TraceEventEnvelope",
    "TraceEventKind",
    "TraceEventPayload",
    "TraceFailure",
    "WaveStartedEvent",
]
