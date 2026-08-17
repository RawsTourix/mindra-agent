# MINDRA-Eval

## Статус документа

**Design Update:** `DU-28 — MINDRA-Eval`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет каноническую семантику Evaluation Runtime, evaluation conditions, benchmark/task suites, controls, causal contrasts, metric/report protocol и statistical evidence MINDRA поверх `DU-01 … DU-27`.

Ключевое решение `DU-28`:

- MINDRA-Eval является **внешним относительно Agent Evaluation Plane**, а не cognitive module;
- evaluation не сводится к одному leaderboard score;
- end-task performance, module diagnostics, causal contribution, calibration, resource efficiency и reproducibility являются разными слоями evidence;
- evaluation condition полностью pin'ит Agent/Environment/checkpoint/data/intervention/software/hardware/compute context;
- stochastic claim требует явной experimental unit, replicate axes и statistical analysis plan;
- causal claim требует не только ablation, но где применимо paired counterfactual/intervention и matched controls;
- `No*`, Dummy, random/shuffled и matched-capacity/compute controls являются first-class evaluation conditions;
- evaluator-only Ground Truth остаётся вне Agent Interaction Plane;
- Policy quality измеряется **до** Action Gate отдельно от post-Gate system behavior;
- условно принятые `Affect`, `Workspace`, `Planner` и `Executive Control` получают explicit negative module gates;
- concrete benchmark library, statistics package, plotting stack и composite score намеренно не фиксируются.

Документ опирается на:

- [`../research-methodology.md`](../research-methodology.md) — общая исследовательская дисциплина;
- [`system-context.md`](system-context.md) — Evaluation Runtime/Research Control Plane вне Agent;
- [`observability-and-intervention.md`](observability-and-intervention.md) — Evidence Plane и Intervention Gateway;
- [`modules/environment.md`](modules/environment.md) — Interaction/Research planes, task/world distributions;
- [`modules/self-model.md`](modules/self-model.md) — competence/calibration semantics;
- [`modules/world-model.md`](modules/world-model.md) — prediction/belief/imagination metrics;
- [`modules/memory.md`](modules/memory.md) и [`modules/memory-regulation.md`](modules/memory-regulation.md) — retrieval/consolidation controls;
- [`modules/affect.md`](modules/affect.md), [`modules/workspace.md`](modules/workspace.md), [`modules/executive-control.md`](modules/executive-control.md), [`modules/policy-planner.md`](modules/policy-planner.md) — explicit negative module gates;
- [`modules/action-boundary.md`](modules/action-boundary.md) — intent/gate/system attribution;
- [`experience-data-replay.md`](experience-data-replay.md) — immutable evaluation evidence lineage;
- [`training-lifecycle.md`](training-lifecycle.md) — training procedure evaluation, behavior/learner revisions;
- [`checkpoint-reproducibility-compute.md`](checkpoint-reproducibility-compute.md) — verified base state, reproducibility и compute manifests.

Документ намеренно **не** выбирает:

- конкретный benchmark framework;
- конкретный MicroWorld task catalog;
- exact number of seeds;
- universal p-value/alpha;
- один statistical test/bootstrap implementation;
- единственный calibration metric;
- общий composite leaderboard score;
- experiment tracker/dashboard;
- plotting library;
- конкретный CI provider;
- concrete implementation architecture Evaluation Runtime;
- engineering test strategy — `DU-29`.

---

# 1. Цель DU-28

После `DU-27` MINDRA уже можно причинно идентифицировать, клонировать и сравнивать при фиксированных revisions/manifests. Теперь нужен слой, отвечающий не на вопрос:

> «Работает ли код?»

а на вопросы:

1. **какие функциональные способности реально присутствуют?**
2. **какой механизм причинно вносит вклад?**
3. **не объясняется ли improvement дополнительными parameters/compute/context/data?**
4. **устойчив ли результат к stochasticity и изменению мира/Cortex?**
5. **насколько хорошо откалиброваны внутренние predictions?**
6. **какова цена результата по compute/data/resource usage?**
7. **какие claims разрешены данным качеством evidence?**

Ключевая установка:

```text
Task score
≠
module evidence
≠
causal evidence
≠
calibration evidence
≠
resource-efficiency evidence
≠
research claim
```

---

# 2. Evaluation Runtime boundary

## 2.1. Ownership

`Evaluation Runtime` находится **вне MINDRA Agent**.

Он может:

- создавать/восстанавливать evaluation checkpoints;
- запускать Environment/world distributions;
- выбирать evaluation condition;
- читать Evidence Plane;
- использовать Environment Research Ground Truth;
- инициировать declared interventions через `Intervention Gateway`;
- вычислять evaluator-only metrics;
- собирать evaluation artifacts;
- строить comparisons/reports.

Он не может normal-runtime способом:

- писать evaluator score в `CognitiveState`;
- давать Agent hidden world state;
- подменять Appraisal/Value/Goal через прямую mutation;
- сообщать oracle action;
- использовать research annotation как cognition input.

Если evaluator intentionally вмешивается во внутренний state, это **intervention condition**, а не скрытая часть normal runtime.

## 2.2. Physical topology

Evaluation Runtime может физически находиться:

- в том же Python process;
- в отдельном worker/process;
- локально;
- в Colab;
- на remote compute.

Deployment topology не меняет logical boundary.

---

# 3. Иерархия evaluation entities

Каноническая структура:

```text
EvaluationStudy
    ↓
EvaluationSuite
    ↓
EvaluationCondition(s)
    ↓
EvaluationRun / replicate
    ↓
EvaluationUnit(s)
    ↓
MetricRecord(s)
    ↓
Contrast / StatisticalAnalysis
    ↓
EvaluationReport
```

## 3.1. `EvaluationStudy`

Исследование с конкретным research question/hypothesis.

Содержит conceptually:

- hypothesis/claim target;
- exploratory/confirmatory status;
- suite;
- conditions;
- controls;
- primary/secondary metrics;
- replicate/sample-size policy;
- statistical plan;
- success/falsification criteria;
- allowed exclusions;
- stopping policy;
- reproducibility requirements.

## 3.2. `EvaluationSuite`

Versioned набор task/world families и measurement protocols.

Suite не равна одному dataset или environment.

Она может включать разные axes:

```text
short-horizon
long-horizon
partial observability
memory dependency
hidden-rule discovery
uncertainty
resource limitation
contingent planning
continual adaptation
OOD / transfer
```

## 3.3. `EvaluationCondition`

Полностью определённая экспериментальная condition:

```text
Agent / component revisions
checkpoint + restore profile
Environment/world distribution
Cortex/backend condition
module composition
interventions/ablations/controls
training/adaptation mode
resource envelopes
actual compute capture policy
data visibility
software/hardware/determinism manifests
seed/RNG policy
metric plan
```

Нельзя сравнивать две configurations как «одинаковые кроме X», если различия в condition manifest не перечислены явно.

## 3.4. `EvaluationRun`

Один причинно идентифицируемый запуск конкретной condition.

Run связывается с:

- condition revision;
- base checkpoint;
- world/task sample;
- RNG initialization;
- actual compute;
- raw Experience/Evidence refs;
- outcome/completeness status.

## 3.5. `EvaluationUnit`

Единица, относительно которой metric имеет смысл.

Примеры:

- Episode;
- Decision Window;
- paired counterfactual branch pair;
- prediction-resolution pair;
- trained checkpoint replicate;
- task family instance;
- Learning Update interval.

`EvaluationUnit` **не означает автоматически statistical independent sample**.

---

# 4. Experimental unit и replicate axes

Это один из главных invariants DU-28.

Нужно различать минимум:

```text
training replicate
Agent/checkpoint replicate
evaluation world replicate
episode replicate
counterfactual branch replicate
stochastic policy replicate
```

Пример:

```text
1 trained checkpoint
× 100 evaluation episodes
```

может хорошо оценивать variability **фиксированной Policy** по world instances, но не даёт 100 независимых samples для claim:

> «Training Algorithm A лучше Training Algorithm B».

Для training-algorithm claim единицей верхнего уровня обычно будет независимый training replicate/checkpoint, а episodes образуют вложенный уровень.

Поэтому каждый statistical claim обязан указывать:

- `analysis_unit`;
- grouping/blocking structure;
- dependency/nesting assumptions;
- replicate axis;
- aggregation level.

Запрещён pseudo-replication, при котором correlated steps/episodes выдаются за независимые training runs.

---

# 5. Task/world distribution semantics

Evaluation измеряет не только конкретный world instance, но и заявленную область generalization.

Нужно явно различать:

```text
train distribution
validation/model-selection distribution
test distribution
held-out world instances
held-out compositions/rules
OOD/shift distributions
stress/adversarial distributions
```

## 5.1. Test isolation

Test condition не используется для:

- training;
- online hyperparameter tuning;
- prompt/systematic policy selection;
- early stopping model selection;

если study явно не исследует test-time adaptation.

