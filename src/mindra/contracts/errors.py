"""Типизированная fail-closed taxonomy ошибок Core Kernel."""


class KernelError(Exception):
    """Базовая ошибка semantic/runtime boundary Core Kernel."""


class ConfigurationError(KernelError):
    """Ошибка чтения или валидации пользовательской конфигурации."""


class CompositionError(KernelError):
    """Ошибка сборки несовместимой kernel composition."""


class DuplicateIdentityError(CompositionError):
    """Ошибка повторного использования identity в одном scope."""


class SchemaError(KernelError):
    """Ошибка structural state schema contract."""


class MissingFieldError(SchemaError):
    """Required structural field отсутствует в active schema/state."""


class UndeclaredReadError(SchemaError):
    """Consumer запросил field вне declared read contract."""


class CommitValidationError(KernelError):
    """Staged state/private effect не прошёл commit validation."""


class UnauthorizedWriteError(CommitValidationError):
    """Producer попытался записать field без write authority."""


class AvailabilityError(KernelError):
    """Availability/freshness не удовлетворяет declared contract."""


class ExecutionPlanError(KernelError):
    """Active descriptors не образуют допустимый execution plan."""


class DependencyCycleError(ExecutionPlanError):
    """Execution plan содержит instantaneous dependency cycle."""


class ModuleExecutionError(KernelError):
    """Ошибка compute одного module attempt."""


class WaveExecutionError(KernelError):
    """Execution wave не может быть атомарно завершена."""


class StaleProposalError(CommitValidationError):
    """Proposal относится к недопустимой base revision."""


class InterventionError(KernelError):
    """Intervention не прошла target/base/policy validation."""


__all__ = [
    "AvailabilityError",
    "CommitValidationError",
    "CompositionError",
    "ConfigurationError",
    "DependencyCycleError",
    "DuplicateIdentityError",
    "ExecutionPlanError",
    "InterventionError",
    "KernelError",
    "MissingFieldError",
    "ModuleExecutionError",
    "SchemaError",
    "StaleProposalError",
    "UnauthorizedWriteError",
    "UndeclaredReadError",
    "WaveExecutionError",
]
