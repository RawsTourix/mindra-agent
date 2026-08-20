"""Contract checks isolation runtime private store от cognitive modules."""

from dataclasses import fields
from typing import cast
from uuid import UUID

import mindra.runtime as runtime
from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    BranchId,
    CognitiveModule,
    CompositionRevision,
    DeterminismMode,
    ExecutionPhase,
    ExecutionTraits,
    ImplementationId,
    ImplementationRevision,
    LineageId,
    LogicalTime,
    ModuleAttemptId,
    ModuleComputeRequest,
    ModuleComputeResult,
    ModuleDescriptor,
    ModuleExecutionContext,
    ModuleId,
    ModuleStatefulness,
    PrivateStateDescriptor,
    PrivateStateSnapshot,
    RunId,
    SchemaRevision,
    StateEnvelope,
    StateRevision,
    StateSchema,
    StateUpdateProposal,
    ValueContract,
)
from mindra.runtime import PrivateStateSlot, PrivateStateStore


def _descriptor(name: str) -> ModuleDescriptor:
    return ModuleDescriptor(
        module_id=ModuleId(name),
        implementation_id=ImplementationId(f"test.{name}.v1"),
        implementation_revision=ImplementationRevision("v1"),
        reads=(),
        writes=(),
        private_state=cast(
            PrivateStateDescriptor[object],
            PrivateStateDescriptor(ValueContract(int)),
        ),
        phases=frozenset({ExecutionPhase.COGNITIVE_CYCLE}),
        traits=ExecutionTraits(
            statefulness=ModuleStatefulness.STATEFUL,
            determinism=DeterminismMode.DETERMINISTIC,
        ),
    )


def _request(
    descriptor: ModuleDescriptor,
    store: PrivateStateStore,
) -> ModuleComputeRequest:
    logical_time = LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
    )
    state = runtime.build_cognitive_state(
        schema=StateSchema(SchemaRevision.initial(), ()),
        envelope=StateEnvelope(
            schema_revision=SchemaRevision.initial(),
            state_revision=StateRevision.initial(),
            parent_state_revision=None,
            lineage_id=LineageId(UUID(int=3)),
            branch_id=BranchId(UUID(int=4)),
            agent_revision_id=AgentRevisionId(UUID(int=5)),
            logical_time=logical_time,
            composition_revision=CompositionRevision.initial(),
        ),
        entries={},
    )
    attempt_id = ModuleAttemptId(UUID(int=6))
    return ModuleComputeRequest(
        state=runtime.build_state_projection(base_state=state, read_specs=()),
        private_state=store.snapshot_for(descriptor.module_id),
        context=ModuleExecutionContext(
            module_attempt_id=attempt_id,
            base_state_revision=state.envelope.state_revision,
            logical_time=logical_time,
            phase=ExecutionPhase.COGNITIVE_CYCLE,
        ),
    )


class _StatefulFixtureModule:
    """Test-only cognitive boundary, которая видит только own snapshot."""

    def __init__(self, descriptor: ModuleDescriptor) -> None:
        self.descriptor = descriptor

    def compute(self, request: ModuleComputeRequest) -> ModuleComputeResult:
        return ModuleComputeResult(
            state_update=StateUpdateProposal(
                base_state_revision=request.context.base_state_revision,
                producer=self.descriptor.module_id,
                module_attempt_id=request.context.module_attempt_id,
                writes=(),
            ),
            private_state_update=None,
        )


def test_stateful_module_request_contains_only_own_snapshot_without_store_access() -> None:
    owner = _descriptor("private.owner")
    peer = _descriptor("private.peer")
    store = PrivateStateStore(
        (owner, peer),
        {owner.module_id: 11, peer.module_id: 22},
    )
    request = _request(owner, store)
    module = _StatefulFixtureModule(owner)

    assert isinstance(module, CognitiveModule)
    assert isinstance(request.private_state, PrivateStateSnapshot)
    assert request.private_state.module_id == owner.module_id
    assert request.private_state.value == 11
    assert {field.name for field in fields(ModuleComputeRequest)} == {
        "state",
        "private_state",
        "context",
    }
    assert not hasattr(request, "private_state_store")
    assert not hasattr(request, "private_lookup")
    assert not hasattr(request, "peer_private_state")
    assert not hasattr(module, "private_state_store")
    assert module.compute(request).private_state_update is None


def test_store_and_slots_are_not_mutable_module_facing_mappings() -> None:
    descriptor = _descriptor("private.encapsulated")
    store = PrivateStateStore((descriptor,), {descriptor.module_id: 1})
    snapshot = store.snapshot_for(descriptor.module_id)

    assert isinstance(snapshot, PrivateStateSnapshot)
    assert not isinstance(snapshot, PrivateStateSlot)
    assert not hasattr(store, "slots")
    assert not hasattr(store, "set_private_state")
    assert not hasattr(store, "mutate")
    assert not hasattr(store, "apply_proposal")
    assert not hasattr(store, "get_mutable_slot")
    assert not hasattr(store, "__setitem__")


def test_only_public_store_types_are_exported_from_runtime_facade() -> None:
    assert runtime.PrivateStateSlot is PrivateStateSlot
    assert runtime.PrivateStateStore is PrivateStateStore
    assert "PrivateStateSlot" in runtime.__all__
    assert "PrivateStateStore" in runtime.__all__
    assert "_PreparedPrivateStateUpdate" not in runtime.__all__
    assert not hasattr(runtime, "_PreparedPrivateStateUpdate")
