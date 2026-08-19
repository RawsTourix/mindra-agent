"""Проверки explicit availability и freshness semantics."""

from dataclasses import FrozenInstanceError, fields
from typing import cast
from uuid import UUID

import pytest

import mindra.contracts.availability as availability_module
from mindra.contracts import (
    AgentSessionId,
    Available,
    FreshnessMetadata,
    LogicalTime,
    RunId,
    Stale,
    StateRevision,
    Unavailable,
    Unknown,
)


def _logical_time() -> LogicalTime:
    return LogicalTime(
        run_id=RunId(UUID(int=1)),
        agent_session_id=AgentSessionId(UUID(int=2)),
    )


def test_available_contains_current_value() -> None:
    assert Available(value=7).value == 7


def test_unknown_and_unavailable_are_distinct_payload_free_variants() -> None:
    unknown = Unknown()
    unavailable = Unavailable()

    assert cast(object, unknown) != unavailable
    assert fields(Unknown) == ()
    assert fields(Unavailable) == ()
    assert not hasattr(unknown, "value")
    assert not hasattr(unavailable, "value")


def test_structural_missing_is_not_an_availability_variant() -> None:
    assert not hasattr(availability_module, "Missing")
    assert Unknown() is not None


def test_stale_preserves_last_known_value_and_freshness() -> None:
    freshness = FreshnessMetadata(
        produced_at=_logical_time(),
        based_on_state_revision=StateRevision(3),
    )
    stale = Stale(value=11, freshness=freshness)

    assert stale.value == 11
    assert stale.freshness is freshness
    assert stale.freshness.based_on_state_revision == StateRevision(3)


@pytest.mark.parametrize(
    "value_object",
    [
        Available(value=7),
        Unknown(),
        Unavailable(),
        FreshnessMetadata(_logical_time(), StateRevision.initial()),
        Stale(
            value=7,
            freshness=FreshnessMetadata(_logical_time(), StateRevision.initial()),
        ),
    ],
)
def test_availability_value_objects_are_frozen(value_object: object) -> None:
    attribute = "unexpected"

    with pytest.raises((AttributeError, FrozenInstanceError, TypeError)):
        setattr(value_object, attribute, "mutation")
