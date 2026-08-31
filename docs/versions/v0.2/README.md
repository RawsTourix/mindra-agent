# MINDRA v0.2 — MicroWorld Interaction

## Статус

**Software milestone:** `v0.2 — MicroWorld Interaction`  
**Статус design:** `accepted`  
**Semantic baseline:** `F31`  
**Входной baseline:** `v0.1 Core Kernel` — `implemented / independently audited / accepted`  
**Roadmap owner:** `docs/design/version-roadmap.md`  
**Implementation sequence:** [`implementation-sequence.md`](implementation-sequence.md) — принимается вместе с этим design  
**Implementation:** открывается только через `docs/design/current.md`

Этот документ задаёт exact software profile первой полноценной вертикали:

```text
Agent
↕
Environment
```

Он конкретизирует подмножества `DU-07`, `DU-08`, `DU-09`, `DU-23`, `DU-24`, `DU-25` поверх foundation `DU-01 … DU-06` и Engineering Verification `DU-29`.

`v0.2` **не меняет F31**. Если implementation требует изменить frozen semantic responsibility, owner, source-of-truth или commit boundary, работа останавливается:

```text
STOP
→ semantic blocker
→ design review
→ ADR
→ freeze impact analysis
```

---

# 1. Цель версии

Главный результат `v0.2`:

```text
MicroWorld reset / previous outcome
        ↓
Raw Observation + External Task Specification
        ↓
Observation / task ingress
        ↓
Canonical Percept
        ↓
Committed Goal state
        ↓
deterministic Reference Policy
        ↓
SelectedActionIntent
        ↓
Action authorization
        ↓
AuthorizedAction
        ↓
Action Commit
        ↓
Dispatch
        ↓
Environment Transition
        ↓
Outcome Commit
        ↓
Experience Journal
        ↓
next Decision Window / Episode end
```

Версия доказывает архитектурную способность MINDRA выполнять причинно строгий end-to-end interaction loop. Она не доказывает интеллектуальность, general intelligence, качество learned policy или необходимость будущих cognitive mechanisms.

---

# 2. Историческая граница v0.1

`v0.2` строится поверх уже принятого Core Kernel и сохраняет его regression contract:

```text
CognitiveState
StateProjection
ModuleDescriptor / CognitiveModule
ExecutionPlan / CognitiveScheduler
WaveExecutor
StateUpdateProposal / PrivateStateProposal
CommitCoordinator
EvidenceRecorder
InterventionGateway
CompositionRoot
KernelRuntime
```

`v0.2` не заменяет kernel другим runtime framework и не превращает `CognitiveState` в mutable global store.

Git tag `v0.1.0` должен указывать на final post-v0.1 documentation-cleanup commit, существовавший **до** добавления `docs/versions/v0.2/`.

---

# 3. Scope F31

## 3.1. Substantial scope

```text
DU-03 — temporal interaction lifecycle refinement
DU-04 — runtime-owned ingress fields в CognitiveState
DU-05 — standardized lifecycle phases вне COGNITIVE_CYCLE
DU-06 — interaction-safe intervention boundaries
DU-07 — Environment / MicroWorld subset
DU-08 — structured deterministic Perception subset
DU-09 — external-task Goal subset
DU-23 — deterministic reference Policy subset, без Planner
DU-24 — Action Boundary + dispatch/reconciliation subset
DU-25 — append-only Experience Journal source layer
DU-29 — v0.2 engineering verification
```

## 3.2. Явный forbidden scope

`v0.2` не реализует:

```text
real Cortex
persistent Agent Memory
World Model
Self Model
Intrinsic Signals
Drives
Appraisal
Affect
full Valuation
full Salience
Memory Regulation
Workspace
Executive Control
Planner
learned Policy
RL / optimizer / training lifecycle
neural training
PyTorch / NumPy requirement
persistent Agent Snapshot / Checkpoint
full MINDRA-Eval
benchmark suite уровня v1.0
research-grade cognitive claims
remote Environment transport
ROS / gRPC / HTTP action transport
async/distributed execution
```

Наличие semantic type/seam для future compatibility не является разрешением реализовать соответствующую responsibility заранее.

---

# 4. Research/tool pass — 2026-08-31

Перед принятием exact profile проверен актуальный software landscape.

## 4.1. Gymnasium

Официальный `Env` сохраняет полезную внешнюю форму:

```text
reset()
step(action)
terminated
truncated
```

Источник:

- https://gymnasium.farama.org/api/env/

Вывод: Gymnasium полезен как будущий interoperability adapter, но не как source of truth MINDRA. Его обычный `info`/space contract не покрывает обязательные MINDRA semantics: строгие Agent/Research capability surfaces, exact Environment snapshot/restore/fork, separate causal identities, multiple RNG streams и privileged-data isolation.

**Решение:** Gymnasium не является runtime dependency `v0.2`.

## 4.2. dm_env

`dm_env` подтверждает ценность маленького typed interaction surface и явных `FIRST/MID/LAST`, termination/truncation helpers.

Источник:

- https://github.com/google-deepmind/dm_env

Вывод: abstraction компактна, но не решает MINDRA-specific two-plane, provenance и snapshot requirements.

**Решение:** не вводить dependency/adaptation внутрь core.

## 4.3. MiniGrid

MiniGrid демонстрирует, что маленький symbolic grid с partial observation, object interaction, keys/doors и unlock/fetch dependency уже достаточно выразителен для полезных controlled tasks.

Источники:

- https://minigrid.farama.org/environments/minigrid/
- https://minigrid.farama.org/environments/minigrid/UnlockPickupEnv/

MiniGrid построен поверх Gymnasium/NumPy и его текущий project profile не делает Windows основной officially supported platform.

**Решение:** использовать его как design evidence, но не как implementation dependency. MINDRA MicroWorld остаётся собственным stdlib-only environment.

