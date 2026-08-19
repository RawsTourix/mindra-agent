"""Concrete factories causal identities для Core Kernel runtime."""

from typing import TypeVar
from uuid import UUID, uuid5, uuid7

from mindra.contracts.identity import IdentityType

IdentityT = TypeVar("IdentityT", bound=UUID)


class Uuid7IdFactory:
    """Factory normal runtime identities на основе stdlib UUIDv7."""

    __slots__ = ()

    def new_id(self, identity_type: IdentityType[IdentityT], /) -> IdentityT:
        """Создать новый UUIDv7 и вернуть требуемый identity-тип."""
        return identity_type(uuid7())


class DeterministicIdFactory:
    """Воспроизводимая namespace/seed/counter identity sequence."""

    __slots__ = ("_counter", "_namespace", "_seed")

    def __init__(self, namespace: UUID, seed: str, counter: int = 0) -> None:
        if not isinstance(namespace, UUID):
            raise TypeError("Namespace deterministic factory должен быть UUID")
        if not isinstance(seed, str):
            raise TypeError("Seed deterministic factory должен быть строкой")
        if type(counter) is not int:
            raise TypeError("Counter deterministic factory должен быть целым числом")
        if counter < 0:
            raise ValueError("Counter deterministic factory не может быть отрицательным")

        self._namespace = namespace
        self._seed = seed
        self._counter = counter

    @property
    def namespace(self) -> UUID:
        """Вернуть namespace sequence."""
        return self._namespace

    @property
    def seed(self) -> str:
        """Вернуть seed sequence."""
        return self._seed

    @property
    def counter(self) -> int:
        """Вернуть counter следующей создаваемой identity."""
        return self._counter

    def new_id(self, identity_type: IdentityType[IdentityT], /) -> IdentityT:
        """Создать следующую deterministic identity требуемого типа."""
        identity_name = identity_type.__name__
        value = uuid5(
            self._namespace,
            f"mindra:{self._seed}:{self._counter}:{identity_name}",
        )
        self._counter += 1
        return identity_type(value)


__all__ = ["DeterministicIdFactory", "Uuid7IdFactory"]
