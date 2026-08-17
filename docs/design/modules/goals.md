# Goal System MINDRA

## Статус документа

**Design Update:** `DU-09 — Goal System`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет:

- семантику цели внутри MINDRA;
- границу между `External Task Specification` и внутренней целью;
- `Goal Proposal` и authority принятия цели;
- `Committed Goal` и `Goal Graph`;
- lifecycle цели;
- scope/persistence;
- parent/subgoal/dependency/conflict semantics;
- различие priority, commitment, progress и future valuation;
- правила externally assigned и internally generated goals;
- observability/intervention/ablation requirements Goal System.

Документ опирается на:

- [`environment.md`](environment.md) — `External Task Specification` является внешней task boundary и не равна internal Goal;
- [`perception.md`](perception.md) — текущий percept отделён от task/goal semantics;
- [`../cognitive-state.md`](../cognitive-state.md) — published Goal state должен иметь owner/provenance/scope/revision semantics;
- [`../module-lifecycle.md`](../module-lifecycle.md) — Goal System участвует в общем scheduler/lifecycle и не мутирует committed state напрямую;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — passive Goal evidence отделено от active Goal intervention.

Документ намеренно **не** определяет:

- exact Python API;
- конкретный контейнер/DSL целей;
- natural-language parser;
- конкретный Cortex backend — это `DU-10`;
- Memory mechanics — это `DU-11`;
- feasibility prediction через World Model — это `DU-12`;
- competence/self-feasibility через Self Model — это `DU-13`;
- механизм autonomous goal generation из intrinsic signals/drives — это `DU-14/15`;
- эмоциональную оценку цели — `DU-16/17`;
- математическую ценность/utility цели — `DU-18`;
- attention/focus policy — `DU-19/22`;
- Policy/Planner — `DU-23`;
- training algorithm — `DU-26`.

---

# 1. Цель DU-09

MINDRA должна иметь явный ответ на вопрос:

> **Что именно Agent в данный момент стремится достичь, изменить, сохранить или предотвратить?**

Этот ответ не должен скрываться внутри:

- reward;
- prompt Cortex;
- Policy hidden state;
- Environment task object;
- Drives;
- Valuation;
- planner scratchpad.

Поэтому принимается отдельная ответственность `Goal System`.

Ключевые отношения:

```text
External Task Specification
≠
Goal Proposal
≠
Committed Goal
```

```text
Goal
≠
Reward
≠
Drive
≠
Utility / Value
≠
Policy
```

---

# 2. Что такое Goal

`Goal` — agent-owned декларативное представление желаемого ограничения на будущую траекторию/состояние/результат, способное влиять на последующее cognition и выбор поведения.

Goal описывает **что считается целевым**, но не обязан сам определять:

- насколько это ценно относительно других целей;
- какое действие выполнить;
- каким планом достичь результата;
- насколько задача выполнима;
- какой reward использовать для обучения.

Goal может соответствовать не только конечному достижению состояния.

Минимально дизайн должен допускать цели класса:

```text
achievement
→ добиться условия

maintenance
→ сохранять условие в допустимом диапазоне/интервале

avoidance / prevention
→ не допустить условия/события
```

Точный enum/DSL goal semantics пока не frozen.

Главный смысл — Goal должен уметь выразить как "изменить", так и "сохранить/не допустить".

---

# 3. Goal System как отдельная ответственность

Goal System принимается как отдельная когнитивная ответственность MINDRA.

Он отвечает за:

- приём goal proposals через declared boundaries;
- validation proposal semantics/provenance;
- принятие/adoption цели;
- создание стабильной goal identity;
- хранение canonical active/inactive/terminal goal state;
- goal lifecycle transitions;
- scope/persistence;
- parent/subgoal/dependency relations;
- structural conflict metadata;
- goal completion/failure/expiry/abandonment state;
- contract-defined progress state;
- publication Goal state в `CognitiveState`;
- Goal-related evidence/probes/interventions.

Goal System **не** отвечает за:

- генерацию всех внутренних желаний сам по себе;
- вычисление общей desirability/utility;
- action selection;
- long-horizon planning;
- hidden Environment oracle evaluation;
- language understanding как обязательный механизм;
- automatic feasibility proof;
- reward shaping.

---

# 4. Authority: Proposal отдельно от Commitment

MINDRA принимает двухступенчатую модель:

```text
Goal Source
    ↓
Goal Proposal
    ↓
Goal System validation/adoption
    ↓
Committed Goal
```

