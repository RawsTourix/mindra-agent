# Каноническая семантика CognitiveState MINDRA

## Статус документа

**Design Update:** `DU-04 — CognitiveState Semantics`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет семантику канонического опубликованного внутреннего состояния MINDRA поверх:

- [`system-context.md`](system-context.md) — логических границ системы;
- [`dependency-rules.md`](dependency-rules.md) — правил зависимостей и композиции;
- [`execution-model.md`](execution-model.md) — причинной временной модели.

Документ намеренно **не** определяет:

- конкретный Python-класс;
- `TensorDict`, `dataclass`, `Pydantic`, `TypedDict` или другой framework;
- точные tensor dimensions;
- конкретные `dtype`;
- точный `ModuleProtocol`;
- runtime scheduler;
- точные `in_keys`/`out_keys` будущих модулей;
- точный wire/checkpoint format;
- observability/intervention API;
- конкретную стратегию копирования/structural sharing.

Эти решения принимаются только после стабилизации соответствующих последующих Design Updates.

---

# 1. Цель DU-04

`DU-03` определил, **когда** происходят причинно значимые изменения MINDRA.

`DU-04` отвечает на следующий вопрос:

> что именно считается каноническим общим внутренним состоянием агента в некоторый committed момент и как это состояние может безопасно изменяться?

После принятия `DU-04` должно быть однозначно понятно:

- чем `CognitiveState` отличается от полного `Agent-owned state`;
- что является committed state snapshot;
- кто имеет право публиковать конкретное состояние;
- как предотвращается скрытая cross-module mutation;
- как различаются `available`, `unknown`, `stale`, `unavailable` и `missing`;
- как значение связывается с logical time и provenance;
- как state scopes соотносятся с Cognitive Cycle, Decision Window, Episode и Agent Session;
- как отделяются observed/derived/predicted/retrieved/intervened данные;
- как state может быть клонирован и разветвлён для counterfactual experiments;
- почему batching/device/dtype не должны определять semantic identity;
- какие данные принципиально не должны попадать в `CognitiveState`.

---

# 2. Главное архитектурное решение

MINDRA принимает **версионированный committed CognitiveState со snapshot-семантикой и owner-scoped staged updates**.

Каноническая модель:

```text
Committed State Rn
        │
        ├── read-only inputs для вычислений
        │
        └── модули/границы формируют proposed updates
                         │
                         ▼
                  validation / commit
                         │
                         ▼
                 Committed State Rn+1
```

Ключевой invariant:

> Уже committed `CognitiveState` не изменяется задним числом.

Любое семантически видимое изменение создаёт новую state revision на соответствующей commit boundary.

Точная granularity commit определяется `DU-05 — Module Protocol & Scheduling`.

Это решение дополнительно зафиксировано в `ADR-0004`.

---

# 3. CognitiveState не равен полному состоянию Agent

`Agent-owned state` является более широким понятием.

Conceptually:

```text
Agent-owned state
├── CognitiveState
│   └── каноническое опубликованное runtime state
├── module-private state
├── trainable parameters
├── active Memory storage
├── Cortex-private/backend state
├── RNG / stochastic state
└── другое явно объявленное causally relevant state
```

## 3.1. Назначение CognitiveState

`CognitiveState` — это **каноническая shared-state поверхность**, через которую будущие когнитивные компоненты смогут обмениваться опубликованными значениями по явным contracts.

Он не должен становиться контейнером всех Python-объектов Agent.

## 3.2. Почему это важно

Если считать `CognitiveState` полным состоянием всего Agent, в него пришлось бы помещать:

- гигантское содержимое Memory;
- optimizer state;
- model weights;
- Cortex KV/cache;
- live backend clients;
- storage handles;
- внутренние cache конкретных implementations.

Это разрушило бы backend isolation и сделало бы shared state техническим dump, а не архитектурным контрактом.

## 3.3. Полный Agent Snapshot

Полный snapshot для restore/counterfactual обязан позднее учитывать **всё causally relevant agent-owned state**, а не только `CognitiveState`.

