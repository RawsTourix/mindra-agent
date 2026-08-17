# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-06` завершены и приняты. Реализация ещё не начата.**

На текущем этапе зафиксированы:

- концепция проекта;
- архитектурная концепция;
- исследовательская методология;
- базовые принципы проектирования;
- глоссарий;
- правила для coding agents;
- реестры ADR, exact contracts и будущих версий;
- карта кандидатных модулей;
- канонический порядок `DU-00` … `DU-32`;
- системный контекст;
- dependency/composition model;
- runtime/temporal model;
- canonical `CognitiveState` semantics;
- module lifecycle и scheduler semantics;
- observability/intervention semantics;
- шесть accepted ADR.

---

# 2. Завершённые Design Updates

```text
DU-00 — Documentation Foundation
DU-01 — System Context
DU-02 — Dependency & Composition Rules
DU-03 — Runtime / Temporal Model
DU-04 — CognitiveState Semantics
DU-05 — Module Protocol & Scheduling
DU-06 — Observability & Intervention
```

## DU-01

Канонический документ:

- [`system-context.md`](system-context.md).

Ключевой результат: MINDRA Agent определяется логической responsibility/state ownership, а не process/VM/GPU; Environment, Training Runtime, Evaluation Runtime и research infrastructure отделены от cognition.

Accepted decision:

- [`ADR-0001`](decisions/ADR-0001-logical-boundaries-independent-of-deployment.md).

## DU-02

Канонический документ:

- [`dependency-rules.md`](dependency-rules.md).

Ключевой результат: concrete implementations собираются через Composition Root; runtime Service Locator/shared mutable globals и concrete peer coupling запрещены.

Accepted decision:

- [`ADR-0002`](decisions/ADR-0002-explicit-composition-no-runtime-service-locator.md).

## DU-03

Канонический документ:

- [`execution-model.md`](execution-model.md).

Ключевой результат: canonical time является logical causal time; различаются Agent Session, Episode, Decision Window, Cognitive Cycle, Action/Outcome Commit, Learning/Replay/Consolidation events.

Accepted decision:

- [`ADR-0003`](decisions/ADR-0003-hierarchical-logical-time.md).

## DU-04

Канонический документ:

- [`cognitive-state.md`](cognitive-state.md).

Ключевой результат: `CognitiveState` является versioned committed shared runtime state, а не всем `Agent-owned state`; published state имеет owner/provenance/freshness/scope и semantic immutability.

Accepted decision:

- [`ADR-0004`](decisions/ADR-0004-versioned-committed-cognitive-state.md).

## DU-05

Канонический документ:

- [`module-lifecycle.md`](module-lifecycle.md).

Ключевой результат: module dependencies компилируются в DAG/execution waves; modules одной wave читают одну base revision, а public и causally relevant private effects commit согласованно.

Accepted decision:

- [`ADR-0005`](decisions/ADR-0005-wave-scheduled-module-protocol.md).

## DU-06

Канонический документ:

- [`observability-and-intervention.md`](observability-and-intervention.md).

Главные результаты:

- passive `Evidence Plane` отделён от active `Intervention Gateway`;
- tracing обязан сохранять causal identities и различать attempt/commit;
- metrics являются производными данными и не заменяют raw causal evidence;
- private-state inspection выполняется через declared research probe/export boundary;
- observability не даёт evaluator write authority;
- raw/backend activations относятся к opt-in research capability, а не universal module contract;
- intervention имеет explicit target, base revision, duration и provenance;
- intervention не меняет semantic owner целевого состояния;
- confirmatory causal experiment по умолчанию предпочитает control/treatment fork от identifiable committed base;
- natural и intervened trajectories различаются по provenance;
- exact counterfactual claim требует полного causally relevant Agent + Environment state;
- partial restore должен называться approximate counterfactual/replay;
- stochastic branch/RNG policy является частью experiment protocol;
- latent/raw interventions требуют учитывать OOD/divergent representations и off-target effects;
- telemetry failure и Agent/module failure различаются;
- evidence-critical loss делает соответствующий research claim incomplete/invalid, если данные нельзя восстановить;
- capture/sampling policy является частью experiment provenance.

