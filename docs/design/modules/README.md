# Карта проектирования модулей MINDRA

## Статус документа

Этот документ является **картой архитектурных областей и порядка их проектирования**, а не заменой канонических subsystem design.

Наличие блока в карте не гарантирует, что он навсегда останется отдельным trainable module.

Главное правило:

> Отдельный модуль существует не из-за когнитивной аналогии, а при наличии самостоятельной вычислительной ответственности, явного state/contract и независимо проверяемого функционального вклада.

Фактический статус определяется каноническим документом и [`../current.md`](../current.md).

---

# 1. Классы архитектурных областей

## 1.1. Границы взаимодействия

```text
Environment
Perception / Representation
Cortex
Action / Actuation boundary
```

## 1.2. Когнитивное состояние и прогнозирование

```text
CognitiveState
Goal System
World Model
Self Model
Memory
Workspace
Metacognitive / Executive Control
```

## 1.3. Внутренние измерения, мотивация, оценка и регуляция

```text
Intrinsic Signal Providers
Drives
Appraisal
Affect Dynamics
Valuation
Salience / Attention Control
```

После `DU-18` роли разведены так:

```text
Intrinsic Signals → свойства опыта
Drives           → persistent regulatory state
Appraisal        → event meaning
Affect           → history-dependent temporal context
Valuation        → decision-relevant comparison
Salience         → будущая allocation priority
```

## 1.4. Выбор и исполнение поведения

```text
Policy / Planner
Action Gate / Executor
```

## 1.5. Обучение и исследовательская инфраструктура

```text
Experience / Trajectory Recorder
Replay / Consolidation
Training Runtime
Checkpoint / Artifact System
Experiment Runner
MINDRA-Eval
```

---

# 2. Уже принятые subsystem boundaries

## DU-07 — Environment

[`environment.md`](environment.md): Agent Interaction Plane отделён от Research Plane.

## DU-08 — Perception

[`perception.md`](perception.md): `Raw Observation → Canonical Percept` со structured core + optional views.

## DU-09 — Goal System

[`goals.md`](goals.md): `Goal Proposal → Committed Goal Graph`.

## DU-10 — Cortex

[`cortex.md`](cortex.md): backend-neutral semantic capability boundary.

## DU-11 — Memory Core

[`memory.md`](memory.md): `MemoryRecord ≠ embedding/index entry`; Memory ≠ replay.

## DU-12 — World Model

[`world-model.md`](world-model.md): belief/assimilation/prediction/imagination разделены.

## DU-13 — Self Model

[`self-model.md`](self-model.md): capability facts ≠ competence ≠ Self Prediction.

## DU-14 — Intrinsic Signals

[`intrinsic-signals.md`](intrinsic-signals.md): independent typed signals, без mandatory intrinsic reward.

## DU-15 — Drives

[`drives.md`](drives.md): persistent typed regulatory state, без global motivation scalar.

## DU-16 — Appraisal

[`appraisal.md`](appraisal.md): multidimensional event-centered appraisal, без mandatory emotion/global valence.

## DU-17 — Affect Dynamics

[`affect.md`](affect.md): falsifiable persistent history-dependent state, без mandatory emotion taxonomy/VA/PAD.

## DU-18 — Valuation

[`valuation.md`](valuation.md)

```text
source evidence
→ typed ValueProfile
→ explicit ComparisonPolicy
→ ComparisonResult / optional ScalarizedValue
```

Канонически:

```text
ValueProfile ≠ ScalarizedValue
ValueProfile ≠ Reward/Critic/Policy
predictive uncertainty ≠ RiskProfile
```

Weighted scalar, Pareto/dominance, lexicographic, constraint-first и nonlinear/learned comparison являются допустимыми policy families, а не universal default.

---

# 3. Первый ещё не спроектированный блок — Salience / Attention

Следующий Design Update:

```text
DU-19 — Salience / Attention
```

Предварительная ответственность:

> определять relative priority информации/targets для ограниченного cognitive processing и explicit allocation, используя разрешённые relevance/novelty/urgency/value/uncertainty/context signals, но не становясь Appraisal, Valuation или Workspace.

Нужно определить:

- Salience Target;
- bottom-up/top-down contributions;
- scalar/ranking/allocation semantics;
- limited attention/compute budget;
- competition/normalization;
- persistence/inhibition/hysteresis;
- relation to Appraisal relevance/urgency;
- relation to Valuation;
- relation to Intrinsic Signals/Affect/Drives;
- Memory retrieval/retention boundary;
- Workspace admission boundary;
- Executive/Policy boundary;
- controls/interventions.

Ключевой gate:

> Salience должна иметь observable allocation effect, а не быть ещё одним декоративным score, дублирующим relevance/value.

---

# 4. Будущие области после Salience

## DU-20 — Memory Regulation / Consolidation

Расширяет нейтральный Memory Core: retention, forgetting, eviction, replay priority, consolidation.

## DU-21 — Workspace

Кандидат на ограниченную temporary global-access surface.

## DU-22 — Metacognitive / Executive Control

Регулирует Cortex/retrieval/planning depth/compute budget/goal focus/strategy switching. Не scheduler.

## DU-23 — Policy / Planner

Преобразует state/predictions/valuation в candidate action/plan.

## DU-24 — Action Gate / Executor

```text
selected action
≠
executed action
≠
observed outcome
```

---

# 5. Research/runtime infrastructure после cognitive architecture

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

Только после `DU-32` создаются concrete software versions и их `implementation-sequence.md`.

---

# 6. Dependency graph проектирования

```text
System boundaries
    ↓
CognitiveState / Module Protocol / Observability
    ↓
Environment
    ↓
Perception
    ├──────────────→ Goal System
    ├──────────────→ Cortex
    └──────────────→ Memory Core
                         ↓
               World Model + Self Model
                         ↓
                Intrinsic Signals
                         ↓
                       Drives
                         ↓
                     Appraisal
                         ↓
                  Affect Dynamics
                         ↓
                     Valuation
                         ↓
               Salience / Attention
                  ┌──────┴──────┐
                  ↓             ↓
       Memory Regulation     Workspace
                  └──────┬──────┘
                         ↓
           Metacognitive / Executive Control
                         ↓
                  Policy / Planner
                         ↓
                Action Gate / Executor
                         ↓
                     Environment
```

Это design dependency graph, не runtime DAG.

---

# 7. Правило независимой диагностируемости

Для каждого принятого subsystem определить минимум:

- disabled/`No*` behavior;
- Dummy/control implementation;
- random/shuffled/constant control, если meaningful;
- parameter/compute-matched control;
- logging/evidence;
- intervention points;
- checkpoint state;
- subsystem metrics;
- failure/degradation behavior.

---

# 8. Правило предотвращения скрытой дубликации

Особенно внимательно проверять:

```text
Appraisal ↔ Valuation
Affect ↔ Valuation
Valuation ↔ Policy critic
Valuation ↔ Salience
Drives ↔ Intrinsic Signals
Drives ↔ Affect
Self Model ↔ Metacognition
Salience ↔ Workspace
CognitiveState ↔ Workspace
Goal System ↔ Policy
Memory ↔ Workspace
Scheduler ↔ Executive Control
```

---

# 9. Следующий шаг

Точный порядок задаётся [`../documentation-plan.md`](../documentation-plan.md).

Следующий допустимый этап:

```text
DU-19 — Salience / Attention
```
