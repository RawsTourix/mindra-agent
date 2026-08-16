# Карта проектирования модулей MINDRA

## Статус документа

Этот документ является **картой будущего проектирования**, а не набором уже принятых module contracts.

Он нужен для того, чтобы:

- видеть полный набор архитектурных областей до начала реализации;
- не прятать важную ответственность внутри случайного соседнего модуля;
- проектировать модули в порядке зависимостей;
- заранее планировать ablation/control/replaceability;
- отличать обязательную ответственность системы от конкретного способа её реализации.

Наличие блока в этой карте **не гарантирует**, что он останется отдельным модулем. В ходе соответствующего design update может быть принято решение:

- оставить отдельный модуль;
- объединить ответственность с другим модулем;
- разделить область на несколько модулей;
- сделать механизм algorithmic/rule-based вместо neural;
- отложить область;
- отказаться от неё, если отдельная роль не обоснована.

Главное правило:

> Отдельный модуль существует не потому, что для него есть красивая когнитивная аналогия, а потому что у него есть самостоятельная вычислительная ответственность, явный контракт и независимо проверяемый функциональный вклад.

---

# 1. Классы архитектурных областей

Удобно различать пять групп.

## 1.1 Границы взаимодействия

```text
Environment
Perception / Representation
Cortex
Action / Actuation boundary
```

Они связывают MINDRA с внешним миром, pretrained model и исполняемыми действиями.

## 1.2 Когнитивное состояние и прогнозирование

```text
CognitiveState
Goal System
World Model
Self Model
Memory
Workspace
Metacognitive / Executive Control
```

## 1.3 Мотивация, оценка и регуляция

```text
Intrinsic Signal Providers
Drives
Appraisal
Affect Dynamics
Valuation
Salience / Attention Control
```

## 1.4 Выбор и исполнение поведения

```text
Policy / Planner
Action Gate / Executor
```

## 1.5 Обучение и исследовательская инфраструктура

Это не обязательно когнитивные модули агента:

```text
Experience / Trajectory Recorder
Replay / Consolidation
Training Runtime
Checkpoint / Artifact System
Experiment Runner
MINDRA-Eval
```

Их нельзя смешивать с внутренней психологической интерпретацией агента.

---

# 2. Environment

## Ответственность

Environment определяет внешний мир, в котором агент наблюдает последствия действий.

Для первой исследовательской линии особенно важен контролируемый MicroWorld, позволяющий:

- детерминированно воспроизводить эпизоды;
- клонировать состояние;
- программно менять скрытые правила;
- отделять train/test worlds;
- проводить counterfactual intervention;
- измерять причинный вклад внутренних состояний.

## Не является

Environment не должен решать за агента, что важно, интересно, опасно или полезно, кроме минимального объективного feedback, если он предусмотрен задачей.

---

# 3. Perception / Representation

## Ответственность

Преобразует raw observation в каноническое представление, пригодное для остальных модулей.

Эта область нужна, чтобы World Model, Memory, Policy и другие компоненты не зависели напрямую от случайной формы observation конкретной среды или от hidden size конкретной LLM.

Возможные ответственности:

- нормализация observations;
- encoding structured/raw input;
- canonical feature representation;
- modality metadata;
- uncertainty/missingness representation;
- обратимая связь с provenance исходного observation.

## Ключевой invariant

Canonical representation не должна становиться неявным alias для model-specific hidden state Cortex.

---

# 4. CognitiveState

`CognitiveState` — не когнитивный модуль в обычном смысле, а каноническая граница обмена состоянием.

Он должен определять:

- какие категории state существуют;
- владельца каждой категории;
- read/write permissions;
- временную семантику;
- absence/unknown/stale;
- сериализуемость;
- наблюдаемость;
- совместимость с checkpoint/replay;
- запрет скрытого state между модулями, если он должен быть частью воспроизводимого поведения.

Точное представление будет отдельным design decision.

---

# 5. Goal System

## Ответственность

Отдельно представляет **что агент стремится изменить или сохранить**, не смешивая это с оценкой текущего состояния или выбором действия.

