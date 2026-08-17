# Candidate contract Engineering Testing MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-29 — Engineering Testing`

Этот документ уточняет machine-facing semantic формы accepted design [`../engineering-testing.md`](../engineering-testing.md).

Он **не является frozen Python API** и не фиксирует test runner, CI provider, property-testing framework, import linter, mocking library, coverage tool или directory layout.

---

# 1. VerificationObligation

```text
VerificationObligation
├── obligation_id
├── obligation_revision
├── source_design_refs[]
├── source_adr_refs[]
├── source_contract_refs[]
├── target_boundary
├── invariant_text
├── invariant_kind
├── enforcement_classes[]
├── required_test_spec_refs[]
├── required_environment_profiles[]
├── severity / fail_closed?
├── automation_status
├── unsupported_reason?
└── provenance
```

`automation_status` conceptually различает machine-checkable, partially checkable и manual-only obligations.

---

# 2. VerificationMatrix

```text
VerificationMatrix
├── matrix_id
├── matrix_revision
├── repository_revision_ref
├── obligation_refs[]
├── obligation_to_test_refs{}
├── obligation_to_ci_tiers{}
├── latest_evidence_refs{}
├── uncovered_obligations[]
└── provenance
```

Line coverage не заменяет этот объект.

---

# 3. EngineeringTestSpec

```text
EngineeringTestSpec
├── test_spec_id
├── revision
├── title / purpose
├── test_class
├── target_boundary
├── obligation_refs[]
├── input_generation_spec?
├── setup/composition_profile_ref
├── test_environment_profile_refs[]
├── capability_requirements[]
├── oracle_spec_ref
├── fault_spec_refs[]
├── assertion_semantics
├── timeout/resource_policy?
├── reproducibility_requirement?
├── expected_statuses[]
└── provenance
```

Conceptual `test_class`:

```text
static_architecture
unit
contract_conformance
property
state_machine
integration
fault_recovery
round_trip
migration
backend_compatibility
system_smoke
```

Exact enum не frozen.

---

# 4. AssertionSemantics

```text
AssertionSemantics
├── equality_mode
├── numeric_tolerance?
├── invariant_predicates[]
├── ordering_constraints[]
├── allowed_nondeterminism?
└── provenance
```

Conceptual equality modes:

```text
bitwise
exact_semantic
bounded_numeric
invariant_only
distributional_property
```

`seed` сам по себе не определяет equality mode.

---

# 5. ContractConformanceProfile

```text
ContractConformanceProfile
├── profile_id
├── target_contract_ref
├── implementation_ref
├── declared_capabilities[]
├── intentionally_absent_capabilities[]
├── control_semantics?
├── required_conformance_tests[]
├── expected_degradations[]
└── provenance
```

`NoX` не обязан проходить tests capability, которую он явно объявляет отсутствующей.

---

# 6. TestCompositionProfile

```text
TestCompositionProfile
├── profile_id
├── composition_revision
├── component_implementation_refs{}
├── test_double_refs{}
├── config_ref
├── visibility_policy_ref
├── logical_clock_profile_ref?
├── rng_profile_ref?
├── resource_limit_profile_ref?
└── provenance
```

Test composition не может вводить hidden runtime Service Locator.

---

# 7. TestOracleSpec

```text
TestOracleSpec
├── oracle_id
├── oracle_kind
├── allowed_privileged_inputs[]
├── expected_output/invariant_source
├── visibility_boundary
├── independence_notes?
└── provenance
```

Test oracle state не становится Agent-visible data.

---

# 8. FaultInjectionSpec

```text
FaultInjectionSpec
├── fault_id
├── target_boundary
├── fault_kind
├── injection_point
├── trigger_semantics
├── expected_system_response
├── expected_persistent_effects[]
├── forbidden_effects[]
├── recovery_expectation?
└── provenance
```

Conceptual kinds включают timeout, unavailable, malformed output, stale revision, storage corruption, OOM, lost acknowledgement, duplicate dispatch, optimizer failure и migration incompatibility.

---

# 9. StatefulModelSpec

```text
StatefulModelSpec
├── model_id
├── target_boundary
├── abstract_state_schema
├── operation_specs[]
├── preconditions[]
├── transition_model
├── invariants[]
├── terminal/error states[]
├── shrinking/reduction requirement?
└── provenance
```

Reference model может быть существенно проще production implementation.

---

# 10. EngineeringTestEnvironmentProfile

```text
EngineeringTestEnvironmentProfile
├── profile_id
├── software_manifest_ref
├── hardware/topology constraints?
├── backend/provider mode
├── network mode
├── precision profile?
├── determinism policy_ref?
├── resource limits{}
├── fault capability refs[]
└── provenance
```

---

# 11. EngineeringTestRunRecord

```text
EngineeringTestRunRecord
├── run_id
├── repository_revision_ref
├── test_spec_ref
├── composition_profile_ref
├── environment_profile_ref
├── seed/RNG refs[]
├── started/ended metadata
├── status
├── assertion/evidence refs[]
├── failure_signature?
├── minimized_counterexample_ref?
├── logs/artifacts refs[]
├── compute/resource refs[]?
└── provenance
```

