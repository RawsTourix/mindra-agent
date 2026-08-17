# Candidate contract Drives MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-15 — Drives`

Этот документ уточняет machine-facing классы данных и capability будущего `Drive System`.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- конкретный список drives;
- exact state dimensions;
- exact homeostatic distance function;
- конкретный coupling framework;
- concrete training objective;
- concrete scheduler implementation.

Приоритет семантики имеет [`../modules/drives.md`](../modules/drives.md).

---

# 1. Архитектурная форма

Future implementation должна поддерживать единый agent-owned `Drive System`, содержащий несколько typed drive components.

Conceptually:

```text
DriveSystem
├── descriptor
├── DriveComponent[]
├── committed DriveStateSet
├── optional coupling logic
├── private dynamics state
└── update / inspect / snapshot / restore
```

`Drive System` не scalarize drives и не выбирает action.

---

# 2. DriveSystemDescriptor

Conceptually:

```text
DriveSystemDescriptor
├── system_id
├── system_revision
├── drive descriptors[]
├── supported lifecycle phases
├── persistence/reset policy
├── coupling capability
├── stochastic/RNG capability
├── learned/fixed capability
├── snapshot capability
└── research/control capability flags
```

Descriptor не является текущим Drive State.

---

# 3. DriveDescriptor

Conceptually:

```text
DriveDescriptor
├── drive_id
├── drive_revision
├── drive_kind / dynamics_semantics
├── required update sources
├── state semantics
├── pressure semantics
├── target/range semantics?
├── bounds/saturation semantics?
├── decay/recovery semantics?
├── persistence scope
├── coupling declarations?
├── stochastic/RNG capability
├── learnable/fixed capability
└── research/control flags
```

Если target/range не имеет semantic смысла, поле должно быть unavailable/not-applicable, а не фиктивным числом.

---

# 4. DriveState

Conceptually:

```text
DriveState
├── drive_id
├── drive_revision
├── state_revision
├── internal_state
├── target/range?
├── regulatory_deviation?
├── pressure/activation
├── saturation/recovery state?
├── availability/status
├── logical time / causal event of last update
├── source revisions
└── provenance
```

`internal_state` и `pressure` могут иметь разные shapes.

`pressure=0` является валидным значением, а не универсальным обозначением отсутствия drive.

---

# 5. DriveStateSet

Conceptually:

```text
DriveStateSet
├── drive_system_revision
├── drive_state_set_revision
├── base CognitiveState revision
├── states by drive_id
├── coupling revision?
├── availability summary
└── provenance
```

Drive states сохраняют отдельную identity; контейнер не вычисляет global motivation score.

---

# 6. DriveUpdateContext

Каждый update должен иметь явный causal context.

Conceptually:

```text
DriveUpdateContext
├── base DriveStateSet revision
├── base CognitiveState revision
├── agent_revision
├── run/session/episode/decision identities
├── logical temporal basis / delta
├── declared IntrinsicSignal references
├── declared agent-visible event/outcome references
├── declared Goal/Self/internal-resource references
├── intervention provenance?
└── requested/eligible drive ids
```

Drive component не получает ambient full Agent state.

---

# 7. DriveUpdateProposal

Drive computation не мутирует committed state inplace.

Conceptually:

```text
DriveUpdateProposal
├── drive_id
├── base drive state revision
├── proposed next state
├── source references
├── update reason
├── dynamics revision
├── availability/failure status
└── provenance
```

Все accepted proposals текущей Drive update boundary проходят validation/coupling и только затем atomic commit.

---

# 8. Cross-drive coupling

Если coupling существует, он должен иметь explicit identity/revision.

Conceptually:

```text
DriveCouplingDescriptor
├── coupling_id
├── coupling_revision
├── source drive ids
├── target drive ids
├── semantics
├── temporal rule
└── learnable/fixed capability
```

Default semantics для взаимного влияния:

```text
all components read committed DriveStateSet_t
→ compute staged next states
→ coupling/validation
→ commit DriveStateSet_(t+1)
```

Нельзя читать private staged state соседа и создавать instantaneous hidden cycle.

