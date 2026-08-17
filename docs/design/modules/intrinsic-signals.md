# Intrinsic Signals MINDRA

## Статус документа

**Design Update:** `DU-14 — Intrinsic Signals`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет нейтральный слой внутренних сигналов MINDRA, выводимых из структуры собственного опыта Agent до появления Drives, Appraisal и Valuation.

Документ определяет:

- responsibility и ownership Intrinsic Signal Layer;
- многопровайдерную архитектуру вместо одного `IntrinsicRewardModule`;
- typed signal semantics;
- различие prediction discrepancy, predictive surprisal, novelty, information gain, uncertainty change, competence change и visitation rarity;
- temporal/reference scope сигналов;
- normalization/stationarity/version semantics;
- representation dependence и drift;
- provenance и online computability;
- границы observed/replayed/imagined/intervened experience;
- private baseline/history state providers;
- `NoSignal`/Dummy/Control configurations;
- observability/intervention/failure/snapshot semantics.

Документ опирается на:

- [`../execution-model.md`](../execution-model.md) — observed/replayed/imagined transitions различаются;
- [`../cognitive-state.md`](../cognitive-state.md) — committed state, provenance и availability semantics;
- [`../module-lifecycle.md`](../module-lifecycle.md) — provider outputs публикуются через staged/committed effects;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — signal observation отделено от intervention;
- [`environment.md`](environment.md) — evaluator/world ground truth не является normal Agent input;
- [`perception.md`](perception.md) — representation identity/revision и partial observability;
- [`memory.md`](memory.md) — опыт/visitation history доступен через явные agent-owned mechanisms;
- [`world-model.md`](world-model.md) — prediction/error/uncertainty evidence не является reward;
- [`self-model.md`](self-model.md) — competence predictions/resolutions и self-estimate semantics.

Документ намеренно **не** определяет:

- Drives — `DU-15`;
- Appraisal/Affect — `DU-16/17`;
- Valuation/scalarization — `DU-18`;
- Salience — `DU-19`;
- конкретный intrinsic reward для RL;
- PPO/RND/ICM/VIME/Plan2Explore/RIDE как обязательный algorithm;
- exact normalization formula;
- exact learned encoder/density model;
- exact training losses — `DU-26`;
- exact Python API/checkpoint encoding — `DU-27`.

---

# 1. Цель DU-14

MINDRA должна уметь вычислять факты класса:

> «это событие было трудно предсказать»;

> «это состояние редко встречалось в моей истории»;

> «после этого наблюдения моя неопределённость о мире уменьшилась»;

> «моя оценка собственной компетентности в этом классе задач изменилась».

Эти факты являются **описанием структуры опыта**, а не готовым ответом на вопрос:

> «хочу ли я это?»

Канонические отношения:

```text
Intrinsic Signal
≠
Reward
≠
Drive
≠
Utility / Value
≠
Goal
≠
Appraisal
```

и:

```text
higher signal magnitude
≠
more desirable
```

---

# 2. Главное архитектурное решение

MINDRA принимает **многопровайдерный typed Intrinsic Signal Layer без обязательной scalarization**.

Conceptually:

```text
World Model evidence ───────────┐
Self Model evidence ────────────┤
Perception / Memory history ────┤
committed experience ───────────┤
                               ▼
                    Intrinsic Signal Providers
                    ├── prediction provider
                    ├── novelty provider
                    ├── information provider
                    ├── competence provider
                    └── visitation provider
                               ↓
                     IntrinsicSignalBundle
                     ├── typed signal A
                     ├── typed signal B
                     └── typed signal C
```

Нет обязательного:

```text
intrinsic_reward = sum(signals)
```

Такое объединение, если понадобится, относится к будущим Drives/Valuation/Training semantics.

Решение дополнительно фиксируется в `ADR-0014`.

---

# 3. Почему не один IntrinsicRewardModule

Один модуль вида:

```text
experience
→ intrinsic_reward = 0.73
```

скрывает различия между причинами сигнала.

Значение `0.73` может означать:

- редкое посещение;
- ошибку World Model;
- снижение неопределённости;
- рост competence;
- несовместимый embedding scale;
- stochastic noise.

Для MINDRA это неприемлемо: downstream-механизм должен иметь возможность различить **что именно произошло**.

Поэтому providers независимы и заменяемы.

---

# 4. Intrinsic Signal Provider

Provider — agent-owned вычислительная capability, которая выводит один или несколько typed signals из явно объявленных causal inputs.

Provider может быть:

- stateless;
- stateful;
- deterministic;
- learned;
- density/count-based;
- model-based;
- rule-based/control implementation.

Если provider имеет causally relevant private baseline/history state, на него распространяются commit/snapshot rules `DU-05`.

Provider не получает ambient access ко всему Agent state.

---

