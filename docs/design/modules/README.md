# Карта проектирования модулей MINDRA

## Статус документа

Этот документ является **картой архитектурных областей и порядка их проектирования**, а не заменой канонических subsystem design.

Наличие блока в карте не гарантирует, что он навсегда останется отдельным trainable module. Соответствующий Design Update может:

- принять отдельный модуль;
- разделить область;
- объединить её с другой;
- принять algorithmic/rule-based mechanism;
- отложить или отклонить boundary.

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

`Intrinsic Signal Providers` являются измерениями опыта, а не готовым reward. `Drives` являются persistent regulatory states. `Appraisal` оценивает конкретный target. `Affect` интегрирует appraisal-history во времени. `Valuation` ещё не спроектирована и будет первой boundary, где появится decision-relevant comparability/desirability.

## 1.4. Выбор и исполнение поведения

```text
Policy / Planner
Action Gate / Executor
```

## 1.5. Обучение и исследовательская инфраструктура

Это не обязательно когнитивные модули Agent:

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

[`environment.md`](environment.md)

```text
Agent Interaction Plane
≠
Environment Research Plane
```

## DU-08 — Perception

[`perception.md`](perception.md)

```text
Raw Observation
→ Canonical Percept
├── structured Semantic Core
└── optional versioned Feature Views
```

## DU-09 — Goal System

[`goals.md`](goals.md)

```text
Goal Proposal
→ Goal System
→ Committed Goal Graph
```

## DU-10 — Cortex

[`cortex.md`](cortex.md)

```text
semantic Cortex Request
→ Cortex Gateway
→ backend-specific adapter/provider
```

## DU-11 — Memory Core

[`memory.md`](memory.md)

```text
MemoryRecord
≠
embedding / vector-index entry
```

Memory отделена от trajectory log и training replay.

## DU-12 — World Model

[`world-model.md`](world-model.md)

```text
actual evidence
→ World Belief assimilation

World Belief + candidate action
→ prediction / imagination
```

## DU-13 — Self Model

[`self-model.md`](self-model.md)

```text
Capability Fact
≠
Competence Estimate
≠
Self Prediction
```

## DU-14 — Intrinsic Signals

[`intrinsic-signals.md`](intrinsic-signals.md)

```text
experience evidence
→ independent typed Signal Providers
→ IntrinsicSignalBundle
```

Нет mandatory `intrinsic_reward`.

## DU-15 — Drives

[`drives.md`](drives.md)

```text
Intrinsic Signals / internal events / logical time
                ↓
            Drive System
                ↓
          DriveStateSet
```

```text
Intrinsic Signal ≠ Drive State
Drive State ≠ Drive Pressure ≠ Utility/Value
homeostatic drive ≠ mandatory form of every drive
Drive System ≠ global motivation scalar
```

## DU-16 — Appraisal

[`appraisal.md`](appraisal.md)

```text
Appraisal Target
+
revisioned Agent context
        ↓
Appraisal System
        ↓
multidimensional AppraisalProfile
```

```text
Appraisal ≠ Affect ≠ Valuation
relevance ≠ Salience
controllability ≠ coping potential
```

## DU-17 — Affect Dynamics

[`affect.md`](affect.md)

```text
AffectStateSet_t
+
eligible AppraisalRecord(s)
+
logical time
        ↓
Affect Dynamics
        ↓
AffectStateSet_(t+1)
```

Канонически:

```text
Appraisal Record ≠ Affect State
Affect State ≠ Drive State
Affect State ≠ Utility/Value/Reward
Affect State ≠ emotion label
```

Affect принят как **falsifiable** history-dependent state boundary. Его самостоятельность должна позднее проверяться против `NoAffect`, `ResetEveryEvent`, shuffled-history и matched recurrent controls.

---

# 3. Первый ещё не спроектированный блок — Valuation

Следующий Design Update:

```text
DU-18 — Valuation
```

Предварительная ответственность:

> формировать decision-relevant оценку candidate states/outcomes/actions/trajectories на основании разнородных Goals, Drives, Appraisal, Affect, World/Self evidence без преждевременного предположения одного universal reward scalar.

Нужно будет определить:

- valuation target boundary;
- vector/structured/scalar semantics;
- scalarization timing;
- multi-Goal/multi-Drive conflicts;
- immediate vs future value;
- state/action/outcome/trajectory value surfaces;
- external feedback boundary;
- Intrinsic Signals boundary;
- Affect modulation;
- risk/uncertainty;
- Self Model feasibility/cost;
- imagined/counterfactual valuation;
- границу с RL reward/critic;
- controls/interventions/calibration.

Ключевой gate:

> Valuation должна создать самостоятельную decision-relevant comparability, но не превращаться в скрытый универсальный reward без явного решения о scalarization.

---

# 4. Будущие области после Valuation

## DU-19 — Salience / Attention

Определяет, какие данные получают приоритет ограниченного cognitive processing.

Salience должна иметь observable downstream effect, а не быть декоративным score.

## DU-20 — Memory Regulation / Consolidation

Расширяет нейтральный Memory Core:

- retention;
- forgetting;
- eviction;
- replay priority;
- consolidation;
- переход от episodic опыта к более медленным learned structures.

## DU-21 — Workspace

Кандидат на ограниченную временную global-access surface.

Сохраняется только если роль не сводится к `CognitiveState`.

## DU-22 — Metacognitive / Executive Control

Регулирует сам cognitive process:

- Cortex invocation;
- retrieval;
- planning depth;
- compute budget;
- goal focus;
- strategy switching.

Это не runtime scheduler.

## DU-23 — Policy / Planner

Преобразует доступное состояние, прогнозы и values в candidate action/plan.

## DU-24 — Action Gate / Executor

Разделяет:

```text
selected action
≠
executed action
≠
observed outcome
```

---

# 5. Research/runtime infrastructure после cognitive architecture

После `DU-24` проектируются:

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

# 6. Текущий dependency graph проектирования

Это порядок **семантического проектирования**, а не окончательный runtime DAG.

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

Runtime позже будет иметь temporal feedback loops. Порядок выше нужен только для design dependencies.

---

# 7. Правило независимой диагностируемости

Для каждого принятого cognitive subsystem определить минимум:

- disabled/`No*` behavior;
- Dummy/control implementation;
- random/shuffled/constant control, если meaningful;
- parameter/compute-matched control, где применимо;
- inputs/outputs для logging;
- intervention points;
- checkpoint state;
- module-specific metrics;
- failure/degradation behavior.

Если subsystem нельзя отключить/подменить без ручного переписывания архитектуры, модульность недостаточна.

---

# 8. Правило предотвращения скрытой дубликации

При проектировании каждого нового блока проверять:

1. Не выполняет ли ответственность уже другой subsystem?
2. Отличается ли state семантически, а не только названием?
3. Есть ли уникальный downstream effect?
4. Можно ли независимо измерить вклад?
5. Нужен ли отдельный trainable network?

Особенно внимательно проверять пары:

```text
Appraisal ↔ Valuation
Appraisal ↔ Affect
Drives ↔ Intrinsic Signals
Drives ↔ Affect
Affect ↔ Valuation
Self Model ↔ Metacognition
Salience ↔ Workspace
CognitiveState ↔ Workspace
Goal System ↔ Policy
World Model ↔ Policy critic
Memory ↔ Workspace
Scheduler ↔ Executive Control
```

---

# 9. Следующий шаг

Точный порядок задаётся [`../documentation-plan.md`](../documentation-plan.md).

Следующий допустимый этап на текущем `main`:

```text
DU-18 — Valuation
```