## 4.1. Goal Proposal

`Goal Proposal` — кандидат на цель, который ещё **не является** частью committed Goal state Agent.

Proposal conceptually содержит:

- proposed objective/specification;
- source/provenance;
- requested scope;
- requested structural priority/constraint metadata, если применимо;
- parent/dependency relation, если применимо;
- source-specific evidence/context;
- proposal identity.

Proposal может быть отклонён, отложен или принят.

## 4.2. Кто может предлагать цели

Архитектура должна допускать источники класса:

```text
External Task Ingress
Future Cortex / language grounding
Future Drives / intrinsic-goal generator
Future Executive Control / Planner decomposition
Research Intervention Gateway
Explicit scripted baseline/control source
```

Наличие capability `propose goal` **не даёт write authority** на committed Goal namespace.

## 4.3. Единственный semantic owner

Goal System является semantic owner canonical Goal state.

Ни Cortex, ни Drives, ни Policy, ни evaluator не должны напрямую мутировать committed goal records normal runtime способом.

Research intervention остаётся отдельной privileged operation по правилам `DU-06` и сохраняет intervention provenance.

---

# 5. External Task Specification ingress

`External Task Specification` принадлежит Environment interaction contract.

Она не становится Goal простым alias/reference.

Правильная граница:

```text
External Task Specification
       ↓
Task-to-Goal ingress / grounding
       ↓
Goal Proposal
       ↓
Goal System
       ↓
Committed Goal
```

Для structured MicroWorld task specification grounding может быть deterministic и rule-based.

Для natural-language instruction позднее может использоваться Cortex или другой parser/grounder, но это не меняет Goal semantics.

Ключевой invariant:

```text
natural-language instruction
≠
canonical Goal representation
```

Текст может быть источником goal proposal, но не является canonical Goal только потому, что лежит в prompt.

---

# 6. Externally assigned и internally generated goals

Goal provenance должна различать источник цели.

Минимально требуются категории происхождения класса:

```text
external_task
internal_generated
planner_subgoal
operator/scripted_control
research_intervention
```

Точные identifiers уточняются contract.

## 6.1. Externally assigned goal

Возникает из agent-visible внешней task specification.

Внешний источник может иметь authority требовать определённый objective, но внутреннее canonical состояние цели всё равно принадлежит Goal System.

## 6.2. Internally generated goal

Возникает из agent-owned механизма.

`DU-09` **не определяет механизм генерации** таких целей.

Будущие Drives/Intrinsic/Executive components смогут создавать proposal через тот же semantic boundary.

Это позволяет исследовать autonomous goal formation без отдельной скрытой ветки архитектуры.

## 6.3. Planner-generated subgoal

Будущий Planner может предложить промежуточную цель, но не получает право самостоятельно переписывать Goal Graph.

Subgoal adoption остаётся контролируемым Goal System transition.

---

# 7. Committed Goal

`Committed Goal` — принятая Goal System цель со стабильной semantic identity и lifecycle state.

Conceptually goal record должен позволять выразить:

```text
goal_id
objective/specification
objective semantics/type
source/provenance
scope
lifecycle status
structural priority metadata
commitment metadata
progress state
success condition / satisfaction semantics
failure condition?
expiry condition?
parent relation?
dependencies?
conflicts?
created_at causal identity
last_transition causal identity
intervention provenance?
```

Точная machine-facing форма определяется candidate contract.

---

# 8. Goal identity

`goal_id` означает identity **конкретного committed goal instance**.

Он не должен равняться:

- тексту instruction;
- hash одного objective без lifecycle context;
- Environment hidden task ID;
- Python object identity;
- planner node memory address.

Две семантически похожие цели могут быть разными instances:

```text
Goal G1: найти воду в Episode 3
Goal G2: найти воду в Episode 8
```

И наоборот, одна session-scoped goal может пережить несколько Episodes без получения нового identity.

Goal identity должна быть пригодна для provenance, Memory, evaluation и graph relations.

---

# 9. Lifecycle цели

MINDRA принимает явный lifecycle вместо implicit boolean `done`.

Conceptually различаются состояния:

```text
proposed          -- ещё не committed Goal

committed states:
  pending         -- принята, но ещё не активна/не готова к pursuit
  active          -- является текущей допустимой целью pursuit
  suspended       -- временно сохранена, но не pursued

terminal states:
  achieved        -- satisfaction/success semantics выполнены
  failed          -- зафиксировано goal-defined failure condition
  abandoned       -- Agent/authority осознанно прекратил commitment
  expired         -- scope/deadline/context завершился без claim failure
  invalidated     -- цель больше невалидна из-за contract/context change
```

