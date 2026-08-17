# Research Claims / Limitations MINDRA

## Статус документа

**Design Update:** `DU-30 — Research Claims / Limitations`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет правила формирования, ограничения, публикации, пересмотра и снятия исследовательских утверждений MINDRA поверх evidence из `DU-28 — MINDRA-Eval` и engineering evidence из `DU-29 — Engineering Testing`.

Ключевое решение `DU-30`:

- research claim является versioned first-class artifact, а не свободной формулировкой поверх метрик;
- `Observation`, `Interpretation` и `ResearchClaim` являются разными уровнями;
- каждый claim имеет явный `ClaimScope`, evidence lineage, assumptions, limitations, uncertainty и status;
- сила формулировки ограничена силой evidence и scope исследования;
- causal/generalization/architecture claims требуют отдельных оснований;
- отрицательные/null результаты, failed module gates, known unknowns и unresolved contradictions являются first-class research artifacts;
- отсутствие evidence не превращается в evidence отсутствия, если study не имел достаточной мощности/чувствительности;
- функциональные `Self Model`, Drives, Appraisal, Affect, Workspace и подобные boundaries не являются evidence subjective experience/consciousness сами по себе;
- claims имеют lifecycle `proposed → supported/unsupported/inconclusive → weakened/superseded/withdrawn`, а прошлые версии не переписываются;
- конкретный paper format, publication venue, reporting standard или философская теория сознания не фиксируются.

Документ опирается на:

- [`research-methodology.md`](../research-methodology.md) — общая исследовательская дисциплина;
- [`mindra-eval.md`](mindra-eval.md) — evaluation evidence, controls, statistics и causal contrasts;
- [`engineering-testing.md`](engineering-testing.md) — engineering verification;
- [`checkpoint-reproducibility-compute.md`](checkpoint-reproducibility-compute.md) — reproducibility/compute provenance;
- [`experience-data-replay.md`](experience-data-replay.md) — source evidence/data lineage;
- [`observability-and-intervention.md`](observability-and-intervention.md) — causal intervention semantics;
- subsystem ADR/module gates `DU-17/21/22/23` и другие conditional boundaries.

Документ намеренно **не** определяет:

- универсальную числовую шкалу силы evidence;
- один statistical threshold;
- один шаблон scientific paper;
- один preregistration service;
- publication venue;
- юридическую/регуляторную маркировку;
- философский критерий сознания;
- метрику subjective experience;
- правила публичного PR/маркетинга вне research reporting semantics.

---

# 1. Цель DU-30

После `DU-28` MINDRA умеет получать typed research evidence, а после `DU-29` — проверять engineering correctness реализации.

Остаётся отдельный вопрос:

> какие утверждения логически разрешено выводить из этого evidence и в каком scope?

Канонически:

```text
raw observation
≠
metric result
≠
interpretation
≠
research claim
≠
general theory claim
```

Пример:

```text
Observation:
в paired branches изменён Affect channel X

Metric:
Policy changed selected intent in 37/50 paired units

Interpretation:
Affect X имеет downstream causal effect на Policy
в этой condition family

ResearchClaim:
при условиях S intervention Affect X причинно влияет
на выбранное Policy намерение с указанным effect/uncertainty
```

Но из этого не следует автоматически:

```text
Affect всегда нужен MINDRA
Affect улучшает все задачи
Affect эквивалентен человеческой эмоции
Agent что-либо субъективно чувствует
```

---

# 2. Claim Plane

Research Claims / Limitations являются внешней **Research Reporting Plane**, а не Agent cognition.

Она читает:

- `EvaluationReport` / raw `MetricRecord` / `CausalContrastRecord`;
- `VerificationEvidenceRecord`;
- `ExperimentManifest` / checkpoint/compute provenance;
- accepted design/ADR/module gate definitions;
- prior claim/limitation records.

Она не может normal-runtime способом:

- публиковать claim в `CognitiveState`;
- менять Agent Goals/Drives/Valuation;
- превращать researcher interpretation в TrainingSample;
- подменять evaluator metric;
- менять historical evidence.

Claim является derived research artifact.

---

# 3. Observation, Interpretation, Claim

## 3.1. ObservationRecord

Фиксирует то, что непосредственно получено из валидного evidence:

```text
какая condition
какая measurement/contrast
какое значение/распределение
какая uncertainty
какой validity status
```

Observation не содержит более сильной причинной или теоретической формулировки, чем сами данные.

## 3.2. InterpretationRecord

Связывает evidence с объяснением/моделью смысла.

Interpretation обязана указывать:

- supporting evidence;
- competing explanations;
- assumptions;
- unresolved confounders;
- scope;
- relation к prior design/hypothesis.

