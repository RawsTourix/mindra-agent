# Lifecycle модулей и scheduling MINDRA

## Статус документа

**Design Update:** `DU-05 — Module Protocol & Scheduling`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет семантический протокол заменяемого модуля MINDRA и правила причинно корректного scheduling поверх:

- [`system-context.md`](system-context.md) — логических границ системы;
- [`dependency-rules.md`](dependency-rules.md) — правил зависимостей и композиции;
- [`execution-model.md`](execution-model.md) — логической временной модели;
- [`cognitive-state.md`](cognitive-state.md) — committed `CognitiveState` и staged update semantics.

Документ намеренно **не** определяет:

- конкретный Python `Protocol`/ABC;
- точные сигнатуры методов;
- окончательную структуру Python packages;
- конкретный scheduler framework;
- `asyncio`, Ray, TorchRL или другой runtime как обязательную технологию;
- concrete `CognitiveState` container;
- точные module-specific `in_keys`/`out_keys`;
- learning algorithms и optimizer API;
- exact checkpoint format;
- exact observability/intervention API;
- конкретное число Cognitive Cycle на Decision Window;
- окончательную роль будущего Executive Control.

Эти решения относятся к последующим Design Updates и version planning.

---

# 1. Цель DU-05

`DU-04` определил, **что** является committed shared state. `DU-05` отвечает на вопрос:

> как независимые модули MINDRA вычисляют новые значения, обновляют собственное causally relevant state и исполняются в причинно однозначном порядке без hidden coupling и partial-state leakage?

После принятия `DU-05` должно быть однозначно понятно:

- что обязан декларировать любой модуль;
- чем module identity отличается от concrete implementation identity;
- как объявляются read/write dependencies;
- как строится execution graph;
- как из DAG формируются параллельные execution waves;
- какую revision читает каждый module compute;
- когда результат становится committed;
- как синхронизируются shared state и module-private state;
- что происходит при module failure или stale result;
- как выражается feedback между модулями без instantaneous cycles;
- как работают disabled/NoOp/Control implementations;
- как batching не смешивает causal lineages;
- где проходит граница между scheduler и будущим Executive Control;
- почему learning/checkpoint/evaluation не превращаются в специальные ad-hoc ветки main loop.

---

# 2. Главное архитектурное решение

MINDRA принимает **contract-declared DAG scheduling с execution waves, snapshot-consistent compute и атомарным commit causally relevant state**.

Каноническая модель одного scheduler segment conceptually выглядит так:

```text
Committed State R10 + Agent Revision A3
                │
                ▼
          Execution Wave 0
        ┌────────┴────────┐
        ▼                 ▼
     Module A          Module B
     reads R10         reads R10
        │                 │
        └── proposed updates ──┐
                              ▼
                       validate / commit
                              ▼
                    Committed State R11
                              │
                              ▼
                       Execution Wave 1
                              │
                           Module C
                         reads R11
                              │
                              ▼
                       validate / commit
                              ▼
                    Committed State R12
```

Модули одной wave:

- читают одну согласованную base revision;
- не видят staged results соседей до commit;
- могут физически выполняться параллельно;
- не зависят от порядка завершения друг друга;
- публикуют только owner-authorized updates.

Следующая wave видит результат предыдущего committed wave.

Это решение дополнительно фиксируется в `ADR-0005`.

---

# 3. Cognitive Scheduler

## 3.1. Роль

`Cognitive Scheduler` — runtime-core механизм MINDRA, который:

- валидирует active module descriptors;
- строит допустимый execution plan;
- определяет ready modules/waves;
- формирует read projections из committed state;
- запускает module computations;
- собирает staged results;
- проверяет write authority и conflicts;
- координирует atomic commit;
- применяет scope/lifecycle transitions;
- обеспечивает causal ordering и failure semantics.

## 3.2. Scheduler не является когнитивным модулем

Scheduler не должен:

- решать задачу Environment;
- определять utility;
- выбирать action за Policy;
- интерпретировать cognition как evaluator;
- иметь скрытую learned policy выбора целей;
- подменять future Executive Control.

Он реализует **механику исполнения уже принятой архитектуры**.

## 3.3. Логическая принадлежность

Scheduler относится к **Agent runtime core** внутри логической границы MINDRA Agent, потому что его правила определяют внутреннюю causal semantics cognition.

`Execution Runtime` может физически хостить/вызывать scheduler, но не должен иметь независимую скрытую scheduling semantics.

Следовательно:

```text
Execution Runtime hosts Agent
        ↓
Agent runtime core owns scheduling semantics
        ↓
Cognitive Scheduler executes module plan
```

Физическое размещение scheduler не меняет эту logical ownership.

---

# 4. Module identity и implementation identity

Для исследовательской заменяемости нужно различать минимум два понятия.

## 4.1. Semantic module identity

Идентичность роли/экземпляра в активной композиции, например conceptually:

```text
world_model
self_model
appraisal
policy
```

Точные identifiers определяются последующими module designs.

## 4.2. Concrete implementation identity

Конкретная реализация этой роли, например:

```text
learned implementation
rule-based implementation
NoOp implementation
control implementation
```

Semantic consumers не должны зависеть от concrete implementation identity.

## 4.3. Provenance

Experiment/runtime evidence должно позволять восстановить, какая implementation была подключена к каждому semantic module identity.

Implementation identity не становится автоматически cognitive input Agent.

---

# 5. Module Descriptor

Каждый активный модуль должен иметь **декларативное semantic description**, достаточное для построения и проверки execution plan.

Exact Python type определяется позднее, но conceptually descriptor содержит следующие классы информации.

## 5.1. Identity/capability

- semantic module identity;
- implementation/provenance identity;
- revision/version contract настолько, насколько нужно для compatibility;
- declared capabilities/optional capabilities.

## 5.2. Reads

Модуль объявляет canonical state paths/namespaces, которые он может читать.

Для read dependency в будущем contract должны быть выразимы как минимум:

- required/optional;
- допустимые availability states;
- freshness requirement;
- semantic temporal relation;
- batch applicability.

## 5.3. Writes

Модуль объявляет canonical paths, которыми он имеет write authority.

Write declaration не даёт права мутировать committed snapshot: она разрешает только сформировать proposed update.

## 5.4. Private state

Модуль объявляет наличие causally relevant private state и его semantic scope/lifecycle.

## 5.5. Lifecycle participation

Модуль объявляет, в каких standardized lifecycle phases он участвует.

## 5.6. Execution traits

Будущий descriptor должен позволять выразить свойства, влияющие на scheduler, например:

- stateless/stateful;
- deterministic/stochastic;
- batch-capable;
- optional/skippable;
- наличие transactional private state;
- resource hints, если они нужны только для physical scheduling.

Конкретный набор traits не фиксируется этим DU.

---

# 6. Declared reads вместо ambient access

Модуль не получает право читать всё `CognitiveState` только потому, что container технически доступен.

Канонический invariant:

> Module compute может зависеть только от state fields, объявленных его active contract.

Scheduler/runtime может передать:

- projection только нужных fields;
- read-only view полного snapshot с enforceable access control;
- другой эквивалентный механизм.

Implementation choice определяется позднее.

Но поведение, зависящее от undeclared field, является architecture violation.

---

# 7. Required, optional и freshness-sensitive reads

Одного списка `in_keys` недостаточно для MINDRA.

## 7.1. Required read

Без применимого значения модуль не может корректно вычислиться.

Если required dependency structurally `missing`, execution plan/configuration invalid.

Если значение `unknown`/`unavailable`/`stale`, допустимость определяется field/module contract.

## 7.2. Optional read

Модуль способен корректно работать без значения и обязан иметь declared semantics его отсутствия.

Optional не означает «молча использовать любой fallback».

## 7.3. Freshness-sensitive dependency

Модуль может требовать, чтобы input был произведён:

- не позднее текущей state revision;
- в текущем Cognitive Cycle;
- после последнего Outcome Commit;
- в текущем Decision Window;
- либо мог использовать предыдущую допустимую revision.

Exact vocabulary freshness constraints определяется contracts позднее.

Главное: dependency на **текущий output другого модуля** должна быть выражена явно и создавать scheduling edge.

---

# 8. Как строится dependency graph

Scheduler строит execution dependency graph из:

1. declared reads;
2. declared writes;
3. freshness/phase requirements;
4. explicit lifecycle constraints;
5. semantic ordering constraints, принятых соответствующими module designs.

Если `Module B` требует current-cycle output `x`, которым владеет `Module A`, возникает edge:

```text
A → B
```

Если B контрактно допускает значение `x` из предыдущей committed revision, same-cycle edge может не требоваться.

Таким образом ordering выводится из **семантики данных**, а не из случайного порядка registration/import/list iteration.

---

# 9. DAG как default execution model

Instantaneous scheduler graph внутри одного plan segment должен быть directed acyclic graph.

