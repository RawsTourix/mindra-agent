# Metacognitive / Executive Control MINDRA

## Статус документа

**Design Update:** `DU-22 — Metacognitive / Executive Control`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет `Executive Control` MINDRA — agent-owned ответственность за **адаптивный выбор допустимых внутренних вычислительных операций, распределение предоставленного cognitive resource budget и решение о продолжении/завершении дополнительной cognition внутри Decision Window**.

`Executive Control` не является `Cognitive Scheduler`, Policy/Planner, Cortex, Salience, Workspace или Self Model. Он не получает ambient доступ к runtime services и не исполняет произвольные Python-вызовы. Он выбирает только из явных `MetaActionProposal`/declared internal operations, после чего invariant `Cognitive Scheduler` проверяет и исполняет допустимый execution segment.

Документ определяет:

- module gate Executive Control;
- различие metacognitive monitoring и control;
- `Executive Control ≠ Cognitive Scheduler`;
- `Executive Control ≠ Policy / Planner`;
- `Internal MetaAction ≠ Environment Action`;
- explicit `CognitiveResourceEnvelope` и `ExecutiveBudgetLedger`;
- hard/soft budget semantics;
- `MetaActionProposal`, `ExecutiveDecision` и scheduler handoff;
- stop/continue cognition semantics;
- decision о Cortex/retrieval/World Model rollout/consolidation и других optional operations;
- relation с Self Model, Salience, Workspace, Valuation, Goals и Memory;
- goal-focus control без mutation `Goal Graph`;
- operation capability/availability и degradation;
- estimated/actual operation cost;
- wall-clock boundary;
- branch/imagination semantics;
- resource exhaustion;
- observability/intervention;
- snapshot/revision;
- `NoExecutive`, fixed-budget и matched controls;
- отрицательный критерий, при котором отдельная Executive boundary должна быть упрощена/удалена.

Документ опирается на:

- [`../execution-model.md`](../execution-model.md) — Decision Window, Cognitive Cycle и logical time;
- [`../module-lifecycle.md`](../module-lifecycle.md) — Scheduler/DAG/wave/commit semantics;
- [`../dependency-rules.md`](../dependency-rules.md) — explicit composition и запрет runtime Service Locator;
- [`../cognitive-state.md`](../cognitive-state.md) — committed state/revision/ownership;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — Evidence Plane/Intervention Gateway;
- [`self-model.md`](self-model.md) — competence/resource predictions без control authority;
- [`salience.md`](salience.md) — processing priority evidence без права запускать compute;
- [`workspace.md`](workspace.md) — bounded shared availability без control authority;
- [`cortex.md`](cortex.md) — explicit Cortex capability/request boundary;
- [`memory.md`](memory.md) — explicit retrieval boundary;
- [`memory-regulation.md`](memory-regulation.md) — explicit Consolidation Event и regulation proposals;
- [`world-model.md`](world-model.md) — prediction/imagination capability;
- [`goals.md`](goals.md) — committed Goals и proposal/adoption ownership;
- [`valuation.md`](valuation.md) — decision-relevant value/risk/constraint evidence без automatic policy authority.

Документ намеренно **не** определяет:

- final action selection и planning semantics — `DU-23`;
- Action Gate / execution — `DU-24`;
- Training Runtime/replay/objectives — `DU-25/26`;
- exact physical compute/checkpoint encoding — `DU-27`;
- конкретный learned controller architecture;
- обязательную Value-of-Computation formula;
- обязательный confidence threshold;
- обязательную стоимость Cortex/token/API;
- конкретный scheduler framework;
- exact Python API.

---

# 1. Цель DU-22

После `DU-05` MINDRA уже имеет invariant `Cognitive Scheduler`, который знает **как безопасно исполнять** разрешённый execution graph.

После `DU-13`, `DU-19` и `DU-21` Agent уже может иметь evidence о собственной competence, processing priority и shared temporary context.

Остаётся отдельный вопрос:

> **Как Agent решает, стоит ли до Action Commit потратить дополнительное внутреннее вычисление, на какую именно допустимую операцию его потратить и когда прекратить deliberation?**

Примеры:

```text
действовать уже сейчас

или

сделать ещё один Cognitive Cycle

или

разрешить дополнительный Memory retrieval

или

запросить Cortex

или

построить ещё несколько World Model rollout

или

инициировать Consolidation Event

или

выделить больше bounded Workspace capacity для текущего purpose
```

Эта responsibility не принадлежит Scheduler, потому что Scheduler не должен принимать task-dependent cognitive decisions.

Она не принадлежит Policy, потому что Policy/Planner `DU-23` отвечает за **содержание поведения/плана**, а не за общий контроль доступного cognitive processing.

---

# 2. Module gate

## 2.1. Альтернатива без Executive Control

Полностью допустима baseline-конфигурация:

```text
Decision Window
→ fixed Cognitive Cycle count
→ fixed retrieval schedule
→ fixed Cortex usage
→ fixed rollout depth
→ Policy
```

Если такая схема при matched budget работает не хуже adaptive control, отдельная Executive boundary может быть лишней.

## 2.2. Что должно добавлять Executive Control

Executive Control считается самостоятельной функцией только если он даёт комбинацию:

1. **adaptive operation selection** — разные ситуации получают разные internal operations;
2. **adaptive stopping/continuation** — число дополнительных cognitive steps зависит от evidence;
3. **budget-aware allocation** — ограниченный resource распределяется между конкурирующими operations;
4. **capability-aware degradation** — controller учитывает unavailable/degraded mechanisms;
5. **causal sensitivity** — controlled изменение competence/uncertainty/budget/cost evidence предсказуемо меняет control decisions.

## 2.3. Gate принят условно

Executive Control **принимается как отдельная boundary**, но falsifiably.

Если future evaluation показывает, что:

- fixed schedule при том же compute не хуже;
- random/matched router даёт тот же эффект;
- controller почти всегда выбирает одну операцию;
- изменение budget/competence/uncertainty не меняет решения ожидаемым образом;
- gain объясняется только большим количеством compute;

то `ADR-0022` должен быть пересмотрен, а Executive Control может быть упрощён до fixed runtime policy.

---

# 3. Главное архитектурное решение

MINDRA использует **proposal-driven, budget-aware Executive Control boundary поверх invariant Scheduler**.

Conceptually:

```text
Committed CognitiveState Rn
        +
ExecutiveState En
        +
CognitiveResourceEnvelope
        +
MetaActionProposal[]
        +
explicit monitoring evidence
        ↓
Executive Control
        ↓
ExecutiveDecision Dn
        ├── selected MetaActionRequest(s)
        ├── budget reservation/allocation
        ├── GoalFocusDirective?
        └── deliberation disposition
                ↓
Scheduler/runtime-core validation
                ↓
valid execution segment / explicit rejection
                ↓
atomic commits
                ↓
next Executive Control Point
```

Ключевые invariants:

```text
Executive Control ≠ Cognitive Scheduler
Executive Control ≠ Policy / Planner
Executive Control ≠ Salience
Executive Control ≠ Self Model
Internal MetaAction ≠ Environment Action
MetaActionProposal ≠ executed operation
ExecutiveDecision ≠ direct service call
Resource estimate ≠ actual resource usage
logical cognitive cost ≠ wall-clock latency автоматически
```

Решение фиксируется в `ADR-0022`.

---

# 4. Metacognitive monitoring ≠ control

## 4.1. Monitoring

Metacognitive monitoring означает evidence о состоянии собственного cognition, например:

- Self Model competence/limitations;
- uncertainty/support;
- progress/stagnation;
- unresolved contradictions;
- resource remaining;
- operation failures/degradation;
- Salience/Workspace state;
- pending MetaAction proposals;
- estimated expected benefit/cost конкретной операции;
- current Goal focus;
- recent control history.

Monitoring **не даёт control authority**.

Например:

```text
Self Model:
P(success) low
```

не означает автоматически:

```text
invoke Cortex
```

## 4.2. Control

Executive Control преобразует explicit monitoring evidence + proposals + budget в versioned `ExecutiveDecision`.

Таким образом:

```text
monitoring says what appears true about cognition
control chooses allowed internal operation
```

## 4.3. Нет обязательного отдельного Monitor-module

`DU-22` не вводит автоматически ещё один monolithic `MetacognitiveMonitor`.

