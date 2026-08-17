# MINDRA

**MINDRA — Modular Internal Dynamics & Reasoning Architecture** — исследовательский проект по разработке модульной когнитивной архитектуры для нейросетевых агентов.

Проект исследует, можно ли построить систему, в которой поведение определяется не только внешней задачей и базовой языковой моделью, но также собственным изменяющимся внутренним состоянием, памятью, моделью мира и себя, внутренними сигналами, drives, appraisal/affect, valuation, управляемым распределением cognitive processing, adaptive Executive Control, явной Policy/Planner boundary и причинно строгой Action Boundary между выбранным намерением и внешним действием.

Отдельные Experience/Data, Training, Checkpoint/Reproducibility/Compute, Evaluation, Engineering Verification и Research Claims/Limitations planes сохраняют причинную историю, изменяют trainable revisions через explicit candidate → validation → activation lifecycle, обеспечивают scoped restore/reproducibility, проверяют функциональный причинный вклад механизмов, машинно контролируют соблюдение contracts/invariants и ограничивают научные утверждения реальным evidence/scope — не смешиваясь с ordinary cognition.

MINDRA не объявляет целью создание сознания или доказательство субъективного опыта у искусственной системы. Исследуются функционально измеримые механизмы и их причинный вклад в поведение; функциональное сходство не считается доказательством феноменологического равенства.

## Статус

Проект находится на стадии **канонического архитектурного проектирования перед Version Roadmap**.

Documentation foundation и `DU-01 … DU-31` приняты.

После `DU-31` архитектура `DU-01 … DU-30` получила semantic freeze baseline:

```text
F31 — ready for version planning
```

Contracts `DU-07 … DU-30` frozen по смыслу, но exact Python/API representation, algorithms/frameworks/models/storage/testing backends ещё не выбраны.

Следующий допустимый Design Update всегда указан в [`docs/design/current.md`](docs/design/current.md). Сейчас это `DU-32 — Version Roadmap`.

Production/research implementation ещё не начата.

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
- invariant-driven Engineering Verification вместо одной метрики line coverage;
- versioned Research Claims с explicit scope/limitations/known unknowns;
- negative/null/inconclusive evidence не скрывается;
- ablation/control/matched-control/intervention для существенных механизмов;
- compute/data/context/tuning attribution;
- semantic freeze до version planning;
- breaking semantic change после F31 — только через новый ADR;
- разделение Design / Implementation / Engineering Testing / Research Evidence / Research Claims;
- причинная проверка функционального вклада;
- отсутствие антропоморфных и phenomenological выводов без достаточных оснований.

## Документация

Входная точка: [`docs/README.md`](docs/README.md).

Перед изменением design/implementation coding agent обязан прочитать [`AGENTS.md`](AGENTS.md), [`docs/design/current.md`](docs/design/current.md) и после DU-31 [`docs/design/contract-adr-consistency-freeze.md`](docs/design/contract-adr-consistency-freeze.md).

## Язык проекта

Документация и комментарии в исходном коде — на русском языке. Technical identifiers/API/package/class/function/type names остаются на английском.

## Репозиторий

`RawsTourix/mindra-agent`
