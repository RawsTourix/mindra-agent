# Valuation MINDRA

## Статус документа

**Design Update:** `DU-18 — Valuation`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет decision-relevant слой MINDRA — `Valuation System`, который строит сравнимое представление ценности candidate states/outcomes/actions/trajectories из разнородного agent-owned evidence, сохраняя структуру конфликтующих целей, drives, рисков и costs до явно определённой стадии сравнения.

Документ определяет:

- responsibility и ownership `Valuation System`;
- `Valuation Target` и causal provenance;
- typed multi-objective `ValueProfile`;
- явную границу `ValueProfile → Comparison/Aggregation Policy`;
- Goal/Drive/Appraisal/Affect integration;
- external feedback и Intrinsic Signals boundary;
- feasibility/cost evidence Self Model;
- risk/downside и predictive uncertainty boundary;
- state/outcome/action/trajectory valuation;
- immediate/prospective/horizon semantics;
- vector/structured value и optional scalarization;
- Pareto/lexicographic/constrained/scalar comparison families;
- predicted/imagined/counterfactual valuation;
- rule-based, learned и hybrid implementations;
- границу с RL reward/value-function/critic;
- observability/intervention;
- `NoValuation`/Dummy/Control configurations;
- revision/snapshot/failure/degradation requirements.

Документ опирается на:

- [`../execution-model.md`](../execution-model.md) — causal provenance и logical time;
- [`../cognitive-state.md`](../cognitive-state.md) — committed state/revisions/availability;
- [`../module-lifecycle.md`](../module-lifecycle.md) — staged computation/atomic commit;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — evidence/intervention;
- [`goals.md`](goals.md) — Goal Graph, priority/commitment/progress;
- [`drives.md`](drives.md) — persistent typed regulatory state;
- [`appraisal.md`](appraisal.md) — event-level multidimensional meaning;
- [`affect.md`](affect.md) — persistent history-dependent modulation;
- [`world-model.md`](world-model.md) — prediction, imagination, uncertainty;
- [`self-model.md`](self-model.md) — competence/feasibility/cost predictions;
- [`intrinsic-signals.md`](intrinsic-signals.md) — neutral internal measurements;
- [`environment.md`](environment.md) — external task feedback и objective metric boundary.

Документ намеренно **не** определяет:

- Policy/Planner — `DU-23`;
- Salience/Attention — `DU-19`;
- конкретную RL reward function;
- конкретный critic architecture;
- mandatory discount factor `gamma`;
- mandatory weighted sum;
- mandatory Pareto/lexicographic/CVaR strategy;
- training objectives/losses — `DU-26`;
- exact Python API/checkpoint encoding — `DU-27`;
- safety/normative preference system, если он отдельно не спроектирован;
- subjective pleasure/pain или phenomenal experience.

---

# 1. Цель DU-18

К `DU-18` MINDRA уже умеет отдельно представлять:

```text
что является текущей целью                    → Goal System
каково регуляторное состояние                 → Drives
что означает конкретное событие               → Appraisal
каков history-dependent affective context      → Affect
что вероятно произойдёт                        → World Model
на что способен сам Agent                      → Self Model
что в опыте ново/редко/информативно            → Intrinsic Signals
```

Но отсутствует единая ответственность, отвечающая на вопрос:

> «Как сравнить несколько возможных состояний, исходов, действий или trajectories с точки зрения текущих committed concerns Agent?»

Важно, что ответ не обязан быть одним числом.

`Valuation System` вводит explicit decision-relevant evaluation boundary, сохраняя происхождение отдельных value components и выполняя scalarization/ordering только через versioned comparison policy.

---

# 2. Module gate

Отдельный `Valuation System` проходит module gate по следующим основаниям:

1. **Самостоятельная ответственность.** Ни Goals, ни Drives, ни Appraisal, ни Affect сами не сравнивают разнородные candidate consequences.
2. **Отдельный semantic output.** `ValueProfile` является decision-relevant representation, а не source signal.
3. **Отдельная comparison boundary.** Конфликт нескольких concerns должен разрешаться явно, а не hidden weighted sum в Policy.
4. **Отдельная intervention surface.** Можно менять comparison/aggregation policy при неизменных source signals и проверять downstream behavior.
5. **Отдельная evaluation strategy.** Можно проверять consistency, preference sensitivity, risk behavior и causal contribution независимо от Policy.
6. **Граница с training.** Algorithm-specific reward/critic не должен неявно становиться архитектурным определением ценности Agent.

`Valuation System` при этом **не выбирает действие**. Он может ранжировать/сравнивать candidates, но `Action Commit` остаётся responsibility будущего Policy/Action boundary.

---

# 3. Канонические различия

```text
External Task Feedback
≠
Intrinsic Signal
≠
Drive State
≠
Appraisal
≠
Affect State
≠
ValueProfile
≠
Scalarized Value
≠
Training Reward
≠
RL Critic Value
≠
Policy Decision
```

Особенно:

```text
predictive uncertainty
≠
risk / downside

P(success)
≠
value

Appraisal polarity
≠
utility

Drive pressure
≠
utility
```

---

# 4. Главное архитектурное решение

MINDRA принимает **typed multi-objective Valuation System с явной comparison/scalarization boundary**.

Conceptually:

```text
Valuation Target
      +
committed context / predicted consequences
      +
source evidence
      │
      ├── Goal impact
      ├── Drive regulation impact
      ├── Appraisal evidence
      ├── Affect modulation context
      ├── External Feedback semantics?
      ├── Intrinsic Signals semantics?
      ├── Self feasibility / effort / resource cost
      ├── World outcome distribution
      └── constraints / downside evidence
      ↓
   Valuation System
      ↓
    ValueProfile
      ↓
explicit ComparisonPolicy
      ↓
ComparisonResult
├── preferred / dominated / incomparable / tie
├── constraint status
├── Pareto relation?
├── lexicographic relation?
└── optional ScalarizedValue
```

Нет обязательного:

```text
value = sum(w_i * component_i)
```

Нет обязательного:

```text
reward = value
```

Нет обязательного:

```text
action = argmax(value)
```

Решение фиксируется `ADR-0018`.

---

# 5. Valuation Target

`Valuation Target` — причинно идентифицируемый объект, относительно которого строится decision-relevant evaluation.

Допустимые target families:

```text
state / belief state
actual outcome
predicted outcome
candidate action + predicted consequences
imagined trajectory / plan branch
counterfactual branch
Goal-related terminal/progress state
```

Само имя action без expected consequences/cost context обычно недостаточно для содержательной valuation.

Target обязан сохранять:

- target identity;
- target kind;
- actual/predicted/imagined/counterfactual provenance;
- base state/decision revision;
- horizon;
- World Model revision, если target predicted;
- branch lineage;
- intervention provenance.

`Valuation Target` не становится observed fact только потому, что ему присвоена высокая ценность.

---

# 6. ValueProfile

Канонический `ValueProfile` — **structured typed representation**, а не обязательный scalar/vector одного dtype.

Conceptually:

```text
ValueProfile
├── valuation_id
├── target reference
├── context references
├── component_set
├── constraint_profile?
├── risk_profile?
├── feasibility_profile?
├── temporal/horizon semantics
├── source revisions
├── normalization/comparability metadata
├── availability/confidence/support
└── provenance
```

Каждый component сохраняет semantic identity.

Одинаковое числовое значение двух components не означает одинаковых единиц или одинаковой важности.

---

# 7. Value Component

`ValueComponent` — decision-relevant contribution определённой семантики.

Минимально полезные component families:

## 7.1 Goal impact

Ожидаемое отношение target к конкретному Goal:

```text
Goal G17
→ progress / completion / obstruction / failure risk / neutral / unknown
```