---

# 9. Goal Proposal boundary

Drive capability может участвовать в формировании `Goal Proposal`, но contract не даёт write authority Goal Graph.

Conceptually возможно:

```text
DriveGoalProposalRequest/Result
```

или отдельный adapter/proposer, использующий committed Drive State.

Exact ownership этой auxiliary capability уточнится после `DU-16…18/22`.

Обязательный invariant:

```text
Drive State
→ Goal Proposal
→ Goal System
```

а не direct Goal mutation.

---

# 10. Valuation boundary

Future `Valuation` получает Drive State через explicit declared read surface.

Drive contract не содержит:

```text
utility
action_value
state_value
reward
winning_drive
```

как обязательные outputs.

---

# 11. Homeostatic drive semantics

Если `drive_kind` homeostatic, contract должен позволять выразить:

```text
regulated_state
homeostatic target/range
regulatory deviation/deficit
pressure mapping
```

Target/range и mapping имеют собственную revision/provenance.

Exact metric может быть scalar/vector/nonlinear и не фиксируется `DU-15`.

---

# 12. Adaptive motivational drive semantics

Если drive не имеет true set-point, contract должен позволять явно определить другую dynamics semantics, например:

```text
accumulation
satiation
recovery
habituation
sensitivity
```

Такой drive не обязан публиковать fake `regulatory_deviation`.

---

# 13. InitialDriveState

Initialization должна быть explicit.

Conceptually:

```text
DriveInitialization
├── drive_id
├── mode
├── fixed state / distribution / snapshot reference
├── RNG state/seed?
├── session/agent context
└── provenance
```

Hidden random initialization запрещена.

---

# 14. Reset semantics

Contract должен позволять различать:

```text
Environment episode reset
Agent Session reset
Drive-specific reset
Snapshot restore
```

Каждый drive descriptor сообщает свой persistence scope/reset behavior.

---

# 15. DriveIntervention

Research intervention conceptually содержит:

```text
DriveIntervention
├── intervention_id
├── target drive / field
├── base revision
├── treatment
├── duration/scope
├── restoration semantics
└── provenance
```

Возможные treatment classes:

- state clamp;
- state offset/replace;
- target/range change;
- dynamics parameter change;
- coupling change;
- input sensitivity change.

Exact intervention API определяется общей `Intervention Gateway` boundary.

---

# 16. DriveSystemSnapshot

Conceptually:

```text
DriveSystemSnapshot
├── DriveStateSet
├── system/drive revisions
├── targets/ranges
├── private dynamics state
├── coupling state
├── last logical update metadata
├── adaptive baselines/history
├── RNG state
├── initialization/reset state
├── intervention/degradation state
└── compatibility manifest
```

Если causally relevant часть состояния не восстановлена, exact counterfactual claim запрещён.

---

# 17. Availability / failure

Contract должен различать минимум семантически:

```text
available
unavailable
insufficient_input
incompatible_revision
invalid_state
degraded
failed
```

Exact enum names будут frozen позже.

Нельзя заменять failure на fake neutral drive.

---

# 18. Control implementations

Общая boundary должна поддерживать:

```text
NoDrives
DummyDriveSystem
ConstantDrive
ClampedDrive
RandomDrive
ShuffledDrive
TimePermutedDrive
MatchedNoiseDrive
RuleBasedHomeostaticDrive
```

`NoDrives` означает отсутствие capability, а не набор нулевых drive states.

---

# 19. Versioning

Нужно различать минимум:

```text
agent_revision
drive_system_revision
drive_revision
drive_state_set_revision
coupling_revision
target/range revision
```

После изменения dynamics/config старое Drive State не должно молча интерпретироваться новой semantics без compatibility policy.

---

# 20. Что остаётся candidate

До contract freeze открыты:

- exact type system;
- exact drive list;
- state dimensions;
- scalar/vector pressure conventions;
- update cadence;
- coupling implementation;
- target/range metrics;
- learned dynamics architecture;
- Goal Proposal auxiliary API;
- exact snapshot serialization.
