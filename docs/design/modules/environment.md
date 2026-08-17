# Environment и MicroWorld MINDRA

## Статус документа

**Design Update:** `DU-07 — Environment / MicroWorld Contract`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет:

- общую семантическую границу `Environment` для MINDRA;
- разделение agent-visible взаимодействия и research-only world state;
- lifecycle `reset / transition / termination / truncation`;
- требования к snapshot/restore/clone/fork;
- stochastic/RNG semantics;
- procedural generation и versioned world distributions;
- первую эталонную исследовательскую среду `MicroWorld`;
- минимальные семейства задач, необходимые для будущих модульных экспериментов.

Документ опирается на:

- [`system-context.md`](../system-context.md) — `Environment` находится вне Agent boundary;
- [`execution-model.md`](../execution-model.md) — `Environment Transition` отделён от `Cognitive Cycle`;
- [`cognitive-state.md`](../cognitive-state.md) — Environment hidden state не является `CognitiveState`;
- [`module-lifecycle.md`](../module-lifecycle.md) — Agent modules не вызывают Environment друг через друга;
- [`observability-and-intervention.md`](../observability-and-intervention.md) — passive evidence отделено от active intervention.

Документ намеренно **не** определяет:

- конкретный Python base class;
- Gymnasium как обязательную runtime-зависимость;
- точные `Space`/dtype/shape;
- canonical internal representation Agent — это `DU-08`;
- internal Goal representation — это `DU-09`;
- Policy/Planner — это `DU-23`;
- Action execution boundary внутри Agent — это `DU-24`;
- scalar reward как обязательную форму feedback;
- exact artifact/snapshot serialization format;
- окончательный benchmark suite и statistical protocol — это `DU-28`;
- конкретные размеры карт, количества объектов и численные difficulty thresholds будущих versions.

---

# 1. Цель DU-07

MINDRA нужен внешний мир, который одновременно:

1. достаточно прост для причинной диагностики;
2. достаточно богат для Memory, World Model, Self Model, Drives, Appraisal, Valuation и Planning;
3. допускает частичную наблюдаемость и скрытые causal rules;
4. генерирует большое число воспроизводимых world instances;
5. поддерживает train/validation/test separation;
6. допускает точное snapshot/restore/fork для counterfactual experiments;
7. не передаёт Agent privileged evaluator/world state;
8. одинаково применим к baseline и полной MINDRA configuration;
9. не заставляет общую архитектуру зависеть от одной конкретной gridworld implementation.

Поэтому `DU-07` проектирует **два уровня**:

```text
общий Environment contract
        ↓
reference implementation family: MicroWorld
```

`MicroWorld` не является синонимом любого будущего Environment.

---

# 2. Главное архитектурное решение

MINDRA принимает **двухконтурную Environment boundary**:

```text
                     Environment
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
      Agent Interaction Plane   Research Plane
                 │                 │
 observation/task/feedback       hidden state
 action/result-visible subset    full transition evidence
                 │              snapshot/restore/fork
                 ▼              interventions/oracles
              Agent                │
                                  ▼
                         Evaluation / Artifact
```

Главный invariant:

```text
agent-visible interaction
≠
research-visible ground truth
```

То, что Environment знает истинное состояние мира или evaluator умеет его сохранить, не делает эту информацию доступной Agent.

Решение дополнительно зафиксировано в `ADR-0007`.

---

# 3. Environment как логическая ответственность

`Environment` владеет внешней динамикой мира, а не cognition Agent.

На semantic уровне Environment отвечает за:

- authoritative hidden world state;
- world transition rules;
- world-local stochastic processes;
- embodiment/world-side состояние агента, если оно является физическим свойством мира;
- task instance и внешние условия успеха/неуспеха;
- формирование agent-visible raw observation;
- применение committed action к миру;
- external task feedback, если оно предусмотрено task contract;
- termination/truncation;
- snapshot/restore/fork world state;
- research-only ground truth и transition evidence;
- procedural world generation;
- world/task/distribution identity и versioning.

Environment **не** отвечает за:

- internal utility;
- Drives;
- Appraisal;
- Memory Agent;
- internal Goal representation;
- Policy;
- Cortex;
- training optimizer;
- evaluator verdict;
- выбор «правильного действия» за Agent.

---

# 4. Три разных класса состояния

