# ADR-0003 — Иерархическое логическое время и причинные commit boundaries

## Статус

`accepted`

## Связанный Design Update

`DU-03 — Runtime / Temporal Model`

## Канонический документ-владелец

[`../execution-model.md`](../execution-model.md)

---

# 1. Контекст

После `DU-01` и `DU-02` MINDRA уже различает логические границы Agent/Environment/training/evaluation и использует explicit composition вместо скрытых concrete dependencies.

Следующий слой design должен определить временную семантику до появления `CognitiveState` и `ModuleProtocol`.

Для проекта критично одновременно поддержать:

- несколько внутренних cognitive cycles на одно внешнее действие;
- controlled replay и counterfactual experiments;
- online/offline learning;
- replay/consolidation;
- sync и async physical execution;
- future distributed collection;
- причинную диагностику;
- evaluation без скрытых temporal confounders.

---

# 2. Проблема

Нужно выбрать temporal model, который отвечает на вопросы:

- что считается одним шагом Agent;
- совпадает ли внутреннее время с Environment step;
- когда действие становится необратимым фактом trajectory;
- как определить causal order при async execution;
- как различить runtime adaptation и training update;
- что именно должен воспроизводить replay;
- как episode reset соотносится с lifetime Agent.

---

# 3. Рассмотренные варианты

## Вариант A — один монолитный `agent.step()` на один `env.step()`

Семантика:

```text
observation
→ agent.step()
→ action
→ env.step()
```

### Плюсы

- очень простая реализация;
- естественно ложится на базовый RL loop;
- легко считать environment steps.

### Минусы

- внутренние reasoning/retrieval/planning cycles не имеют собственной идентичности;
- сложно причинно вмешиваться между внутренними стадиями;
- runtime state update и learning легко смешиваются;
- replay видит только крупные transition boundaries;
- будущий Executive Control пришлось бы встраивать внутрь непрозрачного шага;
- плохо подходит для анализа внутренней динамики MINDRA.

**Решение:** отклонён как canonical temporal model.

---

## Вариант B — полностью свободная event-driven модель

Любой модуль публикует события, а система реагирует на них без обязательных канонических commit boundaries.

### Плюсы

- максимальная гибкость;
- естественная асинхронность;
- подходит для distributed/event-driven систем.

### Минусы

- причинный порядок зависит от scheduler/interleaving;
- трудно обеспечить deterministic experiments;
- race conditions становятся частью поведения;
- module lifecycle из `DU-05` пришлось бы фактически решить заранее;
- counterfactual comparison усложняется;
- async deployment начинает определять semantics.

**Решение:** отклонён как базовая canonical model.

Event-driven implementation может позднее существовать под каноническими causal boundaries, если сохраняет их semantics.

---

## Вариант C — wall-clock / real-time модель

Временные отношения определяются физическими timestamps и elapsed time.

### Плюсы

- естественна для robotics/real-time environments;
- удобно измерять latency/deadlines.

### Минусы

- одинаковая архитектура ведёт себя семантически по-разному на разных GPU;
- Colab/network latency становится частью cognition;
- трудно сравнивать runs;
- аппаратная скорость становится скрытым confounder;
- не подходит как универсальная research semantics.

**Решение:** отклонён как canonical clock.

Wall-clock сохраняется как metadata и может стать частью конкретного Environment contract, если сама задача моделирует физическое время.

---

## Вариант D — иерархическое логическое время с causal commit boundaries

Семантика:

```text
Run
└── Agent Session
    └── Episode
        └── Decision Window
            ├── Cognitive Cycle ...
            ├── Action Commit
            └── Environment Transition / Outcome Commit

Learning / Replay / Consolidation имеют отдельные logical event sequences.
```

Physical async/concurrent execution разрешён, но обязан сводиться к однозначному causal order на уровне каждой trajectory.

### Плюсы

- внутренние и внешние временные масштабы различимы;
- удобно для causal intervention;
- несколько reasoning cycles не создают fake environment steps;
- async training можно снабдить revision provenance;
- natural boundary для replay/counterfactual;
- episode reset не уничтожает автоматически Agent session;
- physical deployment не определяет semantics;
- будущий scheduler может развиваться без смены временной модели.

### Минусы

- больше temporal metadata;
- implementation должна аккуратно поддерживать identifiers/commit boundaries;
- потребуется отдельный state versioning design;
- async execution потребует явного resolution ordering;
- простейший RL loop становится немного более формальным.

