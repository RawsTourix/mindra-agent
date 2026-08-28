"""Process-local passive recorder structural O0 evidence."""

from mindra.contracts.evidence import TraceEventEnvelope


class InMemoryEvidenceRecorder:
    """Append-only recorder, сохраняющий insertion order immutable events."""

    __slots__ = ("_events",)

    _events: list[TraceEventEnvelope]

    def __init__(self) -> None:
        self._events = []

    def record(self, event: TraceEventEnvelope, /) -> None:
        """Fail closed записать ровно переданный immutable envelope."""
        if not isinstance(event, TraceEventEnvelope):
            raise TypeError("event должен быть TraceEventEnvelope")
        self._events.append(event)

    def snapshot(self) -> tuple[TraceEventEnvelope, ...]:
        """Вернуть новый immutable snapshot текущей insertion sequence."""
        return tuple(self._events)

    def __len__(self) -> int:
        return len(self._events)


__all__ = ["InMemoryEvidenceRecorder"]