Future implementation может собирать `ExecutiveObservation`/`MetaControlContext` как read projection из уже существующих canonical sources.

Если отдельный learned monitoring estimator позднее окажется нужен, его boundary должна быть обоснована отдельно и не подменять Self Model/World Model/Salience.

---

# 5. Executive Control и Cognitive Scheduler

## 5.1. Scheduler владеет допустимостью исполнения

Scheduler продолжает отвечать за:

- dependency graph;
- ready waves;
- write authority;
- stale-base validation;
- atomic commit;
- lifecycle phases;
- failure semantics;
- protection от instantaneous cycles.

## 5.2. Executive владеет task-dependent выбором optional cognition

Executive может решить:

```text
из разрешённых optional operations выбрать X
выделить X часть доступного budget
продолжить deliberation
остановить дополнительную cognition
```

Но не:

```text
обойти dependency
вызвать hidden service
переписать чужой state
создать instantaneous cycle
выполнить operation в запрещённой phase
```

## 5.3. Decision не является прямым вызовом

Запрещён canonical pattern:

```python
executive.memory.retrieve(...)
executive.cortex.generate(...)
```

Правильная semantics:

```text
ExecutiveDecision
→ MetaActionRequest
→ Scheduler/runtime validation
→ owning boundary/provider
→ traceable operation
```

Это защищает `DU-02` от превращения Executive в Service Locator.

---

# 6. Internal MetaAction

`Internal MetaAction` — agent-owned решение инициировать/разрешить определённую внутреннюю computation/control operation.

Это **не Environment Action**.

Conceptual families могут включать:

```text
continue_cognition
finish_optional_deliberation / yield_to_policy
request_cortex_operation
request_memory_retrieval
request_world_model_prediction_or_rollout
request_workspace_budget/context adjustment
request_consolidation_event
select/update goal focus context
request another eligible cognitive operation
```

Точный enum не frozen.

## 6.1. MetaAction не создаёт semantic request из воздуха

Executive не должен сам изобретать чужую domain-specific payload.

Например, Memory query или semantic Cortex request обычно формируется соответствующим producer/consumer как `MetaActionProposal`.

Executive выбирает **стоит ли разрешить/профинансировать proposal**, а не становится владельцем Memory query semantics или Cortex prompt semantics.

## 6.2. Internal action provenance

Каждая выполненная internal operation должна связываться минимум с:

```text
executive decision ID
proposal ID
operation semantic ID
provider/owner identity
base state revision
executive revision
budget revision
actual cost evidence
result/failure provenance
```

---

# 7. MetaActionProposal

Чтобы Executive не стал ambient orchestrator, optional cognitive work предлагается через explicit proposals.

Conceptually:

```text
MetaActionProposal
├── proposal_id
├── operation_kind / semantic capability
├── requester/source
├── target/context refs
├── payload/request ref
├── prerequisites
├── required capability
├── estimated resource cost
├── expected benefit / uncertainty evidence?
├── urgency/deadline?
├── allowed logical phase
├── branch/scope
└── provenance/revisions
```

Proposal:

- ещё не резервирует resource автоматически;
- ещё не означает execution;
- не даёт requester права вызвать provider напрямую;
- может стать stale;
- может быть отклонён/отложен/деградирован.

---

# 8. Declared Internal Operation Catalog

Executive может выбирать только из операций, известным Composition/Scheduler boundary.

Conceptually существует versioned описание допустимых operation capabilities:

```text
InternalOperationCatalog
├── operation semantic identity
├── owner/provider boundary
├── required prerequisites
├── allowed phases
├── resource dimensions
├── concurrency/conflict constraints
├── availability/degradation
└── interface revision
```

Это **не runtime Service Locator**.

Executive не получает arbitrary object handles. Catalog описывает доступные semantic operations; конкретная composition/dispatch остаётся у runtime core.

Catalog revision входит в provenance Executive decisions.

---

# 9. CognitiveResourceEnvelope

## 9.1. Кто задаёт верхний предел

Hard resource envelope может быть предоставлен:

- composition/version configuration;
- Environment/task contract, если resource является частью задачи;
- Experiment Runner в явно обозначенном evaluation mode;
- инфраструктурным runtime как enforced hard limit.

Но hidden evaluator information не становится cognitive input.