Точная snapshot/checkpoint schema относится к `DU-27`.

---

# 4. Committed snapshot semantics

## 4.1. Read-only по смыслу

Потребитель получает логически неизменяемый committed snapshot.

Недопустимо:

```text
получить ссылку на shared tensor
→ изменить tensor inplace
→ тем самым задним числом изменить State Rn
```

Даже если concrete container технически mutable, implementation обязана сохранять **semantic immutability**.

## 4.2. Implementation freedom

Semantic immutability не требует полного deep copy на каждом commit.

Допустимы будущие оптимизации:

- structural sharing;
- copy-on-write;
- immutable/frozen container;
- versioned buffers;
- preallocated storage с безопасными views;
- другие механизмы,

если внешне сохраняются принятые snapshot semantics.

## 4.3. Частичные записи невидимы

Потребитель не должен видеть состояние вида:

```text
world обновлён
self ещё старый
metadata уже новая
commit ещё не завершён
```

если такое частичное состояние не объявлено отдельной канонической phase/commit boundary будущим scheduler design.

---

# 5. State revision и lineage

Каждый committed snapshot должен иметь логическую идентичность.

На semantic уровне требуется различать:

- schema revision;
- state revision;
- temporal position из `DU-03`;
- Agent revision;
- lineage/parent relation при clone/fork.

## 5.1. State revision

`state_revision` представляет последовательность committed состояний внутри одной causal lineage.

Она не обязана совпадать с:

- `cognitive_cycle_id`;
- `environment_transition_id`;
- `learning_update_id`;
- wall-clock timestamp.

Одна временная единица может включать несколько state commits или ни одного — точная scheduling semantics определяется позднее.

## 5.2. Parent relation

Новый snapshot должен быть связан с base/parent revision, из которой он получен.

Это позволяет отличать:

```text
Rn → Rn+1
```

от counterfactual fork:

```text
        ┌→ Branch A / Rn+1a
Rn ─────┤
        └→ Branch B / Rn+1b
```

## 5.3. Agent revision

Committed state должен позволять установить, какая `agent_revision` — набор causally relevant trainable/behavioral parameters — использовалась при его формировании.

Если `Learning Update` изменил Agent revision, последующее cognition не должно неявно продолжаться под старой provenance.

Точная связь Learning Update и state commit уточняется в `DU-26`.

---

# 6. State envelope и cognitive payload

На semantic уровне `CognitiveState` состоит из двух разных классов информации.

## 6.1. State envelope

Envelope содержит control/provenance metadata, необходимую для корректной интерпретации snapshot, например conceptually:

```text
schema revision
state revision
parent/lineage
logical temporal identities
agent revision
execution/evaluation mode metadata, если разрешено contract
```

Envelope **не является автоматически cognitive input**.

Например, наличие `experiment_id`, `run_id` или названия ablation не даёт Policy права использовать эти значения при выборе действия.

## 6.2. Cognitive payload

Payload содержит contract-defined значения, которые являются частью опубликованного внутреннего состояния Agent и могут быть доступны будущим модулям по declared read dependencies.

## 6.3. Разделение предотвращает leakage

Research/control metadata должна оставаться provenance, а не незаметно становиться feature vector Agent.

Это продолжает isolation rules из `DU-01`.

---

# 7. Namespaces

Cognitive payload организуется в **стабильные семантические namespaces**.

Точные namespaces будущих модулей будут определяться соответствующими Design Updates.

Conceptual examples:

```text
observation.*
perception.*
goal.*
world.*
self.*
drive.*
appraisal.*
...
```

Эти примеры не фиксируют окончательные ключи.

## 7.1. Namespace отражает meaning, а не backend

Запрещены canonical paths вида:

```text
qwen.hidden.17
faiss.index_result
cuda0.cache
```

если они представляют private детали concrete implementation.

## 7.2. Dynamic ad-hoc keys запрещены

Модуль не должен произвольно создавать новый shared key в runtime только потому, что это удобно.

Поле должно быть частью active state schema/contract текущей композиции.

Это позволяет:

- обнаруживать typo;
- проверять ownership;
- версионировать schema;
- строить architecture tests;
- гарантировать replay compatibility.

---

# 8. Ownership и write authority

Каждый canonical field/namespace должен иметь **однозначного semantic owner**.

Owner определяет:

- смысл значения;
- допустимые способы его публикации;
- lifecycle/scope;
- availability semantics;
- schema evolution этого поля.

## 8.1. Single-writer semantic ownership

По умолчанию конкретный canonical path имеет одного write authority.

Другие компоненты могут читать его через будущий contract, но не мутируют напрямую.

## 8.2. Multi-source aggregation

Если итоговое значение должно объединять данные нескольких producers, оно обязано иметь отдельного владельца/reducer boundary.

Недопустимо:

```text
Module A пишет score
Module B пишет тот же score
последний write случайно победил
```

`last-write-wins` не является допустимой default semantics MINDRA.

## 8.3. Environment не пишет CognitiveState напрямую

Environment является external source.

Contract-defined observation сначала пересекает Agent boundary, после чего ingress responsibility публикует его в agent-owned state с provenance источника.

Точный ingress lifecycle относится к `DU-05`/`DU-07`.

## 8.4. Intervention не меняет ownership

Будущий evaluator intervention может временно override значение через специальный channel, но semantic owner поля от этого не меняется.

Override должен иметь отдельную intervention provenance.

Точная semantics относится к `DU-06`.

---

# 9. Read semantics

Будущий module contract должен явно объявлять, какие canonical fields компонент читает.

Канонический принцип:

> Наличие значения в общем state не означает, что любой модуль имеет право молча начать от него зависеть.

Это защищает архитектуру от hidden coupling.

## 9.1. Read projection

Implementation может передавать модулю весь snapshot или только projection необходимых fields.

Архитектурно значимо лишь то, что dependency объявлена contract.

## 9.2. Retained references

Потребитель не должен сохранять mutable reference на canonical value и позднее менять его вне commit semantics.

Если модулю нужна локальная рабочая копия, она становится module-private/ephemeral state.

---

# 10. Proposed update и commit

Модуль/граница не изменяет committed state напрямую.

Conceptually вычисление создаёт **proposed update** относительно конкретной base revision.

Update должен позволять установить как минимум:

- base state revision;
- producer/owner identity;
- изменяемые paths;
- новые values/availability states;
- temporal provenance;
- source dependencies/lineage настолько, насколько требует contract.

## 10.1. Commit validation

Перед публикацией update должны быть проверены:

- write authority;
- schema compatibility;
- base revision compatibility;
- value/shape semantic contract;
- temporal validity;
- conflicts с другими staged updates.

Точный coordinator/scheduler проектируется в `DU-05`.

## 10.2. Stale-base update

Если update вычислен из revision, которая уже перестала быть допустимой base, его нельзя молча применить как будто ничего не произошло.

Future scheduler должен либо:

- отвергнуть update;
- пересчитать его;
- применить явную разрешённую rebase semantics,

но не скрывать causal mismatch.

## 10.3. Atomicity

Один accepted update/commit создаёт состояние, которое наблюдается как согласованное целое.

Точная granularity atomic commit определяется `DU-05`.

---

# 11. Availability semantics

MINDRA запрещает смешивать разные причины отсутствия корректного значения.

Минимально различаются следующие состояния.

## 11.1. `available`

Поле имеет значение, которое contract считает допустимым и актуальным для текущего temporal context.

## 11.2. `unknown`

Поле семантически применимо, но Agent **не знает/не оценил** значение.

`unknown` является валидным состоянием знания, а не ошибкой.

Пример:

```text
вероятность успеха пока не оценена
```

## 11.3. `stale`

Существует ранее вычисленное значение, но его validity horizon уже не покрывает текущий causal context.

Stale value может сохраняться для диагностики, однако потребитель не должен использовать его как fresh без явного разрешения contract.

## 11.4. `unavailable`

Поле/способность в текущей composition/phase намеренно недоступны.

Причины могут включать:

- модуль отключён;
- capability отсутствует;
- поле не применимо в текущем режиме;
- значение ещё не должно существовать на этой temporal phase.

Точная reason taxonomy определяется позже.

## 11.5. `missing`

`missing` **не является нормальным значением поля**.

Это структурная ситуация, когда required contract ожидает path/value, но его нет.

По умолчанию это contract/initialization error, а не синоним `unknown`.

---

# 12. Запрет magic sentinels

Нельзя универсально кодировать отсутствие знания как:

```text
0
-1
NaN
None
empty tensor
empty string
```

если это не является явно определённой semantic representation конкретного contract.

Например, `0.0` может быть реальной оценкой и не должна означать `unknown`.

Exact representation availability mask/status будет определена позже.

---

# 13. Batch-aware availability

Если implementation векторизует несколько Agent Sessions/Environment instances, availability может различаться между элементами batch.

Следовательно, semantic model должна допускать per-element availability/mask там, где это требуется.

Пример:

```text
batch item 0: available
batch item 1: unknown
batch item 2: stale
```

Нельзя предполагать, что один global `has_value=True` корректен для всего batch.

---

# 14. Origin и provenance данных

Каждое causally relevant published значение должно иметь достаточную provenance, чтобы определить **откуда оно взялось**.

Типичные происхождения могут включать:

- external observation;
- initialization;
- derived computation;
- prediction;
- Memory retrieval;
- replay-derived computation;
- imagined/counterfactual computation;
- controlled intervention.

Это не обязательно единый enum на каждом tensor; exact encoding выбирается позднее.

## 14.1. Observed ≠ predicted

Предсказанное значение не должно перезаписывать observed fact так, чтобы downstream consumer не мог отличить одно от другого.

Conceptually:

```text
observed world state
≠
predicted future world state
```

## 14.2. Retrieved ≠ observed

Воспоминание или retrieval result не становится текущим внешним observation только потому, что оно попало в shared state.

## 14.3. Intervention provenance

Значение, принудительно установленное evaluator, должно отличаться от значения, которое естественно произвёл semantic owner.

Это необходимо для causal experiments.

---

# 15. Freshness и temporal validity

Каждый field contract должен определять, **к какому causal context относится значение**.

Полезные concept-понятия:

- produced-at;
- based-on state revision;
- validity scope/horizon;
- current/stale status.

Например, prediction, вычисленный до нового Environment outcome, может стать stale после `Outcome Commit`.

Точные freshness rules определяются соответствующим module design.

---

# 16. State scopes

Поверх temporal model `DU-03` вводятся semantic scopes опубликованного state:

```text
cycle-scoped
decision-scoped
episode-scoped
session-scoped
agent-long-lived
```

## 16.1. Cycle-scoped

Не должен автоматически переноситься за границу соответствующего Cognitive Cycle.

## 16.2. Decision-scoped

Живёт внутри текущего Decision Window и истекает при переходе к следующему decision.

## 16.3. Episode-scoped

Может сохраняться между decisions одного Episode, но не переносится в новый Episode без явной transformation/initialization semantics.

## 16.4. Session-scoped

Переживает `Environment.reset()` и несколько Episode текущей Agent Session.

## 16.5. Agent-long-lived

Conceptually относится к более долговечному состоянию Agent и может быть восстановлено между sessions через future persistence/checkpoint mechanism.

Точный список таких fields определят последующие module designs.

---

# 17. Scope не равен storage duration и checkpoint policy

Важно различать три вещи:

```text
semantic lifetime
≠
historical retention
≠
checkpoint inclusion
```

Cycle-scoped значение может быть сохранено в trajectory artifact навсегда для анализа.

Session-scoped значение может быть включено в emergency checkpoint для exact resume.

Agent-long-lived значение не обязано физически находиться на диске в каждый момент.

Checkpoint policy определяется отдельно в `DU-27`.

---

# 18. Expiration/reset semantics

На завершении scope значение не должно молча продолжать считаться fresh.

Future lifecycle может:

- удалить optional field из current view;
- перевести его в `unavailable`;
- создать новое initialized значение;
- опубликовать новую revision без прежнего field,

в зависимости от exact contract.

Но недопустимо неявно переносить старое значение только потому, что container его не очистил.

Точный reset ordering относится к `DU-05`.

---

# 19. Module-private state

Не всё causally relevant состояние обязано публиковаться в `CognitiveState`.

Допустимы module-private states, если их ownership ясен.

Примеры потенциально private:

- recurrent hidden state конкретного backend;
- Cortex KV/cache;
- internal Memory index/cache;
- temporary planning search tree;
- implementation-specific optimizer-free runtime buffers.

## 19.1. Causally relevant private state нельзя скрывать

Если private state способен изменить будущие outputs, будущий `ModuleProtocol`/snapshot design должен описать как минимум:

- его owner;
- lifecycle/scope;
- reset semantics;
- snapshot/restore requirements;
- observability requirements там, где это нужно research design.

Нельзя называть behavior-changing state «просто cache», чтобы исключить его из reproducibility.

## 19.2. Pure cache

Если cache полностью детерминированно восстанавливается из canonical/declared state и его удаление не меняет semantics, он может считаться operational optimization и не входить в causal snapshot.

---

# 20. Cortex/model-specific hidden state isolation

Concrete Cortex hidden tensors не являются canonical CognitiveState только потому, что доступны backend.

Запрещено протаскивать по shared state model-specific детали вида:

```text
hidden layer 17 tensor конкретной Qwen
provider request object
KV-cache handle
CUDA-specific model state
```

если downstream архитектуре нужна semantic capability, должен существовать future canonical adapter/representation boundary из `DU-08`/`DU-10`.

Private Cortex state остаётся за Cortex boundary и учитывается в full Agent snapshot настолько, насколько он causally relevant.

---

# 21. Active Memory и CognitiveState

Active Memory логически принадлежит Agent, но её полный storage не обязан находиться внутри CognitiveState.

В CognitiveState позднее могут публиковаться, например:

- retrieval request context;
- selected memory references;
- retrieved representations;
- summaries;
- memory-related metrics/state,

если это будет принято `DU-11`/`DU-20`.

Но сам memory store остаётся отдельным owned subsystem state.

---

# 22. Batch semantics

Canonical CognitiveState описывает **одну причинную state lineage**.

Batching — implementation/vectorization mechanism.

Если несколько independent Agent Sessions упакованы в один tensor container, каждая сохраняет собственные:

- temporal identities;
- state revision/lineage;
- availability;
- provenance.

Batch completion order не создаёт общий causal order между независимыми sessions.

Это продолжает `DU-03`.

---

# 23. Device independence

Physical device не является частью semantic identity CognitiveState.

Conceptually эквивалентные representations на:

```text
CPU
GPU 0
GPU 1
remote device
```

представляют одно semantic state, если значения и contract-equivalent meaning сохранены.

Обычный перенос data между devices сам по себе не должен создавать новую cognitive state revision.

Device placement относится к runtime/compute metadata.

---

# 24. Dtype и precision

Concrete `dtype` также не должен становиться смыслом поля по умолчанию.

Field contract определяет semantic domain/precision requirements, а implementation выбирает допустимое concrete representation.

При этом precision mode важен для reproducibility и должен быть частью future execution provenance.

Если conversion фактически меняет semantic value за пределами допустимого tolerance, это уже не просто transport operation.

---

# 25. Feature shape и batch shape

Future representation должна различать:

```text
batch axes
≠
semantic feature axes
```

Например, latent vector длины `D` не должен терять meaning при добавлении batch dimension `B`.

Точные dimensions будут определены только там, где это требуется конкретным module design.

---

# 26. Serialization requirements

CognitiveState должен быть conceptually сериализуемым без зависимости от live process objects.

Canonical payload/envelope не должны требовать сохранения:

- открытых файлов;
- network sockets;
- coroutine/future objects;
- thread locks;
- provider clients;
- `nn.Module` instances;
- optimizer objects;
- arbitrary Python closures.

