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
current implementation step: V0.1-IS-09 — OPEN
V0.1-IS-10+: CLOSED
```

Общий архитектурный цикл `DU-00 … DU-32` завершён и принят. Текущий разрешённый implementation step всегда определяется только этим файлом.

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
- [`../versions/v0.1/is-09-commit-coordinator-shape.md`](../versions/v0.1/is-09-commit-coordinator-shape.md) — accepted exact clarification текущего `IS-09`;
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md) — canonical operational prompt template, revision `CSPT-02`.

---

# 3. Принятые implementation checkpoints

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

## `V0.1-IS-08 — PrivateStateStore`

```text
92a2dd759b71359aff66d0da0c4a211df0cdc237
feat(runtime): add transactional private state store
```

ChatGPT audit подтвердил explicit stateful initialization, stateless `Unavailable`, private contract freeze, own-snapshot isolation, staged proposal preparation и internal all-or-nothing private batch apply. Targeted verification и local `FULL-C0`: `PASS`, полный suite — `198 passed`; post-push Ubuntu/Windows GitHub Actions подтверждены оператором проекта как успешные.

`V01-008` достиг уровня `substantial/partial`; полное atomic public+private closure выполняется в `IS-09`.

---

# 4. Разрешённая implementation работа

Единственный разрешённый следующий coding step:

```text
V0.1-IS-09 — Atomic CommitCoordinator
```

Scope определяется accepted `implementation-sequence.md`, `is-06-contract-shape.md`, `is-08-private-state-store-shape.md` и exact clarification [`../versions/v0.1/is-09-commit-coordinator-shape.md`](../versions/v0.1/is-09-commit-coordinator-shape.md).

Ключевой результат:

```text
CommitCoordinator
PrivateStateRevisionTransition
CommitRecord
CommitResult
public StateUpdateProposal validation
private proposal preparation
atomic public/private transaction boundary
CommitId assignment
```

Exact clarification фиксирует:

- public `CognitiveState` остаётся immutable и передаётся в commit как current base snapshot;
- все public/private validations и новый public snapshot строятся до private mutation;
- module result/provenance/attempt consistency проверяется fail closed;
- accepted public write создаёт следующую `StateRevision`;
- private-only/no-op successful commit не увеличивает public revision, но получает отдельный `CommitId`;
- никакой partial-success subset, retry или silent rebase не допускаются;
- `V01-002`, `V01-003`, `V01-006`, `V01-008` должны закрыться на commit layer.

`V0.1-IS-10` и последующие шаги закрыты до implementation + verification + отдельного ChatGPT audit `IS-09`.

---

# 5. Operational prompt

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

ChatGPT-side authoring/delivery:

- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md).

Перед открытием `IS-09` применимость `CSPT-02` проверена после добавления step-specific clarification. Новых CI jobs, verification profiles, mandatory commands или reporting semantics не появилось, поэтому revision шаблона не изменяется.

`CSPT-02` требует targeted verification, полный local `FULL-C0`, truthful GitHub Actions status/evidence и предложение Conventional Commit message в конце отчёта.

Финальная инструкция Codex в интерактивной работе ChatGPT должна выдаваться как один copy-ready writing/document block по process rules.

---

# 6. Ограничения

- не переходить к `V0.1-IS-10` до final acceptance `IS-09`;
- не начинать `v0.2` до полного acceptance gate `v0.1`;
- implementation-level correction допустима только внутри accepted `v0.1` semantics;
- semantic blocker требует design review и нового ADR/freeze update;
- Codex не меняет самостоятельно accepted version design/F31 и не открывает следующий implementation step;
- live current step не дублировать в `AGENTS.md`, `docs/README.md` или `docs/versions/README.md`.