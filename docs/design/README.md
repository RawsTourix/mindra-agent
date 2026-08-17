# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, subsystem boundaries, contracts, ADR и будущие version plans.

На текущем этапе приняты `DU-01 … DU-22`. Реализация ещё не начата.

---

# Навигация

## Foundation

- [`principles.md`](principles.md)
- [`glossary.md`](glossary.md)
- [`documentation-plan.md`](documentation-plan.md)
- [`current.md`](current.md)

## Canonical system design

- [`system-context.md`](system-context.md) — `DU-01`
- [`dependency-rules.md`](dependency-rules.md) — `DU-02`
- [`execution-model.md`](execution-model.md) — `DU-03`
- [`cognitive-state.md`](cognitive-state.md) — `DU-04`
- [`module-lifecycle.md`](module-lifecycle.md) — `DU-05`
- [`observability-and-intervention.md`](observability-and-intervention.md) — `DU-06`

## Принятые subsystem boundaries

- [`modules/environment.md`](modules/environment.md) — `DU-07`
- [`modules/perception.md`](modules/perception.md) — `DU-08`
- [`modules/goals.md`](modules/goals.md) — `DU-09`
- [`modules/cortex.md`](modules/cortex.md) — `DU-10`
- [`modules/memory.md`](modules/memory.md) — `DU-11`
- [`modules/world-model.md`](modules/world-model.md) — `DU-12`
- [`modules/self-model.md`](modules/self-model.md) — `DU-13`
- [`modules/intrinsic-signals.md`](modules/intrinsic-signals.md) — `DU-14`
- [`modules/drives.md`](modules/drives.md) — `DU-15`
- [`modules/appraisal.md`](modules/appraisal.md) — `DU-16`
- [`modules/affect.md`](modules/affect.md) — `DU-17`
- [`modules/valuation.md`](modules/valuation.md) — `DU-18`
- [`modules/salience.md`](modules/salience.md) — `DU-19`
- [`modules/memory-regulation.md`](modules/memory-regulation.md) — `DU-20`
- [`modules/workspace.md`](modules/workspace.md) — `DU-21`
- [`modules/executive-control.md`](modules/executive-control.md) — `DU-22`: proposal-driven budget-aware adaptive control optional cognition поверх invariant Scheduler.

Карта областей: [`modules/README.md`](modules/README.md).

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0022` — accepted.

Последнее решение:

- [`ADR-0022`](decisions/ADR-0022-proposal-driven-budget-aware-executive-control.md) — proposal-driven budget-aware Executive Control с explicit resource envelope, MetaAction proposals и Scheduler validation.

## Candidate contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Последний добавленный contract:

- [`contracts/executive-control.md`](contracts/executive-control.md).

Exact Python API ещё не frozen.

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Каждый DU должен закрывать ограниченный scope, исследовать реальные альтернативы, фиксировать responsibilities/invariants, создавать ADR при существенном выборе, синхронизировать contracts/status и завершаться consistency review.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-23 — Policy / Planner
```

---

# Ключевые инварианты после DU-22

```text
Executive Control ≠ Cognitive Scheduler
Executive Control ≠ Policy / Planner
Internal MetaAction ≠ Environment Action
MetaActionProposal ≠ executed operation
ExecutiveDecision ≠ direct service call
CognitiveResourceEnvelope ≠ raw runtime telemetry
resource estimate ≠ reservation ≠ actual consumption
Salience / Self Model ≠ controller
Executive stop / yield ≠ Action Commit
```

- optional cognitive work поступает через explicit proposals/catalog;
- Executive не получает runtime Service Locator;
- Scheduler остаётся owner dependency safety/waves/commit;
- hard resource envelope задаётся явной boundary и не увеличивается Executive самостоятельно;
- budget может быть multi-dimensional;
- stop/continue принимается только на explicit control point относительно committed state;
- Cortex/retrieval/rollout/consolidation не вызываются ambient способом;
- Goal focus не меняет Goal Graph;
- real compute imagination учитывается в real ledger, simulated future budget остаётся branch-local;
- `NoExecutive`, fixed/equal-budget и matched controls обязательны;
- adaptive control должен доказывать пользу на performance/resource frontier, а не за счёт большего compute.

Фактический статус: [`current.md`](current.md).
