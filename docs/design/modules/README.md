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
```

Ключевые различия:

```text
CognitiveState ≠ Workspace
Executive Control ≠ Scheduler ≠ Policy
Policy ≠ Planner
Planner ≠ World Model
Plan ≠ ImaginedTrajectory
Valuation ≠ Policy Decision
SelectedActionIntent ≠ Action Commit / Executed Action
```

---

# 3. DU-23 — Policy / Planner

[`policy-planner.md`](policy-planner.md)

Каноническая форма:

```text
BehavioralContext
      ↓
explicit candidate sources
      ↓
PolicyCandidateSet
      +
Valuation/Comparison evidence
      ↓
Policy
      ├── SelectedActionIntent
      └── DecisionDeferral
```

Optional Planner:

```text
WorldBelief + Goals + Executive planning budget
      ↓
Planner
      ↓
PlanCandidate / ActionCandidate
      ↓
PolicyCandidateSet
```

Policy:

- является единственным owner selected-action intention;
- не исполняет Environment action;
- может быть reactive/direct без Planner;
- может использовать Planner, Cortex-assisted или scripted candidates;
- корректно обрабатывает constraints/risk/incomparability;
- может вернуть `DecisionDeferral` вместо fake scalarization/random implicit fallback;
- сохраняет stochastic selection/RNG provenance.

Planner:

- optional/falsifiable;
- использует World Belief и agent-visible evidence;
- не читает hidden Environment state normal runtime способом;
- не владеет final selection;
- не мутирует Goal Graph;
- может поддерживать PlanState/replanning;
- должен доказывать пользу против reactive/matched controls.

---

# 4. Первый ещё не спроектированный блок — Action Boundary

Следующий Design Update:

```text
DU-24 — Action Boundary / Gate / Executor
```

Предварительная responsibility:

> превратить `SelectedActionIntent` в причинно идентифицируемое разрешённое/committed/dispatchable действие и связать его с фактическим Environment outcome.

Нужно определить:

- Action Gate module/responsibility gate;
- semantic validation;
- stale intent handling;
- action capability/precondition checks;
- accept/reject/modify/substitute semantics;
- exact `Action Commit` boundary;
- dispatch/idempotency/retry;
- execution/acknowledgement/failure;
- outcome correlation;
- termination/truncation/reset;
- controls/interventions/snapshot.

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

Следующий допустимый этап определяется только [`../current.md`](../current.md).
