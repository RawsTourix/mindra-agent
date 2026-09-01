"""Unit checks immutable structural O0 evidence records."""

from collections.abc import Callable
from dataclasses import FrozenInstanceError, fields
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    BranchId,
    CognitiveCycleId,
    CommitAttemptedEvent,
    CommitFailedEvent,
    CommitId,
    CommitSucceededEvent,
    CompositionResolvedEvent,
    CompositionRevision,
    CycleFailedEvent,
    CycleFinishedEvent,
    CycleStartedEvent,
    DecisionWindowId,
    DeterminismMode,
    EpisodeId,
    ExecutionPhase,
    ExecutionPlanId,
    ExecutionPlanRevision,
    ImplementationId,
    ImplementationRevision,
    InterventionAppliedEvent,
    InterventionId,
    LineageId,
    LogicalTime,
    ModuleAttemptFinishedEvent,
    ModuleAttemptId,
    ModuleAttemptOutcome,
    ModuleAttemptStartedEvent,
    ModuleId,
    ModuleStatefulness,
    PlanCompiledEvent,
    PlanDependencyTrace,
    PlanWaveTrace,
    PrivateRevisionTransitionTrace,
    PrivateStateRevision,
    ProfileId,
    ResolvedModuleTrace,
    RunId,
    SchemaRevision,
    StatePath,
    StateRevision,
    StateRevisionCommittedEvent,
    TraceEventEnvelope,
    TraceEventKind,
    TraceEventPayload,
    TraceFailure,
    WaveAttemptId,
    WaveId,
    WaveStartedEvent,
)

SHA256_A = "a" * 64
SHA256_B = "b" * 64


def _uuid(value: int) -> UUID:
    return UUID(int=value)


def _base_time() -> LogicalTime:
    return LogicalTime(
        run_id=RunId(_uuid(1)),
        agent_session_id=AgentSessionId(_uuid(2)),
    )


def _cycle_time() -> LogicalTime:
    return LogicalTime(
        run_id=RunId(_uuid(1)),
        agent_session_id=AgentSessionId(_uuid(2)),
        episode_id=EpisodeId(_uuid(3)),
        decision_window_id=DecisionWindowId(_uuid(4)),
        cognitive_cycle_id=CognitiveCycleId(_uuid(5)),
    )


def _wave_time() -> LogicalTime:
    cycle = _cycle_time()
    return LogicalTime(
        run_id=cycle.run_id,
        agent_session_id=cycle.agent_session_id,
        episode_id=cycle.episode_id,
        decision_window_id=cycle.decision_window_id,
        cognitive_cycle_id=cycle.cognitive_cycle_id,
        wave_id=WaveId(_uuid(6)),
    )


def _path(value: str) -> StatePath:
    return StatePath.from_dotted(value)


def _resolved_module(name: str) -> ResolvedModuleTrace:
    return ResolvedModuleTrace(
        module_id=ModuleId(name),
        implementation_id=ImplementationId(f"reference.{name}.v1"),
        implementation_revision=ImplementationRevision("v1"),
        statefulness=ModuleStatefulness.STATELESS,
        determinism=DeterminismMode.DETERMINISTIC,
    )


