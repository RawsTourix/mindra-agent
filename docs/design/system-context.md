# Системный контекст MINDRA

## Статус документа

**Design Update:** `DU-01 — System Context`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет MINDRA как логическую систему в окружении внешней среды, runtime-инфраструктуры, обучения, оценки, хранения артефактов и вычислительных ресурсов.

Документ намеренно **не** определяет:

- точную структуру `CognitiveState`;
- внутренний порядок выполнения когнитивных модулей;
- Python-интерфейсы;
- process/thread graph;
- конкретный framework;
- конкретную модель Cortex;
- конкретный GPU или compute provider;
- конкретный алгоритм обучения;
- точный формат checkpoint/trajectory.

Эти вопросы принадлежат последующим Design Updates.

---

# 1. Цель DU-01

Основная задача `DU-01` — убрать двусмысленность слова «система» до начала проектирования зависимостей и состояния.

После принятия этого документа должно быть однозначно понятно:

- что является **самим агентом MINDRA**;
- что является **Environment**;
- какие компоненты относятся к исследовательской и training-инфраструктуре;
- где находится Cortex как логическая способность и где может находиться его физическое выполнение;
- кому принадлежит runtime-state, persistent state, параметры и артефакты;
- какие данные могут пересекать системные границы;
- какие потоки данных запрещены как нарушающие исследовательскую валидность;
- почему локальный ПК, Google Colab и будущий удалённый compute не должны менять семантику архитектуры.

---

# 2. Главное архитектурное решение

MINDRA использует **логические границы ответственности, независимые от deployment topology**.

Это означает:

```text
логически разные компоненты
могут физически находиться
в одном Python-процессе / на одном GPU
```

и одновременно:

```text
один логический компонент
может физически исполняться
в другом процессе / на другой машине / удалённом GPU
```

Физическое размещение не изменяет архитектурную принадлежность компонента.

Например:

- `Training Runtime` может временно работать в том же процессе, что и агент, но не становится когнитивным модулем;
- Cortex может исполняться на удалённом GPU, но логически оставаться внутренней способностью агента;
- Memory может использовать внешнее физическое хранилище, но хранимое активное состояние остаётся agent-owned state;
- `Evaluation Runtime` может находиться на том же GPU, но не имеет права превращать evaluation metrics в скрытый вход Policy.

Это решение дополнительно зафиксировано в `ADR-0001`.

---

# 3. Четыре типа границ

Для MINDRA различаются четыре вида границ.

## 3.1. Логическая граница

Определяет, **к какой ответственности относится компонент**.

Пример:

```text
Cortex capability → внутри Agent boundary
Experiment Runner → вне Agent boundary
```

Это главный тип границы для canonical design.

## 3.2. Execution boundary

Определяет, где код фактически выполняется:

- тот же процесс;
- отдельный процесс;
- отдельный worker;
- отдельная машина;
- удалённый runtime.

Execution boundary является implementation/deployment detail до тех пор, пока не меняет наблюдаемую семантику.

## 3.3. Storage boundary

Определяет физическое место хранения:

- RAM;
- VRAM;
- локальный диск;
- внешний диск;
- object storage;
- удалённое хранилище.

Физическое место хранения **не определяет владельца состояния**.

## 3.4. Trust boundary

Определяет, какой компонент считается источником истины для конкретного вида данных и насколько его данные могут использоваться без дополнительной проверки.

В MINDRA trust прежде всего означает **research/integrity trust**, а не полную модель информационной безопасности.

---

# 4. Контекст верхнего уровня

Канонический system context:

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
                │                  │                 │
      ┌─────────▼──────────┐       │       ┌─────────▼──────────┐
      │    MINDRA Agent    │◄──────┘       │ evaluation clone / │
      │                    │               │ controlled subject │
      │ Cortex             │               └────────────────────┘
      │ cognitive modules  │
      │ agent-owned state  │
      └─────────┬──────────┘
                │ observation/action
                ▼
        ┌─────────────────┐
        │   Environment   │
        └─────────────────┘

                  runtime/evaluation/training evidence
                                   │
                                   ▼
                         ┌──────────────────┐
                         │ Artifact Collector│
                         └─────────┬────────┘
                                   ▼
                         ┌──────────────────┐
                         │ Artifact Storage │
                         └──────────────────┘

