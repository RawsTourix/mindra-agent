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
- [`workspace.md`](workspace.md) — bounded Workspace proposal/admission/items/budget/broadcast/read/snapshot semantics после `DU-21`.

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
published state ≠ Workspace admission
SalienceProfile/AttentionAllocation ≠ Workspace admission
Workspace ≠ Memory ≠ Cortex context
Workspace broadcast ≠ callback/module execution
WorkspaceItem ≠ new factual authority
```

Для Workspace дополнительно:

- candidate set/proposals explicit;
- producer не получает direct Workspace write authority;
- capacity/budget explicit;
- admission policy versioned и отделена от Salience;
- consumer read capability declared;
- admitted item сохраняет source revision/provenance;
- source update не переписывает item задним числом;
- branch-local Workspace не мутирует real Workspace;
- Workspace eviction не мутирует source subsystem;
- Cortex context packing выполняется отдельным explicit consumer;
- `NoWorkspace` и matched controls обязательны для функциональных claims.

---

# Текущий статус

После `DU-04 … DU-21` semantic requirements приняты, но **общий exact Python contract set намеренно не frozen**.

`workspace.md` остаётся candidate до Executive/Policy/Data/Training/Checkpoint/Evaluation integration.

До contract freeze нельзя считать каноническими:

- `Protocol`/ABC/dataclass/TensorDict/Pydantic;
- slot/token/byte unit Workspace;
- top-K/winner-take-all/softmax admission;
- concrete neural/shared-latent workspace;
- exact producer/consumer set;
- exact persistence duration;
- exact Cortex packing;
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
