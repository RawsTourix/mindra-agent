# Policy / Planner MINDRA

## Статус документа

**Design Update:** `DU-23 — Policy / Planner`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет границу формирования behavioral candidates, planning и финального **selected-action intention** MINDRA после того, как предыдущие слои уже предоставляют Goals, World/Self beliefs, Memory, Valuation, Salience, Workspace и Executive Control.

Ключевое решение `DU-23`:

- `Policy System` является обязательным semantic owner финального behavioral selection внутри Agent;
- `Planner` является **optional/falsifiable provider** планов, action candidates и subgoal proposals;
- `Planner` не выбирает действие окончательно;
- `World Model` предсказывает/воображает, но не планирует сам по себе;
- `Valuation` оценивает/сравнивает, но не выбирает;
- `Executive Control` решает, сколько дополнительного cognition разрешить, но не выбирает Environment behavior;
- выбранное Policy намерение ещё **не является исполненным действием** и передаётся в будущую `DU-24 — Action Boundary / Gate / Executor`.

Документ опирается на:

- [`../execution-model.md`](../execution-model.md) — Decision Window, Action Commit и causal time;
- [`../cognitive-state.md`](../cognitive-state.md) — committed state/revision/provenance;
- [`../module-lifecycle.md`](../module-lifecycle.md) — scheduler/wave/atomic commit;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — evidence/intervention;
- [`environment.md`](environment.md) — agent-visible action/task boundary и hidden ground truth;
- [`goals.md`](goals.md) — committed Goals, subgoal proposal boundary;
- [`world-model.md`](world-model.md) — World Belief, prediction, imagination;
- [`self-model.md`](self-model.md) — competence/feasibility evidence;
- [`memory.md`](memory.md) — explicit retrieval;
- [`cortex.md`](cortex.md) — optional semantic reasoning capability;
- [`valuation.md`](valuation.md) — `ValueProfile`, risk/constraints, explicit comparison;
- [`salience.md`](salience.md) — processing priority;
- [`workspace.md`](workspace.md) — bounded shared context;
- [`executive-control.md`](executive-control.md) — adaptive compute/meta-actions, yield semantics и budget.

Документ намеренно **не** определяет:

- exact Environment action schema — `DU-24`;
- action validation/safety gate/dispatch — `DU-24`;
- Experience/Data/Replay schema — `DU-25`;
- training objectives, RL algorithm, imitation/offline learning — `DU-26`;
- конкретный MCTS/MPC/beam-search/ToT algorithm;
- конкретную neural Policy architecture;
- обязательный Planner;
- обязательный scalar action score;
- обязательную deterministic или stochastic Policy;
- exact Python API;
- checkpoint encoding — `DU-27`.

---

# 1. Цель DU-23

К `DU-23` MINDRA уже умеет отвечать на вопросы:

```text
чего я пытаюсь достичь?                 → Goals
что происходит и может произойти?       → World Model
на что я способен?                      → Self Model
что я помню?                            → Memory
что для меня ценно/рискованно?          → Valuation
что заслуживает processing?             → Salience
что сейчас общее рабочее содержание?    → Workspace
нужно ли ещё думать и сколько?          → Executive Control
```

Но всё ещё отсутствует отдельный owner ответа:

> **Какое конкретное поведенческое намерение Agent выбирает сейчас?**

`DU-23` должен определить эту responsibility, не смешав её с prediction, planning compute allocation, valuation или execution.

Канонические различия:

```text
World Prediction
≠
Plan
≠
Action Candidate
≠
SelectedActionIntent
≠
Action Commit
≠
Executed Action
≠
Observed Outcome
```

---

# 2. Два независимых module gate

## 2.1. Policy System gate

Policy boundary **проходит gate безусловно как semantic responsibility**.

Даже если concrete implementation — простое правило, neural policy, random baseline или Planner-backed selector, Agent должен иметь однозначного owner результата:

```text
candidate behavior(s)
        ↓
Policy selection
        ↓
SelectedActionIntent
```

Без этой boundary final behavioral choice неизбежно скрывается внутри Valuation, Planner, Cortex, main loop или Environment adapter.

## 2.2. Planner gate

Planner проходит gate **условно/falsifiably**.

Полностью допустима конфигурация:

```text
Committed context
→ Reactive Policy
→ SelectedActionIntent
```

Planner оправдан как отдельная boundary, только если он добавляет измеримую функцию сверх reactive/direct policy:

1. explicit multi-step candidate construction;
2. search/lookahead over alternative futures;
3. temporal/contingent plan representation;
4. plan persistence/replanning;
5. reusable plan evidence для Policy;
6. causal benefit при matched compute/state/parameter controls.

Если `Policy + Planner` не превосходит matched `ReactivePolicy` на задачах, требующих long-horizon/partial-observability planning, отдельный Planner должен быть упрощён/отключён.

---

# 3. Главное архитектурное решение

MINDRA принимает **Policy-owned final behavioral selection с optional Planner как explicit provider планов/candidates**.

Conceptually:

```text
Committed behavioral context
        │
        ├── Goals / Goal focus
        ├── World Belief
        ├── Self evidence
        ├── Workspace / explicit Memory context
        ├── Valuation evidence
        └── action capability surface
        ↓
Candidate generation
        ├── Reactive Policy candidates
        ├── Planner candidates/plans      optional
        ├── scripted/control candidates   optional
        └── Cortex-assisted candidates    optional
        ↓
PolicyCandidateSet
        ↓
Valuation / Comparison evidence
        ↓
Policy Selection
        ├── select candidate
        └── or explicit DecisionDeferral
                ↓
SelectedActionIntent
                ↓
DU-24 Action Boundary
```

Planner path:

```text
PlanningRequest
    +
World Belief / Goals / allowed context
    +
Executive-provided planning budget
        ↓
Planner
        ↓
World Model rollout/search queries
        ↓
PlanCandidate / ActionCandidate
        ↓
PolicyCandidateSet
```

Ключевые invariants:

```text
Policy ≠ Planner
Policy ≠ Executive Control
Planner ≠ World Model
Plan ≠ ImaginedTrajectory
Valuation ≠ Policy Selection
Cortex proposal ≠ Policy decision
SelectedActionIntent ≠ Action Commit
```

Решение фиксируется `ADR-0023`.

---

# 4. Policy System

## 4.1. Responsibility

Policy System отвечает за:

- формирование/приём explicit behavioral candidates;
- проверку candidate comparability на semantic уровне;
- использование разрешённого behavioral context;
- запрос/использование `ValueProfile`/`ComparisonResult`, где это предусмотрено;
- применение versioned selection policy;
- explicit handling constraints/risk/incomparability;
- stochastic/deterministic selection semantics;
- создание `SelectedActionIntent`;
- explicit `DecisionDeferral`, если выбор ещё не сформирован;
- policy-specific state/revision/snapshot/provenance.

## 4.2. Policy System не отвечает за

- выполнение Environment action;
- Action Gate/dispatch;
- hidden Environment validation;
- изменение Goal Graph;
- выполнение World Model rollout;
- распределение global cognitive budget;
- Memory retrieval ambient способом;
- Workspace admission;
- automatic scalarization чужих `ValueProfile` без explicit policy;
- training reward definition.

## 4.3. Единственный owner selected-action intention

Planner, Cortex, Valuation и rule-based candidate source могут предлагать варианты, но canonical `SelectedActionIntent` normal runtime способом создаёт только Policy boundary.

Это позволяет однозначно измерять:

```text
что было предложено
что было оценено
что Policy выбрала
что затем Action Gate разрешил/отклонил
что Environment реально исполнил
```

---

# 5. BehavioralContext

Policy не получает ambient весь `CognitiveState`.

Используется declared projection `BehavioralContext`, который conceptually может содержать:

```text
BehavioralContext
├── base state_revision
├── decision_id
├── current Goal refs / GoalFocusDirective
├── WorldBelief ref/summary
├── Self evidence refs
├── WorkspaceSnapshot/projection?
├── explicit RetrievalResult refs?
├── current Drive/Affect/Appraisal refs, если contract Policy их читает
├── Valuation context refs
├── action capability descriptor
├── Executive budget/control disposition
├── unavailable/degraded capability states
└── provenance
```

Ни одно поле не становится обязательным только потому, что существует в архитектуре.

---

# 6. Action Candidate

`ActionCandidate` — proposal конкретного возможного поведения Agent, ещё не выбранного Policy.

Conceptually:

```text
ActionCandidate
├── candidate_id
├── action semantic proposal/ref
├── source identity
├── base state_revision
├── agent_revision
├── target Goal refs
├── assumptions/preconditions?
├── predicted consequence refs?
├── plan ref?
├── ValueProfile / Comparison refs?
├── feasibility/risk/constraint refs?
├── confidence/support?
├── branch provenance
└── source provenance
```

Candidate может происходить из:

- direct/reactive Policy generation;
- Planner;
- Cortex-assisted proposal;
- scripted/control source;
- hierarchical/subpolicy source;
- research intervention.

`ActionCandidate` не получает authority только из-за source.

---

# 7. Planner как optional provider

## 7.1. Responsibility

Planner отвечает за построение **структурированных возможных путей поведения** из текущего belief/goal/context и разрешённого planning budget.

Planner может:

- генерировать action sequences;
- строить branching/contingent plans;
- искать по imagined futures;
- просить World Model выполнить конкретный rollout;
- использовать Valuation results для search ordering/pruning;
- использовать Self Model feasibility;
- использовать Cortex для semantic plan generation;
- поддерживать plan state/persistence;
- предлагать subgoal через Goal Proposal boundary;
- выдавать action/plan candidates Policy.

## 7.2. Planner не отвечает за

- финальный behavioral choice;
- Action Commit/dispatch;
- собственную физическую dynamics модель;
- direct mutation Goals;
- global cognitive budget;
- hidden Environment oracle;
- automatic Memory retrieval;
- declaration imagined branch natural experience.

## 7.3. Planner ≠ World Model

```text
World Model:
«если выполнить A, возможны B/C»

Planner:
«какие A/B/C… стоит рассмотреть как последовательность/ветвление для Goal G?»
```

World Model предоставляет prediction/imagination primitive.

Planner задаёт search structure, candidate sequence, horizon, branching и plan semantics.

---

# 8. Plan ≠ ImaginedTrajectory

`ImaginedTrajectory` — результат конкретного simulation/rollout World Model.

`Plan` — agent-owned **предписывающая/условная структура намерений**, которая может ссылаться на несколько imagined trajectories и содержать contingencies.

Conceptually:

```text
Plan
├── plan_id
├── plan_revision
├── root Goal refs
├── base belief/state revision
├── steps / nodes
├── action candidates
├── conditions / contingencies
├── predicted consequence refs
├── valuation refs
├── assumptions
├── validity/invalidation conditions
├── horizon semantics
├── source Planner revision
└── provenance
```

Например:

```text
если дверь открыта → войти
иначе если ключ уже найден → использовать ключ
иначе → искать ключ
```

Это plan даже если World Model никогда не породила один единственный rollout, содержащий все эти branches одновременно.

---

# 9. Planning under partial observability

Planner normal runtime способом планирует относительно:

```text
World Belief
agent-visible evidence
predicted observation/outcome distributions
```

а не `Hidden World State` Environment.

Contingent plan может иметь условия по будущим observations/beliefs:

```text
if observation O1:
    branch A
else:
    branch B
```

Но не:

```text
if hidden_environment_variable == X:
```

если X недоступна Agent.

Oracle Planner допускается только как research control.

---

# 10. Candidate generation и PolicyCandidateSet

Policy должна работать с explicit candidate set.

Conceptually:

```text
PolicyCandidateSet
├── candidate_set_id
├── base state_revision
├── decision_id
├── candidate refs[]
├── generation sources
├── dedup/equivalence metadata?
├── coverage status?
├── unavailable source states
└── provenance
```

Candidate generator не получает право выбрать свой candidate автоматически.

Если два sources предложили semantic-equivalent action, future implementation может deduplicate их, но source provenance должна сохраняться.

---

# 11. Valuation и final selection

`Valuation System` может вернуть:

```text
A preferred over B
A/B incomparable
candidate violates constraint
risk profile differs
optional scalarized values
```

Policy обязана иметь explicit versioned semantics, как использовать этот evidence.

Запрещено universal правило:

```text
action = argmax(value)
```

как архитектурный invariant.

Допустимые concrete selection families:

- deterministic preference ordering;
- lexicographic constraint-first selection;
- stochastic selection над admissible set;
- learned chooser;
- rule-based fallback;
- exploration-aware selection.

Конкретная family не frozen.

---

# 12. Incomparability, uncertainty и DecisionDeferral

`ComparisonResult = incomparable` является валидным результатом.

Policy не обязана придумывать фиктивный scalar.

Она может:

1. применить explicit tie-break/selection policy;
2. выбрать exploratory candidate;
3. вернуть `DecisionDeferral` с причиной `insufficient_decision_evidence`;
4. сформировать `MetaActionProposal` дополнительного planning/retrieval/Cortex/valuation refinement и вернуть control Executive;
5. при исчерпанном budget применить заранее определённый fallback или explicit failure.

