"""Чистые deterministic reference modules синтетического graph."""

from dataclasses import dataclass, field
from typing import cast

from mindra.contracts import (
    Available,
    DeterminismMode,
    ExecutionPhase,
    ExecutionTraits,
    FreshnessMode,
    ImplementationId,
    ImplementationRevision,
    ModuleComputeRequest,
    ModuleComputeResult,
    ModuleDescriptor,
    ModuleExecutionError,
    ModuleId,
    ModuleStatefulness,
    ReadSpec,
    StateKey,
    StatePath,
    StateProvenance,
    StateUpdateProposal,
    StateWrite,
)

SYNTHETIC_SOURCE_VALUE_KEY = StateKey[int](StatePath.from_dotted("synthetic.source.value"))
SYNTHETIC_DOUBLE_VALUE_KEY = StateKey[int](StatePath.from_dotted("synthetic.double.value"))
SYNTHETIC_TRIPLE_VALUE_KEY = StateKey[int](StatePath.from_dotted("synthetic.triple.value"))
SYNTHETIC_JOIN_VALUE_KEY = StateKey[int](StatePath.from_dotted("synthetic.join.value"))

_REVISION = ImplementationRevision("v1")
_PHASES = frozenset({ExecutionPhase.COGNITIVE_CYCLE})
_TRAITS = ExecutionTraits(
    statefulness=ModuleStatefulness.STATELESS,
    determinism=DeterminismMode.DETERMINISTIC,
)


def _read_spec(key: StateKey[int]) -> ReadSpec[object]:
    return cast(
        ReadSpec[object],
        ReadSpec(
            key=key,
            required=True,
            allowed_availability=frozenset({Available}),
            freshness=FreshnessMode.CURRENT_CYCLE,
        ),
    )


def _descriptor(
    *,
    module_id: str,
    implementation_id: str,
    reads: tuple[ReadSpec[object], ...],
    write: StateKey[int],
) -> ModuleDescriptor:
    return ModuleDescriptor(
        module_id=ModuleId(module_id),
        implementation_id=ImplementationId(implementation_id),
        implementation_revision=_REVISION,
        reads=reads,
        writes=(cast(StateKey[object], write),),
        private_state=None,
        phases=_PHASES,
        traits=_TRAITS,
    )


_SOURCE_DESCRIPTOR = _descriptor(
    module_id="synthetic.source",
    implementation_id="reference.synthetic_source.v1",
    reads=(),
    write=SYNTHETIC_SOURCE_VALUE_KEY,
)
_DOUBLE_DESCRIPTOR = _descriptor(
    module_id="synthetic.double",
    implementation_id="reference.synthetic_double.v1",
    reads=(_read_spec(SYNTHETIC_SOURCE_VALUE_KEY),),
    write=SYNTHETIC_DOUBLE_VALUE_KEY,
)
_TRIPLE_DESCRIPTOR = _descriptor(
    module_id="synthetic.triple",
    implementation_id="reference.synthetic_triple.v1",
    reads=(_read_spec(SYNTHETIC_SOURCE_VALUE_KEY),),
    write=SYNTHETIC_TRIPLE_VALUE_KEY,
)
_JOIN_DESCRIPTOR = _descriptor(
    module_id="synthetic.join",
    implementation_id="reference.synthetic_join.v1",
    reads=(
        _read_spec(SYNTHETIC_DOUBLE_VALUE_KEY),
        _read_spec(SYNTHETIC_TRIPLE_VALUE_KEY),
    ),
    write=SYNTHETIC_JOIN_VALUE_KEY,
)


def _read_int(request: ModuleComputeRequest, key: StateKey[int]) -> int:
    entry = request.state.read(key)
    if not isinstance(entry.availability, Available) or type(entry.availability.value) is not int:
        raise ModuleExecutionError(f"StatePath {key.path} не содержит Available int")
    return entry.availability.value


def _result(
    descriptor: ModuleDescriptor,
    request: ModuleComputeRequest,
    key: StateKey[int],
    value: int,
) -> ModuleComputeResult:
    write = cast(
        StateWrite[object],
        StateWrite(
            key=key,
            availability=Available(value),
            provenance=StateProvenance(
                producer=descriptor.module_id,
                implementation_id=descriptor.implementation_id,
                base_state_revision=request.context.base_state_revision,
                module_attempt_id=request.context.module_attempt_id,
                logical_time=request.context.logical_time,
            ),
        ),
    )
    return ModuleComputeResult(
        state_update=StateUpdateProposal(
            base_state_revision=request.context.base_state_revision,
            producer=descriptor.module_id,
            module_attempt_id=request.context.module_attempt_id,
            writes=(write,),
        ),
        private_state_update=None,
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class SyntheticSourceModule:
    """Неизменяемый source заданного целого значения."""

    value: int
    descriptor: ModuleDescriptor = field(init=False, default=_SOURCE_DESCRIPTOR, repr=False)

    def __post_init__(self) -> None:
        if type(self.value) is not int:
            raise TypeError("value должен быть int, bool недопустим")

    def compute(self, request: ModuleComputeRequest) -> ModuleComputeResult:
        """Вернуть configured value как staged public update."""
        return _result(self.descriptor, request, SYNTHETIC_SOURCE_VALUE_KEY, self.value)


@dataclass(frozen=True, slots=True)
class SyntheticDoubleModule:
    """Удвоить source value текущего cognitive cycle."""

    descriptor: ModuleDescriptor = field(init=False, default=_DOUBLE_DESCRIPTOR, repr=False)

    def compute(self, request: ModuleComputeRequest) -> ModuleComputeResult:
        """Вернуть source multiplied by two."""
        value = _read_int(request, SYNTHETIC_SOURCE_VALUE_KEY)
        return _result(self.descriptor, request, SYNTHETIC_DOUBLE_VALUE_KEY, value * 2)


@dataclass(frozen=True, slots=True)
class SyntheticTripleModule:
    """Утроить source value текущего cognitive cycle."""

    descriptor: ModuleDescriptor = field(init=False, default=_TRIPLE_DESCRIPTOR, repr=False)

    def compute(self, request: ModuleComputeRequest) -> ModuleComputeResult:
        """Вернуть source multiplied by three."""
        value = _read_int(request, SYNTHETIC_SOURCE_VALUE_KEY)
        return _result(self.descriptor, request, SYNTHETIC_TRIPLE_VALUE_KEY, value * 3)


@dataclass(frozen=True, slots=True)
class SyntheticJoinModule:
    """Сложить double и triple values текущего cognitive cycle."""

    descriptor: ModuleDescriptor = field(init=False, default=_JOIN_DESCRIPTOR, repr=False)

    def compute(self, request: ModuleComputeRequest) -> ModuleComputeResult:
        """Вернуть сумму double и triple в declared read order."""
        double = _read_int(request, SYNTHETIC_DOUBLE_VALUE_KEY)
        triple = _read_int(request, SYNTHETIC_TRIPLE_VALUE_KEY)
        return _result(self.descriptor, request, SYNTHETIC_JOIN_VALUE_KEY, double + triple)


__all__ = [
    "SYNTHETIC_DOUBLE_VALUE_KEY",
    "SYNTHETIC_JOIN_VALUE_KEY",
    "SYNTHETIC_SOURCE_VALUE_KEY",
    "SYNTHETIC_TRIPLE_VALUE_KEY",
    "SyntheticDoubleModule",
    "SyntheticJoinModule",
    "SyntheticSourceModule",
    "SyntheticTripleModule",
]
