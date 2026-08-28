# V0.1-IS-11 — Exact WaveExecutor & Scheduler clarification

## Статус

**Статус:** `accepted`  
**Область:** только `V0.1-IS-11 — WaveExecutor & Scheduler`  
**Baseline:** accepted `v0.1/README.md` + `implementation-sequence.md` + `is-06-contract-shape.md` + `is-07-execution-plan-shape.md` + `is-08-private-state-store-shape.md` + `is-09-commit-coordinator-shape.md` + `is-09-active-boundary-consistency-correction.md` + `is-10-evidence-plane-shape.md` + `F31`

Этот документ устраняет implementation-level неоднозначности deterministic cognitive-cycle execution перед реализацией `IS-11`.

Он не меняет F31, DAG semantics, CognitiveState semantics, commit atomicity или Evidence/Intervention separation. Он фиксирует exact runtime boundary, которая впервые соединяет compiled plan, module instances, same-base projections, private snapshots, `CommitCoordinator` и O0 Evidence.

При конфликте приоритет имеют F31/canonical design. В таком случае implementation останавливается с blocker report.

---

# 1. Граница шага

`IS-11` реализует ровно один deterministic scheduler segment:

```text
already identified Cognitive Cycle
        ↓
compiled ExecutionPlan
        ↓
wave 0
  same public base
  pinned own private snapshots
  module attempts
        ↓
atomic commit OR abort wave
        ↓
wave 1 ...
        ↓
cycle finished OR cycle failed
```

`IS-11`:

- выполняет только `ExecutionPhase.COGNITIVE_CYCLE`;
- создаёт per-wave/per-attempt runtime identities;
- формирует `StateProjection` и `ModuleComputeRequest`;
- выполняет module compute через `WaveExecutor`;
- превращает module exceptions в failed attempt records;
- вызывает существующий `CommitCoordinator` максимум один раз на successful wave;
- сохраняет earlier successful wave commits при later wave failure;
- пишет structural O0 events через уже существующий `EvidenceRecorder`;
- возвращает explicit cycle execution result с фактическим current public state.

`IS-11` не:

- компилирует новый execution plan;
- реализует Composition Root/profile parsing;
- реализует reference synthetic production modules (`IS-12`);
- реализует `KernelRuntime` facade (`IS-13`);
- реализует Intervention Gateway (`IS-14`);
- реализует Environment/Action/Outcome phases;
- реализует retries/recompute/degradation;
- вводит async/thread/process executor;
- меняет module-facing request contracts;
- добавляет O1/O2/O3 evidence.

---

# 2. Physical ownership и public runtime types

Предпочтительный split:

```text
src/mindra/runtime/executor.py
src/mindra/runtime/scheduler.py
```

Допустим эквивалентный split внутри `mindra.runtime`, если package-layer contracts не меняются.

Минимальный public runtime набор `IS-11`:

```text
ModuleAttemptExecutionRequest
ModuleAttemptRecord
WaveExecutor
SequentialWaveExecutor
CycleExecutionOutcome
CycleExecutionResult
CognitiveScheduler
```

`mindra.runtime.__init__` экспортирует эти supported runtime forms.

Evidence contracts из `mindra.contracts.evidence` не получают runtime module/store/service references.

---

# 3. Ownership temporal identities

`IS-11` различает outer lifecycle identity и identities внутреннего исполнения.

## 3.1. CognitiveCycleId

`CognitiveScheduler` **не создаёт `CognitiveCycleId`**.

Scheduler исполняет один уже идентифицированный cycle, переданный caller'ом как `cycle_time: LogicalTime`.

Exact требования к `cycle_time`:

```text
cycle_time.cognitive_cycle_id is not None
cycle_time.wave_id is None
```

Обычные `LogicalTime` hierarchy invariants требуют applicable `episode_id` и `decision_window_id` для cognitive cycle.

`CognitiveCycleId` создаётся owning lifecycle/runtime boundary через injected `IdFactory`. В `IS-13` этим caller станет `KernelRuntime.run_cycle()`; `IS-11` не реализует сам outer lifecycle facade.

Это разделение необходимо, потому что несколько Cognitive Cycle могут существовать внутри одного Decision Window и cycle identity не выводится из `StateRevision`.

## 3.2. Wave/attempt identities

Внутри одного `run_cycle()` Scheduler через injected `IdFactory` создаёт:

```text
WaveId         — один на plan wave в данном cycle
WaveAttemptId  — один attempt данной wave в v0.1
ModuleAttemptId — один на каждый actually dispatched module attempt
```

`v0.1` retries отсутствуют, поэтому на одну `WaveId` существует ровно одна `WaveAttemptId` в normal IS-11 path. Различие identities сохраняется для future retry semantics, но retry сейчас не реализуется.

`CommitId` по-прежнему создаёт только `CommitCoordinator` после его accepted validation/preconstruction pipeline.

---

# 4. Cycle temporal boundary и refinement IS-09

Предыдущий `is-09-commit-coordinator-shape.md` был принят **до lifecycle implementation** и в §6 запрещал менять already-set `cognitive_cycle_id` base state внутри commit, одновременно явно отмечая, что это не lifecycle/reset implementation.

`IS-11` впервые реализует переход:

```text
committed result Cycle N
        ↓
base snapshot Cycle N+1
```

Поэтому для `IS-11` и последующих runtime integration действует узкое refinement:

- `run_id` и `agent_session_id` commit time обязаны совпадать с base state;
- already-established `episode_id` и `decision_window_id` base state обязаны совпадать с current cycle/wave time;
- deeper outer scope может впервые появиться только по обычной `LogicalTime` hierarchy semantics;
- `cognitive_cycle_id` base state **не обязан совпадать** с `cognitive_cycle_id` нового commit time;
- новый commit относится к current `cycle_time`, а base state может быть committed результатом предыдущего cycle;
- `wave_id` является current-wave execution identity и также не выводится из base state.

Это refinement **supersedes только** equality requirement `cognitive_cycle_id` из `IS-09 §6`. Остальные IS-09 temporal/provenance/atomicity rules сохраняются.

Не создаётся фиктивный `CognitiveState` или новая `StateRevision` только ради смены cycle identity.

Ключевой invariant:

```text
new CognitiveCycleId
≠
automatic new StateRevision
```

Cycle, где нет public writes, может завершиться без изменения public `StateRevision`.

---

# 5. Projection logical time

`CURRENT_CYCLE` freshness должна оцениваться относительно **текущего исполняемого cycle**, а не обязательно относительно `base_state.envelope.logical_time`.

Поэтому `IS-11` узко расширяет runtime-controlled projection construction.

Conceptual API:

```text
build_state_projection(
    *,
    base_state: CognitiveState,
    read_specs: Iterable[ReadSpec[object]],
    logical_time: LogicalTime | None = None,
) -> StateProjection
```

Semantics:

- `logical_time=None` сохраняет прежнее поведение: используется `base_state.envelope.logical_time`;
- Scheduler всегда передаёт exact current `wave_time`;
- override меняет только freshness/read context projection;
- base entries и committed `CognitiveState` не копируются/переписываются как новая revision;
- run/session compatibility обязательна;
- already-set episode/decision base context не может silently измениться;
- different `cognitive_cycle_id` разрешён как current-cycle execution context согласно разделу 4.

`StateProjection` public/module-facing shape не меняется. Recorder/evidence capability в него не добавляется.

Это обеспечивает:

```text
Cycle N producer value
→ не считается CURRENT_CYCLE value в Cycle N+1

Cycle N+1 Wave 0 producer commit
→ Cycle N+1 later-wave consumer видит его как CURRENT_CYCLE
```

даже если previous/current cycle содержит private-only или no-op public commits.

---

# 6. Active runtime binding Scheduler

`CognitiveScheduler` создаётся только из already prepared active runtime components.

Conceptual constructor:

```text
CognitiveScheduler(
    *,
    plan: ExecutionPlan,
    modules: tuple[CognitiveModule, ...],
    private_store: PrivateStateStore,
    commit_coordinator: CommitCoordinator,
    wave_executor: WaveExecutor,
    evidence_recorder: EvidenceRecorder,
    id_factory: IdFactory,
)
```

Construction fail closed подтверждает до первого cycle:

1. `plan.phase == COGNITIVE_CYCLE`;
2. active module `ModuleId` unique;
3. module set точно совпадает с `plan.descriptors`;
4. `module.descriptor == corresponding plan descriptor` для каждого `ModuleId`;
5. нет missing/extra concrete module instance;
6. `PrivateStateStore` относится к тем же active descriptors;
7. `CommitCoordinator` относится к тем же active descriptors/schema и **к тому же concrete `PrivateStateStore` object**;
8. `wave_executor` структурно удовлетворяет `WaveExecutor`;
9. recorder/id factory имеют требуемые contracts.

