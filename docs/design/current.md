# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какая implementation-работа разрешена следующей.

---

# 1. Общий статус

```text
Semantic Freeze Baseline F31: accepted
Version Roadmap DU-32: accepted
Current milestone: v0.1 Core Kernel
v0.1 exact design: accepted
v0.1 implementation-sequence: accepted
V0.1-IS-01 … V0.1-IS-07: accepted
current implementation step: V0.1-IS-08 — OPEN
V0.1-IS-09+: CLOSED
```

Общий архитектурный цикл `DU-00 … DU-32` завершён и принят. Приняты 32 ADR и semantic contracts `DU-07 … DU-30`, frozen по смыслу как baseline `F31`.

Текущий разрешённый implementation step всегда определяется только этим файлом.

---

# 2. Канонические входные точки

Semantic baseline:

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md)
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md)
- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md)

Roadmap:

- [`version-roadmap.md`](version-roadmap.md)
- [`ADR-0032`](decisions/ADR-0032-vertical-capability-version-roadmap.md)
- [`../versions/README.md`](../versions/README.md)

Version-specific source of truth:

- [`../versions/v0.1/README.md`](../versions/v0.1/README.md) — accepted exact design;
- [`../versions/v0.1/implementation-sequence.md`](../versions/v0.1/implementation-sequence.md) — accepted dependency-ordered implementation plan;
- [`../versions/v0.1/is-06-contract-shape.md`](../versions/v0.1/is-06-contract-shape.md) — accepted exact clarification `IS-06`;
- [`../versions/v0.1/is-07-execution-plan-shape.md`](../versions/v0.1/is-07-execution-plan-shape.md) — accepted exact clarification `IS-07`;
- [`../versions/v0.1/is-07-controlled-construction-correction.md`](../versions/v0.1/is-07-controlled-construction-correction.md) — accepted correction clarification `IS-07`;
- [`../versions/v0.1/is-08-private-state-store-shape.md`](../versions/v0.1/is-08-private-state-store-shape.md) — accepted exact clarification текущего `IS-08`;
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md) — canonical operational prompt template, revision `CSPT-02`.

---

# 3. Принятые implementation checkpoints

| Step | Статус | Основной implementation/correction |
|---|---|---|
| `IS-01` | accepted | bootstrap + correction `584db766...` |
| `IS-02` | accepted | `e457ada1...` identity/revision/logical time |
| `IS-03` | accepted | `a5c9f314...` availability/provenance/errors |
| `IS-04` | accepted | `86d38ff6...` + correction `afc1937b...` |
| `IS-05` | accepted | `df602abb...` CognitiveState/StateProjection |
| `IS-06` | accepted | `633babaf...` module contracts/proposals |
| `IS-07` | accepted | `c8852930...` + correction `5b60d001...` |

## `V0.1-IS-07 — Execution Plan Compiler`

Implementation commit:

```text
c88529300ab926b052e0b40089539735d64ac2e7
feat(runtime): add deterministic execution plan compiler
```

Correction commit после ChatGPT audit:

```text
5b60d001f2d730c3fdc921244bc68b122f784a16
fix(runtime): restrict execution plan construction
```

ChatGPT audit подтвердил deterministic `CURRENT_CYCLE` DAG, topological waves, stable fingerprint, fail-closed plan validation, отсутствие ID consumption при failed compile и compiler-controlled `ExecutionPlan` construction. Targeted verification и local `FULL-C0`: `PASS`; post-push Ubuntu/Windows GitHub Actions подтверждены оператором проекта как успешные.

`V01-007 — DAG validity`: **closed**.

---

# 4. Разрешённая implementation работа

Единственный разрешённый следующий coding step:

```text
V0.1-IS-08 — PrivateStateStore
```

Scope определяется accepted `implementation-sequence.md`, `is-06-contract-shape.md` и accepted exact clarification [`../versions/v0.1/is-08-private-state-store-shape.md`](../versions/v0.1/is-08-private-state-store-shape.md).

Ключевой результат:

```text
PrivateStateSlot
PrivateStateStore
explicit stateful initialization
own snapshot / stateless Unavailable semantics
private proposal validation + freeze
prepared private update
internal all-or-nothing apply primitive
```

Exact clarification фиксирует:

- каждый active `STATEFUL` module обязан получить explicit initial private value;
- initial private value проходит свой `PrivateStateContract.freeze()` и получает `PrivateStateRevision.initial()`;
- `STATELESS` module slot не имеет и получает `Unavailable`;
- proposal validation не мутирует store;
- actual replacement выполняется только internal all-or-nothing primitive после полной prevalidation batch;
- cognitive modules никогда не получают store/slot reference.

`V01-008` должен достигнуть уровня `substantial/partial`; полная atomic public+private semantics остаётся `IS-09`.

`V0.1-IS-09` и последующие шаги закрыты до implementation + verification + отдельного ChatGPT audit `IS-08`.

---

# 5. Operational prompt

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

Перед открытием `IS-08` применимость `CSPT-02` проверена после добавления step-specific clarification. Новых CI jobs, verification profiles, mandatory commands или reporting semantics не появилось, поэтому revision шаблона не изменяется.

`CSPT-02` требует targeted verification, полный local `FULL-C0`, truthful GitHub Actions status/evidence и предложение Conventional Commit message в конце отчёта.

---

# 6. Ограничения

- не переходить к `V0.1-IS-09` до final acceptance `IS-08`;
- не начинать `v0.2` до полного acceptance gate `v0.1`;
- implementation-level correction допустима только внутри accepted `v0.1` semantics;
- semantic blocker требует design review и нового ADR/freeze update;
- Codex не меняет самостоятельно accepted version design/F31 и не открывает следующий implementation step.
