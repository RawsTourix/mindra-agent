"""Явная configuration/composition boundary Core Kernel MINDRA."""

from mindra.composition.profile import (
    KERNEL_PROFILE_SCHEMA_V1,
    KernelProfile,
    ModuleProfile,
    ProfileSettingValue,
    load_kernel_profile,
    parse_kernel_profile_toml,
)
from mindra.composition.registry import (
    ImplementationFactoryDescriptor,
    ImplementationRegistry,
    InitialPrivateState,
    ResolvedModule,
    ResolvedStateField,
    build_reference_registry,
)
from mindra.composition.root import CompositionRoot
from mindra.composition.runtime import CompositionMetadata, KernelRuntime

__all__ = [
    "KERNEL_PROFILE_SCHEMA_V1",
    "CompositionMetadata",
    "CompositionRoot",
    "ImplementationFactoryDescriptor",
    "ImplementationRegistry",
    "InitialPrivateState",
    "KernelProfile",
    "KernelRuntime",
    "ModuleProfile",
    "ProfileSettingValue",
    "ResolvedModule",
    "ResolvedStateField",
    "build_reference_registry",
    "load_kernel_profile",
    "parse_kernel_profile_toml",
]
