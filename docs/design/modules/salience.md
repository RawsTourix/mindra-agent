# Salience / Attention MINDRA

## Статус документа

**Design Update:** `DU-19 — Salience / Attention`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет `Salience System` MINDRA — agent-owned boundary приоритизации явно предоставленных cognitive targets относительно ограниченного processing/resource budget.

Документ определяет:

- module gate Salience;
- различие relevance, value, salience, attention allocation и Workspace admission;
- `Salience Target` и purpose/context semantics;
- typed `SalienceProfile`;
- bottom-up и top-down evidence без их смешения в universal scalar;
- explicit `AttentionBudget`;
- versioned `AllocationPolicy`;
- ranking/gating/allocation semantics;
- persistence, inhibition, hysteresis и focus continuity;
- границы с Memory, Workspace, Executive Control, Policy и Cortex attention;
- actual/predicted/imagined/intervened provenance;
- observability/intervention;
- `NoSalience`/Dummy/Control configurations;
- snapshot/revision/failure/degradation requirements;
- causal gate, по которому Salience считается функциональным механизмом, а не декоративным score.

Документ опирается на:

- [`../execution-model.md`](../execution-model.md) — logical time и causal provenance;
- [`../cognitive-state.md`](../cognitive-state.md) — committed state/ownership/availability;
- [`../module-lifecycle.md`](../module-lifecycle.md) — staged updates и scheduler semantics;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — passive evidence и controlled intervention;
- [`perception.md`](perception.md) — Canonical Percept;
- [`goals.md`](goals.md) — Goal Graph;
- [`memory.md`](memory.md) — explicit Memory retrieval boundary;
- [`world-model.md`](world-model.md) — prediction/imagination/uncertainty;
- [`self-model.md`](self-model.md) — competence/cost evidence;
- [`intrinsic-signals.md`](intrinsic-signals.md) — novelty/information/surprisal и другие typed signals;
- [`drives.md`](drives.md) — regulatory context;
- [`appraisal.md`](appraisal.md) — relevance/urgency и event-level meaning;
- [`affect.md`](affect.md) — persistent modulation context;
- [`valuation.md`](valuation.md) — decision-relevant value/risk/constraints.

Документ намеренно **не** определяет:

- Memory retention/forgetting/consolidation — `DU-20`;
- Workspace capacity/broadcast — `DU-21`;
- Executive compute strategy — `DU-22`;
- final Policy/Planner — `DU-23`;
- internal Transformer attention конкретного Cortex;
- конкретную neural router architecture;
- конкретную формулу weighted salience;
- exact training objective — `DU-26`;
- exact Python/checkpoint encoding — `DU-27`.

---

# 1. Цель DU-19

К `DU-19` Agent может одновременно иметь множество потенциально значимых объектов:

```text
Percept entities/events
Goals
Memory retrieval results
World hypotheses/predictions
Intrinsic Signals
Appraisal targets
ValueProfiles
candidate plans/actions
```

Но bounded Agent не может одинаково глубоко обрабатывать всё одновременно.

Нужна отдельная ответственность, отвечающая на вопрос:

> «Какие из явно доступных candidates должны получить больший приоритет ограниченного cognitive processing в данном purpose/context?»

Это **не** вопрос desirability.

Можно иметь:

```text
low utility
+
high uncertainty / urgency
→ high processing priority
```

или:

```text
high utility
+
already fully understood / not currently actionable
→ low additional processing priority
```

---

# 2. Module gate

`Salience System` проходит module gate по следующим основаниям:

1. **Самостоятельная ответственность.** Ни Appraisal, ни Valuation не распределяют ограниченный processing budget между разнородными candidates.
2. **Отдельный semantic output.** `AttentionAllocation` описывает приоритет/распределение ресурса, а не meaning/value.
3. **Purpose-dependent semantics.** Один target может иметь разные приоритеты для Workspace, Memory Regulation или дополнительной обработки.
4. **Отдельная causal intervention surface.** Можно изменить allocation при неизменных relevance/value и проверить downstream processing.
5. **Отдельный state возможен, но не обязателен.** Inhibition/focus persistence/habituation могут быть stateful без превращения Salience в Memory/Affect.
6. **Отдельный falsification gate.** Если Salience score не меняет реальное allocation/processing или matched controls дают тот же эффект, boundary должна быть пересмотрена.