# 5. Ownership и shared surface

`Intrinsic Signal Layer` владеет canonical namespace внутренних сигналов.

Каждый provider имеет уникальную identity и владеет только объявленными signal channels.

Conceptually:

```text
intrinsic_signals
├── provider_A / signal_1
├── provider_B / signal_2
└── provider_C / signal_3
```

Несколько providers могут вычислять разные estimators одного semantic family, но один не переписывает output другого.

Если нужен bundle/collection assembler, он выполняет только deterministic validation/collection и **не scalarize/ранжирует** сигналы.

---

# 6. Общая семантика IntrinsicSignal

Каждый canonical signal должен иметь достаточную identity/provenance, чтобы выразить минимум:

```text
IntrinsicSignal
├── signal_id
├── signal_kind
├── provider_identity/revision
├── source evidence references
├── source revisions
├── raw measure
├── optional normalized measure
├── measure semantics/unit
├── reference scope
├── temporal scope/window
├── availability/status
├── normalization identity/revision?
├── representation/feature-space identity?
├── baseline/history revision?
└── provenance
```

Exact field names/types пока не frozen.

---

# 7. Signal magnitude не является desirability

Для каждого signal kind направление означает только семантику измеряемого свойства.

Например:

```text
higher novelty
→ более новое относительно reference history
```

но не:

```text
higher novelty
→ Agent обязан хотеть это сильнее
```

То же относится к surprise, rarity, uncertainty reduction и competence change.

---

# 8. Prediction discrepancy

World Model уже может производить `PredictionErrorEvidence`.

Intrinsic provider может публиковать нормализованное/типизированное представление ошибки, но обязан сохранять связь с исходным prediction/outcome.

Примеры measure semantics:

```text
feature-space distance
semantic mismatch count
prediction loss
negative log-likelihood, если probabilistic model это обосновывает
```

Raw prediction discrepancy не является автоматически novelty или curiosity.

---

# 9. Predictive surprisal

Термин `surprisal` используется строже, чем бытовое «неожиданно».

Если модель задаёт сопоставимую predictive probability/density:

```text
surprisal = -log p(actual_outcome | context)
```

может существовать отдельный `predictive_surprisal` signal.

Если probability semantics отсутствует, нельзя переименовать arbitrary MSE/cosine distance в `surprisal` только ради удобства.

`Prediction discrepancy` и `predictive surprisal` остаются разными signal kinds.

---

# 10. Stochasticity и noisy-source problem

Высокая prediction error может сохраняться для fundamentally stochastic/uncontrollable процесса.

Поэтому:

```text
large persistent prediction error
≠
large learnable information opportunity
```

Intrinsic Signal Layer не пытается решить это скрытой scalarization.

Он сохраняет отдельные signals/evidence, а будущие Drives/Valuation могут предпочитать, например, information gain или reducible uncertainty вместо сырой ошибки.

Provider, который утверждает, что измеряет reducible/epistemic компонент, обязан иметь отдельное estimator/evaluation justification.

---

# 11. Novelty

`Novelty` — отношение текущего опыта к явно определённому reference history/representation.

Novelty record обязан указывать scope, например:

```text
episode novelty
session novelty
agent-lifetime novelty
local-memory novelty
representation-space novelty
```

Novelty не имеет универсальной формулы.

Возможные будущие estimators:

- distance to nearest known representations;
- density/pseudo-count;
- episodic kNN;
- prediction/distillation-based estimator;
- symbolic structural novelty.

Но estimator identity является частью provenance.

---

# 12. Novelty отдельно от surprise

Пример:

- знакомый stochastic объект может быть **не новым**, но трудно предсказуемым;
- новый, но полностью детерминированный объект может быть **новым**, но после объяснения легко предсказуемым.

Поэтому:

```text
novelty
≠
prediction discrepancy
≠
predictive surprisal
```

---

# 13. Visitation rarity

`Visitation rarity` — отдельный signal family, основанный на частоте/плотности посещения некоторого идентифицируемого состояния, события или representation region.

Он обязан определить:

- что считается «одинаковым посещением»;
- reference scope;
- count/density model identity;
- representation revision;
- decay/reset semantics, если применимо.

`1 / sqrt(count)` или pseudo-count bonus не являются canonical формулой MINDRA.

Rarity — измерение частоты, а не готовая ценность.

---

# 14. Information gain

`Information gain` допускается только там, где provider имеет содержательную before/after модель знания.

Conceptually:

```text
knowledge/belief before observation
        ↓ actual evidence
knowledge/belief after observation
        ↓
information gain
```

Возможная математическая форма для конкретного probabilistic estimator:

```text
KL(posterior || prior)
```

но canonical design не требует Bayesian implementation.

Если meaningful belief distribution/compatible estimator отсутствует:

```text
information_gain = unavailable
```

