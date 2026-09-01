"""Исполнение стандартных non-cycle lifecycle phases модулей."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType

from mindra.contracts.errors import (
    CommitValidationError,
    CompositionError,
    DuplicateIdentityError,
    WaveExecutionError,
)
from mindra.contracts.evidence import (
    CommitAttemptedEvent,
    CommitFailedEvent,
    EvidenceRecorder,
    LifecyclePhaseFailedEvent,
    LifecyclePhaseFinishedEvent,
    LifecyclePhaseStartedEvent,
    ModuleAttemptStartedEvent,
    StateRevisionCommittedEvent,
    TraceEventEnvelope,
    TraceEventPayload,
    TraceFailure,
    WaveStartedEvent,
)
from mindra.contracts.identity import (
    IdFactory,
    ModuleAttemptId,
    ModuleId,
    WaveAttemptId,
    WaveId,
)
from mindra.contracts.modules import (
    CognitiveModule,
    ExecutionPhase,
    ModuleComputeRequest,
    ModuleExecutionContext,
    PrivateStateSnapshot,
)
from mindra.contracts.revisions import (
    CompositionRevision,
    PrivateStateRevision,
    SchemaRevision,
    StateRevision,
)
from mindra.contracts.state import CognitiveState
from mindra.contracts.time import LogicalTime
from mindra.runtime.commit import CommitCoordinator
from mindra.runtime.executor import ModuleAttemptExecutionRequest, WaveExecutor
from mindra.runtime.planning import ExecutionPlan, ExecutionWave
from mindra.runtime.private_state import PrivateStateStore
from mindra.runtime.scheduler import (
    _attempt_finished_event,
    _commit_succeeded_event,
    _successful_result,
    _validate_and_order_records,
    _validate_commit_result,
    _validate_result_bindings,
)
from mindra.runtime.state_store import build_state_projection


class LifecycleExecutionOutcome(Enum):
    """Итог исполнения одной стандартной lifecycle phase."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class LifecycleExecutionResult:
    """Фактический current state после lifecycle wave commits."""

    outcome: LifecycleExecutionOutcome
    phase: ExecutionPhase
    phase_time: LogicalTime
    base_state_revision: StateRevision
    state: CognitiveState
    completed_waves: int
    failure: TraceFailure | None

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, LifecycleExecutionOutcome):
            raise TypeError("outcome должен быть LifecycleExecutionOutcome")
        _validate_lifecycle_phase(self.phase)
        if not isinstance(self.phase_time, LogicalTime):
            raise TypeError("phase_time должен быть LogicalTime")
        if (
            self.phase_time.episode_id is None
            or self.phase_time.decision_window_id is None
            or self.phase_time.cognitive_cycle_id is not None
            or self.phase_time.wave_id is not None
        ):
            raise ValueError("phase_time требует DecisionContext и запрещает cycle/wave")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.state, CognitiveState):
            raise TypeError("state должен быть CognitiveState")
        if type(self.completed_waves) is not int or self.completed_waves < 0:
            raise ValueError("completed_waves должен быть non-negative int")
        if self.outcome is LifecycleExecutionOutcome.SUCCEEDED:
            if self.failure is not None:
                raise ValueError("Successful lifecycle phase не может содержать failure")
        elif not isinstance(self.failure, TraceFailure):
            raise ValueError("Failed lifecycle phase требует TraceFailure")


