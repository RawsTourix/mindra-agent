# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какая работа разрешена следующей.

---

# 1. Общий статус

Общий архитектурный цикл `DU-00 … DU-32` завершён и принят.

```text
Semantic Freeze Baseline F31: accepted
Version Roadmap DU-32: accepted
Current milestone: v0.1 Core Kernel
v0.1 exact design: accepted
v0.1 implementation-sequence: accepted
V0.1-IS-01: accepted
V0.1-IS-02: implemented; code/design audit PASS; remote CI evidence pending
current implementation work: V0.1-IS-02 verification follow-up only
V0.1-IS-03: CLOSED until final IS-02 acceptance
```

Приняты 32 ADR и semantic contracts `DU-07 … DU-30`, frozen по смыслу как baseline `F31`.

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
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md) — canonical operational prompt template, revision `CSPT-02`.

---

# 3. Принятый результат `V0.1-IS-01`

`V0.1-IS-01 — Project bootstrap & verification shell` принят после implementation audit и correction audit.

Подтверждено:

```text
implementation scope                         PASS
forbidden scope                             PASS
local FULL-C0                               PASS
GitHub Actions Ubuntu                       PASS
GitHub Actions Windows после UTF-8 fix      PASS
```

Correction commit:

```text
584db766e190739e22c7616f1ea1e68428ecf86e
fix(ci): enable UTF-8 for Import Linter on Windows
```

`V01-012` и `V01-014` остаются закрытыми только на предусмотренном для `IS-01` уровне `foundation/partial`; окончательное закрытие `V01-014` выполняется в `IS-16`.

---

# 4. Текущее состояние `V0.1-IS-02`

Implementation commit:

```text
e457ada1aa8ded3ff70cd47b5328e2bbcc96f724
feat(core): add identity revision and logical time primitives
```

ChatGPT audit подтверждает:

```text
scope IS-02                               PASS
forbidden scope IS-03+                   PASS
14 causal UUID identity types            PASS
semantic ID validation                   PASS
IdFactory boundary                       PASS
Uuid7IdFactory                           PASS
DeterministicIdFactory                   PASS
5 separate revision value types          PASS
logical temporal hierarchy               PASS
wall-clock exclusion                     PASS
code/design compatibility with F31       PASS
```

По отчёту Codex локально подтверждено:

```text
targeted verification                    PASS
FULL-C0                                  PASS
48 tests                                 PASS
build wheel/sdist                        PASS
```

Remote GitHub Actions для implementation commit были `PENDING` на момент отчёта Codex. Доступный ChatGPT GitHub connector не показывает push-triggered workflow runs по SHA, поэтому post-push Ubuntu/Windows evidence ещё должно быть подтверждено отдельно.

Новых нумерованных `V01-*` obligations `IS-02` формально не закрывает; он создаёт foundation для последующих revision/evidence/determinism obligations.

---

# 5. Разрешённая implementation работа

До final acceptance `IS-02` разрешена только verification-follow-up работа:

```text
V0.1-IS-02 — remote CI evidence / defect correction внутри текущего scope, если потребуется
```

`V0.1-IS-03 — Availability / provenance / error foundation` пока закрыт.

После подтверждения declared GitHub Actions jobs выполняется финальный acceptance update и только затем открывается `IS-03`.

---

# 6. Operational prompt

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

`CSPT-02` добавляет обязательный пункт итогового отчёта:

```text
предложить одно краткое название коммита в стиле Conventional Commits
```

Это не является разрешением Codex самостоятельно создавать или отправлять commit/push.

Для `v0.1` после `IS-01` каждый implementation task обязан выполнить:

1. targeted verification текущего step;
2. полный local `FULL-C0` regression gate;
3. GitHub Actions status/evidence для remote commit, если доступно.

`PENDING`, `RUNNING` и `NOT AVAILABLE` не считаются `PASS`.

---

# 7. Ограничения

- не переходить к `V0.1-IS-03` до final acceptance `IS-02`;
- не начинать `v0.2` до полного acceptance gate `v0.1`;
- implementation-level correction допустима только внутри accepted `v0.1` semantics;
- semantic blocker требует design review и нового ADR/freeze update;
- Codex не меняет самостоятельно accepted version design/F31 и не открывает следующий implementation step.

---

# 8. Implementation status

```text
V0.1-IS-01 implementation: ACCEPTED
V0.1-IS-01 verification: PASS
V0.1-IS-02 implementation: CODE/DESIGN PASS
V0.1-IS-02 local verification: PASS
V0.1-IS-02 remote CI evidence: PENDING CONFIRMATION
Current permitted work: IS-02 verification follow-up only
V0.1-IS-03+: CLOSED
```
