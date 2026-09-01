# V0.2-IS-03 — Environment Contract Shape

## Статус

**Статус:** `accepted step-specific clarification`  
**Этап:** `V0.2-IS-03 — Environment contracts & capability split`  
**Semantic baseline:** `F31`  
**Version design:** `docs/versions/v0.2/README.md` — accepted  
**Implementation sequence:** `docs/versions/v0.2/implementation-sequence.md` — accepted  
**Входной implementation baseline:** `c3f2dfb411c92d3048bd833732fdc18d696ec282` — accepted `V0.2-IS-02`

Этот документ снимает implementation ambiguity `IS-03`. Он не меняет `DU-07`, `ADR-0007`, F31, version scope или порядок implementation sequence.

`IS-03` фиксирует **только contracts/capability boundaries**. Concrete MicroWorld dynamics, RNG engines, snapshot contents, world generation и task fixtures остаются `IS-04+`.

---

# 1. Причина clarification

Canonical `docs/design/contracts/environment.md` намеренно имеет статус candidate semantic contract и прямо не фиксирует Python API. Accepted `v0.2` sequence уже требует machine-facing contracts перед concrete engine.

Без clarification Codex пришлось бы самостоятельно выбирать:

- package split;
- exact `RawObservation` envelope;
- форму reset control;
- typed action representation;
- post-commit Environment input;
- `InteractionResult`/transition receipt join;
- snapshot abstraction без преждевременного serialization format;
- exact `EnvironmentInteraction` / `EnvironmentResearch` Protocol methods;
- clone/fork return type;
- enforceable Agent/Research record separation.

`IS-03` принимает narrow additive shape ниже.

---

# 2. Package split

Создать минимум:

```text
src/mindra/contracts/environment.py
src/mindra/contracts/interaction.py
```

Распределение responsibility:

```text
environment.py
→ Environment descriptors
→ research-only descriptors/records
→ snapshot metadata/protocol
→ EnvironmentInteraction / EnvironmentResearch Protocols
→ capability bundle только для composition/research wiring

interaction.py
→ agent/execution-facing typed actions
→ observation/task/feedback records
→ episode reset request/result
→ committed-environment-action envelope
→ interaction result / transition receipt
```

Допустим небольшой internal helper для common validation, но нельзя создавать generic framework следующего step.

Оба файла находятся в `contracts`, используют только stdlib и не импортируют `runtime`, `reference`, `composition` или `entrypoints`.

---

# 3. Existing causal identities

`IS-03` переиспользует уже принятые `IS-01` identities:

```text
EpisodeId
ObservationId
ExternalTaskId
ActionCommitId
EnvironmentTransitionId
EnvironmentSnapshotId
WorldInstanceId
```

Не создавать параллельные UUID identity-типы с тем же meaning.

Ownership сохраняется:

```text
EpisodeId
→ future InteractionRuntime

ObservationId
ExternalTaskId
EnvironmentTransitionId
EnvironmentSnapshotId
WorldInstanceId
→ Environment/reference implementation boundaries через injected IdFactory

ActionCommitId
→ future Action Commit boundary
```

Contracts сами identities не аллоцируют.

---

# 4. Contract revision/value rules

Environment contracts используют explicit non-negative integer revisions там, где version design требует schema/interface revision.

Минимум различать:

```text
interaction_interface_revision
observation_schema_revision
action_schema_revision
task_schema_revision
feedback_schema_revision
snapshot_contract_revision
```

На `IS-03` не требуется добавлять их в global `revisions.py` как новые monotonic runtime revision classes: они являются immutable descriptor metadata, а не mutable committed-state revisions.

Каждый revision field:

- exact `int`, не `bool`;
- `>= 0`.

Version/family/schema labels:

- exact `str`;
- non-empty;
- canonical whitespace-free token where field является identity-like label.

Не вводить SemVer parser/framework.

---

# 5. Agent-visible scalar/field vocabulary

Чтобы `RawObservation`, task specification и feedback были immutable/snapshot-safe без конкретной grid representation, `IS-03` вводит маленький structured public payload vocabulary.

Conceptually:

```text
AgentVisibleScalar = None | bool | int | float | str

AgentVisibleField
├── name: str
└── value: AgentVisibleScalar | tuple[AgentVisibleScalar, ...]

AgentVisibleRecord
├── kind: str
└── fields: tuple[AgentVisibleField, ...]
```

Exact class names могут быть `AgentVisibleField` / `AgentVisibleRecord` либо эквивалентные, но semantics обязательны.

Rules:

- frozen dataclasses;
- field names non-empty;
- duplicate field names в одном record rejected;
- tuples immutable;
- mutable mappings/lists/sets/object payloads запрещены;
- `float` должен быть finite; NaN/±inf rejected;
- order tuple является contract data; implementation обязана формировать deterministic order;
- records не имеют generic `metadata: dict[str, object]` / `info` escape hatch.

Это **не** concrete MicroWorld observation schema. `IS-04` будет строить grid/entity observations из этих public records или accepted equivalent specialization без раскрытия hidden state.

---

# 6. EnvironmentInteractionDescriptor

Frozen agent/execution-facing descriptor exact meaning:

```text
EnvironmentInteractionDescriptor
├── environment_family: str
├── environment_semantic_version: str
├── interaction_interface_revision: int
├── observation_schema_revision: int
├── task_schema_revision: int
├── feedback_schema_revision: int
└── action_capability: ActionCapabilityDescriptor
```

Он намеренно **не содержит**:

```text
engine_version
generator_version
distribution_id
distribution_version
split label
WorldInstanceId
world manifest ref
seed / RNG state
hidden rule mapping
oracle/solver metadata
research objective metric
```

`describe_interaction()` возвращает только этот safe descriptor.

---

# 7. EnvironmentDescriptor — Research Plane

Frozen research-facing descriptor:

```text
EnvironmentDescriptor
├── interaction: EnvironmentInteractionDescriptor
├── engine_version: str
├── generator_version: str
├── task_family: str
├── task_version: str
├── distribution_id: str
├── distribution_version: str
├── world_instance_id: WorldInstanceId
└── world_manifest_ref: str | None
```

Этот descriptor privileged и не является agent-visible interaction output.

`world_manifest_ref` — opaque research reference на `IS-03`; exact WorldManifest content появится вместе с concrete MicroWorld generation в `IS-04/IS-05`.

Не добавлять hidden world state object прямо в descriptor.

---

# 8. Typed v0.2 action vocabulary

Exact v0.2 action types:

```text
Direction
├── NORTH
├── EAST
├── SOUTH
└── WEST

Move(direction)
Interact(direction)
Pickup(direction)
Drop(direction)
Wait()
```

Все action records frozen.

Canonical semantic union:

```text
EnvironmentAction = Move | Interact | Pickup | Drop | Wait
```

Не добавлять в `IS-03`:

```text
Use
Turn
Look
Attack
Navigate
arbitrary command strings
free-form kwargs
```

`Wait` является explicit valid no-op intent, а не `None`.

Structural invalidity определяется construction/type validation. World-level blocked/no-effect semantics появятся в concrete Environment `IS-04` и не являются contract construction error.

---

# 9. ActionCapabilityDescriptor

Frozen descriptor:

```text
ActionCapabilityDescriptor
├── action_schema_revision: int
└── supported_action_kinds: tuple[str, ...]
```

Canonical v0.2 action kind labels:

```text
move
interact
pickup
drop
wait
```

Rules:

- tuple unique;
- canonical lexical order;
- unknown kind rejected;
- empty set rejected;
- capability descriptor сообщает schema capability, но не dynamic hidden-state action mask.

Он не сообщает, например, что конкретная скрытая дверь сейчас locked или какой action oracle считает оптимальным.

---

# 10. RawObservation

`RawObservation` — frozen agent-visible envelope:

```text
RawObservation
├── observation_id: ObservationId
├── observation_schema_revision: int
└── records: tuple[AgentVisibleRecord, ...]
```

`RawObservation` не содержит causal research identities кроме собственного `ObservationId`.

Запрещённые fields/escape hatches:

```text
world_instance_id
seed
rng_state
split
distribution_id
world_manifest
hidden_state
hidden_rules
ground_truth
oracle
objective_metric
research_transition
info: dict
metadata: dict[str, object]
```

