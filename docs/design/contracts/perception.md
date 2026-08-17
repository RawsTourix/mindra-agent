# Candidate contract Perception MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-08 — Perception / Canonical Representation`

Этот документ уточняет machine-facing классы данных и capability, необходимые будущей реализации Perception.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact method names;
- dataclass/TensorDict/Pydantic;
- dtype/shape;
- конкретный encoder architecture;
- exact namespace `CognitiveState`;
- serialization encoding.

Приоритет семантики имеет [`../modules/perception.md`](../modules/perception.md).

---

# 1. Основная capability

Future Perception implementation должна уметь выразить операцию класса:

```text
PerceptionInput
      ↓
Perception Result
      ↓
Canonical Percept
```

Perception работает только с agent-visible observation boundary и не получает Environment Research Plane как normal input.

---

# 2. Perception descriptor

Implementation должна предоставлять стабильное описание как минимум следующих свойств:

```text
semantic_role
implementation_identity
percept_schema_revision
supported_observation_schemas
supported_modalities
normalization_revision
learned_encoder_capabilities
feature_view_capabilities
research_probe_capabilities
intervention_capabilities
```

Concrete names/format определяются позднее.

---

# 3. Perception input

Conceptually:

```text
PerceptionInput
├── raw_observation
├── raw_observation_identity
├── observation_schema_identity
├── causal identities
├── modality/source metadata
└── intervention provenance?
```

`External Task Specification` и `External Task Feedback` не должны автоматически включаться в эту структуру как Perception data. Их routing определяется отдельными boundaries.

Research Ground Truth/hidden world state запрещены normal input.

---

# 4. Canonical Percept

Conceptual output:

```text
CanonicalPercept
├── envelope
├── semantic_core
├── modality_status
└── feature_views[]
```

## Envelope

Должен позволять выразить:

```text
percept_identity
source_observation_identity
source_environment/observation_schema_identity
causal context
percept_schema_revision
perception_pipeline_identity/revision
agent_revision?
intervention provenance?
quality/availability summary?
```

## Semantic core

Должен уметь представлять current-observation semantics как типизированную structure.

Минимальные semantic categories для reference MicroWorld:

```text
observed_self
observed_entities[]
observed_relations[]
observed_events[]
```

Точные field names и enums не frozen.

## Modality status

Для каждой relevant modality должна быть выразима availability/quality semantics без magic zero tensors.

## Feature views

Каждый view должен иметь data + достаточно metadata для проверки provenance/compatibility.

---

# 5. Candidate entity semantics

Conceptually entity record должен позволять выразить:

```text
percept_local_entity_identity
observable/inferred type information?
attributes
spatial facts
quality/confidence?
field-level provenance where required
```

`percept_local_entity_identity` по умолчанию не является persistent world ID.

Entity collection order не имеет semantic meaning, если отдельный contract не заявляет обратное.

---

# 6. Candidate field provenance

Perceptual field должен при необходимости позволять отличить:

```text
direct observation
normalized/deterministically derived
perceptually inferred
intervened
```

Это дополнительно к source observation identity.

Perceptual inference не должна маскироваться под Environment ground truth.

---

# 7. Feature View candidate semantics

Conceptually:

```text
FeatureView
├── view_identity
├── view_kind
├── feature_space_id
├── feature_space_revision
├── encoder_identity?
├── encoder_revision?
├── source references
├── availability/quality
└── data
```

Если view deterministic и не имеет learned encoder, encoder fields могут быть неприменимы.

Равенство shape/dtype не является достаточной compatibility guarantee.

---

# 8. Version compatibility

Future contract должен позволять consumers объявить требования к:

- `percept_schema_revision`;
- конкретному feature view;
- feature-space compatibility;
- freshness;
- modality availability.

Несовместимость должна обнаруживаться явно на composition/runtime validation boundary, а не приводить к silent tensor reuse.

---

# 9. Batch semantics

Future representation должна поддерживать batching независимых percepts.

При этом contract должен сохранять:

- item-level causal identity;
- variable-size entity collections;
- explicit padding/mask semantics, если implementation их использует;
- отсутствие semantic meaning у padding и arbitrary entity order.

Batch container не должен смешивать lineage разных items.

---

# 10. Lifecycle semantics

Perception result вычисляется относительно конкретного source observation и base Agent/state revision.

Staged result следует общему `DU-05` commit protocol.

Уже committed percept не изменяется задним числом при последующем encoder update.

Если новый observation не поступил, один percept может оставаться актуальным несколько Cognitive Cycles согласно freshness contract.

---

# 11. Failure semantics

Будущий contract должен различать:

```text
invalid raw observation schema
unsupported required modality
perception computation failure
optional feature view unavailable
stale/incompatible feature view
```

Не допускается hidden fallback на Cortex, privileged Environment data или другой encoder.

---

# 12. Research-facing capability

Perception должна иметь отдельную research surface, достаточную для:

- inspect semantic percept;
- inspect representation identities/revisions;
- inspect modality/quality status;
- optional private encoder probe;
- sensor/input intervention;
- semantic-percept intervention;
- feature-view intervention;
- representation drift probe.

Research capability не становится normal dependency cognitive consumers.

---

# 13. Snapshot/checkpoint implications

Candidate contract не определяет полный snapshot format, но causally relevant learned Perception state должен быть совместим с будущими Agent Snapshot requirements.

Для reproducibility потребуется сохранять или однозначно идентифицировать:

- percept schema revision;
- normalization state/revision;
- encoder parameters/revision;
- feature-space revision;
- stochastic encoder RNG state, если inference stochastic и влияет на behavior.

Exact policy — `DU-27`.

---

# 14. Cortex compatibility

Future Cortex adapter не должен менять этот contract так, чтобы:

- Cortex становился обязательным для Canonical Percept;
- model-specific hidden tensors становились обязательным Semantic Core;
- no-Cortex configuration становилась invalid.

Cortex-derived view может реализовываться как optional `FeatureView` после принятия `DU-10`.

---

# 15. Что остаётся candidate

До contract freeze не фиксируются:

- field paths;
- class names;
- exact entity schema;
- confidence representation;
- feature tensor dimensions;
- modality enum;
- normalization constants;
- padding strategy;
- storage/reference strategy Raw Observation;
- exact compatibility checker.
