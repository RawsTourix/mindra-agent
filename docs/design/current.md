# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-14` завершены и приняты. Реализация ещё не начата.**

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
- candidate contracts Environment, Perception, Goals, Cortex, Memory, World Model, Self Model и Intrinsic Signals;
- четырнадцать accepted ADR.

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
```

## DU-14

Канонический документ:

- [`modules/intrinsic-signals.md`](modules/intrinsic-signals.md).

Candidate contract:

- [`contracts/intrinsic-signals.md`](contracts/intrinsic-signals.md).

Research pass:

- [`../research/literature/DU-14-intrinsic-signals-landscape-2026-08.md`](../research/literature/DU-14-intrinsic-signals-landscape-2026-08.md).

Accepted decision:

- [`ADR-0014`](decisions/ADR-0014-multi-provider-intrinsic-signal-layer.md).

Главные результаты:

- Intrinsic Signal является измеряемым свойством опыта, а не reward/Drive/Utility;
- принят multi-provider layer вместо одного `IntrinsicRewardModule`;
- provider outputs остаются typed и не обязаны scalarize в одно число;
- prediction discrepancy отделён от probabilistic predictive surprisal;
- novelty отделена от prediction error и visitation rarity;
- persistent prediction error не трактуется автоматически как learnable opportunity;
- information gain допустим только при meaningful before/after knowledge semantics;
- uncertainty change имеет explicit signed convention и compatible estimator revisions;
- competence change основан на temporal Self Model evidence и сохраняет знак improvement/degradation;
- novelty/rarity имеют reference history/scope и representation identity;
- representation drift/normalization/provider revisions входят в signal provenance;
- raw и normalized measure различаются;
- online normalization обязана быть causal и versioned;
- actual/replayed/imagined/intervened/offline signal provenance различается;
- replay sample не считается новым посещением normal runtime способом;
- evaluator-only ground truth не используется natural providers;
- stateful provider history/count/baseline/normalizer/RNG входит в exact Agent snapshot;
- `NoIntrinsicSignals`, Dummy, Constant, Random, Shuffled и Control providers различаются.

---

# 3. Следующий допустимый Design Update

```text
DU-15 — Drives
```

Цель `DU-15` — определить **долгоживущие внутренние регуляторные переменные**, которые превращают нейтральные properties опыта в контекстно зависимое внутреннее давление, не смешивая Drive с Goal, signal, utility или action policy.

Обязательные области:

```text
Drive responsibility / ownership
Drive state vs Intrinsic Signal boundary
homeostatic / set-point semantics
need / deficit / pressure representation
state dynamics over time
sources of update
saturation / decay / recovery
cross-drive interaction
Drive scope / persistence
Drive → Goal Proposal boundary
Drive → Valuation boundary
external manipulation vs natural regulation
NoDrive / Dummy / Control variants
snapshot / observability / intervention
failure / degradation
```

Нужно определить:

- нужен ли общий `Drive System` или независимые typed drives;
- какие drives имеют true homeostatic target, а какие лучше моделировать как adaptive motivational state;
- может ли novelty-seeking быть Drive, если novelty уже signal;
- как Drive state меняется при отсутствии нового внешнего события;
- как не превратить Drive в скрытый scalar reward;
- как несколько drives конфликтуют/насыщаются;
- должен ли Drive напрямую создавать Goal или только `Goal Proposal`;
- как causal intervention одного drive проверяет specificity downstream эффекта;
- какие controls отличают meaningful drive dynamics от дополнительного state/noise.

После принятия `DU-15` допускается:

```text
DU-16 — Appraisal
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
```

---

# 5. Что ещё не принято

Пока отсутствуют accepted решения по:

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

Также пока не выбраны exact Python/package/framework решения, concrete Cortex backend, Memory backend/index, World Model architecture, Self Model estimator/calibration method, Intrinsic Signal estimators или common normalization/scalarization policy.

---

# 6. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начинать implementation до появления version roadmap и implementation sequence.