Допустимы stable references/identifiers на внешний owned storage, если их semantics и restore path явно определены.

## 26.1. Schema revision

Serialized state должен позволять определить schema revision и обнаружить несовместимость.

Schema migration policy определяется позже.

## 26.2. CognitiveState serialization ≠ Agent checkpoint

Сериализация shared state не является достаточным checkpoint всего Agent.

Полный checkpoint должен дополнительно учитывать private state, parameters, Memory, stochastic state и другие causally relevant компоненты.

---

# 27. Clone и counterfactual fork

Committed snapshot должен поддерживать semantic clone/fork.

## 27.1. Clone

Clone начинается из конкретной committed revision и не меняет исходный snapshot.

Copy-on-write допускается как implementation optimization.

## 27.2. Fork lineage

Counterfactual branch должен сохранять связь с parent revision.

Conceptually:

```text
base R42
├── branch A: natural continuation
└── branch B: controlled state intervention
```

## 27.3. CognitiveState clone недостаточен для полного Agent clone

Если private Memory/Cortex/RNG/module state влияет на поведение, для корректного counterfactual необходимо клонировать и его.

Также для полного world counterfactual требуется совместимый Environment clone/restore из `DU-07`.

Точный intervention/fork API относится к `DU-06`.

---

# 28. Learning Updates и CognitiveState

Trainable parameters не обязаны находиться в CognitiveState.

Но state snapshot должен позволять определить, под какой `agent_revision` он сформирован.

После Learning Update нельзя допускать ситуацию, где downstream computation считает себя продолжением старой revision без явной causal boundary.

Точный training/state synchronization protocol определяется в `DU-26`.

---

# 29. Schema evolution

State schema является частью canonical internal contract и не должна зависеть от случайного порядка runtime writes.

Future schema должна поддерживать:

- stable field paths;
- declared owners;
- declared scopes;
- availability semantics;
- semantic type/shape constraints;
- versioning;
- compatibility validation.

Field rename/removal/meaning change считается contract evolution, а не обычным refactor без последствий.

---

# 30. Control/debug metadata не является CognitiveState

Observability data вроде:

- profiler timings;
- raw debug dumps;
- experiment labels;
- evaluator scores;
- trace IDs, не нужные cognitive semantics;
- logger internal state

не должны автоматически помещаться в cognitive payload.

Они могут сопровождать state как external observability/evidence metadata.

Точная boundary проектируется в `DU-06`.

---

# 31. Research evidence и существующие реализации

`DU-04` не выбирает concrete state framework, но существующие инструменты подтверждают реализуемость требований.

## 31.1. TensorDict как пример nested/batched state container

Актуальный `TensorDict` поддерживает nested keys, явный batch size, device movement и `clone()`.

Источник:

- https://docs.pytorch.org/tensordict/stable/reference/generated/tensordict.TensorDict.html

Это показывает, что hierarchical namespaces и batch/device-aware representation не требуют разработки контейнера с нуля.

## 31.2. Serialization

TensorDict предоставляет `state_dict()`/`load_state_dict()` с metadata для nested state.

Источник:

- https://docs.pytorch.org/tensordict/stable/saving.html

## 31.3. Frozen/locked representations

`TensorClass`/`TypedTensorDict` поддерживают frozen semantics, а TensorDict имеет locking mechanisms.

Источники:

- https://docs.pytorch.org/tensordict/stable/reference/generated/tensordict.TensorClass.html
- https://docs.pytorch.org/tensordict/stable/reference/ttd.html

Это не означает, что любой из этих механизмов автоматически удовлетворяет semantic immutability MINDRA: например, container lock может не запрещать все inplace mutations вложенных tensor storage.

Следовательно, конкретный framework будет оцениваться позже по полному набору требований этого документа.

---

# 32. Принятые invariants DU-04

## CS-01

`CognitiveState` — каноническое опубликованное shared runtime state Agent, а не полный `Agent-owned state`.

## CS-02

Committed state snapshot семантически неизменяем.

## CS-03

Семантически видимое изменение появляется только через новую committed state revision.

