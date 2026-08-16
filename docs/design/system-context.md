# Системный контекст MINDRA

## Статус документа

**Design Update:** `DU-01 — System Context`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет MINDRA как логическую систему в окружении внешней среды, runtime-инфраструктуры, обучения, оценки, хранения артефактов и вычислительных ресурсов.

Последующие `DU-02` … `DU-05` уточнили dependency, temporal, state и scheduler semantics, не меняя основного решения `DU-01`: **архитектурная принадлежность определяется логической ответственностью и ownership, а не process/device/deployment topology**.

Документ намеренно не задаёт:

- конкретную Python/package структуру;
- конкретный framework;
- concrete Cortex model;
- concrete GPU/provider;
- exact Environment API;
- exact `CognitiveState` container;
- exact `ModuleProtocol`;
- concrete scheduler/DAG implementation;
- training algorithm;
- checkpoint/trajectory format.

Эти вопросы принадлежат более конкретным canonical design documents.

---

# 1. Цель DU-01

Основная задача системного контекста — для любого компонента сначала ответить:

1. **Кому он логически принадлежит?**
2. **Какую ответственность он несёт?**
3. **Какие данные имеет право видеть/изменять?**
4. **Является ли его физическое размещение частью semantics или только deployment detail?**

Это предотвращает смешивание cognition с infrastructure, training и evaluation только потому, что всё временно исполняется в одном notebook/process.

---

# 2. Главное архитектурное решение

MINDRA использует **логические границы ответственности, независимые от deployment topology**.

Следовательно:

```text
логически разные компоненты
могут физически находиться
в одном process / на одном GPU
```

и одновременно:

```text
один логический компонент
может физически исполняться
в другом process / worker / machine / provider
```

Примеры:

- `Training Runtime` может работать рядом с Agent, но остаётся внешней optimization infrastructure;
- Cortex может исполняться удалённо, но оставаться внутренней capability Agent;
- активная Memory может использовать внешний storage backend, но её содержимое остаётся agent-owned state;
- `Evaluation Runtime` может находиться на том же GPU, но не получает право передавать score в cognition;
- `Cognitive Scheduler` может физически выполняться внутри process Execution Runtime, но его scheduling semantics принадлежат Agent runtime core.

Решение дополнительно зафиксировано в `ADR-0001`.

---

# 3. Типы границ

## 3.1. Logical boundary

Определяет ответственность и ownership.

Пример:

```text
Cortex capability → Agent
Cognitive Scheduler → Agent runtime core
Experiment Runner → Research Control Plane
Training Runtime → внешняя training infrastructure
```

## 3.2. Execution boundary

Физическое размещение:

- тот же process/thread;
- отдельный worker;
- отдельный process;
- другая машина;
- remote runtime.

Само по себе не определяет architecture semantics.

## 3.3. Storage boundary

Физическое место хранения:

- RAM/VRAM;
- local disk;
- object storage;
- remote storage.

Storage location не меняет logical owner state.

## 3.4. Trust boundary

Определяет, какой компонент является допустимым источником конкретного класса данных для research integrity.

Это минимальная research-oriented trust model, а не полная security threat model.

---

# 4. Верхнеуровневый контекст

```text
                         Исследователь / оператор
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Experiment Runner │
                         └─────────┬─────────┘
                                   │ run/config/seed
                  ┌────────────────┼────────────────┐
                  ▼                ▼                ▼
        ┌────────────────┐ ┌───────────────┐ ┌────────────────┐
        │Execution Runtime│ │Training Runtime│ │Evaluation Runtime│
        └───────┬────────┘ └───────┬───────┘ └───────┬────────┘
                │                  │                 │
                ▼                  │                 ▼
      ┌───────────────────────┐    │       evaluation clone /
      │     MINDRA Agent      │◄───┘       controlled subject
      │                       │
      │ Agent runtime core    │
      │ └─ Cognitive Scheduler│
      │ cognitive modules     │
      │ Cortex                │
      │ agent-owned state     │
      └──────────┬────────────┘
                 │ observation/action
                 ▼
          ┌─────────────┐
          │ Environment │
          └─────────────┘

runtime/training/evaluation evidence
                 │
                 ▼
        Artifact Collector
                 │
                 ▼
         Artifact Storage

Все роли физически размещаются на произвольном Compute Substrate.
```

