# ADR-0007 — Разделить agent-visible Environment interaction и research-only world control

## Статус

`accepted`

## Контекст

MINDRA должна использовать Environment одновременно как:

- внешний мир для Agent;
- источник objective task consequences;
- источник ground truth для evaluator;
- объект snapshot/restore/fork;
- генератор procedurally varied tasks;
- основу causal interventions.

Если использовать один универсальный API без логических границ, возникает риск, что privileged world state, evaluator metadata или solver information попадут Agent через удобный `info`/debug channel.

Дополнительно стандартный RL interface `reset/step` сам по себе не определяет exact clone/fork, world versioning, hidden-rule provenance и intervention semantics.

---

## Проблема

Нужно определить Environment boundary так, чтобы:

1. baseline и MINDRA Agent получали одинаковый внешний контракт;
2. evaluator мог видеть больше, чем Agent;
3. research-only visibility не превращалась в agent-visible input;
4. Environment можно было сохранять и ветвить для counterfactual experiments;
5. общий contract не зависел от конкретной MicroWorld implementation;
6. Gymnasium compatibility оставалась возможной без принятия Gymnasium `info` как semantic API MINDRA.

---

## Рассмотренные варианты

### Вариант A — напрямую принять Gymnasium `Env` как канонический Environment contract

Плюсы:

- зрелый стандарт;
- широкий tooling ecosystem;
- `reset/step`, spaces, `terminated/truncated` уже определены;
- лёгкая интеграция RL baselines.

Минусы:

- `info` может содержать privileged/debug data и не задаёт строгой research boundary;
- exact snapshot/restore/fork не является общим обязательным API;
- нет обязательного world/generator/distribution versioning;
- intervention provenance не определена;
- MINDRA design оказался бы привязан к конкретному library-level API раньше version planning.

**Отклонено как canonical semantic contract.** Gymnasium остаётся interoperability target/adaptor candidate.

---

### Вариант B — сделать MicroWorld единственным Environment contract

Плюсы:

- минимальная implementation complexity;
- можно сразу оптимизировать API под gridworld;
- exact snapshot проще спроектировать.

Минусы:

- общая MINDRA architecture становится grid-specific;
- будущие environments потребуют ломать Agent boundary;
- concrete world representation начнёт протекать в Perception/Policy;
- нарушается принцип заменяемости внешней среды.

**Отклонено.**

---

### Вариант C — общий semantic Environment contract + reference MicroWorld + два logical planes

Environment имеет:

1. `Agent Interaction Plane` — raw observation, task specification, declared external feedback, termination/truncation и action interaction;
2. `Research Plane` — hidden world state, authoritative transition evidence, snapshot/restore/clone/fork, generator metadata, oracle/solvability и Environment interventions.

`MicroWorld` реализует этот contract как первая reference family.

Плюсы:

- privileged data отделены архитектурно;
- baseline fairness проще обеспечить;
- exact causal experiments поддерживаются;
- Environment остаётся заменяемым;
- Gymnasium adapter возможен;
- MicroWorld можно оптимизировать для диагностики, не делая gridworld универсальной моделью мира.

Минусы:

- больше типов/границ;
- будущая implementation сложнее простого `env.step()`;
- нужно дисциплинированно поддерживать две проекции transition data.

**Принято.**

---

### Вариант D — считать Environment частью Agent-owned state

Плюсы:

- clone Agent автоматически клонирует мир;
- меньше cross-boundary API.

Минусы:

- разрушает Agent/Environment separation `DU-01`;
- скрытый world state становится опасно близок к cognition;
- baseline comparison ухудшается;
- evaluator/world ownership становится неоднозначным.

**Отклонено.**

---

## Принятое решение

MINDRA принимает общий Environment semantic contract с двумя логически разными поверхностями.

### Agent Interaction Plane

Разрешает только task-defined agent-visible данные:

```text
Environment
    ↓ Raw Observation / External Task Specification / declared feedback
Agent
    ↓ committed action
Environment
```

### Research Plane

Разрешает privileged исследовательские операции и evidence:

```text
Environment
    ↓ hidden ground truth / Transition Record / snapshots
Evaluation / Artifact

Evaluation
    ↓ explicit Environment intervention
Environment Research Boundary
```

Research Plane не является runtime cognitive input.

`MicroWorld` принимается как первая reference Environment family: дискретный 2D symbolic world с partial observability, compositional entities, hidden causal rules, procedural generation и exact snapshot/fork support.

---

## Дополнительные решения

### External Task Feedback не равен Internal Utility

Environment не определяет внутреннюю ценность события для Agent.

### Seed не равен world identity

Воспроизводимость требует Environment/generator/task/distribution versions и при необходимости world manifest/content identity.

### Snapshot включает RNG

Exact restore/fork должен восстанавливать не только world objects, но все causally relevant Environment RNG states и pending dynamics.

### Full observability — control

MicroWorld ориентирован на partial observability, но full-observation condition должна быть доступна для research controls.

### Appearance и causal property factorized

Generator не должен канонически связывать цвет/форму с фиксированным смыслом.

---

## Последствия

### Положительные

- evaluator может иметь privileged ground truth без leakage;
- можно строить exact environment-side counterfactual branches;
- baseline и MINDRA Agent можно сравнивать на одном agent-visible contract;
- procedural train/test splits становятся explicit research artifact;
- Gymnasium integration остаётся возможной через adapter;
- future non-grid environments не требуют менять Agent architecture.

### Отрицательные

- потребуется отдельный research-facing Environment capability;
- нельзя просто передать Agent весь `info` underlying framework;
- snapshot/versioning/generator provenance увеличивают implementation scope;
- procedural task families потребуют validity/solvability checks.

---

## Evidence и существующие подходы

При проектировании использовались:

- Gymnasium Environment API: https://gymnasium.farama.org/api/env/
- MiniGrid: https://minigrid.farama.org/
- MiniGrid/Miniworld paper: https://arxiv.org/abs/2306.13831
- Procgen paper: https://arxiv.org/abs/1912.01588
- Procgen implementation: https://github.com/openai/procgen

Gymnasium подтверждает зрелость минимального `reset/step` + `terminated/truncated` interface. MiniGrid показывает выразительность минималистичных частично наблюдаемых gridworld tasks. Procgen показывает важность procedural level distributions, unseen levels и сохранения Environment state.

Ни один из этих проектов не принимается как полный canonical MINDRA contract.

---

## Что решение намеренно не определяет

ADR не выбирает:

- Python interface/base class;
- Gymnasium как dependency;
- observation/action encoding;
- exact reward/feedback schema;
- concrete generator algorithm;
- exact MicroWorld dimensions/entities;
- snapshot file format;
- solver technology;
- renderer;
- benchmark scoring;
- train/test manifest values.

---

## Затронутые документы

- `docs/design/modules/environment.md`;
- `docs/design/contracts/environment.md`;
- `docs/design/decisions/README.md`;
- `docs/design/README.md`;
- `docs/design/current.md`;
- `docs/design/glossary.md`;
- `AGENTS.md`.
