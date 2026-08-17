# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, subsystem boundaries, contracts, ADR и будущие version plans.

На текущем этапе приняты `DU-01 … DU-24`. Реализация ещё не начата.

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
- [`modules/policy-planner.md`](modules/policy-planner.md) — `DU-23`
- [`modules/action-boundary.md`](modules/action-boundary.md) — `DU-24`: authorization, post-authorization/pre-dispatch `Action Commit`, dispatch/execution correlation и retry/idempotency semantics.

Карта областей: [`modules/README.md`](modules/README.md).

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0024` — accepted.

Последнее решение:

- [`ADR-0024`](decisions/ADR-0024-post-authorization-pre-dispatch-action-commit.md) — `Action Commit` после authorization и до dispatch, explicit override provenance и stable dispatch/idempotency semantics.

## Candidate contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Последний добавленный contract:

- [`contracts/action-boundary.md`](contracts/action-boundary.md).

Exact Python API ещё не frozen.

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Каждый DU должен закрывать ограниченный scope, исследовать реальные альтернативы, фиксировать responsibilities/invariants, создавать ADR при существенном выборе, синхронизировать contracts/status и завершаться consistency review.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-25 — Experience / Data / Replay
```

---

# Ключевые инварианты после DU-24

```text
SelectedActionIntent ≠ AuthorizedAction
AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch
Dispatch ≠ Environment Transition
Environment receipt accepted ≠ execution success
Policy choice ≠ external override
transport failure ≠ Environment no-effect
execution_unknown ≠ definitely_not_sent
```

- stale/malformed/unauthorized intent не commit'ится;
- normal Gate не является второй Policy;
- behavior-changing substitution требует explicit override provenance;
- `Action Commit` находится после финальной authorization и до dispatch;
- post-commit failure не удаляет committed behavioral history;
- retry не создаёт новый Action Commit;
- blind retry запрещён при unknown non-idempotent execution;
- universal physical exactly-once не обещается;
- Dispatcher является execution infrastructure, Environment владеет transition/outcome;
- terminal outcome фиксируется до reset;
- causal evidence связывает Policy candidate до Outcome Commit.

Фактический статус: [`current.md`](current.md).
