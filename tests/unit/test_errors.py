"""Проверки typed fail-closed taxonomy ошибок Core Kernel."""

import pytest

from mindra.runtime import (
    AvailabilityError,
    CommitValidationError,
    CompositionError,
    ConfigurationError,
    DependencyCycleError,
    DuplicateIdentityError,
    ExecutionPlanError,
    InterventionError,
    KernelError,
    MissingFieldError,
    ModuleExecutionError,
    SchemaError,
    StaleProposalError,
    UnauthorizedWriteError,
    UndeclaredReadError,
    WaveExecutionError,
)

ERROR_TYPES = (
    ConfigurationError,
    CompositionError,
    DuplicateIdentityError,
    SchemaError,
    MissingFieldError,
    UndeclaredReadError,
    UnauthorizedWriteError,
    AvailabilityError,
    ExecutionPlanError,
    DependencyCycleError,
    ModuleExecutionError,
    WaveExecutionError,
    CommitValidationError,
    StaleProposalError,
    InterventionError,
)


@pytest.mark.parametrize("error_type", ERROR_TYPES)
def test_kernel_errors_are_typed_exceptions(error_type: type[KernelError]) -> None:
    error = error_type("typed reason")

    assert isinstance(error, KernelError)
    assert str(error) == "typed reason"


def test_specific_errors_have_fail_closed_categories() -> None:
    assert issubclass(DuplicateIdentityError, CompositionError)
    assert issubclass(MissingFieldError, SchemaError)
    assert issubclass(UndeclaredReadError, SchemaError)
    assert issubclass(DependencyCycleError, ExecutionPlanError)
    assert issubclass(UnauthorizedWriteError, CommitValidationError)
    assert issubclass(StaleProposalError, CommitValidationError)


def test_configuration_and_module_compute_failures_are_distinct() -> None:
    assert not issubclass(ConfigurationError, ModuleExecutionError)
    assert not issubclass(ModuleExecutionError, ConfigurationError)


def test_typed_failure_is_raised_instead_of_boolean_status() -> None:
    with pytest.raises(StaleProposalError, match="base revision"):
        raise StaleProposalError("недопустимая base revision")
