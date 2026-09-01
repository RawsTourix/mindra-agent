"""Общая fixture standardized lifecycle phase execution."""

from dataclasses import dataclass, replace
from typing import cast
from uuid import UUID

from mindra.contracts import (
    CognitiveModule,
    ExecutionPhase,
    LogicalTime,
    ModuleDescriptor,
    ModuleId,
)
from mindra.runtime import (
    CommitCoordinator,
    DeterministicIdFactory,
    ExecutionPlan,
    ExecutionPlanCompiler,
    InMemoryEvidenceRecorder,
    LifecycleCoordinator,
    PrivateStateStore,
    SequentialWaveExecutor,
)
from tests.scheduler_support import SchedulerTestContext, TestModule, make_scheduler_context


@dataclass(frozen=True, slots=True)
class LifecycleTestContext:
    """Полная composition-wide fixture с one lifecycle participant."""

    base: SchedulerTestContext
    descriptors: tuple[ModuleDescriptor, ...]
    phase: ExecutionPhase
    plan: ExecutionPlan
    participant: TestModule
    store: PrivateStateStore
    coordinator: CommitCoordinator
    recorder: InMemoryEvidenceRecorder
    lifecycle: LifecycleCoordinator
    phase_time: LogicalTime


def make_lifecycle_context(
    phase: ExecutionPhase = ExecutionPhase.EPISODE_START,
) -> LifecycleTestContext:
    """Создать full composition, где alpha участвует в lifecycle phases."""
    base = make_scheduler_context()
    alpha_original = next(
        module
        for module in base.modules
        if module.descriptor.module_id == ModuleId("scheduler.alpha")
    )
    alpha = replace(
        alpha_original.descriptor,
        phases=frozenset({ExecutionPhase.EPISODE_START, ExecutionPhase.POST_OUTCOME}),
    )
    descriptors = tuple(
        alpha if descriptor.module_id == alpha.module_id else descriptor
        for descriptor in base.descriptors
    )
    participant = TestModule(alpha, alpha_original.compute_function)
    plan = ExecutionPlanCompiler(
        DeterministicIdFactory(UUID(int=800), f"lifecycle-plan-{phase.value}")
    ).compile(
        descriptors,
        base.schema,
        composition_revision=base.plan.composition_revision,
        plan_revision=base.plan.revision,
        phase=phase,
    )
    store = PrivateStateStore(descriptors, {alpha.module_id: 10})
    coordinator = CommitCoordinator(
        schema=base.schema,
        descriptors=descriptors,
        private_store=store,
        id_factory=DeterministicIdFactory(UUID(int=801), "lifecycle-commit"),
    )
    recorder = InMemoryEvidenceRecorder()
    lifecycle = LifecycleCoordinator(
        plan=plan,
        modules=(cast(CognitiveModule, participant),),
        private_store=store,
        commit_coordinator=coordinator,
        wave_executor=SequentialWaveExecutor(),
        evidence_recorder=recorder,
        id_factory=DeterministicIdFactory(UUID(int=802), "lifecycle-runtime"),
    )
    phase_time = replace(
        base.cycle_time,
        cognitive_cycle_id=None,
        wave_id=None,
    )
    return LifecycleTestContext(
        base=base,
        descriptors=descriptors,
        phase=phase,
        plan=plan,
        participant=participant,
        store=store,
        coordinator=coordinator,
        recorder=recorder,
        lifecycle=lifecycle,
        phase_time=phase_time,
    )


__all__ = ["LifecycleTestContext", "make_lifecycle_context"]
