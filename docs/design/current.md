# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-09` завершены и приняты. Реализация ещё не начата.**

На текущем этапе зафиксированы:

- концепция проекта и исследовательская методология;
- системные/dependency/runtime/state/scheduler boundaries;
- observability/intervention discipline;
- Environment/MicroWorld contract;
- Perception/Canonical Percept;
- Goal System/Goal Graph;
- candidate contracts Environment, Perception и Goals;
- девять accepted ADR.

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
DU-09 — Goal System
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

Ключевой результат: общий Environment contract отделён от `MicroWorld`, а Agent Interaction Plane — от research-only hidden world/control plane.

Accepted decision:

- [`ADR-0007`](decisions/ADR-0007-two-plane-environment-boundary.md).

## DU-08

Канонический документ:

- [`modules/perception.md`](modules/perception.md).

Candidate contract:

- [`contracts/perception.md`](contracts/perception.md).

Ключевой результат: принят `Canonical Percept = structured Semantic Core + optional Feature Views`; Cortex hidden space и один universal latent не являются canonical inter-module representation.

Accepted decision:

- [`ADR-0008`](decisions/ADR-0008-hybrid-canonical-percept.md).

## DU-09

Канонический документ:

- [`modules/goals.md`](modules/goals.md).

Candidate contract:

- [`contracts/goals.md`](contracts/goals.md).

Главные результаты:

- Goal отделена от External Task Specification, Reward, Drives, Valuation и Policy;
- принят `Goal Proposal → Goal System → Committed Goal` pipeline;
- Goal System является единственным semantic owner canonical Goal state;
- внешние/internal/planner/research sources могут предлагать goals, но не мутировать Goal Graph напрямую;
- принят `Goal Graph`, а не обязательный LIFO stack;
- поддерживаются несколько committed/active goals;
- parent/subgoal/dependency/conflict semantics различаются;
- dependency relation должна быть ацикличной;
- lifecycle различает `pending`, `active`, `suspended`, `achieved`, `failed`, `abandoned`, `expired`, `invalidated` semantics;
- `failed` не равно `expired`, `suspended` не равно `abandoned`;
- goals могут быть episode/session/agent-long-lived;
- structural/declarative priority отделена от будущей dynamic Valuation;
- commitment отделён от priority/value/focus;
- progress не обязан быть scalar `[0,1]` и не получает hidden evaluator metric;
- Natural-language instruction не является canonical Goal без grounding/proposal boundary;
- Goal intervention/observability semantics определены.

Accepted decision:

- [`ADR-0009`](decisions/ADR-0009-committed-goal-graph.md).

---

# 3. Следующий допустимый Design Update

```text
DU-10 — Cortex Boundary
```

Цель `DU-10` — спроектировать заменяемую pretrained capability `Cortex`, не превращая конкретную LLM в центр архитектуры MINDRA.

Обязательные области:

```text
Cortex semantic capabilities
backend-neutral contract
text / structured / latent inputs and outputs
context construction boundary
reasoning / generation capabilities
Goal Proposal / grounding boundary
Perception Feature View integration
hidden-state / embedding access as optional research capability
local vs remote execution provider
frozen / adapted mode
Cortex identity and revision
NoCortex / DummyCortex
backend switching
multilingual requirements
resource / latency / context reporting
failure / timeout / degradation semantics
observability / intervention
checkpoint / experiment provenance implications
```

Нужно определить:

- какие возможности обязательны для любого Cortex, а какие optional;
- может ли Cortex быть remote black-box backend;
- где заканчивается canonical MINDRA context и начинается model-specific prompt/tokenization;
- как Cortex получает `Canonical Percept`, Goal state и позже Memory без direct peer coupling;
- как Cortex может создавать Goal Proposal, не получая Goal write authority;
- какие hidden/embedding capabilities нельзя требовать от общего contract;
- как `NoCortex` остаётся полноценной конфигурацией;
- как сравнивать/заменять backends без изменения независимых модулей;
- какие требования к русскому/мультиязычности и reasoning нужны исследовательскому baseline;
- какие конкретные open-weight models являются актуальными кандидатами, но не canonical architecture.

После принятия `DU-10` допускается:

```text
DU-11 — Memory Core
```

---

# 4. Действующие фундаментальные отношения

```text
logical architecture boundary ≠ deployment topology
Cognitive Cycle ≠ Environment Transition
CognitiveState ≠ full Agent-owned state
Observability ≠ Intervention
Raw Observation ≠ Canonical Percept
External Task Specification ≠ Committed Goal
Goal Proposal ≠ Committed Goal
Goal ≠ Reward ≠ Drive ≠ Utility/Value ≠ Policy
structural goal priority ≠ dynamic goal value
commitment ≠ focus ≠ priority ≠ value
```

---

# 5. Что ещё не принято

Пока отсутствуют accepted решения по:

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

Также пока не выбраны exact Python/package/framework решения.

---

# 6. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начинать implementation до появления version roadmap и implementation sequence.

---

# 7. Канонические ссылки

- порядок Design Updates: [`documentation-plan.md`](documentation-plan.md);
- Environment/MicroWorld: [`modules/environment.md`](modules/environment.md);
- Perception: [`modules/perception.md`](modules/perception.md);
- Goal System: [`modules/goals.md`](modules/goals.md);
- candidate Environment contract: [`contracts/environment.md`](contracts/environment.md);
- candidate Perception contract: [`contracts/perception.md`](contracts/perception.md);
- candidate Goal contract: [`contracts/goals.md`](contracts/goals.md);
- ADR registry: [`decisions/README.md`](decisions/README.md);
- термины: [`glossary.md`](glossary.md);
- правила coding agents: [`../../AGENTS.md`](../../AGENTS.md).