Повторное ручное изменение architecture на основе test outcome превращает данный test в development evidence; для нового confirmatory claim требуется новый held-out condition.

## 5.2. Distribution-level claims

Claim:

> «метод работает в мире W17»

слабее claim:

> «метод улучшает результат по distribution D».

Для второго нужны sampled worlds/tasks и соответствующая statistical aggregation.

---

# 6. Exploratory vs confirmatory evaluation

## 6.1. Exploratory

Допускает:

- поиск metric;
- диагностику;
- выбор task difficulty;
- поиск range intervention;
- hypothesis generation.

Результаты помечаются exploratory.

## 6.2. Confirmatory

До просмотра confirmatory outcomes фиксируется `EvaluationStudyPlan`:

- hypothesis;
- primary contrasts;
- primary metric(s);
- controls;
- sample/replicate policy;
- analysis unit;
- statistical method family;
- exclusions/censoring;
- stopping rule;
- multiplicity policy;
- success/falsification criterion.

Изменение плана после просмотра результатов создаёт новую revision и не должно маскироваться как исходный preregistered plan.

---

# 7. Baseline / ablation / control taxonomy

## 7.1. Baseline

Сравнительная архитектура/алгоритм, отвечающая на research question.

## 7.2. Ablation

Удаление/выключение целевой semantics:

```text
Full
vs
Full - X
```

Но простой ablation часто недостаточен, потому что одновременно меняет capacity/compute/state.

## 7.3. Semantic controls

First-class conditions:

```text
NoX
DummyX
ConstantX
RandomX
ShuffledX
TimePermutedX
MatchedNoiseX
RuleBasedX
OracleX (research-only)
```

где применимо.

## 7.4. Matched controls

Нужно отдельно фиксировать, какие факторы matched:

- trainable parameter count;
- persistent state capacity;
- input information;
- context length;
- number of Cortex calls;
- actual runtime compute;
- training steps/data;
- search/rollout budget;
- Memory capacity;
- Workspace capacity.

Полное matching не всегда возможно. Тогда deviation измеряется и указывается как limitation.

## 7.5. Tuning fairness

Baseline и treatment должны получать сопоставимый **model-selection/tuning budget**, где это влияет на вывод.

Нельзя:

- тщательно тюнить MINDRA configuration;
- запускать baseline с первым случайным config;
- приписывать разницу architecture.

Tuning procedure и budget становятся частью condition provenance.

---

# 8. Paired counterfactual evaluation

MINDRA специально поддерживает сильный causal pattern:

```text
verified Checkpoint C
+
Environment Snapshot E
+
required RNG/private states
        ↓
     branch
   ┌────┴────┐
   ↓         ↓
Control   Treatment
              │
          Intervention X
```

## 8.1. Требования

Paired counterfactual допустим, если:

- DU-27 checkpoint имеет достаточный restore level;
- Environment clonable/restorable;
- unresolved `execution_unknown` отсутствует или reconciled;
- intervention явно идентифицирована;
- non-target variables pin/match насколько требует claim;
- RNG coupling policy определена.

## 8.2. Common randomness

Для некоторых contrasts полезно использовать общий исходный RNG/base state, чтобы снизить variance.

Но common RNG не должен скрывать тот факт, что treatment сам изменяет количество случайных вызовов/ветвление execution. Такой divergence фиксируется в provenance.

## 8.3. Causal output

`CausalContrastRecord` должен содержать минимум:

- base state/checkpoint;
- treatment/control conditions;
- intervention target/value;
- expected target outcomes;
- measured effect;
- off-target effects;
- completeness;
- statistical uncertainty;
- causal limitations.

---

# 9. Intervention specificity

Корреляция внутренней переменной с поведением не считается сильным evidence причинной роли.

Желательная логика:

```text
state X correlates with behavior Y
        ↓ недостаточно
intervene X while holding relevant context
        ↓
measure target change Y
        +
measure off-target changes Z
```

Для learned distributed representations идеальная isolated intervention может быть невозможна. Тогда report обязан отдельно указывать intervention spillover.

---

# 10. Metric architecture

MINDRA-Eval использует typed metrics.

```text
MetricSpec
├── metric_id/revision
├── target semantic object
├── required evidence
├── visibility/trust requirements
├── unit / direction
├── aggregation semantics
├── missing/censoring policy
├── normalization references
└── provenance
```

## 10.1. Primary vs secondary

Confirmatory study заранее разделяет:

- primary metric(s);
- secondary diagnostics;
- exploratory metrics.

