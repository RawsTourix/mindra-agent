# Version design MINDRA

## Назначение

Этот каталог предназначен для будущих implementation-oriented версий MINDRA.

Version roadmap пока **не спроектирован**.

Версии появятся только после формирования достаточного canonical architecture design и dependency graph.

---

# Главный принцип

Нельзя использовать версии для преждевременного разбиения ещё не определённой архитектуры.

Правильный порядок:

```text
canonical design
→ dependencies
→ evaluation requirements
→ roadmap
→ version specifications
→ implementation sequences
```

---

# Что должна содержать будущая version directory

Conceptually:

```text
versions/vX.Y/
├── README.md
└── implementation-sequence.md
```

`README.md` должен определять:

- цель версии;
- prerequisites;
- scope;
- non-goals;
- canonical design references;
- required research/engineering capabilities;
- acceptance criteria;
- known limitations.

`implementation-sequence.md` должен задавать patch-oriented порядок работ для Codex.

---

# Правила implementation sequence

Каждый будущий patch должен содержать:

- цель;
- prerequisites;
- canonical docs;
- точный scope;
- forbidden scope;
- implementation requirements;
- required tests;
- required evaluation, если применимо;
- acceptance criteria;
- documentation updates.

Поздняя версия не разрешает перепрыгнуть acceptance предыдущих dependency milestones.

---

# Research versions и software versions

Нужно отдельно решить, как MINDRA будет соотносить:

- software version;
- architecture/research milestone;
- experiment protocol version;
- checkpoint format version.

До соответствующего design/ADR эти понятия не следует автоматически объединять.

---

# Состояние

```text
Version roadmap: not designed
Current version: none
Implementation: not started
```
