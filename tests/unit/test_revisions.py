"""Проверки раздельных immutable revision value objects."""

from dataclasses import FrozenInstanceError
from typing import cast

import pytest

from mindra.contracts import (
    CompositionRevision,
    ExecutionPlanRevision,
    PrivateStateRevision,
    SchemaRevision,
    StateRevision,
)

REVISION_TYPES = (
    SchemaRevision,
    StateRevision,
    PrivateStateRevision,
    ExecutionPlanRevision,
    CompositionRevision,
)


@pytest.mark.parametrize("revision_type", REVISION_TYPES)
def test_revision_initial_and_next_preserve_type(
    revision_type: type[
        SchemaRevision
        | StateRevision
        | PrivateStateRevision
        | ExecutionPlanRevision
        | CompositionRevision
    ],
) -> None:
    initial = revision_type.initial()
    following = initial.next()

    assert type(initial) is revision_type
    assert initial.value == 0
    assert type(following) is revision_type
    assert following.value == 1


def test_revision_comparison_is_available_within_each_type() -> None:
    assert SchemaRevision(1) < SchemaRevision(2)
    assert StateRevision(1) < StateRevision(2)
    assert PrivateStateRevision(1) < PrivateStateRevision(2)
    assert ExecutionPlanRevision(1) < ExecutionPlanRevision(2)
    assert CompositionRevision(1) < CompositionRevision(2)


@pytest.mark.parametrize("revision_type", REVISION_TYPES)
def test_revision_rejects_negative_value(
    revision_type: type[
        SchemaRevision
        | StateRevision
        | PrivateStateRevision
        | ExecutionPlanRevision
        | CompositionRevision
    ],
) -> None:
    with pytest.raises(ValueError):
        revision_type(-1)


@pytest.mark.parametrize("value", [cast(int, True), cast(int, 1.5)])
def test_revision_rejects_non_integer_value(value: int) -> None:
    with pytest.raises(TypeError):
        StateRevision(value)


def test_revision_is_frozen() -> None:
    revision = StateRevision.initial()
    value_attribute = "value"

    with pytest.raises(FrozenInstanceError):
        setattr(revision, value_attribute, 2)


def test_different_revision_types_are_not_interchangeable() -> None:
    state_revision = StateRevision.initial()
    schema_revision = SchemaRevision.initial()

    assert state_revision != cast(StateRevision, schema_revision)
    with pytest.raises(TypeError):
        _ = state_revision < cast(StateRevision, schema_revision)
