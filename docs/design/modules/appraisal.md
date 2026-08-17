# Appraisal MINDRA

## Статус документа

**Design Update:** `DU-16 — Appraisal`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет event-level слой контекстной оценки MINDRA — `Appraisal System`, который оценивает **значение конкретного события, изменения, исхода или рассматриваемого будущего относительно текущего состояния Agent**.

Документ определяет:

- responsibility и ownership `Appraisal System`;
- `Appraisal Target` и event boundary;
- контекст оценки и его revision/provenance;
- actual, predicted, imagined, retrospective и intervened appraisal;
- typed multidimensional `Appraisal Profile`;
- relevance;
- goal congruence;
- drive conduciveness;
- expectedness;
- controllability;
- coping potential;
- urgency/temporal pressure;
- causal agency/attribution как optional dimension family;
- границу local event polarity/valence с будущим `Valuation`;
- reappraisal semantics;
- rule-based, learned, hybrid и Cortex-assisted implementations;
- observability/intervention;
- `NoAppraisal`/Dummy/Control configurations;
- snapshot/failure/degradation requirements.

Документ опирается на:

- [`../execution-model.md`](../execution-model.md) — actual/predicted/imagined/replayed causal provenance и logical time;
- [`../cognitive-state.md`](../cognitive-state.md) — committed state, ownership, revision, freshness и availability;
- [`../module-lifecycle.md`](../module-lifecycle.md) — staged computation и atomic commit;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — passive evidence и controlled intervention;
- [`goals.md`](goals.md) — committed Goal Graph;
- [`memory.md`](memory.md) — explicit retrieval и historical evidence;
- [`world-model.md`](world-model.md) — World Belief, prediction, imagination и uncertainty;
- [`self-model.md`](self-model.md) — competence/capability/self-prediction;
- [`intrinsic-signals.md`](intrinsic-signals.md) — novelty, surprisal, information/competence signals;
- [`drives.md`](drives.md) — persistent `DriveStateSet` и typed regulatory pressure.

Документ намеренно **не** определяет:

- human emotion labels как обязательный output;
- Affect Dynamics — `DU-17`;
- общую decision utility/value — `DU-18`;
- Salience/Attention — `DU-19`;
- coping/action selection — `DU-22/23`;
- конкретный Appraisal neural architecture;
- конкретный Cortex prompt;
- exact training targets/losses — `DU-26`;
- exact Python API/checkpoint encoding — `DU-27`;
- наличие субъективных чувств или phenomenal consciousness.

---

# 1. Цель DU-16

К моменту `DU-16` MINDRA уже различает:

```text
что наблюдается                → Perception
что, вероятно, происходит      → World Model
что Agent умеет                → Self Model
что было новым/неожиданным     → Intrinsic Signals
чего Agent committed добивается → Goal System
каково его внутреннее давление → Drive System
```

Но отсутствует отдельный ответ на вопрос:

> «Что **это конкретное событие** означает для **этого Agent именно сейчас**, с учётом его целей, drives, ожиданий и возможностей?»

`Appraisal System` вводит такую event-level relational assessment.

Ключевой исследовательский паттерн:

```text
same event
+
different Goal Graph / DriveStateSet / Self Belief / World Belief
        ↓
different Appraisal Profile
        ↓
future Affect / Valuation / Salience / behavior may differ
```

Это один из механизмов функциональной субъективности MINDRA, но не доказательство субъективного переживания.

---

# 2. Главное архитектурное решение

MINDRA принимает **event-centered typed multidimensional Appraisal System**.

Conceptually:

```text
Appraisal Target
        +
committed context references
        │
        ├── Goals
        ├── DriveStateSet
        ├── World Belief / Prediction
        ├── Self Belief / Prediction
        ├── explicit Memory Retrieval
        ├── Intrinsic Signals
        └── relevant percept/outcome evidence
        ↓
   Appraisal System
        ↓
   AppraisalRecord
        └── AppraisalProfile
            ├── relevance
            ├── goal_congruence[]
            ├── drive_conduciveness[]
            ├── expectedness
            ├── controllability
            ├── coping_potential
            ├── urgency
            ├── agency/attribution?
            └── optional local polarity summary?
```

Нет обязательного:

```text
emotion = "fear"
```

Нет обязательного:

```text
appraisal_value = -0.73
```

Нет обязательного:

```text
reward += appraisal_value
```

