# Проектирование версий MINDRA

## Назначение

Этот каталог является историческим design-era navigation surface. После принятия `DU-32` canonical software roadmap и version-specific implementation design живут в:

- [`../version-roadmap.md`](../version-roadmap.md);
- [`../../versions/README.md`](../../versions/README.md);
- `docs/versions/vX.Y/`.

Фактический live implementation status хранится только в [`../current.md`](../current.md).

---

# Главный принцип

Нельзя использовать версии для преждевременного разбиения ещё не определённой архитектуры.

Принятый порядок:

```text
канонический design
→ зависимости
→ требования к evaluation
→ roadmap
→ спецификации версий
→ последовательности реализации
```

---

# Что содержит директория версии

Основной профиль:

```text
versions/vX.Y/
├── README.md
└── implementation-sequence.md
```

Version-specific каталог может дополнительно содержать verification matrix и accepted clarification/correction documents, если они нужны operational workflow.

`README.md` определяет:

- цель версии;
- prerequisites;
- scope;
- non-goals;
- ссылки на канонический design;
- необходимые исследовательские и инженерные возможности;
- критерии приёмки;
- известные ограничения.

`implementation-sequence.md` задаёт patch-oriented порядок работ для Codex.

---

# Правила последовательности реализации

Каждый patch должен содержать:

- цель;
- prerequisites;
- канонические документы;
- точный scope;
- запрещённый scope;
- требования к реализации;
- обязательные тесты;
- обязательную evaluation, если применимо;
- критерии приёмки;
- обновления документации.

Поздняя версия не разрешает перепрыгнуть приёмку предыдущих зависимых этапов.

---

# Исследовательские и программные версии

MINDRA различает software milestone, архитектурный/исследовательский этап, experiment protocol и checkpoint/artifact version. Они не объединяются автоматически без соответствующего accepted design.

---

# Состояние

```text
DU-32 software roadmap: accepted
v0.1 Core Kernel: implemented / independently audited / accepted
```

Текущее состояние последующих versions и единственный разрешённый implementation step определяет только [`../current.md`](../current.md).
