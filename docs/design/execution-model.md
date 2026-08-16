# Временная модель исполнения MINDRA

## Статус документа

**Design Update:** `DU-03 — Runtime / Temporal Model`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет логическую временную семантику MINDRA поверх системных границ из [`system-context.md`](system-context.md) и правил композиции из [`dependency-rules.md`](dependency-rules.md).

Документ намеренно **не** определяет:

- точную структуру `CognitiveState`;
- конкретный `ModuleProtocol`;
- точный порядок отдельных когнитивных модулей;
- конкретный scheduler implementation;
- конкретный Environment API;
- конкретный learning algorithm;
- точный replay-buffer format;
- checkpoint schema;
- конкретные таймауты и численные бюджеты;
- обязательную async-библиотеку или process topology.

Эти вопросы принадлежат последующим Design Updates.

---

# 1. Цель DU-03

`DU-01` определил логические границы системы, а `DU-02` — допустимые зависимости и способ композиции.

`DU-03` отвечает на следующий вопрос:

> в каком причинном порядке живёт MINDRA и к какому моменту времени относится каждое изменение состояния?

После принятия `DU-03` должно быть однозначно понятно:

- чем внешнее время Environment отличается от внутреннего когнитивного времени Agent;
- что является episode, session, decision window и environment transition;
- можно ли выполнять несколько внутренних циклов до одного внешнего действия;
- когда действие считается окончательно выбранным;
- когда результат действия становится частью доступного опыта;
- какие state changes являются обычной runtime-динамикой, а какие — learning/consolidation;
- как online learning может сосуществовать с продолжающимся execution;
- какие temporal identifiers нужны для provenance;
- что означает deterministic/causal replay;
- что происходит при termination, truncation и reset;
- как синхронное и асинхронное физическое выполнение сохраняют одну логическую семантику.

---

# 2. Главное архитектурное решение

MINDRA принимает **иерархическую логическую временную модель с причинно упорядоченными commit boundaries**.

Каноническая временная семантика не определяется:

- wall-clock временем;
- длительностью GPU kernel;
- скоростью Cortex;
- количеством процессов;
- очередностью завершения асинхронных worker;
- физической задержкой сети.

Вместо этого используются логические причинные единицы.

Conceptually:

```text
Run
└── Agent Session
    ├── Episode 0
    │   ├── Decision Window 0
    │   │   ├── Observation ingest
    │   │   ├── Cognitive Cycle 0
    │   │   ├── Cognitive Cycle 1
    │   │   └── Action Commit
    │   │        ↓
    │   │   Environment Transition 0
    │   │        ↓
    │   │   Outcome Commit
    │   ├── Decision Window 1
    │   └── ...
    ├── Episode 1
    └── ...

Отдельные временные линии:
Learning Update 0, 1, ...
Replay Step 0, 1, ...
Consolidation Event 0, 1, ...
```

Это решение дополнительно зафиксировано в `ADR-0003`.

---

# 3. Логическое время и wall-clock

## 3.1. Логическое время

Логическое время отражает причинный порядок событий MINDRA.

Например:

```text
observation O_t
→ internal processing
→ committed action A_t
→ Environment transition
→ outcome O_(t+1)
```

Если Cortex выполнил вычисление за 100 мс или за 10 секунд, это не меняет logical step identity.

## 3.2. Wall-clock

Wall-clock является диагностическим и operational metadata.

Он нужен для:

- latency;
- throughput;
- compute budget;
- timeout diagnostics;
- profiler data;
- сравнения эффективности.

Wall-clock не должен скрыто менять cognition, если только реальное время явно не входит в Environment/task contract.

## 3.3. Реальное время как часть задачи

Если будущая среда моделирует физическое время, deadline или непрерывную динамику, такая информация должна входить в Environment semantics явно.

Нельзя использовать скорость текущего GPU как неявный аналог «времени мира».

---

# 4. Иерархия временных сущностей

## 4.1. Run

`Run` — внешний orchestration-контекст одного запуска, создаваемый `Experiment Runner`.

Он может содержать:

- один или несколько Agent Session;
- training и evaluation phases;
- несколько Environment instances;
- несколько episodes;
- replay/consolidation phases.

`Run` не является частью cognition Agent.

Точная experiment identity schema определяется позднее.

## 4.2. Agent Session

`Agent Session` — непрерывная логическая жизнь конкретного экземпляра Agent от создания/restore до shutdown/замены экземпляра.

Session может переживать несколько Environment episodes.

Следствие:

> `Environment.reset()` не равен полному reset Agent.

Session boundary нужен, чтобы различать:

- новый мир/episode;
- тот же Agent после окончания episode;
- новый Agent из того же checkpoint;
- evaluation clone;
- восстановленный Agent после interruption.

## 4.3. Episode

`Episode` — непрерывная последовательность взаимодействий с одним Environment state после `reset` до `termination` или `truncation`.

Episode принадлежит Environment interaction, а не полной жизни Agent.

## 4.4. Decision Window

`Decision Window` — интервал логического времени после появления agent-visible observation/outcome и до `Action Commit` следующего внешнего действия.

Decision Window может содержать **несколько Cognitive Cycle**.

В step-locked Environment внешнее состояние не обязано продвигаться во время внутренних Cognitive Cycle.

## 4.5. Cognitive Cycle

`Cognitive Cycle` — одна причинно различимая внутренняя итерация обработки доступного состояния до следующей внутренней commit boundary.

Точный состав модулей и scheduler определяются в `DU-05`.

`DU-03` фиксирует только:

- цикл имеет однозначный порядок относительно соседних циклов;
- результаты предыдущего committed цикла могут быть входом следующего;
- несколько циклов могут существовать внутри одного Decision Window;
- количество циклов не равно числу Environment steps.

## 4.6. Action Commit

`Action Commit` — момент, после которого выбранное действие считается окончательным для данного Decision Window и не может быть ретроактивно изменено последующим learning/update.

До Action Commit внутренние кандидаты действий не считаются выполненными внешними действиями.

## 4.7. Environment Transition

`Environment Transition` — причинный переход внешней среды, инициированный committed action или иным contract-defined внешним событием.

Для step-locked исследовательских сред базовая семантика:

```text
Action Commit
→ Environment transition
→ next observation/outcome
```

`environment tick` не принимается как универсальный фундаментальный термин MINDRA, потому что разные среды могут иметь разную физику времени.

## 4.8. Outcome Commit

`Outcome Commit` — момент, когда результат Environment transition зафиксирован как наблюдённый факт конкретной trajectory.

До Outcome Commit prediction остаётся prediction, а не фактическим исходом.

---

# 5. Базовый причинный цикл взаимодействия

Для step-locked среды каноническая логика выглядит так:

```text
Environment reset / previous outcome
          ↓
agent-visible observation
          ↓
Observation Ingest
          ↓
Decision Window opens
          ↓
Cognitive Cycle 0
          ↓
[optional Cognitive Cycle 1..N]
          ↓
Action Commit
          ↓
Action Dispatch
          ↓
Environment Transition
          ↓
Outcome Observation
          ↓
Outcome Commit
          ↓
termination/truncation?
   ├── нет → next Decision Window
   └── да  → Episode closes → explicit reset/new episode
```

Это semantic order, а не обязательный список функций Python.

---

# 6. Несколько внутренних циклов на одно внешнее действие

MINDRA **разрешает** несколько Cognitive Cycle внутри одного Decision Window.

Это необходимо для будущих механизмов:

- iterative reasoning;
- memory retrieval;
- planning;
- repeated Cortex calls;
- workspace competition;
- metacognitive control;
- уточнение uncertainty;
- ограниченное внутреннее simulation/imagination.

При этом:

```text
3 Cognitive Cycle
≠
3 Environment Transition
```

Во внешнем мире step-locked Environment может не пройти ни одного шага, пока Agent думает.

## 6.1. Ограниченность

Decision Window должен иметь конечное termination condition/budget.

Точный механизм задаётся позднее в `DU-05`, `DU-22` и `DU-23`.

