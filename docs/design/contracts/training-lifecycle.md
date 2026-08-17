# Candidate contract Training Lifecycle MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-26 — Training Lifecycle`

Этот документ уточняет machine-facing semantic формы accepted design [`../training-lifecycle.md`](../training-lifecycle.md).

Он **не является frozen Python API** и не фиксирует PyTorch/JAX, конкретный Trainer, optimizer, RL/SFT algorithm, LoRA/QLoRA/full fine-tuning, tensor shapes, batch size, lr, checkpoint format или distributed topology.

---

# 1. Общая machine-facing форма

```text
DatasetManifest / ReplaySelection
        ↓
TrainingPlan
        ↓
TrainingAttempt
        ↓
CandidateRevisionBundle
        ↓
ValidationResult
        ↓
LearningUpdateRecord
        ↓
RevisionActivationRecord
        ↓
Active AgentRevision
```

---

# 2. TrainableComponentDescriptor

```text
TrainableComponentDescriptor
├── component_id
├── component_kind
├── component_revision
├── parameter_topology_ref
├── trainable_capabilities[]
├── allowed_training_modes[]
├── parameter_group_refs[]
├── gradient_boundary_descriptor_ref
├── input/output contract revisions
├── activation_constraints[]
├── representation_effects[]
└── provenance
```

---

# 3. ParameterGroupDescriptor

```text
ParameterGroupDescriptor
├── parameter_group_id
├── owner_component_id
├── topology_revision
├── parameter_selector semantics
├── trainable / frozen status
├── shared_parameter_refs[]
├── optimizer ownership constraints
└── provenance
```

Один parameter group не должен иметь конфликтующих независимых optimizer owners без explicit coordination policy.

---

# 4. BaseRevisionBundle

```text
BaseRevisionBundle
├── agent_revision
├── component_revisions{}
├── parameter_topology_revisions{}
├── representation_revision_refs[]
├── contract_revision_refs[]
├── compatibility_manifest_ref
└── provenance
```

TrainingAttempt pin'ит этот bundle.

---

# 5. TrainingPlan

```text
TrainingPlan
├── training_plan_id / revision
├── training_mode
├── target_component_ids[]
├── base_revision_policy
├── dataset_manifest_refs[]
├── replay_source_policy?
├── data_visibility_policy_ref
├── training_objective_spec_ref
├── training_target_mapping_refs[]
├── optimizer_policy_ref
├── gradient_flow_policy_ref
├── training_schedule/budget_ref
├── validation_policy_ref
├── activation_policy_ref
├── continual_retention_policy_ref?
├── determinism_policy_ref
├── privileged_supervision flag
└── provenance
```

`TrainingPlan` не является Agent Goal.

---

# 6. TrainingMode

Minimum semantic distinction:

```text
offline
interleaved_online
decoupled_online
research_supervised
```

Supervised/self-supervised/RL/distillation/adaptation могут быть orthogonal method/objective descriptors.

---

# 7. TrainingObjectiveSpec

```text
TrainingObjectiveSpec
├── objective_id / revision
├── objective_kind
├── loss_component_specs[]
├── aggregation/coordination policy ref
├── required sample fields
├── target mappings[]
├── privileged inputs used?
├── normalization semantics
├── temporal/discount semantics?
└── provenance
```

`TrainingObjectiveSpec ≠ ValueProfile ≠ Agent Goal`.

---

# 8. LossComponentSpec / LossBundle

```text
LossComponentSpec
├── loss_component_id
├── semantic target
├── estimator/loss family descriptor
├── source field refs
├── target field refs
├── mask/availability semantics
├── weighting/constraint metadata?
└── provenance
```

`LossBundle` сохраняет component results и explicit aggregation/gradient-coordination result. Mandatory simple weighted sum не требуется.

---

# 9. GradientFlowPolicy