Это означает:

```text
A → B → C
```

допустимо, а:

```text
A → B → C → A
```

не может быть неявно исполнено как одна instantaneous dependency chain.

## 9.1. Почему runtime feedback всё равно возможен

Feedback выражается через время:

```text
Cycle N:
A_N → B_N

Cycle N+1:
A_(N+1) читает committed B_N
```

или через явную delayed/stateful boundary.

Следовательно:

```text
feedback over time
≠
instantaneous scheduling cycle
```

## 9.2. Cycle detection

Если active contracts создают instantaneous cycle, composition/execution-plan compilation должна завершиться ошибкой до нормального выполнения.

Scheduler не должен угадывать произвольный порядок и «разрывать цикл как получится».

## 9.3. Iterative algorithm внутри capability

Если конкретный модуль внутренне выполняет iterative search/convergence loop, это может оставаться его private computation, если external contract видит один causally понятный compute/result boundary.

Если iteration требует взаимодействия нескольких semantic modules, нужна отдельная будущая explicit temporal/control semantics, а не скрытая recursion между модулями.

---

# 10. Execution Plan

Active composition должна компилироваться в **Execution Plan** до исполнения соответствующего scope настолько заранее, насколько это возможно.

Plan conceptually фиксирует:

- active modules;
- module descriptors;
- dependency edges;
- lifecycle phases;
- execution waves;
- expected read/write paths;
- optional/disabled semantics;
- failure/degradation policy references;
- compatibility constraints.

## 10.1. Plan validation

До запуска должны обнаруживаться по возможности:

- missing required producer;
- duplicate/ambiguous writer;
- instantaneous cycle;
- impossible freshness requirement;
- incompatible availability semantics;
- unsupported batch mode;
- illegal module capability combination;
- dependency на disabled capability без допустимой degradation semantics.

## 10.2. Plan identity

Execution evidence должна позволять определить, под каким plan/composition выполнялась trajectory.

Точная `plan_revision`/`composition_revision` schema определяется позже.

---

# 11. Execution Waves

DAG делится на **waves** — множества ready modules, которые не требуют current-wave outputs друг друга.

Conceptually:

```text
Wave 0: A, B, C
          │  │
          └──┼────┐
             ▼    ▼
Wave 1:     D    E
              \  /
               ▼
Wave 2:        F
```

## 11.1. Same-base invariant

Все modules одной wave читают одну и ту же committed base `state_revision` и одну закреплённую `agent_revision`.

## 11.2. Completion order не является semantics

Если B физически завершился раньше A, это не даёт B или downstream component права видеть результат раньше общего wave commit.

## 11.3. Physical parallelism optional

Implementation может выполнить wave:

- последовательно;
- thread/process parallel;
- GPU-batched;
- async;
- distributed,

если наблюдаемая causal semantics одинакова.

---

# 12. Proposed Module Result

Module compute не возвращает «новый глобальный state».

Conceptually результат содержит ограниченный набор staged effects, например:

```text
base_state_revision
agent_revision
producer identity
public proposed updates
private-state staged update/reference
status/failure information
causal provenance
```

Точный data type определяется позднее.

## 12.1. Public update

Изменяет только canonical paths, которыми module contract владеет.

## 12.2. Private update

Изменение causally relevant module-private state также должно участвовать в commit semantics.

## 12.3. Operational diagnostics

Profiler/debug information не является автоматически public cognitive update и относится к `DU-06`.

---

# 13. Transactional private state

Это обязательное следствие `DU-04`.

Недопустима ситуация:

```text
module reads R10
→ необратимо меняет private recurrent state
→ public update validation fails
→ CognitiveState остаётся R10
→ private module state уже соответствует условному R11
```

Такой Agent становится внутренне причинно несогласованным.

## 13.1. Канонический invariant

Causally relevant private-state effect module compute должен быть:

- staged до commit;
- либо rollback-able;
- либо получен функционально из committed private base state;
- либо реализован иным способом, гарантирующим atomic semantic visibility вместе с accepted commit.

## 13.2. Pure operational cache

Operational cache разрешено менять отдельно, только если его изменение/потеря **не способно изменить semantic output** при тех же declared inputs/private state.

Если cache влияет на поведение, он не является pure cache и должен учитываться как causally relevant private state.

---

# 14. Wave commit

После завершения всех required computations wave scheduler:

1. собирает proposed results;
2. проверяет base `state_revision` и `agent_revision`;
3. проверяет module status;
4. проверяет write authority;
5. проверяет schema/availability/freshness constraints;
6. проверяет overlaps/conflicts;
7. проверяет transactional private effects;
8. либо атомарно принимает wave effects;
9. либо не публикует их как committed effects.

## 14.1. Atomic semantic visibility

Ни один downstream consumer не видит половину wave commit.

## 14.2. State revision

Если wave содержит semantic public state changes, commit создаёт следующую `state_revision`.

Если public `CognitiveState` не изменился, scheduler не обязан создавать фиктивную новую revision только потому, что прошла compute wave. Однако изменение causally relevant private state должно сохранять собственную идентифицируемую causal provenance/snapshot semantics.

Точная связь private-only commit и state/agent snapshot identity определяется позднее.

---

# 15. Write conflicts

## 15.1. Disjoint writes

Разные модули одной wave могут публиковать disjoint owned paths.

## 15.2. Overlapping writes

Два независимых модуля не должны одновременно писать один canonical path.

Это должно быть обнаружено как invalid plan/commit conflict.

## 15.3. Aggregation

Если значение семантически агрегируется из нескольких источников, должен существовать отдельный semantic owner/reducer.

Предпочтительная модель:

```text
A writes source.a
B writes source.b
        ↓
Reducer module / owner
        ↓
aggregate.value
```

а не scheduler-specific `last-write-wins` или неявный merge.

---

# 16. Stale-base result

Module result относится к конкретной base revision.

Если к моменту commit эта base revision более не является допустимой для данного computation, result считается stale.

Default semantics:

> stale result не rebased и не применяется молча.

Scheduler должен выполнить одну из явно допустимых стратегий:

- discard + recompute на новой revision;
- cancel текущий segment;
- применить специальную contract-defined rebase semantics, если она когда-либо будет доказана безопасной.

Implicit rebase запрещён.

---

# 17. Agent revision pinning

Каждая execution wave выполняется под конкретной `agent_revision`.

Learning Update не должен менять параметры «под ногами» уже выполняющегося module compute так, чтобы result нельзя было однозначно отнести к одной revision.

Минимальный invariant:

```text
wave start
→ pin agent_revision A3
→ all module compute/results belong to A3
→ wave commit/abort
→ только затем допустима activation другой revision согласно будущему DU-26
```

Точная granularity activation Learning Update определяется в `DU-26`, но in-flight computation всегда должно иметь однозначную revision provenance.

---

# 18. Lifecycle phases

MINDRA принимает стандартизированные **lifecycle boundaries**, а не произвольные ad-hoc вызовы конкретных module classes из main loop.

Conceptually различаются:

```text
composition / validation
agent-session start
episode start
observation/outcome ingress
Decision Window start
Cognitive Cycle compute
Action Commit boundary
Outcome Commit boundary
post-outcome processing
Decision Window end
episode end/reset
agent-session end
snapshot/restore boundary
shutdown
```

Точные hook names определяются exact contracts позднее.

## 18.1. Не каждый модуль реализует каждый hook

Универсальный giant interface с десятками обязательных no-op methods не требуется.

Модуль должен декларативно указывать только lifecycle capabilities, которые ему действительно нужны.

## 18.2. Scheduler owns dispatch semantics

Модуль не подписывается динамически на глобальный event bus и не вызывает lifecycle peers самостоятельно.

Active plan заранее знает, какие handlers/capabilities участвуют в конкретной boundary.

---

# 19. Initialization

Initialization должна привести active Agent composition к состоянию, где:

- descriptors валидированы;
- required private state инициализирован;
- canonical schema совместима с composition;
- required fields не находятся в structural `missing`;
- optional unavailable capabilities представлены явно;
- execution plan может быть построен.

Initialization не должна скрыто выполнять training только ради того, чтобы module contract стал валидным.

---

# 20. Scope transitions и reset

`DU-04` ввёл scopes:

```text
cycle
decision
episode
session
agent-long-lived
```

Scheduler/lifecycle coordinator обязан применять expiration/reset **по semantic scope**, а не методом «очистить всё».

## 20.1. Episode reset

При `Environment.reset()`:

- episode-scoped state завершается/переинициализируется по contract;
- session-scoped/private state сохраняется, если contract не говорит обратное;
- long-lived state не уничтожается автоматически.

## 20.2. Private-state reset

Модуль обязан объявить reset semantics causally relevant private state.

## 20.3. Scope transition — committed event

Если reset/expiration меняет canonical state, это изменение должно проходить через обычную state commit semantics, а не через скрытую очистку container после commit.