Все блоки физически размещаются на произвольном Compute Substrate.
```

Схема показывает **логические роли**, а не обязательные процессы.

---

# 5. MINDRA Agent boundary

## 5.1. Что находится внутри

Внутри логической границы агента находятся:

- все принятые когнитивные модули;
- Cortex как логическая capability;
- agent-owned runtime state;
- agent-owned persistent state;
- параметры обучаемых модулей;
- активная память агента;
- agent-owned адаптеры и representations;
- механизмы выбора действий;
- внутренние сигналы, если они являются частью архитектуры.

Точный состав когнитивных модулей определяется последующими `DU`.

## 5.2. Что не находится внутри

В Agent boundary не входят:

- `Environment`;
- `Experiment Runner`;
- `Training Runtime` как механизм оптимизации;
- `Evaluation Runtime`;
- evaluator metrics;
- experiment registry;
- artifact/log collector;
- архивные checkpoint-копии;
- CI;
- Git repository;
- конкретный физический GPU/CPU/VM;
- Google Colab как сервис;
- внешние benchmark labels;
- скрытое состояние Environment, не входящее в observation contract.

## 5.3. Agent должен быть исполним без trainer/evaluator

Канонический invariant:

> Сформированный экземпляр MINDRA Agent должен иметь семантически корректный execution mode без подключённого `Training Runtime` и без подключённого `Evaluation Runtime`.

Это не означает, что необученный агент обязан быть полезным. Это означает, что обучение и оценка не являются скрытыми обязательными частями inference/control path.

---

# 6. Environment boundary

`Environment` — внешний по отношению к агенту источник динамики мира и наблюдаемых последствий действий.

На system-context уровне Environment владеет:

- истинным состоянием мира;
- правилами переходов;
- скрытыми переменными мира;
- episode termination/truncation semantics;
- внешними task conditions;
- объективными внешними сигналами, если они предусмотрены задачей.

Agent получает только то, что разрешено будущим Environment contract.

Минимальный концептуальный поток:

```text
Environment
   │
   ├── observation
   ├── разрешённый external feedback
   ├── termination / truncation information
   └── contract-defined metadata
        ↓
      Agent
        │
        └── action
             ↓
        Environment
