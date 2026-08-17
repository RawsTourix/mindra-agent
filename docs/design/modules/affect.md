# Affect Dynamics MINDRA

## Статус документа

**Design Update:** `DU-17 — Affect Dynamics`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет persistent history-dependent слой MINDRA — `Affect System`, который интегрирует последовательность `AppraisalRecord` и поддерживает внутреннее состояние, способное создавать временную инерцию и контекстную модуляцию последующей cognition.

Документ определяет:

- module gate отдельного Affect;
- ответственность и ownership `Affect System`;
- различие Appraisal, Affect, Drives и Valuation;
- persistent `AffectState`/typed affect channels;
- appraisal-to-affect update semantics;
- temporal inertia, decay, recovery, accumulation, saturation и hysteresis;
- previous-Affect feedback в будущий Appraisal без instantaneous cycle;
- actual, predicted, imagined, retrospective и intervened source policies;
- baseline/persistence/reset semantics;
- optional low-dimensional affect views;
- границы с Drives, Valuation, Salience, Memory Regulation, Executive Control и Policy;
- rule-based, learned и hybrid dynamics;
- observability/intervention;
- `NoAffect`/Dummy/Control configurations;
- snapshot/failure/degradation requirements;
- критерий, при котором отдельный Affect module должен быть пересмотрен или удалён.

Документ опирается на:

- [`../execution-model.md`](../execution-model.md) — logical time, causal ordering и actual/predicted/imagined provenance;
- [`../cognitive-state.md`](../cognitive-state.md) — committed state, ownership, revision, freshness и availability;
- [`../module-lifecycle.md`](../module-lifecycle.md) — staged updates и atomic commit;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — passive evidence и controlled intervention;
- [`appraisal.md`](appraisal.md) — event-centered `AppraisalRecord`/`AppraisalProfile`;
- [`drives.md`](drives.md) — persistent typed regulatory states;
- [`goals.md`](goals.md) — Goal ownership;
- [`world-model.md`](world-model.md) — prediction/imagination provenance;
- [`self-model.md`](self-model.md) — competence/self-state;
- [`intrinsic-signals.md`](intrinsic-signals.md) — нейтральные свойства опыта.

Документ намеренно **не** определяет:

- человеческие emotion labels как canonical Affect representation;
- обязательные valence/arousal/PAD dimensions;
- Valuation — `DU-18`;
- Salience/Attention — `DU-19`;
- Memory Regulation/Consolidation — `DU-20`;
- Executive Control — `DU-22`;
- Policy/Planner — `DU-23`;
- конкретную neural architecture Affect dynamics;
- exact training objective/loss — `DU-26`;
- exact Python API/checkpoint encoding — `DU-27`;
- наличие субъективных чувств или phenomenal consciousness.

---

# 1. Цель DU-17

После `DU-16` MINDRA умеет оценивать отдельный target относительно текущего контекста Agent:

```text
Event E1 → Appraisal A1
Event E2 → Appraisal A2
Event E3 → Appraisal A3
```

Но без отдельного persistent state два Agent с одинаковым **текущим** Appraisal и одинаковыми Goals/Drives могут быть функционально неразличимы даже при разной недавней истории.

`Affect System` вводит гипотезу:

> недавняя последовательность значимых оценок может оставлять собственное, медленнее меняющееся внутреннее состояние, которое влияет на последующую обработку даже после завершения отдельных events.

Ключевой паттерн:

```text
same current Appraisal
+
same Goal Graph
+
same DriveStateSet
+
different prior AffectState
        ↓
different downstream modulation
        ↓
potentially different future appraisal/value/salience/behavior
```

Это функциональная гипотеза о history-dependent state, а не утверждение о переживаемой эмоции.

---

# 2. Module gate

Отдельный Affect module допустим только если он имеет функциональную роль, не сводимую к переименованию существующих подсистем.

`DU-17` считает module gate **пройденным на design-уровне** по следующим основаниям:

1. **Собственное persistent state.** Affect хранит интегрированный temporal context между отдельными `AppraisalRecord`.
2. **Собственная update boundary.** Новый Appraisal не является новым Affect автоматически; требуется explicit dynamics.
3. **Отдельная causal intervention surface.** Можно изменить Affect при неизменных Goals/Drives/current Appraisal и проверить downstream effect.
4. **Отдельная временная роль.** Affect описывает инерцию/накопление/восстановление appraisal-history, чего отдельный event-level Appraisal не хранит.
5. **Отдельная semantics от Drives.** Affect не обязан представлять регулируемую потребность, deficit или target.
6. **Отдельная semantics от Valuation.** Affect не является action/state utility и ничего не выбирает.

При этом принятие boundary **не означает**, что experiment обязан подтвердить полезность Affect.

Если будущие controlled experiments покажут, что:

- `AffectState` не имеет специфического causal effect;
- тот же результат полностью воспроизводится прямым использованием последнего Appraisal/небольшого history window без отдельного state;
- matched recurrent/history control даёт тот же эффект;

то отдельный Affect module должен быть пересмотрен, объединён с другим механизмом или удалён через новый design review/ADR.

---

# 3. Канонические различия

```text
Appraisal
≠
Affect State
≠
Drive State
≠
Utility / Value
≠
Emotion label
≠
Policy
```

## 3.1 Appraisal

Относится к причинно идентифицируемому target:

> «что это событие означает для меня сейчас?»

## 3.2 Affect State

Persistent summary/modulation state, зависящее от истории appraisals:

> «в каком интегрированном affective context я сейчас нахожусь после недавней последовательности оценок?»

## 3.3 Drive State

Persistent regulatory state конкретного drive:

> «каково текущее состояние моей регуляторной потребности/активации?»

Drive имеет собственную typed semantics и может быть homeostatic/adaptive.

## 3.4 Utility / Value

Будущий decision-relevant механизм оценки состояний/actions/outcomes.

Affect может быть одним из его inputs, но не является готовой utility.

## 3.5 Emotion label

Человеческая/диагностическая интерпретация вроде `fear`, `joy`, `anger`.

Она не является canonical Affect State MINDRA.

---

# 4. Главное архитектурное решение

MINDRA принимает **typed persistent Affect System** с несколькими независимо определяемыми affect channels и optional derived views.

Conceptually:

```text
Committed AffectStateSet A_t
          +
new eligible AppraisalRecord(s)
          +
logical lifecycle/time input
          ↓
      Affect Dynamics
          ↓
 staged AffectUpdateProposal(s)
          ↓
validation / coupling
          ↓
       atomic commit
          ↓
Committed AffectStateSet A_(t+1)
```

Нет обязательного:

```text
affect = "fear"
```

Нет обязательного:

```text
valence = -0.8
arousal = 0.9
```

Нет обязательного:

```text
reward += affect
```

Решение отдельно фиксируется `ADR-0017`.

---

# 5. Почему Affect не является просто Appraisal history

Полный список прошлых `AppraisalRecord` принадлежит historical evidence/Memory/trajectory surfaces.

`AffectState` — **текущее agent-owned состояние**, пригодное для online cognition без обязательного повторного пересчёта всей истории.

Conceptually:

```text
Appraisal history:
A1, A2, A3, ... A1000

Affect State:
compact state S_t = F(history, dynamics, previous S)
```

Конкретная implementation может математически позволять реконструкцию state из history, но это не меняет semantic роли committed Affect в текущем Agent state.

Если Affect implementation является лишь cache без отдельной causal semantics, это должно быть указано как baseline/control, а не выдаваться за самостоятельный механизм.

---

# 6. Typed Affect Channel

MINDRA не фиксирует один universal affect vector.

Каждый affect channel имеет собственную semantic identity.

Conceptually:

```text
AffectChannelDescriptor
├── channel_id
├── channel_revision
├── state semantics
├── source Appraisal dimensions / source policy
├── temporal basis
├── baseline semantics?
├── inertia/decay/recovery semantics?
├── saturation/bounds semantics?
├── coupling declarations?
├── output/modulation semantics
├── stochastic/RNG capability
├── learnable/fixed capability
└── research/control capabilities
```

Примеры потенциальных channel families могут включать интегрированную favorable/adverse tone, activation/tension или другие learned/typed states, но `DU-17` **не принимает конкретный обязательный список**.

---

# 7. Low-dimensional valence/arousal/PAD не являются canonical core

Исторические affect models часто представляют состояние в low-dimensional пространствах вроде:

```text
valence × arousal
```

