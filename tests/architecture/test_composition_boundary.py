"""Static architecture constraints Configuration/Composition Root IS-13."""

import ast
from pathlib import Path


def _production_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imports.add(node.module)
    return imports


def test_runtime_and_reference_do_not_import_composition() -> None:
    paths = tuple(Path("src/mindra/runtime").glob("*.py")) + tuple(
        Path("src/mindra/reference").glob("*.py")
    )
    assert all(
        not any(
            name == "mindra.composition" or name.startswith("mindra.composition.")
            for name in _production_imports(path)
        )
        for path in paths
    )


def test_entrypoints_do_not_assemble_composition_ahead_of_is_15() -> None:
    paths = (*Path("src/mindra/entrypoints").glob("*.py"), Path("src/mindra/__main__.py"))
    assert all(
        not any(
            name == "mindra.composition" or name.startswith("mindra.composition.")
            for name in _production_imports(path)
        )
        for path in paths
    )


def test_composition_has_no_registration_or_plugin_discovery_surface() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8") for path in Path("src/mindra/composition").glob("*.py")
    )
    assert "entry_points" not in source
    assert "import_module" not in source
    assert "@register" not in source
