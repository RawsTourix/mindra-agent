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

После `DU-32` и появления concrete version design дополнительно обязательны exact contracts, version specification, `implementation-sequence.md`, testing/evaluation requirements и acceptance criteria.

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
```

```text
Design ≠ Implementation ≠ Engineering Testing ≠ Research Evidence
```

Research/engineering evidence инициирует review/ADR при необходимости, но не переписывает architecture автоматически.

---

# Язык

Документация и комментарии в коде — на русском языке. Technical identifiers/API/package/class/function/type names остаются на английском.

---

# Исследовательский журнал

Датированные literature/research/tool pass хранятся в [`research/`](research/). Future hypotheses/experiments/results хранятся отдельно от canonical design.

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

После `DU-29` implementation correctness проверяется через versioned `VerificationObligation/VerificationMatrix`, layered conformance/property/state-machine/fault/persistence tests и CI verification gates:

- [`design/engineering-testing.md`](design/engineering-testing.md);
- [`design/contracts/engineering-testing.md`](design/contracts/engineering-testing.md);
- [`design/decisions/ADR-0029-layered-invariant-driven-engineering-verification.md`](design/decisions/ADR-0029-layered-invariant-driven-engineering-verification.md).

Ключевое различие:

```text
Engineering Testing
≠
MINDRA-Eval
```

---

# Текущий этап

Проект находится на стадии **последовательного канонического архитектурного проектирования**.

`DU-01 … DU-29` приняты. Следующий допустимый этап определяется только [`design/current.md`](design/current.md); полный порядок задан в [`design/documentation-plan.md`](design/documentation-plan.md).

Production/research implementation, exact contract freeze, version roadmap и implementation sequences ещё не начаты.
