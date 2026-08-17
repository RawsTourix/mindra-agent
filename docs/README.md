# Документация MINDRA

## Назначение

Этот каталог — каноническая база знаний исследовательского проекта MINDRA.

Документация должна позволять человеку, ChatGPT, Codex или другому агенту разработки восстановить актуальный архитектурный контекст без необходимости опираться на историю отдельных чатов.

Краткое задание не заменяет документацию проекта.

---

# Быстрый порядок чтения

## Для общего понимания

1. [`project-concept.md`](project-concept.md)
2. [`architecture-concept.md`](architecture-concept.md)
3. [`research-methodology.md`](research-methodology.md)
4. [`design/README.md`](design/README.md)
5. [`design/current.md`](design/current.md)

## Перед архитектурной работой

1. [`../AGENTS.md`](../AGENTS.md)
2. [`design/current.md`](design/current.md)
3. [`design/principles.md`](design/principles.md)
4. [`design/glossary.md`](design/glossary.md)
5. [`design/documentation-plan.md`](design/documentation-plan.md)
6. релевантные canonical design owners;
7. релевантные accepted/non-superseded ADR;
8. релевантные candidate contracts;
9. датированный research pass, если DU опирался на внешний landscape.

## Перед будущей реализацией

После появления проектирования версий coding agent дополнительно обязан читать:

1. точные внутренние контракты;
2. спецификацию целевой версии;
3. последовательность реализации;
4. требования к тестированию/оценке;
5. критерии приёмки.

Эти документы ещё не спроектированы полностью и не должны угадываться заранее.

---

# Основные уровни документации

```text
Концепция проекта
→ Архитектурная концепция
→ Исследовательская методология
→ Каноническая архитектурная семантика
→ ADR
→ Candidate / exact internal contracts
→ Проектирование версии
→ Последовательность реализации
→ Исследовательские результаты
```

Research evidence не переписывает design напрямую: противоречащий результат инициирует design review.

---

# Три разных вида истины

MINDRA строго различает:

```text
Design
Реализация
Исследовательские результаты
```

Например:

- «Valuation использует typed `ValueProfile`» — архитектурное утверждение `DU-18`;
- «в commit реализован `ValuationModule`» — утверждение о реализации;
- «structured valuation лучше weighted scalar baseline на N» — эмпирический результат.

Ни один из этих тезисов сам по себе не доказывает наличие субъективного переживания.

---

# Язык

Документация и комментарии в коде пишутся на русском языке.

На английском остаются технические идентификаторы, имена типов, классов, функций, библиотек, API и термины, перевод которых ухудшает точность. Подробное правило: [`../AGENTS.md`](../AGENTS.md).

---

# Исследовательский журнал

Датированные literature/research pass хранятся в [`research/`](research/).

Будущие hypothesis/experiment/result records будут добавляться туда отдельно от canonical design.

---

# Текущий этап

Проект находится на стадии **последовательного канонического архитектурного проектирования**.

Documentation foundation и `DU-01 … DU-18` уже приняты. Следующий допустимый этап определяется только [`design/current.md`](design/current.md); порядок задаётся [`design/documentation-plan.md`](design/documentation-plan.md).

Production/research implementation, exact contract freeze, version roadmap и `implementation-sequence.md` ещё не начаты.