Схема отражает **logical responsibilities**, а не обязательные processes.

---

# 5. MINDRA Agent boundary

## 5.1. Внутри Agent находятся

- принятые cognitive modules;
- Cortex как логическая capability;
- `Agent runtime core`, обеспечивающий внутреннюю execution semantics;
- `Cognitive Scheduler` как часть Agent runtime core;
- canonical runtime state;
- causally relevant module-private state;
- agent-owned persistent state;
- trainable parameters модулей;
- активная Memory;
- agent-owned adapters/representations;
- механизмы выбора действий;
- внутренние сигналы и control mechanisms, если они приняты соответствующими DU.

`Cognitive Scheduler` не является cognitive module: он не определяет цели, utility или action. Он обеспечивает исполнение принятой module/state semantics из `module-lifecycle.md`.

## 5.2. Вне Agent находятся

- `Environment`;
- `Execution Runtime` как внешний host/orchestrator запуска;
- `Experiment Runner`;
- `Training Runtime` как optimization mechanism;
- `Evaluation Runtime`;
- evaluator metrics;
- artifact/log collector;
- archival checkpoints;
- CI/Git repository;
- конкретный CPU/GPU/VM/provider;
- Google Colab как сервис;
- hidden Environment state, не входящий в observation contract.

## 5.3. Agent исполним без trainer/evaluator

Канонический invariant:

> Сформированный MINDRA Agent должен иметь семантически корректный execution path без подключённых Training Runtime и Evaluation Runtime.

Это не означает, что необученный Agent обязан быть полезным; это означает отсутствие скрытой training/evaluation dependency в cognition path.

---

# 6. Agent runtime core и Cognitive Scheduler

`DU-05` уточняет границу `DU-01`.

`Agent runtime core` — некогнитивная внутренняя механика, необходимая для соблюдения архитектурной семантики Agent.

К ней относится `Cognitive Scheduler`, который:

- исполняет active module plan;
- соблюдает dependency/freshness constraints;
- формирует execution waves;
- координирует state/private-state commits;
- применяет lifecycle transitions;
- обеспечивает causal ordering.

Scheduler не должен:

- выбирать task-level action вместо Policy;
- вычислять utility;
- решать goal conflicts как hidden policy;
- использовать evaluator score;
- выполнять optimizer learning.

Физически scheduler может быть реализован внутри Execution Runtime process, но **логическая scheduling semantics принадлежит Agent**.

Это важно: внешний runtime не должен менять cognition простым изменением порядка module calls.

---

# 7. Environment boundary

`Environment` владеет:

- истинным world state;
- transition rules;
- hidden world variables;
- task conditions;
- termination/truncation semantics;
- external feedback, если он предусмотрен task contract.

Agent получает только contract-defined данные.

```text
Environment
  ├─ observation
  ├─ allowed external feedback
  ├─ termination/truncation
  └─ public metadata
        ↓
      Agent
        │
        └─ action
             ↓
         Environment
```

Environment не должен скрыто передавать:

- evaluator verdict;
- test answer/label;
- privileged hidden state;
- правильное действие;
- будущие события;
- internal MINDRA quality metric,

если это не является специально определённым experimental/task condition.

Exact `reset/step/clone/restore` semantics проектируются в `DU-07`.

---

# 8. Cortex: logical и physical boundary

## 8.1. Logical

Cortex — внутренняя capability Agent, потому что его outputs участвуют в cognition.

## 8.2. Physical

Backend может быть:

- local in-process;
- local worker;
- другой GPU;
- remote runtime;
- external inference service,

если будущий Cortex contract это допускает.

## 8.3. Cortex Execution Provider

Физический внешний provider не становится отдельным cognitive module. Он исполняет backend за Cortex integration boundary.

## 8.4. Model leakage запрещён

Общая архитектура не должна предполагать:

```text
hidden_size конкретной модели
конкретное имя Qwen/Gemma/Llama
cuda:0
локальное обязательное исполнение
provider-specific request objects
```

Точные требования Cortex определяются в `DU-10`.

---

# 9. Execution Runtime

`Execution Runtime` — внешняя infrastructure role, которая хостит Agent и соединяет его с Environment.

Он может:

- создать/загрузить Agent;
- предоставить compute/resources;
- передавать разрешённые observations/actions;
- запускать Agent lifecycle entrypoints;
- остановить/restart run;
- подключать разрешённые observability hooks;
- направлять evidence в Artifact Collector.