def _payload_cases() -> tuple[tuple[TraceEventKind, LogicalTime, TraceEventPayload], ...]:
    base_revision = StateRevision(4)
    attempt_id = ModuleAttemptId(_uuid(11))
    wave_attempt_id = WaveAttemptId(_uuid(12))
    failure = TraceFailure("ValueError", "invalid")
    public_path = _path("alpha.value")
    return (
        (
            TraceEventKind.COMPOSITION_RESOLVED,
            _base_time(),
            CompositionResolvedEvent(
                profile_id=ProfileId("reference.profile"),
                composition_revision=CompositionRevision(1),
                schema_revision=SchemaRevision(2),
                agent_revision_id=AgentRevisionId(_uuid(7)),
                composition_fingerprint=SHA256_A,
                modules=(_resolved_module("alpha"),),
            ),
        ),
        (
            TraceEventKind.PLAN_COMPILED,
            _base_time(),
            PlanCompiledEvent(
                plan_id=ExecutionPlanId(_uuid(8)),
                plan_revision=ExecutionPlanRevision(1),
                composition_revision=CompositionRevision(1),
                schema_revision=SchemaRevision(2),
                phase=ExecutionPhase.COGNITIVE_CYCLE,
                plan_fingerprint=SHA256_B,
                dependencies=(),
                waves=(PlanWaveTrace(0, (ModuleId("alpha"),)),),
            ),
        ),
        (
            TraceEventKind.CYCLE_STARTED,
            _cycle_time(),
            CycleStartedEvent(
                base_state_revision=base_revision,
                plan_id=ExecutionPlanId(_uuid(8)),
                plan_revision=ExecutionPlanRevision(1),
                agent_revision_id=AgentRevisionId(_uuid(7)),
            ),
        ),
        (
            TraceEventKind.WAVE_STARTED,
            _wave_time(),
            WaveStartedEvent(
                wave_attempt_id=wave_attempt_id,
                wave_index=0,
                base_state_revision=base_revision,
                module_ids=(ModuleId("alpha"),),
            ),
        ),
        (
            TraceEventKind.MODULE_ATTEMPT_STARTED,
            _wave_time(),
            ModuleAttemptStartedEvent(
                wave_attempt_id=wave_attempt_id,
                module_id=ModuleId("alpha"),
                module_attempt_id=attempt_id,
                implementation_id=ImplementationId("reference.alpha.v1"),
                implementation_revision=ImplementationRevision("v1"),
                base_state_revision=base_revision,
                base_private_revision=None,
            ),
        ),
        (
            TraceEventKind.MODULE_ATTEMPT_FINISHED,
            _wave_time(),
            ModuleAttemptFinishedEvent(
                module_id=ModuleId("alpha"),
                module_attempt_id=attempt_id,
                outcome=ModuleAttemptOutcome.SUCCEEDED,
                proposed_public_paths=(public_path,),
                private_update_proposed=False,
                failure=None,
            ),
        ),
        (
            TraceEventKind.COMMIT_ATTEMPTED,
            _wave_time(),
            CommitAttemptedEvent(wave_attempt_id, base_revision, (attempt_id,)),
        ),
        (
            TraceEventKind.COMMIT_SUCCEEDED,
            _wave_time(),
            CommitSucceededEvent(
                wave_attempt_id=wave_attempt_id,
                commit_id=CommitId(_uuid(13)),
                base_state_revision=base_revision,
                resulting_state_revision=base_revision.next(),
                module_attempt_ids=(attempt_id,),
                public_paths=(public_path,),
                private_revisions=(),
            ),
        ),
        (
            TraceEventKind.COMMIT_FAILED,
            _wave_time(),
            CommitFailedEvent(wave_attempt_id, base_revision, (attempt_id,), failure),
        ),
        (
            TraceEventKind.STATE_REVISION_COMMITTED,
            _base_time(),
            StateRevisionCommittedEvent(
                before=base_revision,
                after=base_revision.next(),
                public_paths=(public_path,),
                lineage_id=LineageId(_uuid(14)),
                branch_id=BranchId(_uuid(15)),
                agent_revision_id=AgentRevisionId(_uuid(7)),
                commit_id=CommitId(_uuid(13)),
                intervention_id=None,
            ),
        ),
        (
            TraceEventKind.INTERVENTION_APPLIED,
            _base_time(),
            InterventionAppliedEvent(
                intervention_id=InterventionId(_uuid(16)),
                base_state_revision=base_revision,
                resulting_state_revision=base_revision.next(),
                target_paths=(public_path,),
                lineage_id=LineageId(_uuid(14)),
                branch_id=BranchId(_uuid(15)),
            ),
        ),
        (
            TraceEventKind.CYCLE_FINISHED,
            _cycle_time(),
            CycleFinishedEvent(base_revision, base_revision),
        ),
        (
            TraceEventKind.CYCLE_FAILED,
            _cycle_time(),
            CycleFailedEvent(base_revision, base_revision.next(), failure),
        ),
    )


