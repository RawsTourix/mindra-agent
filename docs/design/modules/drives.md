# Drives MINDRA

## Статус документа

**Design Update:** `DU-15 — Drives`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет долгоживущий регуляторный слой MINDRA — `Drive System`, который поддерживает внутренние переменные, способные менять относительную значимость одних и тех же событий и состояний во времени.

Документ определяет:

- responsibility и ownership `Drive System`;
- typed drive channels вместо одного global motivation scalar;
- различие `Intrinsic Signal`, `Drive State`, `Drive Pressure`, Goal и Value;
- homeostatic и non-homeostatic/adaptive motivational semantics;
- внутреннюю dynamics drive во времени;
- update sources;
- saturation, decay, recovery и accumulation;
- cross-drive interaction;
- initial conditions и persistence;
- границу `Drive → Goal Proposal`;
- границу `Drive → Valuation`;
- learning/revision semantics;
- observability/intervention;
- `NoDrives`/Dummy/Control configurations;
- snapshot/failure/degradation requirements.

Документ опирается на:

- [`../execution-model.md`](../execution-model.md) — logical time отделено от wall-clock;
- [`../cognitive-state.md`](../cognitive-state.md) — committed state, ownership, provenance и availability;
- [`../module-lifecycle.md`](../module-lifecycle.md) — staged effects и atomic commit;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — passive evidence и intervention разделены;
- [`goals.md`](goals.md) — только Goal System владеет committed Goal Graph;
- [`world-model.md`](world-model.md) — prediction dynamics мира не является desirability;
- [`self-model.md`](self-model.md) — competence/self-state не является Drive;
- [`intrinsic-signals.md`](intrinsic-signals.md) — нейтральные свойства опыта отделены от мотивационной регуляции.

Документ намеренно **не** определяет:

- конкретный обязательный список drives для первой software version;
- Appraisal — `DU-16`;
- Affect Dynamics — `DU-17`;
- Valuation/scalarization — `DU-18`;
- Salience — `DU-19`;
- Policy/Planner — `DU-23`;
- конкретный RL reward;
- exact learning losses/optimizers — `DU-26`;
- exact Python API/checkpoint format — `DU-27`;
- биологическую правдоподобность как обязательное требование.

---

# 1. Цель DU-15

После `DU-14` MINDRA умеет вычислять нейтральные свойства опыта:

```text
novelty = high
information_gain = medium
competence_change = positive
prediction_discrepancy = high
```

Но эти значения сами по себе не говорят:

> «насколько это сейчас важно именно для этого Agent?»

`Drive System` вводит persistent internal state, благодаря которому одинаковое внешнее событие может иметь разное функциональное значение в разные моменты жизни Agent.

Ключевой исследовательский паттерн:

```text
same Environment state
+
same Canonical Percept
+
same committed Goals
+
different Drive State
        ↓
different downstream appraisal/value/goal-pressure
        ↓
potentially different behavior
```

При этом сам `Drive System` **не выбирает действие**.

---

# 2. Канонические различия

```text
Intrinsic Signal
≠
Drive State
≠
Drive Pressure
≠
Goal
≠
Utility / Value
≠
Reward
≠
Policy
```

## 2.1 Intrinsic Signal

Описывает свойство конкретного опыта/изменения знания:

> «событие было новым».

## 2.2 Drive State

Описывает долгоживущее внутреннее регуляторное состояние:

> «текущая потребность в определённом классе регуляции высока».

## 2.3 Drive Pressure

Явное производное от Drive State, показывающее текущую интенсивность регуляторного отклонения/активации **в собственной семантике данного drive**.

`Drive Pressure` не является общей валютой между drives.

## 2.4 Goal

Описывает, чего Agent committed стремится изменить/сохранить.

Drive может стать источником `Goal Proposal`, но не владеет Goal Graph.

## 2.5 Value

Будущий `Valuation` будет определять decision-relevant desirability с учётом drives и других факторов.

Drive сам по себе не является value function.

---

# 3. Главное архитектурное решение

MINDRA принимает **typed stateful Drive System** с единым ownership boundary и независимыми drive channels.

Conceptually:

