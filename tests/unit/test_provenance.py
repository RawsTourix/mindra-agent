"""Проверки immutable cognitive provenance и diagnostic isolation."""

from dataclasses import FrozenInstanceError, fields
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentSessionId,
    CommitId,
    ImplementationId,
    InterventionId,
    LogicalTime,
    ModuleAttemptId,
    ModuleId,
    RunId,
    RuntimeBoundaryId,
    StateProvenance,
    StateRevision,
)


def _logical_time() -> LogicalTime:
    return LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
    )


def test_module_provenance_carries_minimum_causal_context() -> None:
    attempt_id = ModuleAttemptId(UUID(int=3))
    intervention_id = InterventionId(UUID(int=4))
    provenance = StateProvenance(
        producer=ModuleId("synthetic.source"),
        implementation_id=ImplementationId("reference.synthetic_source.v1"),
        base_state_revision=StateRevision(2),
        module_attempt_id=attempt_id,
        logical_time=_logical_time(),
        source_refs=(CommitId(UUID(int=5)),),
        parent_refs=(StateRevision(1),),
        intervention_refs=(intervention_id,),
    )

    assert provenance.producer == ModuleId("synthetic.source")
    assert provenance.module_attempt_id == attempt_id
    assert provenance.source_refs == (CommitId(UUID(int=5)),)
    assert provenance.parent_refs == (StateRevision(1),)
    assert provenance.intervention_refs == (intervention_id,)


def test_runtime_boundary_is_distinct_from_module_identity() -> None:
    provenance = StateProvenance(
        producer=RuntimeBoundaryId("runtime.initialization"),
        base_state_revision=StateRevision.initial(),
        logical_time=_logical_time(),
    )

    assert isinstance(provenance.producer, RuntimeBoundaryId)
    assert not isinstance(provenance.producer, ModuleId)


def test_state_provenance_is_frozen_and_contains_no_diagnostic_metadata() -> None:
    provenance = StateProvenance(
        producer=RuntimeBoundaryId("runtime.initialization"),
        base_state_revision=StateRevision.initial(),
        logical_time=_logical_time(),
    )
    field_names = {field.name for field in fields(StateProvenance)}

    assert field_names.isdisjoint(
        {"diagnostics", "error_text", "experiment_id", "physical_timestamp", "profile_id"}
    )
    parent_refs_attribute = "parent_refs"
    with pytest.raises(FrozenInstanceError):
        setattr(provenance, parent_refs_attribute, (StateRevision(1),))


def test_state_provenance_rejects_mutable_reference_collections() -> None:
    with pytest.raises(TypeError):
        StateProvenance(
            producer=RuntimeBoundaryId("runtime.initialization"),
            base_state_revision=StateRevision.initial(),
            logical_time=_logical_time(),
            parent_refs=cast(tuple[StateRevision, ...], [StateRevision.initial()]),
        )
