# Self Model MINDRA

## Статус документа

**Design Update:** `DU-13 — Self Model`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет функциональную модель собственных возможностей и ограничений MINDRA.

Документ определяет:

- responsibility и ownership `Self Model`;
- границу `self` и `world`;
- достоверные self-observable capability facts отдельно от learned competence;
- `Agent Capability Manifest`;
- `Self Evidence`;
- `Self Belief` и context-conditioned competence profile;
- `Self Prediction` для вероятности успеха, стоимости и будущего собственного состояния;
- calibration и различие вероятности события и неопределённости собственной оценки;
- поведение после Learning Update, Cortex/backend swap и module reconfiguration;
- Cortex self-description boundary;
- границу с будущим Executive Control;
- revision/snapshot semantics;
- `NoSelfModel`/Dummy/Control configurations;
- observability/intervention/failure semantics.

Документ опирается на:

- [`../system-context.md`](../system-context.md) — Agent boundary и runtime/infrastructure разделены;
- [`../execution-model.md`](../execution-model.md) — `agent_revision`, causal time и Learning Update имеют явную семантику;
- [`../cognitive-state.md`](../cognitive-state.md) — committed state/provenance/private-state semantics;
- [`../module-lifecycle.md`](../module-lifecycle.md) — staged effects и module scheduling;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — evidence отдельно от intervention;
- [`environment.md`](environment.md) — evaluator/world ground truth не является normal Agent input;
- [`perception.md`](perception.md) — текущее восприятие не является self-knowledge;
- [`goals.md`](goals.md) — Goal state не является competence estimate;
- [`cortex.md`](cortex.md) — текстовое самоописание Cortex не является authoritative self-state;
- [`memory.md`](memory.md) — прошлый опыт доступен через explicit retrieval;
- [`world-model.md`](world-model.md) — прогноз внешнего мира отделён от модели собственных возможностей.

Документ намеренно **не** определяет:

- Metacognitive / Executive Control — `DU-22`;
- выбор действия/стратегии — `DU-23`;
- Valuation — `DU-18`;
- Intrinsic Signals/competence progress — `DU-14`;
- exact learning losses — `DU-26`;
- exact task/domain taxonomy;
- exact probability/calibration estimator;
- exact Python API;
- exact checkpoint encoding — `DU-27`.

---

# 1. Цель DU-13

MINDRA должна уметь функционально оценивать не только внешний мир, но и **собственные возможности как действующего агента**.

Примеры вопросов Self Model:

> «Доступна ли мне сейчас capability X?»

> «Насколько успешно я обычно решаю задачи такого типа в похожих условиях?»

> «Какова вероятность, что я завершу эту конкретную цель при данном контексте?»

> «Сколько внутреннего ресурса или шагов мне, вероятно, потребуется?»

> «Есть ли у меня достаточно evidence, чтобы доверять этой оценке?»

При этом Self Model не должна становиться:

- текстовым personality/profile prompt;
- утверждением о сознании или феноменальном `я`;
- копией World Model;
- Policy/Planner;
- Executive Control;
- Valuation;
- глобальным scalar `confidence`;
- evaluator oracle;
- скрытым доступом ко всей machine/runtime telemetry.

Канонические отношения:

```text
Agent Capability Fact
≠
Learned Competence Estimate
≠
Self Prediction
≠
Cortex Self-Report
```

и:

```text
probability of success
≠
uncertainty of the probability estimate
```

---

# 2. Главное архитектурное решение

MINDRA принимает **гибридную Self Model architecture**, объединяющую:

1. versioned self-observable capability facts;
2. learned/context-conditioned competence beliefs;
3. queryable predictions собственных outcomes/costs;
4. explicit evidence и calibration semantics.

Conceptually:

```text
Agent Capability Manifest
        │
        ├──────────────┐
        │              │
Self Evidence          │
from experience        │
        │              │
        ▼              ▼
        Self Model update
               ↓
      Committed Self Belief
               │
               ├── competence profile
               ├── known limitations
               ├── capability status belief
               └── evidence/calibration state
               │
               + explicit prediction context
               ↓
          Self Prediction
               ├── success probability?
               ├── expected cost/resource?
               ├── expected own future state?
               └── estimate uncertainty/support
```