Для предотвращения leakage MINDRA различает минимум три состояния.

## 4.1. Hidden World State

Authoritative полное состояние Environment.

Conceptually может включать:

- карту/геометрию;
- позиции и свойства всех entities;
- скрытые causal rules;
- скрытые object mappings;
- dynamic event state;
- task ground truth;
- embodiment/world-side state;
- episode counters;
- Environment RNG state;
- pending stochastic events.

Hidden World State принадлежит Environment и **не является Agent observation**.

## 4.2. Raw Observation

Contract-defined проекция мира, разрешённая Agent.

Это ещё **не** canonical internal representation MINDRA.

`DU-08` определит преобразование:

```text
Raw Observation
      ↓
Perception / Representation
      ↓
canonical internal representation
```

## 4.3. Research Ground Truth

Research-only данные, необходимые evaluator/diagnostics:

- полный world state;
- exact causal rule mapping;
- true object identity/properties;
- task solver/oracle information;
- full action outcome reason;
- generator metadata;
- solvability proof/check;
- privileged objective metrics.

Research Ground Truth проходит через Evidence/Research Plane и по умолчанию не попадает Agent.

---

# 5. Agent Interaction Plane

Agent Interaction Plane должен быть минимальным и audit-friendly.

Conceptually Agent может получить только:

- raw observation;
- external task specification, если task contract её раскрывает;
- external task feedback, если task contract его раскрывает;
- termination/truncation information;
- только ту action/outcome information, которая разрешена interaction contract.

Нельзя автоматически передавать Agent:

- hidden map;
- future stochastic events;
- true hidden rule;
- shortest path;
- oracle action;
- evaluator metric;
- distribution/split label;
- world seed как shortcut, если seed не является намеренной частью задачи;
- hidden reason action failure;
- dynamic action mask, вычисленный из скрытого состояния, если он раскрывает неизвестную информацию;
- privileged `info` dictionary только потому, что underlying framework его поддерживает.

---

# 6. Task Specification

Environment может предъявлять внешнюю задачу Agent, но `DU-07` не определяет, как она становится внутренней Goal representation.

Различаются:

```text
External Task Specification
→ внешний contract задания

Internal Goal State
→ будущая agent-owned representation из DU-09
```

Task Specification может быть:

- structured;
- symbolic;
- текстовой;
- смешанной,

если конкретная task family это определяет.

Для базового `MicroWorld` предпочтителен простой structured/symbolic source of truth; текстовая формулировка может быть альтернативной observation modality позднее.

Это предотвращает ситуацию, где качество LLM становится обязательным условием проверки базовой Environment semantics.

---

# 7. External feedback, objective metric и internal utility

MINDRA строго разводит три понятия.

## 7.1. External Task Feedback

Сигнал, который task/environment **намеренно** предоставляет Agent после действия или события.

Он может быть:

- scalar;
- vector;
- sparse event;
- structured record;
- полностью отсутствовать для некоторых задач.

Форма не фиксируется как единый scalar reward.

## 7.2. Objective Task Metric

Research-only ground-truth оценка результата:

- success;
- path inefficiency;
- safety violation count;
- hidden-rule identification accuracy;
- resource cost;
- другие benchmark metrics.

Objective Task Metric не является Agent input автоматически.

## 7.3. Internal Utility

Agent-owned оценка, которая будет спроектирована позже.

```text
External Task Feedback
≠
Objective Task Metric
≠
Internal Utility
```

Если будущий RL algorithm требует scalar reward, adapter может использовать явно выбранный компонент External Task Feedback. Это implementation/training decision, а не изменение Environment semantics.

---

# 8. Action contract

Environment принимает только **committed action** после `Action Commit` Agent.

Нужно различать минимум три уровня.

## 8.1. Structurally invalid action

Action не соответствует declared action schema/capability.

Например:

- неизвестный action kind;
- malformed arguments;
- type/range violation.

Это contract/runtime error и по возможности обнаруживается до world transition.

## 8.2. Valid action attempt, но world-level effect невозможен

Action соответствует contract, но в текущем мире может:

- не дать эффекта;
- быть заблокирован;
- не найти target;
- не выполнить precondition;
- завершиться stochastic failure.

Это **нормальный Environment outcome**, а не schema error.

## 8.3. Agent-visible outcome