Для пункта 7 допустимо добавить narrow internal runtime-only compatibility helper в `CommitCoordinator`. Он не является module-facing API и не даёт scheduler доступ к mutable private slots.

Причина object-identity проверки store:

```text
scheduler snapshots PrivateStateStore A
commit coordinator mutates PrivateStateStore B
```

не является допустимым active runtime, даже если descriptors временно одинаковы.

Registration/input order concrete modules не определяет execution order; scheduler хранит/использует mapping по `ModuleId`, а plan waves остаются source of scheduling order.

---

# 7. ModuleAttemptExecutionRequest

Frozen runtime request physical executor'у:

```text
ModuleAttemptExecutionRequest
├── module_id: ModuleId
├── module: CognitiveModule
└── compute_request: ModuleComputeRequest
```

Required consistency:

```text
module.descriptor.module_id == module_id
compute_request.context.module_attempt_id is valid ModuleAttemptId
compute_request.context.phase == COGNITIVE_CYCLE
```

Этот object является ephemeral runtime execution handle и **не является Evidence event**. `module` instance никогда не копируется в Evidence Plane.

---

# 8. ModuleAttemptRecord

Frozen runtime outcome physical executor:

```text
ModuleAttemptRecord
├── module_id: ModuleId
├── module_attempt_id: ModuleAttemptId
├── result: ModuleComputeResult | None
└── failure: TraceFailure | None
```

Invariant — exact XOR:

```text
success -> result is ModuleComputeResult and failure is None
failure -> result is None and failure is TraceFailure
```

Допустим derived property:

```text
outcome -> ModuleAttemptOutcome
```

Record содержит actual attempt identity из request, а не доверяет `state_update.module_attempt_id` returned result.

Proposal producer/attempt/base consistency остаётся responsibility `CommitCoordinator`; malformed staged result может быть compute-success, после чего fail closed на commit boundary. Это сохраняет важное различие:

```text
module compute succeeded
≠
proposal committed
```

---

# 9. WaveExecutor Protocol

Exact structural contract:

```text
class WaveExecutor(Protocol):
    def execute(
        self,
        attempts: tuple[ModuleAttemptExecutionRequest, ...],
        /,
    ) -> tuple[ModuleAttemptRecord, ...]: ...
```

Physical executor:

- не строит StateProjection;
- не читает `PrivateStateStore`;
- не вызывает `CommitCoordinator`;
- не создаёт IDs;
- не пишет Evidence;
- не выбирает dependency order;
- не знает plan waves кроме полученной collection;
- не прекращает semantic wave после первого normal module exception.

Scheduler обязан независимо валидировать executor output:

- ровно один record на каждый dispatched request;
- нет duplicate/extra/missing module или attempt identity;
- returned order не используется как semantic dependency;
- records canonicalize по plan wave/module order до дальнейших scheduler actions.

Executor contract violation → explicit wave/cycle failure, no commit.

---

# 10. SequentialWaveExecutor

Concrete `v0.1` executor выполняет attempts в input order.

Input order Scheduler формирует по canonical `ExecutionWave.module_ids`.

Для каждого attempt:

```text
call module.compute(compute_request)
```

Normal `Exception` из module compute:

- не прерывает execution оставшихся sibling attempts;
- копируется в `TraceFailure.from_exception()`;
- создаёт failed `ModuleAttemptRecord`;
- original exception/traceback не сохраняется в record/evidence.

`BaseException` (`KeyboardInterrupt`, `SystemExit` и process-control equivalents) не превращается в normal cognitive/module failure и не обязан перехватываться executor'ом.

Если `compute()` возвращает объект, не являющийся `ModuleComputeResult`, это считается failed module attempt с diagnostic `ModuleExecutionError`/эквивалентным typed runtime diagnostic, а не successful result.

Почему sequential executor продолжает siblings после failure:

> Модули wave семантически независимы по current-wave dataflow. Sequential physical order не должен создавать cancellation semantics, которой не было бы при parallel executor.

---

# 11. CycleExecutionResult

Вводится enum:

```text
CycleExecutionOutcome
├── SUCCEEDED = "succeeded"
└── FAILED    = "failed"
```

Frozen result:

```text
CycleExecutionResult
├── outcome: CycleExecutionOutcome
├── cycle_time: LogicalTime
├── base_state_revision: StateRevision
├── state: CognitiveState
├── completed_waves: int
└── failure: TraceFailure | None
```