Salience **не владеет самим вычислительным ресурсом** и не выполняет consumer action.

---

# 3. Канонические различия

```text
Appraisal relevance
≠
Valuation / Utility
≠
Salience
≠
AttentionAllocation
≠
Workspace admission
≠
Executive compute decision
≠
Policy decision
```

Также:

```text
Intrinsic novelty
≠
Salience

Cortex attention weight
≠
MINDRA Salience

Memory retrieval score
≠
Salience
```

## 3.1 Relevance

Appraisal relation target к текущим concerns Agent.

## 3.2 Value

Decision-relevant desirability/comparison относительно Goals/Drives/cost/risk и других sources.

## 3.3 Salience

Приоритет target для **ограниченного cognitive processing** в конкретном purpose/context.

## 3.4 AttentionAllocation

Конкретное распределение заданного budget между candidates согласно explicit `AllocationPolicy`.

## 3.5 Workspace admission

Будущее решение `DU-21` о том, что реально попадает в ограниченную global-access surface.

Salience может предоставить priority evidence, но не владеет Workspace.

---

# 4. Главное архитектурное решение

MINDRA принимает **typed contextual Salience System с отдельной budgeted allocation boundary**.

Conceptually:

```text
Explicit Candidate Set
        +
Salience Evidence
        +
Purpose / Context
        ↓
   Salience System
        ↓
    SalienceProfile[]
        +
explicit AttentionBudget
        +
versioned AllocationPolicy
        ↓
   AttentionAllocation
```

Нет обязательного:

```text
salience = Σ w_i x_i
```

Нет обязательного:

```text
workspace.add(argmax(salience))
```

Нет обязательного:

```text
if salience > threshold:
    cortex.call(...)
```

Последние два решения принадлежат downstream consumers.

Решение фиксируется `ADR-0019`.

---

# 5. Explicit Candidate Set

Salience не получает ambient право просматривать весь Agent state и самостоятельно искать «что-нибудь интересное».

Consumer/producer предоставляет причинно идентифицируемый набор candidates.

Conceptually:

```text
SalienceCandidateSet
├── candidate_set_id
├── purpose
├── base_state_revision
├── decision/cycle/branch refs
└── SalienceTarget[]
```

Допустимые target families могут включать:

```text
percept entity/event
Goal
MemoryRecord / RetrievalMatch
World hypothesis/prediction
AppraisalRecord
ValueProfile / candidate consequence
candidate plan/action for further processing
other explicit semantic object
```

Salience Target всегда содержит source/provenance reference.

Нельзя передать скрытый Environment Ground Truth как обычный candidate.

---

# 6. Purpose-dependent salience

Salience не является intrinsic property target.

Один target может иметь разные profile/allocation в разных purposes.

Минимальные conceptual purposes:

```text
general_processing
workspace_admission_hint
memory_regulation_hint
retrieval_postprocessing
planning_inspection
executive_attention_hint
context_packing_hint
```

Это не frozen enum.

Пример:

```text
recent catastrophic event

memory_regulation_hint → very high
workspace_admission_hint now → medium
```

Другой пример:

```text
currently urgent Goal cue

workspace_admission_hint → high
long-term retention hint → low/unknown
```

Actual Memory retention остаётся `DU-20`, Workspace admission — `DU-21`, Executive compute allocation — `DU-22`.

---

# 7. SalienceProfile

Канонический intermediate output — typed `SalienceProfile`, сохраняющий evidence decomposition.

Conceptually:

```text
SalienceProfile
├── target_id
├── purpose/context
├── evidence components[]
├── persistence/inhibition context?
├── availability/support
├── salience policy revision
└── provenance
```

Нет обязательного одного `salience_score`.

Profile может включать evidence families вроде:

```text
bottom-up / signal-driven
├── perceptual change
├── novelty
├── predictive surprisal/discrepancy
├── visitation rarity
└── information-related signals

top-down / concern-driven
├── Appraisal relevance
├── urgency
├── Goal relation
├── Valuation/risk/constraint evidence
├── Drive context
├── Affect modulation
├── uncertainty requiring resolution
└── explicit task/focus context
```

`bottom-up` и `top-down` являются полезной functional classification, а не обязательной neural topology.

---

# 8. Evidence не является общей валютой

Например:

```text
novelty = 0.9
urgency = high
risk = tail_probability(...)
relevance = G17-related
```