Решение отдельно фиксируется `ADR-0016`.

---

# 3. Appraisal является отношением, а не свойством события самого по себе

Одно событие не имеет единственного канонического appraisal независимо от Agent state.

Например, один и тот же найденный объект может быть:

```text
Agent state A:
Goal = найти объект
→ goal-congruent

Agent state B:
Goal = избежать объекта
→ goal-incongruent

Agent state C:
Goal unrelated
→ low relevance
```

Поэтому appraisal всегда привязан минимум к:

```text
target identity
+
appraisal context revision(s)
+
agent_revision
+
appraisal-system revision
```

`AppraisalRecord` без context provenance недостаточен для интерпретации.

---

# 4. Appraisal Target

`Appraisal Target` — причинно идентифицируемый объект оценки.

Target может быть:

- фактически произошедшим Environment outcome/event;
- значимым изменением `Canonical Percept`;
- Goal lifecycle/progress event;
- agent-visible internal event;
- World Model prediction;
- imagined outcome/trajectory node;
- явно retrieved historical event;
- controlled intervention target/result.

Не каждый field update автоматически становится отдельным Appraisal Target.

Нужна явная event-construction boundary, иначе система создаст бесконечный поток appraisal для технических изменений state.

Exact event detector/assembler определяется implementation позднее.

---

# 5. Target mode / causal provenance

Канонически различаются по меньшей мере:

```text
actual
predicted
imagined
retrospective/retrieved
intervened
replayed/offline, если appraisal пересчитывается вне natural runtime
```

Эти режимы не являются взаимозаменяемыми.

## 5.1 Actual appraisal

Target уже является committed фактом опыта Agent.

## 5.2 Anticipatory appraisal

Target является World Prediction или другим ещё не произошедшим возможным исходом.

Он не превращается из-за appraisal в observed fact.

## 5.3 Imagined appraisal

Target находится внутри imagination rollout.

Такой appraisal может позже использовать Planner/Valuation, но не считается пережитым actual event.

## 5.4 Retrospective appraisal

Agent явно вспоминает/восстанавливает прошлое событие и оценивает его **сейчас**.

Это новый appraisal record, а не заднее редактирование исходного appraisal прошлого.

---

# 6. Appraisal context

Appraisal не получает ambient access ко всему Agent state.

Для каждого computation должна существовать explicit context surface с references на разрешённые committed данные.

Conceptually:

```text
AppraisalContext
├── target reference
├── state_revision
├── agent_revision
├── Goal Graph revision / relevant goals
├── DriveStateSet revision / relevant drives
├── World Belief/Prediction references
├── Self Belief/Prediction references
├── explicit RetrievalResult references?
├── relevant IntrinsicSignal references?
├── task/external-feedback references, если agent-visible
└── intervention/degradation provenance
```

Не каждый appraisal обязан читать все источники.

Declared dependencies определяются concrete dimension/provider requirements.

---

# 7. Evaluation time и target time различаются

Для retrospective/reappraisal важны два времени:

```text
target_event_time
appraisal_evaluation_time
```

Например, событие произошло в `Episode 2`, а переоценивается в `Episode 9` после нового опыта.

Если задача — реконструировать **исходный** appraisal, нужен historical context snapshot/references.

Если задача — выполнить **текущий reappraisal** прошлого события, используются current committed concerns.

Эти режимы нельзя смешивать.

---

# 8. Appraisal Profile является многомерным

Appraisal dimensions имеют отдельные semantic identity.

Общий обязательный universal scalar отсутствует.

Каждая dimension должна иметь минимум:

```text
dimension_id
semantic definition
target/context references
measure/value
availability/status
confidence/evidence support, если применимо
estimator/rule revision
provenance
```

Dimensions могут быть:

- scalar;
- signed scalar;
- categorical;
- interval/distribution;
- vector по Goal/Drive IDs;
- structured relation.

Нельзя требовать один shape только ради удобства neural network.

---

# 9. Relevance

`Relevance` отвечает:

> насколько target связан с текущими committed concerns Agent?

Concerns могут включать:

- активные/committed Goals;
- текущие Drive States;
- явно agent-visible constraints;
- future value-related concerns после `DU-18`.

Relevance не равна:

```text
Salience
Attention allocation
Utility
Goal priority
novelty
```

Событие может быть очень новым, но почти нерелевантным текущим concerns.

И наоборот, полностью ожидаемый outcome может быть критически релевантен.

