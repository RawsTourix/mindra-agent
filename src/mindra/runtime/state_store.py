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
) -> StateProjection:
    """Создать узкую projection только из declared reads и committed base state."""
    if not isinstance(base_state, CognitiveState):
        raise TypeError("base_state должен быть CognitiveState")
    return StateProjection._from_runtime(
        read_specs=read_specs,
        entries=base_state.entries,
        logical_time=base_state.envelope.logical_time,
    )


__all__ = ["build_cognitive_state", "build_state_projection", "copy_cognitive_state"]