Agent не обязан получать privileged reason.

Например, Research Plane может знать:

```text
interaction failed: door_locked_requires_key_17
```

а Agent-visible consequence может быть только:

```text
позиция не изменилась
вид двери не изменился
```

если task observation contract не сообщает причину явно.

---

# 9. Action vocabulary MicroWorld

MicroWorld должен использовать небольшой action vocabulary, чтобы исследование cognition не вырождалось в сложный motor-control benchmark.

На semantic уровне первая family должна поддерживать действия класса:

- перемещение по дискретному пространству;
- `interact` с доступным объектом;
- `pickup`;
- `drop`;
- `use`, если task family требует явного использования;
- `wait/no-op` как намеренное отсутствие внешнего действия.

Точная encoding/schema action определяется version/exact contract позднее.

Направление взгляда/повороты **не являются обязательной фундаментальной сложностью**. Они могут быть включены конкретной task family, если нужны для исследования active perception.

---

# 10. `reset` semantics

`Environment reset` создаёт новый Episode state и **не является Agent reset**.

Conceptually reset обязан:

1. определить Environment/task/distribution versions;
2. выбрать или восстановить world definition;
3. установить episode-level initial hidden state;
4. инициализировать Environment RNG streams;
5. проверить basic validity/solvability согласно task policy;
6. создать initial Raw Observation;
7. создать research-only reset evidence;
8. присвоить episode/world identities.

После reset Environment находится в состоянии, где первый Agent Decision Window может начаться корректно.

Повторный reset без завершения предыдущего Episode должен иметь явную abort/restart provenance, а не молча стирать историю.

---

# 11. Environment transition semantics

Один внешний шаг conceptually:

```text
Agent Action Commit
       ↓
Environment accepts committed action
       ↓
validate action contract
       ↓
apply world transition
       ↓
advance exogenous dynamics/RNG
       ↓
compute task/world consequences
       ↓
produce authoritative Transition Record
       ↓
construct next Raw Observation
       ↓
Outcome Commit
```

Точный порядок внутренних world sub-phases должен быть deterministic относительно hidden state + action + Environment RNG state для конкретной Environment version.

Если future environment использует parallel physical simulation, результат всё равно должен иметь однозначную logical transition semantics.

---

# 12. Termination и truncation

MINDRA принимает разделение, аналогичное современному Gymnasium API:

## `terminated`

Episode естественно достиг terminal state task/world semantics.

Примеры:

- цель достигнута;
- необратимый провал;
- avatar/world entity уничтожена, если это часть задачи;
- task-specific terminal condition.

## `truncated`

Episode остановлен по внешнему ограничению, не являющемуся естественным terminal state задачи.

Примеры:

- time/step budget;
- experiment budget;
- runtime/resource limit;
- external safety abort;
- infrastructure abort, если результат ещё можно корректно классифицировать.

```text
terminated
≠
truncated
```

Причина завершения должна быть сохранена в research evidence; Agent-visible детализация зависит от task contract.

---

# 13. Partial observability как default исследовательский режим

MicroWorld должен поддерживать partial observability как first-class capability.

Причины:

- Memory иначе становится необязательной для многих задач;
- World Model можно заменить непосредственным чтением полной карты;
- exploration/uncertainty теряют смысл;
- hidden causal rules невозможно честно исследовать при полном privileged state.

Но полная observability также должна существовать как **control configuration**.

Conceptually:

```text
same World Definition
├── partial-observation condition
└── full-observation control
```

Это позволяет измерять, является ли проблема действительно memory/inference-bound.

---

# 14. Raw Observation MicroWorld

DU-07 фиксирует семантику, но не tensor encoding.

Raw Observation может conceptually содержать:

- локально видимую геометрию;
- наблюдаемые свойства видимых entities;
- собственное world-side положение/состояние, если оно доступно агенту;
- inventory-visible content;
- contract-defined recent world event/consequence;
- External Task Specification;
- agent-visible External Task Feedback.

Не должны автоматически входить:

- hidden entity properties;
- causal rule identifiers;
- global map coordinates, если task condition не раскрывает их;
- hidden targets;
- evaluator annotations;
- generator factors/split labels.

Конкретная encoding/projection в canonical representation — `DU-08`.

---

# 15. Embodiment state и внутреннее состояние Agent

