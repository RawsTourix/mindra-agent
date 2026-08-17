# Candidate contract Metacognitive / Executive Control MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-22 — Metacognitive / Executive Control`

Этот документ уточняет machine-facing semantic формы `Executive Control` поверх accepted design [`../modules/executive-control.md`](../modules/executive-control.md).

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- конкретный controller NN;
- RL/supervised/meta-learning objective;
- Value-of-Computation formula;
- confidence threshold;
- exact resource units;
- exact scheduler implementation;
- Policy/Planner algorithm.

---

# 1. Архитектурная форма

```text
Committed CognitiveState
        +
ExecutiveState
        +
CognitiveResourceEnvelope
        +
MetaActionProposal[]
        +
ExecutiveObservation
        ↓
Executive Control
        ↓
ExecutiveDecision
        ↓
Scheduler validation
        ↓
selected internal operation(s)
```

`Executive Control` не получает direct handles на Memory/Cortex/World Model/Workspace providers.

---

# 2. ExecutiveSystemDescriptor

```text
ExecutiveSystemDescriptor
├── system_id
├── system_revision
├── policy_revision
├── supported proposal kinds
├── supported resource dimensions
├── supported deliberation dispositions
├── stateful capability
├── learned capability
├── batch/multi-proposal capability
├── snapshot capability
└── control/research flags
```

---

# 3. InternalOperationDescriptor

Описывает semantic operation, которую runtime composition разрешает Executive выбирать.

```text
InternalOperationDescriptor
├── operation_id
├── operation_kind
├── interface_revision
├── owner/provider boundary
├── required capabilities
├── prerequisites
├── allowed lifecycle phases
├── resource dimensions
├── concurrency/conflict metadata
├── degradation/availability semantics
└── provenance
```

Descriptor не содержит arbitrary live service object.

---

# 4. InternalOperationCatalog

```text
InternalOperationCatalog
├── catalog_id
├── catalog_revision
├── agent_revision
├── operation descriptors[]
├── compatibility metadata
└── provenance
```

Catalog является declarative capability surface, а не Service Locator.

---

# 5. MetaActionProposal

```text
MetaActionProposal
├── proposal_id
├── proposal_revision
├── operation_kind / operation_id
├── requester identity
├── base state_revision
├── agent_revision
├── target/context refs
├── semantic payload/request ref
├── prerequisites
├── required capabilities
├── estimated ResourceCostProfile
├── expected-benefit evidence?
├── uncertainty/support?
├── urgency/deadline?
├── allowed logical phase
├── proposal scope/lifetime
├── branch/mode provenance
└── source provenance
```

Proposal не означает reservation или execution.

---

# 6. CognitiveResourceEnvelope

```text
CognitiveResourceEnvelope
├── envelope_id
├── envelope_revision
├── scope
├── resource dimensions[]
├── hard/soft semantics
├── agent-visible cost semantics
├── validity interval / logical scope
├── issuer/provenance
└── intervention provenance?
```

Resource dimension conceptually:

```text
ResourceDimension
├── resource_kind
├── unit/semantic scale
├── granted amount
├── hard limit?
├── optional soft target?
└── compatibility/revision
```

`CognitiveResourceEnvelope` не обязан совпадать с physical machine resource telemetry.

---

# 7. ExecutiveBudgetLedger

```text
ExecutiveBudgetLedger
├── ledger_id
├── ledger_revision
├── envelope ref/revision
├── resource entries[]
├── reservations[]
├── consumed evidence[]
├── remaining state
├── reconciliation status
└── provenance
```

Для каждого resource kind должны быть различимы:

```text
available
reserved
consumed
remaining
unknown/unreconciled
```

---

# 8. ResourceCostProfile

```text
ResourceCostProfile
├── profile_id
├── operation/proposal ref
├── estimated dimensions[]
├── estimator identity/revision
├── support/uncertainty
├── assumptions
└── provenance
```

После operation может появиться:

```text
ActualResourceCost
├── operation execution ref
├── actual dimensions[]
├── provider/runtime evidence
├── estimate ref
├── estimate error
└── provenance
```

Estimated и actual cost не смешиваются.

---

# 9. ExecutiveObservation / MetaControlContext

Это read-only declared projection monitoring evidence.

```text
ExecutiveObservation
├── observation_id
├── base state_revision
├── executive_state_revision
├── current GoalFocusDirective?
├── Self Model refs/evidence
├── Salience refs/evidence
├── Workspace summary/ref?
├── World/uncertainty refs?
├── Valuation/risk/constraint refs?
├── recent operation outcomes/failures
├── current budget ledger ref
├── proposal set ref
├── missing/unavailable evidence states
└── provenance
```

Не требуется, чтобы все источники всегда присутствовали.

`ExecutiveObservation` не является ambient dump всего `CognitiveState`.

---

# 10. GoalFocusDirective

```text
GoalFocusDirective
├── directive_id
├── referenced committed goal IDs[]
├── focus mode / weights / ordering?  # exact semantics not frozen
├── scope
├── created_by ExecutiveDecision ref
├── base Goal Graph revision
└── provenance
```

Directive не изменяет Goal lifecycle/objective/commitment.

---

# 11. MetaActionRequest

Selected proposal преобразуется в scheduler-facing request.

```text
MetaActionRequest
├── request_id
├── selected proposal ref
├── operation descriptor ref
├── executive decision ref
├── base state_revision
├── reserved budget refs
├── allowed parameters/bounds
├── logical phase
├── branch/scope
└── provenance
```

Request ещё может быть отклонён Scheduler/runtime validation.

---