Он не должен:

- самостоятельно выбирать action;
- менять internal value;
- переставлять cognitive modules вопреки Agent scheduler semantics;
- создавать hidden fallback;
- добавлять evaluator feedback;
- менять cognition из-за provider identity.

Отношение:

```text
Execution Runtime hosts
        ↓
MINDRA Agent
        ↓
Agent runtime core owns scheduling semantics
```

---

# 10. Training Runtime

`Training Runtime` находится вне Agent boundary.

Он может:

- читать разрешённый experience/datasets/snapshots;
- вычислять losses/gradients;
- владеть optimizer state;
- формировать Learning Updates;
- обновлять agent-owned trainable state через явную boundary;
- сохранять training metrics/checkpoints.

Ownership:

```text
Agent owns learned parameters
Training Runtime owns optimization procedure/state
```

`Cognitive Scheduler` не является trainer и не вызывает универсальный `learn()` после каждого cognitive module compute.

Exact training lifecycle проектируется в `DU-26`.

---

# 11. Online execution, online learning и offline training

## Online execution

Environment развивается, Agent выполняет cognition/action. Runtime-state updates допустимы как часть нормальной динамики.

## Online learning

Training Runtime может работать одновременно с interaction, но Learning Updates должны иметь явную causal/revision provenance. In-flight cognitive computations не должны незаметно менять `agent_revision`.

## Offline training

Environment time не развивается; обучение использует сохранённый experience/dataset/snapshot.

## Consolidation

Отдельная maintenance/training phase, способная изменять долговременное state/representations/parameters. Exact ownership проектируется позднее.

---

# 12. Evaluation Runtime

`Evaluation Runtime` — внешний research component.

Он может:

- загружать snapshot;
- создавать evaluation clone;
- запускать controlled Environment;
- управлять test seeds/distributions;
- выполнять explicit intervention;
- измерять trajectories/metrics;
- сравнивать configurations.

Главный invariant:

> Evaluation-derived information не становится normal agent-visible input.

Agent не получает автоматически:

- итоговый score;
- название experimental condition;
- expected outcome;
- benchmark answer;
- metrics других configurations.

Controlled intervention разрешён только через explicit, observable и reproducible boundary, проектируемую в `DU-06`.

---

# 13. Experiment Runner

`Experiment Runner` находится во внешнем Research Control Plane.

Он задаёт/фиксирует:

- experiment identity;
- configuration;
- seed;
- dataset/environment selection;
- agent snapshot/composition;
- runtime/training/evaluation intent;
- artifact destinations;
- launch/stop status.

Run metadata не должна становиться hidden cognitive input.

---

# 14. Artifact Collector и Artifact Storage

`Artifact Collector` пассивно получает evidence:

- logs;
- metrics;
- trajectories;
- committed snapshots;
- checkpoints;
- profiler data;
- configuration manifests;
- intervention/failure records.

Обычный поток однонаправлен:

```text
Agent / Environment / Runtime
            ↓
     Artifact Collector
            ↓
      Artifact Storage
```

Обратный поток разрешён только explicit operations: restore/resume/replay/load.

`Artifact Storage` не является активной Memory Agent.

```text
Agent Memory
→ часть agent-owned cognition state

Artifact Storage
→ external durable research/training storage
```

Даже если они используют один physical backend, logical ownership различается.

---

# 15. Compute Substrate

Физические ресурсы:

- local CPU/GPU;
- workstation;
- notebook VM;
- Google Colab;
- remote GPU host;
- cloud provider;
- multiple workers/processes.

Compute Substrate не является cognitive architecture.

## Ephemeral compute

MINDRA обязана допускать исчезающий runtime:

- durable artifacts не должны существовать только на ephemeral VM;
- semantic restore не зависит от той же физической VM;
- provider-specific path не становится canonical contract.

Exact recovery/checkpoint requirements — `DU-27`.

---

# 16. Исследователь / оператор

Человек находится вне Agent runtime boundary.

Он отвечает за:

- hypotheses;
- architecture decisions;
- configurations;
- запуск исследований;
- interpretation evidence;
- review;
- ADR acceptance/rejection;
- допустимые claims.

Human feedback может стать training data только через explicit documented path.

Ручное вмешательство в episode не должно выдаваться за autonomous Agent behavior.