или:

```text
pleasure × arousal × dominance
```

MINDRA допускает такие representations как:

- конкретную Affect implementation;
- `AffectView` для downstream consumer;
- baseline/control;
- diagnostic mapping.

Но они не являются обязательной канонической геометрией Affect.

Причины:

- человеческие self-report dimensions не обязаны быть оптимальным state для искусственного Agent;
- разные tasks могут требовать разных history-dependent modulations;
- один low-dimensional space может преждевременно смешать разные causal sources;
- `dominance` частично пересекается с уже отдельно спроектированными controllability/coping/self-capability semantics.

---

# 8. AffectStateSet

Канонический published state conceptually:

```text
AffectStateSet
├── affect_system_revision
├── affect_state_set_revision
├── base CognitiveState revision
├── channels by channel_id
├── baseline/context revision
├── last update causal boundary
├── source Appraisal references
├── availability/freshness
└── provenance
```

Каждый channel сохраняет собственную identity и revision.

Нет обязательного общего `overall_affect` scalar.

---

# 9. Temporal dynamics

Affect является persistent, поэтому его состояние зависит не только от текущего target.

Общая семантическая форма:

```text
A_(t+1) = F(A_t, Appraisals_t, Δlogical, context)
```

Это не обязательная математическая equation.

Concrete dynamics может включать:

- inertia;
- exponential/nonlinear decay;
- recovery к baseline;
- accumulation;
- saturation;
- hysteresis;
- asymmetric positive/negative update;
- refractory effects;
- adaptive sensitivity;
- recurrent learned state.

Каждый механизм обязан быть versioned и observable.

---

# 10. Affect time использует logical time

Как и Drives:

```text
GPU latency
network delay
Colab slowdown
```

не изменяют Affect автоматически.

Dynamics может использовать только explicit logical basis, например:

- committed Appraisal event;
- Cognitive Cycle;
- Decision Window;
- Environment Transition;
- Episode boundary;
- Session-level event;
- explicit agent-visible elapsed time, если такой input когда-либо введён.

Hidden background mutation по wall-clock запрещена.

---

# 11. Appraisal → Affect integration

`AppraisalRecord` является основным semantic input Affect.

Affect не должен заново independently вычислять:

- goal congruence;
- drive conduciveness;
- expectedness;
- controllability;
- coping potential;
- urgency.

Иначе `Affect System` начнёт дублировать `Appraisal System`.

Concrete channel объявляет, какие appraisal dimensions/records он использует.

Например, conceptually:

```text
AppraisalRecord A42
├── G17 obstructing
├── urgency high
├── coping potential low
└── expectedness low
        ↓
Affect Dynamics
        ↓
channel-specific state update
```

Mapping является отдельной versioned hypothesis.

---

# 12. Appraisal ↔ Affect temporal feedback

Affect может стать частью контекста **будущего** Appraisal, но instantaneous cycle запрещён.

Правильная форма:

```text
Committed Affect A_t
        ↓
Appraisal computation for target E_t
        ↓
Committed AppraisalRecord R_t
        ↓
Affect update
        ↓
Committed Affect A_(t+1)
        ↓
доступен следующим Appraisal computations
```

Запрещено:

```text
Appraisal_t reads Affect_t
Affect_t reads partially computed Appraisal_t
→ recursive instantaneous loop
```

Если Appraisal implementation использует prior Affect, dependency всегда относится к уже committed предыдущей Affect revision.

Это позволяет исследовать mood/affect-congruent interpretation без нарушения scheduler DAG.

---

# 13. Actual appraisal contribution

Actual committed Appraisal targets являются естественным источником Affect update.

Но даже actual Appraisal не обязан влиять на каждый channel.

Source eligibility и sensitivity определяются concrete dynamics.

Низкая relevance может, например, приводить к negligible update — но такое правило должно быть explicit, а не скрытым hard-coded threshold.

---

# 14. Predicted appraisal и anticipatory affect

Predicted outcome может влиять на **текущее** Affect, если Agent действительно рассматривает prediction как актуальный anticipatory concern.

Это не превращает prediction в факт.

Conceptually:

```text
World Prediction P
→ anticipatory Appraisal AP
→ explicit Affect source policy
→ current Affect update
```

Provenance должна сохранять:

```text
source_mode = predicted
```

Таким образом система потенциально может иметь функциональный anticipatory affect без нарушения `prediction ≠ observation`.

В baseline version predicted contribution может быть отключён.

---

# 15. Imagined appraisal и branch-local Affect

Appraisal внутри World Model imagination **по умолчанию не мутирует реальный committed Affect**.

Правильный pattern:

```text
real Affect A_t
        ↓ clone / branch-local state
imagined Appraisal I1
        ↓
simulated Affect A'_1
        ↓
imagined Appraisal I2
        ↓
simulated Affect A'_2
```

Так Planner/Valuation позже смогут оценивать affective consequences imagined trajectory, не заставляя Agent реально входить в это состояние только потому, что он представил сценарий.

Если future experiment сознательно допускает transfer imagination → real Affect, это должна быть отдельная explicit policy с provenance, а не default semantics.

---

# 16. Retrospective appraisal

Текущее переосмысление прошлого события может менять **текущий** Affect.

Например:

```text
Memory retrieval E_old
→ current Reappraisal R_new
→ current Affect update
```

Это не означает, что Affect в прошлом был другим.

Historical Affect records/snapshots не переписываются задним числом.

---

# 17. Reappraisal

Reappraisal создаёт новый `AppraisalRecord` по `DU-16`.

`Affect System` воспринимает его как новый current causal input согласно source policy.

Если новый appraisal противоположен старому, dynamics может:

- ослабить предыдущее состояние;
- усилить противоположный channel;
- временно сохранить оба следа из-за inertia;
- не изменить Affect, если channel не чувствителен к данной dimension.

Нет обязательного правила «новый appraisal заменяет старую эмоцию».

---

# 18. Affect и Drives

Канонически:

```text
Affect State
≠
Drive State
```

Drive отвечает за persistent regulatory condition конкретного типа.

Affect отвечает за history-dependent integration appraisal trajectory.

Пример различия:

```text
resource Drive pressure = high
```

может сохраняться долго независимо от последних appraisals.

При этом Affect может быстро измениться после серии событий — без изменения самого resource deficit.

Affect не мутирует Drive State.

Если future Drive dynamics использует Affect как explicit input, это потребует явного declared dependency и consistency review; `DU-17` не вводит такую связь автоматически.

---

# 19. Affect и Valuation

Будущий `Valuation` может читать committed Affect как один из inputs:

```text
same predicted outcome
+
same Drives
+
different AffectState
        ↓
potentially different decision-relevant valuation
```

Но Affect не вычисляет:

```text
Q(s,a)
state value
utility(action)
reward
winning option
```

Сам факт негативного/активированного Affect не означает, что действие плохо.

---

# 20. Affect и Salience

Будущий `Salience` может использовать Affect для priority modulation.

Например, одинаковый incoming target потенциально может получить разную processing priority при разном Affect history.

Но Affect сам не выбирает:

- что попадёт в Workspace;
- что будет retrieved;
- что будет consolidated;
- чему выделить compute.

Это остаётся downstream responsibility.

---

# 21. Affect и Memory

Affect не является Memory Store.

`AffectState` не обязан содержать подробную историю событий, вызвавших его.

Однако provenance должна позволять связать update с исходными `AppraisalRecord`.

Будущий `Memory Regulation` может использовать Affect как сигнал для retention/consolidation, но это не реализуется до `DU-20`.

---

# 22. Affect и Goal System

Affect не создаёт committed Goal напрямую.

Если когда-либо affective state должен участвовать в goal generation:

```text
Affect State
→ Goal Proposal source/adapter
→ Goal System
```

Такой механизм пока не принимается автоматически и должен иметь отдельную causal boundary.

---

# 23. Affect и Policy / Executive Control

Affect не выбирает action, coping strategy или compute budget.

Будущие downstream modules могут читать Affect при explicit design.

Нельзя делать:

```text
if affect_negative:
    action = avoid
```

внутри Affect System.

---

# 24. Baseline и persistence

Affect может иметь baseline/recovery state.

Baseline не обязан быть `0` и не обязан означать «нейтральную эмоцию».

Нужно различать:

```text
current Affect State
baseline / attractor state
dynamics parameters
agent-long-lived trait/configuration
```

