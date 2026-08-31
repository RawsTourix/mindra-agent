"""Архитектурные проверки финальной границы ответственности v0.1."""

import ast
import sys
import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import cast

import mindra.entrypoints.cli as cli

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PRODUCTION_ROOT = PROJECT_ROOT / "src" / "mindra"

FOUNDATION_PACKAGES = {
    "composition",
    "contracts",
    "entrypoints",
    "reference",
    "runtime",
}
FOUNDATION_MODULES = {"__init__.py", "__main__.py"}
PUBLIC_COMMANDS = {"kernel-smoke", "validate-profile"}


def _external_import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.partition(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module is not None:
            roots.add(node.module.partition(".")[0])
    return roots


def test_project_declares_no_third_party_runtime_dependencies() -> None:
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)

    assert pyproject["project"]["dependencies"] == []


def test_production_imports_use_only_stdlib_and_mindra() -> None:
    allowed_roots = {*sys.stdlib_module_names, "__future__", "mindra"}
    unexpected = {
        path.relative_to(PROJECT_ROOT).as_posix(): sorted(
            _external_import_roots(path) - allowed_roots
        )
        for path in PRODUCTION_ROOT.rglob("*.py")
        if _external_import_roots(path) - allowed_roots
    }

    assert unexpected == {}


def test_production_surface_contains_only_v0_1_foundation_layers() -> None:
    packages = {
        path.name
        for path in PRODUCTION_ROOT.iterdir()
        if path.is_dir() and path.name != "__pycache__"
    }
    modules = {
        path.name for path in PRODUCTION_ROOT.iterdir() if path.is_file() and path.suffix == ".py"
    }

    assert packages == FOUNDATION_PACKAGES
    assert modules == FOUNDATION_MODULES


def test_public_cli_contains_only_accepted_commands() -> None:
    parser = cli._parser()
    command_actions = [action for action in parser._actions if action.dest == "command"]

    assert len(command_actions) == 1
    choices = cast(Mapping[str, object], command_actions[0].choices)
    assert set(choices) == PUBLIC_COMMANDS
