# Candidate contract Research Claims / Limitations MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-30 — Research Claims / Limitations`

Этот документ уточняет machine-facing semantic формы accepted design [`../research-claims-limitations.md`](../research-claims-limitations.md).

Он **не является frozen Python API** и не фиксирует storage backend, report generator, preregistration service, publication format, exact evidence-strength enum или NLP wording checker.

---

# 1. ObservationRecord

```text
ObservationRecord
├── observation_id
├── observation_revision
├── source_evidence_refs[]
├── source_run/condition_refs[]
├── measurement_kind
├── measured_values / distribution refs
├── uncertainty refs?
├── validity_ref
├── directness / derivation notes
└── provenance
```

Observation не содержит causal/generalization semantics сверх source evidence.

---

# 2. InterpretationRecord

```text
InterpretationRecord
├── interpretation_id
├── revision
├── observation/evidence refs[]
├── interpretation_text / structured proposition
├── competing_explanations[]
├── assumptions[]
├── confounders[]
├── scope_ref
├── uncertainty_notes[]
├── author/reviewer refs?
└── provenance
```

Один evidence set может иметь несколько InterpretationRecord.

---

# 3. ClaimScope

```text
ClaimScope
├── scope_id
├── Agent/component revision constraints[]
├── Cortex conditions[]
├── training/data conditions[]
├── Environment/task/world distributions[]
├── checkpoint/restore constraints[]
├── module composition/interventions[]
├── time/horizon constraints?
├── compute/context/tuning constraints[]
├── software/hardware constraints[]?
├── replicate/population scope[]
├── metric/analysis revisions[]
└── provenance
```

Отсутствующий scope dimension не интерпретируется автоматически как universal.

---

# 4. ResearchClaim

```text
ResearchClaim
├── claim_id
├── claim_revision
├── claim_kind
├── proposition
├── scope_ref
├── status
├── support_evidence_refs[]
├── challenging_evidence_refs[]
├── interpretation_refs[]
├── assumption_refs[]
├── limitation_refs[]
├── known_unknown_refs[]
├── confidence/strength descriptor?
├── originating_hypothesis/module_gate refs[]
├── review_refs[]
├── supersedes / superseded_by refs[]
├── public_statement_refs[]
└── provenance
```

`confidence/strength descriptor` не является probability автоматически.

---

# 5. ClaimKind

Conceptual kinds:

```text
descriptive
associational
predictive
engineering_conformance
causal
comparative
calibration
robustness
generalization
transfer
resource_efficiency
architecture_contribution
negative_or_null
existence_within_scope
theoretical_hypothesis
```

Exact enum не frozen.

---

# 6. ClaimStatus

Conceptual lifecycle states:

```text
proposed
under_evaluation
supported_within_scope
inconclusive
challenged
weakened
unsupported_within_scope
superseded
withdrawn
```

Status transition создаёт `ClaimReviewRecord`; historical revision не переписывается.

---

# 7. EvidenceSupportRecord

```text
EvidenceSupportRecord
├── support_id
├── claim_ref
├── evidence_ref
├── role
├── evidence_strength_class?
├── validity_ref
├── direct / indirect
├── scope_alignment
├── matching/confounding notes[]
├── uncertainty notes[]
└── provenance
```

`role` conceptually различает supporting, challenging, neutral/contextual.

---

# 8. ClaimAssumption

```text
ClaimAssumption
├── assumption_id
├── claim_refs[]
├── assumption_text
├── testability
├── supporting_refs[]
├── violation_effect
├── status
└── provenance
```

Неявная assumption считается reporting gap.

---

# 9. LimitationRecord

```text
LimitationRecord
├── limitation_id
├── limitation_revision
├── limitation_kind
├── target_refs[]
├── description
├── severity/materiality?
├── affected_claim_dimensions[]
├── evidence_refs[]
├── mitigation/status
├── resolved_by_refs[]?
└── provenance
```

Conceptual kinds:

```text
scope
measurement
statistical
causal_confounding
implementation
Cortex_provider
compute_data_tuning
reproducibility
external_validity
engineering_verification_gap
missing_control
unknown_mechanism
interpretation
```

---

# 10. KnownUnknownRecord

```text
KnownUnknownRecord
├── unknown_id
├── revision
├── question
├── related_claim/module refs[]
├── why_unknown
├── required_evidence / candidate study refs[]
├── current_scope
├── status
└── provenance
```

`unknown` не кодируется как false/zero.

---

# 11. UnsupportedClaimPattern

```text
UnsupportedClaimPattern
├── pattern_id
├── source_concept
├── prohibited_or_unjustified_inference
├── rationale
├── allowed_weaker_wording[]
├── required_bridge_evidence?
├── severity
└── provenance
```

Минимальные patterns включают:

```text
Self Model → consciousness/self-awareness proof
Affect → subjective feeling proof
Workspace → consciousness proof
first-person Cortex text → reliable phenomenal self-report
human-like behavior → human-like phenomenology
functional analogy → biological equivalence
single benchmark → AGI
```

---

# 12. ClaimReviewRecord

```text
ClaimReviewRecord
├── review_id
├── claim_before_ref
├── trigger_refs[]
├── new/supporting/challenging evidence refs[]
├── scope_change?
├── limitation_change refs[]
├── decision
├── claim_after_ref?
├── rationale
└── provenance
```

Conceptual decisions:

```text
keep
strengthen_within_scope
narrow_scope
weaken
mark_inconclusive
mark_unsupported_within_scope
supersede
withdraw
```

