"""Contract tests controlled public-state InterventionGateway."""

from dataclasses import FrozenInstanceError
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    Available,
    BranchId,
    CognitiveCycleId,
    CognitiveState,
    CompositionRevision,
    DecisionWindowId,
    EpisodeId,
    EvidenceRecorder,
    IdentityType,
    InterventionAppliedEvent,
    InterventionError,
    InterventionPolicy,
    LineageId,
    LogicalTime,
    ModuleId,
    RunId,
    RuntimeBoundaryId,
    SchemaRevision,
    StateEntry,
    StateEnvelope,
    StateFieldSpec,
    StateInterventionSpec,
    StateInterventionWrite,
    StateKey,
    StatePath,
    StateProvenance,
    StateRevision,
    StateRevisionCommittedEvent,
    StateSchema,
    TraceEventEnvelope,
    TraceEventKind,
    Unknown,
    ValueContract,
)
from mindra.runtime import (
    DeterministicIdFactory,
    InMemoryEvidenceRecorder,
    InterventionGateway,
)
from mindra.runtime.state_store import build_cognitive_state

PATH_A = StatePath.from_dotted("test.alpha.value")
PATH_B = StatePath.from_dotted("test.beta.value")
MISSING_PATH = StatePath.from_dotted("test.missing.value")


def _identity[IdentityT: UUID](identity_type: IdentityType[IdentityT], value: int) -> IdentityT:
    return identity_type(UUID(int=value))


def _state_and_schema() -> tuple[CognitiveState, StateSchema, LogicalTime]:
    schema = StateSchema(
        SchemaRevision.initial(),
        (
            cast(
                StateFieldSpec[object],
                StateFieldSpec(
                    key=StateKey[int](PATH_A),
                    owner=ModuleId("test.alpha"),
                    value_contract=ValueContract(int),
                ),
            ),
            cast(
                StateFieldSpec[object],
                StateFieldSpec(
                    key=StateKey[int](PATH_B),
                    owner=ModuleId("test.beta"),
                    value_contract=ValueContract(int),
                ),
            ),
        ),
    )
    logical_time = LogicalTime(
        run_id=_identity(RunId, 1),
        agent_session_id=_identity(AgentSessionId, 2),
        episode_id=_identity(EpisodeId, 6),
        decision_window_id=_identity(DecisionWindowId, 7),
    )
    provenance = StateProvenance(
        producer=RuntimeBoundaryId("test.initial"),
        base_state_revision=StateRevision.initial(),
        logical_time=logical_time,
    )
    state = build_cognitive_state(
        schema=schema,
        envelope=StateEnvelope(
            schema_revision=schema.revision,
            state_revision=StateRevision.initial(),
            parent_state_revision=None,
            lineage_id=_identity(LineageId, 3),
            branch_id=_identity(BranchId, 4),
            agent_revision_id=_identity(AgentRevisionId, 5),
            logical_time=logical_time,
            composition_revision=CompositionRevision.initial(),
        ),
        entries={
            PATH_A: StateEntry(availability=Unknown(), provenance=provenance),
            PATH_B: StateEntry(availability=Unknown(), provenance=provenance),
        },
    )
    return state, schema, logical_time


def _spec(
    state: CognitiveState,
    *writes: StateInterventionWrite,
) -> StateInterventionSpec:
    return StateInterventionSpec(
        base_state_revision=state.envelope.state_revision,
        base_lineage_id=state.envelope.lineage_id,
        base_branch_id=state.envelope.branch_id,
        writes=tuple(writes),
    )


def _set_attribute(target: object, name: str, value: object) -> None:
    setattr(target, name, value)


def test_contracts_are_frozen_and_canonical() -> None:
    write_a = StateInterventionWrite(PATH_A, 1)
    write_b = StateInterventionWrite(PATH_B, 2)
    state, _, _ = _state_and_schema()
    spec = _spec(state, write_b, write_a)
    policy = InterventionPolicy.allowlist((PATH_B, PATH_A))

    assert tuple(write.path for write in spec.writes) == (PATH_A, PATH_B)
    assert policy.allowed_paths == (PATH_A, PATH_B)
    assert policy.allows(PATH_A)
    assert not policy.allows(StatePath.from_dotted("test.alpha"))
    assert not InterventionPolicy.disabled().allows(PATH_A)
    with pytest.raises(FrozenInstanceError):
        _set_attribute(write_a, "value", 3)
    with pytest.raises(FrozenInstanceError):
        _set_attribute(spec, "writes", ())
    with pytest.raises(FrozenInstanceError):
        _set_attribute(policy, "allowed_paths", ())


