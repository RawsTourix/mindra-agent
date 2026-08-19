# Документация MINDRA

## Назначение

Этот каталог — каноническая база знаний исследовательского проекта MINDRA.

Документация должна позволять человеку, ChatGPT, Codex или другому coding agent восстановить актуальный контекст без истории чатов.

Краткое задание не заменяет repository documentation.

---

# Быстрый порядок чтения

## Для общего понимания

1. [`project-concept.md`](project-concept.md)
2. [`architecture-concept.md`](architecture-concept.md)
3. [`research-methodology.md`](research-methodology.md)
4. [`design/README.md`](design/README.md)
5. [`design/current.md`](design/current.md)
6. [`design/contract-adr-consistency-freeze.md`](design/contract-adr-consistency-freeze.md)
7. [`design/version-roadmap.md`](design/version-roadmap.md)

## Перед version design / implementation

1. [`../AGENTS.md`](../AGENTS.md)
2. [`design/current.md`](design/current.md)
3. [`design/contract-adr-consistency-freeze.md`](design/contract-adr-consistency-freeze.md)
4. [`design/contracts/semantic-freeze-manifest.md`](design/contracts/semantic-freeze-manifest.md)
5. [`design/version-roadmap.md`](design/version-roadmap.md)
6. [`versions/README.md`](versions/README.md)
7. релевантные canonical design owners;
8. релевантные accepted/non-superseded ADR;
9. релевантные semantic contracts;
10. version-specific `README.md`;
11. version-specific `implementation-sequence.md`;
12. section только текущего разрешённого `Vx.y-IS-XX` перед coding;
13. датированный research/tool pass, если current tooling/model/compute materially влияет на решение.

Один Codex task реализует только один разрешённый implementation step; следующий открывается после verification + ChatGPT audit.

---

# Уровни истины

```text
Concept
→ Canonical Design + ADR
→ Semantic Freeze Baseline F31
→ semantic-frozen contracts
→ DU-32 Version Roadmap
→ Version design / exact contracts
→ Implementation sequence
→ Current implementation step
→ Implementation
→ Engineering / Research evidence
→ Versioned Research Claims
```

```text
Design
≠ Implementation
≠ Engineering Testing
≠ Research Evidence
≠ Research Claim
```

Research/engineering evidence инициирует claim/design review при необходимости, но не переписывает architecture автоматически.

---

# Язык

Документация и комментарии в коде — на русском языке. Technical identifiers/API/package/class/function/type names остаются на английском.

---

# Semantic Freeze F31

Canonical owner:

- [`design/contract-adr-consistency-freeze.md`](design/contract-adr-consistency-freeze.md)

Machine-facing manifest:

- [`design/contracts/semantic-freeze-manifest.md`](design/contracts/semantic-freeze-manifest.md)

Accepted decision:

- [`design/decisions/ADR-0031-semantic-contract-consistency-freeze.md`](design/decisions/ADR-0031-semantic-contract-consistency-freeze.md)

Freeze означает semantic ownership/lifecycle/source/provenance/causal boundaries, а не exact Python API.

---

# Version Roadmap

Canonical roadmap:

- [`design/version-roadmap.md`](design/version-roadmap.md)

Accepted decision:

- [`design/decisions/ADR-0032-vertical-capability-version-roadmap.md`](design/decisions/ADR-0032-vertical-capability-version-roadmap.md)

Version index:

- [`versions/README.md`](versions/README.md)

Roadmap строится вертикальными runnable slices и доводит проект от `v0.1 Core Kernel` до `v1.0 MINDRA Research Baseline`.

---

# Исследовательский журнал

Датированные literature/research/tool pass хранятся в [`research/`](research/). Hypotheses/experiments/results/claim evidence хранятся отдельно от canonical design.

---

# Внешние planes

- [`design/experience-data-replay.md`](design/experience-data-replay.md) — Experience/Data, `DU-25`;
- [`design/training-lifecycle.md`](design/training-lifecycle.md) — Training, `DU-26`;
- [`design/checkpoint-reproducibility-compute.md`](design/checkpoint-reproducibility-compute.md) — Checkpoint/Reproducibility/Compute, `DU-27`;
- [`design/mindra-eval.md`](design/mindra-eval.md) — Evaluation, `DU-28`;
- [`design/engineering-testing.md`](design/engineering-testing.md) — Engineering Verification, `DU-29`;
- [`design/research-claims-limitations.md`](design/research-claims-limitations.md) — Research Claims/Limitations, `DU-30`.

---

# Текущий этап

Общий архитектурный цикл:

```text
DU-00 … DU-32 complete
```

Semantic baseline `F31` и software roadmap приняты.

Для `v0.1 Core Kernel` приняты:

- [`versions/v0.1/README.md`](versions/v0.1/README.md) — exact design;
- [`versions/v0.1/implementation-sequence.md`](versions/v0.1/implementation-sequence.md) — `V0.1-IS-01 … V0.1-IS-16`.

Единственная разрешённая следующая coding-работа:

```text
V0.1-IS-01 — Project bootstrap & verification shell
```

Production/research implementation ещё не начата.

Фактический статус всегда определяется [`design/current.md`](design/current.md).
