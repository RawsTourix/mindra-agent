"""Deterministic compilation immutable execution plans Core Kernel."""

import json
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from re import compile as compile_pattern
from uuid import UUID

from mindra.contracts.availability import Available, Stale, Unavailable, Unknown
from mindra.contracts.errors import (
    DependencyCycleError,
    DuplicateIdentityError,
    ExecutionPlanError,
    MissingFieldError,
)
from mindra.contracts.identity import ExecutionPlanId, IdFactory, ModuleId
from mindra.contracts.modules import ExecutionPhase, ModuleDescriptor
from mindra.contracts.revisions import CompositionRevision, ExecutionPlanRevision, SchemaRevision
from mindra.contracts.state import FreshnessMode, StateFieldSpec, StatePath, StateSchema

_FINGERPRINT_PATTERN = compile_pattern(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class PlanFingerprint:
    """Stable SHA-256 fingerprint structural execution semantics."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("PlanFingerprint value должен быть строкой")
        if _FINGERPRINT_PATTERN.fullmatch(self.value) is None:
            raise ValueError("PlanFingerprint должен быть lowercase SHA-256 hex")


@dataclass(frozen=True, slots=True)
class ExecutionDependency:
    """Explicit same-cycle producer-consumer edge for one StatePath."""

    producer: ModuleId
    consumer: ModuleId
    path: StatePath

    def __post_init__(self) -> None:
        if not isinstance(self.producer, ModuleId):
            raise TypeError("producer должен быть ModuleId")
        if not isinstance(self.consumer, ModuleId):
            raise TypeError("consumer должен быть ModuleId")
        if not isinstance(self.path, StatePath):
            raise TypeError("path должен быть StatePath")


@dataclass(frozen=True, slots=True)
class ExecutionWave:
    """Canonical topological generation static execution plan."""

    index: int
    module_ids: tuple[ModuleId, ...]

    def __post_init__(self) -> None:
        if type(self.index) is not int:
            raise TypeError("ExecutionWave index должен быть целым числом")
        if self.index < 0:
            raise ValueError("ExecutionWave index не может быть отрицательным")
        if not isinstance(self.module_ids, tuple):
            raise TypeError("module_ids должен быть tuple ModuleId")
        if not self.module_ids:
            raise ValueError("ExecutionWave module_ids не может быть пустым")
        if any(not isinstance(module_id, ModuleId) for module_id in self.module_ids):
            raise TypeError("module_ids должен содержать ModuleId")
        if len(set(self.module_ids)) != len(self.module_ids):
            raise ValueError("ExecutionWave не может содержать duplicate ModuleId")
        if self.module_ids != tuple(sorted(self.module_ids, key=lambda item: item.value)):
            raise ValueError("ExecutionWave module_ids должны иметь canonical order")


@dataclass(frozen=True, slots=True, init=False)
class ExecutionPlan:
    """Immutable compiler-controlled plan одного cognitive-cycle segment."""

    plan_id: ExecutionPlanId
    revision: ExecutionPlanRevision
    fingerprint: PlanFingerprint
    composition_revision: CompositionRevision
    schema_revision: SchemaRevision
    phase: ExecutionPhase
    descriptors: tuple[ModuleDescriptor, ...]
    dependencies: tuple[ExecutionDependency, ...]
    waves: tuple[ExecutionWave, ...]

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise TypeError("ExecutionPlan создаётся только ExecutionPlanCompiler")


class ExecutionPlanCompiler:
    """Stateless compiler declared contracts в deterministic execution DAG."""

    __slots__ = ("_id_factory",)

    def __init__(self, id_factory: IdFactory) -> None:
        self._id_factory = id_factory

    def compile(
        self,
        descriptors: tuple[ModuleDescriptor, ...],
        schema: StateSchema,
        *,
        composition_revision: CompositionRevision,
        plan_revision: ExecutionPlanRevision,
    ) -> ExecutionPlan:
        """Validate descriptors and compile one immutable cognitive-cycle plan."""
        if not isinstance(descriptors, tuple):
            raise TypeError("descriptors должен быть tuple ModuleDescriptor")
        if not isinstance(schema, StateSchema):
            raise TypeError("schema должна быть StateSchema")
        if not isinstance(composition_revision, CompositionRevision):
            raise TypeError("composition_revision должна быть CompositionRevision")
        if not isinstance(plan_revision, ExecutionPlanRevision):
            raise TypeError("plan_revision должна быть ExecutionPlanRevision")

        canonical_descriptors = _validate_descriptors(descriptors, schema)
        dependencies = _build_dependencies(canonical_descriptors)
        waves = _decompose_waves(canonical_descriptors, dependencies)
        fingerprint = _build_fingerprint(canonical_descriptors, dependencies, waves)
        plan_id = self._id_factory.new_id(ExecutionPlanId)
        return _build_execution_plan(
            plan_id=plan_id,
            revision=plan_revision,
            fingerprint=fingerprint,
            composition_revision=composition_revision,
            schema_revision=schema.revision,
            phase=ExecutionPhase.COGNITIVE_CYCLE,
            descriptors=canonical_descriptors,
            dependencies=dependencies,
            waves=waves,
        )


def _build_execution_plan(
    *,
    plan_id: ExecutionPlanId,
    revision: ExecutionPlanRevision,
    fingerprint: PlanFingerprint,
    composition_revision: CompositionRevision,
    schema_revision: SchemaRevision,
    phase: ExecutionPhase,
    descriptors: tuple[ModuleDescriptor, ...],
    dependencies: tuple[ExecutionDependency, ...],
    waves: tuple[ExecutionWave, ...],
) -> ExecutionPlan:
    """Construct a plan only after compiler-established validation."""
    plan = object.__new__(ExecutionPlan)
    object.__setattr__(plan, "plan_id", plan_id)
    object.__setattr__(plan, "revision", revision)
    object.__setattr__(plan, "fingerprint", fingerprint)
    object.__setattr__(plan, "composition_revision", composition_revision)
    object.__setattr__(plan, "schema_revision", schema_revision)
    object.__setattr__(plan, "phase", phase)
    object.__setattr__(plan, "descriptors", descriptors)
    object.__setattr__(plan, "dependencies", dependencies)
    object.__setattr__(plan, "waves", waves)
    _validate_execution_plan_shape(plan)
    return plan


def _validate_execution_plan_shape(plan: ExecutionPlan) -> None:
    if not isinstance(plan.plan_id, UUID):
        raise TypeError("plan_id должен быть ExecutionPlanId")
    if not isinstance(plan.revision, ExecutionPlanRevision):
        raise TypeError("revision должен быть ExecutionPlanRevision")
    if not isinstance(plan.fingerprint, PlanFingerprint):
        raise TypeError("fingerprint должен быть PlanFingerprint")
    if not isinstance(plan.composition_revision, CompositionRevision):
        raise TypeError("composition_revision должен быть CompositionRevision")
    if not isinstance(plan.schema_revision, SchemaRevision):
        raise TypeError("schema_revision должен быть SchemaRevision")
    if plan.phase is not ExecutionPhase.COGNITIVE_CYCLE:
        raise ValueError("v0.1 ExecutionPlan поддерживает только COGNITIVE_CYCLE")
    if not isinstance(plan.descriptors, tuple) or any(
        not isinstance(descriptor, ModuleDescriptor) for descriptor in plan.descriptors
    ):
        raise TypeError("descriptors должен быть tuple ModuleDescriptor")
    if plan.descriptors != tuple(
        sorted(plan.descriptors, key=lambda descriptor: descriptor.module_id.value)
    ):
        raise ValueError("ExecutionPlan descriptors должны иметь canonical order")
    if not isinstance(plan.dependencies, tuple) or any(
        not isinstance(dependency, ExecutionDependency) for dependency in plan.dependencies
    ):
        raise TypeError("dependencies должен быть tuple ExecutionDependency")
    if plan.dependencies != tuple(sorted(plan.dependencies, key=_dependency_key)):
        raise ValueError("ExecutionPlan dependencies должны иметь canonical order")
    if not isinstance(plan.waves, tuple) or any(
        not isinstance(wave, ExecutionWave) for wave in plan.waves
    ):
        raise TypeError("waves должен быть tuple ExecutionWave")
    if tuple(wave.index for wave in plan.waves) != tuple(range(len(plan.waves))):
        raise ValueError("ExecutionPlan wave indices должны идти с 0 без gaps")

    descriptor_ids = tuple(descriptor.module_id for descriptor in plan.descriptors)
    wave_ids = tuple(module_id for wave in plan.waves for module_id in wave.module_ids)
    if len(set(descriptor_ids)) != len(descriptor_ids):
        raise ValueError("ExecutionPlan descriptors содержат duplicate ModuleId")
    if len(wave_ids) != len(set(wave_ids)) or set(wave_ids) != set(descriptor_ids):
        raise ValueError("Каждый active ModuleId должен входить ровно в одну wave")


def _validate_descriptors(
    descriptors: tuple[ModuleDescriptor, ...], schema: StateSchema
) -> tuple[ModuleDescriptor, ...]:
    for descriptor in descriptors:
        if not isinstance(descriptor, ModuleDescriptor):
            raise TypeError("descriptors должен содержать ModuleDescriptor")

    module_ids = [descriptor.module_id for descriptor in descriptors]
    if len(set(module_ids)) != len(module_ids):
        raise DuplicateIdentityError("Duplicate active ModuleId в execution plan")

    writers: dict[StatePath, ModuleId] = {}
    for descriptor in descriptors:
        if ExecutionPhase.COGNITIVE_CYCLE not in descriptor.phases:
            raise ExecutionPlanError(
                f"Module {descriptor.module_id} не участвует в COGNITIVE_CYCLE"
            )
        for read in descriptor.reads:
            _lookup_plan_field(schema, read.key.path, "read")
        for write in descriptor.writes:
            spec = _lookup_plan_field(schema, write.path, "write")
            existing_writer = writers.get(write.path)
            if existing_writer is not None:
                raise ExecutionPlanError(
                    f"Ambiguous active writers StatePath {write.path}: "
                    f"{existing_writer}, {descriptor.module_id}"
                )
            writers[write.path] = descriptor.module_id
            if spec.owner != descriptor.module_id:
                raise ExecutionPlanError(
                    f"Module {descriptor.module_id} не владеет declared write {write.path}"
                )

    for descriptor in descriptors:
        for read in descriptor.reads:
            if (
                read.freshness is FreshnessMode.CURRENT_CYCLE
                and read.required
                and read.key.path not in writers
            ):
                raise ExecutionPlanError(
                    f"Required CURRENT_CYCLE read {read.key.path} module "
                    f"{descriptor.module_id} не имеет active producer"
                )

    return tuple(sorted(descriptors, key=lambda descriptor: descriptor.module_id.value))


def _lookup_plan_field(
    schema: StateSchema, path: StatePath, operation: str
) -> StateFieldSpec[object]:
    try:
        return schema.lookup(path)
    except MissingFieldError as error:
        raise ExecutionPlanError(
            f"Declared {operation} StatePath отсутствует в schema: {path}"
        ) from error


def _build_dependencies(
    descriptors: tuple[ModuleDescriptor, ...],
) -> tuple[ExecutionDependency, ...]:
    writers = {
        write.path: descriptor.module_id
        for descriptor in descriptors
        for write in descriptor.writes
    }
    dependencies = tuple(
        ExecutionDependency(
            producer=writers[read.key.path],
            consumer=descriptor.module_id,
            path=read.key.path,
        )
        for descriptor in descriptors
        for read in descriptor.reads
        if read.freshness is FreshnessMode.CURRENT_CYCLE and read.key.path in writers
    )
    return tuple(sorted(dependencies, key=_dependency_key))


def _decompose_waves(
    descriptors: tuple[ModuleDescriptor, ...],
    dependencies: tuple[ExecutionDependency, ...],
) -> tuple[ExecutionWave, ...]:
    module_ids = {descriptor.module_id for descriptor in descriptors}
    predecessors: dict[ModuleId, set[ModuleId]] = {module_id: set() for module_id in module_ids}
    successors: dict[ModuleId, set[ModuleId]] = {module_id: set() for module_id in module_ids}
    for dependency in dependencies:
        predecessors[dependency.consumer].add(dependency.producer)
        successors[dependency.producer].add(dependency.consumer)

    remaining = set(module_ids)
    waves: list[ExecutionWave] = []
    while remaining:
        ready = tuple(
            sorted(
                (module_id for module_id in remaining if not predecessors[module_id]),
                key=lambda module_id: module_id.value,
            )
        )
        if not ready:
            cycle_members = ", ".join(sorted(module_id.value for module_id in remaining))
            raise DependencyCycleError(
                f"Instantaneous CURRENT_CYCLE dependency cycle: {cycle_members}"
            )
        waves.append(ExecutionWave(index=len(waves), module_ids=ready))
        for producer in ready:
            remaining.remove(producer)
            for consumer in successors[producer]:
                predecessors[consumer].remove(producer)

    return tuple(waves)


def _build_fingerprint(
    descriptors: tuple[ModuleDescriptor, ...],
    dependencies: tuple[ExecutionDependency, ...],
    waves: tuple[ExecutionWave, ...],
) -> PlanFingerprint:
    payload = {
        "phase": ExecutionPhase.COGNITIVE_CYCLE.value,
        "descriptors": [_descriptor_payload(descriptor) for descriptor in descriptors],
        "dependencies": [
            {
                "producer": dependency.producer.value,
                "consumer": dependency.consumer.value,
                "path": dependency.path.dotted,
            }
            for dependency in dependencies
        ],
        "waves": [
            {
                "index": wave.index,
                "module_ids": [module_id.value for module_id in wave.module_ids],
            }
            for wave in waves
        ],
    }
    canonical_bytes = json.dumps(
        payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return PlanFingerprint(sha256(canonical_bytes).hexdigest())


def _descriptor_payload(descriptor: ModuleDescriptor) -> Mapping[str, object]:
    reads = sorted(
        (
            {
                "path": read.key.path.dotted,
                "required": read.required,
                "allowed_availability": sorted(
                    _availability_name(variant) for variant in read.allowed_availability
                ),
                "freshness": read.freshness.value,
            }
            for read in descriptor.reads
        ),
        key=lambda item: str(item["path"]),
    )
    return {
        "module_id": descriptor.module_id.value,
        "implementation_id": descriptor.implementation_id.value,
        "implementation_revision": descriptor.implementation_revision.value,
        "reads": reads,
        "writes": sorted(write.path.dotted for write in descriptor.writes),
        "traits": {
            "statefulness": descriptor.traits.statefulness.value,
            "determinism": descriptor.traits.determinism.value,
        },
        "has_private_state": descriptor.private_state is not None,
        "phases": sorted(phase.value for phase in descriptor.phases),
    }


def _dependency_key(dependency: ExecutionDependency) -> tuple[str, str, str]:
    return (
        dependency.producer.value,
        dependency.consumer.value,
        dependency.path.dotted,
    )


def _availability_name(variant: type[object]) -> str:
    if variant is Available:
        return "available"
    if variant is Unknown:
        return "unknown"
    if variant is Stale:
        return "stale"
    if variant is Unavailable:
        return "unavailable"
    raise ExecutionPlanError("ReadSpec содержит unknown availability variant")


__all__ = [
    "ExecutionDependency",
    "ExecutionPlan",
    "ExecutionPlanCompiler",
    "ExecutionWave",
    "PlanFingerprint",
]
