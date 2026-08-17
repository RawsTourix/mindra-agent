# Candidate / exact internal contracts MINDRA

## Назначение

Этот каталог хранит machine-facing semantic contracts уже принятых subsystem/data/training boundaries.

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
- [`training-lifecycle.md`](training-lifecycle.md) — TrainingPlan/Attempt, GradientFlowPolicy, CandidateRevisionBundle, LearningUpdateRecord и RevisionActivation semantics после `DU-26`.

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
ActionCandidate ≠ SelectedActionIntent
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
TraceEvent ≠ ExperienceEvent
Experience Journal ≠ Agent runtime state
Source Experience ≠ TrainingSample
ResearchAnnotation ≠ agent-visible payload
Training Runtime ≠ cognitive module
Runtime State Update ≠ Learning Update
Replay Selection ≠ Learning Update
Training Objective ≠ Agent Goal ≠ ValueProfile
runtime dependency graph ≠ gradient graph
optimizer state ≠ CognitiveState
CandidateRevisionBundle ≠ Active AgentRevision
```

Для Training Lifecycle дополнительно:

- ordinary module `compute()` не выполняет hidden optimizer update;
- `TrainingPlan` pin'ит base revisions, data, objectives, visibility и gradient policies;
- stale base revision не rebased молча;
- source samples/behavior revisions traceable до `LearningUpdateRecord`;
- privileged supervision explicit;
- shared parameters требуют explicit optimizer coordination;
- candidate revision не активируется только потому, что loss уменьшился;
- activation происходит только на допустимой causal boundary;
- in-flight cognition сохраняет pinned старую revision;
- coupled revision bundle активируется атомарно;
- representation-breaking update требует compatibility/migration semantics;
- failed candidate не мутирует live Agent;
- rollback не удаляет исторический update/activation;
- training metrics/replay priorities не становятся cognitive signals автоматически.

---

# Текущий статус

После `DU-04 … DU-26` semantic requirements приняты, но **общий exact Python contract set намеренно не frozen**.

`training-lifecycle.md` остаётся candidate до Checkpoint/Evaluation integration.

До contract freeze нельзя считать каноническими:

- `Protocol`/ABC/dataclass/TensorDict/Pydantic;
- exact event/status enums;
- PyTorch/JAX/TensorFlow;
- optimizer/scheduler/scaler implementation;
- RL/SFT/distillation algorithm;
- LoRA/QLoRA/full fine-tuning;
- batch/tensor layout;
- loss weighting/gradient surgery method;
- distributed actor/learner topology;
- checkpoint payload format;
- storage/artifact backend.

---

# Иерархия

```text
accepted ADR + canonical design
→ candidate/exact contract
→ version specification
→ implementation sequence
→ implementation
```
