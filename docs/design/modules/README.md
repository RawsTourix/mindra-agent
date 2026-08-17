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
→ budget-aware lifecycle/replay/consolidation policy поверх canonical Memory Core
```

Ключевые различия:

```text
relevance ≠ value ≠ salience
SalienceProfile ≠ AttentionAllocation
AttentionAllocation ≠ Memory lifecycle decision
Memory Core ≠ Memory Regulation
forgetting ≠ physical deletion
Memory Replay ≠ Training Replay
consolidation ≠ rewrite ≠ Learning Update
```

---

# 3. DU-20 — Memory Regulation / Consolidation

[`memory-regulation.md`](memory-regulation.md) расширяет [`memory.md`](memory.md).

Каноническая форма:

```text
Memory Core
→ canonical Store / validation / commit

Memory Regulation
→ profiles + purpose-specific policies
→ admission/retention/eviction/replay/consolidation decisions
→ proposals back to Memory Core
```

Consolidation:

```text
source episodic MemoryRecords
→ explicit Consolidation Event
→ gated derivation
→ new derived MemoryRecord
→ derived_from/support/conflict provenance
```

Memory Regulation:

- не является вторым Store owner;
- не использует universal `memory_importance` scalar как canonical truth;
- принимает explicit `MemoryBudget`;
- использует Salience только как один из evidence sources;
- различает logical forgetting и physical deletion;
- не считает retrieval count automatic importance;
- не запускает hidden background replay;
- не смешивает Agent Memory Replay с Training Replay;
- не делает optimizer/slow-weight update;
- сохраняет raw/source evidence и contradictions;
- должна сравниваться с episodic-only/FIFO/random/shuffled/matched controls.

---

# 4. Первый ещё не спроектированный блок — Workspace

Следующий Design Update:

```text
DU-21 — Workspace
```

Предварительная responsibility:

> проверить, нужен ли MINDRA отдельный ограниченный temporary global-access surface сверх committed `CognitiveState`, explicit dependencies и Salience allocation.

Нужно определить:

- module gate;
- Workspace candidate/admission;
- capacity/budget;
- `Workspace ≠ CognitiveState`;
- `Workspace ≠ Salience`;
- `Workspace ≠ Memory`;
- `Workspace ≠ Cortex context`;
- producer/consumer authority;
- global-read/broadcast semantics;
- persistence/replacement;
- Salience integration;
- retrieval → Workspace boundary;
- Cortex context packing;
- imagined/branch-local Workspace;
- interventions/controls;
- negative gate, при котором отдельный Workspace отклоняется.

---

# 5. Будущие cognitive areas

## DU-22 — Metacognitive / Executive Control

Реальный выбор Cortex/retrieval/planning depth/compute budget/goal focus. Не scheduler.

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