## 10.2. One-number score не canonical

Основной результат — `MetricBundle / EvaluationScorecard`, а не обязательное число.

Допустим optional `AggregateScore`, если:

- aggregator explicit;
- weights/normalization explicit;
- source metrics сохранены;
- revision/provenance сохранены;
- composite score не заменяет primary causal diagnostics.

---

# 11. End-to-end task metrics

Task metrics могут включать в зависимости от suite:

- success/failure;
- partial completion;
- goal completion time/steps;
- external task feedback;
- constraint violation;
- action efficiency;
- resource consumption;
- robustness under shift;
- recovery after disruption.

`Objective Task Metric` остаётся evaluator-only, если Environment contract не делает его agent-visible.

---

# 12. Calibration metrics

Для probabilistic claims важны отдельно:

```text
accuracy / task quality
calibration
sharpness/resolution
ranking/discrimination
robustness/stability
```

Они не являются синонимами.

## 12.1. Proper scoring

Если subsystem выдаёт meaningful probability, confirmatory evaluation должна где возможно включать **proper scoring rule family** или другой estimator, соответствующий заявляемой probability semantics.

Conceptual candidates:

- Brier-like score;
- log score / NLL;
- task-specific proper scores.

Exact metric не фиксируется DU-28.

## 12.2. ECE-like diagnostics

Binned calibration error может быть полезным diagnostic view, но не является универсально достаточным доказательством truthful probabilities.

## 12.3. Trajectory confidence

Если Self/Executive/Policy выдаёт confidence по ходу trajectory, evaluation должна явно определить:

- что прогнозируется;
- horizon/outcome;
- conditioning history;
- censored trajectory semantics;
- per-prefix vs collapsed score.

---

# 13. World Model evaluation

Минимальные классы:

```text
one-step prediction quality
multi-step rollout degradation
belief-state accuracy/consistency where Ground Truth exists
uncertainty calibration
rare-event / rule-change prediction
model error under distribution shift
```

Evaluator может использовать hidden world state для диагностики `World Belief`, но этот Ground Truth не возвращается Agent.

Важно отдельно оценивать:

- actual-observation posterior/assimilation;
- prior/prediction;
- imagination quality.

Нельзя оценивать imagined rollout как будто он natural experience.

---

# 14. Self Model evaluation

Классы metrics:

```text
success-probability calibration
cost/effort prediction
competence discrimination
OOD uncertainty/support
revision-staleness handling
capability-fact correctness
```

Пример сильного test:

```text
Self predicts 0.8 success
→ среди comparable resolved cases success ≈ expected frequency
```

При смене `agent_revision` отдельно проверяется, не сохраняет ли Self Model старую competence слишком уверенно.

---

# 15. Memory evaluation

Memory оценивается не одной retrieval accuracy.

Нужны разные слои:

```text
retrieval relevance/coverage
retrieval utility for downstream task
retrieval cost
correct vs shuffled retrieval
NoMemory
recency-only/random controls
retention/forgetting behavior
contradiction preservation
source provenance integrity
```

Для Memory Regulation/Consolidation минимум:

```text
episodic-only / NoConsolidation
vs consolidation
```

и отдельно:

- storage/context budget;
- information retained/lost;
- derived-record factual/provenance errors;
- repeated-consolidation degradation.

`compression ratio` сам по себе не является memory quality.

---

# 16. Intrinsic Signals evaluation

Signal provider должен проверяться на различение intended phenomena.

Примеры:

```text
novel but predictable
familiar but stochastic
high prediction error but low learnable information
rare vs semantically novel
competence improvement vs competence degradation
```

Метрики могут включать:

- sensitivity;
- specificity;
- temporal stability;
- representation-revision robustness;
- source/provenance correctness.

Высокий signal magnitude не является success criterion сам по себе.

---

# 17. Drives evaluation

Нужно проверять:

- persistence;
- accumulation/recovery;
- logical-time dynamics;
- saturation/hysteresis, если заявлены;
- specificity к intended inputs;
- target downstream effect;
- no direct Goal/Policy authority leakage.

Causal pattern:

```text
same external state
same Goals
intervene Drive X
→ expected downstream change
→ limited off-target change
```

---

# 18. Appraisal evaluation

Dimension-level evaluation предпочтительнее emotion-label accuracy.

Проверяются где применимо:

- relevance;
- goal congruence;
- drive conduciveness;
- expectedness;
- controllability;
- coping potential;
- urgency;
- reappraisal under new evidence.

Особенно важны constructed worlds, где Ground Truth конкретной functional dimension известен evaluator'у.