---

# 10. Goal congruence

`Goal congruence` описывает отношение target к конкретным committed Goals.

Предпочтительная semantics — **per-goal relation**, а не один общий scalar.

Conceptually:

```text
goal_congruence
├── G17 → facilitating / obstructing / neutral / unknown
├── G21 → facilitating / obstructing / neutral / unknown
└── ...
```

Допустима quantitative magnitude, если её semantics operationally определена.

Appraisal не меняет Goal Graph.

Если несколько Goals конфликтуют, Appraisal сохраняет это различие и не решает, какой Goal важнее.

---

# 11. Drive conduciveness

`Drive conduciveness` оценивает, как target относится к текущей регуляции конкретных drives.

Conceptually:

```text
drive_conduciveness
├── drive_A → pressure likely reduced / increased / unchanged / unknown
├── drive_B → ...
```

Это event-level оценка влияния, а не новый committed `Drive State`.

Appraisal не мутирует drives и не scalarize их конфликт.

Если target только предположительно изменит drive в будущем, provenance должна указывать predicted/imagined character оценки.

---

# 12. Expectedness

`Expectedness` отвечает:

> насколько target согласуется с тем, что Agent ожидал непосредственно перед ним?

Это relation между target и prior predictive state/evidence.

Канонически:

```text
expectedness
≠
novelty
≠
predictive surprisal
≠
prediction discrepancy
```

Intrinsic Signal provider может дать raw/normalized surprisal или discrepancy.

Appraisal может использовать эти данные вместе с context, но не переименовывает их в новое универсальное значение.

Если prior prediction отсутствовало, expectedness может быть `unknown`/`unavailable`, а не `0`.

---

# 13. Controllability

`Controllability` отвечает:

> в какой степени развитие данной ситуации **вообще чувствительно к доступным действиям Agent**?

Это в первую очередь свойство отношения:

```text
current World Belief
+
available action space
+
World dynamics
+
target/consequence
```

Controllability не равна competence.

Ситуация может быть в принципе контролируема, но конкретный Agent может плохо уметь выполнить необходимое действие.

---

# 14. Coping potential

`Coping potential` отвечает:

> насколько **этот конкретный Agent в текущем состоянии** способен эффективно изменить, выдержать, обойти или адаптироваться к последствиям target?

Он может использовать:

- Self Model competence;
- available capabilities;
- known resource/compute constraints, если они agent-visible;
- World Model alternatives;
- Goal/Drive context.

Канонически:

```text
controllability
≠
coping_potential
```

Например:

```text
ситуация controllable = high
но current competence = low
→ coping potential может быть low
```

или наоборот: исход нельзя отменить, но Agent может иметь высокую способность адаптироваться к последствиям.

Appraisal не выбирает coping strategy — это будущая Executive/Policy responsibility.

---

# 15. Urgency / temporal pressure

`Urgency` оценивает, насколько быстро требуется потенциальная реакция относительно релевантных consequences.

Она может зависеть от:

- World Model horizon;
- deadline/closing action window;
- скорости ухудшения Goal/Drive condition;
- необратимости последствий.

Urgency не равна:

```text
Salience
Action priority
Utility
Drive pressure
```

Высокая urgency может позже влиять на эти механизмы, но Appraisal сама не выполняет arbitration.

---

# 16. Causal agency / attribution

Appraisal contract допускает optional dimension family, которая отвечает:

> чему/кому Agent приписывает причинную роль в target?

Возможные categories зависят от Environment semantics, например:

```text
self
other agent
external process/environment
mixed
unknown
```

Такая dimension не является обязательной для минимального MicroWorld.

Она особенно полезна, если future environments содержат других agents или social/normative tasks.

Ground Truth causal attribution evaluator не может использоваться natural Appraisal автоматически.

---

# 17. Norm compatibility не является обязательной core dimension

Человеческие appraisal theories часто включают normative/moral compatibility.

MINDRA не вводит её как mandatory field до появления отдельной agent-owned semantics норм/стандартов.

Нельзя подменять её:

- evaluator rule;
- developer preference;
- hidden safety policy;
- system prompt;
- внешней human annotation.

Если future design вводит agent-visible Norm/Standard representation, dimension может быть добавлена как extension с собственной ownership/provenance.

---

# 18. Valence / pleasantness и граница с Valuation

MINDRA **не принимает обязательный global valence scalar** в `DU-16`.

