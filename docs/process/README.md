# Workflow разработки MINDRA

## Статус

**Статус:** `accepted operational governance`  
**Назначение:** постоянный handoff и source of truth для совместной работы ChatGPT, Codex и оператора проекта  
**Область:** version design, implementation steps, independent audit, correction loop, verification и открытие следующего шага

Этот каталог фиксирует рабочий процесс MINDRA так, чтобы новый чат или новый agent мог восстановить его **без истории предыдущего разговора**.

Operational workflow не переопределяет `F31`, canonical design, ADR, semantic contracts, version design или implementation sequence. Он определяет, **как именно** accepted design превращается в код и как этот код принимается.

---

# 1. Канонические документы процесса

- [`independent-audit.md`](independent-audit.md) — независимый аудит implementation/correction после push;
- [`codex-instruction-authoring.md`](codex-instruction-authoring.md) — подготовка инструкции Codex и открытие следующего `IS`;
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md) — canonical content template для одного Codex implementation task;
- [`../design/current.md`](../design/current.md) — **единственный** source of truth для текущего открытого implementation step.

Если история чата расходится с этими документами, приоритет имеет repository documentation.

---

# 2. Роли

## 2.1. ChatGPT

ChatGPT выполняет роли:

- архитектор version-level design и step-specific clarification;
- независимый reviewer/auditor реализации Codex;
- gatekeeper между implementation steps;
- автор correction-инструкций;
- автор инструкции на следующий открытый `IS`;
- maintainer operational documentation, когда workflow меняется.

ChatGPT **не принимает отчёт Codex на веру**. Для acceptance нужен независимый просмотр remote diff/code/tests и сверка с accepted documentation.

ChatGPT не открывает следующий `IS`, пока не выполнены acceptance gates текущего шага.

## 2.2. Codex

Codex — implementation agent.

По умолчанию он:

- реализует только один явно разрешённый `Vx.y-IS-XX`;
- читает обязательный контекст до изменений;
- не выбирает новую архитектуру при пробеле документации;
- выполняет targeted verification и полный текущий regression gate;
- возвращает structured evidence report;
- предлагает Conventional Commit message;
- **не делает commit/push**, если конкретное задание явно этого не разрешило;
- не обновляет `docs/design/current.md` и не открывает следующий step.

## 2.3. Оператор проекта

Оператор проекта:

- запускает/контролирует Codex;
- после отчёта Codex создаёт commit/push, если это не делал другой разрешённый workflow;
- сообщает ChatGPT, что изменения находятся на remote;
- при необходимости подтверждает GitHub Actions status, если доступный ChatGPT connector не видит push-triggered run;
- принимает архитектурные/design решения, если ChatGPT обнаружил настоящий blocker.

Operator-confirmed CI допустим как evidence, но в документации/ответе он должен называться **operator-confirmed**, а не independently observed by ChatGPT.

---

# 3. Единственный live status

Текущий implementation step и его состояние определяются только:

```text
docs/design/current.md
```

`AGENTS.md`, `docs/README.md`, `docs/versions/README.md`, version README и process docs **не должны хранить копию текущего номера `IS`**.

Они могут описывать workflow, roadmap и accepted version design, но для ответа на вопрос:

> какой step сейчас открыт?

всегда читается `docs/design/current.md`.

Это правило предотвращает stale status после нескольких implementation iterations.

---

# 4. Source-of-truth chain

```text
accepted ADR + canonical design
        ↓
Semantic Freeze Baseline F31
        ↓
semantic contracts
        ↓
DU-32 Version Roadmap
        ↓
accepted version design
        ↓
accepted implementation-sequence
        ↓
step-specific accepted clarification/correction, если существует
        ↓
docs/design/current.md
        ↓
current OPEN implementation step
        ↓
canonical Codex prompt template
        ↓
Codex implementation + verification report
        ↓
operator commit/push
        ↓
independent ChatGPT audit
        ↓
correction loop ИЛИ acceptance
        ↓
open next step
```

Operational document более низкого уровня не имеет права молча переопределить semantic документ более высокого уровня.

---