Observation не содержит `EpisodeId`/`DecisionWindowId`: logical scope назначает runtime ingress/provenance, а Environment output остаётся external typed datum.

---

# 11. ExternalTaskSpecification

Frozen agent-visible external task contract:

```text
ExternalTaskSpecification
├── external_task_id: ExternalTaskId
├── task_schema_revision: int
├── task_kind: str
└── parameters: tuple[AgentVisibleField, ...]
```

Rules:

- `task_kind` non-empty canonical label;
- parameters unique by name;
- только intentionally disclosed task information;
- никакого GoalProposal/GoalId/CommittedGoal;
- никакого solver path/oracle answer/hidden success rule, если они не являются самим public task contract.

Exact distinction остаётся:

```text
ExternalTaskSpecification
≠ GoalProposal
≠ CommittedGoal
```

---

# 12. ExternalTaskFeedback

Добавить enum:

```text
ExternalTaskFeedbackStatus
├── IN_PROGRESS
├── SUCCEEDED
└── FAILED
```

Frozen feedback:

```text
ExternalTaskFeedback
├── external_task_id: ExternalTaskId
├── feedback_schema_revision: int
├── status: ExternalTaskFeedbackStatus
└── events: tuple[AgentVisibleRecord, ...]
```

Feedback — только то, что task contract намеренно сообщает Agent.

Он не содержит objective evaluator metric автоматически.

`None` остаётся valid способом отсутствия feedback в `EpisodeStartResult`/`InteractionResult`.

---

# 13. Agent-visible action outcome

Для v0.2 достаточно narrow optional outcome:

```text
AgentVisibleActionOutcomeStatus
├── EFFECT
└── NO_EFFECT

AgentVisibleActionOutcome
├── status
└── events: tuple[AgentVisibleRecord, ...]
```

Privileged failure reason не включается.

Malformed/structurally invalid action не превращается в `NO_EFFECT`: это contract error до normal Environment transition.

World-level valid blocked action может стать `NO_EFFECT`.

---

# 14. Episode reset control

`EpisodeStartRequest` является runtime/control input Environment, а не Agent observation.

Чтобы future `IS-04/IS-05` могли reproducibly выбрать world/task без изменения method signature, добавить research/control-only frozen form:

```text
EnvironmentEpisodeControl
├── world_manifest_ref: str | None
├── generation_seed: int | None
├── dynamics_seed: int | None
├── task_seed: int | None
└── full_observation: bool
```

`None` seed означает, что конкретная configured Environment family выбирает значение через свою deterministic/configured policy; exact generation policy реализуется позже.

`EnvironmentEpisodeControl` не возвращается Agent и не вкладывается в `EpisodeStartResult`/`RawObservation`.

`EpisodeStartRequest`:

```text
EpisodeStartRequest
├── episode_id: EpisodeId
└── control: EnvironmentEpisodeControl | None
```

`EpisodeId` создаёт future `InteractionRuntime`, не Environment.

`IS-03` не реализует reset history/abort state machine.

---

# 15. EpisodeStartResult

Frozen agent-visible result:

```text
EpisodeStartResult
├── raw_observation: RawObservation
├── external_task: ExternalTaskSpecification | None
├── external_feedback: ExternalTaskFeedback | None
├── terminated: bool
└── truncated: bool
```

Для successful reset `IS-03` contract требует:

```text
terminated is False
truncated is False
```

Research reset evidence/manifest/seed не входят в этот result.

Final task/observation identity появляется только в agent-visible records; current Episode/Decision logical scope задаётся будущим InteractionRuntime ingress.

---

# 16. Narrow post-Action-Commit Environment input

`IS-03` не реализует Action Boundary/authorization/commit state machine, но Environment interface должен иметь typed causal input, который later `IS-09` сможет производить без API redesign.

Добавить frozen transport-neutral envelope:

```text
CommittedEnvironmentAction
├── action_commit_id: ActionCommitId
└── action: EnvironmentAction
```

Этот type:

- **не является** `ActionCommitRecord`;
- не создаёт Action Commit;
- не проверяет authorization;
- не содержит dispatch/retry/reconciliation state;
- является только минимальным Environment-facing immutable semantic payload после already-existing commit boundary.