Причина: один target может одновременно:

```text
помогать Goal A
мешать Goal B
снижать Drive X
повышать Drive Y
```

Сведение этого в:

```text
valence = +0.2
```

уже требует aggregation/scalarization policy, которая относится к будущему `DU-18 — Valuation`.

Допускается optional **local event polarity summary**, если конкретная implementation/experiment его требует, но он обязан:

- быть derived;
- иметь explicit aggregator/revision;
- ссылаться на underlying dimensions;
- не называться action/state utility;
- не заменять многомерный profile;
- не становиться RL reward автоматически.

---

# 19. Appraisal ≠ Valuation

Каноническое разделение:

```text
Appraisal:
«что означает этот target относительно моего текущего контекста?»

Valuation:
«какова decision-relevant ценность возможных состояний/исходов/действий с учётом разных факторов?»
```

Appraisal event-level и descriptive-relational.

Valuation будет выполнять aggregation/decision-facing evaluation в `DU-18`.

---

# 20. Appraisal ≠ Affect

AppraisalRecord относится к конкретному target и evaluation context.

Он не является persistent mood/emotional state.

Conceptually:

```text
Event E1 → Appraisal A1
Event E2 → Appraisal A2
Event E3 → Appraisal A3
              ↓
future Affect Dynamics may integrate them over time
```

Decay, inertia, accumulation и recovery affective state относятся к `DU-17`.

`Appraisal System` не должен скрыто хранить persistent emotional state только потому, что такой state удобен model implementation.

---

# 21. Appraisal ≠ Intrinsic Signals

Intrinsic Signals измеряют свойства опыта/знания.

Appraisal оценивает target относительно concerns.

Например:

```text
novelty = high
```

может сопровождаться:

```text
relevance = low
```

или:

```text
relevance = high
```

в зависимости от Goals/Drives.

Это различие обязательно сохраняется.

---

# 22. Appraisal и Memory

Appraisal не имеет ambient доступа ко всему Memory Store.

Если прошлый опыт требуется для оценки, существует explicit:

```text
RetrievalRequest
→ RetrievalResult
→ AppraisalContext
```

Например, retrieved evidence может помогать оценить:

- знакомство с ситуацией;
- прошлую controllability;
- прошлую competence;
- похожие outcomes.

Но факт retrieval остаётся отдельным causal event.

---

# 23. Appraisal и Cortex

Cortex может быть optional implementation capability для:

- semantic interpretation сложного target;
- language-heavy appraisal;
- candidate dimension estimation;
- explanation generation.

Но Cortex output не становится AppraisalRecord автоматически.

Правильная boundary:

```text
Appraisal component
→ semantic CortexRequest
→ CortexResult
→ validation / dimension estimation
→ AppraisalRecord
```

`NoCortex`-совместимая Appraisal implementation должна оставаться архитектурно допустимой.

Model-specific prompt/CoT не является canonical appraisal state.

---

# 24. Rule-based, learned и hybrid Appraisal

Допустимы:

- deterministic/rule-based dimensions;
- learned regressors/classifiers;
- probabilistic estimators;
- Cortex-assisted estimation;
- hybrid systems.

Разные dimensions одного profile не обязаны вычисляться одной neural network.

Например, goal congruence в простом MicroWorld может быть rule-derived, а coping potential — learned/calibrated.

Архитектура не требует единого estimator.

---

# 25. Dimension availability и partial profile

Не каждая dimension применима или вычислима всегда.

Допустим:

```text
relevance = available
expectedness = unavailable (prior prediction отсутствовало)
controllability = unknown
coping_potential = available
agency = not_applicable
```

Нельзя заменять все эти состояния одним `0`/`None`.

`AppraisalProfile` может быть частичным, если downstream contracts допускают это.

Required dimensions конкретного experiment/configuration определяются явно.

---

# 26. Evidence и support

Dimension value должна по возможности ссылаться на evidence, из которого она получена.

Например:

```text
expectedness
→ WorldPrediction P17 + Outcome O18

coping_potential
→ SelfPrediction SP22 + World alternatives

goal_congruence G5
→ Goal G5 + predicted/actual progress evidence
```

Если dimension learned и не имеет простой deterministic derivation, сохраняются estimator identity/revision и confidence/support semantics, если они meaningful.

---

# 27. Calibration / validation

Appraisal dimensions не получают автоматическую «истинность» только потому, что выглядят психологически разумно.

