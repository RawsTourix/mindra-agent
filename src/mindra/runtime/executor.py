"""Physical execution module attempts без scheduling/commit authority."""

from dataclasses import dataclass
from typing import Protocol, runtime_checkable
from uuid import UUID

from mindra.contracts.errors import ModuleExecutionError
from mindra.contracts.evidence import ModuleAttemptOutcome, TraceFailure
from mindra.contracts.identity import ModuleAttemptId, ModuleId
from mindra.contracts.modules import (
    CognitiveModule,
    ExecutionPhase,
    ModuleComputeRequest,
    ModuleComputeResult,
)


@dataclass(frozen=True, slots=True)
class ModuleAttemptExecutionRequest:
    """Ephemeral physical handle одного уже подготовленного module attempt."""

    module_id: ModuleId
    module: CognitiveModule
    compute_request: ModuleComputeRequest

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        if not isinstance(self.module, CognitiveModule):
            raise TypeError("module должен удовлетворять CognitiveModule")
        if not isinstance(self.compute_request, ModuleComputeRequest):
            raise TypeError("compute_request должен быть ModuleComputeRequest")
        if self.module.descriptor.module_id != self.module_id:
            raise ValueError("Module descriptor identity не совпадает с execution request")
        if not isinstance(self.compute_request.context.module_attempt_id, UUID):
            raise TypeError("context должен содержать valid ModuleAttemptId")
        if self.compute_request.context.phase is not ExecutionPhase.COGNITIVE_CYCLE:
            raise ValueError("v0.1 executor поддерживает только COGNITIVE_CYCLE")


@dataclass(frozen=True, slots=True)
class ModuleAttemptRecord:
    """Physical outcome одного attempt с exact success/failure XOR."""

    module_id: ModuleId
    module_attempt_id: ModuleAttemptId
    result: ModuleComputeResult | None
    failure: TraceFailure | None

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        if not isinstance(self.module_attempt_id, UUID):
            raise TypeError("module_attempt_id должен быть ModuleAttemptId")
        if self.result is not None and not isinstance(self.result, ModuleComputeResult):
            raise TypeError("result должен быть ModuleComputeResult или None")
        if self.failure is not None and not isinstance(self.failure, TraceFailure):
            raise TypeError("failure должен быть TraceFailure или None")
        if (self.result is None) == (self.failure is None):
            raise ValueError("ModuleAttemptRecord требует exact result XOR failure")

    @property
    def outcome(self) -> ModuleAttemptOutcome:
        """Вернуть derived semantic attempt outcome."""
        if self.result is not None:
            return ModuleAttemptOutcome.SUCCEEDED
        return ModuleAttemptOutcome.FAILED


@runtime_checkable
class WaveExecutor(Protocol):
    """Structural physical executor уже ordered attempt collection."""

    def execute(
        self,
        attempts: tuple[ModuleAttemptExecutionRequest, ...],
        /,
    ) -> tuple[ModuleAttemptRecord, ...]:
        """Выполнить все dispatched attempts без commit/evidence side effects."""
        ...


class SequentialWaveExecutor:
    """Reference sequential executor, сохраняющий sibling execution after failure."""

    __slots__ = ()

    def execute(
        self,
        attempts: tuple[ModuleAttemptExecutionRequest, ...],
        /,
    ) -> tuple[ModuleAttemptRecord, ...]:
        """Выполнить attempts в input order и скопировать normal failures."""
        if not isinstance(attempts, tuple):
            raise TypeError("attempts должен быть tuple ModuleAttemptExecutionRequest")

        records: list[ModuleAttemptRecord] = []
        for attempt in attempts:
            if not isinstance(attempt, ModuleAttemptExecutionRequest):
                raise TypeError("attempts должен содержать ModuleAttemptExecutionRequest")
            attempt_id = attempt.compute_request.context.module_attempt_id
            try:
                result = attempt.module.compute(attempt.compute_request)
                if not isinstance(result, ModuleComputeResult):
                    raise ModuleExecutionError(
                        f"Module {attempt.module_id} вернул не ModuleComputeResult"
                    )
            except Exception as error:
                records.append(
                    ModuleAttemptRecord(
                        module_id=attempt.module_id,
                        module_attempt_id=attempt_id,
                        result=None,
                        failure=TraceFailure.from_exception(error),
                    )
                )
                continue

            records.append(
                ModuleAttemptRecord(
                    module_id=attempt.module_id,
                    module_attempt_id=attempt_id,
                    result=result,
                    failure=None,
                )
            )
        return tuple(records)


__all__ = [
    "ModuleAttemptExecutionRequest",
    "ModuleAttemptRecord",
    "SequentialWaveExecutor",
    "WaveExecutor",
]