MicroWorld может моделировать **world-side embodiment variables**:

- положение;
- инвентарь;
- физическую целостность;
- переносимые ресурсы;
- world-defined capacity/limitations.

Это не делает их Drives.

Например:

```text
Environment: avatar_health = 20/100
Agent: safety/need appraisal of this fact
```

— разные ответственности.

Будущие Drives могут реагировать на наблюдаемые embodiment variables, но Environment не определяет внутреннюю ценность этих состояний за Agent.

---

# 16. Скрытые causal rules

MicroWorld должен поддерживать правила, которые:

- являются частью Hidden World State/World Definition;
- могут меняться между world instances/distributions;
- не выводятся напрямую из object label;
- имеют наблюдаемые последствия;
- могут быть обнаружены через взаимодействие/наблюдение, если task задумана как learnable.

Примеры классов:

- switch → door mapping;
- object property → effect mapping;
- resource → transformation;
- hazard behavior;
- tool → action capability;
- context-dependent interaction rule;
- delayed effect;
- stochastic transition probability.

Важно:

> hidden rule не должен быть просто скрытым answer key без достаточного observable evidence, если experiment проверяет способность Agent её выучить.

Намеренно неидентифицируемые conditions допустимы как control, но должны быть обозначены отдельно.

---

# 17. Observed feature не равно causal property

MicroWorld не фиксирует shortcut вида:

```text
red = danger
blue = resource
```

Наблюдаемые признаки и causal properties генерируются как разные факторы.

Например:

```text
visual/symbolic appearance
    ├── color
    ├── shape
    └── marker

causal properties
    ├── harmful
    ├── consumable
    ├── opens X
    └── transforms Y
```

Связь между ними может:

- рандомизироваться;
- удерживаться внутри конкретной distribution;
- специально меняться в rule-shift test;
- использоваться как controlled shortcut experiment.

Это позволяет проверять actual adaptation вместо memorization поверх superficial cue.

---

# 18. Stochasticity и RNG

Одного общего `seed` недостаточно для строгой causal диагностики.

Environment conceptually разделяет независимые stochastic sources минимум на:

1. **generation RNG** — создание World Definition;
2. **dynamics RNG** — stochastic world transitions внутри Episode;
3. **task RNG** — sampling task-specific initial conditions, если он отделён от world generation.

Intervention/evaluator RNG не должен скрыто использовать тот же mutable stream.

Agent/training RNG также находится за Environment boundary.

Exact counterfactual restore требует восстановления всех Environment RNG states, влияющих на будущее.

---

# 19. Seed не является полным world identity

Для воспроизводимости недостаточно записать:

```text
seed = 42
```

Потому что generator code/version может измениться.

World identity должна связывать минимум:

- Environment family/version;
- generator version;
- task family/version;
- distribution identity/version;
- generation parameters;
- generation seed;
- при необходимости content/world manifest hash.

Для confirmatory benchmarks желательно сохранять normalized generated `World Manifest` или иной artifact, позволяющий доказать, какой именно мир использовался.

---

# 20. Environment Snapshot

Exact `Environment Snapshot` должен быть достаточен для восстановления **будущей world dynamics**, а не только картинки текущей карты.

Conceptually snapshot включает:

- complete hidden world state;
- task state;
- embodiment/world-side state;
- episode counters;
- pending events;
- all causally relevant Environment RNG states;
- Environment/world/task versions;
- world identity/manifest reference;
- snapshot causal identity.

Необязательные render caches/profiler objects не являются semantic state, если их отсутствие не меняет future behavior.

Exact serialization format определяется позже.

---

# 21. `snapshot`, `restore`, `clone`, `fork`

Нужно различать операции.

## Snapshot

Создать неизменяемое research representation текущего causally relevant Environment state.

## Restore

Восстановить Environment из совместимого snapshot.

Это privileged research/runtime operation и не является Agent action.

## Clone

Создать независимый Environment instance из одного snapshot.

Изменение clone не меняет оригинал.

## Fork

Создать новую research lineage от snapshot с явной parent relation.

```text
Environment Snapshot E42
       ├── branch control
       └── branch treatment
```

Exact MINDRA counterfactual требует совместимого fork как Agent, так и Environment state.

---

# 22. Environment intervention

Environment intervention выполняется только через Research/Intervention boundary.

