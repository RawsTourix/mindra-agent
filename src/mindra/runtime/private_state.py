"""Runtime-owned transactional storage module-private state Core Kernel."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from mindra.contracts.availability import Unavailable
from mindra.contracts.errors import (
    CommitValidationError,
    ConfigurationError,
    DuplicateIdentityError,
    StaleProposalError,
)
from mindra.contracts.identity import ModuleId
from mindra.contracts.modules import (
    ModuleDescriptor,
    ModuleStatefulness,
    PrivateStateProposal,
    PrivateStateSnapshot,
)
from mindra.contracts.revisions import PrivateStateRevision


@dataclass(frozen=True, slots=True)
class PrivateStateSlot:
    """Immutable committed slot одного semantic module."""

    module_id: ModuleId
    revision: PrivateStateRevision
    value: object

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        if not isinstance(self.revision, PrivateStateRevision):
            raise TypeError("revision должен быть PrivateStateRevision")


@dataclass(frozen=True, slots=True)
class _PreparedPrivateStateUpdate:
    """Validated frozen private effect до внутреннего apply."""

    module_id: ModuleId
    expected_revision: PrivateStateRevision
    next_revision: PrivateStateRevision
    frozen_value: object

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        if not isinstance(self.expected_revision, PrivateStateRevision):
            raise TypeError("expected_revision должен быть PrivateStateRevision")
        if not isinstance(self.next_revision, PrivateStateRevision):
            raise TypeError("next_revision должен быть PrivateStateRevision")
        if self.next_revision != self.expected_revision.next():
            raise CommitValidationError(
                "Prepared private update должен увеличивать revision ровно на один"
            )


class PrivateStateStore:
    """Encapsulated active private state с staged all-or-nothing mutation."""

    __slots__ = ("_descriptors", "_slots")

    _descriptors: Mapping[ModuleId, ModuleDescriptor]
    _slots: dict[ModuleId, PrivateStateSlot]

    def __init__(
        self,
        descriptors: tuple[ModuleDescriptor, ...],
        initial_values: Mapping[ModuleId, object],
    ) -> None:
        if not isinstance(descriptors, tuple):
            raise TypeError("descriptors должен быть tuple ModuleDescriptor")
        if not isinstance(initial_values, Mapping):
            raise TypeError("initial_values должен быть Mapping")

        registered: dict[ModuleId, ModuleDescriptor] = {}
        for descriptor in descriptors:
            if not isinstance(descriptor, ModuleDescriptor):
                raise TypeError("descriptors должен содержать ModuleDescriptor")
            if descriptor.module_id in registered:
                raise DuplicateIdentityError(
                    f"Duplicate active ModuleId private state: {descriptor.module_id}"
                )
            registered[descriptor.module_id] = descriptor

        for module_id in initial_values:
            if not isinstance(module_id, ModuleId):
                raise TypeError("initial_values keys должны быть ModuleId")
            if module_id not in registered:
                raise ConfigurationError(
                    f"Initial private state передан unknown module: {module_id}"
                )

        slots: dict[ModuleId, PrivateStateSlot] = {}
        for descriptor in descriptors:
            module_id = descriptor.module_id
            has_initial_value = module_id in initial_values
            if descriptor.traits.statefulness is ModuleStatefulness.STATELESS:
                if has_initial_value:
                    raise ConfigurationError(
                        f"Stateless module не принимает initial private state: {module_id}"
                    )
                continue

            if not has_initial_value:
                raise ConfigurationError(
                    f"Stateful module требует explicit initial private state: {module_id}"
                )
            private_descriptor = descriptor.private_state
            if private_descriptor is None:
                raise ConfigurationError(
                    f"Stateful module не имеет private-state descriptor: {module_id}"
                )
            frozen_value = private_descriptor.contract.freeze(initial_values[module_id])
            slots[module_id] = PrivateStateSlot(
                module_id=module_id,
                revision=PrivateStateRevision.initial(),
                value=frozen_value,
            )

        self._descriptors = MappingProxyType(registered)
        self._slots = slots

    def snapshot_for(self, module_id: ModuleId) -> PrivateStateSnapshot[object] | Unavailable:
        """Вернуть snapshot только requested registered semantic module."""
        descriptor = self._descriptor_for(module_id)
        if descriptor.traits.statefulness is ModuleStatefulness.STATELESS:
            return Unavailable()

        slot = self._stateful_slot_for(module_id)
        return PrivateStateSnapshot(
            module_id=slot.module_id,
            revision=slot.revision,
            value=slot.value,
        )

    def _prepare(self, proposal: PrivateStateProposal[object]) -> _PreparedPrivateStateUpdate:
        """Validate/freeze proposal без mutation committed slots."""
        if not isinstance(proposal, PrivateStateProposal):
            raise TypeError("proposal должен быть PrivateStateProposal")

        descriptor = self._descriptor_for(proposal.module_id)
        if descriptor.traits.statefulness is ModuleStatefulness.STATELESS:
            raise ConfigurationError(
                f"Stateless module не может предложить private update: {proposal.module_id}"
            )

        slot = self._stateful_slot_for(proposal.module_id)
        if proposal.base_revision != slot.revision:
            raise StaleProposalError(
                f"Private proposal module {proposal.module_id} ожидает revision "
                f"{proposal.base_revision.value}, current {slot.revision.value}"
            )

        private_descriptor = descriptor.private_state
        if private_descriptor is None:
            raise ConfigurationError(
                f"Stateful module не имеет private-state descriptor: {proposal.module_id}"
            )
        frozen_value = private_descriptor.contract.freeze(proposal.value)
        return _PreparedPrivateStateUpdate(
            module_id=proposal.module_id,
            expected_revision=slot.revision,
            next_revision=slot.revision.next(),
            frozen_value=frozen_value,
        )

    def _apply_prepared(self, updates: tuple[_PreparedPrivateStateUpdate, ...]) -> None:
        """После полной prevalidation заменить все affected slots либо ни одного."""
        if not isinstance(updates, tuple):
            raise TypeError("updates должен быть tuple prepared private updates")

        seen: set[ModuleId] = set()
        replacements: dict[ModuleId, PrivateStateSlot] = {}
        for update in updates:
            if not isinstance(update, _PreparedPrivateStateUpdate):
                raise TypeError("updates должен содержать prepared private updates")
            if update.module_id in seen:
                raise DuplicateIdentityError(
                    f"Duplicate ModuleId в private apply batch: {update.module_id}"
                )
            seen.add(update.module_id)

            descriptor = self._descriptor_for(update.module_id)
            if descriptor.traits.statefulness is ModuleStatefulness.STATELESS:
                raise ConfigurationError(
                    f"Stateless module не имеет private slot: {update.module_id}"
                )
            slot = self._stateful_slot_for(update.module_id)
            if slot.revision != update.expected_revision:
                raise StaleProposalError(
                    f"Prepared private update module {update.module_id} ожидает revision "
                    f"{update.expected_revision.value}, current {slot.revision.value}"
                )
            if update.next_revision != slot.revision.next():
                raise CommitValidationError(
                    f"Invalid next private revision module {update.module_id}"
                )

            replacements[update.module_id] = PrivateStateSlot(
                module_id=update.module_id,
                revision=update.next_revision,
                value=update.frozen_value,
            )

        self._slots.update(replacements)

    def _descriptor_for(self, module_id: ModuleId) -> ModuleDescriptor:
        if not isinstance(module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        try:
            return self._descriptors[module_id]
        except KeyError as error:
            raise ConfigurationError(f"Unknown active ModuleId: {module_id}") from error

    def _stateful_slot_for(self, module_id: ModuleId) -> PrivateStateSlot:
        try:
            return self._slots[module_id]
        except KeyError as error:
            raise ConfigurationError(
                f"Active stateful module не имеет initialized private slot: {module_id}"
            ) from error


__all__ = ["PrivateStateSlot", "PrivateStateStore"]
