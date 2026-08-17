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
```

Ключевые различия:

```text
CognitiveState ≠ Workspace
SalienceProfile ≠ Workspace admission
Workspace ≠ Memory ≠ Cortex context
broadcast ≠ module execution
Workspace ≠ Policy / Executive Control
```

---

# 3. DU-21 — Workspace

[`workspace.md`](workspace.md)

Каноническая форма:

```text
explicit producers
→ WorkspaceCandidateSet
→ optional Salience evidence
→ Workspace admission under explicit budget
→ bounded WorkspaceSnapshot
→ declared eligible consumers
```

Workspace:

- не является вторым `CognitiveState`;
- имеет реальный capacity/bandwidth bottleneck;
- сохраняет source revision/provenance;
- поддерживает temporary multi-cycle persistence;
- использует broadcast как availability, а не callback;
- не выполняет Memory retrieval;
- не является Cortex prompt;
- не выбирает Environment action;
- поддерживает branch-local simulated Workspace;
- имеет first-class `NoWorkspace` и matched controls;
- должен быть пересмотрен, если matched shared/recurrent buffers объясняют эффект.

---

# 4. Первый ещё не спроектированный блок — Executive Control

Следующий Design Update:

```text
DU-22 — Metacognitive / Executive Control
```

Предварительная responsibility:

> выбирать допустимые internal cognitive operations и распределять global compute/resource budget без подмены Scheduler или final Policy.

Нужно определить:

- module gate;
- monitoring vs control;
- compute/resource budgets;
- continue/stop Cognitive Cycles;
- Cortex/retrieval/planning/consolidation decisions;
- Workspace budget/focus control;
- Goal focus;
- Self Model/uncertainty/cost evidence;
- meta-action semantics;
- Scheduler boundary;
- Policy boundary;
- controls/interventions/snapshot.

---

# 5. Будущие cognitive areas

## DU-23 — Policy / Planner

Final planning/action-selection boundary.

## DU-24 — Action Gate / Executor

```text
selected action
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
