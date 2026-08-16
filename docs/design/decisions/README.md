# Architecture Decision Records MINDRA

## Назначение

Этот каталог предназначен для значимых архитектурных решений MINDRA.

ADR создаётся, когда существует несколько реалистичных вариантов, а выбор влияет на module boundaries, internal contracts, state ownership, training semantics, reproducibility, evaluation validity, runtime topology или future version design.

ADR не нужен для каждой локальной implementation detail.

---

# Статусы

- `proposed` — решение подготовлено для review;
- `accepted` — решение принято и является частью текущего design;
- `superseded` — полностью заменено более новым ADR;
- `superseded in part` — частично заменено/уточнено;
- `rejected` — вариант рассмотрен и явно не принят.

---

# Обязательная структура ADR

1. Контекст.
2. Проблема/decision scope.
3. Требования и constraints.
4. Рассмотренные варианты.
5. Evidence/references, если применимо.
6. Принятое решение.
7. Последствия и trade-offs.
8. Что решение намеренно не определяет.
9. Какие canonical design/contracts/version docs должны быть обновлены.

---

# Правила

Если ADR меняет ранее принятый design:

```text
ADR
→ canonical design owner
→ exact internal contracts
→ version plans/status
→ implementation
```

Не оставлять два одновременно действующих противоречащих решения.

Rejected/superseded ADR сохраняются как история reasoning проекта.

Research experiment сам по себе не становится ADR: сначала проводится interpretation/design review.

---

# Реестр

## Accepted

- [`ADR-0001 — Логические границы независимы от deployment topology`](ADR-0001-logical-boundaries-independent-of-deployment.md) — архитектурная принадлежность определяется responsibility/state ownership, а не процессом, устройством или compute provider.
- [`ADR-0002 — Явная композиция и запрет runtime Service Locator`](ADR-0002-explicit-composition-no-runtime-service-locator.md) — concrete implementations разрешаются в Composition Root; потребители получают зависимости явно и не ищут их через глобальный runtime container/registry.
- [`ADR-0003 — Иерархическое логическое время и причинные commit boundaries`](ADR-0003-hierarchical-logical-time.md) — MINDRA различает внешнее и внутреннее логическое время, допускает несколько Cognitive Cycle на одно действие и отделяет causal order от wall-clock/physical concurrency.
- [`ADR-0004 — Версионированный committed CognitiveState вместо общего mutable bus`](ADR-0004-versioned-committed-cognitive-state.md) — canonical shared state представлен committed snapshots; изменения публикуются через owner-scoped staged updates и новую state revision, а hidden inplace mutation/`last-write-wins` запрещены.

## Proposed

Нет.

## Rejected

Нет самостоятельных ADR со статусом `rejected`.

Отклонённые альтернативы сохранены внутри соответствующих ADR.

## Superseded

Нет.