Архитектура не должна допускать бесконечный внутренний цикл без observable budget/failure semantics.

## 6.2. Fixed scheduler и Executive Control

На ранних версиях число/порядок внутренних циклов может определяться fixed scheduler.

Будущий `Executive Control` может влиять на продолжение/остановку cognition, но **не переопределяет саму временную семантику**.

То есть learned control может решить:

```text
«нужен ещё один Cognitive Cycle»
```

но не может сделать уже committed action «не случившимся».

---

# 7. Runtime state update и learning update — разные события

Это один из главных temporal invariants.

## 7.1. Runtime state update

Обычная жизнь Agent может изменять внутреннее состояние без optimizer learning.

К потенциальным примерам относятся:

- working state;
- текущие goals;
- drive state;
- affect state;
- counters;
- активная Memory;
- retrieval context;
- текущие estimates/predictions.

Точный ownership полей определяется в `DU-04` и module designs.

Такие изменения являются частью execution semantics.

## 7.2. Learning Update

`Learning Update` — отдельное событие, которое изменяет trainable/learned state согласно явной learning semantics.

К нему потенциально относятся:

- optimizer step;
- gradient update;
- parameter adaptation;
- trainable adapter update;
- иные явно признанные weight/learned-state updates.

Точная граница определяется в `DU-26`.

## 7.3. Почему различие обязательно

Нельзя считать любое изменение памяти или drive «training step».

И наоборот, нельзя скрывать изменение trainable parameters внутри обычного `forward()` и затем считать run frozen.

---

# 8. Online learning

Online learning допустим архитектурно, но должен сохранять causal provenance.

Главное правило:

> Learning Update не может ретроактивно изменить уже committed action или уже записанный outcome.

Conceptually:

```text
Action A_t committed under Agent Revision R_5
Environment outcome recorded
Learning Update
Agent Revision becomes R_6
next action is produced under R_6
```

Если collection и training физически асинхронны, отдельные trajectories могут быть собраны разными revision Agent.

Каждый action/trajectory должен в будущем иметь возможность указать, **какая revision/версия trainable state его породила**.

Точная version schema относится к `DU-25`–`DU-27`.

---

# 9. Replay и Consolidation имеют собственное время

## 9.1. Replay Step

Replay повторно использует ранее записанный опыт.

Replay Step:

- не продвигает Environment Episode;
- не является новым внешним опытом;
- не увеличивает environment-step index исходной trajectory;
- должен сохранять ссылку на source experience.

## 9.2. Consolidation Event

Consolidation — отдельная state-changing maintenance phase.

Она может изменять:

- memory organization;
- learned representations;
- parameters;
- long-term summaries,

если соответствующий будущий design это разрешит.

Consolidation не должна маскироваться под дополнительный Environment interaction.

## 9.3. Imagined/simulated trajectory

Внутреннее воображаемое развитие World Model, если оно появится, не является фактической Environment trajectory.

Должно быть возможно различить:

```text
observed transition
replayed transition
imagined transition
counterfactual branch
```

без анализа содержимого tensors.

---

# 10. Синхронность и асинхронность

MINDRA различает **semantic ordering** и физическую concurrency.

## 10.1. Канонический causal order

На уровне одной trajectory должны существовать однозначные commit boundaries:

```text
observation
< cognition
< action commit
< environment outcome
< next observation-dependent action
```

## 10.2. Допустимая concurrency

Физически могут выполняться параллельно:

- разные Environment workers;
- разные Agent sessions;
- независимые module computations, если scheduler/contracts это разрешат;
- training и collection;
- evaluation и training;
- storage/logging.

## 10.3. Ограничение

Concurrency не должна создавать нефиксируемую неоднозначность причинного порядка.

Если результат зависит от race/interleaving, эта зависимость должна быть:

- явно допустимой semantics;
- наблюдаемой;
- воспроизводимой настолько, насколько practically возможно;
- отмеченной как потенциальный confounder.

## 10.4. Async training и policy lag

Асинхронная collection может использовать слегка устаревшую revision policy/Agent.

