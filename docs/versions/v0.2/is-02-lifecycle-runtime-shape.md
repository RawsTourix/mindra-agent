# V0.2-IS-02 — Lifecycle Runtime Shape

## Статус

**Статус:** `accepted step-specific clarification`  
**Этап:** `V0.2-IS-02 — Lifecycle phases & KernelRuntime context bridge`  
**Semantic baseline:** `F31`  
**Version design:** `docs/versions/v0.2/README.md` — accepted  
**Implementation sequence:** `docs/versions/v0.2/implementation-sequence.md` — accepted  
**Входной implementation baseline:** `5ddc0daff12536e080c9fd1bc50476464109a455` — accepted `V0.2-IS-01`

Этот документ снимает implementation ambiguity текущего step. Он не меняет F31, canonical DU/ADR, version scope или порядок implementation sequence.

---

# 1. Причина clarification

Accepted `IS-02` требует одновременно:

- новых lifecycle phases;
- phase-specific plans;
- отдельного `LifecycleCoordinator`;
- reuse `WaveExecutor` и atomic module commit semantics;
- context-aware `KernelRuntime`;
- сохранения `CognitiveScheduler` как `COGNITIVE_CYCLE`-only;
- блокировки intervention во время in-flight kernel execution.

Accepted v0.1 implementation при этом жёстко предполагает `COGNITIVE_CYCLE` в `ExecutionPhase`, `ExecutionPlanCompiler`, `ModuleAttemptExecutionRequest`, `CommitCoordinator` binding и O0 trace scoping.

Чтобы Codex не выбирал самостоятельно generic scheduler/event architecture, `IS-02` реализует только additive shape ниже.

---

# 2. ExecutionPhase

Canonical supported phases после `IS-02`:

```text
COGNITIVE_CYCLE
EPISODE_START
POST_OUTCOME
```

`ModuleDescriptor.phases` остаётся non-empty `frozenset[ExecutionPhase]` и может содержать любое непустое подмножество этих phases.

Один и тот же `CognitiveModule.compute()` используется во всех phases. Giant hook interface вида `on_episode_start()/on_outcome()/...` не вводится.

Текущая phase передаётся только через:

```text
ModuleExecutionContext.phase
```

Модуль не получает scheduler/coordinator/runtime facade.

---

# 3. DecisionContext

Добавить отдельный frozen temporal input contract:

```text
DecisionContext
├── RunId
├── AgentSessionId
├── EpisodeId
└── DecisionWindowId
```

Exact Python shape:

```python
@dataclass(frozen=True, slots=True)
class DecisionContext:
    run_id: RunId
    agent_session_id: AgentSessionId
    episode_id: EpisodeId
    decision_window_id: DecisionWindowId
```

Все четыре identities обязательны.

`DecisionContext` намеренно не содержит:

```text
CognitiveCycleId
WaveId
EnvironmentTransitionId
OutcomeId
```

Caller не получает права назначать `CognitiveCycleId`.

Runtime может преобразовать `DecisionContext` в `LogicalTime` с:

```text
cognitive_cycle_id = None
wave_id = None
```

через небольшой contract/runtime helper либо explicit construction. Отдельный generic temporal framework не нужен.

---

# 4. LogicalTime и lifecycle waves

Для `LifecycleCoordinator` internal execution wave должна быть causally representable без fake `CognitiveCycleId`.

После `IS-02` hierarchy rule:

```text
DecisionWindowId requires EpisodeId
CognitiveCycleId requires DecisionWindowId
WaveId requires DecisionWindowId
```

То есть `WaveId` может принадлежать:

1. wave внутри `COGNITIVE_CYCLE`, где одновременно задан `CognitiveCycleId`;
2. wave внутри `EPISODE_START` / `POST_OUTCOME`, где `CognitiveCycleId = None`.

Запрещено создавать lifecycle wave через synthetic/fake `CognitiveCycleId` только ради прохождения старого validator.

Cycle-level events по-прежнему требуют настоящий `CognitiveCycleId`.

Это additive temporal refinement только для standardized kernel lifecycle execution; Environment transition не становится scheduler wave.

---

# 5. Phase-specific ExecutionPlanCompiler

Existing API расширяется additive keyword parameter:

```text
ExecutionPlanCompiler.compile(..., phase=ExecutionPhase.COGNITIVE_CYCLE)
```

Default обязателен для backward compatibility существующих callers/tests.

Compiler получает полный active descriptor set и для requested phase выбирает только descriptors, где:

```text
phase in descriptor.phases
```

`ExecutionPlan.descriptors` содержит только participants данного phase.

