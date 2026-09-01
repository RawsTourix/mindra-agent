"""Проверки opaque causal identities interaction foundation."""

from uuid import UUID

from mindra.contracts import (
    ActionCommitId,
    ActionIntentId,
    AuthorizedActionId,
    DispatchAttemptId,
    DispatchId,
    EnvironmentSnapshotId,
    EnvironmentTransitionId,
    ExperienceEventId,
    ExternalTaskId,
    GoalId,
    GoalProposalId,
    JournalId,
    ObservationId,
    OutcomeId,
    PerceptId,
    WorldInstanceId,
)
from mindra.contracts.identity import IdentityType
from mindra.runtime import DeterministicIdFactory

INTERACTION_IDENTITIES: tuple[IdentityType[UUID], ...] = (
    ObservationId,
    PerceptId,
    ExternalTaskId,
    GoalProposalId,
    GoalId,
    ActionIntentId,
    AuthorizedActionId,
    ActionCommitId,
    DispatchId,
    DispatchAttemptId,
    EnvironmentTransitionId,
    OutcomeId,
    ExperienceEventId,
    JournalId,
    EnvironmentSnapshotId,
    WorldInstanceId,
)


def test_interaction_identity_types_are_distinct_and_factory_compatible() -> None:
    factory = DeterministicIdFactory(UUID(int=1), "interaction")

    generated = tuple(factory.new_id(identity_type) for identity_type in INTERACTION_IDENTITIES)

    assert len(set(INTERACTION_IDENTITIES)) == len(INTERACTION_IDENTITIES)
    assert len(set(generated)) == len(generated)
    assert all(isinstance(identity, UUID) for identity in generated)


def test_interaction_identity_generation_is_deterministic_and_type_separated() -> None:
    first = DeterministicIdFactory(UUID(int=2), "interaction")
    second = DeterministicIdFactory(UUID(int=2), "interaction")

    assert first.new_id(ObservationId) == second.new_id(ObservationId)
    assert first.new_id(OutcomeId) == second.new_id(OutcomeId)
    assert DeterministicIdFactory(UUID(int=2), "interaction").new_id(
        ObservationId
    ) != DeterministicIdFactory(UUID(int=2), "interaction").new_id(OutcomeId)
