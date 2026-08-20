"""Единственная runtime boundary атомарной публикации staged module effects."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from uuid import UUID

from mindra.contracts.errors import (
    CommitValidationError,
    DuplicateIdentityError,
    StaleProposalError,
    UnauthorizedWriteError,
)
from mindra.contracts.identity import CommitId, IdFactory, ModuleAttemptId, ModuleId
from mindra.contracts.modules import (
    ExecutionPhase,
    ModuleComputeResult,
    ModuleDescriptor,
    StateWrite,
)
from mindra.contracts.revisions import PrivateStateRevision, StateRevision
from mindra.contracts.state import (
    CognitiveState,
    StateEntry,
    StateEnvelope,
    StatePath,
    StateSchema,
)
from mindra.contracts.time import LogicalTime
from mindra.runtime.private_state import (
    PrivateStateStore,
    _PreparedPrivateStateUpdate,
)
from mindra.runtime.state_store import copy_cognitive_state


@dataclass(frozen=True, slots=True)
class PrivateStateRevisionTransition:
    """Изменение revision одного фактически committed private slot."""

    module_id: ModuleId
    before: PrivateStateRevision
    after: PrivateStateRevision

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        if not isinstance(self.before, PrivateStateRevision):
            raise TypeError("before должен быть PrivateStateRevision")
        if not isinstance(self.after, PrivateStateRevision):
            raise TypeError("after должен быть PrivateStateRevision")
        if self.after != self.before.next():
            raise CommitValidationError(
                "Committed private transition должен увеличивать revision ровно на один"
            )


@dataclass(frozen=True, slots=True)
class CommitRecord:
    """Immutable structural record одной successful commit transaction."""

    commit_id: CommitId
    base_state_revision: StateRevision
    resulting_state_revision: StateRevision
    logical_time: LogicalTime
    module_attempt_ids: tuple[ModuleAttemptId, ...]
    public_paths: tuple[StatePath, ...]
    private_revisions: tuple[PrivateStateRevisionTransition, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.commit_id, UUID):
            raise TypeError("commit_id должен быть CommitId")
        if not isinstance(self.base_state_revision, StateRevision):
            raise TypeError("base_state_revision должен быть StateRevision")
        if not isinstance(self.resulting_state_revision, StateRevision):
            raise TypeError("resulting_state_revision должен быть StateRevision")
        if not isinstance(self.logical_time, LogicalTime):
            raise TypeError("logical_time должен быть LogicalTime")
        if not isinstance(self.module_attempt_ids, tuple) or any(
            not isinstance(attempt_id, UUID) for attempt_id in self.module_attempt_ids
        ):
            raise TypeError("module_attempt_ids должен быть tuple ModuleAttemptId")
        if len(set(self.module_attempt_ids)) != len(self.module_attempt_ids):
            raise CommitValidationError("CommitRecord содержит duplicate ModuleAttemptId")
        if not isinstance(self.public_paths, tuple) or any(
            not isinstance(path, StatePath) for path in self.public_paths
        ):
            raise TypeError("public_paths должен быть tuple StatePath")
        if self.public_paths != tuple(sorted(set(self.public_paths), key=lambda path: path.dotted)):
            raise CommitValidationError("public_paths должен иметь canonical unique ordering")
        if not isinstance(self.private_revisions, tuple) or any(
            not isinstance(transition, PrivateStateRevisionTransition)
            for transition in self.private_revisions
        ):
            raise TypeError("private_revisions должен быть tuple PrivateStateRevisionTransition")
        private_module_ids = tuple(transition.module_id for transition in self.private_revisions)
        canonical_private_module_ids = tuple(
            sorted(set(private_module_ids), key=lambda item: item.value)
        )
        if private_module_ids != canonical_private_module_ids:
            raise CommitValidationError(
                "private_revisions должен иметь canonical unique ModuleId ordering"
            )

        expected_revision = (
            self.base_state_revision.next() if self.public_paths else self.base_state_revision
        )
        if self.resulting_state_revision != expected_revision:
            raise CommitValidationError(
                "Resulting StateRevision не согласована с наличием public writes"
            )


@dataclass(frozen=True, slots=True)
class CommitResult:
    """Успешно опубликованный public state и его structural commit record."""

    state: CognitiveState
    record: CommitRecord

    def __post_init__(self) -> None:
        if not isinstance(self.state, CognitiveState):
            raise TypeError("state должен быть CognitiveState")
        if not isinstance(self.record, CommitRecord):
            raise TypeError("record должен быть CommitRecord")
        if self.state.envelope.state_revision != self.record.resulting_state_revision:
            raise CommitValidationError("CommitResult state revision не согласована с CommitRecord")


class CommitCoordinator:
    """Validate и атомарно публикует одну transaction staged results."""

    __slots__ = ("_descriptors", "_id_factory", "_private_store", "_schema")

    _schema: StateSchema
    _descriptors: Mapping[ModuleId, ModuleDescriptor]
    _private_store: PrivateStateStore
    _id_factory: IdFactory

    def __init__(
        self,
        *,
        schema: StateSchema,
        descriptors: tuple[ModuleDescriptor, ...],
        private_store: PrivateStateStore,
        id_factory: IdFactory,
    ) -> None:
        if not isinstance(schema, StateSchema):
            raise TypeError("schema должен быть StateSchema")
        if not isinstance(descriptors, tuple):
            raise TypeError("descriptors должен быть tuple ModuleDescriptor")
        if not isinstance(private_store, PrivateStateStore):
            raise TypeError("private_store должен быть PrivateStateStore")
        if not callable(getattr(id_factory, "new_id", None)):
            raise TypeError("id_factory должен удовлетворять IdFactory")

        registered: dict[ModuleId, ModuleDescriptor] = {}
        for descriptor in descriptors:
            if not isinstance(descriptor, ModuleDescriptor):
                raise TypeError("descriptors должен содержать ModuleDescriptor")
            if descriptor.module_id in registered:
                raise DuplicateIdentityError(
                    f"Duplicate active ModuleId commit coordinator: {descriptor.module_id}"
                )
            registered[descriptor.module_id] = descriptor

        self._schema = schema
        self._descriptors = MappingProxyType(registered)
        self._private_store = private_store
        self._id_factory = id_factory

    def commit(
        self,
        *,
        current_state: CognitiveState,
        results: tuple[ModuleComputeResult, ...],
        logical_time: LogicalTime,
    ) -> CommitResult:
        """Validate transaction целиком и опубликовать все private effects atomically."""
        self._validate_base(current_state=current_state, logical_time=logical_time)
        canonical_results = self._canonicalize_results(
            current_state=current_state,
            results=results,
        )
        public_writes = self._validate_public_writes(
            current_state=current_state,
            results=canonical_results,
            logical_time=logical_time,
        )
        prepared_private = self._prepare_private(canonical_results)
        resulting_state = self._build_resulting_state(
            current_state=current_state,
            public_writes=public_writes,
            logical_time=logical_time,
        )
        private_revisions = tuple(
            PrivateStateRevisionTransition(
                module_id=update.module_id,
                before=update.expected_revision,
                after=update.next_revision,
            )
            for update in sorted(prepared_private, key=lambda item: item.module_id.value)
        )
        commit_id = self._id_factory.new_id(CommitId)
        record = CommitRecord(
            commit_id=commit_id,
            base_state_revision=current_state.envelope.state_revision,
            resulting_state_revision=resulting_state.envelope.state_revision,
            logical_time=logical_time,
            module_attempt_ids=tuple(
                result.state_update.module_attempt_id for result in canonical_results
            ),
            public_paths=tuple(write.key.path for write in public_writes),
            private_revisions=private_revisions,
        )
        result = CommitResult(state=resulting_state, record=record)

        self._private_store._apply_prepared(prepared_private)
        return result

    def _validate_base(
        self,
        *,
        current_state: CognitiveState,
        logical_time: LogicalTime,
    ) -> None:
        if not isinstance(current_state, CognitiveState):
            raise TypeError("current_state должен быть CognitiveState")
        if not isinstance(logical_time, LogicalTime):
            raise TypeError("logical_time должен быть LogicalTime")
        if current_state.envelope.schema_revision != self._schema.revision:
            raise CommitValidationError(
                "CognitiveState schema revision не совпадает с active StateSchema"
            )

        base_time = current_state.envelope.logical_time
        if base_time.run_id != logical_time.run_id:
            raise CommitValidationError("Commit не может менять run_id base state")
        if base_time.agent_session_id != logical_time.agent_session_id:
            raise CommitValidationError("Commit не может менять agent_session_id base state")
        for field_name in ("episode_id", "decision_window_id", "cognitive_cycle_id"):
            base_value = getattr(base_time, field_name)
            if base_value is not None and base_value != getattr(logical_time, field_name):
                raise CommitValidationError(f"Commit logical time несовместим с base {field_name}")

    def _canonicalize_results(
        self,
        *,
        current_state: CognitiveState,
        results: tuple[ModuleComputeResult, ...],
    ) -> tuple[ModuleComputeResult, ...]:
        if not isinstance(results, tuple):
            raise TypeError("results должен быть tuple ModuleComputeResult")

        producers: set[ModuleId] = set()
        attempts: set[ModuleAttemptId] = set()
        for result in results:
            if not isinstance(result, ModuleComputeResult):
                raise TypeError("results должен содержать ModuleComputeResult")
            proposal = result.state_update
            producer = proposal.producer
            descriptor = self._descriptors.get(producer)
            if descriptor is None:
                raise CommitValidationError(
                    f"Result producer не зарегистрирован в active composition: {producer}"
                )
            if producer in producers:
                raise CommitValidationError(f"Duplicate result producer в transaction: {producer}")
            producers.add(producer)
            if proposal.module_attempt_id in attempts:
                raise CommitValidationError("Duplicate ModuleAttemptId в commit transaction")
            attempts.add(proposal.module_attempt_id)
            if proposal.base_state_revision != current_state.envelope.state_revision:
                raise StaleProposalError(
                    f"Public proposal producer {producer} ожидает revision "
                    f"{proposal.base_state_revision.value}, current "
                    f"{current_state.envelope.state_revision.value}"
                )
            if ExecutionPhase.COGNITIVE_CYCLE not in descriptor.phases:
                raise CommitValidationError(f"Producer не участвует в COGNITIVE_CYCLE: {producer}")

            private_proposal = result.private_state_update
            if private_proposal is not None:
                if private_proposal.module_id != producer:
                    raise CommitValidationError(
                        "Private proposal module_id не совпадает с public producer"
                    )
                if private_proposal.module_attempt_id != proposal.module_attempt_id:
                    raise CommitValidationError(
                        "Private proposal ModuleAttemptId не совпадает с public proposal"
                    )

        return tuple(sorted(results, key=lambda item: item.state_update.producer.value))

    def _validate_public_writes(
        self,
        *,
        current_state: CognitiveState,
        results: tuple[ModuleComputeResult, ...],
        logical_time: LogicalTime,
    ) -> tuple[StateWrite[object], ...]:
        seen_paths: set[StatePath] = set()
        validated: list[StateWrite[object]] = []
        current_revision = current_state.envelope.state_revision

        for result in results:
            proposal = result.state_update
            descriptor = self._descriptors[proposal.producer]
            declared_paths = {key.path for key in descriptor.writes}
            for write in proposal.writes:
                path = write.key.path
                spec = self._schema.lookup(path)
                if spec.owner != proposal.producer:
                    raise UnauthorizedWriteError(
                        f"Producer {proposal.producer} не является owner StatePath {path}"
                    )
                if path not in declared_paths:
                    raise UnauthorizedWriteError(
                        f"StatePath {path} не объявлен в descriptor.writes producer "
                        f"{proposal.producer}"
                    )
                if path in seen_paths:
                    raise CommitValidationError(f"Duplicate/conflicting staged StatePath: {path}")
                seen_paths.add(path)
                self._validate_provenance(
                    write=write,
                    descriptor=descriptor,
                    producer=proposal.producer,
                    module_attempt_id=proposal.module_attempt_id,
                    current_revision=current_revision,
                    logical_time=logical_time,
                )
                validated.append(write)

        return tuple(sorted(validated, key=lambda item: item.key.path.dotted))

    @staticmethod
    def _validate_provenance(
        *,
        write: StateWrite[object],
        descriptor: ModuleDescriptor,
        producer: ModuleId,
        module_attempt_id: ModuleAttemptId,
        current_revision: StateRevision,
        logical_time: LogicalTime,
    ) -> None:
        provenance = write.provenance
        if not isinstance(provenance.producer, ModuleId) or provenance.producer != producer:
            raise CommitValidationError(
                "StateWrite provenance producer не совпадает с proposal producer"
            )
        if provenance.implementation_id != descriptor.implementation_id:
            raise CommitValidationError(
                "StateWrite provenance implementation_id не совпадает с active descriptor"
            )
        if provenance.base_state_revision != current_revision:
            raise CommitValidationError(
                "StateWrite provenance base revision не совпадает с current state"
            )
        if provenance.module_attempt_id != module_attempt_id:
            raise CommitValidationError(
                "StateWrite provenance ModuleAttemptId не совпадает с proposal"
            )
        if provenance.logical_time != logical_time:
            raise CommitValidationError(
                "StateWrite provenance logical_time не совпадает с commit logical_time"
            )

    def _prepare_private(
        self,
        results: tuple[ModuleComputeResult, ...],
    ) -> tuple[_PreparedPrivateStateUpdate, ...]:
        return tuple(
            self._private_store._prepare(private_proposal)
            for result in results
            if (private_proposal := result.private_state_update) is not None
        )

    def _build_resulting_state(
        self,
        *,
        current_state: CognitiveState,
        public_writes: tuple[StateWrite[object], ...],
        logical_time: LogicalTime,
    ) -> CognitiveState:
        if not public_writes:
            return current_state

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
            for write in public_writes
        }
        return copy_cognitive_state(
            base_state=current_state,
            schema=self._schema,
            envelope=envelope,
            replacements=replacements,
        )


__all__ = [
    "CommitCoordinator",
    "CommitRecord",
    "CommitResult",
    "PrivateStateRevisionTransition",
]