```

Environment не должен неявно передавать:

- evaluator verdict;
- test-set answer;
- скрытое правильное действие;
- privileged world state;
- будущие события;
- внутреннюю метрику качества MINDRA,

если это специально не является observation/task contract конкретного эксперимента.

Точная семантика `reset`, `step`, `clone`, `restore`, seeds и branching относится к `DU-07`.

---

# 7. Cortex: логическая и физическая граница

Cortex требует отдельного уточнения, потому что pretrained model может физически выполняться различными способами.

## 7.1. Логически

Cortex является **внутренней capability агента**.

Причина: его outputs участвуют в когнитивном процессе и поведении MINDRA так же, как outputs других внутренних модулей.

## 7.2. Физически

Cortex backend может быть:

- загружен в тот же процесс;
- размещён в отдельном local worker;
- размещён на другом GPU;
- размещён в удалённом runtime;
- предоставлен через внешний inference service,

если будущий `Cortex` contract это допускает.

## 7.3. Cortex Execution Provider

Если физическое выполнение Cortex находится вне основного process/machine boundary, внешний сервис рассматривается как **Cortex Execution Provider**.

Provider не становится самостоятельным когнитивным субъектом архитектуры MINDRA. Он предоставляет вычислительный backend через будущую Cortex integration boundary.

## 7.4. Запрет model leakage

Физические детали Cortex backend не должны неявно проникать в другие модули.

Нельзя строить общую архитектуру вокруг предположений вида:

```text
«у Cortex всегда hidden_size = X»
«Cortex всегда является Qwen»
«Cortex всегда находится на cuda:0»
«Cortex всегда доступен локально»
```

Точные требования Cortex boundary относятся к `DU-10`.

---

# 8. Execution Runtime

`Execution Runtime` — внешняя инфраструктурная роль, которая **хостит исполнение агента**, но не является частью его когнитивной семантики.

Conceptually он отвечает за:

- создание/загрузку экземпляра Agent;
- соединение Agent с Environment;
- передачу разрешённых observation/action;
- запуск runtime lifecycle;
- управление run-level ресурсами;
- остановку/перезапуск исполнения;
- подключение разрешённых observability hooks;
- передачу данных в recorder/collector.

`Execution Runtime` не должен самостоятельно:

- выбирать action за Agent;
- подменять internal value;
- добавлять hidden evaluator feedback;
- интерпретировать evaluation metrics как agent input;
- менять когнитивную семантику в зависимости от deployment topology.

Точный temporal loop относится к `DU-03`.

---

# 9. Training Runtime

`Training Runtime` является **внешней по отношению к логическому Agent инфраструктурой обновления обучаемого состояния**.

На этом уровне design Training Runtime conceptually может:

- читать разрешённый опыт;
- читать training datasets;
- читать snapshot/checkpoint состояния;
- вычислять losses/gradients/updates;
- обновлять agent-owned trainable parameters через явную update boundary;
- поддерживать optimizer-owned state;
- записывать training metrics;
- создавать новые checkpoint snapshots.

Training Runtime не становится когнитивным модулем только потому, что меняет его параметры.

Аналогия:

```text
Agent owns learned parameters
Training Runtime owns optimization procedure/state
```

Точная граница между module-owned learning logic и external optimizer/runtime будет определена в `DU-26`.

---

# 10. Online execution, online learning и offline training

На system-context уровне различаются режимы, но точная временная семантика откладывается до `DU-03` и `DU-26`.

## 10.1. Online execution

Environment развивается, Agent получает observations и выбирает actions.

Допустимы runtime-state updates, являющиеся частью нормальной агентной динамики.

## 10.2. Online learning

Если в будущем будет принят online learning, Training Runtime может работать во время продолжающегося взаимодействия со средой.

При этом обучение остаётся отдельной ответственностью и должно иметь явную provenance обновлений.

Физическая параллельность не является обязательной.

## 10.3. Offline training

Environment time не развивается.

Training Runtime работает с ранее полученным опытом, dataset или snapshot и обновляет параметры без текущего action loop.

## 10.4. Consolidation

`Consolidation` на этом этапе определяется только как отдельная state-changing maintenance phase, которая не обязана совпадать с live environment interaction.

Она может использовать сохранённый опыт для изменения памяти, representations или параметров.

Точное владение consolidation logic распределяется позднее между `DU-20`, `DU-25` и `DU-26`.

---

# 11. Evaluation Runtime

`Evaluation Runtime` — внешний исследовательский компонент, который измеряет поведение Agent и выполняет разрешённые controlled experiments.

Он может:

- загружать snapshot агента;
- создавать evaluation clone;
- запускать Agent в специально выбранном Environment;
- управлять seeds/test distributions;
- отключать или подменять модули через будущие intervention hooks;
- выполнять controlled intervention;
- измерять trajectories и metrics;
- сравнивать конфигурации.

## 11.1. Evaluation isolation invariant

> Evaluation-derived information не должна становиться обычным agent-visible input.

В частности, Agent не получает автоматически:

- итоговый score;
- название experimental condition;
- ожидаемый outcome;
- hidden baseline result;
- правильный ответ benchmark;
- статистику других конфигураций.

## 11.2. Controlled intervention — исключение, а не leakage

Evaluator может намеренно изменить внутреннюю переменную **только** через явный intervention mechanism, когда само вмешательство является частью дизайна эксперимента.

Такое изменение должно быть:

- идентифицируемым;
- воспроизводимым;
- записанным в evidence;
- отделённым от normal execution semantics.

Точный intervention contract относится к `DU-06` и `DU-28`.

---

# 12. Experiment Runner

`Experiment Runner` — внешний control-plane компонент.

Он отвечает за orchestration исследовательского запуска, но не участвует в cognition Agent.

Conceptually он задаёт/фиксирует:

- experiment identity;
- конфигурацию;
- seed;
- dataset/environment selection;
- agent snapshot/configuration;
- runtime mode;
- training/evaluation intent;
- artifact destinations;
- launch/stop status.

Runner не должен превращать run metadata в скрытый agent input.

Например, Agent не должен знать, что текущий запуск называется `ablation_without_memory`, если это не специальная experimental treatment.

---

# 13. Artifact Collector

`Artifact Collector` — пассивная исследовательская инфраструктура наблюдения и сохранения evidence.

Он может получать:

- logs;
- metrics;
- trajectories;
- state snapshots;
- model/module checkpoints;
- profiler data;
- configuration manifests;
- intervention records;
- error/crash reports.

Главный invariant:

> Artifact Collector не является источником поведения Agent.

Обычный runtime data flow должен быть однонаправленным:

```text
Agent / Environment / Runtime
            ↓
     Artifact Collector
            ↓
      Artifact Storage
