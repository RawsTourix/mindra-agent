# V0.2-IS-04 — MicroWorld Core Shape

## Статус

**Статус:** `accepted step-specific clarification`  
**Этап:** `V0.2-IS-04 — Deterministic MicroWorld core, MW0 & snapshot`  
**Semantic baseline:** `F31`  
**Version design:** `docs/versions/v0.2/README.md` — accepted  
**Implementation sequence:** `docs/versions/v0.2/implementation-sequence.md` — accepted  
**Environment contract shape:** `docs/versions/v0.2/is-03-environment-contract-shape.md` — accepted  
**Входной implementation baseline:** `576248fd389a3211adc1d722e1d154c9c0eaabed` — accepted `V0.2-IS-03`

Этот документ снимает implementation ambiguity `IS-04`. Он не меняет `DU-07`, `ADR-0007`, F31, version scope или порядок implementation sequence.

`IS-04` реализует первый concrete Environment engine только для `MW0_DIRECT_REACH` и generic basic primitives, необходимые этому engine. `MW1_FETCH_UNLOCK`, `MW3_HIDDEN_SWITCH`, hidden causal mappings, door/switch semantics и solvability framework остаются `IS-05`.

---

# 1. Причина clarification

Accepted sequence уже требует concrete deterministic Environment, но canonical DU-07 намеренно не фиксирует:

- exact Python package/API concrete MicroWorld;
- immutable hidden-state records;
- exact MW0 geometry;
- exact partial-observation projection;
- exact fixed/procedural fixture selection;
- exact seed derivation bytes;
- ordering sub-phases одного transition;
- MW0 success/truncation semantics;
- snapshot concrete payload;
- restore compatibility rules;
- clone/fork concrete lineage behavior;
- relationship `IdFactory` / snapshot continuation.

Без этого Codex пришлось бы принимать архитектурные решения самостоятельно.

---

# 2. Package split

Создать package минимум:

```text
src/mindra/reference/microworld/
├── __init__.py
├── model.py
├── tasks.py
└── engine.py
```

Responsibility:

```text
model.py
→ frozen reference world/config/state/snapshot records
→ grid coordinates / object kinds
→ concrete MicroWorldSnapshot

tasks.py
→ MW0 fixed/procedural definitions
→ deterministic seed-role derivation
→ manifest/content hashing

engine.py
→ private _MicroWorldCore
→ transition/reset logic
→ observation projection
→ MicroWorldInteraction wrapper
→ MicroWorldResearch wrapper
→ public build_microworld factory
```

Допустимы небольшие private helpers внутри этих файлов. Не создавать generic game-engine framework.

`mindra.reference.microworld` может экспортировать concrete reference types/factory. Top-level `mindra.reference` export допускается только если соответствует существующему package style; не требуется ради самого step.

---

# 3. Layering

Сохраняется:

```text
entrypoints
    ↓
composition
   ↙   ↘
runtime  reference
   ↘   ↙
 contracts
```

MicroWorld:

- импортирует только stdlib + `mindra.contracts`;
- не импортирует `mindra.runtime`, `composition`, `entrypoints`;
- не зависит от Perception/Goal/Policy/Action Boundary/Journal;
- не получает `KernelRuntime`;
- не пишет `CognitiveState`;
- не вызывает lifecycle coordinator.

Runtime third-party dependency target остаётся `0`.

---

# 4. Concrete construction surface

Добавить frozen config conceptually:

```text
MicroWorldConfig
├── root_seed: int
├── observation_radius: int
└── max_steps: int
```

Rules:

- exact `int`, не `bool`;
- `root_seed >= 0`;
- `observation_radius >= 0`;
- `max_steps > 0`.

Canonical defaults для reference tests/future composition:

```text
observation_radius = 2
max_steps = 64
```

Factory conceptually:

```python
build_microworld(
    *,
    id_factory: IdFactory,
    root_seed: int,
    observation_radius: int = 2,
    max_steps: int = 64,
) -> EnvironmentCapabilities
```

Exact positional/keyword style может следовать repository conventions, но dependencies и semantics выше обязательны.

Factory обязан физически создать **разные objects**:

```text
MicroWorldInteraction
MicroWorldResearch
```

которые разделяют один private core.

---

# 5. Private core ownership

`_MicroWorldCore` является private implementation detail и владеет минимум:

```text
config
current immutable WorldDefinition | None
current immutable WorldState | None
current EnvironmentDescriptor | None
current EnvironmentGenerationProvenance | None
generation_rng | None
dynamics_rng | None
task_rng | None
research transition records
snapshot lineage anchor
injected/root IdFactory
world-local Environment ID sequence state
```

Agent/research wrappers не дублируют authoritative mutable world state.

Public/research records frozen. Core может быть mutable owner указателей на immutable revisions/records и `random.Random` streams.

---

# 6. World model — IS-04 exact subset

Добавить frozen types эквивалентные:

```text
GridPosition
├── x: int
└── y: int

MicroWorldObjectKind
├── TARGET
└── PORTABLE

MicroWorldObject
├── object_id: str              # research-only local identity
├── kind: MicroWorldObjectKind
├── appearance: str
└── position: GridPosition | None

MicroWorldDefinition
├── width: int
├── height: int
├── walls: tuple[GridPosition, ...]
├── avatar_start: GridPosition
├── objects: tuple[MicroWorldObject, ...]
└── manifest_ref: str

MicroWorldState
├── episode_id: EpisodeId
├── avatar_position: GridPosition
├── objects: tuple[MicroWorldObject, ...]
├── inventory_object_id: str | None
├── step_count: int
├── full_observation: bool
├── terminated: bool
└── truncated: bool
```

Exact class names могут слегка отличаться, если semantics и tests сохраняются.

Rules:

- `width/height >= 3`;
- coordinates exact ints;
- all positions inside bounds;
- walls unique/canonical sorted;
- outside boundary не является implicit playable cell;
- boundary walls должны замыкать perimeter canonical MW0 definitions;
- avatar не стартует в wall;
- object IDs unique;
- TARGET всегда имеет position;
- PORTABLE может иметь `position=None` только когда находится в inventory;
- одновременно inventory содержит максимум один portable object;
- object tuple имеет deterministic canonical order by `object_id`;
- target и portable appearance agent-visible, `object_id` — research-only;
- hidden/world object IDs никогда не появляются в `RawObservation`.

`floor` — implicit terrain для in-bounds non-wall cells. Не создавать отдельный mutable Floor object на каждую клетку.

---

# 7. IS-04 object scope

В `IS-04` реально поддерживаются только:

```text
wall
floor
target
generic portable object
```

Не реализовывать сейчас:

```text
key
tool
door
switch
hidden causal mapping
hazard behavior
pending delayed events
resource transformations
```

Эти primitives принадлежат `IS-05`.

Если future-ready field необходим snapshot shape, допускается immutable empty placeholder только если он уже прямо принят version design; не добавлять behavior.

---

# 8. MW0 task semantics

Exact task family:

```text
MW0_DIRECT_REACH
```

Agent-visible task:

```text
task_kind = "mw0_direct_reach"
```

Task success:

```text
avatar_position == TARGET.position
```

Success является natural terminal state:

```text
terminated = True
truncated = False
ExternalTaskFeedback.status = SUCCEEDED
```

До success:

```text
ExternalTaskFeedback.status = IN_PROGRESS
```

MW0 не имеет natural failure terminal state.

Если step budget достигнут до success:

```text
terminated = False
truncated = True
feedback остаётся IN_PROGRESS
```

Если success достигнут ровно на последнем разрешённом step:

```text
terminated = True
truncated = False
```

Natural termination имеет приоритет над budget truncation одного и того же transition.

После `terminated` или `truncated` normal `apply_committed_action()` fail-closed до следующего reset и не создаёт natural transition.

---

# 9. Canonical fixed MW0 fixture

Обязательный canonical smoke fixture alias:

```text
mw0.direct_reach.fixed.v1
```

Definition:

```text
width = 7
height = 7
perimeter = walls
interior walls = none
avatar_start = (1, 1)
target = (5, 5)
target appearance = "target"
portable objects = none
```

Этот fixture намеренно простой: он должен позднее позволить stateless deterministic ReferencePolicy закрыть end-to-end smoke без превращения Policy в Planner.

Partial-observation mode с radius=2 на initial state не видит target.

Full-observation control видит target через тот же `RawObservation` type.

---

# 10. Auxiliary contract fixtures

Для tests engine допускаются дополнительные **MW0-only** fixed definitions/aliases, например:

```text
mw0.occlusion.fixed.v1
mw0.portable.fixed.v1
```

Они не являются новыми task families.

`mw0.occlusion.fixed.v1` может содержать interior wall для доказательства occlusion.

`mw0.portable.fixed.v1` может содержать один generic PORTABLE object для action semantics tests.