а не synthetic zero.

---

# 15. Uncertainty change

Вместо предположения, что uncertainty всегда уменьшается, канонически полезнее signed semantics:

```text
uncertainty_change = uncertainty_after - uncertainty_before
```

или эквивалентная явно документированная convention.

Тогда:

- отрицательное изменение может означать reduction;
- положительное — рост неопределённости.

Provider обязан указывать convention.

Сравнивать uncertainty до/после можно только при совместимой estimator/revision semantics.

---

# 16. Information gain отдельно от uncertainty change

Reduction одного scalar uncertainty summary не обязательно равен information gain.

Поэтому:

```text
information_gain
≠
uncertainty_change
```

Без formal estimator их нельзя использовать как взаимозаменяемые названия.

---

# 17. Competence change / learning progress

Self Model предоставляет context-conditioned competence estimates и resolutions.

Intrinsic provider может вычислять temporal signal класса:

```text
competence_before
→ evidence/update window
→ competence_after
→ competence_change
```

Предпочтительная базовая семантика — **signed change**.

```text
positive → improvement
negative → degradation/forgetting
zero-ish → little measured change
```

Absolute learning-progress magnitude, если понадобится, является отдельным derived channel, а не заменой signed evidence.

`Competence change` не становится reward автоматически.

---

# 18. Reference window и baseline

Некоторые signals нельзя определить по одному transition.

Например:

- learning progress;
- rarity/density;
- adaptive normalization;
- moving prediction baseline.

Provider должен иметь explicit:

```text
window identity
history scope
baseline revision
update policy
```

Нельзя использовать future observations для normal online signal, если experiment не обозначен как offline/research computation.

---

# 19. Temporal classes сигналов

Architecture должна допускать минимум:

```text
transition-scoped
outcome-scoped
event-scoped
window-scoped
episode-summary
session-summary
```

Signal timestamp сам по себе недостаточен: нужен causal source reference.

---

# 20. Observed, imagined и replayed signals

Natural runtime Intrinsic Signal должен сохранять provenance источника.

Канонически различаются:

```text
signal from actual committed experience
signal estimated over imagined trajectory
signal recomputed during replay
signal produced under intervention
```

Replay старого события **не считается новым посещением** normal runtime способом только потому, что sample снова прошёл через provider.

Imagined novelty не является пережитой novelty.

Если Planner позднее запросит expected future signal, такой результат должен иметь predicted/imagined provenance и не подменять actual signal.

---

# 21. Representation dependence

Novelty/rarity/distance-based signals могут зависеть от representation space.

Поэтому record обязан сохранять, где применимо:

```text
feature_space_id
feature_space_revision
encoder/model revision
distance/density semantics
```

Одинаковый scalar magnitude в несовместимых feature spaces не является сопоставимым measurement.

---

# 22. Representation drift

После изменения encoder:

```text
same event
→ novelty score under F3
→ novelty score under F4
```

может измениться без изменения самого мира.

Такой discontinuity не должен скрываться.

Возможные будущие стратегии:

- frozen signal encoder;
- re-encoding history;
- separate baselines by feature-space revision;
- compatibility adapter;
- restart/explicit reset estimator state.

DU-14 не выбирает universal strategy, но требует explicit revision semantics.

---

# 23. Normalization

Разные signal kinds могут иметь радикально разные масштабы.

Например:

```text
prediction_loss = 0.003
pseudo_count_rarity = 12.7
information_gain = 0.41
```

Поэтому provider может выдавать:

```text
raw_measure
normalized_measure?
```

Но normalizer обязан иметь собственную identity/revision/scope.

Нельзя молча сравнивать normalized values разных providers, если их шкалы не имеют explicit common semantics.

---

# 24. Causal online normalization

Online normalizer может зависеть только от доступного прошлого/текущего evidence.

Если normalizer обновляется:

```text
N17 → N18
```

signal должен быть связан с конкретной `normalizer_revision`.

Confirmatory evaluation позднее должна уметь отличить:

- frozen normalization;
- online adaptive normalization;
- offline post-hoc normalization.

Это разные экспериментальные режимы.

---

# 25. Stationarity

Intrinsic signals по своей природе часто нестационарны:

- Agent учится;
- World Model меняется;
- Self Model меняется;
- visitation counts растут;
- representation encoder меняется;
- normalizer меняется.

Поэтому temporal decline/рост сигнала не должен автоматически интерпретироваться как изменение мира.

Signal provenance должна позволять восстановить соответствующие source/provider revisions.

---

# 26. External feedback и evaluator leakage

Intrinsic provider normal runtime способом не использует:

- Environment Research Ground Truth;
- Objective Task Metric;
- hidden test split;
- oracle shortest path;
- evaluator success label,

если эти данные не были agent-visible или явно введены research intervention/supervision.