Допустимые классы conceptually:

- изменить скрытое world property;
- переставить entity;
- изменить causal rule;
- изменить stochastic parameter;
- изменить task state;
- создать/удалить объект;
- изменить future exogenous event.

Intervention обязан иметь:

- `intervention_id`;
- target;
- base Environment snapshot/revision;
- treatment;
- resulting lineage;
- provenance;
- duration/persistence semantics.

Agent не должен автоматически получать сообщение «исследователь поменял правило», если это не является частью experimental treatment.

Natural и intervened Environment trajectories различаются в evidence.

---

# 23. Procedural generation

MicroWorld использует procedural generation как средство:

- получать много world instances;
- отделять memorization от generalization;
- контролировать difficulty factors;
- создавать held-out combinations;
- генерировать matched control/treatment worlds;
- увеличивать sample diversity при низкой computational cost.

Генератор должен быть **factorized**, а не одним непрозрачным `random_world(seed)`.

Conceptual factors:

- geometry/topology;
- object inventory;
- observable appearance mapping;
- hidden causal rules;
- task graph/dependency depth;
- distractors;
- observability radius/occlusion;
- stochasticity;
- resource constraints;
- horizon;
- feedback sparsity;
- dynamic events.

Каждый factor должен быть доступен Research Plane как generation provenance, но не обязательно Agent.

---

# 24. Solvability и generator validity

Procedural generation не должен незаметно создавать benchmark noise через случайно невозможные задачи.

Для каждой task family должна быть определена одна из политик:

1. generated instances обязаны проходить solver/validator;
2. невозможные instances явно маркируются и используются только в специальных experiments;
3. solvability неизвестна — тогда это является documented limitation и такой family нельзя использовать для claims, требующих гарантированно решаемых задач, без дополнительного контроля.

Предпочтение для core MicroWorld benchmark:

> generated training/evaluation instances должны иметь проверяемую task validity/solvability.

Research oracle/solver не передаётся Agent.

---

# 25. World distributions и splits

MINDRA не ограничивается случайным делением seed на train/test.

Нужно различать как минимум классы evaluation distributions.

## 25.1. In-distribution unseen instances

Новые seeds из той же factor distribution.

Проверяет generalization к новым world instances без semantic shift.

## 25.2. Compositional holdout

Знакомые primitives, но новые combinations:

- topology + object combination;
- tool + target relation;
- task dependency ordering;
- rule composition.

## 25.3. Rule-shift / remapping

Изменяется mapping наблюдаемых features к causal properties.

Проверяет adaptation и сопротивление shortcut memorization.

## 25.4. Difficulty/scale shift

Held-out значения:

- больший мир;
- длиннее dependency chain;
- более редкий feedback;
- больше distractors;
- другая stochasticity.

## 25.5. Structural OOD

Более сильный shift topology/task grammar, используемый только для специально заявленных transfer claims.

Конкретный набор splits фиксируется будущим Evaluation Harness/version, но Environment design обязан их поддерживать.

---

# 26. Split leakage prevention

Agent не получает автоматически:

- `train`/`validation`/`test` label;
- generator seed;
- distribution ID;
- hidden difficulty label;
- task solution class.

Если training code использует split metadata, это остаётся Training/Evaluation Runtime metadata.

World generation artifacts должны позволять проверить отсутствие overlap там, где protocol заявляет held-out instances/combinations.

---

# 27. Environment versioning

Версионируются независимо как минимум:

- Environment semantic contract;
- MicroWorld engine/rules;
- generator;
- task family;
- distribution definition;
- world manifests/benchmark set.

Изменение визуального renderer, не влияющее на symbolic agent observation, не обязано менять world semantics.

Изменение transition rule, observation visibility, task feedback или generator factor distribution должно быть идентифицируемо как semantic/version change.

Нельзя сравнивать experiment results как один benchmark, если Environment semantics изменились без фиксации version boundary.

---

# 28. Research Transition Record

Для каждого Environment Transition Evidence Plane должен иметь возможность сохранить authoritative record, conceptually содержащий:

- run/session/episode identities;
- environment/world/task/distribution versions;
- world instance identity;
- transition identity;
- pre-transition snapshot/revision reference;
- committed action;
- structural action validation result;
- full world-level action outcome;
- stochastic draws/provenance настолько, насколько требуется causal replay;
- external task feedback;
- objective research metrics/events;
- termination/truncation state и reason;
- post-transition snapshot/revision reference;
- intervention provenance, если есть.

