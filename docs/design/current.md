# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-13` завершены и приняты. Реализация ещё не начата.**

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
- candidate contracts Environment, Perception, Goals, Cortex, Memory, World Model и Self Model;
- тринадцать accepted ADR.

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
```

## DU-13

Канонический документ:

- [`modules/self-model.md`](modules/self-model.md).

Candidate contract:

- [`contracts/self-model.md`](contracts/self-model.md).

Research pass:

- [`../research/literature/DU-13-self-model-landscape-2026-08.md`](../research/literature/DU-13-self-model-landscape-2026-08.md).

Accepted decision:

- [`ADR-0013`](decisions/ADR-0013-hybrid-functional-self-model.md).

Главные результаты:

- Self Model является agent-owned functional cognitive subsystem, а не personality/self-awareness claim;
- self-observable `Agent Capability Manifest` отделён от learned competence;
- capability availability не означает фактическую competence;
- `Self Evidence` имеет явную provenance и не получает evaluator-only truth normal runtime способом;
- `Self Belief` context/domain-conditioned и не сводится к одному global scalar;
- Self Prediction имеет explicit target/context/horizon;
- `P(success)` имеет смысл только относительно формального outcome;
- probability of success отделена от uncertainty/support самой оценки;
- SelfPredictionResolution связывает forecast с фактическим outcome для calibration evidence;
- старые competence estimates могут стать stale после behavior-relevant `agent_revision`/capability-manifest change;
- internal resource/cost channels должны быть explicit agent-visible semantics, а не произвольная host telemetry;
- Self Model отделена от World Model, Valuation и Executive Control;
- Cortex self-report является optional derived evidence, а не canonical self-knowledge;
- Self Model оценивает собственную capability/competence, но не решает, как действовать на основании оценки;
- exact Agent snapshot обязан учитывать causally relevant Self Model state;
- `NoSelfModel`, Dummy и Control configurations различаются;
- accurate/miscalibrated/shuffled/NoSelfModel comparison является будущим causal evaluation pattern.

---

# 3. Следующий допустимый Design Update

```text
DU-14 — Intrinsic Signals
```

Цель `DU-14` — определить **нейтральные внутренние сигналы, выводимые из структуры собственного опыта Agent**, до появления Drives/Valuation: novelty, prediction surprise/error, information gain, uncertainty reduction, competence progress и visitation rarity как возможные измеряемые свойства опыта.

Обязательные области:

```text
Intrinsic Signal responsibility / ownership
signal vs reward / drive / utility boundary
prediction-error source from World Model
novelty semantics
information gain / uncertainty reduction
competence-progress source from Self Model
state/event visitation rarity
normalization / scale / stationarity
per-step vs event/window aggregation
representation dependence / drift
source provenance
online computability without evaluator leakage
NoSignal / Dummy / Control variants
observability / intervention
failure / degradation
```

Нужно определить:

- нужен ли один `Intrinsic Signal` module или несколько provider capabilities;
- какие signals являются свойствами события/обновления, а какие требуют temporal baseline/history;
- чем raw prediction error отличается от surprise и novelty;
- когда information gain можно оценивать корректно;
- как competence progress использует Self Model predictions/resolutions, не становясь self-reward автоматически;
- как representation drift влияет на novelty/distance signals;
- как избежать нестационарной шкалы, делающей разные signals несопоставимыми;
- как не превратить intrinsic signal сразу в reward/utility;
- какие random/shuffled/constant controls нужны для causal evaluation.

После принятия `DU-14` допускается:

```text
DU-15 — Drives
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
```

---

# 5. Что ещё не принято

Пока отсутствуют accepted решения по:

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

Также пока не выбраны exact Python/package/framework решения, concrete Cortex backend, Memory backend/index, World Model architecture, Self Model estimator/calibration method или uncertainty estimator.

---

# 6. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начинать implementation до появления version roadmap и implementation sequence.
