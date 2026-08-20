# V0.1-IS-10 — Exact O0 Evidence Plane clarification

## Статус

**Статус:** `accepted`  
**Область:** только `V0.1-IS-10 — O0 Evidence Plane`  
**Baseline:** accepted `v0.1/README.md` + `implementation-sequence.md` + `F31` + `ADR-0003` + `ADR-0006`

Этот документ устраняет implementation-level неоднозначности structural O0 trace перед реализацией `IS-10`.

Он не меняет F31, scheduler/commit semantics или Intervention semantics. Он фиксирует exact immutable evidence contracts и минимальный process-local recorder, на которые позднее будут опираться `IS-11`, `IS-13` и `IS-14`.

При конфликте приоритет имеют canonical design/F31, и implementation останавливается с blocker report.

---

# 1. Граница шага

`IS-10` создаёт passive structural Evidence Plane foundation:

```text
producer-owned runtime fact
        ↓ immutable structural copy
TraceEventEnvelope
        ↓
EvidenceRecorder
        ↓
InMemoryEvidenceRecorder
```

На этом шаге реализуются **контракты событий и recorder**, но не producer integration.

То есть `IS-10` не должен добавлять emit-вызовы в:

- `ExecutionPlanCompiler`;
- `CommitCoordinator`;
- будущий Scheduler/WaveExecutor;
- Composition Root;
- Intervention Gateway.

Emit integration появляется в соответствующих следующих implementation steps.

Это важно для scope discipline: passive evidence schema может быть проверена независимо от ещё не существующих producers.

---

# 2. Physical ownership и dependency direction

Предпочтительный split:

```text
src/mindra/contracts/evidence.py
src/mindra/runtime/evidence.py
```

`mindra.contracts.evidence` содержит только immutable semantic/structural evidence value objects и `EvidenceRecorder` Protocol.

`mindra.runtime.evidence` содержит `InMemoryEvidenceRecorder`.

Dependency direction:

```text
mindra.runtime.evidence
        ↓
mindra.contracts.evidence
```

`contracts` не импортирует `runtime`.

Evidence contracts не должны хранить runtime service objects (`CognitiveState`, `PrivateStateStore`, `CommitCoordinator`, module instances, registry, Composition Root).

`mindra.contracts.__init__` экспортирует public evidence contracts.

`mindra.runtime.__init__` экспортирует только concrete runtime recorder `InMemoryEvidenceRecorder`; internal backing collection не экспортируется.

---

# 3. TraceEventKind

Вводится enum exact event kinds `v0.1`:

```text
TraceEventKind
├── COMPOSITION_RESOLVED      = "composition_resolved"
├── PLAN_COMPILED             = "plan_compiled"
├── CYCLE_STARTED             = "cycle_started"
├── WAVE_STARTED              = "wave_started"
├── MODULE_ATTEMPT_STARTED    = "module_attempt_started"
├── MODULE_ATTEMPT_FINISHED   = "module_attempt_finished"
├── COMMIT_ATTEMPTED          = "commit_attempted"
├── COMMIT_SUCCEEDED          = "commit_succeeded"
├── COMMIT_FAILED             = "commit_failed"
├── STATE_REVISION_COMMITTED  = "state_revision_committed"
├── INTERVENTION_APPLIED      = "intervention_applied"
├── CYCLE_FINISHED            = "cycle_finished"
└── CYCLE_FAILED              = "cycle_failed"
```

Kind не хранится как свободная строка рядом с arbitrary payload.

Каждый typed payload variant имеет однозначный `TraceEventKind`; envelope предоставляет derived `kind` property.

Таким образом невозможно создать record вида:

```text
kind = commit_succeeded
payload = CycleFailedEvent(...)
```

без test-only обхода type system/internal construction.

`TraceEventId` в `v0.1` не вводится: accepted identity set его не требует. Causal correlation выполняется существующими typed identities + `LogicalTime`, а process-local recording order сохраняется recorder snapshot.

---

# 4. TraceEventEnvelope

Exact envelope:

```text
TraceEventEnvelope
├── logical_time: LogicalTime
├── payload: TraceEventPayload
└── physical_timestamp_ns: int | None
```

Envelope — frozen dataclass.

`physical_timestamp_ns`:

- optional;
- если задан, является неотрицательным integer diagnostic wall-clock/physical timestamp;
- не является `LogicalTime`;
- не участвует в state revisions, freshness, plan ordering или scheduling semantics;
- `InMemoryEvidenceRecorder` **не вызывает clock самостоятельно** и не дописывает timestamp;
- reference deterministic tests/profile могут оставлять его `None`.