Requirements:

```text
SUCCEEDED -> failure is None
FAILED    -> failure is TraceFailure
completed_waves >= 0
cycle_time.cognitive_cycle_id is not None
cycle_time.wave_id is None
```

`state` имеет критическую semantics:

> Это фактический current committed public state после всех wave commits, которые реально завершились до окончания cycle execution.

Поэтому при failure later wave earlier successful waves **не rollback'ятся** и `CycleExecutionResult.state` уже содержит их public commits.

`completed_waves` считает только waves, чей `CommitCoordinator.commit()` успешно завершился. Successful no-op/private-only wave также считается completed wave.

Private state хранится в том же injected `PrivateStateStore`; result его не exposes.

---

# 12. CognitiveScheduler cycle API

Conceptual API:

```text
run_cycle(
    *,
    current_state: CognitiveState,
    cycle_time: LogicalTime,
) -> CycleExecutionResult
```

Preflight каждого call:

- `current_state` — valid committed `CognitiveState`;
- state `schema_revision == plan.schema_revision`;
- state `composition_revision == plan.composition_revision`;
- `cycle_time` удовлетворяет разделу 3;
- run/session совместимы с current state;
- already-set episode/decision context не меняется;
- pin `cycle_base_revision = current_state.envelope.state_revision`;
- pin `cycle_agent_revision_id = current_state.envelope.agent_revision_id`.

Scheduler не мутирует входной `CognitiveState`.

Если plan не содержит waves, cycle всё равно имеет valid lifecycle:

```text
cycle_started
cycle_finished
```

и возвращает successful result с `completed_waves == 0` и unchanged public state.

---

# 13. Exact per-wave pipeline

Для каждой `ExecutionWave` строго по `wave.index`:

```text
1. pin base_state = current current_state
2. pin base_state_revision
3. assert agent_revision == cycle pinned revision
4. allocate WaveId
5. build wave_time from cycle_time + WaveId
6. allocate WaveAttemptId
7. for module_ids canonical by plan wave:
     allocate ModuleAttemptId
     capture own private snapshot BEFORE any compute
     build StateProjection(base_state, descriptor.reads, wave_time)
     build ModuleExecutionContext
     build ModuleComputeRequest
     build ModuleAttemptExecutionRequest
8. all requests/private snapshots are now pinned
9. record wave_started
10. record module_attempt_started for every dispatched request in canonical order
11. execute entire request collection through WaveExecutor
12. validate/canonicalize executor records
13. record module_attempt_finished for every record in canonical order
14. if any attempt failed:
      no commit call
      record cycle_failed
      return FAILED result with current_state unchanged for this wave
15. record commit_attempted
16. call CommitCoordinator exactly once with successful results in canonical module order
17. if commit call fails:
      record commit_failed
      record cycle_failed
      return FAILED result with pre-wave current_state
18. on commit success:
      set current_state = CommitResult.state
      record commit_succeeded
      if actual public revision advanced:
          record state_revision_committed
      increment completed_waves
19. continue next plan wave
```

После всех waves:

```text
record cycle_finished
return SUCCEEDED result
```

No separate hidden state publication path exists.

---

# 14. Same-base and private snapshot pinning

Для одной wave:

```text
all ModuleComputeRequest.context.base_state_revision
    == wave base StateRevision
```

Все `StateProjection` строятся из **одного exact `base_state` snapshot**.

Sibling proposals не добавляются в projection и не становятся visible до successful wave commit.

Private snapshot semantics:

- snapshot каждого active module берётся до вызова любого sibling compute этой wave;
- stateful module получает own `PrivateStateSnapshot`;
- stateless module получает `Unavailable`;
- peer private state не передаётся;
- successful sibling compute не меняет private store до common commit;
- failed wave оставляет current-wave private state unchanged.

Следующая wave получает public/private committed results предыдущей successful wave.

---

# 15. Agent revision pinning

`cycle_agent_revision_id` берётся из cycle-entry public state.

Для каждой wave Scheduler fail closed подтверждает:

```text
base_state.envelope.agent_revision_id == cycle_agent_revision_id
```

Successful `CommitCoordinator` result также обязан сохранять эту revision.

IS-11 не реализует Learning Update/Agent revision activation. Если revision неожиданно меняется внутри одного cycle, execution fails rather than silently continuing mixed-revision computation.

