# Candidate contract Checkpoint / Reproducibility / Compute MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-27 — Checkpoint / Reproducibility / Compute`

Этот документ уточняет machine-facing semantic формы accepted design [`../checkpoint-reproducibility-compute.md`](../checkpoint-reproducibility-compute.md).

Он **не является frozen Python API** и не фиксирует tensor format, serialization library, hash algorithm, storage backend, compression, distributed checkpoint framework, profiler или container technology.

---

# 1. Общая форма

```text
runtime/training state
        ↓
CheckpointCaptureRequest
        ↓
CaptureBoundary
        ↓
CheckpointAttempt
        ↓
ArtifactPlan
        ↓
materialize + verify
        ↓
CheckpointManifest
        ↓
RestoreRequest
        ↓
RestoreRecord
```

Отдельно:

```text
CheckpointManifest
+
ExperimentManifest
+
ComputeManifest
+
ReproducibilityClaim
```

описывают воспроизводимый experiment condition.

---

# 2. AgentSnapshotDescriptor

```text
AgentSnapshotDescriptor
├── snapshot_id
├── logical_time
├── agent_revision
├── component_revisions{}
├── cognitive_state_revision
├── state_component_refs[]
├── private_state_refs[]
├── memory_snapshot_ref?
├── workspace_snapshot_ref?
├── executive_snapshot_ref?
├── policy_planner_snapshot_ref?
├── action_boundary_state_ref?
├── rng_state_refs[]
├── compatibility_manifest_refs[]
└── provenance
```

Это semantic descriptor, не обязательный persistent file.

---

# 3. CheckpointScope

```text
CheckpointScope
├── scope_id / kind
├── intended_use
├── required_state_classes[]
├── optional_state_classes[]
├── environment_included?
├── training_state_included?
├── pending_external_state_policy
└── restore_claim_ceiling
```

Conceptual kinds:

```text
agent_inference
agent_exact_state
training_resume
full_system_resume
research_archive
```

Exact enum не frozen.

---

# 4. CheckpointCaptureRequest

```text
CheckpointCaptureRequest
├── checkpoint_attempt_id
├── requested_scope
├── requested_capture_policy
├── target logical scope
├── active revision refs
├── include candidate revisions?
├── include Environment?
├── include Training Runtime?
├── requested reproducibility level
├── storage/artifact policy ref
├── timeout/resource policy
└── provenance
```

---

# 5. CaptureBoundary

```text
CaptureBoundary
├── boundary_id
├── logical_time
├── decision_window_id?
├── cognitive_cycle_id?
├── environment_transition_id?
├── training_attempt_id?
├── committed revisions{}
├── pending action status
├── pending training status
├── capture capability
└── provenance
```

Checkpoint обязан pin'ить конкретную committed causal boundary.

---

# 6. CheckpointAttempt

```text
CheckpointAttempt
├── checkpoint_attempt_id
├── request_ref
├── capture_boundary_ref
├── phase
├── pinned revisions{}
├── required artifact plan
├── produced artifact refs[]
├── verification results[]
├── status
├── failure/degradation info
└── provenance
```

`CheckpointAttempt` не становится `CheckpointManifest` автоматически.

---

# 7. ArtifactRef

```text
ArtifactRef
├── logical_artifact_id
├── artifact_kind
├── content_digest
├── digest_algorithm
├── byte_size
├── schema_revision
├── format_descriptor
├── storage_locations[]
├── portability_class
├── visibility/trust class
├── base_artifact_refs[]?
└── provenance
```

Канонически:

```text
artifact identity ≠ path/URI
```

---

# 8. ArtifactVerificationRecord

```text
ArtifactVerificationRecord
├── artifact_ref
├── existence check
├── size check
├── digest/integrity check
├── schema check
├── required/optional classification
├── status
└── evidence
```

---

# 9. CheckpointManifest

```text
CheckpointManifest
├── checkpoint_id
├── checkpoint_revision
├── checkpoint_scope
├── capture_boundary_ref
├── agent snapshot descriptor ref
├── active revision manifest
├── candidate revision refs[]
├── Environment snapshot/world refs?
├── Training Runtime state refs?
├── Experience/Dataset/Replay refs[]
├── artifact_refs[]
├── required artifact set
├── optional artifact set
├── software manifest ref
├── hardware/topology manifest ref
├── determinism policy ref
├── reproducibility claim ceiling
├── completeness/integrity status
├── parent/base checkpoint refs[]
├── committed_at
└── provenance
```