# 12. DeliberationDisposition

Нужно различать минимум semantics:

```text
continue_optional_cognition
yield_to_policy
budget_exhausted
degraded
blocked/failure
```

Точные enum names не frozen.

`yield_to_policy` не является `Action Commit`.

---

# 13. ExecutiveDecision

```text
ExecutiveDecision
├── decision_id
├── base state_revision
├── executive_system_revision
├── executive_policy_revision
├── executive_state_revision
├── operation_catalog_revision
├── resource envelope revision
├── budget ledger revision
├── considered proposal IDs[]
├── selected MetaActionRequest(s)[]
├── rejected/deferred proposal resolutions[]
├── budget reservation/allocation deltas
├── GoalFocusDirective?
├── deliberation disposition
├── monitoring/evidence refs
├── degradation/fallback provenance
├── branch/mode provenance
└── created-at logical identity
```

---

# 14. ProposalResolution

Не выбранный proposal должен по возможности иметь explicit resolution:

```text
ProposalResolution
├── proposal_id
├── status
├── reason class
├── budget/capability conflict refs?
├── stale/unavailable refs?
├── executive decision ref
└── provenance
```

Semantic reasons могут включать:

```text
selected
rejected
deferred
stale
unsupported
capability_unavailable
insufficient_budget
constraint_conflict
superseded
```

Exact taxonomy не frozen.

---

# 15. SchedulerResolution

После ExecutiveDecision runtime должен позволять связать request с фактическим execution outcome:

```text
SchedulerResolution
├── MetaActionRequest ref
├── validation status
├── scheduled execution segment ref?
├── rejection/failure reason?
├── actual provider/owner identity
├── base/commit state revisions
└── provenance
```

Так `Executive selected` и `operation executed` остаются разными фактами.

---

# 16. ExecutiveState

Если implementation stateful:

```text
ExecutiveState
├── state_revision
├── control history summary
├── GoalFocusDirective?
├── adaptive cost/benefit estimator state?
├── stopping/control recurrent state?
├── recent failure/degradation state?
├── budget ledger ref/state
├── last Executive Control Point
└── provenance
```

Concrete hidden latent остаётся module-private, если не опубликован declared probe.

---

# 17. ExecutiveControlPoint

```text
ExecutiveControlPoint
├── control_point_id
├── Decision Window / Cognitive Cycle refs
├── base committed state_revision
├── allowed operation catalog revision
├── envelope/ledger refs
├── phase identity
└── provenance
```

Decision принимается только относительно committed state.

---

# 18. ExecutiveSnapshot

```text
ExecutiveSnapshot
├── executive descriptor revisions
├── ExecutiveState
├── ExecutiveBudgetLedger
├── resource envelope refs/state
├── pending reservations
├── causally relevant pending proposals
├── GoalFocusDirective
├── operation catalog revision
├── private learned/recurrent state
├── adaptive estimator state
├── RNG
├── degradation/intervention state
└── compatibility metadata
```

---

# 19. Failure/degradation contract

Machine-facing semantics должна позволять различить:

```text
invalid proposal
unsupported operation
capability unavailable
hard budget exhausted
reservation failure
actual cost overrun
Scheduler rejection
provider failure
stale result
controller failure
invalid ExecutiveDecision
```

Нельзя заменять failure fake-success payload.

---

# 20. Observability requirements

Минимальный trace должен связывать:

```text
ExecutiveControlPoint
→ ExecutiveObservation
→ considered MetaActionProposal[]
→ ExecutiveDecision
→ MetaActionRequest[]
→ SchedulerResolution
→ operation result/failure
→ ActualResourceCost
→ new ledger/state revision
```

---

# 21. Intervention requirements

Интервенции должны иметь targets класса:

```text
resource envelope / budget ledger
operation cost estimate
proposal availability
Self competence evidence
uncertainty evidence
Salience evidence
GoalFocusDirective
forced/forbidden MetaAction
forced stop/continue
capability availability/degradation
Executive policy/control implementation
```

Все interventions используют `Intervention Gateway` и сохраняют lineage/provenance.

---

# 22. Control configurations

Contract должен позволять first-class configurations:

```text
NoExecutive
FixedScheduleExecutive
FixedBudgetExecutive
RandomMetaActionExecutive
SimpleThresholdExecutive
SalienceOnlyExecutive
CostUnawareExecutive
MatchedLearnedRouterControl
OracleBudgetAllocationControl
```

Конкретные class names не frozen.

---

# 23. Invariants, пригодные для future automatic checks

Future validation/tests должны проверять, где применимо:

- `ExecutiveDecision.base_state_revision` соответствует control point;
- selected operation существует в catalog revision;
- selected proposal входит в considered candidate set;
- hard resource reservation не превышает available envelope;
- proposal/request не исполняется в запрещённой lifecycle phase;
- Executive не получает direct provider handle через contract;
- GoalFocusDirective ссылается только на допустимые committed goals или явно корректно обрабатывает stale refs;
- `yield_to_policy` не создаёт Environment Action;
- simulated branch ledger не коммитится как real ledger;
- actual cost reconciles reservation/ledger explicit способом;
- hidden fallback невозможен без degradation provenance.

---

# 24. Что остаётся открытым до version design

Не frozen:

- exact operation kinds первой версии;
- resource units;
- proposal ranking/comparison policy;
- learned controller architecture;
- Value-of-Computation estimator;
- stopping rule;
- budget refill policy;
- default control-point frequency;
- parallel meta-action selection;
- exact GoalFocus representation;
- Policy/Planner integration details;
- Python types/serialization.
