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
implementation: V0.1-IS-01 implemented; final verification evidence pending
current implementation work: V0.1-IS-01 verification follow-up
next coding step V0.1-IS-02: CLOSED until audit/verification acceptance
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
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md) — canonical operational prompt template для одного implementation step.

Tooling research pass:

- [`../research/literature/v0.1-core-kernel-tooling-landscape-2026-08.md`](../research/literature/v0.1-core-kernel-tooling-landscape-2026-08.md)

---

# 3. Разрешённая implementation работа

`V0.1-IS-01` уже реализован Codex и прошёл содержательный ChatGPT code/design audit без correction blocker.

До открытия `IS-02` разрешена только verification-follow-up работа для `IS-01`:

```text
V0.1-IS-01 — final local/CI verification evidence
```

Нужно подтвердить предусмотренный local `FULL-C0` и, когда изменения доступны как remote commit, GitHub Actions Linux/Windows evidence либо честно зафиксировать `PENDING/NOT AVAILABLE` до появления такого evidence.

Следующий implementation step:

```text
V0.1-IS-02 — Identity / revision / logical time
```

остаётся закрытым до завершения verification + отдельного ChatGPT audit `IS-01`.

Для всех implementation-задач используется canonical prompt:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md).

Встроенные/старые примеры prompt в version-specific документах или истории чата не считаются актуальным source of truth, если расходятся с canonical template.

---

# 4. Ограничения

- не переходить к `V0.1-IS-02` до acceptance audit `IS-01`;
- не начинать `v0.2` до полного acceptance gate `v0.1`;
- implementation-level correction допустима только внутри accepted `v0.1` semantics;
- semantic blocker требует design review и нового ADR/freeze update;
- Codex не меняет самостоятельно accepted version design/F31 и не отмечает milestone завершённым;
- каждый implementation prompt включает targeted verification, полный уже существующий local regression gate и CI status/evidence semantics согласно canonical template;
- `CI PENDING/NOT AVAILABLE` не считается `PASS`.

---

# 5. Implementation status

```text
Production/research code: bootstrap Core Kernel создан
Implementation HEAD: commit с V0.1-IS-01 существует в main history
C0 verification environment: создан
V0.1-IS-01 code/design audit: PASS
V0.1-IS-01 final execution evidence: pending confirmation
Codex coding: разрешён только verification-follow-up для V0.1-IS-01
V0.1-IS-02: закрыт
```