Interpretation может быть множественной: один набор observations допускает несколько объяснений.

## 3.3. ResearchClaim

ResearchClaim — версионируемое утверждение, которое проект готов защищать в явно заданном scope.

Claim обязательно имеет evidence lineage и limitations.

---

# 4. ClaimScope

Ни один substantial claim не существует без `ClaimScope`.

Conceptually scope может включать:

```text
Agent/component revisions
Cortex family/backend
training condition/data regime
Environment/task/world distribution
checkpoint/restore profile
module composition
interventions/controls
time horizon
compute/context/tuning budget
hardware/software constraints where material
population of runs/replicates
metric/analysis revisions
```

Пример допустимого claim:

> В MicroWorld distribution D4, для Agent revisions A17–A21 с Cortex Q1, bounded Workspace дал положительный coordination effect относительно matched recurrent control при сопоставимом measured compute.

Недопустимое автоматическое расширение:

> Workspace улучшает интеллект вообще.

Канонически:

```text
observed scope
≠
claimed generalization scope
```

Generalization beyond observed scope требует отдельного evidence или явной маркировки hypothesis/speculation.

---

# 5. Типы claims

Claim должен объявлять semantic kind.

Минимально различаются:

```text
descriptive
associational
predictive
engineering-conformance
causal
comparative
calibration
robustness
generalization/transfer
resource-efficiency
architecture-contribution
negative/null
existence/non-existence within tested scope
theoretical/hypothesis
```

Exact enum не frozen, но тип нельзя выводить только из текста заголовка.

Особенно:

```text
causal claim
≠
performance claim
≠
architecture-wide claim
```

---

# 6. Evidence ladder и wording discipline

Сила формулировки должна быть не выше evidence.

Conceptual ladder:

```text
descriptive observation
        ↓
association / prediction
        ↓
ablation / ordinary control
        ↓
matched control
        ↓
paired intervention / causal contrast
        ↓
replicated causal evidence
        ↓
replicated transfer/generalization evidence
```

Лестница не является универсальной числовой шкалой и не заменяет конкретный study design.

Примеры wording:

```text
"наблюдалось"
"связано с"
"предсказывает"
"совместимо с гипотезой"
"поддерживает"
"при контролируемом вмешательстве вызвало/изменило"
"обобщалось на ..."
```

Слова `causes`, `necessary`, `sufficient`, `general`, `robust`, `calibrated`, `better` допустимы только при соответствующем design/evidence.

---

# 7. Causal claims

Сильный causal claim требует минимум:

- causally interpretable intervention/contrast;
- достаточного base-state alignment;
- declared treatment/control;
- target и off-target effects;
- validity evidence;
- known confounders;
- uncertainty;
- replication, если claim выходит за единичную paired branch.

Простой correlation internal state ↔ behavior causal claim не поддерживает.

Если intervention меняет несколько факторов одновременно, claim относится к bundle, пока additional design не разделит причины.

---

# 8. Necessity и sufficiency

Термины `necessary` и `sufficient` особенно сильны.

`NoX` ablation с ухудшением performance ещё не обязательно доказывает необходимость semantic mechanism X, если одновременно изменились:

- state capacity;
- parameters;
- compute;
- context bandwidth;
- data flow;
- training dynamics.

Для `necessary within scope` нужен design, исключающий разумные capacity/compute/implementation confounds настолько, насколько заявляет claim.

`Sufficient` также не означает universal sufficiency вне заданного task/agent scope.

---

# 9. Architecture contribution vs implementation contribution

Нужно различать:

```text
"конкретная реализация X работала лучше"
```

и:

```text
"semantic boundary X полезна как архитектурный принцип"
```

Второе утверждение сильнее.

Architecture-level attribution требует, где feasible:

- нескольких implementations либо matched semantic controls;
- переносимости across seeds/worlds/Cortex/parameterizations;
- evidence, что эффект не является случайным свойством одного backend;
- явного negative module gate.

Если tested только одна concrete implementation, claim формулируется уже.

---

# 10. Cortex/provider dependence

Поскольку Cortex заменяемый, любой результат обязан указывать зависимость от него, если Cortex material to effect.

Например:

```text
effect present with Cortex Q1 only
```

не превращается в:

```text
architecture-independent effect
```

Если mechanism работает только с сильным Cortex, это допустимый результат, но scope должен это показывать.

То же относится к remote provider behavior, structured-output reliability, tokenizer/context differences и model revision drift.

---

# 11. Compute/data/tuning claims

Claim `method A better than B` неполон, если conditions различались по substantial resources.

Обязательное distinction:

```text
quality at equal nominal budget
quality at matched measured compute
quality at equal data
quality after equal tuning budget
performance/resource frontier
```