Goal priority/commitment остаются source semantics Goal System и не превращаются автоматически в числовой weight.

## 7.2 Drive regulation impact

Ожидаемое изменение конкретного drive:

```text
Drive D3
→ predicted pressure reduction / increase / no change / unknown
```

Текущий `Drive Pressure` сам по себе не является value target.

## 7.3 Appraisal-derived evidence

Valuation может читать relevant Appraisal dimensions, например:

- goal congruence;
- drive conduciveness;
- controllability;
- coping potential;
- urgency;
- local polarity view, если она явно доступна.

Appraisal не становится готовой utility; Valuation обязана сохранять, какие dimensions использованы.

## 7.4 Affect modulation

`AffectState` может менять valuation sensitivity/context, если concrete policy это объявляет.

Например, тот же predicted downside может иметь другую decision relevance при разных Affect contexts.

Но запрещено универсальное:

```text
negative affect → negative value
positive affect → positive value
```

## 7.5 External feedback contribution

Agent-visible `External Task Feedback` может быть source evidence **только через explicit semantic mapping**.

Environment feedback не становится автоматически внутренней utility.

Evaluator-only `Objective Task Metric` natural Valuation не читает.

## 7.6 Intrinsic-signal contribution

Novelty/information gain/competence change и другие Intrinsic Signals могут участвовать в Valuation только через explicit mapping/policy.

```text
novelty = high
```

не означает автоматически:

```text
value = high
```

## 7.7 Effort/resource/cost contribution

Если Agent имеет explicit self-visible cost/resource semantics, Self Model/другой owner может предоставить evidence:

- expected effort;
- expected compute use;
- probability of successful execution;
- expected resource consumption;
- known capability limitations.

`P(success)`/cost не являются utility сами по себе; comparison policy решает, как они ограничивают/модифицируют candidate.

---

# 8. Source preservation

Valuation не имеет права уничтожать происхождение компонентов до comparison stage.

Неправильно:

```text
Goal + Drive + Appraisal + Affect
→ value = 0.61
```

как единственный canonical output.

Правильно:

```text
ValueProfile
├── goal.G1 = facilitating/high-support
├── goal.G2 = obstructing/medium-support
├── drive.D1 = predicted reduction
├── drive.D2 = predicted increase
├── effort = medium
├── risk = tail downside present
└── ...
```

и только затем explicit comparison.

---

# 9. Comparison Policy

`ComparisonPolicy` — versioned semantic rule, преобразующее один или несколько `ValueProfile` в relation/ordering/optional scalar.

Conceptually:

```text
ComparisonPolicy
├── policy_id
├── policy_revision
├── required component schema
├── normalization policy
├── constraints
├── preference/priority semantics
├── risk semantics
├── temporal aggregation semantics
├── tie/incomparability semantics
└── learned/fixed capability
```

Comparison policy **не является Policy/Planner**.

Она отвечает:

> «Как сравнивать value profiles?»

Policy отвечает позже:

> «Какое действие фактически выбрать с учётом valuation и других decision mechanisms?»

---

# 10. Допустимые comparison families

Canonical architecture допускает несколько семейств.

## 10.1 Weighted/scalar utility

```text
u = f(components; weights/context)
```

Допустимо как explicit policy.

Но weights имеют identity/revision/provenance и не возникают из воздуха.

## 10.2 Pareto/dominance relation

Candidate A может доминировать B по всем relevant objectives без ранней scalarization.

Если A лучше по одному concern, а B по другому, они могут остаться `incomparable` до additional preference context.

## 10.3 Lexicographic comparison

Некоторые priorities/constraints могут иметь строгий порядок:

```text
сначала удовлетворить criterion C1
при равенстве — C2
затем C3
```

Такой режим не эквивалентен большим weights в linear sum.

## 10.4 Constraint-first comparison

Некоторые условия могут быть `constraint`, а не soft negative reward.

Conceptually:

```text
feasible candidates
→ value comparison

constraint-violating candidate
→ separate status / policy
```

