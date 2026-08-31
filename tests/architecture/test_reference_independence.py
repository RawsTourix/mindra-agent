"""Механические проверки production dependency boundary reference package."""

import ast
from pathlib import Path

import mindra.reference

_REFERENCE_ROOT = Path(mindra.reference.__file__).parent
_FORBIDDEN_DEPENDENCIES = (
    "mindra.runtime",
    "mindra.composition",
    "mindra.entrypoints",
)
_FORBIDDEN_ACCESS_NAMES = {
    "composition_root",
    "config",
    "registry",
    "service_locator",
    "services",
}


def _production_trees() -> tuple[ast.Module, ...]:
    return tuple(
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for path in sorted(_REFERENCE_ROOT.glob("*.py"))
    )


def test_reference_imports_only_contracts_and_its_own_package() -> None:
    imported_modules: set[str] = set()
    for tree in _production_trees():
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported_modules.add(node.module)

    assert not any(
        imported == forbidden or imported.startswith(f"{forbidden}.")
        for imported in imported_modules
        for forbidden in _FORBIDDEN_DEPENDENCIES
    )
    first_party = {name for name in imported_modules if name.startswith("mindra")}
    assert all(
        name == "mindra.contracts"
        or name.startswith("mindra.contracts.")
        or name == "mindra.reference"
        or name.startswith("mindra.reference.")
        for name in first_party
    )


def test_reference_has_no_service_locator_registry_or_config_access() -> None:
    used_names = {
        node.id.casefold()
        for tree in _production_trees()
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
    }
    used_names.update(
        node.attr.casefold()
        for tree in _production_trees()
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
    )

    assert used_names.isdisjoint(_FORBIDDEN_ACCESS_NAMES)