Final manifest создаётся только после required verification.

---

# 10. TrainingResumeStateDescriptor

```text
TrainingResumeStateDescriptor
├── TrainingPlan ref
├── TrainingAttempt ref
├── BaseRevisionBundle ref
├── active AgentRevision ref
├── CandidateRevisionBundle refs[]
├── optimizer state refs[]
├── scheduler state refs[]
├── scaler/mixed precision state refs[]
├── trainer counters/state
├── gradient accumulation state?
├── replay population/sampler refs
├── sample/dataloader cursor refs
├── training RNG refs[]
├── validation/activation state
└── resume_semantics
```

---

# 11. EnvironmentCheckpointDescriptor

```text
EnvironmentCheckpointDescriptor
├── environment_id/revision
├── WorldManifest ref
├── environment snapshot artifact ref
├── Environment RNG ref
├── transition counter/logical scope
├── termination/truncation state
├── pending action/execution refs[]
├── clone/restore capability
└── visibility/trust class
```

Hidden Environment state остаётся research/checkpoint-only.

---

# 12. PendingExternalEffectDescriptor

```text
PendingExternalEffectDescriptor
├── action_commit_id
├── dispatch_id
├── dispatch attempts[]
├── environment receipt refs[]
├── execution state
├── idempotency/dedup capability
├── reconciliation status
├── safe_to_retry?
├── safe_to_branch?
└── provenance
```

При `execution_unknown` exact/safe branch restore может быть запрещён до reconciliation.

---

# 13. RNGStateDescriptor

```text
RNGStateDescriptor
├── rng_id
├── owner boundary
├── algorithm/provider identity
├── state artifact/ref
├── seed/origin metadata
├── logical capture time
├── portability constraints
└── provenance
```

`seed` и current RNG state хранятся раздельно.

---

# 14. DeterminismPolicy

```text
DeterminismPolicy
├── policy_id / revision
├── deterministic mode requested?
├── framework flags{}
├── known nondeterministic operations[]
├── precision/dtype policy
├── compiler/autotuning policy
├── worker/process policy
├── parallelism topology constraints
├── allowed nondeterminism
├── comparison criterion
└── provenance
```

---

# 15. ReproducibilityClaim

```text
ReproducibilityClaim
├── claim_id
├── claim_level
├── scope
├── source checkpoint/experiment refs
├── required software/hardware constraints
├── allowed migrations/differences
├── comparison criterion
├── determinism policy ref
├── known limitations
├── validation/probe refs[]
└── status
```

Semantic levels должны различать минимум:

- provenance reproducibility;
- state restore;
- constrained deterministic continuation;
- bitwise equivalence where supported;
- statistical reproducibility.

Exact names/numbers не frozen.

---

# 16. RestoreProfile

```text
RestoreProfile
├── requested restore kind
├── exact/compatible/portable/approximate semantics
├── required state classes[]
├── allowed missing optional classes[]
├── allowed migration policies[]
├── software/hardware compatibility constraints
├── RNG/determinism requirements
├── Environment restore requirements
├── pending external-effect policy
└── provenance
```

---

# 17. RestoreRequest

```text
RestoreRequest
├── restore_attempt_id
├── checkpoint_ref
├── requested profile
├── target runtime/topology
├── migration policy refs[]
├── storage resolver config ref
├── validation policy
└── provenance
```

---

# 18. RestoreRecord

```text
RestoreRecord
├── restore_attempt_id
├── checkpoint_ref
├── requested profile
├── actual profile
├── resolved artifact refs[]
├── integrity results[]
├── migrations[]
├── compatibility results[]
├── invariant validation results[]
├── deterministic probe result?
├── restored revision refs
├── status
├── degradation/limitations
└── provenance
```

Silent exact→approximate downgrade запрещён.

---

# 19. MigrationRecord

```text
MigrationRecord
├── migration_id
├── source checkpoint/artifact ref
├── source schema/revision
├── migration policy/revision
├── target schema/revision
├── output artifact/checkpoint ref
├── lossless/lossy classification
├── warnings
├── validation results
└── provenance
```

Original artifact/checkpoint не переписывается.

---

# 20. SoftwareEnvironmentManifest