эти values нельзя молча суммировать.

Каждый component сохраняет:

- semantic kind;
- source identity/revision;
- units/scale;
- normalization state;
- support/confidence, если применимо;
- causal mode.

Если concrete implementation использует weighted score, weight/normalization/policy должны быть explicit и versioned.

---

# 9. Bottom-up и top-down salience

Salience должна допускать конкуренцию двух классов причин:

## 9.1 Signal-driven

Target получает processing priority из-за свойств текущего evidence:

- резкого изменения;
- novelty;
- unexpectedness/surprisal;
- редкости;
- information potential.

## 9.2 Concern-driven

Target получает priority из-за текущих committed concerns:

- active Goal;
- Appraisal relevance;
- urgency;
- risk/constraint;
- current Drive/Affect context;
- explicit cognitive purpose.

Канонически:

```text
high bottom-up salience
≠
high top-down salience
```

AllocationPolicy может учитывать оба типа.

---

# 10. AttentionBudget

`AttentionBudget` — explicit constraint ресурса, предоставляемый downstream consumer/context.

Salience System **не создаёт глобальный budget из воздуха**.

Conceptually budget может выражать:

```text
max_items = K
normalized allocation mass = 1
max context slots
max candidates for deeper inspection
consumer-defined abstract units
```

До `DU-22` Salience не владеет физическими FLOPs, Cortex-call budget или количеством Cognitive Cycles.

Если Executive Control позже задаёт compute budget, Salience может распределять priority внутри явно предоставленного budget, но не менять его самостоятельно.

---

# 11. AllocationPolicy

`AllocationPolicy` преобразует profiles + budget в конкретное распределение.

Допустимые families:

```text
ranking
top-K
threshold/gating
soft allocation distribution
quota / category-aware allocation
weighted scalar policy
learned router
hybrid rule+learned policy
```

Ни одна family не является universal default на architecture level.

Policy обязана иметь identity/revision/config provenance.

---

# 12. AttentionAllocation

Conceptually:

```text
AttentionAllocation
├── allocation_id
├── candidate_set_id
├── purpose
├── budget
├── allocation_policy revision
├── entries[]
├── unused budget?
├── constraint/degradation status
└── provenance
```

Entry может содержать:

```text
target_id
rank?
selected/gated?
allocation share/units?
derived priority score?
reason/source refs
```

Optional `priority score` является **derived policy output**, не canonical meaning самого target.

---

# 13. Ranking, gating и allocation различаются

```text
ranking
→ относительный порядок

gating
→ проходит ли target дальше

allocation
→ сколько ограниченного ресурса получает target
```

Они не обязаны совпадать.

Например первый target по ranking может получить 60% budget, второй 40%, остальные — 0.

Или policy может специально резервировать quota для novelty и Goal-critical targets.

---

# 14. Salience может быть query/context dependent

Один target не имеет вечной global salience.

```text
salience(target | purpose, context, time)
```

— полезная conceptual форма.

Изменение Goal focus, Drive state, Affect, Valuation или available budget может изменить allocation без изменения самого target.

Это создаёт новую Salience/Allocation revision, а не переписывает прошлую запись.

---

# 15. Temporal persistence, inhibition и hysteresis

Полностью stateless salience допустима как baseline.

Но отдельный `Salience System` может иметь causally relevant state для механизмов вроде:

```text
focus persistence
inhibition of return
habituation
hysteresis
refractory interval
recent-selection penalty
```

Это не Memory Store и не Affect.

State предназначен только для динамики приоритизации.

Пример:

```text
target X selected repeatedly
        ↓
inhibition state increases
        ↓
другие candidates получают шанс processing
```

Concrete persistence mechanism не выбран.

---

# 16. Logical time

Salience state изменяется только на explicit logical boundaries.

Запрещено:

```text
GPU stall 10 sec
→ salience decayed
```

если wall-clock не введён как explicit agent-visible semantic input.

Это продолжает `DU-03`.

---

# 17. Appraisal boundary

```text
Appraisal relevance / urgency
→ Salience evidence
```

Но:

```text
relevance
≠
salience
```

Appraisal не распределяет processing budget.

Salience не пересчитывает goal congruence/controllability/coping potential заново.

---

# 18. Valuation boundary

`ValueProfile` может быть source evidence Salience.

Но:

```text
high value
≠
high salience automatically
```

