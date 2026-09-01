"""Контрактные проверки Environment data/action vocabulary V0.2-IS-03."""

from dataclasses import dataclass, fields
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    ActionCapabilityDescriptor,
    ActionCommitId,
    AgentVisibleActionOutcome,
    AgentVisibleActionOutcomeStatus,
    AgentVisibleField,
    AgentVisibleRecord,
    AgentVisibleValue,
    CommittedEnvironmentAction,
    Direction,
    Drop,
    EnvironmentEpisodeControl,
    EnvironmentResearchTransitionRecord,
    EnvironmentSnapshotId,
    EnvironmentTransitionId,
    EnvironmentTransitionReceipt,
    EnvironmentTransitionRef,
    EpisodeId,
    EpisodeStartRequest,
    EpisodeStartResult,
    ExternalTaskFeedback,
    ExternalTaskFeedbackStatus,
    ExternalTaskId,
    ExternalTaskSpecification,
    Interact,
    InteractionResult,
    Move,
    ObservationId,
    Pickup,
    RawObservation,
    ResearchActionOutcomeStatus,
    Wait,
    WorldInstanceId,
)


def _observation(value: int = 1) -> RawObservation:
    return RawObservation(
        observation_id=ObservationId(UUID(int=value)),
        observation_schema_revision=0,
        records=(
            AgentVisibleRecord(
                kind="visible_entity",
                fields=(AgentVisibleField(name="symbol", value="target"),),
            ),
        ),
    )


@dataclass(frozen=True, slots=True)
class LeakyVisibleField(AgentVisibleField):
    hidden_state: str


@dataclass(frozen=True, slots=True)
class Navigate(Move):
    distance: int


def test_exact_direction_and_action_vocabulary_is_frozen() -> None:
    assert tuple(Direction) == (
        Direction.NORTH,
        Direction.EAST,
        Direction.SOUTH,
        Direction.WEST,
    )
    actions = (
        Move(Direction.NORTH),
        Interact(Direction.EAST),
        Pickup(Direction.SOUTH),
        Drop(Direction.WEST),
        Wait(),
    )

    assert tuple(type(action).__name__ for action in actions) == (
        "Move",
        "Interact",
        "Pickup",
        "Drop",
        "Wait",
    )
    assert all(
        bool(getattr(getattr(type(action), "__dataclass_params__", None), "frozen", False))
        for action in actions
    )
    with pytest.raises(TypeError):
        Move(cast(Direction, "north"))


@pytest.mark.parametrize(
    "kinds",
    [
        (),
        ("move", "move"),
        ("move", "drop"),
        ("attack",),
    ],
)
def test_action_capability_rejects_empty_duplicate_noncanonical_or_unknown_kinds(
    kinds: tuple[str, ...],
) -> None:
    with pytest.raises(ValueError):
        ActionCapabilityDescriptor(action_schema_revision=0, supported_action_kinds=kinds)


def test_action_capability_requires_exact_nonnegative_revision() -> None:
    descriptor = ActionCapabilityDescriptor(
        action_schema_revision=2,
        supported_action_kinds=("drop", "interact", "move", "pickup", "wait"),
    )

    assert descriptor.action_schema_revision == 2
    with pytest.raises(TypeError):
        ActionCapabilityDescriptor(
            action_schema_revision=True,
            supported_action_kinds=("wait",),
        )
    with pytest.raises(ValueError):
        ActionCapabilityDescriptor(
            action_schema_revision=-1,
            supported_action_kinds=("wait",),
        )


