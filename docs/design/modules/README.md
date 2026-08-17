# Карта проектирования модулей MINDRA

## Статус

Этот документ — карта принятых cognitive/runtime boundaries и оставшихся областей. Канонический статус определяется специализированными design docs и [`../current.md`](../current.md).

Отдельный cognitive module существует только при самостоятельной ответственности, явной boundary/state semantics и независимо проверяемом causal вкладе.

`DU-25` уже находится **вне cognitive module chain**: это внешний Experience/Data plane.

---

# 1. Принятые cognitive/runtime boundaries

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
DU-23  Policy / Planner
DU-24  Action Boundary / Gate / Executor
```

Канонические subsystem documents находятся рядом в `docs/design/modules/`.

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
→ adaptive allocation optional cognitive operations/resources

Policy
→ final selected behavioral intention

Planner
→ optional explicit multi-step/contingent plan/action candidate provider

Action Boundary
→ validation/authorization → Action Commit → dispatch/execution correlation
```

Ключевые различия:

```text
CognitiveState ≠ Workspace
Executive Control ≠ Scheduler ≠ Policy
Policy ≠ Planner
Planner ≠ World Model
Plan ≠ ImaginedTrajectory
Valuation ≠ Policy Decision
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
Policy choice ≠ external override
```

---

# 3. Завершённая cognitive interaction chain

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
Policy ← Planner(optional)
   ↓
Action Boundary / Gate
   ↓
Environment
```

Это design dependency/causal map, не literal runtime DAG одного Cognitive Cycle.

---

# 4. DU-25 — Experience / Data / Replay находится сбоку от cognition

Canonical owner:

- [`../experience-data-replay.md`](../experience-data-replay.md)

Experience Data Plane наблюдает causally relevant execution и создаёт долговременную data history, но не входит в cognitive feedback path normal runtime способом.

```text
Agent / Environment / Runtime
          ↓
      Evidence Plane
          ↓
   Experience Recorder
          ↓
    Experience Journal
          ↓
 Projection / Dataset Builder
          ↓
 Training Samples / Replay
```

Ключевые различия:

```text
TraceEvent ≠ ExperienceEvent
Experience Journal ≠ Agent runtime state
Experience Journal ≠ Agent Memory
Experience Journal ≠ Replay Buffer
Source Experience ≠ TrainingSample
Agent Memory Replay ≠ Training Replay
```

`Experience Journal` не становится новым cognitive module только потому, что хранит internal events.

---

# 5. Первый ещё не спроектированный блок — Training Lifecycle

Следующий Design Update:

```text
DU-26 — Training Lifecycle
```

Предварительная responsibility:

> определить external Training Runtime, Learning Update semantics, ownership optimizer/loss state и causal activation новых agent/component revisions поверх `TrainingSample`/Replay data boundary `DU-25`.

Нужно определить минимум:

- Training Runtime ownership;
- trainable vs ordinary runtime state;
- losses/objectives;
- TrainingSample consumption;
- replay/batch/sequence semantics;
- optimizer state;
- Learning Update proposal/commit/activation;
- online/offline/on-policy/off-policy distinctions;
- new `agent_revision` activation;
- in-flight cognition under previous revision;
- frozen/trainable Cortex/adapters;
- module-local vs joint optimization;
- representation drift;
- privileged supervision;
- rollback/failure/degradation.

---

# 6. Оставшиеся Design Updates

```text
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

# 7. Diagnostic rule

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

Для Planner отрицательный gate обязателен: если matched reactive/search controls объясняют эффект, отдельную boundary нужно пересмотреть.

Для сложного Action Gate/override обязателен simpler pass-through/schema/capability control и отдельная Policy-vs-override attribution.

Для Experience/Data отдельный module gate не применяется: это infrastructure/data responsibility, но требуются data-lineage, leakage, schema and replay controls из `DU-25`.

Следующий допустимый этап определяется только [`../current.md`](../current.md).