Plan fingerprint обязательно включает requested `phase`; одинаковые descriptors/dependencies/waves разных phases не имеют права давать одинаковый semantic plan fingerprint только из-за совпадения остальных fields.

`PlanCompiledEvent.phase` принимает все три supported phases.

## 5.1. Dependency semantics

Для `COGNITIVE_CYCLE` сохраняется existing rule:

```text
required CURRENT_CYCLE read
→ active same-cycle producer required
→ dependency edge
```

Для `EPISODE_START` и `POST_OUTCOME`:

- `CURRENT_CYCLE` read запрещён как semantic mismatch;
- `CURRENT_DECISION_WINDOW` и `CURRENT_EPISODE` проверяются projection/freshness layer;
- они не создают same-phase module edge сами по себе.

`CURRENT_PHASE`/`CURRENT_LIFECYCLE_PHASE` freshness vocabulary в `IS-02` не вводится.

Следствие для reference `v0.2`: lifecycle phases пока могут состоять из независимых participants одной wave; более сложная same-phase chaining semantics deferred, если она когда-либо реально понадобится.

## 5.2. Empty non-cycle phase

Explicit compile `EPISODE_START`/`POST_OUTCOME` без participants допускает valid zero-wave `ExecutionPlan`.

Это выражает «ни один active module не участвует в этой standardized phase», а не configuration error.

Normal v0.1 root не обязан компилировать/record такие планы до v0.2 Composition Root step.

---

# 6. Phase-aware module commit

`CommitCoordinator` остаётся единственной module-owned commit authority и не становится runtime-boundary writer.

Его existing commit API расширяется additive phase context, conceptually:

```text
commit(..., phase=ExecutionPhase.COGNITIVE_CYCLE)
```

Default сохраняет v0.1 callers.

При commit каждый producer обязан:

- быть зарегистрирован в active composition;
- участвовать именно в переданной `phase`;
- иметь existing write authority;
- удовлетворять existing public/private atomic validation.

`StateUpdateProposal` не получает отдельное mutable/global phase поле: authoritative phase задаётся execution coordinator и уже присутствует в `ModuleExecutionContext` attempt.

Lifecycle result binding обязан доказать, что returned proposal относится к dispatched module/attempt так же строго, как existing cognitive scheduler.

---

# 7. Composition-wide store/coordinator и phase subsets

`PrivateStateStore` и `CommitCoordinator` принадлежат полной active Agent composition.

Phase-specific plan может содержать subset active modules.

Поэтому runtime binding после `IS-02` должен различать:

```text
active composition descriptors
≠
participants одного phase plan
```

Допустимый binding invariant:

- `PrivateStateStore` содержит полный active descriptor set;
- `CommitCoordinator` содержит полный active descriptor set;
- phase plan descriptors являются exact subset этих descriptors;
- этот subset должен равняться всем active descriptors, объявившим requested phase;
- concrete modules, переданные конкретному scheduler/coordinator, должны exactly соответствовать descriptors его plan;
- schema/composition revisions должны совпадать.

Нельзя ослабить binding до «похожий ModuleId где-то существует».

Existing v0.1 composition, где все reference modules участвуют в `COGNITIVE_CYCLE`, должна давать тот же cycle plan и тот же runtime behavior.

---

# 8. CognitiveScheduler

`CognitiveScheduler` остаётся строго:

```text
ExecutionPhase.COGNITIVE_CYCLE only
```

Он не превращается в generic phase scheduler и обязан продолжать reject non-cycle `ExecutionPlan`.

Ему разрешено получить только concrete modules, входящие в его cycle plan, при том что shared `PrivateStateStore`/`CommitCoordinator` могут знать дополнительные lifecycle-only modules будущей v0.2 composition.

Existing cycle semantics не меняются:

- same-base wave;
- atomic commit;
- previous successful waves остаются committed при failure более поздней wave;
- O0 cycle evidence;
- caller не назначает `CognitiveCycleId` через `run_cycle_in`.

---

# 9. LifecycleCoordinator

Добавить отдельный runtime component:

```text
LifecycleCoordinator
```

Один instance исполняет один compiled non-cycle `ExecutionPlan`.

Constructor принимает минимум:

```text
plan
exact concrete participant modules
composition-wide PrivateStateStore
composition-wide CommitCoordinator
WaveExecutor
EvidenceRecorder
IdFactory
```

Он обязан reject:

```text
COGNITIVE_CYCLE plan
```

и принимать только:

```text
EPISODE_START
POST_OUTCOME
```

## 9.1. Execution algorithm

Для каждой plan wave:

1. pin current public base revision и AgentRevision;
2. создать `WaveId` и `WaveAttemptId`;
3. получить own private snapshots только participant modules;
4. построить `StateProjection` из declared reads;
5. создать `ModuleExecutionContext` с exact lifecycle `phase`;
6. выполнить attempts через existing `WaveExecutor`;
7. fail closed на executor/result-binding/module failure;
8. вызвать phase-aware `CommitCoordinator` один раз для successful wave;
9. следующая wave, если она существует, видит committed предыдущую;
10. partial current-wave publication запрещена.

`LifecycleCoordinator` не вызывает:

```text
Environment.reset
Environment.step/apply_committed_action
Dispatcher
ActionBoundary
InteractionRuntime
InterventionGateway
```

## 9.2. Result

Добавить frozen result/outcome contract, conceptually:

```text
LifecycleExecutionOutcome { SUCCEEDED, FAILED }

LifecycleExecutionResult
├── outcome
├── phase
├── phase_time
├── base_state_revision
├── state
├── completed_waves
└── failure | None
```

`phase_time`:

- содержит Run/Session/Episode/Decision identities;
- не содержит `CognitiveCycleId`;
- не содержит `WaveId`.

Failure semantics совпадает с cycle segment:

- текущая failed wave ничего не публикует;
- commits предыдущих completed waves не откатываются задним числом.

---

# 10. O0 evidence lifecycle phase

Добавить typed lifecycle phase events минимум:

```text
LifecyclePhaseStartedEvent
LifecyclePhaseFinishedEvent
LifecyclePhaseFailedEvent
```

и соответствующие `TraceEventKind`.

Phase-start payload содержит минимум:

```text
phase
base_state_revision
plan_id
plan_revision
agent_revision_id
```

Finished:

```text
phase
base_state_revision
resulting_state_revision
```

Failed:

```text
phase
base_state_revision
current_state_revision
failure
```

Эти phase events записываются с `phase_time` без `CognitiveCycleId`/`WaveId`.

Для internal lifecycle waves переиспользуются существующие structural O0 variants:

```text
WaveStartedEvent
ModuleAttemptStartedEvent
ModuleAttemptFinishedEvent
CommitAttemptedEvent
CommitSucceededEvent
CommitFailedEvent
StateRevisionCommittedEvent
```

Они записываются с lifecycle `wave_time`:

```text
DecisionContext identities
CognitiveCycleId = None
WaveId = current lifecycle wave id
```

`CycleStarted/Finished/FailedEvent` для lifecycle phase не используются.

Trace metadata не становится cognitive input.

---

# 11. KernelRuntime context bridge

Добавить public additive API:

```text
KernelRuntime.run_cycle_in(context: DecisionContext) -> CycleExecutionResult
```

Semantics:

1. caller задаёт только `DecisionContext`;
2. `run_id` и `agent_session_id` обязаны совпадать с runtime root/session;
3. current committed state должен быть совместим с exact `EpisodeId`/`DecisionWindowId` context;
4. KernelRuntime сам создаёт новый `CognitiveCycleId` через injected `IdFactory`;
5. каждый вызов `run_cycle_in()` создаёт новый `CognitiveCycleId`, даже внутри того же Decision Window;
6. `CognitiveScheduler.run_cycle()` получает normal cycle `LogicalTime`;
7. current state обновляется фактическим result state.

Caller не может передать готовый `CognitiveCycleId`.

Existing:

```text
KernelRuntime.run_cycle()
```

остаётся без аргументов и сохраняет behavior historical v0.1 reference profile.

Допускается общий private helper внутри `KernelRuntime`, если public behavior обоих путей остаётся однозначным.

---

# 12. KernelRuntime lifecycle facade

Добавить additive public API conceptually:

```text
KernelRuntime.run_lifecycle(
    phase: ExecutionPhase,
    context: DecisionContext,
) -> LifecycleExecutionResult
```

Допустимы только:

```text
EPISODE_START
POST_OUTCOME
```

`COGNITIVE_CYCLE` выполняется только через `run_cycle()` / `run_cycle_in()`.

KernelRuntime может хранить immutable mapping:

```text
ExecutionPhase -> LifecycleCoordinator
```

Для phase, coordinator которой не wired в текущей composition, вызов fail-closed с typed composition/runtime error; hidden no-op не выполняется.

Historical v0.1 `CompositionRoot` в `IS-02` не обязан создавать lifecycle plans/coordinators и не должен добавлять новые lifecycle plan events в canonical v0.1 evidence только ради наличия API.