Это **research evidence**, а не Agent observation.

Exact record schema относится к `DU-25/27/28`.

---

# 29. Rendering и human inspection

MicroWorld должен допускать human-readable rendering для debugging/review, но renderer не является source of truth world semantics.

Допустимы будущие формы:

- ASCII/text;
- simple 2D visualization;
- RGB image;
- interactive viewer.

Если Agent получает pixels, это отдельная observation modality/configuration, а не побочный эффект того, что renderer существует.

---

# 30. Vectorization и batching

Environment contract должен допускать несколько независимых Environment instances для batch/vectorized collection.

Но:

```text
vector batch
≠
shared world lineage
```

Каждый item имеет собственные:

- world state;
- RNG state;
- episode identity;
- snapshot lineage;
- termination/truncation state.

Autoreset не должен скрывать final outcome/terminal observation от trajectory evidence.

Concrete vectorization framework определяется позднее.

---

# 31. Почему MicroWorld — 2D symbolic world

Для первой reference family принимается **дискретный 2D symbolic world**.

Причины:

- дёшево генерируется;
- легко snapshot/restore;
- легко построить oracle/solvability checker;
- легко визуально проверить;
- не требует дорогого vision stack;
- позволяет partial observability;
- поддерживает objects, tools, doors, hazards, resources и hidden rules;
- позволяет длинные causal/task dependencies;
- хорошо подходит для controlled counterfactual changes;
- не привязывает cognition quality к pixel representation раньше `DU-08`.

Это не означает, что MINDRA ограничивается gridworld forever.

---

# 32. MicroWorld entities

Core entity model должен быть compositional.

Conceptually entity имеет разные категории свойств:

```text
identity/provenance
spatial properties
observable appearance
interaction affordances
hidden causal properties
mutable dynamic state
```

Кандидатные entity classes:

- wall/barrier;
- floor/terrain;
- door/gate;
- switch/control;
- key/tool;
- portable object;
- container;
- resource;
- hazard;
- target/marker;
- dynamic entity.

Список не является окончательным enum будущего API.

Главный invariant — appearance не должна автоматически определять hidden causal property.

---

# 33. Minimal task families MicroWorld

Core MicroWorld должен уметь выражать несколько **раздельно диагностируемых** task families.

## MW-0 — Direct Reach

Простая наблюдаемая цель без скрытых зависимостей.

Назначение:

- sanity baseline;
- Action/Policy baseline;
- проверка basic navigation;
- контроль, что сложные модули не ухудшают простую задачу.

## MW-1 — Fetch / Unlock / Dependency

Нужно выполнить последовательность зависимых действий:

```text
найти tool
→ получить доступ
→ взаимодействовать с target
```

Назначение:

- planning;
- task dependency;
- delayed external feedback.

## MW-2 — Cue / Memory

Релевантная информация доступна раньше, но отсутствует в момент решения.

Назначение:

- Memory Core;
- partial observability;
- retrieval utility.

## MW-3 — Hidden Rule Discovery

Agent должен по наблюдаемым последствиям определить неизвестную causal relation.

Назначение:

- World Model;
- uncertainty;
- intrinsic signals;
- exploration.

## MW-4 — Exploration / Safety Trade-off

Есть несколько неизвестных возможностей с различным risk/resource profile.

Назначение:

- Drives;
- Valuation;
- Appraisal;
- exploration/exploitation.

Environment задаёт объективные consequences, но **не задаёт внутреннюю значимость** этих consequences.

## MW-5 — Delayed Consequence

Действие даёт эффект через несколько transitions или меняет будущие возможности.

Назначение:

- World Model;
- planning;
- non-myopic valuation.

## MW-6 — Rule Reversal / Adaptation

Causal mapping, работавший ранее, меняется между sessions/world distributions или в объявленной phase.

Назначение:

- adaptation;
- resistance to shortcut memorization;
- Memory/update dynamics;
- uncertainty recalibration.

## MW-7 — Compositional Task

Комбинация знакомых primitives в новом dependency graph.

Назначение:

- Goal System;
- planning;
- generalization;
- transfer.

