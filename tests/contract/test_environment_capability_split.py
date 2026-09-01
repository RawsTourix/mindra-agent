"""Проверки machine-distinct Environment Interaction и Research planes."""

from __future__ import annotations

import ast
import sys
import tomllib
from dataclasses import dataclass, fields
from pathlib import Path
from uuid import UUID

import pytest

from mindra.contracts import (
    ActionCapabilityDescriptor,
    AgentVisibleActionOutcome,
    AgentVisibleField,
    AgentVisibleRecord,
    CommittedEnvironmentAction,
    EnvironmentCapabilities,
    EnvironmentDescriptor,
    EnvironmentGenerationProvenance,
    EnvironmentInteraction,
    EnvironmentInteractionDescriptor,
    EnvironmentResearch,
    EnvironmentResearchTransitionRecord,
    EnvironmentResearchView,
    EnvironmentSnapshot,
    EnvironmentSnapshotId,
    EnvironmentSnapshotMetadata,
    EnvironmentTransitionReceipt,
    EnvironmentTransitionRef,
    EpisodeStartRequest,
    EpisodeStartResult,
    ExternalTaskFeedback,
    ExternalTaskSpecification,
    InteractionResult,
    RawObservation,
    SchemaError,
    ValueContract,
    WorldInstanceId,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_ROOT = PROJECT_ROOT / "src" / "mindra" / "contracts"

INTERACTION_METHODS = {"apply_committed_action", "describe_interaction", "reset"}
RESEARCH_METHODS = {"clone", "fork", "inspect", "restore", "snapshot", "transition_records"}
FORBIDDEN_AGENT_FIELDS = {
    "distribution_id",
    "ground_truth",
    "hidden_rules",
    "hidden_state",
    "objective_metric",
    "oracle",
    "research_transition",
    "rng_state",
    "seed",
    "split",
    "termination_reason",
    "world_instance_id",
    "world_manifest",
}


def _interaction_descriptor() -> EnvironmentInteractionDescriptor:
    return EnvironmentInteractionDescriptor(
        environment_family="microworld",
        environment_semantic_version="0.2",
        interaction_interface_revision=0,
        observation_schema_revision=0,
        task_schema_revision=0,
        feedback_schema_revision=0,
        action_capability=ActionCapabilityDescriptor(
            action_schema_revision=0,
            supported_action_kinds=("drop", "interact", "move", "pickup", "wait"),
        ),
    )


def _environment_descriptor() -> EnvironmentDescriptor:
    return EnvironmentDescriptor(
        interaction=_interaction_descriptor(),
        engine_version="0.2",
        generator_version="0.2",
        task_family="direct_reach",
        task_version="0.1",
        distribution_id="test",
        distribution_version="0.1",
        world_instance_id=WorldInstanceId(UUID(int=1)),
        world_manifest_ref="world:1",
    )


@dataclass(frozen=True, slots=True)
class FakeSnapshot:
    metadata: EnvironmentSnapshotMetadata


class FakeInteraction:
    def describe_interaction(self) -> EnvironmentInteractionDescriptor:
        return _interaction_descriptor()

    def reset(self, request: EpisodeStartRequest, /) -> EpisodeStartResult:
        raise NotImplementedError(request)

    def apply_committed_action(
        self,
        action: CommittedEnvironmentAction,
        /,
    ) -> InteractionResult:
        raise NotImplementedError(action)


class FakeResearch:
    def __init__(self, interaction: FakeInteraction, snapshot: FakeSnapshot) -> None:
        self._interaction = interaction
        self._snapshot = snapshot

    def inspect(self) -> EnvironmentResearchView:
        return EnvironmentResearchView(
            descriptor=_environment_descriptor(),
            hidden_state_ref="hidden:1",
            generation=EnvironmentGenerationProvenance(
                generator_version="0.2",
                world_manifest_ref="world:1",
                generation_seed=1,
                dynamics_seed=2,
                task_seed=3,
            ),
            terminated=False,
            truncated=False,
            termination_reason=None,
        )

    def snapshot(self) -> EnvironmentSnapshot:
        return self._snapshot

    def restore(self, snapshot: EnvironmentSnapshot, /) -> None:
        self._snapshot = FakeSnapshot(metadata=snapshot.metadata)

    def clone(self) -> EnvironmentCapabilities:
        return EnvironmentCapabilities(interaction=self._interaction, research=self)

    def fork(self, snapshot: EnvironmentSnapshot, /) -> EnvironmentCapabilities:
        self.restore(snapshot)
        return self.clone()

    def transition_records(self) -> tuple[EnvironmentResearchTransitionRecord, ...]:
        return ()


def _protocol_methods(protocol: type[object]) -> set[str]:
    return {
        name
        for name, value in vars(protocol).items()
        if not name.startswith("_") and callable(value)
    }


def test_interaction_descriptor_has_exact_safe_surface_and_revisions() -> None:
    descriptor = _interaction_descriptor()

    assert {field.name for field in fields(type(descriptor))} == {
        "environment_family",
        "environment_semantic_version",
        "interaction_interface_revision",
        "observation_schema_revision",
        "task_schema_revision",
        "feedback_schema_revision",
        "action_capability",
    }
    with pytest.raises(TypeError):
        EnvironmentInteractionDescriptor(
            environment_family="microworld",
            environment_semantic_version="0.2",
            interaction_interface_revision=True,
            observation_schema_revision=0,
            task_schema_revision=0,
            feedback_schema_revision=0,
            action_capability=descriptor.action_capability,
        )


def test_protocol_surfaces_are_exact_and_separate() -> None:
    assert _protocol_methods(EnvironmentInteraction) == INTERACTION_METHODS
    assert _protocol_methods(EnvironmentResearch) == RESEARCH_METHODS
    assert not issubclass(EnvironmentResearch, EnvironmentInteraction)
    assert INTERACTION_METHODS.isdisjoint(RESEARCH_METHODS)


def test_fake_capabilities_satisfy_protocols_independently() -> None:
    interaction = FakeInteraction()
    metadata = EnvironmentSnapshotMetadata(
        environment_snapshot_id=EnvironmentSnapshotId(UUID(int=2)),
        world_instance_id=WorldInstanceId(UUID(int=1)),
        snapshot_contract_revision=0,
        parent_snapshot_id=None,
        environment=_environment_descriptor(),
    )
    snapshot = FakeSnapshot(metadata=metadata)
    research = FakeResearch(interaction, snapshot)
    capabilities = EnvironmentCapabilities(interaction=interaction, research=research)

    assert isinstance(interaction, EnvironmentInteraction)
    assert not isinstance(interaction, EnvironmentResearch)
    assert isinstance(research, EnvironmentResearch)
    assert not isinstance(research, EnvironmentInteraction)
    assert isinstance(snapshot, EnvironmentSnapshot)
    assert capabilities.interaction is interaction
    assert capabilities.research is research
    assert not hasattr(capabilities.interaction, "snapshot")

    with pytest.raises(SchemaError):
        ValueContract(EnvironmentCapabilities).validate(capabilities)


def test_agent_visible_records_have_no_research_leakage() -> None:
    agent_visible_types = (
        ActionCapabilityDescriptor,
        AgentVisibleActionOutcome,
        AgentVisibleField,
        AgentVisibleRecord,
        CommittedEnvironmentAction,
        EnvironmentInteractionDescriptor,
        EnvironmentTransitionReceipt,
        EnvironmentTransitionRef,
        RawObservation,
        EpisodeStartResult,
        ExternalTaskFeedback,
        ExternalTaskSpecification,
        InteractionResult,
    )

    for record_type in agent_visible_types:
        names = {field.name for field in fields(record_type)}
        assert names.isdisjoint(FORBIDDEN_AGENT_FIELDS)
        assert "info" not in names
        assert "metadata" not in names


def test_research_records_carry_only_typed_privileged_references() -> None:
    assert "world_instance_id" in {field.name for field in fields(EnvironmentDescriptor)}
    assert "hidden_state_ref" in {field.name for field in fields(EnvironmentResearchView)}
    assert "environment_snapshot_id" in {
        field.name for field in fields(EnvironmentSnapshotMetadata)
    }
    assert "environment_transition_id" in {
        field.name for field in fields(EnvironmentResearchTransitionRecord)
    }
    assert "metadata" in vars(EnvironmentSnapshot)


def test_snapshot_metadata_is_immutable_and_protocol_has_no_payload_escape_hatch() -> None:
    names = {field.name for field in fields(EnvironmentSnapshotMetadata)}
    metadata = EnvironmentSnapshotMetadata(
        environment_snapshot_id=EnvironmentSnapshotId(UUID(int=3)),
        world_instance_id=WorldInstanceId(UUID(int=1)),
        snapshot_contract_revision=0,
        parent_snapshot_id=None,
        environment=_environment_descriptor(),
    )

    assert names == {
        "environment_snapshot_id",
        "world_instance_id",
        "snapshot_contract_revision",
        "parent_snapshot_id",
        "environment",
    }
    assert "payload" not in vars(EnvironmentSnapshot)
    assert "data" not in vars(EnvironmentSnapshot)
    assert bool(getattr(getattr(type(metadata), "__dataclass_params__", None), "frozen", False))


def _absolute_import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.partition(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module is not None:
            roots.add(node.module.partition(".")[0])
    return roots


def test_environment_contracts_are_stdlib_only_and_respect_package_layers() -> None:
    allowed_roots = {*sys.stdlib_module_names, "__future__", "mindra"}
    forbidden_mindra_roots = {
        "mindra.composition",
        "mindra.entrypoints",
        "mindra.reference",
        "mindra.runtime",
    }
    paths = (CONTRACTS_ROOT / "environment.py", CONTRACTS_ROOT / "interaction.py")

    for path in paths:
        roots = _absolute_import_roots(path)
        assert roots <= allowed_roots
        source = path.read_text(encoding="utf-8")
        assert all(root not in source for root in forbidden_mindra_roots)


def test_no_environment_third_party_runtime_dependency_was_added() -> None:
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)

    assert pyproject["project"]["dependencies"] == []
    sources = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (CONTRACTS_ROOT / "environment.py", CONTRACTS_ROOT / "interaction.py")
    )
    assert "gymnasium" not in sources.lower()
    assert "numpy" not in sources.lower()