External Task Feedback также не становится intrinsic signal автоматически только потому, что прошёл через внутренний код.

---

# 27. Source dependencies

Providers должны использовать explicit declared sources.

Примеры:

```text
prediction provider
← PredictionErrorEvidence / WorldPrediction + actual outcome

competence provider
← SelfPredictionResolution / Self Belief revisions

novelty provider
← Canonical Percept / Memory-derived history / dedicated estimator state
```

Provider не должен сам искать скрытые зависимости через Service Locator/ambient Memory lookup.

---

# 28. Signal provider failure

Нельзя использовать один zero как универсальный failure result.

Нужно различать, где применимо:

```text
available
unknown
unavailable
insufficient_history
incompatible_revision
out_of_domain
stale
failed
```

Например, отсутствие Bayesian belief distribution означает `information_gain unavailable`, а не `information_gain = 0`.

---

# 29. Snapshot / restore

Exact Agent snapshot должен учитывать causally relevant state всех stateful providers, например:

```text
provider revisions
visitation counts/density state
novelty reference history
normalization statistics
competence windows/baselines
learned estimator parameters
RNG state
intervention/degradation state
```

Иначе restored Agent может получить другие intrinsic signals при том же внешнем опыте.

---

# 30. Intervention

Допустимы explicit interventions вида:

- изменить конкретный published signal;
- заменить provider на Control implementation;
- изменить provider baseline/history snapshot;
- заморозить normalizer;
- подменить signal ordering/identity в специальном experiment.

Любое intervention сохраняет provenance и не меняет semantic owner signal.

Composition-level ablation предпочтительнее runtime mutation provider implementation.

---

# 31. Control configurations

Нужно различать:

```text
NoIntrinsicSignals
DummySignalProvider
ConstantSignalProvider
RandomSignalProvider
ShuffledSignalProvider
MatchedNoiseProvider
real provider
```

Возможен также oracle research control, если он явно использует privileged data и никогда не выдаётся за natural intrinsic signal.

---

# 32. Causal evaluation

Будущая проверка должна различать минимум:

```text
correct signal
vs
shuffled/constant/noise control
vs
NoSignal
```

И отдельно проверять:

1. измеряет ли provider заявленное свойство опыта;
2. влияет ли этот signal downstream после появления Drives/Valuation;
3. специфичен ли эффект;
4. не объясняется ли выигрыш просто дополнительным compute/context/noise.

Высокая корреляция signal с успешным поведением сама по себе не доказывает причинность.

---

# 33. Отношение к Drives

DU-14 намеренно заканчивается до мотивации.

```text
Intrinsic Signal
→ «какое свойство имеет опыт?»

Drive
→ «насколько/в каком направлении подобное свойство сейчас создаёт внутреннее давление?»
```

Например, высокая novelty может существовать при низком будущемся novelty-seeking Drive.

---

# 34. Отношение к Valuation

Intrinsic Signal Layer не scalarize несколько каналов.

Будущий `Valuation` сможет учитывать, например:

```text
novelty
information_gain
competence_change
external feedback
goal progress
drives
risk
```

Но это не responsibility DU-14.

---

# 35. Отношение к Appraisal

Appraisal позднее может использовать intrinsic signals как evidence о событии, но signal сам по себе не является эмоциональной/контекстной оценкой.

Например:

```text
novelty = high
```

не означает автоматически:

```text
valence = positive
urgency = high
```

---

# 36. Research hypotheses, подготовленные DU-14

Архитектура позволяет позднее проверять гипотезы класса:

1. корректный novelty signal отличается по поведению от shuffled novelty после подключения Drives/Valuation;
2. information-gain-oriented signal устойчивее raw prediction error к irreducible stochasticity;
3. competence-change signal поддерживает адаптивный выбор обучаемых задач лучше constant/random control;
4. representation drift без revision control создаёт ложные novelty spikes;
5. один scalar intrinsic reward скрывает причинно различимые эффекты нескольких signal families.

Эти формулировки пока не являются зарегистрированными `HYP-*` до появления formal hypothesis registry.

---

# 37. Completion gate DU-14

`DU-14` считается завершённым, когда:

- signal/reward/drive/value boundaries определены;
- multi-provider architecture принята;
- signal identity/provenance/reference scope определены;
- prediction discrepancy отделён от surprisal/novelty;
- information gain/uncertainty-change semantics ограничены estimator validity;
- competence change имеет signed/window semantics;
- visitation rarity/novelty не смешаны без явного estimator;
- normalization/stationarity/revision rules определены;
- replay/imagined/natural signal provenance разведена;
- provider snapshot/control/failure semantics определены;
- downstream Drives/Valuation не спроектированы преждевременно;
- ADR и candidate contract синхронизированы.

После этого допускается `DU-15 — Drives`.
