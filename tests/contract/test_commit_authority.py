"""Contract checks write authority, provenance и public commit records."""

from dataclasses import FrozenInstanceError, replace
from uuid import UUID

import pytest

from mindra.contracts import (
    Available,
    CommitValidationError,
    ImplementationId,
    MissingFieldError,
    ModuleComputeResult,
    ModuleId,
    PrivateStateSnapshot,
    RunId,
    RuntimeBoundaryId,
    StateKey,
    StatePath,
    UnauthorizedWriteError,
)
from mindra.runtime import CommitRecord, CommitResult, PrivateStateRevisionTransition
from tests.commit_support import attempt_id, descriptor_for, make_context, result_for


def test_public_only_commit_enforces_owner_and_builds_next_snapshot() -> None:
    context = make_context()

    result = context.coordinator.commit(
        current_state=context.state,
        results=(result_for(context, "alpha", public_value=9),),
        logical_time=context.logical_time,
    )

    assert result.state is not context.state
    assert result.state.envelope.state_revision.value == 1
    assert result.state.envelope.parent_state_revision == result.record.base_state_revision
    assert result.state.read(context.keys["alpha"]).availability == Available(9)
    assert result.record.public_paths == (context.keys["alpha"].path,)
    private_snapshot = context.store.snapshot_for(ModuleId("commit.alpha"))
    assert isinstance(private_snapshot, PrivateStateSnapshot)
    assert private_snapshot.revision.value == 0


def test_unknown_owner_and_undeclared_paths_fail_closed() -> None:
    context = make_context()
    valid = result_for(context, "alpha", public_value=9)
    write = valid.state_update.writes[0]

    missing_write = replace(
        write,
        key=StateKey[int](StatePath.from_dotted("commit.missing.value")),
    )
    missing = replace(
        valid,
        state_update=replace(valid.state_update, writes=(missing_write,)),
    )
    with pytest.raises(MissingFieldError):
        context.coordinator.commit(
            current_state=context.state,
            results=(missing,),
            logical_time=context.logical_time,
        )

    beta_key = context.keys["beta"]
    owner_write = replace(write, key=beta_key)
    wrong_owner = replace(
        valid,
        state_update=replace(valid.state_update, writes=(owner_write,)),
    )
    with pytest.raises(UnauthorizedWriteError, match="owner"):
        context.coordinator.commit(
            current_state=context.state,
            results=(wrong_owner,),
            logical_time=context.logical_time,
        )

    alpha = descriptor_for(context, "alpha")
    object.__setattr__(alpha, "writes", ())
    with pytest.raises(UnauthorizedWriteError, match=r"descriptor\.writes"):
        context.coordinator.commit(
            current_state=context.state,
            results=(valid,),
            logical_time=context.logical_time,
        )


@pytest.mark.parametrize(
    "field",
    ["producer", "implementation_id", "base_state_revision", "module_attempt_id", "logical_time"],
)
def test_provenance_mismatch_is_rejected(field: str) -> None:
    context = make_context()
    valid = result_for(context, "alpha", public_value=9)
    write = valid.state_update.writes[0]
    if field == "producer":
        invalid_provenance = replace(write.provenance, producer=ModuleId("commit.beta"))
    elif field == "implementation_id":
        invalid_provenance = replace(
            write.provenance,
            implementation_id=ImplementationId("test.wrong.v1"),
        )
    elif field == "base_state_revision":
        invalid_provenance = replace(
            write.provenance,
            base_state_revision=write.provenance.base_state_revision.next(),
        )
    elif field == "module_attempt_id":
        invalid_provenance = replace(
            write.provenance,
            module_attempt_id=attempt_id("beta"),
        )
    else:
        invalid_provenance = replace(
            write.provenance,
            logical_time=replace(context.logical_time, run_id=RunId(UUID(int=88))),
        )
    invalid_write = replace(write, provenance=invalid_provenance)
    invalid = replace(
        valid,
        state_update=replace(
            valid.state_update,
            writes=(invalid_write,),
        ),
    )

    with pytest.raises((CommitValidationError, TypeError)):
        context.coordinator.commit(
            current_state=context.state,
            results=(invalid,),
            logical_time=context.logical_time,
        )


def test_runtime_boundary_cannot_masquerade_as_module_producer() -> None:
    context = make_context()
    valid = result_for(context, "alpha", public_value=9)
    write = valid.state_update.writes[0]
    invalid_write = replace(
        write,
        provenance=replace(
            write.provenance,
            producer=RuntimeBoundaryId("runtime.masquerade"),
        ),
    )
    invalid = ModuleComputeResult(
        state_update=replace(
            valid.state_update,
            writes=(invalid_write,),
        ),
        private_state_update=None,
    )

    with pytest.raises(CommitValidationError, match="producer"):
        context.coordinator.commit(
            current_state=context.state,
            results=(invalid,),
            logical_time=context.logical_time,
        )


def test_commit_value_objects_are_frozen_and_private_store_is_not_exposed() -> None:
    context = make_context()
    result = context.coordinator.commit(
        current_state=context.state,
        results=(),
        logical_time=context.logical_time,
    )

    assert isinstance(result, CommitResult)
    assert isinstance(result.record, CommitRecord)
    assert not hasattr(result, "private_store")
    with pytest.raises(FrozenInstanceError):
        result_attribute = "record"
        setattr(result, result_attribute, result.record)
    with pytest.raises(FrozenInstanceError):
        record_attribute = "public_paths"
        setattr(result.record, record_attribute, ())
    alpha_snapshot = context.store.snapshot_for(ModuleId("commit.alpha"))
    assert isinstance(alpha_snapshot, PrivateStateSnapshot)
    with pytest.raises(CommitValidationError):
        PrivateStateRevisionTransition(
            module_id=ModuleId("commit.alpha"),
            before=alpha_snapshot.revision,
            after=alpha_snapshot.revision,
        )