Self Model может иметь private learned/recurrent representation, но backend-specific latent не становится универсальным межмодульным контрактом.

Решение дополнительно фиксируется в `ADR-0013`.

---

# 3. Responsibility и ownership

## 3.1. Self Model является agent-owned cognitive subsystem

Self Model владеет:

- committed `Self Belief`;
- competence profiles/estimates;
- known/learned limitation state;
- evidence summaries, используемыми для self-estimation;
- causally relevant private state конкретной implementation;
- self-model-specific parameters/adapters;
- calibration-related state;
- self-model-specific research probes.

## 3.2. Self Model отвечает за

- интеграцию self-observable capability facts и опыта;
- оценку собственной competence в конкретном контексте;
- вероятностный прогноз собственного успеха там, где outcome формально определён;
- прогноз собственного resource/cost usage там, где соответствующая величина agent-visible и decision-relevant;
- выражение ограничений и unavailable capabilities;
- поддержку uncertainty/evidence-support собственной оценки;
- актуализацию после behavior-relevant изменения Agent;
- публикацию self-prediction evidence для downstream consumers.

## 3.3. Self Model не отвечает за

- выбор цели;
- выбор действия;
- решение, когда вызвать Cortex/Memory/Planner;
- управление compute budget;
- оценку желательности результата;
- прогноз внешней физической динамики;
- Environment embodiment ground truth;
- прямое изменение других модулей;
- создание natural-language identity/personality.

---

# 4. Self boundary: что относится к `self`

Self Model описывает **функционально значимые свойства Agent как вычислительного/действующего субъекта архитектуры**, а не всё, что связано с телом или процессом исполнения.

## 4.1. Self Model examples

К Self Model могут относиться:

- наличие/доступность declared capability;
- поддерживаемая Cortex capability;
- доступность Memory/World Model/другого optional subsystem;
- компетентность для task/action class;
- вероятность успешного выполнения цели;
- известные failure modes;
- оценка необходимого cognitive/action cost;
- способность использовать определённый interface/tool/action;
- ожидаемая собственная functional state после операции.

## 4.2. Что остаётся World Model/Environment side

Если состояние принадлежит динамике внешнего мира или embodiment Environment, оно по умолчанию не становится Self Model только потому, что относится к телу Agent.

Например:

```text
позиция в MicroWorld
состояние физического inventory
видимое повреждение тела
доступная в мире энергия/заряд
```

могут быть Perception/World Model state в зависимости от Environment contract.

## 4.3. Что остаётся runtime metadata

Не вся telemetry compute substrate является self-knowledge.

Например:

```text
GPU temperature
host PID
CUDA allocator internals
network RTT
случайная latency notebook
```

не становятся Agent-visible только потому, что технически измеримы.

Если некоторый ресурс намеренно влияет на cognition, например explicit remaining Cortex-call budget, он должен быть представлен через отдельную agent-visible boundary и только затем может участвовать в Self Model.

---

# 5. Agent Capability Manifest

Некоторые факты Agent может знать о себе **не через статистическое обучение**, а потому что они являются частью собственной конфигурации.

Для этого вводится concept `Agent Capability Manifest`.

Conceptually он может описывать:

```text
Agent Capability Manifest
├── manifest_revision
├── agent_revision
├── capability entries
│   ├── capability identity
│   ├── enabled / unavailable / degraded
│   ├── declared interface revision
│   ├── declared limits/budgets?
│   └── provenance
└── configuration-change provenance
```

Exact fields не frozen.

## 5.1. Manifest не является Composition Root dump

Self Model не должна получать:

- произвольные Python objects;
- provider clients;
- secret keys;
- hidden evaluator configuration;
- весь process environment;
- private state соседних модулей.

Manifest содержит только **намеренно self-observable функциональные facts**.

## 5.2. Capability availability ≠ competence

```text
Cortex structured-output capability available = true
```

не означает:

```text
Agent успешно решит задачу с вероятностью 1.0
```

Manifest сообщает доступность/contract facts.

Self Model учится оценивать фактическую competence.

---

# 6. Self Evidence

`Self Evidence` — причинно идентифицируемая информация, на которой Self Model может обновлять собственные оценки.

Источники могут включать:

- actual task/action outcome, доступный Agent;
- Goal lifecycle/progress evidence;
- module capability/degradation event;
- committed action execution result;
- explicit resource-use evidence;
- prediction-vs-outcome comparison;
- retrieved собственный прошлый опыт;
- behavior-relevant `agent_revision` change.

## 6.1. Evidence provenance

Нужно различать минимум:

```text
self-observed operational fact
agent-visible external outcome
inferred evidence
Cortex-derived claim
research-supervised label
```

## 6.2. Evaluator leakage запрещён

`Objective Task Metric` или Research Ground Truth нельзя молча использовать как normal Self Model input.

Если Self Model обучается privileged labels в специальном supervised experiment, это должно иметь explicit research provenance и не выдаваться за natural self-learning.

---

# 7. Self Belief

`Self Belief` — committed оценка собственных функциональных свойств Agent.

Она не обязана быть одним object/vector.

Conceptually она может включать:

```text
Self Belief
├── self_belief_revision
├── agent_revision basis
├── capability-state beliefs
├── competence profiles
├── known limitations
├── evidence/support metadata
├── calibration state
└── provenance
```

Backend может поддерживать private latent state, но consumers не получают его автоматически.

---

# 8. Competence не является глобальным scalar

MINDRA не принимает универсальную переменную:

```text
competence = 0.78
```

без определения области применимости.

Competence должна быть context-conditioned.

Conceptually профиль может быть условным относительно:

```text
task family / objective kind
environment distribution
required capability set
language/modality
action/strategy family
relevant state context
agent revision
```

Точная taxonomy проектируется позже.

Один Agent может одновременно иметь:

```text
высокую competence для navigation
низкую competence для hidden-rule discovery
неизвестную competence для нового language/task family
```

---

# 9. Self Prediction

Self Model должна поддерживать explicit prediction request вместо ambient глобального confidence.

Conceptually:

```text
SelfPredictionRequest
├── target event/outcome
├── context references
├── goal/task reference?
├── candidate action/strategy reference?
├── horizon / completion condition
├── required estimate channels
└── causal provenance
```

Результат может включать:

```text
SelfPrediction
├── prediction identity
├── probability of defined success event?
├── expected cost/resource usage?
├── expected own functional-state outcome?
├── estimate uncertainty/support
├── applicability/domain metadata
├── self-model/agent revision
└── provenance
```

Prediction не выбирает action и не меняет Goal.

---

# 10. `P(success)` имеет смысл только для формального события

Число:

```text
P(success) = 0.73
```

имеет смысл только если определены:

- что считается success;
- какой horizon/termination condition;
- для какого Goal/task/context;
- какая `agent_revision`;
- какие capabilities доступны;
- на какой evidence domain основана оценка.

Запрещено публиковать универсальное `confidence = 0.73`, если неизвестно, что именно прогнозируется.

---

# 11. Probability of success и estimate uncertainty — разные оси

Self Model должна различать:

```text
predicted probability of outcome
```

и:

```text
насколько хорошо сама Self Model поддерживает эту оценку evidence
```

Например:

```text
P(success) = 0.70
estimate_support = low
```

может означать:

> «если моя текущая модель применима, шанс примерно 70%, но похожего опыта мало».

Это отличается от:

```text
P(success) = 0.70
estimate_support = high
```

Точная математическая форма `estimate uncertainty` не frozen.

---

# 12. Calibration

Self Model должна проектироваться как **проверяемый вероятностный predictor**, а не как генератор убедительно звучащей уверенности.

Для прогнозов с бинарным success outcome будущая evaluation должна иметь возможность связывать:

```text
SelfPrediction
        ↓
later actual outcome
        ↓
Prediction Resolution
        ↓
calibration evidence
```

Будущие метрики могут включать proper scoring rules и calibration diagnostics, но exact MINDRA-Eval набор определяется в `DU-28`.

Ключевой invariant:

> Хорошая Self Model должна быть не только discriminative, но и calibrated на заявленной области применимости.

---

# 13. Prediction Resolution

Для обучения и оценки полезно сохранять связь между forecast и фактическим outcome.

Conceptually:

```text
SelfPrediction SP42
    P(success)=0.8
          ↓
реальный опыт / Goal outcome
          ↓
SelfPredictionResolution
    outcome = success/failure/unknown
    resolution provenance
```