Точные названия enum могут быть уточнены позднее; семантические различия обязательны.

## 9.1. `failed` не равно `expired`

Например, Episode был truncated по research budget.

Незавершённая episode-scoped цель не должна автоматически становиться `failed`.

Она может стать `expired`/interrupted согласно scope semantics.

Это сохраняет различие `terminated`/`truncated` из `DU-07`.

## 9.2. `suspended` не равно `abandoned`

Suspension сохраняет commitment/identity и допускает возврат.

Abandonment является терминальным отказом от данного goal instance.

## 9.3. Terminal history не стирается

Переход цели в terminal state должен оставаться доступен research evidence/trajectory и не удаляться как будто цели никогда не существовало.

Historical retention policy определится позднее Memory/Data design.

---

# 10. Scope и persistence

Goal имеет semantic scope, согласованный с temporal model.

Минимально допускаются:

```text
episode-scoped
session-scoped
agent-long-lived
```

`cycle-scoped`/`decision-scoped` objective обычно лучше рассматривать как transient planning intent, а не полноценную durable Goal; исключения требуют отдельной justification.

## 10.1. Episode reset

```text
Environment.reset()
≠
clear all goals
```

Episode-scoped goals должны завершить lifecycle согласно termination/truncation/scope policy.

Session-scoped и agent-long-lived goals могут переживать reset.

## 10.2. Persistent goal не равна Memory record

Goal state является active agent-owned control state.

Memory позднее может хранить историю целей, но Memory не становится owner текущего Goal lifecycle.

---

# 11. Goal Graph вместо Goal Stack

MINDRA не принимает один LIFO `goal stack` как универсальную модель.

Канонически используется **Goal Graph**.

Conceptually:

```text
Goal Graph
├── Goal nodes
├── parent/subgoal relations
├── dependency relations
└── conflict relations
```

## 11.1. Иерархия

Goal может иметь parent и subgoals.

Но:

```text
subgoal achieved
≠
parent automatically achieved
```

если decomposition semantics явно не утверждает такое правило.

Parent satisfaction определяется собственной goal semantics либо явно принятым decomposition rule.

## 11.2. Dependencies

Можно выразить:

```text
G2 depends_on G1
```

То есть pursuit/activation G2 требует определённого состояния G1.

Execution/dependency relation committed Goal Graph должна быть ацикличной в рамках одного goal instance graph.

Рекуррентные/повторяющиеся жизненные цели выражаются новыми instances/temporal rules, а не скрытым dependency cycle.

## 11.3. Несколько родителей

Design не запрещает одному subgoal поддерживать несколько higher-level goals.

Поэтому graph предпочтительнее дерева/стека.

---

# 12. Conflict semantics

MINDRA различает:

```text
structural conflict
≠
dynamic conflict
≠
valuation trade-off
```

## 12.1. Structural conflict

Явно заданная несовместимость objective/constraint semantics.

Например, две цели могут требовать взаимоисключающих terminal states.

Goal System может хранить такой conflict relation.

## 12.2. Dynamic conflict

Конфликт, который возникает только в конкретном состоянии мира/ресурсов.

Его полноценное обнаружение может требовать World Model/Self Model и поэтому не принадлежит целиком DU-09.

## 12.3. Resolution

Goal System не должен автоматически сводить все конфликты к "побеждает больший scalar priority".

Будущие Valuation/Executive/Policy mechanisms смогут участвовать в arbitration.

Goal System сохраняет canonical lifecycle/relations и применяет только явно разрешённые transition decisions.

---

# 13. Priority отдельно от Value

Понятие priority необходимо, но его нельзя смешивать с будущей internal utility.

MINDRA различает:

```text
structural/declarative goal priority
≠
dynamic goal value/desirability
```

## 13.1. Structural priority

Может отражать:

- external task precedence;
- safety/contract constraint;
- ordering requirement;
- явно заданный scheduling class.

Она является metadata Goal System.

## 13.2. Dynamic value

Насколько Agent **сейчас** предпочитает продвигать конкретную цель с учётом Drives, Appraisal, Affect, expected outcome и других факторов — ответственность будущего `DU-18 Valuation`.

Следовательно:

```text
goal.priority = high
```