## 10.5 Nonlinear/context-conditioned utility

Допускается nonlinear aggregation, если semantics explicit и versioned.

## 10.6 Learned comparison

Comparison может быть learned, но training target/data/provenance должны быть известны. Learned comparator не получает право скрыть evaluator preference как будто она естественно принадлежит Agent.

`DU-18` не выбирает universal comparison family.

---

# 11. Scalarization

Scalarization разрешена, но является **derived operation**.

```text
ValueProfile
+
ComparisonPolicy P17
        ↓
ScalarizedValue
```

`ScalarizedValue` обязан сохранять:

- policy identity/revision;
- source ValueProfile IDs;
- component revisions;
- normalization revision;
- horizon;
- risk semantics;
- provenance.

Числа scalarized разными policies/revisions нельзя считать напрямую совместимыми без explicit compatibility semantics.

---

# 12. Priority и preference sources

Valuation не создаёт hidden «истинные желания» Agent.

Preference context может использовать только explicit agent-owned sources, например:

- Goal structural priority/commitment;
- Drive state/dynamics semantics;
- explicit agent-visible constraints;
- Affect modulation policy;
- learned preference parameters, если они имеют отдельный training/provenance contract;
- externally supplied task preference, если она agent-visible и contractually разрешена.

Developer/evaluator preference не становится internal preference молча.

---

# 13. Multi-objective conflict

Если Goal G1 и G2 конфликтуют:

```text
Target A:
G1 +
G2 -

Target B:
G1 -
G2 +
```

`ValueProfile` обязан сохранить конфликт.

Он не должен автоматически превращаться в:

```text
A = 0.1
B = 0.2
```

до explicit comparison policy.

`incomparable` является допустимым результатом valuation comparison, а не ошибкой.

---

# 14. Immediate и prospective value

MINDRA различает минимум:

```text
immediate / local valuation
prospective / horizon-conditioned valuation
```

## 14.1 Immediate valuation

Оценивает непосредственно target/outcome относительно current concerns.

## 14.2 Prospective valuation

Оценивает predicted/imagined sequence последствий на explicit horizon.

Conceptually:

```text
current state
+ candidate action
→ World Model rollout
→ sequence of target states/outcomes
→ trajectory ValueProfile
```

Никакой universal discount factor не является частью architecture.

Temporal aggregation policy должна иметь identity/revision.

---

# 15. State Value / Action Value / Outcome Value / Trajectory Value

MINDRA не фиксирует один universal `V(s)` или `Q(s,a)` как основной contract.

Допустимы разные target surfaces:

```text
State/Bief valuation
Outcome valuation
Candidate-action valuation
Trajectory/plan valuation
```

`StateValue` и `ActionValue` в классическом RL могут быть implementation views/estimators конкретного Valuation backend, но не определяют саму архитектурную семантику ценности.

Это позволяет rule-based/planning и learned critic implementations существовать за одной границей.

---

# 16. Risk и uncertainty

Канонически:

```text
predictive uncertainty
≠
risk
≠
downside
≠
constraint violation probability
```

## 16.1 Predictive uncertainty

World Model сообщает, насколько неопределён prediction.

## 16.2 Downside

Насколько конкретные возможные outcomes неблагоприятны относительно explicit value concerns.

## 16.3 Risk

Decision-relevant construct, объединяющий outcome distribution и explicit risk semantics.

Например, concrete implementation может использовать:

- expected outcome;
- lower quantile;
- tail probability;
- CVaR-like statistic;
- probability of violating constraint;
- worst-case bound.

Но ни одна measure не является mandatory.

Если World Model не предоставляет подходящую distribution/uncertainty semantics, соответствующий RiskProfile может быть `unavailable`, а не выдумываться из одного confidence scalar.

---

# 17. RiskProfile

Conceptually:

```text
RiskProfile
├── target/reference distribution
├── adverse-event definitions
├── loss/downside semantics
├── risk measure identity
├── horizon
├── estimate/support
├── model revision
└── provenance
```