Не добавлять door/key/switch под видом test fixture.

---

# 11. Procedural MW0 subset

Если `EpisodeStartRequest.control.world_manifest_ref is None`, `IS-04` использует narrow procedural MW0 generator.

Generator exact profile:

```text
width = 7
height = 7
perimeter walls only
no interior walls
no portable distractors
avatar_start sampled from interior cells by generation_rng
target sampled from remaining interior cells by task_rng
```

Такой subset guaranteed-solvable конструктивно и не требует generic solver/solvability framework `IS-05`.

Generation order обязан быть deterministic поверх canonical sorted interior-cell tuple.

`dynamics_rng` в MW0 может не потребляться, потому что MW0 transitions deterministic. Stream всё равно существует и snapshot'ится.

---

# 12. Fixed fixture selection

Если `EnvironmentEpisodeControl.world_manifest_ref` задан, `IS-04` поддерживает только известные fixed aliases этого step.

Unknown manifest ref fail-closed как configuration/control error до reset publication.

Generated manifest hash не обязан становиться process-global lookup registry на `IS-04`. Reproduction procedural MW0 обеспечивается semantic/generator versions + effective seeds; exact state branching — snapshot/restore/fork.

Не создавать global mutable manifest registry.

---

# 13. Seed-role derivation

MicroWorld владеет тремя независимыми `random.Random` instances:

```text
generation_rng
dynamics_rng
task_rng
```

Process-global functions `random.seed/random.random/...` запрещены.

Если конкретный role seed не передан через `EnvironmentEpisodeControl`, он derivation из `MicroWorldConfig.root_seed`.

Exact derivation:

```python
payload = f"mindra|microworld|0.2|{root_seed}|{role}".encode("utf-8")
derived = int.from_bytes(sha256(payload).digest(), "big")
```

Exact role labels:

```text
generation
dynamics
task
```

Если `generation_seed` / `dynamics_seed` / `task_seed` явно передан control, используется exact explicit seed для соответствующего stream вместо derived value.

`EnvironmentGenerationProvenance` хранит **effective role seeds**, не root seed.

Python `hash()` запрещён для causal derivation.

---

# 14. Environment-owned IDs

Contracts сами IDs не создают. MicroWorld получает injected `IdFactory`.

На каждом successful reset Environment через injected `IdFactory` создаёт новый:

```text
WorldInstanceId
```

EpisodeId приходит от caller и не создаётся Environment.

Environment-owned episode-local identities минимум:

```text
ObservationId
ExternalTaskId
EnvironmentTransitionId
EnvironmentSnapshotId
```

должны создаваться через injected `IdFactory` или private owner-scoped `IdFactory` wrapper, rooted в injected factory.

Если используется owner-scoped wrapper, он обязан:

- сам удовлетворять `IdFactory` semantics;
- использовать stable stdlib UUID derivation, не process-global randomness;
- иметь snapshot/restorable counter/state, если его state влияет на exact same-instance snapshot continuation;
- не выдавать Agent seed/counter/namespace.

Нельзя создавать эти IDs прямыми `uuid4()/uuid7()` calls внутри semantic engine.

`ActionCommitId` приходит только в `CommittedEnvironmentAction` и не создаётся Environment.

---

# 15. Descriptor/version constants

IS-04 использует stable constants эквивалентные:

```text
environment_family = "microworld"
environment_semantic_version = "0.2"
interaction_interface_revision = 0
observation_schema_revision = 0
action_schema_revision = 0
task_schema_revision = 0
feedback_schema_revision = 0
snapshot_contract_revision = 0
engine_version = "mw_engine_v1"
generator_version = "mw0_generator_v1"
task_family = "mw0_direct_reach"
task_version = "1"
```

Exact constant variable names могут отличаться. Значения descriptor fields должны быть deterministic и consistent.

`distribution_id` различает минимум fixed/procedural source, например canonical tokens:

```text
mw0_fixed
mw0_procedural
```

`distribution_version = "1"`.

---

# 16. World manifest identity

Каждая concrete `MicroWorldDefinition` получает deterministic content-derived manifest ref.

Использовать SHA-256 над explicit canonical representation definition.

Requirements:

- representation не использует unordered set/dict iteration;
- включает dimensions, walls, avatar start, object kinds/appearances/positions;
- не включает runtime `EpisodeId`, `WorldInstanceId`, ObservationId или RNG current state;
- equivalent definition даёт одинаковый manifest ref;
- manifest ref research-only.