Например высокоценный, но уже полностью решённый вариант может не требовать дополнительного processing.

Также низкоценный/опасный candidate может быть highly salient из-за risk/constraint violation.

Salience не выполняет повторную scalarization ValueProfile и не заменяет ComparisonPolicy.

---

# 19. Intrinsic Signals boundary

Novelty, surprisal, information gain и rarity являются возможными bottom-up evidence.

Но:

```text
IntrinsicSignal magnitude
≠
Salience directly
```

Mapping зависит от purpose/context/policy.

Например noise source может иметь высокий prediction discrepancy, но low information value и быть подавлен allocation policy.

---

# 20. Drives и Affect boundary

Drive/Affect могут модулировать Salience через explicit mapping.

Например:

```text
same perceptual cue
+
different DriveState
→ different processing priority
```

или:

```text
same target
+
different AffectState
→ different allocation tendency
```

Но Salience не мутирует Drive/Affect и не предполагает fixed biological mapping.

Все mappings versioned/intervenable.

---

# 21. Memory boundary

`Memory Core` остаётся owner records/retrieval.

Salience не имеет ambient права искать по Memory.

Допустимые взаимодействия:

```text
RetrievalResult
→ explicit salience ranking/post-processing
```

и позднее:

```text
MemoryWriteProposal / MemoryRecord candidate
+
SalienceProfile
→ DU-20 Memory Regulation
```

При этом:

```text
Salience hint
≠
retention decision
≠
replay priority decision
```

до `DU-20`.

---

# 22. Workspace boundary

Salience может выдавать:

```text
workspace_admission_hint
```

но не решает окончательное admission/capacity/broadcast.

Правильная будущая форма:

```text
Candidates
→ Salience
→ prioritized candidates
→ Workspace admission policy
→ Workspace contents
```

Если Workspace окажется не нужен после `DU-21`, Salience остаётся полезной для других allocation purposes.

---

# 23. Executive Control boundary

Salience говорит:

> «этому candidate стоит уделить больше ограниченного processing».

Executive Control позже решает:

> «вызвать ли Cortex, сделать retrieval, увеличить planning depth, провести verification или ещё один Cognitive Cycle».

Поэтому запрещено:

```text
if salience > 0.8:
    cortex.invoke()
```

как скрытая responsibility Salience.

---

# 24. Policy boundary

Salience может применяться к action/plan candidates **только как priority дальнейшего рассмотрения**, а не desirability/final selection.

```text
action salience
≠
action value
≠
action choice
```

Final action selection остаётся `DU-23`.

---

# 25. Cortex internal attention ≠ Salience

Transformer attention weights, KV routing, sparse attention masks или model-internal head activations являются backend mechanics Cortex.

Они не являются canonical `SalienceProfile` автоматически.

Причины:

- они model-specific;
- могут отсутствовать у remote backend;
- attention weights не обязаны быть faithful measure causal importance;
- их масштаб/семантика меняются между revisions.

Они могут быть diagnostic `Research Probe` или optional evidence только через explicit adapter/validation.

---

# 26. Scheduler boundary

`Cognitive Scheduler` исполняет declared DAG/waves.

Salience не меняет dependency graph и не нарушает scheduler invariants.

Salience allocation может стать **данными** для будущего Executive/Workspace/consumer logic, но не переписывает runtime order скрытым side effect.

---

# 27. Actual / predicted / imagined provenance

Salience target/evidence обязаны сохранять causal mode.

```text
actual percept target
predicted risk target
imagined plan branch
retrieved historical event
intervened target
```

не смешиваются.

Imagined target может быть highly salient **внутри planning branch**, но не должен автоматически вытеснять реальные contents из current processing без explicit bridge policy.

---

# 28. Normalization и competition

Salience сравнивает candidates внутри явного candidate set/purpose.

Нормализация обязана иметь identity/revision/scope.

Нельзя считать:

```text
salience score 0.8 из purpose A
>
salience score 0.7 из purpose B
```

если policy/scales различаются.

Competition может быть:

- global внутри candidate set;
- category-aware;
- quota-based;
- pairwise;
- learned.

Конкретная стратегия не выбрана.

---

# 29. Failure и degradation

Нужно различать:

```text
profile unavailable
profile partial
allocation unavailable
policy unsupported
budget invalid
candidate stale
normalization/revision mismatch
learned router failure
```

