"""Контрактные проверки synthetic reference modules."""

from dataclasses import FrozenInstanceError
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentSessionId,
    Available,
    CognitiveCycleId,
    CognitiveModule,
    DecisionWindowId,
    DeterminismMode,
    EpisodeId,
    ExecutionPhase,
    FreshnessMode,
    ImplementationId,
    ImplementationRevision,
    LogicalTime,
    ModuleAttemptId,
    ModuleComputeRequest,
    ModuleExecutionContext,
    ModuleId,
    ModuleStatefulness,
    ReadSpec,
    RunId,
    StateEntry,
    StateKey,
    StateProjection,
    StateProvenance,
    StateRevision,
    Unavailable,
)
from mindra.reference import (
    SYNTHETIC_DOUBLE_VALUE_KEY,
    SYNTHETIC_JOIN_VALUE_KEY,
    SYNTHETIC_SOURCE_VALUE_KEY,
    SYNTHETIC_TRIPLE_VALUE_KEY,
    SyntheticDoubleModule,
    SyntheticJoinModule,
    SyntheticSourceModule,
    SyntheticTripleModule,
)

_LOGICAL_TIME = LogicalTime(
    run_id=RunId(UUID(int=1)),
    agent_session_id=AgentSessionId(UUID(int=2)),
    episode_id=EpisodeId(UUID(int=3)),
    decision_window_id=DecisionWindowId(UUID(int=4)),
    cognitive_cycle_id=CognitiveCycleId(UUID(int=5)),
)
_BASE_REVISION = StateRevision(7)


def _entry(key_owner: str, value: int) -> StateEntry[object]:
    return cast(
        StateEntry[object],
        StateEntry(
            availability=Available(value),
            provenance=StateProvenance(
                producer=ModuleId(key_owner),
                implementation_id=ImplementationId(f"reference.{key_owner.replace('.', '_')}.v1"),
                base_state_revision=_BASE_REVISION,
                module_attempt_id=ModuleAttemptId(UUID(int=20)),
                logical_time=_LOGICAL_TIME,
            ),
        ),
    )


def _request(
    reads: tuple[ReadSpec[object], ...],
    entries: dict[StateKey[int], StateEntry[object]] | None = None,
    *,
    attempt: int = 30,
) -> ModuleComputeRequest:
    entries = entries or {}
    projection = StateProjection._from_runtime(
        read_specs=reads,
        entries={key.path: entry for key, entry in entries.items()},
        logical_time=_LOGICAL_TIME,
    )
    return ModuleComputeRequest(
        state=projection,
        private_state=Unavailable(),
        context=ModuleExecutionContext(
            module_attempt_id=ModuleAttemptId(UUID(int=attempt)),
            base_state_revision=_BASE_REVISION,
            logical_time=_LOGICAL_TIME,
            phase=ExecutionPhase.COGNITIVE_CYCLE,
        ),
    )


type ReferenceModule = (
    SyntheticSourceModule | SyntheticDoubleModule | SyntheticTripleModule | SyntheticJoinModule
)


def _output(module: ReferenceModule, request: ModuleComputeRequest) -> int:
    result = module.compute(request)
    write = result.state_update.writes[0]
    assert isinstance(write.availability, Available)
    assert type(write.availability.value) is int
    return write.availability.value


def test_reference_modules_satisfy_protocol_and_have_exact_identities() -> None:
    modules = (
        SyntheticSourceModule(value=2),
        SyntheticDoubleModule(),
        SyntheticTripleModule(),
        SyntheticJoinModule(),
    )
    expected = (
        ("synthetic.source", "reference.synthetic_source.v1"),
        ("synthetic.double", "reference.synthetic_double.v1"),
        ("synthetic.triple", "reference.synthetic_triple.v1"),
        ("synthetic.join", "reference.synthetic_join.v1"),
    )

    assert all(isinstance(module, CognitiveModule) for module in modules)
    assert (
        tuple(
            (module.descriptor.module_id.value, module.descriptor.implementation_id.value)
            for module in modules
        )
        == expected
    )
    assert all(
        module.descriptor.implementation_revision == ImplementationRevision("v1")
        for module in modules
    )


