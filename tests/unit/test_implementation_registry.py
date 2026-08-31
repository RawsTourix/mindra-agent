"""Immutable factory registry и strict reference resolution IS-13."""

from dataclasses import FrozenInstanceError

import pytest

from mindra.composition import (
    ImplementationFactoryDescriptor,
    ImplementationRegistry,
    ModuleProfile,
    build_reference_registry,
)
from mindra.contracts import (
    ConfigurationError,
    DuplicateIdentityError,
    ImplementationId,
    ModuleId,
    Unknown,
)


def _profile(module_id: str, implementation_id: str, **settings: object) -> ModuleProfile:
    return ModuleProfile(
        ModuleId(module_id),
        ImplementationId(implementation_id),
        tuple(settings.items()),  # type: ignore[arg-type]
    )


def test_reference_registry_has_exact_immutable_surface() -> None:
    registry = build_reference_registry()

    assert len(registry) == 4
    assert not any(hasattr(registry, name) for name in ("add", "register", "remove", "replace"))
    with pytest.raises(FrozenInstanceError):
        registry._descriptors = {}  # type: ignore[misc]


def test_duplicate_and_unknown_implementation_ids_fail_closed() -> None:
    descriptor = build_reference_registry().resolve(ImplementationId("reference.synthetic_join.v1"))
    with pytest.raises(DuplicateIdentityError):
        ImplementationRegistry((descriptor, descriptor))
    with pytest.raises(ConfigurationError):
        build_reference_registry().resolve(ImplementationId("unknown.impl"))


@pytest.mark.parametrize(
    ("profile", "message"),
    [
        (_profile("synthetic.source", "reference.synthetic_source.v1"), "value"),
        (
            _profile("synthetic.source", "reference.synthetic_source.v1", value=True),
            "int",
        ),
        (
            _profile("synthetic.source", "reference.synthetic_source.v1", value=2, extra=1),
            "value",
        ),
        (
            _profile("wrong.source", "reference.synthetic_source.v1", value=2),
            "ModuleId",
        ),
        (
            _profile("synthetic.join", "reference.synthetic_join.v1", extra=1),
            "settings",
        ),
    ],
)
def test_reference_factories_strict_validate_profile(
    profile: ModuleProfile,
    message: str,
) -> None:
    factory = build_reference_registry().resolve(profile.implementation_id).factory
    with pytest.raises(ConfigurationError, match=message):
        factory(profile)


def test_source_factory_returns_exact_unknown_int_field() -> None:
    profile = _profile("synthetic.source", "reference.synthetic_source.v1", value=2)
    resolved = build_reference_registry().resolve(profile.implementation_id).factory(profile)

    assert resolved.module.descriptor.module_id == profile.module_id
    assert resolved.module.descriptor.implementation_id == profile.implementation_id
    assert resolved.resolved_settings == (("value", 2),)
    assert resolved.initial_private_state is None
    assert len(resolved.state_fields) == 1
    field = resolved.state_fields[0]
    assert field.spec.owner == profile.module_id
    assert field.spec.value_contract.value_type is int
    assert isinstance(field.initial_availability, Unknown)


def test_factory_descriptor_requires_callable() -> None:
    with pytest.raises(TypeError):
        ImplementationFactoryDescriptor(
            ImplementationId("example.impl"),
            object(),  # type: ignore[arg-type]
        )
