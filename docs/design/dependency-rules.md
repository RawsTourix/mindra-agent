# Правила зависимостей и композиции MINDRA

## Статус документа

**Design Update:** `DU-02 — Dependency & Composition Rules`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет правила зависимостей, композиции и подмены компонентов MINDRA поверх логических границ, принятых в [`system-context.md`](system-context.md).

Документ намеренно **не** определяет:

- окончательную структуру Python-пакетов и каталогов;
- конкретный DI-framework;
- точную форму `CognitiveState`;
- точный `ModuleProtocol`;
- runtime scheduler;
- конкретный plugin framework;
- конкретные neural/RL библиотеки;
- точные interfaces когнитивных модулей;
- конкретную конфигурационную библиотеку.

Эти решения принимаются только там, где они действительно становятся необходимыми последующим Design Updates или implementation planning.

---

# 1. Цель DU-02

`DU-01` определил **кому логически принадлежат** Agent, Environment, Cortex, Training Runtime, Evaluation Runtime и инфраструктурные компоненты.

`DU-02` отвечает на следующий вопрос:

> каким образом эти компоненты и будущие модули могут зависеть друг от друга, не разрушая модульность, заменяемость и исследовательскую диагностируемость?

После принятия `DU-02` должно быть возможно:

- нарисовать разрешённый dependency graph;
- отличить semantic dependency от concrete implementation dependency;
- определить, где разрешено знание о concrete backend;
- подменить реализацию без переписывания независимых потребителей;
- исключить hidden Service Locator и global mutable state;
- отделить composition/bootstrap от cognition;
- не допустить зависимости Agent runtime от Training/Evaluation Runtime;
- подготовить будущие architecture tests для проверки import boundaries.

---

# 2. Главный принцип

MINDRA использует следующий dependency invariant:

```text
behavioral component
        ↓ depends on
stable semantic contract / canonical data boundary
        ↑ implemented by
concrete implementation / adapter / backend
```

Высокоуровневая когнитивная логика не должна зависеть от конкретного способа реализации capability, если эта зависимость может быть выражена через стабильный контракт.

В частности:

```text
Policy ─X─→ Qwen implementation
World Model ─X─→ FAISS backend
Memory ─X─→ конкретный vector DB client
Agent ─X─→ Evaluation Runtime
Agent ─X─→ Training Runtime
```

Вместо этого concrete implementations подключаются через **composition boundary**.

---

# 3. Dependency graph и runtime feedback — разные вещи

MINDRA неизбежно будет содержать временные feedback loops:

```text
Memory
  ↓
Decision
  ↓
Action
  ↓
Outcome
  ↓
Memory
```

Это **не** означает, что Python/import/object dependency graph должен быть циклическим.

Канонический invariant:

> Runtime feedback разрешён через состояние, события и scheduler semantics; hidden static dependency cycles между concrete implementations запрещены.

Следовательно:

```text
runtime dataflow cycle
≠
import cycle
≠
mutual object ownership
```

`DU-03`–`DU-05` определят временную модель, `CognitiveState` и scheduling. `DU-02` только запрещает маскировать будущие feedback loops прямыми взаимными ссылками concrete modules.

---

# 4. Семантические слои зависимостей

До окончательной структуры `src/` принимается следующая **логическая**, а не файловая модель слоёв.

```text
┌─────────────────────────────────────────────┐
│ Entry points / Composition Root             │
│ run / train / evaluate / research bootstrap │
└─────────────────────┬───────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│ Runtime / Training / Evaluation orchestration│
└─────────────────────┬───────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│ Agent composition + cognitive modules       │
└─────────────────────┬───────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│ Semantic contracts / shared value objects   │
└─────────────────────────────────────────────┘

Concrete providers/adapters реализуют contracts
и подключаются сверху через composition boundary.
```

Эта схема не требует именно четырёх Python packages. Она фиксирует только направление знания.

---

# 5. Семантические contracts — нижняя граница

Общие contracts/value objects должны быть максимально независимыми от concrete implementations.

Они не должны без необходимости зависеть от:

- конкретной LLM;
- конкретного storage backend;
- `Experiment Runner`;
- evaluator implementation;
- training loop;
- notebook/Colab;
- provider SDK;
- concrete environment implementation;
- concrete cognitive module implementation.