Нельзя заменять failure на `salience = 0`.

Explicit degradation может использовать:

- uniform allocation;
- deterministic recency/order baseline;
- configured simplified policy.

Но degradation обязан быть видим в provenance.

---

# 30. NoSalience / Dummy / Control

Необходимо различать:

## `NoSalience`

Salience capability отсутствует.

## `DummySalience`

Детерминированная engineering implementation для тестов.

## `ControlSalience`

Исследовательская замена.

Минимальные controls:

```text
uniform allocation
random allocation
shuffled correct profiles
novelty-only
value-only
urgency-only
recency-only
fixed top-K
matched learned router with shuffled labels/evidence
oracle research control
```

Oracle использует privileged evidence только как explicit research control.

---

# 31. Критерий функциональной роли

Декоративный score не считается доказательством Salience.

Нужен downstream effect:

```text
Salience intervention
→ changed allocation
→ changed actual processing/admission/inspection
→ predicted task/compute effect
```

Минимальный будущий causal test:

```text
same Agent Snapshot
same candidates
same Value/Appraisal/Signals
same budget

Control: correct allocation
Treatment: shuffled allocation
```

Затем измеряется:

- что реально получило processing;
- compute/context usage;
- task outcome;
- retrieval/workspace behavior;
- off-target effects.

Если `Correct ≈ Shuffled/Uniform` на задачах, где priority должна иметь значение, отдельная Salience boundary требует пересмотра.

---

# 32. Observability

Trace должен позволять восстановить:

```text
candidate_set_id
purpose
budget
source evidence refs
SalienceProfile revision
AllocationPolicy revision
ranking/gating/allocation
consumer outcome
intervention/degradation
```

Важно отличать:

```text
high profile salience
≠
actually allocated resource
```

и:

```text
allocated resource
≠
successful downstream processing
```

---

# 33. Intervention

Через `Intervention Gateway` допускаются:

- изменение отдельного Salience component;
- clamp profile;
- изменение persistence/inhibition state;
- замена AllocationPolicy;
- изменение budget;
- swap correct/shuffled allocation;
- принудительный gate target;
- изменение purpose-specific mapping.

Intervention сохраняет semantic owner и получает отдельную provenance.

---

# 34. Snapshot

Если Salience implementation stateful, exact Agent Snapshot включает causally relevant:

```text
Salience system/policy revisions
persistence/inhibition/habituation state
learned router state
normalization state
RNG
last logical update
intervention/degradation state
```

Исторические `AttentionAllocation` records могут храниться в trajectory/evidence и не обязаны быть текущим mutable state.

---

# 35. Rule-based, learned и hybrid implementations

Допустимы:

```text
rule-based profiles + rule-based allocation
learned profile estimator + explicit allocation
explicit profiles + learned router
hybrid system
```

Architecture не требует отдельной neural network.

Первая версия может быть полностью rule-based, если это лучше для диагностируемости.

---

# 36. Что переносится downstream

`DU-19` намеренно оставляет открытыми:

## DU-20

Как Salience влияет на:

- retention;
- forgetting;
- eviction;
- replay selection;
- consolidation.

## DU-21

Как Salience используется для Workspace admission/capacity/broadcast.

## DU-22

Как Executive Control использует salience priorities для реального compute allocation.

## DU-23

Как Policy использует attended/prioritized information при action selection.

---

# 37. Acceptance gate DU-19

`DU-19` считается завершённым, если:

- Salience отделена от relevance/value/Workspace/Executive/Policy;
- target и purpose explicit;
- candidate set не ambient;
- typed evidence сохраняет provenance;
- scalar salience не обязателен;
- budget принадлежит explicit consumer/context;
- allocation policy versioned;
- ranking/gating/allocation различены;
- persistent inhibition/focus state допускается, но не обязательно;
- Memory/Workspace/Executive boundaries не нарушены;
- Cortex attention не объявлено canonical Salience;
- actual/predicted/imagined provenance сохранена;
- предусмотрены `NoSalience`/controls/interventions;
- определён measurable downstream causal gate;
- конкретная neural/formula implementation не зафиксирована.

---

# 38. Следующий шаг

После принятия `DU-19` допускается:

```text
DU-20 — Memory Regulation / Consolidation
```

Теперь Memory Core сможет использовать explicit Salience evidence, не делая Salience скрытой частью самой памяти.