Risk без определения adverse outcome бессодержателен.

Evaluator-only catastrophic label нельзя использовать natural способом, если Agent его не знает.

---

# 18. Feasibility и value

`Self Model` может сообщить:

```text
P(success | action/task/context)
expected effort
known limitation
```

Это не готовая value.

Valuation может использовать feasibility как:

- constraint;
- multiplicative/modulating evidence;
- отдельный component;
- tie breaker;
- source для risk/cost calculation.

Конкретная semantics задаётся ComparisonPolicy.

Нельзя скрыто делать:

```text
value = utility * P(success)
```

как universal rule.

---

# 19. Actual, predicted и imagined valuation

## Actual/retrospective

Оценивается произошедший target относительно текущего или historical context, явно указанного request.

## Predicted

Оценивается World Prediction, но value record сохраняет `predicted` provenance.

## Imagined

Оценивается branch внутри World Model imagination.

Imagined valuation:

- не является experienced utility;
- не меняет Environment history;
- не становится автоматически Memory;
- может использовать simulated Affect/Drive state branch, если соответствующие models поддерживают branch-local simulation.

## Counterfactual

Сравниваются branch-local ValueProfiles от общего base snapshot.

---

# 20. Branch-local internal dynamics

Для длинной imagined trajectory недостаточно оценивать каждый step относительно неизменного реального Drive/Affect state, если hypothesis требует моделировать внутреннее изменение.

Допустимы два explicit режима:

```text
static-context valuation
```

или:

```text
simulated-internal-state valuation
```

Во втором режиме predicted branch может иметь:

- simulated Drive evolution;
- simulated Affect evolution;
- Goal progress updates;
- updated World Belief.

Эти states остаются branch-local и не commit'ятся в real Agent.

Mode обязан быть записан в provenance.

---

# 21. External Task Feedback

Agent-visible feedback может играть разные роли:

1. evidence о Goal progress/outcome;
2. отдельный value component через explicit mapping;
3. training signal позднее;
4. вообще не входить в internal valuation.

Эти роли нельзя смешивать.

```text
external feedback = +1
```

не означает автоматически:

```text
internal utility = +1
```

`Objective Task Metric` из Environment Research Plane natural Valuation не видит.

---

# 22. Intrinsic Signals boundary

Аналогично:

```text
novelty = 0.9
```

не означает:

```text
utility = 0.9
```

Если Agent ценит exploration/learning, mapping должен быть explicit и может зависеть от:

- current Drive State;
- Goal context;
- uncertainty;
- learning stage;
- ComparisonPolicy.

Это позволяет один и тот же novelty signal делать decision-relevant в одном состоянии и почти нейтральным в другом.

---

# 23. Affect boundary

Affect может:

- модулировать sensitivity к некоторым components;
- участвовать в risk/urgency weighting;
- изменять context-conditioned comparison;
- не участвовать вообще в определённой implementation.

Но `AffectState` не является hidden weight vector по умолчанию.

Любое Affect → Valuation mapping versioned, observable и intervenable.

---

# 24. Appraisal boundary

Appraisal уже предоставляет event meaning.

Valuation не должна повторно независимо вычислять:

- goal congruence;
- drive conduciveness;
- controllability;
- coping potential;
- urgency;
- expectedness.

Она может использовать их как source evidence и преобразовывать в decision-relevant components через explicit mapping.

Иначе Appraisal и Valuation начнут дублировать друг друга.

---

# 25. Reward boundary

`Training Reward` — алгоритмический learning signal.

Он может быть:

- Environment reward/feedback;
- derived scalar из ValueProfile;
- shaped reward;
- auxiliary signal;
- vector reward;
- вообще отсутствовать в конкретном learning method.

Канонически:

```text
Training Reward
≠
ValueProfile
```

Даже если конкретная версия строит reward из valuation, mapping должен быть explicit, versioned и относиться к `DU-26`.

