# MINDRA

**MINDRA — Modular Internal Dynamics & Reasoning Architecture** — исследовательский проект по разработке модульной когнитивной архитектуры для нейросетевых агентов.

Проект исследует, можно ли построить систему, в которой поведение определяется не только внешней задачей и базовой языковой моделью, но также собственным изменяющимся внутренним состоянием, памятью, моделью мира и себя, внутренними сигналами, drives, appraisal/affect, valuation, управляемым распределением cognitive processing, adaptive Executive Control, явной Policy/Planner boundary и причинно строгой Action Boundary между выбранным намерением и внешним действием.

Отдельные Experience/Data, Training, Checkpoint/Reproducibility/Compute, Evaluation, Engineering Verification и Research Claims/Limitations planes сохраняют причинную историю, изменяют trainable revisions через explicit candidate → validation → activation lifecycle, обеспечивают scoped restore/reproducibility, проверяют функциональный причинный вклад механизмов, машинно контролируют contracts/invariants и ограничивают научные утверждения реальным evidence/scope — не смешиваясь с ordinary cognition.

MINDRA не объявляет целью создание сознания или доказательство субъективного опыта у искусственной системы. Исследуются функционально измеримые механизмы и их причинный вклад в поведение; функциональное сходство не считается доказательством феноменологического равенства.

## Статус

Общий архитектурный цикл **`DU-00 … DU-32` завершён**.

После `DU-31` semantic architecture получила baseline:

```text
F31
```

После `DU-32` принят software roadmap:

```text
v0.1 Core Kernel
→ v0.2 MicroWorld Interaction
→ v0.3 Cortex Gateway
→ v0.4 Memory & Restore
→ v0.5 World & Self
→ v0.6 Intrinsic / Drives / Appraisal
→ v0.7 Affect / Valuation / Salience
→ v0.8 Memory Regulation / Workspace
→ v0.9 Executive / Planner
→ v0.10 Training & Revision Lifecycle
→ v0.11 Research Harness
→ v0.12 Integration Hardening
→ v1.0 MINDRA Research Baseline
```

Production/research implementation ещё не начата.

Следующий этап — **подробный Version Design `v0.1 Core Kernel`**, затем его `implementation-sequence.md`, и только после этого coding.

## Основные принципы

- модульная и заменяемая архитектура;
- LLM — сменный Cortex backend, а не вся система;
- явные contracts/ownership/provenance;
- versioned committed state и causal execution;
- immutable source experience + explicit derived data lineage;
- Training Runtime отдельно от cognition;
- candidate/validated/activated revisions вместо скрытой live mutation;
- manifest-driven checkpoints и scoped reproducibility claims;
- typed evaluation evidence вместо одного universal score;
- invariant-driven Engineering Verification;
- versioned Research Claims с explicit scope/limitations/known unknowns;
- negative/null/inconclusive evidence не скрывается;
- semantic freeze `F31` до реализации;
- vertical runnable milestones вместо реализации modules по порядку design-документов;
- CPU-only deterministic core; neural compute подключается как optional capability;
- breaking semantic change после F31 — только через новый ADR;
- разделение Design / Implementation / Engineering Testing / Research Evidence / Research Claims;
- отсутствие anthropomorphic/phenomenological выводов без достаточного evidence.

## Документация

Входная точка: [`docs/README.md`](docs/README.md).

Semantic freeze:

- [`docs/design/contract-adr-consistency-freeze.md`](docs/design/contract-adr-consistency-freeze.md)

Roadmap:

- [`docs/design/version-roadmap.md`](docs/design/version-roadmap.md)
- [`docs/versions/README.md`](docs/versions/README.md)

Фактический текущий статус:

- [`docs/design/current.md`](docs/design/current.md)

Перед любой version/implementation работой coding agent обязан прочитать [`AGENTS.md`](AGENTS.md).

## Язык проекта

Документация и комментарии в исходном коде — на русском языке. Technical identifiers/API/package/class/function/type names остаются на английском.

## Репозиторий

`RawsTourix/mindra-agent`