Если Executive должен учитывать limit при выборе, ему передаётся **намеренно agent-visible semantic resource envelope**, а не raw infrastructure secret.

## 9.2. Executive не создаёт resource из воздуха

Executive может распределять/резервировать только предоставленный envelope.

```text
provided resource envelope
→ Executive allocation
→ actual operation consumption
```

Не:

```text
budget exhausted
→ Executive increases budget itself
```

## 9.3. Multi-dimensional budget

Не принимается один universal:

```text
compute = 100
```

Envelope может иметь независимые dimensions, например conceptually:

```text
additional Cognitive Cycles
Cortex operation quota
generation/token-like allowance, если semantic/version-specific
Memory retrieval operations
World Model rollout steps/branches
consolidation allowance
Workspace capacity envelope
other declared cognitive resources
```

Concrete dimensions первой версии определяются version design.

---

# 10. ExecutiveBudgetLedger

Executive-owned state отслеживает agent-visible resource semantics:

```text
ExecutiveBudgetLedger
├── envelope revision
├── resource dimensions
├── initial grant
├── reserved
├── consumed
├── remaining
├── pending reservations
├── hard/soft limits
└── provenance
```

Ключевое:

```text
budget estimate
≠
reservation
≠
actual consumption
```

Если Cortex operation оценивалась в 100 units, а реально использовала 150, ledger должен сохранить discrepancy.

Provider/runtime hard enforcement имеет приоритет: Executive не может потратить физически недоступный resource только потому, что его внутренний estimate ошибся.

---

# 11. Hard и soft limits

## 11.1. Hard limit

Нельзя превысить.

Например:

```text
remaining Cortex calls = 0
```

Executive не может решить вызвать Cortex ещё раз.

## 11.2. Soft budget / cost preference

Может быть превышен только если concrete policy/version это разрешает и hard envelope остаётся валиден.

Soft cost может участвовать в trade-off:

```text
expected cognitive benefit
vs
expected resource cost
```

Но `DU-22` не принимает universal Value-of-Computation formula.

---

# 12. Cost semantics и wall-clock boundary

По умолчанию:

```text
GPU latency
network RTT
Colab pause
host scheduling delay
```

не являются cognitive cost только потому, что физически произошли.

Если task/version намеренно делает latency, money/API quota, energy или другую physical quantity decision-relevant и agent-visible, она должна быть представлена через explicit resource/cost contract.

Поэтому:

```text
logical operation cost
≠
wall-clock duration автоматически
```

При этом observability может всегда сохранять physical latency как telemetry, не превращая её в input Agent.

---

# 13. Executive Control Point

Executive decision принимается только на явной causal boundary, где доступен committed state.

Conceptual Decision Window:

```text
Observation / Outcome Commit
        ↓
mandatory scheduled cognition
        ↓
Committed State Rn
        ↓
Executive Control Point EC0
        ↓
optional execution segment
        ↓
Committed State Rn+1
        ↓
Executive Control Point EC1
        ↓
...
        ↓
Yield to Policy
```

Executive не меняет решение посередине atomic wave на основании partial state.

Точное расположение control points задаётся version execution plan.

---

# 14. Continue / Stop semantics

Executive должен уметь выразить минимум semantic distinction:

```text
continue optional cognition
```

и:

```text
finish optional deliberation / yield to Policy
```

Это не равно:

```text
Action Commit
```

Executive **не выбирает Environment action**. Он только прекращает дополнительный internal compute и передаёт committed context будущему `Policy / Planner`.

## 14.1. Budget exhaustion

Если hard budget исчерпан:

```text
no additional optional cognition available
→ explicit budget-exhausted disposition
→ Policy/degradation path
```

а не hidden extra compute.

## 14.2. Необязательный learned stopping

Stopping может быть:

- fixed threshold control;
- heuristic;
- rule-based;
- learned;
- Value-of-Computation-like;
- uncertainty-aware;
- hybrid.

Concrete method не frozen.

---

# 15. Cortex invocation boundary

Executive не строит backend-specific prompt и не вызывает provider SDK.

Допустимый путь:

```text
consumer / semantic producer
→ Cortex-related MetaActionProposal
→ Executive selection/budget
→ Scheduler validation
→ Cortex Gateway
→ CortexResult
```

