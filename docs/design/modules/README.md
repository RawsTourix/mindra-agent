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
DU-23  Policy / Planner
DU-24  Action Boundary / Gate / Executor
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

# 3. DU-24 — Action Boundary / Gate / Executor

[`action-boundary.md`](action-boundary.md)

Каноническая форма:

```text
SelectedActionIntent
        ↓
Action Gate / Authorization
        ↓
AuthorizedAction
        ↓
Action Commit
        ↓
Dispatch
        ↓
Environment acceptance/execution
        ↓
Environment Transition
        ↓
Outcome Commit
```

Action Boundary:

- обязательна как semantic boundary между Policy и Environment;
- базовый Gate не является второй Policy;
- проверяет schema/freshness/capability/preconditions/explicit constraints;
- не использует hidden evaluator/Environment Ground Truth normal runtime способом;
- по умолчанию accept/reject + semantics-preserving normalization;
- behavior-changing replacement допускается только как explicit override с отдельной provenance;
- фиксирует `Action Commit` после authorization, но до dispatch;
- сохраняет commit даже при последующем dispatch/execution failure;
- различает `definitely_not_sent`, `execution_unknown`, Environment `no_effect` и partial execution;
- использует stable dispatch identity и explicit retry/idempotency capability;
- не обещает universal physical exactly-once execution.

Dispatcher:

- execution infrastructure, не cognitive Policy;
- не меняет committed semantic action;
- управляет transport/retry/reconciliation;
- Environment остаётся владельцем transition/outcome.

---

# 4. Первый ещё не спроектированный блок — Experience / Data / Replay

Следующий Design Update:

```text
DU-25 — Experience / Data / Replay
```

Предварительная responsibility:

> зафиксировать canonical causal experience/data schema, из которой можно получать research trajectories и training replay samples без смешивания natural experience, Memory, imagination и derived training data.

Нужно определить:

- event/transition/trajectory hierarchy;
- action candidate→intent→commit→dispatch→outcome linkage;
- natural/replayed/imagined/intervened/counterfactual provenance;
- evaluator-only vs agent-visible data;
- agent/model/state revision refs;
- failed-dispatch/no-transition representation;
- sequence/window extraction;
- derived training sample/relabeling semantics;
- replay sample provenance;
- schema/version/storage tiers;
- quality/completeness flags.

---

# 5. После cognitive architecture

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

# 6. Design dependency graph

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

Это design dependency graph, не runtime DAG.

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

Для сложного Action Gate/override также обязателен simpler pass-through/schema/capability control и отдельная Policy-vs-override attribution.

Следующий допустимый этап определяется только [`../current.md`](../current.md).