---

# 16. Exact O0 producer ownership

`IS-11` интегрирует только события, producer которых впервые существует в Scheduler path:

```text
cycle_started
wave_started
module_attempt_started
module_attempt_finished
commit_attempted
commit_succeeded
commit_failed
state_revision_committed
cycle_finished
cycle_failed
```

`IS-11` **не** emit'ит:

```text
composition_resolved
plan_compiled
intervention_applied
```

Их producers принадлежат последующим `IS-13/IS-14` boundaries.

`CommitCoordinator` сам по-прежнему не получает recorder и не начинает automatic emission. Scheduler instruments фактический commit call снаружи, что предотвращает duplicate evidence и сохраняет commit boundary independently reusable.

Scheduler не создаёт physical timestamps; `physical_timestamp_ns=None` для deterministic reference IS-11 path.

---

# 17. Logical O0 event order

Insertion order `EvidenceRecorder` является deterministic structural order, а не physical profiler order.

## 17.1. Cycle start/end

Cycle-scoped events используют exact `cycle_time` (`wave_id=None`).

```text
cycle_started
...
cycle_finished OR cycle_failed
```

`CycleStartedEvent`:

- base revision = cycle entry state revision;
- plan id/revision = active `ExecutionPlan`;
- agent revision = pinned cycle revision.

`CycleFinishedEvent`:

- base revision = cycle entry revision;
- resulting revision = final current public revision.

`CycleFailedEvent`:

- base revision = cycle entry revision;
- current revision = revision после all earlier successful waves;
- current failed wave не публикует partial state.

## 17.2. Wave start

`wave_started` записывается после полного preparation/pinning attempt requests, но до dispatch в executor.

`ModuleAttemptStartedEvent` означает **logical dispatch boundary**: attempt передан как часть фактически исполняемой wave collection. Это не wall-clock момент первой инструкции внутри `module.compute()`.

Все started events пишутся в canonical plan module order непосредственно перед `WaveExecutor.execute()`.

## 17.3. Attempt finish

Executor может физически завершать attempts в любом порядке в future implementation.

Scheduler после получения complete wave result collection:

- fail closed валидирует identities;
- canonicalize records по plan module order;
- пишет `module_attempt_finished` в том же canonical order.

Physical completion order не кодируется insertion order O0 trace. Future physical timestamps/profiler metadata могут существовать отдельно без изменения semantics.

## 17.4. Successful public wave

Exact logical sequence:

```text
wave_started
module_attempt_started...
module_attempt_finished(SUCCEEDED)...
commit_attempted
commit_succeeded
state_revision_committed
```

`state_revision_committed` существует только если public paths non-empty и revision реально advanced.

## 17.5. Private-only/no-op successful wave

```text
...
commit_attempted
commit_succeeded(public_paths=())
# no state_revision_committed
```

## 17.6. Module failure

```text
wave_started
module_attempt_started...
module_attempt_finished(... including FAILED ...)
# no commit_attempted
# no commit_succeeded/commit_failed
cycle_failed
```

Sequential executor всё равно завершает остальные normally dispatched sibling attempts.

## 17.7. Commit failure

```text
module_attempt_finished(SUCCEEDED)...
commit_attempted
commit_failed
cycle_failed
```

No `state_revision_committed`.

---

# 18. Event payload construction

Scheduler строит O0 payload только из structural copies.

## ModuleAttemptStartedEvent

- implementation identity/revision — exact active descriptor;
- base state revision — wave base;
- base private revision — pinned own private revision или `None` для stateless.

## ModuleAttemptFinishedEvent

Successful record:

- attempt identity — actual execution request identity;
- public paths — unique canonical sort `result.state_update.writes[*].key.path`;
- private update proposed — `result.private_state_update is not None`;
- failure = `None`.

Failed record:

- public paths = `()`;
- private update proposed = `False`;
- failure = record failure.

## CommitAttemptedEvent / CommitFailedEvent

Attempt IDs следуют canonical **scheduled module order**. На valid result path это совпадает с canonical producer order commit transaction.

## CommitSucceededEvent

Payload зеркалит successful `CommitRecord` structural fields. Runtime `PrivateStateRevisionTransition` преобразуется в evidence `PrivateRevisionTransitionTrace`; runtime record object не сохраняется в evidence.

## StateRevisionCommittedEvent

Использует resulting state envelope lineage/branch/agent revision и exact successful `CommitId`.