def test_descriptors_have_exact_stateless_deterministic_graph_contracts() -> None:
    source = SyntheticSourceModule(value=2).descriptor
    double = SyntheticDoubleModule().descriptor
    triple = SyntheticTripleModule().descriptor
    join = SyntheticJoinModule().descriptor

    for descriptor in (source, double, triple, join):
        assert descriptor.private_state is None
        assert descriptor.phases == frozenset({ExecutionPhase.COGNITIVE_CYCLE})
        assert descriptor.traits.statefulness is ModuleStatefulness.STATELESS
        assert descriptor.traits.determinism is DeterminismMode.DETERMINISTIC

    assert source.reads == ()
    assert source.writes == (SYNTHETIC_SOURCE_VALUE_KEY,)
    assert tuple(read.key for read in double.reads) == (SYNTHETIC_SOURCE_VALUE_KEY,)
    assert double.writes == (SYNTHETIC_DOUBLE_VALUE_KEY,)
    assert tuple(read.key for read in triple.reads) == (SYNTHETIC_SOURCE_VALUE_KEY,)
    assert triple.writes == (SYNTHETIC_TRIPLE_VALUE_KEY,)
    assert tuple(read.key for read in join.reads) == (
        SYNTHETIC_DOUBLE_VALUE_KEY,
        SYNTHETIC_TRIPLE_VALUE_KEY,
    )
    assert join.writes == (SYNTHETIC_JOIN_VALUE_KEY,)
    for read in (*double.reads, *triple.reads, *join.reads):
        assert read.required is True
        assert read.allowed_availability == frozenset({Available})
        assert read.freshness is FreshnessMode.CURRENT_CYCLE


@pytest.mark.parametrize("invalid", [True, False, 2.0, "2", None])
def test_source_rejects_bool_and_non_int_values(invalid: object) -> None:
    with pytest.raises(TypeError):
        SyntheticSourceModule(value=cast(int, invalid))


def test_source_accepts_unbounded_int_and_setting_is_immutable() -> None:
    module = SyntheticSourceModule(value=10**100)
    attribute = "value"

    assert module.value == 10**100
    with pytest.raises(FrozenInstanceError):
        setattr(module, attribute, 1)


def test_modules_compute_exact_arithmetic_without_mutating_projection() -> None:
    source = SyntheticSourceModule(value=2)
    source_request = _request(source.descriptor.reads)
    assert _output(source, source_request) == 2

    source_entry = _entry("synthetic.source", 2)
    double = SyntheticDoubleModule()
    double_request = _request(
        double.descriptor.reads,
        {SYNTHETIC_SOURCE_VALUE_KEY: source_entry},
    )
    assert _output(double, double_request) == 4
    assert double_request.state.read(SYNTHETIC_SOURCE_VALUE_KEY) == source_entry

    triple = SyntheticTripleModule()
    assert (
        _output(
            triple,
            _request(
                triple.descriptor.reads,
                {SYNTHETIC_SOURCE_VALUE_KEY: source_entry},
            ),
        )
        == 6
    )

    join = SyntheticJoinModule()
    assert (
        _output(
            join,
            _request(
                join.descriptor.reads,
                {
                    SYNTHETIC_DOUBLE_VALUE_KEY: _entry("synthetic.double", 4),
                    SYNTHETIC_TRIPLE_VALUE_KEY: _entry("synthetic.triple", 6),
                },
            ),
        )
        == 10
    )


@pytest.mark.parametrize(
    ("module", "entries", "output_key"),
    [
        (SyntheticSourceModule(value=2), {}, SYNTHETIC_SOURCE_VALUE_KEY),
        (
            SyntheticDoubleModule(),
            {SYNTHETIC_SOURCE_VALUE_KEY: _entry("synthetic.source", 2)},
            SYNTHETIC_DOUBLE_VALUE_KEY,
        ),
        (
            SyntheticTripleModule(),
            {SYNTHETIC_SOURCE_VALUE_KEY: _entry("synthetic.source", 2)},
            SYNTHETIC_TRIPLE_VALUE_KEY,
        ),
        (
            SyntheticJoinModule(),
            {
                SYNTHETIC_DOUBLE_VALUE_KEY: _entry("synthetic.double", 4),
                SYNTHETIC_TRIPLE_VALUE_KEY: _entry("synthetic.triple", 6),
            },
            SYNTHETIC_JOIN_VALUE_KEY,
        ),
    ],
)
def test_results_mirror_request_and_descriptor_provenance(
    module: ReferenceModule,
    entries: dict[StateKey[int], StateEntry[object]],
    output_key: StateKey[int],
) -> None:
    request = _request(module.descriptor.reads, entries, attempt=31)
    result = module.compute(request)
    proposal = result.state_update

    assert proposal.base_state_revision == request.context.base_state_revision
    assert proposal.producer == module.descriptor.module_id
    assert proposal.module_attempt_id == request.context.module_attempt_id
    assert len(proposal.writes) == 1
    write = proposal.writes[0]
    assert write.key == output_key
    assert write.provenance.producer == module.descriptor.module_id
    assert write.provenance.implementation_id == module.descriptor.implementation_id
    assert write.provenance.base_state_revision == request.context.base_state_revision
    assert write.provenance.module_attempt_id == request.context.module_attempt_id
    assert write.provenance.logical_time == request.context.logical_time
    assert write.provenance.source_refs == ()
    assert write.provenance.parent_refs == ()
    assert write.provenance.intervention_refs == ()
    assert result.private_state_update is None
