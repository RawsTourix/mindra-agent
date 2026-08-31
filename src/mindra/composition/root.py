"""Единственная explicit production assembly boundary Core Kernel v0.1."""

import json
from hashlib import sha256

from mindra.composition.profile import KernelProfile, ModuleProfile
from mindra.composition.registry import ImplementationRegistry, ResolvedModule
from mindra.composition.runtime import (
    CompositionMetadata,
    KernelRuntime,
    _build_kernel_runtime,
)
from mindra.contracts import (
    AgentRevisionId,
    AgentSessionId,
    BranchId,
    CompositionResolvedEvent,
    CompositionRevision,
    ConfigurationError,
    DecisionWindowId,
    EpisodeId,
    ExecutionPlanRevision,
    IdFactory,
    InterventionPolicy,
    LineageId,
    LogicalTime,
    PlanCompiledEvent,
    PlanDependencyTrace,
    PlanWaveTrace,
    ResolvedModuleTrace,
    RunId,
    RuntimeBoundaryId,
    SchemaRevision,
    StateEntry,
    StateEnvelope,
    StatePath,
    StateProvenance,
    StateRevision,
    StateSchema,
    TraceEventEnvelope,
)
from mindra.runtime import (
    CognitiveScheduler,
    CommitCoordinator,
    ExecutionPlanCompiler,
    InMemoryEvidenceRecorder,
    InterventionGateway,
    PrivateStateStore,
    SequentialWaveExecutor,
    build_cognitive_state,
)


