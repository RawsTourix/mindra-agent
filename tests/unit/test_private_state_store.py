"""Проверки initialization, staging и private batch atomicity."""

from dataclasses import FrozenInstanceError, fields
from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    CommitValidationError,
    ConfigurationError,
    DeterminismMode,
    DuplicateIdentityError,
    ExecutionPhase,
    ExecutionTraits,
    ImplementationId,
    ImplementationRevision,
    ModuleAttemptId,
    ModuleDescriptor,
    ModuleId,
    ModuleStatefulness,
    PrivateStateContract,
    PrivateStateDescriptor,
    PrivateStateProposal,
    PrivateStateRevision,
    PrivateStateSnapshot,
    SchemaError,
    StaleProposalError,
    Unavailable,
    ValueContract,
)
from mindra.runtime import PrivateStateSlot, PrivateStateStore
from mindra.runtime.private_state import _PreparedPrivateStateUpdate


def _descriptor(
    name: str,
    *,
    stateful: bool = True,
    contract: PrivateStateContract[object] | None = None,
) -> ModuleDescriptor:
    statefulness = ModuleStatefulness.STATEFUL if stateful else ModuleStatefulness.STATELESS
    selected_contract = (
        contract if contract is not None else cast(PrivateStateContract[object], ValueContract(int))
    )
    private_state = (
        cast(
            PrivateStateDescriptor[object],
            PrivateStateDescriptor(selected_contract),
        )
        if stateful
        else None
    )
    return ModuleDescriptor(
        module_id=ModuleId(name),
        implementation_id=ImplementationId(f"test.{name}.v1"),
        implementation_revision=ImplementationRevision("v1"),
        reads=(),
        writes=(),
        private_state=private_state,
        phases=frozenset({ExecutionPhase.COGNITIVE_CYCLE}),
        traits=ExecutionTraits(
            statefulness=statefulness,
            determinism=DeterminismMode.DETERMINISTIC,
        ),
    )


def _snapshot(
    store: PrivateStateStore, descriptor: ModuleDescriptor
) -> PrivateStateSnapshot[object]:
    snapshot = store.snapshot_for(descriptor.module_id)
    assert isinstance(snapshot, PrivateStateSnapshot)
    return snapshot


def _proposal(
    descriptor: ModuleDescriptor,
    value: object,
    *,
    revision: PrivateStateRevision | None = None,
    attempt: int = 1,
) -> PrivateStateProposal[object]:
    return PrivateStateProposal(
        module_id=descriptor.module_id,
        base_revision=revision if revision is not None else PrivateStateRevision.initial(),
        module_attempt_id=ModuleAttemptId(UUID(int=attempt)),
        value=value,
    )


class _TupleFreezingContract:
    """Test contract, который превращает mutable input в immutable tuple."""

    def __init__(self) -> None:
        self.seen: list[object] = []

    def validate(self, value: object) -> None:
        if not isinstance(value, list) or any(type(item) is not int for item in value):
            raise SchemaError("Ожидался list[int]")

    def freeze(self, value: object) -> tuple[int, ...]:
        self.validate(value)
        frozen = tuple(cast(list[int], value))
        self.seen.append(frozen)
        return frozen


def test_stateful_initialization_creates_independent_revision_zero_slots() -> None:
    first = _descriptor("state.first")
    second = _descriptor("state.second")
    store = PrivateStateStore(
        (first, second),
        {first.module_id: 1, second.module_id: 2},
    )

    first_snapshot = _snapshot(store, first)
    second_snapshot = _snapshot(store, second)

    assert first_snapshot.value == 1
    assert second_snapshot.value == 2
    assert first_snapshot.module_id == first.module_id
    assert second_snapshot.module_id == second.module_id
    assert first_snapshot.revision == PrivateStateRevision.initial()
    assert second_snapshot.revision == PrivateStateRevision.initial()


def test_initial_value_passes_concrete_private_contract_freeze() -> None:
    contract = _TupleFreezingContract()
    descriptor = _descriptor("state.freezing", contract=contract)
    mutable_initial = [1, 2]

    store = PrivateStateStore((descriptor,), {descriptor.module_id: mutable_initial})
    mutable_initial.append(3)

    assert contract.seen == [(1, 2)]
    assert _snapshot(store, descriptor).value == (1, 2)


def test_invalid_or_mutable_initial_value_is_rejected_by_contract() -> None:
    descriptor = _descriptor("state.strict")

    with pytest.raises(SchemaError, match="тип int"):
        PrivateStateStore((descriptor,), {descriptor.module_id: [1]})


def test_stateful_module_requires_explicit_initial_value() -> None:
    descriptor = _descriptor("state.required")

    with pytest.raises(ConfigurationError, match="explicit initial"):
        PrivateStateStore((descriptor,), {})


def test_stateless_module_has_no_slot_and_returns_unavailable() -> None:
    descriptor = _descriptor("state.stateless", stateful=False)
    store = PrivateStateStore((descriptor,), {})

    assert store.snapshot_for(descriptor.module_id) == Unavailable()
    assert not hasattr(store, "slots")


def test_stateless_unknown_and_duplicate_initialization_fail_closed() -> None:
    stateless = _descriptor("state.stateless", stateful=False)
    unknown = ModuleId("state.unknown")

    with pytest.raises(ConfigurationError, match="Stateless"):
        PrivateStateStore((stateless,), {stateless.module_id: 1})
    with pytest.raises(ConfigurationError, match="unknown module"):
        PrivateStateStore((stateless,), {unknown: 1})
    with pytest.raises(DuplicateIdentityError):
        PrivateStateStore((stateless, stateless), {})