```

Обратный поток разрешён только для явно определённых операций вроде restore/resume/replay и не должен происходить скрыто.

---

# 14. Artifact Storage

`Artifact Storage` — долговечное внешнее хранилище исследовательских и training-артефактов.

Conceptually здесь могут находиться:

- checkpoints;
- adapters;
- experiment manifests;
- trajectories;
- replay datasets;
- logs;
- evaluation results;
- plots/reports;
- provenance metadata.

Это **не** то же самое, что активная Memory агента.

## 14.1. Active Memory vs Artifact Storage

```text
Agent Memory
→ часть логического Agent state
→ используется cognition по собственному contract

Artifact Storage
→ внешняя исследовательская инфраструктура
→ хранит копии/доказательства/снимки
```

Если физический storage backend используется для активной Memory, сами данные логически остаются agent-owned, а backend рассматривается как infrastructure resource.

---

# 15. Compute Substrate

`Compute Substrate` — физические ресурсы, на которых размещаются логические компоненты.

Примеры допустимых ролей:

- локальный CPU/GPU;
- локальная рабочая станция;
- временная notebook VM;
- Google Colab;
- удалённый GPU-host;
- будущий cloud provider;
- несколько процессов или workers.

Compute Substrate **не является частью когнитивной архитектуры**.

Канонический design не должен требовать конкретного provider, пока это не является сознательно принятым operational constraint.

## 15.1. Ephemeral compute

Архитектура должна допускать временный compute runtime, который может исчезнуть между запусками.

Следствие:

- долговечные артефакты не должны существовать только в ephemeral runtime;
- восстановление не должно зависеть от сохранения конкретной VM;
- provider-specific filesystem path не должен становиться частью semantic contract.

Точные checkpoint/recovery требования относятся к `DU-27`.

---

# 16. Исследователь / оператор

Человек находится вне runtime Agent boundary.

Его роли:

- формулирование гипотез;
- принятие architecture decisions;
- подготовка конфигураций;
- запуск исследований;
- интерпретация evidence;
- review изменений;
- принятие/отклонение ADR;
- определение допустимых claims.

Human feedback может когда-либо стать training data, но только через явный documented data/training path.

Ручное вмешательство исследователя в конкретный episode не должно маскироваться под autonomous Agent behavior.

---

# 17. Внешние datasets и pretrained artifacts

Training data, pretrained weights, tokenizers, model files и другие импортируемые artifacts находятся **вне Agent boundary до загрузки через явный resource/configuration path**.

После загрузки:

- instantiated Cortex остаётся внутренней capability;
- agent-owned trainable parameters становятся частью состояния агента;
- исходный external artifact остаётся provenance/source artifact.

Сторонний pretrained artifact не является каноническим источником архитектурной семантики.

Поведение конкретной foundation model не должно молча определять meaning внутренних MINDRA signals.

---

# 18. Владение состоянием

На system-context уровне принимается следующая семантика ownership.

| Категория | Логический владелец |
|---|---|
| внутренний runtime state Agent | MINDRA Agent |
| активная Memory Agent | MINDRA Agent |
| trainable parameters модулей | MINDRA Agent |
| Cortex integration state/adapters | MINDRA Agent |
| Environment hidden/world state | Environment |
| optimizer state | Training Runtime |
| run configuration / seed / experiment identity | Experiment Runner |
| evaluation metrics | Evaluation Runtime / experiment evidence |
| logs / trajectories / snapshots | Artifact pipeline |
| архивная копия checkpoint | Artifact Storage |
| физический GPU/VM state | Compute Substrate |

Важно:

> snapshot чужого состояния не меняет его логического владельца.

Например, checkpoint в Artifact Storage является сохранённой копией agent-owned state, но само хранилище не становится когнитивным владельцем этих параметров.

---

# 19. Разрешённые потоки данных

## 19.1. Environment → Agent

Разрешены только contract-defined:

- observations;
- external feedback;
- episode/task signals;
- termination/truncation;
- публичная metadata.

## 19.2. Agent → Environment

- action;
- при необходимости contract-defined action metadata.

## 19.3. Agent/Environment → recorder/artifact pipeline

Разрешены наблюдательные копии:

- trajectory events;
- diagnostics;
- snapshots;
- metrics;
- provenance.

## 19.4. Training Runtime → Agent

Разрешены явные state/parameter updates согласно будущему training contract.

## 19.5. Agent/Experience Storage → Training Runtime

Разрешены training inputs, datasets, trajectories, snapshots.

## 19.6. Agent snapshot → Evaluation Runtime

Evaluator может получить frozen/copy state для controlled evaluation.

## 19.7. Evaluation Runtime → Agent

По умолчанию — **нет нормального feedback-потока**.

Допустим только явный intervention/control channel в соответствующем experimental mode.

## 19.8. Artifact Storage → runtime

Разрешены только явные операции:

- restore;
- resume;
- replay;
- load pretrained artifact;
- load configuration,

с provenance и проверкой совместимости в будущих contracts.

---

# 20. Запрещённые скрытые потоки

Следующие потоки являются архитектурным нарушением, если не оформлены как специальное experiment condition:

```text
Evaluation score ───────────────► Policy input
Hidden Environment state ───────► Agent
Test answer/label ───────────────► Agent
Experiment name ────────────────► Agent behavior
Artifact logger result ─────────► internal value
GPU/provider identity ──────────► cognition
Training-only privileged data ──► normal evaluation Agent
Other-agent metrics ────────────► tested Agent
```

Запрет относится к **семантическому leakage**, а не только к прямому Python-вызову.

Если информация косвенно попадает в prompt, feature vector, shared object или global variable, это всё равно пересечение границы.

---

# 21. Trust model

MINDRA вводит минимальную research-oriented trust model.

## 21.1. Research Control Plane

Включает:

- researcher/operator;
- accepted configuration;
- Experiment Runner;
- Evaluation Runtime;
- artifact/evidence pipeline.

Эта область считается trusted для постановки эксперимента и сохранения evidence.

При этом она **не должна быть агенту источником скрытого решения задачи**.

## 21.2. Agent Plane

Agent является объектом исследования.

Его outputs не считаются доказательством собственной корректности.

Например:

```text
Agent сказал «я уверен на 95%»
≠
Self Model действительно calibrated
```

## 21.3. Environment Plane

Environment является источником contract-defined world dynamics.

Agent-visible данные Environment считаются входом, который может быть:

- неполным;
- шумным;
- неожиданным;
- adversarial в будущих experiments.

## 21.4. Infrastructure Plane

Compute/storage/provider могут считаться operationally trusted для исполнения/хранения в рамках выбранного эксперимента, но не являются источником когнитивной семантики или research truth.

Сторонние weights/datasets требуют provenance и будущих reproducibility checks.

Полная security threat model в `DU-01` не проектируется.

---

# 22. Deployment patterns, которые обязана допускать архитектура

Следующие схемы считаются семантически эквивалентными, если contracts и результаты исполнения сохранены.

## 22.1. Local single-process

```text
одна машина
└── один process
    ├── Environment
    ├── Agent
    ├── Training Runtime
    └── recorder