Это допустимо только если revision provenance сохраняется и learning algorithm допускает такую семантику.

`DU-03` не решает, какие algorithms допускают lag.

---

# 11. Temporal identities

Будущие data/contracts должны поддерживать идентификацию как минимум следующих уровней:

```text
run_id
agent_session_id
episode_id
decision_id
cognitive_cycle_id
environment_transition_id
learning_update_id
replay_step_id
consolidation_id
agent_revision
```

Точные типы, namespace и serialization определяются позднее.

## 11.1. Требования

Идентификаторы должны позволять:

- восстановить causal ordering;
- различать параллельные sessions;
- не спутать replay с новым опытом;
- сопоставить action с revision Agent;
- строить counterfactual lineage;
- диагностировать reset boundaries.

Один глобальный integer `step` недостаточен.

---

# 12. Episode reset и scope состояния

`Environment.reset()` закрывает/создаёт Episode, но не обязан уничтожать Agent Session.

На temporal уровне различаются будущие state scopes:

```text
cycle-scoped
decision-scoped
episode-scoped
session-scoped
persistent/checkpointed
```

Точные поля относятся к `DU-04`.

## 12.1. Default invariant

Episode reset должен очищать только то состояние, которое canonical design объявляет episode-scoped.

Он не должен автоматически:

- переинициализировать trainable parameters;
- удалять long-term Memory;
- создавать новый Cortex backend;
- сбрасывать session identity,

если experiment/configuration явно этого не требует.

## 12.2. Независимые evaluation episodes

Если эксперимент требует независимых episodes из одного base Agent, Evaluation Runtime должен явно восстанавливать один base snapshot/создавать отдельные sessions, а не полагаться на неявный «полный reset».

---

# 13. Termination и truncation

MINDRA сохраняет различие между:

- **termination** — естественным завершением задачи/состояния в semantics Environment;
- **truncation** — внешним ограничением episode, не эквивалентным terminal state.

Это различие должно сохраняться в experience/evaluation data.

Причина — termination и truncation могут иметь разную learning semantics.

## 13.1. Final outcome before reset

Последний outcome завершившегося episode должен быть зафиксирован **до** reset следующего episode.

Автоматический reset допустим как implementation convenience только если он не уничтожает возможность однозначно восстановить:

- финальное observation;
- termination/truncation reason;
- финальный external feedback;
- episode boundary.

---

# 14. Evaluation-only execution

Evaluation Runtime использует ту же execution semantics Agent, но с отдельной experimental policy относительно learning.

## 14.1. Обычная runtime-динамика

Нельзя автоматически «заморозить всё состояние» Agent, если нормальная архитектура включает:

- memory writes;
- drive dynamics;
- affect dynamics;
- goal updates;
- другие runtime state changes.

Иначе evaluator тестирует уже другую систему.

## 14.2. Trainable updates

По умолчанию clean evaluation не должна выполнять optimizer/parameter Learning Updates.

Если исследуется online adaptation, разрешение learning должно быть явной частью experiment condition.

## 14.3. Cross-episode persistence

Сохраняется ли runtime/persistent state между evaluation episodes, должно быть задано протоколом эксперимента, а не зависеть от convenience autoreset.

Точная evaluation policy относится к `DU-28`.

---

# 15. Causal replay и numerical replay

MINDRA различает два уровня воспроизводимости.

## 15.1. Causal/structural replay

Архитектурная цель:

- тот же исходный snapshot;
- те же recorded external inputs;
- те же controlled interventions;
- тот же logical order;
- те же Agent revisions;
- те же stochastic states/seeds там, где они контролируемы

должны позволять воспроизвести ту же causal trajectory настолько полно, насколько допускают underlying operations.

## 15.2. Numerical/bitwise replay

Bitwise-identical результат **не является универсальным архитектурным обещанием**.

ML framework, hardware, low-precision kernels и platform могут вносить nondeterminism.

Поэтому evidence должно различать:

```text
same causal experiment
vs
bitwise identical execution
```

## 15.3. Determinism profile

