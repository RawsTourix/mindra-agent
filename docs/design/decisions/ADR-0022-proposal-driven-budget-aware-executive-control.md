# ADR-0022 — Proposal-driven budget-aware Executive Control поверх invariant Scheduler

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-22 — Metacognitive / Executive Control`

---

# 1. Контекст

После `DU-05` MINDRA имеет invariant `Cognitive Scheduler`, который обеспечивает допустимое causal execution, но намеренно не решает, **какое optional cognition полезно выполнить**.

После `DU-13/19/21` существуют Self Model, Salience и Workspace, но ни один из них не владеет global cognitive resource allocation.

Нужно решить:

- нужен ли отдельный adaptive Executive Control;
- как выбирать между optional internal operations;
- как остановить/продолжить deliberation;
- кто управляет agent-visible cognitive budget;
- как не превратить Executive в Service Locator или Policy.

---

# 2. Рассмотренные варианты

1. только fixed runtime schedule, без отдельного Executive;
2. learned/dynamic Scheduler, который сам решает и допустимость, и полезность;
3. Executive как central orchestrator с direct handles на все modules/services;
4. Executive как часть Policy/Planner;
5. один scalar confidence/Value-of-Computation threshold;
6. proposal-driven budget-aware Executive Control, выбирающий из declared internal operations, при invariant Scheduler validation.

---

# 3. Требования

Решение должно:

- сохранять Scheduler как invariant execution owner;
- сохранять Policy/Planner как downstream owner поведения/плана;
- отделять internal MetaAction от Environment Action;
- не использовать runtime Service Locator;
- иметь explicit resource envelope/ledger;
- поддерживать adaptive stop/continue;
- поддерживать Cortex/retrieval/rollout/consolidation как optional operations без direct ownership leakage;
- учитывать unavailable/degraded capabilities;
- поддерживать causal observability/intervention;
- иметь matched fixed/random controls;
- быть falsifiable по equal-compute evaluation;
- не фиксировать конкретный learned algorithm.

---

# 4. Вариант A — Только fixed runtime schedule

```text
N cycles
→ fixed retrieval
→ fixed Cortex calls
→ fixed rollout depth
→ Policy
```

## Плюсы

- просто;
- детерминируемо;
- низкий control overhead;
- отличный baseline.

## Минусы

- easy/hard situations получают одинаковый compute;
- не адаптируется к competence/uncertainty/capability degradation;
- budget allocation нельзя исследовать как agent-owned function;
- ограниченный compute может расходоваться неэффективно.

**Решение:** отклонён как единственная architecture; обязателен как `NoExecutive`/fixed baseline.

---

# 5. Вариант B — Cognitive Scheduler становится learned controller

## Плюсы

- меньше компонентов;
- scheduler уже знает execution plan/resources.

## Минусы

- смешивает invariant safety/causal mechanics с learned task-dependent decisions;
- трудно отделить invalid execution от плохого cognitive choice;
- learned controller может начать обходить dependency semantics;
- существенно ухудшается воспроизводимость и verification.

**Решение:** отклонён.

Scheduler остаётся механикой допустимого исполнения.

---

# 6. Вариант C — Central orchestrator / Service Locator

```text
Executive
├── memory.retrieve()
├── cortex.generate()
├── world_model.rollout()
└── workspace.write()
```

## Плюсы

- очень легко программировать orchestration;
- полный контроль в одном месте.

## Минусы

- нарушает `ADR-0002`;
- Executive знает concrete services;
- ownership/provenance скрываются;
- модульность становится декларативной только на бумаге;
- тестирование/ablation усложняются.

**Решение:** отклонён.

---

# 7. Вариант D — Executive внутри Policy/Planner

## Плюсы

- action planning и reasoning depth можно совместно оптимизировать;
- меньше subsystem boundaries.

## Минусы

- невозможно независимо исследовать cognitive resource allocation;
- Policy получает власть над Cortex/Memory/Workspace lifecycle;
- planning semantics и general meta-control смешиваются;
- NoPlanner/alternate Policy configurations труднее сравнивать.

**Решение:** отклонён как canonical ownership.

Policy может предлагать planning-related meta-actions, но selection/resource control остаётся Executive boundary.

---

# 8. Вариант E — Один scalar confidence/VOC threshold

Например:

```text
if confidence < 0.6:
    think_more()
```

или:

```text
if VOC > 0:
    compute()
