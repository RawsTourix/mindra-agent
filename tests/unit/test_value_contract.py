"""Проверки default snapshot-safe ValueContract."""

from dataclasses import dataclass
from enum import Enum
from uuid import UUID

import pytest

from mindra.contracts import SchemaError, ValueContract


@dataclass(frozen=True, slots=True)
class FrozenPayload:
    """Тестовый immutable canonical payload."""

    label: str
    values: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class FrozenShellWithMutableField:
    """Frozen dataclass с небезопасным вложенным mutable value."""

    values: list[int]


def _mutable_enum_value() -> list[int]:
    return [1, 2]


class ImmutableValueEnum(Enum):
    """Enum с immutable underlying value."""

    VALUE = ("safe", 1)


class MutableListValueEnum(Enum):
    """Enum с mutable list как underlying value."""

    VALUE = _mutable_enum_value()


class NestedMutableValueEnum(Enum):
    """Enum с вложенным mutable underlying value."""

    VALUE = ("unsafe", _mutable_enum_value())


@pytest.mark.parametrize(
    "value",
    [
        7,
        "canonical",
        UUID(int=1),
        (1, "two", frozenset({3})),
        FrozenPayload(label="safe", values=(1, 2)),
    ],
)
def test_value_contract_accepts_snapshot_safe_immutable_values(value: object) -> None:
    contract = ValueContract(object)

    contract.validate(value)

    assert contract.freeze(value) is value


@pytest.mark.parametrize("value", [[1], {"value": 1}, {1, 2}])
def test_value_contract_rejects_known_mutable_builtins(value: object) -> None:
    contract = ValueContract(object)

    with pytest.raises(SchemaError):
        contract.validate(value)
    with pytest.raises(SchemaError):
        contract.freeze(value)


def test_value_contract_rejects_mutability_nested_in_frozen_dataclass() -> None:
    contract = ValueContract(FrozenShellWithMutableField)

    with pytest.raises(SchemaError):
        contract.freeze(FrozenShellWithMutableField(values=[1]))


def test_value_contract_accepts_enum_with_immutable_value() -> None:
    contract = ValueContract(ImmutableValueEnum)

    assert contract.freeze(ImmutableValueEnum.VALUE) is ImmutableValueEnum.VALUE


@pytest.mark.parametrize("value", [MutableListValueEnum.VALUE, NestedMutableValueEnum.VALUE])
def test_value_contract_rejects_enum_with_mutable_value(value: Enum) -> None:
    contract = ValueContract(type(value))

    with pytest.raises(SchemaError, match="snapshot-safe"):
        contract.freeze(value)


def test_value_contract_rejects_wrong_runtime_type() -> None:
    contract = ValueContract(int)

    with pytest.raises(SchemaError):
        contract.validate("7")
