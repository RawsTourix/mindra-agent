"""Отдельная runtime boundary атомарной публикации boundary-owned state."""

from dataclasses import dataclass
from uuid import UUID

from mindra.contracts.availability import Available, Stale
from mindra.contracts.boundary_state import BoundaryStateUpdate, BoundaryStateWrite
from mindra.contracts.errors import (
    CommitValidationError,
    StaleProposalError,
    UnauthorizedWriteError,
)
from mindra.contracts.identity import CommitId, IdFactory, RuntimeBoundaryId
from mindra.contracts.provenance import StateProvenance
from mindra.contracts.revisions import StateRevision
from mindra.contracts.state import (
    CognitiveState,
    StateEntry,
    StateEnvelope,
    StatePath,
    StateSchema,
)
from mindra.contracts.time import LogicalTime
from mindra.runtime.state_store import copy_cognitive_state


@dataclass(frozen=True, slots=True)
class BoundaryCommitRecord:
    """Immutable structural record successful runtime-boundary commit."""

    commit_id: CommitId
    producer: RuntimeBoundaryId
    base_state_revision: StateRevision
    resulting_state_revision: StateRevision
    logical_time: LogicalTime
    public_paths: tuple[StatePath, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.commit_id, UUID):
            raise TypeError("commit_id должен быть CommitId")
        if not isinstance(self.producer, RuntimeBoundaryId):
            raise TypeError("producer должен быть RuntimeBoundaryId")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.resulting_state_revision, StateRevision):
            raise TypeError("resulting_state_revision должен быть StateRevision")
        if self.resulting_state_revision != self.base_state_revision.next():
            raise CommitValidationError(
                "Boundary commit должен увеличивать StateRevision ровно на один"
            )
        if not isinstance(self.logical_time, LogicalTime):
            raise TypeError("logical_time должен быть LogicalTime")
        if not isinstance(self.public_paths, tuple) or any(
            not isinstance(path, StatePath) for path in self.public_paths
        ):
            raise TypeError("public_paths должен быть tuple StatePath")
        if self.public_paths != tuple(sorted(set(self.public_paths), key=lambda path: path.dotted)):
            raise CommitValidationError("public_paths должен иметь canonical unique ordering")
        if not self.public_paths:
            raise CommitValidationError("Boundary commit должен публиковать хотя бы один path")


@dataclass(frozen=True, slots=True)
class BoundaryCommitResult:
    """Успешно опубликованный boundary-owned state и commit record."""

    state: CognitiveState
    record: BoundaryCommitRecord

    def __post_init__(self) -> None:
        if not isinstance(self.state, CognitiveState):
            raise TypeError("state должен быть CognitiveState")
        if not isinstance(self.record, BoundaryCommitRecord):
            raise TypeError("record должен быть BoundaryCommitRecord")
        if self.state.envelope.state_revision != self.record.resulting_state_revision:
            raise CommitValidationError(
                "BoundaryCommitResult state revision не согласована с record"
            )