## 4.4. RNG snapshot

Python 3.14 `random.Random` предоставляет `getstate()` / `setstate()` для сохранения и восстановления внутреннего PRNG state.

Источник:

- https://docs.python.org/3/library/random.html

**Решение:** `v0.2` использует независимые instance-local `random.Random` streams и включает их state в `EnvironmentSnapshot`.

## 4.5. Experience storage

SQLite предоставляет transactional durable storage; Apache Arrow/Parquet предоставляет versioned/schema-rich columnar representation и metadata, полезные для будущих projections/datasets.

Источники:

- https://www.sqlite.org/transactional.html
- https://arrow.apache.org/docs/python/data.html
- https://arrow.apache.org/docs/python/parquet.html

**Решение:** source semantics `ExperienceJournal` не привязываются к storage backend. Reference `v0.2` — in-memory append-only journal. SQLite/Arrow/Parquet остаются совместимыми будущими backends/projections без изменения meaning source events.

---

# 5. Technology profile

Сохраняется foundation `v0.1`:

```text
CPython >=3.14,<3.15
uv
uv_build
src/ layout
stdlib-only runtime
Ruff
mypy --strict
pytest
Hypothesis
Import Linter
GitHub Actions
```

Runtime third-party dependencies после `v0.2`:

```text
0
```

CPU-only reference path обязателен. GPU, network и provider credentials не требуются.

Target package version после завершения version migration:

```text
0.2.0
```

Metadata bump выполняется только в dependency-ordered step, который одновременно вводит v0.2 artifact verification. До этого partial implementation сохраняет текущую package metadata, чтобы не ломать historical v0.1 clean-wheel checks посередине version work.

---

# 6. Package/repository profile

После реализации ожидаются additive areas:

```text
src/mindra/contracts/
├── environment.py
├── interaction.py
├── perception.py
├── goals.py
├── policy.py
├── action.py
└── experience.py

src/mindra/runtime/
├── boundary_commit.py
├── lifecycle.py
├── interaction.py
├── action.py
└── experience.py

src/mindra/reference/
├── microworld/
│   ├── model.py
│   ├── engine.py
│   └── tasks.py
├── perception.py
├── goals.py
└── policy.py

configs/v0.2/reference.toml
tools/verify_v0_2_artifact.py
```

Exact file split может быть слегка уточнён implementation sequence без semantic change. Top-level layer model остаётся:

```text
entrypoints
    ↓
composition
   ↙   ↘
runtime  reference
   ↘   ↙
 contracts
```

Обязательные ограничения сохраняются:

- `contracts` — только stdlib;
- `runtime` не импортирует `reference`/`composition`/`entrypoints`;
- `reference` не импортирует `runtime`;
- `composition` — единственное место wiring concrete runtime/reference objects;
- cognitive modules не получают Composition Root/registry/Environment Research Plane;
- Service Locator/global mutable registry запрещены.

---

# 7. Interaction orchestration owner

## 7.1. Новая boundary

`v0.2` вводит **`InteractionRuntime`** как explicit owner внешнего interaction lifecycle.

Conceptually:

```text
InteractionRuntime
├── narrow KernelRuntime capability
├── EnvironmentInteraction capability
├── ActionBoundary
├── Dispatcher
├── ExperienceJournal
├── IdFactory
└── interaction lifecycle state
```

`InteractionRuntime`:

- не является cognitive module;
- не является Environment;
- не является Policy;
- не выбирает action;
- не исполняет cognitive DAG самостоятельно;
- не получает Environment Research capability;
- не превращается в Service Locator.

Его responsibility — причинно упорядочить уже принятые boundaries.

## 7.2. Что остаётся у KernelRuntime

`KernelRuntime` продолжает владеть внутренним Agent execution:

- committed `CognitiveState`;
- module-private state;
- cognitive cycles;
- kernel lifecycle phase execution;
- kernel Evidence Plane;
- intervention gateway.

`KernelRuntime` **не вызывает `Environment.step()`**.

## 7.3. CognitiveScheduler

`CognitiveScheduler` остаётся owner только `COGNITIVE_CYCLE` DAG semantics.

Environment orchestration, dispatch и episode state machine не добавляются в него.

Для `EPISODE_START` / `POST_OUTCOME` вводится отдельный `LifecycleCoordinator`, переиспользующий contracts, projections, `WaveExecutor` и atomic module commit machinery, но не выполняющий Environment transition.

---

# 8. Temporal identities и ownership

Exact ownership `v0.2`:

```text
RunId
→ создаётся composition/run boundary

AgentSessionId
→ создаётся при создании Agent runtime
→ сохраняется между Environment episodes

EpisodeId
→ создаётся InteractionRuntime непосредственно перед reset нового Episode

DecisionWindowId
→ создаётся InteractionRuntime после получения очередного agent-visible observation

CognitiveCycleId
→ создаётся KernelRuntime для каждого внутреннего cycle

ActionIntentId
→ создаётся Policy

ActionCommitId / DispatchId / DispatchAttemptId
→ создаются Action/Execution runtime boundaries

EnvironmentTransitionId
→ создаётся Environment для опубликованного authoritative transition

OutcomeId
→ создаётся InteractionRuntime при Outcome Commit

ExperienceEventId
→ создаётся Experience Recorder при append
```

Все identities создаются через injected `IdFactory` или owner-scoped wrapper над ним. Wall-clock не определяет causal identity/order.

---

# 9. Kernel temporal compatibility

`v0.1` facade `KernelRuntime.run_cycle()` сохраняется для historical reference profile.

`v0.2` добавляет context-aware путь, conceptually:

```text
KernelRuntime.run_cycle_in(decision_context)
```

где caller задаёт уже существующие:

```text
RunId
AgentSessionId
EpisodeId
DecisionWindowId
```

