"""Проверка metadata и запуска clean wheel v0.1 в отдельном окружении."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from email.parser import BytesParser
from email.policy import default
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROFILE = (PROJECT_ROOT / "configs" / "v0.1" / "reference.toml").resolve()
WHEEL = PROJECT_ROOT / "dist" / "mindra_agent-0.1.0-py3-none-any.whl"

EXPECTED_VALIDATE = "OK validate-profile profile=v0_1.reference modules=4 waves=3\n"
EXPECTED_SMOKE = "OK kernel-smoke profile=v0_1.reference waves=3 revision=3 join=10\n"


class VerificationError(RuntimeError):
    """Ошибка проверки собранного artifact."""


def _verify_metadata() -> None:
    if not WHEEL.is_file():
        raise VerificationError(f"wheel не найден: {WHEEL}")

    with zipfile.ZipFile(WHEEL) as wheel_archive:
        metadata_paths = [
            name for name in wheel_archive.namelist() if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_paths) != 1:
            raise VerificationError(
                f"wheel должен содержать ровно один *.dist-info/METADATA, найдено: {metadata_paths}"
            )
        metadata = BytesParser(policy=default).parsebytes(wheel_archive.read(metadata_paths[0]))

    if metadata.get("Name") != "mindra-agent":
        raise VerificationError(f"неожиданное metadata Name: {metadata.get('Name')!r}")
    if metadata.get("Version") != "0.1.0":
        raise VerificationError(f"неожиданное metadata Version: {metadata.get('Version')!r}")
    requirements = metadata.get_all("Requires-Dist", [])
    if requirements:
        raise VerificationError(f"найдены runtime requirements: {requirements}")


def _run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment["PYTHONNOUSERSITE"] = "1"
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _require_success(command: list[str], *, cwd: Path) -> None:
    result = _run(command, cwd=cwd)
    if result.returncode != 0:
        raise VerificationError(
            f"команда завершилась с кодом {result.returncode}: {command!r}; "
            f"stdout={result.stdout!r}; stderr={result.stderr!r}"
        )


def _require_exact(
    command: list[str],
    *,
    cwd: Path,
    expected_stdout: str,
) -> None:
    result = _run(command, cwd=cwd)
    actual = (result.returncode, result.stdout, result.stderr)
    expected = (0, expected_stdout, "")
    if actual != expected:
        raise VerificationError(
            f"неожиданный CLI result для {command!r}: {actual!r}; ожидался {expected!r}"
        )


def _verify_clean_install() -> None:
    uv = shutil.which("uv")
    if uv is None:
        raise VerificationError("current uv не найден в PATH")

    with tempfile.TemporaryDirectory(prefix="mindra-v0-1-artifact-") as temp_name:
        temp_root = Path(temp_name)
        venv = temp_root / "venv"
        _require_success([uv, "venv", "--python", "3.14", str(venv)], cwd=temp_root)

        scripts = venv / ("Scripts" if os.name == "nt" else "bin")
        python = scripts / ("python.exe" if os.name == "nt" else "python")
        mindra = scripts / ("mindra.exe" if os.name == "nt" else "mindra")
        if not python.is_file():
            raise VerificationError(f"venv Python не найден: {python}")

        _require_exact(
            [
                str(python),
                "-c",
                "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
            ],
            cwd=temp_root,
            expected_stdout="3.14\n",
        )
        _require_success(
            [uv, "pip", "install", "--python", str(python), str(WHEEL.resolve())],
            cwd=temp_root,
        )

        profile_arguments = ["--profile", str(PROFILE)]
        _require_exact(
            [str(python), "-m", "mindra", "validate-profile", *profile_arguments],
            cwd=temp_root,
            expected_stdout=EXPECTED_VALIDATE,
        )
        _require_exact(
            [str(python), "-m", "mindra", "kernel-smoke", *profile_arguments],
            cwd=temp_root,
            expected_stdout=EXPECTED_SMOKE,
        )
        _require_exact(
            [str(mindra), "validate-profile", *profile_arguments],
            cwd=temp_root,
            expected_stdout=EXPECTED_VALIDATE,
        )
        _require_exact(
            [str(mindra), "kernel-smoke", *profile_arguments],
            cwd=temp_root,
            expected_stdout=EXPECTED_SMOKE,
        )


def main() -> int:
    try:
        _verify_metadata()
        _verify_clean_install()
    except (OSError, VerificationError, zipfile.BadZipFile) as error:
        print(f"FAIL verify-v0.1-artifact: {error}", file=sys.stderr)
        return 1

    print(f"PASS verify-v0.1-artifact wheel={WHEEL.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
