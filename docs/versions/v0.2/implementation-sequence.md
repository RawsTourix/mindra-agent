# MINDRA v0.2 — Implementation Sequence

## Статус

**Software milestone:** `v0.2 — MicroWorld Interaction`  
**Статус:** `accepted`  
**Version design:** [`README.md`](README.md) — `accepted`  
**Semantic baseline:** `F31`  
**Входной baseline:** accepted `v0.1 Core Kernel`  
**Live implementation status:** только `docs/design/current.md`

Этот документ выводит dependency-ordered implementation steps из accepted exact design `v0.2`.

Он не создаёт новую semantic architecture. Если step невозможно реализовать без изменения `F31`, accepted `v0.2/README.md` или frozen contracts, coding останавливается с blocker report.

---

# 1. Dependency graph

Exact dependency graph:

```text
IS-01 interaction temporal/state-ingress foundation
   ↓
IS-02 lifecycle phases + KernelRuntime context bridge
   ↓
IS-03 Environment contracts / capability split
   ↓
IS-04 deterministic MicroWorld core + MW0 + snapshot
   ↓
IS-05 MicroWorld task families / hidden-rule controls
   ↓
IS-06 Perception
   ↓
IS-07 Goals
   ↓
IS-08 Reference Policy
   ↓
IS-09 Action Boundary / dispatch / reconciliation
   ↓
IS-10 Experience Journal
   ↓
IS-11 InteractionRuntime vertical orchestration
   ↓
IS-12 v0.2 Composition Root / profile / package migration
   ↓
IS-13 CLI / clean artifact / CI
   ↓
IS-14 version acceptance hardening
```

Cross-dependencies:

```text
IS-08 depends on IS-06 + IS-07
IS-09 depends on SelectedActionIntent from IS-08
IS-10 depends on interaction/action identities from IS-01/IS-09
IS-11 depends on IS-02 + IS-04..IS-10
IS-12 wires only already accepted boundaries
```

Ни один step не реализует следующий заранее.

---

# 2. Общие operational rules

Для каждого `V0.2-IS-XX` обязательны:

1. repository preflight;
2. чтение `AGENTS.md`, `docs/design/current.md`, F31 freeze/manifest, roadmap, `CSPT-02`, v0.2 README и текущего section;
3. чтение перечисленных canonical design/ADR/contracts;
4. exact scope only;
5. targeted verification;
6. полный уже существующий local regression profile;
7. truthful CI status semantics;
8. structured Codex report;
9. independent ChatGPT audit после operator commit/push;
10. следующий IS остаётся `CLOSED` до отдельного transition.

Запрещено:

- самостоятельно менять F31/version design/sequence;
- ослаблять tests/import/type contracts;
- скрывать failure через skip/xfail/broad ignore;
- делать test-only production bypass;
- использовать Research Ground Truth как agent-visible input;
- добавлять future modules/responsibilities;
- commit/push из Codex без отдельного разрешения.

---

# 3. Verification profiles

## Targeted

Каждый step указывает обязательные targeted tests/checks.

## Existing regression

