# Candidate contract Self Model MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-13 — Self Model`

Этот документ уточняет machine-facing классы данных и capability будущей реализации Self Model.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- exact task/capability taxonomy;
- конкретную calibration method;
- конкретную probability/uncertainty model;
- конкретные losses;
- exact serialization format.

Приоритет семантики имеет [`../modules/self-model.md`](../modules/self-model.md).

---

# 1. Capability surfaces

Future Self Model должна уметь выразить capability класса:

```text
ingest/update Agent Capability Manifest
ingest Self Evidence
publish committed Self Belief
query context-conditioned Self Prediction
resolve prediction against later outcome
report estimate support / calibration status
inspect self-belief/prediction evidence
snapshot/restore/fork causally relevant state
```

Research interventions проходят через explicit Intervention Gateway.

---

# 2. AgentCapabilityManifest

Conceptually:

```text
AgentCapabilityManifest
├── manifest_revision
├── agent_revision
├── capability_entries[]
│   ├── capability_id
│   ├── enabled/status
│   ├── interface/capability revision
│   ├── declared limits/budgets?
│   └── provenance
└── change provenance
```

Manifest не должен содержать arbitrary runtime/private objects, evaluator secrets или full process telemetry.

---

# 3. SelfEvidence

Conceptually:

```text
SelfEvidence
├── evidence_id
├── evidence_kind
├── target capability/task/action reference?
├── context references
├── outcome / operational fact
├── source identities
├── agent_revision
├── causal identities
├── evidence provenance
└── intervention / privileged-supervision provenance?
```

Evidence должна различать natural agent-visible evidence и research-supervised label.

---

# 4. SelfBelief

Conceptually:

```text
SelfBelief
├── self_belief_revision
├── self_model_revision
├── basis agent_revision
├── capability_manifest_revision
├── competence profiles[]
├── known limitations[]
├── evidence/support summary
├── calibration state?
├── status / staleness
└── provenance
```

Backend-specific latent/recurrent state может оставаться private.

---

# 5. CompetenceProfile

Conceptually:

```text
CompetenceProfile
├── profile_id
├── domain / applicability descriptor
├── target outcome semantics
├── estimate representation
├── evidence support
├── source agent revisions
├── validity/staleness
└── provenance
```

Contract не предполагает один universal scalar competence для всего Agent.

---

# 6. SelfPredictionRequest

Conceptually:

```text
SelfPredictionRequest
├── request_id
├── target event/outcome definition
├── goal/task reference?
├── context references
├── candidate action/strategy reference?
├── horizon / resolution condition
├── requested estimate channels
├── required applicability/domain?
├── causal identities
├── agent_revision
└── provenance
```

Request не является action/strategy selection.

---

# 7. SelfPrediction

Conceptually:

```text
SelfPrediction
├── prediction_id
├── request_id
├── self_belief_revision
├── self_model_revision
├── agent_revision
├── target semantics
├── success_probability?
├── expected cost/resource channels?
├── expected own-state outcome?
├── estimate uncertainty/support
├── applicability / out-of-domain status
├── status/degradation
└── provenance
```

`success_probability` и `estimate uncertainty/support` являются разными semantic axes.

---

# 8. Prediction target semantics

Если публикуется вероятность успеха, contract должен сохранять:

```text
what counts as success
horizon / resolution rule
task/goal/context scope
agent_revision
capability context
```

Запрещён неразмеченный global `confidence` без target semantics.

---

# 9. SelfPredictionResolution

Conceptually:

```text
SelfPredictionResolution
├── resolution_id
├── prediction_id
├── resolved outcome
├── resolution status
├── outcome source/provenance
├── causal identities
└── resolution time/scope
```

Outcome может быть:

```text
success
failure
partial / structured outcome
unknown / unresolved
invalidated
```

Exact enum не frozen.

Evaluator-only truth не используется как natural resolution без explicit research provenance.

---

# 10. Calibration state

Contract должна позволять описать calibration/evidence состояние без навязывания конкретной метрики.

Conceptually:

```text
CalibrationState
├── calibration_domain
├── sample/evidence support
├── estimator revision
├── diagnostic metric references?
├── status
└── provenance
```

Exact Brier/NLL/ECE implementation относится к future evaluation/training design.

---

# 11. Agent revision compatibility

Self estimates должны быть связаны с behavior-relevant Agent revision.

Contract должна уметь выразить:

```text
valid for current revision
stale after revision change
partially transferable
unknown / recalibration required
```

Точная transfer policy не frozen.

---

# 12. Resource / cost channels

Если Self Prediction публикует cost, channel должен иметь explicit semantics, например:

```text
expected cognitive cycles
expected Cortex invocations
expected action count
expected retrieval count
explicit declared budget usage
```

Wall-clock или host telemetry не становятся cognitive resource channel автоматически.

---

# 13. Snapshot

Self Model snapshot должен уметь восстановить минимум:

```text
self_model_revision
Self Belief
private causally relevant state
capability manifest identity/revision
calibration/evidence summaries
RNG state
intervention/degradation state
```

`exact`, `causally equivalent` и `approximate` restore semantics не смешиваются.

---

# 14. Observability

Evidence должна позволять ссылаться на:

```text
manifest revision
self-belief revision
competence profile id/domain
Self Evidence id
SelfPrediction request/result
Prediction Resolution
calibration/evidence state
staleness/invalidation event
intervention id
```

---

# 15. Failure / degradation

Contract должна различать минимум:

```text
Self Model unavailable
manifest incompatible/stale
insufficient evidence
estimate out-of-domain
unsupported prediction target
self-belief stale after agent revision
calibration state unavailable
partial/degraded estimate
snapshot incompatible
```

Универсальное число вроде `0.5` не должно скрывать отсутствие оценки.

---

# 16. Configurations

Должны быть различимы:

```text
NoSelfModel
DummySelfModel
ControlSelfModel
real SelfModel
```

Control implementations могут включать:

```text
constant confidence
global empirical baseline
shuffled profile
recency-only estimate
oracle-calibrated research control
parameter/cost-matched predictor
```

и обязаны соблюдать ту же semantic request/result boundary.

---

# 17. Что ещё не frozen

До последующих DU не фиксируются:

- concrete competence estimator;
- task/domain embedding/taxonomy;
- calibration algorithm;
- uncertainty estimator;
- online/offline learning schedule;
- exact capability manifest generation API;
- exact interaction with Executive Control;
- exact Valuation use;
- training losses;
- checkpoint encoding.
