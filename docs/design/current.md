# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что фактически уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-04` завершены и приняты. Реализация ещё не начата.**

На текущем этапе зафиксированы:

- концепция проекта;
- архитектурная концепция;
- исследовательская методология;
- базовые принципы проектирования;
- глоссарий;
- правила для coding agents;
- реестры ADR, точных контрактов и будущих версий;
- карта кандидатных модулей и архитектурных областей;
- канонический порядок `DU-00` … `DU-32`;
- системный контекст MINDRA;
- dependency/composition model;
- runtime/temporal model;
- canonical `CognitiveState` semantics;
- четыре accepted ADR.

---

# 2. Завершённые Design Updates

```text
DU-00 — Documentation Foundation
DU-01 — System Context
DU-02 — Dependency & Composition Rules
DU-03 — Runtime / Temporal Model
DU-04 — CognitiveState Semantics
```

## DU-01

Канонический документ:

- [`system-context.md`](system-context.md).

Главные результаты:

- `MINDRA Agent` является логической когнитивной системой, а не process/VM/GPU;
- `Environment`, `Training Runtime`, `Evaluation Runtime`, `Experiment Runner` и artifact infrastructure находятся за отдельными логическими границами;
- Cortex является внутренней capability Agent, даже если backend физически исполняется удалённо;
- deployment topology не определяет architecture semantics;
- evaluation-derived information не является normal agent-visible input.

Accepted decision:

- [`ADR-0001`](decisions/ADR-0001-logical-boundaries-independent-of-deployment.md).

## DU-02

Канонический документ:

- [`dependency-rules.md`](dependency-rules.md).

Главные результаты:

- concrete implementations разрешаются на явной composition boundary;
- принят `Composition Root` как logical owner сборки конкретного запуска;
- потребители получают зависимости явно и не используют runtime Service Locator;
- registry допустим только как composition/discovery catalogue;
- cognitive modules по умолчанию не владеют concrete references на peers;
- runtime feedback loops не должны превращаться в static dependency cycles;
- shared mutable globals запрещены как межмодульный state mechanism;
- Agent/core не зависит от Training/Evaluation Runtime;
- concrete Cortex/provider details изолируются за capability boundary;
- no-op/dummy/control implementations подключаются через ту же composition semantics;
- behavior-changing fallback обязан быть явным и наблюдаемым.

Accepted decision:

- [`ADR-0002`](decisions/ADR-0002-explicit-composition-no-runtime-service-locator.md).

## DU-03

Канонический документ:

- [`execution-model.md`](execution-model.md).

Главные результаты:

- canonical time MINDRA является логическим причинным временем, а не wall-clock;
- различаются `Run`, `Agent Session`, `Episode`, `Decision Window`, `Cognitive Cycle` и `Environment Transition`;
- один внешний action может предваряться несколькими внутренними Cognitive Cycle;
- `Action Commit` и `Outcome Commit` являются причинными boundaries;
- runtime state update отделён от Learning Update;
- Replay, Consolidation и imagined trajectories имеют собственную temporal/provenance semantics и не создают fake Environment steps;
- physical sync/async execution допустим при сохранении однозначного causal order trajectory;
- async collection/training требует provenance Agent revision;
- `Environment.reset()` закрывает/создаёт Episode, но не равен полному reset Agent Session;
- termination и truncation сохраняются раздельно;
- clean evaluation по умолчанию запрещает trainable Learning Updates, но не выключает нормальную runtime-динамику Agent;
- causal replay является обязательной архитектурной целью, bitwise replay — best-effort свойством concrete runtime.

Accepted decision:

- [`ADR-0003`](decisions/ADR-0003-hierarchical-logical-time.md).

## DU-04

Канонический документ:

- [`cognitive-state.md`](cognitive-state.md).

Главные результаты:

- `CognitiveState` определён как canonical published shared runtime state, а не полный `Agent-owned state`;
- committed state snapshot семантически неизменяем;
- изменения публикуются через owner-scoped proposed updates и новую state revision;
- partial staged writes не являются видимым committed state;
- canonical path имеет однозначного semantic write owner;
- `last-write-wins` запрещён как default conflict semantics;
- read dependencies должны быть declared, наличие поля в state не создаёт implicit dependency;
- различаются `available`, `unknown`, `stale`, `unavailable` и structural `missing`;
- magic sentinel (`0`, `NaN`, `None` и т. п.) не заменяет availability semantics;
- published values должны иметь temporal/provenance context;
- observed/predicted/retrieved/intervened information не должна становиться неразличимой;
- введены scopes `cycle`, `decision`, `episode`, `session`, `agent-long-lived`;
- semantic lifetime отделён от artifact retention и checkpoint policy;
- causally relevant module-private state допускается, но не может быть скрыто от будущих snapshot/reproducibility requirements;
- Cortex/model-specific hidden state и полный Memory storage не обязаны входить в `CognitiveState`;
- batching/device placement не определяют semantic identity;
- `CognitiveState` должен быть conceptually serializable без live infrastructure objects;
- counterfactual fork начинается из identifiable committed revision и сохраняет lineage;
- clone `CognitiveState` не равен full Agent clone.

Accepted decision:

- [`ADR-0004`](decisions/ADR-0004-versioned-committed-cognitive-state.md).

---

# 3. Следующий допустимый Design Update

```text
DU-05 — Module Protocol & Scheduling
```

Цель `DU-05` — определить единый lifecycle cognitive modules и способ причинно корректного scheduling поверх committed `CognitiveState`.

Обязательные области:

```text
module identity / capability
initialize
reset
read committed state
compute
propose update
commit coordination
observe outcome
runtime-state update
train/eval mode
learn/update hooks
checkpoint/restore hooks
shutdown
```