---

# 21. Outcome processing

После `Outcome Commit` модули, которым contract разрешает реагировать на outcome, участвуют в стандартизированной post-outcome phase через тот же scheduler/state mechanism.

Не допускается отдельный ad-hoc путь:

```text
main_loop вручную вызывает
memory.remember(...)
drives.update(...)
appraisal.observe(...)
```

для каждого нового модуля.

Иначе архитектура снова станет централизованным набором специальных вызовов.

Конкретные outcome fields и owners появятся после `DU-07` и module designs.

---

# 22. Runtime update ≠ Learning Update

Нормальная module lifecycle может менять:

- canonical runtime state;
- module-private runtime state;
- Memory state;
- другие agent-owned non-parameter states,

не выполняя gradient/optimizer learning.

`Learning Update` остаётся отдельной boundary из `DU-03`.

## 22.1. Scheduler не является trainer

Cognitive Scheduler не должен универсально вызывать `learn()` после каждого module compute.

Training Runtime находится вне Agent boundary и будет использовать отдельные training capabilities/contracts, определяемые в `DU-26`.

## 22.2. Trainable module

Факт, что module содержит trainable parameters, не меняет его runtime compute contract.

## 22.3. Online adaptation

Если будущий модуль выполняет genuinely online parameter update как часть исследуемой architecture, это всё равно должно быть оформлено как explicit `Learning Update` с revision boundary, а не скрытая mutation внутри `compute()`.

---

# 23. Execution/evaluation mode

Нужно различать:

```text
experiment role
framework neural mode
learning permission
cognitive runtime state
```

## 23.1. Evaluation label не является input

Модуль не должен менять cognition только потому, что прочитал глобальный `is_evaluation=True` из experiment config.

## 23.2. Behavior-affecting framework mode

Если `train()/eval()` конкретной neural library меняет dropout, normalization или другой output behavior, выбранный режим является частью execution provenance/Agent revision semantics.

## 23.3. Learning permission

Evaluation может запрещать optimizer updates, сохраняя нормальные runtime state dynamics.

Точная training/evaluation policy определяется `DU-26`/`DU-28`.

---

# 24. Stochastic modules

Stochastic behavior допустим, но randomness является causally relevant state/input.

Модуль не должен полагаться на неидентифицируемый process-global RNG так, чтобы:

- retry неожиданно давал другую semantics;
- counterfactual fork нельзя было воспроизвести;
- batch reorder менял unrelated trajectories.

Exact RNG ownership/state contract относится к `DU-27`, но module descriptor должен позволять позднее классифицировать stochastic module.

---

# 25. Failure semantics

Default policy MINDRA — **fail explicit, commit nothing partial**.

Если required module в wave завершился ошибкой до commit:

- его staged public/private effects не становятся committed;
- успешные staged effects той же atomic wave также не публикуются как частичный wave state;
- failure сохраняется в observability/evidence;
- дальнейшее действие определяется explicit failure policy.

## 25.1. Допустимые будущие policy

В зависимости от module contract/config могут быть разрешены:

- fail run/session/episode;
- retry относительно той же base revision;
- recompute относительно новой base revision;
- explicit degradation to `unavailable`;
- переход на заранее сконфигурированную fallback implementation.

Но поведение обязано быть заявлено до события и наблюдаемо.

## 25.2. Hidden fallback запрещён

Недопустимо:

```text
Memory упала
→ Policy сама незаметно спросила Cortex
→ experiment продолжился как будто ничего не произошло
```

## 25.3. Timeout

Wall-clock timeout является operational failure condition, а не автоматически прошедшим cognitive time.

---

# 26. Retry semantics

Retry не должен создавать скрытую новую causal историю.

Нужно сохранять как минимум conceptually:

- original base revision;
- attempt identity;
- stochastic state/retry policy;
- reason первого failure;
- был ли computation повторён полностью.

Если retry resamples randomness, это должна быть explicit semantics, а не случайный побочный эффект повторного вызова.

Exact observability определяется `DU-06`.

---

# 27. Disabled module

`disabled` означает, что semantic module/capability не входит в active execution plan.

## 27.1. Required dependency

Если другой active module требует его capability и не поддерживает отсутствие, composition invalid и должна fail-fast.

## 27.2. Optional capability

Если отсутствие допустимо, принадлежащие capability значения должны иметь contract-defined `unavailable` semantics, а не structural `missing`.

Инициализация этой unavailable state может принадлежать schema/composition boundary, а не «несуществующему модулю».

