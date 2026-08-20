"""Property checks atomic public/private transaction behavior."""

from dataclasses import replace

import pytest
from hypothesis import given
from hypothesis import strategies as st

from mindra.contracts import (
    Available,
    CommitValidationError,
    ModuleId,
    PrivateStateSnapshot,
    SchemaError,
)
from tests.commit_support import CommitTestContext, make_context, result_for


def _private_value(context: CommitTestContext, module_id: ModuleId) -> object:
    snapshot = context.store.snapshot_for(module_id)
    assert isinstance(snapshot, PrivateStateSnapshot)
    return snapshot.value


def test_public_private_private_only_and_empty_success_paths() -> None:
    context = make_context()
    alpha = ModuleId("commit.alpha")

    combined = context.coordinator.commit(
        current_state=context.state,
        results=(result_for(context, "alpha", public_value=8, private_value=18),),
        logical_time=context.logical_time,
    )
    assert combined.state.read(context.keys["alpha"]).availability == Available(8)
    assert _private_value(context, alpha) == 18
    assert combined.record.private_revisions[0].before.value == 0
    assert combined.record.private_revisions[0].after.value == 1

    private_only = context.coordinator.commit(
        current_state=combined.state,
        results=(
            result_for(
                context,
                "alpha",
                private_value=19,
                base_revision=combined.state.envelope.state_revision,
                private_revision=combined.record.private_revisions[0].after,
            ),
        ),
        logical_time=context.logical_time,
    )
    assert private_only.state is combined.state
    assert private_only.record.resulting_state_revision == combined.state.envelope.state_revision
    assert private_only.record.commit_id != combined.record.commit_id

    empty = context.coordinator.commit(
        current_state=private_only.state,
        results=(),
        logical_time=context.logical_time,
    )
    assert empty.state is private_only.state
    assert empty.record.module_attempt_ids == ()
    assert empty.record.public_paths == ()
    assert empty.record.private_revisions == ()
    assert empty.record.commit_id not in {
        combined.record.commit_id,
        private_only.record.commit_id,
    }


def test_invalid_private_payload_prevents_valid_public_publication() -> None:
    context = make_context()
    before = context.store.snapshot_for(ModuleId("commit.alpha"))

    with pytest.raises(SchemaError):
        context.coordinator.commit(
            current_state=context.state,
            results=(result_for(context, "alpha", public_value=8, private_value="bad"),),
            logical_time=context.logical_time,
        )

    assert context.store.snapshot_for(ModuleId("commit.alpha")) == before
    assert context.state.read(context.keys["alpha"]).availability == Available(1)


def test_invalid_public_payload_prevents_valid_private_mutation() -> None:
    context = make_context()
    valid = result_for(context, "alpha", public_value=8, private_value=18)
    write = valid.state_update.writes[0]
    invalid_write = replace(write, availability=Available("bad"))
    invalid = replace(
        valid,
        state_update=replace(
            valid.state_update,
            writes=(invalid_write,),
        ),
    )
    before = context.store.snapshot_for(ModuleId("commit.alpha"))

    with pytest.raises(SchemaError):
        context.coordinator.commit(
            current_state=context.state,
            results=(invalid,),
            logical_time=context.logical_time,
        )

    assert context.store.snapshot_for(ModuleId("commit.alpha")) == before


@given(st.permutations(("alpha", "beta", "gamma")))
def test_commit_record_and_semantic_state_are_permutation_independent(
    order: list[str],
) -> None:
    first = make_context()
    second = make_context()
    first_results = tuple(
        result_for(
            first,
            name,
            public_value={"alpha": 7, "beta": 8, "gamma": 9}[name],
            private_value={"alpha": 17, "beta": 18, "gamma": None}[name],
        )
        for name in order
    )
    second_results = tuple(
        result_for(
            second,
            name,
            public_value={"alpha": 7, "beta": 8, "gamma": 9}[name],
            private_value={"alpha": 17, "beta": 18, "gamma": None}[name],
        )
        for name in reversed(order)
    )

    first_commit = first.coordinator.commit(
        current_state=first.state,
        results=first_results,
        logical_time=first.logical_time,
    )
    second_commit = second.coordinator.commit(
        current_state=second.state,
        results=second_results,
        logical_time=second.logical_time,
    )

    assert first_commit.state == second_commit.state
    assert first_commit.record == second_commit.record
    assert tuple(path.dotted for path in first_commit.record.public_paths) == (
        "commit.alpha.value",
        "commit.beta.value",
        "commit.gamma.value",
    )
    assert tuple(
        transition.module_id.value for transition in first_commit.record.private_revisions
    ) == ("commit.alpha", "commit.beta")


def test_duplicate_path_producer_and_attempt_are_rejected() -> None:
    context = make_context()
    alpha = result_for(context, "alpha", public_value=7)
    beta = result_for(context, "beta", public_value=8)
    beta_write = replace(beta.state_update.writes[0], key=context.keys["alpha"])
    duplicate_path = replace(
        beta,
        state_update=replace(
            beta.state_update,
            producer=ModuleId("commit.alpha"),
            writes=(beta_write,),
        ),
    )
    with pytest.raises(CommitValidationError):
        context.coordinator.commit(
            current_state=context.state,
            results=(alpha, duplicate_path),
            logical_time=context.logical_time,
        )

    duplicate_attempt = result_for(
        context,
        "beta",
        public_value=8,
        module_attempt_id=alpha.state_update.module_attempt_id,
    )
    with pytest.raises(CommitValidationError, match="ModuleAttemptId"):
        context.coordinator.commit(
            current_state=context.state,
            results=(alpha, duplicate_attempt),
            logical_time=context.logical_time,
        )


def test_equal_public_payload_still_creates_new_revision() -> None:
    context = make_context()
    committed = context.coordinator.commit(
        current_state=context.state,
        results=(result_for(context, "alpha", public_value=1),),
        logical_time=context.logical_time,
    )

    assert committed.state.envelope.state_revision.value == 1
    assert committed.state.read(context.keys["alpha"]).availability == Available(1)