Canonical public form:

```text
sha256:<lowercase hex digest>
```

Fixed alias (`mw0.direct_reach.fixed.v1`) и content manifest ref — разные concepts.

---

# 17. Reset state machine — IS-04

Before first reset:

- `describe_interaction()` разрешён;
- interaction action, research snapshot/world-state inspection requiring active world fail-closed.

Successful reset:

1. validate request/control;
2. reject active unfinished Episode;
3. resolve effective role seeds;
4. create fresh local RNG streams;
5. resolve fixed fixture OR generate procedural definition;
6. create fresh `WorldInstanceId`;
7. create external task identity;
8. build initial immutable state;
9. build descriptor/provenance;
10. build initial RawObservation;
11. only after all validation/construction succeeds publish the new core state;
12. clear previous natural transition record sequence;
13. return `EpisodeStartResult` with `terminated=False`, `truncated=False`.

Repeated reset while current Episode neither terminated nor truncated:

```text
RuntimeError (or narrow equivalent reference state error)
```

и current world/RNG/records остаются unchanged.

После terminated/truncated новый reset разрешён.

`IS-04` не реализует explicit abort operation/history record. Fail-closed active reset удовлетворяет requirement «не стирать молча» в текущем scope.

---

# 18. Observation schema produced by MicroWorld

MicroWorld строит `RawObservation.records` только из `AgentVisibleRecord`.

Exact v0.2 MW0 schema:

## Self record

```text
kind = "self"
fields:
  inventory = tuple[str, ...]
```

Inventory содержит только agent-visible `appearance` переносимого объекта, не research `object_id`.

## Cell record

```text
kind = "cell"
fields:
  dx: int
  dy: int
  terrain: "floor" | "wall"
  object_kind: "target" | "portable" | None
  appearance: str | None
```

Coordinates relative к current avatar:

```text
dx = cell.x - avatar.x
dy = cell.y - avatar.y
```

Absolute world coordinates Agent не получает.

Record ordering:

```text
self first
then cell records sorted by (dy, dx)
```

Field ordering внутри records fixed implementation-wide и test-covered.

No hidden IDs, world identity, seeds, manifest, distribution, reasons или research state.

---

# 19. Partial observation

Partial mode uses configured `observation_radius`.

Candidate visible cell должен одновременно:

1. иметь Chebyshev distance от avatar `<= observation_radius`;
2. иметь line of sight согласно deterministic integer grid ray;
3. находиться внутри bounds.

Occlusion:

- wall cell itself visible, если попадает в radius/ray;
- первая wall на ray блокирует cells за ней;
- никакого orientation/FOV cone;
- no stochastic visibility.

Использовать deterministic integer Bresenham-style ray или exact equivalent с test-covered tie behavior. Один и тот же definition/state обязан давать identical visible-cell set на Ubuntu/Windows.

`observation_radius=0` показывает self + current cell.

---

# 20. Full-observation control

Если current reset control имеет:

```text
full_observation = True
```

RawObservation содержит все grid cells в bounds через **тот же `cell` record schema**.

Full-observation control:

- ignores radius/occlusion filtering;
- не возвращает `MicroWorldState`;
- не раскрывает research object IDs;
- не раскрывает seeds/manifest/distribution/reasons;
- остаётся Agent Interaction Plane datum.

---

# 21. Canonical action semantics

Все пять actions должны реально обрабатываться engine.

## Move(direction)

Destination = adjacent cardinal cell.

- wall/out-of-playable-area → valid `NO_EFFECT` transition;
- occupied by PORTABLE object → valid `NO_EFFECT` transition;
- floor/target cell → avatar moves, `EFFECT`.

TARGET не блокирует movement.

## Pickup(direction)

- adjacent PORTABLE + empty inventory → object position becomes `None`, inventory binds object ID, `EFFECT`;
- otherwise → valid `NO_EFFECT`.

## Drop(direction)

- inventory non-empty + adjacent floor + no wall/object + destination not avatar cell → portable object moved there, inventory cleared, `EFFECT`;
- otherwise → valid `NO_EFFECT`.

Не разрешать drop поверх TARGET.

## Interact(direction)

В IS-04 нет door/switch/interactable causal primitive.

Поэтому canonical IS-04 behavior:

```text
valid NO_EFFECT transition
```

для любого structurally valid direction.

## Wait()

Всегда valid `NO_EFFECT` natural transition.

Каждый structurally valid action, включая `NO_EFFECT`, увеличивает `step_count` на 1 и создаёт authoritative Environment transition.