def test_construction_and_lookup_reject_invalid_shapes_or_unknown_module() -> None:
    descriptor = _descriptor("state.known")

    with pytest.raises(TypeError, match="tuple"):
        PrivateStateStore(cast(tuple[ModuleDescriptor, ...], [descriptor]), {})
    with pytest.raises(TypeError, match="ModuleDescriptor"):
        PrivateStateStore(cast(tuple[ModuleDescriptor, ...], (object(),)), {})

    store = PrivateStateStore((descriptor,), {descriptor.module_id: 1})
    with pytest.raises(ConfigurationError, match="Unknown active ModuleId"):
        store.snapshot_for(ModuleId("state.unknown"))


def test_slot_is_frozen_value_object_without_commit_behavior() -> None:
    slot = PrivateStateSlot(
        module_id=ModuleId("state.slot"),
        revision=PrivateStateRevision.initial(),
        value=1,
    )

    assert {field.name for field in fields(PrivateStateSlot)} == {
        "module_id",
        "revision",
        "value",
    }
    assert not hasattr(slot, "commit")
    value_attribute = "value"
    with pytest.raises(FrozenInstanceError):
        setattr(slot, value_attribute, 2)


def test_valid_proposal_is_frozen_and_prepared_without_store_mutation() -> None:
    contract = _TupleFreezingContract()
    descriptor = _descriptor("state.prepared", contract=contract)
    store = PrivateStateStore((descriptor,), {descriptor.module_id: [1]})
    before = _snapshot(store, descriptor)

    prepared = store._prepare(_proposal(descriptor, [2]))

    assert store.snapshot_for(descriptor.module_id) == before
    assert prepared.module_id == descriptor.module_id
    assert prepared.expected_revision == PrivateStateRevision.initial()
    assert prepared.next_revision == PrivateStateRevision(1)
    assert prepared.frozen_value == (2,)


def test_stale_unknown_and_stateless_proposals_fail_without_mutation() -> None:
    stateful = _descriptor("state.stateful")
    stateless = _descriptor("state.stateless", stateful=False)
    store = PrivateStateStore((stateful, stateless), {stateful.module_id: 1})
    before = _snapshot(store, stateful)

    with pytest.raises(StaleProposalError):
        store._prepare(_proposal(stateful, 2, revision=PrivateStateRevision(99)))
    with pytest.raises(ConfigurationError, match="Unknown active ModuleId"):
        store._prepare(
            PrivateStateProposal(
                module_id=ModuleId("state.unknown"),
                base_revision=PrivateStateRevision.initial(),
                module_attempt_id=ModuleAttemptId(UUID(int=2)),
                value=2,
            )
        )
    with pytest.raises(ConfigurationError, match="Stateless"):
        store._prepare(_proposal(stateless, 2))

    assert store.snapshot_for(stateful.module_id) == before


def test_valid_prepared_batch_replaces_all_slots_and_stabilizes_old_snapshots() -> None:
    first = _descriptor("state.first")
    second = _descriptor("state.second")
    store = PrivateStateStore(
        (first, second),
        {first.module_id: 1, second.module_id: 2},
    )
    old_first = _snapshot(store, first)
    old_second = _snapshot(store, second)
    updates = (
        store._prepare(_proposal(first, 10, attempt=1)),
        store._prepare(_proposal(second, 20, attempt=2)),
    )

    store._apply_prepared(updates)

    assert _snapshot(store, first).value == 10
    assert _snapshot(store, second).value == 20
    assert _snapshot(store, first).revision == PrivateStateRevision(1)
    assert _snapshot(store, second).revision == PrivateStateRevision(1)
    assert old_first.value == 1
    assert old_second.value == 2
    assert old_first.revision == PrivateStateRevision.initial()
    assert old_second.revision == PrivateStateRevision.initial()


def test_stale_member_rejects_entire_multi_module_batch() -> None:
    first = _descriptor("state.first")
    second = _descriptor("state.second")
    store = PrivateStateStore(
        (first, second),
        {first.module_id: 1, second.module_id: 2},
    )
    first_update = store._prepare(_proposal(first, 10, attempt=1))
    stale_second = store._prepare(_proposal(second, 20, attempt=2))
    store._apply_prepared((stale_second,))
    before_first = _snapshot(store, first)
    before_second = _snapshot(store, second)

    with pytest.raises(StaleProposalError):
        store._apply_prepared((first_update, stale_second))

    assert store.snapshot_for(first.module_id) == before_first
    assert store.snapshot_for(second.module_id) == before_second


def test_duplicate_or_invalid_prepared_item_rejects_before_mutation() -> None:
    descriptor = _descriptor("state.duplicate")
    store = PrivateStateStore((descriptor,), {descriptor.module_id: 1})
    prepared = store._prepare(_proposal(descriptor, 2))
    before = _snapshot(store, descriptor)

    with pytest.raises(DuplicateIdentityError):
        store._apply_prepared((prepared, prepared))
    with pytest.raises(TypeError, match="prepared private updates"):
        store._apply_prepared(cast(tuple[_PreparedPrivateStateUpdate, ...], (prepared, object())))

    invalid_next = _PreparedPrivateStateUpdate(
        module_id=descriptor.module_id,
        expected_revision=PrivateStateRevision.initial(),
        next_revision=PrivateStateRevision(1),
        frozen_value=2,
    )
    object.__setattr__(invalid_next, "next_revision", PrivateStateRevision(5))
    with pytest.raises(CommitValidationError, match="next private revision"):
        store._apply_prepared((invalid_next,))

    assert store.snapshot_for(descriptor.module_id) == before