Там, где dimension имеет проверяемый target, нужны отдельные diagnostics.

Примеры:

- expectedness ↔ prior predictive distribution/evidence;
- controllability ↔ controlled action/counterfactual sensitivity;
- coping potential ↔ фактическая успешность adaptation при сопоставимых условиях;
- goal congruence ↔ explicit Goal progress/consequence semantics;
- urgency ↔ фактический response horizon/deadline, если он operationally определён.

Не все dimensions обязаны иметь одинаковый тип calibration metric.

Exact evaluation определяется `DU-28`.

---

# 28. Reappraisal

Один target может быть оценён повторно.

Правильно:

```text
Target E42
├── Appraisal A10 @ context R100
└── Appraisal A31 @ context R180
        relation: reappraisal_of A10
```

Неправильно:

```text
A10.value = new_value
```

с уничтожением исторического state.

Reappraisal может измениться из-за:

- нового World evidence;
- изменения Goals;
- изменения DriveStateSet;
- роста competence;
- нового Memory retrieval;
- нового interpretation.

Это создаёт явную temporal trajectory appraisal, не требуя отдельного Affect state.

---

# 29. Appraisal history и Memory

История AppraisalRecord может храниться в trajectory/evidence автоматически для исследования.

Но долговременная **agent-accessible** память appraisal не возникает автоматически.

Чтобы Agent позже вспомнил собственный прошлый appraisal:

```text
AppraisalRecord
→ MemoryWriteProposal
→ Memory Core
```

согласно Memory contract.

`DU-20` позднее сможет изменить retention/consolidation policy, но не semantic identity исходного appraisal.

---

# 30. Appraisal lifecycle

Reference lifecycle:

```text
Appraisal Target becomes eligible
        ↓
construct explicit context
        ↓
compute dimensions
        ↓
validate profile
        ↓
staged AppraisalRecord
        ↓
commit
        ↓
future consumers may read it
```

Appraisal computation не должна задним числом мутировать target, Goals, Drives, World Model или Self Model.

---

# 31. Persistence scope

AppraisalRecord является event-level state.

По умолчанию его active cognitive lifetime ближе к decision/cycle/event scope, а не к permanent internal mood.

Historical retention отдельно обеспечивается:

- Evidence Plane;
- trajectory;
- explicit Memory;
- future Affect integration.

Не нужно держать бесконечный список appraisal records в `CognitiveState` только ради истории.

---

# 32. Intervention semantics

Через `Intervention Gateway` допускаются controlled treatments:

- заменить отдельную dimension;
- изменить relevance;
- изменить appraisal конкретного Goal/Drive relation;
- изменить controllability;
- изменить coping potential;
- изменить urgency;
- заменить entire profile control implementation;
- подменить estimator конкретной dimension.

Intervention обязан сохранять:

```text
intervention_id
target AppraisalRecord/dimension
base revision
treatment
provenance
duration/scope
```

Semantic owner остаётся `Appraisal System`, а origin значения становится `intervened`.

---

# 33. Causal specificity

Хороший experiment должен пытаться отличить:

```text
meaningful appraisal effect
```

от:

```text
любое изменение дополнительного числа
или общий OOD corruption
```

Поэтому полезны controls:

- dimension-specific intervention;
- shuffled dimension;
- matched-noise dimension;
- constant profile;
- cross-dimension swap;
- parameter/compute-matched estimator;
- intervention-magnitude controls.

Особенно для learned latent/internal appraisal representations действуют ограничения `DU-06` по OOD/off-target effects.

---

# 34. Failure / degradation

Не использовать hidden fallback:

```text
Appraisal failed
→ output all zeros
→ продолжить как neutral
```

Нужно различать минимум:

```text
available
partial
unknown
unavailable
invalid
failed
stale
incompatible
```

Если обязательная dimension недоступна, scheduler/configured degradation policy решает дальнейшее исполнение.

Optional dimension failure не обязана рушить весь Agent, если contract допускает partial profile.

---

# 35. Revision semantics

Версионируются минимум:

```text
appraisal_system_revision
dimension_schema_revision
estimator/rule revisions
normalization/calibration revisions, если применимо
source model/feature revisions
agent_revision
```

AppraisalRecord, вычисленный до изменения behavior-relevant estimator/Agent capability, остаётся историческим фактом прежней revision.

Его нельзя молча пересчитать и подменить в trajectory.

---