---

# 26. RL critic boundary

Классический critic/value network может оценивать expected return under policy.

Такой critic может быть:

- implementation одного prospective-value estimator;
- auxiliary estimator;
- training-only component;
- control baseline.

Но:

```text
critic scalar
≠
canonical ValueProfile
```

без explicit contract.

Critic не получает ownership Goals/Drives/Appraisal/Affect только потому, что обучается предсказывать return.

---

# 27. Distributional value

Для stochastic futures полезно сохранять не только expectation.

Valuation contract допускает distributional estimates:

```text
ValueDistribution / ReturnDistribution
```

как optional view.

Это позволяет разные comparison policies извлекать:

- mean;
- quantiles;
- tail risk;
- constraint probabilities.

Но distributional RL не является mandatory implementation.

---

# 28. Normalization и units

Разные components могут иметь разные units/scales.

Поэтому normalization не может быть hidden preprocessing.

Для numeric component указывается, где применимо:

```text
raw measure
unit / semantic scale
normalizer_id
normalizer_revision
reference population/scope
online/frozen/offline mode
```

Особенно запрещено сравнивать components разных revisions как будто они уже находятся в общей валюте.

---

# 29. Learned Valuation

Valuation может быть:

```text
rule-based
learned
hybrid
Cortex-assisted
```

Learned implementation обязана иметь provenance training data/targets/revision.

Если labels отражают human/evaluator preferences, это должно быть описано как externally supervised valuation, а не как «самостоятельно возникшие ценности» Agent.

Cortex может помогать интерпретировать semantic target или строить candidate ValueProfile, но не получает ambient state access и не становится hidden owner preferences.

---

# 30. Valuation record и temporal identity

Каждый computation создаёт immutable/versioned `ValuationRecord`.

Conceptually:

```text
ValuationRecord
├── valuation_id
├── target reference
├── base state revision
├── agent revision
├── valuation system revision
├── source references/revisions
├── ValueProfile
├── ComparisonResult?, если сравнение выполнялось
├── horizon/time semantics
├── provenance
└── status
```

Повторная valuation того же target в новом context создаёт новый record.

Исторический value не переписывается задним числом.

---

# 31. ComparisonResult

Сравнение двух или нескольких profiles может вернуть не только winner.

Допустимые semantic outcomes:

```text
A preferred to B
B preferred to A
equivalent/tie
A dominates B
B dominates A
incomparable
constraint violation
insufficient evidence
unavailable
failed
```

`incomparable` — нормальное состояние multi-objective valuation.

Policy позже решит, что делать при incomparability/uncertainty.

---

# 32. Counterfactual comparison

Для matched branches:

```text
Base Snapshot S
      ├── branch A → ValueProfile VA
      └── branch B → ValueProfile VB
```

Comparison должен сохранять:

- общий base lineage;
- branch IDs;
- intervention differences;
- internal simulation mode;
- model revisions;
- comparison policy revision.

Это позволит отдельно исследовать causal effect Valuation, не путая его с World Model differences.

---

# 33. Observability

Минимально логируются:

- valuation request/target;
- source component references;
- missing/unavailable sources;
- generated ValueProfile;
- component mappings;
- normalization revisions;
- risk/constraint computations;
- ComparisonPolicy identity;
- ComparisonResult;
- scalarization, если выполнялась;
- Cortex/learned estimator call, если был;
- latency/compute metadata;
- intervention/degradation provenance.

Observer не получает mutation authority.

---

# 34. Intervention

Через `Intervention Gateway` должны быть возможны controlled treatments класса:

```text
изменить один ValueComponent
удалить/замаскировать source component
изменить ComparisonPolicy
изменить scalarization weights
изменить risk attitude/measure
изменить constraint threshold
изменить normalization revision
подменить candidate profile
```

Intervention не маскируется под natural valuation.

Особенно полезный тест:

```text
same target / same source evidence
branch A → ComparisonPolicy P1
branch B → ComparisonPolicy P2
```

и downstream behavior comparison.

---

# 35. Control configurations

Нужно различать:

## NoValuation

Valuation capability отсутствует.

Не fake profile из нулей.

## DummyValuation

Детерминированный engineering stub.

## ConstantValuation

Одинаковые profiles/scores независимо от target.

## RandomValuation

Random profiles с controlled RNG.

## ShuffledValuation

ValueProfiles другого target/branch подставляются при сохранении shape/compute.

## MatchedLinearValuation

Parameter/compute-matched linear/random aggregation без ожидаемой semantic structure.

## WeightedScalarBaseline

Все компоненты сводятся к явному fixed weighted sum.

Полезный baseline против structured comparison.

## LexicographicControl

Фиксированный known priority ordering.

## OracleValuationControl

Может использовать evaluator/world ground truth **только как research control**.

Не natural Agent configuration.

---

# 36. Проверка функционального вклада

Недостаточно показать:

```text
Valuation > NoValuation
```

Нужно исключить альтернативы:

- Policy просто получила дополнительный scalar;
- больший network/compute улучшил результат;
- evaluator truth просочился в value;
- weighted sum случайно совпал с benchmark reward;
- comparison policy не влияет на behavior;
- World Model accuracy, а не valuation, объясняет gain.

Минимально полезны:

```text
Structured Valuation
vs
WeightedScalarBaseline
vs
Shuffled/Matched Valuation
vs
NoValuation
```

и preference-intervention tests.

---

# 37. Snapshot

Если Valuation implementation имеет causally relevant persistent/adaptive state, exact `Agent Snapshot` включает:

- valuation system revision;
- component schema revisions;
- comparison-policy revision/state;
- learned estimator parameters/state;
- normalizer state;
- risk-model state;
- adaptive preference/calibration state;
- RNG;
- intervention/degradation state.

Stateless rule-based Valuation может не иметь отдельного dynamic snapshot state, но descriptor/revisions всё равно нужны для reproducibility.

---

# 38. Failure/degradation

Нужно различать:

```text
source unavailable
component unsupported
incompatible revision
normalization unavailable
insufficient predictive distribution
risk measure unavailable
comparison undefined
incomparable
constraint conflict
estimator failure
Cortex/backend failure
```

`incomparable` и `constraint violation` не являются техническими exception по умолчанию.

Hidden fallback к другому comparison policy запрещён.

---

# 39. Что намеренно не фиксируется

`DU-18` не выбирает:

- конкретный набор ValueComponents для первой software version;
- concrete weight vector;
- linear/nonlinear scalarization;
- Pareto/Tchebycheff/lexicographic policy как universal default;
- CVaR/quantile/worst-case risk measure;
- exact Goal/Drive mapping equations;
- exact Affect modulation;
- exact temporal discounting;
- critic/value architecture;
- PPO/DQN/actor-critic;
- конкретную preference-learning dataset;
- human preference model;
- Python framework/API.

---

# 40. Gate завершения DU-18

`DU-18` считается завершённым, если:

- `Valuation System` имеет отдельную responsibility/ownership boundary;
- `Valuation Target` определён для state/outcome/action/trajectory families;
- принят typed multi-objective `ValueProfile`;
- scalarization вынесена в explicit ComparisonPolicy;
- multi-objective conflict не теряется до comparison stage;
- Goal/Drive/Appraisal/Affect boundaries сохранены;
- External Feedback/Intrinsic Signals не становятся utility автоматически;
- uncertainty отделена от risk/downside;
- Self competence отделена от value;
- immediate/prospective/horizon semantics различены;
- imagined/counterfactual valuation сохраняет provenance;
- RL reward/critic отделены от canonical valuation;
- normalization/revision rules заданы;
- controls/interventions/snapshot/failure semantics определены;
- конкретный algorithm/backend не зафиксирован преждевременно.