```text
GradientFlowPolicy
├── policy_id / revision
├── trainable parameter groups[]
├── allowed cross-component gradient edges[]
├── explicit stop-gradient boundaries[]
├── shared parameter coordination rules[]
├── joint-update groups[]
└── provenance
```

Runtime dependency graph не определяет gradient graph автоматически.

---

# 10. OptimizerPolicyDescriptor

```text
OptimizerPolicyDescriptor
├── optimizer_policy_id / revision
├── optimizer lineages[]
├── parameter_group assignments
├── state initialization policy
├── state migration/reset policy
├── update coordination semantics
├── scheduler semantics?
├── precision/scaler semantics?
└── provenance
```

Concrete optimizer остаётся version-level choice.

---

# 11. TrainingAttempt

```text
TrainingAttempt
├── training_attempt_id
├── training_plan_ref
├── base_revision_bundle
├── dataset/replay selection refs[]
├── sample/batch manifest refs[]
├── optimizer-state lineage refs[]
├── training logical scope
├── RNG manifest/ref
├── resource evidence refs[]
├── status
└── provenance
```

TrainingAttempt может содержать множество internal optimizer/minibatch steps.

---

# 12. TrainingStepRecord

Optional normalized evidence:

```text
TrainingStepRecord
├── training_step_id
├── training_attempt_id
├── source sample refs[]
├── objective/loss refs
├── gradient statistics refs?
├── optimizer lineage/revision
├── parameter base/candidate refs
├── numerical status
├── resource evidence refs
└── provenance
```

---

# 13. CandidateComponentRevision

```text
CandidateComponentRevision
├── component_id
├── base_component_revision
├── candidate_component_revision
├── parameter_artifact_ref
├── parameter_topology_revision
├── representation_effect_descriptor?
├── compatibility claims[]
├── training_attempt_ref
└── provenance
```

---

# 14. CandidateRevisionBundle

```text
CandidateRevisionBundle
├── candidate_bundle_id
├── base_revision_bundle
├── candidate_component_revisions[]
├── unchanged component refs[]
├── compatibility_manifest
├── required migration actions[]
├── activation atomicity group
├── status
└── provenance
```

Candidate bundle ещё не active Agent.

---

# 15. RepresentationEffectDescriptor

```text
RepresentationEffectDescriptor
├── affected feature_space_ids[]
├── old revisions[]
├── new revisions[]
├── compatibility status
├── downstream affected components[]
├── Memory representation impact
├── migration/re-encoding requirements[]
└── provenance
```

---

# 16. ValidationPolicyDescriptor / ValidationResult

```text
ValidationPolicyDescriptor
├── policy_id / revision
├── numerical checks[]
├── contract/schema checks[]
├── smoke/capability checks[]
├── representation compatibility checks[]
├── retention/regression checks[]
├── acceptance rules
└── provenance
```

```text
ValidationResult
├── validation_id
├── candidate_bundle_ref
├── policy_ref
├── check results[]
├── accepted / rejected / inconclusive
├── failure reasons[]
├── artifact/metric refs[]
└── provenance
```

Exact evaluation metrics — `DU-28`.

---

# 17. LearningUpdateRecord

```text
LearningUpdateRecord
├── learning_update_id
├── training_attempt_ref
├── training_plan_ref
├── base_revision_bundle
├── source dataset/replay refs[]
├── source sample/transform refs[]
├── objective/optimizer/gradient policy refs
├── candidate_revision_bundle_ref
├── validation_result_refs[]
├── privileged_supervision status
├── RNG/determinism refs
├── training metrics refs[]
├── artifact refs[]
├── final update status
└── provenance
```

`LearningUpdateRecord` не означает automatic activation.

---

# 18. AgentRevisionManifest

```text
AgentRevisionManifest
├── agent_revision
├── component_revisions{}
├── Cortex base/adapter revisions
├── parameter topology refs[]
├── representation revisions[]
├── contract/config refs[]
├── compatibility manifest ref
├── parent agent revision(s)
├── originating learning update refs[]
└── provenance
```