---

# 28. NoOp implementation

`NoOp` — активная concrete implementation того же semantic contract, используемая для baseline/ablation.

NoOp обязана:

- соблюдать declared reads/writes;
- не обращаться к hidden peers;
- выдавать contract-valid neutral/unknown/unavailable result согласно design;
- сохранять lifecycle compatibility;
- быть отличимой в provenance;
- не получать специальных преимуществ через main loop.

NoOp не должна быть хаотичным набором `if disable_x` по потребителям.

---

# 29. Control implementation

Control implementation используется для исключения альтернативных объяснений эффекта.

Например, позднее это может быть:

- random control;
- parameter-matched control;
- shuffled control;
- rule-based control.

Она подключается той же Composition Root/scheduler semantics, что и target implementation.

Evaluator/Agent не должен получать experiment label «это контрольная группа» как cognitive feature.

---

# 30. Parallel compute safety

Два module computations могут находиться в одной wave только если scheduler доказал отсутствие same-wave causal dependency и incompatible write/private-state conflict.

Минимально требуется:

- same committed base state;
- fixed agent revision;
- disjoint canonical writes либо отсутствие public writes;
- независимое private-state ownership;
- отсутствие undeclared shared mutable resource, влияющего на semantics.

Если два модуля физически используют один GPU/lock/provider, это resource scheduling concern и само по себе не создаёт cognitive dependency.

---

# 31. Structured concurrency как implementation possibility

Concrete runtime может использовать structured concurrency, при которой группа tasks запускается совместно, ожидается как единая scope и при failure корректно отменяет siblings.

Это хорошо соответствует atomic wave failure semantics, но **конкретный `asyncio.TaskGroup` или другой framework не является canonical requirement**.

Architecture требует свойства, а не библиотеку.

---

# 32. Batch/vectorized execution

Batching не меняет semantic module protocol.

## 32.1. Homogeneous batch

Несколько независимых Agent Sessions могут исполнять один compatible plan векторизованно.

Каждый batch element сохраняет собственные:

- state revision/lineage;
- episode/decision identities;
- availability masks;
- RNG/private state;
- failure/termination status.

## 32.2. Asynchronous episode endings

Termination одного batch element не должен автоматически reset/advance остальные.

Scheduler должен поддерживать per-item activity/reset masks либо безопасное split/rebatch.

## 32.3. Divergent control flow

Если future Executive Control создаёт разные числа cognitive cycles/eligible modules по batch elements, implementation может:

- маскировать inactive items;
- regroup/split batch;
- выполнять отдельные plans,

но не объединять causal lineages.

---

# 33. Fixed Scheduler и будущий Executive Control

На текущем уровне scheduler отвечает за **допустимую механику**, а не за learned metacognitive choice.

Conceptually:

```text
Scheduler defines:
- какие dependencies обязательны
- какой module сейчас ready
- что можно commit
- что нарушает contracts

Future Executive Control may influence:
- нужен ли ещё Cognitive Cycle
- какой optional capability запросить
- сколько compute budget выделить
- какую допустимую ветвь processing выбрать
```

Executive Control не сможет:

- обходить ownership;
- читать undeclared state;
- создавать instantaneous dependency cycles;
- подменять committed history;
- запускать concrete peer напрямую;
- bypass commit validation.

Точная boundary определяется `DU-22`.

---

# 34. Запрет recursive peer execution

Cognitive module не должен самостоятельно выполнять:

```text
other_module.compute(...)
scheduler.run_module("memory")
registry.resolve("cortex").generate(...)
```

чтобы динамически расширить cognition.

Если модулю требуется результат другой capability:

- dependency выражается через state contract;
- scheduler строит edge/wave;
- либо future control mechanism формирует explicit scheduling intent через каноническую boundary.

Это продолжает запрет Service Locator из `DU-02`.

---

# 35. External provider calls

Модуль может использовать собственный injected backend/provider в пределах своей capability boundary, например future Cortex adapter.

Но provider call не даёт модулю право:

- публиковать чужие namespaces;
- обходить scheduler commit;
- получать evaluator-only data;
- мутировать peer private state.

Внешний provider response считается частью module computation и получает соответствующую provenance.

---

# 36. Irreversible side effects

Обычный cognitive module compute не должен совершать irreversible causally visible side effect **до успешного commit**, если этот effect нельзя согласовать/rollback.

Примеры потенциально опасных side effects:

- irreversible Memory storage mutation;
- отправка внешнего action;
- изменение внешней среды;
- необратимое изменение persistent private state.

