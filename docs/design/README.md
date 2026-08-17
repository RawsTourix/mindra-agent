# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, subsystem boundaries, contracts, ADR и будущие version plans.

На текущем этапе приняты `DU-01 … DU-19`. Реализация ещё не начата.

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
- [`modules/salience.md`](modules/salience.md) — `DU-19`: contextual Salience Profiles, explicit budgets и Attention Allocation.

Карта областей: [`modules/README.md`](modules/README.md).

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0019` — accepted.

Последнее решение:

- [`ADR-0019`](decisions/ADR-0019-budgeted-contextual-salience-allocation.md) — contextual Salience Profiles + explicit budgeted Attention Allocation.

## Candidate contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Последний добавленный contract:

- [`contracts/salience.md`](contracts/salience.md).

Exact Python API ещё не frozen.

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Каждый DU должен:

- закрывать ограниченный design scope;
- исследовать реальные альтернативы;
- фиксировать responsibilities/non-goals/invariants;
- создавать ADR при существенном выборе;
- обновлять canonical owner/contracts/status;
- не протаскивать downstream decisions;
- завершаться consistency review.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-20 — Memory Regulation / Consolidation
```

---

# Ключевые инварианты после DU-19

```text
Appraisal relevance ≠ Salience
Value ≠ Salience
Intrinsic novelty ≠ Salience
SalienceProfile ≠ AttentionAllocation
AttentionAllocation ≠ Workspace admission
AttentionAllocation ≠ Executive compute decision
AttentionAllocation ≠ Policy decision
Cortex attention weight ≠ MINDRA Salience
Memory retrieval score ≠ Salience
```

- Salience работает только с explicit candidate set;
- Salience всегда имеет explicit purpose/context;
- scalar salience не является обязательным source of truth;
- budget приходит от consumer/context;
- ranking, gating и resource allocation различаются;
- bottom-up и top-down evidence сохраняются различимыми;
- stateful inhibition/focus persistence допустимы, но stateless baseline обязателен;
- Memory retention остаётся `DU-20`;
- Workspace admission остаётся `DU-21`;
- actual compute/Cortex/retrieval strategy остаётся `DU-22`;
- final action choice остаётся `DU-23`;
- функциональная Salience должна менять реальное allocation/processing, а не только логировать score.

Фактический статус: [`current.md`](current.md).
