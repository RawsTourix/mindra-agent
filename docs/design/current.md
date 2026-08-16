# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-05` завершены и приняты. Реализация ещё не начата.**

На текущем этапе зафиксированы:

- концепция проекта;
- архитектурная концепция;
- исследовательская методология;
- базовые принципы проектирования;
- глоссарий;
- правила для coding agents;
- реестры ADR, точных контрактов и будущих версий;
- карта кандидатных модулей;
- канонический порядок `DU-00` … `DU-32`;
- системный контекст;
- dependency/composition model;
- runtime/temporal model;
- canonical `CognitiveState` semantics;
- module lifecycle и scheduler semantics;
- пять accepted ADR.

---

# 2. Завершённые Design Updates

```text
DU-00 — Documentation Foundation
DU-01 — System Context
DU-02 — Dependency & Composition Rules
DU-03 — Runtime / Temporal Model
DU-04 — CognitiveState Semantics
DU-05 — Module Protocol & Scheduling
```

## DU-01

Канонический документ:

- [`system-context.md`](system-context.md).

Основные результаты:

- Agent определяется логической ответственностью, а не process/VM/GPU;
- Environment, Training Runtime, Evaluation Runtime и research infrastructure отделены от cognition;
- Cortex является внутренней capability Agent независимо от physical deployment;
- evaluation-derived data не становится обычным agent input.

Accepted decision:

- [`ADR-0001`](decisions/ADR-0001-logical-boundaries-independent-of-deployment.md).

## DU-02

Канонический документ:

- [`dependency-rules.md`](dependency-rules.md).

Основные результаты:

- concrete implementations собираются через явный Composition Root;
- runtime Service Locator/shared mutable globals запрещены;
- cognitive modules не зависят от concrete peers;
- Agent/core не зависит от Training/Evaluation Runtime;
- NoOp/Dummy/Control подключаются через ту же composition semantics.

Accepted decision:

- [`ADR-0002`](decisions/ADR-0002-explicit-composition-no-runtime-service-locator.md).

## DU-03

Канонический документ:

- [`execution-model.md`](execution-model.md).

Основные результаты:

- canonical time является логическим причинным временем;
- различаются Run, Agent Session, Episode, Decision Window, Cognitive Cycle и Environment Transition;
- один action может предваряться несколькими внутренними cycles;
- Action Commit/Outcome Commit являются causal boundaries;
- runtime state update отделён от Learning Update;
- replay/imagined/counterfactual transitions не смешиваются с observed transitions;
- causal replay является архитектурной целью.

Accepted decision:

- [`ADR-0003`](decisions/ADR-0003-hierarchical-logical-time.md).

## DU-04

Канонический документ:

- [`cognitive-state.md`](cognitive-state.md).

Основные результаты:

- `CognitiveState` является canonical published shared runtime state, а не всем `Agent-owned state`;
- committed snapshots семантически неизменяемы;
- изменения публикуются через owner-scoped proposed updates;
- canonical paths имеют одного semantic write owner;
- `available`, `unknown`, `stale`, `unavailable` и structural `missing` различаются;
- state values имеют provenance/freshness/scope;
- private causally relevant state не скрывается от snapshot requirements;
- model-specific hidden state не протекает в canonical shared state;
- counterfactual fork начинается только из identifiable committed revision.

Accepted decision:

- [`ADR-0004`](decisions/ADR-0004-versioned-committed-cognitive-state.md).

## DU-05

Канонический документ:

- [`module-lifecycle.md`](module-lifecycle.md).

Основные результаты:

- каждый модуль имеет declarative descriptor с reads/writes/lifecycle/private-state semantics;
- execution order строится из declared dependencies, freshness и lifecycle constraints;
- instantaneous scheduler graph является DAG;
- ready modules группируются в execution waves;
- modules одной wave читают одну base `state_revision` и `agent_revision`;
- physical completion order внутри wave не определяет semantics;
- public proposed updates и causally relevant private-state effects commit согласованно;
- overlapping writers запрещены без отдельного reducer/owner;
- stale-base result не применяется молча;
- lifecycle boundaries стандартизированы;
- scheduler не выполняет optimizer learning;
- `disabled`, `NoOp` и `Control` имеют разные явные semantics;
- module failure по умолчанию не оставляет partial wave commit;
- future Executive Control ограничен admissible scheduler semantics;
- recursive peer execution и hidden dynamic Service Locator запрещены.

Accepted decision:

- [`ADR-0005`](decisions/ADR-0005-wave-scheduled-module-protocol.md).

---

