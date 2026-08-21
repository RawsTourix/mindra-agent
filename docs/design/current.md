# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какая implementation-работа разрешена следующей.

Operational workflow не хранится в истории чата. Его canonical entry points:

- [`../process/README.md`](../process/README.md) — durable handoff, роли, modes и acceptance lifecycle;
- [`../process/independent-audit.md`](../process/independent-audit.md) — independent implementation/correction audit;
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md) — opening next step и authoring copy-ready Codex instructions.

---

# 1. Общий статус

```text
Semantic Freeze Baseline F31: accepted
Version Roadmap DU-32: accepted
Current milestone: v0.1 Core Kernel
v0.1 exact design: accepted
v0.1 implementation-sequence: accepted
V0.1-IS-01 … V0.1-IS-08: accepted
V0.1-IS-09 implementation: EXISTS
V0.1-IS-09 correction: EXISTS
V0.1-IS-09 independent code/design audit: PASS
V0.1-IS-09 verification/acceptance gate: OPEN
V0.1-IS-10+: CLOSED
```

Общий архитектурный цикл `DU-00 … DU-32` завершён и принят.

`V0.1-IS-09` **не должен реализовываться повторно**. Его implementation/correction уже находятся в истории `main`; текущая разрешённая работа — только восстановление/подтверждение required verification evidence и final acceptance audit.

`V0.1-IS-10` нельзя открывать до закрытия verification/acceptance gate `IS-09`.

---

# 2. Канонические входные точки

Semantic baseline:

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md)
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md)
- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md)

Operational workflow:

- [`../process/README.md`](../process/README.md);
- [`../process/independent-audit.md`](../process/independent-audit.md);
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md).

Version-specific source of truth:

- [`../versions/v0.1/README.md`](../versions/v0.1/README.md) — accepted exact design;
- [`../versions/v0.1/implementation-sequence.md`](../versions/v0.1/implementation-sequence.md) — accepted dependency-ordered implementation plan;
- [`../versions/v0.1/is-06-contract-shape.md`](../versions/v0.1/is-06-contract-shape.md) — accepted clarification `IS-06`;
- [`../versions/v0.1/is-07-execution-plan-shape.md`](../versions/v0.1/is-07-execution-plan-shape.md) — accepted clarification `IS-07`;
- [`../versions/v0.1/is-07-controlled-construction-correction.md`](../versions/v0.1/is-07-controlled-construction-correction.md) — accepted correction `IS-07`;
- [`../versions/v0.1/is-08-private-state-store-shape.md`](../versions/v0.1/is-08-private-state-store-shape.md) — accepted clarification `IS-08`;
- [`../versions/v0.1/is-09-commit-coordinator-shape.md`](../versions/v0.1/is-09-commit-coordinator-shape.md) — accepted exact clarification `IS-09`;
- [`../versions/v0.1/is-09-active-boundary-consistency-correction.md`](../versions/v0.1/is-09-active-boundary-consistency-correction.md) — accepted correction clarification `IS-09`;
- [`../versions/v0.1/is-10-evidence-plane-shape.md`](../versions/v0.1/is-10-evidence-plane-shape.md) — accepted clarification будущего `IS-10`, пока implementation step CLOSED;
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md) — canonical operational prompt template, revision `CSPT-02`.

---

# 3. Implementation checkpoints

| Step | Статус | Implementation/correction |
|---|---|---|
| `IS-01` | accepted | bootstrap + correction `584db766...` |
| `IS-02` | accepted | `e457ada1...` |
| `IS-03` | accepted | `a5c9f314...` |
| `IS-04` | accepted | `86d38ff6...` + `afc1937b...` |
| `IS-05` | accepted | `df602abb...` |
| `IS-06` | accepted | `633babaf...` |
| `IS-07` | accepted | `c8852930...` + `5b60d001...` |
| `IS-08` | accepted | `92a2dd75...` |
| `IS-09` | verification/acceptance pending | `c11d79e7...` + correction clarification `a4e99807...` + correction `978897ad...` |

## `V0.1-IS-08 — PrivateStateStore`

```text
92a2dd759b71359aff66d0da0c4a211df0cdc237
feat(runtime): add transactional private state store
```

ChatGPT audit подтвердил explicit stateful initialization, stateless `Unavailable`, private contract freeze, own-snapshot isolation, staged proposal preparation и internal all-or-nothing private batch apply. Targeted verification и local `FULL-C0`: `PASS`, полный suite — `198 passed`; post-push Ubuntu/Windows GitHub Actions подтверждены оператором проекта как успешные.