```text
Intrinsic Signals ───────────────┐
agent-visible internal events ──┤
Goal/outcome evidence ──────────┤
logical time progression ───────┤
explicit regulatory inputs ─────┤
                                ▼
                         Drive System
                  ┌─────────────┼─────────────┐
                  ▼             ▼             ▼
               Drive A       Drive B       Drive C
                  │             │             │
                  └──────┬──────┴──────┬──────┘
                         ▼             ▼
                     DriveStateSet
                         │
              ┌──────────┴───────────┐
              ▼                      ▼
        Goal Proposal path      future Appraisal /
                               Valuation consumers
```

Нет обязательного:

```text
global_motivation = sum(drive.pressure)
```

и нет обязательного:

```text
reward += drive.pressure
```

Решение отдельно фиксируется `ADR-0015`.

---

# 4. Почему нужен общий Drive System

Можно было бы сделать полностью независимые drive-модули без общего владельца.

Это плохо масштабируется, потому что нужны общие invariants:

- stable drive identity;
- atomic update нескольких drives;
- cross-drive coupling;
- initial conditions;
- persistence/reset policy;
- snapshot/restore;
- consistent intervention;
- отсутствие hidden scalarization;
- validation единиц/semantics;
- versioning.

Поэтому `Drive System` является semantic owner общего `DriveStateSet`, а конкретные drive implementations являются заменяемыми компонентами внутри этой boundary.

`Drive System` не является центральным Policy и не получает ambient access ко всему Agent state.

---

# 5. Typed Drive Channel

Каждый drive обязан иметь собственную semantic identity.

Conceptually:

```text
DriveDescriptor
├── drive_id
├── drive_revision
├── dynamics_kind
├── declared update sources
├── persistence scope
├── target/range semantics?
├── pressure semantics
├── bounds/saturation semantics?
├── recovery/decay semantics?
├── coupling declarations?
├── stochastic/RNG capability
├── learnable/fixed capability
└── research/control capabilities
```

Два drive нельзя считать взаимозаменяемыми только потому, что оба представлены числом `0.7`.

---

# 6. Не все drives являются homeostatic

MINDRA не принимает правило:

> «каждая мотивация обязана быть расстоянием до set-point».

Канонически допускаются по меньшей мере две семантические семьи.

## 6.1 Homeostatic Drive

Имеет регулируемую внутреннюю переменную и target/range.

Conceptually:

```text
regulated variable x_t
+
target/range H
        ↓
regulatory deviation / deficit
        ↓
Drive Pressure
```

Например, если когда-либо появится явно спроектированный internal resource/energy variable, такой drive может иметь естественный set-point/range.

Для homeostatic drive target/range является частью канонической semantics и имеет revision/provenance.

## 6.2 Adaptive Motivational Drive

Имеет persistent motivational state, но **не притворяется физиологической переменной с естественным set-point**.

Его dynamics может включать:

- accumulation/deprivation;
- satiation;
- decay;
- recovery;
- habituation;
- sensitivity modulation;
- temporal baseline.

Например, будущая exploration/novelty-related мотивация может оказаться такой системой — но `DU-15` **не принимает конкретный curiosity drive как обязательный**.

Если у drive нет осмысленного set-point, нельзя добавлять фиктивный `target=0.5` только ради единого API.

---

# 7. Drive State и Drive Pressure

`Drive State` может быть структурированным и не обязан быть одним scalar.

Conceptually:

```text
DriveState
├── drive_id/revision
├── state_revision
├── internal regulated state
├── optional target/range
├── optional regulatory deviation
├── pressure/activation representation
├── saturation/recovery state?
├── availability/status
├── last causal update
├── temporal scope
└── provenance
```

`pressure` может быть scalar только если это корректно для конкретного drive.

Даже если несколько drives имеют scalar pressure, эти числа не обязаны быть сопоставимы без будущей Valuation semantics.

```text
curiosity_pressure = 0.8
resource_pressure = 0.8
```

не означает:

> обе потребности одинаково важны.

---

# 8. Динамика во времени

Drive является persistent state, поэтому должен уметь изменяться не только как мгновенная функция последнего signal.

Общая causal форма:

```text
D_t
+
explicit update inputs
+
logical time delta / lifecycle event
        ↓
Drive Dynamics
        ↓
staged D_(t+1)
        ↓
atomic commit
```

Conceptually:

```text
D_(t+1) = F(D_t, inputs_t, Δlogical, context)
```

Это **семантическая форма**, а не обязательная математическая реализация.

---

# 9. Wall-clock не является drive time

В соответствии с `DU-03`:

```text
GPU latency
Colab slowdown
network delay
```

не должны сами по себе повышать «голод», «скука» или другой drive.

Drive dynamics использует только явно определённую logical temporal basis, например:

- Cognitive Cycle;
- Decision Window;
- Environment Transition;
- Episode boundary;
- Session-level event;
- специально определённый agent-visible elapsed-time signal.

Если реальное физическое время когда-либо должно влиять на drive, оно сначала должно стать явным agent-visible input с собственной семантикой.

---

# 10. Drive может меняться без нового внешнего observation

Да.

Например, drive может иметь:

- recovery;
- decay;
- accumulation;
- habituation;
- internal resource drain.

Поэтому отсутствие нового Environment event не означает frozen Drive State.

Но update всё равно происходит только на объявленной causal boundary.

Нельзя запускать hidden background thread, который меняет drive по wall-clock между committed revisions.

---

# 11. Update sources

Drive implementation обязана явно объявлять источники обновления.

Кандидаты:

```text
IntrinsicSignal
agent-visible outcome/event
Goal lifecycle/progress evidence
Self Model evidence
explicit internal resource state
previous DriveStateSet
logical-time/lifecycle event
explicit intervention
```

Это не означает, что любой drive читает всё перечисленное.

Каждый concrete drive получает только declared inputs.

Environment Research Ground Truth и evaluator-only metric не являются normal source.

---

# 12. Intrinsic Signal → Drive

Intrinsic Signals являются **evidence/input**, а не готовым drive pressure.

Например:

```text
novelty = high
```

не определяет автоматически:

```text
curiosity_drive += high
```

В зависимости от semantics конкретного drive высокий novelty может:

- удовлетворять drive и снижать pressure;
- кратковременно повышать activation;
- не влиять на данный drive;
- влиять только вместе с information gain;
- влиять с delay/habituation.

Mapping является частью versioned drive dynamics.

Это позволяет экспериментально проверять разные мотивационные модели без переписывания Intrinsic Signal Providers.

---

# 13. Homeostatic deficit и reward не одно и то же

Homeostatic RL показывает полезную связь между уменьшением regulatory deviation и reward-maximizing behavior.

MINDRA, однако, сохраняет архитектурное разделение:

```text
homeostatic deficit / pressure
≠
RL reward
```

`Drive System` сообщает внутреннее состояние регуляции.

Если позднее `Valuation` или `Training Runtime` использует изменение drive как часть utility/reward objective, это должно быть отдельным explicit design decision.

Так мы не превращаем `DU-15` в преждевременную реализацию `DU-18/26`.

---

# 14. Saturation, bounds и recovery

Concrete drive обязан явно определить, применимы ли:

- lower/upper bounds;
- saturation;
- soft saturation;
- recovery;
- decay;
- hysteresis;
- refractory/satiation interval;
- accumulation rate.

Нельзя молча делать:

```text
pressure = clip(pressure, 0, 1)
```

и считать это универсальной drive semantics.

Если normalization используется только для downstream representation, raw drive state и normalized view должны различаться.

---

# 15. Несколько drives и cross-drive interaction

MINDRA допускает несколько одновременно активных drives.

Они не обязаны быть mutually exclusive.

Conceptually:

```text
DriveStateSet_t
├── A_t
├── B_t
└── C_t
```

На следующем update все drive components читают **одну и ту же committed предыдущую revision**:

```text
DriveStateSet R10
      │
      ├── compute A_next
      ├── compute B_next
      └── compute C_next
                ↓
          validate/couple
                ↓
         atomic Drive commit
                ↓
DriveStateSet R11
```

Так можно выразить взаимное влияние без instantaneous dependency cycle.

---

# 16. Cross-drive coupling

Если state одного drive влияет на dynamics другого, coupling обязан быть explicit.

Недопустимо:

```text
DriveA._state = ...
DriveB читает DriveA._state напрямую
```

Допустимы, например:

- declared previous-revision dependency;
- explicit coupling component/reducer внутри Drive System;
- shared regulatory input с отдельным owner.

Coupling не должен автоматически производить ranking/utility между drives.