---

# 19. RevisionActivationPolicy / Record

```text
RevisionActivationPolicy
├── policy_id / revision
├── safe activation boundary
├── compatibility requirements
├── migration prerequisites
├── in-flight handling semantics
├── fallback/rollback policy ref
└── provenance
```

```text
RevisionActivationRecord
├── activation_id
├── previous_agent_revision
├── activated_agent_revision
├── candidate_bundle_ref
├── learning_update_ref?
├── activation_policy_ref
├── logical activation boundary
├── in-flight pinned revision summary
├── migration/degradation refs[]
├── activation status
└── provenance
```

Activation не переписывает in-flight causal segment.

---

# 20. BehaviorRevisionDescriptor

```text
BehaviorRevisionDescriptor
├── source sample/trajectory refs[]
├── behavior agent/policy revision
├── learner target revision
├── policy-lag descriptor?
├── compatibility/on-policy status
├── correction policy ref?
└── provenance
```

Exact off-policy correction formula не frozen.

---

# 21. PrivilegedSupervisionDescriptor

```text
PrivilegedSupervisionDescriptor
├── enabled
├── ResearchAnnotation classes used[]
├── visibility policy ref
├── target mappings[]
├── permitted claim scope
└── provenance
```

Default natural-learning condition: `enabled = false`.

---

# 22. ContinualRetentionPolicy

```text
ContinualRetentionPolicy
├── policy_id / revision
├── prior capability/task references[]
├── retained datasets/evaluation refs[]
├── drift diagnostics[]
├── regularization/replay/freeze strategy descriptors[]
├── acceptance/failure semantics
└── provenance
```

Concrete continual-learning method не frozen.

---

# 23. OptimizerStateLineage

```text
OptimizerStateLineage
├── optimizer_lineage_id
├── optimizer policy/revision
├── parameter topology revision
├── base state/artifact ref
├── compatible component revisions[]
├── migration/reset events[]
├── current training-only state ref
└── provenance
```

Optimizer state не является cognitive state.

---

# 24. Failure / rollback

```text
TrainingFailureRecord
├── failure_id
├── training_attempt/update ref
├── failure_kind
├── stage
├── affected candidate refs[]
├── live agent affected? default false
├── recovery/retry refs[]
└── provenance
```

```text
RollbackRecord
├── rollback_id
├── from_active_agent_revision
├── target revision/bundle
├── trigger evidence
├── originating update refs[]
├── rollback activation ref
└── provenance
```

Rollback не удаляет старые update/activation records.

---

# 25. DeterminismManifest

```text
DeterminismManifest
├── data sampling RNG
├── replay RNG
├── transform/augmentation RNG
├── parameter initialization RNG
├── stochastic model RNG
├── optimizer stochasticity refs
├── framework/hardware determinism claims
└── provenance
```

Полная reproducibility semantics — `DU-27`.

---

# 26. Checkpoint requirements emitted by DU-26

Будущий checkpoint должен уметь связать минимум:

```text
active AgentRevisionManifest
candidate revision bundles, если resume training требуется
TrainingPlan/Attempt
OptimizerStateLineage
scheduler/scaler/trainer state
RNG manifests
replay/sample cursor refs
validation/activation state
```

---

# 27. Проверяемые invariants

```text
LearningUpdate ≠ RuntimeStateUpdate
LearningUpdate ≠ ConsolidationEvent
ReplaySelection ≠ LearningUpdate
Training Runtime ≠ cognitive module
optimizer state ≠ CognitiveState
base revision pinned
source samples traceable
privileged inputs explicit
candidate revision ≠ active revision
activation occurs only at allowed boundary
in-flight decision revision unchanged
joint revision bundle activated atomically
stale base not silently rebased
representation-breaking update not silently activated
failed candidate does not mutate live Agent
rollback preserves historical update evidence
training metrics do not leak into cognition automatically
```