# 36. Snapshot / restore

Если Appraisal implementation stateful, exact Agent Snapshot должен учитывать causally relevant:

- Appraisal System revision;
- dimension schema;
- private estimator state;
- adaptive normalization/calibration state;
- active event/reappraisal state;
- RNG;
- degradation/intervention state.

Event records, уже опубликованные в `CognitiveState` или Memory, восстанавливаются через соответствующих owners.

---

# 37. NoAppraisal, Dummy и Control

## 37.1 NoAppraisal

Appraisal capability отсутствует.

Это не fake neutral profile.

## 37.2 DummyAppraisal

Deterministic engineering implementation для проверки contracts/scheduler.

## 37.3 ControlAppraisal

Research implementations могут включать:

- constant dimensions;
- random/shuffled profiles;
- time-permuted profiles;
- matched-noise profiles;
- goal-only appraisal;
- drive-only appraisal;
- rule-based appraisal;
- parameter/compute-matched control.

Oracle Appraisal, использующий Research Ground Truth, допустим только как privileged research control и не выдаётся за natural capability.

---

# 38. Минимальная reference semantics

`DU-16` **не фиксирует concrete first-version dimensions**, но для design/evaluation наиболее фундаментальными кандидатами считаются:

```text
relevance
goal_congruence
drive_conduciveness
expectedness
controllability
coping_potential
urgency
```

`agency/attribution`, normative compatibility и local polarity являются extension/optional families до отдельного обоснования.

Наличие dimension в этом списке не означает, что первая software version обязана реализовать её learned estimator.

---

# 39. Что Appraisal System запрещено делать

Без нового design decision Appraisal запрещено:

- выбирать action;
- менять Goal Graph напрямую;
- менять Drive State напрямую;
- записывать Memory без `MemoryWriteProposal`;
- превращать prediction/imagination в observed fact;
- использовать evaluator-only Ground Truth natural способом;
- scalarize весь profile в universal utility;
- выдавать emotion label как единственный canonical output;
- хранить hidden persistent Affect state;
- скрыто выполнять Memory retrieval/Cortex invocation;
- считать Intrinsic Signal автоматически appraisal/value;
- выдавать `0` как универсальный neutral/unknown/unavailable;
- переписывать старый AppraisalRecord при reappraisal.

---

# 40. Исследовательский gate отдельного Appraisal System

`Appraisal System` остаётся отдельной responsibility, если можно показать хотя бы часть следующего:

1. при одинаковом target изменение Goal/Drive context предсказуемо меняет Appraisal Profile;
2. dimension-specific interventions дают специфичные downstream effects;
3. meaningful Appraisal превосходит shuffled/random/constant controls;
4. профиль объясняет/поддерживает downstream Affect/Valuation лучше, чем простое добавление extra parameters/context;
5. отдельные dimensions имеют проверяемые operational targets;
6. Appraisal не дублирует полностью Valuation или Intrinsic Signals.

Если будущие эксперименты покажут функциональную избыточность, boundary может быть пересмотрена через ADR.

---

# 41. Что остаётся открытым

До следующих DU намеренно не решены:

- нужен ли отдельный persistent Affect state;
- какие appraisal dimensions первая версия реализует обязательно;
- нужен ли local polarity summary вообще;
- как Appraisal feeds future Affect;
- как Valuation агрегирует Goals/Drives/Appraisal/Affect;
- какие dimensions Salience использует;
- concrete appraisal estimator architecture;
- concrete training labels/objectives;
- human emotion category mapping;
- exact normalization/calibration metrics;
- exact data types/shapes.

---

# 42. Gate завершения DU-16

`DU-16` завершён, если:

- Appraisal Target имеет explicit event/provenance semantics;
- evaluation context revisioned и не ambient;
- actual/predicted/imagined/retrospective appraisal различаются;
- принят multidimensional typed profile без mandatory emotion label/utility scalar;
- relevance, goal congruence, drive conduciveness, expectedness, controllability, coping potential и urgency разведены;
- novelty/surprisal не дублируются скрыто;
- Appraisal отделён от Drives/Affect/Valuation/Salience/Policy;
- reappraisal создаёт новый record, а не переписывает историю;
- partial/unknown/failure semantics explicit;
- intervention/control/snapshot requirements определены;
- конкретная implementation не зафиксирована раньше времени.

После этого разрешается:

```text
DU-17 — Affect Dynamics
```