Создавать его до Action Commit future runtime path запрещено orchestration semantics, но `IS-03` contracts не реализуют этот state machine.

---

# 17. Environment transition ref/receipt

Frozen causal reference:

```text
EnvironmentTransitionRef
└── environment_transition_id: EnvironmentTransitionId
```

Frozen execution-facing receipt:

```text
EnvironmentTransitionReceipt
├── action_commit_id: ActionCommitId
└── transition: EnvironmentTransitionRef
```

Receipt подтверждает связь опубликованного authoritative Environment transition с committed semantic action.

Receipt **не** означает task success и не раскрывает hidden world effect reason.

`EnvironmentTransitionId` создаёт Environment при фактической публикации authoritative transition, а не caller.

---

# 18. InteractionResult

Frozen agent/execution-facing result:

```text
InteractionResult
├── receipt: EnvironmentTransitionReceipt
├── raw_observation: RawObservation
├── external_feedback: ExternalTaskFeedback | None
├── action_outcome: AgentVisibleActionOutcome | None
├── terminated: bool
└── truncated: bool
```

`terminated` и `truncated` — отдельные booleans.

`IS-03` **не запрещает** ситуацию, где оба `True`: contract различает причины/semantics, а concrete family/experiment policy определяет допустимые combinations.

Agent-visible result не содержит research-only termination reason. Research transition record хранит reason/category отдельно.

---

# 19. Research generation provenance

Добавить frozen research-only metadata:

```text
EnvironmentGenerationProvenance
├── generator_version: str
├── world_manifest_ref: str | None
├── generation_seed: int | None
├── dynamics_seed: int | None
└── task_seed: int | None
```

Это research provenance, не agent-visible datum.

`IS-03` не фиксирует seed derivation algorithm; SHA-256 role derivation конкретного MicroWorld реализуется в `IS-04` согласно accepted v0.2 design.

---

# 20. Research view

Добавить frozen research-only structural view:

```text
EnvironmentResearchView
├── descriptor: EnvironmentDescriptor
├── hidden_state_ref: str
├── generation: EnvironmentGenerationProvenance
├── terminated: bool
├── truncated: bool
└── termination_reason: str | None
```

`hidden_state_ref` — opaque research reference на `IS-03`; concrete immutable hidden state records появляются в `IS-04`.

Не использовать `object`/dict escape hatch для full hidden state в generic contract.

---

# 21. Environment snapshot contract

Exact snapshot serialization/content ещё deferred `IS-04`/`DU-27`, поэтому `IS-03` **не** вводит bytes/JSON/pickle snapshot payload как canonical format.

Добавить frozen metadata:

```text
EnvironmentSnapshotMetadata
├── environment_snapshot_id: EnvironmentSnapshotId
├── world_instance_id: WorldInstanceId
├── snapshot_contract_revision: int
├── parent_snapshot_id: EnvironmentSnapshotId | None
└── environment: EnvironmentDescriptor
```

Добавить runtime-checkable Protocol:

```text
EnvironmentSnapshot
└── metadata -> EnvironmentSnapshotMetadata
```

Concrete `MicroWorldSnapshot` в `IS-04` реализует этот Protocol и содержит complete hidden state + causally relevant RNG states immutably.

Generic `IS-03` snapshot contract не содержит mutable payload property.

---

# 22. Research transition record

Добавить research-only enums/records минимум:

```text
ResearchActionOutcomeStatus
├── EFFECT
├── NO_EFFECT
└── STOCHASTIC_FAILURE

EnvironmentResearchTransitionRecord
├── environment_transition_id: EnvironmentTransitionId
├── episode_id: EpisodeId
├── world_instance_id: WorldInstanceId
├── action_commit_id: ActionCommitId
├── action: EnvironmentAction
├── pre_snapshot_id: EnvironmentSnapshotId | None
├── post_snapshot_id: EnvironmentSnapshotId | None
├── action_status: ResearchActionOutcomeStatus
├── reason: str | None
├── external_feedback: ExternalTaskFeedback | None
├── terminated: bool
├── truncated: bool
└── termination_reason: str | None
```

