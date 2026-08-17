# Candidate contract Memory Core MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-11 — Memory Core`

Этот документ уточняет machine-facing классы данных и capability будущей реализации Memory Core.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- конкретную database;
- FAISS/HNSW/SQL backend;
- конкретный embedding encoder;
- exact enum identifiers;
- exact serialization format.

Приоритет семантики имеет [`../modules/memory.md`](../modules/memory.md).

---

# 1. Capability surfaces

Future Memory Core должна уметь выразить capability класса:

```text
submit write proposal
validate/admit/reject write
publish committed memory revision
retrieve by explicit request
inspect record/retrieval evidence
build/rebuild representations/indexes
snapshot/restore/fork logical memory state
```

Research interventions проходят через explicit Intervention Gateway.

---

# 2. MemoryWriteProposal

Conceptually:

```text
MemoryWriteProposal
├── proposal_id
├── content_kind
├── semantic/source payload
├── source references
├── provenance
├── requested retention scope?
├── source agent_revision
├── causal identities
└── intervention provenance?
```

Proposal не получает `memory_id`, пока не принят Memory Core.

Outcome должен различать минимум:

```text
accepted
rejected
invalid
capacity_rejected
deferred?   # если будущий contract это допускает
```

Точный enum не frozen.

---

# 3. MemoryRecord

Conceptually:

```text
MemoryRecord
├── memory_id
├── content_kind
├── semantic_payload
├── source references
├── provenance
├── creation causal identity
├── source agent_revision
├── retention scope
├── content_schema_revision
├── lifecycle/status
├── relations[]
└── intervention provenance?
```

`memory_id` не зависит от физического row/index/vector slot.

Canonical source payload после committed write не должен молча переписываться задним числом.

---

# 4. Record relations

Contract должен позволять выразить ссылки класса:

```text
derived_from
supersedes
contradicts
corroborates
same_source_event / related_event
```

Точный relation vocabulary не frozen.

Наличие relation не обязано менять truth/value semantics автоматически.

---

# 5. MemoryRevision

Memory Core должна публиковать logical revision identity.

Conceptually:

```text
MemoryRevision
├── memory_revision_id
├── previous_revision?
├── causal commit identity
├── store schema revision
└── behavior-relevant configuration revision
```

Retrieval result обязан ссылаться на base Memory revision.

---

# 6. MemoryRepresentation

Derived representation conceptually:

```text
MemoryRepresentation
├── representation_id
├── memory_id
├── representation_kind
├── feature_space_id
├── feature_space_revision
├── encoder_identity
├── encoder_revision
├── source_content_revision
├── data
├── availability/status
└── provenance
```

Representation identity не является Memory identity.

Нельзя сравнивать/смешивать несовместимые feature spaces только из-за одинакового shape.

---

# 7. RetrievalIndexDescriptor

Conceptually:

```text
RetrievalIndexDescriptor
├── index_id
├── index_revision
├── strategy/backend identity
├── indexed_memory_scope/set identity
├── representation/feature-space identity?
├── metric/scoring semantics
├── config/build revision
├── exact/approximate semantics
└── reproducibility metadata
```

Index является rebuildable derived structure, если конкретная implementation может гарантировать rebuild semantics.

---

# 8. RetrievalRequest

Conceptually:

```text
RetrievalRequest
├── request_id
├── semantic/structured query?
├── feature query?
│   ├── feature_space_id
│   └── feature_space_revision
├── temporal constraints?
├── record-kind filters?
├── provenance/source filters?
├── goal/entity references?
├── requested result count/range
├── required strategy/capabilities?
├── base memory_revision requirement?
├── causal identities
└── provenance
```

Memory capability не получает implicit право читать весь `CognitiveState` для построения query.

---

# 9. RetrievalMatch

Conceptually:

```text
RetrievalMatch
├── memory_id
├── match/rank
├── score components
├── representation reference?
├── match explanation/metadata?
└── availability/degradation metadata
```

Score не является автоматически utility, salience, importance или truth probability.

---

# 10. RetrievalResult

Conceptually:

```text
RetrievalResult
├── request_id
├── base memory_revision
├── index/strategy revision
├── matches[]
├── status
├── truncation/degradation metadata
├── resource evidence?
└── provenance
```

Result не создаёт новый `MemoryRecord` автоматически.

---

# 11. Capacity semantics

Contract должен уметь явно сообщать:

```text
available capacity
hard capacity exhausted
write rejected by configured baseline policy
eviction performed by explicit configured policy
```

До `DU-20` contract не предполагает importance/salience-driven retention.

Hidden eviction запрещён.

---

# 12. Scope

Memory record должен допускать как минимум retention scope класса:

```text
episode
session
agent-persistent
```

Source event scope и retention scope должны оставаться различимыми.

---

# 13. Snapshot

Logical Memory snapshot должен уметь восстановить минимум:

```text
memory_revision
canonical records
relations/lifecycle metadata
scope/capacity state
representation manifests
index manifests/config revisions
causally relevant RNG state
```

Если physical index не snapshot-ится, contract должен уметь указать способ/качество rebuild.

`exact`, `causally equivalent` и `approximate` restore semantics не должны смешиваться.

---

# 14. Observability

Evidence должна позволять ссылаться на:

```text
write proposal id
admission result
memory id
memory revision
representation id/revision
index id/revision
retrieval request id
retrieval result
snapshot/restore/fork event
intervention id
```

---

# 15. Failure / degradation

Contract должен различать минимум классы:

```text
memory unavailable
write invalid/rejected
capacity exhausted
representation unavailable
feature-space incompatible
index unavailable/stale
retrieval timeout
partial/truncated retrieval
snapshot incompatible
restore failed
```

Универсальный `None`/empty-list не должен скрывать разные причины, если они причинно/исследовательски значимы.

---

# 16. Configurations

Должны быть различимы capability semantics:

```text
NoMemory
DummyMemory
ControlMemory
real Memory
```

Control implementations могут включать random/shuffled/recency-only retrieval, но обязаны соблюдать тот же semantic request/result boundary.

---

# 17. Что ещё не frozen

До последующих DU не фиксируются:

- конкретный memory backend;
- конкретный vector index;
- embedding model;
- hybrid ranking formula;
- learned retrieval controller;
- salience/importance admission;
- consolidation;
- forgetting curve;
- semantic knowledge extraction;
- replay sampling;
- exact checkpoint encoding.