---

# 22. Agent-visible vs research outcome

Agent result:

```text
AgentVisibleActionOutcome.status
= EFFECT | NO_EFFECT
```

На IS-04 `events=()` допустим и является canonical reference choice. Не раскрывать reason.

Research record использует:

```text
ResearchActionOutcomeStatus.EFFECT
ResearchActionOutcomeStatus.NO_EFFECT
```

`STOCHASTIC_FAILURE` на MW0 не возникает, но enum contract сохраняется.

Research `reason` использует stable non-agent tokens. Минимум различать эквиваленты:

```text
moved
blocked_wall
blocked_object
pickup_succeeded
pickup_unavailable
inventory_full
drop_succeeded
drop_unavailable
interact_no_effect
wait
```

Exact token set может быть немного шире для deterministic diagnostics, но не должен содержать future door/key/switch semantics.

---

# 23. Transition sub-phase order

Для structurally valid committed action exact conceptual order:

```text
validate active Episode + committed-action shape
→ pin pre-state + RNG states + latest snapshot lineage ref
→ compute action effect against pre-state
→ advance/copy dynamics state as required
→ increment step_count
→ evaluate MW0 success
→ if no success evaluate max_steps truncation
→ compute ExternalTaskFeedback
→ construct candidate post-state
→ construct agent RawObservation/outcome/result
→ allocate/publish EnvironmentTransitionId and research record
→ atomically replace authoritative core state/RNG/record sequence
```

MW0 не обязан consume `dynamics_rng`, если transition deterministic.

`ActionCommitId` в receipt/research record должен exact совпадать с input.

---

# 24. Transition atomicity

World transition должен быть staged.

До final publish нельзя изменять authoritative:

```text
WorldState
RNG stream states
research transition record sequence
current descriptor/provenance
```

Recommended implementation:

- immutable candidate state;
- local/copy `random.Random` instances initialized из pinned getstate();
- build all output records before assignment;
- one final core publication section.

Если validation/construction/ID allocation/output construction бросает exception до publication:

```text
current hidden state unchanged
all three authoritative RNG states unchanged
transition record sequence unchanged
```

Opaque identity allocation во внешнем injected IdFactory может быть non-rollbackable и не считается hidden world mutation; semantic engine не должен компенсировать ID failure повторным silent transition.

Tests должны включать failure injection через обычный failing `IdFactory`/contract dependency, а не production test bypass.

---

# 25. Observation/task identities per transition

Successful reset создаёт:

```text
ExternalTaskId
initial ObservationId
```

Каждый successful natural transition создаёт новый:

```text
EnvironmentTransitionId
ObservationId
```

ExternalTaskId сохраняется тем же на протяжении Episode.

Feedback ссылается на тот же ExternalTaskId.

No-effect transition всё равно получает new EnvironmentTransitionId + new ObservationId, потому что logical external transition произошёл.

---

# 26. Concrete snapshot payload

Добавить frozen `MicroWorldSnapshot`, satisfying `EnvironmentSnapshot` Protocol.

Он содержит минимум:

```text
metadata: EnvironmentSnapshotMetadata
config: MicroWorldConfig
definition: MicroWorldDefinition
state: MicroWorldState
generation: EnvironmentGenerationProvenance
generation_rng_state
dynamics_rng_state
task_rng_state
external_task_id: ExternalTaskId
world_local_id_state/counter, если используется scoped ID wrapper
```

RNG state — immutable deep tuple compatible with `random.Random.setstate()`; не pickle/bytes/JSON canonical format.

Snapshot не содержит wrapper/core objects, locks, caches или mutable `random.Random` instances.

Snapshot достаточно для exact future world/task continuation в том же semantic engine version.

---

# 27. Snapshot creation

`snapshot()`:

- требует active initialized world;
- создаёт fresh `EnvironmentSnapshotId`;
- metadata world_instance_id exact совпадает current descriptor;
- `parent_snapshot_id` = latest lineage snapshot anchor, если есть;
- captures all three RNG states;
- captures current immutable world/task/config/id-sequence state;
- не создаёт natural transition;
- не меняет Agent-visible state/observation/task;
- обновляет только research snapshot lineage anchor.

Research snapshot call не должен consume Environment RNG.

---

# 28. Restore compatibility

`MicroWorldResearch.restore(snapshot)` принимает только compatible concrete snapshot, достаточный для hidden restore.

Fail-closed минимум при:

- snapshot не concrete `MicroWorldSnapshot`;
- environment family mismatch;
- semantic version mismatch;
- engine version mismatch;
- snapshot contract revision mismatch;
- inconsistent metadata world_instance_id/descriptor;
- malformed frozen payload.

Successful restore:

- atomically restores config/definition/state/task identity;
- restores all three RNG states;
- restores world-local ID continuation state, если он causal для Environment-owned IDs;
- restores descriptor/provenance;
- sets snapshot lineage anchor to restored snapshot ID;
- clears current natural transition record sequence, чтобы не смешивать прежнюю и restored lineage;
- не создаёт `EnvironmentTransitionId`;
- не возвращает Agent-visible result автоматически.

Restore failure оставляет current instance unchanged.

---

# 29. Snapshot continuation equality

Обязательный strongest same-instance property:

```text
S = snapshot()
run action suffix A → continuation C1
restore(S)
run same action suffix A → continuation C2
C1 == C2
```

Если MicroWorld использует snapshot-restored owner-local ID sequence, equality включает Environment-owned opaque IDs.

Если конкретный implementation использует external non-snapshotable root IdFactory для some non-world-causal identity allocation, tests минимум обязаны доказать exact equality:

```text
hidden world states
RawObservation.records/schema
ExternalTaskFeedback
AgentVisibleActionOutcome
terminated/truncated
research action status/reasons
all Environment RNG states
```

и separately prove causal joins/uniqueness opaque IDs.

Предпочтителен owner-local snapshotable Environment ID sequence, потому что он даёт stronger exact continuation без изменения generic `IdFactory` contract.

---

# 30. Clone semantics

`clone()` создаёт independent Environment capabilities из **текущего exact state**.

Requirements:

- source current state snapshot-equivalent;
- new private core object;
- new `MicroWorldInteraction` wrapper;
- new `MicroWorldResearch` wrapper;
- no shared mutable WorldState container;
- no shared mutable `random.Random` objects;
- actions/restore/reset clone не мутируют original hidden state/RNG;
- semantic world/task continuation from creation point matches source under same action suffix.

Clone may receive a distinct `WorldInstanceId`/opaque branch identities if implementation uses explicit branch identity; world definition/task semantics must remain identical.

---

# 31. Fork semantics

`fork(snapshot)` создаёт independent research lineage от explicit compatible snapshot.

Requirements:

- same hidden world/task/RNG state as snapshot at fork point;
- independent core/wrappers/RNG objects;
- parent lineage represented at least через source `EnvironmentSnapshotId` in concrete snapshot lineage state;
- future branch mutations do not alter source/original;
- fork itself is not natural Environment transition.

Distinct branch/world opaque identities are permitted and preferred to avoid cross-branch identity collisions, provided parent snapshot relation remains explicit.

Не добавлять Agent snapshot/coordinated Kernel restore.

---

# 32. Research inspection

Generic `EnvironmentResearch.inspect()` возвращает accepted `EnvironmentResearchView`.

Concrete `MicroWorldResearch` дополнительно может/должен предоставить narrow research-only getters эквивалентные:

```text
world_definition() -> MicroWorldDefinition
world_state() -> MicroWorldState
```

чтобы Research Plane реально мог inspect authoritative frozen ground truth без generic `object/dict` escape hatch.

Эти methods:

- отсутствуют на `EnvironmentInteraction` Protocol/wrapper;
- возвращают frozen records;
- не возвращают private core;
- не являются Agent input.

`hidden_state_ref` в generic research view должен быть deterministic opaque reference/hash текущего hidden state, а не raw object handle.

Renderer/debug output на `IS-04` optional и не входит general Protocol.

---

# 33. Research transition records

`transition_records()` возвращает immutable tuple natural transitions **текущей reset/restore lineage**.

Каждый record:

- exact EnvironmentTransitionId текущего transition;
- current EpisodeId;
- current WorldInstanceId;
- exact ActionCommitId;
- exact semantic EnvironmentAction;
- latest explicit pre-state snapshot ref, если он существует;
- post snapshot ref может быть `None`, если explicit snapshot не materialized;
- research action status/reason;
- ExternalTaskFeedback;
- terminated/truncated;
- research termination reason.

MW0 termination reason stable equivalent:

```text
mw0_target_reached
```

MW0 truncation reason stable equivalent:

```text
step_budget_exhausted
```

Agent-visible `InteractionResult` не содержит эти reasons.

---

# 34. Snapshot lineage anchor