Нужно будет различить как минимум:

- внешне поставленную цель;
- внутренне сформированную цель;
- subgoal;
- active/inactive/completed/failed/abandoned state;
- priority;
- commitment/persistence;
- termination condition;
- конфликт целей;
- связь цели с ожидаемым прогрессом.

## Не является

Goal System не должен автоматически быть Policy и не должен сводиться к scalar reward.

---

# 6. Cortex

## Ответственность

Cortex предоставляет богатые pretrained capabilities, например:

- язык;
- semantic representations;
- general knowledge;
- reasoning/planning candidates;
- интерпретацию natural-language instruction;
- генерацию natural-language output.

## Ключевые свойства

- backend заменяем;
- конкретная model family не является архитектурой MINDRA;
- model-specific hidden state не должен протекать в остальные модули без adapter boundary;
- должны существовать диагностические `DummyCortex`/`NoCortex` режимы;
- Cortex может быть frozen, partially adapted или trainable в зависимости от будущего training design.

---

# 7. Memory Core

## Ответственность

Хранение и retrieval прошлого опыта без преждевременной привязки к механизму эмоциональной значимости.

Нужно будет определить:

- episodic memory;
- необходимость отдельной semantic/procedural memory;
- identity/provenance эпизода;
- indexing/retrieval;
- capacity;
- temporal ordering;
- similarity/relevance semantics;
- deterministic replay compatibility.

## Почему core проектируется отдельно

Если сразу сделать запись/удаление памяти зависимыми от Appraisal/Salience, получится циклический design: Appraisal может требовать Memory, а Memory — уже требовать Appraisal. Поэтому сначала проектируется нейтральный memory substrate, а правила retention/forgetting/consolidation добавляются позднее.

---

# 8. World Model

## Ответственность

Предсказывает динамику внешнего мира и последствия возможных действий.

Потенциальные outputs:

- next-state prediction;
- multi-step rollout;
- outcome features;
- prediction error;
- epistemic/aleatoric uncertainty, если выбранный подход позволяет различать их обоснованно;
- latent imagined trajectory.

World Model не определяет сам по себе, желательно ли предсказанное состояние.

---

# 9. Self Model

## Ответственность

Моделирует функционально значимые свойства самого агента.

Кандидаты:

- probability of success;
- competence;
- uncertainty/calibration;
- resource/cost estimate;
- capability boundaries;
- ожидаемое собственное состояние после действия;
- известные ограничения.

## Не является

Self Model не является текстовым personality profile и не является доказательством самосознания.

---

# 10. Intrinsic Signal Providers

## Ответственность

Формируют **внутренние обучающие/мотивационные сигналы**, выводимые из структуры опыта, а не напрямую задаваемые внешней задачей.

Кандидаты:

- novelty;
- surprise/prediction error;
- information gain;
- uncertainty reduction;
- competence progress;
- state visitation rarity.

Этот слой следует отличать от Drives: signal сообщает о свойстве события, а Drive задаёт контекстную внутреннюю потребность/направление регуляции.

---

# 11. Drives

## Ответственность

Поддерживают внутренние переменные, меняющие относительную ценность состояний и действий во времени.

Design должен определить:

- state dynamics;
- target/range/homeostatic semantics, если применимо;
- update sources;
- saturation/decay;
- interactions между drives;
- различие learned и fixed dynamics;
- связь с goals и valuation.

Ключевой исследовательский критерий:

```text
одинаковое внешнее состояние
+
разное drive state
→
предсказуемо различающееся поведение
```

при контроле off-target effects.

---

# 12. Appraisal

## Ответственность

Оценивает **значение конкретного события или ситуации для текущего агента в текущем контексте**.

Возможные inputs:

- observation;
- goals;
- drives;
- World Model prediction/error;
- Self Model;
- retrieved memories;
- uncertainty;
- actual action outcome.

Возможные outputs могут включать многомерные свойства вроде valence, controllability, goal congruence, novelty, urgency, но точная схема пока не принята.

## Не является

Appraisal не должен незаметно превратиться в ещё один scalar reward model.

---

# 13. Affect Dynamics

