"""Общие test-only fixtures deterministic Scheduler integration."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast
from uuid import UUID

from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    Available,
    BranchId,
    CognitiveCycleId,
    CognitiveState,
    CompositionRevision,
    DecisionWindowId,
    DeterminismMode,
    EpisodeId,
    ExecutionPhase,
    ExecutionPlanRevision,
    ExecutionTraits,
    FreshnessMode,
    ImplementationId,
    ImplementationRevision,
    LineageId,
    LogicalTime,
    ModuleComputeRequest,
    ModuleComputeResult,
    ModuleDescriptor,
    ModuleId,
    ModuleStatefulness,
    PrivateStateDescriptor,
    PrivateStateProposal,
    PrivateStateSnapshot,
    ReadSpec,
    RunId,
    RuntimeBoundaryId,
    SchemaRevision,
    StateEntry,
    StateEnvelope,
    StateFieldSpec,
    StateKey,
    StatePath,
    StateProvenance,
    StateRevision,
    StateSchema,
    StateUpdateProposal,
    StateWrite,
    ValueContract,
)
from mindra.runtime import (
    CognitiveScheduler,
    CommitCoordinator,
    DeterministicIdFactory,
    ExecutionPlan,
    ExecutionPlanCompiler,
    InMemoryEvidenceRecorder,
    PrivateStateStore,
    SequentialWaveExecutor,
    WaveExecutor,
    build_cognitive_state,
)


class TestModule:
    """Test-only pure module с наблюдаемыми received requests."""

    __test__ = False
    __slots__ = ("_compute", "descriptor", "requests")

    def __init__(
        self,
        descriptor: ModuleDescriptor,
        compute: Callable[[ModuleComputeRequest], ModuleComputeResult],
    ) -> None:
        self.descriptor = descriptor
        self._compute = compute
        self.requests: list[ModuleComputeRequest] = []

    def compute(self, request: ModuleComputeRequest) -> ModuleComputeResult:
        """Записать request и выполнить pure test behavior."""
        self.requests.append(request)
        return self._compute(request)

    def set_compute(
        self,
        compute: Callable[[ModuleComputeRequest], ModuleComputeResult],
    ) -> None:
        """Заменить test-only behavior для failure scenario."""
        self._compute = compute

    @property
    def compute_function(self) -> Callable[[ModuleComputeRequest], ModuleComputeResult]:
        """Вернуть текущий test-only behavior без выполнения."""
        return self._compute


@dataclass(frozen=True, slots=True)
class SchedulerTestContext:
    """Полная active runtime fixture одного two-wave plan."""

    schema: StateSchema
    descriptors: tuple[ModuleDescriptor, ...]
    modules: tuple[TestModule, ...]
    plan: ExecutionPlan
    store: PrivateStateStore
    coordinator: CommitCoordinator
    recorder: InMemoryEvidenceRecorder
    scheduler: CognitiveScheduler
    state: CognitiveState
    previous_cycle_time: LogicalTime
    cycle_time: LogicalTime
    keys: dict[str, StateKey[int]]


def make_scheduler_context(
    *,
    wave_executor: WaveExecutor | None = None,
    alpha_compute: Callable[[ModuleComputeRequest], ModuleComputeResult] | None = None,
) -> SchedulerTestContext:
    """Создать alpha -> (beta, gamma) plan с stateful alpha."""
    keys = {
        name: StateKey[int](StatePath.from_dotted(f"scheduler.{name}.value"))
        for name in ("alpha", "beta", "gamma")
    }
    alpha_id = ModuleId("scheduler.alpha")
    beta_id = ModuleId("scheduler.beta")
    gamma_id = ModuleId("scheduler.gamma")
    alpha = _descriptor(alpha_id, keys["alpha"], reads=(), stateful=True)
    current_alpha = cast(
        ReadSpec[object],
        ReadSpec(
            key=keys["alpha"],
            required=True,
            allowed_availability=frozenset({Available}),
            freshness=FreshnessMode.CURRENT_CYCLE,
        ),
    )
    beta = _descriptor(beta_id, keys["beta"], reads=(current_alpha,), stateful=False)
    gamma = _descriptor(gamma_id, keys["gamma"], reads=(current_alpha,), stateful=False)
    descriptors = (gamma, alpha, beta)
    schema = StateSchema(
        SchemaRevision.initial(),
        tuple(
            cast(
                StateFieldSpec[object],
                StateFieldSpec(
                    key=keys[name],
                    owner={"alpha": alpha_id, "beta": beta_id, "gamma": gamma_id}[name],
                    value_contract=ValueContract(int),
                ),
            )
            for name in ("alpha", "beta", "gamma")
        ),
    )
    composition_revision = CompositionRevision.initial()
    plan = ExecutionPlanCompiler(DeterministicIdFactory(UUID(int=100), "scheduler-plan")).compile(
        descriptors,
        schema,
        composition_revision=composition_revision,
        plan_revision=ExecutionPlanRevision.initial(),
    )

    previous_cycle_time = _cycle_time(10)
    cycle_time = _cycle_time(11)
    envelope = StateEnvelope(
        schema_revision=schema.revision,
        state_revision=StateRevision.initial(),
        parent_state_revision=None,
        lineage_id=LineageId(UUID(int=20)),
        branch_id=BranchId(UUID(int=21)),
        agent_revision_id=AgentRevisionId(UUID(int=22)),
        logical_time=previous_cycle_time,
        composition_revision=composition_revision,
    )
    entries = {
        keys[name].path: StateEntry(
            availability=Available(value),
            provenance=StateProvenance(
                producer=RuntimeBoundaryId("runtime.initialization"),
                base_state_revision=StateRevision.initial(),
                logical_time=previous_cycle_time,
            ),
        )
        for name, value in {"alpha": 1, "beta": 2, "gamma": 3}.items()
    }
    state = build_cognitive_state(schema=schema, envelope=envelope, entries=entries)
    store = PrivateStateStore(descriptors, {alpha_id: 10})

    alpha_behavior = alpha_compute or _write_behavior(alpha, keys["alpha"], lambda _value: 2)
    beta_behavior = _write_behavior(beta, keys["beta"], lambda value: value * 2)
    gamma_behavior = _write_behavior(gamma, keys["gamma"], lambda value: value * 3)
    modules = (
        TestModule(gamma, gamma_behavior),
        TestModule(alpha, alpha_behavior),
        TestModule(beta, beta_behavior),
    )
    coordinator = CommitCoordinator(
        schema=schema,
        descriptors=descriptors,
        private_store=store,
        id_factory=DeterministicIdFactory(UUID(int=101), "scheduler-commit"),
    )
    recorder = InMemoryEvidenceRecorder()
    scheduler = CognitiveScheduler(
        plan=plan,
        modules=modules,
        private_store=store,
        commit_coordinator=coordinator,
        wave_executor=wave_executor or SequentialWaveExecutor(),
        evidence_recorder=recorder,
        id_factory=DeterministicIdFactory(UUID(int=102), "scheduler-runtime"),
    )
    return SchedulerTestContext(
        schema=schema,
        descriptors=descriptors,
        modules=modules,
        plan=plan,
        store=store,
        coordinator=coordinator,
        recorder=recorder,
        scheduler=scheduler,
        state=state,
        previous_cycle_time=previous_cycle_time,
        cycle_time=cycle_time,
        keys=keys,
    )


def module_for(context: SchedulerTestContext, name: str) -> TestModule:
    """Найти concrete test module по semantic suffix."""
    return next(
        module
        for module in context.modules
        if module.descriptor.module_id == ModuleId(f"scheduler.{name}")
    )


def _descriptor(
    module_id: ModuleId,
    key: StateKey[int],
    *,
    reads: tuple[ReadSpec[object], ...],
    stateful: bool,
) -> ModuleDescriptor:
    return ModuleDescriptor(
        module_id=module_id,
        implementation_id=ImplementationId(f"test.{module_id.value}.v1"),
        implementation_revision=ImplementationRevision("v1"),
        reads=reads,
        writes=(cast(StateKey[object], key),),
        private_state=(
            cast(
                PrivateStateDescriptor[object],
                PrivateStateDescriptor(ValueContract(int)),
            )
            if stateful
            else None
        ),
        phases=frozenset({ExecutionPhase.COGNITIVE_CYCLE}),
        traits=ExecutionTraits(
            statefulness=(
                ModuleStatefulness.STATEFUL if stateful else ModuleStatefulness.STATELESS
            ),
            determinism=DeterminismMode.DETERMINISTIC,
        ),
    )


def _write_behavior(
    descriptor: ModuleDescriptor,
    output_key: StateKey[int],
    transform: Callable[[int], int],
) -> Callable[[ModuleComputeRequest], ModuleComputeResult]:
    def compute(request: ModuleComputeRequest) -> ModuleComputeResult:
        input_value = 0
        if descriptor.reads:
            entry = request.state.read(cast(StateKey[int], descriptor.reads[0].key))
            assert isinstance(entry.availability, Available)
            input_value = entry.availability.value
        output_value = transform(input_value)
        attempt_id = request.context.module_attempt_id
        write = cast(
            StateWrite[object],
            StateWrite(
                key=output_key,
                availability=Available(output_value),
                provenance=StateProvenance(
                    producer=descriptor.module_id,
                    implementation_id=descriptor.implementation_id,
                    base_state_revision=request.context.base_state_revision,
                    module_attempt_id=attempt_id,
                    logical_time=request.context.logical_time,
                ),
            ),
        )
        private_update = None
        if isinstance(request.private_state, PrivateStateSnapshot):
            private_update = PrivateStateProposal(
                module_id=descriptor.module_id,
                base_revision=request.private_state.revision,
                module_attempt_id=attempt_id,
                value=cast(int, request.private_state.value) + 1,
            )
        return ModuleComputeResult(
            state_update=StateUpdateProposal(
                base_state_revision=request.context.base_state_revision,
                producer=descriptor.module_id,
                module_attempt_id=attempt_id,
                writes=(write,),
            ),
            private_state_update=private_update,
        )

    return compute


def _cycle_time(cycle_value: int) -> LogicalTime:
    return LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
        episode_id=EpisodeId(UUID(int=3)),
        decision_window_id=DecisionWindowId(UUID(int=4)),
        cognitive_cycle_id=CognitiveCycleId(UUID(int=cycle_value)),
    )


__all__ = [
    "SchedulerTestContext",
    "TestModule",
    "make_scheduler_context",
    "module_for",
]
