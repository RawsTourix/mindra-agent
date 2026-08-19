"""Cognitive causal provenance опубликованного state."""

from dataclasses import dataclass
from uuid import UUID

from mindra.contracts.identity import (
    BranchId,
    CommitId,
    ImplementationId,
    InterventionId,
    LineageId,
    ModuleAttemptId,
    ModuleId,
    RuntimeBoundaryId,
)
from mindra.contracts.revisions import StateRevision
from mindra.contracts.time import LogicalTime

type ProvenanceRef = (
    StateRevision | ModuleAttemptId | CommitId | InterventionId | LineageId | BranchId
)


@dataclass(frozen=True, slots=True)
class StateProvenance:
    """Минимальная causal provenance canonical state value."""

    producer: ModuleId | RuntimeBoundaryId
    base_state_revision: StateRevision
    logical_time: LogicalTime
    implementation_id: ImplementationId | None = None
    module_attempt_id: ModuleAttemptId | None = None
    source_refs: tuple[ProvenanceRef, ...] = ()
    parent_refs: tuple[StateRevision, ...] = ()
    intervention_refs: tuple[InterventionId, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.producer, ModuleId | RuntimeBoundaryId):
            raise TypeError("producer должен быть ModuleId или RuntimeBoundaryId")
        if self.implementation_id is not None and not isinstance(
            self.implementation_id, ImplementationId
        ):
            raise TypeError("implementation_id должен быть ImplementationId или None")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if self.module_attempt_id is not None and not isinstance(self.module_attempt_id, UUID):
            raise TypeError("module_attempt_id должен быть ModuleAttemptId или None")
        if not isinstance(self.logical_time, LogicalTime):
            raise TypeError("logical_time должен быть LogicalTime")
        if not isinstance(self.source_refs, tuple) or any(
            not isinstance(reference, StateRevision | UUID) for reference in self.source_refs
        ):
            raise TypeError("source_refs должен быть tuple допустимых causal references")
        if not isinstance(self.parent_refs, tuple) or any(
            not isinstance(reference, StateRevision) for reference in self.parent_refs
        ):
            raise TypeError("parent_refs должен быть tuple StateRevision")
        if not isinstance(self.intervention_refs, tuple) or any(
            not isinstance(reference, UUID) for reference in self.intervention_refs
        ):
            raise TypeError("intervention_refs должен быть tuple InterventionId")


__all__ = ["ProvenanceRef", "StateProvenance"]
