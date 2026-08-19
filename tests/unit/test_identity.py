"""Проверки causal и semantic identity foundation."""

from dataclasses import FrozenInstanceError
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    AgentSessionId,
    CommitId,
    IdFactory,
    ImplementationId,
    ModuleId,
    ProfileId,
    RunId,
    StateNamespace,
)
from mindra.runtime import DeterministicIdFactory, Uuid7IdFactory


@pytest.mark.parametrize(
    ("identity_type", "value"),
    [
        (ModuleId, "synthetic.source"),
        (ImplementationId, "reference.synthetic_source.v1"),
        (ProfileId, "reference_v1"),
        (StateNamespace, "cognitive.synthetic_state"),
    ],
)
def test_semantic_identity_accepts_canonical_value(
    identity_type: type[ModuleId | ImplementationId | ProfileId | StateNamespace],
    value: str,
) -> None:
    identity = identity_type(value)

    assert identity.value == value
    assert str(identity) == value


@pytest.mark.parametrize(
    "value",
    [
        "",
        "Synthetic.source",
        "synthetic-source",
        "synthetic..source",
        ".synthetic",
        "synthetic.",
        "synthetic source",
        "1synthetic.source",
    ],
)
def test_semantic_identity_rejects_noncanonical_value(value: str) -> None:
    with pytest.raises(ValueError):
        ModuleId(value)


def test_semantic_identity_is_frozen_and_type_distinct() -> None:
    module_id = ModuleId("synthetic.source")
    value_attribute = "value"

    with pytest.raises(FrozenInstanceError):
        setattr(module_id, value_attribute, "synthetic.other")

    assert module_id != cast(ModuleId, ImplementationId("synthetic.source"))


def test_uuid7_factory_satisfies_contract_and_creates_uuid7() -> None:
    factory: IdFactory = Uuid7IdFactory()

    run_id = factory.new_id(RunId)
    session_id = factory.new_id(AgentSessionId)

    assert isinstance(run_id, UUID)
    assert run_id.version == 7
    assert session_id.version == 7
    assert run_id != cast(UUID, session_id)


def test_deterministic_factory_repeats_typed_sequence() -> None:
    namespace = UUID("9f14c4d3-baf5-43f0-861f-f85183d05359")
    first = DeterministicIdFactory(namespace, seed="reference", counter=4)
    second = DeterministicIdFactory(namespace, seed="reference", counter=4)

    first_sequence = (
        first.new_id(RunId),
        first.new_id(AgentSessionId),
        first.new_id(CommitId),
    )
    second_sequence = (
        second.new_id(RunId),
        second.new_id(AgentSessionId),
        second.new_id(CommitId),
    )

    assert first_sequence == second_sequence
    assert first.counter == second.counter == 7
    assert len(set(first_sequence)) == len(first_sequence)


def test_deterministic_factory_identity_type_is_part_of_sequence() -> None:
    namespace = UUID("9f14c4d3-baf5-43f0-861f-f85183d05359")

    run_id = DeterministicIdFactory(namespace, "reference").new_id(RunId)
    commit_id = DeterministicIdFactory(namespace, "reference").new_id(CommitId)

    assert cast(UUID, run_id) != cast(UUID, commit_id)


@pytest.mark.parametrize("counter", [-1, cast(int, True), cast(int, 1.5)])
def test_deterministic_factory_rejects_invalid_counter(counter: int) -> None:
    with pytest.raises((TypeError, ValueError)):
        DeterministicIdFactory(UUID(int=0), "reference", counter)