а KernelRuntime создаёт новый `CognitiveCycleId`.

Это additive extension. `InteractionRuntime` не имеет права передавать произвольный `CognitiveCycleId` и тем самым подменять kernel ownership.

---

# 10. Runtime-owned CognitiveState ingress

Canonical `DU-04` требует, чтобы Environment не писала Agent state напрямую.

`v0.2` использует explicit runtime boundary owner:

```text
Environment
→ typed agent-visible result
→ InteractionRuntime ingress
→ validated BoundaryStateUpdate
→ BoundaryCommitCoordinator
→ committed CognitiveState
```

Existing `RuntimeBoundaryId` становится допустимым semantic owner `StateFieldSpec` наряду с `ModuleId`.

Module `CommitCoordinator` не получает право принимать arbitrary runtime writes. Для runtime-owned paths существует отдельный `BoundaryCommitCoordinator` с:

- schema ownership validation;
- exact base revision validation;
- temporal validation;
- `ValueContract` validation;
- atomic publication;
- explicit boundary provenance.

Никакого direct mutable state access не добавляется.

---

# 11. Canonical state surface v0.2

Минимальные canonical paths:

```text
observation.current
perception.current
task.external
goal.graph
policy.selected_intent
action.capability
interaction.outcome
```

Owners:

```text
observation.current      → runtime.interaction_ingress
task.external            → runtime.interaction_ingress
action.capability        → runtime.action_boundary
interaction.outcome      → runtime.interaction_ingress
perception.current       → perception.reference
goal.graph               → goal.system
policy.selected_intent   → policy.reference
```

Concrete owner IDs могут иметь эквивалентные canonical dotted names, но ownership relation является exact design.

`CognitiveState` не содержит:

- Environment hidden state;
- full World Manifest;
- research annotations;
- journal store;
- Environment object;
- policy/action dispatcher object.

---

# 12. Freshness v0.2

К existing:

```text
ANY_COMMITTED
CURRENT_CYCLE
```

добавляются минимум:

```text
CURRENT_DECISION_WINDOW
CURRENT_EPISODE
```

Semantics:

- `observation.current` должен соответствовать current `DecisionWindowId`;
- `task.external` и episode Goal state могут быть valid в пределах current `EpisodeId`;
- `perception.current` для reference Policy требуется из текущего Cognitive Cycle;
- stale temporal input не rebased silently.

Freshness проверяется через logical identities/provenance, не через wall-clock.

---

# 13. Standardized lifecycle phases v0.2

`ModuleDescriptor` additive поддерживает:

```text
COGNITIVE_CYCLE
EPISODE_START
POST_OUTCOME
```

Не вводится giant universal hook interface.

Reference participation:

```text
EPISODE_START
→ Goal System grounding/adoption

COGNITIVE_CYCLE
→ Perception
→ Reference Policy

POST_OUTCOME
→ Goal lifecycle/progress transition
```

Environment reset/step не является scheduler phase и не исполняется `LifecycleCoordinator`.

---

# 14. Episode start lifecycle

Canonical order:

```text
Agent Session exists
→ InteractionRuntime allocates EpisodeId
→ Environment.reset(EpisodeStartRequest)
→ Environment returns agent-visible EpisodeStartResult
→ InteractionRuntime allocates DecisionWindowId
→ observation/task ingress commit
→ EPISODE_START module phase
→ Decision Window OPEN
```

`Environment.reset()`:

```text
≠ AgentSession reset
≠ clear all CognitiveState
≠ clear all module-private state
```

Only scope-defined state transitions are permitted.

---

# 15. Decision Window lifecycle

Reference flow:

```text
OPEN
→ Cognitive Cycle 1
→ [Cognitive Cycle 2..N]
→ SelectedActionIntent
→ authorization
→ Action Commit
→ dispatch
→ transition / post-commit failure / execution_unknown
→ Outcome Commit or explicit failure/reconciliation state
→ CLOSED
```

Reference profile default:

```text
cognitive_cycles_per_decision = 1
```

Contract/tests обязательно поддерживают `N > 1` и доказывают:

```text
N Cognitive Cycle
≠ N Environment Transition
```

Один Decision Window допускает не более одного normal `ActionCommitRecord`.

---

# 16. Intervention timing

Agent-state intervention через `InterventionGateway` разрешена только на declared safe boundary:

- между cognitive cycles до Action Commit;
- до начала следующего cycle;
- с explicit base revision/lineage.

Запрещено применять normal state intervention:

- внутри module wave;
- между Action Commit и resolution/outcome;
- задним числом к уже committed action/outcome.

Environment intervention существует только через Research Plane и не становится Agent action.

---

# 17. Environment capability split

Reference MicroWorld физически использует private core, но наружу выдаёт **разные capability objects**:

```text
MicroWorldInteraction
MicroWorldResearch
```

`MicroWorldInteraction` содержит только agent/execution-facing contract:

```text
describe_interaction()
reset(request)
apply_committed_action(action)
```

`MicroWorldResearch` содержит privileged operations:

```text
inspect descriptor / ground truth
snapshot
restore
clone/fork
research transition records
render/debug representation
```

`InteractionRuntime`, Perception, Goal System и Policy не получают `MicroWorldResearch`.

Enforcement не строится на соглашении «не читать `_hidden`»: agent-visible и research-only records — разные frozen types, а interaction capability не предоставляет research methods.

---

# 18. Environment exact implementation

`v0.2` выбирает собственный lightweight **discrete 2D symbolic MicroWorld**.

Reference engine:

- stdlib-only;
- synchronous;
- in-process;
- step-locked;
- immutable/frozen public records;
- mutable engine state скрыт за capability boundaries либо заменяется immutable world-state revisions;
- без GPU/network;
- deterministic при фиксированном complete state/RNG;
- достаточно мал для exhaustive/debug reasoning.