class BoundaryCommitCoordinator:
    """Validate и атомарно публикует только RuntimeBoundaryId-owned writes."""

    __slots__ = ("_id_factory", "_schema")

    _schema: StateSchema
    _id_factory: IdFactory

    def __init__(self, *, schema: StateSchema, id_factory: IdFactory) -> None:
        if not isinstance(schema, StateSchema):
            raise TypeError("schema должен быть StateSchema")
        if not callable(getattr(id_factory, "new_id", None)):
            raise TypeError("id_factory должен удовлетворять IdFactory")
        self._schema = schema
        self._id_factory = id_factory

    def commit(
        self,
        *,
        current_state: CognitiveState,
        update: BoundaryStateUpdate,
        logical_time: LogicalTime,
    ) -> BoundaryCommitResult:
        """Проверить staged update целиком и вернуть новую committed revision."""
        self._validate_base(
            current_state=current_state,
            update=update,
            logical_time=logical_time,
        )
        writes = self._validate_writes(
            update=update,
            logical_time=logical_time,
        )
        resulting_state = self._build_resulting_state(
            current_state=current_state,
            writes=writes,
            logical_time=logical_time,
        )
        record = BoundaryCommitRecord(
            commit_id=self._id_factory.new_id(CommitId),
            producer=update.producer,
            base_state_revision=update.base_state_revision,
            resulting_state_revision=resulting_state.envelope.state_revision,
            logical_time=logical_time,
            public_paths=tuple(write.key.path for write in writes),
        )
        return BoundaryCommitResult(state=resulting_state, record=record)

    def _validate_base(
        self,
        *,
        current_state: CognitiveState,
        update: BoundaryStateUpdate,
        logical_time: LogicalTime,
    ) -> None:
        if not isinstance(current_state, CognitiveState):
            raise TypeError("current_state должен быть CognitiveState")
        if not isinstance(update, BoundaryStateUpdate):
            raise TypeError("update должен быть BoundaryStateUpdate")
        if not isinstance(update.producer, RuntimeBoundaryId):
            raise TypeError("BoundaryStateUpdate producer должен быть RuntimeBoundaryId")
        if not isinstance(logical_time, LogicalTime):
            raise TypeError("logical_time должен быть LogicalTime")
        if current_state.envelope.schema_revision != self._schema.revision:
            raise CommitValidationError(
                "CognitiveState schema revision не совпадает с active StateSchema"
            )
        current_revision = current_state.envelope.state_revision
        if update.base_state_revision != current_revision:
            raise StaleProposalError(
                f"Boundary update ожидает revision {update.base_state_revision.value}, "
                f"current {current_revision.value}"
            )

        base_time = current_state.envelope.logical_time
        if base_time.run_id != logical_time.run_id:
            raise CommitValidationError("Boundary commit не может менять run_id base state")
        if base_time.agent_session_id != logical_time.agent_session_id:
            raise CommitValidationError(
                "Boundary commit не может менять agent_session_id base state"
            )

    def _validate_writes(
        self,
        *,
        update: BoundaryStateUpdate,
        logical_time: LogicalTime,
    ) -> tuple[BoundaryStateWrite[object], ...]:
        seen_paths: set[StatePath] = set()
        validated: list[BoundaryStateWrite[object]] = []
        if not update.writes:
            raise CommitValidationError("BoundaryStateUpdate не может быть пустым")
        for write in update.writes:
            if not isinstance(write, BoundaryStateWrite):
                raise TypeError("BoundaryStateUpdate содержит не BoundaryStateWrite")
            path = write.key.path
            if path in seen_paths:
                raise CommitValidationError(f"Duplicate/conflicting staged StatePath: {path}")
            seen_paths.add(path)
            spec = self._schema.lookup(path)
            if not isinstance(spec.owner, RuntimeBoundaryId) or spec.owner != update.producer:
                raise UnauthorizedWriteError(
                    f"Runtime boundary {update.producer} не является owner StatePath {path}"
                )
            self._validate_provenance(
                provenance=write.provenance,
                producer=update.producer,
                base_state_revision=update.base_state_revision,
                logical_time=logical_time,
            )
            availability = write.availability
            if isinstance(availability, Available | Stale):
                spec.value_contract.validate(availability.value)
            validated.append(write)
        return tuple(sorted(validated, key=lambda item: item.key.path.dotted))

    @staticmethod
    def _validate_provenance(
        *,
        provenance: StateProvenance,
        producer: RuntimeBoundaryId,
        base_state_revision: StateRevision,
        logical_time: LogicalTime,
    ) -> None:
        if not isinstance(provenance.producer, RuntimeBoundaryId):
            raise CommitValidationError(
                "BoundaryStateWrite provenance producer должен быть RuntimeBoundaryId"
            )
        if provenance.producer != producer:
            raise CommitValidationError(
                "BoundaryStateWrite provenance producer не совпадает с update producer"
            )
        if provenance.module_attempt_id is not None:
            raise CommitValidationError(
                "BoundaryStateWrite provenance не может содержать ModuleAttemptId"
            )
        if provenance.base_state_revision != base_state_revision:
            raise CommitValidationError(
                "BoundaryStateWrite provenance base revision не совпадает с update"
            )
        if provenance.logical_time != logical_time:
            raise CommitValidationError(
                "BoundaryStateWrite provenance logical_time не совпадает с commit logical_time"
            )

    def _build_resulting_state(
        self,
        *,
        current_state: CognitiveState,
        writes: tuple[BoundaryStateWrite[object], ...],
        logical_time: LogicalTime,
    ) -> CognitiveState:
        base_envelope = current_state.envelope
        envelope = StateEnvelope(
            schema_revision=base_envelope.schema_revision,
            state_revision=base_envelope.state_revision.next(),
            parent_state_revision=base_envelope.state_revision,
            lineage_id=base_envelope.lineage_id,
            branch_id=base_envelope.branch_id,
            agent_revision_id=base_envelope.agent_revision_id,
            logical_time=logical_time,
            composition_revision=base_envelope.composition_revision,
        )
        replacements: dict[StatePath, StateEntry[object]] = {
            write.key.path: StateEntry(
                availability=write.availability,
                provenance=write.provenance,
            )
            for write in writes
        }
        return copy_cognitive_state(
            base_state=current_state,
            schema=self._schema,
            envelope=envelope,
            replacements=replacements,
        )


__all__ = [
    "BoundaryCommitCoordinator",
    "BoundaryCommitRecord",
    "BoundaryCommitResult",
]
