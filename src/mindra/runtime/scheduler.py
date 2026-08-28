"""Deterministic cognitive-cycle scheduler Core Kernel v0.1."""

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
    CommitSucceededEvent,
    CycleFailedEvent,
    CycleFinishedEvent,
    CycleStartedEvent,
    EvidenceRecorder,
    ModuleAttemptFinishedEvent,
    ModuleAttemptStartedEvent,
    PrivateRevisionTransitionTrace,
    StateRevisionCommittedEvent,
    TraceEventEnvelope,
    TraceEventPayload,
    TraceFailure,
    WaveStartedEvent,
)
from mindra.contracts.identity import (
    AgentRevisionId,
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
    ModuleComputeResult,
    ModuleExecutionContext,
    PrivateStateSnapshot,
)
from mindra.contracts.revisions import PrivateStateRevision, StateRevision
from mindra.contracts.state import CognitiveState
from mindra.contracts.time import LogicalTime
from mindra.runtime.commit import CommitCoordinator, CommitResult
from mindra.runtime.executor import (
    ModuleAttemptExecutionRequest,
    ModuleAttemptRecord,
    WaveExecutor,
)
from mindra.runtime.planning import ExecutionPlan, ExecutionWave
from mindra.runtime.private_state import PrivateStateStore
from mindra.runtime.state_store import build_state_projection


