# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, subsystem boundaries, contracts, ADR и будущие version plans.

На текущем этапе приняты `DU-01 … DU-23`. Реализация ещё не начата.

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
- [`modules/executive-control.md`](modules/executive-control.md) — `DU-22`
- [`modules/policy-planner.md`](modules/policy-planner.md) — `DU-23`: Policy-owned final behavioral selection с optional/falsifiable Planner provider.

Карта областей: [`modules/README.md`](modules/README.md).

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0023` — accepted.

Последнее решение:

- [`ADR-0023`](decisions/ADR-0023-policy-owned-selection-optional-planner.md) — обязательный Policy owner selected-action intention и optional Planner как provider планов/action candidates.

## Candidate contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Последний добавленный contract:

- [`contracts/policy-planner.md`](contracts/policy-planner.md).

Exact Python API ещё не frozen.

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Каждый DU должен закрывать ограниченный scope, исследовать реальные альтернативы, фиксировать responsibilities/invariants, создавать ADR при существенном выборе, синхронизировать contracts/status и завершаться consistency review.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-24 — Action Boundary / Gate / Executor
```

---

# Ключевые инварианты после DU-23

```text
Policy ≠ Planner
Planner ≠ World Model
Plan ≠ ImaginedTrajectory
Valuation ≠ Policy Decision
Executive Control ≠ Policy
ActionCandidate ≠ SelectedActionIntent
SelectedActionIntent ≠ Action Commit ≠ Executed Action
```

- Policy является единственным semantic owner selected behavioral intention normal runtime способом;
- Planner остаётся optional/falsifiable capability/provider;
- reactive/no-Planner configuration first-class;
- Policy работает с explicit `PolicyCandidateSet`;
- Planner строит plans/candidates относительно World Belief и agent-visible context;
- hidden Environment state недоступен Planner normal runtime способом;
- Plan может быть contingent/persistent, но имеет assumptions/revision/stale/invalidation semantics;
- Valuation предоставляет comparison evidence, а не final selection;
- `incomparable` не требует fake scalarization;
- Policy может вернуть `DecisionDeferral` и proposals дополнительного cognition;
- Planner subgoal проходит Goal Proposal boundary;
- planning compute регулируется Executive Control;
- Cortex может помогать generation/planning, но не становится Policy owner;
- stochastic selection сохраняет RNG/provenance;
- Planner contribution должен проверяться против reactive и matched controls при сопоставимом compute;
- `SelectedActionIntent` ещё не разрешено и не исполнено — это boundary `DU-24`.

Фактический статус: [`current.md`](current.md).