Будущие exact contracts появятся после стабилизации semantic design соответствующих областей.

До этого момента `DU-02` не создаёт пустые интерфейсы только ради формальной абстракции.

---

# 6. Composition Root

MINDRA принимает явный **Composition Root** как единственную область, где допустимо знание о полном наборе concrete implementations, необходимом для конкретного запуска.

Composition Root conceptually отвечает за:

1. чтение уже валидированной run/configuration intent;
2. разрешение symbolic implementation identifiers;
3. создание concrete providers/adapters/modules;
4. проверку совместимости заявленных capabilities/contracts;
5. передачу зависимостей потребителям;
6. построение Agent/runtime/evaluation composition для выбранного режима;
7. fail-fast при невозможной или неоднозначной композиции.

Composition Root **не** является когнитивным модулем и не принимает решения за Agent.

---

# 7. Один принцип композиции, несколько entry points

Фраза `Composition Root` не требует одного физического файла или одной функции.

Допустимы разные application entry points:

```text
run
train
evaluate
research experiment
```

но они должны использовать совместимую composition semantics и не создавать независимые скрытые способы сборки Agent.

Например, недопустимо:

```text
run.py создаёт Memory одним способом
train.py вручную создаёт другую Memory
notebook.py импортирует третью concrete реализацию напрямую
```

если различия не представлены явной конфигурацией/профилем композиции.

---

# 8. Dependency Injection

Зависимости должны передаваться явно через будущие constructors/factories/protocol boundaries либо через каноническую state/data boundary там, где взаимодействие является dataflow, а не service call.

`DU-02` **не выбирает** конкретный DI-container.

Каноническое требование — не библиотека, а свойство:

> Потребитель получает уже разрешённую зависимость и не ищет её самостоятельно в глобальном окружении.

Будущая реализация может использовать обычные constructors/factories, если этого достаточно.

---

# 9. Service Locator запрещён

Когнитивные модули и runtime core не должны во время работы выполнять запросы вида:

```text
registry.get("memory")
services.resolve(Cortex)
global_container["world_model"]
```

для получения своих зависимостей.

Причины запрета:

- dependency становится скрытой;
- unit/ablation tests требуют глобальной настройки;
- модуль невозможно понять по собственному контракту;
- возрастает риск runtime cycles;
- control/no-op подмена превращается в глобальное побочное состояние;
- concrete implementation leakage становится трудно обнаружить.

Registry может существовать **только на composition/discovery boundary**, а не как runtime Service Locator для cognitive code.

---

# 10. Registry и plugin discovery

MINDRA допускает registry как каталог:

```text
symbolic id
    ↓
factory / provider descriptor
    ↓
concrete implementation
```

но только при следующих условиях:

1. registry используется composition layer;
2. модуль не обращается к registry для поиска соседей;
3. registry не хранит mutable cognitive state;
4. регистрация не меняет поведение уже собранного Agent скрыто;
5. конфликт identifiers обнаруживается явно;
6. provenance выбранной реализации попадает в experiment/config evidence.

На ранних версиях registry может быть статическим и локальным.

Внешнее plugin discovery через Python package metadata/`entry points` является допустимым будущим вариантом, но **не требуется** текущим design.

---

# 11. Contracts вместо concrete peers

Если модулю действительно требуется capability другого компонента как service dependency, он может зависеть только от стабильного semantic contract, а не от concrete class.

Например conceptually:

```text
потребитель → CortexContract ← QwenAdapter
потребитель → StorageContract ← LocalStorageAdapter
```

Однако для когнитивных модулей предпочтительным способом обмена остаётся будущая canonical state/data boundary, если зависимость выражается как состояние/representation.

Это предотвращает превращение Agent в граф взаимно вызывающих друг друга объектов.

---

# 12. Прямые зависимости между когнитивными модулями

По умолчанию cognitive module **не должен владеть concrete reference на другой cognitive module**.

Запрещён типичный pattern:

```text
Appraisal.__init__(memory: EpisodicMemory,
                   world_model: RSSMWorldModel,
                   cortex: QwenCortex)
```

если нужные данные могут быть опубликованы через будущий `CognitiveState`/scheduler contract.

