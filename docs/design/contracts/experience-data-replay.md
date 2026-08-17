# Candidate contract Experience / Data / Replay MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-25 — Experience / Data / Replay`

Этот документ уточняет machine-facing semantic формы accepted design [`../experience-data-replay.md`](../experience-data-replay.md).

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC/dataclass/Pydantic/TensorDict;
- JSONL/Arrow/Parquet/HDF5/TFRecord/SQLite/PostgreSQL;
- RLDS/Minari/Reverb/TorchRL как обязательный backend;
- exact event enum;
- exact field encoding nullable/union types;
- concrete replay algorithm;
- reward definition;
- checkpoint encoding;
- optimizer/training batch semantics.

---

# 1. Общая machine-facing форма

```text
Runtime / Environment / Agent
        ↓
ExperienceEvent
        ↓
ExperienceJournal
        ↓
ProjectionSpec
        ↓
TrajectoryProjection / DatasetManifest
        ↓
SampleTransformationRecord
        ↓
TrainingSample
        ↓
ReplayItem / ReplaySelectionRecord
        ↓
DU-26 Training Runtime
```

Research Ground Truth проходит отдельной веткой:

```text
Evaluation / Research Plane
        ↓
ResearchAnnotationRecord
        ↓
explicit visibility policy
        ↓
optional privileged derived dataset
```

---

# 2. ExperienceEventEnvelope

Conceptual fields:

```text
ExperienceEventEnvelope
├── event_id
├── event_schema_id
├── event_schema_revision
├── event_kind
├── lineage_id
├── causal_parent_ids[]
├── logical_scope
├── producer_boundary
├── source_mode
├── execution_context
├── intervention_refs[]
├── visibility_class
├── trust_class
├── revision_set_ref / inline revision set
├── semantic_payload
├── payload_schema_id / revision
├── trace_refs[]
├── artifact_refs[]
├── integrity_status
└── provenance
```

`semantic_payload` может быть inline либо reference-backed.

---

# 3. LogicalScope

```text
LogicalScope
├── run_id
├── agent_session_id
├── episode_id
├── decision_window_id
├── cognitive_cycle_id
├── wave_id
├── module_attempt_id
├── environment_transition_id
├── replay_step_id
├── consolidation_event_id
└── learning_update_id
```

Каждое поле имеет explicit applicability/availability semantics.

Не применять обычный `null` как единственный способ различить:

```text
not_applicable
unknown
unavailable
missing
```

---

# 4. CausalRevisionSet

```text
CausalRevisionSet
├── agent_revision
├── state_revision
├── memory_revision
├── world_model_revision
├── world_belief_revision
├── self_model_revision
├── self_belief_revision
├── goal_revision
├── drive_revision
├── affect_revision
├── valuation_revision?
├── salience_revision?
├── workspace_revision
├── executive_revision
├── policy_revision
├── planner_revision
├── action_boundary_revision
├── environment_revision
├── world_manifest_ref
├── representation_revision_refs[]
└── provenance
```

Конкретный event обязан нести только causally relevant subset либо reference на shared immutable revision bundle.

---

# 5. SourceMode / provenance dimensions

Не использовать один универсальный комбинированный enum для всех условий.

Conceptually:

```text
RealityMode
├── actual
├── imagined
├── memory_reactivation
├── training_replay
└── counterfactual

InterventionContext
├── natural
└── intervention_refs[]

ExecutionContext
├── normal_runtime
├── evaluation
├── offline_processing
└── training
```

Exact labels могут измениться, но ортогональные dimensions должны сохраняться.

---

# 6. ProducerBoundary

Conceptual values/refs:

```text
agent
agent_runtime_core
environment
execution_runtime
training_runtime
evaluation_runtime
experience_recorder
dataset_builder
artifact_collector
```

Producer identity не повышает factual authority автоматически.

---

# 7. VisibilityClass

Minimum semantic classes:

```text
agent_visible
agent_generated_private_evidence
research_only
training_only
public_exportable
restricted
```

Точные security classes не frozen.

Главное правило:

```text
research_only
→ не включать в normal agent-visible training projection
  без explicit policy
```

---

# 8. IntegrityStatus

Conceptual structure:

```text
IntegrityStatus
├── overall_status
├── required_causal_links_complete
├── payload_status
├── artifact_status
├── schema_status
├── unresolved_refs[]
├── reconstruction_refs[]
└── notes/provenance
```

