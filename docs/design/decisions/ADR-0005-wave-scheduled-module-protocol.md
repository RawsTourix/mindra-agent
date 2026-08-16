# ADR-0005 — DAG scheduling с execution waves и атомарным module commit

## Статус

`accepted`

## Связанный Design Update

`DU-05 — Module Protocol & Scheduling`

## Канонический документ-владелец

[`../module-lifecycle.md`](../module-lifecycle.md)

---

# 1. Контекст

После `DU-01`–`DU-04` MINDRA уже имеет следующие инварианты:

- cognitive modules принадлежат Agent и не должны зависеть от concrete peers;
- runtime feedback не равен static dependency cycle;
- существует иерархическое logical time;
- несколько Cognitive Cycle могут предшествовать одному Environment action;
- `CognitiveState` состоит из committed semantically immutable revisions;
- canonical writes являются owner-scoped proposed updates;
- partial hidden mutation и `last-write-wins` запрещены;
- causally relevant module-private state также должно учитываться для reproducibility.

Теперь нужно определить общий способ исполнения модулей так, чтобы эти свойства не были разрушены main loop/scheduler implementation.

---

# 2. Проблема

Нужна scheduling model, которая одновременно:

1. выводит порядок исполнения из declared dependencies;
2. допускает parallel computation независимых modules;
3. сохраняет snapshot-consistent reads;
4. не делает completion order частью cognition;
5. поддерживает feedback через logical time;
6. обнаруживает instantaneous dependency cycles;
7. синхронизирует shared и module-private state;
8. позволяет NoOp/control substitution;
9. не требует конкретного async/graph framework;
10. оставляет место для future Executive Control.

---

# 3. Рассмотренные варианты

## Вариант A — ручной sequential main loop

Примерно:

```text
perception()
world_model()
self_model()
memory()
appraisal()
policy()
```

### Плюсы

- минимальная сложность;
- очевидный порядок;
- легко написать первый прототип.

### Минусы

- порядок зашивается в central loop;
- добавление модуля требует редактировать orchestration code;
- dependencies выражаются position, а не contracts;
- ablation создаёт ветки `if`;
- сложно параллелить независимые computations;
- легко получить partial mutable state;
- future modules начинают требовать ad-hoc вызовы.

**Решение:** отклонён как canonical model.

---

## Вариант B — глобальный event bus / pub-sub

Модули подписываются на события/fields и запускаются при публикации нужной информации.

### Плюсы

- высокая extensibility;
- естественно выглядит для event-driven cognition;
- producers не обязаны знать consumers.

### Минусы

- causal order становится труднее доказать;
- возможны re-entrant cascades;
- hidden subscriptions превращаются в скрытые dependencies;
- event arrival/completion order легко становится semantics;
- сложно получить атомарный committed snapshot;
- instantaneous cycles могут проявляться только runtime;
- debug/replay требуют сложного event-log reconstruction.

**Решение:** отклонён как primary scheduler semantics.

Observability event stream позднее допустим, но не как механизм cognitive dependency resolution.

---

## Вариант C — direct actor/module messaging

Каждый модуль имеет mailbox/API и напрямую запрашивает outputs других modules.

### Плюсы

- естественная concurrency;
- удобно распределять по processes/machines;
- локальное ownership private state.

### Минусы

- конфликтует с `DU-02` direct peer isolation;
- runtime call graph может стать циклическим;
- `CognitiveState` перестаёт быть canonical shared boundary;
- трудно контролировать какие revision читает каждый request;
- retries/timeouts способны менять causal semantics;
- исследовательская ablation усложняется.

**Решение:** отклонён как canonical cognitive interaction model.

Actor-like physical deployment позднее допустим за adapters, если сохраняет accepted semantics.

---

## Вариант D — declared DAG + execution waves + committed snapshots

Семантика:

```text
module descriptors
      ↓
compile dependency DAG
      ↓
topological waves
      ↓
modules in wave read same committed snapshot
      ↓
stage public/private effects
      ↓
validate
      ↓
atomic commit
      ↓
next wave
```

### Плюсы

- dependencies явны;
- instantaneous cycles обнаруживаются заранее;
- independent modules естественно параллелятся;
- completion order не влияет на state visibility;
- хорошо сочетается с versioned CognitiveState;
- NoOp/control implementations не требуют другого loop;
- можно строить architecture tests;
- future Executive Control может выбирать admissible optional work поверх graph;
- concrete scheduler library остаётся заменяемой.

### Минусы

- требует descriptors/contracts богаче простого `forward()`;
- transactional private state сложнее обычной mutation объекта;
- dynamic behavior нужно выражать через temporal cycles/control intents, а не произвольные recursive calls;
- graph compilation/validation добавляет инфраструктуру;
- слишком крупные waves могут требовать careful resource scheduling.

**Решение:** принят.

---

## Вариант E — полностью immutable event sourcing без materialized execution waves

Каждая module reaction создаёт event, а состояние вычисляется как projection event history.

### Плюсы

- превосходный audit trail;
- естественная lineage;
- replay-friendly.

### Минусы

- сложнее runtime current-state access;
- высокая event/log overhead;
- private neural state и tensor payload плохо ложатся в pure event model;
- не решает сам по себе scheduling conflicts;
- избыточно как основной execution mechanism.

