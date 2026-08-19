"""Проверки наличия всех принятых слоёв пакета."""

from importlib import import_module

import pytest

PACKAGE_LAYERS = (
    "mindra.contracts",
    "mindra.runtime",
    "mindra.reference",
    "mindra.composition",
    "mindra.entrypoints",
)


@pytest.mark.parametrize("package_name", PACKAGE_LAYERS)
def test_package_layer_is_importable(package_name: str) -> None:
    assert import_module(package_name).__name__ == package_name
