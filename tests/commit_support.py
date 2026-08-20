"""Общие строго типизированные fixtures atomic commit tests."""

from dataclasses import dataclass
from typing import cast
from uuid import UUID

from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    Available,
    BranchId,
    CognitiveState,
    CompositionRevision,
    DeterminismMode,
    ExecutionPhase,
    ExecutionTraits,
    ImplementationId,
    ImplementationRevision,
    LineageId,
    LogicalTime,
    ModuleAttemptId,
    ModuleComputeResult,
    ModuleDescriptor,
    ModuleId,
    ModuleStatefulness,
    PrivateStateDescriptor,
    PrivateStateProposal,
    PrivateStateRevision,
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
    CommitCoordinator,
    DeterministicIdFactory,
    PrivateStateStore,
    build_cognitive_state,
)


@dataclass(frozen=True, slots=True)
class CommitTestContext:
    """Полная active composition для commit-level tests."""

    schema: StateSchema
    descriptors: tuple[ModuleDescriptor, ...]
    store: PrivateStateStore
    factory: DeterministicIdFactory
    coordinator: CommitCoordinator
    state: CognitiveState
    logical_time: LogicalTime
    keys: dict[str, StateKey[int]]


def _descriptor(name: str, key: StateKey[int], *, stateful: bool) -> ModuleDescriptor:
    private_state = (
        cast(
            PrivateStateDescriptor[object],
            PrivateStateDescriptor(ValueContract(int)),
        )
        if stateful
        else None
    )
    return ModuleDescriptor(
        module_id=ModuleId(f"commit.{name}"),
        implementation_id=ImplementationId(f"test.commit.{name}.v1"),
        implementation_revision=ImplementationRevision("v1"),
        reads=(),
        writes=(cast(StateKey[object], key),),
        private_state=private_state,
        phases=frozenset({ExecutionPhase.COGNITIVE_CYCLE}),
        traits=ExecutionTraits(
            statefulness=(
                ModuleStatefulness.STATEFUL if stateful else ModuleStatefulness.STATELESS
            ),
            determinism=DeterminismMode.DETERMINISTIC,
        ),
    )


def make_context() -> CommitTestContext:
    """Создать composition с двумя stateful и одним stateless producer."""
    keys = {
        name: StateKey[int](StatePath.from_dotted(f"commit.{name}.value"))
        for name in ("alpha", "beta", "gamma")
    }
    descriptors_by_name = {
        "alpha": _descriptor("alpha", keys["alpha"], stateful=True),
        "beta": _descriptor("beta", keys["beta"], stateful=True),
        "gamma": _descriptor("gamma", keys["gamma"], stateful=False),
    }
    descriptors = (
        descriptors_by_name["beta"],
        descriptors_by_name["gamma"],
        descriptors_by_name["alpha"],
    )
    schema = StateSchema(
        SchemaRevision.initial(),
        tuple(
            cast(
                StateFieldSpec[object],
                StateFieldSpec(
                    key=keys[name],
                    owner=descriptors_by_name[name].module_id,
                    value_contract=ValueContract(int),
                ),
            )
            for name in ("alpha", "beta", "gamma")
        ),
    )
    logical_time = LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
    )
    envelope = StateEnvelope(
        schema_revision=schema.revision,
        state_revision=StateRevision.initial(),
        parent_state_revision=None,
        lineage_id=LineageId(UUID(int=3)),
        branch_id=BranchId(UUID(int=4)),
        agent_revision_id=AgentRevisionId(UUID(int=5)),
        logical_time=logical_time,
        composition_revision=CompositionRevision.initial(),
    )
    entries = {
        keys[name].path: StateEntry(
            availability=Available(index),
            provenance=StateProvenance(
                producer=RuntimeBoundaryId("runtime.initialization"),
                base_state_revision=StateRevision.initial(),
                logical_time=logical_time,
            ),
        )
        for index, name in enumerate(("alpha", "beta", "gamma"), start=1)
    }
    state = build_cognitive_state(schema=schema, envelope=envelope, entries=entries)
    store = PrivateStateStore(
        descriptors,
        {
            descriptors_by_name["alpha"].module_id: 10,
            descriptors_by_name["beta"].module_id: 20,
        },
    )
    factory = DeterministicIdFactory(UUID(int=100), "commit-tests")
    coordinator = CommitCoordinator(
        schema=schema,
        descriptors=descriptors,
        private_store=store,
        id_factory=factory,
    )
    return CommitTestContext(
        schema=schema,
        descriptors=descriptors,
        store=store,
        factory=factory,
        coordinator=coordinator,
        state=state,
        logical_time=logical_time,
        keys=keys,
    )


def descriptor_for(context: CommitTestContext, name: str) -> ModuleDescriptor:
    """Найти descriptor по test suffix."""
    return next(
        descriptor
        for descriptor in context.descriptors
        if descriptor.module_id == ModuleId(f"commit.{name}")
    )


def attempt_id(name: str) -> ModuleAttemptId:
    """Вернуть стабильный test attempt identity."""
    values = {"alpha": 11, "beta": 12, "gamma": 13}
    return ModuleAttemptId(UUID(int=values[name]))


def result_for(
    context: CommitTestContext,
    name: str,
    *,
    public_value: object | None = None,
    private_value: object | None = None,
    base_revision: StateRevision | None = None,
    private_revision: PrivateStateRevision | None = None,
    module_attempt_id: ModuleAttemptId | None = None,
    logical_time: LogicalTime | None = None,
) -> ModuleComputeResult:
    """Построить valid staged result с optional public/private effect."""
    descriptor = descriptor_for(context, name)
    selected_attempt = module_attempt_id or attempt_id(name)
    selected_time = logical_time or context.logical_time
    selected_base = base_revision or StateRevision.initial()
    writes: tuple[StateWrite[object], ...] = ()
    if public_value is not None:
        writes = (
            cast(
                StateWrite[object],
                StateWrite(
                    key=context.keys[name],
                    availability=Available(public_value),
                    provenance=StateProvenance(
                        producer=descriptor.module_id,
                        implementation_id=descriptor.implementation_id,
                        base_state_revision=selected_base,
                        module_attempt_id=selected_attempt,
                        logical_time=selected_time,
                    ),
                ),
            ),
        )
    private_proposal = None
    if private_value is not None:
        private_proposal = PrivateStateProposal(
            module_id=descriptor.module_id,
            base_revision=private_revision or PrivateStateRevision.initial(),
            module_attempt_id=selected_attempt,
            value=private_value,
        )
    return ModuleComputeResult(
        state_update=StateUpdateProposal(
            base_state_revision=selected_base,
            producer=descriptor.module_id,
            module_attempt_id=selected_attempt,
            writes=writes,
        ),
        private_state_update=private_proposal,
    )


__all__ = [
    "CommitTestContext",
    "attempt_id",
    "descriptor_for",
    "make_context",
    "result_for",
]
