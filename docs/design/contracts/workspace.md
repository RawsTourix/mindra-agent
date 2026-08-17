# Candidate contract Workspace MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-21 — Workspace`

Этот документ уточняет machine-facing semantic формы будущего `Workspace`.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- обязательный slot/token format;
- mandatory top-K/winner-take-all;
- concrete neural router/cross-attention;
- exact Workspace capacity;
- exact consumer set;
- exact Cortex context packing;
- training objective.

Приоритет имеет [`../modules/workspace.md`](../modules/workspace.md).

---

# 1. Архитектурная форма

Future implementation должна поддерживать:

```text
WorkspaceProposal[]
+
WorkspaceBudget
+
optional Salience/admission evidence
→ WorkspaceAdmissionProfile[]
→ WorkspaceAdmissionDecision[]
→ atomic Workspace commit
→ WorkspaceSnapshot
```

Workspace не получает ambient access ко всему Agent state и не выполняет consumer callbacks.

---

# 2. WorkspaceSystemDescriptor

Conceptually:

```text
WorkspaceSystemDescriptor
├── system_id
├── system_revision
├── supported content kinds
├── supported producer kinds
├── supported consumer capabilities
├── supported budget dimensions
├── supported admission policies
├── persistence capability
├── branch/simulation capability
├── snapshot capability
└── research/control flags
```

---

# 3. WorkspaceProposal

```text
WorkspaceProposal
├── proposal_id
├── producer_id / subsystem
├── source_ref
├── source_revision
├── semantic_payload / projection
├── content_kind
├── causal_mode
├── availability/freshness
├── requested_lifetime?
├── base_state_revision
├── agent_revision
└── provenance
```

Proposal не даёт direct write authority.

---

# 4. WorkspaceCandidateSet

```text
WorkspaceCandidateSet
├── candidate_set_id
├── base_state_revision
├── workspace_revision
├── decision_id?
├── cognitive_cycle_id?
├── branch_id?
├── proposals[]
└── provenance
```

Candidate set explicit; Workspace не сканирует Agent state.

---

# 5. WorkspaceBudget

```text
WorkspaceBudget
├── budget_id
├── budget_revision
├── resource_dimensions[]
├── hard/soft semantics
├── write-bandwidth dimension?
├── persistence constraints?
├── base workspace_revision
└── provenance
```

Possible dimensions:

```text
item/slot count
bytes
semantic units
token-like estimate
feature capacity
per-cycle write bandwidth
```

Exact units не frozen.

`WorkspaceBudget ≠ AttentionBudget ≠ MemoryBudget ≠ Executive global compute budget`.

---

# 6. WorkspaceAdmissionEvidence

```text
WorkspaceAdmissionEvidence
├── evidence_id
├── evidence_kind
├── source subsystem/ref
├── semantic value/structure
├── units/scale
├── availability/support
├── source revision
└── provenance
```

Possible evidence:

- SalienceProfile / AttentionAllocation;
- relevance/urgency;
- Value/Risk/Constraint evidence;
- freshness;
- redundancy/diversity;
- content cost;
- persistence state;
- compatibility;
- producer/source authority.

Ни один evidence kind не имеет automatic admission semantics.

---

# 7. WorkspaceAdmissionProfile

```text
WorkspaceAdmissionProfile
├── profile_id
├── proposal/active-item target
├── purpose
├── evidence[]
├── WorkspaceBudget ref
├── current occupancy/context
├── missing/unknown evidence state
├── policy-compatible derived views?
└── provenance/revisions
```

Universal `workspace_importance` scalar не обязателен.

---

# 8. WorkspaceAdmissionPolicyDescriptor

```text
WorkspaceAdmissionPolicyDescriptor
├── policy_id
├── policy_revision
├── supported purposes
├── required evidence
├── comparison/admission semantics
├── replacement semantics
├── lifetime semantics
├── deterministic/stochastic mode
├── RNG requirements
└── control flags
```

Concrete policy может быть fixed/rule-based/learned/hybrid.

---

# 9. WorkspaceAdmissionDecision

```text
WorkspaceAdmissionDecision
├── decision_id
├── target proposal/item
├── base workspace_revision
├── policy_id/revision
├── status
├── action
├── replacement target?
├── assigned lifetime?
├── assigned resource allocation?
├── evidence refs
└── provenance
```

Possible semantic actions:

```text
admit
defer
reject
retain
refresh
replace
evict
expire
```

Exact enum не frozen.

---

# 10. WorkspaceItem

```text
WorkspaceItem
├── workspace_item_id
├── source_ref
├── source_revision
├── source subsystem
├── source authority/provenance
├── semantic_payload / projection
├── content_kind/schema revision
├── causal_mode
├── admitted_at logical identity
├── admitted_workspace_revision
├── freshness/staleness
├── lifetime/expiration state
├── admission policy provenance
├── projection/encoder provenance?
└── intervention/degradation provenance?
```

`WorkspaceItem` не становится новым factual authority.

---

# 11. WorkspaceSnapshot

```text
WorkspaceSnapshot
├── workspace_revision
├── base state_revision
├── agent_revision
├── logical temporal refs
├── WorkspaceBudget ref
├── active items[]
├── occupancy/resource state
├── policy/revision refs
├── branch lineage
└── provenance
```

Snapshot semantically immutable после commit.

---

# 12. WorkspaceReadCapability

Consumer access должен быть declared.

Conceptually:

```text
WorkspaceReadCapability
├── consumer_id/subsystem
├── allowed content kinds
├── allowed projections
├── required freshness?
├── branch-mode support
└── contract revision
```

Наличие Workspace не делает все items ambient input каждого module.

---

# 13. WorkspaceReadRecord

Для causal observability полезна semantic форма:

```text
WorkspaceReadRecord
├── read_id
├── consumer_id
├── workspace_revision
├── item_ids actually read
├── filtering/projection info
├── decision/cycle refs
└── provenance
```

Фактическое чтение отличать от простой доступности item.

---

# 14. WorkspaceUpdateProposal

Stateful Workspace update conceptually:

```text
WorkspaceUpdateProposal
├── base workspace_revision
├── admission decisions[]
├── replacement/expiration decisions[]
├── staged private-state update?
├── expected new occupancy
└── provenance
```

Commit следует общей atomic scheduling semantics.

---

# 15. BranchWorkspaceContext

Для imagination/counterfactual:

```text
BranchWorkspaceContext
├── parent workspace_revision
├── branch_id
├── cloned WorkspaceSnapshot
├── simulated updates
├── RNG state
└── provenance
```

Branch-local updates не применяются к real Workspace автоматически.

---

# 16. WorkspaceIntervention

Conceptual targets:

```text
budget
candidate presence
admission decision
item content/projection
item lifetime
replacement policy
consumer read capability
broadcast accessibility
```

Каждое intervention сохраняет `intervention_id`, base revision и provenance.

---

# 17. WorkspaceSystemSnapshot

Полный causally relevant snapshot может включать:

```text
WorkspaceSnapshot
system/policy revisions
budget state
item lifetimes
private router/recurrent state
RNG state
branch state
intervention/degradation state
```

Exact checkpoint encoding относится к `DU-27`.

---

# 18. Failure / degradation

Contract должен уметь различить conceptually:

```text
invalid_candidate
budget_unavailable
capacity_exhausted
source_stale/unavailable
projection_failure
policy_failure
schema_incompatibility
consumer_incompatible
workspace_unavailable
```

Unavailable/failure не кодируются fake empty/zero Workspace без explicit degradation policy.

---

# 19. Control descriptors

Future evaluation должна уметь выразить:

```text
NoWorkspace
DummyWorkspace
DirectReadsControl
FixedLatestKWorkspace
RandomWorkspace
ShuffledWorkspace
UnboundedWorkspace
WorkspaceWithoutBroadcast
MatchedSharedBufferControl
MatchedRecurrentBufferControl
```

Controls проходят через ту же composition boundary.

---

# 20. Automatically checkable invariants

Будущие contract/engineering tests должны проверять минимум:

- proposal producer не мутирует Workspace напрямую;
- item source revision/provenance обязательны;
- Workspace commit атомарен;
- item не переписывается при изменении source задним числом;
- budget violations detect/reject/degrade explicitly;
- consumer читает только разрешённые content kinds;
- broadcast не запускает callback/module execution;
- branch-local Workspace не мутирует real Workspace;
- Workspace eviction не мутирует source Memory/Goal/etc.;
- imagined item не становится actual без explicit reification proposal;
- Workspace content не является Cortex prompt автоматически;
- item/source authority не повышается после projection/admission.
