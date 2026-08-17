# Документация MINDRA

## Назначение

Этот каталог — каноническая база знаний исследовательского проекта MINDRA.

Документация должна позволять человеку, ChatGPT, Codex или другому coding agent восстановить актуальный архитектурный контекст без истории чатов.

Краткое задание не заменяет repository documentation.

---

# Быстрый порядок чтения

## Для общего понимания

1. [`project-concept.md`](project-concept.md)
2. [`architecture-concept.md`](architecture-concept.md)
3. [`research-methodology.md`](research-methodology.md)
4. [`design/README.md`](design/README.md)
5. [`design/current.md`](design/current.md)
6. [`design/contract-adr-consistency-freeze.md`](design/contract-adr-consistency-freeze.md) — после `DU-31`.

## Перед архитектурной работой

1. [`../AGENTS.md`](../AGENTS.md)
2. [`design/current.md`](design/current.md)
3. [`design/principles.md`](design/principles.md)
4. [`design/contract-adr-consistency-freeze.md`](design/contract-adr-consistency-freeze.md)
5. [`design/contracts/semantic-freeze-manifest.md`](design/contracts/semantic-freeze-manifest.md)
6. [`design/glossary.md`](design/glossary.md)
7. [`design/documentation-plan.md`](design/documentation-plan.md)
8. релевантные canonical design owners;
9. релевантные accepted/non-superseded ADR;
10. релевантные semantic contracts;
11. датированный research/tool pass, если он material для текущего решения.

## Перед будущей реализацией

После `DU-32` и появления concrete version design дополнительно обязательны:

- semantic baseline `F31`;
- version specification;
- version-specific exact contracts/API decisions;
- `implementation-sequence.md`;
- Engineering Verification obligations;
- MINDRA-Eval requirements и acceptance criteria.

До появления version specification implementation choices не угадываются заранее.

---

# Уровни истины

```text
Concept
→ Canonical Design + ADR
→ Semantic Freeze Baseline F31
→ semantic-frozen contracts
→ Version design / exact contracts
→ Implementation sequence
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

После `DU-31` архитектурная линия `DU-01 … DU-30` считается согласованной baseline:

```text
F31
= ready for version planning
```

Canonical owner:

- [`design/contract-adr-consistency-freeze.md`](design/contract-adr-consistency-freeze.md).

Machine-facing freeze manifest:

- [`design/contracts/semantic-freeze-manifest.md`](design/contracts/semantic-freeze-manifest.md).

Accepted decision:

- [`design/decisions/ADR-0031-semantic-contract-consistency-freeze.md`](design/decisions/ADR-0031-semantic-contract-consistency-freeze.md).

Freeze означает semantic ownership/lifecycle/source/provenance/causal boundaries, а не exact Python API.

---

# Исследовательский журнал

Датированные literature/research/tool pass хранятся в [`research/`](research/). Future hypotheses/experiments/results/claim evidence хранятся отдельно от canonical design.

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

Проект находится на стадии **Version Roadmap planning после semantic freeze**.

`DU-01 … DU-31` приняты. Следующий допустимый этап определяется только [`design/current.md`](design/current.md); сейчас это:

```text
DU-32 — Version Roadmap
```

Production/research implementation, concrete software versions и implementation sequences ещё не начаты.
