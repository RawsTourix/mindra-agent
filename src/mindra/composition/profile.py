"""Immutable kernel profiles и strict TOML parsing v0.1."""

import math
import tomllib
from dataclasses import dataclass
from pathlib import Path
from re import compile as compile_pattern

from mindra.contracts import ConfigurationError, ImplementationId, ModuleId, ProfileId

KERNEL_PROFILE_SCHEMA_V1 = "mindra.kernel-profile/v1"
type ProfileSettingValue = str | int | float | bool

_SETTING_KEY_PATTERN = compile_pattern(r"[a-z][a-z0-9_]*")
_TOP_LEVEL_KEYS = frozenset({"schema", "profile_id", "modules"})
_MODULE_KEYS = frozenset({"module_id", "implementation", "settings"})


def _validate_setting_value(value: object, *, key: str) -> None:
    if type(value) not in {str, int, float, bool}:
        raise ConfigurationError(f"Setting {key!r} должен быть scalar str/int/finite float/bool")
    if type(value) is float and not math.isfinite(value):
        raise ConfigurationError(f"Setting {key!r} должен быть finite float")


def _canonical_settings(
    settings: tuple[tuple[str, ProfileSettingValue], ...],
) -> tuple[tuple[str, ProfileSettingValue], ...]:
    if not isinstance(settings, tuple):
        raise ConfigurationError("settings должен быть immutable tuple пар key/value")

    values: dict[str, ProfileSettingValue] = {}
    for item in settings:
        if not isinstance(item, tuple) or len(item) != 2:
            raise ConfigurationError("Каждый setting должен быть tuple (key, value)")
        key, value = item
        if not isinstance(key, str) or _SETTING_KEY_PATTERN.fullmatch(key) is None:
            raise ConfigurationError(
                "Setting key должен иметь canonical lowercase snake representation"
            )
        if key in values:
            raise ConfigurationError(f"Duplicate setting key: {key}")
        _validate_setting_value(value, key=key)
        values[key] = value
    return tuple(sorted(values.items()))


@dataclass(frozen=True, slots=True)
class ModuleProfile:
    """Immutable selection одной concrete module implementation."""

    module_id: ModuleId
    implementation_id: ImplementationId
    settings: tuple[tuple[str, ProfileSettingValue], ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, ModuleId):
            raise TypeError("module_id должен быть ModuleId")
        if not isinstance(self.implementation_id, ImplementationId):
            raise TypeError("implementation_id должен быть ImplementationId")
        object.__setattr__(self, "settings", _canonical_settings(self.settings))


@dataclass(frozen=True, slots=True)
class KernelProfile:
    """Canonical immutable configuration активной kernel composition."""

    schema: str
    profile_id: ProfileId
    modules: tuple[ModuleProfile, ...]

    def __post_init__(self) -> None:
        if self.schema != KERNEL_PROFILE_SCHEMA_V1:
            raise ConfigurationError(f"Unsupported kernel profile schema: {self.schema!r}")
        if not isinstance(self.profile_id, ProfileId):
            raise TypeError("profile_id должен быть ProfileId")
        if not isinstance(self.modules, tuple):
            raise ConfigurationError("modules должен быть tuple ModuleProfile")
        if not self.modules:
            raise ConfigurationError("KernelProfile должен содержать хотя бы один module")
        if any(not isinstance(module, ModuleProfile) for module in self.modules):
            raise ConfigurationError("modules должен содержать только ModuleProfile")

        module_ids = tuple(module.module_id for module in self.modules)
        if len(module_ids) != len(set(module_ids)):
            raise ConfigurationError("KernelProfile содержит duplicate ModuleId")
        object.__setattr__(
            self,
            "modules",
            tuple(sorted(self.modules, key=lambda module: module.module_id.value)),
        )


def parse_kernel_profile_toml(text: str) -> KernelProfile:
    """Strict-разобрать один kernel profile из TOML text."""
    if not isinstance(text, str):
        raise ConfigurationError("TOML profile text должен быть строкой")
    try:
        document = tomllib.loads(text)
        return _parse_document(document)
    except ConfigurationError:
        raise
    except (tomllib.TOMLDecodeError, TypeError, ValueError) as error:
        raise ConfigurationError(f"Некорректный kernel profile TOML: {error}") from error