# 3. Следующий допустимый Design Update

```text
DU-06 — Observability & Intervention
```

Цель `DU-06` — сделать исследовательскую наблюдаемость и controlled intervention частью архитектуры до проектирования конкретных когнитивных модулей.

Обязательные области:

```text
execution-plan tracing
wave/module attempt tracing
state revision tracing
public/private-state observability boundary
metrics/events
intervention targeting
intervention provenance
counterfactual fork
snapshot capture
replay/capture requirements
debug metadata vs cognitive payload
Cortex activation size/privacy boundaries
```

Нужно определить:

- что именно evaluator/collector может наблюдать;
- как наблюдать private state без разрушения encapsulation;
- где допустимо вмешательство в canonical state;
- как override не меняет semantic owner;
- как фиксируется natural vs intervened value;
- на каких committed boundaries разрешён fork;
- как tracing не становится скрытым input Agent;
- что нужно записывать для causal reconstruction wave/module execution;
- как не превратить observability в зависимость cognition от logger/evaluator.

После принятия `DU-06` допускается:

```text
DU-07 — Environment / MicroWorld Contract
```

---

# 4. Действующие фундаментальные отношения

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
committed snapshot
≠
mutable shared bus
```

```text
semantic lifetime
≠
historical retention
≠
checkpoint inclusion
```

```text
scheduler mechanics
≠
cognitive decision policy
```

```text
runtime state update
≠
Learning Update
```

---

# 5. Действующие scheduler/module invariants

До явного изменения canonical design запрещаются:

- module → concrete peer imports/calls;
- runtime Service Locator внутри cognitive/runtime code;
- undeclared state reads;
- direct mutation committed `CognitiveState`;
- canonical inplace mutation через retained references;
- скрытый `last-write-wins`;
- overlapping writers без reducer/owner;
- ordering по registration/import/completion order;
- instantaneous dependency cycles;
- recursive peer/scheduler execution из module compute;
- применение stale-base result без explicit semantics;
- изменение `agent_revision` внутри in-flight wave;
- partial public/private wave commit;
- hidden behavior-changing fallback;
- скрытая private-state mutation до failed public commit;
- ad-hoc lifecycle calls конкретных module classes из main loop;
- скрытый optimizer update внутри normal compute;
- использование batch completion order как causal order;
- irreversible causally visible side effect до explicit commit/boundary без специального design.

---

# 6. Что ещё не принято

Пока отсутствуют accepted решения по:

- exact `CognitiveState` container/API;
- exact Python `ModuleProtocol`;
- concrete scheduler/DAG implementation;
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

Также пока не выбраны:

- exact Python package tree;
- `Protocol`/ABC/interface mechanism;
- DI/config framework;
- plugin/registry implementation;
- TensorDict/dataclass/Pydantic state framework;
- graphlib/NetworkX/другая scheduler graph library;
- asyncio/Ray/другой parallel runtime;
- concrete copy-on-write/private-state transaction mechanism;
- concrete architecture-test tool.

---

# 7. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начинать implementation до появления version roadmap и implementation sequence.

---

# 8. Запрещённый преждевременный scope

До соответствующего Design Update не фиксировать как обязательные:

- конкретный Cortex backend;
- TensorDict или другой state framework;
- PPO/GRPO/Dreamer или другой learning algorithm;
- RND/ICM или конкретный curiosity mechanism;
- FAISS/vector DB или конкретный Memory backend;
- PEFT/LoRA/QLoRA как tuning mechanism;
- Google Colab как единственный runtime;
- конкретные latent dimensions;
- окончательную структуру `src/`;
- exact Python module interfaces;
- concrete scheduler/async framework;
- отдельный Workspace/Affect/Executive Control только на основании когнитивной аналогии.

---

# 9. Канонические ссылки

- порядок Design Updates: [`documentation-plan.md`](documentation-plan.md);
- системный контекст: [`system-context.md`](system-context.md);
- dependency/composition: [`dependency-rules.md`](dependency-rules.md);
- runtime/temporal model: [`execution-model.md`](execution-model.md);
- `CognitiveState`: [`cognitive-state.md`](cognitive-state.md);
- module lifecycle/scheduling: [`module-lifecycle.md`](module-lifecycle.md);
- ADR registry: [`decisions/README.md`](decisions/README.md);
- карта областей: [`modules/README.md`](modules/README.md);
- общие принципы: [`principles.md`](principles.md);
- термины: [`glossary.md`](glossary.md);
- исследовательская дисциплина: [`../research-methodology.md`](../research-methodology.md).
