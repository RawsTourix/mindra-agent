# Candidate contract Appraisal MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-16 — Appraisal`

Этот документ уточняет machine-facing классы данных и capability будущего `Appraisal System`.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- concrete neural architecture;
- concrete Cortex prompt;
- точный список mandatory dimensions первой software version;
- universal scalar valence/utility;
- emotion labels;
- exact normalization/calibration formula;
- training objective.

Приоритет семантики имеет [`../modules/appraisal.md`](../modules/appraisal.md).

---

# 1. Архитектурная форма

Future implementation должна поддерживать event-centered `Appraisal System` с typed multidimensional outputs.

Conceptually:

```text
AppraisalSystem
├── descriptor
├── dimension providers/estimators
├── optional private estimator state
├── appraise
├── reappraise
├── inspect
├── snapshot
└── restore
```

`Appraisal System` не выбирает action и не вычисляет universal utility.

---

# 2. AppraisalSystemDescriptor

Conceptually:

```text
AppraisalSystemDescriptor
├── system_id
├── system_revision
├── dimension_schema_revision
├── supported target modes
├── supported dimensions
├── required source capabilities
├── partial-profile capability
├── Cortex-assisted capability?
├── learned/fixed capability
├── stochastic/RNG capability
├── snapshot capability
└── research/control capability flags
```

Descriptor не является current appraisal state.

---

# 3. AppraisalTarget

Conceptually:

```text
AppraisalTarget
├── target_id
├── target_kind
├── target_mode
├── source causal identity/revision
├── target_event_time
├── horizon?
├── semantic payload/reference
├── observed/predicted/imagined/retrieved/intervened provenance
└── availability/status
```

`target_mode` должен позволять отличить как минимум:

```text
actual
predicted
imagined
retrospective/retrieved
intervened
replayed/offline
```

Exact enum names пока не frozen.

---

# 4. AppraisalContext

Conceptually:

```text
AppraisalContext
├── context_id
├── evaluation logical time
├── state_revision
├── agent_revision
├── relevant Goal references/revision
├── relevant DriveState references/revision
├── World Belief/Prediction references?
├── Self Belief/Prediction references?
├── RetrievalResult references?
├── IntrinsicSignal references?
├── percept/outcome/task-feedback references?
├── degradation state?
└── intervention provenance?
```

Appraisal component не получает ambient full Agent state.

---

# 5. AppraisalRequest

Conceptually:

```text
AppraisalRequest
├── request_id
├── target
├── context
├── requested/required dimensions
├── execution budget/capabilities?
├── expected output requirements
└── provenance
```

Consumer может запрашивать subset dimensions, если composition/experiment это допускает.

---

# 6. AppraisalDimensionDescriptor

Conceptually:

```text
AppraisalDimensionDescriptor
├── dimension_id
├── dimension_revision
├── semantic definition
├── value domain/shape
├── direction/convention
├── required source types
├── applicability rules
├── estimator/rule identity
├── confidence/support capability
├── normalization/calibration revision?
└── intervention capability
```

Одно название dimension без semantic definition недостаточно.

---

# 7. AppraisalDimensionValue

Conceptually:

```text
AppraisalDimensionValue
├── dimension_id/revision
├── value / relation / distribution
├── availability/status
├── source references
├── estimator/rule revision
├── confidence/support?
├── normalization/calibration metadata?
├── target/context references
└── provenance
```

`0` является валидным значением только если это определено dimension semantics и не означает автоматически unknown/unavailable.

---

# 8. GoalCongruenceEntry

Conceptually:

```text
GoalCongruenceEntry
├── goal_id
├── goal_revision
├── relation
├── magnitude?
├── evidence references
├── availability/status
└── provenance
```

Relation может conceptually выражать:

```text
facilitating
obstructing
neutral
mixed
unknown
```

Exact encoding не frozen.

Goal congruence не scalarize весь Goal Graph.

---

# 9. DriveConducivenessEntry

Conceptually:

```text
DriveConducivenessEntry
├── drive_id
├── drive_revision
├── relation to regulation/pressure
├── magnitude?
├── actual/predicted semantics
├── evidence references
├── availability/status
└── provenance
```

Это appraisal target относительно drive, а не committed next `DriveState`.

---

# 10. Expectedness

Expectedness dimension должна ссылаться на prior predictive evidence, если такой evidence необходим выбранной semantics.

Conceptually:

```text
ExpectednessValue
├── relation to prior expectation
├── prior prediction reference?
├── outcome/target reference
├── IntrinsicSignal discrepancy/surprisal reference?
├── estimator revision
└── status/provenance
```

Если prior expectation отсутствует, нельзя молча публиковать neutral zero.

---

# 11. Controllability

Conceptually dimension metadata должна различать:

```text
controllability of situation/consequence by available actions
```

от competence конкретного Agent.

Возможные evidence sources:

- World Model action-conditioned alternatives;
- Environment action contract, если agent-visible;
- learned causal estimator.

Evaluator oracle controllability допустима только research-control способом.

---