**Решение:** отклонён как primary scheduler model.

Event/evidence log остаётся допустимым дополнением в `DU-06`/`DU-25`.

---

# 4. Evidence

## Declared data dependencies

TorchRL/TensorDict modules используют `in_keys`/`out_keys` для явного описания входных и выходных state entries.

Источники:

- https://docs.pytorch.org/rl/stable/tutorials/getting-started-1.html
- https://docs.pytorch.org/rl/stable/reference/generated/torchrl.modules.tensordict_module.SafeModule.html

Это показывает практичность declarative dataflow, хотя MINDRA требует более строгой ownership/freshness semantics.

## Topological scheduling

Python standard library содержит `graphlib.TopologicalSorter`, который поддерживает получение ready tasks и parallel-friendly dependency processing.

Источник:

- https://docs.python.org/3/library/graphlib.html

NetworkX поддерживает topological sort и topological generations для DAG.

Источники:

- https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.topological_sort.html
- https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.topological_generations.html

Следовательно, graph/wave mechanics не требуют custom graph-theory implementation.

## Functional state handling

PyTorch `torch.func.functional_call()` показывает возможность выполнять module относительно явно переданного parameter/buffer state вместо обязательной mutation исходного module object.

Источник:

- https://docs.pytorch.org/docs/stable/generated/torch.func.functional_call.html

Это поддерживает реализуемость staged/transactional patterns для части модулей, но не фиксирует конкретную implementation MINDRA.

## Structured concurrency

Python `asyncio.TaskGroup` показывает доступность structured parallel task scope с coordinated failure/cancellation.

Источник:

- https://docs.python.org/3/library/asyncio-task.html#task-groups

Это потенциальный implementation mechanism wave execution, но не canonical dependency.

---

# 5. Принятое решение

MINDRA принимает:

1. declarative module descriptors;
2. dependency graph, выводимый из reads/writes/freshness/phase constraints;
3. DAG requirement для instantaneous plan segment;
4. execution waves/topological generations;
5. same-base snapshot reads для modules одной wave;
6. staged public и causally relevant private effects;
7. validation + atomic semantic commit wave effects;
8. no implicit `last-write-wins`;
9. default rejection/recompute stale-base results;
10. fixed `agent_revision` для in-flight wave;
11. standardized lifecycle boundaries;
12. explicit failure/degradation semantics;
13. scheduler mechanics как часть Agent runtime core;
14. separation scheduler mechanics от future Executive Control policy.

---

# 6. Дополнительные invariants

## ADR5-01

Registration/import order не определяет cognitive execution order.

## ADR5-02

Physical completion order modules одной wave не определяет semantic visibility их outputs.

## ADR5-03

Runtime feedback loop должен пересекать explicit temporal/state boundary и не создаёт instantaneous graph cycle.

## ADR5-04

Causally relevant private state не может commit отдельно раньше связанного wave result без explicit semantics.

## ADR5-05

Default module failure не приводит к partial wave commit.

## ADR5-06

Scheduler не выполняет optimizer learning и не становится cognitive decision module.

## ADR5-07

NoOp/control implementations проходят тот же scheduler path, что и обычная implementation.

## ADR5-08

Future Executive Control ограничен admissible scheduler/contracts и не имеет права bypass dependency/state rules.

---

# 7. Последствия

## Положительные

- появляется единый lifecycle всех будущих modules;
- module graph можно валидировать до запуска;
- parallelism становится implementation detail, а не causal semantics;
- исследования ablation становятся чище;
- state snapshots не зависят от случайного ordering;
- private/public state можно согласовывать transactionally;
- feedback loops становятся явными во времени;
- future distributed execution остаётся возможным;
- architecture tests смогут проверять cycles/writers/undeclared dependencies.

## Отрицательные / стоимость

- потребуется scheduler/plan compiler;
- module descriptors сложнее простого `nn.Module.forward`;
- stateful modules должны поддерживать staged/rollback-like semantics;
- dynamic recursive cognition нельзя реализовать произвольными peer calls;
- failure/retry semantics нужно формализовать;
- batch divergence потребует masks/split planning.

---

# 8. Что решение намеренно не определяет

ADR не выбирает:

- `graphlib` или NetworkX как обязательную graph library;
- `asyncio.TaskGroup` как обязательный parallel runtime;
- concrete `ModuleProtocol` Python type;
- exact lifecycle hook signatures;
- concrete `ModuleDescriptor` schema;
- exact state-update container;
- private-state transaction implementation;
- scheduler performance/resource policy;
- exact Executive Control integration;
- exact learning/checkpoint APIs;
- module-specific graph edges.

---

# 9. Обязательные consistency updates

После принятия ADR должны быть согласованы:

- `docs/design/module-lifecycle.md`;
- `docs/design/system-context.md` — ownership Cognitive Scheduler;
- `docs/design/README.md`;
- `docs/design/decisions/README.md`;
- `docs/design/glossary.md`;
- `docs/design/current.md`;
- `AGENTS.md`.

Exact machine-facing contract пока не фиксируется: semantic protocol должен сначала пройти последующие module design pressure tests до version freeze.
