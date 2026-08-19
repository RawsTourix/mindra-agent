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
current implementation step: V0.1-IS-02 — OPEN
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
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md) — canonical operational prompt template.

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

Correction меняет только CI encoding environment для `lint-imports`; semantic/version scope не изменён.

`V01-012` и `V01-014` остаются закрытыми только на предусмотренном для `IS-01` уровне `foundation/partial`; окончательное закрытие `V01-014` выполняется в `IS-16`.

---

# 4. Разрешённая implementation работа

Единственный разрешённый следующий coding step:

```text
V0.1-IS-02 — Identity / revision / logical time
```

Codex выполняет только этот step согласно accepted `implementation-sequence.md` и canonical `CSPT-01`.

Следующий `IS` не открывается автоматически после завершения Codex task: после implementation + targeted verification + `FULL-C0` + CI status/evidence выполняется отдельный ChatGPT audit.

---

# 5. Operational prompt

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-01`.

Перед открытием `IS-02` применимость `CSPT-01` повторно проверена. Новых verification profiles, CI jobs, mandatory commands или reporting semantics не появилось, поэтому revision шаблона **не изменяется**.

Для `v0.1` после `IS-01` каждый implementation task обязан выполнить:

1. targeted verification текущего step;
2. полный local `FULL-C0` regression gate;
3. GitHub Actions status/evidence для remote commit, если доступно.

`PENDING`, `RUNNING` и `NOT AVAILABLE` не считаются `PASS`.

---

# 6. Ограничения

- не переходить к `V0.1-IS-03` до audit `IS-02`;
- не начинать `v0.2` до полного acceptance gate `v0.1`;
- implementation-level correction допустима только внутри accepted `v0.1` semantics;
- semantic blocker требует design review и нового ADR/freeze update;
- Codex не меняет самостоятельно accepted version design/F31 и не открывает следующий implementation step.

---

# 7. Implementation status

```text
Production/research code: bootstrap Core Kernel создан
V0.1-IS-01 implementation: ACCEPTED
V0.1-IS-01 verification: PASS
Current permitted coding: V0.1-IS-02
V0.1-IS-03+: CLOSED
```
