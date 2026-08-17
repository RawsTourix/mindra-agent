# Candidate / exact internal contracts MINDRA

## Назначение

Этот каталог хранит machine-facing semantic contracts уже принятых subsystem boundaries.

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
- [`action-boundary.md`](action-boundary.md) — authorization stages, AuthorizedAction, ActionCommitRecord, dispatch/receipt/execution/reconciliation semantics после `DU-24`.

---

# Общие требования

Contract должен фиксировать, где применимо:

- required/optional semantic fields;
- ownership/read/write boundaries;
- revision/freshness/availability;
- causal provenance;
- lifecycle;
- public/private state;
- snapshot/restore;
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
Forgetting ≠ physical deletion
Memory Replay ≠ Training Replay
Consolidation ≠ in-place rewrite ≠ Learning Update
CognitiveState ≠ Workspace
Workspace ≠ Memory ≠ Cortex context
Workspace broadcast ≠ callback/module execution
WorkspaceItem ≠ new factual authority
Executive Control ≠ Cognitive Scheduler
Executive Control ≠ Policy / Planner
Internal MetaAction ≠ Environment Action
MetaActionProposal ≠ execution
ExecutiveDecision ≠ direct provider/service call
Policy ≠ Planner
Planner ≠ World Model
Plan ≠ ImaginedTrajectory
Valuation ≠ Policy Decision
ActionCandidate ≠ SelectedActionIntent
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
Policy choice ≠ external override
transport failure ≠ Environment no-effect
```

Для Action Boundary дополнительно:

- stale/malformed/rejected intent не получает `ActionCommitRecord`;
- normal Gate не выбирает replacement behavior скрыто;
- semantics-preserving normalization сохраняет отдельную transformation provenance;
- behavior-changing override имеет explicit `ActionOverrideRecord`;
- `Action Commit` происходит после final authorization и до dispatch;
- post-commit dispatch/execution failure не отменяет commit;
- retry не создаёт новый commit и использует stable logical dispatch identity;
- retry требует explicit idempotency/dedup semantics либо definite-non-send evidence;
- `execution_unknown` не считается `not_executed`;
- Environment receipt `accepted` не считается success;
- partial/no-effect/transport failure остаются разными causal classes;
- hidden evaluator truth не становится normal Gate input;
- provider-native payload не протекает обратно в Policy semantic contract.

---

# Текущий статус

После `DU-04 … DU-24` semantic requirements приняты, но **общий exact Python contract set намеренно не frozen**.

`action-boundary.md` остаётся candidate до Data/Training/Checkpoint/Evaluation integration.

До contract freeze нельзя считать каноническими:

- `Protocol`/ABC/dataclass/TensorDict/Pydantic;
- exact Environment action enum/schema;
- exact authorization stage ordering;
- constraint DSL;
- shielding/RTA implementation;
- idempotency token format;
- ROS/gRPC/HTTP transport;
- retry/backoff policy;
- cancellation state machine;
- timeout values;
- exact dispatch runtime library;
- exact experience serialization.

---

# Иерархия

```text
accepted ADR + canonical design
→ candidate/exact contract
→ version specification
→ implementation sequence
→ implementation
```
