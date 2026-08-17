# MINDRA

**MINDRA — Modular Internal Dynamics & Reasoning Architecture** — исследовательский проект по разработке модульной когнитивной архитектуры для нейросетевых агентов.

Проект исследует, можно ли построить систему, в которой поведение определяется не только внешней задачей и базовой языковой моделью, но также собственным изменяющимся внутренним состоянием, памятью, моделью мира и себя, внутренними сигналами, drives, appraisal/affect, valuation, управляемым распределением cognitive processing, adaptive Executive Control, явной Policy/Planner boundary и причинно строгой Action Boundary между выбранным намерением и внешним действием.

Отдельный Experience/Data plane сохраняет причинную историю работы системы и позволяет строить воспроизводимые research/training datasets без смешивания Agent Memory, source experience и Training Replay.

MINDRA не объявляет целью создание сознания или доказательство субъективного опыта у искусственной системы. Исследуются функционально измеримые механизмы и их причинный вклад в поведение.

## Статус

Проект находится на стадии **канонического архитектурного и исследовательского проектирования**.

Documentation foundation и `DU-01 … DU-25` приняты. Следующий допустимый Design Update всегда указан в [`docs/design/current.md`](docs/design/current.md).

Production/research implementation, software versions, exact contract freeze, конкретные algorithms/frameworks, storage backend и Cortex backend ещё не зафиксированы.

## Основные принципы

- модульная и заменяемая архитектура;
- LLM — сменный Cortex backend, а не вся система;
- явные contracts/ownership/provenance;
- versioned committed state и causal execution;
- immutable source experience + explicit derived data lineage;
- ablation/control/intervention для каждого существенного механизма;
- воспроизводимость;
- разделение Design / Implementation / Research Evidence;
- причинная проверка функционального вклада;
- отсутствие антропоморфных выводов без достаточных оснований.

## Документация

Входная точка: [`docs/README.md`](docs/README.md).

Перед изменением design/implementation coding agent обязан прочитать [`AGENTS.md`](AGENTS.md) и актуальный [`docs/design/current.md`](docs/design/current.md).

## Язык проекта

Документация и комментарии в исходном коде — на русском языке. Technical identifiers/API/package/class/function/type names остаются на английском.

## Репозиторий

`RawsTourix/mindra-agent`
