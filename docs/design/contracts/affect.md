# Candidate contract Affect MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-17 — Affect Dynamics`

Этот документ уточняет machine-facing semantic формы будущего `Affect System`.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- конкретный список affect channels;
- valence/arousal/PAD как обязательную геометрию;
- exact state dimension;
- exact decay/inertia equations;
- concrete neural architecture;
- training objective;
- scheduler/framework implementation.

Приоритет семантики имеет [`../modules/affect.md`](../modules/affect.md).

---

# 1. Архитектурная форма

Future implementation должна поддерживать agent-owned `Affect System`, который хранит committed persistent `AffectStateSet` и обновляет его из eligible `AppraisalRecord` на явных temporal boundaries.

Conceptually:

```text
AffectSystem
├── descriptor
├── AffectChannel[]
├── committed AffectStateSet
├── optional coupling logic
├── private recurrent/adaptive state
└── update / inspect / snapshot / restore
```

`Affect System` не выполняет Valuation или Policy.

---

# 2. AffectSystemDescriptor

Conceptually:

```text
AffectSystemDescriptor
├── system_id
├── system_revision
├── channel descriptors[]
├── supported lifecycle phases
├── source-mode policy
├── persistence/reset policy
├── coupling capability
├── stochastic/RNG capability
├── learned/fixed capability
├── snapshot capability
└── research/control capability flags
```

Descriptor не является текущим Affect State.

---

# 3. AffectChannelDescriptor

Conceptually:

```text
AffectChannelDescriptor
├── channel_id
├── channel_revision
├── state_semantics
├── declared Appraisal source dimensions
├── eligible source modes
├── temporal basis
├── baseline/attractor semantics?
├── inertia/decay/recovery semantics?
├── bounds/saturation semantics?
├── coupling declarations?
├── output/modulation semantics
├── stochastic/RNG capability
├── learnable/fixed capability
└── research/control flags
```

Если baseline/bounds не имеют semantic смысла, они не должны подставляться фиктивно только ради общего API.

---

# 4. AffectChannelState

Conceptually:

```text
AffectChannelState
├── channel_id
├── channel_revision
├── state_revision
├── state_payload
├── optional baseline/attractor
├── optional activation/derived summary
├── saturation/recovery state?
├── availability/status
├── last causal update
├── source Appraisal references
├── source-mode summary
├── logical-time basis
└── provenance
```

`state_payload` может быть scalar/vector/structured.

`0` является валидным значением, а не universal sentinel для unavailable/failed.

---

# 5. AffectStateSet

Conceptually:

```text
AffectStateSet
├── affect_system_revision
├── affect_state_set_revision
├── base CognitiveState revision
├── channels by channel_id
├── baseline/context revision?
├── last update causal boundary
├── availability/freshness summary
└── provenance
```

Контейнер не обязан вычислять global valence/overall mood scalar.

---

# 6. AffectUpdateContext

Каждый natural update имеет явный causal context.

Conceptually:

```text
AffectUpdateContext
├── base AffectStateSet revision
├── base CognitiveState revision
├── agent_revision
├── run/session/episode/decision/cycle identities
├── logical temporal basis / delta
├── eligible AppraisalRecord references
├── source mode per Appraisal
├── intervention/degradation provenance?
└── requested/eligible channel ids
```

Affect System не получает ambient full Agent state.

---

# 7. AffectUpdateProposal

Affect computation не мутирует committed state inplace.

Conceptually:

```text
AffectUpdateProposal
├── channel_id
├── base channel-state revision
├── proposed next state
├── source Appraisal references
├── contribution/effect summary
├── dynamics revision
├── logical temporal basis
├── availability/failure status
└── provenance
```

Accepted proposals проходят validation/coupling и только затем atomic commit.

---

# 8. Appraisal source modes

Contract должен различать минимум:

```text
actual
predicted
imagined
retrospective
intervened
replayed/offline
```

`source_mode` влияет на eligibility/update semantics и не теряется после aggregation.

Default invariants:

- actual appraisal может участвовать в natural Affect update;
- predicted appraisal может участвовать только через explicit anticipatory source policy;
- imagined appraisal по умолчанию обновляет branch-local simulated Affect, а не real committed Affect;
- retrospective current reappraisal может изменять current Affect;
- intervention остаётся treatment provenance;
- replay/offline computation не выдаётся за natural online Affect update.

---

# 9. Affect temporal lineage

Каждая committed Affect revision должна иметь causal lineage:

```text
Affect A_t
+
AppraisalRecord ids
+
logical boundary
+
dynamics revision
→ Affect A_(t+1)
```

Нельзя публиковать state без возможности определить, на основании каких Appraisal revisions он изменился.

---

# 10. Appraisal ↔ Affect scheduling

Если Appraisal использует prior Affect как context, contract должен поддерживать только committed previous-revision dependency.

Conceptually:

```text
Affect A_t
→ Appraisal R_t
→ Affect A_(t+1)
```

Нельзя разрешать recursive same-wave read/write cycle между Appraisal и Affect.

---

# 11. Branch-local simulated Affect

Imagination/counterfactual path может использовать отдельную state lineage:

```text
SimulatedAffectState
├── parent real Affect revision
├── branch identity
├── imagined Appraisal references
├── simulated revisions
└── provenance = imagined/counterfactual
```

Она не становится real committed Affect без отдельной explicit promotion/intervention semantics.

---

# 12. AffectView

Допускается derived representation для consumers.

Conceptually:

```text
AffectView
├── view_id
├── view_revision
├── source AffectStateSet revision
├── mapping/encoder revision
├── representation kind
├── availability
└── data
```

Примеры могут включать valence-arousal view или learned compact view.

View не является canonical source of truth Affect.

---

# 13. Baseline/persistence state

Если Affect implementation имеет baseline/attractor/recovery state, contract должен явно различать:

```text
current state
baseline/attractor
runtime adaptive baseline
fixed configuration
agent-long-lived parameters/traits, если существуют
```

`Environment.reset()` не означает автоматический Affect reset.

---

# 14. Affect intervention

Conceptually:

```text
AffectIntervention
├── intervention_id
├── target channel/state/parameter
├── base Affect/CognitiveState revision
├── treatment
├── duration/scope
└── provenance
```

Допустимые классы targets могут включать:

- channel state;
- baseline;
- decay/inertia/recovery parameter;
- source eligibility;
- coupling;
- dynamics implementation;
- reset/clamp.

Intervention не маскируется под natural update.

---

# 15. Failure/degradation

Contract должен различать минимум:

```text
success
partial
unavailable
failed
stale-base
incompatible revision
```

Если update не состоялся:

- предыдущий committed Affect State остаётся исторически валидным;
- freshness/status отражает пропущенный update;
- private state не может тайно продвинуться вперёд;
- fake neutral value не публикуется.

---

# 16. Snapshot

Conceptually:

```text
AffectSystemSnapshot
├── AffectStateSet
├── system/channel revisions
├── baseline/attractor state
├── private recurrent/adaptive state
├── dynamics/coupling revision refs
├── adaptive normalization/history
├── last logical update
├── source eligibility state
├── RNG state
└── intervention/degradation state
```

Snapshot обязан включать всё, что может изменить future Affect trajectory.

---

# 17. Control implementations

Contract должен позволять композиционно подменять Affect System на:

```text
NoAffect
DummyAffect
ConstantAffect
FrozenAffect
ResetEveryEventAffect
LeakyIntegratorControl
RandomAffect
ShuffledHistoryAffect
TimePermutedAffect
MatchedRecurrentControl
RuleBasedAffect
```

Все control implementations сохраняют тот же downstream boundary там, где capability присутствует.

`NoAffect` означает отсутствие capability, а не fake zero state.

---

# 18. Observability

Research evidence должна позволять получить, где применимо:

```text
before/after AffectStateSet
per-channel before/after
source AppraisalRecord ids
source modes
channel contribution summaries
dynamics/baseline revisions
saturation/recovery events
failure/degradation
intervention provenance
```

Private neural activations являются optional research capability, а не обязательной частью общего contract.

---

# 19. Versioning

Нужно различать минимум:

```text
affect_system_revision
channel_revision
affect_state_revision
dynamics_revision
view/feature revision
agent_revision
```

Если learned dynamics revision меняет geometry/meaning private state, старое состояние не считается автоматически совместимым.

---

# 20. Запрещённые implicit outputs

Affect contract не содержит как обязательные authoritative outputs:

```text
emotion_label
global_valence
reward
utility
action_value
goal mutation
salience allocation
memory retention decision
policy action
```

Такие функции относятся к другим boundaries или optional research views.

---

# 21. Что остаётся candidate

До downstream DU и contract freeze остаются открытыми:

- exact channel taxonomy;
- state shapes/types;
- low-dimensional view;
- update equations;
- source weights;
- persistence defaults;
- learned model architecture;
- training objective;
- downstream consumers;
- serialization format;
- exact Python API.