class CycleExecutionOutcome(Enum):
    """Terminal outcome одного caller-identified cognitive cycle."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class CycleExecutionResult:
    """Фактический current public state после завершившихся wave commits."""

    outcome: CycleExecutionOutcome
    cycle_time: LogicalTime
    base_state_revision: StateRevision
    state: CognitiveState
    completed_waves: int
    failure: TraceFailure | None

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, CycleExecutionOutcome):
            raise TypeError("outcome должен быть CycleExecutionOutcome")
        if not isinstance(self.cycle_time, LogicalTime):
            raise TypeError("cycle_time должен быть LogicalTime")
        if self.cycle_time.cognitive_cycle_id is None or self.cycle_time.wave_id is not None:
            raise ValueError("cycle_time требует cognitive_cycle_id и запрещает wave_id")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.state, CognitiveState):
            raise TypeError("state должен быть CognitiveState")
        if type(self.completed_waves) is not int:
            raise TypeError("completed_waves должен быть целым числом")
        if self.completed_waves < 0:
            raise ValueError("completed_waves не может быть отрицательным")
        if self.outcome is CycleExecutionOutcome.SUCCEEDED:
            if self.failure is not None:
                raise ValueError("Successful cycle не может содержать failure")
        elif not isinstance(self.failure, TraceFailure):
            raise ValueError("Failed cycle требует TraceFailure")


class CognitiveScheduler:
    """Execute one compiled COGNITIVE_CYCLE plan wave-by-wave."""

    __slots__ = (
        "_commit_coordinator",
        "_evidence_recorder",
        "_id_factory",
        "_modules",
        "_plan",
        "_private_store",
        "_wave_executor",
    )

    _plan: ExecutionPlan
    _modules: Mapping[ModuleId, CognitiveModule]
    _private_store: PrivateStateStore
    _commit_coordinator: CommitCoordinator
    _wave_executor: WaveExecutor
    _evidence_recorder: EvidenceRecorder
    _id_factory: IdFactory

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
        if plan.phase is not ExecutionPhase.COGNITIVE_CYCLE:
            raise CompositionError("Scheduler поддерживает только COGNITIVE_CYCLE plan")
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
            missing = sorted(item.value for item in set(plan_descriptors) - set(registered))
            extra = sorted(item.value for item in set(registered) - set(plan_descriptors))
            raise CompositionError(
                f"Concrete modules не совпадают с ExecutionPlan: missing={missing}, extra={extra}"
            )
        for module_id, module in registered.items():
            if module.descriptor != plan_descriptors[module_id]:
                raise CompositionError(
                    f"Concrete module descriptor не совпадает с ExecutionPlan: {module_id}"
                )

        private_store._assert_compatible_descriptors(plan_descriptors)
        commit_coordinator._assert_runtime_binding(
            descriptors=plan.descriptors,
            private_store=private_store,
            schema_revision=plan.schema_revision,
        )

        self._plan = plan
        self._modules = MappingProxyType(registered)
        self._private_store = private_store
        self._commit_coordinator = commit_coordinator
        self._wave_executor = wave_executor
        self._evidence_recorder = evidence_recorder
        self._id_factory = id_factory

    def run_cycle(
        self,
        *,
        current_state: CognitiveState,
        cycle_time: LogicalTime,
    ) -> CycleExecutionResult:
        """Исполнить один caller-identified cognitive cycle."""
        self._validate_cycle_input(current_state=current_state, cycle_time=cycle_time)
        cycle_base_revision = current_state.envelope.state_revision
        cycle_agent_revision_id = current_state.envelope.agent_revision_id
        completed_waves = 0
        state = current_state

        self._record(
            cycle_time,
            CycleStartedEvent(
                base_state_revision=cycle_base_revision,
                plan_id=self._plan.plan_id,
                plan_revision=self._plan.revision,
                agent_revision_id=cycle_agent_revision_id,
            ),
        )

        for wave in self._plan.waves:
            if state.envelope.agent_revision_id != cycle_agent_revision_id:
                failure = TraceFailure.from_exception(
                    WaveExecutionError(
                        f"AgentRevision изменилась до wave {wave.index} текущего cycle"
                    )
                )
                return self._failed_result(
                    cycle_time=cycle_time,
                    cycle_base_revision=cycle_base_revision,
                    state=state,
                    completed_waves=completed_waves,
                    failure=failure,
                )

            wave_base_state = state
            wave_base_revision = state.envelope.state_revision
            wave_id = self._id_factory.new_id(WaveId)
            wave_time = _wave_time(cycle_time, wave_id)
            wave_attempt_id = self._id_factory.new_id(WaveAttemptId)
            try:
                attempts, private_revisions = self._prepare_attempts(
                    wave=wave,
                    base_state=wave_base_state,
                    wave_time=wave_time,
                )
            except Exception as error:
                failure = TraceFailure.from_exception(
                    WaveExecutionError(
                        f"Wave {wave.index} preparation failed: {type(error).__name__}: {error}"
                    )
                )
                return self._failed_result(
                    cycle_time=cycle_time,
                    cycle_base_revision=cycle_base_revision,
                    state=state,
                    completed_waves=completed_waves,
                    failure=failure,
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
                returned_records = self._wave_executor.execute(attempts)
                records = _validate_and_order_records(
                    wave=wave,
                    attempts=attempts,
                    records=returned_records,
                )
            except Exception as error:
                failure = TraceFailure.from_exception(
                    WaveExecutionError(
                        f"Wave {wave.index} executor failed: {type(error).__name__}: {error}"
                    )
                )
                return self._failed_result(
                    cycle_time=cycle_time,
                    cycle_base_revision=cycle_base_revision,
                    state=state,
                    completed_waves=completed_waves,
                    failure=failure,
                )

            for record in records:
                self._record(wave_time, _attempt_finished_event(record))

            first_failure = next((record for record in records if record.failure is not None), None)
            if first_failure is not None:
                underlying = first_failure.failure
                assert underlying is not None
                failure = TraceFailure.from_exception(
                    WaveExecutionError(
                        f"Wave {wave.index} module {first_failure.module_id} failed: "
                        f"{underlying.error_type}: {underlying.message}"
                    )
                )
                return self._failed_result(
                    cycle_time=cycle_time,
                    cycle_base_revision=cycle_base_revision,
                    state=state,
                    completed_waves=completed_waves,
                    failure=failure,
                )

            results = tuple(_successful_result(record) for record in records)
            module_attempt_ids = tuple(record.module_attempt_id for record in records)
            self._record(
                wave_time,
                CommitAttemptedEvent(
                    wave_attempt_id=wave_attempt_id,
                    base_state_revision=wave_base_revision,
                    module_attempt_ids=module_attempt_ids,
                ),
            )
            try:
                commit_result = self._commit_coordinator.commit(
                    current_state=wave_base_state,
                    results=results,
                    logical_time=wave_time,
                )
                _validate_commit_result(
                    result=commit_result,
                    base_revision=wave_base_revision,
                    wave_time=wave_time,
                    agent_revision_id=cycle_agent_revision_id,
                )
            except Exception as error:
                failure = TraceFailure.from_exception(error)
                self._record(
                    wave_time,
                    CommitFailedEvent(
                        wave_attempt_id=wave_attempt_id,
                        base_state_revision=wave_base_revision,
                        module_attempt_ids=module_attempt_ids,
                        failure=failure,
                    ),
                )
                return self._failed_result(
                    cycle_time=cycle_time,
                    cycle_base_revision=cycle_base_revision,
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
            cycle_time,
            CycleFinishedEvent(
                base_state_revision=cycle_base_revision,
                resulting_state_revision=state.envelope.state_revision,
            ),
        )
        return CycleExecutionResult(
            outcome=CycleExecutionOutcome.SUCCEEDED,
            cycle_time=cycle_time,
            base_state_revision=cycle_base_revision,
            state=state,
            completed_waves=completed_waves,
            failure=None,
        )

    def _validate_cycle_input(
        self,
        *,
        current_state: CognitiveState,
        cycle_time: LogicalTime,
    ) -> None:
        if not isinstance(current_state, CognitiveState):
            raise TypeError("current_state должен быть CognitiveState")
        if not isinstance(cycle_time, LogicalTime):
            raise TypeError("cycle_time должен быть LogicalTime")
        if cycle_time.cognitive_cycle_id is None:
            raise ValueError("cycle_time требует cognitive_cycle_id")
        if cycle_time.wave_id is not None:
            raise ValueError("cycle_time не может содержать wave_id")
        if current_state.envelope.schema_revision != self._plan.schema_revision:
            raise CommitValidationError(
                "CognitiveState schema revision не совпадает с ExecutionPlan"
            )
        if current_state.envelope.composition_revision != self._plan.composition_revision:
            raise CommitValidationError(
                "CognitiveState composition revision не совпадает с ExecutionPlan"
            )

        base_time = current_state.envelope.logical_time
        if base_time.run_id != cycle_time.run_id:
            raise CommitValidationError("Cycle не может менять run_id current state")
        if base_time.agent_session_id != cycle_time.agent_session_id:
            raise CommitValidationError("Cycle не может менять agent_session_id current state")
        for field_name in ("episode_id", "decision_window_id"):
            base_value = getattr(base_time, field_name)
            if base_value is not None and base_value != getattr(cycle_time, field_name):
                raise CommitValidationError(
                    f"Cycle logical time несовместим с current state {field_name}"
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
            compute_request = ModuleComputeRequest(
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
                    phase=ExecutionPhase.COGNITIVE_CYCLE,
                ),
            )
            attempts.append(
                ModuleAttemptExecutionRequest(
                    module_id=module_id,
                    module=module,
                    compute_request=compute_request,
                )
            )
        return tuple(attempts), MappingProxyType(private_revisions)

    def _failed_result(
        self,
        *,
        cycle_time: LogicalTime,
        cycle_base_revision: StateRevision,
        state: CognitiveState,
        completed_waves: int,
        failure: TraceFailure,
    ) -> CycleExecutionResult:
        self._record(
            cycle_time,
            CycleFailedEvent(
                base_state_revision=cycle_base_revision,
                current_state_revision=state.envelope.state_revision,
                failure=failure,
            ),
        )
        return CycleExecutionResult(
            outcome=CycleExecutionOutcome.FAILED,
            cycle_time=cycle_time,
            base_state_revision=cycle_base_revision,
            state=state,
            completed_waves=completed_waves,
            failure=failure,
        )

    def _record(self, logical_time: LogicalTime, payload: TraceEventPayload) -> None:
        self._evidence_recorder.record(
            TraceEventEnvelope(logical_time=logical_time, payload=payload)
        )


def _wave_time(cycle_time: LogicalTime, wave_id: WaveId) -> LogicalTime:
    return LogicalTime(
        run_id=cycle_time.run_id,
        agent_session_id=cycle_time.agent_session_id,
        episode_id=cycle_time.episode_id,
        decision_window_id=cycle_time.decision_window_id,
        cognitive_cycle_id=cycle_time.cognitive_cycle_id,
        wave_id=wave_id,
    )


def _validate_and_order_records(
    *,
    wave: ExecutionWave,
    attempts: tuple[ModuleAttemptExecutionRequest, ...],
    records: object,
) -> tuple[ModuleAttemptRecord, ...]:
    if not isinstance(records, tuple):
        raise WaveExecutionError("WaveExecutor должен вернуть tuple ModuleAttemptRecord")
    if len(records) != len(attempts):
        raise WaveExecutionError("WaveExecutor вернул missing/extra attempt records")

    expected = {
        attempt.module_id: attempt.compute_request.context.module_attempt_id for attempt in attempts
    }
    by_module: dict[ModuleId, ModuleAttemptRecord] = {}
    seen_attempt_ids: set[ModuleAttemptId] = set()
    for record in records:
        if not isinstance(record, ModuleAttemptRecord):
            raise WaveExecutionError("WaveExecutor вернул не ModuleAttemptRecord")
        expected_attempt = expected.get(record.module_id)
        if expected_attempt is None or record.module_attempt_id != expected_attempt:
            raise WaveExecutionError("WaveExecutor record identity не совпадает с request")
        if record.module_id in by_module or record.module_attempt_id in seen_attempt_ids:
            raise WaveExecutionError("WaveExecutor вернул duplicate record identity")
        by_module[record.module_id] = record
        seen_attempt_ids.add(record.module_attempt_id)

    if set(by_module) != set(expected):
        raise WaveExecutionError("WaveExecutor вернул missing/extra module records")
    return tuple(by_module[module_id] for module_id in wave.module_ids)


def _attempt_finished_event(record: ModuleAttemptRecord) -> ModuleAttemptFinishedEvent:
    if record.result is None:
        assert record.failure is not None
        return ModuleAttemptFinishedEvent(
            module_id=record.module_id,
            module_attempt_id=record.module_attempt_id,
            outcome=record.outcome,
            proposed_public_paths=(),
            private_update_proposed=False,
            failure=record.failure,
        )
    paths = tuple(
        sorted(
            {write.key.path for write in record.result.state_update.writes},
            key=lambda item: item.dotted,
        )
    )
    return ModuleAttemptFinishedEvent(
        module_id=record.module_id,
        module_attempt_id=record.module_attempt_id,
        outcome=record.outcome,
        proposed_public_paths=paths,
        private_update_proposed=record.result.private_state_update is not None,
        failure=None,
    )


def _successful_result(record: ModuleAttemptRecord) -> ModuleComputeResult:
    if record.result is None:
        raise WaveExecutionError("Failed ModuleAttemptRecord не имеет successful result")
    return record.result


def _validate_commit_result(
    *,
    result: object,
    base_revision: StateRevision,
    wave_time: LogicalTime,
    agent_revision_id: AgentRevisionId,
) -> None:
    if not isinstance(result, CommitResult):
        raise WaveExecutionError("CommitCoordinator должен вернуть CommitResult")
    if result.record.base_state_revision != base_revision:
        raise WaveExecutionError("CommitResult base revision не совпадает с wave base")
    if result.record.logical_time != wave_time:
        raise WaveExecutionError("CommitResult logical time не совпадает с wave time")
    if result.state.envelope.agent_revision_id != agent_revision_id:
        raise WaveExecutionError("CommitResult изменил pinned AgentRevision")


def _commit_succeeded_event(
    wave_attempt_id: WaveAttemptId,
    result: CommitResult,
) -> CommitSucceededEvent:
    record = result.record
    return CommitSucceededEvent(
        wave_attempt_id=wave_attempt_id,
        commit_id=record.commit_id,
        base_state_revision=record.base_state_revision,
        resulting_state_revision=record.resulting_state_revision,
        module_attempt_ids=record.module_attempt_ids,
        public_paths=record.public_paths,
        private_revisions=tuple(
            PrivateRevisionTransitionTrace(
                module_id=transition.module_id,
                before=transition.before,
                after=transition.after,
            )
            for transition in record.private_revisions
        ),
    )


__all__ = ["CognitiveScheduler", "CycleExecutionOutcome", "CycleExecutionResult"]
