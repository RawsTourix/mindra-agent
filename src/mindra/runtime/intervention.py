"""Controlled one-shot public-state InterventionGateway."""

from dataclasses import dataclass
from uuid import UUID

from mindra.contracts.availability import Available
from mindra.contracts.errors import InterventionError, KernelError
from mindra.contracts.evidence import (
    EvidenceRecorder,
    InterventionAppliedEvent,
    StateRevisionCommittedEvent,
    TraceEventEnvelope,
)
from mindra.contracts.identity import (
    BranchId,
    IdFactory,
    InterventionId,
    LineageId,
    RuntimeBoundaryId,
)
from mindra.contracts.intervention import (
    InterventionPolicy,
    StateInterventionSpec,
)
from mindra.contracts.provenance import StateProvenance
from mindra.contracts.revisions import StateRevision
from mindra.contracts.state import (
    CognitiveState,
    StateEntry,
    StateEnvelope,
    StatePath,
    StateSchema,
)
from mindra.contracts.time import LogicalTime
from mindra.runtime.state_store import copy_cognitive_state

_INTERVENTION_PRODUCER = RuntimeBoundaryId("evaluation.intervention")


@dataclass(frozen=True, slots=True)
class InterventionRecord:
    """Structural result successful intervention без treatment values."""

    intervention_id: InterventionId
    base_state_revision: StateRevision
    resulting_state_revision: StateRevision
    target_paths: tuple[StatePath, ...]
    base_lineage_id: LineageId
    base_branch_id: BranchId
    resulting_lineage_id: LineageId
    resulting_branch_id: BranchId
    logical_time: LogicalTime

    def __post_init__(self) -> None:
        if not isinstance(self.intervention_id, UUID):
            raise TypeError("intervention_id должен быть InterventionId")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.resulting_state_revision, StateRevision):
            raise TypeError("resulting_state_revision должен быть StateRevision")
        if self.resulting_state_revision != self.base_state_revision.next():
            raise ValueError("resulting_state_revision должен быть ровно base.next()")
        if not isinstance(self.target_paths, tuple):
            raise TypeError("target_paths должен быть tuple StatePath")
        if not self.target_paths:
            raise ValueError("target_paths не может быть пустым")
        if any(not isinstance(path, StatePath) for path in self.target_paths):
            raise TypeError("target_paths должен содержать StatePath")
        if self.target_paths != tuple(sorted(set(self.target_paths), key=lambda item: item.dotted)):
            raise ValueError("target_paths должен иметь canonical unique ordering")
        for value, field_name in (
            (self.base_lineage_id, "base_lineage_id"),
            (self.base_branch_id, "base_branch_id"),
            (self.resulting_lineage_id, "resulting_lineage_id"),
            (self.resulting_branch_id, "resulting_branch_id"),
        ):
            if not isinstance(value, UUID):
                raise TypeError(f"{field_name} должен быть typed UUID identity")
        if self.resulting_lineage_id == self.base_lineage_id:
            raise ValueError("resulting_lineage_id должен отличаться от base_lineage_id")
        if self.resulting_branch_id == self.base_branch_id:
            raise ValueError("resulting_branch_id должен отличаться от base_branch_id")
        if not isinstance(self.logical_time, LogicalTime):
            raise TypeError("logical_time должен быть LogicalTime")
        if (
            self.logical_time.cognitive_cycle_id is not None
            or self.logical_time.wave_id is not None
        ):
            raise ValueError("InterventionRecord требует between-cycle logical_time")


@dataclass(frozen=True, slots=True)
class InterventionResult:
    """Committed treatment snapshot и согласованный structural record."""

    state: CognitiveState
    record: InterventionRecord

    def __post_init__(self) -> None:
        if not isinstance(self.state, CognitiveState):
            raise TypeError("state должен быть CognitiveState")
        if not isinstance(self.record, InterventionRecord):
            raise TypeError("record должен быть InterventionRecord")
        envelope = self.state.envelope
        if envelope.state_revision != self.record.resulting_state_revision:
            raise ValueError("State revision не согласована с InterventionRecord")
        if envelope.parent_state_revision != self.record.base_state_revision:
            raise ValueError("State parent revision не согласована с InterventionRecord")
        if envelope.lineage_id != self.record.resulting_lineage_id:
            raise ValueError("State lineage не согласована с InterventionRecord")
        if envelope.branch_id != self.record.resulting_branch_id:
            raise ValueError("State branch не согласована с InterventionRecord")
        if envelope.logical_time != self.record.logical_time:
            raise ValueError("State logical_time не согласована с InterventionRecord")