Possible semantic states include:

```text
complete
partial
unresolved
corrupt
causal_gap
required_payload_missing
optional_artifact_missing
schema_unsupported
```

Точные enum names не frozen.

---

# 9. ArtifactRef

```text
ArtifactRef
├── artifact_id
├── artifact_schema_id / revision
├── content_identity / hash?
├── media/semantic kind
├── codec/format descriptor
├── logical owner
├── size metadata
├── storage reference abstraction
├── availability
├── integrity
├── lossy/lossless status
└── provenance
```

Provider-native path/URL не должен становиться canonical semantic identity.

---

# 10. ExperienceJournalManifest

```text
ExperienceJournalManifest
├── journal_id
├── journal_revision
├── event_schema_registry_revision
├── included event ranges/partitions
├── first/last logical scope refs
├── environment/world manifests[]
├── agent/session manifests[]
├── storage backend descriptor ref
├── completeness summary
├── late/unresolved event summary
├── created/updated metadata
└── provenance
```

`journal_revision` меняется при добавлении событий, но старые `event_id` и смысл source events не изменяются.

---

# 11. ExperienceEventKindRegistry

Registry conceptually связывает:

```text
event_kind
→ payload schema id/revision
→ required scope fields
→ required causal parents
→ visibility defaults
→ minimum integrity requirements
```

Registry versioned.

Новый payload field не должен молча менять смысл старого `event_kind`.

---

# 12. Core interaction event references

Contract должен позволять выразить ссылки минимум на:

```text
ObservationCommitEvent
OutcomeCommitEvent
StateCommitEvent/Reference
ExecutiveDecisionEvent
PolicyCandidateSetEvent
PolicySelectionEvent
DecisionDeferralEvent
ActionAuthorizationEvent
ActionCommitEvent
DispatchAttemptEvent
ActionExecutionEvent
DispatchReconciliationEvent
EnvironmentTransitionEvent
EpisodeLifecycleEvent
InterventionEvent
```

Exact class names/enums не frozen.

---

# 13. ResearchAnnotationRecord

```text
ResearchAnnotationRecord
├── annotation_id
├── annotation_schema_id / revision
├── target_event_refs[]
├── target_projection/sample refs[]
├── source_boundary
├── trust class
├── visibility = research_only by default
├── payload / artifact refs
├── annotation method/revision
├── uncertainty/support
└── provenance
```

Annotation не мутирует target event.

Examples:

```text
hidden world state
oracle success
shortest path
solver label
counterfactual oracle
manual annotation
```

---

# 14. DataVisibilityPolicy

```text
DataVisibilityPolicy
├── policy_id
├── policy_revision
├── allowed visibility classes
├── allowed annotation classes
├── privileged supervision flag
├── field/artifact inclusion rules
├── redaction rules refs[]
└── provenance
```

Default normal cognitive/training claim policy не включает research-only данные.

---

# 15. ProjectionSpec

```text
ProjectionSpec
├── projection_id
├── projection_revision
├── source_journal_manifest_refs[]
├── projection_kind
├── event selectors
├── causal-order policy
├── grouping policy
├── field/materialization policy
├── visibility policy ref
├── completeness requirements
├── transform chain refs[]
├── representation policy
├── deterministic extraction config
└── provenance
```

---

# 16. EpisodeTrajectory

```text
EpisodeTrajectory
├── trajectory_id
├── source journal manifest ref
├── episode_id
├── environment/world manifest ref
├── ordered causal spine refs[]
├── decision_window_refs[]
├── terminal/truncated status
├── lifecycle/failure status
├── source agent revision summary
├── intervention refs[]
├── completeness status
└── provenance
```

Episode trajectory не обязана inline-копировать все events.

---

# 17. DecisionTrajectory

```text
DecisionTrajectory
├── decision_trajectory_id
├── decision_window_id
├── input observation/outcome refs
├── base/final state revisions
├── executive-decision refs[]
├── workspace/planner/policy evidence refs[]
├── selected_intent_ref?
├── decision_deferral_refs[]
├── authorization_ref?
├── action_commit_ref?
├── dispatch/execution refs[]
├── environment_transition_ref?
├── outcome_ref?
├── completeness
└── provenance
```

---

# 18. InteractionTransitionView