World primitives минимум:

```text
floor
wall
target
key
door
switch
portable object
hazard marker
```

Hidden causal properties отделены от observable appearance.

---

# 19. Agent action schema

Typed action semantic surface:

```text
Move(direction)
Interact(direction)
Pickup(direction)
Drop(direction)
Wait
```

`direction`:

```text
NORTH
EAST
SOUTH
WEST
```

Reference v0.2 не вводит orientation/turn actions. Это уменьшает unrelated control complexity.

Environment distinction:

```text
schema-invalid command
≠ valid attempt with no effect
≠ successful world effect
```

Например попытка пройти в стену — valid Environment Transition с `no_effect`, а malformed payload — contract error до normal world transition.

---

# 20. Raw Observation

`RawObservation` — frozen agent-visible record отдельного schema revision.

Минимально содержит:

```text
observation_id
observation_schema_revision
local visible cells/entities
observed self position/relative frame data по profile
agent-visible inventory
agent-visible local events?
source Environment interface revision
logical source refs
```

Не содержит:

```text
world_instance_id как shortcut feature
generation seed
split/distribution label
hidden rule mapping
hidden entity identity
oracle solution
shortest path
objective research metric
research transition record
full hidden state
```

World/seed identities остаются research provenance.

---

# 21. Partial observability

Reference profile поддерживает configurable observation radius и occlusion.

Обязательные modes:

```text
partial observation
full-observation research/control mode
```

Full-observation mode всё равно возвращает **agent-visible observation type**, а не ResearchGroundTruth type.

Нельзя реализовать full-observation control через передачу private WorldState object Policy.

---

# 22. RNG streams

Environment владеет минимум тремя независимыми instance-local streams:

```text
generation_rng
dynamics_rng
task_rng
```

Root seed разделяется deterministic role derivation, например через SHA-256 над:

```text
environment semantic revision
root seed
a role label
```

Запрещено использовать process-global `random` или Python `hash()` как causal seed derivation.

Snapshot содержит state каждого stream через `getstate()`.

Seed используется для reproduction request, но:

```text
seed ≠ EnvironmentSnapshot
seed ≠ World identity
```

---

# 23. Environment identity / generation

Research descriptor минимум:

```text
environment_family
semantic_version
engine_revision
generator_revision
task_family
task_revision
factor_configuration
world_instance_id
world_manifest_identity/content hash
```

Procedural generation factorized. `v0.2` не обещает большой benchmark distribution; достаточно reproducible parameterized generators + fixed fixtures.

Generation failure/unsolvable world — research/config error, не Agent task failure.

---

# 24. EnvironmentSnapshot

`EnvironmentSnapshot` — frozen in-memory research artifact, не Agent Checkpoint.

Содержит или однозначно фиксирует:

```text
snapshot_id
parent lineage
Environment/world/task revisions
complete hidden WorldState
task state
embodiment/inventory state
transition counters
pending events
all causally relevant RNG states
terminated/truncated state
intervention provenance
compatibility metadata
```

Operations:

```text
snapshot
restore
clone
fork
```

Requirements:

- restore fail-closed проверяет compatibility;
- clone/fork не разделяют mutable state;
- restore не публикуется как natural Environment Transition;
- fork создаёт explicit research lineage;
- snapshot/restore continuation с тем же action suffix даёт ту же canonical continuation.

Это **не** full Agent Snapshot: coordinated Agent+Environment restore остаётся будущим milestone (`v0.4+`).

---

# 25. Reference task families

`v0.2` реализует ограниченный архитектурно полезный subset canonical MicroWorld families.

## `MW0_DIRECT_REACH`

Наблюдаемая цель + navigation.

Используется для canonical end-to-end smoke и deterministic reference Policy acceptance.

## `MW1_FETCH_UNLOCK`

Dependency:

```text
найти/подобрать key/tool
→ открыть door
→ достичь/взаимодействовать с target
```

Проверяет typed object interaction и delayed task dependency без Planner requirement.

## `MW3_HIDDEN_SWITCH`

Observable switches имеют скрытое causal mapping к door/target effect.

Используется для:

- two-plane isolation;
- hidden rule provenance;
- snapshot/restore;
- future World Model readiness.

Reference Policy **не обязана** решать эту family лучше простого deterministic control.

## Future-ready primitives

Engine может иметь `pending_events`/delayed-effect primitive и hazard/resource entities, чтобы snapshot semantics не пришлось ломать позже, но отдельные `MW2/MW4/MW5+` benchmark families в `v0.2` не принимаются.

---

# 26. Perception exact profile

Reference Perception — deterministic structured normalization без learned encoder.

```text
RawObservation
→ ReferencePerception
→ CanonicalPercept
```

`CanonicalPercept`:

```text
CanonicalPercept
├── envelope
├── semantic_core
│   ├── observed_self
│   ├── observed_entities[]
│   ├── observed_relations[]
│   └── observed_events[]
├── modality_status
└── feature_views[]
```

Envelope минимум:

```text
percept_id
source_observation_id
percept_schema_revision
perception implementation/revision
logical scope
source refs/provenance
```

Reference `feature_views`:

```text
()
```

Seam существует как typed optional tuple, но NumPy/PyTorch tensor view не добавляется.

---

# 27. Perception invariants

```text
current percept
≠ belief about hidden world
≠ memory
≠ future prediction
```

Reference semantic core содержит только:

- directly observed facts;
- deterministic normalization текущего observation.

`percept_local_entity_id` не является persistent hidden world ID.

Canonical collection ordering выбирается deterministic для equality/serialization/debugging, но order не получает semantic meaning.

Perception constructor/API не получает Environment Research capability.

---

# 28. Goal ingress

Сохраняется distinction:

```text
ExternalTaskSpecification
≠ GoalProposal
≠ CommittedGoal
```

Ownership:

```text
Environment task contract
→ ExternalTaskSpecification

StructuredExternalTaskGrounder
→ GoalProposal authority

Goal System
→ validation + adoption/rejection + Goal commit authority
```

Grounder не может мутировать GoalGraph напрямую.

---

# 29. Goal exact profile

`v0.2` реализует episode-scoped external goals only.

`GoalProposal` минимум:

```text
proposal_id
external_task_ref
objective_specification
source kind/provenance
EpisodeId
base state revision
```

`CommittedGoal` минимум:

```text
goal_id
objective_specification
scope = EPISODE
lifecycle_status
structured progress
source proposal/task refs
created logical scope
last transition logical scope
```

`GoalGraph` поддерживает typed collections/relations, но reference profile принимает один root external goal и не выполняет autonomous decomposition.

Lifecycle subset реально используемый `v0.2`:

```text
active
achieved
failed
expired
```

Contract types не должны переопределять frozen future statuses как boolean `done`.

---

# 30. Goal lifecycle routing

## Episode start

`GoalSystem` участвует в `EPISODE_START`:

```text
committed task.external
→ StructuredExternalTaskGrounder proposal
→ GoalSystem validation
→ committed goal.graph
```

Required external task, который нельзя ground/validate, блокирует normal episode execution с typed failure.

## Post outcome

`GoalSystem` участвует в `POST_OUTCOME` и читает только agent-visible outcome/task feedback.

Reference Environment может явно давать:

```text
in_progress
succeeded
failed
```

как External Task Feedback по task contract.

Objective research metric/oracle truth не используется normal Goal progress path.

On episode:

```text
success termination → achieved
failure termination → failed
truncation → expired
```

если task contract не предоставляет более специфичную agent-visible semantics.

---

# 31. Policy exact profile

`v0.2` содержит только deterministic stateless `ReferencePolicy`.

Declared reads:

```text
perception.current  CURRENT_CYCLE
goal.graph          CURRENT_EPISODE
action.capability   ANY_COMMITTED
```

Output:

```text
policy.selected_intent
```

Reference Policy:

- не получает Environment object;
- не получает ResearchGroundTruth;
- не получает seed/split/oracle metadata;
- не получает Planner;
- не получает Value/World/Self/Memory/Cortex substitutes;
- использует deterministic tie-break rules.

Acceptance behavioral responsibility — устойчиво закрыть `MW0_DIRECT_REACH` reference smoke, а не решать все task families.

---

# 32. SelectedActionIntent

Минимальный record:

```text
intent_id
intent_revision
decision_window_id
base_state_revision
agent_revision_id
policy implementation/revision
semantic action
Goal refs
source percept/state refs
status/provenance
```

Для `v0.2` candidate-set machinery может быть минимальной deterministic reference form. Не допускается alias:

```text
SelectedActionIntent == ActionCommitRecord
```

Policy не имеет dispatch capability.

---

# 33. Action Boundary

Canonical chain:

```text
SelectedActionIntent
→ ActionAuthorizationRequest
→ SchemaOnlyActionGate
→ ActionAuthorizationResult
→ AuthorizedAction
→ ActionCommitRecord
→ DispatchAttempt
→ Environment interaction
→ EnvironmentTransition / failure / unknown
→ Outcome Commit / reconciliation
```

Reference gate проверяет:

- payload/schema;
- action interface revision;
- current EpisodeId/DecisionWindowId;
- base/current StateRevision;
- AgentRevisionId;
- action capability membership;
- stale intent.

Gate не использует hidden Environment Ground Truth.

Behavior-changing override в `v0.2` отсутствует. Semantics-preserving normalization допустима только если явно записана; reference profile предпочитает уже canonical payload.

---

# 34. Action Commit

`ActionCommitRecord` создаётся только после successful authorization и до dispatch.

Минимум:

```text
action_commit_id
authorized_action_ref
selected_intent_ref
committed action
decision_window_id
episode_id
state_revision_at_commit
agent_revision_id
gate/action-interface revisions
dispatch_id
logical commit provenance
```

После commit:

- semantic action immutable;
- post-commit failure не удаляет record;
- Intervention не может задним числом изменить intent/action;
- второй normal Action Commit в том же Decision Window запрещён.

---

# 35. Dispatch profile

Reference dispatcher — synchronous in-process adapter над `EnvironmentInteraction` capability.

Он не выбирает behavior и не импортирует concrete MicroWorld implementation.

`DispatchAttempt` минимум сохраняет:

```text
dispatch_attempt_id
dispatch_id
action_commit_ref
attempt_index
adapter revision
send/result classification
provenance
```

Automatic retry в `v0.2`:

```text
DISABLED
```

Даже definite-not-sent failure не retry'ится молча; caller/runtime policy должен начать explicit recovery path.

---

# 36. Failure taxonomy

Минимально machine-distinct:

```text
malformed intent
stale intent
authorization rejection
definite dispatch failure
execution_unknown
successful Environment Transition
```

Дополнительно Environment различает:

```text
valid no-effect transition
terminal task failure
Environment internal error
invalid generated world
infrastructure truncation
```

`valid no-effect transition` не превращается в dispatch failure.

---

# 37. execution_unknown / reconciliation

Если adapter не может доказать, произошло ли применение committed action:

```text
Action Commit
→ DispatchAttempt
→ execution_unknown
→ RECONCILIATION_REQUIRED
```

В этом state запрещены:

- blind retry;
- новый Action Commit;
- следующий normal Decision Window;
- reset, маскирующий unresolved causal history.

Minimal reconciliation capability создаёт **новый** record/event и может разрешить:

```text
definitely_not_executed
executed_with_recoverable_result
executed_but_result_unavailable
still_unknown
```

Если `executed_with_recoverable_result`, normal Outcome Commit продолжается из recovered InteractionResult.

