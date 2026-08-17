# MINDRA

**MINDRA — Modular Internal Dynamics & Reasoning Architecture** — исследовательский проект по разработке модульной когнитивной архитектуры для нейросетевых агентов.

Проект исследует, можно ли построить систему, в которой поведение определяется не только внешней задачей и базовой языковой моделью, но также собственным изменяющимся внутренним состоянием, памятью, моделью мира и себя, внутренними сигналами, drives, appraisal/affect, valuation, управляемым распределением cognitive processing, adaptive Executive Control, явной Policy/Planner boundary и причинно строгой Action Boundary между выбранным намерением и внешним действием.

Отдельные Experience/Data, Training, Checkpoint/Reproducibility/Compute, Evaluation и Engineering Verification planes сохраняют причинную историю, изменяют trainable revisions через explicit candidate → validation → activation lifecycle, обеспечивают scoped restore/reproducibility, проверяют функциональный причинный вклад механизмов и машинно контролируют соблюдение contracts/invariants — не смешиваясь с ordinary cognition.

MINDRA не объявляет целью создание сознания или доказательство субъективного опыта у искусственной системы. Исследуются функционально измеримые механизмы и их причинный вклад в поведение.

## Статус

Проект находится на стадии **канонического архитектурного и исследовательского проектирования**.

Documentation foundation и `DU-01 … DU-29` приняты. Следующий допустимый Design Update всегда указан в [`docs/design/current.md`](docs/design/current.md).

Production/research implementation, software versions, exact contract freeze, конкретные algorithms/frameworks, storage/evaluation/testing backends и Cortex backend ещё не зафиксированы.

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
- ablation/control/matched-control/intervention для существенных механизмов;
- compute/data/context attribution;
- разделение Design / Implementation / Engineering Testing / Research Evidence;
- причинная проверка функционального вклада;
- отсутствие антропоморфных выводов без достаточных оснований.

## Документация

Входная точка: [`docs/README.md`](docs/README.md).

Перед изменением design/implementation coding agent обязан прочитать [`AGENTS.md`](AGENTS.md) и актуальный [`docs/design/current.md`](docs/design/current.md).

## Язык проекта

Документация и комментарии в исходном коде — на русском языке. Technical identifiers/API/package/class/function/type names остаются на английском.

## Репозиторий

`RawsTourix/mindra-agent`