`NoCortex`/unsupported capability должна быть видна через declared availability.

Если Cortex unavailable, Executive может выбрать **явно предусмотренную** альтернативу, но silent fallback запрещён.

---

# 16. Memory retrieval boundary

Executive не сканирует Memory и не генерирует ambient retrieval query.

Допустимый pattern:

```text
consumer
→ RetrievalRequest proposal
→ MetaActionProposal
→ Executive decision
→ Scheduler/runtime
→ Memory Retrieval
→ RetrievalResult
```

Так можно отдельно наблюдать:

- кто хотел retrieval;
- почему Executive его разрешил/отклонил;
- сколько budget было выделено;
- что Memory вернула;
- был ли результат затем admitted в Workspace.

---

# 17. World Model / planning compute

`DU-22` может выбирать количество разрешённой prediction/imagination работы, но не становится Planner.

Conceptually:

```text
prediction/rollout proposal
→ Executive budget allocation
→ World Model operation
→ prediction/imagination result
```

Executive может ограничить:

- rollout depth;
- branch count;
- number of prediction calls;
- continuation of additional rollout work,

если соответствующие resource dimensions/version semantics объявлены.

Но **какие action candidates моделировать и как построить план** относится к `DU-23`.

---

# 18. Consolidation initiation

`DU-20` определил explicit `Consolidation Event`.

Executive может в будущем разрешать/инициировать его через explicit meta-action:

```text
ConsolidationProposal/need evidence
→ MetaActionProposal
→ ExecutiveDecision
→ Memory Regulation boundary
→ explicit Consolidation Event
```

Executive не выбирает derived memory contents и не мутирует Memory Store.

---

# 19. Workspace relation

Workspace имеет собственный `WorkspaceBudget` и AdmissionPolicy.

Executive может, если concrete version это поддерживает:

- предоставить/изменить budget envelope для Workspace purpose;
- изменить current control context/focus, используемый при admission;
- решить, стоит ли тратить additional processing на Workspace-related operation.

Но:

```text
Executive allocation
≠
Workspace admission
```

Executive не выбирает конкретные `WorkspaceItem` вместо Workspace owner.

---

# 20. Salience relation

Salience может предоставить:

```text
which targets deserve processing?
```

Executive решает:

```text
which allowed operation gets scarce compute now?
```

Поэтому:

```text
SalienceProfile / AttentionAllocation
→ evidence для Executive
```

но:

```text
AttentionAllocation
≠
execute this operation
```

Executive также может учитывать operation cost/capability/expected benefit, которых Salience сама не обязана моделировать.

---

# 21. Self Model relation

Self Model предоставляет competence/limitation/resource predictions.

Например:

```text
Self Prediction:
Cortex-assisted strategy likely improves success
```

или:

```text
Self Prediction:
additional rollout cost high, expected benefit uncertain
```

Это evidence, не команда.

Executive может использовать его, сохраняя:

```text
Self Model
→ monitor/predict

Executive
→ regulate
```

Если Self Model unavailable, Executive должен иметь explicit degradation/control behavior.

---

# 22. Goal focus

`Goal Graph` остаётся собственностью Goal System.

Executive может владеть temporary **Goal Focus Directive/Control State**, которое:

- содержит refs на уже committed goal IDs;
- влияет на processing purpose/priority/context;
- не меняет lifecycle/commitment/objective Goal;
- не создаёт и не удаляет Goal.

Если нужен новый subgoal:

```text
Executive / Planner
→ Goal Proposal
→ Goal System
```

а не direct mutation Goal Graph.

---

# 23. Valuation и Value of Computation

Executive может учитывать decision-relevant evidence о выгоде дополнительного computation.

Conceptually:

```text
expected improvement in decision quality
expected uncertainty reduction
expected information gain
expected success improvement
expected resource cost
risk / deadline
```

Но `DU-22` не принимает один универсальный scalar:

```text
VOC = benefit - cost
```

как canonical truth.

`Value of Computation` может быть derived estimator/policy feature конкретной версии.

Если используется scalar, он обязан иметь estimator/policy/revision/provenance.

---

# 24. ExecutiveDecision

Conceptually:

```text
ExecutiveDecision
├── decision_id
├── base state_revision
├── executive_revision
├── executive_policy_revision
├── operation_catalog_revision
├── budget ledger revision
├── considered MetaActionProposal IDs
├── selected MetaActionRequest(s)
├── budget reservations/allocations
├── GoalFocusDirective?
├── deliberation disposition
├── evidence refs
├── degradation/fallback provenance
└── branch/mode provenance
```

Decision должен быть causally inspectable.

Если proposal не выбран, future evaluation должна по возможности отличать:

```text
rejected
vs
deferred
vs
unavailable
vs
insufficient budget
vs
stale
vs
constraint conflict
```

Exact enums не frozen.

---

# 25. Parallel internal operations

ExecutiveDecision может выбрать более одной internal operation, если:

- operations semantic-compatible;
- budget позволяет;
- Scheduler dependency graph разрешает параллельное/совместное execution;
- нет state/write conflicts;
- version policy допускает batch selection.

Кто выполняется параллельно — окончательно определяет Scheduler.

Executive не задаёт unsafe thread order.

---

# 26. Branch / imagination semantics

Нужно различать два класса resource/state.

## 26.1. Реальный compute, потраченный на imagination

Если Agent реально вычислил World Model branch, это **реально израсходованный cognitive resource** текущей lineage.

Он списывается из real `ExecutiveBudgetLedger`.

## 26.2. Симулируемый будущий internal state внутри branch

Если World Model/Planner моделирует, сколько future compute понадобилось бы в hypothetical future, такой budget/state является:

```text
simulated / branch-local
```

и не изменяет реальный ledger автоматически.

## 26.3. Branch-local ExecutiveState

Counterfactual/imagination может иметь отдельный simulated ExecutiveState, если concrete Planner/World Model использует такую capability.

Но он не коммитится в real Agent без explicit real-world/control transition.

---

# 27. Failure / degradation

Executive layer должна различать минимум semantic classes:

```text
proposal unavailable
required capability unavailable
hard budget exhausted
reservation failed
actual cost exceeded estimate
operation rejected by Scheduler
operation failed
operation result stale
control policy failure
invalid decision
```

Fallback/degradation всегда explicit и versioned.

Запрещено:

```text
Cortex unavailable
→ silently run different expensive path
```

или:

```text
budget exhausted
→ continue anyway
```

---

# 28. Resource exhaustion

При hard exhaustion Executive должен сформировать observable состояние/decision.

Possible policy outcomes:

```text
yield_to_policy
use cheaper already-allowed operation
degrade capability
explicitly fail Decision Window
```

Но concrete fallback определяется version design.

Resource exhaustion не превращается автоматически в Environment failure.

---

# 29. Revision semantics

Нужно различать минимум:

```text
executive_system_revision
executive_policy_revision
executive_state_revision
resource_envelope_revision
budget_ledger_revision
operation_catalog_revision
agent_revision
```

Если Agent revision меняет доступные capabilities/costs, старые control policies/estimates могут стать stale.

Особенно нельзя молча продолжать считать старую Cortex cost/competence semantics актуальной после backend swap.

---

# 30. Snapshot

Полный Agent Snapshot должен учитывать causally relevant Executive state:

```text
ExecutiveState
ExecutiveBudgetLedger
resource envelope refs/state
pending reservations
pending MetaAction proposals, если causally relevant
GoalFocusDirective
operation catalog revision
learned/recurrent controller state
adaptive cost/benefit estimators
RNG
intervention/degradation state
```

Две ветви с одинаковым CognitiveState, но разным remaining cognitive budget не являются exact counterfactual clones.

---

# 31. Observability

Evidence Plane должен позволять восстановить минимум:

```text
какой Executive Control Point
какой committed state был прочитан
какой budget/envelope действовал
какие proposals рассматривались
какие evidence refs использовались
какое решение принято
какие ресурсы зарезервированы
что Scheduler принял/отклонил
что реально исполнилось
какая actual cost получилась
почему cognition продолжилась/остановилась
какой remaining budget остался
```

Это особенно важно для claim:

> adaptive compute улучшил результат.

Без trace невозможно отличить адаптивность от простого увеличения compute.

---

# 32. Interventions

Допустимы controlled interventions:

- изменить `CognitiveResourceEnvelope`;
- clamp remaining budget;
- изменить operation estimated cost;
- изменить/скрыть Self competence evidence;
- изменить uncertainty evidence;
- shuffle/remove Salience evidence;
- force/forbid конкретный MetaAction;
- force stop/continue at control point;
- изменить GoalFocusDirective;
- сделать capability unavailable/degraded;
- заменить Executive policy/control implementation.

Intervention всегда сохраняет provenance `DU-06`.

---

# 33. Control configurations

Обязательны минимум:

```text
NoExecutive
FixedScheduleExecutive
FixedBudgetExecutive
RandomMetaActionExecutive
SimpleThresholdExecutive
SalienceOnlyExecutive
CostUnawareExecutive
MatchedLearnedRouterControl
OracleBudgetAllocationControl   # research-only
```

Точные имена implementations не frozen.

## 33.1. NoExecutive

Optional cognition задаётся fixed runtime/version schedule без adaptive agent-owned control.

Это first-class baseline.

## 33.2. Matched control

Особенно важно сравнивать learned Executive не только с `NoExecutive`, но и с controller схожей:

- parameter capacity;
- state capacity;
- total compute;
- observation/evidence bandwidth,

но без целевой metacognitive semantics.

---

# 34. Evaluation obligations

Executive Control считается полезным только при **matched resource accounting**.

Нужно измерять минимум:

```text
task performance
actual cognitive resource consumption
performance / resource frontier
operation selection distribution
stopping distribution
budget violations
resource-estimation error
failure/degradation rate
sensitivity to uncertainty/competence/cost
OOD generalization
```

Обязательные families:

## 34.1. Adaptive vs fixed compute

```text
Adaptive Executive
vs
Fixed schedule
```

при одинаковом expected/total budget.

## 34.2. Budget sweep

```text
very small
small
medium
large
```

и сравнение performance-resource frontier.

## 34.3. Difficulty/uncertainty shift

Adaptive system должен при прочих равных выделять различный compute там, где relevant evidence действительно различается, если это соответствует принятой policy hypothesis.

## 34.4. Capability degradation

Например:

```text
Cortex available
vs
Cortex unavailable
```

и проверка explicit adaptation без hidden fallback.

## 34.5. Causal evidence intervention

```text
same task/state
same true capability

branch A:
Self competence evidence high

branch B:
Self competence evidence low
```

проверяется изменение control decision отдельно от фактической capability.

---

# 35. Negative gate

Отдельная Executive boundary должна быть пересмотрена, если:

- fixed schedule на matched compute не хуже;
- controller использует почти постоянный operation pattern;
- performance gain исчезает после equal-compute matching;
- budget/competence/uncertainty interventions не дают предсказуемого control effect;
- matched learned router работает столь же хорошо;
- overhead Executive превышает functional gain;
- controller систематически нарушает/обходит modular ownership и требует central ambient state.

Отрицательный результат является нормальным research outcome.

---

# 36. Что DU-22 намеренно не фиксирует

Не фиксируются:

- конкретная RL/supervised/meta-learning objective;
- конкретный neural controller;
- один scalar Value of Computation;
- confidence threshold;
- token pricing;
- exact resource units;
- exact default number Cognitive Cycles;
- exact max rollout depth;
- exact Cortex-call policy;
- Policy/Planner algorithm;
- Action selection;
- optimizer;
- Python scheduling implementation.

Эти решения относятся к downstream DU/version design.

---

# 37. Completion gate DU-22

`DU-22` считается завершённым, если однозначно определено:

- Executive Control имеет отдельную falsifiable responsibility;
- monitoring и control разведены;
- Scheduler остаётся invariant execution owner;
- Policy/Planner остаётся downstream action/plan owner;
- internal MetaActions отделены от Environment Actions;
- optional operations поступают через explicit proposal/catalog boundary;
- resource envelope explicit и Executive не создаёт budget сам;
- stop/continue имеет causal control-point semantics;
- Cortex/retrieval/rollout/consolidation не вызываются ambient способом;
- Goal focus не мутирует Goal Graph;
- Salience/Self Model являются evidence, а не controllers;
- branch-local state и actual computation cost разведены;
- snapshot/intervention/failure/control/evaluation requirements заданы;
- конкретная implementation не зафиксирована.
