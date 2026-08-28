"""Integration checks wave module/commit failure atomicity."""

from dataclasses import replace

from mindra.contracts import (
    Available,
    ModuleComputeRequest,
    ModuleComputeResult,
    ModuleId,
    PrivateStateSnapshot,
)
from mindra.runtime import (
    CycleExecutionOutcome,
    ModuleAttemptExecutionRequest,
    ModuleAttemptRecord,
    SequentialWaveExecutor,
)
from tests.scheduler_support import make_scheduler_context, module_for


def test_module_failure_discards_successful_sibling_and_preserves_earlier_wave() -> None:
    context = make_scheduler_context()
    gamma = module_for(context, "gamma")

    def fail(_request: ModuleComputeRequest) -> ModuleComputeResult:
        raise RuntimeError("beta failed")

    beta = module_for(context, "beta")
    beta.set_compute(fail)

    result = context.scheduler.run_cycle(
        current_state=context.state,
        cycle_time=context.cycle_time,
    )

    assert result.outcome is CycleExecutionOutcome.FAILED
    assert result.completed_waves == 1
    assert result.state.envelope.state_revision.value == 1
    assert result.state.read(context.keys["alpha"]).availability == Available(2)
    assert result.state.read(context.keys["beta"]).availability == Available(2)
    assert result.state.read(context.keys["gamma"]).availability == Available(3)
    assert len(gamma.requests) == 1
    private = context.store.snapshot_for(ModuleId("scheduler.alpha"))
    assert isinstance(private, PrivateStateSnapshot)
    assert private.value == 11
    assert not any(
        event.kind.value == "commit_attempted"
        and event.logical_time.wave_id == beta.requests[0].context.logical_time.wave_id
        for event in context.recorder.snapshot()
    )


def test_commit_failure_publishes_no_current_wave_effect() -> None:
    context = make_scheduler_context()
    beta = module_for(context, "beta")
    original = beta.compute_function

    def malformed(request: ModuleComputeRequest) -> ModuleComputeResult:
        result = original(request)
        write = result.state_update.writes[0]
        bad_provenance = replace(write.provenance, logical_time=context.previous_cycle_time)
        return replace(
            result,
            state_update=replace(
                result.state_update,
                writes=(replace(write, provenance=bad_provenance),),
            ),
        )

    beta.set_compute(malformed)
    result = context.scheduler.run_cycle(
        current_state=context.state,
        cycle_time=context.cycle_time,
    )

    assert result.outcome is CycleExecutionOutcome.FAILED
    assert result.completed_waves == 1
    assert result.state.envelope.state_revision.value == 1
    kinds = [event.kind.value for event in context.recorder.snapshot()]
    assert kinds[-3:] == ["commit_attempted", "commit_failed", "cycle_failed"]


def test_executor_missing_record_fails_closed_without_commit() -> None:
    class MissingRecordExecutor:
        def execute(
            self,
            attempts: tuple[ModuleAttemptExecutionRequest, ...],
            /,
        ) -> tuple[ModuleAttemptRecord, ...]:
            return SequentialWaveExecutor().execute(attempts)[:-1]

    context = make_scheduler_context(wave_executor=MissingRecordExecutor())
    result = context.scheduler.run_cycle(
        current_state=context.state,
        cycle_time=context.cycle_time,
    )

    assert result.outcome is CycleExecutionOutcome.FAILED
    assert result.completed_waves == 0
    assert result.state is context.state
    assert result.failure is not None
    assert result.failure.error_type == "WaveExecutionError"
    assert "missing/extra" in result.failure.message
    assert [event.kind.value for event in context.recorder.snapshot()] == [
        "cycle_started",
        "wave_started",
        "module_attempt_started",
        "cycle_failed",
    ]