---

# 19. Failure semantics

## 19.1. Module compute failure

`SequentialWaveExecutor` ловит normal `Exception` одного module compute и продолжает siblings.

Если хотя бы один `ModuleAttemptRecord` failed:

- wave commit не вызывается;
- successful sibling proposals discarded;
- public/private current-wave state unchanged;
- cycle завершается `FAILED`;
- earlier successful waves остаются committed.

Если failed attempts несколько, для `CycleFailedEvent.failure` и `CycleExecutionResult.failure` используется deterministic summary по **первому failed module в canonical plan order**. Допустим diagnostic type `WaveExecutionError` с message, содержащим wave index, module id и copied underlying failure type/message.

Все individual failures уже присутствуют в `module_attempt_finished` events.

## 19.2. Executor contract failure

Missing/duplicate/extra/wrong attempt record является `WaveExecutionError`-class scheduler failure:

- no commit;
- cycle failed;
- current-wave state unchanged.

## 19.3. Commit failure

Если `CommitCoordinator.commit()` не возвращает successful `CommitResult` из-за normal `Exception`:

- Scheduler создаёт `TraceFailure.from_exception(error)`;
- emit `commit_failed`;
- emit `cycle_failed` с тем же diagnostic failure;
- возвращает failed cycle result;
- pre-wave public state остаётся current public state;
- private store остаётся unchanged согласно accepted atomic coordinator contract.

`BaseException`/process-control failure не обязана конвертироваться в recoverable cycle result.

## 19.4. Earlier-wave commits не rollback

Cycle-level failure не является transaction всей sequence waves.

```text
Wave 0 commit success
Wave 1 failure
```

означает:

```text
Wave 0 public/private effects remain committed
Wave 1 publishes nothing
CycleExecutionResult.state == state after Wave 0
CycleFailedEvent.current_state_revision == revision after Wave 0
```

Это следует canonical wave-by-wave commit semantics и уже поддерживается `CycleFailedEvent` contract.

---

# 20. Evidence recorder failure

Evidence Plane остаётся passive и не становится degradation policy.

`IS-11` не вводит best-effort/silent-drop/retry exporter semantics.

Если `EvidenceRecorder.record()` itself raises:

- scheduler не должен silently ignore failure;
- failure не превращается в alternative cognitive result/path;
- runtime continuation после такого infrastructure failure не является supported v0.1 path;
- exception может propagate как run/infrastructure-fatal condition.

Это соответствует `IS-10`: process/memory failure не маскируется silent drop. `IS-11` не создаёт второй recorder transaction layer.

---

# 21. Determinism и ordering

Semantic dependency order определяется только compiled plan.

Deterministic v0.1 rules:

- plan waves идут `0..N-1`;
- module preparation/ID allocation/dispatch O0 order внутри wave — `ExecutionWave.module_ids` canonical order;
- executor return order не определяет semantics;
- commit input successful results передаётся в canonical plan module order;
- finished O0 events canonicalized по plan module order;
- first failure summary выбирается canonical module order;
- no random scheduler tie-breakers;
- no wall-clock ordering;
- no registry/import order dependency.

`IdFactory` — единственный source wave/attempt identities Scheduler.

---

# 22. CommitCoordinator integration refinement

`IS-11` может минимально изменить `mindra.runtime.commit` только для двух integration needs:

1. temporal compatibility refinement раздела 4;
2. internal active-runtime binding assertion раздела 6.

Нельзя:

- менять commit transaction pipeline;
- переносить module execution внутрь coordinator;
- добавлять evidence recorder в coordinator;
- ослаблять owner/schema/provenance/private validation;
- добавлять retry/rebase;
- менять CommitId allocation semantics.

Regression tests обязаны доказать, что ordinary IS-09 atomicity сохраняется.

---

# 23. Required tests

Минимальные files из sequence:

```text
tests/integration/test_scheduler_wave_semantics.py
tests/property/test_same_base_wave.py
tests/integration/test_wave_failure_atomicity.py
tests/integration/test_scheduler_trace.py
```

Допустим отдельный focused unit test `SequentialWaveExecutor`, если это улучшает coverage без выхода за scope.

Обязательно проверить минимум:

1. scheduler construction exact plan/module descriptor binding;
2. missing/extra/duplicate module instance reject;
3. scheduler/coordinator different PrivateStateStore object reject;
4. plan/current-state schema revision mismatch reject;
5. plan/current-state composition revision mismatch reject;
6. invalid cycle_time: missing cycle id или existing wave id reject;
7. incompatible run/session/episode/decision context reject;
8. transition previous cycle -> new cycle не создаёт fake public revision;
9. first wave new cycle может commit с new cognitive_cycle provenance;
10. projection CURRENT_CYCLE использует supplied wave_time, а не stale base envelope time;
11. current-cycle producer earlier wave становится readable later wave;
12. previous-cycle value не проходит CURRENT_CYCLE before current producer commit;
13. same wave attempts получают exact same public base revision/object contents;
14. sibling proposal не виден sibling attempt;
15. all own private snapshots pinned before any wave compute;
16. stateful modules получают own private snapshot; stateless — `Unavailable`;
17. sequential executor продолжает sibling attempts после one normal exception;
18. module exception -> failed attempt record/evidence, no commit;
19. successful sibling proposal discarded on one failed attempt;
20. failed wave leaves current-wave public/private state unchanged;
21. earlier successful wave remains committed if later wave fails;
22. successful wave calls coordinator exactly once;
23. next wave sees previous wave committed public/private state;
24. executor output missing/duplicate/extra record fail closed, no commit;
25. successful public wave event sequence exact;
26. private-only/no-op success has no `state_revision_committed`;
27. module failure has no `commit_attempted`;
28. commit failure has `commit_attempted -> commit_failed`, no state transition event;
29. cycle finished base/result revisions correct;
30. cycle failed current revision includes earlier successful waves;
31. started/finished O0 events deterministic canonical module order;
32. `CommitSucceededEvent` mirrors actual `CommitRecord` structural data;
33. private transitions copied, runtime record refs not stored in evidence;
34. scheduler does not emit `composition_resolved`, `plan_compiled`, `intervention_applied`;
35. no recorder/evidence capability leaks into `ModuleComputeRequest`/`StateProjection`;
36. registration/module tuple order does not change execution/evidence ordering;
37. two distinct successful cycles with no public transition still have distinct caller-provided cycle identities and no fake `StateRevision`;
38. IS-09 public/private atomic commit regression remains green.

Tests используют test-only modules/fixtures. Production reference graph из `IS-12` не реализуется заранее.

---

# 24. VerificationObligations

После accepted `IS-11`:

- `V01-001` — closed: same-base wave execution mechanically enforced;
- `V01-002` — closed at runtime wave level;
- `V01-008` — runtime closed: private snapshot/commit integration exercised end-to-end at wave level;
- `V01-009` — substantial: runtime cycle/wave/module/commit/state O0 emission существует; composition/intervention producers остаются future steps;
- `V01-010` — closed: evidence/cognition isolation подтверждена при real scheduler emission.

Не объявлять `V01-009` полностью closed до предусмотренной дальнейшей producer integration.

---

# 25. Verification

Targeted profile:

```text
FAST + ARCH
```

Минимум targeted pytest:

```text
tests/integration/test_scheduler_wave_semantics.py
tests/property/test_same_base_wave.py
tests/integration/test_wave_failure_atomicity.py
tests/integration/test_scheduler_trace.py
```

Плюс все новые focused scheduler/executor tests, если созданы.

После targeted green обязателен полный existing `FULL-C0`:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked lint-imports
uv run --locked pytest
uv build
```

`git diff --check` выполнить и отразить в report.

---

# 26. Forbidden scope

Не реализовывать в `IS-11`:

- `mindra.reference` production synthetic modules;
- configuration/TOML/profile schema;
- ImplementationRegistry;
- CompositionRoot;
- KernelRuntime facade;
- automatic `composition_resolved`/`plan_compiled` emission;
- InterventionGateway/intervention mutation;
- Environment ingress/action/outcome phases;
- retry/recompute/rebase;
- optional/skippable/degradation/fallback policy;
- cancellation semantics, требующую новый attempt outcome;
- asyncio/thread/process/distributed executor;
- resource scheduler;
- learning/Agent revision activation;
- RNG contract expansion;
- O1/O2/O3 evidence;
- logger/exporter/network/filesystem telemetry;
- global event bus/subscriber API;
- Service Locator;
- mutable global module registry;
- new cognitive state fields ради scheduler/evidence;
- новый semantic identity type без отдельного accepted need.

Следующий implementation step остаётся `V0.1-IS-12 — Reference synthetic modules` и открывается только после independent audit/acceptance `IS-11`.