---

# 17. Конфликт drives не решается внутри Drive System

Например:

```text
exploration-like pressure = high
resource-preservation pressure = high
```

`Drive System` не обязан решать:

> какой drive «победил»?

Он обязан честно опубликовать оба состояния.

То, как их конфликт влияет на desirability/behavior, относится к `Appraisal`, `Valuation`, `Executive Control` и `Policy` согласно их будущим contracts.

Это сохраняет vector-valued motivational state.

---

# 18. Drive → Goal Proposal

Drive может быть источником нового goal pressure, но не получает direct mutation authority Goal Graph.

Допустимая цепочка:

```text
Drive State
    ↓
drive-specific proposal logic
    ↓
Goal Proposal
    ↓
Goal System
    ↓
accept / defer / reject
```

Например, высокий resource-related drive **может** породить proposal восстановить ресурс.

Но это не означает:

```text
drive.pressure > threshold
→ напрямую создать committed Goal
```

Threshold/proposal logic также является versioned и observable.

---

# 19. Drive → Valuation

Будущий `Valuation` получает Drive State как один из decision-relevant inputs.

Conceptually:

```text
same predicted outcome
+
different DriveStateSet
        ↓
different valuation
```

Но `Drive System` сам не вычисляет окончательное:

```text
utility(action)=...
```

и не scalarize несколько drives.

---

# 20. Drive и Appraisal

`DU-16` сможет использовать Drive State при оценке значения конкретного события.

Например, одно и то же событие может быть appraisal-различным при разном internal regulation state.

Но Drive не должен заранее вычислять все будущие appraisal dimensions вроде valence/urgency/controllability — иначе responsibilities сольются.

---

# 21. Initial conditions

Каждый drive обязан иметь explicit initialization semantics.

Initial state может быть:

- fixed;
- sampled из versioned distribution;
- restored из Agent Snapshot;
- получен из explicit session initialization;
- установлен intervention.

Random initialization требует собственного RNG/provenance.

Нельзя использовать hidden random стартовое давление без фиксации seed/state.

---

# 22. Persistence и reset

`Environment.reset()` не сбрасывает drives автоматически.

Каждый drive объявляет semantic lifetime, например:

- episode-scoped;
- session-scoped;
- agent-long-lived.

Для исходной идеи MINDRA особенно важны drives, которые могут переживать несколько Decision Window и при необходимости Episodes.

Reset policy должна быть explicit и versioned.

---

# 23. Fixed и learned dynamics

Drive implementation может иметь:

```text
fixed/rule-based dynamics
learned dynamics
hybrid dynamics
```

Но `DU-15` не выбирает training objective.

После изменения trainable dynamics:

```text
drive_revision / agent_revision
```

должны позволять определить, какая dynamics породила конкретную trajectory.

Если изменение dynamics меняет interpretation старого state, требуется compatibility/staleness policy.

---

# 24. Natural regulation и external intervention

Нужно различать:

```text
natural Drive update
≠
research intervention
```

Intervention может изменять, например:

- current drive state;
- target/range;
- dynamics parameter;
- coupling;
- sensitivity к определённому input.

Но intervention обязательно проходит через `Intervention Gateway` и имеет treatment provenance.

---

# 25. Causal specificity experiment

Один из основных будущих тестов:

```text
Base Agent Snapshot + Base Environment Snapshot
                │
        ┌───────┴────────┐
        ▼                ▼
     Control          Treatment
  Drive A = normal   Drive A = altered
  Drive B = same     Drive B = same
  world = same       world = same
  goals = same       goals = same
```

Проверяем:

- изменился ли ожидаемый downstream канал;
- остались ли untargeted drives неизменными;
- не возник ли broad corruption;
- сохранился ли effect при нескольких matched contexts;
- исчезает ли effect в `NoDrive`/shuffled controls.

Так мы исследуем причинную роль Drive State, а не просто корреляцию с поведением.

---

# 26. Drive-specific observability

Research evidence должна позволять увидеть минимум:

- base Drive revision;
- update trigger;
- input references;
- state before;
- staged state after;
- committed state after;
- target/range revision, если применимо;
- saturation/recovery/coupling flags;
- intervention provenance;
- failure/degradation.

