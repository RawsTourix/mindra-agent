"""Property checks stale public/private and temporal fail-closed behavior."""

from collections.abc import Callable
from dataclasses import replace
from uuid import UUID

import pytest
from hypothesis import given
from hypothesis import strategies as st

from mindra.contracts import (
    AgentSessionId,
    Available,
    CommitValidationError,
    LogicalTime,
    ModuleId,
    PrivateStateProposal,
    PrivateStateRevision,
    RunId,
    StaleProposalError,
    StateRevision,
)
from tests.commit_support import make_context, result_for


@given(st.integers(min_value=1, max_value=1000))
def test_stale_public_proposal_never_consumes_id_or_mutates_state(stale: int) -> None:
    context = make_context()
    before_private = context.store.snapshot_for(ModuleId("commit.alpha"))

    with pytest.raises(StaleProposalError):
        context.coordinator.commit(
            current_state=context.state,
            results=(
                result_for(
                    context,
                    "alpha",
                    public_value=9,
                    private_value=19,
                    base_revision=StateRevision(stale),
                ),
            ),
            logical_time=context.logical_time,
        )

    assert context.factory.counter == 0
    assert context.store.snapshot_for(ModuleId("commit.alpha")) == before_private
    assert context.state.read(context.keys["alpha"]).availability == Available(1)


def test_stale_private_proposal_prevents_valid_public_publication() -> None:
    context = make_context()
    before = context.store.snapshot_for(ModuleId("commit.alpha"))

    with pytest.raises(StaleProposalError):
        context.coordinator.commit(
            current_state=context.state,
            results=(
                result_for(
                    context,
                    "alpha",
                    public_value=9,
                    private_value=19,
                    private_revision=PrivateStateRevision(7),
                ),
            ),
            logical_time=context.logical_time,
        )

    assert context.factory.counter == 0
    assert context.store.snapshot_for(ModuleId("commit.alpha")) == before


def test_private_module_and_attempt_mismatch_are_rejected_before_prepare() -> None:
    context = make_context()
    valid = result_for(context, "alpha", private_value=19)
    private = valid.private_state_update
    assert private is not None

    wrong_module = replace(private, module_id=ModuleId("commit.beta"))
    with pytest.raises(CommitValidationError, match="module_id"):
        context.coordinator.commit(
            current_state=context.state,
            results=(replace(valid, private_state_update=wrong_module),),
            logical_time=context.logical_time,
        )

    wrong_attempt = PrivateStateProposal(
        module_id=private.module_id,
        base_revision=private.base_revision,
        module_attempt_id=result_for(context, "beta").state_update.module_attempt_id,
        value=private.value,
    )
    with pytest.raises(CommitValidationError, match="ModuleAttemptId"):
        context.coordinator.commit(
            current_state=context.state,
            results=(replace(valid, private_state_update=wrong_attempt),),
            logical_time=context.logical_time,
        )


@pytest.mark.parametrize(
    "logical_time",
    [
        lambda time: replace(time, run_id=RunId(UUID(int=99))),
        lambda time: replace(time, agent_session_id=AgentSessionId(UUID(int=99))),
    ],
)
def test_incompatible_root_temporal_context_is_rejected(
    logical_time: Callable[[LogicalTime], LogicalTime],
) -> None:
    context = make_context()
    invalid_time = logical_time(context.logical_time)

    with pytest.raises(CommitValidationError):
        context.coordinator.commit(
            current_state=context.state,
            results=(),
            logical_time=invalid_time,
        )

    assert context.factory.counter == 0


def test_success_after_failed_validation_gets_first_deterministic_id() -> None:
    failed_then_success = make_context()
    clean_success = make_context()
    with pytest.raises(StaleProposalError):
        failed_then_success.coordinator.commit(
            current_state=failed_then_success.state,
            results=(
                result_for(
                    failed_then_success,
                    "alpha",
                    base_revision=StateRevision(1),
                ),
            ),
            logical_time=failed_then_success.logical_time,
        )

    after_failure = failed_then_success.coordinator.commit(
        current_state=failed_then_success.state,
        results=(),
        logical_time=failed_then_success.logical_time,
    )
    clean = clean_success.coordinator.commit(
        current_state=clean_success.state,
        results=(),
        logical_time=clean_success.logical_time,
    )

    assert after_failure.record.commit_id == clean.record.commit_id