def test_v01_event_cases_have_exact_typed_payload_and_derived_kind() -> None:
    cases = _payload_cases()
    envelopes = tuple(TraceEventEnvelope(time, payload) for _, time, payload in cases)

    assert len(cases) == 13
    assert {kind for kind, _, _ in cases} == {
        kind for kind in TraceEventKind if not kind.value.startswith("lifecycle_phase_")
    }
    assert tuple(envelope.kind for envelope in envelopes) == tuple(kind for kind, _, _ in cases)


def test_envelope_has_no_public_kind_constructor_field_for_mismatch() -> None:
    _, logical_time, payload = _payload_cases()[-1]
    constructor = cast(Callable[..., TraceEventEnvelope], TraceEventEnvelope)

    assert {field.name for field in fields(TraceEventEnvelope)} == {
        "logical_time",
        "payload",
        "physical_timestamp_ns",
    }
    with pytest.raises(TypeError, match="unexpected keyword argument 'kind'"):
        constructor(
            logical_time=logical_time,
            payload=payload,
            kind=TraceEventKind.COMMIT_SUCCEEDED,
        )


def test_envelope_rejects_payload_subclass_outside_exact_union() -> None:
    class _DerivedCycleFinishedEvent(CycleFinishedEvent):
        pass

    payload = _DerivedCycleFinishedEvent(StateRevision(0), StateRevision(0))

    with pytest.raises(TypeError, match="exact TraceEventPayload"):
        TraceEventEnvelope(_cycle_time(), cast(TraceEventPayload, payload))


def test_all_envelopes_helpers_and_payloads_are_frozen() -> None:
    helpers: tuple[object, ...] = (
        TraceFailure("ValueError", "invalid"),
        _resolved_module("alpha"),
        PlanDependencyTrace(ModuleId("alpha"), ModuleId("beta"), _path("alpha.value")),
        PlanWaveTrace(0, (ModuleId("alpha"),)),
        PrivateRevisionTransitionTrace(
            ModuleId("alpha"), PrivateStateRevision(0), PrivateStateRevision(1)
        ),
    )
    records = helpers + tuple(payload for _, _, payload in _payload_cases())
    records += (TraceEventEnvelope(_base_time(), _payload_cases()[0][2]),)

    for record in records:
        field = fields(cast(TraceFailure, record))[0]
        with pytest.raises(FrozenInstanceError):
            setattr(record, field.name, getattr(record, field.name))


@pytest.mark.parametrize("timestamp", [-1, True, 1.5, "1"])
def test_invalid_physical_timestamp_is_rejected(timestamp: object) -> None:
    payload = _payload_cases()[0][2]
    constructor = cast(Callable[..., TraceEventEnvelope], TraceEventEnvelope)

    with pytest.raises(TypeError if timestamp in {True, 1.5, "1"} else ValueError):
        constructor(_base_time(), payload, timestamp)


def test_cycle_and_wave_events_require_expected_temporal_depth() -> None:
    cycle_payload = CycleFinishedEvent(StateRevision(0), StateRevision(0))
    wave_payload = CommitAttemptedEvent(WaveAttemptId(_uuid(10)), StateRevision(0), ())

    with pytest.raises(ValueError, match="cognitive_cycle_id"):
        TraceEventEnvelope(_base_time(), cycle_payload)
    with pytest.raises(ValueError, match="wave_id"):
        TraceEventEnvelope(_cycle_time(), wave_payload)


def test_composition_modules_require_canonical_unique_order_and_fingerprint() -> None:
    alpha = _resolved_module("alpha")
    beta = _resolved_module("beta")

    with pytest.raises(ValueError, match="canonical unique"):
        CompositionResolvedEvent(
            ProfileId("reference.profile"),
            CompositionRevision(0),
            SchemaRevision(0),
            AgentRevisionId(_uuid(1)),
            SHA256_A,
            (beta, alpha),
        )
    with pytest.raises(ValueError, match="SHA-256"):
        CompositionResolvedEvent(
            ProfileId("reference.profile"),
            CompositionRevision(0),
            SchemaRevision(0),
            AgentRevisionId(_uuid(1)),
            "A" * 64,
            (alpha,),
        )