Accepted decision:

- [`ADR-0006`](decisions/ADR-0006-separated-evidence-plane-and-intervention-gateway.md).

---

# 3. Следующий допустимый Design Update

```text
DU-07 — Environment / MicroWorld Contract
```

Цель `DU-07` — определить общий Environment boundary и первую контролируемую исследовательскую среду, на которой можно будет одинаково тестировать baseline и будущие MINDRA configurations.

Обязательные области:

```text
Environment state
agent-visible observation
hidden world state
action contract
external task feedback
reset / step
termination / truncation
clone / restore / fork
seed / procedural generation
train / validation / test distributions
world/task versioning
Environment intervention
transition evidence
```

Нужно определить:

- что Environment считает истинным world state;
- что Agent имеет право наблюдать;
- как отделяется external feedback от internal utility;
- как выглядит action acceptance/failure semantics;
- какие состояния/правила скрыты от Agent;
- как обеспечивается procedural diversity без leakage;
- как создаются reproducible worlds;
- как Environment участвует в exact counterfactual fork;
- как evaluator вмешивается в world state, не маскируя intervention под normal observation;
- как задаются train/validation/test distributions;
- какие минимальные task families необходимы для будущих module experiments;
- как MicroWorld остаётся достаточно простым для диагностики, но не вырождается в одну игрушечную задачу.

После принятия `DU-07` допускается:

```text
DU-08 — Perception / Canonical Representation
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
scheduler mechanics
≠
cognitive decision policy
```

```text
Observability
≠
Intervention
```

```text
natural execution
≠
intervened execution
```

```text
inspection capability
≠
write authority
```

---

# 5. Действующие observability/intervention invariants

До явного изменения canonical design запрещаются:

- использовать logger/collector/evaluator как normal cognitive dependency;
- возвращать trace/metric/debug metadata в cognitive payload без отдельного design;
- считать наличие research probe правом другого module читать private state;
- выдавать evaluator mutable reference на private/canonical state как canonical inspection mechanism;
- объединять passive tracing и active mutation в один неразличимый callback contract;
- выполнять intervention без explicit target/base/provenance;
- менять semantic owner target из-за evaluator override;
- изменять natural lineage задним числом;
- выдавать partial restore за exact counterfactual clone;
- смешивать intervened trajectory с natural experience без explicit provenance/training decision;
- делать arbitrary mid-operation mutation через race/alias и интерпретировать её как clean causal intervention;
- считать raw activation access обязательным для любого Cortex/backend;
- игнорировать intervention OOD/off-target risk при сильных latent manipulations;
- молча терять evidence-critical trace и затем делать confirmatory claim;
- использовать physical telemetry timestamp как logical causal order.

---

# 6. Что ещё не принято

Пока отсутствуют accepted решения по:

- exact `CognitiveState` container/API;
- exact Python `ModuleProtocol`;
- concrete scheduler/DAG implementation;
- exact trace/event/probe/intervention Python contracts;
- OpenTelemetry/другому telemetry backend;
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
- OpenTelemetry;
- PyTorch hooks как canonical mechanism;
- pyvene или другой intervention library;
- artifact database/storage stack;
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

# 8. Канонические ссылки

- порядок Design Updates: [`documentation-plan.md`](documentation-plan.md);
- системный контекст: [`system-context.md`](system-context.md);
- dependency/composition: [`dependency-rules.md`](dependency-rules.md);
- runtime/temporal model: [`execution-model.md`](execution-model.md);
- `CognitiveState`: [`cognitive-state.md`](cognitive-state.md);
- module lifecycle/scheduling: [`module-lifecycle.md`](module-lifecycle.md);
- observability/intervention: [`observability-and-intervention.md`](observability-and-intervention.md);
- ADR registry: [`decisions/README.md`](decisions/README.md);
- карта областей: [`modules/README.md`](modules/README.md);
- общие принципы: [`principles.md`](principles.md);
- термины: [`glossary.md`](glossary.md);
- исследовательская дисциплина: [`../research-methodology.md`](../research-methodology.md).