`Action dispatch` специально вынесен в `DU-24` и не маскируется как обычный module write.

Для storage-backed modules конкретный design должен обеспечить staging/idempotency/transactional semantics либо другую доказуемо согласованную модель.

---

# 37. Snapshot/restore boundary

`DU-05` не определяет checkpoint format, но фиксирует lifecycle requirement:

> causally relevant module-private state должно быть snapshot/restore-able либо детерминированно реконструируемо из состояния, которое входит в snapshot.

Snapshot не должен фиксировать Agent посередине незавершённой wave как будто это обычный committed state.

Предпочтительная semantic boundary — quiescent committed point, где:

- нет half-applied wave;
- known active state revision;
- known agent revision;
- private state согласовано с public commit.

Exact checkpoint coordination определяется в `DU-27`.

---

# 38. Shutdown

Shutdown является lifecycle boundary, а не когнитивным событием сам по себе.

Модуль может освобождать operational resources:

- handles;
- workers;
- device allocations;
- provider sessions;

но shutdown не должен скрыто выполнять behavior-changing learning/consolidation, если это не было отдельной explicit phase.

---

# 39. Research/evaluation implications

`DU-05` создаёт основу для будущих проверок:

## 39.1. Scheduler determinism

При одинаковых descriptors/dependencies/base revisions plan должен строиться одинаково на semantic уровне.

## 39.2. Order invariance внутри wave

Перестановка физического completion order независимых modules не должна менять committed result.

## 39.3. Atomic failure test

Failure одного required module не должен оставлять partial public/private commit соседей wave.

## 39.4. Stale result test

Result с недопустимой base revision не должен применяться молча.

## 39.5. Cycle detection

Instantaneous dependency cycle должен обнаруживаться до normal execution.

## 39.6. NoOp/control substitutability

Подмена implementation не должна требовать изменений независимых consumers/main loop.

Точный evaluation harness появится в `DU-28`, engineering tests — в `DU-29`.

---

# 40. Evidence из существующих инструментов

`DU-05` не выбирает конкретный framework, но существующие инструменты подтверждают реализуемость принятой модели.

## 40.1. Declared input/output keys

TorchRL/TensorDict modules уже используют `in_keys`/`out_keys` как явное описание читаемых и записываемых данных.

Источники:

- https://docs.pytorch.org/rl/stable/tutorials/getting-started-1.html
- https://docs.pytorch.org/rl/stable/reference/generated/torchrl.modules.tensordict_module.SafeModule.html

Это является evidence, что declarative state dependencies практичны, но MINDRA требует более богатой семантики freshness/availability/ownership.

## 40.2. DAG/topological scheduling

Стандартная библиотека Python предоставляет `graphlib.TopologicalSorter`, включая получение ready tasks для потенциально параллельного выполнения.

Источник:

- https://docs.python.org/3/library/graphlib.html

NetworkX также предоставляет `topological_sort` и `topological_generations`, где generation содержит узлы, чьи ancestors находятся в предыдущих generations.

Источники:

- https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.topological_sort.html
- https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.topological_generations.html

Это подтверждает, что wave plan не требует разработки нового graph algorithm с нуля.

## 40.3. Functional module execution

PyTorch `torch.func.functional_call()` позволяет выполнять module с явно переданными parameters/buffers вместо обязательной mutation самого module object.

Источник:

- https://docs.pytorch.org/docs/stable/generated/torch.func.functional_call.html

Это показывает реализуемость functional/staged approaches для части module state, но не является обязательным механизмом MINDRA.

## 40.4. Structured concurrency

Python `asyncio.TaskGroup` предоставляет structured task scope и cancellation siblings при failure одного task.

Источник:

- https://docs.python.org/3/library/asyncio-task.html#task-groups

Это потенциально удобно для physical wave execution, но конкретный async framework не принят.

---

# 41. Принятые invariants DU-05

## MP-01

Все cognitive modules исполняются через единый scheduler/lifecycle semantics, а не ad-hoc вызовы из main loop.

## MP-02

`Cognitive Scheduler` принадлежит Agent runtime core, но не является когнитивным модулем.

## MP-03

Module dependencies декларируются; ambient/undeclared state access является нарушением архитектуры.

## MP-04

Instantaneous execution dependency graph является DAG; feedback loops выражаются через logical time/state revisions.

## MP-05

Ordering выводится из contracts/freshness/phase constraints, а не registration order.

## MP-06