def load_kernel_profile(path: str | Path) -> KernelProfile:
    """Прочитать local TOML file и вернуть strict immutable profile."""
    try:
        text = Path(path).read_text(encoding="utf-8")
        return parse_kernel_profile_toml(text)
    except ConfigurationError as error:
        raise ConfigurationError(
            f"Не удалось загрузить kernel profile {path!s}: {error}"
        ) from error
    except (OSError, UnicodeError, TypeError, ValueError) as error:
        raise ConfigurationError(
            f"Не удалось загрузить kernel profile {path!s}: {error}"
        ) from error


def _parse_document(document: object) -> KernelProfile:
    if not isinstance(document, dict):
        raise ConfigurationError("TOML root должен быть table")
    _require_exact_keys(document, _TOP_LEVEL_KEYS, context="top-level")

    schema = document["schema"]
    profile_id_value = document["profile_id"]
    raw_modules = document["modules"]
    if not isinstance(schema, str):
        raise ConfigurationError("schema должен быть строкой")
    if not isinstance(profile_id_value, str):
        raise ConfigurationError("profile_id должен быть строкой")
    if not isinstance(raw_modules, list):
        raise ConfigurationError("modules должен быть TOML array of tables")

    try:
        profile_id = ProfileId(profile_id_value)
    except (TypeError, ValueError) as error:
        raise ConfigurationError(f"Некорректный profile_id: {profile_id_value!r}") from error

    modules = tuple(
        _parse_module(raw_module, index) for index, raw_module in enumerate(raw_modules)
    )
    return KernelProfile(schema=schema, profile_id=profile_id, modules=modules)


def _parse_module(raw_module: object, index: int) -> ModuleProfile:
    if not isinstance(raw_module, dict):
        raise ConfigurationError(f"modules[{index}] должен быть table")
    required_keys = frozenset({"module_id", "implementation"})
    keys = frozenset(raw_module)
    unknown = keys - _MODULE_KEYS
    missing = required_keys - keys
    if unknown or missing:
        raise ConfigurationError(
            f"Некорректные keys modules[{index}]: unknown={sorted(unknown)}, "
            f"missing={sorted(missing)}"
        )

    module_id_value = raw_module["module_id"]
    implementation_value = raw_module["implementation"]
    if not isinstance(module_id_value, str):
        raise ConfigurationError(f"modules[{index}].module_id должен быть строкой")
    if not isinstance(implementation_value, str):
        raise ConfigurationError(f"modules[{index}].implementation должен быть строкой")

    raw_settings = raw_module.get("settings", {})
    if not isinstance(raw_settings, dict):
        raise ConfigurationError(f"modules[{index}].settings должен быть table")
    settings: list[tuple[str, ProfileSettingValue]] = []
    for key, value in raw_settings.items():
        if not isinstance(key, str):
            raise ConfigurationError(f"modules[{index}] setting key должен быть строкой")
        _validate_setting_value(value, key=key)
        settings.append((key, value))

    try:
        return ModuleProfile(
            module_id=ModuleId(module_id_value),
            implementation_id=ImplementationId(implementation_value),
            settings=tuple(settings),
        )
    except (TypeError, ValueError) as error:
        raise ConfigurationError(f"Некорректный modules[{index}]: {error}") from error


def _require_exact_keys(
    value: dict[object, object],
    expected: frozenset[str],
    *,
    context: str,
) -> None:
    keys = frozenset(value)
    unknown = keys - expected
    missing = expected - keys
    if unknown or missing:
        raise ConfigurationError(
            f"Некорректные keys {context}: unknown={sorted(map(str, unknown))}, "
            f"missing={sorted(missing)}"
        )


__all__ = [
    "KERNEL_PROFILE_SCHEMA_V1",
    "KernelProfile",
    "ModuleProfile",
    "ProfileSettingValue",
    "load_kernel_profile",
    "parse_kernel_profile_toml",
]