`run_id`/`agent_session_id` берутся из `LogicalTime` и не дублируются отдельными envelope fields.

Не каждый event обязан физически повторять все causal identities, если они уже однозначно присутствуют в `LogicalTime` или typed payload.

Temporal depth validation:

- `cycle_started/cycle_finished/cycle_failed` требуют non-`None` `cognitive_cycle_id`;
- `wave_started/module_attempt_*/commit_*` требуют non-`None` `wave_id`;
- composition/plan/intervention/state-revision events могут существовать без wave scope;
- обычные hierarchy invariants остаются ответственностью `LogicalTime`.

---

# 5. Общие structural helper records

Все helper records — frozen dataclasses и содержат только snapshot-safe structural values.

## 5.1. TraceFailure

```text
TraceFailure
├── error_type: str
└── message: str
```

Оба поля — непустые printable strings.

Допустим convenience constructor `from_exception(error: BaseException)`, который копирует только diagnostic type/name/text и **не хранит exception object/traceback reference**.

`TraceFailure` является evidence data, а не новой kernel exception taxonomy.

## 5.2. ResolvedModuleTrace

```text
ResolvedModuleTrace
├── module_id: ModuleId
├── implementation_id: ImplementationId
├── implementation_revision: ImplementationRevision
├── statefulness: ModuleStatefulness
└── determinism: DeterminismMode
```

Он намеренно не содержит `ModuleDescriptor`/private contract object/settings object.

## 5.3. PlanDependencyTrace

```text
PlanDependencyTrace
├── producer: ModuleId
├── consumer: ModuleId
└── path: StatePath
```

## 5.4. PlanWaveTrace

```text
PlanWaveTrace
├── index: int
└── module_ids: tuple[ModuleId, ...]
```

`index >= 0`; `module_ids` non-empty, unique, canonical by `ModuleId.value`.

## 5.5. PrivateRevisionTransitionTrace

```text
PrivateRevisionTransitionTrace
├── module_id: ModuleId
├── before: PrivateStateRevision
└── after: PrivateStateRevision
```

Invariant:

```text
after == before.next()
```

Этот record является evidence representation и не импортирует runtime `PrivateStateRevisionTransition`.

---

# 6. Module attempt outcome

Вводится enum:

```text
ModuleAttemptOutcome
├── SUCCEEDED = "succeeded"
└── FAILED    = "failed"
```

`IS-10` не вводит retry/cancel/degraded policy.

Если будущий scheduler не запускает attempt из-за более раннего failure, он не должен фабриковать `module_attempt_finished` без соответствующего `module_attempt_started` только ради заполнения trace.

Расширение outcome taxonomy возможно только при реальной runtime semantics последующих versions.

---

# 7. Exact payload variants

Все payload classes — frozen dataclasses.

Типовой alias:

```text
TraceEventPayload =
    CompositionResolvedEvent
  | PlanCompiledEvent
  | CycleStartedEvent
  | WaveStartedEvent
  | ModuleAttemptStartedEvent
  | ModuleAttemptFinishedEvent
  | CommitAttemptedEvent
  | CommitSucceededEvent
  | CommitFailedEvent
  | StateRevisionCommittedEvent
  | InterventionAppliedEvent
  | CycleFinishedEvent
  | CycleFailedEvent
```

## 7.1. CompositionResolvedEvent

```text
CompositionResolvedEvent
├── profile_id: ProfileId
├── composition_revision: CompositionRevision
├── schema_revision: SchemaRevision
├── agent_revision_id: AgentRevisionId
├── composition_fingerprint: str
└── modules: tuple[ResolvedModuleTrace, ...]
```

Requirements:

- fingerprint — lowercase 64-character SHA-256 hex;
- modules unique/canonical by `module_id.value`;
- event содержит structural composition evidence, а не runtime module references или raw settings.

Producer появляется в `IS-13`; `IS-10` только создаёт contract.

## 7.2. PlanCompiledEvent

```text
PlanCompiledEvent
├── plan_id: ExecutionPlanId
├── plan_revision: ExecutionPlanRevision
├── composition_revision: CompositionRevision
├── schema_revision: SchemaRevision
├── phase: ExecutionPhase
├── plan_fingerprint: str
├── dependencies: tuple[PlanDependencyTrace, ...]
└── waves: tuple[PlanWaveTrace, ...]
```