Исключение возможно только если будущий design докажет, что:

1. взаимодействие является самостоятельной capability, а не dataflow;
2. contract стабилен;
3. ownership остаётся однозначным;
4. это не создаёт cycle;
5. зависимость нужна для исследовательской семантики, а не для удобства реализации.

Такое исключение должно быть явно зафиксировано в canonical module design.

---

# 13. Shared mutable state запрещён

Будущая реализация не должна использовать неявное общее изменяемое состояние как средство связи модулей:

- module-level mutable globals;
- singleton с cognitive variables;
- process-global cache, влияющий на cognition без контракта;
- общий dictionary, который произвольные модули меняют без ownership rules;
- глобальный config object, который модуль читает в любой момент runtime.

Каноническое состояние и правила владения будут спроектированы в `DU-04`.

До этого момента `DU-02` фиксирует только запрет обходить будущую state boundary через globals.

---

# 14. Configuration не является зависимостью-сервисом

Конфигурация описывает **намерение сборки и параметры**, но не должна использоваться как глобальный Service Locator.

Предпочтительная семантика:

```text
raw config
   ↓
validate / resolve
   ↓
Composition Root
   ↓
constructed components with local immutable/resolved settings
```

Модуль не должен самостоятельно искать в глобальной конфигурации:

- какой backend ему вызвать;
- какой соседний модуль существует;
- какой evaluator активен;
- как называется текущая ablation;
- какие test-only параметры доступны.

Это одновременно предотвращает experiment leakage из `DU-01`.

---

# 15. Concrete provider/adapters

Любая внешняя или backend-specific технология должна быть изолирована adapter/provider boundary настолько, насколько это practically обосновано.

Кандидатные примеры:

- конкретная LLM/Cortex library;
- remote inference SDK;
- vector database;
- object storage;
- experiment tracker;
- environment framework;
- checkpoint backend.

Concrete adapter может импортировать стороннюю библиотеку.

Независимый cognitive/core code не должен импортировать SDK этой реализации только ради доступа к capability.

---

# 16. Cortex backend isolation

Поверх `SC-03` принимаются дополнительные dependency invariants.

Независимые компоненты MINDRA не должны зависеть от:

- concrete Cortex class;
- tokenizer class конкретной модели;
- provider SDK;
- model-specific generation object;
- model-specific hidden-state container;
- фиксированного `hidden_size`;
- конкретного device placement;
- конкретной quantization library.

Эти детали принадлежат concrete Cortex implementation/adapter и будущему `DU-10`.

Если model-specific representations должны пересечь Cortex boundary, `DU-10` обязан явно определить adapter/canonicalization semantics.

---

# 17. Environment isolation

Agent и cognitive modules не должны зависеть от concrete MicroWorld/Gymnasium-like implementation.

Environment concrete implementation может зависеть от будущего Environment contract и собственных библиотек, но:

```text
Agent core ─X─→ concrete environment
Environment ─X─→ Agent internals
```

Обмен выполняется только через будущую Environment boundary из `DU-07`.

---

# 18. Runtime не знает concrete cognition без необходимости

`Execution Runtime` должен оркестрировать уже собранный Agent через стабильную runtime boundary.

Runtime core не должен содержать ветвления вида:

```text
if isinstance(module, SpecificMemory): ...
if cortex_name == "qwen": ...
```

для нормальной execution semantics.

Backend-specific bootstrap может существовать в composition/adapter layer, но не должен проникать в общий execution loop.

---

# 19. Agent не зависит от Training Runtime

Поверх `SC-05` принимается статическое dependency rule:

> Agent runtime/core code не импортирует Training Runtime и не требует trainer/optimizer для normal execution.

Training Runtime может зависеть от:

- agent/module training contracts;
- trainable parameter surfaces;
- experience/data contracts;
- checkpoint/update contracts,

когда они появятся.

Направление знания:

```text
Training Runtime
      ↓
public training/update boundary
      ↓
Agent-owned trainable state
```

но не наоборот.

---

# 20. Agent не зависит от Evaluation Runtime

Поверх `SC-06` принимается статическое dependency rule:

```text
Evaluation Runtime → evaluation/observability contracts → Agent
Agent ─X─→ Evaluation Runtime
```

