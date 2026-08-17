# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-15` завершены и приняты. Реализация ещё не начата.**

На текущем этапе зафиксированы:

- системные/dependency/runtime/state/scheduler boundaries;
- observability/intervention discipline;
- Environment/MicroWorld;
- Perception/Canonical Percept;
- Goal System/Goal Graph;
- Cortex semantic capability boundary;
- Memory Core;
- World Model;
- Self Model;
- Intrinsic Signal Layer;
- Drive System;
- candidate contracts Environment, Perception, Goals, Cortex, Memory, World Model, Self Model, Intrinsic Signals и Drives;
- пятнадцать accepted ADR.

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
DU-13 — Self Model
DU-14 — Intrinsic Signals
DU-15 — Drives
```

## DU-15

Канонический документ:

- [`modules/drives.md`](modules/drives.md).

Candidate contract:

- [`contracts/drives.md`](contracts/drives.md).

Research pass:

- [`../research/literature/DU-15-drives-landscape-2026-08.md`](../research/literature/DU-15-drives-landscape-2026-08.md).

Accepted decision:

- [`ADR-0015`](decisions/ADR-0015-typed-stateful-drive-system.md).

Главные результаты:

- Drive является persistent internal regulatory state, а не Intrinsic Signal/reward/value;
- принят единый ownership boundary `Drive System` с несколькими typed drive components;
- обязательного global motivation scalar нет;
- `Drive State`, `Drive Pressure` и `Utility/Value` являются разными сущностями;
- homeostatic drives имеют meaningful regulated variable + target/range semantics;
- не-homeostatic adaptive motivational drives не обязаны иметь фиктивный set-point;
- Intrinsic Signal является input/evidence для drive dynamics, а не готовым pressure;
- drive dynamics использует logical time и может включать accumulation/decay/recovery/satiation;
- отсутствие нового Environment observation не обязано замораживать Drive State;
- wall-clock/compute latency не является implicit drive time;
- cross-drive interaction читает предыдущую committed `DriveStateSet` revision и не создаёт hidden instantaneous cycle;
- Drive System не выбирает `winning drive` и не scalarize конфликт;
- Drive может участвовать в создании `Goal Proposal`, но не получает Goal Graph write authority;
- future Valuation получает Drive State как input, но Drive не вычисляет action utility;
- initial conditions/reset/persistence имеют explicit semantics;
- natural regulation отделена от research intervention;
- causally relevant dynamics/coupling/RNG state входит в exact Agent Snapshot;
- `NoDrives`, Dummy, Constant, Clamped, Random, Shuffled и matched controls различаются.

---

# 3. Следующий допустимый Design Update

```text
DU-16 — Appraisal
```

Цель `DU-16` — определить **контекстную многомерную оценку значения конкретного события/ситуации для текущего Agent**, не смешивая её с persistent Drive/Affect state или общей decision value.

Обязательные области:

```text
Appraisal responsibility / ownership
appraisal event boundary
input context
Goal / Drive / World / Self / Memory integration
actual vs predicted / imagined appraisal
multidimensional output semantics
goal congruence
controllability / coping potential
novelty / expectedness boundary with Intrinsic Signals
urgency / relevance semantics
valence semantics
rule-derived vs learned appraisal
calibration / evidence
Appraisal vs Drive vs Affect vs Valuation
NoAppraisal / Dummy / Control
snapshot / observability / intervention
failure / degradation
```

Нужно определить:

- что считается appraisal event, а что просто raw signal/state;
- должен ли Appraisal оценивать только actual events или также predicted/imagined outcomes с отдельной provenance;
- какие dimensions имеют самостоятельный смысл и какие нельзя вводить только ради эмоциональной аналогии;
- чем appraisal novelty/expectedness отличается от neutral Intrinsic Signal novelty/surprisal;
- как Drive State и Goal state меняют meaning одного и того же события;
- где проходит граница между event-level valence и будущей общей `Valuation`;
- как не превратить Appraisal в scalar reward model;
- какие interventions позволяют независимо менять отдельную appraisal dimension.

После принятия `DU-16` допускается:

```text
DU-17 — Affect Dynamics
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
Agent Capability Fact ≠ Learned Competence Estimate ≠ Self Prediction
P(success) ≠ uncertainty/support самой self-estimate
Self Model ≠ Cortex self-report ≠ Executive Control
Intrinsic Signal ≠ Reward ≠ Drive ≠ Utility/Value
prediction discrepancy ≠ predictive surprisal ≠ novelty
novelty ≠ visitation rarity
information gain ≠ arbitrary uncertainty reduction
higher intrinsic signal ≠ greater desirability
Intrinsic Signal ≠ Drive State
Drive State ≠ Drive Pressure ≠ Utility/Value
Drive ≠ Goal ≠ Policy
higher Drive Pressure ≠ universally greater desirability
homeostatic drive ≠ mandatory form of every drive
Environment reset ≠ Drive reset
wall-clock ≠ implicit Drive time
```

---

# 5. Что ещё не принято

Пока отсутствуют accepted решения по:

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

Также пока не выбраны exact Python/package/framework решения, concrete Cortex backend, Memory backend/index, World Model architecture, Self Model estimator/calibration method, Intrinsic Signal estimators, concrete Drive list/dynamics или common normalization/scalarization policy.

---

# 6. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начинать implementation до появления version roadmap и implementation sequence.
