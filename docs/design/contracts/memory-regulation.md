# Candidate contract Memory Regulation / Consolidation MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-20 — Memory Regulation / Consolidation`

Этот документ уточняет machine-facing semantic формы regulation/consolidation поверх [`memory.md`](memory.md).

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- конкретный forgetting curve;
- mandatory memory importance scalar;
- FIFO/LRU/top-K как universal policy;
- concrete LLM summarizer;
- concrete clustering/index backend;
- optimizer/slow-weight update;
- Training Replay schema.

Приоритет имеет [`../modules/memory-regulation.md`](../modules/memory-regulation.md), а canonical record/store semantics остаются в [`../modules/memory.md`](../modules/memory.md).

---

# 1. Архитектурная форма

Conceptually:

```text
Memory Core
├── canonical Memory Store
├── validation / commit
└── retrieval

Memory Regulation
├── profile builders
├── admission policy
├── retention/eviction policy
├── replay-selection policy
├── consolidation policy
├── optional state
└── inspect/snapshot/restore
```

`Memory Regulation` не получает direct store mutation authority.

---

# 2. MemoryRegulationSystemDescriptor

```text
MemoryRegulationSystemDescriptor
├── system_id
├── system_revision
├── supported purposes
├── supported evidence kinds
├── supported policy families
├── consolidation capabilities
├── Cortex-assisted capability
├── stateful-aging capability
├── snapshot capability
└── research/control flags
```

---

# 3. MemoryRegulationTarget

```text
MemoryRegulationTarget
├── target_id
├── target_kind
├── memory_id? / proposal_id?
├── base memory_revision
├── content/provenance refs
├── lifecycle/accessibility status
├── scope
└── provenance
```

Target kinds могут включать:

```text
write_proposal
existing_record
record_group
replay_candidate
consolidation_candidate
representation-maintenance candidate
```

---

# 4. RegulationPurpose

Semantic purposes должны различаться:

```text
admission
retention_review
eviction
replay_selection
consolidation_selection
consolidation_acceptance
representation_maintenance
```

Одинаковая policy/score между purposes не предполагается.

---

# 5. MemoryBudget

```text
MemoryBudget
├── budget_id
├── budget_revision
├── purpose
├── resource dimensions[]
├── hard/soft semantics
├── base memory_revision
└── provenance
```

Resource dimension может описывать record count, bytes, active-tier capacity, representation/index cost или другой version-specific ресурс.

`MemoryBudget` не является глобальным Executive compute budget.

---

# 6. MemoryRegulationEvidence

```text
MemoryRegulationEvidence
├── evidence_id
├── evidence_kind
├── source subsystem/ref
├── semantic value/structure
├── units/scale
├── availability/support
├── source revision
└── provenance
```

Possible evidence kinds:

```text
recency / age
access history
retrieval history
redundancy
similarity
diversity / coverage
contradiction role
source quality/provenance
storage cost
scope/expiration
SalienceProfile
ValueProfile-derived evidence
Appraisal/Affect/Drive-derived declared evidence
representation compatibility
```

Ни один evidence kind не имеет automatic priority semantics.

---

# 7. MemoryRegulationProfile

```text
MemoryRegulationProfile
├── profile_id
├── target
├── purpose
├── evidence[]
├── MemoryBudget ref
├── missing/unknown evidence state
├── policy-compatible normalized views?
├── base revisions
└── provenance
```

Profile сам не является final decision.

---

# 8. RegulationPolicyDescriptor

```text
RegulationPolicyDescriptor
├── policy_id
├── policy_revision
├── purpose
├── required/optional evidence kinds
├── budget semantics
├── deterministic/stochastic semantics
├── stateful capability
├── learned/fixed capability
└── control flags
```

---

# 9. RegulationDecision

```text
RegulationDecision
├── decision_id
├── target_id
├── purpose
├── result
├── policy id/revision
├── base memory_revision
├── profile/evidence refs
├── budget effect
├── rationale/structured factors?
├── stochastic/RNG provenance?
└── intervention/degradation provenance
```

Possible semantic outcomes зависят от purpose: `admit`, `reject`, `defer`, `retain`, `deprioritize`, `evict`, `select_for_replay`, `select_for_consolidation` и т.п.; exact enums не frozen.

---

# 10. MemoryLifecycleUpdateProposal

```text
MemoryLifecycleUpdateProposal
├── proposal_id
├── memory_id
├── requested lifecycle/accessibility transition
├── regulation decision ref
├── base memory_revision
├── expected budget effect
└── provenance
```

Только `Memory Core` commit'ит lifecycle update.

---

# 11. MemoryUsageHistory

Если policy использует usage/history:

```text
MemoryUsageHistory
├── memory_id
├── retrieval events
├── replay/reactivation events
├── last logical access refs
├── usage counters/windows
└── revision/provenance
```

Нужно различать:

```text
actual retrieval
memory replay
training replay
```

