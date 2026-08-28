"""Runtime-controlled construction committed state и module projections."""

from collections.abc import Iterable, Mapping

from mindra.contracts.state import (
    CognitiveState,
    ReadSpec,
    StateEntry,
    StateEnvelope,
    StatePath,
    StateProjection,
    StateSchema,
)
from mindra.contracts.time import LogicalTime


def build_cognitive_state(
    *,
    schema: StateSchema,
    envelope: StateEnvelope,
    entries: Mapping[StatePath, StateEntry[object]],
) -> CognitiveState:
    """Построить committed snapshot с schema validation и payload freeze."""
    return CognitiveState(schema=schema, envelope=envelope, entries=entries)


def copy_cognitive_state(
    *,
    base_state: CognitiveState,
    schema: StateSchema,
    envelope: StateEnvelope,
    replacements: Mapping[StatePath, StateEntry[object]],
) -> CognitiveState:
    """Построить новый snapshot copy-on-commit без мутации base state."""
    if not isinstance(base_state, CognitiveState):
        raise TypeError("base_state должен быть CognitiveState")
    if not isinstance(replacements, Mapping):
        raise TypeError("replacements должен быть Mapping")
    entries = dict(base_state.entries)
    entries.update(replacements)
    return CognitiveState(schema=schema, envelope=envelope, entries=entries)


def build_state_projection(
    *,
    base_state: CognitiveState,
    read_specs: Iterable[ReadSpec[object]],
    logical_time: LogicalTime | None = None,
) -> StateProjection:
    """Создать узкую projection только из declared reads и committed base state."""
    if not isinstance(base_state, CognitiveState):
        raise TypeError("base_state должен быть CognitiveState")
    projection_time = base_state.envelope.logical_time if logical_time is None else logical_time
    if not isinstance(projection_time, LogicalTime):
        raise TypeError("logical_time должен быть LogicalTime или None")

    base_time = base_state.envelope.logical_time
    if projection_time.run_id != base_time.run_id:
        raise ValueError("Projection logical_time не может менять run_id base state")
    if projection_time.agent_session_id != base_time.agent_session_id:
        raise ValueError("Projection logical_time не может менять agent_session_id base state")
    for field_name in ("episode_id", "decision_window_id"):
        base_value = getattr(base_time, field_name)
        if base_value is not None and base_value != getattr(projection_time, field_name):
            raise ValueError(f"Projection logical_time несовместим с base {field_name}")
    return StateProjection._from_runtime(
        read_specs=read_specs,
        entries=base_state.entries,
        logical_time=projection_time,
    )


__all__ = ["build_cognitive_state", "build_state_projection", "copy_cognitive_state"]