## CS-04

Каждый canonical field/namespace имеет однозначного write owner.

## CS-05

`last-write-wins` не является допустимой default semantics конфликтующих canonical writes.

## CS-06

Consumer читает только declared dependencies и не должен неявно зависеть от произвольных присутствующих fields.

## CS-07

`available`, `unknown`, `stale`, `unavailable` и structural `missing` имеют разные значения.

## CS-08

Magic sentinel не заменяет явную availability semantics.

## CS-09

Published value должно иметь достаточную temporal/provenance information для причинной интерпретации.

## CS-10

Observed, predicted, retrieved и intervened information не должны становиться неразличимыми.

## CS-11

Каждый published field имеет semantic lifetime/scope.

## CS-12

Semantic scope, historical retention и checkpoint policy являются разными понятиями.

## CS-13

Causally relevant module-private state должно быть явно объявлено и позднее поддерживать необходимые snapshot/restore semantics.

## CS-14

Model/backend-specific hidden objects не протекают в canonical state без adapter/semantic boundary.

## CS-15

Batching является representation optimization и не объединяет causal lineages независимых sessions.

## CS-16

Device placement не определяет semantic identity state.

## CS-17

CognitiveState должен быть conceptually serializable без live infrastructure objects.

## CS-18

Counterfactual fork начинается только из identifiable committed revision и сохраняет lineage.

## CS-19

Clone одного `CognitiveState` не считается полным clone Agent, если существует другое causally relevant owned state.

## CS-20

Evaluation/debug metadata не становится cognitive payload без явного semantic contract.

---

# 33. Что DU-04 намеренно не решает

Открытыми остаются:

- concrete container/framework;
- exact field names;
- exact schemas будущих modules;
- exact tensor shapes/dtypes;
- concrete availability encoding;
- update/patch Python type;
- exact state coordinator;
- scheduling/commit granularity;
- module lifecycle;
- read/write API;
- intervention API;
- environment ingress API;
- exact snapshot/checkpoint format;
- schema migration tooling;
- concrete copy-on-write/immutability mechanism;
- performance optimization strategy.

Эти вопросы не должны решаться implementation раньше соответствующих Design Updates/version planning.

---

# 34. Последствия для следующих Design Updates

## DU-05 — Module Protocol & Scheduling

Должен определить:

- как модуль объявляет read/write dependencies;
- как получает committed snapshot/projection;
- как формирует proposed update;
- кто валидирует/commit updates;
- commit granularity;
- conflict/stale-base handling;
- lifecycle reset относительно state scopes;
- scheduling без partial-state leakage.

## DU-06 — Observability & Intervention

Должен определить:

- как наблюдать snapshots/updates/provenance;
- как выполнить override, не меняя semantic ownership;
- как клонировать/fork lineage;
- как не допустить debug/evaluator metadata leakage.

## DU-08 — Perception

Должен определить canonical representation, публикуемую вместо raw backend-specific tensors.

## DU-10 — Cortex

Должен отделить Cortex-private state от canonical published representations.

## DU-11/DU-20 — Memory

Должны определить, что остаётся private Memory storage, а что публикуется в CognitiveState.

## DU-25 — Experience/Data

Должен зафиксировать, какие state revisions/updates входят в trajectory evidence.

## DU-27 — Checkpoint/Reproducibility

Должен определить полный `Agent Snapshot`, включающий CognitiveState и другое causally relevant state.

---

# 35. Completion gate DU-04

`DU-04` считается завершённым, если для любого будущего state value можно ответить:

1. **Является ли оно canonical shared state или private/internal state?**
2. **Кто владеет его semantic write authority?**
3. **Из какой committed revision и causal context оно получено?**
4. **Каков его availability/freshness status?**
5. **Каков его semantic lifetime?**
6. **Можно ли отличить его origin от observation/prediction/retrieval/intervention?**
7. **Может ли оно быть сериализовано/клонировано без hidden live object dependency?**

После принятия этого документа следующий допустимый Design Update:

```text
DU-05 — Module Protocol & Scheduling
```