и не смешивать их counters.

---

# 12. MemoryReplayCandidateSet

```text
MemoryReplayCandidateSet
├── candidate_set_id
├── base memory_revision
├── Consolidation Event id
├── memory IDs[]
├── candidate metadata/evidence refs
└── provenance
```

---

# 13. MemoryReplaySelection

```text
MemoryReplaySelection
├── selection_id
├── candidate_set_id
├── selected memory IDs[]
├── ordering/allocation?
├── selection policy id/revision
├── base memory_revision
├── RNG provenance?
└── provenance
```

Selection не делает Environment Transition и не является Training Replay batch.

---

# 14. MemoryReactivationRecord

```text
MemoryReactivationRecord
├── reactivation_id
├── memory_id
├── source memory_revision
├── Consolidation Event id
├── mode
├── destination/consumer ref?
└── provenance
```

Реактивация не создаёт новый `MemoryRecord` автоматически.

---

# 15. ConsolidationEventContext

```text
ConsolidationEventContext
├── consolidation_event_id
├── base memory_revision
├── logical time identity
├── source candidate set
├── budget / allowed capabilities
├── selected policy revisions
├── branch/session refs
└── provenance
```

---

# 16. ConsolidationSourceSet

```text
ConsolidationSourceSet
├── source_set_id
├── source memory IDs[]
├── supporting/contradicting group structure?
├── source revisions
├── source availability
└── provenance
```

Consolidation не должна терять individual source identities.

---

# 17. ConsolidationProposal

```text
ConsolidationProposal
├── proposal_id
├── source_set_id
├── derivation kind
├── derived semantic payload candidate
├── supporting source refs
├── contradicting source refs
├── derivation method id/revision
├── Cortex/backend provenance?, если использован
├── confidence/support semantics?
├── authority/provenance constraints
├── base memory_revision
└── provenance
```

`ConsolidationProposal` ещё не является committed memory.

---

# 18. DerivedMemoryRecordProposal

После validation/normalization consolidation result должен быть представим как обычный `MemoryWriteProposal`/derived record candidate с обязательной lineage:

```text
DerivedMemoryRecordProposal
├── new proposed memory identity
├── content_kind = derived/semantic/etc.
├── semantic payload
├── derived_from memory IDs[]
├── support/conflict refs
├── derivation metadata
├── source authority constraints
└── provenance
```

Memory Core создаёт новый committed `MemoryRecord`.

---

# 19. ConsolidationResolution

```text
ConsolidationResolution
├── consolidation_event_id
├── proposal ids
├── accepted derived memory ids[]
├── rejected/deferred proposals[]
├── source retention decisions?
├── final memory_revision
├── failure/degradation state
└── provenance
```

Source retention не следует автоматически из consolidation acceptance.

---

# 20. RepresentationMaintenanceRequest

```text
RepresentationMaintenanceRequest
├── request_id
├── memory IDs / index refs
├── old feature-space revisions
├── target feature-space revision
├── encoder revision
└── provenance
```

Re-encoding не является semantic consolidation.

---

# 21. Forgetting / accessibility semantics

Contract должен уметь различать:

```text
normal agent accessibility
reduced/deprioritized accessibility
logically unavailable/forgotten
scope expiration
physical payload removal
```

Exact enum/tiers не frozen.

Physical deletion не должна неявно masquerade как reversible cognitive forgetting.

---

# 22. Snapshot

```text
MemoryRegulationSnapshot
├── regulation system/policy revisions
├── MemoryBudget state
├── lifecycle/accessibility metadata
├── logical aging markers
├── usage/access histories used by policy
├── replay/reactivation history/state
├── consolidation lineage/pending state
├── representation-maintenance state
├── RNG
├── intervention/degradation state
└── compatibility manifest
```

Memory Core snapshot сохраняется отдельно/составно согласно `contracts/memory.md`.

---

# 23. Observability

Evidence plane должна поддерживать trace минимум для:

```text
regulation profile computation
policy decision
budget before/after
lifecycle update proposal/commit
replay candidate/selection/reactivation
consolidation source selection
consolidation proposal/accept/reject
source/contradiction lineage
representation maintenance
failure/degradation
```

---

# 24. Controls

Contract должен позволять конфигурации класса:

```text
NoRegulation
NoConsolidation / episodic-only
FIFO/oldest-first
recency-only
random retention/eviction
uniform/random replay
shuffled evidence
Salience-only
value-only
matched learned control
fixed periodic consolidation
random grouping consolidation
retain-raw-only
oracle research control
```

Control implementation подключается через обычную composition boundary.

---

# 25. Не заморожено

До contract/version freeze не считать обязательными:

- названия Python типов;
- конкретные lifecycle enum;
- exact importance/retention score;
- exact forgetting equation;
- exact budget units;
- replay priority formula;
- LLM/embedding consolidation;
- clustering;
- generative replay;
- gradient-based slow memory;
- Training Replay integration.
