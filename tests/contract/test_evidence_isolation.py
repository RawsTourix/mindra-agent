"""Contract checks passive evidence isolation от cognition и runtime owners."""

import ast
import inspect
from dataclasses import fields
from pathlib import Path
from typing import cast
from uuid import UUID

import pytest

import mindra.contracts.evidence as evidence_contracts
from mindra.contracts import (
    AgentSessionId,
    CompositionResolvedEvent,
    CompositionRevision,
    EvidenceRecorder,
    LogicalTime,
    ModuleComputeRequest,
    ProfileId,
    RunId,
    SchemaRevision,
    StateProjection,
    TraceEventEnvelope,
)
from mindra.contracts.identity import AgentRevisionId
from mindra.runtime import CommitCoordinator, ExecutionPlanCompiler, InMemoryEvidenceRecorder


def _event(timestamp: int | None = None) -> TraceEventEnvelope:
    return TraceEventEnvelope(
        logical_time=LogicalTime(
            run_id=RunId(UUID(int=1)),
            agent_session_id=AgentSessionId(UUID(int=2)),
        ),
        payload=CompositionResolvedEvent(
            profile_id=ProfileId("reference.profile"),
            composition_revision=CompositionRevision(0),
            schema_revision=SchemaRevision(0),
            agent_revision_id=AgentRevisionId(UUID(int=3)),
            composition_fingerprint="a" * 64,
            modules=(),
        ),
        physical_timestamp_ns=timestamp,
    )


def test_in_memory_recorder_structurally_conforms_to_protocol() -> None:
    recorder = InMemoryEvidenceRecorder()

    assert isinstance(recorder, EvidenceRecorder)


def test_recorder_preserves_insertion_order_and_exact_event_objects() -> None:
    recorder = InMemoryEvidenceRecorder()
    first = _event()
    second = _event(10)

    recorder.record(first)
    recorder.record(second)

    assert len(recorder) == 2
    assert recorder.snapshot() == (first, second)
    assert recorder.snapshot()[0] is first
    assert recorder.snapshot()[1] is second


def test_snapshot_is_tuple_hides_backing_list_and_remains_stable() -> None:
    recorder = InMemoryEvidenceRecorder()
    first = _event()
    second = _event(10)
    recorder.record(first)
    snapshot = recorder.snapshot()

    recorder.record(second)

    assert type(snapshot) is tuple
    assert snapshot == (first,)
    assert recorder.snapshot() == (first, second)
    assert not hasattr(recorder, "events")
    assert not hasattr(recorder, "records")


def test_recorder_has_only_append_operation_and_rejects_invalid_record() -> None:
    recorder = InMemoryEvidenceRecorder()

    for method_name in ("clear", "pop", "remove", "replace", "truncate"):
        assert not hasattr(recorder, method_name)
    with pytest.raises(TypeError, match="TraceEventEnvelope"):
        recorder.record(cast(TraceEventEnvelope, object()))
    assert len(recorder) == 0


def test_recorder_does_not_create_identity_or_timestamp() -> None:
    recorder = InMemoryEvidenceRecorder()
    event = _event()

    recorder.record(event)

    recorded = recorder.snapshot()[0]
    assert recorded is event
    assert recorded.physical_timestamp_ns is None
    assert inspect.signature(InMemoryEvidenceRecorder).parameters == {}


def test_contracts_evidence_has_no_runtime_import() -> None:
    source_path = Path(evidence_contracts.__file__)
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    imported_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }

    assert all(not module.startswith("mindra.runtime") for module in imported_modules)


def test_cognitive_contracts_have_no_evidence_capability() -> None:
    assert {field.name for field in fields(ModuleComputeRequest)} == {
        "state",
        "private_state",
        "context",
    }
    assert {field.name for field in fields(StateProjection)} == {
        "_read_specs",
        "_entries",
        "_logical_time",
    }
    for capability in ("evidence", "recorder", "logger", "evaluator", "trace"):
        assert not hasattr(ModuleComputeRequest, capability)
        assert not hasattr(StateProjection, capability)


def test_runtime_recorder_has_no_state_private_or_intervention_authority() -> None:
    recorder = InMemoryEvidenceRecorder()

    for capability in (
        "state",
        "private_state",
        "commit",
        "apply",
        "intervene",
        "write",
        "replace",
    ):
        assert not hasattr(recorder, capability)


def test_existing_planner_and_commit_boundaries_have_no_automatic_emission() -> None:
    compiler_parameters = inspect.signature(ExecutionPlanCompiler).parameters
    coordinator_parameters = inspect.signature(CommitCoordinator).parameters

    assert "evidence" not in compiler_parameters
    assert "recorder" not in compiler_parameters
    assert "evidence" not in coordinator_parameters
    assert "recorder" not in coordinator_parameters
    assert "evidence" not in ExecutionPlanCompiler.__slots__
    assert "recorder" not in ExecutionPlanCompiler.__slots__
    assert "evidence" not in CommitCoordinator.__slots__
    assert "recorder" not in CommitCoordinator.__slots__