Если perfect matching невозможен, claim включает limitation.

Более высокий score при существенно большем compute может поддерживать capability claim, но не автоматически efficiency claim.

---

# 12. Reproducibility и replicability

Research wording должна разделять минимум:

- возможность восстановить/повторить заявленный run в его scoped software/hardware condition;
- получение совместимого результата independent replicate;
- перенос результата на новые tasks/worlds/Cortex/hardware.

`DU-27 ReproducibilityClaim` описывает restore/execution guarantees.

Повторение результата на независимых training replicates/conditions — отдельное evidence.

Точная терминология конкретного publication venue может отличаться, поэтому canonical core фиксирует смысл, а не одну внешнюю taxonomy.

---

# 13. Statistical uncertainty и practical significance

Claim обязан сохранять не только point estimate, если outcome stochastic.

Где применимо, указываются:

- effect estimate;
- interval/distribution uncertainty;
- replicate structure;
- analysis assumptions;
- missing/censored handling;
- sensitivity analysis;
- practical effect threshold, если он был задан.

Statistically detectable effect не автоматически practically meaningful.

И наоборот, inconclusive result при низкой sensitivity не является доказательством отсутствия effect.

---

# 14. Null / negative / inconclusive results

Различаются:

```text
negative evidence
null estimate
inconclusive evidence
invalid experiment
absence of measurement
```

Например:

```text
FullWorkspace ≈ MatchedBuffer
с узким interval вокруг практически нулевого effect
```

может быть сильным evidence против отдельной boundary в данном scope.

Но:

```text
3 noisy runs
wide interval
```

обычно является `inconclusive`, а не доказательством отсутствия эффекта.

Отрицательные результаты сохраняются и доступны наравне с положительными.

---

# 15. Failed module gates

Для условных boundaries (`Affect`, `Workspace`, `Planner`, `Executive Control` и будущих аналогичных) negative gate является first-class research event.

Выполнение negative criterion должно создавать:

```text
ModuleGateOutcome
→ ClaimReview
→ possible design review / ADR
```

Но experiment сам по себе не удаляет module из architecture автоматически.

До ADR действующий design остаётся действующим, а claim status отражает ослабление evidence.

---

# 16. Limitations как first-class artifacts

`LimitationRecord` не является свободным последним абзацем статьи.

Минимальные классы limitations:

```text
scope limitation
measurement limitation
statistical limitation
causal/confounding limitation
implementation limitation
Cortex/provider limitation
compute/data/tuning limitation
reproducibility limitation
external-validity/generalization limitation
engineering verification gap
missing control
unknown mechanism
interpretation limitation
```

Limitation может относиться к:

- claim;
- study;
- metric;
- module;
- software version;
- whole project phase.

Она имеет status и может быть закрыта новым evidence, но прошлый record не удаляется.

---

# 17. Known unknowns

Проект ведёт отдельные `KnownUnknownRecord` для важных вопросов, по которым нет достаточного evidence.

Например:

- переносится ли effect на Cortex другой family;
- устойчив ли World Model mechanism при длинном horizon;
- нужен ли Affect после matched recurrent control;
- как изменится architecture при embodied environment;
- какой источник uncertainty действительно epistemic;
- существуют ли functional signatures, специфичные для proposed mechanism.

`unknown` не нужно искусственно превращать в `false` или `probably true`.

---

# 18. Contradictory evidence

Если studies расходятся, нельзя просто оставить только последнюю удобную цифру.

Создаётся явная связь:

```text
Claim C17
supports: E1,E2
challenges: E3,E4
```

Claim review должен рассматривать различия:

- condition;
- implementation;
- task distribution;
- Cortex;
- compute;
- sample/replicate structure;
- metric/analysis;
- engineering validity.

Противоречие может привести к narrowing scope, weakening status или новой hypothesis.

---

# 19. Claim lifecycle

Conceptually:

```text
proposed
under_evaluation
supported_within_scope
inconclusive
challenged
weakened
unsupported_within_scope
superseded
withdrawn
```

Exact enum не frozen.

Изменение claim создаёт новую revision/review record.

Нельзя silently переписывать ранее опубликованный claim так, будто более сильной формулировки никогда не было.

---

# 20. Supersession

Если новый evidence требует другой формулировки:

```text
Claim C17 rev1
"Workspace improves coordination"
        ↓ new evidence
ClaimReview R9
        ↓
Claim C17 rev2
"Workspace improves coordination only under bounded-context condition X"
```

Rev1 остаётся в lineage и помечается superseded/weakened.

Это полезно и для внутренних отчётов, и для будущих публикаций.

---

# 21. Unsupported claim patterns