Если `definitely_not_executed`, исходный Action Commit остаётся в history; Decision Window закрывается как post-commit execution failure, после чего новый window может повторно ingest последнее достоверное observation.

Если action executed, но next observation/outcome нельзя восстановить, `v0.2` fail-closed truncates Episode с explicit infrastructure provenance вместо выдуманного outcome.

Test fault adapter обязан уметь моделировать unknown как до применения action, так и после фактического transition с потерянным result.

---

# 38. Environment Transition / Outcome Commit

На success:

```text
Dispatch
→ MicroWorld publishes EnvironmentTransitionId
→ agent-facing InteractionResult
→ InteractionRuntime creates OutcomeId
→ interaction.outcome boundary commit
→ Experience Journal append
→ POST_OUTCOME phase
```

`InteractionResult` содержит:

```text
next RawObservation
ExternalTaskFeedback?
agent-visible action outcome?
terminated
truncated
```

Research-only authoritative transition record хранится через Environment Research Plane и не передаётся Agent.

Final observation/outcome сохраняется в causal experience до любого reset.

---

# 39. Next Decision Window

Если outcome не terminal:

```text
POST_OUTCOME completes
→ previous Decision Window CLOSED
→ allocate new DecisionWindowId
→ ingest InteractionResult.raw_observation as observation.current
→ next Decision Window OPEN
```

Outcome Commit и next observation ingress — разные causal boundaries/state revisions.

Если `terminated` или `truncated`:

```text
final outcome recorded
→ POST_OUTCOME
→ Decision Window CLOSED
→ Episode CLOSED
```

Новый Episode требует explicit reset; `AgentSessionId` сохраняется.

---

# 40. Experience Journal boundary

Invariant:

```text
Experience Journal
≠ CognitiveState
≠ Evidence Trace
≠ Training Replay
≠ Agent Memory
```

Reference contracts:

```text
ExperienceEventEnvelope
ExperienceEvent payload variants
ExperienceJournal Protocol
InMemoryExperienceJournal
```

Journal API:

```text
append(event)
snapshot() -> immutable ordered tuple
manifest/summary read
```

Нет update/delete source event API.

---

# 41. Experience event envelope

Минимум:

```text
event_id
event_schema_id/revision
event_kind
logical scope
causal parent event IDs
producer boundary
visibility class
source mode/execution context subset
semantic payload
revision/provenance refs
integrity status
```

Logical scope умеет выразить применимые:

```text
RunId
AgentSessionId
EpisodeId
DecisionWindowId
CognitiveCycleId
EnvironmentTransitionId
```

Wall-clock допускается только diagnostic metadata и не является causal order.

---

# 42. Core journal events v0.2

Минимальный registry:

```text
EpisodeStarted
ObservationCommitted
GoalCommitted
GoalTransitioned
PerceptCommitted
PolicyIntentSelected
AuthorizationResolved
ActionCommitted
DispatchAttempted
DispatchResolved
ExecutionUnknown
ReconciliationResolved
EnvironmentTransitionObserved
OutcomeCommitted
DecisionWindowClosed
EpisodeEnded
```

Не каждый event обязан содержать full duplicated payload; reference-backed causal identity допустима, если reconstruction не требует ambient mutable object.

Unknown/failure сохраняются как source history.

Пример:

```text
E100 = ExecutionUnknown
E147 = ReconciliationResolved(target=E100)
```

`E100` не мутируется.

---

# 43. Research annotations isolation

MicroWorld authoritative hidden transition evidence и oracle labels не добавляются в normal `ExperienceJournal`.

Reference Research Plane имеет отдельный append-only research record/log surface и может ссылаться на interaction IDs.

```text
ExperienceEvent
≠ ResearchAnnotationRecord
```

Будущая privileged dataset projection сможет явно join эти planes по policy; `v0.2` такого training projection не реализует.

---

# 44. Journal storage / schema evolution

Reference backend:

```text
InMemoryExperienceJournal
```

Events frozen/typed. `journal_revision` увеличивается append-only, но старые event IDs/payload meaning не меняются.

Event registry связывает:

```text
event_kind
→ payload schema id/revision
→ required scope
→ required causal parents
→ default visibility
```

Future SQLite backend, Arrow/Parquet projections или durable journal могут быть добавлены без изменения source-event semantics.

---

# 45. Evidence Plane coexistence

Existing O0 `EvidenceRecorder` продолжает фиксировать kernel structural execution:

```text
waves
module attempts
state commits
interventions
```

`ExperienceJournal` фиксирует semantic interaction history.

Допустим cross-reference по causal IDs, но запрещено:

- считать Evidence Trace Agent Memory;
- строить Journal простым alias списка TraceEvent;
- помещать research ground truth в Journal потому, что оно доступно profiler/evaluator.

---

# 46. Reference profile configuration

Новый strict TOML schema:

```text
mindra.interaction-profile/v1
```

Conceptual sections:

```toml
schema = "mindra.interaction-profile/v1"
profile_id = "v0_2.reference"

[kernel]
# resolved module composition

[interaction]
cognitive_cycles_per_decision = 1
max_decision_windows = ...

[environment]
family = "reference.microworld.v1"
task_family = "mw0_direct_reach"
root_seed = ...
observation_radius = ...

[experience]
backend = "in_memory"
```

Parser strict-validates unknown keys/settings. Raw profile не читается cognitive modules.

Research-only generation metadata отделяется от agent-visible state.

---

# 47. Composition Root v0.2

`CompositionRoot` остаётся единственным wiring boundary.

Он должен собирать:

```text
KernelRuntime
LifecycleCoordinator
MicroWorld private core
MicroWorldInteraction capability
MicroWorldResearch capability
ReferencePerception
ReferenceGoalSystem + StructuredExternalTaskGrounder
ReferencePolicy
SchemaOnlyActionGate
ActionCommitCoordinator
InProcessDispatcher
InMemoryExperienceJournal
InteractionRuntime
```

