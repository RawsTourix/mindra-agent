"""Проверки устанавливаемого пакета и его метаданных."""

from importlib.metadata import version

import mindra


def test_package_import_and_version() -> None:
    assert mindra.__version__ == "0.1.0"


def test_distribution_metadata_version() -> None:
    assert version("mindra-agent") == "0.1.0"