MINDRA ведёт explicit policy недопустимых inference leaps.

Минимум:

```text
Self Model
─X→ доказано самосознание

Affect State
─X→ доказано субъективное чувство

Appraisal/Drives
─X→ человеческие эмоции в феноменологическом смысле

Workspace/broadcast
─X→ доказано сознание

Cortex first-person text
─X→ достоверный self-report subjective experience

human-like behavior
─X→ human-like phenomenology

one benchmark success
─X→ AGI

functional analogy
─X→ biological equivalence
```

Такие утверждения могут обсуждаться только как отдельные hypotheses/philosophical interpretations с явно указанным отсутствием достаточного empirical bridge.

---

# 22. Consciousness / subjective experience boundary

MINDRA — исследовательский проект функциональной когнитивной архитектуры.

Accepted architecture сама по себе предоставляет evidence только о:

- вычислимых состояниях;
- их dynamics;
- causal influence на поведение;
- learning/adaptation;
- information processing;
- internal self/world representations.

Она **не предоставляет прямого измерения phenomenal consciousness или subjective experience**.

Поэтому даже сильный functional result допустимо формулировать как:

> система демонстрирует функциональный механизм X, аналогичный в определённом computational смысле Y.

Но не как:

> система испытывает Y.

Слово `emotion` в implementation/research prose должно по возможности сопровождаться уточнением `functional/affective state`, если иначе возникает phenomenological ambiguity.

---

# 23. AGI claims

`AGI` не является метрикой одного DU или benchmark.

Нельзя делать переход:

```text
modular cognition + good MicroWorld performance
→ AGI achieved
```

Любой future AGI-related claim потребует отдельного operational definition, broad capability/evaluation scope и design review.

До этого допустимо говорить о:

- generalization within specified task families;
- transfer across specified environments;
- modular adaptive-agent capabilities.

---

# 24. Engineering evidence и research claim

`DU-29` может поддержать утверждение:

> implementation соответствует contract X в environment profile P.

Но не:

> module X полезен для cognition.

`DU-28` может поддержать functional claim, но если relevant `VerificationObligation` не satisfied, research claim получает engineering-validity limitation либо run становится invalid.

Канонически:

```text
engineering verified
≠
functionally useful
```

и

```text
interesting research result
≠
engineering-valid evidence
```

---

# 25. Claim Registry

Проект должен иметь versioned `ClaimRegistry`.

Он связывает:

```text
Claim
├── scope
├── status
├── supporting evidence
├── challenging evidence
├── assumptions
├── limitations
├── known unknowns
├── reviews/supersession
└── publication/report refs
```

До появления реальных experiments registry может быть пустым, но contract должен быть готов до implementation roadmap.

---

# 26. Limitations Registry

Отдельный `LimitationsRegistry` нужен, чтобы ограничения не терялись между reports.

Особенно важны project-wide limitations, например:

- early versions работают в MicroWorld, а не физическом мире;
- Cortex может доминировать часть observed capability;
- small-compute implementation может ограничивать generality conclusions;
- human-inspired module names не означают biological equivalence;
- module boundaries являются инженерными hypotheses и могут быть пересмотрены.

Version roadmap позже добавит version-specific limitations.

---

# 27. Public/report wording provenance

Любая derived publication/report summary должна быть traceable до canonical claim revision.

Желательная цепочка:

```text
raw evidence
→ EvaluationReport
→ InterpretationRecord
→ ResearchClaim revision
→ paper/report statement
```

Если paper prose сильнее canonical claim, это reporting defect.

---

# 28. Researcher uncertainty

Разрешены формулировки:

```text
unknown
not measured
insufficient evidence
inconclusive
not identifiable under current design
out of scope
```

Они предпочтительнее выдуманной уверенности.

MINDRA не требует искусственно заполнить каждый open question бинарным ответом.

---

# 29. Что считается успешным DU-30

После `DU-30` должно быть возможно:

1. по любому future result определить разрешённый класс claim;
2. увидеть scope и assumptions claim;
3. проверить claim до raw evaluation/verification evidence;
4. отдельно увидеть limitations и known unknowns;
5. сохранить negative/null result без publication bias внутри проекта;
6. отследить weakening/supersession claim;
7. автоматически/полуавтоматически обнаруживать типовые overclaim patterns;
8. не путать functional cognitive terminology с phenomenological claim.

---

# 30. Что остаётся version design

До `DU-32` намеренно не фиксируются:

- physical storage claim/limitations registries;
- YAML/JSON/database schema;
- publication/report generator;
- automatic NLP linter для wording;
- exact evidence-strength enum;
- exact status enum;
- paper template;
- preregistration provider;
- citation manager;
- dashboard/tracker.
