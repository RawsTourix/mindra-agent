# Candidate / exact internal contracts MINDRA

## Назначение

Этот каталог хранит machine-facing semantic contracts уже принятых subsystem/data/training/reproducibility boundaries.

До общего contract freeze документы здесь остаются **candidate contracts**: они уточняют форму принятого design, но не имеют права молча менять его смысл или превращать удобный Python choice в архитектурный invariant.

---

# Текущие candidate contracts

- [`environment.md`](environment.md) — Environment interaction/research boundary после `DU-07`;
- [`perception.md`](perception.md) — Canonical Percept/Semantic Core/Feature Views после `DU-08`;
- [`goals.md`](goals.md) — Goal Proposal/Committed Goal/Goal Graph после `DU-09`;
- [`cortex.md`](cortex.md) — Cortex Gateway/capabilities/request/result после `DU-10`;
- [`memory.md`](memory.md) — Memory records/representations/retrieval после `DU-11`;
- [`world-model.md`](world-model.md) — World Belief/assimilation/prediction/imagination после `DU-12`;
- [`self-model.md`](self-model.md) — capability/competence/Self Prediction после `DU-13`;
- [`intrinsic-signals.md`](intrinsic-signals.md) — typed Intrinsic Signals после `DU-14`;
- [`drives.md`](drives.md) — typed persistent Drives после `DU-15`;
- [`appraisal.md`](appraisal.md) — multidimensional Appraisal после `DU-16`;
- [`affect.md`](affect.md) — persistent Affect dynamics после `DU-17`;
- [`valuation.md`](valuation.md) — ValueProfile/ComparisonPolicy/Risk/Constraint semantics после `DU-18`;
- [`salience.md`](salience.md) — SalienceTarget/Profile, AttentionBudget и AttentionAllocation после `DU-19`;
- [`memory-regulation.md`](memory-regulation.md) — MemoryBudget, lifecycle/replay/consolidation после `DU-20`;
- [`workspace.md`](workspace.md) — Workspace proposal/admission/items/budget/broadcast/read/snapshot semantics после `DU-21`;
- [`executive-control.md`](executive-control.md) — MetaActionProposal/InternalOperationCatalog, CognitiveResourceEnvelope, ExecutiveDecision, stop/continue и budget ledger semantics после `DU-22`;
- [`policy-planner.md`](policy-planner.md) — BehavioralContext, ActionCandidate, PlanCandidate, PolicyCandidateSet, DecisionDeferral и SelectedActionIntent после `DU-23`;
- [`action-boundary.md`](action-boundary.md) — authorization stages, AuthorizedAction, ActionCommitRecord, dispatch/receipt/execution/reconciliation semantics после `DU-24`;
- [`experience-data-replay.md`](experience-data-replay.md) — ExperienceEvent/Journal, causal revisions, annotations, projections, DatasetManifest, TrainingSample и Training Replay provenance после `DU-25`;
- [`training-lifecycle.md`](training-lifecycle.md) — TrainingPlan/Attempt, GradientFlowPolicy, CandidateRevisionBundle, LearningUpdateRecord и RevisionActivation semantics после `DU-26`;
- [`checkpoint-reproducibility-compute.md`](checkpoint-reproducibility-compute.md) — checkpoint scope/capture/artifacts, restore profiles, reproducibility claims и software/hardware/compute manifests после `DU-27`.

---

# Общие требования

Contract должен фиксировать, где применимо:

- required/optional semantic fields;
- ownership/read/write boundaries;
- revision/freshness/availability;
- causal provenance;
- lifecycle;
- public/private/visibility state;
- snapshot/restore references;
- observability/intervention;
- failure/degradation;
- compatibility/serialization;
- автоматически проверяемые invariants.

Exact implementation detail одного backend не должен протекать в canonical contract без design justification.

---

# Действующие safeguards

```text
Environment Ground Truth ≠ Agent input
Canonical Percept ≠ concrete encoder latent
Goal Proposal ≠ direct Goal mutation
Cortex ≠ ambient Agent-state owner
MemoryRecord ≠ embedding/index
World Prediction ≠ observed fact
Self Prediction ≠ Policy decision
Intrinsic Signal ≠ reward/value
Drive State ≠ global motivation/value
Appraisal ≠ emotion/value/Affect
Affect ≠ emotion label/Drive/value
ValueProfile ≠ mandatory scalar/reward/Policy decision
SalienceProfile ≠ AttentionAllocation
Memory Core validation ≠ Regulation admission
Memory Replay ≠ Training Replay
Consolidation ≠ in-place rewrite ≠ Learning Update
CognitiveState ≠ Workspace
Executive Control ≠ Cognitive Scheduler ≠ Policy
Policy ≠ Planner
Plan ≠ ImaginedTrajectory
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
TraceEvent ≠ ExperienceEvent
Experience Journal ≠ Agent runtime state
Source Experience ≠ TrainingSample
Training Runtime ≠ cognitive module
Runtime State Update ≠ Learning Update
Training Objective ≠ Agent Goal ≠ ValueProfile
runtime dependency graph ≠ gradient graph
CandidateRevisionBundle ≠ Active AgentRevision
AgentSnapshot ≠ persistent Checkpoint
Checkpoint ≠ TrainingResumeCheckpoint ≠ ExperimentManifest
same seed ≠ same RNG state ≠ guaranteed same execution
semantic restore ≠ bitwise reproducibility
artifact identity ≠ physical path
ComputeManifest ≠ CognitiveResourceEnvelope
```

Для Checkpoint / Reproducibility / Compute дополнительно:

- final `CheckpointManifest` commit только после verification обязательных artifacts;
- checkpoint scope явно определяет required state;
- content/integrity identity не зависит от storage path;
- active/candidate revisions не смешиваются при restore;
- `execution_unknown` не разрешает unsafe blind retry/branch;
- full-system restore требует causally aligned Agent/Environment state;
- exact restore не downgraded молча до approximate;
- migration создаёт explicit lineage;
- missing delta base fail closed;
- weights-only не masquerade как training resume;
- stronger reproducibility claim требует соответствующих software/hardware/RNG/determinism manifests/evidence;
- infrastructure compute telemetry не становится cognition автоматически.

---

# Текущий статус

После `DU-04 … DU-27` semantic requirements приняты, но **общий exact Python contract set намеренно не frozen**.

`checkpoint-reproducibility-compute.md` остаётся candidate до Evaluation/Engineering Testing/contract freeze integration.

До contract freeze нельзя считать каноническими:

- `Protocol`/ABC/dataclass/TensorDict/Pydantic;
- exact event/status enums;
- PyTorch/JAX/TensorFlow;
- optimizer/trainer implementation;
- checkpoint directory/file layout;
- `torch.save`/safetensors/DCP/Accelerate;
- hash algorithm;
- local/object/database storage;
- compression;
- container/package manager;
- exact reproducibility level names;
- exact deterministic flags;
- compute/FLOP/energy profiler;
- checkpoint retention/delta algorithm.

---

# Иерархия

```text
accepted ADR + canonical design
→ candidate/exact contract
→ version specification
→ implementation sequence
→ implementation
```
