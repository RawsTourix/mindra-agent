"""Contract checks раздельной module/runtime-boundary state authority."""

from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    Available,
    BoundaryStateUpdate,
    BoundaryStateWrite,
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
    UnauthorizedWriteError,
    ValueContract,
)
from mindra.runtime import (
    BoundaryCommitCoordinator,
    CommitCoordinator,
    DeterministicIdFactory,
    PrivateStateStore,
    build_cognitive_state,
)

MODULE = ModuleId("synthetic.module")
BOUNDARY = RuntimeBoundaryId("runtime.interaction_ingress")
MODULE_KEY = StateKey[int](StatePath.from_dotted("synthetic.module_value"))
BOUNDARY_KEY = StateKey[int](StatePath.from_dotted("observation.current"))


def _time() -> LogicalTime:
    return LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
    )


def _schema() -> StateSchema:
    return StateSchema(
        SchemaRevision.initial(),
        (
            cast(
                StateFieldSpec[object],
                StateFieldSpec(MODULE_KEY, MODULE, ValueContract(int)),
            ),
            cast(
                StateFieldSpec[object],
                StateFieldSpec(BOUNDARY_KEY, BOUNDARY, ValueContract(int)),
            ),
        ),
    )


def _state(schema: StateSchema) -> CognitiveState:
    logical_time = _time()
    return build_cognitive_state(
        schema=schema,
        envelope=StateEnvelope(
            schema_revision=schema.revision,
            state_revision=StateRevision.initial(),
            parent_state_revision=None,
            lineage_id=LineageId(UUID(int=3)),
            branch_id=BranchId(UUID(int=4)),
            agent_revision_id=AgentRevisionId(UUID(int=5)),
            logical_time=logical_time,
            composition_revision=CompositionRevision.initial(),
        ),
        entries={
            MODULE_KEY.path: StateEntry(
                Available(1),
                StateProvenance(BOUNDARY, StateRevision.initial(), logical_time),
            ),
            BOUNDARY_KEY.path: StateEntry(
                Available(2),
                StateProvenance(BOUNDARY, StateRevision.initial(), logical_time),
            ),
        },
    )


def test_state_schema_accepts_module_and_runtime_boundary_owners() -> None:
    schema = _schema()

    assert schema.lookup(MODULE_KEY).owner == MODULE
    assert schema.lookup(BOUNDARY_KEY).owner == BOUNDARY


def test_state_schema_rejects_unknown_owner_kind() -> None:
    with pytest.raises(TypeError, match="ModuleId или RuntimeBoundaryId"):
        StateFieldSpec(
            MODULE_KEY,
            cast(ModuleId | RuntimeBoundaryId, "synthetic.invalid"),
            ValueContract(int),
        )


def test_module_commit_cannot_publish_runtime_owned_field() -> None:
    schema = _schema()
    state = _state(schema)
    descriptor = ModuleDescriptor(
        module_id=MODULE,
        implementation_id=ImplementationId("test.synthetic.module.v1"),
        implementation_revision=ImplementationRevision("v1"),
        reads=(),
        writes=(cast(StateKey[object], BOUNDARY_KEY),),
        private_state=None,
        phases=frozenset({ExecutionPhase.COGNITIVE_CYCLE}),
        traits=ExecutionTraits(
            statefulness=ModuleStatefulness.STATELESS,
            determinism=DeterminismMode.DETERMINISTIC,
        ),
    )
    attempt_id = ModuleAttemptId(UUID(int=6))
    result = ModuleComputeResult(
        state_update=StateUpdateProposal(
            base_state_revision=StateRevision.initial(),
            producer=MODULE,
            module_attempt_id=attempt_id,
            writes=(
                cast(
                    StateWrite[object],
                    StateWrite(
                        key=BOUNDARY_KEY,
                        availability=Available(3),
                        provenance=StateProvenance(
                            producer=MODULE,
                            implementation_id=descriptor.implementation_id,
                            base_state_revision=StateRevision.initial(),
                            module_attempt_id=attempt_id,
                            logical_time=_time(),
                        ),
                    ),
                ),
            ),
        ),
        private_state_update=None,
    )
    coordinator = CommitCoordinator(
        schema=schema,
        descriptors=(descriptor,),
        private_store=PrivateStateStore((descriptor,), {}),
        id_factory=DeterministicIdFactory(UUID(int=7), "module-ownership"),
    )

    with pytest.raises(UnauthorizedWriteError, match="owner"):
        coordinator.commit(current_state=state, results=(result,), logical_time=_time())


def test_runtime_boundary_cannot_publish_module_owned_field() -> None:
    schema = _schema()
    logical_time = _time()
    coordinator = BoundaryCommitCoordinator(
        schema=schema,
        id_factory=DeterministicIdFactory(UUID(int=8), "boundary-ownership"),
    )
    update = BoundaryStateUpdate(
        base_state_revision=StateRevision.initial(),
        producer=BOUNDARY,
        writes=(
            cast(
                BoundaryStateWrite[object],
                BoundaryStateWrite(
                    key=MODULE_KEY,
                    availability=Available(4),
                    provenance=StateProvenance(
                        producer=BOUNDARY,
                        base_state_revision=StateRevision.initial(),
                        logical_time=logical_time,
                    ),
                ),
            ),
        ),
    )

    with pytest.raises(UnauthorizedWriteError, match="owner"):
        coordinator.commit(
            current_state=_state(schema),
            update=update,
            logical_time=logical_time,
        )


def test_module_id_cannot_masquerade_as_boundary_update_producer() -> None:
    with pytest.raises(TypeError, match="RuntimeBoundaryId"):
        BoundaryStateUpdate(
            base_state_revision=StateRevision.initial(),
            producer=cast(RuntimeBoundaryId, MODULE),
            writes=(
                cast(
                    BoundaryStateWrite[object],
                    BoundaryStateWrite(
                        key=BOUNDARY_KEY,
                        availability=Available(4),
                        provenance=StateProvenance(
                            producer=MODULE,
                            base_state_revision=StateRevision.initial(),
                            logical_time=_time(),
                        ),
                    ),
                ),
            ),
        )
