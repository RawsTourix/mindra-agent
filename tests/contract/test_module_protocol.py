"""Contract checks structural CognitiveModule boundary v0.1."""

from dataclasses import FrozenInstanceError, fields
from typing import cast
from uuid import UUID

import pytest

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
    RunId,
    SchemaRevision,
    StateEnvelope,
    StateRevision,
    StateSchema,
    StateUpdateProposal,
    Unavailable,
)
from mindra.runtime import build_cognitive_state, build_state_projection


def _logical_time() -> LogicalTime:
    return LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
    )


def _descriptor() -> ModuleDescriptor:
    return ModuleDescriptor(
        module_id=ModuleId("synthetic.contract_fixture"),
        implementation_id=ImplementationId("test.contract_fixture.v1"),
        implementation_revision=ImplementationRevision("fixture-1"),
        reads=(),
        writes=(),
        private_state=None,
        phases=frozenset({ExecutionPhase.COGNITIVE_CYCLE}),
        traits=ExecutionTraits(
            statefulness=ModuleStatefulness.STATELESS,
            determinism=DeterminismMode.DETERMINISTIC,
        ),
    )


def _request() -> ModuleComputeRequest:
    logical_time = _logical_time()
    state = build_cognitive_state(
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
        state=build_state_projection(base_state=state, read_specs=()),
        private_state=Unavailable(),
        context=ModuleExecutionContext(
            module_attempt_id=attempt_id,
            base_state_revision=state.envelope.state_revision,
            logical_time=logical_time,
            phase=ExecutionPhase.COGNITIVE_CYCLE,
        ),
    )


class ContractFixtureModule:
    """Минимальная test-only structural implementation, не reference module."""

    descriptor = _descriptor()

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


def test_fixture_structurally_satisfies_cognitive_module_protocol() -> None:
    module = ContractFixtureModule()

    assert isinstance(module, CognitiveModule)
    result = cast(CognitiveModule, module).compute(_request())
    assert result.state_update.writes == ()


def test_compute_request_contains_only_three_allowed_boundaries() -> None:
    request = _request()
    field_names = {field.name for field in fields(ModuleComputeRequest)}

    assert field_names == {"state", "private_state", "context"}
    assert not hasattr(request, "cognitive_state")
    assert not hasattr(request, "registry")
    assert not hasattr(request, "config")
    assert not hasattr(request, "evaluator")
    assert not hasattr(request, "services")
    assert {field.name for field in fields(ModuleExecutionContext)} == {
        "module_attempt_id",
        "base_state_revision",
        "logical_time",
        "phase",
    }


def test_compute_result_is_only_staged_public_private_proposals() -> None:
    result = ContractFixtureModule().compute(_request())

    assert {field.name for field in fields(ModuleComputeResult)} == {
        "state_update",
        "private_state_update",
    }
    assert not hasattr(result, "diagnostics")
    assert not hasattr(result, "commit")
    state_update_attribute = "state_update"
    with pytest.raises(FrozenInstanceError):
        setattr(result, state_update_attribute, result.state_update)