def test_spec_rejects_empty_and_duplicate_targets() -> None:
    state, _, _ = _state_and_schema()
    with pytest.raises(ValueError, match="пустым"):
        _spec(state)
    with pytest.raises(ValueError, match="duplicate"):
        _spec(
            state,
            StateInterventionWrite(PATH_A, 1),
            StateInterventionWrite(PATH_A, 2),
        )
    with pytest.raises(ValueError, match="duplicate"):
        InterventionPolicy.allowlist((PATH_A, PATH_A))


def test_successful_gateway_commit_has_exact_state_provenance_and_evidence() -> None:
    state, schema, logical_time = _state_and_schema()
    recorder = InMemoryEvidenceRecorder()
    factory = DeterministicIdFactory(UUID(int=10), "intervention")
    result = InterventionGateway(
        schema=schema,
        policy=InterventionPolicy.allowlist((PATH_A,)),
        evidence_recorder=recorder,
        id_factory=factory,
    ).apply(
        current_state=state,
        spec=_spec(state, StateInterventionWrite(PATH_A, 7)),
        logical_time=logical_time,
    )

    assert state.envelope.state_revision == StateRevision.initial()
    assert isinstance(state.entries[PATH_A].availability, Unknown)
    assert result.state.envelope.state_revision == state.envelope.state_revision.next()
    assert result.state.envelope.parent_state_revision == state.envelope.state_revision
    assert result.state.envelope.lineage_id != state.envelope.lineage_id
    assert result.state.envelope.branch_id != state.envelope.branch_id
    assert result.state.entries[PATH_B] == state.entries[PATH_B]
    assert result.state.entries[PATH_B].provenance is state.entries[PATH_B].provenance
    treatment = result.state.entries[PATH_A]
    assert treatment.availability == Available(7)
    assert treatment.provenance.producer == RuntimeBoundaryId("evaluation.intervention")
    assert treatment.provenance.implementation_id is None
    assert treatment.provenance.module_attempt_id is None
    assert treatment.provenance.base_state_revision == state.envelope.state_revision
    assert treatment.provenance.source_refs == (
        state.envelope.state_revision,
        state.envelope.lineage_id,
        state.envelope.branch_id,
    )
    assert treatment.provenance.parent_refs == (state.envelope.state_revision,)
    assert treatment.provenance.intervention_refs == (result.record.intervention_id,)
    assert schema.lookup(PATH_A).owner == ModuleId("test.alpha")

    events = recorder.snapshot()
    assert tuple(event.kind for event in events) == (
        TraceEventKind.INTERVENTION_APPLIED,
        TraceEventKind.STATE_REVISION_COMMITTED,
    )
    assert all(event.logical_time == logical_time for event in events)
    assert all(event.physical_timestamp_ns is None for event in events)
    applied = cast(InterventionAppliedEvent, events[0].payload)
    committed = cast(StateRevisionCommittedEvent, events[1].payload)
    assert applied.intervention_id == result.record.intervention_id
    assert applied.target_paths == result.record.target_paths
    assert committed.commit_id is None
    assert committed.intervention_id == result.record.intervention_id
    assert committed.public_paths == result.record.target_paths


def test_multi_target_intervention_commits_one_canonical_revision() -> None:
    state, schema, logical_time = _state_and_schema()
    result = InterventionGateway(
        schema=schema,
        policy=InterventionPolicy.allowlist((PATH_B, PATH_A)),
        evidence_recorder=InMemoryEvidenceRecorder(),
        id_factory=DeterministicIdFactory(UUID(int=15), "multi-target"),
    ).apply(
        current_state=state,
        spec=_spec(
            state,
            StateInterventionWrite(PATH_B, 2),
            StateInterventionWrite(PATH_A, 1),
        ),
        logical_time=logical_time,
    )

    assert result.record.target_paths == (PATH_A, PATH_B)
    assert result.state.envelope.state_revision == state.envelope.state_revision.next()
    assert result.state.entries[PATH_A].availability == Available(1)
    assert result.state.entries[PATH_B].availability == Available(2)