class LifecycleCoordinator:
    """Исполнить один compiled EPISODE_START или POST_OUTCOME plan."""

    __slots__ = (
        "_commit_coordinator",
        "_evidence_recorder",
        "_id_factory",
        "_modules",
        "_plan",
        "_private_store",
        "_wave_executor",
    )

    def __init__(
        self,
        *,
        plan: ExecutionPlan,
        modules: tuple[CognitiveModule, ...],
        private_store: PrivateStateStore,
        commit_coordinator: CommitCoordinator,
        wave_executor: WaveExecutor,
        evidence_recorder: EvidenceRecorder,
        id_factory: IdFactory,
    ) -> None:
        if not isinstance(plan, ExecutionPlan):
            raise TypeError("plan должен быть compiled ExecutionPlan")
        _validate_lifecycle_phase(plan.phase)
        if not isinstance(modules, tuple):
            raise TypeError("modules должен быть tuple CognitiveModule")
        if not isinstance(private_store, PrivateStateStore):
            raise TypeError("private_store должен быть PrivateStateStore")
        if not isinstance(commit_coordinator, CommitCoordinator):
            raise TypeError("commit_coordinator должен быть CommitCoordinator")
        if not isinstance(wave_executor, WaveExecutor):
            raise TypeError("wave_executor должен удовлетворять WaveExecutor")
        if not isinstance(evidence_recorder, EvidenceRecorder):
            raise TypeError("evidence_recorder должен удовлетворять EvidenceRecorder")
        if not callable(getattr(id_factory, "new_id", None)):
            raise TypeError("id_factory должен удовлетворять IdFactory")

        registered: dict[ModuleId, CognitiveModule] = {}
        for module in modules:
            if not isinstance(module, CognitiveModule):
                raise TypeError("modules должен содержать CognitiveModule")
            module_id = module.descriptor.module_id
            if module_id in registered:
                raise DuplicateIdentityError(f"Duplicate concrete ModuleId: {module_id}")
            registered[module_id] = module

        plan_descriptors = {descriptor.module_id: descriptor for descriptor in plan.descriptors}
        if set(registered) != set(plan_descriptors):
            raise CompositionError("Concrete modules не совпадают с lifecycle plan")
        for module_id, module in registered.items():
            if module.descriptor != plan_descriptors[module_id]:
                raise CompositionError(
                    f"Concrete module descriptor не совпадает с plan: {module_id}"
                )
        commit_coordinator._assert_runtime_binding(
            descriptors=plan.descriptors,
            private_store=private_store,
            schema_revision=plan.schema_revision,
            phase=plan.phase,
        )

        self._plan = plan
        self._modules = MappingProxyType(registered)
        self._private_store = private_store
        self._commit_coordinator = commit_coordinator
        self._wave_executor = wave_executor
        self._evidence_recorder = evidence_recorder
        self._id_factory = id_factory

    @property
    def phase(self) -> ExecutionPhase:
        """Вернуть exact phase compiled plan."""
        return self._plan.phase

    def _assert_kernel_binding(
        self,
        *,
        private_store: PrivateStateStore,
        composition_revision: CompositionRevision,
        schema_revision: SchemaRevision,
    ) -> None:
        """Подтвердить composition-wide runtime binding без выдачи authority."""
        if private_store is not self._private_store:
            raise CompositionError(
                "KernelRuntime и LifecycleCoordinator должны использовать один PrivateStateStore"
            )
        if not isinstance(composition_revision, CompositionRevision):
            raise TypeError("composition_revision должна быть CompositionRevision")
        if not isinstance(schema_revision, SchemaRevision):
            raise TypeError("schema_revision должна быть SchemaRevision")
        if self._plan.composition_revision != composition_revision:
            raise CompositionError(
                "Lifecycle plan composition revision не совпадает с KernelRuntime"
            )
        if self._plan.schema_revision != schema_revision:
            raise CompositionError("Lifecycle plan schema revision не совпадает с KernelRuntime")

    def run(
        self,
        *,
        current_state: CognitiveState,
        phase_time: LogicalTime,
    ) -> LifecycleExecutionResult:
        """Исполнить одну standardized lifecycle phase."""
        self._validate_input(current_state=current_state, phase_time=phase_time)
        base_revision = current_state.envelope.state_revision
        agent_revision_id = current_state.envelope.agent_revision_id
        state = current_state
        completed_waves = 0
        self._record(
            phase_time,
            LifecyclePhaseStartedEvent(
                phase=self._plan.phase,
                base_state_revision=base_revision,
                plan_id=self._plan.plan_id,
                plan_revision=self._plan.revision,
                agent_revision_id=agent_revision_id,
            ),
        )

        for wave in self._plan.waves:
            if state.envelope.agent_revision_id != agent_revision_id:
                return self._failed_result(
                    phase_time=phase_time,
                    base_revision=base_revision,
                    state=state,
                    completed_waves=completed_waves,
                    failure=TraceFailure.from_exception(
                        WaveExecutionError("AgentRevision изменилась в lifecycle phase")
                    ),
                )
            wave_base_state = state
            wave_base_revision = state.envelope.state_revision
            wave_time = _lifecycle_wave_time(phase_time, self._id_factory.new_id(WaveId))
            wave_attempt_id = self._id_factory.new_id(WaveAttemptId)
            try:
                attempts, private_revisions = self._prepare_attempts(
                    wave=wave,
                    base_state=wave_base_state,
                    wave_time=wave_time,
                )
            except Exception as error:
                return self._failed_result(
                    phase_time=phase_time,
                    base_revision=base_revision,
                    state=state,
                    completed_waves=completed_waves,
                    failure=TraceFailure.from_exception(
                        WaveExecutionError(
                            f"Lifecycle wave {wave.index} preparation failed: "
                            f"{type(error).__name__}: {error}"
                        )
                    ),
                )

            self._record(
                wave_time,
                WaveStartedEvent(
                    wave_attempt_id=wave_attempt_id,
                    wave_index=wave.index,
                    base_state_revision=wave_base_revision,
                    module_ids=wave.module_ids,
                ),
            )
            for attempt in attempts:
                descriptor = attempt.module.descriptor
                self._record(
                    wave_time,
                    ModuleAttemptStartedEvent(
                        wave_attempt_id=wave_attempt_id,
                        module_id=attempt.module_id,
                        module_attempt_id=attempt.compute_request.context.module_attempt_id,
                        implementation_id=descriptor.implementation_id,
                        implementation_revision=descriptor.implementation_revision,
                        base_state_revision=wave_base_revision,
                        base_private_revision=private_revisions[attempt.module_id],
                    ),
                )

            try:
                records = _validate_and_order_records(
                    wave=wave,
                    attempts=attempts,
                    records=self._wave_executor.execute(attempts),
                )
            except Exception as error:
                return self._failed_result(
                    phase_time=phase_time,
                    base_revision=base_revision,
                    state=state,
                    completed_waves=completed_waves,
                    failure=TraceFailure.from_exception(
                        WaveExecutionError(
                            f"Lifecycle wave {wave.index} executor failed: "
                            f"{type(error).__name__}: {error}"
                        )
                    ),
                )
            for record in records:
                self._record(wave_time, _attempt_finished_event(record))
            first_failure = next((record for record in records if record.failure is not None), None)
            if first_failure is not None:
                underlying = first_failure.failure
                assert underlying is not None
                return self._failed_result(
                    phase_time=phase_time,
                    base_revision=base_revision,
                    state=state,
                    completed_waves=completed_waves,
                    failure=TraceFailure.from_exception(
                        WaveExecutionError(
                            f"Lifecycle wave {wave.index} module "
                            f"{first_failure.module_id} failed: "
                            f"{underlying.error_type}: {underlying.message}"
                        )
                    ),
                )
            try:
                _validate_result_bindings(wave=wave, records=records)
            except WaveExecutionError as error:
                return self._failed_result(
                    phase_time=phase_time,
                    base_revision=base_revision,
                    state=state,
                    completed_waves=completed_waves,
                    failure=TraceFailure.from_exception(error),
                )

            results = tuple(_successful_result(record) for record in records)
            attempt_ids = tuple(record.module_attempt_id for record in records)
            self._record(
                wave_time,
                CommitAttemptedEvent(
                    wave_attempt_id=wave_attempt_id,
                    base_state_revision=wave_base_revision,
                    module_attempt_ids=attempt_ids,
                ),
            )
            try:
                commit_result = self._commit_coordinator.commit(
                    current_state=wave_base_state,
                    results=results,
                    logical_time=wave_time,
                    phase=self._plan.phase,
                )
                _validate_commit_result(
                    result=commit_result,
                    base_revision=wave_base_revision,
                    wave_time=wave_time,
                    agent_revision_id=agent_revision_id,
                )
            except Exception as error:
                failure = TraceFailure.from_exception(error)
                self._record(
                    wave_time,
                    CommitFailedEvent(
                        wave_attempt_id=wave_attempt_id,
                        base_state_revision=wave_base_revision,
                        module_attempt_ids=attempt_ids,
                        failure=failure,
                    ),
                )
                return self._failed_result(
                    phase_time=phase_time,
                    base_revision=base_revision,
                    state=state,
                    completed_waves=completed_waves,
                    failure=failure,
                )

            state = commit_result.state
            self._record(wave_time, _commit_succeeded_event(wave_attempt_id, commit_result))
            if commit_result.record.resulting_state_revision != wave_base_revision:
                self._record(
                    wave_time,
                    StateRevisionCommittedEvent(
                        before=wave_base_revision,
                        after=commit_result.record.resulting_state_revision,
                        public_paths=commit_result.record.public_paths,
                        lineage_id=state.envelope.lineage_id,
                        branch_id=state.envelope.branch_id,
                        agent_revision_id=state.envelope.agent_revision_id,
                        commit_id=commit_result.record.commit_id,
                        intervention_id=None,
                    ),
                )
            completed_waves += 1

        self._record(
            phase_time,
            LifecyclePhaseFinishedEvent(
                phase=self._plan.phase,
                base_state_revision=base_revision,
                resulting_state_revision=state.envelope.state_revision,
            ),
        )
        return LifecycleExecutionResult(
            outcome=LifecycleExecutionOutcome.SUCCEEDED,
            phase=self._plan.phase,
            phase_time=phase_time,
            base_state_revision=base_revision,
            state=state,
            completed_waves=completed_waves,
            failure=None,
        )

    def _validate_input(self, *, current_state: CognitiveState, phase_time: LogicalTime) -> None:
        if not isinstance(current_state, CognitiveState):
            raise TypeError("current_state должен быть CognitiveState")
        if not isinstance(phase_time, LogicalTime):
            raise TypeError("phase_time должен быть LogicalTime")
        if (
            phase_time.episode_id is None
            or phase_time.decision_window_id is None
            or phase_time.cognitive_cycle_id is not None
            or phase_time.wave_id is not None
        ):
            raise ValueError("phase_time требует DecisionContext без cycle/wave")
        if current_state.envelope.schema_revision != self._plan.schema_revision:
            raise CommitValidationError("State schema revision не совпадает с plan")
        if current_state.envelope.composition_revision != self._plan.composition_revision:
            raise CommitValidationError("State composition revision не совпадает с plan")
        base_time = current_state.envelope.logical_time
        for field_name in (
            "run_id",
            "agent_session_id",
            "episode_id",
            "decision_window_id",
        ):
            if getattr(base_time, field_name) != getattr(phase_time, field_name):
                raise CommitValidationError(
                    f"Lifecycle logical time несовместим с current state {field_name}"
                )

    def _prepare_attempts(
        self,
        *,
        wave: ExecutionWave,
        base_state: CognitiveState,
        wave_time: LogicalTime,
    ) -> tuple[
        tuple[ModuleAttemptExecutionRequest, ...],
        Mapping[ModuleId, PrivateStateRevision | None],
    ]:
        attempts: list[ModuleAttemptExecutionRequest] = []
        private_revisions: dict[ModuleId, PrivateStateRevision | None] = {}
        for module_id in wave.module_ids:
            module = self._modules[module_id]
            private_state = self._private_store.snapshot_for(module_id)
            private_revisions[module_id] = (
                private_state.revision if isinstance(private_state, PrivateStateSnapshot) else None
            )
            module_attempt_id = self._id_factory.new_id(ModuleAttemptId)
            request = ModuleComputeRequest(
                state=build_state_projection(
                    base_state=base_state,
                    read_specs=module.descriptor.reads,
                    logical_time=wave_time,
                ),
                private_state=private_state,
                context=ModuleExecutionContext(
                    module_attempt_id=module_attempt_id,
                    base_state_revision=base_state.envelope.state_revision,
                    logical_time=wave_time,
                    phase=self._plan.phase,
                ),
            )
            attempts.append(
                ModuleAttemptExecutionRequest(
                    module_id=module_id,
                    module=module,
                    compute_request=request,
                )
            )
        return tuple(attempts), MappingProxyType(private_revisions)

    def _failed_result(
        self,
        *,
        phase_time: LogicalTime,
        base_revision: StateRevision,
        state: CognitiveState,
        completed_waves: int,
        failure: TraceFailure,
    ) -> LifecycleExecutionResult:
        self._record(
            phase_time,
            LifecyclePhaseFailedEvent(
                phase=self._plan.phase,
                base_state_revision=base_revision,
                current_state_revision=state.envelope.state_revision,
                failure=failure,
            ),
        )
        return LifecycleExecutionResult(
            outcome=LifecycleExecutionOutcome.FAILED,
            phase=self._plan.phase,
            phase_time=phase_time,
            base_state_revision=base_revision,
            state=state,
            completed_waves=completed_waves,
            failure=failure,
        )

    def _record(self, logical_time: LogicalTime, payload: TraceEventPayload) -> None:
        self._evidence_recorder.record(
            TraceEventEnvelope(logical_time=logical_time, payload=payload)
        )


def _validate_lifecycle_phase(phase: object) -> None:
    if phase not in (ExecutionPhase.EPISODE_START, ExecutionPhase.POST_OUTCOME):
        raise CompositionError("LifecycleCoordinator запрещает COGNITIVE_CYCLE plan")


def _lifecycle_wave_time(phase_time: LogicalTime, wave_id: WaveId) -> LogicalTime:
    return LogicalTime(
        run_id=phase_time.run_id,
        agent_session_id=phase_time.agent_session_id,
        episode_id=phase_time.episode_id,
        decision_window_id=phase_time.decision_window_id,
        cognitive_cycle_id=None,
        wave_id=wave_id,
    )


__all__ = [
    "LifecycleCoordinator",
    "LifecycleExecutionOutcome",
    "LifecycleExecutionResult",
]
