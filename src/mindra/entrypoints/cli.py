"""Тонкий CLI-адаптер deterministic Core Kernel smoke."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast
from uuid import NAMESPACE_URL

from mindra.composition import (
    CompositionRoot,
    KernelRuntime,
    build_reference_registry,
    load_kernel_profile,
)
from mindra.contracts import AvailabilityError, Available, KernelError, StateKey, StatePath
from mindra.runtime import CycleExecutionOutcome, DeterministicIdFactory

_VALIDATE_SEED = "mindra.v0_1.validate_profile"
_SMOKE_SEED = "mindra.v0_1.kernel_smoke"
_JOIN_VALUE_KEY = StateKey[int](StatePath.from_dotted("synthetic.join.value"))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mindra")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("validate-profile", "kernel-smoke"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("--profile", required=True, type=Path)
    return parser


def _build_runtime(profile_path: Path, *, seed: str) -> KernelRuntime:
    profile = load_kernel_profile(profile_path)
    registry = build_reference_registry()
    id_factory = DeterministicIdFactory(NAMESPACE_URL, seed, counter=0)
    return CompositionRoot(registry=registry, id_factory=id_factory).build(profile)


def _validate_profile(profile_path: Path) -> int:
    runtime = _build_runtime(profile_path, seed=_VALIDATE_SEED)
    print(
        "OK validate-profile "
        f"profile={runtime.profile.profile_id} "
        f"modules={len(runtime.composition.descriptors)} "
        f"waves={len(runtime.plan.waves)}"
    )
    return 0


def _kernel_smoke(profile_path: Path) -> int:
    runtime = _build_runtime(profile_path, seed=_SMOKE_SEED)
    result = runtime.run_cycle()
    if result.outcome is CycleExecutionOutcome.FAILED:
        assert result.failure is not None
        print(
            "error: kernel smoke cycle failed: "
            f"{result.failure.error_type}: {result.failure.message}",
            file=sys.stderr,
        )
        return 1

    join_availability = runtime.state.read(_JOIN_VALUE_KEY).availability
    if not isinstance(join_availability, Available) or type(join_availability.value) is not int:
        raise AvailabilityError("synthetic.join.value должен быть Available[int]")

    print(
        "OK kernel-smoke "
        f"profile={runtime.profile.profile_id} "
        f"waves={len(runtime.plan.waves)} "
        f"revision={runtime.state.envelope.state_revision.value} "
        f"join={join_availability.value}"
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Разобрать CLI и выполнить ровно одну запрошенную kernel-команду."""
    arguments = _parser().parse_args(argv)
    command = cast(str, arguments.command)
    profile_path = cast(Path, arguments.profile)

    try:
        if command == "validate-profile":
            return _validate_profile(profile_path)
        return _kernel_smoke(profile_path)
    except KernelError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except Exception as error:
        print(
            f"error: internal failure: {type(error).__name__}: {error}",
            file=sys.stderr,
        )
        return 1


__all__ = ["main"]