Requirements:

- `phase == COGNITIVE_CYCLE` для `v0.1`;
- fingerprint — lowercase SHA-256 hex;
- dependencies имеют deterministic canonical ordering `(producer.value, consumer.value, path.dotted)`;
- wave indices идут `0..N-1` без gaps;
- каждый module встречается максимум в одной wave.

Producer integration **не добавляется** в `ExecutionPlanCompiler` на IS-10.

## 7.3. CycleStartedEvent

```text
CycleStartedEvent
├── base_state_revision: StateRevision
├── plan_id: ExecutionPlanId
├── plan_revision: ExecutionPlanRevision
└── agent_revision_id: AgentRevisionId
```

Envelope обязан иметь `cognitive_cycle_id`.

## 7.4. WaveStartedEvent

```text
WaveStartedEvent
├── wave_attempt_id: WaveAttemptId
├── wave_index: int
├── base_state_revision: StateRevision
└── module_ids: tuple[ModuleId, ...]
```

Requirements:

- `wave_index >= 0`;
- module IDs non-empty, unique, canonical;
- envelope имеет `wave_id`.

## 7.5. ModuleAttemptStartedEvent

```text
ModuleAttemptStartedEvent
├── wave_attempt_id: WaveAttemptId
├── module_id: ModuleId
├── module_attempt_id: ModuleAttemptId
├── implementation_id: ImplementationId
├── implementation_revision: ImplementationRevision
├── base_state_revision: StateRevision
└── base_private_revision: PrivateStateRevision | None
```

`base_private_revision=None` означает отсутствие applicable private-state revision у stateless module; это не universal availability encoding cognitive state.

Envelope имеет `wave_id`.

## 7.6. ModuleAttemptFinishedEvent

```text
ModuleAttemptFinishedEvent
├── module_id: ModuleId
├── module_attempt_id: ModuleAttemptId
├── outcome: ModuleAttemptOutcome
├── proposed_public_paths: tuple[StatePath, ...]
├── private_update_proposed: bool
└── failure: TraceFailure | None
```

Requirements:

```text
SUCCEEDED -> failure is None
FAILED    -> failure is TraceFailure
```

Для failed compute attempt:

```text
proposed_public_paths == ()
private_update_proposed == False
```

`proposed_public_paths` unique/canonical by `StatePath.dotted`.

Event фиксирует **proposal metadata**, но не payload values O1/O2.

Envelope имеет `wave_id`.

## 7.7. CommitAttemptedEvent

```text
CommitAttemptedEvent
├── wave_attempt_id: WaveAttemptId
├── base_state_revision: StateRevision
└── module_attempt_ids: tuple[ModuleAttemptId, ...]
```

`module_attempt_ids` unique; deterministic order соответствует canonical producer order, передаваемому будущим scheduler в `CommitCoordinator`.

Event существует только если runtime действительно вызывает commit boundary. Wave, завершившаяся module failure **до commit call**, не создаёт фиктивный `commit_attempted`.

Envelope имеет `wave_id`.

## 7.8. CommitSucceededEvent

```text
CommitSucceededEvent
├── wave_attempt_id: WaveAttemptId
├── commit_id: CommitId
├── base_state_revision: StateRevision
├── resulting_state_revision: StateRevision
├── module_attempt_ids: tuple[ModuleAttemptId, ...]
├── public_paths: tuple[StatePath, ...]
└── private_revisions: tuple[PrivateRevisionTransitionTrace, ...]
```

Semantics зеркалят successful `CommitRecord`, но evidence не хранит runtime `CommitRecord` object.

Requirements:

- module attempt IDs unique;
- public paths unique/canonical;
- private revisions unique/canonical by module id;
- если `public_paths` non-empty, resulting public revision == `base.next()`;
- если `public_paths == ()`, resulting public revision == base;
- private-only/no-op successful commit всё равно имеет `CommitId` и `commit_succeeded`.

Envelope имеет `wave_id`.

## 7.9. CommitFailedEvent

```text
CommitFailedEvent
├── wave_attempt_id: WaveAttemptId
├── base_state_revision: StateRevision
├── module_attempt_ids: tuple[ModuleAttemptId, ...]
└── failure: TraceFailure
```

Failed event не требует `CommitId`: normal semantic failure IS-09 происходит до allocation, а late already-allocated ID не является необходимым public evidence contract `v0.1`.

Event означает, что commit call не вернул successful `CommitResult`; он не маскирует module execution failure.

