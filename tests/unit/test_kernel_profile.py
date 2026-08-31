"""Strict configuration profile parsing IS-13."""

from datetime import date
from pathlib import Path

import pytest

from mindra.composition import (
    KERNEL_PROFILE_SCHEMA_V1,
    KernelProfile,
    ModuleProfile,
    load_kernel_profile,
    parse_kernel_profile_toml,
)
from mindra.contracts import ConfigurationError, ImplementationId, ModuleId, ProfileId


def test_reference_profile_uses_exact_schema_identity_and_canonical_order() -> None:
    profile = load_kernel_profile(Path("configs/v0.1/reference.toml"))

    assert profile.schema == KERNEL_PROFILE_SCHEMA_V1
    assert profile.profile_id == ProfileId("v0_1.reference")
    assert tuple(item.module_id.value for item in profile.modules) == (
        "synthetic.double",
        "synthetic.join",
        "synthetic.source",
        "synthetic.triple",
    )
    source = next(
        item for item in profile.modules if item.module_id == ModuleId("synthetic.source")
    )
    assert source.settings == (("value", 2),)


@pytest.mark.parametrize(
    "text",
    [
        'schema="mindra.kernel-profile/v1"\nprofile_id="v0_1.reference"\nmodules=[]\nextra=1',
        'schema="mindra.kernel-profile/v1"\nprofile_id="v0_1.reference"',
        (
            'schema="mindra.kernel-profile/v1"\nprofile_id="v0_1.reference"\n'
            '[[modules]]\nmodule_id="a"\nimplementation="b"\nextra=1'
        ),
        'schema="mindra.kernel-profile/v1"\nprofile_id="v0.1-reference"\nmodules=[]',
        'schema="mindra.kernel-profile/v1"\nprofile_id="v0_1.reference"\nmodules=[',
    ],
)
def test_invalid_profile_surface_is_configuration_error(text: str) -> None:
    with pytest.raises(ConfigurationError):
        parse_kernel_profile_toml(text)


@pytest.mark.parametrize(
    "setting",
    ["value = [1]", "value = 1979-05-27", "value = nan", "value = { nested = 1 }"],
)
def test_non_scalar_or_non_finite_settings_are_rejected(setting: str) -> None:
    text = (
        'schema = "mindra.kernel-profile/v1"\n'
        'profile_id = "v0_1.reference"\n'
        '[[modules]]\nmodule_id = "synthetic.source"\n'
        'implementation = "reference.synthetic_source.v1"\n'
        f"[modules.settings]\n{setting}\n"
    )
    with pytest.raises(ConfigurationError):
        parse_kernel_profile_toml(text)


def test_profile_and_settings_are_canonicalized_independent_of_input_order() -> None:
    profile = KernelProfile(
        schema=KERNEL_PROFILE_SCHEMA_V1,
        profile_id=ProfileId("example.profile"),
        modules=(
            ModuleProfile(ModuleId("z"), ImplementationId("impl.z"), (("z", 1), ("a", True))),
            ModuleProfile(ModuleId("a"), ImplementationId("impl.a")),
        ),
    )

    assert tuple(item.module_id.value for item in profile.modules) == ("a", "z")
    assert profile.modules[1].settings == (("a", True), ("z", 1))
    assert type(dict(profile.modules[1].settings)["a"]) is bool


def test_duplicate_module_and_setting_keys_are_rejected() -> None:
    module = ModuleProfile(ModuleId("a"), ImplementationId("impl.a"))
    with pytest.raises(ConfigurationError):
        KernelProfile(KERNEL_PROFILE_SCHEMA_V1, ProfileId("example.profile"), (module, module))
    with pytest.raises(ConfigurationError):
        ModuleProfile(ModuleId("a"), ImplementationId("impl.a"), (("value", 1), ("value", 2)))


def test_datetime_object_cannot_be_used_as_direct_setting() -> None:
    with pytest.raises(ConfigurationError):
        ModuleProfile(
            ModuleId("a"),
            ImplementationId("impl.a"),
            (("value", date(2026, 1, 1)),),  # type: ignore[arg-type]
        )


def test_load_wraps_io_failure() -> None:
    with pytest.raises(ConfigurationError):
        load_kernel_profile("configs/v0.1/does-not-exist.toml")