`V01-008` достиг уровня `substantial/partial`; полное atomic public+private closure принадлежит `IS-09`.

## `V0.1-IS-09 — Atomic CommitCoordinator`

Основная implementation:

```text
c11d79e78716d2273a602b94d1e78a4a3846c45b
feat(runtime): add atomic commit coordinator
```

После independent audit был обнаружен defect active composition boundary. Для него принят correction clarification:

```text
a4e99807669a4506105851edba99e88900beff8c
docs(v0.1): clarify IS-09 active boundary consistency
```

Correction implementation:

```text
978897ad57c9f0c84a05489c4568d6fd7832ceb6
fix(runtime): validate commit composition boundary
```

Independent review текущего repository state подтвердил:

- scope `IS-09` и forbidden scope `IS-10+`;
- atomic public/private commit pipeline;
- active descriptor/private-store composition consistency correction;
- fail-closed ownership/revision/provenance boundaries;
- отсутствие нового implementation/F31 blocker.

Code/design/correction audit: `PASS`.

Формальное acceptance `IS-09` пока **не зафиксировано**, потому что в доступном evidence не установлены targeted verification + полный `FULL-C0` именно после correction `978897ad...`, а post-push Actions этого SHA не подтверждены независимо.

До восстановления/подтверждения этого evidence `V01-002`, `V01-003`, `V01-006`, `V01-008` не маркируются закрытыми на final accepted `IS-09` gate.

---

# 4. Разрешённая текущая работа

Новый feature coding step сейчас **не открыт**.

Разрешённая работа:

```text
V0.1-IS-09 verification / final acceptance only
```

Нужно восстановить или повторно получить evidence минимум для:

1. targeted `IS-09` verification:
   - `FAST`;
   - `ARCH`;
   - tests текущего commit/correction layer, включая:
     - `tests/contract/test_commit_authority.py`;
     - `tests/contract/test_commit_active_composition.py`;
     - `tests/property/test_atomic_commit.py`;
     - `tests/property/test_stale_proposals.py`;
     - `tests/state_machine/test_commit_state_machine.py`;
2. полного current local regression gate `FULL-C0`;
3. post-push GitHub Actions Ubuntu/Windows для production state после correction либо equivalent accepted evidence.

Если local verification выполняется на более позднем HEAD, допустимо использовать его как regression evidence для `IS-09` только если между `978897ad...` и проверяемым HEAD отсутствуют production changes, способные изменить `IS-09` semantics. Это должно быть проверено по commit diff/history и явно указано в audit evidence.

После достаточного evidence ChatGPT выполняет final `MODE-AUDIT` verdict:

```text
AUDIT-PASS
→ IS-09 accepted
→ V01-002 / V01-003 / V01-006 / V01-008 close на предусмотренном commit layer
→ MODE-TRANSITION
→ только затем IS-10 OPEN
```

`V0.1-IS-10` и последующие шаги остаются CLOSED.

---

# 5. Следующий потенциальный step после acceptance IS-09

Следующий по accepted sequence:

```text
V0.1-IS-10 — O0 Evidence Plane
```

Для него уже принят exact clarification:

- [`../versions/v0.1/is-10-evidence-plane-shape.md`](../versions/v0.1/is-10-evidence-plane-shape.md).

Наличие clarification **не означает**, что `IS-10` открыт. До final acceptance `IS-09` Codex instruction на implementation `IS-10` не выдаётся.

---

# 6. Operational prompt

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

ChatGPT-side audit/authoring:

- [`../process/independent-audit.md`](../process/independent-audit.md);
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md).

Текущий этап находится не в `MODE-INSTRUCTION`, а в `MODE-AUDIT`/verification recovery для уже существующего `IS-09`.

Нельзя выдавать implementation prompt на `IS-09` повторно.

Нельзя выдавать implementation prompt на `IS-10` до final `AUDIT-PASS` `IS-09`.

---

# 7. Ограничения

- не переходить к `V0.1-IS-10` до final acceptance `IS-09`;
- не повторять implementation уже существующего `IS-09`;
- не начинать `v0.2` до полного acceptance gate `v0.1`;
- implementation-level correction допустима только внутри accepted `v0.1` semantics;
- semantic blocker требует design review и нового ADR/freeze update;
- Codex не меняет самостоятельно accepted version design/F31 и не открывает следующий implementation step;
- live current status не дублировать в `AGENTS.md`, `docs/README.md` или `docs/versions/README.md`.