---

# 17. External datasets и pretrained artifacts

Weights, datasets, tokenizers и model files находятся вне Agent boundary до явной загрузки.

После загрузки:

- instantiated Cortex является internal capability;
- agent-owned trainable parameters принадлежат Agent;
- source artifact остаётся provenance.

Поведение foundation model не определяет автоматически meaning внутренних MINDRA signals.

---

# 18. Ownership state

| Категория | Логический владелец |
|---|---|
| `CognitiveState` и internal runtime state | MINDRA Agent |
| causally relevant module-private state | MINDRA Agent / semantic module owner |
| active Memory | MINDRA Agent |
| trainable parameters | MINDRA Agent |
| Cortex integration state/adapters | MINDRA Agent |
| Agent scheduling semantics | Agent runtime core |
| Environment hidden/world state | Environment |
| optimizer state | Training Runtime |
| run configuration/seed/experiment identity | Experiment Runner |
| evaluation metrics | Evaluation Runtime / evidence |
| logs/trajectories/snapshot copies | Artifact pipeline |
| archival checkpoint copy | Artifact Storage |
| physical GPU/VM state | Compute Substrate |

Snapshot/copy чужого state не меняет его semantic owner.

---

# 19. Разрешённые потоки данных

## Environment → Agent

Только contract-defined observations, feedback, task/termination signals и public metadata.

## Agent → Environment

Action и contract-defined action metadata.

## Agent/Environment/runtime → artifact pipeline

Наблюдательные копии evidence.

## Training Runtime → Agent

Только explicit Learning Update/state update согласно future training contract.

## Agent/experience → Training Runtime

Разрешённые training inputs/datasets/trajectories/snapshots.

## Agent snapshot → Evaluation Runtime

Evaluation clone/control subject.

## Evaluation Runtime → Agent

По умолчанию normal feedback отсутствует; допускается только explicit intervention channel.

## Artifact Storage → runtime

Explicit restore/resume/replay/load operations с provenance/compatibility checks.

## Execution Runtime → Agent runtime core

Запуск lifecycle и передача разрешённых external inputs. Execution Runtime не передаёт скрытые module-order decisions: active schedule определяется Agent contracts/plan.

---

# 20. Запрещённые скрытые потоки

```text
Evaluation score ─────────────► Policy input
Hidden Environment state ─────► Agent
Test answer/label ─────────────► Agent
Experiment name ──────────────► Agent behavior
Artifact logger result ────────► internal value
GPU/provider identity ─────────► cognition
Training-only privileged data ─► clean evaluation Agent
Other-agent metrics ───────────► tested Agent
Execution Runtime ad-hoc order ─► hidden cognitive semantics
```

Запрет относится к semantic leakage независимо от формы: prompt, global variable, shared object, tensor feature или hidden callback.

---

# 21. Research trust model

## Research Control Plane

Researcher, accepted config, Experiment Runner, Evaluation Runtime и evidence pipeline trusted для постановки/фиксации эксперимента, но не для скрытого решения задачи за Agent.

## Agent Plane

Agent — объект исследования. Его самоотчёт не является evidence собственной корректности.

```text
«я уверен на 95%»
≠
Self Model calibrated
```

## Environment Plane

Environment — источник contract-defined dynamics; observations могут быть неполными, шумными или adversarial в future experiments.

## Infrastructure Plane

Compute/storage/provider trusted operationally в рамках experiment, но не являются источником cognitive meaning/research truth.

---

# 22. Deployment patterns

Архитектура должна допускать при сохранении contracts:

## Local single-process

```text
one process
├─ Environment
├─ Execution Runtime
├─ Agent + Agent runtime core
├─ Training Runtime
└─ recorder
```

Логические границы сохраняются.

## Local multi-process

```text
environment worker
agent worker
training worker
evaluation worker
```

## Notebook / Colab

```text
persistent repository/storage
          ↓
temporary notebook VM
          ↓
Agent / training / evaluation
          ↓
persistent artifacts
```

## Hybrid / distributed

Cortex, training, evaluation или environment workers могут быть распределены без изменения logical ownership.

Первая software version не обязана поддерживать все patterns; canonical architecture только не должна без причины запрещать их.

---

# 23. Research isolation invariants