## Причина выделения

Appraisal может быть мгновенной оценкой события, но исходная гипотеза MINDRA требует проверить также **сохраняющееся внутреннее состояние**, которое переносит влияние прошлого опыта на последующие решения.

Affect Dynamics — кандидат на отдельный модуль, который может:

- интегрировать appraisal во времени;
- иметь decay/recovery;
- обладать inertia;
- модулировать attention/valuation/policy/learning;
- сохранять контекст между соседними событиями.

## Gate существования

Если отдельная affect state не показывает функционально отличимой роли от Appraisal/Drives, область должна быть объединена, а не сохраняться ради антропоморфной аналогии.

---

# 14. Valuation

## Ответственность

Это центральная область, которой нельзя позволить раствориться внутри Policy.

Valuation должна определять, как decision-relevant ценность строится из нескольких классов информации:

```text
external feedback
intrinsic signals
goal progress
drives
appraisal
affect
predicted future states
risk/uncertainty
```

Нужно развести:

- immediate utility;
- predicted future value;
- vector-valued criteria;
- scalarization, если она вообще нужна;
- state value и action value;
- learned critic и rule-based aggregation.

Именно здесь будет проверяться исходная идея о сложной внутренней системе оценки вместо одного заранее заданного reward.

---

# 15. Salience / Attention Control

## Ответственность

Определяет относительную приоритетность информации и распределение ограниченного cognitive processing.

Возможные downstream effects:

- memory write priority;
- retrieval priority;
- replay priority;
- Workspace admission;
- Cortex/planner compute allocation;
- learning priority;
- event logging detail.

Salience score сам по себе бесполезен, если он ни на что причинно не влияет.

---

# 16. Memory Regulation / Consolidation

Эта область расширяет Memory Core после появления Salience/Appraisal/Valuation.

Нужно определить:

- retention;
- forgetting;
- eviction;
- replay scheduling;
- prioritized replay;
- consolidation;
- transition от episodic опыта к slow learned parameters/representations;
- защита от catastrophic forgetting;
- provenance влияния replay на обучение.

---

# 17. Workspace

## Ответственность

Кандидат на ограниченный интеграционный механизм, через который небольшая часть информации становится временно доступна нескольким downstream-процессам.

Нужно проверить:

- ограниченную capacity;
- competition/gating;
- broadcast/read semantics;
- persistence across ticks;
- consumers;
- intervention;
- отличие от обычного `CognitiveState` и Memory.

## Gate существования

Если Workspace не имеет самостоятельной роли сверх общего state bus, его нельзя сохранять только по аналогии с Global Workspace Theory.

---

# 18. Metacognitive / Executive Control

## Причина выделения

Self Model отвечает на вопрос «что система знает/предсказывает о себе», но не обязательно отвечает на вопрос «как на основании этой информации менять собственный процесс мышления».

Кандидатный Executive Control может управлять:

- решением вызвать Cortex или обойтись без него;
- глубиной planning;
- memory retrieval;
- exploration/exploitation mode;
- computational budget;
- проверкой собственной uncertainty;
- выбором стратегии обучения/адаптации;
- переходом между goal focus.

Это **не** тот же scheduler, что исполняет технический lifecycle модулей. Scheduler обеспечивает детерминированный runtime graph; Executive Control, если будет принят, является частью поведения агента.

## Gate существования

Необходимо доказать, что эта роль не сводится без потерь к Self Model + Policy + Workspace.

---

# 19. Policy / Planner

## Ответственность

Преобразует доступное состояние, прогнозы и ценности в candidate action/plan.

Нужно будет отдельно определить:

- model-free policy;
- model-based planning;
- hierarchical/subgoal planning;
- роль Cortex reasoning;
- использование World Model;
- exploration;
- action distribution;
- deterministic/evaluation mode;
- critic/value coupling.

Policy не должна напрямую владеть всеми остальными механизмами только ради удобства реализации.

---

# 20. Action Gate / Executor

## Ответственность

Отделяет **выбранное действие** от **фактически исполненного действия**.

Эта граница нужна даже в MicroWorld, а особенно важна для будущих внешних инструментов/сред.