Agent не импортирует:

- evaluator;
- benchmark implementation;
- test labels;
- metric calculators, если они существуют только для external evaluation;
- experimental condition logic.

Вмешательства `DU-06` будут предоставляться через отдельную явную boundary, а не через обратную runtime dependency.

---

# 21. Training и Evaluation не должны владеть cognitive semantics

Training/Evaluation infrastructure может знать, **как обучать или измерять** объявленную capability, но не должна тайно определять её meaning.

Например:

- значение `salience` определяется canonical module design, а не тем, как evaluator решил его интерпретировать;
- `Self Model` semantics не определяются только calibration metric;
- trainer не должен добавлять скрытый field в Agent state без изменения contract/design.

Иначе design перемещается из `docs/design/` в infrastructure code.

---

# 22. Module-private state

Каждый будущий модуль должен иметь однозначного владельца private state.

Другие cognitive modules не должны:

- читать private fields напрямую;
- менять private buffers;
- получать внутренний concrete model object;
- менять cache/state через undocumented side channel.

Допустимы только:

- опубликованные outputs/state;
- будущие public contracts;
- явно разрешённая training/update boundary;
- явно разрешённая intervention boundary для research mode.

Training/Evaluation Runtime также не получают автоматического права на произвольную мутацию private state.

---

# 23. No-op, Dummy и Control implementations

Ablation/control semantics должны реализовываться **композицией**, а не scattered conditions по коду.

Предпочтительный pattern:

```text
ModuleContract
├── LearnedImplementation
├── RuleBasedImplementation
├── NoOpImplementation
├── DummyImplementation
└── ControlImplementation
```

Конкретный набор вариантов зависит от модуля.

Ключевые требования:

1. подмена происходит на composition boundary;
2. потребители не переписываются;
3. output contract остаётся валидным либо явно используется отдельный compatible control contract;
4. выбранная реализация фиксируется в experiment provenance;
5. `NoOp` не должен скрыто вызывать production implementation;
6. отсутствие модуля не должно активировать незадокументированный fallback.

---

# 24. Отключение модуля

Отключение значимого модуля должно иметь одну из явных семантик:

1. `NoOp`/identity implementation;
2. neutral/default output implementation;
3. composition profile без capability, если потребители contractually допускают её отсутствие;
4. test-specific control implementation.

Нельзя распространять по проекту:

```text
if config.disable_memory:
if config.disable_appraisal:
if config.ablation_x:
```

в независимых потребителях.

Исключение — локальная implementation detail внутри composition/runtime boundary, которая сама реализует принятую общую semantics подмены.

---

# 25. Fallback semantics

Fallback является архитектурно значимым, если способен изменить поведение Agent.

Поэтому запрещён скрытый pattern:

```text
try primary Cortex
except:
    use another Cortex
```

или:

```text
if Memory unavailable:
    silently ask Cortex again
```

если это не является явно принятым behavior mode.

Fallback должен быть:

- объявлен в composition/config;
- наблюдаем;
- отражён в provenance;
- отдельно учитываем в evaluation.

Точные failure/degradation semantics относятся к `DU-05` и соответствующим module designs.

---

# 26. Optional dependencies

Опциональная capability не должна превращать весь core package в обязательного потребителя тяжёлой библиотеки.

Conceptually:

```text
core contracts
    ↑
optional adapter package/component
    ↑
external dependency
```

Если Cortex backend требует конкретный framework/provider SDK, отсутствие этого backend не должно мешать использовать `NoCortex` или другой backend, если composition profile этого не требует.

Точная packaging strategy определяется позже.

---

# 27. Plugin discovery не равно runtime dynamism

Даже если позже используются package `entry points` или другой discovery mechanism, discovery выполняется до/во время composition.

После сборки Agent нельзя считать нормой, что произвольная установка нового Python package автоматически меняет уже выполняющуюся cognition.

Изменение implementation set должно приводить к новой явной composition/configuration identity.

---

# 28. Dependency direction для research tooling

Research tooling находится снаружи и может зависеть от публичных MINDRA contracts.

Разрешено:

```text
Experiment Runner → composition/configuration
Evaluator → evaluation/intervention contracts
Artifact Collector → observability/event contracts
Training Runtime → training/data/update contracts
```

