"""Immutable implementation registry и explicit reference factories."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import cast

from mindra.composition.profile import ModuleProfile, ProfileSettingValue, _canonical_settings
from mindra.contracts import (
    CognitiveModule,
    CompositionError,
    ConfigurationError,
    DuplicateIdentityError,
    ImplementationId,
    ModuleDescriptor,
    ModuleId,
    ModuleStatefulness,
    StateFieldSpec,
    StateKey,
    Unavailable,
    Unknown,
    ValueContract,
)
from mindra.reference import (
    SYNTHETIC_DOUBLE_VALUE_KEY,
    SYNTHETIC_JOIN_VALUE_KEY,
    SYNTHETIC_SOURCE_VALUE_KEY,
    SYNTHETIC_TRIPLE_VALUE_KEY,
    SyntheticDoubleModule,
    SyntheticJoinModule,
    SyntheticSourceModule,
    SyntheticTripleModule,
)


@dataclass(frozen=True, slots=True)
class ResolvedStateField:
    """One resolved public field и его explicit initial availability."""

    spec: StateFieldSpec[object]
    initial_availability: Unknown | Unavailable

    def __post_init__(self) -> None:
        if not isinstance(self.spec, StateFieldSpec):
            raise TypeError("spec должен быть StateFieldSpec")
        if not isinstance(self.initial_availability, Unknown | Unavailable):
            raise CompositionError(
                "Initial public availability должна быть Unknown или Unavailable"
            )


@dataclass(frozen=True, slots=True)
class InitialPrivateState:
    """Explicit wrapper initial private payload, включая legitimate None."""

    value: object


@dataclass(frozen=True, slots=True)
class ResolvedModule:
    """Полностью resolved module assembly metadata."""

    module: CognitiveModule
    state_fields: tuple[ResolvedStateField, ...]
    resolved_settings: tuple[tuple[str, ProfileSettingValue], ...]
    initial_private_state: InitialPrivateState | None

    def __post_init__(self) -> None:
        if not isinstance(self.module, CognitiveModule):
            raise TypeError("module должен удовлетворять CognitiveModule")
        if not isinstance(self.state_fields, tuple) or any(
            not isinstance(field, ResolvedStateField) for field in self.state_fields
        ):
            raise TypeError("state_fields должен быть tuple ResolvedStateField")

        descriptor = self.module.descriptor
        canonical_fields = tuple(
            sorted(self.state_fields, key=lambda field: field.spec.key.path.dotted)
        )
        paths = tuple(field.spec.key.path for field in canonical_fields)
        if len(paths) != len(set(paths)):
            raise CompositionError("ResolvedModule содержит duplicate StatePath")
        if any(field.spec.owner != descriptor.module_id for field in canonical_fields):
            raise CompositionError("Resolved state field owner не совпадает с ModuleId")
        if set(paths) != {key.path for key in descriptor.writes}:
            raise CompositionError("Resolved state fields не совпадают с descriptor.writes")

        is_stateful = descriptor.traits.statefulness is ModuleStatefulness.STATEFUL
        if is_stateful != (self.initial_private_state is not None):
            raise CompositionError(
                "Stateful module требует InitialPrivateState, stateless запрещает его"
            )

        object.__setattr__(self, "state_fields", canonical_fields)
        object.__setattr__(self, "resolved_settings", _canonical_settings(self.resolved_settings))


type ModuleFactory = Callable[[ModuleProfile], ResolvedModule]


@dataclass(frozen=True, slots=True)
class ImplementationFactoryDescriptor:
    """Immutable binding semantic implementation identity к pure factory."""

    implementation_id: ImplementationId
    factory: ModuleFactory

    def __post_init__(self) -> None:
        if not isinstance(self.implementation_id, ImplementationId):
            raise TypeError("implementation_id должен быть ImplementationId")
        if not callable(self.factory):
            raise TypeError("factory должен быть callable")


@dataclass(frozen=True, slots=True, init=False)
class ImplementationRegistry:
    """Read-only catalogue concrete factories composition boundary."""

    _descriptors: Mapping[ImplementationId, ImplementationFactoryDescriptor]

    def __init__(
        self,
        descriptors: tuple[ImplementationFactoryDescriptor, ...],
    ) -> None:
        if not isinstance(descriptors, tuple):
            raise TypeError("descriptors должен быть tuple ImplementationFactoryDescriptor")
        values: dict[ImplementationId, ImplementationFactoryDescriptor] = {}
        for descriptor in descriptors:
            if not isinstance(descriptor, ImplementationFactoryDescriptor):
                raise TypeError("descriptors должен содержать ImplementationFactoryDescriptor")
            if descriptor.implementation_id in values:
                raise DuplicateIdentityError(
                    f"Duplicate ImplementationId: {descriptor.implementation_id}"
                )
            values[descriptor.implementation_id] = descriptor
        object.__setattr__(self, "_descriptors", MappingProxyType(values))

    def resolve(
        self,
        implementation_id: ImplementationId,
        /,
    ) -> ImplementationFactoryDescriptor:
        """Вернуть exact registered factory либо fail closed."""
        if not isinstance(implementation_id, ImplementationId):
            raise TypeError("implementation_id должен быть ImplementationId")
        try:
            return self._descriptors[implementation_id]
        except KeyError as error:
            raise ConfigurationError(f"Unknown implementation_id: {implementation_id}") from error

    def __len__(self) -> int:
        return len(self._descriptors)


def build_reference_registry() -> ImplementationRegistry:
    """Явно построить immutable registry четырёх v0.1 reference modules."""
    return ImplementationRegistry(
        (
            ImplementationFactoryDescriptor(
                ImplementationId("reference.synthetic_source.v1"),
                _build_source,
            ),
            ImplementationFactoryDescriptor(
                ImplementationId("reference.synthetic_double.v1"),
                _build_double,
            ),
            ImplementationFactoryDescriptor(
                ImplementationId("reference.synthetic_triple.v1"),
                _build_triple,
            ),
            ImplementationFactoryDescriptor(
                ImplementationId("reference.synthetic_join.v1"),
                _build_join,
            ),
        )
    )


def _build_source(profile: ModuleProfile) -> ResolvedModule:
    _require_module_id(profile, "synthetic.source")
    settings = dict(profile.settings)
    if set(settings) != {"value"}:
        raise ConfigurationError("Synthetic source требует ровно setting 'value'")
    value = settings["value"]
    if type(value) is not int:
        raise ConfigurationError("Synthetic source setting 'value' должен быть int, не bool")
    return _resolved_stateless(
        profile=profile,
        module=cast(CognitiveModule, SyntheticSourceModule(value=value)),
        output_key=cast(StateKey[object], SYNTHETIC_SOURCE_VALUE_KEY),
    )


def _build_double(profile: ModuleProfile) -> ResolvedModule:
    _require_module_id(profile, "synthetic.double")
    _require_empty_settings(profile)
    return _resolved_stateless(
        profile=profile,
        module=cast(CognitiveModule, SyntheticDoubleModule()),
        output_key=cast(StateKey[object], SYNTHETIC_DOUBLE_VALUE_KEY),
    )


def _build_triple(profile: ModuleProfile) -> ResolvedModule:
    _require_module_id(profile, "synthetic.triple")
    _require_empty_settings(profile)
    return _resolved_stateless(
        profile=profile,
        module=cast(CognitiveModule, SyntheticTripleModule()),
        output_key=cast(StateKey[object], SYNTHETIC_TRIPLE_VALUE_KEY),
    )


def _build_join(profile: ModuleProfile) -> ResolvedModule:
    _require_module_id(profile, "synthetic.join")
    _require_empty_settings(profile)
    return _resolved_stateless(
        profile=profile,
        module=cast(CognitiveModule, SyntheticJoinModule()),
        output_key=cast(StateKey[object], SYNTHETIC_JOIN_VALUE_KEY),
    )


def _require_module_id(profile: ModuleProfile, expected: str) -> None:
    if not isinstance(profile, ModuleProfile):
        raise TypeError("factory принимает только ModuleProfile")
    if profile.module_id != ModuleId(expected):
        raise ConfigurationError(
            f"Implementation {profile.implementation_id} требует ModuleId {expected}"
        )


def _require_empty_settings(profile: ModuleProfile) -> None:
    if profile.settings:
        raise ConfigurationError(
            f"Implementation {profile.implementation_id} не принимает settings"
        )


def _resolved_stateless(
    *,
    profile: ModuleProfile,
    module: CognitiveModule,
    output_key: StateKey[object],
) -> ResolvedModule:
    descriptor: ModuleDescriptor = module.descriptor
    if descriptor.implementation_id != profile.implementation_id:
        raise ConfigurationError(
            "Profile implementation_id не совпадает с reference factory implementation"
        )
    return ResolvedModule(
        module=module,
        state_fields=(
            ResolvedStateField(
                spec=StateFieldSpec(
                    key=output_key,
                    owner=descriptor.module_id,
                    value_contract=ValueContract(int),
                ),
                initial_availability=Unknown(),
            ),
        ),
        resolved_settings=profile.settings,
        initial_private_state=None,
    )


__all__ = [
    "ImplementationFactoryDescriptor",
    "ImplementationRegistry",
    "InitialPrivateState",
    "ResolvedModule",
    "ResolvedStateField",
    "build_reference_registry",
]
