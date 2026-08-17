# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-16` завершены и приняты. Реализация ещё не начата.**

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
- Appraisal System;
- candidate contracts Environment, Perception, Goals, Cortex, Memory, World Model, Self Model, Intrinsic Signals, Drives и Appraisal;
- шестнадцать accepted ADR.

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
DU-16 — Appraisal
```

## DU-16

Канонический документ:

- [`modules/appraisal.md`](modules/appraisal.md).

Candidate contract:

- [`contracts/appraisal.md`](contracts/appraisal.md).

Research pass:

- [`../research/literature/DU-16-appraisal-landscape-2026-08.md`](../research/literature/DU-16-appraisal-landscape-2026-08.md).

Accepted decision:

- [`ADR-0016`](decisions/ADR-0016-multidimensional-event-centered-appraisal.md).

Главные результаты:

- Appraisal является event-level relational assessment, а не persistent Affect/Reward/Value;
- принят explicit `Appraisal Target` с actual/predicted/imagined/retrospective/intervened provenance;
- appraisal context versioned и строится только из declared committed sources;
- один target может иметь разные appraisal при разных Goals/Drives/Self/World context;
- принят typed multidimensional `Appraisal Profile` без обязательного emotion label/global valence scalar;
- relevance отделена от Salience/novelty/utility;
- goal congruence сохраняется per Goal и не решает Goal conflict;
- drive conduciveness сохраняется per Drive и не мутирует Drive State;
- expectedness отделена от novelty/prediction discrepancy/probabilistic surprisal;
- controllability отделена от coping potential;
- controllability относится к action-sensitivity ситуации, coping potential — к способности текущего Agent справиться/адаптироваться;
- urgency отделена от Salience/action priority/value;
- agency/causal attribution является optional dimension family;
- normative compatibility не вводится до отдельной agent-owned semantics норм/стандартов;
- mandatory global valence отклонён; optional local polarity допустим только как derived summary;
- reappraisal создаёт новый temporally identified `AppraisalRecord`, а не переписывает историю;
- explicit Memory retrieval/Cortex call не скрываются внутри Appraisal;
- rule-based, learned, hybrid и Cortex-assisted estimators допускаются;
- partial profile и per-dimension availability/failure являются first-class semantics;
- causally relevant estimator/calibration/RNG state входит в exact Agent Snapshot;
- `NoAppraisal`, Dummy, Constant, Random, Shuffled и matched controls различаются.

---

# 3. Следующий допустимый Design Update

```text
DU-17 — Affect Dynamics
```

Цель `DU-17` — проверить необходимость и, если она обоснована, спроектировать **отдельный persistent affective state**, который интегрирует последовательность Appraisal Records во времени и способен создавать history-dependent modulation, не смешиваясь с Drives или Valuation.

Обязательные области:

```text
Affect responsibility / module gate
Appraisal → Affect integration
persistent state semantics
valence/arousal-like representation necessity
multidimensional vs low-dimensional affect
inertia / decay / recovery
accumulation / saturation
hysteresis / baseline
actual vs predicted / imagined appraisal contribution
interaction with Drives
interaction with future Valuation / Salience / Memory
state scope / reset / persistence
reappraisal effect
learning / adaptation
NoAffect / Dummy / Control
snapshot / observability / intervention
failure / degradation
```

Нужно определить:

- существует ли у Affect самостоятельная functional responsibility или достаточно Appraisal + Drives;
- что именно persistent Affect хранит сверх последних Appraisal Records;
- должен ли Affect иметь valence/arousal-like low-dimensional state или typed/vector state;
- как один и тот же новый Appraisal даёт разный Affect update в зависимости от предыдущего Affect;
- как decay/inertia/recovery используют logical time;
- следует ли predicted/imagined appraisal менять real Affect и с какой provenance;
- где проходит граница Affect ↔ Drive;
- где проходит граница Affect ↔ будущая Valuation;
- какие causal interventions показывают самостоятельную роль Affect;
- какой отрицательный результат приведёт к решению не выделять отдельный Affect module.

После принятия `DU-17` допускается:

```text
DU-18 — Valuation
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
Appraisal ≠ Intrinsic Signal ≠ Drive ≠ Affect ≠ Valuation
Appraisal Target ≠ Appraisal Context
relevance ≠ Salience ≠ novelty ≠ utility
goal congruence ≠ global Goal priority/value
drive conduciveness ≠ committed Drive update
expectedness ≠ novelty ≠ prediction discrepancy ≠ predictive surprisal
controllability ≠ coping potential
urgency ≠ Salience ≠ action priority
Appraisal local polarity ≠ Utility/Value/Reward
reappraisal ≠ mutation of historical AppraisalRecord
```

---

# 5. Что ещё не принято

Пока отсутствуют accepted решения по:

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

Также пока не выбраны exact Python/package/framework решения, concrete Cortex backend, Memory backend/index, World Model architecture, Self Model estimator/calibration method, Intrinsic Signal estimators, concrete Drive list/dynamics, concrete Appraisal estimator/dimension subset или common normalization/scalarization policy.

---

# 6. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начинать implementation до появления version roadmap и implementation sequence.
