# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-07` завершены и приняты. Реализация ещё не начата.**

На текущем этапе зафиксированы:

- концепция проекта;
- архитектурная концепция;
- исследовательская методология;
- базовые принципы проектирования;
- глоссарий;
- правила для coding agents;
- реестры ADR, candidate/exact contracts и будущих версий;
- карта кандидатных модулей;
- канонический порядок `DU-00` … `DU-32`;
- системный контекст;
- dependency/composition model;
- runtime/temporal model;
- canonical `CognitiveState` semantics;
- module lifecycle и scheduler semantics;
- observability/intervention semantics;
- общий Environment/MicroWorld design;
- candidate Environment contract;
- семь accepted ADR.

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
DU-07 — Environment / MicroWorld Contract
```

## DU-01

Канонический документ:

- [`system-context.md`](system-context.md).

Ключевой результат: MINDRA Agent определяется logical responsibility/state ownership, а не process/VM/GPU; Environment, Training Runtime, Evaluation Runtime и research infrastructure отделены от cognition.

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

Ключевой результат: passive `Evidence Plane` отделён от active `Intervention Gateway`; tracing сохраняет causal identities, private state наблюдается через declared probes, intervention создаёт отдельную provenance/lineage, а exact counterfactual требует полного causally relevant state.

Accepted decision:

- [`ADR-0006`](decisions/ADR-0006-separated-evidence-plane-and-intervention-gateway.md).

## DU-07

Канонический документ:

- [`modules/environment.md`](modules/environment.md).

Candidate contract:

- [`contracts/environment.md`](contracts/environment.md).

Главные результаты:

- общий Environment contract отделён от конкретного `MicroWorld`;
- Environment имеет отдельные `Agent Interaction Plane` и research-only control/evidence surface;
- Hidden World State и Research Ground Truth не становятся Agent input;
- `Raw Observation` отделена от будущего canonical representation;
- `External Task Specification` отделена от internal Goal state;
- `External Task Feedback`, `Objective Task Metric` и `Internal Utility` различаются;
- structurally invalid action отделён от valid-but-ineffective world action;
- `terminated` и `truncated` различаются;
- partial observability является first-class capability, full observability — control condition;
- observed appearance и hidden causal property factorized;
- Environment stochasticity разделяется на identifiable RNG roles;
- seed не является достаточной world identity;
- exact `Environment Snapshot` включает hidden state, task state, pending events и causally relevant RNG state;
- snapshot/restore/clone/fork являются privileged research/runtime operations;
- Environment intervention создаёт отдельную provenance/lineage;
- procedural generator должен быть factorized/versioned;
- core benchmark instances должны иметь явную solvability/validity policy;
- distributions должны поддерживать ID unseen, compositional holdout, rule-shift и stronger OOD conditions;
- `MicroWorld` принят как reference 2D symbolic Environment family;
- MicroWorld должен быть выразителен для baseline, Memory, World Model, exploration/trade-off, delayed consequence, adaptation и compositional tasks;
- Gymnasium остаётся interoperability/adapter candidate, а не canonical dependency.

Accepted decision:

- [`ADR-0007`](decisions/ADR-0007-two-plane-environment-boundary.md).

---

# 3. Следующий допустимый Design Update

```text
DU-08 — Perception / Canonical Representation
```

Цель `DU-08` — определить границу между `Raw Observation` Environment и стабильным внутренним representation space, которым смогут пользоваться World Model, Memory, Self Model, Policy и другие независимые модули.

Обязательные области:

```text
Raw Observation ingestion
structured vs learned encoding
canonical representation semantics
modality metadata
partial/missing observation
normalization
representation identity/versioning
provenance back to Environment observation
trainable encoder boundary
representation drift
backend/device independence
Cortex embedding adapter
no-Cortex mode
batch semantics
research probes/interventions
```

Нужно определить:

- какие свойства representation должны быть semantic, а какие implementation-private;
- должен ли canonical representation быть одним latent vector или структурой нескольких namespaces;
- как сохранить observable provenance и не смешать prediction/retrieval с observation;
- как downstream modules не привязать к exact MicroWorld encoding;
- как representation остаётся совместимой при замене Cortex;
- где заканчивается deterministic normalization и начинается learned Perception;
- как version/drift representation влияет на Memory/World Model/checkpoints;
- какие raw/latent intervention targets допустимы;
- как no-Cortex baseline получает тот же canonical boundary.

После принятия `DU-08` допускается:

```text
DU-09 — Goal System
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
agent-visible Environment interaction
≠
research-visible world ground truth
```

```text
Raw Observation
≠
canonical internal representation
```

```text
External Task Feedback
≠
Objective Task Metric
≠
Internal Utility
```

```text
seed
≠
complete world identity
```

```text
Environment Snapshot
≠
rendered observation
```

---

# 5. Действующие Environment invariants

До явного изменения canonical design запрещается:

- передавать Agent hidden world state, oracle path/action или evaluator metric как normal input;
- использовать framework `info`/debug metadata как Agent input без explicit task semantics;
- считать split/distribution/world seed обычным observation;
- путать External Task Feedback с research-only Objective Task Metric;
- использовать Environment reward/feedback как определение Internal Utility MINDRA;
- считать malformed action нормальным world-level no-op;
- передавать privileged reason failed action Agent, если observation contract его не раскрывает;
- сводить `terminated` и `truncated` в один неразличимый `done` внутри canonical evidence;
- считать полный hidden world map обычной partial observation;
- фиксировать causal meaning object по цвету/форме без сознательно принятой distribution semantics;
- использовать один seed как полное доказательство воспроизводимости world instance;
- называть restore exact, если не восстановлены causally relevant Environment RNG/pending state;
- использовать Environment restore/intervention как обычное Agent action;
- изменять natural world lineage intervention-ом без provenance;
- смешивать train/test distributions без manifest/version identity;
- использовать procedural instances с неизвестной solvability для claims, требующих гарантированно решаемых задач, без documented limitation;
- терять final terminal outcome из-за autoreset/vectorization;
- считать `MicroWorld` универсальным internal representation Agent.

---

# 6. Что ещё не принято

Пока отсутствуют accepted решения по:

- exact `CognitiveState` container/API;
- exact Python `ModuleProtocol`;
- concrete scheduler/DAG implementation;
- exact trace/event/probe/intervention Python contracts;
- exact Python Environment API;
- concrete Gymnasium adapter;
- exact MicroWorld observation/action encoding;
- exact grid sizes/entity enum/task grammar;
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
- Gymnasium как mandatory dependency;
- procedural-generation library;
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
- Environment/MicroWorld: [`modules/environment.md`](modules/environment.md);
- candidate Environment contract: [`contracts/environment.md`](contracts/environment.md);
- ADR registry: [`decisions/README.md`](decisions/README.md);
- карта областей: [`modules/README.md`](modules/README.md);
- общие принципы: [`principles.md`](principles.md);
- термины: [`glossary.md`](glossary.md);
- исследовательская дисциплина: [`../research-methodology.md`](../research-methodology.md).
