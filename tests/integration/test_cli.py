"""In-process и subprocess contracts public CLI IS-15."""

import shutil
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from typing import cast
from uuid import NAMESPACE_URL

import pytest

import mindra.entrypoints.cli as cli
from mindra.composition import (
    CompositionRoot,
    KernelRuntime,
    build_reference_registry,
    load_kernel_profile,
)
from mindra.contracts import TraceFailure
from mindra.entrypoints import main
from mindra.runtime import (
    CycleExecutionOutcome,
    CycleExecutionResult,
    DeterministicIdFactory,
)

PROFILE = Path("configs/v0.1/reference.toml")
VALIDATE_OUTPUT = "OK validate-profile profile=v0_1.reference modules=4 waves=3\n"
SMOKE_OUTPUT = "OK kernel-smoke profile=v0_1.reference waves=3 revision=3 join=10\n"


@pytest.mark.parametrize(
    ("command", "expected"),
    (("validate-profile", VALIDATE_OUTPUT), ("kernel-smoke", SMOKE_OUTPUT)),
)
def test_main_success_output_is_exact(
    command: str,
    expected: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main((command, "--profile", str(PROFILE))) == 0
    captured = capsys.readouterr()
    assert captured.out == expected
    assert captured.err == ""


def test_validate_profile_does_not_run_cycle(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def forbid_cycle(self: KernelRuntime) -> CycleExecutionResult:
        raise AssertionError("validate-profile не должен вызывать run_cycle")

    monkeypatch.setattr(KernelRuntime, "run_cycle", forbid_cycle)

    assert main(("validate-profile", "--profile", str(PROFILE))) == 0
    captured = capsys.readouterr()
    assert captured.out == VALIDATE_OUTPUT
    assert captured.err == ""


def test_main_missing_profile_is_domain_error(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    missing = tmp_path / "missing.toml"

    assert main(("validate-profile", "--profile", str(missing))) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("error: Не удалось загрузить kernel profile ")
    assert "Traceback" not in captured.err
    assert captured.err.count("\n") == 1


def test_main_unexpected_exception_is_internal_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fail_load(path: str | Path) -> object:
        raise RuntimeError(f"boom: {path}")

    monkeypatch.setattr(cli, "load_kernel_profile", fail_load)

    assert main(("validate-profile", "--profile", str(PROFILE))) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == (f"error: internal failure: RuntimeError: boom: {PROFILE}\n")
    assert "Traceback" not in captured.err


class _FailedRuntime:
    def __init__(self, result: CycleExecutionResult) -> None:
        self._result = result

    def run_cycle(self) -> CycleExecutionResult:
        return self._result


def test_normal_failed_cycle_result_is_exit_one(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    runtime = CompositionRoot(
        registry=build_reference_registry(),
        id_factory=DeterministicIdFactory(NAMESPACE_URL, "failed-cli-result"),
    ).build(load_kernel_profile(PROFILE))
    succeeded = runtime.run_cycle()
    failed = replace(
        succeeded,
        outcome=CycleExecutionOutcome.FAILED,
        failure=TraceFailure("SyntheticFailure", "expected failure"),
    )

    def build_failed_runtime(profile_path: Path, *, seed: str) -> KernelRuntime:
        assert profile_path == PROFILE
        assert seed == "mindra.v0_1.kernel_smoke"
        return cast(KernelRuntime, _FailedRuntime(failed))

    monkeypatch.setattr(cli, "_build_runtime", build_failed_runtime)

    assert main(("kernel-smoke", "--profile", str(PROFILE))) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == (
        "error: kernel smoke cycle failed: SyntheticFailure: expected failure\n"
    )


def test_malformed_cli_uses_standard_argparse_exit(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as raised:
        main(("kernel-smoke",))

    assert raised.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("usage: mindra kernel-smoke")
    assert "the following arguments are required: --profile" in captured.err


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )


def _entry_commands(arguments: list[str]) -> tuple[list[str], list[str]]:
    console_script = shutil.which("mindra")
    assert console_script is not None, "uv sync --locked должен установить console script mindra"
    return ([sys.executable, "-m", "mindra", *arguments], [console_script, *arguments])


@pytest.mark.parametrize(
    ("arguments", "expected"),
    (
        (["validate-profile", "--profile", str(PROFILE)], VALIDATE_OUTPUT),
        (["kernel-smoke", "--profile", str(PROFILE)], SMOKE_OUTPUT),
    ),
)
def test_module_and_installed_console_script_are_equivalent(
    arguments: list[str],
    expected: str,
) -> None:
    module_command, console_command = _entry_commands(arguments)
    module_result = _run(module_command)
    console_result = _run(console_command)

    expected_result = (
        0,
        expected,
        "",
    )
    assert (module_result.returncode, module_result.stdout, module_result.stderr) == expected_result
    assert (
        console_result.returncode,
        console_result.stdout,
        console_result.stderr,
    ) == expected_result


def test_invalid_profile_is_equivalent_for_both_entry_forms(tmp_path: Path) -> None:
    missing = tmp_path / "missing.toml"
    arguments = ["validate-profile", "--profile", str(missing)]
    module_command, console_command = _entry_commands(arguments)
    module_result = _run(module_command)
    console_result = _run(console_command)

    assert module_result.returncode == 2
    assert module_result.stdout == ""
    assert module_result.stderr.startswith("error: ")
    assert "Traceback" not in module_result.stderr
    assert (
        console_result.returncode,
        console_result.stdout,
        console_result.stderr,
    ) == (
        module_result.returncode,
        module_result.stdout,
        module_result.stderr,
    )