Будущая infrastructure должна позволять research/debug profile с максимально строгой детерминированностью там, где это practically возможно.

Точные настройки относятся к `DU-27` и implementation planning.

---

# 16. Counterfactual branching

Temporal model должна поддерживать создание ветки из сохранённой causal boundary.

Conceptually:

```text
State at boundary B
        ├── branch A: internal variable X = x1
        └── branch B: internal variable X = x2
```

Обе ветви должны иметь:

- общий parent boundary;
- отдельную branch identity;
- независимое продолжение temporal identifiers;
- provenance вмешательства.

Точная clone/restore/intervention mechanics определяется в `DU-04`, `DU-06`, `DU-07` и `DU-27`.

---

# 17. Failure и interruption semantics

Физический runtime может завершиться между logical boundaries.

Нужно различать:

- committed causal event;
- partial/uncommitted computation;
- persisted snapshot;
- recoverable state.

Канонический invariant:

> частично выполненный Cognitive Cycle или Learning Update не должен молча считаться committed только потому, что часть вычислений уже произошла физически.

Точный transactional/checkpoint mechanism пока не выбирается.

Для Colab/remote runtime это особенно важно, но правило не зависит от provider.

---

# 18. Векторизованные и параллельные Environment

Параллельное выполнение нескольких environments не создаёт один общий temporal stream.

Каждая trajectory должна сохранять собственные:

- Agent Session identity;
- Episode identity;
- Environment Transition ordering;
- decision/cycle ordering.

Общая batch order не должна использоваться как причинный порядок между независимыми trajectories.

---

# 19. Research evidence, использованное при проектировании DU-03

## 19.1. Environment transition semantics

Gymnasium определяет Environment через явные `reset()` и `step(action)`, причём `step` возвращает новое observation и отдельно `terminated`/`truncated`.

Источники:

- https://gymnasium.farama.org/api/env/
- https://gymnasium.farama.org/main/tutorials/handling_time_limits/

MINDRA не принимает Gymnasium как обязательную зависимость на этом этапе; используется зрелая семантика внешнего transition boundary.

## 19.2. Collection и training могут быть асинхронны

TorchRL collectors поддерживают direct, synchronous multi-worker и asynchronous collection. Документация отдельно предупреждает, что async collection может собирать данные с policy lag.

Источники:

- https://docs.pytorch.org/rl/main/reference/collectors.html
- https://docs.pytorch.org/rl/main/reference/collectors_basics.html

Это является evidence в пользу явного `agent_revision` provenance и разделения logical order от physical concurrency.

## 19.3. Environment/policy execution может быть физически конвейеризировано

TorchRL `AsyncBatchedCollector` разносит environment stepping и inference server, сохраняя при этом per-environment coordinator flow.

Источник:

- https://docs.pytorch.org/rl/main/reference/generated/torchrl.collectors.AsyncBatchedCollector.html

Это подтверждает, что physical concurrency не требует отказываться от причинного порядка отдельной trajectory.

## 19.4. Полная bitwise reproducibility не гарантируется framework

PyTorch официально указывает, что полная воспроизводимость не гарантируется между releases/platforms и даже между CPU/GPU при одинаковых seeds; при этом framework предоставляет deterministic algorithms и средства контроля randomness.

Источник:

- https://docs.pytorch.org/docs/stable/notes/randomness.html

Поэтому MINDRA принимает causal reproducibility как обязательную архитектурную цель, а bitwise reproducibility — как best-effort implementation profile.

## 19.5. Внутренняя temporal abstraction является нормальным классом agent computation

RL-литература по temporally extended actions/options показывает, что внутренние и внешние временные масштабы не обязаны совпадать один-к-одному.

Reference:

- Bacon, Harb, Precup, *The Option-Critic Architecture*, 2016: https://arxiv.org/abs/1609.05140

MINDRA не принимает options framework как свой decision mechanism; работа используется только как evidence того, что temporal abstraction требует явной семантики разных масштабов.

---

# 20. Принятые temporal invariants DU-03

## TM-01

