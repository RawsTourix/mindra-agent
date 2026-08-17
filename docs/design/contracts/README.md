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
- [`policy-planner.md`](policy-planner.md) — BehavioralContext, ActionCandidate, PlanCandidate, PolicyCandidateSet, DecisionDeferral и SelectedActionIntent после `DU-23`.

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
SelectedActionIntent ≠ Action Commit / Executed Action
```

Для Policy / Planner дополнительно:

- Policy является owner `SelectedActionIntent`;
- Planner normal runtime способом не создаёт final selected intent;
- Planner планирует относительно `World Belief`, а не hidden Environment state;
- Planner subgoal проходит Goal Proposal boundary;
- candidate sources входят в explicit `PolicyCandidateSet`;
- stale plan/candidate set нельзя silent-rebase;
- `incomparable` допускает deferral/tie-break, но не требует fake scalarization;
- `DecisionDeferral` не вызывает Executive рекурсивно, а создаёт lifecycle-visible proposals;
- Cortex/World Model/Valuation outputs не становятся action автоматически;
- stochastic selection сохраняет causal RNG/provenance;
- selected intent передаётся в `DU-24`, а не dispatch'ится Policy напрямую;
- `NoPlanner`/ReactivePolicy и matched controls обязательны для claims о planning.

---

# Текущий статус

После `DU-04 … DU-23` semantic requirements приняты, но **общий exact Python contract set намеренно не frozen**.

`policy-planner.md` остаётся candidate до Action/Data/Training/Checkpoint/Evaluation integration.

До contract freeze нельзя считать каноническими:

- `Protocol`/ABC/dataclass/TensorDict/Pydantic;
- exact action encoding;
- Policy/Planner neural architecture;
- MCTS/MPC/POMCP/ToT/beam search;
- plan tree/graph/list representation;
- candidate count;
- horizon/replanning frequency;
- stochastic distribution/tie-break rule;
- value scalarization;
- exact Action Gate integration;
- training objective.

---

# Иерархия

```text
accepted ADR + canonical design
→ candidate/exact contract
→ version specification
→ implementation sequence
→ implementation
```