Ключевой цикл:

```text
Executive yields to Policy
        ↓
Policy selection attempt
        ├── SelectedActionIntent
        └── DecisionDeferral + MetaActionProposal(s)
                         ↓
                  Executive Control Point
```

Это не instantaneous recursive call. Возврат к Executive происходит через declared lifecycle boundary и committed evidence.

---

# 13. Executive Control ↔ Planner/Policy

Executive Control отвечает за:

```text
разрешить/не разрешить дополнительный planning compute
planning horizon/branch budget как resource allocation
разрешить extra Cortex/retrieval/rollout operations
остановить optional deliberation и yield Policy
```

Planner отвечает за:

```text
как использовать разрешённый planning budget
какую search/planning структуру построить
какие plan/action candidates предложить
```

Policy отвечает за:

```text
какое behavioral intention выбрать
```

Следовательно:

```text
Executive budget allocation
≠
Planner search semantics
≠
Policy selection semantics
```

---

# 14. Cortex-assisted planning boundary

Cortex может:

- предложить candidate action;
- предложить high-level plan structure;
- интерпретировать textual Goal;
- предложить decomposition;
- оценить semantic plausibility как explicit evidence.

Но:

```text
Cortex output
≠
Plan автоматически
≠
SelectedActionIntent
```

Cortex-derived proposal должен пройти соответствующий Planner/Policy boundary.

Backend-specific prompt/token details не входят в Policy/Planner contract.

---

# 15. Subgoals

Planner может обнаружить необходимость промежуточной цели.

Правильная цепочка:

```text
Planner
→ Goal Proposal
→ Goal System
→ accepted/rejected/deferred
```

Planner scratchpad/node не становится committed subgoal автоматически.

Если Goal System не принял proposal, Planner обязан либо адаптировать plan, либо пометить dependency unresolved.

---

# 16. Plan persistence и replanning

Planner может иметь persistent `PlanState`, но plan не является вечной инструкцией.

Plan должен связываться с assumptions и revisions, например:

```text
base WorldBelief revision
Goal revision/status
action capability revision
Planner revision
critical assumptions
```

После изменения context plan может стать:

```text
valid
stale
partially applicable
invalidated
unknown
```

Replanning не происходит hidden background способом.

Planner/Policy может создать `MetaActionProposal`:

```text
replan current plan
```

а Executive решает, стоит ли выделять дополнительный resource.

## 16.1. Receding-horizon pattern

Допускается pattern:

```text
plan several steps
→ select only next intention
→ observe actual outcome
→ assimilate
→ reuse/revalidate/replan
```

Но MPC/receding horizon не является обязательным algorithm.

---

# 17. Stochastic Policy

Policy может быть stochastic.

Нужно различать:

```text
policy distribution / preference state
≠
sampled SelectedActionIntent
```

Causal evidence должно сохранять:

- policy revision;
- candidate set;
- distribution/selection evidence, если доступно;
- RNG identity/state, где causally relevant;
- sampled candidate;
- intervention/fallback provenance.

Одинаковый candidate ranking не гарантирует одинаковую sampled action intention при independent RNG.

---

# 18. SelectedActionIntent

`SelectedActionIntent` — canonical output Policy для одного Decision Window до Action Gate.

Conceptually:

```text
SelectedActionIntent
├── intent_id
├── decision_id
├── selected candidate ref
├── action semantic proposal/ref
├── source Policy revision
├── candidate-set ref
├── supporting Plan ref?
├── Value/Comparison refs?
├── risk/constraint refs?
├── Goal refs
├── base state_revision
├── agent_revision
├── stochastic selection provenance?
├── branch/intervention/degradation provenance
└── status
```

`SelectedActionIntent` означает:

> Policy предпочла это поведение при данном committed context.

Он **не означает**:

- action валиден по final action contract;
- действие безопасно/разрешено Gate;
- action уже committed;
- Environment его принял;
- action был выполнен;
- ожидаемый outcome произошёл.

Эти различия принадлежат `DU-24`.

---

# 19. Failure / degradation

Нужно различать минимум:

```text
no candidates
Planner unavailable
Planner budget exhausted
World Model unavailable
Cortex unavailable
Valuation unavailable
all candidates constraint-rejected
all candidates incomparable under current policy
selection timeout/resource exhaustion
invalid/stale candidate set
stale plan
Policy backend failure
```

Нельзя маскировать всё под random action без provenance.

Fallback может быть:

- reactive Policy;
- deterministic safe/default candidate;
- explicit no-op candidate, если Environment contract допускает;
- DecisionDeferral;
- failure.

Но fallback policy обязана быть versioned и observable.

---

# 20. Snapshot / revision

Policy causally relevant snapshot может включать:

- policy/system revision;
- private recurrent state;
- stochastic RNG;
- exploration state;
- current candidate-generation state;
- pending deferral state;
- learned parameters/adapters.

Planner snapshot может включать:

- planner revision;
- active `PlanState`;
- search frontier/tree/graph, если он переносится между control points;
- branch lineage;
- cached evaluations;
- private recurrent/search state;
- Planner RNG;
- Cortex/World Model request provenance;
- intervention/degradation state.

Если search tree влияет на будущий choice и не сохранён, exact Agent clone не гарантируется.

---

# 21. Observability / intervention

Evidence Plane должен позволять проследить:

```text
candidate generation
→ candidate set
→ planning/search events
→ World Model rollout refs
→ plan creation/revision/invalidation
→ valuation/comparison refs
→ Policy selection attempt
→ deferral/fallback
→ SelectedActionIntent
```

Research interventions могут изменять:

- candidate set;
- candidate source;
- plan availability;
- plan ordering;
- Planner budget;
- plan assumptions;
- Value/Comparison evidence;
- Policy temperature/selection policy;
- constraint handling;
- selected intent напрямую как explicit intervention control.

Все treatment data сохраняют provenance.

---

# 22. Controls / baselines

## 22.1. Policy controls

Минимум:

```text
RandomPolicy
FixedRulePolicy
ReactivePolicy
ValueArgmaxControl
MatchedLearnedPolicy
OraclePolicy        research-only
```

`NoPolicy` допустим только как structural/failure configuration и не способен normal образом породить external behavior.

## 22.2. Planner controls

Минимум:

```text
NoPlanner
FixedPlan
RandomPlanner
ShuffledPlan
Depth1Planner
ReactiveLookaheadControl
MatchedSearchControl
OraclePlanner       research-only
```

## 22.3. Planner gate evaluation

Сравнивать:

```text
Policy + Planner
vs
Reactive Policy
vs
Policy + matched recurrent/search capacity
```

при matched actual compute/resource настолько, насколько возможно.

На core planning tasks измерять:

- long-horizon success;
- sample efficiency;
- plan validity;
- replanning frequency;
- robustness к model error;
- candidate quality/diversity;
- constraint/risk behavior;
- compute/performance frontier;
- generalization на unseen world instances/rule combinations.

Если benefit исчезает после matched controls, Planner boundary пересматривается.

---

# 23. Исследовательские гипотезы

`DU-23` открывает проверяемые гипотезы:

### H1 — explicit planning

На long-horizon compositional MicroWorld задачах Planner улучшает performance относительно reactive policy при сопоставимом compute.

### H2 — partial observability

Belief-conditioned contingent plans выигрывают у open-loop action sequences при скрытой информации.

### H3 — model error robustness

Receding/replanning policy устойчивее к ошибкам World Model, чем rigid long plan.

### H4 — Valuation separation

Изменение `ComparisonPolicy` при фиксированных candidates/plans предсказуемо изменяет Policy selection, не меняя World prediction.

### H5 — Planner semantics

Правильные plans превосходят shuffled/matched search controls, а не только добавляют recurrent/search capacity.

### H6 — Cortex assistance

Cortex-assisted candidate generation помогает semantic/compositional tasks, но benefit исчезает или уменьшается на задачах, где deterministic Planner уже имеет достаточную структуру.

---

# 24. Completion gate DU-23

`DU-23` считается завершённым, когда однозначно определены:

- обязательный Policy owner final behavioral selection;
- conditional/falsifiable Planner boundary;
- `ActionCandidate` и `PolicyCandidateSet`;
- `Plan ≠ ImaginedTrajectory`;
- Planner/World Model boundary;
- Policy/Valuation boundary;
- Policy/Executive boundary;
- partial-observability planning semantics;
- candidate generation;
- incomparability/constraints/deferral;
- stochastic Policy semantics;
- plan persistence/replanning;
- Cortex-assisted planning boundary;
- subgoal proposal boundary;
- `SelectedActionIntent` до Action Gate;
- failure/degradation;
- snapshot/revision;
- observability/intervention;
- reactive/Planner/matched controls;
- negative Planner gate.

После принятия `DU-23` допускается:

```text
DU-24 — Action Boundary / Gate / Executor
```
