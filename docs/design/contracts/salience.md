# Candidate contract Salience / Attention MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-19 — Salience / Attention`

Этот документ уточняет machine-facing semantic формы будущего `Salience System`.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- mandatory scalar salience;
- concrete neural router;
- exact weighted formula;
- top-K/softmax/threshold как universal policy;
- physical compute unit;
- Workspace/Executive/Memory Regulation implementation.

Приоритет имеет [`../modules/salience.md`](../modules/salience.md).

---

# 1. Архитектурная форма

Future implementation должна поддерживать agent-owned `Salience System`, который:

```text
explicit candidates
+
explicit evidence/context
→ SalienceProfile[]

SalienceProfile[]
+
AttentionBudget
+
AllocationPolicy
→ AttentionAllocation
```

Salience не выполняет Memory retrieval, Workspace admission, Cortex invocation, Policy action selection или scheduler mutation.

---

# 2. SalienceSystemDescriptor

Conceptually:

```text
SalienceSystemDescriptor
├── system_id
├── system_revision
├── supported target kinds
├── supported purposes
├── supported evidence kinds
├── supported allocation policies
├── stateful-persistence capability
├── learned/fixed capability
├── snapshot capability
└── research/control flags
```

---

# 3. SalienceTarget

```text
SalienceTarget
├── target_id
├── target_kind
├── source_ref
├── source_revision
├── causal_mode
├── branch/decision/cycle refs?
├── availability/status
└── provenance
```

Target должен быть causally identifiable.

Target kind не даёт Salience ambient access к source subsystem.

---

# 4. SalienceCandidateSet

```text
SalienceCandidateSet
├── candidate_set_id
├── purpose
├── base_state_revision
├── decision_id?
├── cycle_id?
├── branch_id?
├── targets[]
└── provenance
```

Candidate set формируется explicit producer/consumer boundary.

---

# 5. SaliencePurpose

Conceptually purpose описывает **для какого вида ограниченного processing** строится priority.

Примеры semantics:

```text
general_processing
workspace_admission_hint
memory_regulation_hint
retrieval_postprocessing
planning_inspection
executive_attention_hint
context_packing_hint
```

Exact enum не frozen.

Один target может иметь разные profiles между purposes.

---

# 6. SalienceEvidence

```text
SalienceEvidence
├── evidence_id
├── evidence_kind
├── target_id
├── raw/structured value
├── units/scale
├── source_ref
├── source_revision
├── normalization_ref?
├── support/confidence?
├── causal_mode
└── provenance
```

Evidence kinds могут включать references на:

- novelty/surprisal/information signals;
- perceptual change;
- Appraisal relevance/urgency;
- Goal relation;
- ValueProfile/risk/constraints;
- Drive/Affect context;
- uncertainty-resolution need;
- explicit task/focus context.

Они не являются общей числовой валютой автоматически.

---

# 7. SalienceRequest

```text
SalienceRequest
├── request_id
├── candidate_set
├── evidence refs / allowed sources
├── purpose
├── context refs
├── requested profile version?
├── allocation requested?
├── budget?
├── allocation_policy?
└── provenance
```

Request не даёт ambient read authority всему `CognitiveState`.

---

# 8. SalienceComponent

```text
SalienceComponent
├── component_id
├── component_kind
├── source evidence refs
├── raw/normalized value or structured relation
├── scale/units
├── estimator/mapping revision
├── support/confidence?
├── availability
└── provenance
```

Examples:

```text
novelty contribution
urgency contribution
goal relevance contribution
risk/constraint attention contribution
inhibition contribution
```

Название contribution не означает универсальную additive semantics.

---

# 9. SalienceProfile

```text
SalienceProfile
├── profile_id
├── target_id
├── purpose
├── base_state_revision
├── component set
├── persistence/inhibition refs?
├── profile policy revision
├── optional derived priority score?
├── availability/status
└── provenance
```

`priority score`, если существует, не является mandatory canonical representation.

---

# 10. AttentionBudget

```text
AttentionBudget
├── budget_id
├── purpose
├── budget_kind
├── amount/capacity
├── hard/soft semantics
├── owner/consumer identity
├── units
└── provenance
```

Examples:

```text
max_items
normalized_mass
context_slots
abstract_consumer_units
```

Physical FLOPs/Cortex calls/Cognitive Cycles принадлежат downstream Executive semantics, если явно не введены позднее.

---

# 11. AllocationPolicyDescriptor