Запрещено:

```text
Agent core → Experiment Runner
Agent core → Artifact Collector concrete backend
Agent core → evaluator implementation
Agent core → experiment tracker SDK
```

Agent может **эмитировать** diagnostic events через абстрактную boundary; конкретный collector определяется внешней композицией.

---

# 29. Dependency direction для external libraries

Сторонняя библиотека может использоваться непосредственно там, где она является implementation substrate данного компонента.

Но её типы не должны без необходимости становиться canonical cross-module contracts.

Пример общей политики:

```text
adapter implementation → external SDK       [допустимо]
canonical contract → external SDK type       [по умолчанию нет]
cognitive peer → adapter concrete class      [нет]
composition root → adapter concrete factory  [да]
```

Исключение возможно, если сторонний тип является сознательно принятым стабильным foundation contract. Такое решение требует отдельного design review/ADR, потому что создаёт долгосрочную зависимость.

---

# 30. Type contracts и structural typing

`DU-02` не фиксирует Python `Protocol` как обязательную реализацию, но считает structural/behavioral contracts подходящим кандидатом там, где важна replaceability без inheritance coupling.

Официальный Python `typing.Protocol` позволяет описывать структурные интерфейсы без требования наследоваться от конкретной базовой реализации.

Это используется как evidence практичности принятой contract-first стратегии, а не как окончательный выбор exact contract technology.

---

# 31. Plugin discovery evidence

PyPA документирует несколько стандартных способов plugin discovery, включая package metadata `entry points`.

Это подтверждает, что будущий внешний plugin ecosystem можно построить без разрешения cognitive modules самостоятельно импортировать concrete implementations.

MINDRA **не обязана** поддерживать внешние plugins в ранних версиях.

Plugin discovery рассматривается как composition concern.

---

# 32. Требования к будущей структуре исходного кода

`DU-02` не выбирает окончательные пути каталогов, но будущая структура должна позволять автоматически различить как минимум:

- semantic contracts;
- cognitive/core implementation;
- concrete providers/adapters;
- runtime orchestration;
- training infrastructure;
- evaluation/research tooling;
- application composition/bootstrap.

Если package layout делает запрещённое направление импорта естественным и незаметным, layout должен быть пересмотрен.

---

# 33. Architecture tests как обязательное следствие

Будущая engineering testing strategy должна автоматически проверять значимую часть dependency invariants.

Минимальные кандидатные проверки:

- Agent/core не импортирует training/evaluation packages;
- cognitive modules не импортируют concrete Cortex backends;
- core contracts не импортируют concrete implementations;
- concrete adapters не становятся обратными зависимостями core;
- запрещённые package-layer cycles отсутствуют;
- control/no-op implementation можно подменить через composition;
- обычный Agent execution не требует evaluator/trainer imports.

Конкретный инструмент (`import graph` checker, architecture test, linter или собственная проверка) выбирается в `DU-29`.

---

# 34. Исследовательская проверяемость композиции

Каждый meaningful experiment должен иметь возможность установить:

- какие implementations были выбраны;
- какие capabilities были disabled;
- какие control implementations использованы;
- какие provider versions подключены;
- какой composition/config hash соответствует run.

Точный experiment schema относится к `DU-25`–`DU-28`, но dependency design обязан не препятствовать такой provenance.

---

# 35. Запрещённые архитектурные shortcuts

Без отдельного будущего design запрещаются:

```text
1. global singleton с Agent/services
2. mutable global registry во время cognition
3. module → concrete peer imports
4. Agent → trainer/evaluator imports
5. runtime core → конкретная Qwen/Gemma/Llama ветка
6. cross-module доступ к private fields
7. shared mutable dict как неформальный CognitiveState
8. test condition, читаемый Agent из global config
9. hidden fallback на другой module/backend
10. notebook-specific wiring, которое становится единственным способом запуска
11. direct SDK types как случайный canonical contract
12. dynamic plugin discovery внутри cognitive step
```

---

# 36. Принятые invariants DU-02

## DC-01

Concrete implementations подключаются через явную composition boundary.

## DC-02

Composition Root является единственным логическим местом, где допустимо знание о полном наборе concrete implementations запуска.

