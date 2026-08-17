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

## Перед архитектурной работой

1. [`../AGENTS.md`](../AGENTS.md)
2. [`design/current.md`](design/current.md)
3. [`design/principles.md`](design/principles.md)
4. [`design/glossary.md`](design/glossary.md)
5. [`design/documentation-plan.md`](design/documentation-plan.md)
6. релевантные canonical design owners;
7. релевантные accepted/non-superseded ADR;
8. релевантные candidate contracts;
9. датированный research/tool pass, если текущий DU использовал внешний landscape.

## Перед будущей реализацией

После `DU-32` и появления concrete version design дополнительно обязательны semantic-frozen/exact contracts, version specification, `implementation-sequence.md`, testing/evaluation requirements и acceptance criteria.

До этого implementation choices не угадываются заранее.

---

# Уровни истины

```text
Concept
→ Canonical Design
→ ADR
→ Candidate / exact contracts
→ Version design
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

# Исследовательский журнал

Датированные literature/research/tool pass хранятся в [`research/`](research/). Future hypotheses/experiments/results/claim evidence хранятся отдельно от canonical design.

---

# Experience / Data Plane

- [`design/experience-data-replay.md`](design/experience-data-replay.md) — `DU-25`.

# Training Plane

- [`design/training-lifecycle.md`](design/training-lifecycle.md) — `DU-26`.

# Checkpoint / Reproducibility / Compute Plane

- [`design/checkpoint-reproducibility-compute.md`](design/checkpoint-reproducibility-compute.md) — `DU-27`.

# Evaluation Plane

- [`design/mindra-eval.md`](design/mindra-eval.md) — `DU-28`.

# Engineering Verification Plane

- [`design/engineering-testing.md`](design/engineering-testing.md) — `DU-29`.

Engineering correctness не заменяет research evidence функциональной полезности.

# Research Claims / Limitations Plane

После `DU-30` scientific/reporting claims имеют explicit scope/evidence/limitations/known-unknowns и lifecycle:

- [`design/research-claims-limitations.md`](design/research-claims-limitations.md);
- [`design/contracts/research-claims-limitations.md`](design/contracts/research-claims-limitations.md);
- [`design/decisions/ADR-0030-versioned-evidence-bounded-research-claims.md`](design/decisions/ADR-0030-versioned-evidence-bounded-research-claims.md).

Ключевые различия:

```text
Observation ≠ Interpretation ≠ ResearchClaim
association ≠ causation
claim scope ≠ universal scope
functional similarity ≠ phenomenological equivalence
```

---

# Текущий этап

Проект находится на стадии **последовательного канонического архитектурного проектирования**.

`DU-01 … DU-30` приняты. Следующий допустимый этап определяется только [`design/current.md`](design/current.md); полный порядок задан в [`design/documentation-plan.md`](design/documentation-plan.md).

Следующий этап — общий `DU-31 — Contract + ADR Consistency Freeze`, а не новая cognitive subsystem.

Production/research implementation, общий contract freeze, version roadmap и implementation sequences ещё не начаты.
