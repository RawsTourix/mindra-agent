# Architecture Decision Records MINDRA

## Назначение

Этот каталог предназначен для значимых архитектурных решений MINDRA.

ADR создаётся, когда существует несколько реалистичных вариантов, а выбор влияет на:

- module boundaries;
- internal contracts;
- state ownership;
- training semantics;
- reproducibility;
- evaluation validity;
- runtime topology;
- future version design.

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

На стадии documentation foundation accepted ADR отсутствуют.

Первые ADR появятся только после фактического анализа альтернатив в следующих design topics.