# 5. Режимы работы

Работа ведётся в явном режиме. Один ответ/проход может последовательно перейти между режимами только там, где выполнены exit conditions предыдущего.

| Режим | Когда используется | Результат |
|---|---|---|
| `MODE-DESIGN` | перед новой version или когда текущий step имеет implementation ambiguity | accepted design/clarification либо blocker |
| `MODE-INSTRUCTION` | текущий `IS` уже OPEN и достаточно определён | готовая инструкция Codex по canonical template |
| `MODE-AUDIT` | implementation/correction уже запушена | независимый audit verdict |
| `MODE-CORRECTION` | audit нашёл defect в пределах accepted semantics | минимальная correction-инструкция; следующий `IS` остаётся CLOSED |
| `MODE-TRANSITION` | текущий step прошёл audit + verification gates | текущий step accepted, следующий OPEN, затем переход в `MODE-INSTRUCTION` |

Подробные правила `MODE-AUDIT` и `MODE-CORRECTION` находятся в [`independent-audit.md`](independent-audit.md).

Подробные правила `MODE-INSTRUCTION`, `MODE-DESIGN` перед step и `MODE-TRANSITION` находятся в [`codex-instruction-authoring.md`](codex-instruction-authoring.md).

---

# 6. Основной lifecycle одного implementation step

```text
previous step ACCEPTED
        ↓
MODE-TRANSITION
        ↓
проверка prerequisites следующего step
        ↓
проверка ambiguity / exact shape
        ↓
при необходимости MODE-DESIGN clarification patch
        ↓
current.md: next step OPEN
        ↓
проверка актуальности CSPT
        ↓
MODE-INSTRUCTION
        ↓
готовый copy-ready Codex prompt
        ↓
Codex implementation
        ↓
targeted verification
        ↓
full local regression gate
        ↓
Codex report + proposed commit message
        ↓
operator commit/push
        ↓
MODE-AUDIT
        ↓
        ├── defect → MODE-CORRECTION → Codex → push → MODE-AUDIT
        │
        ├── architectural/semantic blocker → MODE-DESIGN / ADR review
        │
        └── PASS + evidence → MODE-TRANSITION
```

Нельзя сокращать цепочку до:

```text
Codex says PASS
→ next IS
```

Отчёт Codex является входом для независимого audit, а не acceptance decision.

---

# 7. Acceptance gate implementation step

Implementation step может получить `accepted` только если одновременно выполнены:

1. **Scope gate** — реализован только разрешённый step, forbidden scope не протёк;
2. **Design gate** — code/API/invariants соответствуют accepted design/clarifications;
3. **Independent audit gate** — ChatGPT просмотрел remote implementation, а не только отчёт Codex;
4. **Targeted verification gate** — обязательные проверки текущего step имеют evidence;
5. **Full regression gate** — текущий version-wide local regression profile прошёл;
6. **Remote CI gate** — declared remote jobs подтверждены, если они являются acceptance requirement;
7. **Correction gate** — все найденные blocking defects исправлены и повторно audited;
8. **Documentation gate** — `docs/design/current.md` отражает acceptance и только после этого открывает следующий step.

Для CI допускаются два вида подтверждения:

```text
independently observed by ChatGPT
operator-confirmed
```

Оба должны называться честно. `PENDING`, `RUNNING`, `NOT AVAILABLE` не являются `PASS`.

---

# 8. Correction loop

Если `MODE-AUDIT` находит defect внутри accepted semantics:

```text
current step остаётся OPEN / correction required
next step остаётся CLOSED
↓
ChatGPT формулирует минимальный correction scope
↓
Codex исправляет только defect
↓
повторяет targeted + full regression verification
↓
operator commit/push
↓
ChatGPT independently audits correction diff
```

Correction не должна превращаться в скрытый следующий feature step.

Если defect обнаруживает **пробел или противоречие accepted documentation**, сначала выполняется documentation clarification/design review. Нельзя заставлять Codex самостоятельно угадывать архитектуру.

---

# 9. Step-specific clarification

Перед выдачей инструкции следующего шага ChatGPT обязан проверить, достаточно ли existing version docs определяют exact implementation boundary.