# 12. CopingPotential

Conceptually:

```text
CopingPotentialValue
├── target/consequence reference
├── Self Prediction/competence references
├── available capability/resource references
├── World alternatives references?
├── estimate
├── estimate support/uncertainty?
└── provenance
```

Coping potential не выбирает coping strategy/action.

---

# 13. Urgency

Conceptually:

```text
UrgencyValue
├── response horizon/deadline semantics
├── consequence deterioration/irreversibility evidence?
├── estimate
├── availability/status
└── provenance
```

Urgency не является Salience или action priority.

---

# 14. AppraisalProfile

Conceptually:

```text
AppraisalProfile
├── profile_id
├── target_id
├── context_id
├── appraisal_system_revision
├── dimension_schema_revision
├── dimensions by id
├── completeness/partial status
├── required-dimension satisfaction
├── optional local polarity summary?
└── provenance
```

Profile не содержит mandatory global utility/action value.

---

# 15. AppraisalRecord

`AppraisalRecord` связывает profile с causal history.

Conceptually:

```text
AppraisalRecord
├── appraisal_id
├── target
├── context
├── profile
├── evaluation logical time
├── parent/reappraisal relation?
├── state/agent revisions
├── actual/predicted/imagined/etc provenance
├── intervention/degradation metadata?
└── status
```

Record, однажды committed как historical fact, не переписывается при reappraisal.

---

# 16. ReappraisalRequest / relation

Conceptually:

```text
ReappraisalRequest
├── original target reference
├── prior appraisal reference?
├── new AppraisalContext
├── requested dimensions
└── reappraisal reason/provenance
```

Result создаёт новый `AppraisalRecord`.

Conceptual relation:

```text
new_appraisal.reappraisal_of = prior_appraisal_id
```

---

# 17. Optional local polarity summary

Если implementation/experiment требует local polarity:

```text
LocalPolaritySummary
├── value
├── aggregator_id/revision
├── source dimension ids
├── aggregation semantics
├── availability/status
└── provenance
```

Он не является:

```text
utility
action_value
state_value
reward
```

и не заменяет underlying profile.

---

# 18. Dimension providers

Future implementation может conceptually иметь:

```text
AppraisalDimensionProvider
├── descriptor
├── declared source dependencies
├── optional private estimator state
└── compute → one/more dimension values
```

Несколько providers могут работать в одной Appraisal boundary.

Они не получают write authority чужим canonical namespaces.

---

# 19. Partial profiles

Contract должен различать:

```text
complete
partial
failed
```

и per-dimension statuses.

Если downstream consumer требует dimension X, наличие profile без X не считается автоматически successful compatible result.

Compatibility должна проверяться явно.

---

# 20. Observability

Evidence Plane должен позволять восстановить минимум:

- Appraisal request identity;
- target/context revisions;
- какие dimensions запрашивались;
- какие providers/estimators участвовали;
- dimension outputs/status;
- evidence references;
- Cortex call, если был;
- partial/failure/degradation;
- commit/reappraisal relation;
- intervention provenance.

Private neural activations не обязательны общей Appraisal capability.

---

# 21. Intervention

Conceptually:

```text
AppraisalIntervention
├── intervention_id
├── target appraisal/profile/dimension
├── base revision
├── treatment
├── duration/scope
├── treatment validity metadata?
└── provenance
```

Dimension intervention не меняет semantic owner.

Intervened value не маскируется под natural appraisal output.

---

# 22. Snapshot

Если Appraisal System stateful:

```text
AppraisalSystemSnapshot
├── system/dimension schema revisions
├── private estimator state
├── calibration/normalization state?
├── active lifecycle state?
├── RNG state?
├── degradation/intervention state
└── provenance
```

Historical AppraisalRecords в Memory/trajectory принадлежат соответствующим owners/artifacts и не дублируются бесконтрольно в private snapshot.

---

# 23. Failure / degradation

Contract должен различать минимум:

```text
unsupported_dimension
insufficient_context
unknown
unavailable
stale_source
incompatible_revision
partial_success
estimator_failure
Cortex_failure, если Cortex optional path использован
invalid_output
```

Hidden fallback to zero/neutral profile запрещён.

Fallback estimator допустим только explicit configured degradation policy с provenance.

---

# 24. NoAppraisal / Dummy / Control

Contract должен позволять различать:

```text
NoAppraisal
DummyAppraisal
ConstantAppraisal
RandomAppraisal
ShuffledAppraisal
MatchedNoiseAppraisal
RuleBasedAppraisal
OracleResearchAppraisal
real Appraisal
```

`NoAppraisal` означает отсутствие capability, а не fake neutral profile.

---

# 25. Что ещё не frozen

До следующих DU не фиксируются:

- точный Python `AppraisalProtocol`;
- exact mandatory dimension set первой версии;
- exact numeric ranges;
- exact local polarity formula;
- specific human emotion mapping;
- Affect update interface;
- Valuation aggregation;
- Salience mapping;
- exact learned estimator architecture;
- exact training/evaluation metrics.