`DU-17` не вводит personality traits как обязательную часть Affect.

Concrete implementation обязана явно определить scope:

- decision/episode/session persistence;
- что переживает `Environment.reset()`;
- что сбрасывается при новой `Agent Session`;
- что входит в persistent checkpoint.

Default архитектурный invariant:

```text
Environment.reset()
≠
automatic Affect reset
```

---

# 25. Episode boundary

Episode завершение само по себе не означает, что Affect должен исчезнуть.

Возможны policy:

```text
preserve across episodes within Agent Session
reset toward baseline
partial carry-over
explicit reset
```

Выбор является configuration/design property concrete implementation и должен быть частью experiment provenance.

---

# 26. Affect views

Для downstream consumers допускаются derived `AffectView`.

Например:

```text
AffectStateSet
→ ValenceArousalView
```

или:

```text
AffectStateSet
→ learned compact feature view
```

View обязан иметь:

- `view_id`;
- `view_revision`;
- source affect revision;
- mapping/encoder revision;
- provenance.

Derived view не становится source of truth вместо canonical AffectStateSet.

---

# 27. Emotion labels как diagnostic mapping

При необходимости исследовательского сравнения с человеческими datasets допускается:

```text
AffectState/Appraisal trajectory
→ diagnostic emotion mapper
→ label probabilities
```

Но label mapper находится за отдельной research/diagnostic boundary.

Он не определяет внутреннюю архитектуру Agent.

```text
emotion label prediction
≠
functional Affect state
```

---

# 28. Rule-based, learned и hybrid dynamics

Допускаются:

```text
RuleBasedAffect
LearnedRecurrentAffect
HybridAffect
```

Rule-based baseline особенно полезен для первой causal validation, поскольку update semantics легко инспектировать.

Learned implementation может использовать recurrent/state-space architecture, но обязана соблюдать те же owner/provenance/snapshot boundaries.

Cortex не является обязательным для Affect.

Если Cortex помогает классифицировать/интерпретировать appraisal sources, такой вызов должен быть explicit и не даёт Cortex ownership Affect State.

---

# 29. Training и state dynamics

Нужно различать:

```text
runtime Affect update
≠
Learning Update параметров Affect model
```

Например, recurrent hidden state может меняться на каждом event без изменения trainable weights.

Learning parameters/normalizers/baselines позже определяются `DU-26`.

Если Affect model обучается online, новая `agent_revision` не должна смешиваться с in-flight Affect update по правилам `DU-03/05`.

---

# 30. Representation/revision semantics

Если learned Affect representation меняется после model update, нужно различать:

```text
affect_state_revision
affect_model_revision
feature/view revision
agent_revision
```

Нельзя молча интерпретировать hidden state новой модели как совместимый со старой моделью.

При несовместимости требуется:

- reset/reinitialize;
- migration adapter;
- explicit stale/incompatible state;
- другой versioned mechanism.

---

# 31. Failure/degradation

Affect update может завершиться:

```text
success
partial
unavailable
failed
stale-base
incompatible revision
```

При failure предыдущий committed Affect исторически остаётся существующим, но его freshness/status должен отражать, что ожидаемый update не состоялся.

Нельзя молча:

- заменить failure на «neutral Affect»;
- использовать `0` как sentinel;
- продолжить adaptive private state после rejected public commit;
- fallback на Cortex/provider без provenance.

---

# 32. Observability

Минимально полезные evidence:

```text
affect_state_before
affect_state_after
source AppraisalRecord ids
source modes
logical time/boundary
dynamics revision
channel-specific update contributions
baseline/recovery state
saturation/clipping events
availability/failure
intervention provenance
```

Для learned Affect допустимы дополнительные research probes, но они не становятся runtime dependencies.

---

# 33. Intervention

Через `Intervention Gateway` должны быть возможны, где применимо:

- изменить один affect channel;
- clamp channel/state;
- изменить baseline;
- изменить inertia/decay/recovery parameter;
- изменить source eligibility;
- изменить coupling;
- reset конкретный channel;
- заменить dynamics implementation;
- создать branch с другим prior Affect при одинаковом current Appraisal.

Intervention создаёт treatment provenance и не маскируется под natural Affect update.

---

# 34. Ключевой causal experiment

Самая важная проверка самостоятельной роли Affect:

```text
Common Agent/Environment snapshot
same Goals
same Drives
same current Appraisal target/profile
        │
        ├── branch A: Affect State X
        └── branch B: Affect State Y
                    ↓
             downstream cognition
```

Если controlled intervention Affect при прочих равных систематически меняет предусмотренный downstream mechanism, это evidence causal role.

Если эффект исчезает при controls или полностью объясняется hidden difference в Goals/Drives/Appraisal, hypothesis не подтверждается.

---

# 35. Control configurations

Нужно различать:

```text
NoAffect
DummyAffect
ConstantAffect
FrozenAffect
ResetEveryEventAffect
LeakyIntegratorControl
RandomAffect
ShuffledHistoryAffect
TimePermutedAffect
MatchedRecurrentControl
RuleBasedAffect
real learned Affect
```

Особенно важны:

## NoAffect

Отдельной Affect capability нет.

## ResetEveryEventAffect

Использует те же current appraisal inputs, но не переносит state между events.

Проверяет вклад persistence.

## ShuffledHistoryAffect

Сохраняет похожее распределение inputs, но ломает temporal order.

Проверяет вклад реальной последовательности appraisal.

## MatchedRecurrentControl

Имеет сопоставимые parameters/compute/state size, но не получает правильной appraisal semantics.

Проверяет, не объясняется ли эффект просто дополнительным recurrent capacity.

---

# 36. Ablation и отрицательный gate

Будущая evaluation должна уметь сравнить минимум:

```text
full Affect
vs NoAffect
vs ResetEveryEvent
vs ShuffledHistory
vs matched recurrent/history control
```

Сам факт, что full Affect улучшает task score относительно `NoAffect`, недостаточен.

Нужно исключить альтернативы:

- дополнительная parameter capacity;
- дополнительная память;
- дополнительный compute;
- hidden access к прошлым Appraisals;
- случайная корреляция state с Goal/Drive;
- downstream consumer просто использует любое дополнительное число.

Если содержательная temporal semantics не даёт эффекта относительно matched controls, отдельный Affect boundary может быть лишним.

---

# 37. Snapshot

Exact Agent Snapshot должен включать всё causally relevant Affect state:

```text
AffectStateSet
affect_system/channel revisions
baseline/attractor state
private recurrent state
dynamics/coupling parameters or revision refs
adaptive normalization/history state
last logical update
source eligibility state
RNG state
intervention/degradation state
```

Snapshot только published `AffectStateSet` недостаточен, если future behavior зависит от private recurrent/adaptive state.

---

# 38. Research claims

Допустимые формулировки после будущих экспериментов:

> persistent Affect state улучшил определённую history-dependent способность относительно указанных controls.

> intervention Affect channel причинно изменило определённый downstream mechanism при контролируемых условиях.

Недопустимо автоматически заключать:

> Agent испытывает чувство X.

или:

> наличие Affect State доказывает субъективный опыт.

Functional Affect является инженерно-исследовательской конструкцией.

---

# 39. Что намеренно осталось открытым

`DU-17` не выбирает:

- concrete Affect channels;
- обязательный valence/arousal/PAD representation;
- exact dimensionality;
- exact decay/inertia equation;
- exact baseline;
- source weights;
- learned architecture;
- exact coupling;
- episode/session persistence policy первой версии;
- конкретную downstream integration с Valuation/Salience/Memory;
- Affect training objective;
- emotion label mapping;
- Python framework/API.

Эти choices должны быть сделаны позднее на основании version scope и experiment design.

---

# 40. Критерий завершения DU-17

`DU-17` считается завершённым, когда:

- separate Affect module gate сформулирован и принят условно на проверяемой causal hypothesis;
- Appraisal и Affect строго разведены;
- Affect и Drives строго разведены;
- Affect и Valuation строго разведены;
- принят typed persistent state вместо mandatory human emotion taxonomy;
- low-dimensional views оставлены optional;
- определены temporal update и no-instantaneous-cycle semantics;
- actual/predicted/imagined/retrospective source policies разделены;
- defined branch-local imagined Affect;
- определены persistence/reset/snapshot/failure требования;
- определены causal controls и falsification condition;
- принято `ADR-0017`;
- `current.md` переведён на `DU-18 — Valuation`.
