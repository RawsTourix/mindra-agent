# Карта проектирования модулей MINDRA

## Статус документа

Этот документ является **картой архитектурных областей и порядка их проектирования**, а не заменой канонических subsystem design.

Наличие блока в карте не гарантирует, что он останется отдельным trainable module. Соответствующий Design Update может:

- принять отдельный модуль;
- разделить область;
- объединить её с другой;
- принять algorithmic/rule-based mechanism;
- отложить или отклонить отдельную boundary.

Главное правило:

> Отдельный модуль существует не из-за когнитивной аналогии, а при наличии самостоятельной вычислительной ответственности, явного контракта и независимо проверяемого функционального вклада.

Фактический статус каждого блока определяется его каноническим документом и [`../current.md`](../current.md).

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

`Intrinsic Signal Providers` находятся здесь как источник внутренних **измерений опыта**, а не как готовая мотивация/reward.

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

Канонический документ: [`environment.md`](environment.md).

Главное:

```text
Agent Interaction Plane
≠
Environment Research Plane
```

`MicroWorld` — reference environment family, а не универсальное внутреннее представление MINDRA.

## DU-08 — Perception

Канонический документ: [`perception.md`](perception.md).

Главное:

```text
Raw Observation
→ Canonical Percept
├── structured Semantic Core
└── optional versioned Feature Views
```

## DU-09 — Goal System

Канонический документ: [`goals.md`](goals.md).

Главное:

```text
Goal Proposal
→ Goal System
→ Committed Goal Graph
```

Goal не является reward/value/policy.

## DU-10 — Cortex

Канонический документ: [`cortex.md`](cortex.md).

Главное:

```text
semantic Cortex Request
→ Cortex Gateway
→ backend-specific adapter/provider
```

Concrete LLM не является архитектурой MINDRA.

## DU-11 — Memory Core

Канонический документ: [`memory.md`](memory.md).

Главное:

```text
MemoryRecord
≠
embedding / vector-index entry
```

Memory отделена от trajectory log и training replay.

## DU-12 — World Model

Канонический документ: [`world-model.md`](world-model.md).

Главное:

```text
actual evidence
→ World Belief assimilation

World Belief + candidate action
→ prediction / imagination
```

Prediction/imagination не является observed fact.

## DU-13 — Self Model

Канонический документ: [`self-model.md`](self-model.md).

Главное:

```text
Capability Fact
≠
Competence Estimate
≠
Self Prediction
```

Self Model оценивает собственные функциональные возможности, но не управляет cognition/behavior.

## DU-14 — Intrinsic Signals

Канонический документ: [`intrinsic-signals.md`](intrinsic-signals.md).

Главное:

```text
experience evidence
→ independent typed Signal Providers
→ IntrinsicSignalBundle
```

Нет mandatory `intrinsic_reward`.

## DU-15 — Drives

Канонический документ: [`drives.md`](drives.md).

Главное:

```text
Intrinsic Signals / internal events / logical time
                ↓
            Drive System
                ↓
          DriveStateSet
```

`Drive System` поддерживает persistent typed regulatory state.

Канонически:

```text
Intrinsic Signal ≠ Drive State
Drive State ≠ Drive Pressure ≠ Utility/Value
homeostatic drive ≠ mandatory form of every drive
Drive System ≠ global motivation scalar
```

Cross-drive interaction explicit, drives не commit Goals напрямую и не выбирают actions.

---

# 3. Первый ещё не спроектированный блок — Appraisal

Следующий Design Update:

```text
DU-16 — Appraisal
```

Предварительная ответственность:

> оценивать значение конкретного события/ситуации для текущего Agent с учётом Goal, Drive, World/Self Model, Memory и доступного evidence.

Нужно будет определить:

- event boundary;
- multidimensional appraisal semantics;
- goal congruence;
- controllability/coping potential;
- relevance/urgency;
- event-level valence;
- actual vs predicted/imagined appraisal;
- relation to Intrinsic Signals;
- relation to Drives;
- relation to future Affect;
- relation to Valuation;
- rule-based vs learned semantics;
- calibration/evidence;
- intervention/control implementations.

Ключевой gate:

> Appraisal должна иметь самостоятельную event-level responsibility и не сводиться к scalar reward/value prediction.

---

# 4. Будущие области после Appraisal

## DU-17 — Affect Dynamics

Кандидат на persistent affective state, интегрирующий appraisal во времени.

Сохраняется отдельным модулем только если показывает функционально отличимую роль от `Appraisal + Drives`.

## DU-18 — Valuation

Центральная decision-relevant система ценности.

Должна развести:

```text
external feedback
Intrinsic Signals
Drive State
Goal progress
Appraisal
Affect
predicted future state
risk / uncertainty
```

и только здесь решать, нужна ли scalarization.

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
- transition от episodic опыта к более медленным learned structures.

## DU-21 — Workspace

Кандидат на ограниченную временную global-access surface.

Сохраняется только если роль не сводится к `CognitiveState`.

## DU-22 — Metacognitive / Executive Control

Использует Self Model/uncertainty и другие signals для регулирования самого cognitive process:

- Cortex invocation;
- retrieval;
- planning depth;
- compute budget;
- goal focus;
- strategy switching.

Это не runtime scheduler.

## DU-23 — Policy / Planner

Преобразует доступное состояние, прогнозы и values в candidate action/plan.

Policy не должна становиться владельцем всех остальных подсистем.

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

Это **порядок семантического проектирования**, а не окончательный runtime DAG.

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

Фактический runtime будет иметь temporal feedback loops; порядок выше нужен только для design dependencies.

---

# 7. Правило независимой диагностируемости

Для каждого принятого cognitive module/subsystem нужно определить минимум:

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
2. Отличается ли его state семантически, а не только названием?
3. Есть ли уникальный downstream effect?
4. Можно ли независимо измерить вклад?
5. Нужен ли отдельный trainable network?

Особенно внимательно проверять пары:

```text
Appraisal ↔ Valuation
Appraisal ↔ Affect
Drives ↔ Intrinsic Signals
Drives ↔ Affect
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
DU-16 — Appraisal
```
