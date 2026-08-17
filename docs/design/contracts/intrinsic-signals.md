# Candidate contract Intrinsic Signals MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-14 — Intrinsic Signals`

Этот документ уточняет machine-facing классы данных и capability будущей реализации Intrinsic Signal Layer.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- RND/ICM/VIME/RIDE/Plan2Explore;
- конкретную probability/density model;
- exact normalization formula;
- exact signal scalarization;
- training objective.

Приоритет семантики имеет [`../modules/intrinsic-signals.md`](../modules/intrinsic-signals.md).

---

# 1. Архитектурная форма

Future implementation должна поддерживать **несколько независимо конфигурируемых providers**, а не один обязательный scalar reward producer.

Conceptually:

```text
IntrinsicSignalProvider
├── descriptor
├── declared source dependencies
├── optional private estimator/baseline state
└── compute → IntrinsicSignal[]
```

Outputs разных providers сохраняют отдельную identity.

---

# 2. IntrinsicSignalProviderDescriptor

Conceptually:

```text
IntrinsicSignalProviderDescriptor
├── provider_id
├── provider_revision
├── supported signal kinds
├── required source capabilities
├── required representation spaces/revisions?
├── temporal scope requirements
├── history/baseline requirements
├── normalization capability
├── stochastic/RNG capability
├── snapshot capability
└── research/control capability flags
```

Descriptor не является current signal state.

---

# 3. IntrinsicSignalRequest / trigger context

Не каждый provider требует отдельного imperative request от consumer, но scheduler/lifecycle boundary должна позволять выразить causal context вычисления.

Conceptually:

```text
IntrinsicSignalComputationContext
├── causal event identity
├── source state_revision
├── agent_revision
├── episode/session identity
├── actual/imagined/replayed/intervened provenance
├── declared source references
└── requested/eligible signal channels
```

Provider не получает ambient full Agent state.

---

# 4. IntrinsicSignal

Conceptually:

```text
IntrinsicSignal
├── signal_id
├── signal_kind
├── provider_id
├── provider_revision
├── source references
├── source revisions
├── raw_measure
├── normalized_measure?
├── measure_semantics
├── direction/convention
├── reference_scope
├── temporal_scope/window
├── representation_identity/revision?
├── baseline_identity/revision?
├── normalizer_identity/revision?
├── availability/status
└── provenance
```

`raw_measure` не обязано быть universal scalar; exact shape определяется signal kind contract.

---

# 5. IntrinsicSignalBundle

Conceptually:

```text
IntrinsicSignalBundle
├── bundle_id
├── causal source identity
├── state_revision / agent_revision
├── signals[]
└── provenance
```

Bundle является collection surface.

Он **не** содержит обязательного:

```text
combined_intrinsic_reward
```

и не задаёт ranking/scalarization между signals.

---

# 6. Prediction discrepancy signal

Contract должна позволять выразить:

```text
PredictionDiscrepancySignal
├── source prediction_id
├── actual outcome/percept reference
├── error metric identity
├── raw discrepancy
├── representation/channel identity
└── compatibility/revision status
```

Arbitrary discrepancy не называется probabilistic surprisal автоматически.

---

# 7. Predictive surprisal signal

Если provider имеет корректную predictive probability/density semantics:

```text
PredictiveSurprisalSignal
├── source prediction distribution identity
├── actual outcome reference
├── probability/density semantics
├── surprisal measure
└── calibration/validity metadata?
```

Если compatible probability model отсутствует, channel должен быть `unavailable`, а не подменяться MSE.

---

# 8. Novelty signal

Conceptually:

```text
NoveltySignal
├── current experience/percept/event reference
├── novelty estimator identity
├── reference history identity/revision
├── reference scope
├── representation identity/revision?
├── distance/density semantics?
├── raw novelty measure
└── provenance
```

Reference scope является обязательной semantic частью novelty.

---

# 9. Visitation rarity signal

Conceptually:

```text
VisitationRaritySignal
├── visitation subject identity/description
├── count/density model identity
├── count/density state revision
├── scope/reset semantics
├── representation identity/revision?
├── raw rarity/count/pseudo-count evidence
└── provenance
```

Exact transformation в exploration bonus не относится к DU-14.

---

# 10. Information gain signal

Conceptually:

```text
InformationGainSignal
├── knowledge model identity/revision
├── prior/before belief reference
├── actual evidence reference
├── posterior/after belief reference
├── estimator semantics
├── information-gain measure
└── validity/status
```

Если meaningful before/after knowledge representation отсутствует, signal `unavailable`.

---

# 11. Uncertainty change signal

Conceptually:

```text
UncertaintyChangeSignal
├── uncertainty estimator identity/revision
├── before uncertainty reference/value
├── after uncertainty reference/value
├── signed convention
├── change measure
└── compatibility/status
```

Нельзя сравнивать before/after values из несовместимых estimator revisions без explicit compatibility semantics.

---

# 12. Competence change signal

Conceptually:

```text
CompetenceChangeSignal
├── competence domain/target identity
├── self-model revision(s)
├── baseline/window identity
├── before estimate/evidence
├── after estimate/evidence
├── signed competence change
├── optional absolute-progress derived measure
└── provenance
```

Signed change и absolute magnitude являются разными channels/semantics.

---

# 13. NormalizationState

Если provider поддерживает normalization:

```text
NormalizationState
├── normalizer_id
├── normalizer_revision
├── provider/signal kind
├── scope
├── statistics/state
├── update policy
├── frozen/adaptive/offline mode
└── source provenance
```

Normalized signal всегда ссылается на конкретную normalizer revision.

---

# 14. Provider private state

Stateful provider может иметь causally relevant private state, например:

```text
visitation counts
reference embeddings/history
density-model state
moving prediction baseline
competence-progress window
normalization statistics
learned estimator parameters
RNG
```

Такое состояние следует transactional/snapshot semantics `DU-04/05`.

---

# 15. Failure/status semantics

Contract должна различать, где применимо:

```text
available
unknown
unavailable
insufficient_history
incompatible_revision
out_of_domain
stale
failed
```

Universal zero/`None` failure sentinel запрещён.

---

# 16. Provenance classes

Signal должен сохранять distinction минимум между:

```text
actual natural experience
intervened actual experience
imagined/predicted experience
training replay recomputation
offline post-hoc computation
research oracle/control
```

Эти signal records не являются взаимозаменяемыми.

---

# 17. Snapshot

Conceptual `IntrinsicSignalLayerSnapshot` должен уметь сохранить:

```text
provider identities/revisions
provider private states
history/count/density states
normalizer states
representation compatibility manifests
RNG states
intervention/degradation state
```

Exact serialization будет определена в `DU-27`.

---

# 18. No/Dummy/Control

Contract должна позволять composition-level варианты:

```text
NoIntrinsicSignals
DummySignalProvider
ConstantSignalProvider
RandomSignalProvider
ShuffledSignalProvider
MatchedNoiseProvider
OracleResearchSignalProvider
```

Oracle provider всегда маркируется privileged research provenance.

---

# 19. Что остаётся candidate

До contract freeze не определены:

- конкретный set signal kinds первой software version;
- scalar/vector representation каждого measure;
- exact provider interface;
- shared bundle storage shape;
- normalization algorithms;
- count/density/novelty estimators;
- information-gain estimator;
- competence-progress window formula;
- provider scheduling details beyond `DU-05` semantics;
- training integration;
- downstream Drives/Valuation interface.