Envelope имеет `wave_id`.

## 7.10. StateRevisionCommittedEvent

```text
StateRevisionCommittedEvent
├── before: StateRevision
├── after: StateRevision
├── public_paths: tuple[StatePath, ...]
├── lineage_id: LineageId
├── branch_id: BranchId
├── agent_revision_id: AgentRevisionId
├── commit_id: CommitId | None
└── intervention_id: InterventionId | None
```

Requirements:

```text
after == before.next()
public_paths != ()
exactly one of commit_id / intervention_id is not None
```

Это event **фактического public state revision transition**.

Следовательно:

- private-only successful commit не создаёт `state_revision_committed`;
- empty no-op commit не создаёт `state_revision_committed`;
- normal public commit использует `commit_id`;
- будущая state intervention может использовать `intervention_id`.

No fake public revision создаётся ради tracing.

## 7.11. InterventionAppliedEvent

```text
InterventionAppliedEvent
├── intervention_id: InterventionId
├── base_state_revision: StateRevision
├── resulting_state_revision: StateRevision
├── target_paths: tuple[StatePath, ...]
├── lineage_id: LineageId
└── branch_id: BranchId
```

Requirements:

- target paths non-empty, unique, canonical;
- resulting state revision == `base.next()` для basic `v0.1` state override seam.

Этот contract не реализует gateway и не определяет allowlist/target validation — это `IS-14`.

## 7.12. CycleFinishedEvent

```text
CycleFinishedEvent
├── base_state_revision: StateRevision
└── resulting_state_revision: StateRevision
```

`resulting >= base` в пределах одного revision type.

Cycle может завершиться без public writes, поэтому equality допустима.

Envelope имеет `cognitive_cycle_id`.

## 7.13. CycleFailedEvent

```text
CycleFailedEvent
├── base_state_revision: StateRevision
├── current_state_revision: StateRevision
└── failure: TraceFailure
```

`current_state_revision >= base_state_revision`.

Это важно: если предыдущая wave уже была успешно committed, failure более поздней wave не должен ложно изображать rollback всего cognitive cycle, если такой rollback не существует в accepted scheduler semantics.

Envelope имеет `cognitive_cycle_id`.

---

# 8. Attempt, commit и state-transition events не сливаются

Обязательное различие:

```text
module_attempt_finished(SUCCEEDED)
≠
commit_succeeded
≠
state_revision_committed
```

Примеры:

### private-only successful wave

```text
module_attempt_finished(SUCCEEDED)
commit_attempted
commit_succeeded(public_paths=())
# state_revision_committed отсутствует
```

### invalid/stale commit

```text
module_attempt_finished(SUCCEEDED)
commit_attempted
commit_failed
# state_revision_committed отсутствует
```

### module compute exception

```text
module_attempt_started
module_attempt_finished(FAILED)
# scheduler не вызывает commit
# commit_attempted отсутствует
```

Эта granularity является core O0 causal evidence.

---

# 9. EvidenceRecorder Protocol

Contract:

```text
class EvidenceRecorder(Protocol):
    def record(self, event: TraceEventEnvelope, /) -> None: ...
```

Recorder:

- принимает уже построенный immutable event;
- не изменяет payload/envelope;
- не получает state/private/module service references;
- не возвращает cognitive value;
- не имеет intervention/write API.

`record()` является outward evidence sink operation, а не cognitive callback.

Не вводить universal subscriber/event bus API.

---

# 10. InMemoryEvidenceRecorder

Reference concrete implementation:

```text
InMemoryEvidenceRecorder
├── record(event) -> None
├── snapshot() -> tuple[TraceEventEnvelope, ...]
└── __len__() -> int
```

Semantics:

- process-local;
- append-only по public API;
- insertion order сохраняется;
- `record()` проверяет `TraceEventEnvelope` и append'ит ровно переданный immutable record;
- `snapshot()` возвращает новый immutable tuple;
- ранее полученный snapshot не меняется после последующих append;
- backing mutable list/collection не выдаётся;
- нет `clear/pop/remove/replace/truncate` public API;
- нет network/filesystem exporter;
- нет capacity/drop policy;
- нет background thread/task;
- recorder не создаёт IDs и не читает physical clock.

`MemoryError`/process failure не маскируются silent drop. Separate best-effort exporter policy не входит в `v0.1` IS-10.

---

# 11. Snapshot safety и isolation

Evidence records могут содержать только immutable/snapshot-safe structural values:

- UUID identities;
- semantic ID value objects;
- revision value objects;
- enums;
- `LogicalTime`;
- `StatePath`;
- strings/ints/bools;
- frozen evidence dataclasses;
- tuples этих значений.

Запрещено сохранять непосредственно:

- mutable state mapping;
- `CognitiveState` как shortcut вместо explicit O0 fields;
- `PrivateStateStore`/slot;
- `ModuleComputeResult` object;
- `CommitCoordinator`/`ExecutionPlanCompiler`;
- module instance;
- private contract object;
- traceback/exception object;
- arbitrary `dict[str, Any]` diagnostics.

O1/O2 semantic values и diagnostic artifacts не реализуются этим шагом.

---

# 12. Cognitive isolation

`IS-10` не меняет:

```text
ModuleComputeRequest
StateProjection
ModuleDescriptor
StateSchema
CognitiveState
PrivateStateStore
CommitCoordinator
ExecutionPlanCompiler
```

Evidence metadata не добавляется как state field и не становится declared read.

Не добавлять recorder/logger/evaluator reference в `ModuleComputeRequest`.

Не добавлять global recorder singleton.

Cognitive modules не вызывают Evidence Recorder самостоятельно в reference kernel path.

Producer-side emission является ответственностью runtime/composition/intervention boundaries соответствующих будущих steps.

---

# 13. Required tests

Минимум:

```text
tests/unit/test_evidence_records.py
tests/contract/test_evidence_isolation.py
```

Проверить минимум:

1. все 13 event kinds представлены typed payload variant;
2. envelope kind выводится из payload и не может semantic mismatch;
3. envelope/все helper/payload records frozen;
4. invalid physical timestamp reject;
5. required cycle/wave temporal depth reject;
6. composition modules canonical/unique;
7. plan dependencies/waves canonical и structurally valid;
8. `TraceFailure` не хранит original exception object;
9. module success/failure invariant;
10. failed module attempt не содержит proposal metadata;
11. commit succeeded revision semantics для public-only/private-only/no-op shape;
12. private revision transition == exact next;
13. state_revision_committed требует actual `before.next()` + non-empty paths;
14. state_revision_committed требует ровно один origin (`commit_id` XOR `intervention_id`);
15. cycle failure допускает already-committed earlier-wave revision;
16. `EvidenceRecorder` structural Protocol conformance;
17. in-memory recorder сохраняет insertion order;
18. snapshot является tuple и не exposes backing list;
19. старый snapshot остаётся стабильным после нового append;
20. recorder public API не имеет mutation методов кроме append `record`;
21. recorder не создаёт IDs/timestamps;
22. evidence module не импортирует runtime;
23. `ModuleComputeRequest`/`StateProjection` не получают evidence fields/capabilities;
24. runtime recorder не имеет state/private write authority;
25. никаких emit side effects не добавлено в planner/commit coordinator на этом шаге.

Допустимы дополнительные property tests canonical ordering/immutability, если они не расширяют scope.

---

# 14. VerificationObligations

После `IS-10`:

- `V01-009` — `foundation`: typed structural evidence contracts + passive append-only recorder существуют;
- `V01-010` — `substantial`: evidence/cognition isolation механически представлена contracts/API, но полная runtime emission проверяется после scheduler/composition integration.

`V01-009` не считается полностью закрытым до integration trace в следующих steps.

---

# 15. Verification

Запустить:

```text
FAST + ARCH
```

Targeted pytest минимум включает:

```text
tests/unit/test_evidence_records.py
tests/contract/test_evidence_isolation.py
```

После targeted green выполнить `FULL-C0` перед завершением coding task.

---

# 16. Forbidden scope

Не реализовывать в `IS-10`:

- Scheduler/WaveExecutor;
- module execution;
- automatic trace emission из существующих planner/commit classes;
- Composition Root/profile parsing;
- Intervention Gateway;
- state/private intervention;
- O1/O2/O3 data capture;
- private-state probes;
- metrics aggregation;
- logging framework;
- OpenTelemetry;
- exporter/network/file telemetry;
- Experience Journal;
- replay/event sourcing;
- global event bus/subscribers;
- async/background recorder;
- bounded-loss/backpressure policy;
- new cognitive state fields ради evidence;
- TraceEventId/new causal identity без отдельного design need.

Следующий implementation step остаётся `V0.1-IS-11 — WaveExecutor & Scheduler` только после отдельного ChatGPT audit completed IS-10.