Каждая future version может реализовать только подмножество families согласно roadmap. `DU-07` фиксирует требуемую выразительность Environment, а не обязательный scope первой software version.

---

# 34. Difficulty axes

Difficulty должна изменяться контролируемо по отдельным факторам, а не только одним `easy/hard` флагом.

Кандидатные axes:

- world size;
- topology complexity;
- partial-observation radius;
- occlusion;
- number of entities;
- distractor count;
- task dependency depth;
- horizon;
- feedback sparsity;
- hidden-rule entropy;
- stochasticity;
- resource scarcity;
- action failure probability;
- number of plausible hypotheses;
- dynamic change rate.

Experiment provenance должна фиксировать relevant axes/factor distribution.

---

# 35. Matched worlds для causal experiments

Generator должен по возможности поддерживать создание world pairs, различающихся ограниченным фактором.

Например:

```text
World A: switch X opens door Y
World B: switch X opens door Z
```

при одинаковых:

- geometry;
- visible objects;
- starting position;
- task structure;
- остальных rules.

Это позволяет отделять эффект конкретного causal factor от общего procedural variation.

Matched generation особенно полезна для Appraisal/Drives/World Model experiments.

---

# 36. Baseline и oracle support

Environment должен позволять строить внешние research-only baselines/oracles, но не включать их внутрь Agent.

Кандидаты:

- random policy baseline;
- shortest-path/full-state oracle;
- task-specific scripted solver;
- full-observation baseline;
- perfect-rule-information oracle.

Они нужны для:

- sanity checks;
- solvability validation;
- upper/lower bounds;
- оценки task difficulty.

Oracle information не пересекает Agent Interaction Plane.

---

# 37. Failure semantics Environment

Нужно различать:

- Agent action contract error;
- normal ineffective action;
- Environment terminal failure state;
- task failure;
- invalid generated world;
- Environment internal error;
- infrastructure abort/truncation;
- evidence capture failure.

Эти классы нельзя сводить к одному `done=False/True` или единому exception без provenance.

---

# 38. Compatibility с Gymnasium-подобным API

Gymnasium является полезным interoperability target:

```text
reset
step(action)
observation space
action space
terminated
truncated
```

Но MINDRA semantic contract шире:

- exact snapshot/restore/clone/fork;
- research transition record;
- split/distribution identity;
- hidden ground-truth boundary;
- intervention provenance;
- multiple RNG streams;
- world/task/generator versioning.

Поэтому будущая реализация может иметь:

```text
MINDRA Environment
        ↕ adapter
Gymnasium-compatible Env
```

но Gymnasium `info` не становится автоматически Agent input.

---

# 39. Research evidence, использованное при проектировании

## Gymnasium

Современный Gymnasium `Env` отделяет `reset()` и `step(action)`, задаёт observation/action spaces и принципиально различает `terminated` и `truncated`.

Источник:

- https://gymnasium.farama.org/api/env/

MINDRA использует эту модель как interoperability evidence, но расширяет её research semantics.

## MiniGrid

MiniGrid предоставляет минималистичные, настраиваемые goal-oriented grid environments, partial observations, object interaction и task families. Это подтверждает, что простой symbolic gridworld может быть достаточно выразительным для memory/navigation/interaction research без тяжёлой physics/vision инфраструктуры.

Источники:

- https://minigrid.farama.org/
- https://arxiv.org/abs/2306.13831

## Procgen

Procgen показывает ценность procedurally generated environment distributions для измерения generalization и использует независимые level ranges/seeds. Его implementation также демонстрирует практичность save/load Environment state.

Источники:

- https://arxiv.org/abs/1912.01588
- https://github.com/openai/procgen

MINDRA идёт дальше, требуя factorized distributions, explicit versioning и exact causal provenance для counterfactual experiments.

---

# 40. Принятые invariants DU-07

## ENV-01

Environment находится вне Agent boundary и владеет authoritative world dynamics.

## ENV-02

Agent Interaction Plane и Research Plane логически разделены.

## ENV-03

Hidden World State/Research Ground Truth не становятся Agent observation автоматически.

## ENV-04

Raw Observation не является canonical internal representation MINDRA.

## ENV-05

External Task Specification не равна внутреннему Goal state Agent.

## ENV-06