Также предстоит определить:

- как модуль объявляет read/write dependencies;
- какие lifecycle hooks обязательны/опциональны;
- кто формирует state projections;
- как scheduler строит порядок вычислений;
- где допустимо parallel compute;
- commit granularity;
- stale-base/conflict handling;
- cycle prevention;
- semantics disabled/NoOp/Control implementations;
- error/degradation behavior;
- отношение fixed scheduler к будущему Executive Control;
- batch/vectorized execution.

После принятия `DU-05` допускается:

```text
DU-06 — Observability & Intervention
```

---

# 4. Действующие фундаментальные границы

Канонически различаются:

```text
MINDRA Agent
Environment
Execution Runtime
Training Runtime
Evaluation Runtime
Experiment Runner
Artifact Collector / Artifact Storage
Compute Substrate
Cortex Execution Provider
Composition Root
```

И временные уровни:

```text
Run
Agent Session
Episode
Decision Window
Cognitive Cycle
Action Commit
Environment Transition
Outcome Commit
Learning Update
Replay Step
Consolidation Event
```

Для state дополнительно различаются:

```text
CognitiveState
module-private state
trainable parameters
active Memory storage
Cortex-private/backend state
stochastic state
```

Главные relations:

```text
logical architecture boundary
≠
process / device / machine boundary
```

```text
runtime feedback cycle
≠
static dependency cycle
```

```text
logical causal time
≠
wall-clock
```

```text
Cognitive Cycle
≠
Environment Transition
```

```text
CognitiveState
≠
full Agent-owned state
```

```text
semantic lifetime
≠
historical retention
≠
checkpoint inclusion
```

---

# 5. Действующие state/dependency/temporal invariants

До их явного изменения через design/ADR запрещаются:

- module → concrete peer imports;
- cognitive/runtime code → global Service Locator;
- shared mutable global state для cognition;
- direct mutation committed CognitiveState;
- inplace mutation canonical value через retained reference;
- implicit `last-write-wins` для конфликтующих canonical paths;
- неявная зависимость модуля от произвольного присутствующего state field;
- использование magic sentinel вместо declared availability semantics;
- смешивание observation/prediction/retrieval/intervention без provenance;
- Agent/core → trainer/evaluator imports;
- independent module → concrete Cortex backend/provider SDK;
- runtime core → backend-specific behavior branches;
- cross-module direct private-state mutation;
- scattered ablation flags вместо composition substitution;
- hidden behavior-changing fallback;
- dynamic plugin discovery внутри cognitive step;
- использование wall-clock как неявного cognitive clock;
- трактовка internal reasoning cycle как Environment step;
- ретроактивное изменение committed action/outcome/state revision;
- смешивание replay/imagined transition с observed Environment transition;
- неявный полный reset Agent при `Environment.reset()`;
- использование batch completion order как causal order независимых trajectories.

---

# 6. Что ещё не принято

Пока отсутствуют accepted решения по:

- exact `CognitiveState` container/API;
- module lifecycle/scheduling;
- observability/intervention contract;
- Environment/MicroWorld;
- Perception representation;
- Goal System;
- Cortex contract/backend;
- Memory Core;
- World Model;
- Self Model;
- intrinsic signals;
- Drives;
- Appraisal;
- Affect Dynamics;
- Valuation;
- Salience/Attention;
- Memory Regulation/Consolidation;
- Workspace;
- Metacognitive/Executive Control;
- Policy/Planner;
- Action boundary;
- trajectory/data/replay schema;
- training lifecycle;
- checkpointing/reproducibility;
- exact evaluation harness;
- testing strategy;
- research claims/limitations;
- version roadmap;
- implementation sequences.

Также пока **не выбраны**:

- exact Python package tree;
- `Protocol`/ABC/другой interface mechanism;
- DI/config framework;
- registry implementation;
- plugin `entry points`;
- concrete scheduler;
- async framework;
- TensorDict/dataclass/Pydantic/другой state framework;
- concrete copy-on-write/immutability implementation;
- concrete architecture-test tool.

---

# 7. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начать implementation до появления version roadmap и implementation sequence.

---

# 8. Запрещённый преждевременный scope

До соответствующего Design Update не фиксировать как обязательные:

- Qwen/Gemma/Llama или другую конкретную модель Cortex;
- TensorDict или другой framework состояния;
- PPO/GRPO/Dreamer или другой learning algorithm;
- RND/ICM или конкретный curiosity mechanism;
- FAISS/vector DB или конкретный backend памяти;
- PEFT/LoRA/QLoRA как обязательный tuning mechanism;
- Google Colab как единственный runtime;
- конкретные latent dimensions;
- окончательную структуру `src/`;
- конкретное число Cognitive Cycle;
- конкретный scheduler/async framework;
- exact `CognitiveState` Python type;
- отдельный Workspace/Affect/Executive Control только на основании когнитивной аналогии.

Эти варианты остаются кандидатами для targeted research/design comparison.

---

# 9. Канонические ссылки

- порядок Design Updates: [`documentation-plan.md`](documentation-plan.md);
- системный контекст: [`system-context.md`](system-context.md);
- dependency/composition rules: [`dependency-rules.md`](dependency-rules.md);
- runtime/temporal model: [`execution-model.md`](execution-model.md);
- CognitiveState semantics: [`cognitive-state.md`](cognitive-state.md);
- ADR registry: [`decisions/README.md`](decisions/README.md);
- карта областей: [`modules/README.md`](modules/README.md);
- общие принципы: [`principles.md`](principles.md);
- термины: [`glossary.md`](glossary.md);
- исследовательская дисциплина: [`../research-methodology.md`](../research-methodology.md).