```text
InteractionTransitionView
├── transition_view_id
├── source event refs[]
├── observation/state-before refs
├── selected_intent_ref?
├── committed_action_ref?
├── execution_status
├── environment_transition_ref?
├── outcome/next-observation refs?
├── external feedback refs[]
├── terminated
├── truncated
├── behavior revision refs
├── processing revision refs
├── intervention refs[]
├── completeness
└── provenance
```

Допускается:

```text
action_commit_ref present
environment_transition_ref unavailable
```

---

# 19. DatasetManifest

```text
DatasetManifest
├── dataset_id
├── dataset_revision
├── dataset_kind
├── source journal manifests[]
├── source trajectory/projection refs[]
├── environment distribution/manifests[]
├── source agent revisions[] / heterogeneity descriptor
├── projection spec ref
├── visibility policy ref
├── transform chain
├── schema registry revisions
├── representation/feature-space revisions
├── split policy/ref
├── deterministic sampling config
├── required artifacts
├── completeness/quality requirements
├── sensitivity/license/access refs, если применимо
└── provenance
```

---

# 20. SampleTransformationRecord

```text
SampleTransformationRecord
├── transform_event_id
├── transform_id
├── transform_revision
├── transform_kind
├── source event/projection/sample refs[]
├── configuration
├── RNG semantics
├── output sample/artifact refs[]
├── lossless/lossy status
├── privileged-input usage
└── provenance
```

Examples:

```text
window extraction
hindsight goal relabel
reward/target recomputation
n-step return
feature re-encoding
masking
negative sampling
sequence packing
normalization
```

---

# 21. TrainingSample

```text
TrainingSample
├── sample_id
├── sample_schema_id / revision
├── sample_kind
├── source refs[]
├── transform lineage refs[]
├── input fields / artifact refs
├── target fields / artifact refs
├── mask/availability fields
├── behavior revision refs
├── representation revisions
├── visibility/privileged status
├── split identity
├── quality/completeness
└── provenance
```

`TrainingSample` никогда не становится source historical event.

---

# 22. HindsightRelabelRecord

Specialized derived transform conceptually:

```text
HindsightRelabelRecord
├── transform ref
├── source trajectory/sample refs
├── original_goal_ref
├── relabeled_goal representation/ref
├── achieved outcome refs
├── original external feedback refs
├── recomputed target/reward refs
├── relabel strategy/revision
└── provenance
```

Original Goal/source experience остаются неизменными.

---

# 23. Reward / target mapping

Source Experience Event не обязан иметь universal `reward` field.

Derived training target mapping:

```text
TrainingTargetMapping
├── mapping_id
├── mapping_revision
├── source evidence classes
├── target semantics
├── privileged inputs used?
├── normalization/discount semantics
└── provenance
```

Potential source evidence:

```text
External Task Feedback
Goal outcome
Intrinsic Signal
Value component
research annotation
```

Но любое включение является explicit training design, не automatic equivalence.

---

# 24. ReplayItem

```text
ReplayItem
├── replay_item_id
├── source sample/projection refs[]
├── insertion event/ref
├── replay-table/buffer revision ref
├── priority metadata?
├── sequence/window metadata?
├── expiration/removal metadata?
└── provenance
```

ReplayItem — derived training infrastructure object, не source ExperienceEvent и не Agent MemoryRecord.

---

# 25. ReplaySelectionRecord

```text
ReplaySelectionRecord
├── replay_step_id
├── replay_runtime/table id/revision
├── sampler_id / revision
├── source population manifest/revision
├── selected replay_item/sample refs[]
├── selection priorities?
├── sampling probabilities?
├── importance weights?
├── RNG seed/state semantics
├── training consumer ref
├── actual selection status
└── provenance
```

Sampling probability/importance weights обязательны только если алгоритм их определяет.

---

# 26. Replay distinction

Contract обязан различать owner/event kinds:

```text
AgentMemoryReplayRecord
≠
TrainingReplaySelectionRecord
```

Даже если они ссылаются на один source episode.

---

# 27. ExecutionGapRecord / unresolved action

Для action без подтверждённого transition нужна expressible semantics:

```text
ExecutionGapRecord
├── action_commit_ref
├── dispatch_attempt_refs[]
├── current execution status
├── definitely_not_sent evidence?
├── execution_unknown evidence?
├── partial execution evidence?
├── reconciliation refs[]
├── environment transition ref?
├── resolution status
└── provenance
```

Не fabricatе next observation/state.

---

# 28. DataSplitDescriptor