```

Логические границы всё равно сохраняются.

## 22.2. Local multi-process

```text
local machine
├── environment worker
├── agent worker
├── training worker
└── evaluator worker
```

## 22.3. Notebook / Colab runtime

```text
persistent repository/storage
          ↓
 temporary notebook VM
          ↓
   Agent / train / eval
          ↓
 persistent artifacts
```

## 22.4. Hybrid local + remote compute

```text
local control plane
        ↓
remote compute
├── Cortex backend
├── training
└── evaluation
        ↓
external/persistent artifact storage
```

## 22.5. Future distributed execution

Несколько workers/devices могут выполнять разные роли без изменения logical ownership.

`DU-01` не требует поддержки всех схем в первой software version. Он запрещает архитектурные решения, которые **без необходимости делают одну из схем единственно возможной**.

---

# 23. Research isolation rules

Для сохранения валидности экспериментов принимаются следующие invariants.

1. `Evaluation Runtime` не является источником обычных cognitive signals.
2. Test-only hidden state не попадает в Agent observation.
3. Artifact Collector не влияет на decision path.
4. Training-specific privileged data не используется в clean evaluation без явного условия.
5. Любой evaluator intervention записывается как intervention, а не normal behavior.
6. Любое состояние, изменённое Training Runtime, должно иметь version/provenance в будущем design.
7. Deployment change не должен незаметно менять experimental semantics.
8. Human intervention не должен выдаваться за autonomous behavior.

---

# 24. Research evidence, использованное при проектировании DU-01

`DU-01` не выбирает конкретный framework, но существующие реализации подтверждают практичность разделения логических ролей.

## 24.1. Environment boundary

Gymnasium определяет `Env` как объект динамики среды с явными `reset()` и `step(action)` и отделяет observation/reward/termination от самого агента.

Источник:

- [Gymnasium — Env](https://gymnasium.farama.org/api/env/)

Это не делает Gymnasium обязательной зависимостью MINDRA; используется только как evidence зрелости явной agent/environment boundary.

## 24.2. Collection и training могут быть разнесены

TorchRL collectors поддерживают direct, process и distributed execution, а асинхронный collector может собирать опыт независимо от training loop.

Источники:

- [TorchRL — collectors](https://docs.pytorch.org/rl/main/reference/collectors.html)
- [TorchRL — single node collectors](https://docs.pytorch.org/rl/main/reference/collectors_single.html)

Это подтверждает, что semantic separation collection/training совместима как с простым, так и с распределённым execution.

## 24.3. Evaluation может быть отдельной runtime-ролью

TorchRL `Evaluator` поддерживает синхронную, асинхронную и process-separated evaluation с передачей weights.

Источник:

- [TorchRL — Evaluation](https://docs.pytorch.org/rl/main/reference/collectors_eval.html)

MINDRA принимает более строгий research invariant: evaluation-derived metrics не становятся normal agent inputs.

## 24.4. Compute runtime может быть временным

Google Colab выполняет код в VM, которая удаляется после периода бездействия и имеет ограниченный lifetime.

Источник:

- [Google Colab — FAQ](https://research.google.com/colaboratory/intl/en-GB/faq.html)

Это является практическим основанием отделять durable artifacts от ephemeral compute, но Google Colab не становится каноническим runtime MINDRA.

---

# 25. Принятые invariants DU-01

После этого Design Update считаются принятыми следующие положения.

## SC-01

`MINDRA Agent` является логической когнитивной системой, а не процессом, VM или GPU.

## SC-02

`Environment` находится вне Agent boundary.

## SC-03

Cortex является внутренней логической capability Agent, даже если его backend физически выполняется удалённо.

## SC-04

`Execution Runtime` хостит Agent, но не является когнитивным модулем.

## SC-05

`Training Runtime` находится вне Agent boundary и обновляет agent-owned trainable state только через явную update boundary.

## SC-06

`Evaluation Runtime` находится вне Agent boundary; evaluation-derived information по умолчанию недоступна Agent.

## SC-07

`Experiment Runner` является внешним control-plane компонентом и не участвует в cognition.

## SC-08

`Artifact Collector/Storage` являются внешней инфраструктурой и не должны скрыто влиять на decision path.

## SC-09

Логическое владение state не зависит от физического storage location.

## SC-10

Deployment topology не определяет architecture semantics.

## SC-11

Agent должен иметь корректный execution mode без подключённых Training/Evaluation Runtime.

## SC-12

Все state-changing cross-boundary operations должны быть явными и в будущем иметь provenance.

## SC-13

Evaluator interventions допустимы только как явно обозначенные experimental operations.

## SC-14

Compute provider не является canonical cognitive dependency.

## SC-15

Active Agent Memory и external Artifact Storage являются разными логическими сущностями даже при общем физическом backend.

---

# 26. Что DU-01 намеренно не решает

Открытыми остаются:

- import/dependency graph;
- composition root;
- plugin/registry semantics;
- process model;
- thread model;
- sync/async runtime semantics;
- exact step ordering;
- `CognitiveState` representation;
- module lifecycle;
- scheduler;
- observability API;
- intervention API;
- Environment API;
- Cortex API;
- trajectory schema;
- optimizer/training algorithm;
- checkpoint schema;
- exact storage backend;
- concrete local/Colab/cloud workflow.

Эти вопросы не должны решаться implementation-ом раньше соответствующих Design Updates.

---

# 27. Последствия для следующих Design Updates

## DU-02 — Dependency & Composition Rules

Должен построить dependency model на основе принятых логических границ.

Особенно:

- cognitive modules не должны зависеть от Experiment Runner;
- Agent не должен импортировать evaluator logic;
- training code не должен становиться implicit runtime dependency inference path;
- concrete Cortex backend не должен протекать за Cortex boundary;
- infrastructure backends не должны определять semantic ownership.

## DU-03 — Runtime / Temporal Model

Должен определить temporal semantics уже известных ролей:

- online execution;
- environment progression;
- online learning;
- offline training;
- consolidation;
- evaluation-only execution.

## DU-04 — CognitiveState

Должен описать внутренний agent-owned state, не смешивая его с:

- Environment hidden state;
- evaluator metadata;
- optimizer state;
- experiment metadata;
- artifact metadata.

## DU-06 — Observability & Intervention

Должен определить controlled research boundary между Agent и Evaluation Runtime без leakage.

## DU-27 — Checkpoint / Reproducibility / Compute

Должен конкретизировать restore/resume и provider-independent artifact persistence поверх принятых logical/storage boundaries.

---

# 28. Completion gate DU-01

`DU-01` считается завершённым, если для любого будущего объекта можно сначала ответить на два вопроса:

1. **Кому он логически принадлежит?**
2. **Является ли его физическое размещение архитектурной семантикой или только deployment detail?**

После принятия этого документа следующий допустимый Design Update:

```text
DU-02 — Dependency & Composition Rules
```