```text
SoftwareEnvironmentManifest
├── software_manifest_id
├── repository revision
├── repository dirty-state identity
├── language/runtime version
├── framework/library versions{}
├── accelerator runtime versions{}
├── compiler/runtime identities{}
├── model/tokenizer/backend revisions{}
├── relevant environment/config flags{}
├── package/container/lock identities[]
└── provenance
```

Exact package manager/container mechanism не frozen.

---

# 21. HardwareTopologyManifest

```text
HardwareTopologyManifest
├── hardware_manifest_id
├── CPU architecture/class
├── accelerator devices[]
├── memory capacities
├── device count
├── interconnect/topology info?
├── precision capabilities
├── provider/runtime class
├── distributed topology
└── provenance
```

Не является agent-visible Self state автоматически.

---

# 22. ComputeManifest

```text
ComputeManifest
├── compute_manifest_id
├── run/training/evaluation refs
├── allocated resources
├── software/hardware manifest refs
├── precision/dtype
├── batch/sequence workload descriptors?
├── compile/warmup policy
├── measurement methods[]
├── usage record refs[]
└── provenance
```

---

# 23. ComputeUsageRecord

```text
ComputeUsageRecord
├── usage_record_id
├── causal/logical scope
├── resource kind
├── requested?
├── allocated?
├── estimated usage?
├── measured usage?
├── provider-reported usage?
├── wall-clock duration?
├── accelerator time?
├── CPU time?
├── memory/VRAM peak?
├── FLOP estimate/measurement?
├── I/O/network?
├── energy/power?
├── method/accuracy metadata
└── provenance
```

Не все поля обязаны быть доступны.

---

# 24. ExperimentManifest

```text
ExperimentManifest
├── experiment/run id
├── repository/code revision
├── config/version/design refs
├── checkpoint refs[]
├── Environment/world refs[]
├── Experience/Dataset refs[]
├── intervention/evaluation condition refs[]
├── software manifest ref
├── hardware manifest ref
├── compute manifest ref
├── determinism policy ref
├── seed/RNG initialization policy
├── reproducibility claims[]
├── output artifact refs[]
├── metric/result refs[]
└── provenance
```

---

# 25. DeltaCheckpointDescriptor

```text
DeltaCheckpointDescriptor
├── checkpoint_id
├── base checkpoint refs[]
├── changed artifact refs[]
├── unchanged inherited refs[]
├── dependency-chain integrity
├── compaction lineage?
└── provenance
```

Missing required base → restore failure.

---

# 26. CheckpointRetentionPolicyDescriptor

```text
CheckpointRetentionPolicyDescriptor
├── policy_id/revision
├── protected refs/rules
├── storage budget
├── delta-base dependency rules
├── archive/milestone rules
├── garbage-collection semantics
└── provenance
```

Checkpoint retention не становится cognitive importance.

---

# 27. CheckpointFailure

Conceptual classes:

```text
capture_boundary_unavailable
unresolved_external_effect
artifact_write_failure
artifact_corrupt
manifest_incomplete
integrity_mismatch
unsupported_schema
migration_failed
missing_base_checkpoint
missing_external_artifact
restore_invariant_failed
reproducibility_probe_failed
```

Exact enum не frozen.

---

# 28. Invariants

Будущая implementation должна проверять минимум:

```text
manifest committed only after required artifacts verify
artifact content identity independent from path
required artifact digest/size/schema match
checkpoint scope requirements satisfied
active/candidate revisions remain distinct
seed is not substituted for current RNG state
execution_unknown blocks unsafe retry/branch semantics
full-system restore uses causally aligned Agent/Environment state
exact restore cannot silently become approximate
migration creates explicit lineage
missing delta base fails closed
optimizer/trainer state not required for inference-only scope
training-resume scope includes declared trainer state
infrastructure compute telemetry does not mutate cognition
```

---

# 29. Не frozen

До contract freeze не считать каноническими:

- Python class/Protocol/dataclass/Pydantic layout;
- exact checkpoint directory layout;
- `torch.save`/`safetensors`/DCP/Accelerate;
- JSON/MsgPack/Protobuf;
- local/object/database storage;
- SHA-256/BLAKE3;
- zstd/gzip;
- Docker/Nix/Conda/uv;
- specific RNG algorithms;
- exact reproducibility-level names/numbers;
- exact profiler/FLOP/energy tool;
- retention cadence;
- delta encoding algorithm.