Logical causal time имеет приоритет над wall-clock при описании canonical execution semantics.

## TM-02

`Run`, `Agent Session`, `Episode`, `Decision Window`, `Cognitive Cycle`, `Environment Transition` являются различными временными уровнями.

## TM-03

Один Environment transition может предваряться несколькими Cognitive Cycle.

## TM-04

Cognitive Cycle не продвигает step-locked Environment сам по себе.

## TM-05

Action становится внешним фактом только после `Action Commit`.

## TM-06

Outcome становится фактическим опытом trajectory только после `Outcome Commit`.

## TM-07

Runtime state update и Learning Update являются разными классами state change.

## TM-08

Replay, consolidation и imagined trajectories не увеличивают original Environment step count.

## TM-09

Physical concurrency допустима, но causal order отдельной trajectory должен оставаться однозначным.

## TM-10

Async collection/training требует provenance Agent revision/policy version.

## TM-11

Environment reset закрывает/создаёт Episode, но не равен полному reset Agent Session.

## TM-12

Termination и truncation сохраняются как разные semantics.

## TM-13

Финальный outcome episode должен быть committed до reset следующего episode.

## TM-14

Clean evaluation по умолчанию не выполняет trainable Learning Updates, но сохраняет нормальную runtime-динамику исследуемого Agent.

## TM-15

Causal replay является обязательной архитектурной целью; bitwise replay — best-effort свойство конкретного runtime.

## TM-16

Counterfactual branch должен иметь явный parent/provenance и не смешиваться с original trajectory.

## TM-17

Partial physical computation не считается committed causal event без соответствующей logical commit boundary.

## TM-18

Batch/worker completion order не является причинным порядком независимых trajectories.

---

# 21. Что DU-03 намеренно не решает

Открытыми остаются:

- exact `CognitiveState` versioning;
- immutable snapshot vs mutable state bus;
- module phase ordering;
- exact scheduler graph;
- module lifecycle methods;
- atomic state publication implementation;
- exact environment interface;
- exact action protocol;
- exact number/budget Cognitive Cycle;
- exact Executive Control semantics;
- exact online learning safe-point policy;
- exact parameter/version data types;
- replay buffer implementation;
- checkpoint transactions;
- async framework;
- distributed runtime framework;
- конкретные determinism flags;
- exact wall-clock timeout policy.

Эти вопросы не должны решаться implementation раньше соответствующих DU.

---

# 22. Последствия для следующих Design Updates

## DU-04 — CognitiveState Semantics

Должен спроектировать state так, чтобы каждое значение можно было привязать к логическому моменту и scope:

```text
cycle
decision
episode
session
persistent
```

Также должен поддержать clone/counterfactual и distinguish committed/stale state.

## DU-05 — Module Protocol & Scheduling

Должен определить, как модули исполняются внутри Cognitive Cycle и как результаты публикуются между logical commit boundaries.

## DU-06 — Observability & Intervention

Должен позволить записывать causal events и выполнять intervention в конкретной временной boundary.

## DU-07 — Environment Contract

Должен конкретизировать `reset`, transition, termination/truncation, clone/restore и step-locked semantics MicroWorld.

## DU-25 — Experience / Data / Replay

Должен превратить temporal identities и observed/replayed/imagined distinction в exact trajectory schema.

## DU-26 — Training Lifecycle

Должен определить разрешённые Learning Update safe points и relation с Agent Revision.

## DU-27 — Checkpoint / Reproducibility / Compute

Должен определить persistence logical boundaries, RNG state и deterministic profiles.

---

# 23. Completion gate DU-03

`DU-03` считается завершённым, если для любого будущего state/action/update можно ответить:

1. **На каком логическом временном уровне это произошло?**
2. **Что было committed до этого события и что стало committed после него?**
3. **Продвинулось ли при этом Environment?**
4. **Изменилась ли только runtime-динамика или произошло learning/consolidation?**
5. **Можно ли однозначно восстановить causal parent события?**

После принятия этого документа следующий допустимый Design Update:

```text
DU-04 — CognitiveState Semantics
```