Entrypoint не конструирует эти objects вручную.

Research capability возвращается только через explicit research-facing composition result/test harness и не внедряется в Agent-facing constructors.

---

# 48. CLI / smoke

Добавляется:

```text
mindra interaction-smoke --profile configs/v0.2/reference.toml
```

Smoke:

- создаёт Composition Root v0.2 profile;
- выполняет `MW0_DIRECT_REACH` до terminal success;
- печатает concise deterministic summary;
- не печатает hidden state/oracle;
- не требует network/GPU.

Existing:

```text
mindra validate-profile --profile configs/v0.1/reference.toml
mindra kernel-smoke --profile configs/v0.1/reference.toml
```

остаются regression-supported.

`validate-profile` расширяется на оба profile schema fail-closed.

---

# 49. Determinism claim v0.2

Reference claim:

```text
same code revision
same locked dependencies
same resolved interaction profile
same root seed / deterministic ID configuration
same initial Environment definition/state
same action/cognition sequence
→ same canonical agent-visible trajectory
→ same Environment transition sequence
→ same state revisions/logical identities
→ same Experience event-kind/causal sequence
```

Physical timestamps/benchmark duration не входят в equality claim.

Snapshot claim:

```text
snapshot at S
→ run suffix A
restore S
→ run same suffix A
→ same canonical continuation
```

в пределах compatible Environment version/profile.

---

# 50. VerificationObligations v0.2

## `V02-001 — Canonical trajectory determinism`

Одинаковый code/profile/seed/initial state → одинаковая canonical interaction trajectory и logical event sequence.

## `V02-002 — Environment snapshot continuation`

Snapshot/restore захватывает hidden state + all causal RNG state; одинаковый action suffix даёт одинаковое продолжение.

## `V02-003 — Agent/Research plane isolation`

Hidden state, seed/split/oracle/world manifest metadata не доступны через agent interaction capability, RawObservation, Perception или Policy declared reads.

## `V02-004 — Session/Episode lifecycle`

Один AgentSession переживает несколько Environment resets; каждый reset создаёт новый EpisodeId и не выполняет полный Agent reset.

## `V02-005 — Decision Window multiplicity`

Один Episode содержит несколько Decision Windows; один Decision Window может содержать несколько Cognitive Cycles и не более одного normal Action Commit/Environment Transition.

## `V02-006 — Correct outcome lineage`

Outcome Commit и EnvironmentTransition ссылаются на правильный ActionCommit/Dispatch/DecisionWindow; terminal final outcome сохраняется до reset.

## `V02-007 — Percept boundary`

CanonicalPercept содержит только current observation semantics/deterministic normalization и не alias hidden belief/memory/prediction.

## `V02-008 — Goal authority/lifecycle`

External task → proposal → committed goal различимы; proposal source не мутирует GoalGraph; terminal/truncation transitions имеют correct episode-scoped semantics.

## `V02-009 — Policy isolation`

Reference Policy использует только declared agent-visible state fields, не получает Research Plane/Environment object и только создаёт SelectedActionIntent.

## `V02-010 — Action causal separation`

`SelectedActionIntent ≠ AuthorizedAction ≠ ActionCommit ≠ Dispatch ≠ EnvironmentTransition` машинно доказуемо по types/IDs/tests.

## `V02-011 — Action failure taxonomy`

Malformed/stale/rejected/definite dispatch failure/execution_unknown/successful transition различаются и имеют разные legal transitions.

## `V02-012 — No blind retry / immutable post-commit history`

`execution_unknown` не retry'ится автоматически; post-commit failure/reconciliation не удаляет и не переписывает ActionCommit.

## `V02-013 — Journal append-only lineage`

Experience events append-only, causal parents reconstruct episode/window/observation/percept/goal/intent/action/outcome history; failed/unknown interactions сохраняются.

## `V02-014 — Research annotation isolation`

Research-only Environment records/annotations не смешиваются с normal ExperienceJournal/agent-visible experience.

## `V02-015 — Termination/truncation/reset semantics`

`terminated` и `truncated` различаются; final outcome фиксируется; следующий Episode требует explicit reset; session state сохраняется по scope.

## `V02-016 — Scope negative gate`

В production package отсутствуют скрытые Cortex/Memory/World/Self/Drive/Appraisal/Planner/learning/training responsibilities; v0.1 invariants остаются green.

## `V02-017 — Build/install/CI reproducibility`

Final v0.2 wheel CPU-only устанавливается clean и запускает v0.1 + v0.2 reference smokes на Ubuntu/Windows Python 3.14.

---

# 51. Test taxonomy additions

Добавляются targeted suites минимум для:

```text
tests/unit/test_interaction_identities.py
tests/contract/test_boundary_state_commit.py
tests/contract/test_environment_capabilities.py
tests/property/test_microworld_determinism.py
tests/property/test_environment_snapshot.py
tests/contract/test_perception_boundary.py
tests/contract/test_goal_authority.py
tests/contract/test_policy_isolation.py
tests/contract/test_action_boundary.py
tests/state_machine/test_action_lifecycle.py
tests/state_machine/test_interaction_lifecycle.py
tests/contract/test_experience_journal.py
tests/integration/test_interaction_runtime.py
tests/integration/test_v0_2_reference_profile.py
tests/integration/test_v0_2_cli.py
```

Exact file split может измениться, но obligation coverage не ослабляется.

Negative/bypass tests обязательны, а не только happy path.

---

# 52. Full local verification profile

Final profile называется:

```text
FULL-C0-v0.2
```