Research record может знать больше, чем Agent-visible `InteractionResult`.

`reason`/`termination_reason` не копируются автоматически в agent-visible outcome.

`IS-03` не реализует journal/evidence persistence этих records.

---

# 23. EnvironmentInteraction Protocol

Добавить `@runtime_checkable` Protocol exact public surface:

```python
class EnvironmentInteraction(Protocol):
    def describe_interaction(self) -> EnvironmentInteractionDescriptor: ...

    def reset(self, request: EpisodeStartRequest, /) -> EpisodeStartResult: ...

    def apply_committed_action(
        self,
        action: CommittedEnvironmentAction,
        /,
    ) -> InteractionResult: ...
```

В Protocol **нет**:

```text
inspect
hidden_state
ground_truth
snapshot
restore
clone
fork
transition_records
render_debug
seed
manifest
oracle
```

Cognitive modules вообще не получают EnvironmentInteraction object; later `InteractionRuntime` получает narrow capability.

---

# 24. EnvironmentResearch Protocol

Добавить отдельный `@runtime_checkable` Protocol:

```python
class EnvironmentResearch(Protocol):
    def inspect(self) -> EnvironmentResearchView: ...

    def snapshot(self) -> EnvironmentSnapshot: ...

    def restore(self, snapshot: EnvironmentSnapshot, /) -> None: ...

    def clone(self) -> EnvironmentCapabilities: ...

    def fork(self, snapshot: EnvironmentSnapshot, /) -> EnvironmentCapabilities: ...

    def transition_records(self) -> tuple[EnvironmentResearchTransitionRecord, ...]: ...
```

`clone()` означает независимый instance текущего exact state.

`fork(snapshot)` означает независимую research lineage от explicit snapshot.

Exact clone/fork lineage metadata и concrete hidden-state copying реализуются/tested в `IS-04`.

`restore()` не является Environment natural transition и ничего не возвращает в Agent Interaction Plane автоматически.

Renderer/debug method в general Protocol намеренно не обязателен: concrete MicroWorld Research capability может добавить research-only renderer позже без изменения Agent boundary.

---

# 25. EnvironmentCapabilities bundle

Чтобы clone/fork могли вернуть обе capability surfaces, не выдавая private core, добавить frozen wiring-only bundle:

```text
EnvironmentCapabilities
├── interaction: EnvironmentInteraction
└── research: EnvironmentResearch
```

Bundle:

- используется только composition/research infrastructure;
- не является Agent input;
- не попадает CognitiveState;
- future `InteractionRuntime` получает только `.interaction`, не весь bundle.

General contracts допускают, что arbitrary future environment один physical object удовлетворяет обоим Protocols, но reference `MicroWorld` `IS-04` обязан выдавать **разные wrapper objects** `MicroWorldInteraction` и `MicroWorldResearch` согласно accepted v0.2 design.

---

# 26. Capability/record privacy invariants

Machine-checkable `IS-03` invariants:

1. `EnvironmentInteractionDescriptor` не содержит research-only fields.
2. `RawObservation` не содержит research-only fields/metadata dict.
3. `ExternalTaskSpecification` и `ExternalTaskFeedback` не содержат oracle/objective metric fields.
4. `EpisodeStartResult` не содержит reset control, seed, manifest или research view.
5. `InteractionResult` не содержит hidden outcome reason, manifest, seed, world instance id или research transition record.
6. `EnvironmentInteraction` не предоставляет research methods.
7. `EnvironmentResearch` является отдельным Protocol и не наследует `EnvironmentInteraction`.
8. `EnvironmentCapabilities` не используется как field agent-visible records.
9. Environment object/capability не является допустимым `CognitiveState` payload через этот step.
10. `CommittedEnvironmentAction` содержит только ActionCommitId + semantic action и не становится substitute `ActionCommitRecord`.
11. research records могут ссылаться на world/snapshot identities, agent-visible outputs — нет.
12. никаких generic `info`/`metadata: Mapping[str, object]` escape hatches на Agent Interaction Plane.

---

# 27. Validation/error semantics

Contracts fail closed через existing обычные `TypeError`/`ValueError` style rules для malformed construction.