**Решение:** принят.

---

# 4. Evidence

## Gymnasium

Gymnasium поддерживает явные `reset()`/`step(action)` boundaries и различает `terminated` и `truncated`.

Источники:

- https://gymnasium.farama.org/api/env/
- https://gymnasium.farama.org/main/tutorials/handling_time_limits/

Это подтверждает ценность явной Environment transition semantics.

## TorchRL

TorchRL поддерживает synchronous и asynchronous collection; документация отдельно отмечает возможный policy lag при async collection.

Источники:

- https://docs.pytorch.org/rl/main/reference/collectors.html
- https://docs.pytorch.org/rl/main/reference/collectors_basics.html

Это поддерживает решение отделять physical concurrency от causal trajectory order и фиксировать Agent revision.

## PyTorch reproducibility

PyTorch не гарантирует полную bitwise reproducibility между releases/platforms/CPU/GPU, хотя предоставляет средства управления randomness и deterministic algorithms.

Источник:

- https://docs.pytorch.org/docs/stable/notes/randomness.html

Поэтому архитектура должна требовать causal reproducibility, но не обещать универсальную bitwise identity.

## Temporal abstraction

Option-Critic и более ранняя options framework демонстрируют самостоятельную ценность temporal abstraction в agent learning/planning.

Reference:

- https://arxiv.org/abs/1609.05140

MINDRA не принимает options как decision architecture; источник используется только как evidence различия временных масштабов.

---

# 5. Принятое решение

MINDRA принимает:

1. logical causal time как canonical temporal semantics;
2. различие `Run`, `Agent Session`, `Episode`, `Decision Window`, `Cognitive Cycle`, `Environment Transition`;
3. `Action Commit` и `Outcome Commit` как причинные boundaries;
4. возможность нескольких Cognitive Cycle на одно внешнее действие;
5. отдельные event sequences для Learning Update, Replay Step и Consolidation Event;
6. distinction runtime state update vs trainable learning;
7. physical sync/async execution как implementation topology при сохранении causal order;
8. Agent revision provenance для async learning/collection;
9. causal replay как обязательную цель;
10. bitwise replay только как best-effort runtime property;
11. Environment reset как episode boundary, а не полный Agent reset.

---

# 6. Дополнительные invariants

## ADR3-01

Wall-clock не является canonical cognitive clock.

## ADR3-02

Уже committed action/outcome не могут быть ретроактивно переписаны последующим learning.

## ADR3-03

Batch completion order не определяет causal order независимых trajectories.

## ADR3-04

Replay/imagined/counterfactual transitions должны отличаться от observed transitions по provenance.

## ADR3-05

Будущий Executive Control может регулировать количество внутренних cycles, но не нарушает commit semantics.

## ADR3-06

Partial physical computation не становится committed event автоматически.

---

# 7. Последствия

## Положительные

- `CognitiveState` можно проектировать с ясной temporal scope;
- появляется основа для causal intervention;
- async training становится исследовательски наблюдаемым;
- future planner/workspace/executive control получают внутреннее время;
- deterministic replay получает реалистичное определение;
- evaluation episodes можно корректно изолировать;
- Colab/distributed execution не меняют semantic time.

## Отрицательные / стоимость

- нужно хранить больше identifiers и provenance;
- необходима дисциплина commit boundaries;
- future data schema станет сложнее простого `(s, a, r, s')`;
- понадобится строгая обработка interruption/restore;
- scheduler должен учитывать causal consistency.

---

# 8. Что решение намеренно не определяет

ADR не выбирает:

- конкретный scheduler;
- async framework;
- process/thread model;
- точный `CognitiveState`;
- exact state version type;
- количество Cognitive Cycle;
- конкретные timeout values;
- learning safe points;
- replay implementation;
- checkpoint transaction mechanism;
- environment framework;
- fixed или learned Executive Control.

---

# 9. Обязательные consistency updates

После принятия ADR должны быть согласованы:

- `docs/design/execution-model.md`;
- `docs/design/decisions/README.md`;
- `docs/design/README.md`;
- `docs/design/current.md`;
- `AGENTS.md` в части temporal discipline;
- `docs/design/glossary.md` при последующем consistency patch.

Следующий Design Update: `DU-04 — CognitiveState Semantics`.
