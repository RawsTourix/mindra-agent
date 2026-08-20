# Codex Instruction Authoring & Step Transition

## Статус

**Статус:** `accepted operational governance`  
**Режимы:** `MODE-DESIGN`, `MODE-INSTRUCTION`, `MODE-TRANSITION`  
**Назначение:** правила открытия следующего implementation step и подготовки готовой инструкции Codex

Этот документ определяет ChatGPT-side workflow перед каждым новым Codex task.

Canonical content template самого задания Codex:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md).

Этот документ не заменяет `CSPT`: он определяет, **когда**, **на основании каких источников** и **в каком пользовательском формате** ChatGPT должен собрать конкретный prompt.

---

# 1. Когда разрешён MODE-INSTRUCTION

ChatGPT может писать instruction для нового implementation step только если:

1. предыдущий step accepted;
2. все blocking corrections предыдущего step accepted;
3. required verification/CI gate предыдущего step закрыт;
4. `docs/design/current.md` явно помечает новый `Vx.y-IS-XX` как `OPEN`;
5. prerequisites нового step выполнены;
6. accepted documentation достаточно однозначна для implementation;
7. применимость текущей revision `CSPT` проверена.

Если новый step ещё CLOSED, инструкция на coding не выдаётся.

---

# 2. MODE-TRANSITION: как открыть следующий step

После `AUDIT-PASS` текущего шага ChatGPT выполняет transition отдельно от coding.

Порядок:

```text
current step audit PASS
↓
подтвердить verification/CI gate
↓
зафиксировать current step = accepted
↓
прочитать следующий section implementation-sequence
↓
проверить prerequisites
↓
проверить exact implementation ambiguity
↓
при необходимости MODE-DESIGN clarification
↓
проверить CSPT revision/applicability
↓
обновить docs/design/current.md
↓
next step = OPEN
↓
только затем MODE-INSTRUCTION
```

Нельзя сначала написать coding prompt, а потом задним числом открыть step.

---

# 3. MODE-DESIGN перед implementation step

Перед каждым новым `IS` ChatGPT должен спросить не пользователя, а repository documentation:

> достаточно ли существующих accepted документов, чтобы Codex реализовал шаг без самостоятельного архитектурного выбора?

Нужно проверить минимум:

- exact public/internal API shape;
- identity/revision types;
- initialization semantics;
- ownership;
- fail-closed errors;
- transaction/preparation/apply boundary;
- deterministic/canonical ordering;
- controlled construction;
- fingerprint/serialization semantics, если актуально;
- relation текущего step к предыдущему и следующему;
- что именно намеренно deferred.

Если ответ «нет», ChatGPT **сначала** создаёт step-specific clarification.

Clarification должен быть:

- version-level;
- accepted;
- внутри F31/canonical semantics;
- достаточно точным для Codex;
- указан в `docs/design/current.md` как обязательный source текущего step.

Только после этого разрешён `MODE-INSTRUCTION`.

---

# 4. Обязательный контекст при написании инструкции

Перед созданием prompt ChatGPT должен прочитать актуальные версии минимум:

1. `AGENTS.md`;
2. [`README.md`](README.md);
3. `docs/design/current.md`;
4. `docs/design/contract-adr-consistency-freeze.md`;
5. `docs/design/contracts/semantic-freeze-manifest.md`;
6. `docs/design/version-roadmap.md`;
7. [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md);
8. current version `README.md`;
9. current version `implementation-sequence.md`, section текущего step;
10. все accepted step-specific clarifications/corrections;
11. canonical design/ADR/contracts, перечисленные для текущего step;
12. фактическую реализацию prerequisites, если exact API нового step от неё зависит.

Нельзя строить новый prompt по памяти из старого чата.

---

# 5. Canonical template rule

Каждый implementation prompt обязан соответствовать **актуальной revision**:

```text
docs/versions/codex-step-prompt-template.md
```

Step-specific instruction **расширяет**, но не ослабляет CSPT.

В конкретный prompt добавляются:

- exact step title/id;
- дополнительные обязательные документы;
- exact accepted shapes;
- step-specific invariants;
- forbidden scope;
- required tests;
- VerificationObligations;
- targeted verification commands;
- дополнительные regression/negative scenarios.

Нельзя удалять из CSPT:

- prerequisite check;
- blocker behavior;
- one-step-only rule;
- prohibition on silent architecture choices;
- targeted + full regression verification;
- truthful CI statuses;
- structured final report;
- Conventional Commit suggestion;
- prohibition on automatic next-step opening;
- default prohibition on commit/push.

---

# 6. Проверка актуальности CSPT

Перед **каждым** новым implementation step ChatGPT явно проверяет, остаётся ли текущая CSPT revision применимой.

CSPT нужно обновить, если изменились обязательные:

- prompt sections;
- verification semantics;
- CI semantics;
- reporting fields;
- commit/push policy;
- mandatory source-of-truth paths внутри самого Codex prompt;
- новые классы evidence, которые Codex обязан вернуть.

CSPT не нужно bump'ать только потому, что:

- появился step-specific clarification;
- меняется exact API конкретного `IS`;
- меняется ChatGPT-side UI presentation готовой инструкции;
- текущая revision по-прежнему полностью покрывает operational contract Codex.

Если CSPT меняется, новая revision должна быть отражена в repository documentation до выдачи следующего prompt.

---

# 7. Требования к содержанию конкретной инструкции

Готовый prompt должен быть максимально самодостаточным, но не переписывать всю документацию проекта.

Он обязан содержать:

## 7.1. Scope header

```text
Реализуй только этап Vx.y-IS-XX — <title> ...
```