Status не сворачивается в boolean pass/fail внутри source evidence.

---

# 12. VerificationEvidenceRecord

```text
VerificationEvidenceRecord
├── evidence_id
├── obligation_refs[]
├── test_run_refs[]
├── result_status
├── environment_scope
├── capability_scope
├── validity_notes[]
├── known_gaps[]
└── provenance
```

---

# 13. ArchitectureDependencySpec

```text
ArchitectureDependencySpec
├── spec_id
├── package/module sets
├── rule_kind
├── allowed_edges[]?
├── forbidden_edges[]?
├── layering/order?
├── cycle_policy?
├── exception_refs[]
└── provenance
```

Concrete import-lint syntax не frozen.

---

# 14. OwnershipTestSpec

```text
OwnershipTestSpec
├── target_namespace/resource
├── owner_ref
├── allowed_writer_refs[]
├── forbidden_writer_classes[]
├── stale_write_policy
├── atomicity_requirement
├── expected_failure_semantics
└── provenance
```

---

# 15. DataLeakageTestSpec

```text
DataLeakageTestSpec
├── privileged_source_ref
├── sentinel/instrumentation policy
├── prohibited_agent_visible_boundaries[]
├── allowed_research_boundaries[]
├── execution_paths[]
├── artifact/log checks[]
└── provenance
```

---

# 16. RoundTripTestSpec

```text
RoundTripTestSpec
├── source_schema/revision
├── encode/materialize step
├── restore/decode step
├── comparison semantics
├── required preserved identities[]
├── allowed migrations[]
└── provenance
```

---

# 17. MigrationTestSpec

```text
MigrationTestSpec
├── source_revision
├── target_revision
├── migration_policy_ref
├── valid_fixture_refs[]
├── invalid_fixture_refs[]
├── lineage_expectations
├── lossless/lossy expectation
├── repeat_application_semantics
└── provenance
```

---

# 18. GoldenArtifactSpec

```text
GoldenArtifactSpec
├── golden_id
├── contract_surface
├── artifact_ref
├── generation_revision
├── comparison_semantics
├── update_policy_ref
├── review_requirements[]
└── provenance
```

Neural stochastic outputs не считаются подходящим golden без explicit deterministic contract.

---

# 19. FlakyTestRecord

```text
FlakyTestRecord
├── flaky_id
├── test_spec_ref
├── observed_failure_runs[]
├── observed_pass_runs[]
├── suspected_nondeterminism_sources[]
├── quarantine_status?
├── owner?
├── repair_issue_ref?
├── first_seen_revision
└── provenance
```

Quarantine не удовлетворяет `VerificationObligation`.

---

# 20. CITierDescriptor

```text
CITierDescriptor
├── tier_id
├── purpose
├── included_test_classes[]
├── environment_profile_refs[]
├── capability_requirements[]
├── scheduling_policy
├── merge_blocking_policy
├── skipped_requirement_policy
└── provenance
```

Concrete tier names/provider не frozen.

---

# 21. VerificationGate

```text
VerificationGate
├── gate_id
├── change_scope / boundary refs[]
├── required_obligation_refs[]
├── required_test_evidence_refs[]
├── allowed_exceptions[]
├── unresolved_status_policy
└── provenance
```

`not run`/`skipped` не становятся `pass` автоматически.

---

# 22. CoverageProfile

```text
CoverageProfile
├── profile_id
├── code_coverage?
├── contract_coverage
├── invariant_coverage
├── failure_mode_coverage
├── schema/migration_coverage
├── backend/capability_matrix_coverage
├── uncovered_obligation_refs[]
└── provenance
```

Ни один line-coverage threshold не frozen.

---

# 23. EngineeringTestReport

```text
EngineeringTestReport
├── report_id
├── repository_revision_ref
├── verification_matrix_ref
├── run_refs[]
├── gate_results[]
├── coverage_profile_ref
├── failed_obligations[]
├── unverified_obligations[]
├── quarantined_tests[]
├── environment_matrix[]
└── provenance
```

---

# 24. Инварианты candidate contract

```text
Engineering Testing ≠ MINDRA-Eval
VerificationObligation ≠ ordinary test case
line coverage ≠ invariant coverage
skipped ≠ passed
quarantined ≠ verified
seed ≠ deterministic equality contract
Test Oracle ≠ Agent-visible input
fault injector ≠ production Service Locator
NoX capability absence ≠ conformance failure
bitwise equality ≠ universal restore/test requirement
```

---

# 25. Что contract не фиксирует

- Python test classes/functions;
- pytest/unittest;
- Hypothesis;
- Import Linter;
- CI YAML/provider;
- coverage threshold;
- mutation score;
- exact status enums;
- exact artifact storage;
- exact accelerator matrix;
- exact timeout values;
- test directory layout.