```

## Плюсы

- понятно;
- легко реализовать;
- хороший baseline.

## Минусы

- competence, estimate uncertainty, operation cost, risk, urgency и capability availability схлопываются;
- один threshold не выбирает между разными operations;
- scale/calibration drift может полностью менять control;
- hard multi-dimensional budgets плохо выражаются.

**Решение:** отклонён как universal architecture; scalar threshold/VOC допускается как concrete policy/control.

---

# 9. Вариант F — Proposal-driven budget-aware Executive Control

Conceptually:

```text
MetaActionProposal[]
        +
ExecutiveObservation
        +
CognitiveResourceEnvelope
        ↓
Executive policy
        ↓
ExecutiveDecision
        ↓
Scheduler validation
        ↓
allowed internal operation(s)
```

## Плюсы

- adaptive cognition отделена от execution mechanics;
- Executive не знает concrete service objects;
- multi-dimensional budget explicit;
- operation selection/stop/continue легко наблюдать/intervene;
- Self/Salience/Workspace остаются evidence providers;
- capability degradation естественно представима;
- equal-compute controls возможны;
- Policy/Planner остаётся независимым downstream layer.

## Минусы

- больше metadata/proposals;
- появляется control overhead;
- нужно оценивать estimated/actual costs;
- poor controller может тратить compute хуже fixed schedule;
- требуется строгая защита от превращения MetaActionCatalog в Service Locator.

**Решение:** принято.

---

# 10. Принятое решение

MINDRA принимает **proposal-driven budget-aware Executive Control**.

Канонически:

```text
Executive Control ≠ Scheduler
Executive Control ≠ Policy/Planner
Internal MetaAction ≠ Environment Action
MetaActionProposal ≠ execution
ExecutiveDecision ≠ direct service call
Salience/Self Model ≠ controller
ResourceEnvelope ≠ runtime telemetry dump
```

Executive:

- читает declared monitoring context;
- выбирает из explicit proposals/catalog;
- резервирует/распределяет agent-visible budget;
- решает continue/yield;
- публикует versioned decision;
- передаёт requests invariant Scheduler/runtime validation.

---

# 11. Resource ownership

Hard resource limit задаётся внешней configuration/runtime/task boundary и при необходимости становится намеренно agent-visible `CognitiveResourceEnvelope`.

Executive владеет **allocation/ledger semantics внутри предоставленного envelope**, но не может сам увеличить hard resource.

Provider/runtime остаётся последним hard enforcement layer.

---

# 12. Stop semantics

Executive stop означает:

```text
закончить optional deliberation
→ yield to Policy
```

а не:

```text
выбрать Environment action
→ Action Commit
```

Final behavior остаётся `DU-23/24`.

---

# 13. Последствия

## Положительные

- можно исследовать adaptive compute отдельно от task policy;
- easy/hard cases могут получать разный compute;
- Cortex/retrieval/rollout usage становится объяснимым;
- capability degradation не требует hidden fallback;
- возможен performance/resource frontier;
- stopping/operation selection становятся causal intervention targets.

## Отрицательные

- architecture сложнее fixed pipeline;
- controller сам потребляет compute;
- learned control требует отдельной training/evaluation discipline;
- cost estimation может быть неточным;
- существует риск centralization через чрезмерно широкие proposals/context.

---

# 14. Evaluation obligations

Нужно сравнивать минимум:

```text
Adaptive Executive
vs NoExecutive/fixed schedule
vs FixedBudget
vs RandomMetaAction
vs SimpleThreshold
vs SalienceOnly
vs CostUnaware
vs MatchedLearnedRouter
```

При этом сравнение должно учитывать **одинаковый/сопоставимый actual cognitive resource**, а не только одинаковое число Decision Windows.

Обязательны:

- budget sweeps;
- operation-selection distribution;
- stop/continue distribution;
- resource-estimation error;
- competence/uncertainty/cost interventions;
- capability degradation tests;
- OOD difficulty shift;
- controller overhead accounting.

---

# 15. Negative gate

ADR должен быть пересмотрен, если:

- fixed schedule при matched compute не хуже;
- adaptive policy почти всегда константна;
- control decisions не чувствительны к релевантному evidence;
- matched generic router объясняет эффект;
- control overhead систематически превышает gain;
- Executive требует ambient global state/service access для работы.

В таком случае Executive boundary может быть упрощена до fixed/version-level runtime policy.

---

# 16. Что решение не определяет

ADR не выбирает:

- controller NN;
- optimizer/objective;
- Value-of-Computation formula;
- confidence threshold;
- resource dimensions первой версии;
- default budget;
- Cortex quota;
- rollout depth;
- control-point frequency;
- GoalFocus encoding;
- Policy/Planner algorithm;
- Python dispatch/runtime implementation.