def test_plan_requires_valid_fingerprint_dependencies_and_waves() -> None:
    alpha_to_beta = PlanDependencyTrace(ModuleId("alpha"), ModuleId("beta"), _path("alpha.value"))
    beta_to_gamma = PlanDependencyTrace(ModuleId("beta"), ModuleId("gamma"), _path("beta.value"))
    common: dict[str, object] = {
        "plan_id": ExecutionPlanId(_uuid(1)),
        "plan_revision": ExecutionPlanRevision(0),
        "composition_revision": CompositionRevision(0),
        "schema_revision": SchemaRevision(0),
        "phase": ExecutionPhase.COGNITIVE_CYCLE,
        "plan_fingerprint": SHA256_A,
    }
    constructor = cast(Callable[..., PlanCompiledEvent], PlanCompiledEvent)

    with pytest.raises(ValueError, match="canonical ordering"):
        constructor(
            **common,
            dependencies=(beta_to_gamma, alpha_to_beta),
            waves=(),
        )
    with pytest.raises(ValueError, match="gaps"):
        constructor(
            **common,
            dependencies=(),
            waves=(PlanWaveTrace(1, (ModuleId("alpha"),)),),
        )
    with pytest.raises(ValueError, match="максимум в одну"):
        constructor(
            **common,
            dependencies=(),
            waves=(
                PlanWaveTrace(0, (ModuleId("alpha"),)),
                PlanWaveTrace(1, (ModuleId("alpha"),)),
            ),
        )
    with pytest.raises(ValueError, match="SHA-256"):
        constructor(**{**common, "plan_fingerprint": "bad"}, dependencies=(), waves=())


def test_trace_failure_copies_only_printable_diagnostics() -> None:
    error = ValueError("bad value")
    failure = TraceFailure.from_exception(error)

    assert failure == TraceFailure("ValueError", "bad value")
    assert {field.name for field in fields(TraceFailure)} == {"error_type", "message"}
    assert not hasattr(failure, "exception")
    assert not hasattr(failure, "traceback")
    with pytest.raises(ValueError, match="printable"):
        TraceFailure("ValueError", "bad\nvalue")


def test_module_attempt_outcome_and_proposal_metadata_invariants() -> None:
    common: dict[str, object] = {
        "module_id": ModuleId("alpha"),
        "module_attempt_id": ModuleAttemptId(_uuid(1)),
    }
    constructor = cast(Callable[..., ModuleAttemptFinishedEvent], ModuleAttemptFinishedEvent)

    with pytest.raises(ValueError, match="Successful"):
        constructor(
            **common,
            outcome=ModuleAttemptOutcome.SUCCEEDED,
            proposed_public_paths=(),
            private_update_proposed=False,
            failure=TraceFailure("ValueError", "bad"),
        )
    with pytest.raises(ValueError, match="требует TraceFailure"):
        constructor(
            **common,
            outcome=ModuleAttemptOutcome.FAILED,
            proposed_public_paths=(),
            private_update_proposed=False,
            failure=None,
        )
    with pytest.raises(ValueError, match="proposal metadata"):
        constructor(
            **common,
            outcome=ModuleAttemptOutcome.FAILED,
            proposed_public_paths=(_path("alpha.value"),),
            private_update_proposed=False,
            failure=TraceFailure("ValueError", "bad"),
        )
    with pytest.raises(ValueError, match="canonical unique"):
        constructor(
            **common,
            outcome=ModuleAttemptOutcome.SUCCEEDED,
            proposed_public_paths=(_path("beta.value"), _path("alpha.value")),
            private_update_proposed=False,
            failure=None,
        )


def test_commit_attempts_require_unique_ids_but_preserve_producer_order() -> None:
    first = ModuleAttemptId(_uuid(2))
    second = ModuleAttemptId(_uuid(1))
    event = CommitAttemptedEvent(WaveAttemptId(_uuid(3)), StateRevision(0), (first, second))

    assert event.module_attempt_ids == (first, second)
    with pytest.raises(ValueError, match="duplicate"):
        CommitAttemptedEvent(WaveAttemptId(_uuid(3)), StateRevision(0), (first, first))