`IS-03` не добавляет Environment runtime exception hierarchy для transition failures, потому что concrete dynamics ещё отсутствуют.

Structural action invalidity должна быть обнаружима до normal world transition в `IS-04`.

Valid-but-no-effect/stochastic-failure остаётся normal `InteractionResult` + richer research transition record.

Не добавлять exception, который кодирует конкретные MicroWorld hidden rules.

---

# 28. Controlled construction

Dataclasses из `IS-03` могут иметь normal constructors, если `__post_init__` полностью валидирует immutable shape.

Не требуется compiler-controlled construction как у `ExecutionPlan`, потому что эти records являются typed boundary data, а не compiled authority object.

Protocols не должны предоставлять mutable attributes/stores.

---

# 29. Explicit forbidden scope

`IS-03` не реализует:

```text
MicroWorld private core
world grid/entity model
walls/floor/target dynamics
partial-observation renderer
occlusion algorithm
procedural generation
RNG instances/getstate/setstate
seed derivation
snapshot hidden payload
restore/clone/fork implementation
MW0/MW1/MW3 fixtures
solvability validator
Perception
CanonicalPercept
Goal System
Reference Policy
Action authorization
AuthorizedAction
ActionCommitRecord
Dispatcher/retry/reconciliation
Experience Journal
InteractionRuntime
v0.2 Composition Root/profile/CLI
Gymnasium adapter
NumPy/PyTorch
```

Не создавать dummy concrete Environment только для tests contracts.

---

# 30. Required tests

Минимум:

```text
tests/contract/test_environment_contracts.py
tests/contract/test_environment_capability_split.py
```

Обязательные cases:

## Data/action contracts

1. exact action vocabulary + Direction;
2. actions frozen;
3. invalid action direction/type rejected;
4. capability unknown/duplicate/non-canonical kinds rejected;
5. public field/record mutable payload rejected;
6. duplicate public field names rejected;
7. non-finite float rejected;
8. `RawObservation` frozen and carries only safe envelope fields;
9. task spec/feedback preserve ExternalTaskId relation;
10. successful `EpisodeStartResult` rejects terminated/truncated true;
11. `CommittedEnvironmentAction` joins ActionCommitId to semantic action;
12. `InteractionResult` keeps terminated/truncated separate;
13. transition receipt joins exact ActionCommitId to EnvironmentTransitionId.

## Capability split

14. `EnvironmentInteraction` has exactly interaction methods and no research operations;
15. `EnvironmentResearch` is separate and does not inherit interaction surface;
16. agent-facing dataclass field names have no forbidden research fields;
17. research records can carry world/snapshot/generation references;
18. snapshot metadata is research-only and immutable;
19. snapshot Protocol does not prescribe mutable/generic payload;
20. `EnvironmentCapabilities` bundle contains two separate capability-typed fields;
21. constructor/import tests prove contracts do not import runtime/reference/composition;
22. no Gymnasium/NumPy dependency/import introduced.

Negative field-name checks не являются единственной privacy proof: tests также должны instantiate fake interaction/research capabilities и подтвердить, что consumer typed как `EnvironmentInteraction` не получает research methods через declared Protocol surface.

---

# 31. VerificationObligations

`IS-03` продвигает:

```text
V02-003 — contract foundation
V02-010 — Environment action-interface foundation
V02-015 — termination/truncation contract foundation
V02-016 — scope/architecture regression
```

`V02-016` остаётся version-wide regression obligation; текущий step может подтвердить его layer coverage, но не объявляет final version-wide PASS.

---

# 32. Acceptance condition

`IS-03` принят только если:

- concrete Environment ещё отсутствует;
- Agent/Research capability surfaces machine-distinct;
- agent-visible records structurally не имеют privileged research fields/escape hatches;
- typed MicroWorld semantic actions зафиксированы;
- reset/interaction/termination contracts выражены;
- ActionCommitId → EnvironmentTransitionId causal seam выражен без реализации Action Boundary;
- snapshot/research contract выражен без premature serialization/engine implementation;
- contracts остаются stdlib-only;
- v0.1/v0.2 foundation regression green.

Следующий `IS-04` остаётся CLOSED до independent audit и отдельного transition.
