# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-22` завершены и приняты. Реализация ещё не начата.**

Приняты:

- foundation/system boundaries `DU-01 … DU-06`;
- Environment/MicroWorld;
- Perception;
- Goal System;
- Cortex boundary;
- Memory Core;
- World Model;
- Self Model;
- Intrinsic Signals;
- Drives;
- Appraisal;
- Affect;
- Valuation;
- Salience / Attention;
- Memory Regulation / Consolidation;
- Workspace;
- Metacognitive / Executive Control;
- 22 accepted ADR;
- candidate semantic contracts для subsystem boundaries `DU-07 … DU-22`.

---

# 2. Завершённые Design Updates

```text
DU-00 — Documentation Foundation
DU-01 — System Context
DU-02 — Dependency & Composition Rules
DU-03 — Runtime / Temporal Model
DU-04 — CognitiveState Semantics
DU-05 — Module Protocol & Scheduling
DU-06 — Observability & Intervention
DU-07 — Environment / MicroWorld Contract
DU-08 — Perception / Canonical Representation
DU-09 — Goal System
DU-10 — Cortex Boundary
DU-11 — Memory Core
DU-12 — World Model
DU-13 — Self Model
DU-14 — Intrinsic Signals
DU-15 — Drives
DU-16 — Appraisal
DU-17 — Affect Dynamics
DU-18 — Valuation
DU-19 — Salience / Attention
DU-20 — Memory Regulation / Consolidation
DU-21 — Workspace
DU-22 — Metacognitive / Executive Control
```

---

# 3. DU-22

Canonical design:

- [`modules/executive-control.md`](modules/executive-control.md)

Candidate contract:

- [`contracts/executive-control.md`](contracts/executive-control.md)

Accepted decision:

- [`ADR-0022`](decisions/ADR-0022-proposal-driven-budget-aware-executive-control.md)

Research pass:

- [`../research/literature/DU-22-executive-control-landscape-2026-08.md`](../research/literature/DU-22-executive-control-landscape-2026-08.md)

Главные результаты:

```text
metacognitive monitoring ≠ Executive Control
Executive Control ≠ Cognitive Scheduler
Executive Control ≠ Policy / Planner
Internal MetaAction ≠ Environment Action
MetaActionProposal ≠ executed operation
ExecutiveDecision ≠ direct service call
CognitiveResourceEnvelope ≠ raw runtime telemetry
resource estimate ≠ reservation ≠ actual consumption
Salience / Self Model ≠ controller
Executive stop ≠ Action Commit
```

- Executive Control принят как proposal-driven budget-aware agent-owned control boundary;
- отдельная boundary имеет conditional/falsifiable module gate;
- invariant Scheduler остаётся owner допустимого execution/commit;
- Executive выбирает только из explicit `MetaActionProposal` и declared `InternalOperationCatalog`;
- runtime Service Locator/direct provider handles Executive не получает;
- resource envelope предоставляется внешней/version/runtime boundary и при необходимости намеренно становится agent-visible;
- Executive может распределять/резервировать resource только внутри предоставленного envelope;
- budget может быть multi-dimensional;
- hard и soft resource semantics разведены;
- physical latency/Colab/network delay не становятся cognitive cost автоматически;
- stop/continue решения принимаются на explicit `Executive Control Point` относительно committed state;
- `yield_to_policy` завершает optional deliberation, но не выбирает Environment action;
- Cortex/retrieval/World Model rollout/consolidation проходят через explicit proposal → ExecutiveDecision → Scheduler validation;
- Executive может управлять temporary Goal focus refs, но не мутирует Goal Graph;
- Workspace admission остаётся responsibility Workspace, даже если Executive регулирует предоставляемый Workspace budget/context;
- Self Model и Salience предоставляют evidence, но не control commands;
- real compute, потраченный на imagination, списывается из real budget, а simulated future budget остаётся branch-local;
- Executive state/ledger входят в causally relevant Agent Snapshot;
- обязательны `NoExecutive`, fixed schedule/budget, random, threshold, Salience-only, cost-unaware и matched learned-router controls;
- полезность Executive оценивается по performance/resource frontier и equal/matched compute comparisons;
- если fixed/matched controls объясняют эффект, отдельная Executive boundary должна быть пересмотрена.

---

# 4. Следующий допустимый Design Update

```text
DU-23 — Policy / Planner
```

Цель `DU-23` — спроектировать **границу формирования behavioral candidates, planning и final action-selection intention** после того, как MINDRA уже умеет регулировать объём внутреннего compute.

Обязательные вопросы:

```text
Policy module gate
Planner module gate
Policy ≠ Executive Control
Planner ≠ World Model
plan ≠ imagined trajectory
Action Candidate ≠ selected action ≠ executed action
reactive policy vs explicit planning
candidate generation
candidate evaluation через Valuation
Goal / Workspace / Memory / World / Self inputs
Cortex-assisted planning boundary
subgoal proposal → Goal System
planning under partial observability
risk/constraints/incomparability
stochastic policy semantics
planning horizon / search tree ownership
Executive budget → Planner compute boundary
plan persistence / replanning
failure/degradation
branch provenance
observability/intervention
NoPlanner / reactive / random / oracle controls
snapshot/revision
```

Нужно особенно определить:

- является ли `Policy` единым owner final behavioral choice или Planner отдельный provider candidates/plans;
- где заканчивается Executive решение «ещё считать» и начинается решение «какое поведение выбрать»;
- как World Model предоставляет rollout, но не выбирает план;
- как Valuation сравнивает candidates, но не делает final choice автоматически;
- как incomparability/constraints обрабатываются Policy;
- как Planner предлагает subgoal через Goal System, а не мутирует Goal Graph;
- как Cortex может помогать generation/planning, не становясь owner Policy;
- что считается committed selected-action intention до `DU-24 Action Gate`;
- какой causal evidence нужен, чтобы доказать пользу Planner сверх reactive Policy;
- при каком отрицательном результате отдельный Planner должен быть отключён/удалён.

После принятия `DU-23` допускается:

```text
DU-24 — Action Boundary / Gate / Executor
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

- Policy / Planner;
- Action Gate / Executor;
- Experience / Data / Replay schema;
- Training Lifecycle;
- Checkpoint / Reproducibility / Compute;
- MINDRA-Eval;
- Engineering Testing;
- Research Claims / Limitations;
- Contract + ADR Freeze;
- Version Roadmap;
- implementation sequences.

Также не выбраны concrete Python/framework/model/algorithm implementations.

---

# 6. Implementation status

```text
Исследовательская/production реализация: не начата
Дорожная карта версий: не спроектирована
Software version: отсутствует
Implementation HEAD: отсутствует
```

Detailed design сам по себе не разрешает Codex начинать implementation до `DU-32` и соответствующего version/implementation sequence.