## 7.2. Mandatory reading

Точный список обязательных документов, включая step-specific clarification.

## 7.3. Preflight

Codex проверяет:

- HEAD/status;
- `current.md`;
- prerequisites;
- scope;
- forbidden scope;
- acceptance criteria;
- VerificationObligations.

## 7.4. Blocker rule

Если accepted documentation не определяет требуемое архитектурное решение:

```text
STOP
→ blocker report
```

а не самостоятельная импровизация Codex.

## 7.5. Exact implementation requirements

Перечислить critical invariants/shape текущего step настолько подробно, насколько нужно для отсутствия архитектурной свободы.

## 7.6. Forbidden scope

Явно перечислить соседние механизмы, которые нельзя реализовывать заранее.

## 7.7. Tests

Указать minimum required test files/scenarios и negative/regression cases.

## 7.8. Verification

Сначала targeted checks, затем полный текущий regression profile.

Для `v0.1` после `IS-01` это включает `FULL-C0`.

## 7.9. CI evidence

Потребовать честный status:

```text
PASS / FAIL / RUNNING / PENDING / NOT AVAILABLE
```

## 7.10. Final report

Потребовать:

- implemented scope;
- changed files;
- deviations;
- VerificationObligations status;
- verification evidence table;
- blockers/risks;
- implementation-complete verdict со стороны Codex;
- **одно предлагаемое название коммита в стиле Conventional Commits**.

## 7.11. Commit/push rule

По умолчанию:

```text
Самостоятельно commit/push не выполняй.
```

Если конкретный workflow когда-либо изменит это правило, изменение должно быть accepted operational documentation update.

---

# 8. Формат выдачи инструкции пользователю

Это обязательное ChatGPT-side presentation rule.

Когда ChatGPT завершил `MODE-INSTRUCTION`, **готовый prompt для Codex должен быть выдан как один отдельный копируемый writing block / документный блок ChatGPT**, а не как обычный текст, размазанный внутри ответа.

Цель:

- пользователь может одним действием скопировать весь prompt;
- внутри блока нет audit commentary;
- инструкция не смешивается с пояснениями ChatGPT;
- границы prompt однозначны.

Допускается короткое пояснение **перед** блоком, например:

```text
IS-09 открыт, CSPT-02 применим. Отправляй Codex:
```

После этого — один complete prompt block.

Внутри writing block:

- только текст, который должен получить Codex;
- никаких file citations ChatGPT;
- никаких пояснений пользователю;
- никаких альтернативных вариантов prompt;
- никаких незаполненных placeholders.

Если текущий интерфейс ChatGPT технически не поддерживает writing block, fallback — один fenced text/code block, полностью готовый к копированию.

Обычный prose paragraph вместо copy-ready блока использовать нельзя, если задача — подготовить финальную инструкцию Codex.

---

# 9. Correction instruction format

Готовая correction-инструкция из `MODE-CORRECTION` подчиняется тому же presentation rule:

- один copy-ready writing block;
- exact defect;
- violated invariant;
- minimal correction scope;
- regression tests;
- targeted + full regression verification;
- CI status semantics;
- proposed commit name;
- запрет следующего `IS`;
- default no commit/push.

Correction prompt не должен повторно просить реализовать весь исходный step, если defect локален.

---

# 10. Что делать после отправки инструкции

После выдачи prompt ChatGPT **не считает step реализованным**.

Ожидаемый следующий вход:

```text
Codex report
+
«код запушен»
```

После этого ChatGPT входит в [`MODE-AUDIT`](independent-audit.md).

Нельзя по следующему сообщению автоматически писать prompt следующего step без independent audit текущего.

---

# 11. Обновление status documentation

При принятии/открытии step:

- `docs/design/current.md` содержит live status;
- index/README документы не должны копировать номер current `IS`;
- version-level accepted clarifications добавляются в список canonical входных точек current status;
- closed/open distinction должен быть однозначным.

Если `docs/README.md` или `docs/versions/README.md` содержат stale live status, его нужно удалить и заменить ссылкой на `current.md`, а не синхронизировать вручную после каждого step.

---

# 12. Формат MODE-TRANSITION ответа

После acceptance предыдущего шага хороший transition ответ имеет структуру:

1. коротко: `<previous IS> accepted`;
2. `<next IS> OPEN`;
3. указать, был ли нужен clarification;
4. указать текущую CSPT revision и результат applicability check;
5. дать готовую Codex instruction **в writing block**.

Не нужно повторять весь audit предыдущего шага ещё раз.

---

# 13. Запрещённые формы инструкции

Нельзя выдавать Codex только:

```text
реализуй IS-09 по документации
```

Нельзя:

- ссылаться на старый prompt из истории чата как canonical;
- оставлять архитектурные вопросы в формулировке «сделай как считаешь лучше»;
- объединять несколько `IS`;
- разрешать «заодно» refactor следующего слоя;
- пропускать full regression gate;
- просить Codex самостоятельно открыть следующий step;
- смешивать prompt и audit commentary в одном блоке;
- отдавать финальный prompt простым prose, если доступен copy-ready writing block.

---

# 14. Exit condition MODE-INSTRUCTION

`MODE-INSTRUCTION` завершён, когда пользователь получил **одну полностью готовую к отправке Codex инструкцию**, которая:

- соответствует current OPEN step;
- соответствует CSPT;
- учитывает все step-specific accepted clarifications;
- содержит verification + reporting requirements;
- не требует от Codex самостоятельного design choice;
- предоставлена в copy-ready writing block;
- не открывает следующий step автоматически.