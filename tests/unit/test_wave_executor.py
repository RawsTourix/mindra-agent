"""Focused checks physical SequentialWaveExecutor boundary."""

from typing import cast

from mindra.contracts import ModuleComputeRequest, ModuleComputeResult
from mindra.runtime import (
    ModuleAttemptExecutionRequest,
    SequentialWaveExecutor,
)
from tests.scheduler_support import TestModule, make_scheduler_context, module_for


def test_sequential_executor_continues_siblings_after_normal_exception() -> None:
    context = make_scheduler_context()
    context.scheduler.run_cycle(current_state=context.state, cycle_time=context.cycle_time)
    beta = module_for(context, "beta")
    gamma = module_for(context, "gamma")

    def fail(_request: ModuleComputeRequest) -> ModuleComputeResult:
        raise RuntimeError("expected failure")

    failing = TestModule(beta.descriptor, fail)
    succeeding = TestModule(gamma.descriptor, gamma.compute_function)
    attempts = (
        ModuleAttemptExecutionRequest(
            beta.descriptor.module_id,
            failing,
            beta.requests[0],
        ),
        ModuleAttemptExecutionRequest(
            gamma.descriptor.module_id,
            succeeding,
            gamma.requests[0],
        ),
    )

    records = SequentialWaveExecutor().execute(attempts)

    assert records[0].failure is not None
    assert records[0].failure.error_type == "RuntimeError"
    assert records[1].result is not None
    assert len(succeeding.requests) == 1


def test_non_module_result_becomes_typed_failed_attempt() -> None:
    context = make_scheduler_context()
    context.scheduler.run_cycle(current_state=context.state, cycle_time=context.cycle_time)
    beta = module_for(context, "beta")

    def malformed(_request: ModuleComputeRequest) -> ModuleComputeResult:
        return cast(ModuleComputeResult, object())

    module = TestModule(beta.descriptor, malformed)
    attempt = ModuleAttemptExecutionRequest(
        beta.descriptor.module_id,
        module,
        beta.requests[0],
    )

    record = SequentialWaveExecutor().execute((attempt,))[0]

    assert record.result is None
    assert record.failure is not None
    assert record.failure.error_type == "ModuleExecutionError"
