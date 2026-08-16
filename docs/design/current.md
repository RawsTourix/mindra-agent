# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что фактически уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01`, `DU-02` и `DU-03` завершены и приняты. Реализация ещё не начата.**

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
- три accepted ADR.

---

# 2. Завершённые Design Updates

```text
DU-00 — Documentation Foundation
DU-01 — System Context
DU-02 — Dependency & Composition Rules
DU-03 — Runtime / Temporal Model
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
- causal replay является обязательной архитектурной целью, bitwise replay — best-effort свойством конкретного runtime.

Accepted decision:

- [`ADR-0003`](decisions/ADR-0003-hierarchical-logical-time.md).

---

# 3. Следующий допустимый Design Update

```text
DU-04 — CognitiveState Semantics
```

Цель `DU-04` — спроектировать каноническую модель внутреннего состояния поверх уже принятых system/dependency/temporal boundaries.

Обязательные вопросы:

```text
state categories
ownership
cycle/decision/episode/session/persistent scopes
observed/derived/predicted state
read/write semantics
unknown/missing/stale
provenance
temporal versioning
clone/counterfactual requirements
serialization/checkpoint compatibility
batch/device/dtype independence
model-specific hidden state isolation
```

После принятия `DU-04` допускается:

```text
DU-05 — Module Protocol & Scheduling
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

---

# 5. Действующие dependency/temporal invariants

До их явного изменения через design/ADR запрещаются:

- module → concrete peer imports;
- cognitive/runtime code → global Service Locator;
- shared mutable global state для cognition;
- Agent/core → trainer/evaluator imports;
- independent module → concrete Cortex backend/provider SDK;
- runtime core → backend-specific behavior branches;
- cross-module direct private-state mutation;
- scattered ablation flags вместо composition substitution;
- hidden behavior-changing fallback;
- dynamic plugin discovery внутри cognitive step;
- использование wall-clock как неявного cognitive clock;
- трактовка internal reasoning cycle как Environment step;
- ретроактивное изменение уже committed action/outcome;
- смешивание replay/imagined transition с observed Environment transition;
- неявный полный reset Agent при `Environment.reset()`;
- использование batch completion order как causal order независимых trajectories.

---

# 6. Что ещё не принято

Пока отсутствуют accepted решения по:

- canonical `CognitiveState`;
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
- state bus implementation;
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
- отдельный Workspace/Affect/Executive Control только на основании когнитивной аналогии.

Эти варианты остаются кандидатами для targeted research/design comparison.

---

# 9. Канонические ссылки

- порядок Design Updates: [`documentation-plan.md`](documentation-plan.md);
- системный контекст: [`system-context.md`](system-context.md);
- dependency/composition rules: [`dependency-rules.md`](dependency-rules.md);
- runtime/temporal model: [`execution-model.md`](execution-model.md);
- ADR registry: [`decisions/README.md`](decisions/README.md);
- карта областей: [`modules/README.md`](modules/README.md);
- общие принципы: [`principles.md`](principles.md);
- термины: [`glossary.md`](glossary.md);
- исследовательская дисциплина: [`../research-methodology.md`](../research-methodology.md).