Clarification нужен, если без него Codex должен самостоятельно выбирать, например:

- public API shape;
- representation version/revision token;
- controlled construction boundary;
- initialization semantics;
- fingerprint/canonicalization semantics;
- transaction/apply boundary;
- ownership/validation responsibility между соседними `IS`.

Clarification:

- остаётся внутри accepted F31/version semantics;
- не создаёт новый semantic invariant без design review;
- хранится рядом с version docs;
- добавляется в обязательный context текущего step;
- фиксируется в `docs/design/current.md` как accepted source для текущей работы.

---

# 10. Verification discipline

Canonical prompt template задаёт общие правила verification.

Для каждого step:

```text
targeted verification
→ full current local regression profile
→ remote CI evidence/status
→ Codex report
→ independent audit
```

Нельзя:

- ослабить test/type/import contract ради green;
- скрыть failure через `skip`, `xfail`, quarantine или broad ignore без accepted причины;
- считать конфигурацию CI доказательством успешного запуска CI;
- считать локальный `PASS` заменой обязательному remote CI;
- считать отчёт Codex независимым audit evidence.

---

# 11. Правила обновления operational governance

Operational workflow пересматривается, если меняются:

- роли ChatGPT/Codex/operator;
- acceptance gates;
- correction lifecycle;
- правило commit/push;
- CI evidence semantics;
- source-of-truth paths;
- canonical prompt authoring/delivery rules;
- порядок открытия следующего implementation step.

При изменении процесса:

1. обновить соответствующий документ `docs/process/`;
2. проверить `AGENTS.md`;
3. проверить применимость `docs/versions/codex-step-prompt-template.md`;
4. если меняется **содержимое обязательного Codex prompt**, обновить revision `CSPT`;
5. если меняется только ChatGPT-side workflow/delivery presentation, `CSPT` не нужно bump'ать формально;
6. не оставлять новое обязательное правило только в чате.

---

# 12. Recovery protocol после потери контекста чата

В новом чате не нужен отдельный вручную написанный handoff, если repository documentation актуальна.

Минимальный порядок восстановления:

1. `AGENTS.md`;
2. этот файл `docs/process/README.md`;
3. mode-specific документ:
   - audit → `docs/process/independent-audit.md`;
   - next-step/prompt → `docs/process/codex-instruction-authoring.md`;
4. `docs/design/current.md`;
5. `docs/design/contract-adr-consistency-freeze.md`;
6. `docs/design/contracts/semantic-freeze-manifest.md`;
7. `docs/design/version-roadmap.md`;
8. current version `README.md`;
9. current version `implementation-sequence.md`;
10. все accepted step-specific clarifications, перечисленные в `current.md`;
11. `docs/versions/codex-step-prompt-template.md` при подготовке Codex task;
12. remote commits/diff текущего implementation step при audit.

После этого новый ChatGPT instance должен уметь продолжить workflow без предположений из старого чата.

---

# 13. Запрещённые сокращения процесса

Нельзя:

```text
читать только Codex report вместо remote diff
```

```text
считать local PASS автоматически accepted
```

```text
открывать следующий IS до independent audit
```

```text
давать Codex общий prompt «реализуй всю версию»
```

```text
оставлять implementation ambiguity на усмотрение Codex
```

```text
хранить текущий номер IS в нескольких README
```

```text
делать correction и следующий IS одним task
```

```text
использовать старый prompt из истории чата вместо canonical CSPT
```

---

# 14. Критерий самодостаточности процесса

Workflow считается достаточно документированным, если новый ChatGPT/Codex session может по repository state однозначно определить:

- какая version сейчас реализуется;
- какой `IS` открыт;
- что уже accepted;
- какие source docs обязательны;
- что должен сделать Codex;
- какие проверки обязательны;
- кто делает commit/push;
- как проводится independent audit;
- что делать при defect;
- когда можно открыть следующий step;
- как оформить готовую инструкцию Codex.

Если для ответа на любой из этих вопросов требуется история чата, operational documentation считается неполной и должна быть обновлена.