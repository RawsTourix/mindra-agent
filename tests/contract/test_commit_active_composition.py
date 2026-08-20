"""Regression checks active descriptor/private-store composition boundary."""

from collections.abc import Callable
from dataclasses import replace
from typing import cast

import pytest

import mindra.runtime as runtime
from mindra.contracts import (
    CompositionError,
    DeterminismMode,
    ExecutionTraits,
    ImplementationId,
    ImplementationRevision,
    ModuleDescriptor,
    ModuleId,
    ModuleStatefulness,
    PrivateStateContract,
    PrivateStateDescriptor,
    PrivateStateSnapshot,
    ValueContract,
)
from mindra.runtime import CommitCoordinator, PrivateStateStore
from tests.commit_support import descriptor_for, make_context, result_for


def _initial_values(
    descriptors: tuple[ModuleDescriptor, ...],
    *,
    alpha_value: object = 10,
) -> dict[ModuleId, object]:
    values: dict[ModuleId, object] = {}
    for descriptor in descriptors:
        if descriptor.traits.statefulness is ModuleStatefulness.STATEFUL:
            values[descriptor.module_id] = (
                alpha_value if descriptor.module_id == ModuleId("commit.alpha") else 20
            )
    return values


def _construct_with_store_descriptors(
    store_descriptors: tuple[ModuleDescriptor, ...],
    *,
    alpha_value: object = 10,
) -> None:
    context = make_context()
    store = PrivateStateStore(
        store_descriptors,
        _initial_values(store_descriptors, alpha_value=alpha_value),
    )
    CommitCoordinator(
        schema=context.schema,
        descriptors=context.descriptors,
        private_store=store,
        id_factory=context.factory,
    )


def _replace_descriptor(
    descriptors: tuple[ModuleDescriptor, ...],
    replacement: ModuleDescriptor,
) -> tuple[ModuleDescriptor, ...]:
    return tuple(
        replacement if descriptor.module_id == replacement.module_id else descriptor
        for descriptor in descriptors
    )


def test_exactly_matching_descriptors_construct_coordinator() -> None:
    context = make_context()

    coordinator = CommitCoordinator(
        schema=context.schema,
        descriptors=context.descriptors,
        private_store=context.store,
        id_factory=context.factory,
    )

    assert isinstance(coordinator, CommitCoordinator)
    assert context.factory.counter == 0


@pytest.mark.parametrize(
    "replacement",
    [
        lambda descriptor: replace(
            descriptor,
            implementation_id=ImplementationId("test.commit.alpha.incompatible"),
        ),
        lambda descriptor: replace(
            descriptor,
            implementation_revision=ImplementationRevision("incompatible"),
        ),
    ],
    ids=("implementation-id", "implementation-revision"),
)
def test_implementation_identity_or_revision_mismatch_is_rejected(
    replacement: Callable[[ModuleDescriptor], ModuleDescriptor],
) -> None:
    context = make_context()
    alpha = descriptor_for(context, "alpha")
    mismatched = _replace_descriptor(context.descriptors, replacement(alpha))

    with pytest.raises(CompositionError, match="descriptor"):
        _construct_with_store_descriptors(mismatched)


def test_statefulness_mismatch_is_rejected() -> None:
    context = make_context()
    alpha = descriptor_for(context, "alpha")
    stateless_alpha = replace(
        alpha,
        private_state=None,
        traits=ExecutionTraits(
            statefulness=ModuleStatefulness.STATELESS,
            determinism=DeterminismMode.DETERMINISTIC,
        ),
    )
    mismatched = _replace_descriptor(context.descriptors, stateless_alpha)

    with pytest.raises(CompositionError, match="descriptor"):
        _construct_with_store_descriptors(mismatched)


class _IdentityContract:
    """Custom contract с identity-only equality по умолчанию."""

    def validate(self, value: object) -> None:
        ValueContract(int).validate(value)

    def freeze(self, value: object) -> int:
        self.validate(value)
        return cast(int, value)