Exact final commands:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked lint-imports
uv run --locked pytest
uv run --locked mindra validate-profile --profile configs/v0.1/reference.toml
uv run --locked mindra kernel-smoke --profile configs/v0.1/reference.toml
uv run --locked mindra validate-profile --profile configs/v0.2/reference.toml
uv run --locked mindra interaction-smoke --profile configs/v0.2/reference.toml
uv build
uv run --locked python tools/verify_v0_2_artifact.py
```

`verify_v0_2_artifact.py` обязан в отдельном clean Python 3.14 environment проверить:

- package metadata `0.2.0`;
- runtime third-party requirements = 0;
- historical v0.1 validation/kernel smoke;
- v0.2 validation/interaction smoke.

До появления соответствующих v0.2 files каждый IS выполняет весь уже существующий `FULL-C0` regression плюс доступную применимую часть `FULL-C0-v0.2`. Отсутствующий future command до его scheduled step — `NOT APPLICABLE`, а не fictitious PASS.

---

# 53. CI profile

GitHub Actions остаётся CI provider.

Final declared matrix:

```text
Ubuntu latest / Python 3.14 / FULL-C0-v0.2
Windows latest / Python 3.14 / FULL-C0-v0.2
```

CI:

- locked environment;
- CPU-only;
- tests не требуют network после dependency installation;
- запускает v0.1 и v0.2 canonical CLI;
- проверяет clean v0.2 wheel.

Не создаётся отдельный GPU job.

---

# 54. Acceptance gate v0.2

Version может быть принята только если одновременно:

1. все `V02-001 … V02-017` имеют explicit PASS evidence;
2. `V01-001 … V01-014` остаются regression-green по применимым tests;
3. `MW0_DIRECT_REACH` end-to-end smoke завершается deterministic success;
4. MicroWorld partial-observation + Research Plane isolation проверены negative tests;
5. snapshot/restore continuation deterministic;
6. multiple Cognitive Cycles не вызывают multiple Environment transitions;
7. Action Commit происходит после authorization и до dispatch;
8. malformed/stale/rejected intent не commit'ится;
9. definite failure и `execution_unknown` различимы;
10. blind retry при unknown невозможен;
11. Journal append-only и восстанавливает causal lineage;
12. research records не попадают в Journal/Policy/Perception;
13. terminated/truncated/reset/session semantics machine-tested;
14. final `FULL-C0-v0.2` green локально в доступной OS;
15. Ubuntu + Windows CI green для implementation candidate;
16. clean wheel verification green;
17. no forbidden future scope найдено independent audit.

---

# 55. Known risks / design controls

## Risk: InteractionRuntime превращается в god object

Control: он владеет только lifecycle sequencing и capabilities; cognition остаётся в KernelRuntime/modules, dynamics — Environment, behavior selection — Policy, dispatch semantics — Action boundary/execution runtime.

## Risk: hidden state leakage через удобный MicroWorld object

Control: разные capability wrappers + разные data types + constructor/import negative tests.

## Risk: Goal completion использует evaluator truth

Control: GoalSystem получает только agent-visible ExternalTaskFeedback; objective research metrics живут Research Plane.

## Risk: Journal становится вторым Evidence Trace

Control: отдельные event schemas/responsibilities; journal records semantic interaction events, Evidence records kernel structural execution.

## Risk: premature future abstraction

Control: feature views пусты; Planner/Memory/World Model отсутствуют; delayed-event primitive допускается только как Environment state needed for snapshot readiness, не как отдельный cognitive feature.

## Risk: `execution_unknown` слишком сложен для in-process world

Control: normal reference dispatcher остаётся synchronous/exact; injected fault adapter machine-tests semantics, чтобы future remote integration не потребовала breaking causal redesign.

---

# 56. Deferred work

Явно отложено:

- Gymnasium adapter;
- dm_env adapter;
- durable ExperienceJournal backend;
- Arrow/Parquet dataset projections;
- coordinated Agent+Environment snapshot/restore;
- real Memory/Cortex/World/Self;
- Planner;
- learned Policy/RL;
- async dispatch/cancellation;
- distributed/vectorized Environment;
- large procedural benchmark distributions;
- MINDRA-Eval scoring/claims.

---

# 57. Migration compatibility с v0.1

`v0.2` обязана сохранить:

```text
mindra kernel-smoke --profile configs/v0.1/reference.toml
```

и весь accepted Core Kernel behavior.

Additive API evolution допускается для:

- `StateFieldSpec.owner` → `ModuleId | RuntimeBoundaryId`;
- new freshness modes;
- new lifecycle phases;
- context-aware KernelRuntime cycle path;
- new identity types;
- phase-aware execution-plan/lifecycle support.

Недопустимы:

- mutable global state;
- direct Environment writes into CognitiveState;
- replacing `StateProjection` by full ambient state reads;
- direct peer calls between cognitive modules;
- Environment execution inside CognitiveScheduler;
- semantic alias action intent/commit/outcome.

---

# 58. Design acceptance result

Exact profile принят:

```text
custom stdlib-only symbolic MicroWorld
strict Agent Interaction Plane / Research Plane capability split
InteractionRuntime owns external lifecycle
KernelRuntime owns internal cognition
CognitiveScheduler remains COGNITIVE_CYCLE-only
LifecycleCoordinator handles EPISODE_START / POST_OUTCOME module phases
runtime-owned state ingress through BoundaryCommitCoordinator
structured CanonicalPercept, no tensor dependency
episode-scoped external Goal System subset
deterministic ReferencePolicy, no Planner
post-authorization pre-dispatch Action Commit
explicit definite failure / execution_unknown / reconciliation semantics
append-only typed InMemoryExperienceJournal
FULL-C0-v0.2 on Ubuntu + Windows CPU-only
17 machine-checkable VerificationObligations
```

Dependency-ordered implementation находится в:

```text
docs/versions/v0.2/implementation-sequence.md
```

Live status и единственный `OPEN` step определяет только `docs/design/current.md`.