```text
AllocationPolicyDescriptor
├── policy_id
├── policy_revision
├── policy_family
├── supported purposes
├── required profile components
├── normalization refs
├── stochastic/RNG capability
├── learned/fixed capability
└── configuration provenance
```

Possible policy families:

```text
ranking
top_k
threshold
soft_distribution
quota
weighted_scalar
learned_router
hybrid
```

Ни одна не universal default.

---

# 12. AllocationEntry

```text
AllocationEntry
├── target_id
├── rank?
├── selected/gated?
├── allocated_units/share?
├── optional derived priority score?
├── reason/component refs
├── availability/status
└── provenance
```

---

# 13. AttentionAllocation

```text
AttentionAllocation
├── allocation_id
├── candidate_set_id
├── purpose
├── base_state_revision
├── budget
├── allocation_policy revision
├── entries[]
├── unused budget?
├── degradation/intervention state
└── provenance
```

Allocation является advisory/decision input для downstream consumer, если его contract не говорит иначе.

Она сама не выполняет consumer side effect.

---

# 14. SalienceState

Если implementation stateful:

```text
SalienceState
├── state_revision
├── focus persistence state?
├── inhibition-of-return state?
├── habituation/refractory state?
├── adaptive normalization state?
├── learned router private state?
├── last logical update
└── provenance
```

Stateless implementation должна быть допустима.

---

# 15. SalienceUpdateProposal

Для causally relevant persistent state:

```text
SalienceUpdateProposal
├── base SalienceState revision
├── staged next state
├── source Allocation/Profile refs
├── logical boundary
└── provenance
```

Применяется только через scheduler/commit semantics.

---

# 16. Causal mode

Минимально различаются:

```text
actual
predicted
imagined
retrieved/retrospective
intervened
counterfactual
offline/replayed
```

Imagined allocation не становится real allocation автоматически.

---

# 17. Memory integration boundary

Допустимо:

```text
RetrievalResult
→ SalienceCandidateSet
→ AttentionAllocation
```

и:

```text
Memory candidate + SalienceProfile
→ future Memory Regulation
```

Но contract Salience не содержит hidden retrieval/write/eviction methods.

---

# 18. Workspace integration boundary

Допустимо:

```text
AttentionAllocation(purpose=workspace_admission_hint)
→ future Workspace
```

Workspace самостоятельно определяет capacity/admission/broadcast.

---

# 19. Executive integration boundary

Допустимо:

```text
AttentionAllocation(purpose=executive_attention_hint)
→ future Executive Control
```

Salience не вызывает Cortex/retrieval/planning сама.

---

# 20. Cortex boundary

Model-internal attention tensors/weights могут быть доступны только как optional diagnostic/evidence adapter.

Они не реализуют `SalienceProfile` автоматически.

---

# 21. Failure/degradation statuses

Contract должен позволять отличать минимум:

```text
candidate_stale
profile_unavailable
profile_partial
unsupported_evidence
normalization_mismatch
budget_invalid
allocation_unavailable
policy_failure
learned_router_failure
```

`0` не заменяет failure/unavailable.

---

# 22. Research controls

Composition должна позволять:

```text
NoSalience
DummySalience
UniformSalience
RandomSalience
ShuffledSalience
NoveltyOnlySalience
ValueOnlySalience
UrgencyOnlySalience
RecencyOnlySalience
FixedTopKSalience
MatchedLearnedControl
OracleResearchSalience
```

Oracle не agent-natural configuration.

---

# 23. Observability

Machine-facing evidence должна позволять связать:

```text
candidate set
→ evidence
→ profile
→ allocation
→ actual downstream consumer effect
```

Иначе causal contribution Salience не проверяется.

---

# 24. Intervention

Intervention surface должна позволять отдельно менять:

- component/evidence mapping;
- profile;
- persistence/inhibition state;
- budget;
- AllocationPolicy;
- final allocation entry.

Все interventions сохраняют provenance.

---

# 25. Snapshot

Stateful implementation snapshot включает:

```text
system/policy revisions
persistent salience state
normalization state
learned parameters/private state
RNG
last logical update
intervention/degradation state
```

Historical allocation records относятся к Evidence/Trajectory, если сами не нужны для будущей causality.

---

# 26. Что остаётся candidate

До последующих DU не frozen:

- concrete target taxonomy;
- purpose enum;
- component set;
- scalar vs non-scalar profile implementation;
- persistence dynamics;
- inhibition formula;
- allocation policy;
- normalization strategy;
- neural architecture;
- exact budget units;
- Memory/Workspace/Executive integration API.
