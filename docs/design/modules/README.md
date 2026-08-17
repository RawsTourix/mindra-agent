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

`Intrinsic Signal Providers` находятся здесь как источник внутренних **измерений опыта**, а не как уже готовая мотивация или reward.

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

Эти области нельзя смешивать с внутренней психологической интерпретацией Agent только потому, что они работают в том же процессе.

---

# 2. Принятые subsystem boundaries

## Environment — `DU-07`

Канонический владелец: [`environment.md`](environment.md).

Environment задаёт внешний мир и отделяет Agent Interaction Plane от research-only hidden world control.

## Perception / Representation — `DU-08`

Канонический владелец: [`perception.md`](perception.md).

Perception преобразует `Raw Observation` в hybrid `Canonical Percept`, не делая model-specific latent универсальным языком MINDRA.

## Goal System — `DU-09`

Канонический владелец: [`goals.md`](goals.md).

Goal System владеет committed Goal Graph; внешние/Cortex/internal sources создают proposals, а не мутируют goals напрямую.

## Cortex — `DU-10`

Канонический владелец: [`cortex.md`](cortex.md).

Cortex является replaceable semantic capability через Gateway/Adapter boundary, а не центральной архитектурой Agent.

## Memory Core — `DU-11`

Канонический владелец: [`memory.md`](memory.md).

Memory хранит stable `MemoryRecord`; embeddings/indexes являются производными retrieval structures.

## World Model — `DU-12`

Канонический владелец: [`world-model.md`](world-model.md).

World Model поддерживает `World Belief`, assimilation actual evidence, action-conditioned prediction и imagination, не смешивая prediction с observation/value.

## Self Model — `DU-13`

Канонический владелец: [`self-model.md`](self-model.md).

Self Model объединяет self-observable capability facts, context-conditioned competence и calibrated self-predictions, но не принимает executive/behavior decisions.

## Intrinsic Signals — `DU-14`

Канонический владелец: [`intrinsic-signals.md`](intrinsic-signals.md).

Принята multi-provider architecture:

```text
experience-derived evidence
→ typed Intrinsic Signal Providers
→ IntrinsicSignalBundle
```

Канонически:

```text
Intrinsic Signal
≠
Reward
≠
Drive
≠
Utility / Value
```

Signal сообщает о свойстве опыта. Он не определяет автоматически, насколько это свойство желаемо.

---

# 3. Следующие ещё не спроектированные области

## Drives — `DU-15`

Предварительная ответственность:

- persistent internal regulatory state;
- need/deficit/pressure semantics;
- homeostatic/adaptive dynamics, где обосновано;
- saturation/decay/recovery;
- interaction между drives;
- влияние на Goal Proposal и будущую Valuation.

Ключевой вопрос:

```text
одинаковый внешний контекст
+
разное Drive state
→
предсказуемо различающееся downstream поведение
```

при контроле off-target effects.

## Appraisal — `DU-16`

Предварительная ответственность: оценка значения конкретного события/ситуации для текущего Agent в текущем контексте.

Appraisal не должен превращаться в ещё один scalar reward model.

## Affect Dynamics — `DU-17`

Кандидат на persistent internal state, интегрирующий effects Appraisal во времени.

Gate: если отдельная state не имеет функционально отличимой роли от Appraisal/Drives, её следует объединить, а не сохранять ради аналогии.

## Valuation — `DU-18`

Предварительная ответственность: decision-relevant value из нескольких независимых источников:

```text
external feedback
intrinsic signals
goal progress
drives
appraisal
affect
predicted futures
risk / uncertainty
```

Именно здесь, а не в `DU-14`, решается вопрос scalarization/value.

## Salience / Attention — `DU-19`

Предварительная ответственность: приоритет информации и распределение ограниченного cognitive processing.

## Memory Regulation / Consolidation — `DU-20`

Расширяет Memory Core: retention, forgetting, replay scheduling, consolidation и transition от episodic experience к slow learned knowledge.

## Workspace — `DU-21`

Кандидат на ограниченную временную globally available surface.

Gate: если он не даёт роли сверх `CognitiveState`, отдельный Workspace не принимается.

## Metacognitive / Executive Control — `DU-22`

Кандидат на regulation cognition: retrieval, Cortex invocation, planning depth, compute budget и goal focus.

Он не равен техническому `Cognitive Scheduler`.

## Policy / Planner — `DU-23`

Преобразует состояние, predictions и value evidence в candidate actions/plans.

## Action Gate / Executor — `DU-24`

Отделяет выбранное действие от фактически валидированного/исполненного действия и его outcome.

---

# 4. Обучение и исследовательские области

После когнитивных subsystem boundaries проектируются:

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

Точный scope задаёт [`../documentation-plan.md`](../documentation-plan.md).

---

# 5. Предварительный dependency graph

Это **порядок проектирования**, а не окончательный runtime graph.

```text
System boundaries
    ↓
CognitiveState / module protocol
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

Runtime позже будет содержать feedback loops. Порядок выше нужен только для dependency-aware design.

---

# 6. Правило независимой диагностируемости

Для каждого принятого cognitive subsystem/provider нужно определить, где применимо:

- disabled/`No*` behavior;
- Dummy/Control implementation;
- random/shuffled control;
- parameter/compute-matched control;
- observable inputs/outputs;
- intervention points;
- snapshot/checkpoint state;
- module-specific metrics;
- failure/degradation behavior.

Если механизм нельзя отключить или подменить без ручного переписывания соседей, модульность недостаточна.

---

# 7. Правило предотвращения скрытой дубликации

При проектировании каждого нового блока проверять:

1. Не выполняет ли эту ответственность уже другой блок?
2. Отличается ли state семантически, а не только названием?
3. Есть ли уникальный downstream effect?
4. Можно ли независимо измерить вклад?
5. Нужна ли trainable network или достаточно algorithmic transform?

Особенно внимательно проверять:

```text
Appraisal ↔ Valuation
Appraisal ↔ Affect
Drives ↔ Intrinsic Signals
Self Model ↔ Metacognition
Salience ↔ Workspace
CognitiveState ↔ Workspace
Goal System ↔ Policy
World Model ↔ Policy critic
Memory ↔ Workspace
Scheduler ↔ Executive Control
```

---

# 8. Следующий шаг

Текущий первый ещё не спроектированный блок:

```text
DU-15 — Drives
```

Фактический разрешённый шаг всегда подтверждать через [`../current.md`](../current.md).
