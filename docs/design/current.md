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
implementation: не начата
current implementation step: V0.1-IS-01
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
- [`../versions/v0.1/implementation-sequence.md`](../versions/v0.1/implementation-sequence.md) — accepted dependency-ordered implementation plan.

Tooling research pass:

- [`../research/literature/v0.1-core-kernel-tooling-landscape-2026-08.md`](../research/literature/v0.1-core-kernel-tooling-landscape-2026-08.md)

---

# 3. Разрешённая implementation работа

Единственный разрешённый следующий coding step:

```text
V0.1-IS-01 — Project bootstrap & verification shell
```

Codex выполняет только этот step согласно `implementation-sequence.md`.

После implementation + предусмотренных проверок выполняется ChatGPT audit. Следующий `IS` не открывается автоматически из-за того, что Codex завершил предыдущий task.

Стандартный prompt находится в разделе `Стандартный prompt для Codex` implementation sequence.

---

# 4. Ограничения

- не переходить к `V0.1-IS-02` до audit `IS-01`;
- не начинать `v0.2` до полного acceptance gate `v0.1`;
- implementation-level correction допустима только внутри accepted `v0.1` semantics;
- semantic blocker требует design review и нового ADR/freeze update;
- Codex не меняет самостоятельно accepted version design/F31 и не отмечает milestone завершённым.

---

# 5. Implementation status

```text
Production/research code: отсутствует
Implementation HEAD: отсутствует
C0 verification environment: ещё не создан
Codex coding: разрешён только для V0.1-IS-01
```
