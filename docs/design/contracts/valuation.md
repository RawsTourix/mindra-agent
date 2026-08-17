# Candidate contract Valuation MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-18 — Valuation`

Этот документ уточняет machine-facing semantic формы будущего `Valuation System`.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- concrete ValueComponent taxonomy первой версии;
- mandatory scalar value;
- exact scalarization/weights;
- Pareto/lexicographic/Tchebycheff/CVaR как universal algorithm;
- discount factor;
- critic architecture;
- training reward/loss;
- Policy implementation.

Приоритет имеет [`../modules/valuation.md`](../modules/valuation.md).

---

# 1. Архитектурная форма

Future implementation должна поддерживать agent-owned `Valuation System`, который строит typed `ValueProfile` для causally identified targets и сравнивает profiles только через explicit versioned `ComparisonPolicy`.

Conceptually:

```text
ValuationSystem
├── descriptor
├── component providers/mappers
├── comparison policy set
├── optional risk/constraint estimators
├── optional learned/adaptive state
└── evaluate / compare / inspect / snapshot / restore
```

Valuation не выполняет final action selection.

---

# 2. ValuationSystemDescriptor

Conceptually:

```text
ValuationSystemDescriptor
├── system_id
├── system_revision
├── supported target kinds
├── component schema revisions
├── supported comparison policies
├── risk/constraint capabilities
├── distributional-value capability
├── learned/fixed capability
├── Cortex-assisted capability
├── snapshot capability
└── research/control flags
```

Descriptor не является текущей valuation.

---

# 3. ValuationTarget

Conceptually:

```text
ValuationTarget
├── target_id
├── target_kind
├── causal_mode
├── base_state_revision
├── decision_id?
├── branch_id?
├── source state/outcome/action/trajectory refs
├── horizon
├── World Model revision?, если predicted/imagined
├── internal-simulation mode?
└── provenance
```

Target kinds должны позволять минимум:

```text
state / belief
outcome
action_candidate
trajectory / plan branch
counterfactual branch
```

`causal_mode` различает actual/predicted/imagined/retrospective/intervened/counterfactual/offline.

---

# 4. ValuationRequest

Conceptually:

```text
ValuationRequest
├── request_id
├── target
├── context references
├── requested component families
├── requested risk/constraint views?
├── requested comparison policy?
├── horizon / temporal mode
├── allowed optional capabilities
└── provenance
```

Request не даёт Valuation ambient access ко всему Agent state.

---

# 5. ValueComponent

Conceptually:

```text
ValueComponent
├── component_id
├── component_kind
├── semantic_subject_id?       # Goal/Drive/etc.
├── raw value / structured relation / distribution
├── units / semantic scale
├── directionality semantics?
├── source references
├── estimator/mapping revision
├── normalization state?
├── confidence/support?
├── availability/status
└── provenance
```

`component_kind` может относиться к Goal impact, Drive regulation, effort/cost, feedback contribution, exploration/learning value или другой принятой semantics.

Одинаковый numeric dtype/shape не означает общую валюту.

---

# 6. GoalValueComponent

Должен сохранять конкретный `goal_id`.

Conceptually:

```text
GoalValueComponent
├── goal_id
├── relation / expected progress
├── completion/failure implications?
├── horizon
├── Goal revision
├── source Appraisal/World refs
└── support/provenance
```

Несколько Goals не scalarize автоматически.

---

# 7. DriveValueComponent

Conceptually:

```text
DriveValueComponent
├── drive_id
├── current Drive revision
├── predicted regulatory change
├── horizon
├── source prediction/appraisal refs
└── support/provenance
```

Current pressure не является готовой Utility.

---

# 8. ExternalFeedbackComponent

Если External Task Feedback включается в valuation:

```text
ExternalFeedbackComponent
├── feedback source/reference
├── agent-visible semantics
├── mapping_id
├── mapping_revision
├── transformed contribution
└── provenance
```

Без explicit mapping feedback не становится value component автоматически.

Evaluator-only metric недопустим natural способом.

---

# 9. IntrinsicSignalValueComponent

Если Intrinsic Signal включается:

```text
IntrinsicSignalValueComponent
├── signal reference
├── provider/reference scope revision
├── mapping_id
├── mapping_revision
├── context-conditioned contribution
└── provenance
```

Signal magnitude не равна desirability.

---

# 10. FeasibilityProfile

Conceptually:

```text
FeasibilityProfile
├── target/action reference
├── P(success)?
├── capability requirements
├── known limitations
├── expected effort?
├── expected resource cost?
├── Self Model revision
├── estimate support
└── provenance
```

Feasibility не scalarize в value автоматически.

---

# 11. ConstraintProfile

Conceptually:

```text
ConstraintProfile
├── constraints[]
│   ├── constraint_id
│   ├── semantic source
│   ├── threshold/rule
│   ├── predicted satisfaction/violation
│   ├── hard/soft/unknown semantics
│   └── support/provenance
└── overall status?             # только если policy определяет
```

Hard constraint не должен превращаться в большой отрицательный weight без explicit design.

---

# 12. RiskProfile

Conceptually:

```text
RiskProfile
├── risk_profile_id
├── target reference
├── outcome distribution/reference
├── adverse-outcome definition
├── risk_measure_id
├── risk_measure_revision
├── horizon
├── statistic/distribution result
├── estimate support
├── World/estimator revisions
└── provenance
```

Допустимые concrete views могут включать mean, quantile, tail probability, CVaR-like statistic или violation probability, но contract не требует их.

---

# 13. ValueProfile

Conceptually:

```text
ValueProfile
├── profile_id
├── target
├── base state / agent revision
├── component schema revision
├── components[]
├── feasibility_profile?
├── constraint_profile?
├── risk_profile?
├── temporal aggregation metadata
├── normalization manifests
├── availability/status
└── provenance
```

`ValueProfile` не обязан быть tensor/vector.

---

# 14. ComparisonPolicyDescriptor

Conceptually:

```text
ComparisonPolicyDescriptor
├── policy_id
├── policy_revision
├── comparison_family
├── required components
├── preference source refs
├── normalization policy
├── constraint semantics
├── risk semantics
├── temporal aggregation semantics
├── tie/incomparability policy
├── scalar output capability
├── learned/fixed capability
└── provenance
```

`comparison_family` может быть scalar, dominance/Pareto, lexicographic, constraint-first, nonlinear или learned.

---

# 15. ComparisonRequest

Conceptually:

```text
ComparisonRequest
├── request_id
├── ValueProfile refs[]
├── comparison_policy_id/revision
├── preference context refs
├── base decision context
└── provenance
```

Comparison нескольких profiles должна подтверждать их semantic compatibility или явно обрабатывать различия.

---

# 16. ComparisonResult

Conceptually:

```text
ComparisonResult
├── comparison_id
├── compared profile refs
├── policy identity/revision
├── relation
├── winner/ranking?, если определён
├── dominated/Pareto set?, если применимо
├── constraint statuses
├── scalarized values?, если policy их производит
├── explanation/source component refs
├── uncertainty/support
├── status
└── provenance
```

`relation` допускает минимум:

```text
preferred
reverse_preferred
tie/equivalent
dominates
dominated
incomparable
constraint_violation
insufficient_evidence
unavailable
```

---

# 17. ScalarizedValue

Conceptually:

```text
ScalarizedValue
├── scalar_id
├── profile_id
├── value
├── comparison/scalarization policy revision
├── weight/preference refs
├── normalization refs
├── risk semantics
├── horizon
└── provenance
```

Нельзя сравнивать scalarized values разных policies как одну шкалу без explicit compatibility.

---

# 18. Prospective/Trajectory Valuation

Для trajectory:

```text
TrajectoryValuation
├── branch/trajectory ref
├── horizon
├── per-step ValueProfile refs?
├── terminal ValueProfile?
├── temporal aggregation policy
├── simulated internal-state mode
├── aggregate profile/result
└── provenance
```

Discount factor не является обязательным contract field, если concrete temporal policy его не использует.

---

# 19. ValuationRecord

Conceptually:

```text
ValuationRecord
├── valuation_id
├── request reference
├── target reference
├── base_state_revision
├── agent_revision
├── valuation_system_revision
├── ValueProfile
├── ComparisonResult?
├── source revisions
├── horizon/time semantics
├── status
└── provenance
```

Повторная valuation создаёт новый record.

---

# 20. Intervention semantics

Controlled intervention должен уметь target минимум:

```text
ValueComponent
component mapping
ComparisonPolicy
scalarization weights/preferences
constraint threshold
risk measure/attitude
normalization state
ValueProfile
```

Intervened result обязательно сохраняет `intervention_id` и base lineage.

---

# 21. Control implementations

Contract должен позволять композиционно различать:

```text
NoValuation
DummyValuation
ConstantValuation
RandomValuation
ShuffledValuation
MatchedLinearValuation
WeightedScalarBaseline
LexicographicControl
OracleValuationControl
real Valuation
```

`NoValuation` не возвращает fake zero profile.

Oracle control не используется natural Agent.

---

# 22. Snapshot

Если implementation stateful, `ValuationSnapshot` включает causally relevant:

```text
system/component revisions
comparison-policy state
learned parameters/adapters
normalizer state
risk estimator state
adaptive preference/calibration state
RNG
intervention/degradation state
```

Stateless implementation всё равно требует descriptor/revision reproducibility.

---

# 23. Failure/status semantics

Нужно различать:

```text
source unavailable
component unsupported
incompatible revision
normalization unavailable
insufficient distribution
risk unavailable
comparison undefined
incomparable
constraint violation
estimator failure
backend failure
```

`incomparable` не является технической ошибкой.

---

# 24. Versioning

Минимально различаются:

```text
valuation_system_revision
component_schema_revision
component_mapping_revision
comparison_policy_revision
normalizer_revision
risk_measure_revision
source module revisions
agent_revision
```

Изменение comparison weights/policy — behavior-relevant revision и должно быть воспроизводимо.

---

# 25. Что остаётся candidate

До последующих DU не frozen:

- exact component schema;
- preference representation;
- scalarization/default comparison;
- risk measure;
- temporal aggregation;
- state/action/trajectory value API;
- critic integration;
- training reward mapping;
- Policy consumption contract;
- concrete tensors/classes/frameworks.