До появления final v0.2 artifact tooling каждый step запускает существующий полный Core Kernel regression минимум:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked lint-imports
uv run --locked pytest
uv build
```

Плюс canonical v0.1 CLI, когда изменения затрагивают composition/entrypoints:

```text
uv run --locked mindra validate-profile --profile configs/v0.1/reference.toml
uv run --locked mindra kernel-smoke --profile configs/v0.1/reference.toml
```

## Final `FULL-C0-v0.2`

После `IS-13` обязательный full profile:

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

До scheduled появления конкретной v0.2 command она `NOT APPLICABLE`, не `PASS`.

---

# 4. `V0.2-IS-01 — Interaction temporal & boundary-state foundation`

## Цель

Добавить минимальные causally typed primitives, без которых Environment/Perception/Goals нельзя публиковать корректно, не реализуя сами эти subsystems.

## Prerequisites

- `v0.1` accepted;
- `v0.2/README.md` accepted;
- этот sequence accepted;
- только этот step `OPEN` в `docs/design/current.md`.

## Mandatory canonical context

- `docs/design/execution-model.md` (`DU-03`);
- `docs/design/cognitive-state.md` (`DU-04`);
- `docs/design/module-lifecycle.md` (`DU-05`);
- `docs/design/contracts/semantic-freeze-manifest.md`;
- `ADR-0003`, `ADR-0004`, `ADR-0005`.

## Exact scope

В `mindra.contracts` добавить/уточнить interaction identities минимум:

```text
ObservationId
PerceptId
ExternalTaskId
GoalProposalId
GoalId
ActionIntentId
AuthorizedActionId
ActionCommitId
DispatchId
DispatchAttemptId
EnvironmentTransitionId
OutcomeId
ExperienceEventId
JournalId
EnvironmentSnapshotId
WorldInstanceId
```

Сохранить injected `IdFactory` ownership.

Расширить state ownership:

```text
StateFieldSpec.owner
ModuleId
→ ModuleId | RuntimeBoundaryId
```

при сохранении single-writer semantic ownership.

Добавить freshness modes:

```text
CURRENT_DECISION_WINDOW
CURRENT_EPISODE
```

и их fail-closed temporal validation.

Добавить runtime-boundary staged/commit path conceptually:

```text
BoundaryStateUpdate
BoundaryStateWrite
BoundaryCommitCoordinator
```

с отдельной authority validation от module `CommitCoordinator`.

Boundary commit обязан:

- принимать только `RuntimeBoundaryId`-owned paths;
- проверять exact base revision;
- проверять schema/value/freshness/logical scope;
- публиковать atomically;
- создавать normal state revision/provenance;
- не выдавать mutable store.

## Forbidden scope

Не создавать:

- Environment API/MicroWorld;
- new lifecycle phases;
- Perception/Goal/Policy/Action types кроме перечисленных opaque identities;
- Experience Journal;
- InteractionRuntime;
- v0.2 config/CLI.

Не рефакторить existing module `CommitCoordinator` в универсальный unrestricted writer.

## Tests

Минимум:

```text
tests/unit/test_interaction_identities.py
tests/contract/test_runtime_state_ownership.py
tests/contract/test_boundary_state_commit.py
tests/unit/test_interaction_freshness.py
```

Negative cases:

- ModuleId не может использовать BoundaryCommitCoordinator;
- RuntimeBoundaryId не может писать ModuleId-owned path;
- stale base rejected;
- wrong EpisodeId/DecisionWindowId freshness rejected;
- validation failure не публикует partial state.

## VerificationObligations

- `V02-004` — foundation;
- `V02-005` — temporal foundation;
- `V02-016` — architecture regression.

## Targeted verification

```text
uv run --locked pytest tests/unit/test_interaction_identities.py tests/unit/test_interaction_freshness.py tests/contract/test_runtime_state_ownership.py tests/contract/test_boundary_state_commit.py
uv run --locked mypy src tests
uv run --locked lint-imports
```

После targeted — полный существующий regression profile.

## Acceptance

Step принят только если runtime-boundary state publication возможна без Environment implementation и без ослабления v0.1 module ownership/atomicity.

---

# 5. `V0.2-IS-02 — Lifecycle phases & KernelRuntime context bridge`

## Цель

Дать Agent kernel standardized non-environment lifecycle execution и передавать Episode/Decision context внутрь cognitive cycles без переноса Environment orchestration в scheduler.

## Prerequisite

`IS-01 accepted`.

## Mandatory canonical context

- `DU-03` execution model;
- `DU-05` module lifecycle;
- `DU-06` observability/intervention;
- `ADR-0003`, `ADR-0005`, `ADR-0006`.

## Exact scope

Добавить phases:

```text
EPISODE_START
POST_OUTCOME
```

Сохранить `CognitiveScheduler` как `COGNITIVE_CYCLE`-only.

Ввести отдельный `LifecycleCoordinator`, который:

- исполняет compiled module plans только для supported non-cycle phases;
- использует `StateProjection`, `WaveExecutor`, atomic module commit semantics;
- не вызывает Environment/Dispatcher;
- имеет O0 evidence для phase/module/commit attempts настолько, насколько нужно reconstructability.

Расширить plan compilation на phase-specific plans без instantaneous cross-phase cycle.

Добавить additive `KernelRuntime` API для caller-supplied current Episode/Decision context, при котором `CognitiveCycleId` по-прежнему создаёт KernelRuntime.

Existing no-argument `run_cycle()` v0.1 profile остаётся regression-compatible.

Intervention boundary validation должна запрещать intervention во время in-flight lifecycle/cycle execution; interaction-specific post-commit lock появится в `IS-11`.

## Forbidden scope

- Environment reset/step;
- InteractionRuntime;
- Goal module;
- action lifecycle;
- generic global event bus;
- rename/remove v0.1 public behavior без необходимости.

## Tests

```text
tests/contract/test_lifecycle_phases.py
tests/integration/test_lifecycle_coordinator.py
tests/integration/test_kernel_runtime_context.py
```

Проверить:

- phase plan содержит только declared participants;
- `CognitiveScheduler` rejects non-cycle plan;
- multiple cycles под одним DecisionWindow имеют разные CognitiveCycleId;
- context mismatch fail-closed;
- v0.1 `run_cycle()` unchanged.

## Obligations

- `V02-004` — foundation;
- `V02-005` — substantial;
- `V02-016` — regression.

---

# 6. `V0.2-IS-03 — Environment contracts & capability split`

## Цель

Зафиксировать exact machine-facing Environment boundary без concrete dynamics.

## Prerequisite

`IS-02 accepted`.

## Mandatory canonical context

- `docs/design/modules/environment.md`;
- `docs/design/contracts/environment.md`;
- `ADR-0007`;
- `DU-03`, `DU-04`, `DU-06`.

## Exact scope

В `mindra.contracts.environment`/`interaction` реализовать frozen typed forms минимум:

```text
EnvironmentDescriptor
EnvironmentInteractionDescriptor
ActionCapabilityDescriptor
EpisodeStartRequest
EpisodeStartResult
RawObservation
ExternalTaskSpecification
ExternalTaskFeedback
InteractionResult
EnvironmentTransitionRef/receipt
EnvironmentSnapshot contract types
EnvironmentInteraction Protocol
EnvironmentResearch Protocol
```

Typed MicroWorld semantic actions:

```text
Move
Interact
Pickup
Drop
Wait
Direction
```

Agent-facing types не содержат hidden/research fields.

Research-facing types отдельно выражают:

- World/environment identities;
- hidden state descriptor refs;
- world manifest/generation provenance;
- snapshot/restore/fork capability;
- research transition records.

No concrete engine.

## Forbidden scope

- Gymnasium/dm_env dependency;
- NumPy;
- concrete grid dynamics;
- Perception/Goal/Policy;
- Environment object внутри CognitiveState.

## Tests

```text
tests/contract/test_environment_contracts.py
tests/contract/test_environment_capability_split.py
```

Negative tests подтверждают отсутствие Research Ground Truth fields/methods на agent-facing contracts.

## Obligations

- `V02-003` — contract foundation;
- `V02-010` — action-interface foundation;
- `V02-015` — terminated/truncated contract foundation.

---

# 7. `V0.2-IS-04 — Deterministic MicroWorld core, MW0 & snapshot`

## Цель

Реализовать минимальный, но архитектурно полный Environment engine до cognitive modules.

## Prerequisite

`IS-03 accepted`.

## Mandatory context

- Environment canonical design/contract;
- `v0.2/README.md` sections Environment/RNG/Snapshot/MW0;
- `ADR-0007`.

## Exact scope

Создать `mindra.reference.microworld`:

- private world core;
- `MicroWorldInteraction` capability wrapper;
- `MicroWorldResearch` capability wrapper;
- immutable public definitions/state records;
- walls/floor/target/basic portable entity primitives;
- typed `Move/Interact/Pickup/Drop/Wait` handling;
- partial observation radius/occlusion;
- full-observation agent control mode;
- `MW0_DIRECT_REACH` fixed + procedural fixtures;
- separate `generation_rng`, `dynamics_rng`, `task_rng` using instance `random.Random`;
- SHA-256 role seed derivation;
- snapshot/restore/clone/fork with all RNG states;
- deterministic research transition records;
- terminated/truncated distinction.

World-level blocked movement is successful no-effect transition.

Environment publishes transition atomically: exception before publish cannot expose partial hidden mutation.

## Forbidden scope

- cognitive modules;
- Action Boundary dispatcher;
- Experience Journal;
- Gym adapter;
- graphical game/UI dependency;
- benchmark suite.

## Tests

```text
tests/unit/test_microworld_actions.py
tests/property/test_microworld_determinism.py
tests/property/test_environment_snapshot.py
tests/contract/test_microworld_capability_isolation.py
```

Property tests:

- same seed/spec/action suffix same trajectory;
- snapshot/restore same continuation;
- clone/fork no mutable alias;
- interaction capability cannot inspect hidden state;
- partial observation omits hidden cells/rules;
- seed/world manifest not present in RawObservation.

## Obligations

- `V02-001` — Environment layer;
- `V02-002` — closed at Environment layer;
- `V02-003` — substantial;
- `V02-015` — Environment layer.

---

# 8. `V0.2-IS-05 — Controlled task families & hidden-rule controls`

## Цель

Расширить MicroWorld достаточно для architecture stress без превращения версии в benchmark project.

## Prerequisite

`IS-04 accepted`.

## Exact scope

Добавить:

```text
MW1_FETCH_UNLOCK
MW3_HIDDEN_SWITCH
```

World primitives:

```text
key/tool
door
switch
hidden causal mapping
pending event representation
hazard marker support where needed for fixtures
```

Добавить deterministic solvability/config validators для canonical fixtures/generator subset.

Hidden mapping доступен только через Research Plane. Observable appearance не кодирует mapping shortcut.

`pending_events` реализуется как Environment state primitive только для snapshot/future delayed-effect readiness; отдельный delayed benchmark family не добавляется.

## Forbidden scope

- Memory/World Model;
- learned solver;
- Planner;
- reward shaping framework;
- large random benchmark distribution;
- research claim о hidden-rule learning.

## Tests

```text
tests/integration/test_mw1_fetch_unlock.py
tests/integration/test_mw3_hidden_switch.py
tests/contract/test_hidden_rule_leakage.py
tests/property/test_task_snapshot_continuation.py
```

## Obligations

- `V02-002` — task-state extension;
- `V02-003` — closed Environment leakage layer;
- `V02-016` — no future cognition.

---

# 9. `V0.2-IS-06 — Structured Perception`

## Цель

Преобразовать RawObservation в structured CanonicalPercept без belief/memory/neural coupling.

## Prerequisite

`IS-05 accepted`.

## Mandatory context

- `docs/design/modules/perception.md`;
- `docs/design/contracts/perception.md`;
- `ADR-0008`;
- `DU-04`, `DU-05`.

## Exact scope

Implement frozen types:

```text
CanonicalPercept
PerceptEnvelope
SemanticCore
ObservedSelf
ObservedEntity
ObservedRelation
ObservedEvent
FeatureView
```

Reference feature views = empty tuple.

`ReferencePerception`:

- `COGNITIVE_CYCLE` module;
- reads only `observation.current` with `CURRENT_DECISION_WINDOW`;
- writes only `perception.current`;
- uses percept-local entity IDs;
- deterministic canonical ordering/normalization;
- no hidden inference.

## Forbidden scope

- tensors/embeddings;
- Cortex;
- object permanence/World Belief;
- memory;
- Research Plane access.

## Tests

```text
tests/contract/test_perception_boundary.py
tests/unit/test_reference_perception.py
tests/property/test_perception_determinism.py
```

Negative tests feed observations with same visible data but different hidden worlds and require same percept.

## Obligations

- `V02-003` — downstream leakage;
- `V02-007` — closed;
- `V02-016` — scope.

---

# 10. `V0.2-IS-07 — External-task Goal System subset`

## Цель

Реализовать distinction ExternalTask → GoalProposal → Committed Goal и episode lifecycle без autonomous goals.

## Prerequisites

`IS-06 accepted`, lifecycle machinery from `IS-02`.

## Mandatory context

- `docs/design/modules/goals.md`;
- `docs/design/contracts/goals.md`;
- `ADR-0009`;
- `DU-03`, `DU-04`, `DU-05`.

## Exact scope

Frozen forms:

```text
GoalProposal
CommittedGoal
GoalGraph
GoalObjective variants для v0.2 tasks
GoalLifecycleStatus
GoalProgress
```

`StructuredExternalTaskGrounder` имеет proposal authority only.

`ReferenceGoalSystem`:

- единственный owner `goal.graph`;
- `EPISODE_START`: читает `task.external`, ground/validate/adopt;
- `POST_OUTCOME`: читает `interaction.outcome`, меняет progress/lifecycle;
- uses only agent-visible ExternalTaskFeedback;
- one root episode-scoped external goal.

Terminal mapping по README.

## Forbidden scope

- autonomous goal generation;
- Drives;
- planner decomposition;
- goal utility/value architecture;
- hidden oracle success.

## Tests

```text
tests/contract/test_goal_authority.py
tests/integration/test_goal_episode_start.py
tests/integration/test_goal_post_outcome.py
```

Negative:

- grounder cannot commit;
- research success label cannot enter GoalSystem input;
- wrong-episode task/outcome rejected.

## Obligations

- `V02-008` — closed;
- `V02-015` — goal terminal semantics;
- `V02-016` — no autonomous future scope.

---

# 11. `V0.2-IS-08 — Deterministic Reference Policy`

## Цель

Закрыть behavior-selection boundary простым deterministic control без Planner/Cortex.

## Prerequisites

`IS-06`, `IS-07 accepted`.

## Mandatory context

- `docs/design/modules/policy-planner.md`;
- `docs/design/contracts/policy-planner.md`;
- `ADR-0023`;
- `DU-05`, `DU-24` boundary distinction.

## Exact scope

Frozen `SelectedActionIntent` v0.2 form.

`ReferencePolicy`:

- stateless/deterministic `COGNITIVE_CYCLE` module;
- reads only `perception.current`, `goal.graph`, `action.capability`;
- writes only `policy.selected_intent`;
- deterministic tie-break;
- direct visible-goal greedy behavior + deterministic legal fallback;
- sufficient to solve canonical `MW0_DIRECT_REACH` fixtures.

Policy constructor must not accept Environment/Research capability.

## Forbidden scope

- Planner;
- candidate search tree;
- World Model;
- Memory;
- RL/neural policy;
- action execution/authorization.

## Tests

```text
tests/contract/test_policy_isolation.py
tests/unit/test_reference_policy.py
tests/property/test_policy_determinism.py
```

Architecture tests inspect constructor/import dependency and declared reads.

## Obligations

- `V02-009` — closed;
- `V02-010` — intent side foundation;
- `V02-016` — scope.

---

# 12. `V0.2-IS-09 — Action Boundary, dispatch & reconciliation`

## Цель

Реализовать causal separation Policy choice → authorization → commit → dispatch → execution classification.

## Prerequisite

`IS-08 accepted`.

## Mandatory context

- `docs/design/modules/action-boundary.md`;
- `docs/design/contracts/action-boundary.md`;
- `ADR-0024`;
- `DU-03` Action Commit semantics.

## Exact scope

Implement types/boundaries минимум:

```text
ActionAuthorizationRequest
ActionAuthorizationResult
AuthorizedAction
ActionCommitRecord
DispatchAttempt
DispatchResult
DispatchReconciliationRecord
SchemaOnlyActionGate
ActionCommitCoordinator
Dispatcher Protocol
InProcessDispatcher
```

Gate validates schema/interface/current episode/window/state/agent revision/capability.

`ActionCommitCoordinator` enforces one normal commit per DecisionWindow.

Dispatcher depends only on `EnvironmentInteraction` contract.

Failure classes:

```text
malformed
stale
rejected
definite_not_sent / definite dispatch failure
execution_unknown
success transition
```

No automatic retry.

Add injected fault dispatcher fixtures for:

- definitely not sent;
- action actually applied but result lost → unknown;
- unknown resolved as not executed;
- unknown resolved with recovered result;
- unresolved/irrecoverable result.

## Forbidden scope

- policy fallback inside gate;
- hidden behavior-changing override;
- retry/backoff framework;
- async/network transport;
- InteractionRuntime orchestration;
- Environment-specific imports in runtime.

## Tests

```text
tests/contract/test_action_boundary.py
tests/state_machine/test_action_lifecycle.py
tests/integration/test_dispatch_faults.py
```

## Obligations

- `V02-010` — closed;
- `V02-011` — closed at boundary layer;
- `V02-012` — closed at boundary layer.

---

# 13. `V0.2-IS-10 — Append-only Experience Journal`

## Цель

Создать source causal interaction recording до orchestration integration.

## Prerequisite

`IS-09 accepted`.

## Mandatory context

- `docs/design/experience-data-replay.md`;
- `docs/design/contracts/experience-data-replay.md`;
- `ADR-0025`;
- `DU-06` evidence distinction.

## Exact scope

Implement:

```text
ExperienceEventEnvelope
LogicalScope subset
VisibilityClass subset
IntegrityStatus subset
v0.2 payload variants / registry
ExperienceJournal Protocol
InMemoryExperienceJournal
ExperienceJournalManifest/Snapshot
separate ResearchAnnotation/ResearchRecord interface where needed
```

Core event kinds from README.

Journal:

- append-only public API;
- old events immutable;
- causal parents validated where required;
- journal revision increments on append;
- immutable snapshot to consumers;
- no EvidenceRecorder alias.

Research-only records use separate storage/surface.

## Forbidden scope

- SQLite/Arrow/Parquet dependency;
- training replay;
- dataset projection;
- Agent Memory;
- mutating unknown event after reconciliation.

## Tests

```text
tests/contract/test_experience_journal.py
tests/property/test_journal_append_only.py
tests/contract/test_research_record_isolation.py
```

Include `ExecutionUnknown` then later `ReconciliationResolved` as two source events.

## Obligations

- `V02-013` — journal layer closed;
- `V02-014` — journal/research separation closed.

---

# 14. `V0.2-IS-11 — InteractionRuntime vertical orchestration`

## Цель

Соединить уже реализованные boundaries в correct Agent↔Environment temporal state machine без wiring/config/CLI concerns.

## Prerequisites

`IS-02 … IS-10 accepted`.

## Mandatory context

- `DU-03` temporal model;
- `DU-05` lifecycle;
- `DU-06` interventions;
- `DU-07`, `DU-24`, `DU-25`;
- `ADR-0003`, `ADR-0024`, `ADR-0025`;
- v0.2 README interaction lifecycle sections.

## Exact scope

Implement `InteractionRuntime` with explicit states sufficient to express:

```text
SESSION_IDLE
EPISODE_ACTIVE / WINDOW_OPEN
ACTION_COMMITTED
RECONCILIATION_REQUIRED
EPISODE_TERMINATED
EPISODE_TRUNCATED
```

Exact enum naming may differ, legal transitions may not.

Implement operations conceptually:

```text
start_episode()
run_cognitive_cycle()
run_decision()
reconcile_pending()
close/abort according to typed outcome
```

Required sequence:

1. allocate EpisodeId;
2. Environment reset;
3. allocate DecisionWindowId;
4. observation/task boundary ingress;
5. EPISODE_START Goal phase;
6. 1..N cognitive cycles with no Environment transition;
7. select current-window intent;
8. authorize;
9. Action Commit;
10. dispatch;
11. success/failure/unknown branch;
12. Outcome Commit on known transition;
13. Journal semantic events;
14. POST_OUTCOME Goal phase;
15. next window or terminal Episode close.

Definite-not-executed failure closes committed window without EnvironmentTransition; a later new window may re-ingest last trustworthy observation with new DecisionWindowId.

Unknown blocks next normal action/reset until explicit reconciliation or fail-closed truncation record.

Agent-state interventions allowed only before Action Commit at declared safe boundary.

InteractionRuntime receives only `EnvironmentInteraction`, not Research capability.

## Forbidden scope

- CompositionRoot wiring;
- TOML parsing;
- CLI;
- action selection inside runtime;
- environment step inside CognitiveScheduler;
- manual Goal/Perception peer calls outside lifecycle scheduler;
- automatic retry.

## Tests

```text
tests/integration/test_interaction_runtime.py
tests/state_machine/test_interaction_lifecycle.py
tests/integration/test_multi_cycle_decision.py
tests/integration/test_interaction_unknown_reconciliation.py
```

State-machine must exercise:

- two episodes same AgentSession;
- multiple windows per episode;
- two cognitive cycles/one transition;
- stale/malformed/rejected no commit;
- definite failure;
- unknown blocks next action;
- post-commit record persists;
- termination vs truncation;
- final outcome before reset;
- journal causal chain.

## Obligations

- `V02-004`, `005`, `006` — closed;
- `V02-011`, `012` — runtime closed;
- `V02-013` — integration closed;
- `V02-015` — closed.

---

# 15. `V0.2-IS-12 — v0.2 Composition Root & interaction profile`

## Цель

Сделать новый vertical profile воспроизводимо собираемым только через canonical composition boundary.

## Prerequisite

`IS-11 accepted`.

## Exact scope

Implement strict:

```text
mindra.interaction-profile/v1
configs/v0.2/reference.toml
v0.2 composition result/facade
reference constructors/registry entries
```

CompositionRoot wires:

- KernelRuntime/lifecycle coordinator;
- MicroWorld private core + separate capabilities;
- Perception/Goal/Policy modules;
- Action Boundary/dispatcher;
- ExperienceJournal;
- InteractionRuntime.

Only research-facing composition result exposes `MicroWorldResearch`; Agent/runtime/module constructors do not.

Add v0.2 schema fields/owners/initial values including `action.capability`.

Strict unknown profile/settings rejection.

Import Linter updates machine-check new files while preserving runtime/reference independence.

Target package metadata bump to `0.2.0` may occur here only if artifact verifier transition is included consistently; otherwise it is deferred atomically to `IS-13`. Codex must follow accepted repository state and not leave CI expecting nonexistent wheel version.

## Forbidden scope

- CLI smoke;
- CI rewrite beyond import/profile tests;
- plugin discovery/DI framework;
- Gym adapter.

## Tests

```text
tests/unit/test_interaction_profile.py
tests/integration/test_v0_2_composition_root.py
tests/architecture/test_v0_2_dependency_boundaries.py
```

Explicitly assert Policy/Perception constructors cannot reach research capability through composition objects.

## Obligations

- `V02-003` — composition isolation closed;
- `V02-009` — composition proof;
- `V02-016` — architecture/scope substantial.

---

# 16. `V0.2-IS-13 — CLI, clean artifact & CI profile`

## Цель

Сделать v0.2 runnable/installable vertical milestone и сформировать final `FULL-C0-v0.2`.

## Prerequisite

`IS-12 accepted`.

## Exact scope

Add:

```text
mindra interaction-smoke --profile configs/v0.2/reference.toml
validate-profile support for interaction-profile/v1
tools/verify_v0_2_artifact.py
final package version 0.2.0
GitHub Actions FULL-C0-v0.2 Ubuntu/Windows
```

`interaction-smoke`:

- uses Composition Root only;
- deterministic `MW0_DIRECT_REACH`;
- reaches success within fixed budget;
- concise output without hidden/research state.

`verify_v0_2_artifact.py` creates clean Python 3.14 environment and validates from built wheel:

- metadata `mindra-agent==0.2.0`;
- no runtime third-party Requires-Dist;
- v0.1 `validate-profile` + `kernel-smoke`;
- v0.2 `validate-profile` + `interaction-smoke`.

CI same matrix OS: Ubuntu/Windows.

## Forbidden scope

- new features/task families;
- release publication;
- GitHub Release/PyPI;
- performance benchmark claims.

## Tests

```text
tests/integration/test_v0_2_reference_profile.py
tests/integration/test_v0_2_cli.py
```

Run final `FULL-C0-v0.2`.

## Obligations

- `V02-001` — end-to-end closed;
- `V02-016` — regression scope;
- `V02-017` — local substantial, CI closure after remote evidence.

---

# 17. `V0.2-IS-14 — Version acceptance hardening`

## Цель

Не добавлять feature, а доказать fulfillment accepted design.

## Prerequisite

`IS-13 accepted`.

## Exact scope

1. Исправить только actual defects внутри accepted semantics.
2. Создать:

```text
docs/versions/v0.2/verification-matrix.md
```

с mapping:

```text
V02-001 … V02-017
→ concrete tests/commands
→ latest implementation evidence
→ Ubuntu/Windows CI evidence
```

3. Independently audit no-leakage/no-future-scope.
4. Verify v0.1 regression.
5. Verify `FULL-C0-v0.2` clean.
6. Verify clean wheel on declared CI OS.
7. Verify documentation/comments language policy.
8. Verify no runtime dependencies.

## Mandatory final gate

Exactly `FULL-C0-v0.2` from version README.

GitHub Actions evidence required for implementation candidate:

```text
Ubuntu Python 3.14 PASS
Windows Python 3.14 PASS
```

## Obligations

`V02-001 … V02-017` all explicit PASS.

## Important restriction

Codex **не** переводит самостоятельно `v0.2` в accepted historical milestone и не открывает `v0.3`.

Final acceptance — отдельный ChatGPT audit/update after remote evidence.

## Forbidden scope

Никаких new features/refactors/future version work.

---

# 18. VerificationObligation coverage

| Obligation | Main closing steps |
|---|---|
| `V02-001` trajectory determinism | `IS-04`, `IS-11`, `IS-13`, `IS-14` |
| `V02-002` snapshot continuation | `IS-04`, `IS-05`, `IS-14` |
| `V02-003` plane isolation | `IS-03 … IS-06`, `IS-12`, `IS-14` |
| `V02-004` session/episode lifecycle | `IS-01`, `IS-02`, `IS-11`, `IS-14` |
| `V02-005` decision multiplicity | `IS-01`, `IS-02`, `IS-11`, `IS-14` |
| `V02-006` outcome lineage | `IS-11`, `IS-14` |
| `V02-007` percept boundary | `IS-06`, `IS-14` |
| `V02-008` goal authority | `IS-07`, `IS-14` |
| `V02-009` policy isolation | `IS-08`, `IS-12`, `IS-14` |
| `V02-010` action separation | `IS-03`, `IS-08`, `IS-09`, `IS-14` |
| `V02-011` failure taxonomy | `IS-09`, `IS-11`, `IS-14` |
| `V02-012` no blind retry | `IS-09`, `IS-11`, `IS-14` |
| `V02-013` journal lineage | `IS-10`, `IS-11`, `IS-14` |
| `V02-014` annotation isolation | `IS-10`, `IS-14` |
| `V02-015` termination/reset | `IS-03`, `IS-04`, `IS-07`, `IS-11`, `IS-14` |
| `V02-016` scope/regression | every step, final `IS-14` |
| `V02-017` build/install/CI | `IS-13`, final `IS-14` |

---

# 19. Governance / CSPT

`CSPT-02` остаётся fully applicable.

Причина: все новые обязательные verification requirements задаются version-specific README/step sections, а `CSPT-02` уже требует:

- читать version design/sequence;
- выполнять targeted checks;
- выполнять полный current local regression profile;
- truthful CI status;
- structured VerificationObligation evidence;
- blocker on semantic ambiguity;
- no autonomous commit/push;
- no next-step opening.

Нового universal prompt-level rule нет, поэтому formal CSPT bump не требуется.

Каждый Codex prompt v0.2 обязан явно назвать current `FULL-C0-v0.2`/transitional regression requirement из текущего step.

---

# 20. Opening rule

После принятия design/sequence:

```text
V0.2-IS-01 → OPEN
V0.2-IS-02 … V0.2-IS-14 → CLOSED
```

Только `docs/design/current.md` хранит этот live status.

Следующий step открывается только после:

```text
implementation
→ operator commit/push
→ independent ChatGPT audit
→ acceptance
→ explicit MODE-TRANSITION
```
