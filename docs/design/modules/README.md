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
```

Ключевые различия:

```text
relevance ≠ value ≠ salience
SalienceProfile ≠ AttentionAllocation
AttentionAllocation ≠ Workspace admission
AttentionAllocation ≠ Executive compute decision
```

---

# 3. DU-19 — Salience / Attention

[`salience.md`](salience.md)

Каноническая форма:

```text
Explicit Candidate Set
+
Typed Evidence
+
Purpose
→ SalienceProfile[]

SalienceProfile[]
+
AttentionBudget
+
AllocationPolicy
→ AttentionAllocation
```

Salience:

- не владеет Memory retrieval/retention;
- не является Workspace;
- не вызывает Cortex;
- не меняет scheduler;
- не выбирает action;
- не считает Transformer attention weights canonical salience;
- может иметь optional persistence/inhibition state;
- должна иметь measurable downstream allocation effect.

---

# 4. Первый ещё не спроектированный блок — Memory Regulation / Consolidation

Следующий Design Update:

```text
DU-20 — Memory Regulation / Consolidation
```

Предварительная ответственность:

> расширить нейтральный Memory Core политиками admission/retention/forgetting/eviction/replay/consolidation, используя explicit Salience и другой разрешённый evidence без превращения Memory в скрытую Valuation или Training Runtime.

Нужно будет определить:

- memory admission;
- retention/aging;
- forgetting/eviction;
- replay candidate priority;
- consolidation boundary;
- episodic → derived/semantic abstraction;
- Salience integration;
- capacity/resource policy;
- conflict между recency/salience/diversity/value;
- representation drift при consolidation;
- training replay vs Agent memory replay;
- catastrophic forgetting;
- snapshot/revision/intervention;
- controls `NoRegulation`, random/recency/shuffled/matched.

---

# 5. Будущие cognitive areas

## DU-21 — Workspace

Ограниченная temporary global-access surface, если module gate подтвердит отдельную роль сверх `CognitiveState`.

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
Goals / Cortex / Memory
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
Memory Regulation
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
