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
V0.1-IS-01 … V0.1-IS-09: accepted
V0.1-IS-10: OPEN
V0.1-IS-11+: CLOSED
```

Общий архитектурный цикл `DU-00 … DU-32` завершён и принят.

`V0.1-IS-09 — Atomic CommitCoordinator` принят после independent code/design/correction audit и восстановления required verification evidence. Targeted verification и полный `FULL-C0` прошли на post-correction regression HEAD `8b39497d7486bb7e69146249193ef38fb8246c2c`; GitHub Actions run `32516404539` для exact SHA завершился успешно на Ubuntu и Windows / Python 3.14.

Текущая разрешённая implementation-работа:

```text
V0.1-IS-10 — O0 Evidence Plane
```

Следующие implementation steps остаются закрыты до отдельного audit/transition.

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
- [`../versions/v0.1/is-10-evidence-plane-shape.md`](../versions/v0.1/is-10-evidence-plane-shape.md) — accepted exact clarification текущего `IS-10`;
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
| `IS-09` | accepted | `c11d79e7...` + correction clarification `a4e99807...` + correction `978897ad...` |
| `IS-10` | OPEN | implementation not started |

## `V0.1-IS-08 — PrivateStateStore`

```text
92a2dd759b71359aff66d0da0c4a211df0cdc237
feat(runtime): add transactional private state store
```

ChatGPT audit подтвердил explicit stateful initialization, stateless `Unavailable`, private contract freeze, own-snapshot isolation, staged proposal preparation и internal all-or-nothing private batch apply. Targeted verification и local `FULL-C0`: `PASS`, полный suite — `198 passed`; post-push Ubuntu/Windows GitHub Actions подтверждены оператором проекта как успешные.

`V01-008` достиг уровня `substantial/partial`; полное atomic public+private closure было завершено в `IS-09`.

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

Final independent acceptance audit подтвердил:

- scope `IS-09` и отсутствие leakage в `IS-10+`;
- atomic public/private commit pipeline;
- active descriptor/private-store composition consistency correction;
- fail-closed ownership/revision/provenance boundaries;
- отсутствие нового implementation/F31 blocker;
- post-correction reconciliation: от `978897ad...` до verification HEAD production code, tests, toolchain и CI workflow не менялись;
- targeted verification: `PASS`, `32 passed`;
- полный local `FULL-C0`: `PASS`, полный suite `230 passed`;
- build: `PASS`;
- GitHub Actions run `32516404539`, exact head `8b39497d7486bb7e69146249193ef38fb8246c2c`, event `push`: `PASS`;
- Ubuntu `FULL-C0 (ubuntu-latest, Python 3.14)`: `PASS`;
- Windows `FULL-C0 (windows-latest, Python 3.14)`: `PASS`.

Verdict:

```text
AUDIT-PASS
V0.1-IS-09: accepted
```

VerificationObligations на предусмотренном `IS-09` commit layer:

- `V01-002` — closed at commit layer;
- `V01-003` — closed;
- `V01-006` — closed;
- `V01-008` — closed at commit layer.

`V01-001 same-base wave` остаётся работой последующего Scheduler/WaveExecutor step согласно accepted sequence.

---

# 4. Разрешённая текущая работа

Открыт ровно один feature coding step:

```text
V0.1-IS-10 — O0 Evidence Plane
```

Prerequisites `IS-01 … IS-09` приняты.

Для `IS-10` уже принят exact implementation clarification:

- [`../versions/v0.1/is-10-evidence-plane-shape.md`](../versions/v0.1/is-10-evidence-plane-shape.md).

Clarification фиксирует passive typed structural Evidence Plane foundation: immutable evidence contracts + append-only process-local recorder, без producer integration в planner/commit/scheduler/composition/intervention boundaries на этом шаге.

Перед implementation обязательны section `V0.1-IS-10` в `implementation-sequence.md`, exact clarification и перечисленные там canonical design/ADR.

Targeted verification для `IS-10`: `FAST + ARCH` и минимум:

```text
tests/unit/test_evidence_records.py
tests/contract/test_evidence_isolation.py
```

После targeted green обязателен `FULL-C0`.

`V0.1-IS-11` и последующие steps остаются CLOSED.

---

# 5. Следующий потенциальный step после acceptance IS-10

Следующий по accepted sequence:

```text
V0.1-IS-11 — WaveExecutor & Scheduler
```

Он остаётся CLOSED до implementation, verification и independent ChatGPT audit `IS-10`.

Наличие дальнейшей version documentation не является разрешением реализовывать `IS-11` заранее.

---

# 6. Operational prompt

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

ChatGPT-side audit/authoring:

- [`../process/independent-audit.md`](../process/independent-audit.md);
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md).

`CSPT-02` проверен при открытии `IS-10` и остаётся применимым: обязательные verification semantics, CI evidence semantics, reporting и commit/push policy не изменились.

Текущий operational mode после transition допускает `MODE-INSTRUCTION` только для:

```text
V0.1-IS-10 — O0 Evidence Plane
```

Codex не открывает следующий implementation step самостоятельно.

---

# 7. Ограничения

- не переходить к `V0.1-IS-11` до independent acceptance `IS-10`;
- не повторять implementation уже принятого `IS-09`;
- не начинать `v0.2` до полного acceptance gate `v0.1`;
- implementation-level correction допустима только внутри accepted `v0.1` semantics;
- semantic blocker требует design review и нового ADR/freeze update;
- Codex не меняет самостоятельно accepted version design/F31 и не открывает следующий implementation step;
- live current status не дублировать в `AGENTS.md`, `docs/README.md` или `docs/versions/README.md`.