External Task Feedback, Objective Task Metric и Internal Utility являются разными сущностями.

## ENV-07

Structurally invalid action и valid-but-ineffective world action различаются.

## ENV-08

`terminated` и `truncated` различаются.

## ENV-09

Partial observability является first-class MicroWorld capability; full observability доступна как control.

## ENV-10

Observed appearance не должна канонически определять hidden causal property.

## ENV-11

Environment stochasticity имеет identifiable RNG provenance; exact restore включает causally relevant RNG state.

## ENV-12

Seed сам по себе не является достаточной world identity.

## ENV-13

Exact Environment Snapshot достаточен для восстановления будущей world dynamics.

## ENV-14

Restore/clone/fork являются privileged research/runtime operations, не Agent actions.

## ENV-15

Environment intervention создаёт явную intervened lineage/provenance.

## ENV-16

Procedural generator должен быть factorized и versioned.

## ENV-17

Core benchmark instances должны иметь контролируемую validity/solvability policy.

## ENV-18

Environment должен поддерживать ID unseen, compositional holdout, rule-shift и более сильные OOD distributions.

## ENV-19

Split/distribution metadata не является Agent-visible input по умолчанию.

## ENV-20

MicroWorld является reference 2D symbolic Environment family, а не универсальным определением любого Environment MINDRA.

## ENV-21

MicroWorld должен поддерживать независимые task families для baseline, memory, hidden-rule discovery, exploration/trade-off, delayed consequence, adaptation и compositional tasks.

## ENV-22

Environment Transition evidence и Agent-visible outcome являются разными проекциями одного transition.

## ENV-23

Vectorized Environment instances сохраняют независимые causal lineages/RNG/state.

## ENV-24

Gymnasium compatibility допустима через adapter, но Gymnasium не является канонической архитектурной зависимостью.

---

# 41. Что DU-07 намеренно оставляет открытым

- concrete Python `EnvironmentProtocol`;
- конкретный Gymnasium adapter;
- точные observation/action types;
- размеры grid/maps;
- exact list entity classes;
- exact task grammar;
- exact reward/feedback values;
- конкретный procedural-generation algorithm;
- конкретный solver;
- exact snapshot serialization;
- exact RNG implementation;
- concrete split manifests;
- concrete difficulty ranges;
- exact rendering stack;
- vectorization library;
- training curriculum;
- benchmark scoring.

Эти решения принимаются в exact contracts/version planning или соответствующих downstream Design Updates.

---

# 42. Последствия для следующих Design Updates

## DU-08 — Perception / Canonical Representation

Получает явный `Raw Observation` boundary и должен определить, как heterogeneous Environment data превращаются во внутреннее representation без privileged leakage.

## DU-09 — Goal System

Получает `External Task Specification` и должен определить, как Agent создаёт/поддерживает internal goal state.

## DU-11 — Memory Core

Получает частично наблюдаемые task families и temporal cues для честной проверки retrieval.

## DU-12 — World Model

Получает versioned transition semantics, hidden causal rules и matched world factors.

## DU-14 — Intrinsic Signals

Получает novelty/exploration tasks без необходимости кодировать curiosity внутри Environment reward.

## DU-15…DU-18

Получают объективные world consequences, но не готовую внутреннюю ценность — именно это позволяет исследовать Drives/Appraisal/Valuation.

## DU-23 — Policy / Planner

Получает небольшой и стабильный action boundary, не смешанный с low-level continuous motor control.

## DU-25 / DU-27 / DU-28

Должны формализовать Transition Record, snapshot artifact, world manifest и evaluation distributions.

---

# 43. Completion gate DU-07

`DU-07` завершён, если можно описать один и тот же world/task instance так, чтобы:

1. baseline и MINDRA configuration получили **одинаковый agent-visible contract**;
2. evaluator имел достаточный privileged ground truth для измерения результата, не передавая его Agent;
3. world можно было воспроизводимо создать, сохранить, восстановить и разветвить;
4. natural/intervened world histories различались по provenance;
5. train/test могли отличаться контролируемыми generation factors;
6. Environment не определял internal utility, Goal representation или cognition Agent;
7. MicroWorld мог выражать будущие диагностические task families без изменения фундаментального contract.

После принятия этого документа следующий допустимый Design Update:

```text
DU-08 — Perception / Canonical Representation
```
