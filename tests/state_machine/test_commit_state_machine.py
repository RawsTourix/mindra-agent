"""Commit sequence: success, stale/invalid failures, private update, rollback, success."""

from dataclasses import replace

import pytest

from mindra.contracts import (
    Available,
    CommitValidationError,
    ModuleId,
    PrivateStateSnapshot,
    SchemaError,
    StaleProposalError,
    StateRevision,
)
from tests.commit_support import make_context, result_for


def test_commit_state_machine_sequence() -> None:
    context = make_context()
    alpha_id = ModuleId("commit.alpha")

    first = context.coordinator.commit(
        current_state=context.state,
        results=(result_for(context, "alpha", public_value=2),),
        logical_time=context.logical_time,
    )
    assert first.state.envelope.state_revision == StateRevision(1)

    with pytest.raises(StaleProposalError):
        context.coordinator.commit(
            current_state=first.state,
            results=(result_for(context, "alpha", public_value=3),),
            logical_time=context.logical_time,
        )

    current_result = result_for(
        context,
        "alpha",
        public_value=3,
        base_revision=StateRevision(1),
    )
    invalid_write = replace(
        current_result.state_update.writes[0],
        key=context.keys["beta"],
    )
    with pytest.raises(CommitValidationError):
        context.coordinator.commit(
            current_state=first.state,
            results=(
                replace(
                    current_result,
                    state_update=replace(
                        current_result.state_update,
                        writes=(invalid_write,),
                    ),
                ),
            ),
            logical_time=context.logical_time,
        )

    private_commit = context.coordinator.commit(
        current_state=first.state,
        results=(
            result_for(
                context,
                "alpha",
                private_value=21,
                base_revision=StateRevision(1),
            ),
        ),
        logical_time=context.logical_time,
    )
    assert private_commit.state is first.state
    private_snapshot = context.store.snapshot_for(alpha_id)
    assert isinstance(private_snapshot, PrivateStateSnapshot)
    assert private_snapshot.value == 21

    invalid_private = result_for(
        context,
        "alpha",
        public_value=4,
        private_value="invalid",
        base_revision=StateRevision(1),
        private_revision=private_snapshot.revision,
    )
    with pytest.raises(SchemaError):
        context.coordinator.commit(
            current_state=first.state,
            results=(invalid_private,),
            logical_time=context.logical_time,
        )
    assert context.store.snapshot_for(alpha_id) == private_snapshot
    assert first.state.read(context.keys["alpha"]).availability == Available(2)

    next_success = context.coordinator.commit(
        current_state=first.state,
        results=(
            result_for(
                context,
                "alpha",
                public_value=5,
                private_value=22,
                base_revision=StateRevision(1),
                private_revision=private_snapshot.revision,
            ),
        ),
        logical_time=context.logical_time,
    )
    assert next_success.state.envelope.state_revision == StateRevision(2)
    assert next_success.state.read(context.keys["alpha"]).availability == Available(5)
