# Документация MINDRA

## Назначение

Этот каталог — каноническая база знаний исследовательского проекта MINDRA.

Документация должна позволять человеку, ChatGPT, Codex или другому coding agent восстановить актуальный design context без необходимости опираться на историю отдельных чатов.

Краткий task prompt не заменяет документацию проекта.

---

# Быстрый порядок чтения

## Для общего понимания

1. [`project-concept.md`](project-concept.md)
2. [`architecture-concept.md`](architecture-concept.md)
3. [`research-methodology.md`](research-methodology.md)
4. [`design/README.md`](design/README.md)
5. [`design/current.md`](design/current.md)

## Перед design-работой

1. [`../AGENTS.md`](../AGENTS.md)
2. [`design/current.md`](design/current.md)
3. [`design/principles.md`](design/principles.md)
4. [`design/glossary.md`](design/glossary.md)
5. [`design/documentation-plan.md`](design/documentation-plan.md)
6. релевантные canonical design documents;
7. релевантные accepted/non-superseded ADR из `design/decisions/`.

## Перед будущей реализацией

После появления version design coding agent дополнительно обязан читать:

1. exact internal contracts;
2. target version specification;
3. target implementation sequence;
4. testing/evaluation requirements;
5. acceptance gates.

Эти документы ещё не спроектированы полностью и не должны угадываться заранее.

---

# Основные уровни документации

```text
Project concept
→ Architecture concept
→ Research methodology
→ Canonical design semantics
→ ADR
→ Exact internal contracts
→ Version design
→ Implementation sequence
→ Research evidence
```

Каждый уровень отвечает на свой тип вопросов.

### Concept

Объясняет направление проекта, его предметную границу и главные идеи без точной реализации.

### Canonical design

Фиксирует принятые архитектурные семантики, responsibilities, invariants и взаимодействие подсистем.

### ADR

Фиксирует значимый выбор между несколькими реалистичными вариантами и его trade-offs.

### Exact internal contracts

Фиксируют точную machine-facing форму уже принятой семантики: протоколы, поля, типы, lifecycle и другие интерфейсные детали.

### Version design

Определяет ограниченный scope конкретного этапа реализации и его acceptance prerequisites.

### Research evidence

Фиксирует фактические эксперименты и результаты. Research evidence не переписывает design напрямую: противоречащий результат инициирует design review.

---

# Иерархия решений

До появления более детальных документов действует общий порядок:

```text
accepted non-superseded ADR + canonical Design
→ exact internal contract
→ target version specification
→ implementation sequence
→ architecture concept
→ project concept
```

Более конкретный документ не должен молча отменять более фундаментальный invariant.

Если evidence требует изменить принятое решение:

```text
Research evidence
→ design review
→ ADR / canonical design update
→ contract/version consistency update
→ implementation
```

---

# Три разных вида истины

MINDRA строго различает:

```text
Design
Implementation
Research evidence
```

Документация не должна смешивать их.

Например:

- «Appraisal должен влиять на выбор действия» — design claim;
- «в текущем commit реализован `AppraisalModule`» — implementation claim;
- «ablation снизил метрику на 8 ± 2 п.п.» — empirical claim.

Ни один из этих тезисов сам по себе не доказывает наличие субъективного переживания.

---

# Язык

Документация и комментарии в коде пишутся на русском языке.

Технические идентификаторы и общепринятые machine-facing названия остаются на английском согласно [`../AGENTS.md`](../AGENTS.md).

---

# Текущий этап

На текущем этапе создаётся только documentation foundation.

Version roadmap, exact module contracts, конкретные алгоритмы и implementation stack будут проектироваться отдельно после формирования достаточного canonical design.

Фактический статус: [`design/current.md`](design/current.md).
