# Candidate contract MINDRA-Eval

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-28 — MINDRA-Eval`

Этот документ уточняет machine-facing semantic формы accepted design [`../mindra-eval.md`](../mindra-eval.md).

Он **не является frozen Python API** и не фиксирует benchmark framework, statistics library, storage backend, plotting/report stack, конкретные CI/bootstrapping routines или universal metric set.

---

# 1. Общая форма

```text
EvaluationStudyPlan
        ↓
EvaluationManifest
        ↓
EvaluationCondition[]
        ↓
EvaluationRun[]
        ↓
EvaluationUnit[]
        ↓
MetricRecord[]
        ↓
Contrast / StatisticalAnalysis
        ↓
EvaluationReport
```

Для causal studies:

```text
Verified Base State
       ↓
PairedCounterfactualPlan
       ↓
ControlBranch + TreatmentBranch
       ↓
CausalContrastRecord
```

---

# 2. EvaluationStudyPlan

```text
EvaluationStudyPlan
├── study_id
├── study_revision
├── title / purpose
├── mode                         # exploratory / confirmatory
├── hypothesis_specs[]
├── evaluation_suite_ref
├── condition_refs[]
├── primary_contrast_refs[]
├── primary_metric_refs[]
├── secondary_metric_refs[]
├── replicate_structure
├── statistical_analysis_plan
├── success_criteria[]
├── falsification_criteria[]
├── exclusion_policy
├── stopping_policy
├── reproducibility_requirement
├── created_before_outcome_evidence?
└── provenance
```

Confirmatory revision после просмотра outcome не должна masquerade как исходный preregistered plan.

---

# 3. HypothesisSpec

```text
HypothesisSpec
├── hypothesis_id
├── target_claim
├── independent_variable / intervention
├── target_outcomes[]
├── expected_direction_or_relation?
├── off_target_outcomes[]
├── scope
├── required_controls[]
├── success_criterion
├── falsification_or_weakening_criterion
└── provenance
```

`HypothesisSpec` не является Research Claim сам по себе.

---

# 4. EvaluationSuiteManifest

```text
EvaluationSuiteManifest
├── suite_id
├── suite_revision
├── task_family_refs[]
├── world_distribution_refs[]
├── split_manifest_refs[]
├── protocol_refs[]
├── metric_spec_refs[]
├── stress_shift_refs[]
├── aggregate_metric_policy_ref?
└── provenance
```

Suite version меняется при semantic изменении task/distribution/measurement protocol.

---

# 5. TaskFamilyDescriptor

```text
TaskFamilyDescriptor
├── task_family_id
├── revision
├── capability_targets[]
├── horizon_class?
├── observability_class?
├── memory_dependency?
├── planning_dependency?
├── hidden_rule_structure?
├── success_semantics
├── termination_semantics
├── evaluator_ground_truth_schema_ref?
└── provenance
```

Не является concrete Environment instance.

---

# 6. EvaluationSplitManifest

```text
EvaluationSplitManifest
├── split_id
├── train_distribution_refs[]
├── validation_distribution_refs[]
├── test_distribution_refs[]
├── held_out_rules/compositions refs[]
├── OOD/stress refs[]
├── selection_access_policy
├── contamination/exposure_notes
└── provenance
```

---

# 7. EvaluationCondition

```text
EvaluationCondition
├── condition_id
├── condition_revision
├── role                         # treatment / baseline / control / oracle / etc.
├── agent_revision_ref
├── component_revision_refs{}
├── checkpoint_ref
├── restore_profile_ref
├── cortex_condition_ref?
├── module_composition_ref
├── environment_distribution_ref
├── intervention_plan_ref?
├── action_gate/runtime_assurance_ref?
├── training_or_adaptation_mode
├── data_visibility_policy_ref
├── cognitive_resource_envelope_ref?
├── tuning_budget_ref?
├── resource_match_profile_ref?
├── determinism_policy_ref
├── software_manifest_ref
├── hardware_manifest_ref
├── compute_capture_policy_ref
├── metric_plan_ref
└── provenance
```

`condition_id` не заменяет содержимое manifests/revisions.

---

# 8. ControlDescriptor

```text
ControlDescriptor
├── control_id
├── control_kind
├── target_boundary
├── semantic_change
├── preserved_factors[]
├── intentionally_changed_factors[]
├── matching_targets[]
├── oracle_privileged?
└── provenance
```

Conceptual kinds:

```text
baseline
ablation
NoX
DummyX
ConstantX
RandomX
ShuffledX
TimePermutedX
MatchedNoiseX
MatchedCapacityX
MatchedComputeX
RuleBasedX
OracleX
```

Exact enum не frozen.

---

# 9. ResourceMatchProfile

```text
ResourceMatchProfile
├── profile_id
├── parameter_count_target?
├── trainable_parameter_target?
├── state_capacity_target?
├── context_budget_target?
├── cortex_call_target?
├── memory_capacity_target?
├── workspace_capacity_target?
├── rollout/search_budget_target?
├── training_data_target?
├── training_update_target?
├── measured_compute_target?
├── tolerances{}
├── known_unmatched_factors[]
└── provenance
```

Matching claim должен ссылаться на фактические observed values, если они доступны.

---

# 10. TuningBudgetDescriptor

```text
TuningBudgetDescriptor
├── budget_id
├── number_of_trials?
├── training_compute_budget?
├── evaluation_budget?
├── data_access_budget?
├── human_selection_budget?
├── allowed_search_space_ref?
├── selection_metric_ref?
└── provenance
```

Tuning fairness является частью comparison validity.

---

# 11. ReplicateStructure

```text
ReplicateStructure
├── training_replicates
├── checkpoint_replicates
├── world_replicates
├── episode_replicates
├── stochastic_policy_replicates
├── counterfactual_branch_replicates
├── nesting_relations[]
├── blocking_relations[]
├── independence_assumptions[]
└── provenance
```

Example:

```text
training_seed
  └── checkpoint
      └── world_seed
          └── episode
