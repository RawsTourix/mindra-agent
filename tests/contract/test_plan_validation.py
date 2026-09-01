"""Fail-closed contract checks execution plan compilation."""

from typing import cast
from uuid import UUID

import pytest

from mindra.contracts import (
    Available,
    CompositionRevision,
    DependencyCycleError,
    DeterminismMode,
    DuplicateIdentityError,
    ExecutionPhase,
    ExecutionPlanError,
    ExecutionPlanRevision,
    ExecutionTraits,
    FreshnessMode,
    IdFactory,
    ImplementationId,
    ImplementationRevision,
    ModuleDescriptor,
    ModuleId,
    ModuleStatefulness,
    ReadSpec,
    SchemaRevision,
    StateFieldSpec,
    StateKey,
    StatePath,
    StateSchema,
    ValueContract,
)
from mindra.runtime import DeterministicIdFactory, ExecutionPlan, ExecutionPlanCompiler

NAMESPACE = UUID("98cdd85f-ff03-4455-87bc-b9bba3b008a9")


def _key(name: str) -> StateKey[int]:
    return StateKey(StatePath.from_dotted(f"{name}.value"))


def _read(
    name: str,
    *,
    required: bool = True,
    freshness: FreshnessMode = FreshnessMode.CURRENT_CYCLE,
) -> ReadSpec[object]:
    return cast(
        ReadSpec[object],
        ReadSpec(
            key=_key(name),
            required=required,
            allowed_availability=frozenset({Available}),
            freshness=freshness,
        ),
    )


def _descriptor(
    name: str,
    *,
    reads: tuple[ReadSpec[object], ...] = (),
    writes: tuple[str, ...] = (),
) -> ModuleDescriptor:
    return ModuleDescriptor(
        module_id=ModuleId(name),
        implementation_id=ImplementationId(f"reference.{name}.v1"),
        implementation_revision=ImplementationRevision("v1"),
        reads=reads,
        writes=tuple(cast(StateKey[object], _key(writer)) for writer in writes),
        private_state=None,
        phases=frozenset({ExecutionPhase.COGNITIVE_CYCLE}),
        traits=ExecutionTraits(
            statefulness=ModuleStatefulness.STATELESS,
            determinism=DeterminismMode.DETERMINISTIC,
        ),
    )


def _schema(*owner_paths: tuple[str, str]) -> StateSchema:
    return StateSchema(
        SchemaRevision.initial(),
        tuple(
            cast(
                StateFieldSpec[object],
                StateFieldSpec(
                    key=_key(path),
                    owner=ModuleId(owner),
                    value_contract=ValueContract(int),
                ),
            )
            for path, owner in owner_paths
        ),
    )


def _compile(
    descriptors: tuple[ModuleDescriptor, ...],
    schema: StateSchema,
    factory: IdFactory | None = None,
) -> ExecutionPlan:
    id_factory = factory or DeterministicIdFactory(NAMESPACE, "validation")
    return ExecutionPlanCompiler(id_factory).compile(
        descriptors,
        schema,
        composition_revision=CompositionRevision.initial(),
        plan_revision=ExecutionPlanRevision.initial(),
    )


def test_duplicate_module_id_is_rejected() -> None:
    descriptor = _descriptor("alpha")

    with pytest.raises(DuplicateIdentityError):
        _compile((descriptor, descriptor), _schema())


def test_missing_read_path_is_rejected() -> None:
    with pytest.raises(ExecutionPlanError, match="read StatePath"):
        _compile((_descriptor("consumer", reads=(_read("missing"),)),), _schema())


def test_missing_write_path_is_rejected() -> None:
    with pytest.raises(ExecutionPlanError, match="write StatePath"):
        _compile((_descriptor("writer", writes=("missing",)),), _schema())


def test_writer_must_equal_schema_owner() -> None:
    with pytest.raises(ExecutionPlanError, match="не владеет"):
        _compile(
            (_descriptor("intruder", writes=("owned",)),),
            _schema(("owned", "owner")),
        )


def test_ambiguous_active_writers_are_rejected() -> None:
    with pytest.raises(ExecutionPlanError, match="Ambiguous active writers"):
        _compile(
            (
                _descriptor("owner", writes=("shared",)),
                _descriptor("intruder", writes=("shared",)),
            ),
            _schema(("shared", "owner")),
        )


def test_required_current_cycle_without_producer_is_rejected() -> None:
    with pytest.raises(ExecutionPlanError, match="active producer"):
        _compile(
            (_descriptor("consumer", reads=(_read("source"),)),),
            _schema(("source", "source")),
        )


def test_optional_current_cycle_without_producer_has_no_edge() -> None:
    plan = _compile(
        (_descriptor("consumer", reads=(_read("source", required=False),)),),
        _schema(("source", "source")),
    )

    assert plan.dependencies == ()
    assert plan.waves[0].module_ids == (ModuleId("consumer"),)


def test_any_committed_never_creates_same_cycle_edge() -> None:
    plan = _compile(
        (
            _descriptor("source", writes=("source",)),
            _descriptor(
                "consumer",
                reads=(_read("source", freshness=FreshnessMode.ANY_COMMITTED),),
            ),
        ),
        _schema(("source", "source")),
    )

    assert plan.dependencies == ()
    assert plan.waves[0].module_ids == (ModuleId("consumer"), ModuleId("source"))


def test_current_cycle_self_dependency_is_cycle_error() -> None:
    with pytest.raises(DependencyCycleError):
        _compile(
            (_descriptor("self", reads=(_read("self"),), writes=("self",)),),
            _schema(("self", "self")),
        )


def test_multi_module_cycle_is_rejected() -> None:
    with pytest.raises(DependencyCycleError):
        _compile(
            (
                _descriptor("a", reads=(_read("b"),), writes=("a",)),
                _descriptor("b", reads=(_read("a"),), writes=("b",)),
            ),
            _schema(("a", "a"), ("b", "b")),
        )


def test_failed_compile_does_not_consume_plan_identity() -> None:
    factory = DeterministicIdFactory(NAMESPACE, "identity")
    invalid = _descriptor("consumer", reads=(_read("source"),))

    with pytest.raises(ExecutionPlanError):
        _compile((invalid,), _schema(("source", "source")), factory)
    assert factory.counter == 0

    _compile((), _schema(), factory)
    assert factory.counter == 1


def test_identity_and_revision_metadata_do_not_affect_fingerprint() -> None:
    descriptor = _descriptor("alpha")
    first = _compile((descriptor,), _schema())
    second = ExecutionPlanCompiler(DeterministicIdFactory(NAMESPACE, "other")).compile(
        (descriptor,),
        StateSchema(SchemaRevision(99), ()),
        composition_revision=CompositionRevision(88),
        plan_revision=ExecutionPlanRevision(77),
    )

    assert first.plan_id != second.plan_id
    assert first.revision != second.revision
    assert first.composition_revision != second.composition_revision
    assert first.schema_revision != second.schema_revision
    assert first.fingerprint == second.fingerprint


def test_compiler_rejects_descriptor_without_cognitive_cycle() -> None:
    descriptor = _descriptor("alpha")
    object.__setattr__(descriptor, "phases", frozenset())

    with pytest.raises(ExecutionPlanError, match="ExecutionPhase"):
        _compile((descriptor,), _schema())


def test_compiler_rejects_non_descriptor_item() -> None:
    with pytest.raises(TypeError, match="ModuleDescriptor"):
        _compile(cast(tuple[ModuleDescriptor, ...], (object(),)), _schema())