`AppraisalProfile` не оценивается через совпадение с человеческой emotion taxonomy по умолчанию.

---

# 19. Affect negative module gate

Affect принят условно и должен пройти explicit falsification test.

Минимальные conditions:

```text
FullAffect
NoAffect
ResetEveryEvent
ShuffledHistory
MatchedRecurrentControl
```

При возможности state-matched causal intervention:

```text
same world
same current event
same Goals/Drives
same current Appraisal
Affect state X vs Y
```

Поддержка отдельной Affect boundary усиливается, если:

- temporal history/persistence систематически влияет на предусмотренные downstream functions;
- `FullAffect` превосходит matched recurrent control на affect-specific tasks;
- intervention effects специфичны;
- эффект нельзя объяснить просто дополнительной recurrent state capacity.

Boundary ослабляется/фальсифицируется, если:

- `ResetEveryEvent ≈ FullAffect`;
- shuffled history почти не меняет outcome;
- arbitrary matched recurrent state даёт тот же эффект;
- interventions Affect не имеют специфичного downstream effect.

---

# 20. Valuation evaluation

Нужно различать:

```text
source component correctness
ValueProfile integrity
ComparisonPolicy behavior
final Policy choice
```

Проверки:

- preservation multi-objective conflicts;
- constraint handling;
- risk/downside sensitivity;
- expected response на controlled preference changes;
- pairwise/ordering consistency там, где policy это предполагает;
- `incomparable` semantics;
- scalarization provenance.

Изменение `ComparisonPolicy` должно причинно менять choice в предусмотренном направлении на специально сконструированных задачах.

---

# 21. Salience evaluation

Salience оценивается через **реальное selective processing**, а не красоту score.

Controls:

```text
CorrectAllocation
Uniform
Random
Shuffled
NoveltyOnly
ValueOnly
FixedTopK
MatchedRouter
NoSalience
```

Metrics:

- target processing allocation;
- downstream utility under fixed resource budget;
- allocation stability;
- resource efficiency;
- intervention specificity;
- purpose dependence.

Если allocation не меняет фактическую обработку, Salience не имеет подтверждённой функциональной роли.

---

# 22. Workspace negative module gate

Минимальные comparisons:

```text
FullWorkspace
NoWorkspace / DirectReads
MatchedSharedBuffer
MatchedRecurrentBuffer
RandomAdmission
ShuffledAdmission
FixedLatestK
UnboundedWorkspace
WorkspaceWithoutBroadcast
```

Обязателен capacity sweep, где practically feasible.

Отдельная Workspace boundary поддерживается, если bounded admission+broadcast дают специфичную пользу при сопоставимой capacity/compute.

Она ослабляется, если generic matched buffer/direct reads дают тот же результат, а broadcast/capacity lesions не имеют специфичного эффекта.

---

# 23. Executive Control negative module gate

Главный объект оценки — **performance/resource frontier**.

Минимальные controls:

```text
AdaptiveExecutive
FixedSchedule
FixedBudget
SimpleThreshold
RandomMetaAction
SalienceOnly
CostUnaware
MatchedLearnedRouter
```

Нужно сравнивать при максимально сопоставимом **actual compute**, а не только nominal budget.

Metrics:

- task performance;
- actual cognitive resource usage;
- Cortex/retrieval/rollout calls;
- stop/continue quality;
- wasted compute;
- under-computation failures;
- allocation response на uncertainty/competence/budget intervention.

Отдельная Executive boundary ослабляется, если fixed schedule при matched compute даёт тот же frontier либо controller почти всегда воспроизводит один и тот же pipeline.

---

# 24. Planner negative module gate

Planner не является обязательным механизмом.

Минимальные comparisons:

```text
Policy + Planner
ReactivePolicy / NoPlanner
Depth1 / FixedLookahead
RandomPlan
ShuffledPlan
MatchedSearch/RecurrentControl
```

Оценка проводится особенно на:

- long-horizon;
- contingent;
- partial-observation;
- hidden-rule;
- model-error;
- replanning tasks.

Обязательно сравнивать actual planning compute.

Planner boundary поддерживается, если multi-step/contingent semantics дают эффект сверх matched compute/capacity control.

---

# 25. Policy vs Action Gate attribution

Это обязательный MINDRA-Eval split.

Нужно отдельно измерять:

## 25.1. Policy quality до Gate

По `SelectedActionIntent`:

- semantic validity;
- task quality;
- constraint/safety violation rate относительно evaluator labels;
- preference/value consistency;
- action efficiency.