Core может хранить latest explicit snapshot ID как research-only lineage anchor.

Rules:

- initial/reset anchor = `None`;
- `snapshot()` creates new ID whose parent is previous anchor, затем anchor = new ID;
- natural transition may use current anchor as `pre_snapshot_id`, затем state changes but parent lineage knowledge сохраняется;
- `restore(snapshot)` sets anchor = snapshot ID;
- clone/fork establishes source snapshot relation without exposing it Agent.

Не создавать fake post-snapshot ref, если соответствующий immutable snapshot artifact не был materialized.

---

# 35. Research/Agent isolation in concrete engine

Обязательный concrete enforcement:

```text
MicroWorldInteraction is not MicroWorldResearch
MicroWorldResearch is not MicroWorldInteraction
```

`MicroWorldInteraction` public method surface — только accepted interaction capability:

```text
describe_interaction
reset
apply_committed_action
```

Он не предоставляет public:

```text
inspect
world_state
world_definition
snapshot
restore
clone
fork
transition_records
seed/config/manifest getter
private core getter
```

`MicroWorldResearch` не передаётся через Agent result.

Python private implementation attributes не рассматриваются как security sandbox; enforceable architectural boundary строится на separate wrappers, Protocol surfaces и separate frozen data types, а не на одном object с public privileged methods.

---

# 36. No research leakage in observations

Tests обязаны доказать для partial и full modes:

- no `WorldInstanceId`;
- no object_id;
- no manifest ref;
- no seed/RNG state;
- no distribution label;
- no hidden_state_ref;
- no research reason;
- no absolute hidden map object;
- no `EnvironmentResearchTransitionRecord`.

Full observation увеличивает множество visible `cell` records, но не изменяет privacy class datum.

---

# 37. Determinism definition IS-04

Для двух fresh MicroWorld instances с:

- одинаковым config;
- одинаковым EpisodeStartRequest/control;
- эквивалентно seeded deterministic IdFactory sequence;
- одинаковой action sequence;
- без различающихся research-side calls;

должны совпадать:

```text
resolved WorldDefinition
manifest_ref
agent-visible observations
external task/feedback semantics
action outcomes
terminated/truncated
research transition semantic records
RNG states after each corresponding point
```

При deterministic IdFactory также должны совпадать Environment-owned opaque IDs.

Wall-clock, process hash randomization и physical test order не влияют на result.

---

# 38. Structural invalidity

`apply_committed_action()` обязан fail-closed до natural transition, если:

- input не exact `CommittedEnvironmentAction`;
- semantic action не exact canonical action type;
- Environment not reset;
- Episode already ended.

Failure:

```text
no state change
no RNG change
no transition record
no step_count increment
```

Не преобразовывать malformed action в `NO_EFFECT`.

---

# 39. Forbidden scope

`IS-04` не реализует:

```text
MW1_FETCH_UNLOCK
MW3_HIDDEN_SWITCH
key/tool semantics
door
switch
hidden causal mapping
hazard behavior
pending delayed-effect behavior
generic solvability framework
large benchmark distribution
train/validation/test split framework
Environment interventions
Gymnasium adapter
renderer/UI dependency

Perception
CanonicalPercept
Goal System
Reference Policy
Planner
Action Boundary
Dispatcher/retry/reconciliation
Experience Journal
InteractionRuntime
v0.2 Composition Root/profile/CLI
package version 0.2.0
v0.2 artifact verifier
```

Do not create future subsystem stubs.

---

# 40. Required tests

Минимум создать:

```text
tests/unit/test_microworld_actions.py
tests/property/test_microworld_determinism.py
tests/property/test_environment_snapshot.py
tests/contract/test_microworld_capability_isolation.py
```

## Action/reset tests

Проверить минимум:

1. describe works before reset;
2. action/snapshot requiring active world fail before reset;
3. canonical fixed reset exact MW0 geometry;
4. active unfinished reset rejected atomically;
5. reset after terminal/truncated allowed;
6. Move success;
7. blocked Move = natural NO_EFFECT transition;
8. no-effect increments step_count and creates new transition/observation IDs;
9. Pickup success/no-effect;
10. Drop success/no-effect;
11. Interact = NO_EFFECT in IS-04;
12. Wait = NO_EFFECT;
13. target entry => terminated + SUCCEEDED;
14. max_steps => truncated, not failed task feedback;
15. success on final budget step => terminated not truncated;
16. action after end rejected without transition;
17. malformed/subclass action rejected before mutation;
18. action receipt preserves exact ActionCommitId;
19. ExternalTaskId stable across Episode transitions;
20. research reason absent Agent outcome.