@pytest.mark.parametrize(
    "value",
    [
        cast(AgentVisibleValue, []),
        cast(AgentVisibleValue, {}),
        cast(AgentVisibleValue, {"x"}),
        cast(AgentVisibleValue, object()),
        float("nan"),
        float("inf"),
        float("-inf"),
        cast(AgentVisibleValue, ("ok", float("nan"))),
    ],
)
def test_agent_visible_field_rejects_mutable_object_and_nonfinite_payload(
    value: AgentVisibleValue,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        AgentVisibleField(name="value", value=value)


def test_agent_visible_records_reject_invalid_labels_and_duplicate_fields() -> None:
    field = AgentVisibleField(name="symbol", value=("target", 1, True, None))

    with pytest.raises(ValueError):
        AgentVisibleField(name="", value="x")
    with pytest.raises(ValueError):
        AgentVisibleRecord(kind="visible entity", fields=(field,))
    with pytest.raises(ValueError):
        AgentVisibleRecord(kind="entity", fields=(field, field))
    with pytest.raises(TypeError):
        AgentVisibleRecord(
            kind="entity",
            fields=(
                cast(
                    AgentVisibleField,
                    LeakyVisibleField(name="symbol", value="target", hidden_state="oracle"),
                ),
            ),
        )


def test_raw_observation_is_immutable_and_has_exact_safe_fields() -> None:
    observation = _observation()

    assert {field.name for field in fields(RawObservation)} == {
        "observation_id",
        "observation_schema_revision",
        "records",
    }
    assert bool(getattr(getattr(type(observation), "__dataclass_params__", None), "frozen", False))


def test_task_specification_and_feedback_preserve_external_task_identity() -> None:
    task_id = ExternalTaskId(UUID(int=2))
    task = ExternalTaskSpecification(
        external_task_id=task_id,
        task_schema_revision=1,
        task_kind="direct_reach",
        parameters=(AgentVisibleField(name="target", value="marker"),),
    )
    feedback = ExternalTaskFeedback(
        external_task_id=task_id,
        feedback_schema_revision=1,
        status=ExternalTaskFeedbackStatus.IN_PROGRESS,
        events=(),
    )

    assert task.external_task_id == feedback.external_task_id == task_id


def test_episode_start_control_is_input_only_and_success_flags_are_false() -> None:
    control = EnvironmentEpisodeControl(
        world_manifest_ref="world:mw0:1",
        generation_seed=1,
        dynamics_seed=2,
        task_seed=3,
        full_observation=True,
    )
    request = EpisodeStartRequest(episode_id=EpisodeId(UUID(int=3)), control=control)
    assert not EpisodeStartResult(
        raw_observation=_observation(),
        external_task=None,
        external_feedback=None,
        terminated=False,
        truncated=False,
    ).terminated

    assert request.control is control
    assert "control" not in {field.name for field in fields(EpisodeStartResult)}
    with pytest.raises(ValueError):
        EpisodeStartResult(
            raw_observation=_observation(),
            external_task=None,
            external_feedback=None,
            terminated=True,
            truncated=False,
        )
    with pytest.raises(ValueError):
        EpisodeStartResult(
            raw_observation=_observation(),
            external_task=None,
            external_feedback=None,
            terminated=False,
            truncated=True,
        )


def test_committed_action_and_transition_receipt_preserve_causal_join() -> None:
    commit_id = ActionCommitId(UUID(int=4))
    transition_id = EnvironmentTransitionId(UUID(int=5))
    committed = CommittedEnvironmentAction(
        action_commit_id=commit_id,
        action=Move(Direction.NORTH),
    )
    receipt = EnvironmentTransitionReceipt(
        action_commit_id=commit_id,
        transition=EnvironmentTransitionRef(environment_transition_id=transition_id),
    )

    assert committed.action_commit_id == receipt.action_commit_id == commit_id
    assert receipt.transition.environment_transition_id == transition_id
    with pytest.raises(TypeError):
        CommittedEnvironmentAction(
            action_commit_id=commit_id,
            action=cast(Move, None),
        )
    with pytest.raises(TypeError):
        CommittedEnvironmentAction(
            action_commit_id=commit_id,
            action=cast(Move, Navigate(direction=Direction.NORTH, distance=2)),
        )


@pytest.mark.parametrize(
    ("terminated", "truncated"),
    [(False, False), (True, False), (False, True), (True, True)],
)
def test_interaction_result_preserves_independent_termination_flags(
    terminated: bool,
    truncated: bool,
) -> None:
    result = InteractionResult(
        receipt=EnvironmentTransitionReceipt(
            action_commit_id=ActionCommitId(UUID(int=6)),
            transition=EnvironmentTransitionRef(
                environment_transition_id=EnvironmentTransitionId(UUID(int=7))
            ),
        ),
        raw_observation=_observation(),
        external_feedback=None,
        action_outcome=AgentVisibleActionOutcome(
            status=AgentVisibleActionOutcomeStatus.NO_EFFECT,
            events=(),
        ),
        terminated=terminated,
        truncated=truncated,
    )

    assert (result.terminated, result.truncated) == (terminated, truncated)


def test_research_transition_keeps_privileged_reason_outside_agent_outcome() -> None:
    record = EnvironmentResearchTransitionRecord(
        environment_transition_id=EnvironmentTransitionId(UUID(int=8)),
        episode_id=EpisodeId(UUID(int=9)),
        world_instance_id=WorldInstanceId(UUID(int=10)),
        action_commit_id=ActionCommitId(UUID(int=11)),
        action=Interact(Direction.EAST),
        pre_snapshot_id=EnvironmentSnapshotId(UUID(int=12)),
        post_snapshot_id=EnvironmentSnapshotId(UUID(int=13)),
        action_status=ResearchActionOutcomeStatus.NO_EFFECT,
        reason="door_locked",
        external_feedback=None,
        terminated=False,
        truncated=False,
        termination_reason=None,
    )
    public = AgentVisibleActionOutcome(
        status=AgentVisibleActionOutcomeStatus.NO_EFFECT,
        events=(),
    )

    assert record.reason == "door_locked"
    assert "reason" not in {field.name for field in fields(type(public))}