@pytest.mark.parametrize(
    "case",
    ("stale_revision", "wrong_lineage", "wrong_branch", "missing", "not_allowed"),
)
def test_rejected_base_or_target_consumes_no_identity_or_evidence(case: str) -> None:
    state, schema, logical_time = _state_and_schema()
    recorder = InMemoryEvidenceRecorder()
    factory = DeterministicIdFactory(UUID(int=20), "reject")
    policy = InterventionPolicy.allowlist((PATH_A,))
    spec = _spec(state, StateInterventionWrite(PATH_A, 1))
    if case == "stale_revision":
        spec = StateInterventionSpec(
            StateRevision(99), spec.base_lineage_id, spec.base_branch_id, spec.writes
        )
    elif case == "wrong_lineage":
        spec = StateInterventionSpec(
            spec.base_state_revision,
            _identity(LineageId, 99),
            spec.base_branch_id,
            spec.writes,
        )
    elif case == "wrong_branch":
        spec = StateInterventionSpec(
            spec.base_state_revision,
            spec.base_lineage_id,
            _identity(BranchId, 99),
            spec.writes,
        )
    elif case == "missing":
        spec = _spec(state, StateInterventionWrite(MISSING_PATH, 1))
    else:
        policy = InterventionPolicy.disabled()

    gateway = InterventionGateway(
        schema=schema,
        policy=policy,
        evidence_recorder=recorder,
        id_factory=factory,
    )
    with pytest.raises(InterventionError):
        gateway.apply(current_state=state, spec=spec, logical_time=logical_time)
    assert factory.counter == 0
    assert recorder.snapshot() == ()
    assert state.envelope.state_revision == StateRevision.initial()


@pytest.mark.parametrize("value", ("wrong", [1]))
def test_invalid_or_snapshot_unsafe_treatment_rejects_whole_batch(value: object) -> None:
    state, schema, logical_time = _state_and_schema()
    recorder = InMemoryEvidenceRecorder()
    factory = DeterministicIdFactory(UUID(int=30), "invalid-value")
    gateway = InterventionGateway(
        schema=schema,
        policy=InterventionPolicy.allowlist((PATH_A, PATH_B)),
        evidence_recorder=recorder,
        id_factory=factory,
    )
    spec = _spec(
        state,
        StateInterventionWrite(PATH_A, 1),
        StateInterventionWrite(PATH_B, value),
    )

    with pytest.raises(InterventionError):
        gateway.apply(current_state=state, spec=spec, logical_time=logical_time)
    assert factory.counter == 0
    assert recorder.snapshot() == ()
    assert all(isinstance(entry.availability, Unknown) for entry in state.entries.values())


def test_cycle_scoped_time_rejected_before_identity_allocation() -> None:
    state, schema, logical_time = _state_and_schema()
    recorder = InMemoryEvidenceRecorder()
    factory = DeterministicIdFactory(UUID(int=40), "unsafe-time")
    cycle_time = LogicalTime(
        run_id=logical_time.run_id,
        agent_session_id=logical_time.agent_session_id,
        episode_id=logical_time.episode_id,
        decision_window_id=logical_time.decision_window_id,
        cognitive_cycle_id=_identity(CognitiveCycleId, 42),
    )
    gateway = InterventionGateway(
        schema=schema,
        policy=InterventionPolicy.allowlist((PATH_A,)),
        evidence_recorder=recorder,
        id_factory=factory,
    )
    with pytest.raises(InterventionError, match="between-cycle"):
        gateway.apply(
            current_state=state,
            spec=_spec(state, StateInterventionWrite(PATH_A, 1)),
            logical_time=cycle_time,
        )
    assert factory.counter == 0
    assert recorder.snapshot() == ()


class _FailingRecorder:
    def record(self, event: TraceEventEnvelope, /) -> None:
        raise RuntimeError("recorder failed")


def test_evidence_failure_propagates_without_mutating_base_state() -> None:
    state, schema, logical_time = _state_and_schema()
    gateway = InterventionGateway(
        schema=schema,
        policy=InterventionPolicy.allowlist((PATH_A,)),
        evidence_recorder=cast(EvidenceRecorder, _FailingRecorder()),
        id_factory=DeterministicIdFactory(UUID(int=50), "evidence-failure"),
    )
    with pytest.raises(RuntimeError, match="recorder failed"):
        gateway.apply(
            current_state=state,
            spec=_spec(state, StateInterventionWrite(PATH_A, 1)),
            logical_time=logical_time,
        )
    assert state.envelope.state_revision == StateRevision.initial()
    assert isinstance(state.entries[PATH_A].availability, Unknown)
