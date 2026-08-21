# Repository Status Reconciliation

## Статус

**Статус:** `accepted operational governance`  
**Назначение:** защита от stale `docs/design/current.md` и повторной реализации уже существующего implementation step

`docs/design/current.md` остаётся единственным каноническим документом live implementation status, но его содержимое должно соответствовать фактической remote repository history.

Это означает:

> `current.md` — source of truth после reconciliation, а не разрешение игнорировать противоречащую ему commit history.

---

# 1. Когда reconciliation обязательна

Проверка обязательна минимум:

- в новом чате / после потери контекста;
- перед `MODE-INSTRUCTION`;
- перед `MODE-TRANSITION`;
- когда пользователь говорит, что implementation/correction уже была сделана;
- когда remote HEAD содержит commits, не отражённые в `current.md`;
- когда version-specific clarification существует в history, но отсутствует среди canonical entry points `current.md`;
- когда status-файл предлагает реализовать step, production code которого уже существует.

---

# 2. Минимальная reconciliation procedure

Перед выдачей нового coding prompt ChatGPT обязан:

1. получить фактический remote HEAD/default branch;
2. прочитать `docs/design/current.md`;
3. определить последний accepted implementation baseline из `current.md`;
4. просмотреть commits/compare от baseline до remote HEAD;
5. проверить, существуют ли implementation/correction commits текущего или следующего `IS`;
6. проверить наличие step-specific clarification/correction docs в history;
7. классифицировать расхождение.

---

# 3. Классы расхождения

## `STATUS-CONSISTENT`

`current.md` соответствует remote history.

Можно продолжать normal operational mode.

## `STATUS-STALE-IMPLEMENTATION-EXISTS`

`current.md` говорит, что step только открыт для coding, но remote history уже содержит его implementation.

Действие:

```text
НЕ выдавать повторный implementation prompt
→ восстановить actual implementation/correction history
→ перейти в MODE-AUDIT / verification recovery
→ обновить current.md до фактического gate
```

## `STATUS-STALE-CORRECTION-EXISTS`

`current.md` не отражает уже выполненную correction.

Действие:

```text
НЕ повторять correction
→ independently audit correction
→ восстановить verification evidence
→ обновить current.md
```

## `STATUS-AHEAD-OF-EVIDENCE`

`current.md` маркирует step accepted/open next step, но required acceptance evidence отсутствует или история не подтверждает переход.

Действие:

```text
остановить next-step coding
→ вернуть status к последнему доказанному gate
→ восстановить evidence / audit
```

## `HISTORY-CONFLICT`

Commit graph/branch state неоднозначен или содержит competing histories.

Действие:

```text
STOP
→ blocker/status investigation
```

Не выбирать branch/baseline по предположению.

---

# 4. Приоритет при расхождении

При обнаружении противоречия нельзя слепо выполнять ни один из источников.

Используется evidence-driven reconciliation:

```text
remote commit ancestry + actual files
        ↓
accepted design/version docs
        ↓
implementation/correction evidence
        ↓
verification/audit evidence
        ↓
исправленный docs/design/current.md
```

Commit history не имеет права переопределить F31/design semantics, но имеет право доказать, что status-файл **устарел относительно уже существующей реализации**.

---

# 5. Live-status ownership после reconciliation

После выяснения фактического состояния обновляется `docs/design/current.md`.

В нём нужно различать минимум:

```text
implementation not started
implementation exists / audit pending
correction required
correction exists / audit pending
code/design PASS / verification pending
accepted
next step OPEN
```

Нельзя сводить всё к одному слову `OPEN`, если coding уже завершён и открыт только evidence/acceptance gate.

---

# 6. Verification recovery

Если implementation/correction существуют, но historical verification report недоступен:

- не повторять feature implementation;
- восстановить evidence отдельным verification-only task или независимым local run;
- targeted tests должны соответствовать фактическому step/correction;
- полный version regression gate повторяется;
- remote CI проверяется/подтверждается отдельно;
- более поздний HEAD можно использовать как regression evidence только после проверки, что после production correction не было semantic production changes relevant текущему step.

---

# 7. Связь с operational modes

```text
reconciliation
├── status consistent + coding not started
│   → MODE-INSTRUCTION
├── implementation exists
│   → MODE-AUDIT
├── correction exists
│   → MODE-AUDIT correction
├── verification missing
│   → verification recovery внутри MODE-AUDIT
└── semantic/history conflict
    → MODE-DESIGN / blocker investigation
```

---

# 8. Главное запрещённое поведение

Нельзя:

```text
current.md says OPEN
→ значит обязательно написать implementation prompt
```

без проверки remote history.

Нельзя также автоматически считать commit existence acceptance evidence.

Правильная схема:

```text
history показывает, что код существует
→ не повторяем coding
→ проверяем code/design
→ восстанавливаем verification evidence
→ только после acceptance открываем следующий IS
```