Если outcome невозможно определить из agent-visible/разрешённого evidence, resolution остаётся `unknown`, а не подменяется evaluator truth.

---

# 14. Изменение Agent и устаревание self-knowledge

После behavior-relevant изменения:

```text
Learning Update
Cortex swap
adapter revision change
module enable/disable
capability degradation/recovery
```

старые competence estimates нельзя молча считать полностью актуальными.

Self Model должна знать basis:

```text
agent_revision / capability_manifest_revision
```

и иметь semantics для:

```text
valid
stale / partially transferable
unknown after change
recalibrating
```

Точный transfer policy не frozen.

Например, замена Cortex 0.8B на 2B не должна автоматически давать старому `P(success)` новый смысл только потому, что остальная архитектура не изменилась.

---

# 15. Resource и cost estimates

Self Model может прогнозировать только те resource/cost величины, которые:

1. имеют определённую semantic boundary;
2. действительно могут влиять на future decision/execution;
3. agent-visible по design;
4. измеримы без скрытого leakage.

Примеры возможных каналов:

```text
expected number of cognitive cycles
expected Cortex-call count
expected action count
remaining declared budget compatibility
expected Memory retrieval count/cost class
```

Wall-clock latency не становится cognitive cost автоматически.

---

# 16. Self Model и World Model

Канонически:

```text
World Model
→ что происходит/произойдёт во внешнем мире

Self Model
→ что способен/вероятно сможет сделать сам Agent
```

Граница может пересекаться на embodiment/action outcome, но ownership не должен дублироваться.

Пример:

```text
World Model:
дверь тяжёлая и откроется при силе > X

Self Model:
моя текущая capability выполнить соответствующее действие имеет такую-то competence/ограничение
```

Совместный downstream predictor может использовать оба результата, но это не делает Self Model расширением World Model.

---

# 17. Self Model и Cortex

Cortex может помочь:

- классифицировать task/capability domain;
- сформировать hypothesis о limitation;
- интерпретировать natural-language self-evidence;
- дать candidate self-assessment.

Но natural-language ответ:

> «Я уверен, что справлюсь»

не становится `Self Belief` автоматически.

Cortex self-report имеет provenance `Cortex-derived` и должен проходить semantic owner boundary Self Model.

Нельзя использовать pretraining-derived идентичность вроде знания названия модели как доказательство реальной runtime capability, если это не подтверждено manifest/evidence.

---

# 18. Self Model и Executive Control

Это принципиальная граница:

```text
Self Model
→ оценивает

Executive Control
→ решает, что делать с оценкой
```

Например Self Model может сказать:

```text
P(success without retrieval) = low
P(success with extra reasoning) = unknown
```

Но решение:

```text
вызвать ли Memory
вызвать ли Cortex
сделать ли ещё Cognitive Cycle
передать ли задачу другому механизму
```

принадлежит будущему `DU-22` и/или Policy.

Self Model не должна скрыто регулировать cognition только потому, что её оценка низкая.

---

# 19. Self Model и Valuation

Self Model сообщает prediction/competence/cost evidence.

Она не решает, хорошо это или плохо.

```text
P(success)=0.3
```

может быть приемлемо для дешёвой exploratory задачи и неприемлемо для дорогой/опасной.

Такое decision relevance будет обязанностью Valuation/Policy, а не Self Model.

---

# 20. Revision semantics

Нужно различать:

```text
agent_revision
capability_manifest_revision
self_model_revision
self_belief_revision
prediction_id
calibration/evidence state revision
```

Learning Update Self Model parameters создаёт новую `self_model_revision` и новую `agent_revision` согласно общим правилам.

Обновление committed `Self Belief` на новом evidence не обязано означать изменение trainable parameters.

---

# 21. Snapshot / restore

Exact Agent snapshot должен учитывать causally relevant Self Model state:

```text
Self Model parameters/revision
committed Self Belief
private recurrent/latent state
capability manifest identity
calibration/evidence summaries
RNG state
intervention/degradation state
```

Если часть learned competence externalized в separate store, она всё равно является agent-owned state и должна участвовать в snapshot semantics.

---

# 22. Observability

Evidence должна позволять исследователю видеть минимум:

- capability manifest revision;
- self-belief revision;
- competence estimate domain;
- SelfPrediction request/result;
- probability target semantics;
- estimate support/uncertainty;
- evidence source summary;
- prediction resolution;
- calibration state/metrics artifact references;
- stale/invalidation event после Agent change;
- Cortex assistance provenance;
- intervention/degradation.

Raw private latent не является обязательным public output.

---

# 23. Interventions

Полезные research interventions:

- изменить конкретную competence estimate при неизменной реальной capability;
- сделать Self Model искусственно overconfident;
- сделать её underconfident;
- убрать/скрыть capability manifest entry;
- дать stale competence profile;
- подменить prediction shuffled/control estimate;
- изменить estimate-support signal независимо от `P(success)`;
- сравнить accurate vs miscalibrated Self Model.

Все interventions проходят через `Intervention Gateway` и создают experimental lineage/provenance.

Ключевой causal experiment будущего:

```text
same Agent capability
same Environment state
same Goal
same World Belief

control:
Self estimate = calibrated

treatment:
Self estimate = systematically overconfident

→ измерить downstream strategy/action/compute behavior
```

До `DU-22/23` сам downstream механизм ещё не определён.

---

# 24. Configurations

Нужно различать:

```text
NoSelfModel
DummySelfModel
ControlSelfModel
real SelfModel
```

## NoSelfModel

Self Model capability отсутствует.

## DummySelfModel

Deterministic engineering implementation для integration tests.

## ControlSelfModel

Research baseline, например:

- constant confidence;
- global empirical success rate;
- shuffled competence profile;
- recency-only estimate;
- oracle-calibrated research control;
- parameter/cost-matched predictor.

Oracle control не является normal Agent configuration.

---

# 25. Failure / degradation

Нужно различать минимум:

```text
Self Model unavailable
capability manifest stale/incompatible
insufficient evidence
estimate out-of-domain
prediction target unsupported
self-belief stale after agent revision
calibration state unavailable
Cortex assistance failure
snapshot incompatibility
```

Универсальный `confidence=0.5` не должен скрывать отсутствие модели/данных.

---

# 26. Evaluation implications

Будущий `MINDRA-Eval` должен проверять как минимум:

## 26.1. Prediction quality

Насколько Self Model предсказывает собственный success/failure/cost.

## 26.2. Calibration

Если она говорит `P(success)≈0.8` на большой группе сопоставимых прогнозов, фактическая частота успеха должна быть близка к 0.8 в заявленном domain.

## 26.3. Discrimination

Успешные случаи должны в среднем получать более высокие предсказанные вероятности, чем неуспешные, если target это допускает.

## 26.4. Adaptation after self-change

После Cortex/module/training revision Self Model должна корректно помечать/перестраивать старые оценки, а не использовать их как вечную истину.

## 26.5. Causal utility

Сравнивать:

```text
accurate Self Model
miscalibrated Self Model
shuffled/control Self Model
NoSelfModel
```

и измерять downstream effect после появления Executive Control/Policy.

## 26.6. Leakage control

Проверять, не использует ли Self Model evaluator-only truth.

---

# 27. Research hypotheses, которые DU-13 делает проверяемыми

Позже можно будет формализовать гипотезы:

### H-SM-1

Context-conditioned Self Model лучше предсказывает собственный успех, чем global empirical confidence baseline.

### H-SM-2

Calibrated self-estimates улучшают decision/resource allocation после подключения Executive Control.

### H-SM-3

Systematic overconfidence и underconfidence причинно вызывают различимые downstream стратегии при одинаковых реальных capabilities.

### H-SM-4

Self Model способна адаптировать competence beliefs после behavior-relevant Agent revision.

Эти формулировки пока являются design-ready направлениями, а не зарегистрированными hypothesis records.

---

# 28. Открытые implementation questions

`DU-13` намеренно оставляет открытыми:

- parametric neural vs statistical/table/hybrid competence model;
- representation task/capability domain;
- calibration method;
- uncertainty estimator;
- sliding-window vs lifelong evidence aggregation;
- transfer competence между Agent revisions;
- exact cost channels;
- Cortex participation;
- online update algorithm;
- exact training targets/losses;
- exact public/private state schema.

Эти решения должны приниматься в последующих design/version updates, а не скрыто внутри реализации.