Нужно определить:

- validation against action space;
- feasibility;
- safety/constraint hooks;
- action identity;
- dispatch;
- timeout/failure/unknown outcome;
- outcome observation;
- связь action с trajectory record.

Это не должно становиться скрытым вторым Policy.

---

# 21. Learning / Training subsystems

Обучение не является одним когнитивным модулем.

Нужно будет разделить как минимум:

```text
runtime state update
online parameter update
experience collection
offline replay
consolidation
module pretraining
joint training
optional Cortex adaptation
```

Каждая trainable subsystem должна явно сообщать:

- что является target;
- откуда приходит learning signal;
- когда обновляются weights;
- что frozen;
- какие optimizer/checkpoint boundaries существуют.

---

# 22. MINDRA-Eval

MINDRA-Eval — **внешняя исследовательская система**, а не часть когнитивной архитектуры агента.

Она должна уметь:

- собирать baseline matrix;
- выполнять ablation;
- подменять modules control implementations;
- клонировать состояния;
- проводить causal interventions;
- сравнивать Cortex backends;
- выполнять generalization/transfer tests;
- агрегировать seeds;
- хранить experiment evidence.

Нельзя позволять evaluator незаметно давать агенту информацию, которой тот не имел бы в обычном runtime.

---

# 23. Предварительный dependency graph

Это **план проектирования**, а не окончательный runtime graph.

```text
System boundaries
    ↓
CognitiveState / module protocol
    ↓
Environment contract
    ↓
Perception / Representation
    ├──────────────→ Goal System
    ├──────────────→ Cortex boundary
    └──────────────→ Memory Core
                         ↓
               World Model + Self Model
                         ↓
                Intrinsic Signals
                         ↓
                       Drives
                         ↓
                     Appraisal
                         ↓
                  Affect Dynamics
                         ↓
                     Valuation
                         ↓
               Salience / Attention
                  ┌──────┴──────┐
                  ↓             ↓
       Memory Regulation     Workspace
                  └──────┬──────┘
                         ↓
           Metacognitive / Executive Control
                         ↓
                  Policy / Planner
                         ↓
                Action Gate / Executor
                         ↓
                     Environment
```

Фактический runtime почти наверняка будет иметь feedback loops; порядок выше нужен только для того, чтобы **семантика каждого следующего блока опиралась на уже определённые контракты**, а не проектировалась в вакууме.

---

# 24. Правило независимой диагностируемости

Для каждого принятого cognitive module design нужно определить минимум:

- `NoOp`/disabled behavior;
- deterministic или rule-based control, если применимо;
- random/shuffled control, если это meaningful;
- parameter/compute-matched control для learned module, где возможно;
- входы/выходы для logging;
- intervention points;
- checkpoint state;
- module-specific metrics;
- failure/degradation behavior.

Если модуль нельзя отключить без ручного переписывания архитектуры, модульность считается недостаточной.

---

# 25. Правило предотвращения скрытой дубликации

При проектировании каждого нового блока необходимо проверять:

1. Не выполняет ли эту ответственность уже другой модуль?
2. Отличается ли его state от уже существующего state семантически, а не только названием?
3. Есть ли downstream effect, который невозможно выразить существующим контрактом без нарушения его ответственности?
4. Можно ли независимо измерить вклад?
5. Нужен ли отдельный trainable network или достаточно алгоритмического преобразования?

Особенно внимательно проверять пары:

```text
Appraisal ↔ Valuation
Appraisal ↔ Affect
Drives ↔ Intrinsic Signals
Self Model ↔ Metacognition
Salience ↔ Workspace
CognitiveState ↔ Workspace
Goal System ↔ Policy
World Model ↔ Policy critic
Memory ↔ Workspace
Scheduler ↔ Executive Control
```

---

# 26. Следующий шаг

Точный порядок проектирования этих областей задаётся `../documentation-plan.md`.

Первым ещё не спроектированным блоком остаются system context и фундаментальные dependency/runtime boundaries. До их принятия начинать детальный design отдельных когнитивных модулей преждевременно.
