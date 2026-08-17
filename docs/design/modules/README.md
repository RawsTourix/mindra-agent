# Карта проектирования модулей MINDRA

## Статус

Этот документ — карта принятых boundaries и оставшихся областей. Канонический статус определяется специализированными design docs и [`../current.md`](../current.md).

Отдельный модуль существует только при самостоятельной ответственности, явной boundary/state semantics и независимо проверяемом causal вкладе.

---

# 1. Принятые boundaries

```text
DU-07  Environment
DU-08  Perception / Canonical Representation
DU-09  Goal System
DU-10  Cortex Boundary
DU-11  Memory Core
DU-12  World Model
DU-13  Self Model
DU-14  Intrinsic Signals
DU-15  Drives
DU-16  Appraisal
DU-17  Affect Dynamics
DU-18  Valuation
DU-19  Salience / Attention
DU-20  Memory Regulation / Consolidation
DU-21  Workspace
DU-22  Metacognitive / Executive Control
```

Канонические документы находятся рядом в `docs/design/modules/`.

---

# 2. Разведение внутренних слоёв

```text
Intrinsic Signals
→ свойства опыта

Drives
→ persistent regulatory state

Appraisal
→ event-level meaning относительно Agent context

Affect
→ history-dependent persistent modulation state

Valuation
→ decision-relevant multi-objective comparison

Salience
→ purpose-dependent priority ограниченного processing

Memory Regulation
→ budget-aware lifecycle/replay/consolidation policy

Workspace
→ bounded temporary shared availability/broadcast admitted content

Executive Control
→ adaptive selection/stop/allocation optional cognitive operations под explicit budget
```

Ключевые различия:

```text
CognitiveState ≠ Workspace
SalienceProfile ≠ Workspace admission
Workspace ≠ Memory ≠ Cortex context
broadcast ≠ module execution
Executive Control ≠ Cognitive Scheduler
Executive Control ≠ Policy / Planner
Internal MetaAction ≠ Environment Action
```

---

# 3. DU-22 — Executive Control

[`executive-control.md`](executive-control.md)

Каноническая форма:

```text
MetaActionProposal[]
+
ExecutiveObservation
+
CognitiveResourceEnvelope
        ↓
Executive Control
        ↓
ExecutiveDecision
        ↓
Scheduler validation
        ↓
allowed internal operation(s)
```

Executive Control:

- не является Scheduler;
- не выбирает Environment action;
- не имеет direct provider/service handles;
- выбирает только из declared proposal/catalog boundary;
- управляет allocation/ledger внутри предоставленного resource envelope;
- поддерживает explicit continue/yield control points;
- может разрешать Cortex/retrieval/rollout/consolidation без ownership leakage;
- использует Self/Salience/Workspace/Valuation evidence без передачи им control authority;
- не мутирует Goal Graph через temporary Goal focus;
- учитывает actual resource consumption отдельно от estimates;
- имеет `NoExecutive`/fixed/equal-budget/matched controls;
- должен быть пересмотрен, если adaptive gain исчезает при matched actual compute.

---

# 4. Первый ещё не спроектированный блок — Policy / Planner

Следующий Design Update:

```text
DU-23 — Policy / Planner
```

Предварительная responsibility:

> генерировать/оценивать behavioral candidates/plans и выбирать final action intention, не подменяя Executive resource control, World Model dynamics, Valuation comparison или Action Gate.

Нужно определить:

- Policy/Planner module gates;
- reactive vs planning path;
- Action Candidate semantics;
- plan representation/persistence;
- Planner ↔ World Model;
- Planner ↔ Goal Proposal;
- candidate valuation/comparison;
- constraints/risk/incomparability;
- Cortex-assisted planning;
- Executive compute budget boundary;
- stochastic selection;
- failure/degradation;
- observability/intervention/snapshot;
- NoPlanner/reactive/matched controls.

---

# 5. Будущие cognitive areas

## DU-24 — Action Gate / Executor

```text
selected action intention
≠ executed action
≠ observed outcome
```

---

# 6. После cognitive architecture

```text
DU-25 — Experience / Data / Replay
DU-26 — Training Lifecycle
DU-27 — Checkpoint / Reproducibility / Compute
DU-28 — MINDRA-Eval
DU-29 — Engineering Testing
DU-30 — Research Claims / Limitations
DU-31 — Contract + ADR Consistency Freeze
DU-32 — Version Roadmap
```

Только после `DU-32` появляются concrete software versions и `implementation-sequence.md`.

---

# 7. Design dependency graph

```text
Environment
   ↓
Perception
   ↓
Goals / Cortex / Memory Core
   ↓
World + Self
   ↓
Intrinsic Signals
   ↓
Drives
   ↓
Appraisal
   ↓
Affect
   ↓
Valuation
   ↓
Salience
   ↓
Memory Regulation / Consolidation
   ↓
Workspace
   ↓
Executive Control
   ↓
Policy / Planner
   ↓
Action Gate
   ↓
Environment
```

Это design dependency graph, не runtime DAG.

---

# 8. Diagnostic rule

Для каждого cognitive subsystem требуются, где применимо:

- `No*` configuration;
- Dummy/control implementation;
- random/shuffled/constant baseline;
- parameter/compute/state-matched control;
- observability;
- interventions;
- snapshot state;
- failure/degradation semantics;
- module-specific causal metrics.

Следующий допустимый этап определяется только [`../current.md`](../current.md).