Heavy private learned state может иметь отдельный Research Probe согласно `DU-06`.

---

# 27. Failure и availability

Если drive нельзя вычислить корректно, запрещено молча возвращать `pressure=0`.

Нужно различать минимум:

```text
available
unavailable
insufficient_input
incompatible_revision
invalid_state
degraded
failed
```

Точные enum names будут определены позже.

Zero pressure является **валидным значением**, а не универсальным sentinel failure.

---

# 28. NoDrives, Dummy и Control

Нужно различать:

## 28.1 NoDrives

Drive capability отсутствует.

Это не fake `DriveStateSet` из нулей.

## 28.2 DummyDriveSystem

Deterministic engineering implementation для lifecycle/integration tests.

## 28.3 Control drives

Возможные research controls:

```text
ConstantDrive
ClampedDrive
RandomDrive
ShuffledDrive
TimePermutedDrive
MatchedNoiseDrive
RuleBasedHomeostaticDrive
```

Контроль обязан сохранять тот же внешний contract, но не притворяться natural learned drive.

---

# 29. Snapshot / restore

Полный Agent Snapshot должен сохранять всё causally relevant состояние Drive System:

```text
DriveStateSet + revision
Drive descriptors/revisions
target/range state
private dynamics state
coupling state
last-update logical time/event
adaptive baselines
RNG state
initialization/reset state
intervention/degradation state
```

Если часть private state не сохранена, exact counterfactual claim недопустим.

---

# 30. Что не является Drive

Следующие вещи сами по себе не становятся drive:

```text
novelty score
prediction error
external reward
Goal priority
Cortex confidence
Self Model P(success)
World Model uncertainty
Memory retrieval score
Appraisal valence
Policy entropy
```

Они могут быть inputs в будущие механизмы при явном design, но смена названия не создаёт самостоятельную регуляторную динамику.

---

# 31. Gate отдельного drive

Каждый предлагаемый drive должен пройти минимум следующие вопросы:

1. Есть ли persistent state, отличимый от входного signal?
2. Есть ли явная dynamics во времени?
3. Имеет ли pressure/regulatory state собственную semantics?
4. Можно ли независимо вмешаться в него?
5. Есть ли downstream effect, который не сводится к простому постоянному reward weight?
6. Можно ли построить `NoDrive`/constant/shuffled control?
7. Нужен ли true homeostatic target или это adaptive drive?
8. Не дублирует ли он Appraisal/Affect/Valuation?

Если ответы не обосновывают отдельную роль, новый drive не добавляется только ради психологической аналогии.

---

# 32. Research hypotheses, которые открывает DU-15

После implementation можно будет проверять, например:

```text
H1:
same external state + different DriveState
→ predictable downstream behavioral difference

H2:
meaningful drive dynamics
> constant/matched-noise drive

H3:
correct drive-specific input mapping
> shuffled signal-to-drive mapping

H4:
Drive effect сохраняется при смене Cortex backend

H5:
persistent Drive State объясняет behavior лучше,
чем мгновенный Intrinsic Signal напрямую
```

Это функциональные hypotheses, а не утверждения о субъективном желании или эмоциях.

---

# 33. Open implementation questions

До version design остаются открытыми:

- какие drives входят в первый vertical slice;
- нужен ли homeostatic resource drive в MicroWorld;
- нужен ли отдельный exploration/curiosity drive;
- exact state dimension каждого drive;
- rule-based или learned dynamics;
- exact target/range functions;
- exact update cadence;
- exact coupling mechanism;
- exact normalization representation;
- concrete Python types;
- concrete training objectives.

Эти вопросы нельзя считать молча решёнными из примеров этого документа.

---

# 34. Итоговые инварианты DU-15

```text
Intrinsic Signal ≠ Drive State
Drive State ≠ Drive Pressure ≠ Value
Drive ≠ Goal ≠ Policy
higher pressure ≠ universally greater desirability
homeostatic drive ≠ mandatory form of every drive
Drive System ≠ global scalar motivation
cross-drive interaction ≠ hidden direct mutation
Environment reset ≠ Drive reset
wall-clock ≠ implicit Drive time
natural regulation ≠ research intervention
```

`Drive System` создаёт persistent regulatory state, но не решает, какое событие «хорошее», какую цель обязательно принять и какое действие выбрать.