не означает автоматически:

```text
goal.utility = максимальная
```

---

# 14. Commitment отдельно от Priority

`Commitment` — степень/состояние устойчивости принятого намерения продолжать считать цель принятой несмотря на локальные изменения ситуации.

В DU-09 commitment является **lifecycle/control semantics**, а не человеческим чувством.

Он нужен, чтобы отличать:

```text
эта цель сейчас не в фокусе
```

от:

```text
эта цель больше не является моей целью
```

Commitment может влиять на допустимость `suspend`/`abandon` transitions, но точная математическая форма пока не фиксируется.

Не допускается скрытая реализация:

```text
commitment = scalar reward weight
```

без последующего design.

---

# 15. Goal Focus отдельно от Goal Existence

Agent может иметь несколько одновременно committed/active целей.

Поэтому:

```text
active goals
≠
one focused goal
```

DU-09 не требует единственного `current_goal`.

Future Executive Control/Policy сможет выбирать focus/attention subset, но Goal System должен хранить полный committed active set.

Это предотвращает потерю долгосрочной цели при временном переключении внимания.

---

# 16. Progress semantics

Progress нужен для мониторинга, но не должен становиться универсальным hidden reward.

MINDRA **не требует**, чтобы каждая цель имела scalar:

```text
progress ∈ [0, 1]
```

Progress может быть:

- discrete milestone state;
- structured set выполненных conditions;
- interval/distance estimate;
- `unknown`;
- `not_applicable` для некоторых goal types.

## 16.1. Источник progress

Goal progress может вычисляться только из agent-visible/agent-owned information и declared inference capabilities.

Research-only `Objective Task Metric` нельзя использовать как runtime goal progress, если он не раскрыт Agent task contract.

## 16.2. Progress не равен success

Высокая оценка progress не переводит цель в `achieved`, если satisfaction semantics не выполнена.

## 16.3. Progress provenance

Нужно отличать:

```text
directly verifiable progress
inferred progress
predicted future progress
unknown progress
```

Predicted future progress позднее принадлежит World Model/Planner, а не должен маскироваться под текущий Goal state.

---

# 17. Satisfaction и failure semantics

Goal должна иметь определяемую или проверяемую completion semantics.

При этом Goal System не получает Environment oracle автоматически.

Для reference MicroWorld goal satisfaction может оцениваться по agent-visible/canonical state там, где задача это позволяет.

Если истинный успех по design раскрывается только через explicit Environment feedback, Goal System использует именно этот разрешённый сигнал.

Нельзя:

```text
Objective Task Metric
→ secretly mark goal achieved
```

если metric research-only.

Для maintenance/avoidance goals satisfaction может быть temporal, поэтому понятие `achieved` может применяться только на определённой terminal/commit boundary.

Exact goal predicate/temporal DSL определяется позднее.

---

# 18. Goal transition authority

Различные компоненты могут **предлагать** transition:

```text
activate
suspend
resume
abandon
create subgoal
mark candidate completion
```

Но canonical lifecycle transition проходит через Goal System validation/commit.

Goal System проверяет минимум:

- существование goal identity;
- допустимость lifecycle transition;
- scope;
- graph invariants;
- source authority;
- required evidence/provenance;
- conflict с текущей committed revision.

Это предотвращает scattered direct mutation из Policy/Cortex/Planner.

---

# 19. Goal System и Scheduler

Goal System является когнитивным модулем/ответственностью, исполняемым через общий `Cognitive Scheduler`.

Он не должен самостоятельно рекурсивно вызывать Cortex, Policy или Planner.

Если grounding/decomposition требует другой capability:

```text
upstream module produces proposal
      ↓ commit
Goal System consumes proposal
```

через declared dependencies/waves.

Feedback loop выражается через последующие state revisions, а не direct peer calls.

---

# 20. Goal state в CognitiveState

Точный namespace не frozen, но canonical published surface должна позволять downstream modules читать минимум:

- committed goal identities;
- objective/specification references;
- lifecycle status;
- scope;
- graph/dependency relations;
- structural priority metadata;
- commitment state/metadata;
- progress state;
- provenance;
- availability/freshness.

Private implementation state Goal System не должен становиться автоматически общим CognitiveState.

---

# 21. Goal observability

Evidence Plane должен позволять восстановить:

- proposal creation;
- source/provenance;
- accept/reject decision;
- goal identity creation;
- lifecycle transition;
- parent/subgoal/dependency change;
- conflict relation change;
- progress update;
- scope expiry;
- terminal transition;
- intervention.