## 25.2. Gate quality

- rejection rate;
- correct rejection;
- false rejection;
- normalization rate;
- override rate;
- prevented invalid/unsafe intents;
- introduced degradation;
- `execution_unknown`/dispatch outcomes.

## 25.3. Post-Gate system quality

По committed/executed actions и final outcomes.

Запрещён вывод:

```text
post-Gate success high
→ Policy quality high
```

если significant correction сделал Action Gate/Runtime Assurance.

---

# 26. Training Lifecycle evaluation

Training procedure оценивается отдельно от одного final checkpoint.

Нужно различать:

```text
plasticity
retention
sample efficiency
data efficiency
compute efficiency
training stability
candidate rejection/activation rate
```

Минимальные regimes, где применимо:

```text
Frozen / NoLearning
Offline
Interleaved Online
Decoupled Online
```

Training claim требует independent training replicates, а не только много evaluation episodes одного checkpoint.

Privileged supervision, data amount, tuning budget и training compute всегда являются condition factors.

---

# 27. Compute-normalized evaluation

Из `DU-27` используются два разных слоя:

```text
CognitiveResourceEnvelope / Executive ledger
→ agent-visible logical resource semantics

ComputeManifest / ComputeUsageRecord
→ actual infrastructure/research evidence
```

MINDRA-Eval может сравнивать:

- equal nominal budget;
- equal measured compute;
- performance-at-cost;
- cost-at-target-performance;
- Pareto/performance-resource frontier.

Нельзя объявлять improvement architecture, если treatment получил значительно больше actual compute, не проведя соответствующий resource-normalized analysis.

Estimated/provider-reported/measured compute не смешиваются без provenance.

---

# 28. Parameter/data/context matching

Compute matching недостаточно.

Comparison manifest должен уметь показать различия в:

```text
parameter count
trainable parameter count
state capacity
context length
Memory capacity
Cortex model/calls
dataset size
training updates
rollout branches
```

Иногда архитектура intrinsically требует большего state/compute. Тогда вместо искусственного perfect match нужно честно показать trade-off curve и matched generic-capacity control.

---

# 29. StatisticalAnalysisPlan

Статистика является частью protocol, а не post-hoc plotting choice.

`StatisticalAnalysisPlan` должен фиксировать минимум:

- primary effect/metric;
- analysis unit;
- grouping/nesting;
- paired/unpaired design;
- interval/uncertainty estimator;
- point/aggregate estimator;
- resampling/blocking semantics, если используются;
- multiplicity policy;
- missing/censored/unresolved handling;
- minimum practical effect / equivalence criterion, если применимо;
- stopping/sample-size policy;
- reporting distribution.

## 29.1. Не один universal test

DU-28 не фиксирует:

- t-test;
- Mann–Whitney;
- bootstrap;
- permutation test;
- Bayesian model;
- конкретный alpha.

Выбор зависит от unit/dependence/distribution/claim.

## 29.2. Interval evidence

Для stochastic aggregate claim point estimate без uncertainty считается недостаточным.

Предпочтительно сохранять:

- replicate-level observations;
- distribution summaries;
- interval estimates;
- effect size.

## 29.3. Robust aggregate metrics

Suite может использовать mean, median, interquartile mean, optimality-gap-like metrics, performance profiles и другие summaries. Aggregator revision фиксируется явно.

Никакой один summary не является универсальным.

---

# 30. Multiple comparisons

Большое количество модулей/metrics создаёт риск выбрать удачные результаты постфактум.

Confirmatory study должен:

- заранее выделить primary hypotheses;
- определить family comparisons;
- задать multiplicity policy, если требуется;
- помечать остальные analyses exploratory.

Конкретный correction method не фиксируется.

---

# 31. Missing, censored и unresolved outcomes

Evaluation outcome не всегда бинарный success/failure.

Нужно различать conceptually:

```text
complete
partial
censored
execution_unknown
causal_gap
artifact_missing
invalid_condition
aborted_by_runtime
metric_unavailable
```

Запрещено автоматически превращать:

```text
execution_unknown
→ failure
```

или исключать неудобные runs без предопределённой policy.

`MetricSpec` определяет, какие статусы допустимы и как они обрабатываются.

---

# 32. Reproducibility requirements

Каждый significant evaluation result связан минимум с:

