# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-08` завершены и приняты. Реализация ещё не начата.**

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
- Perception/Canonical Percept design;
- candidate Perception contract;
- восемь accepted ADR.

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
DU-08 — Perception / Canonical Representation
```

## DU-01 … DU-06

Канонические документы:

- [`system-context.md`](system-context.md);
- [`dependency-rules.md`](dependency-rules.md);
- [`execution-model.md`](execution-model.md);
- [`cognitive-state.md`](cognitive-state.md);
- [`module-lifecycle.md`](module-lifecycle.md);
- [`observability-and-intervention.md`](observability-and-intervention.md).

Accepted decisions:

- `ADR-0001` … `ADR-0006`.

## DU-07

Канонический документ:

- [`modules/environment.md`](modules/environment.md).

Candidate contract:

- [`contracts/environment.md`](contracts/environment.md).

Главные результаты:

- общий Environment contract отделён от `MicroWorld`;
- Agent Interaction Plane отделён от Research Plane;
- Hidden World State/Research Ground Truth не становятся Agent input;
- `Raw Observation` отделена от internal representation;
- External Task Specification отделена от Goal state;
- External Task Feedback, Objective Task Metric и Internal Utility различаются;
- exact Environment Snapshot включает hidden state/task/pending events/RNG;
- procedural generation versioned/factorized;
- partial observability является first-class capability;
- `MicroWorld` принят как reference 2D symbolic Environment family.

Accepted decision:

- [`ADR-0007`](decisions/ADR-0007-two-plane-environment-boundary.md).

## DU-08

Канонический документ:

- [`modules/perception.md`](modules/perception.md).

Candidate contract:

- [`contracts/perception.md`](contracts/perception.md).

Главные результаты:

- Perception является отдельной boundary между `Raw Observation` и internal representation;
- принят `Canonical Percept`;
- `Canonical Percept` состоит из structured `Semantic Core` и optional `Feature Views`;
- один universal learned latent vector не является canonical inter-module representation;
- Cortex hidden state не является canonical representation;
- Semantic Core описывает current observation, а не hidden belief/Memory/World Model prediction;
- External Task Specification и External Task Feedback не поглощаются Perception;
- entity collection семантически unordered по умолчанию;
- persistent world identity entity не выдаётся Perception бесплатно;
- direct, normalized и perceptually inferred facts различаются provenance;
- невидимый hidden entity не создаётся из Research Ground Truth;
- modality availability/missingness являются explicit semantics;
- deterministic normalization отделена от learned Perception;
- `Feature View` имеет feature-space/encoder identity/revision;
- равенство dimensionality не означает compatibility feature spaces;
- representation drift считается наблюдаемым versioned явлением;
- frozen evaluation должна pin relevant representation revisions;
- batching/device/layout не определяют semantic identity;
- no-Cortex configuration сохраняет полноценную Perception boundary;
- sensor/input, semantic-percept и feature-view interventions различаются.

Accepted decision:

- [`ADR-0008`](decisions/ADR-0008-hybrid-canonical-percept.md).

---

# 3. Следующий допустимый Design Update

```text
DU-09 — Goal System
```

Цель `DU-09` — определить, как MINDRA представляет **что именно она стремится изменить, достичь или сохранить**, отдельно от Perception, External Task Specification, Drives, Valuation и Policy.

Обязательные области:

```text
External Task Specification ingress
internal Goal representation
goal identity
source/provenance
externally assigned vs internally generated goals
subgoals / hierarchy
goal lifecycle
activation / suspension
priority
commitment / persistence
progress
success / failure / abandonment
termination condition
goal conflict
multiple simultaneous goals
goal scope across Episode / Session
Goal intervention
Goal observability
NoOp/baseline goal handling
```

Нужно определить:

- является ли Goal отдельным модулем или canonical state responsibility;
- как External Task Specification становится internal Goal без прямого alias;
- кто имеет authority создавать/активировать/закрывать цели;
- как различить цель и reward/utility;
- как goal priority отличается от Value/Drive;
- может ли Agent иметь несколько активных целей;
- как представлять subgoal/dependency graph без циклической логики;
- как измерять progress без использования evaluator-only metric;
- как цель переживает Episode reset;
- как World Model/Policy позднее читают Goal state;
- какие Goal interventions нужны MINDRA-Eval.

После принятия `DU-09` допускается:

```text
DU-10 — Cortex Boundary
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
Canonical Percept
```

```text
Canonical Percept
≠
Cortex hidden state
```

```text
Semantic Core
≠
Feature View
```

```text
current percept
≠
Memory
≠
World Model prediction
```

```text
External Task Specification
≠
Internal Goal State
```

```text
External Task Feedback
≠
Objective Task Metric
≠
Internal Utility
```

```text
feature dimension equality
≠
feature-space compatibility
```

---

# 5. Действующие Perception invariants

До явного изменения canonical design запрещается:

- передавать Environment-specific raw schema напрямую независимым cognitive modules;
- использовать Research Ground Truth как normal Perception input;
- выдавать hidden/unobserved entity только потому, что evaluator знает о его существовании;
- использовать persistent Environment object ID как perception identity, если ID не является agent-visible;
- считать arbitrary entity array order semantic information;
- смешивать direct/normalized/inferred perceptual facts без provenance;
- кодировать missing modality/property универсальным zero/NaN/None без contract;
- включать External Task Specification/Feedback в Perception только потому, что они представлены текстом/структурой рядом с observation;
- считать один learned vector всем Canonical Percept;
- протаскивать model-specific Cortex hidden state в contracts независимых modules;
- считать одинаковый vector dimension достаточным доказательством compatibility;
- молча сравнивать/store/reuse incompatible feature revisions;
- переписывать committed percept задним числом после encoder update;
- выполнять hidden fallback на Cortex/privileged data при Perception failure;
- считать padding/batch index/entity ordering частью semantic identity;
- считать device/backend объект semantic identity representation;
- смешивать sensor/input intervention с Environment world-state intervention;
- интерпретировать сильный latent intervention без OOD/off-target limitations.

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
- exact `Canonical Percept` field paths/types;
- exact entity/relation schema;
- concrete Perception encoder architecture;
- feature vector dimensions;
- feature-space compatibility algorithm;
- exact Cortex-derived feature adapter;
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
- TensorDict/dataclass/Pydantic state framework;
- graph/async runtime;
- specific Perception framework;
- Slot Attention/GNN/Set Transformer/Perceiver/другая neural architecture;
- concrete Cortex backend;
- artifact database/storage stack.

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
- Perception/Canonical Percept: [`modules/perception.md`](modules/perception.md);
- candidate Environment contract: [`contracts/environment.md`](contracts/environment.md);
- candidate Perception contract: [`contracts/perception.md`](contracts/perception.md);
- ADR registry: [`decisions/README.md`](decisions/README.md);
- карта областей: [`modules/README.md`](modules/README.md);
- общие принципы: [`principles.md`](principles.md);
- термины: [`glossary.md`](glossary.md);
- исследовательская дисциплина: [`../research-methodology.md`](../research-methodology.md).