---

# 13. ClaimSupersessionRecord

```text
ClaimSupersessionRecord
├── supersession_id
├── old_claim_ref
├── new_claim_ref
├── reason
├── evidence_refs[]
├── semantic_difference
└── provenance
```

Supersession не удаляет old claim.

---

# 14. NegativeResultRecord

```text
NegativeResultRecord
├── result_id
├── study/run/contrast refs[]
├── target_hypothesis/claim refs[]
├── result_class
├── effect/uncertainty refs[]
├── sensitivity/power notes[]?
├── validity_ref
├── interpretation
└── provenance
```

Conceptual result classes:

```text
negative_evidence
null_estimate
inconclusive
invalid
not_measured
```

Они не сворачиваются в один boolean `failed`.

---

# 15. ModuleGateOutcome

```text
ModuleGateOutcome
├── gate_ref
├── study/evidence refs[]
├── support_criteria_results[]
├── weakening/falsification_criteria_results[]
├── validity_ref
├── outcome
├── triggered_claim_reviews[]
├── design_review_required?
└── provenance
```

ModuleGateOutcome сам не изменяет accepted ADR автоматически.

---

# 16. GeneralizationClaimSpec

```text
GeneralizationClaimSpec
├── source_scope_ref
├── target_scope_ref
├── shift_dimensions[]
├── transfer_evidence_refs[]
├── unchanged/matched factors[]
├── changed factors[]
├── failure/exclusion semantics
└── provenance
```

Claim не распространяется на untested target scope молча.

---

# 17. CausalClaimSupportSpec

```text
CausalClaimSupportSpec
├── claim_ref
├── intervention/contrast refs[]
├── base-state alignment refs[]
├── target_effect refs[]
├── off_target_effect refs[]
├── control/matching refs[]
├── confounder assessment[]
├── replication refs[]
├── causal limitations[]
└── provenance
```

---

# 18. ArchitectureContributionClaimSpec

```text
ArchitectureContributionClaimSpec
├── semantic_boundary_ref
├── tested_implementation refs[]
├── matched semantic/control refs[]
├── Cortex/world/seed transfer refs[]
├── capacity/compute matching refs[]
├── module_gate_ref?
├── known implementation confounds[]
└── provenance
```

Одна concrete implementation не доказывает architecture-level universality автоматически.

---

# 19. ConsciousnessClaimBoundaryRecord

```text
ConsciousnessClaimBoundaryRecord
├── boundary_id
├── functional_evidence_refs[]
├── phenomenological_bridge_evidence_refs[]
├── current_statement
├── unsupported_inferences[]
├── scope/limitations
└── provenance
```

Default для текущего MINDRA design:

```text
phenomenological_bridge_evidence = unavailable
```

Это не утверждает отсутствие consciousness; это означает отсутствие достаточного evidence для соответствующего claim.

---

# 20. ClaimRegistry

```text
ClaimRegistry
├── registry_id
├── registry_revision
├── claim_refs[]
├── active_claim_refs[]
├── challenged_claim_refs[]
├── superseded_claim_refs[]
├── unsupported/withdrawn_claim_refs[]
├── open_review_refs[]
└── provenance
```

---

# 21. LimitationsRegistry

```text
LimitationsRegistry
├── registry_id
├── revision
├── limitation_refs[]
├── project_wide_refs[]
├── version_specific_refs[]
├── unresolved_refs[]
├── resolved_refs[]
└── provenance
```

---

# 22. ClaimWordingPolicy

```text
ClaimWordingPolicy
├── policy_id
├── revision
├── evidence_to_wording_rules[]
├── restricted_terms[]
├── required_qualifiers[]
├── unsupported_pattern_refs[]
├── domain-specific exceptions[]
└── provenance
```

Автоматический NLP linter не обязателен этим contract.

---

# 23. PublicationStatementRecord

```text
PublicationStatementRecord
├── statement_id
├── claim_revision_ref
├── publication/report ref
├── rendered_statement
├── qualifiers/limitations included[]
├── wording_policy_ref
├── review status
└── provenance
```

Publication wording не должна быть сильнее canonical claim.

---

# 24. ResearchClaimsManifest

```text
ResearchClaimsManifest
├── manifest_id
├── project/repository revision
├── ClaimRegistry ref
├── LimitationsRegistry ref
├── active unsupported-pattern policy ref
├── relevant Evaluation/Verification manifests[]
├── open known-unknown refs[]
└── provenance
```

---

# 25. Инварианты candidate contract

```text
Observation ≠ Interpretation ≠ ResearchClaim
ResearchClaim ≠ raw MetricRecord
Claim scope ≠ universal scope
engineering verified ≠ functionally useful
association ≠ causation
ablation ≠ necessity proof automatically
single implementation effect ≠ architecture-level effect
null/inconclusive/invalid ≠ same result class
unknown ≠ false
functional similarity ≠ phenomenological equivalence
Affect/Workspace/Self Model ≠ consciousness evidence automatically
supersession ≠ history rewrite
publication prose ≠ source of truth
```

---

# 26. Что contract не фиксирует

- Python classes/dataclasses;
- exact status/kind enums;
- SQL/JSON/YAML schema;
- universal numeric evidence strength;
- universal p-value/credible-interval threshold;
- exact terminology required by a journal;
- preregistration platform;
- paper/report template;
- automatic consciousness classifier;
- NLP wording linter;
- dashboard/tracker implementation.