- repository/code revision;
- EvaluationStudy/Condition revision;
- Agent revision;
- checkpoint + RestoreProfile;
- Environment/world distribution manifest;
- Cortex identity/revision;
- interventions/controls;
- RNG/seed policy;
- Dataset/TrainingPlan refs, если relevant;
- SoftwareEnvironmentManifest;
- HardwareTopologyManifest;
- ComputeManifest/usage;
- raw Experience/Evidence refs;
- metric/analysis revisions;
- `ReproducibilityClaim`.

Сильный paired causal claim нельзя строить на checkpoint, не обеспечивающем требуемый causal restore.

Remote/provider uncertainty может снижать reproducibility claim и требовать большего stochastic replication.

---

# 33. EvaluationManifest и report lineage

`EvaluationManifest` — versioned описание всего study condition space и protocol.

Conceptually:

```text
EvaluationManifest
├── study/suite revision
├── hypotheses
├── conditions
├── task/world distributions
├── checkpoints
├── controls/interventions
├── resource matching
├── metric specs
├── statistical plan
├── reproducibility requirements
└── provenance
```

`EvaluationReport` является derived artifact и содержит source refs к raw run/metric records.

Изменение plotting или aggregate representation не переписывает raw evaluation evidence.

---

# 34. Causal claim ladder

MINDRA-Eval различает силу evidence.

Conceptual ladder:

```text
L0 — descriptive
     state/metric correlation

L1 — predictive
     internal variable предсказывает outcome

L2 — ablation/control
     изменение architecture condition меняет outcome

L3 — matched causal intervention
     controlled intervention при aligned base state
     меняет target outcome с ограниченными off-target effects

L4 — replicated/generalized causal evidence
     эффект повторяется по независимым replicates/
     world distributions/Cortex conditions
```

Точные имена уровней могут измениться, но principle canonical:

> сила research claim не должна превышать силу experiment design/evidence.

Это не утверждение причинной идентифицируемости во всех статистических смыслах; конкретный study обязан описывать assumptions.

---

# 35. Cortex transfer evaluation

Так как Cortex заменяем, architecture claim желательно проверять на нескольких Cortex conditions, где practically feasible:

```text
NoCortex
small Cortex
stronger Cortex
alternative family/backend
```

Но сравнение должно учитывать:

- model capability;
- context;
- calls;
- token/compute budget;
- multilingual support;
- backend nondeterminism.

Если architecture gain существует только у одного конкретного Cortex, claim формулируется соответственно узко.

---

# 36. Factorial interactions

Для модулей с предполагаемой синергией допускается factorial design:

```text
none
A
B
A+B
```

При этом interaction effect рассматривается отдельно от main effects.

Особенно релевантны пары/группы:

- World Model × Planner;
- Intrinsic Signals × Drives;
- Appraisal × Affect;
- Salience × Workspace;
- Self Model × Executive Control;
- Memory × Memory Regulation.

Full factorial по всей архитектуре практически невозможен; study выбирает hypothesis-driven subset.

---

# 37. Robustness / distribution shift

End-task evaluation должна при необходимости различать:

```text
nominal performance
robustness under perturbation
resilience/recovery after disruption
OOD transfer
```

Один nominal score не доказывает robust behavior.

Perturbation type/intensity/agent visibility должны быть versioned и заранее определены.

---

# 38. Oracle controls

Evaluator может использовать privileged oracle implementation как **research ceiling/control**, например:

- Oracle World Model;
- Oracle Planner;
- Oracle Salience labels;
- Ground Truth Self capability labels.

Но oracle condition:

- маркируется privileged;
- не считается normal Agent architecture;
- не сравнивается как обычный deployment result;
- не создаёт agent-visible leakage в соседних conditions.

---

# 39. Evaluation of adaptation

По умолчанию фиксированная evaluation condition не меняет trainable Agent parameters.

Если исследуется online/test-time adaptation, это отдельный protocol:

```text
pre-adaptation phase
adaptation data/interaction budget
allowed Learning Updates
post-adaptation evaluation
```

Нужно различать:

- adaptation performance;
- final performance;
- retention;
- data/compute cost;
- test-data reuse/leakage.

---

# 40. Failure validity

Evaluation run может быть **invalid**, если нарушены protocol assumptions, например:

- wrong checkpoint revision;
- Ground Truth leaked to Agent;
- unmatched forbidden resource difference;
- corrupted checkpoint;
- missing required artifact;
- stale metric schema;
- undeclared intervention;
- condition drift during run;
- violated test isolation.

Invalid run не должен молча учитываться как poor task performance.

Причина invalidation фиксируется отдельно.

---

# 41. Module gate semantics

Для условно принятых boundaries evaluation должна иметь заранее определённый negative result, способный инициировать design review.

