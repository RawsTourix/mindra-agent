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
9. датированный research pass, если текущий DU использовал внешний literature/tooling landscape.

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

Research result, противоречащий design, инициирует review/ADR, а не молча переписывает архитектуру.

---

# Язык

Документация и комментарии в коде — на русском языке. Technical identifiers/API/package/class/function/type names остаются на английском.

---

# Исследовательский журнал

Датированные literature/research pass хранятся в [`research/`](research/). Future hypotheses/experiments/results хранятся отдельно от canonical design.

---

# Experience / Data Plane

После `DU-25` source experience, Agent Memory, Training Samples и Training Replay являются разными слоями:

- [`design/experience-data-replay.md`](design/experience-data-replay.md);
- [`design/contracts/experience-data-replay.md`](design/contracts/experience-data-replay.md);
- [`design/decisions/ADR-0025-causal-experience-journal-derived-projections.md`](design/decisions/ADR-0025-causal-experience-journal-derived-projections.md).

# Training Plane

После `DU-26` Training Runtime отделён от cognition и работает через pinned base revision → candidate → validation → activation:

- [`design/training-lifecycle.md`](design/training-lifecycle.md);
- [`design/contracts/training-lifecycle.md`](design/contracts/training-lifecycle.md);
- [`design/decisions/ADR-0026-candidate-revision-validated-activation-training-lifecycle.md`](design/decisions/ADR-0026-candidate-revision-validated-activation-training-lifecycle.md).

# Checkpoint / Reproducibility / Compute Plane

После `DU-27` checkpoint является manifest-driven causal artifact set с explicit scope/restore/reproducibility/compute semantics:

- [`design/checkpoint-reproducibility-compute.md`](design/checkpoint-reproducibility-compute.md);
- [`design/contracts/checkpoint-reproducibility-compute.md`](design/contracts/checkpoint-reproducibility-compute.md);
- [`design/decisions/ADR-0027-manifest-driven-causal-checkpoint-restore.md`](design/decisions/ADR-0027-manifest-driven-causal-checkpoint-restore.md).

# Evaluation Plane

После `DU-28` MINDRA-Eval отделён от Agent cognition и строит fully specified conditions, controls/interventions, typed metrics и statistical evidence:

- [`design/mindra-eval.md`](design/mindra-eval.md);
- [`design/contracts/mindra-eval.md`](design/contracts/mindra-eval.md);
- [`design/decisions/ADR-0028-multi-layer-causal-evaluation-harness.md`](design/decisions/ADR-0028-multi-layer-causal-evaluation-harness.md).

---

# Текущий этап

Проект находится на стадии **последовательного канонического архитектурного проектирования**.

`DU-01 … DU-28` приняты. Следующий допустимый этап определяется только [`design/current.md`](design/current.md); полный порядок задан в [`design/documentation-plan.md`](design/documentation-plan.md).

Production/research implementation, exact contract freeze, version roadmap и implementation sequences ещё не начаты.