1. Evaluation Runtime не является normal cognitive signal source.
2. Test-only hidden state не попадает в observation.
3. Artifact Collector не влияет на decision path.
4. Training privileged data не попадает в clean evaluation без explicit condition.
5. Intervention всегда маркируется как intervention.
6. Learning state changes имеют future version/provenance.
7. Deployment change не должен незаметно менять semantics.
8. Human intervention не выдаётся за autonomy.
9. Execution Runtime не создаёт скрытый cognitive order поверх `Cognitive Scheduler`.
10. Scheduler не получает evaluator-only data для выбора module execution.

---

# 24. Evidence, использованное при системном проектировании

## Environment boundary

Gymnasium предоставляет явную `Env` boundary с `reset()`/`step(action)`.

Источник:

- https://gymnasium.farama.org/api/env/

## Collection/training separation

TorchRL поддерживает direct/process/distributed collectors и decoupled collection/training.

Источники:

- https://docs.pytorch.org/rl/main/reference/collectors.html
- https://docs.pytorch.org/rl/main/reference/collectors_single.html

## Separate evaluation

TorchRL поддерживает отдельную evaluation runtime role.

Источник:

- https://docs.pytorch.org/rl/main/reference/collectors_eval.html

## Ephemeral compute

Google Colab использует временные VM с ограниченным lifetime.

Источник:

- https://research.google.com/colaboratory/intl/en-GB/faq.html

Эти инструменты являются evidence реализуемости boundaries, но не обязательными dependencies MINDRA.

---

# 25. Принятые invariants системного контекста

## SC-01

`MINDRA Agent` — logical cognitive system, а не process/VM/GPU.

## SC-02

Environment находится вне Agent boundary.

## SC-03

Cortex является internal logical capability даже при remote backend.

## SC-04

Execution Runtime хостит Agent, но не является cognitive module и не владеет скрытой cognition semantics.

## SC-05

Training Runtime находится вне Agent и изменяет trainable state только через explicit Learning Update boundary.

## SC-06

Evaluation Runtime находится вне Agent; evaluation-derived information по умолчанию недоступна cognition.

## SC-07

Experiment Runner — внешний control-plane component.

## SC-08

Artifact pipeline не влияет на decision path.

## SC-09

Logical state ownership не зависит от storage location.

## SC-10

Deployment topology не определяет architecture semantics.

## SC-11

Agent имеет корректный execution mode без trainer/evaluator.

## SC-12

State-changing cross-boundary operations должны быть explicit/provenance-aware.

## SC-13

Evaluator intervention — только explicit experimental operation.

## SC-14

Compute provider не является cognitive dependency.

## SC-15

Active Agent Memory и Artifact Storage — разные logical entities.

## SC-16

`Cognitive Scheduler` принадлежит Agent runtime core, но не является cognitive module; Execution Runtime может физически хостить его, не получая права переопределять scheduling semantics.

---

# 26. Что этот документ намеренно не решает

Открытыми остаются:

- concrete process/thread model;
- exact Python interfaces;
- concrete state/scheduler framework;
- observability/intervention API;
- Environment API;
- Cortex API;
- trajectory schema;
- optimizer/training algorithm;
- checkpoint schema;
- storage backend;
- concrete local/Colab/cloud workflow.

Уже решённые downstream вопросы не считаются open:

- dependency/composition semantics — `DU-02`;
- logical temporal model — `DU-03`;
- `CognitiveState` semantics — `DU-04`;
- module lifecycle/DAG-wave scheduler semantics — `DU-05`.

---

# 27. Связь с последующими Design Updates

## DU-02

Определяет dependency/composition поверх system boundaries.

## DU-03

Определяет causal temporal semantics известных ролей.

## DU-04

Определяет shared `CognitiveState`, не смешивая его с Environment/evaluator/optimizer/artifact metadata.

## DU-05

Уточняет Agent runtime core и `Cognitive Scheduler`: execution mechanics принадлежат Agent и не становятся внешней hidden orchestration policy.

## DU-06

Определяет observability/intervention boundary между Agent и Research Control Plane без leakage.

## DU-27

Конкретизирует restore/resume/provider-independent persistence.

---

# 28. Completion gate DU-01

Системный контекст считается устойчивым, если для любого будущего объекта можно определить:

1. logical owner;
2. responsibility;
3. допустимые cross-boundary data flows;
4. является ли physical placement semantics или deployment detail.

Текущий следующий Design Update определяется только `current.md`.
