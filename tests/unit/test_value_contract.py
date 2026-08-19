"""Проверки default snapshot-safe ValueContract."""

from dataclasses import dataclass

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


@pytest.mark.parametrize(
    "value",
    [
        7,
        "canonical",
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


def test_value_contract_rejects_wrong_runtime_type() -> None:
    contract = ValueContract(int)

    with pytest.raises(SchemaError):
        contract.validate("7")