На `DU-28` explicit gates обязательны минимум для:

```text
Affect
Workspace
Planner
Executive Control
```

Другие механизмы также могут иметь module-specific falsification criteria.

Evaluation result **не удаляет boundary автоматически**. Flow остаётся:

```text
result
→ interpretation
→ design review
→ ADR
→ canonical change
```

---

# 42. No universal leaderboard

MINDRA-Eval может публиковать удобные summaries, но research conclusion должен опираться на профиль evidence.

Предпочтительный conceptual report:

```text
Task Performance
Calibration
Causal Module Evidence
Generalization
Robustness
Resource Efficiency
Reproducibility
Failure/Unknown Rates
```

а не только:

```text
MINDRA Score = 87.4
```

Если composite score нужен для конкретной version/competition, его definition принадлежит `AggregateMetricPolicy` конкретного EvaluationSuite и не становится universal utility проекта.

---

# 43. Snapshot / restore requirements для causal evaluation

Paired/branching studies требуют `DU-27` profile, способного восстановить causally relevant state.

Если exact counterfactual restore невозможен из-за external provider/physical Environment:

- study использует weaker randomized/blocked design;
- causal claim ограничивается;
- impossibility/uncertainty указывается в report.

Нельзя описывать ordinary independent runs как exact counterfactual branches.

---

# 44. Interaction с DU-29

`MINDRA-Eval` проверяет **research/functional properties**.

`DU-29 — Engineering Testing` должен отдельно определить:

- unit tests;
- contract tests;
- property/invariant tests;
- deterministic integration tests;
- failure injection;
- migration/checkpoint tests;
- CI gates.

Поэтому:

```text
Evaluation success
≠
engineering correctness
```

и наоборот.

---

# 45. Candidate first implementation strategy

Без фиксации software version design разумный минимальный будущий slice:

```text
1. deterministic MicroWorld suite
2. fixed checkpoint evaluation
3. several independent world seeds
4. Full vs NoX vs one matched control
5. raw per-episode records
6. typed metric bundle
7. confidence/interval report
8. actual compute capture
9. paired counterfactual branch там, где restore exact
```

Это лишь implementation candidate; version design появится после `DU-32`.

---

# 46. Invariants DU-28

После принятия `DU-28` действуют:

1. `Evaluation Runtime` не является частью Agent cognition.
2. Evaluator-only Ground Truth не пересекает Agent Interaction Plane normal runtime способом.
3. Evaluation condition pin'ит versions/checkpoints/world/resource/data/analysis context.
4. One-number task score не является достаточным MINDRA research evidence.
5. Experimental/statistical unit объявляется явно.
6. Один trained checkpoint с большим количеством episodes не считается множеством independent training replicates.
7. Stochastic aggregate claim включает uncertainty/distribution evidence.
8. Ablation не заменяет matched control там, где effect может объясняться capacity/compute/context.
9. Paired causal intervention требует compatible verified base checkpoint/Environment state.
10. Policy quality измеряется до Action Gate отдельно от post-Gate system outcome.
11. `execution_unknown`/censored/missing не преобразуются молча в failure/success.
12. Compute comparison использует actual/provenanced resource evidence, где claim зависит от efficiency.
13. Primary hypothesis/metrics confirmatory study фиксируются до просмотра confirmatory outcome.
14. Privileged oracle conditions маркируются отдельно.
15. Affect/Workspace/Planner/Executive имеют explicit negative module gates.
16. Training algorithm claims используют independent training replicates и учитывают plasticity/retention/data/compute.
17. Composite score optional и всегда сохраняет source metric lineage.
18. Strength of research claim bounded by evaluation design/evidence strength.
19. Evaluation report имеет source lineage до raw Experience/Evidence/Metric records.
20. Concrete benchmark/statistics/plotting implementation не является architecture invariant.

---

# 47. Completion gate DU-28

`DU-28` считается завершённым, когда:

- определена Evaluation Runtime boundary;
- определены study/suite/condition/run/unit semantics;
- определён control/matched-control protocol;
- определён paired counterfactual/intervention protocol;
- определена metric architecture;
- определены statistical/replicate requirements;
- определён compute-normalized comparison;
- определена Policy/Action Gate attribution;
- определены module-specific diagnostics и negative gates;
- определены reproducibility/report lineage requirements;
- существует candidate semantic contract;
- принят ADR по evaluation architecture;
- literature/research pass сохранён отдельно;
- `current.md` переведён на `DU-29`;
- consistency review пройден.