```

Nested child units не считаются independent parent units автоматически.

---

# 12. EvaluationRunRecord

```text
EvaluationRunRecord
├── run_id
├── study_ref
├── condition_ref
├── suite/task/world refs
├── base_checkpoint_ref
├── restore_record_ref
├── rng_initialization_refs[]
├── actual_agent_revision_refs[]
├── ExperienceJournal refs[]
├── Evidence/Trace refs[]
├── ComputeUsageRecord refs[]
├── status
├── completeness
├── started_logical/physical metadata
├── ended metadata
└── provenance
```

Status/completeness не сворачиваются в task success.

---

# 13. EvaluationUnitRecord

```text
EvaluationUnitRecord
├── unit_id
├── unit_kind
├── run_ref
├── parent_unit_ref?
├── source_event_refs[]
├── resolution_status
├── grouping_keys{}
├── evaluator_annotation_refs[]
└── provenance
```

Conceptual kinds:

```text
training_replicate
checkpoint
world_instance
episode
decision_window
prediction_resolution
paired_branch_pair
learning_interval
```

---

# 14. MetricSpec

```text
MetricSpec
├── metric_id
├── metric_revision
├── metric_family
├── target_semantics
├── required_inputs[]
├── required_visibility_classes[]
├── unit
├── direction                    # higher/lower/non-monotonic
├── valid_resolution_statuses[]
├── missing_censoring_policy
├── normalization_policy_ref?
├── aggregation_semantics_ref?
├── proper_scoring_semantics?
└── provenance
```

Metric name без revision недостаточен для reproducible report.

---

# 15. MetricRecord

```text
MetricRecord
├── metric_record_id
├── metric_spec_ref
├── target_unit_refs[]
├── raw_value / structured_value
├── availability_status
├── uncertainty_if_intrinsic_to_metric?
├── source_event_refs[]
├── research_annotation_refs[]
├── compute_context_ref?
└── provenance
```

`MetricRecord` не является Agent-visible state.

---

# 16. MetricBundle / EvaluationScorecard

```text
EvaluationScorecard
├── scorecard_id
├── condition/run refs
├── task_metrics[]
├── calibration_metrics[]
├── causal_metrics[]
├── robustness_metrics[]
├── resource_metrics[]
├── reproducibility_metrics[]
├── failure_unknown_metrics[]
├── optional_aggregate_score_ref?
└── provenance
```

Отсутствует mandatory universal scalar.

---

# 17. AggregateMetricPolicy

```text
AggregateMetricPolicy
├── policy_id
├── revision
├── source_metric_refs[]
├── normalization_refs[]
├── aggregation_rule
├── weights/preferences?
├── missing_policy
└── provenance
```

Aggregate score всегда derived и не удаляет source metrics.

---

# 18. StatisticalAnalysisPlan

```text
StatisticalAnalysisPlan
├── plan_id
├── revision
├── primary_metric_refs[]
├── primary_contrast_refs[]
├── analysis_unit
├── grouping/nesting_spec
├── paired_design?
├── effect_estimator_spec
├── aggregate_estimator_spec
├── uncertainty_interval_spec
├── resampling/blocking_spec?
├── multiplicity_policy_ref?
├── missing/censoring_policy
├── minimum_practical_effect?
├── equivalence/noninferiority_spec?
├── sample_size/power_policy?
├── stopping_rule
├── reporting_requirements
└── provenance
```

Ни один statistical method не является default architecture invariant.

---

# 19. StatisticalResultRecord

```text
StatisticalResultRecord
├── result_id
├── analysis_plan_ref
├── source_metric_record_refs[]
├── point/effect_estimate
├── interval/uncertainty
├── distribution_summary?
├── sample_counts_by_level{}
├── exclusions/censoring counts{}
├── multiplicity_adjustment?
├── analysis_status
└── provenance
```

---

# 20. ContrastSpec

```text
ContrastSpec
├── contrast_id
├── condition_A_ref
├── condition_B_ref
├── contrast_kind
├── matched_factors[]
├── intentionally_different_factors[]
├── primary_metric_refs[]
├── expected_effect?
└── provenance
```

---

# 21. PairedCounterfactualPlan

```text
PairedCounterfactualPlan
├── pair_plan_id
├── base_checkpoint_ref
├── required_restore_profile
├── environment_snapshot_ref
├── pending_external_effect_requirement
├── control_condition_ref
├── treatment_condition_ref
├── intervention_spec_ref
├── RNG_coupling_policy
├── allowed_divergence_policy
└── provenance
```

`execution_unknown` может сделать plan ineligible.

---

# 22. InterventionSpec

```text
InterventionSpec
├── intervention_id
├── target_boundary/state
├── intervention_kind
├── control_value?
├── treatment_value?
├── timing / causal boundary
├── expected_target_effects[]
├── monitored_off_target_effects[]
├── intervention_gateway_ref
└── provenance
```

---

# 23. CausalContrastRecord

```text
CausalContrastRecord
├── causal_contrast_id
├── contrast_spec_ref
├── base_state_ref
├── control_run/unit refs
├── treatment_run/unit refs
├── intervention_ref
├── target_effect_records[]
├── off_target_effect_records[]
├── matching_quality
├── completeness
├── statistical_result_refs[]
├── causal_assumptions[]
├── limitations[]
└── provenance
```

Не является автоматическим proof of causality вне заявленных assumptions.

---

# 24. ModuleGateSpec

```text
ModuleGateSpec
├── gate_id
├── target_boundary
├── accepted_design_ref
├── required_conditions[]
├── required_matched_controls[]
├── primary_metrics[]
├── supporting_interventions[]
├── support_criterion
├── weakening/falsification_criterion
├── design_review_trigger
└── provenance
```

Обязательные DU-28 gates минимум:

```text
Affect
Workspace
Planner
Executive Control
```

---

# 25. PolicyActionAttributionRecord

```text
PolicyActionAttributionRecord
├── selected_action_intent_ref
├── policy_quality_metric_refs[]
├── authorization_result_ref
├── gate_rejection/normalization/override refs[]
├── committed_action_ref?
├── execution_record_ref?
├── outcome_ref?
├── post_gate_metric_refs[]
└── provenance
```

Позволяет раздельно оценивать Policy, Gate и whole system.

---

# 26. CalibrationEvaluationSpec

```text
CalibrationEvaluationSpec
├── target_prediction_semantics
├── probability_field
├── resolution_event
├── horizon
├── proper_scoring_metric_refs[]
├── calibration_diagnostic_refs[]
├── discrimination_metric_refs[]
├── censoring_policy
├── grouping/stratification
└── provenance
```

Verbal confidence не считается meaningful probability без соответствующего contract/estimator.

---

# 27. ComputeComparisonSpec

```text
ComputeComparisonSpec
├── comparison_id
├── normalization_mode
├── requested_budget_refs[]
├── actual_compute_metric_refs[]
├── parameter/context/data refs[]
├── performance_metric_refs[]
├── frontier_estimator_spec?
└── provenance
```

Conceptual modes:

```text
equal_nominal_budget
equal_measured_compute
performance_at_cost
cost_at_target_performance
performance_resource_frontier
```

---

# 28. RobustnessEvaluationSpec

```text
RobustnessEvaluationSpec
├── nominal_distribution_ref
├── perturbation/shift_refs[]
├── intensity_levels[]
├── agent_visibility_semantics
├── robustness_metric_refs[]
├── resilience/recovery_metric_refs[]
└── provenance
```

---

# 29. AdaptationEvaluationSpec

```text
AdaptationEvaluationSpec
├── pre_adaptation_eval_ref
├── adaptation_interaction/data_budget
├── allowed_learning_update_policy
├── adaptation_compute_budget
├── post_adaptation_eval_ref
├── retention_eval_ref
├── leakage/isolation_policy
└── provenance
```

Обычная fixed evaluation не активирует Learning Updates.

---

# 30. EvaluationValidityRecord

```text
EvaluationValidityRecord
├── run_or_study_ref
├── validity_status
├── violated_assumptions[]
├── leakage_detected?
├── checkpoint_integrity_status
├── condition_drift?
├── missing_required_artifacts[]
├── undeclared_resource_differences[]
└── provenance
```

Invalid run не эквивалентен failed task.

---

# 31. EvaluationManifest

```text
EvaluationManifest
├── manifest_id
├── manifest_revision
├── study_plan_ref
├── suite_ref
├── condition_refs[]
├── control_refs[]
├── task/world/split refs[]
├── checkpoint/restore refs[]
├── intervention refs[]
├── metric refs[]
├── replicate_structure_ref
├── statistical_plan_ref
├── resource_match/tuning refs[]
├── reproducibility requirements
└── provenance
```

---

# 32. EvaluationReport

```text
EvaluationReport
├── report_id
├── report_revision
├── evaluation_manifest_ref
├── run_refs[]
├── scorecards[]
├── statistical_results[]
├── causal_contrast_records[]
├── module_gate_results[]
├── validity_summary
├── compute_summary
├── reproducibility_claim_refs[]
├── limitations[]
├── exploratory_findings[]
└── source_artifact_refs[]
```

Report является derived artifact; raw records не переписываются.

---

# 33. CausalEvidenceLevel

Conceptual ordered semantics:

```text
descriptive
predictive
ablation_control
matched_intervention
replicated_generalized_causal
```

Exact labels/order могут измениться до contract freeze.

Claim не должен иметь evidence level выше supporting records.

---

# 34. EvaluationStatus

Conceptual statuses могут включать:

```text
complete
partial
censored
execution_unknown
causal_gap
artifact_missing
invalid_condition
aborted
metric_unavailable
```

Exact enum не frozen.

---

# 35. Availability / unknown semantics

Нельзя использовать одну numeric sentinel, например `0`, для:

- failed metric;
- unavailable metric;
- censored outcome;
- unresolved action;
- actual measured zero.

Availability/status являются отдельной частью contract.

---

# 36. Privileged evaluator semantics

```text
Evaluator Ground Truth
≠ Agent-visible data
```

Любой `MetricSpec`, использующий Research Plane / ResearchAnnotation, имеет explicit `required_visibility_classes` и не должен делать эти данные доступными Agent.

---

# 37. Invariants candidate contract

1. Evaluation entity identities versioned.
2. Condition полностью ссылается на checkpoint/world/resource/software/hardware context.
3. Experimental unit и statistical analysis unit explicit.
4. Nested units не объявляются independent автоматически.
5. Metric source/provenance traceable.
6. Aggregate score derived; source metrics сохраняются.
7. Causal intervention хранит base state и control/treatment lineage.
8. Matched-control claim хранит фактические matched/unmatched factors.
9. `execution_unknown` не становится success/failure без policy.
10. Invalid run не считается task failure.
11. Policy pre-Gate и system post-Gate metrics separate.
12. Privileged evaluator data не становится cognition input.
13. Actual compute provenance сохраняется для efficiency claims.
14. Module gates имеют negative criteria.
15. Statistical plan versioned и связан с source results.
16. Report имеет lineage до raw run/metric/evidence artifacts.

---

# 38. Что намеренно не frozen

- Python classes/Protocols/dataclasses;
- storage schema;
- benchmark engine;
- distributed runner;
- metrics library;
- statistical test/CI implementation;
- exact CausalEvidenceLevel enum;
- seed count;
- p-value threshold;
- Brier/NLL/ECE mandatory set;
- rliable or other statistics package;
- experiment tracker;
- visualization/dashboard;
- composite score;
- concrete MicroWorld tasks.
