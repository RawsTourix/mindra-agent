# Candidate contract Goal System MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-09 — Goal System`

Этот документ уточняет machine-facing классы данных и capability, необходимые будущей реализации Goal System.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- concrete graph library;
- exact enum identifiers;
- exact Goal DSL;
- serialization encoding;
- numerical representation priority/commitment/progress.

Приоритет семантики имеет [`../modules/goals.md`](../modules/goals.md).

---

# 1. Основные capability surfaces

Future Goal System должна уметь выразить операции класса:

```text
submit goal proposal
validate/adopt/reject proposal
transition committed goal lifecycle
modify graph relations through authorized transition
publish committed Goal state
inspect goal state/evidence
snapshot/restore private goal-system state where required
```

Research-facing interventions остаются отдельной privileged capability по `DU-06`.

---

# 2. Goal Proposal

Conceptually:

```text
GoalProposal
├── proposal_id
├── objective_specification
├── source_kind
├── source_identity/provenance
├── requested_scope
├── requested_parent/dependencies?
├── requested_structural_priority?
├── requested_commitment?
├── source_context/evidence?
├── causal identities
└── intervention provenance?
```

Proposal не имеет `goal_id`, пока не принят Goal System.

Proposal может завершиться состоянием класса:

```text
accepted
rejected
deferred
invalid
```

Точная lifecycle proposal не frozen.

---

# 3. Committed Goal record

Conceptually:

```text
CommittedGoal
├── goal_id
├── objective_specification
├── objective_semantics/type
├── source/provenance
├── scope
├── lifecycle_status
├── structural_priority
├── commitment
├── progress
├── satisfaction/failure/expiry semantics references
├── created_at causal identity
├── last_transition causal identity
└── intervention provenance?
```

`goal_id` идентифицирует конкретный goal instance, а не generic objective.

---

# 4. Goal Graph

Published Goal state должен позволять выразить:

```text
GoalGraph
├── goals[goal_id]
├── parent_subgoal_relations[]
├── dependency_relations[]
└── conflict_relations[]
```

## Dependency constraints

Goal dependency graph должен быть валидируемым и ацикличным в пределах одной committed revision.

Conflict relation не обязана иметь DAG semantics, потому что это не execution dependency.

Graph mutation проходит как owner-scoped staged update Goal System.

---

# 5. Lifecycle transition request

Conceptually внешний authorized producer может создать request класса:

```text
GoalTransitionRequest
├── target_goal_id
├── requested_transition
├── reason/source
├── supporting evidence references?
├── base_state_revision
├── causal identity
└── intervention provenance?
```

Запрос не является committed transition до validation Goal System.

Goal System должна проверить:

- identity;
- source authority;
- lifecycle transition legality;
- scope;
- graph invariants;
- stale-base semantics;
- required evidence/provenance.

---

# 6. Candidate lifecycle semantics

Contract должен сохранять различия как минимум между:

```text
pending
active
suspended
achieved
failed
abandoned
expired
invalidated
```

Нельзя collapsing:

```text
suspended → inactive boolean
failed + expired + abandoned → done
```

без потери семантики.

---

# 7. Scope

Goal record должен поддерживать как минимум:

```text
episode-scoped
session-scoped
agent-long-lived
```

При Episode end Goal System должна иметь достаточную causal information, чтобы корректно обработать goal согласно `terminated`/`truncated` и scope semantics.

---

# 8. Goal objective semantics

Candidate contract должен допускать objective classes типа:

```text
achievement
maintenance
avoidance/prevention
```

Но exact DSL/predicate representation пока не frozen.

Goal objective не может ссылаться на research-only Environment field, если этот field недоступен normal Agent runtime.

---

# 9. Priority

Contract должен уметь выразить **structural/declarative priority metadata** отдельно от future dynamic valuation.

Priority может быть:

- отсутствующей;
- ordered class/rank;
- structured constraint;
- другим future representation.

Exact numeric form не frozen.

Нельзя требовать, чтобы priority автоматически была scalar utility.

---

# 10. Commitment

Contract должен позволять отличить persistent adoption цели от текущего focus.

Commitment state/metadata должна быть доступна lifecycle policy и observability, но exact scalar/discrete form пока не frozen.

`commitment` не равно `priority` и не равно `value`.

---

# 11. Progress

Progress representation должна поддерживать как минимум semantic варианты:

```text
unknown
not_applicable
milestone/structured state
quantitative estimate
```

Universal `[0,1]` scalar не обязателен.

Progress должен иметь provenance достаточную, чтобы отличить directly verified и inferred state.

Research-only Objective Task Metric не является допустимым normal progress source без explicit task visibility.

---

# 12. Goal state publication

Goal System должна публиковать canonical surface через `CognitiveState` с owner-scoped semantics.

Exact namespace не frozen.

Downstream consumer должен иметь возможность объявить dependencies на категории класса:

```text
active goal set
specific goal record
goal graph relations
lifecycle status
scope
priority metadata
commitment state
progress state
```

Наличие full private Goal System object не является prerequisite consumer access.

---

# 13. Goal source adapters

Architecture должна допускать adapters/providers для sources класса:

```text
StructuredExternalTaskGrounder
CortexGoalGrounder
InternalGoalProposalProvider
PlannerSubgoalProvider
ScriptedGoalProvider
```

Это conceptual roles, не frozen class names.

Все они возвращают `GoalProposal`/transition proposal через stable boundary и не получают direct Goal Graph mutation access.

---

# 14. Research probes

Goal System должна предоставлять declared read-only evidence/probe surface, достаточную для получения:

- proposal history/status;
- committed goal records;
- graph relations;
- lifecycle transition history;
- structural priority;
- commitment;
- progress;
- source/provenance;
- rejection/validation reasons в research-visible форме.

Research-only diagnostic reason не становится normal cognitive input автоматически.

---

# 15. Intervention capability

Candidate research capability должна уметь выразить controlled operation класса:

```text
inject proposal
force adoption/rejection
force lifecycle transition
alter structural priority
alter commitment
replace objective
add/remove dependency
add/remove parent-subgoal relation
add/remove conflict relation
```

Каждая intervention обязана иметь:

```text
intervention_id
base causal revision
target
treatment
provenance
```

и следовать branch/intervened-lineage semantics `DU-06`.

---

# 16. Snapshot / restore

Если Goal System имеет causally relevant private state, полный Agent Snapshot позднее должен его захватывать.

Минимально restore должен сохранять:

- Goal Graph;
- goal identities;
- lifecycle statuses;
- scope;
- priority/commitment/progress;
- source/provenance;
- causally relevant private proposal/transition state;
- RNG state, если Goal System когда-либо использует stochastic decision logic.

Точный serialization format определяется `DU-27`.

---

# 17. Candidate errors / invalid states

Future contract должен различать минимум:

```text
invalid proposal schema
unauthorized source
invalid lifecycle transition
unknown goal identity
stale-base transition
cyclic dependency insertion
invalid scope transition
unsupported objective semantics
conflicting concurrent owner updates
```

Нельзя молча чинить graph/lifecycle через last-write-wins.

---

# 18. Что остаётся открытым

До последующих DU не frozen:

- exact Goal DSL;
- natural-language grounding;
- internal goal generation;
- feasibility estimator;
- dynamic desirability/value;
- focus arbitration;
- automatic decomposition algorithm;
- exact conflict-resolution policy;
- training/losses;
- concrete Python types/library.