## Determinism/observation property tests

1. same config/control/seed/actions => same world/trajectory;
2. role seed derivation exact and platform-independent;
3. generation/task streams independent;
4. process-global random state not used/changed;
5. procedural MW0 always avatar != target and structurally reachable;
6. partial initial canonical fixture hides target at radius 2;
7. full observation same fixture exposes target;
8. wall occludes cells behind it in partial fixture;
9. observation cell ordering deterministic;
10. no absolute coordinates/research IDs in RawObservation;
11. fixed/procedural manifest refs deterministic.

## Snapshot tests

1. snapshot captures all three RNG states;
2. snapshot frozen/no mutable random objects;
3. restore same snapshot + same suffix gives same continuation;
4. restore failure atomic;
5. restore does not append natural transition;
6. snapshot does not consume RNG;
7. clone has no mutable world/RNG alias;
8. fork has no mutable world/RNG alias;
9. source mutation does not mutate clone/fork and vice versa;
10. snapshot parent lineage deterministic;
11. transition record pre_snapshot ref only references materialized snapshot;
12. restore clears unrelated current transition history;
13. terminated/truncated state restored exactly.

## Capability isolation tests

1. wrappers are distinct objects;
2. MicroWorldInteraction satisfies EnvironmentInteraction;
3. MicroWorldResearch satisfies EnvironmentResearch;
4. interaction wrapper has no research public methods;
5. research can retrieve frozen world state/definition;
6. full-observation interaction result still lacks research-only fields;
7. seed/manifest/world ID not present in RawObservation;
8. clone/fork return bundles with separate interaction/research wrappers;
9. reference package does not import runtime/composition/entrypoints;
10. no third-party runtime dependency/import.

## Atomicity failure test

Добавить failing injected `IdFactory` или equivalent normal dependency failure так, чтобы exception произошёл после candidate computation, но до final publication.

Доказать:

```text
hidden state unchanged
RNG states unchanged
step_count unchanged
transition_records unchanged
```

Не добавлять production test hook.

---

# 41. VerificationObligations

`IS-04` продвигает:

```text
V02-001 — Environment-layer deterministic trajectory coverage
V02-002 — closed at Environment layer
V02-003 — substantial concrete capability isolation
V02-015 — Environment reset/termination/truncation layer coverage
V02-016 — architecture/scope regression layer coverage
```

`V02-002 closed at Environment layer` не означает final version-wide acceptance всего v0.2.

`V02-001` final end-to-end closure требует later full interaction vertical.

---

# 42. Targeted verification

Минимум:

```text
uv run --locked pytest \
  tests/unit/test_microworld_actions.py \
  tests/property/test_microworld_determinism.py \
  tests/property/test_environment_snapshot.py \
  tests/contract/test_microworld_capability_isolation.py

uv run --locked mypy src tests
uv run --locked lint-imports
```

Также запустить affected regression минимум:

```text
IS-03 Environment contracts/capability split
identity contracts
reference layer architecture tests
state snapshot immutability/value tests where relevant
v0.1 reference determinism
```

---

# 43. Full regression

После targeted обязательно:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked lint-imports
uv run --locked pytest
uv build
uv run --locked mindra validate-profile --profile configs/v0.1/reference.toml
uv run --locked mindra kernel-smoke --profile configs/v0.1/reference.toml
```

Historical smoke остаётся:

```text
modules=4
waves=3
revision=3
join=10
```

До scheduled появления v0.2 profile/CLI/artifact verifier они `NOT APPLICABLE`.

---

# 44. Acceptance condition

`IS-04` принят только если:

- concrete stdlib-only MicroWorld engine существует;
- только MW0 + basic wall/floor/target/portable semantics реализованы;
- agent/research wrappers физически separate;
- fixed + narrow procedural MW0 reproducible;
- partial/full observation работают через один safe RawObservation contract;
- all five action types handled;
- blocked movement является natural no-effect transition;
- reset/state transition publication atomic;
- three RNG streams independent and snapshot-restorable;
- snapshot/restore continuation доказана;
- clone/fork не имеют mutable world/RNG alias;
- research transition records deterministic;
- no hidden/research leakage Agent;
- no IS-05+ behavior;
- full existing regression green.

Следующий `IS-05` остаётся CLOSED до independent audit и отдельного transition.