@pytest.mark.parametrize(
    ("public_paths", "private_revisions", "resulting_revision"),
    [
        ((_path("alpha.value"),), (), StateRevision(2)),
        (
            (),
            (
                PrivateRevisionTransitionTrace(
                    ModuleId("alpha"), PrivateStateRevision(0), PrivateStateRevision(1)
                ),
            ),
            StateRevision(1),
        ),
        ((), (), StateRevision(1)),
    ],
)
def test_commit_succeeded_public_private_and_noop_revision_semantics(
    public_paths: tuple[StatePath, ...],
    private_revisions: tuple[PrivateRevisionTransitionTrace, ...],
    resulting_revision: StateRevision,
) -> None:
    event = CommitSucceededEvent(
        wave_attempt_id=WaveAttemptId(_uuid(1)),
        commit_id=CommitId(_uuid(2)),
        base_state_revision=StateRevision(1),
        resulting_state_revision=resulting_revision,
        module_attempt_ids=(),
        public_paths=public_paths,
        private_revisions=private_revisions,
    )

    assert event.resulting_state_revision == resulting_revision


def test_private_transition_requires_exact_next_revision() -> None:
    with pytest.raises(ValueError, match=r"before\.next"):
        PrivateRevisionTransitionTrace(
            ModuleId("alpha"), PrivateStateRevision(0), PrivateStateRevision(2)
        )


def test_state_revision_committed_requires_transition_paths_and_one_origin() -> None:
    common: dict[str, object] = {
        "before": StateRevision(1),
        "after": StateRevision(2),
        "public_paths": (_path("alpha.value"),),
        "lineage_id": LineageId(_uuid(1)),
        "branch_id": BranchId(_uuid(2)),
        "agent_revision_id": AgentRevisionId(_uuid(3)),
    }
    constructor = cast(Callable[..., StateRevisionCommittedEvent], StateRevisionCommittedEvent)

    with pytest.raises(ValueError, match=r"before\.next"):
        constructor(
            **{**common, "after": StateRevision(3)},
            commit_id=CommitId(_uuid(4)),
            intervention_id=None,
        )
    with pytest.raises(ValueError, match="не может быть пустым"):
        constructor(
            **{**common, "public_paths": ()},
            commit_id=CommitId(_uuid(4)),
            intervention_id=None,
        )
    with pytest.raises(ValueError, match="ровно один origin"):
        constructor(**common, commit_id=None, intervention_id=None)
    with pytest.raises(ValueError, match="ровно один origin"):
        constructor(
            **common,
            commit_id=CommitId(_uuid(4)),
            intervention_id=InterventionId(_uuid(5)),
        )


def test_intervention_requires_exact_next_and_canonical_nonempty_targets() -> None:
    common: dict[str, object] = {
        "intervention_id": InterventionId(_uuid(1)),
        "base_state_revision": StateRevision(1),
        "resulting_state_revision": StateRevision(2),
        "target_paths": (_path("alpha.value"),),
        "lineage_id": LineageId(_uuid(2)),
        "branch_id": BranchId(_uuid(3)),
    }
    constructor = cast(Callable[..., InterventionAppliedEvent], InterventionAppliedEvent)

    with pytest.raises(ValueError, match=r"base\.next"):
        constructor(**{**common, "resulting_state_revision": StateRevision(3)})
    with pytest.raises(ValueError, match="не может быть пустым"):
        constructor(**{**common, "target_paths": ()})


def test_cycle_finished_allows_equality_and_failed_cycle_keeps_later_revision() -> None:
    finished = CycleFinishedEvent(StateRevision(3), StateRevision(3))
    failed = CycleFailedEvent(
        StateRevision(3), StateRevision(5), TraceFailure("RuntimeError", "failed")
    )

    assert finished.resulting_state_revision == finished.base_state_revision
    assert failed.current_state_revision > failed.base_state_revision