def test_different_private_contract_instance_is_rejected_fail_closed() -> None:
    context = make_context()
    alpha = descriptor_for(context, "alpha")
    active_contract = _IdentityContract()
    active_alpha = replace(
        alpha,
        private_state=cast(
            PrivateStateDescriptor[object],
            PrivateStateDescriptor(cast(PrivateStateContract[object], active_contract)),
        ),
    )
    active_descriptors = _replace_descriptor(context.descriptors, active_alpha)
    store_alpha = replace(
        active_alpha,
        private_state=cast(
            PrivateStateDescriptor[object],
            PrivateStateDescriptor(cast(PrivateStateContract[object], _IdentityContract())),
        ),
    )
    store_descriptors = _replace_descriptor(active_descriptors, store_alpha)
    store = PrivateStateStore(store_descriptors, _initial_values(store_descriptors))

    with pytest.raises(CompositionError, match="descriptor"):
        CommitCoordinator(
            schema=context.schema,
            descriptors=active_descriptors,
            private_store=store,
            id_factory=context.factory,
        )


def test_store_missing_active_module_is_rejected() -> None:
    context = make_context()
    store_descriptors = tuple(
        descriptor
        for descriptor in context.descriptors
        if descriptor.module_id != ModuleId("commit.gamma")
    )

    with pytest.raises(CompositionError, match=r"missing=.*commit.gamma"):
        _construct_with_store_descriptors(store_descriptors)


def test_store_extra_module_is_rejected() -> None:
    context = make_context()
    gamma = descriptor_for(context, "gamma")
    extra = replace(
        gamma,
        module_id=ModuleId("commit.extra"),
        implementation_id=ImplementationId("test.commit.extra.v1"),
    )
    store_descriptors = (*context.descriptors, extra)

    with pytest.raises(CompositionError, match=r"extra=.*commit.extra"):
        _construct_with_store_descriptors(store_descriptors)


def test_failed_construction_preserves_private_snapshots_and_id_counter() -> None:
    context = make_context()
    before = {
        module_id: context.store.snapshot_for(module_id)
        for module_id in (ModuleId("commit.alpha"), ModuleId("commit.beta"))
    }
    alpha = descriptor_for(context, "alpha")
    incompatible = _replace_descriptor(
        context.descriptors,
        replace(alpha, implementation_revision=ImplementationRevision("incompatible")),
    )

    with pytest.raises(CompositionError):
        CommitCoordinator(
            schema=context.schema,
            descriptors=incompatible,
            private_store=context.store,
            id_factory=context.factory,
        )

    assert context.factory.counter == 0
    assert {module_id: context.store.snapshot_for(module_id) for module_id in before} == before


def test_public_private_commit_paths_remain_available_after_compatibility_check() -> None:
    context = make_context()

    public_only = context.coordinator.commit(
        current_state=context.state,
        results=(result_for(context, "gamma", public_value=30),),
        logical_time=context.logical_time,
    )
    private_only = context.coordinator.commit(
        current_state=public_only.state,
        results=(
            result_for(
                context,
                "alpha",
                private_value=40,
                base_revision=public_only.state.envelope.state_revision,
            ),
        ),
        logical_time=context.logical_time,
    )
    combined = context.coordinator.commit(
        current_state=private_only.state,
        results=(
            result_for(
                context,
                "beta",
                public_value=50,
                private_value=60,
                base_revision=private_only.state.envelope.state_revision,
            ),
        ),
        logical_time=context.logical_time,
    )

    alpha = context.store.snapshot_for(ModuleId("commit.alpha"))
    beta = context.store.snapshot_for(ModuleId("commit.beta"))
    assert isinstance(alpha, PrivateStateSnapshot)
    assert isinstance(beta, PrivateStateSnapshot)
    assert alpha.value == 40
    assert beta.value == 60
    assert combined.state.envelope.state_revision.value == 2


def test_compatibility_helper_is_not_exported_from_runtime_facade() -> None:
    assert "_assert_compatible_descriptors" not in runtime.__all__
    assert not hasattr(runtime, "_assert_compatible_descriptors")
