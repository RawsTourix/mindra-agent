# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-12` завершены и приняты. Реализация ещё не начата.**

На текущем этапе зафиксированы:

- системные/dependency/runtime/state/scheduler boundaries;
- observability/intervention discipline;
- Environment/MicroWorld;
- Perception/Canonical Percept;
- Goal System/Goal Graph;
- Cortex semantic capability boundary;
- Memory Core;
- World Model;
- candidate contracts Environment, Perception, Goals, Cortex, Memory и World Model;
- двенадцать accepted ADR.

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
DU-10 — Cortex Boundary
DU-11 — Memory Core
DU-12 — World Model
```

## DU-12

Канонический документ:

- [`modules/world-model.md`](modules/world-model.md).

Candidate contract:

- [`contracts/world-model.md`](contracts/world-model.md).

Research pass:

- [`../research/literature/DU-12-world-model-landscape-2026-08.md`](../research/literature/DU-12-world-model-landscape-2026-08.md).

Accepted decision:

- [`ADR-0012`](decisions/ADR-0012-belief-state-world-model.md).

Главные результаты:

- `Canonical Percept`, `World Belief`, `World Prediction`, imagination и Hidden World State являются разными сущностями;
- World Model является agent-owned cognitive subsystem;
- partial observability выражается через committed belief-state semantics;
- assimilation actual percept/outcome отделена от prior/action-conditioned prediction;
- candidate action query не означает Action Commit;
- multi-step imagination не является Environment trajectory;
- backend-specific latent может быть private state/optional Feature View, но не universal inter-module representation;
- prediction surface может быть structured и/или learned;
- observation reconstruction не является обязательным requirement;
- Goal не является обязательным causal input physical dynamics;
- Memory используется только через explicit RetrievalResult;
- Cortex assistance остаётся optional/traceable и не становится world truth;
- predictive uncertainty допускается, а epistemic/aleatoric decomposition требует отдельного обоснования;
- prediction error/surprise evidence не является reward или intrinsic utility автоматически;
- baseline training не может молча использовать Environment Research Ground Truth как будто Agent её наблюдал;
- World Model имеет отдельные belief/model revision и snapshot obligations;
- `NoWorldModel`, Dummy и Control configurations различаются;
- correct/degraded/NoWorldModel comparison является будущим causal evaluation pattern.

---

# 3. Следующий допустимый Design Update

```text
DU-13 — Self Model
```

Цель `DU-13` — определить, как MINDRA представляет и обновляет **модель собственных функциональных свойств Agent**, не смешивая её с World Model, Goal, Valuation или текстовым самоописанием Cortex.

Обязательные области:

```text
Self Model responsibility / ownership
self vs world boundary
capability / competence representation
success probability / calibration
resource / compute / action-cost estimates
known limitations / unavailable capabilities
self-state under partial observability
source evidence / learning targets
uncertainty / confidence semantics
prediction of own future state
Cortex self-description boundary
Self Model revision / snapshot
NoSelfModel / Dummy / Control
observability / intervention
failure / degradation
```

Нужно определить:

- какие свойства Agent вообще относятся к Self Model, а какие остаются обычным runtime metadata;
- чем Self Model отличается от World Model prediction embodiment state;
- как измерять competence без evaluator-only leakage;
- как представлять calibrated `P(success)` и где такой target применим;
- как учитывать изменение собственных capabilities после Learning Update/Cortex swap/module disable;
- как Self Model узнаёт о собственных ограничениях через causal experience;
- где заканчивается Self Model и начинается будущий Executive Control;
- как не превратить natural-language self-report Cortex в каноническое self-knowledge;
- какие interventions позволяют проверить причинную роль self-estimates.

После принятия `DU-13` допускается:

```text
DU-14 — Intrinsic Signals
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
MINDRA Agent ≠ Cortex ≠ concrete LLM
MemoryRecord ≠ embedding/index entry
Memory ≠ trajectory/replay
Canonical Percept ≠ World Belief ≠ World Prediction
World Prediction ≠ observed fact
Imagined Transition ≠ Environment Transition
prediction error ≠ reward / intrinsic utility
predictive uncertainty ≠ risk / value
```

---

# 5. Что ещё не принято

Пока отсутствуют accepted решения по:

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

Также пока не выбраны exact Python/package/framework решения, concrete Cortex backend, Memory backend/index, World Model architecture или uncertainty estimator.

---

# 6. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начинать implementation до появления version roadmap и implementation sequence.