class CompositionRoot:
    """Resolve, validate и assemble kernel только из explicit dependencies."""

    __slots__ = ("_id_factory", "_intervention_policy", "_registry")

    def __init__(
        self,
        *,
        registry: ImplementationRegistry,
        id_factory: IdFactory,
        intervention_policy: InterventionPolicy | None = None,
    ) -> None:
        if not isinstance(registry, ImplementationRegistry):
            raise TypeError("registry должен быть ImplementationRegistry")
        if not callable(getattr(id_factory, "new_id", None)):
            raise TypeError("id_factory должен удовлетворять IdFactory")
        if intervention_policy is not None and not isinstance(
            intervention_policy, InterventionPolicy
        ):
            raise TypeError("intervention_policy должен быть InterventionPolicy или None")
        self._registry = registry
        self._id_factory = id_factory
        self._intervention_policy = (
            InterventionPolicy.disabled() if intervention_policy is None else intervention_policy
        )

    def build(self, profile: KernelProfile, /) -> KernelRuntime:
        """Fail closed собрать и instrument полностью готовую runtime composition."""
        if not isinstance(profile, KernelProfile):
            raise TypeError("profile должен быть KernelProfile")

        resolved = tuple(self._resolve_module(item) for item in profile.modules)
        modules = tuple(item.module for item in resolved)
        descriptors = tuple(item.module.descriptor for item in resolved)
        fields = tuple(field for item in resolved for field in item.state_fields)

        schema_revision = SchemaRevision.initial()
        composition_revision = CompositionRevision.initial()
        schema = StateSchema(schema_revision, (field.spec for field in fields))
        fingerprint = _composition_fingerprint(profile, resolved, schema_revision)

        run_id = self._id_factory.new_id(RunId)
        agent_session_id = self._id_factory.new_id(AgentSessionId)
        episode_id = self._id_factory.new_id(EpisodeId)
        decision_window_id = self._id_factory.new_id(DecisionWindowId)
        lineage_id = self._id_factory.new_id(LineageId)
        branch_id = self._id_factory.new_id(BranchId)
        agent_revision_id = self._id_factory.new_id(AgentRevisionId)
        root_time = LogicalTime(
            run_id=run_id,
            agent_session_id=agent_session_id,
            episode_id=episode_id,
            decision_window_id=decision_window_id,
        )

        provenance = StateProvenance(
            producer=RuntimeBoundaryId("composition.initial_state"),
            implementation_id=None,
            base_state_revision=StateRevision.initial(),
            module_attempt_id=None,
            logical_time=root_time,
            source_refs=(),
            parent_refs=(),
            intervention_refs=(),
        )
        entries: dict[StatePath, StateEntry[object]] = {
            field.spec.key.path: StateEntry[object](
                availability=field.initial_availability,
                provenance=provenance,
            )
            for field in fields
        }
        if set(entries) != set(schema.fields):
            raise ConfigurationError("Initial state fields не совпадают с active StateSchema")
        state = build_cognitive_state(
            schema=schema,
            envelope=StateEnvelope(
                schema_revision=schema_revision,
                state_revision=StateRevision.initial(),
                parent_state_revision=None,
                lineage_id=lineage_id,
                branch_id=branch_id,
                agent_revision_id=agent_revision_id,
                logical_time=root_time,
                composition_revision=composition_revision,
            ),
            entries=entries,
        )

        initial_private_values = {
            item.module.descriptor.module_id: item.initial_private_state.value
            for item in resolved
            if item.initial_private_state is not None
        }
        private_store = PrivateStateStore(descriptors, initial_private_values)
        plan = ExecutionPlanCompiler(self._id_factory).compile(
            descriptors,
            schema,
            composition_revision=composition_revision,
            plan_revision=ExecutionPlanRevision.initial(),
        )
        coordinator = CommitCoordinator(
            schema=schema,
            descriptors=descriptors,
            private_store=private_store,
            id_factory=self._id_factory,
        )
        executor = SequentialWaveExecutor()
        recorder = InMemoryEvidenceRecorder()
        intervention_gateway = InterventionGateway(
            schema=schema,
            policy=self._intervention_policy,
            evidence_recorder=recorder,
            id_factory=self._id_factory,
        )
        scheduler = CognitiveScheduler(
            plan=plan,
            modules=modules,
            private_store=private_store,
            commit_coordinator=coordinator,
            wave_executor=executor,
            evidence_recorder=recorder,
            id_factory=self._id_factory,
        )
        composition = CompositionMetadata(
            profile_id=profile.profile_id,
            composition_revision=composition_revision,
            schema_revision=schema_revision,
            agent_revision_id=agent_revision_id,
            fingerprint=fingerprint,
            descriptors=descriptors,
        )
        runtime = _build_kernel_runtime(
            profile=profile,
            composition=composition,
            plan=plan,
            state=state,
            private_store=private_store,
            scheduler=scheduler,
            evidence_recorder=recorder,
            id_factory=self._id_factory,
            root_time=root_time,
            intervention_gateway=intervention_gateway,
        )

        recorder.record(
            TraceEventEnvelope(
                logical_time=root_time,
                payload=CompositionResolvedEvent(
                    profile_id=profile.profile_id,
                    composition_revision=composition_revision,
                    schema_revision=schema_revision,
                    agent_revision_id=agent_revision_id,
                    composition_fingerprint=fingerprint,
                    modules=tuple(
                        ResolvedModuleTrace(
                            module_id=descriptor.module_id,
                            implementation_id=descriptor.implementation_id,
                            implementation_revision=descriptor.implementation_revision,
                            statefulness=descriptor.traits.statefulness,
                            determinism=descriptor.traits.determinism,
                        )
                        for descriptor in descriptors
                    ),
                ),
                physical_timestamp_ns=None,
            )
        )
        recorder.record(
            TraceEventEnvelope(
                logical_time=root_time,
                payload=PlanCompiledEvent(
                    plan_id=plan.plan_id,
                    plan_revision=plan.revision,
                    composition_revision=plan.composition_revision,
                    schema_revision=plan.schema_revision,
                    phase=plan.phase,
                    plan_fingerprint=plan.fingerprint.value,
                    dependencies=tuple(
                        PlanDependencyTrace(
                            producer=dependency.producer,
                            consumer=dependency.consumer,
                            path=dependency.path,
                        )
                        for dependency in plan.dependencies
                    ),
                    waves=tuple(
                        PlanWaveTrace(index=wave.index, module_ids=wave.module_ids)
                        for wave in plan.waves
                    ),
                ),
                physical_timestamp_ns=None,
            )
        )
        return runtime

    def _resolve_module(self, profile: ModuleProfile) -> ResolvedModule:
        descriptor = self._registry.resolve(profile.implementation_id)
        resolved = descriptor.factory(profile)
        if not isinstance(resolved, ResolvedModule):
            raise ConfigurationError("Implementation factory должна вернуть ResolvedModule")
        module_descriptor = resolved.module.descriptor
        if module_descriptor.module_id != profile.module_id:
            raise ConfigurationError("Resolved module_id не совпадает с ModuleProfile")
        if module_descriptor.implementation_id != descriptor.implementation_id:
            raise ConfigurationError(
                "Resolved implementation_id не совпадает с registry descriptor"
            )
        if profile.implementation_id != descriptor.implementation_id:
            raise ConfigurationError("Profile implementation_id не совпадает с registry descriptor")
        return resolved


def _composition_fingerprint(
    profile: KernelProfile,
    resolved: tuple[ResolvedModule, ...],
    schema_revision: SchemaRevision,
) -> str:
    normalized = {
        "profile_schema": profile.schema,
        "state_schema_revision": schema_revision.value,
        "modules": [
            {
                "module_id": item.module.descriptor.module_id.value,
                "implementation_id": item.module.descriptor.implementation_id.value,
                "implementation_revision": item.module.descriptor.implementation_revision.value,
                "settings": dict(item.resolved_settings),
            }
            for item in resolved
        ],
    }
    serialized = json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return sha256(serialized.encode("utf-8")).hexdigest()


__all__ = ["CompositionRoot"]
