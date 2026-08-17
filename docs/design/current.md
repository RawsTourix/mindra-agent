# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-18` завершены и приняты. Реализация ещё не начата.**

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
- Valuation System;
- candidate contracts Environment, Perception, Goals, Cortex, Memory, World Model, Self Model, Intrinsic Signals, Drives, Appraisal, Affect и Valuation;
- восемнадцать accepted ADR.

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
DU-18 — Valuation
```

## DU-18

Канонический документ:

- [`modules/valuation.md`](modules/valuation.md).

Candidate contract:

- [`contracts/valuation.md`](contracts/valuation.md).

Research pass:

- [`../research/literature/DU-18-valuation-landscape-2026-08.md`](../research/literature/DU-18-valuation-landscape-2026-08.md).

Accepted decision:

- [`ADR-0018`](decisions/ADR-0018-typed-multi-objective-valuation.md).

Главные результаты:

- `Valuation System` принят как отдельная decision-relevant boundary, но не владеет final action selection;
- `ValueProfile ≠ ScalarizedValue ≠ Training Reward ≠ Critic Value ≠ Policy Decision`;
- принят typed multi-objective `ValueProfile`, сохраняющий Goal/Drive/cost/risk/feedback/intrinsic-source semantics;
- scalarization вынесена в explicit versioned `ComparisonPolicy`;
- mandatory weighted sum отклонён как canonical representation, но сохранён как baseline/policy family;
- допускаются scalar/nonlinear, Pareto/dominance, lexicographic, constraint-first и learned comparison families;
- `incomparable` является валидным ComparisonResult;
- hard/structural constraints не обязаны превращаться в большие отрицательные reward weights;
- Goal conflicts и Drive conflicts сохраняются до explicit comparison stage;
- External Task Feedback не становится internal utility автоматически;
- Intrinsic Signal magnitude не становится desirability автоматически;
- Appraisal dimensions используются как evidence, но Appraisal не дублируется внутри Valuation;
- Affect может модулировать comparison только через explicit versioned mapping;
- Self Model feasibility/`P(success)`/cost отделены от value и могут использоваться как constraints/components/modulators;
- predictive uncertainty отделена от risk/downside;
- `RiskProfile` требует outcome distribution/adverse semantics/risk measure;
- immediate/local и prospective/horizon-conditioned valuation различаются;
- universal discount factor не принят;
- state/outcome/action/trajectory value surfaces поддерживаются без обязательного `V(s)`/`Q(s,a)` API;
- predicted/imagined/counterfactual valuation сохраняет branch provenance и не становится experienced utility;
- branch-local simulated Drives/Affect могут использоваться только в explicit simulation mode;
- RL reward и critic остаются downstream training/estimator choices;
- normalization/units/revisions являются first-class provenance;
- `NoValuation`, weighted-scalar, shuffled, matched-linear, lexicographic и oracle research controls различаются.

---

# 3. Следующий допустимый Design Update

```text
DU-19 — Salience / Attention
```

Цель `DU-19` — спроектировать **ограниченный механизм приоритизации информации и cognitive processing**, который преобразует relevance/novelty/urgency/value/uncertainty и другие разрешённые signals в явные allocation/prioritization decisions, не смешивая Salience с Appraisal, Utility или Workspace.

Обязательные области:

```text
Salience responsibility / module gate
salience target identity
feature/event/memory/goal/action-candidate salience
input evidence model
Appraisal relevance / urgency
Valuation relation
Intrinsic novelty / information signals
Affect / Drive modulation
bottom-up vs top-down salience
attention budget / resource semantics
ranking vs gating vs allocation
soft vs hard selection
persistence / inhibition / hysteresis
competition / normalization
query-dependent salience
Memory retrieval / retention boundary
Workspace admission boundary
Executive Control boundary
Policy boundary
NoSalience / Dummy / Control
observability / intervention
snapshot / revision / degradation
```

Нужно определить:

- что именно является `Salience Target`;
- является ли Salience scalar score, ranking, allocation distribution или structured policy;
- где проходит граница relevance ↔ salience;
- как high novelty может быть salient без высокой utility и наоборот;
- где проходит граница Valuation ↔ Salience;
- может ли Salience влиять на Memory retrieval/admission до `DU-20` и в какой форме;
- как выражать ограниченный compute/attention budget;
- нужен ли persistent salience/inhibition state;
- как избежать hidden attention внутри Cortex/Policy;
- как Salience передаёт кандидатов будущему Workspace, не становясь самим Workspace;
- какие interventions доказывают causal role priority allocation.

После принятия `DU-19` допускается:

```text
DU-20 — Memory Regulation / Consolidation
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
ValueProfile ≠ ScalarizedValue
ValueProfile ≠ Training Reward
ValueProfile ≠ Critic Value
ValueProfile ≠ Policy Decision
predictive uncertainty ≠ RiskProfile
P(success) ≠ Utility/Value
External Task Feedback ≠ internal utility
Intrinsic Signal ≠ decision value
incomparable valuation ≠ technical failure
```

---

# 5. Что ещё не принято

Пока отсутствуют accepted решения по:

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

Также пока не выбраны exact Python/package/framework решения, concrete Cortex backend, Memory backend/index, World Model architecture, Self Model estimator/calibration method, Intrinsic Signal estimators, concrete Drive list/dynamics, Appraisal dimension subset/estimator, Affect channels/dynamics, ValueComponent subset, ComparisonPolicy/scalarization, risk measure или training reward/critic.

---

# 6. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начинать implementation до появления version roadmap и implementation sequence.
