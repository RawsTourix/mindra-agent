"""Property-level evidence same-base public/private wave pinning."""

import pytest

from mindra.contracts import (
    AvailabilityError,
    Available,
    PrivateStateSnapshot,
    Unavailable,
    UndeclaredReadError,
)
from mindra.runtime import build_state_projection
from tests.scheduler_support import make_scheduler_context, module_for


def test_same_wave_attempts_share_exact_public_base_and_cannot_read_siblings() -> None:
    context = make_scheduler_context()
    context.scheduler.run_cycle(current_state=context.state, cycle_time=context.cycle_time)

    beta = module_for(context, "beta").requests[0]
    gamma = module_for(context, "gamma").requests[0]
    assert beta.context.base_state_revision == gamma.context.base_state_revision
    assert beta.state.read(context.keys["alpha"]).availability == Available(2)
    assert gamma.state.read(context.keys["alpha"]).availability == Available(2)
    with pytest.raises(UndeclaredReadError, match="Read не объявлен"):
        beta.state.read(context.keys["gamma"])


def test_previous_cycle_value_is_not_current_but_earlier_wave_commit_is_current() -> None:
    context = make_scheduler_context()
    beta = module_for(context, "beta")

    with pytest.raises(AvailabilityError, match="текущем cognitive cycle"):
        projection = build_state_projection(
            base_state=context.state,
            read_specs=beta.descriptor.reads,
            logical_time=context.cycle_time,
        )
        projection.read(context.keys["alpha"])

    context.scheduler.run_cycle(current_state=context.state, cycle_time=context.cycle_time)
    assert beta.requests[0].state.read(context.keys["alpha"]).availability == Available(2)


def test_stateful_receives_own_snapshot_and_stateless_receives_unavailable() -> None:
    context = make_scheduler_context()
    context.scheduler.run_cycle(current_state=context.state, cycle_time=context.cycle_time)

    alpha_private = module_for(context, "alpha").requests[0].private_state
    beta_private = module_for(context, "beta").requests[0].private_state
    assert isinstance(alpha_private, PrivateStateSnapshot)
    assert alpha_private.value == 10
    assert isinstance(beta_private, Unavailable)