```text
DataSplitDescriptor
├── split_id
├── split_revision
├── split_name/role
├── source grouping unit
├── environment distribution refs
├── world/episode/session grouping rules
├── holdout criteria
├── leakage constraints
├── assignment method/RNG
└── provenance
```

Exact evaluation split policy определяется позднее в `DU-28`.

---

# 29. SchemaMigrationRecord

```text
SchemaMigrationRecord
├── migration_id
├── migration_revision
├── source schema id/revision
├── target schema id/revision
├── source manifest refs
├── output manifest refs
├── migration semantics
├── lossless/lossy status
├── validation result
└── provenance
```

Migration не меняет исторический смысл source event.

---

# 30. ReconstructionRecord

Если потерянный/неполный event post-hoc восстанавливается:

```text
ReconstructionRecord
├── reconstruction_id
├── target missing concept/ref
├── source evidence refs[]
├── reconstruction method/revision
├── uncertainty/support
├── generated derived payload/ref
└── provenance
```

Reconstructed record не получает identity оригинального события, которого фактически не было в journal.

---

# 31. DeterministicExtractionDescriptor

```text
DeterministicExtractionDescriptor
├── extractor_id/revision
├── source manifest revision
├── ordering/grouping policy
├── filters
├── shuffle policy
├── RNG algorithm/seed/state semantics
├── distributed determinism level
└── provenance
```

`seed` без source/extractor revision недостаточен для воспроизводимости.

---

# 32. SnapshotReference

Experience layer может ссылаться на future `DU-27` snapshot descriptors:

```text
SnapshotReference
├── snapshot_id
├── snapshot_kind
├── causal position/event refs
├── agent/environment identity
├── snapshot schema revision
├── completeness capability
└── artifact ref
```

`DU-25` не задаёт binary snapshot format.

---

# 33. DataSensitivityDescriptor

Зарезервирован для future external/human data:

```text
DataSensitivityDescriptor
├── sensitivity_class
├── access policy ref
├── source/license/consent refs, если применимо
├── redaction/anonymization transform refs[]
└── provenance
```

Не обязателен для первой MicroWorld версии.

---

# 34. Candidate capabilities

Future `ExperienceDataStore`/service surface conceptually может поддерживать:

```text
append validated event
read events by refs/scopes
resolve causal parents
freeze journal manifest
build projection
build dataset
validate completeness
resolve artifact refs
attach research annotation
apply explicit transformation
sample/replay via training boundary
snapshot/store metadata
```

Но exact service topology и API не frozen.

---

# 35. Failure semantics

Нужно различать как минимум:

```text
event_validation_failed
journal_append_failed
artifact_write_failed
late_event
causal_parent_unresolved
schema_unsupported
projection_failed
visibility_policy_violation
dataset_incomplete
replay_population_changed
sample_extraction_failed
```

Data failure не должен masquerade как Agent cognitive failure.

---

# 36. Автоматически проверяемые invariants

1. source `event_id` immutable/unique;
2. event kind согласован с payload schema;
3. required causal parent links валидны либо integrity явно degraded;
4. source event не переписывается transform'ом;
5. derived sample имеет source + transform lineage;
6. `ResearchAnnotationRecord` не включается normal training projection без explicit visibility policy;
7. action commit без Environment transition валиден;
8. `execution_unknown` не равен `not_executed`;
9. terminated/truncated различаются;
10. replay selection не создаёт actual Environment event;
11. Memory Replay owner отличается от Training Replay owner;
12. mixed behavior revisions сохраняются;
13. feature-space revisions не теряются при re-encoding;
14. dataset manifest фиксирует source selection;
15. lossy transform маркируется;
16. split/group provenance сохраняется;
17. storage append order не подменяет causal order;
18. privileged feature leakage detectable;
19. missing core causal links влияют на completeness;
20. transformation/replay RNG provenance доступна там, где требуется reproducibility.

---

# 37. Что намеренно остаётся открытым

До `DU-26 … DU-32` не frozen:

```text
storage engine
file formats
partitioning
index/database technology
exact event enum
exact Python types
batch/sample tensor layout
reward/return definition
replay prioritization
sequence lengths
n-step horizons
sampling APIs
data-loader framework
checkpoint payload format
public dataset export format
```

Иерархия остаётся:

```text
accepted design + ADR
→ candidate contract
→ version specification
→ implementation sequence
→ implementation
```
