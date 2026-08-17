# Candidate contract World Model MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-12 — World Model`

Этот документ уточняет machine-facing классы данных и capability будущей реализации World Model.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- RSSM/GRU/Transformer/SSM;
- latent dimensions;
- probability distribution family;
- training losses;
- rollout backend/framework.

Приоритет семантики имеет [`../modules/world-model.md`](../modules/world-model.md).

---

# 1. Capability surfaces

Future World Model должна уметь выразить capability класса:

```text
initialize / reset belief
assimilate actual percept/outcome
query one-step action-conditioned prediction
query multi-step imagination rollout
report uncertainty capability/status
compare prediction with actual outcome
inspect belief/prediction evidence
snapshot/restore/fork causally relevant world-model state
```

Research interventions проходят через explicit Intervention Gateway.

---

# 2. WorldModelDescriptor

Conceptually:

```text
WorldModelDescriptor
├── implementation identity
├── world_model_revision
├── supported input representation revisions
├── supported action representation revisions
├── prediction capabilities
├── maximum/recommended rollout horizon?
├── uncertainty capabilities
├── structured/feature prediction capabilities
├── Cortex dependency/capabilities?
└── training/research capability flags
```

Descriptor не является runtime prediction state.

---

# 3. WorldBelief

Conceptually committed belief identity должна позволять выразить:

```text
WorldBelief
├── belief_revision
├── world_model_revision
├── source state/percept/outcome identities
├── availability/status
├── optional structured hypotheses
├── optional public feature view
├── uncertainty summary?
└── provenance
```

Backend-specific recurrent/latent state может оставаться private causally relevant module state.

Consumer не получает raw private state только из-за наличия `WorldBelief`.

---

# 4. AssimilationRequest

Conceptually:

```text
AssimilationRequest
├── request_id
├── base belief revision?
├── actual Canonical Percept reference
├── actual action/outcome reference?
├── allowed RetrievalResult references?
├── causal identities
├── agent_revision
└── provenance
```

Outcome должен различать минимум:

```text
updated
no_change
uninitialized
incompatible_input
failed
```

Exact enum не frozen.

---

# 5. WorldPredictionRequest

Conceptually:

```text
WorldPredictionRequest
├── prediction_request_id
├── base belief revision
├── candidate action description/reference
├── requested prediction views/channels
├── horizon = 1
├── stochastic sampling policy?
├── uncertainty requirements?
├── causal identities
├── agent_revision
└── provenance
```

Запрос prediction не является Action Commit.

---

# 6. WorldPrediction

Conceptually:

```text
WorldPrediction
├── prediction_id
├── request_id
├── base belief revision
├── world_model_revision
├── candidate action identity
├── predicted semantic outcomes?
├── predicted external task-visible signals?
├── predicted termination semantics?
├── predicted belief reference/view?
├── feature/latent views?
├── uncertainty
├── status/degradation
├── horizon/depth
└── provenance = predicted
```

Prediction не становится observed fact автоматически.

---

# 7. Prediction Feature View

Если prediction пересекает module boundary как learned representation, conceptually требуется:

```text
WorldPredictionFeatureView
├── feature_view_id
├── prediction_id
├── feature_space_id
├── feature_space_revision
├── encoder/model identity
├── world_model_revision
├── data
└── provenance
```

Одинаковый shape не доказывает compatibility.

---

# 8. ImaginationRequest

Conceptually:

```text
ImaginationRequest
├── rollout_request_id
├── base belief revision
├── action sequence / branching action provider
├── requested horizon
├── requested prediction channels
├── stochastic sampling policy
├── stop/degradation policy
├── causal identities
└── provenance
```

Exact representation будущего Planner/action provider пока не frozen.

---

# 9. ImaginedTrajectory

Conceptually:

```text
ImaginedTrajectory
├── rollout_id
├── base belief revision
├── world_model_revision
├── branches / nodes
│   ├── depth
│   ├── candidate action
│   ├── prediction
│   ├── predicted belief identity/view
│   ├── uncertainty
│   └── parent relation
├── status/truncation/degradation
├── RNG/sampling provenance
└── provenance = imagined
```

Imagined trajectory не является Environment trajectory и не создаёт MemoryRecord автоматически.

---

# 10. Uncertainty

Contract должна уметь выразить минимум:

```text
unavailable
unknown
predictive uncertainty available
```

Если implementation заявляет decomposition:

```text
epistemic
aleatoric
```

она обязана иметь explicit estimator identity/revision и evaluation semantics.

Нельзя заполнять отсутствующую uncertainty нулём.

---

# 11. PredictionErrorEvidence

После actual Outcome Commit conceptually:

```text
PredictionErrorEvidence
├── evidence_id
├── prediction_id
├── actual outcome/percept reference
├── world_model_revision
├── channel/component errors
├── aggregate error? optional
├── likelihood/surprisal? optional
├── compatibility/status
└── provenance
```

Prediction error не является reward/intrinsic utility автоматически.

---

# 12. WorldModelRevision

Behavior identity должна позволять различать:

```text
world_model_revision
belief_revision
agent_revision
feature-space revisions
```

Изменение trainable model/adapters, влияющее на predictions, не должно молча сохранять прежнюю behavior identity.

---

# 13. Snapshot

Conceptual World Model snapshot должен уметь восстановить минимум:

```text
world_model_revision
belief revision
causally relevant private recurrent/latent state
representation manifests
behavior-relevant configuration
RNG state
intervention/degradation state
```

Trainable weight storage может ссылаться на общий Agent checkpoint manifest.

---

# 14. Observability

Evidence должна позволять ссылаться на:

```text
belief update attempt
belief revision
prediction request/result id
rollout id/branch/depth
world_model_revision
source percept/outcome/action ids
uncertainty status
prediction error evidence
failure/degradation
intervention id
```

---

# 15. Failure / degradation

Contract должен различать минимум классы:

```text
world_model_unavailable
belief_uninitialized
incompatible_belief_revision
incompatible_input_representation
unsupported_action_representation
unsupported_horizon
prediction_unavailable
uncertainty_unavailable
rollout_truncated
numerical_invalid
feature_space_mismatch
snapshot_incompatible
sub-capability_unavailable
```

Универсальный `None`/zero-vector не должен скрывать эти состояния.

---

# 16. Configurations

Должны быть различимы:

```text
NoWorldModel
DummyWorldModel
ControlWorldModel
real WorldModel
```

Control implementations могут включать:

```text
last-percept persistence
simple tabular/rule predictor
random/shuffled prediction
parameter/compute-matched predictor
oracle research control
```

Oracle control не является normal Agent input/model.

---

# 17. Что ещё не frozen

До последующих DU не фиксируются:

- exact architecture;
- latent distribution/state dimension;
- decoder/reconstruction requirement;
- exact structured prediction schema;
- uncertainty estimator/decomposition;
- exact rollout API;
- training loss/schedule;
- replay sequence format;
- privileged supervision variant;
- exact action schema;
- exact checkpoint encoding.