Ready modules группируются в execution waves; все modules одной wave читают одну base `state_revision` и `agent_revision`.

## MP-07

Physical completion order внутри wave не влияет на semantic result.

## MP-08

Module compute не мутирует committed `CognitiveState` напрямую.

## MP-09

Causally relevant module-private state участвует в transactional commit semantics и не может опережать failed public commit.

## MP-10

Wave effects становятся видимыми atomically; partial commit required wave запрещён.

## MP-11

Overlapping canonical writers запрещены без отдельного semantic reducer/owner.

## MP-12

Stale-base result не применяется и не rebased молча.

## MP-13

In-flight wave pinned к одной `agent_revision`.

## MP-14

Lifecycle boundaries стандартизированы; module-specific special calls из central loop запрещены.

## MP-15

Runtime state update не является Learning Update; Cognitive Scheduler не является trainer.

## MP-16

`disabled`, `NoOp` и `Control` имеют разные явные semantics и используют обычную composition/scheduling boundary.

## MP-17

Failure required module не оставляет partial wave commit; degradation/fallback всегда explicit и observable.

## MP-18

Batching не объединяет независимые causal lineages.

## MP-19

Future Executive Control может выбирать только внутри admissible scheduler semantics и не bypass contracts/commit rules.

## MP-20

Cognitive module не запускает peers/scheduler recursively для получения hidden dependency.

## MP-21

Irreversible causally visible side effects до commit требуют отдельной explicit boundary/transactional design.

## MP-22

Snapshot/restore происходит относительно согласованного committed state, а не half-applied wave.

---

# 42. Что DU-05 намеренно не решает

Открытыми остаются:

- exact `ModuleProtocol` Python signatures;
- concrete `ModuleDescriptor` data type;
- exact read/write requirement schema;
- concrete scheduler implementation;
- конкретный DAG library;
- concrete async/parallel framework;
- exact wave commit data structure;
- exact private-state transaction API;
- exact failure enum/retry policy types;
- exact availability encoding;
- exact module lifecycle hook names;
- exact agent/composition/plan revision identifiers;
- exact RNG API;
- exact snapshot/checkpoint interface;
- exact learning capability interface;
- exact future Executive Control scheduling-intent API;
- performance/resource scheduler;
- module-specific dependencies и phases.

Эти решения не должны появляться как случайные implementation details до соответствующего design/version planning.

---

# 43. Последствия для следующих Design Updates

## DU-06 — Observability & Intervention

Должен определить:

- tracing execution plan/wave/module attempts;
- наблюдение base/result/commit revisions;
- intervention между committed boundaries;
- safe fork/replay;
- failure/retry evidence;
- visibility module-private state без разрушения encapsulation.

## DU-07 — Environment

Должен определить observation/outcome ingress и action/outcome boundaries, совместимые с scheduler lifecycle.

## DU-08–DU-24 — Module designs

Каждый module design обязан определить:

- semantic module identity;
- declared reads;
- declared writes;
- freshness/availability requirements;
- lifecycle participation;
- private state/scopes;
- stochasticity;
- failure/degradation behavior;
- compatibility with NoOp/control implementation;
- snapshot/restore implications.

## DU-22 — Executive Control

Должен работать поверх admissible scheduler graph, а не заменять его hidden learned orchestration.

## DU-25 — Experience/Data

Должен сохранять plan/wave/module/base revision provenance, достаточную для causal reconstruction.

## DU-26 — Training Lifecycle

Должен определить Learning Update и atomic activation новой `agent_revision` относительно in-flight waves.

## DU-27 — Checkpoint/Reproducibility

Должен определить snapshot всего causally relevant public/private/RNG state на quiescent committed boundary.

---

# 44. Completion gate DU-05

`DU-05` считается завершённым, если для любого будущего cognitive module можно ответить:

1. **Какие state fields он читает и с какой freshness/availability semantics?**
2. **Какими paths он имеет write authority?**
3. **Какое causally relevant private state он имеет?**
4. **В каких lifecycle phases он участвует?**
5. **Из какой committed revision он вычисляется?**
6. **С какими модулями он может находиться в одной execution wave?**
7. **Что произойдёт при его failure/stale result?**
8. **Как его NoOp/control implementation подключается без специальных вызовов consumers?**
9. **Как public и private effects становятся committed согласованно?**
10. **Может ли scheduler доказать отсутствие instantaneous cycle и illegal write conflict?**

После принятия этого документа следующий допустимый Design Update:

```text
DU-06 — Observability & Intervention
```