Важно различать:

```text
proposal rejected
≠
goal adopted then abandoned
```

и:

```text
goal suspended
≠
goal terminal
```

---

# 22. Goal interventions

Evaluation Runtime должна иметь возможность через `Intervention Gateway` проводить controlled operations класса:

```text
inject Goal Proposal
force adopt goal
activate / suspend goal
alter structural priority
alter commitment metadata
replace goal objective
inject/remove dependency relation
mark conflict relation
```

Точная capability matrix определяется candidate contract.

Intervention:

- имеет `intervention_id`;
- привязывается к base causal revision;
- сохраняет semantic owner Goal System;
- создаёт intervention provenance;
- предпочтительно выполняется в forked treatment lineage для confirmatory experiment.

Произвольное редактирование Goal object reference запрещено.

---

# 23. Ablation и controls

Goal System должен быть независимо проверяем.

Минимально полезны будущие конфигурации:

```text
StructuredExternalGoalSystem
→ принимает только детерминированно grounded external goals

NoInternalGoalGeneration
→ внутренние proposal sources отсутствуют, external goals работают

SingleGoalControl
→ допускается только одна активная goal instance

FlatGoalControl
→ subgoal/dependency decomposition отключена

NoCommitmentControl
→ persistence/commitment semantics минимизирована
```

Это candidate control families, а не frozen implementation names.

Полное `NoOp Goal System` допустимо только для task configurations, где отсутствие goals не нарушает downstream required contracts; иначе baseline должен использовать минимальную structured goal implementation.

---

# 24. Goal System и будущие модули

## Cortex (`DU-10`)

Cortex может:

- интерпретировать natural-language instruction;
- предложить grounded goal;
- предложить decomposition/subgoal.

Но Cortex не является owner Goal state.

## Memory (`DU-11`)

Memory может хранить прошлые goals/attempts/outcomes.

Но retrieval не меняет текущую Goal автоматически.

## World Model (`DU-12`)

Может оценивать достижимость и последствия pursuit.

Но prediction не является lifecycle transition Goal.

## Self Model (`DU-13`)

Может оценивать собственную competence/cost для цели.

Но competence не определяет факт существования цели.

## Intrinsic Signals / Drives (`DU-14/15`)

Могут участвовать в autonomous goal proposal/selection pressure.

Но не получают direct Goal write authority.

## Valuation (`DU-18`)

Определяет dynamic relative value/desirability, не semantic identity цели.

## Executive Control (`DU-22`)

Может предлагать focus/suspension/resumption и compute allocation в рамках contracts.

## Policy / Planner (`DU-23`)

Потребляет Goal state и может предлагать subgoals/plans, но не скрывает Goal state внутри planner scratchpad.

---

# 25. Исследовательские гипотезы, поддерживаемые design

DU-09 должен позволить позднее проверить как минимум:

1. повышает ли explicit persistent Goal state выполнение long-horizon задач относительно prompt/policy-only baseline;
2. помогает ли subgoal graph без изменения внешнего reward;
3. влияет ли commitment на устойчивость pursuit после distractor events;
4. может ли Agent сохранять session-scoped goal между Episodes;
5. отличается ли externally assigned goal от internally generated goal при одинаковом objective;
6. как goal conflict/arbitration меняется при подключении будущих Drives/Valuation;
7. сохраняется ли поведение при замене Cortex, если Goal representation остаётся той же.

Эти пункты являются design affordances, а не уже подтверждёнными claims.

---

# 26. Completion gate DU-09

DU-09 считается завершённым, если:

- Goal отделена от Task Specification, Reward, Drive, Value и Policy;
- принят единый semantic owner Goal state;
- Proposal отделён от Committed Goal;
- external/internal/planner/research provenance различимы;
- lifecycle имеет явные nonterminal/terminal состояния;
- `failed`, `expired`, `abandoned`, `suspended` не смешаны;
- scope across Episode/Session определён;
- Goal Graph принят вместо обязательного stack;
- dependency graph не допускает скрытые cycles;
- structural priority отделена от future dynamic Valuation;
- commitment отделён от priority/value;
- progress не требует universal scalar и не использует evaluator-only metric;
- несколько active goals разрешены;
- Goal observability/intervention semantics определены;
- downstream modules получают стабильную semantic surface без ownership leakage.

После этого допускается `DU-10 — Cortex Boundary`.
