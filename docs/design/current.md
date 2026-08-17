# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-17` завершены и приняты. Реализация ещё не начата.**

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
- Affect System;
- candidate contracts Environment, Perception, Goals, Cortex, Memory, World Model, Self Model, Intrinsic Signals, Drives, Appraisal и Affect;
- семнадцать accepted ADR.

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
DU-17 — Affect Dynamics
```

## DU-17

Канонический документ:

- [`modules/affect.md`](modules/affect.md).

Candidate contract:

- [`contracts/affect.md`](contracts/affect.md).

Research pass:

- [`../research/literature/DU-17-affect-dynamics-landscape-2026-08.md`](../research/literature/DU-17-affect-dynamics-landscape-2026-08.md).

Accepted decision:

- [`ADR-0017`](decisions/ADR-0017-typed-persistent-affect-state.md).

Главные результаты:

- отдельный Affect прошёл module gate как **falsifiable persistent history-dependent state boundary**;
- `Appraisal ≠ Affect ≠ Drive ≠ Valuation`;
- Affect интегрирует последовательность `AppraisalRecord` во времени, но не хранит полную историю вместо Memory/trajectory;
- принят typed `AffectStateSet`, а mandatory emotion labels/valence-arousal/PAD geometry отклонены;
- low-dimensional affect representations допускаются только как implementation/view/baseline;
- dynamics может включать inertia/decay/recovery/accumulation/saturation/hysteresis;
- Affect использует logical time, а не GPU/network/wall-clock latency;
- canonical feedback имеет порядок `Affect_t → Appraisal_t → Affect_(t+1)` без instantaneous cycle;
- actual appraisal является natural eligible source;
- predicted appraisal может создавать anticipatory Affect только через explicit source policy;
- imagined appraisal по умолчанию изменяет только branch-local simulated Affect;
- current retrospective reappraisal может влиять на current Affect, не переписывая историческое состояние;
- Affect не мутирует Drives/Goals и не вычисляет Utility/action;
- будущие Valuation/Salience/Memory Regulation могут читать Affect только через explicit boundary;
- `Environment.reset()` не является автоматическим Affect reset;
- causally relevant recurrent/baseline/RNG/dynamics state входит в exact Agent Snapshot;
- обязательны `NoAffect`, `ResetEveryEvent`, shuffled-history и matched-recurrent controls;
- если temporal Affect не показывает специфической causal роли относительно matched controls, отдельный module должен быть пересмотрен новым ADR.

---

# 3. Следующий допустимый Design Update

```text
DU-18 — Valuation
```

Цель `DU-18` — спроектировать **decision-relevant систему ценности**, которая преобразует разнородные Goal/Drive/Appraisal/Affect/World/Self evidence в сравнимую оценку candidate outcomes/actions, не превращая всё заранее в один reward scalar.

Обязательные области:

```text
Valuation responsibility / ownership
valuation target boundary
state/outcome/action/trajectory valuation
input evidence model
Goal / Drive / Appraisal / Affect integration
external task feedback boundary
Intrinsic Signals boundary
World Prediction / uncertainty / risk
Self Model / feasibility / cost
vector-valued vs scalar value
context-dependent scalarization
multi-objective conflict
immediate vs future value
state value vs action value vs utility
predicted / imagined valuation
counterfactual comparison
risk / downside / uncertainty treatment
normalization / comparability / units
rule-based vs learned valuation
critic / RL value-function boundary
training reward boundary
NoValuation / Dummy / Control
observability / intervention / calibration
snapshot / revision / degradation
```

Нужно определить:

- что именно является `Valuation Target`;
- является ли canonical value вектором typed components, distribution/structured relation или scalar;
- где и когда допустима scalarization;
- как сохранить конфликт нескольких Goals/Drives вместо скрытого weighted sum;
- чем event-level Appraisal polarity отличается от decision value;
- чем persistent Affect modulation отличается от value;
- как external task feedback участвует в valuation, не становясь автоматически внутренней utility;
- как Intrinsic Signals входят или не входят в decision value;
- как predictive uncertainty отличается от risk/downside;
- как учитывать Self Model competence/expected cost;
- как оценивать imagined trajectories без превращения их в observed outcomes;
- где проходит граница между архитектурным Valuation и algorithm-specific RL reward/critic;
- нужны ли разные value surfaces для state/action/outcome/trajectory;
- какие controls исключают объяснение «любой дополнительный scalar помогает Policy».

После принятия `DU-18` допускается:

```text
DU-19 — Salience / Attention
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
Appraisal Record ≠ Affect State
Affect State ≠ Drive State
Affect State ≠ Utility/Value/Reward
Affect State ≠ emotion label
Affect history integration ≠ Memory Store
Affect_t → Appraisal_t → Affect_(t+1)
imagined Affect ≠ real committed Affect
Environment reset ≠ Affect reset
```

---

# 5. Что ещё не принято

Пока отсутствуют accepted решения по:

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

Также пока не выбраны exact Python/package/framework решения, concrete Cortex backend, Memory backend/index, World Model architecture, Self Model estimator/calibration method, Intrinsic Signal estimators, concrete Drive list/dynamics, concrete Appraisal dimension subset/estimator, concrete Affect channels/dynamics или common normalization/scalarization policy.

---

# 6. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начинать implementation до появления version roadmap и implementation sequence.