Фактическое production wiring v0.2 lifecycle plans выполняется в dependency-ordered v0.2 Composition Root step.

---

# 13. Intervention safe-boundary guard

Existing `KernelRuntime.apply_intervention()` обязан reject intervention, если в данный момент исполняется:

```text
cognitive cycle
ИЛИ
lifecycle phase
```

Можно сохранить отдельные internal flags:

```text
_cycle_active
_lifecycle_active
```

либо эквивалентную private execution-state representation, если она не вводит generic state machine следующего step.

Existing between-cycle intervention semantics v0.1 сохраняется.

Interaction-specific lock:

```text
после Action Commit
→ до resolution/outcome
```

не реализуется здесь и остаётся `IS-11` scope.

---

# 14. Scope/reset semantics в IS-02

`IS-02` создаёт standardized phase execution mechanism, но не создаёт универсальный scope-expiration/reset engine.

В частности, сейчас запрещено заранее реализовывать:

- Environment episode reset;
- generic clearing episode/decision fields;
- Goal lifecycle logic;
- post-outcome Memory/Drive/Appraisal logic;
- Action/Outcome Commit;
- InteractionRuntime episode state machine.

Будущие modules будут выполнять свои accepted lifecycle transitions через этот phase mechanism.

---

# 15. Required verification additions

Минимум доказать tests:

## Phase/contracts/compiler

- `ExecutionPhase` содержит exact 3 values;
- `ModuleDescriptor` принимает mixed phase declarations;
- compiler default остаётся `COGNITIVE_CYCLE`;
- requested phase выбирает только declared participants;
- plan phase/fingerprint phase-sensitive;
- non-cycle `CURRENT_CYCLE` read rejected;
- explicit empty non-cycle phase даёт valid zero-wave plan;
- `PlanCompiledEvent` принимает non-cycle phase.

## Executor/commit binding

- `WaveExecutor` исполняет request для exact declared lifecycle phase;
- request phase, которой module не участвует, rejected;
- phase-aware commit rejects producer, не объявивший current phase;
- phase-plan subset не ослабляет composition-wide private/commit binding;
- module public/private atomicity сохраняется.

## LifecycleCoordinator

- rejects `COGNITIVE_CYCLE` plan;
- executes only exact plan participants;
- same-base semantics внутри wave;
- required attempt failure публикует zero effects текущей wave;
- successful commit обновляет state/private state как normal module commit;
- lifecycle phase evidence содержит start/wave/module/commit/finish;
- failed phase содержит explicit failure event, а не fake CycleFailedEvent;
- Environment/Dispatcher API отсутствует из coordinator dependencies.

## KernelRuntime

- два `run_cycle_in()` одного `DecisionContext` создают разные `CognitiveCycleId`;
- caller не передаёт cycle identity;
- wrong RunId/AgentSessionId/EpisodeId/DecisionWindowId fail closed;
- historical no-arg `run_cycle()` regression unchanged;
- `CognitiveScheduler` по-прежнему rejects lifecycle plan;
- `run_lifecycle()` rejects `COGNITIVE_CYCLE` и unwired phase;
- intervention guard учитывает active cycle и active lifecycle execution.

---

# 16. Forbidden architecture choices

В `IS-02` запрещено:

- превращать `CognitiveScheduler` в generic all-phase scheduler;
- добавлять Environment calls в scheduler/coordinator;
- создавать global event bus;
- вводить generic hook registry;
- создавать fake CognitiveCycleId для lifecycle phase;
- вводить `CURRENT_PHASE` freshness без отдельного design;
- реализовывать generic scope-reset framework;
- wiring v0.2 Environment/Goal/Policy/Action/Journal;
- менять v0.1 CLI/config/package metadata;
- реализовывать `InteractionRuntime`;
- реализовывать post-Action-Commit interaction lock раньше `IS-11`.

---

# 17. Acceptance interpretation

`V0.2-IS-02` можно принять, если после implementation доказано:

```text
EPISODE_START / POST_OUTCOME
→ standardized module DAG execution boundary существует
→ Environment orchestration в нём отсутствует

DecisionContext
→ caller задаёт Episode/Decision scope
→ KernelRuntime остаётся owner CognitiveCycleId

CognitiveScheduler
→ остаётся COGNITIVE_CYCLE-only

module commit authority
→ одна composition-wide authority
→ phase-aware
→ не ослаблена

intervention
→ запрещена во время in-flight cycle/lifecycle execution

v0.1 run_cycle / profile / tests / artifact
→ regression-compatible
```

Этот clarification является обязательным source для Codex при реализации `V0.2-IS-02`.