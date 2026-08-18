# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какая работа разрешена следующей.

---

# 1. Общий статус

Общий архитектурный цикл `DU-00 … DU-32` завершён и принят. Реализация ещё не начата.

```text
Semantic Freeze Baseline F31: accepted
Version Roadmap DU-32: accepted
Current milestone: v0.1 Core Kernel
v0.1 exact design: proposed / review
implementation-sequence: отсутствует
implementation: не начата
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

---

# 3. Текущий version design

Proposed design `v0.1 Core Kernel`:

- [`../versions/v0.1/README.md`](../versions/v0.1/README.md)

Tooling research pass:

- [`../research/literature/v0.1-core-kernel-tooling-landscape-2026-08.md`](../research/literature/v0.1-core-kernel-tooling-landscape-2026-08.md)

Design конкретизирует foundation `DU-01 … DU-06` и Engineering Verification foundation `DU-29`: Python/tooling, package layers, identities/revisions, `CognitiveState`, module protocol, DAG/waves, public/private transactional commits, composition/config, O0 trace, basic intervention seam и `V01-001 … V01-014`.

Статус:

```text
proposed
готов к design review
не принят автоматически
```

---

# 4. Следующая разрешённая работа

Сейчас разрешён только review proposed `v0.1` design.

Если `docs/versions/v0.1/README.md` принят, следующим документационным шагом становится:

```text
docs/versions/v0.1/implementation-sequence.md
```

Coding начинается только после acceptance обоих version-specific документов.

Implementation-level correction `v0.1` design не требует нового ADR, пока сохраняет F31 semantics. Semantic blocker требует design review и нового ADR/freeze update.

---

# 5. Implementation status

```text
Production/research code: отсутствует
Implementation HEAD: отсутствует
C0 verification environment: ещё не создан
Codex coding: не разрешён до acceptance version design + implementation sequence
```