## DC-03

Cognitive/runtime consumers получают зависимости явно и не используют глобальный Service Locator.

## DC-04

Registry допустим как composition-time каталог factories/providers, но не как runtime service lookup для cognitive modules.

## DC-05

По умолчанию cognitive modules не владеют concrete references на другие cognitive modules.

## DC-06

Runtime feedback loops не оправдывают static import/object dependency cycles.

## DC-07

Shared mutable global state запрещён как механизм межмодульной коммуникации.

## DC-08

Agent/core не зависит от Training Runtime.

## DC-09

Agent/core не зависит от Evaluation Runtime и research tooling.

## DC-10

Concrete Cortex/backend/provider details не пересекают capability boundary без явного будущего contract.

## DC-11

Environment implementation и Agent internals не зависят друг от друга напрямую.

## DC-12

Module-private state доступен другим компонентам только через объявленные public/update/intervention boundaries.

## DC-13

No-op/dummy/control implementations подключаются через composition, а не scattered feature flags.

## DC-14

Behavior-changing fallback должен быть явным, наблюдаемым и воспроизводимым.

## DC-15

Configuration описывает composition intent, но не является runtime Service Locator.

## DC-16

Сторонние SDK/framework types по умолчанию не являются canonical cross-module contracts.

## DC-17

Plugin discovery, если появится, является responsibility composition layer.

## DC-18

Будущая структура кода должна позволять автоматически проверять запрещённые dependency directions.

---

# 37. ADR DU-02

Основной выбор между:

1. direct concrete wiring;
2. global Service Locator/container;
3. explicit Composition Root + dependency inversion + optional composition-time registry

зафиксирован в:

[`ADR-0002 — Явная композиция и запрет runtime Service Locator`](decisions/ADR-0002-explicit-composition-no-runtime-service-locator.md).

---

# 38. Что DU-02 намеренно не решает

Открытыми остаются:

- точный Python package tree;
- `Protocol` vs ABC vs другой exact interface mechanism;
- concrete registry implementation;
- использовать ли package `entry points`;
- конкретный config framework;
- точный composition API;
- точная модель runtime scheduler;
- temporal ordering;
- exact `CognitiveState`;
- module lifecycle methods;
- async/process execution;
- exact observability/intervention API;
- concrete architecture-test tool.

Эти вопросы нельзя решать implementation-ом скрыто, если они влияют на последующий canonical design.

---

# 39. Последствия для следующих Design Updates

## DU-03 — Runtime / Temporal Model

Должен спроектировать временную семантику так, чтобы feedback loops реализовывались scheduler/state transitions, а не circular object calls.

## DU-04 — CognitiveState

Должен дать canonical data boundary, через которую cognitive modules смогут обмениваться опубликованным состоянием без доступа к concrete peers/private state.

## DU-05 — Module Protocol & Scheduling

Должен формализовать:

- dependency declaration;
- lifecycle;
- module registration в уже собранном Agent;
- ordering;
- disabled/control behavior;
- failure/degradation semantics.

Он не должен возвращать runtime Service Locator.

## DU-06 — Observability & Intervention

Должен предоставить evaluator доступ через отдельную диагностическую boundary, не создавая Agent → Evaluator dependency.

## DU-10 — Cortex

Должен конкретизировать capability contract и adapter boundary без model leakage.

## DU-26 — Training

Должен определить update/training contracts без обратной Agent → Training Runtime dependency.

## DU-29 — Engineering Testing

Должен сделать dependency invariants исполнимыми architecture tests.

---

# 40. Completion gate DU-02

`DU-02` считается завершённым, если для любой будущей зависимости можно ответить:

1. **Почему эта dependency семантически необходима?**
2. **Зависит ли потребитель от contract или от concrete implementation?**
3. **Кто разрешает/создаёт concrete implementation?**
4. **Можно ли подменить её без изменения независимого потребителя?**
5. **Не создаёт ли зависимость скрытый Service Locator, shared mutable state или cycle?**
6. **Не пересекает ли она границы Agent/Training/Evaluation из DU-01?**

После принятия этого документа следующий допустимый Design Update:

```text
DU-03 — Runtime / Temporal Model
```