class InterventionGateway:
    """Privileged boundary controlled public-state treatment commit."""

    __slots__ = ("_evidence_recorder", "_id_factory", "_policy", "_schema")

    def __init__(
        self,
        *,
        schema: StateSchema,
        policy: InterventionPolicy,
        evidence_recorder: EvidenceRecorder,
        id_factory: IdFactory,
    ) -> None:
        if not isinstance(schema, StateSchema):
            raise TypeError("schema должен быть StateSchema")
        if not isinstance(policy, InterventionPolicy):
            raise TypeError("policy должен быть InterventionPolicy")
        if not callable(getattr(evidence_recorder, "record", None)):
            raise TypeError("evidence_recorder должен удовлетворять EvidenceRecorder")
        if not callable(getattr(id_factory, "new_id", None)):
            raise TypeError("id_factory должен удовлетворять IdFactory")
        self._schema = schema
        self._policy = policy
        self._evidence_recorder = evidence_recorder
        self._id_factory = id_factory

    def apply(
        self,
        *,
        current_state: CognitiveState,
        spec: StateInterventionSpec,
        logical_time: LogicalTime,
    ) -> InterventionResult:
        """Validate, construct и instrument один atomic treatment commit."""
        if not isinstance(current_state, CognitiveState):
            raise TypeError("current_state должен быть CognitiveState")
        if not isinstance(spec, StateInterventionSpec):
            raise TypeError("spec должен быть StateInterventionSpec")
        if not isinstance(logical_time, LogicalTime):
            raise TypeError("logical_time должен быть LogicalTime")

        envelope = current_state.envelope
        if envelope.schema_revision != self._schema.revision:
            raise InterventionError("Current state использует не active schema revision")
        if logical_time.cognitive_cycle_id is not None or logical_time.wave_id is not None:
            raise InterventionError("Intervention разрешена только at between-cycle boundary")
        base_time = envelope.logical_time
        if logical_time.run_id != base_time.run_id:
            raise InterventionError("Intervention logical_time меняет run_id")
        if logical_time.agent_session_id != base_time.agent_session_id:
            raise InterventionError("Intervention logical_time меняет agent_session_id")
        if base_time.episode_id is not None and logical_time.episode_id != base_time.episode_id:
            raise InterventionError("Intervention logical_time меняет established episode_id")
        if (
            base_time.decision_window_id is not None
            and logical_time.decision_window_id != base_time.decision_window_id
        ):
            raise InterventionError(
                "Intervention logical_time меняет established decision_window_id"
            )
        if spec.base_state_revision != envelope.state_revision:
            raise InterventionError("Intervention base StateRevision stale")
        if spec.base_lineage_id != envelope.lineage_id:
            raise InterventionError("Intervention base LineageId не совпадает с current state")
        if spec.base_branch_id != envelope.branch_id:
            raise InterventionError("Intervention base BranchId не совпадает с current state")

        resolved_targets = []
        for write in spec.writes:
            try:
                field = self._schema.lookup(write.path)
            except KernelError as error:
                raise InterventionError(f"Unknown intervention target: {write.path}") from error
            resolved_targets.append((write, field))

        for write, _ in resolved_targets:
            if not self._policy.allows(write.path):
                raise InterventionError(f"Intervention target не разрешён policy: {write.path}")

        prepared: list[tuple[StatePath, object]] = []
        for write, field in resolved_targets:
            try:
                frozen_value = field.value_contract.freeze(write.value)
            except KernelError as error:
                raise InterventionError(
                    f"Treatment value не прошёл ValueContract для {write.path}"
                ) from error
            prepared.append((write.path, frozen_value))

        intervention_id = self._id_factory.new_id(InterventionId)
        resulting_lineage_id = self._id_factory.new_id(LineageId)
        resulting_branch_id = self._id_factory.new_id(BranchId)
        resulting_revision = envelope.state_revision.next()

        provenance = StateProvenance(
            producer=_INTERVENTION_PRODUCER,
            implementation_id=None,
            base_state_revision=envelope.state_revision,
            module_attempt_id=None,
            logical_time=logical_time,
            source_refs=(
                envelope.state_revision,
                envelope.lineage_id,
                envelope.branch_id,
            ),
            parent_refs=(envelope.state_revision,),
            intervention_refs=(intervention_id,),
        )
        replacements = {
            path: StateEntry(availability=Available(value), provenance=provenance)
            for path, value in prepared
        }
        resulting_state = copy_cognitive_state(
            base_state=current_state,
            schema=self._schema,
            envelope=StateEnvelope(
                schema_revision=envelope.schema_revision,
                state_revision=resulting_revision,
                parent_state_revision=envelope.state_revision,
                lineage_id=resulting_lineage_id,
                branch_id=resulting_branch_id,
                agent_revision_id=envelope.agent_revision_id,
                logical_time=logical_time,
                composition_revision=envelope.composition_revision,
            ),
            replacements=replacements,
        )
        target_paths = tuple(path for path, _ in prepared)
        record = InterventionRecord(
            intervention_id=intervention_id,
            base_state_revision=envelope.state_revision,
            resulting_state_revision=resulting_revision,
            target_paths=target_paths,
            base_lineage_id=envelope.lineage_id,
            base_branch_id=envelope.branch_id,
            resulting_lineage_id=resulting_lineage_id,
            resulting_branch_id=resulting_branch_id,
            logical_time=logical_time,
        )
        result = InterventionResult(state=resulting_state, record=record)

        self._evidence_recorder.record(
            TraceEventEnvelope(
                logical_time=logical_time,
                payload=InterventionAppliedEvent(
                    intervention_id=intervention_id,
                    base_state_revision=envelope.state_revision,
                    resulting_state_revision=resulting_revision,
                    target_paths=target_paths,
                    lineage_id=resulting_lineage_id,
                    branch_id=resulting_branch_id,
                ),
                physical_timestamp_ns=None,
            )
        )
        self._evidence_recorder.record(
            TraceEventEnvelope(
                logical_time=logical_time,
                payload=StateRevisionCommittedEvent(
                    before=envelope.state_revision,
                    after=resulting_revision,
                    public_paths=target_paths,
                    lineage_id=resulting_lineage_id,
                    branch_id=resulting_branch_id,
                    agent_revision_id=envelope.agent_revision_id,
                    commit_id=None,
                    intervention_id=intervention_id,
                ),
                physical_timestamp_ns=None,
            )
        )
        return result


__all__ = ["InterventionGateway", "InterventionRecord", "InterventionResult"]
