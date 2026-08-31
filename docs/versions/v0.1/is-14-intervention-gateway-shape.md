# V0.1-IS-14 — InterventionGateway exact shape

## Статус

**Статус:** `accepted exact clarification`  
**Область:** `V0.1-IS-14 — InterventionGateway`  
**Baseline:** F31 + accepted v0.1 design + accepted IS-01 … IS-13

Этот документ фиксирует implementation-level choices basic controlled intervention seam, которые нельзя оставлять Codex на самостоятельный архитектурный выбор.

Он не меняет F31, ownership, scheduler/commit semantics, Evidence Plane taxonomy или Composition Root semantics. Он конкретизирует только минимальную public-state intervention boundary первой версии.

---

# 1. Scope и relation к DU-06

`DU-06`/ADR-0006 различают passive Evidence Plane и explicit Intervention Gateway и conceptually предпочитают paired fork для confirmatory causal experiments.

`v0.1` ещё НЕ имеет полного Agent Snapshot, Environment clone/restore, branch runtime manager или exact counterfactual replay.

Поэтому IS-14 реализует только:

```text
committed CognitiveState
        ↓
explicit one-shot public StateInterventionSpec
        ↓
policy/base/schema/value validation
        ↓
new intervention-derived committed CognitiveState
        ↓
O0 intervention evidence
```

Это **in-place treatment continuation** текущего `KernelRuntime`, а не paired exact counterfactual clone.

Natural base snapshot immutable и не переписывается. Resulting state получает новую treatment lineage/branch identity, чтобы дальнейшая trajectory не masquerade как natural continuation.

IS-14 НЕ реализует:

- module-result interception до commit;
- private-state intervention;
- backend/raw intervention;
- composition ablation/substitution;
- persistent clamp/release semantics;
- full fork/restore manager.

---

# 2. Physical layout

Добавить:

```text
src/mindra/contracts/intervention.py
src/mindra/runtime/intervention.py
```

Допустимые focused integration changes:

```text
src/mindra/contracts/__init__.py
src/mindra/runtime/__init__.py
src/mindra/composition/root.py
src/mindra/composition/runtime.py
```

`contracts.intervention` импортирует только stdlib + другие `mindra.contracts` modules и НЕ импортирует runtime/composition.

`runtime.intervention` зависит от contracts/runtime state construction/evidence, но НЕ от composition/reference/entrypoints.

`composition` может собрать gateway и policy как privileged control-plane dependency.

Cognitive module contracts не получают intervention capability.

---

# 3. Supported intervention class v0.1

IS-14 поддерживает ровно один класс treatment:

```text
one-shot committed public-state Available(value) override
```

Semantics `one-shot`:

- gateway выполняет один intervention commit;
- после commit никакой hidden clamp/hook не остаётся активным;
- treatment value остаётся обычным committed state value до следующей natural/intervention publication этого field;
- release event/API отсутствует, потому что persistent treatment не реализуется.

Нельзя через IS-14 напрямую установить `Unknown`, `Stale` или `Unavailable`.

Нельзя изменять private state.

---

# 4. StateInterventionWrite

В `mindra.contracts.intervention` определить frozen+slots:

```text
StateInterventionWrite
├── path: StatePath
└── value: object
```

Requirements:

- `path` обязан быть `StatePath`;
- `value` является ephemeral requested treatment payload;
- snapshot/type freeze выполняется Gateway через active `StateFieldSpec.value_contract` непосредственно перед construction committed state;
- write не содержит producer/owner/InterventionId/revision — эти causal данные принадлежат gateway.

Spec/request не является Evidence artifact и не сохраняется Recorder-ом целиком.

---

# 5. StateInterventionSpec

Frozen+slots exact fields:

```text
StateInterventionSpec
├── base_state_revision: StateRevision
├── base_lineage_id: LineageId
├── base_branch_id: BranchId
└── writes: tuple[StateInterventionWrite, ...]
```

Requirements:

- `writes` non-empty;
- each path unique;
- writes canonical order по `path.dotted`;
- duplicate path reject, не last-write-wins;
- base revision/lineage/branch typed;
- constructor canonicalize ordering, но не меняет treatment values.

Base определяется тройкой:

```text
(StateRevision, LineageId, BranchId)
```

а не одним `StateRevision`, потому что intervention semantics уже различает causal branches/lineages.

---

# 6. InterventionPolicy

В `mindra.contracts.intervention` определить frozen+slots exact-path policy:

```text
InterventionPolicy
└── allowed_paths: tuple[StatePath, ...]
```

Public constructors/helpers:

```text
InterventionPolicy.disabled() -> InterventionPolicy
InterventionPolicy.allowlist(paths: tuple[StatePath, ...], /) -> InterventionPolicy
allows(path: StatePath, /) -> bool
```

Semantics:

- paths canonical by `StatePath.dotted`;
- duplicates reject;
- empty tuple = interventions disabled;
- allowlist exact path only;
- no namespace wildcard/prefix matching;
- no regex;
- no value-transform callbacks;
- no dynamic mutation/add/remove after build.

Policy является Evaluation/Research Control Plane configuration, а не cognitive composition setting.

Она:

- НЕ входит в `KernelProfile`;
- НЕ входит в composition fingerprint;
- НЕ меняет AgentRevisionId semantics;
- НЕ доступна modules.

---

# 7. Runtime records

В `mindra.runtime.intervention` определить frozen+slots:

```text
InterventionRecord
├── intervention_id: InterventionId
├── base_state_revision: StateRevision
├── resulting_state_revision: StateRevision
├── target_paths: tuple[StatePath, ...]
├── base_lineage_id: LineageId
├── base_branch_id: BranchId
├── resulting_lineage_id: LineageId
├── resulting_branch_id: BranchId
└── logical_time: LogicalTime
```

Invariants:

- `resulting_state_revision == base_state_revision.next()`;
- `target_paths` non-empty/canonical/unique;
- base/result lineage/branch typed;
- resulting lineage/branch are newly allocated treatment identities;
- `logical_time` is safe-boundary time with `cognitive_cycle_id is None` and `wave_id is None`.

Также:

```text
InterventionResult
├── state: CognitiveState
└── record: InterventionRecord
```

Result validation подтверждает, что state envelope revision/lineage/branch/logical_time совпадают с record.

Record является structural runtime result и не содержит treatment values/O1 payload.

---

# 8. InterventionGateway constructor

Exact public runtime API:

```text
InterventionGateway(
    *,
    schema: StateSchema,
    policy: InterventionPolicy,
    evidence_recorder: EvidenceRecorder,
    id_factory: IdFactory,
)
```

Gateway получает только authority, необходимую public state intervention:

- immutable schema;
- immutable policy;
- evidence sink;
- causal ID factory.

Gateway НЕ получает:

- `PrivateStateStore`;
- `CommitCoordinator`;
- Scheduler/module map;
- registry;
- CompositionRoot;
- Service Locator.

Поэтому arbitrary private mutation механически невозможна через этот API.

---

# 9. InterventionGateway.apply

Exact method:

```text
apply(
    *,
    current_state: CognitiveState,
    spec: StateInterventionSpec,
    logical_time: LogicalTime,
) -> InterventionResult
```

`logical_time` представляет explicit committed safe boundary.

IS-14 допускает только between-cycle boundary:

```text
logical_time.cognitive_cycle_id is None
logical_time.wave_id is None
```

Environment phases ещё отсутствуют.

---

# 10. Validation order

До allocation любого нового causal ID Gateway fail-closed проверяет минимум:

1. exact runtime types;
2. `current_state.envelope.schema_revision == active schema.revision`;
3. safe-boundary `logical_time` имеет no cycle/no wave;
4. run/session совпадают с current state;
5. если base state уже имеет episode/decision ids, intervention time обязана сохранять их;
6. spec base revision == current state revision;
7. spec base lineage == current state lineage;
8. spec base branch == current state branch;
9. каждый path присутствует в active schema;
10. каждый path разрешён policy;
11. все values проходят corresponding `ValueContract.freeze()`;
12. все targets подготовлены полностью до publication.

Если один target invalid/not allowed/stale — отвергается весь batch.

Никакой partial state/evidence publication.

Validation failure не расходует `InterventionId`, `LineageId` или `BranchId` у deterministic factory.

---

# 11. Identity allocation

После полной prevalidation exact allocation order:

```text
InterventionId
LineageId
BranchId
```

Все три создаются одним injected `IdFactory`.

Resulting lineage/branch всегда новые для successful intervention.

`InterventionId` не masquerade как CommitId/ModuleAttemptId.

---

# 12. Treatment lineage semantics

Successful intervention создаёт:

```text
base immutable snapshot
        ↓ parent_state_revision
new treatment snapshot
```

Result envelope:

```text
schema_revision       = base.schema_revision
state_revision        = base.state_revision.next()
parent_state_revision = base.state_revision
lineage_id            = newly allocated LineageId
branch_id             = newly allocated BranchId
agent_revision_id     = base.agent_revision_id
logical_time          = supplied safe-boundary logical_time
composition_revision  = base.composition_revision
```

Natural base object не изменяется.

Это означает:

- дальнейшие ordinary scheduler commits продолжают treatment lineage/branch;
- intervention-derived trajectory можно отличить от natural base;
- v0.1 НЕ утверждает, что одновременно продолжает paired control branch;
- exact counterfactual fork остаётся future snapshot/runtime work.

---

# 13. Semantic ownership и treatment provenance

Active `StateSchema` НЕ изменяется.

`StateFieldSpec.owner` остаётся semantic module owner.

Для каждого intervention target создаётся `StateEntry`:

```text
availability = Available(frozen_treatment_value)
```

Exact `StateProvenance`:

```text
producer = RuntimeBoundaryId("evaluation.intervention")
implementation_id = None
base_state_revision = base.state_revision
module_attempt_id = None
logical_time = intervention safe-boundary time
source_refs = (
    base.state_revision,
    base.lineage_id,
    base.branch_id,
)
parent_refs = (base.state_revision,)
intervention_refs = (intervention_id,)
```

Это intentional distinction:

```text
semantic owner = schema field owner
current value origin = controlled intervention boundary
```

Gateway не создаёт fake ModuleId/ImplementationId/ModuleAttemptId/CommitId.

Unchanged fields сохраняют exact previous `StateEntry` objects/provenance через copy-on-commit semantics.

---

# 14. Atomic public state construction

После validation + identity allocation Gateway строит все replacement entries и новый immutable `CognitiveState` через existing runtime-controlled state construction/copy boundary.

Multi-target intervention:

```text
all replacements publish together
or
none publish
```

Gateway не мутирует supplied `current_state`.

Новый `StateRevision` создаётся ровно один на successful intervention batch независимо от числа target paths.

---

# 15. O0 Evidence ordering

Successful intervention публикует ровно два existing O0 events в exact order:

```text
intervention_applied
state_revision_committed
```

Оба используют supplied safe-boundary logical time и `physical_timestamp_ns=None`.

`InterventionAppliedEvent` зеркалит actual record:

```text
intervention_id
base_state_revision
resulting_state_revision
target_paths
resulting_lineage_id as lineage_id
resulting_branch_id as branch_id
```

Сразу после него:

`StateRevisionCommittedEvent`:

```text
before = base revision
after = resulting revision
public_paths = target paths
lineage_id = resulting lineage
branch_id = resulting branch
agent_revision_id = resulting state agent revision
commit_id = None
intervention_id = actual InterventionId
```

Failure до successful publication:

- no `intervention_applied`;
- no `state_revision_committed`.

IS-14 не добавляет новый TraceEventKind.

Treatment values остаются вне O0 evidence.

---

# 16. Evidence failure semantics

Gateway не использует best-effort tracing.

Порядок:

1. полностью construct immutable candidate resulting state + record;
2. record `intervention_applied`;
3. record `state_revision_committed`;
4. только затем return `InterventionResult`.

Если `EvidenceRecorder.record()` raises:

- exception propagate;
- Gateway result не возвращается;
- `KernelRuntime` не заменяет current state;
- cognitive/public state publication через facade не происходит.

Recorder append-only API не предоставляет rollback уже записанного первого event, поэтому infrastructure failure между двумя records может оставить incomplete evidence tail; это infrastructure-fatal/invalid run, не successful intervention.

Не маскировать такой failure и не продолжать execution как будто intervention succeeded.

---

# 17. CompositionRoot integration

IS-13 exact constructor получает backward-compatible optional control-plane refinement:

```text
CompositionRoot(
    *,
    registry: ImplementationRegistry,
    id_factory: IdFactory,
    intervention_policy: InterventionPolicy | None = None,
)
```

Semantics:

```text
None -> InterventionPolicy.disabled()
```

Existing callers без нового argument сохраняют прежнее поведение.

Composition Root:

- использует тот же shared `IdFactory`;
- после создания `InMemoryEvidenceRecorder` создаёт `InterventionGateway` с active schema/policy/recorder/factory;
- передаёт gateway в `KernelRuntime`;
- root `composition_resolved`/`plan_compiled` evidence остаётся в прежнем exact order;
- intervention policy НЕ входит в composition fingerprint/profile metadata.

Reference TOML не получает intervention section.

Default `configs/v0.1/reference.toml` runtime остаётся interventions-disabled.

---

# 18. KernelRuntime integration

`KernelRuntime` хранит internal gateway, но НЕ exposes raw gateway/service/store.

Public surface получает:

```text
apply_intervention(spec: StateInterventionSpec, /) -> InterventionResult
```

Method:

1. доступен только когда runtime не исполняет `run_cycle()`;
2. использует root safe-boundary LogicalTime с pinned Run/Session/Episode/DecisionWindow и no Cycle/Wave;
3. вызывает internal gateway на current `self._state`;
4. только после successful Gateway return делает `self._state = result.state`;
5. возвращает exact result.

Для механической safe-boundary защиты `KernelRuntime` может хранить internal `_cycle_active: bool` control flag.

`run_cycle()` должен устанавливать его на время synchronous scheduler call через `try/finally`.

`apply_intervention()` при active cycle -> `InterventionError` до gateway call.

Flag:

- не является CognitiveState;
- не доступен modules;
- не влияет на logical time;
- не является scheduler outcome/retry policy.

Default disabled runtime вызывает тот же method, но policy fail-closed reject любой target.

---

# 19. Error semantics

Использовать existing `InterventionError` для policy/base/boundary/intervention validation failures, где более specific existing structural exception не является обязательной public semantics.

Внешний caller должен однозначно отличать rejected intervention от successful `InterventionResult`.

Не добавлять evaluator score/error taxonomy.

Failure не меняет runtime current state.

---

# 20. Public exports

`mindra.contracts` экспортирует минимум:

```text
StateInterventionWrite
StateInterventionSpec
InterventionPolicy
```

`mindra.runtime` экспортирует минимум:

```text
InterventionRecord
InterventionResult
InterventionGateway
```

`mindra.composition` не обязан re-export intervention types; caller может импортировать control contract из `mindra.contracts`.

---

# 21. Required tests

Минимум:

```text
tests/contract/test_intervention_gateway.py
tests/integration/test_intervention_lineage.py
tests/state_machine/test_intervention_commit_sequence.py
```

Также допустим focused unit test policy/spec.

Обязательное покрытие:

## Contracts/policy

1. spec/write/policy frozen;
2. spec non-empty;
3. duplicate targets reject;
4. target order canonicalized;
5. policy exact-path canonical allowlist;
6. empty/disabled policy rejects all;
7. no wildcard/namespace implicit permission.

## Validation/atomicity

8. stale StateRevision reject;
9. wrong base LineageId reject;
10. wrong base BranchId reject;
11. missing schema path reject;
12. non-allowlisted path reject;
13. invalid value type reject;
14. mutable/snapshot-unsafe value reject;
15. multi-write one-invalid -> no publication/evidence;
16. validation failure does not consume Intervention/Lineage/Branch IDs;
17. Gateway has no private-state mutation surface.

## Successful commit

18. one target -> revision exactly +1;
19. multi-target -> one revision exactly +1;
20. parent revision == base revision;
21. resulting LineageId/BranchId new;
22. base CognitiveState remains unchanged;
23. unchanged entries retain prior provenance;
24. schema owner unchanged;
25. target availability = Available treatment;
26. exact intervention provenance fields/source refs;
27. no fake module/commit identity.

## Evidence

28. exact order `intervention_applied -> state_revision_committed`;
29. event payloads mirror record/state;
30. StateRevisionCommitted origin has `commit_id=None`, exact `intervention_id`;
31. no events on validation failure;
32. physical timestamp remains None;
33. recorder failure propagates and facade does not publish resulting state.

## KernelRuntime/composition

34. default reference runtime rejects intervention;
35. explicit allowlist research runtime accepts exact allowed path;
36. intervention policy change does not change composition fingerprint;
37. runtime public surface does not expose raw gateway/private store;
38. apply_intervention updates runtime.state only on success;
39. intervention during active cycle fail closed (test may use controlled/reentrant test fixture without changing production module contracts);
40. subsequent scheduler commit continues resulting treatment lineage/branch;
41. `ModuleComputeRequest`/`StateProjection` remain intervention-free.

## State-machine

Минимальная sequence:

```text
natural committed state
→ successful intervention
→ stale old-base intervention rejected
→ normal cycle/commit continues treatment lineage
→ another valid intervention creates next treatment lineage/revision
```

At every failed step current state remains exact prior committed snapshot.

---

# 22. VerificationObligations

После independent acceptance ожидается:

```text
V01-011 — closed
V01-009 — intervention lineage extension substantial/closed for v0.1 intervention producer
```

`V01-009` overall fully closed только после final integration/hardening, если implementation-sequence так требует.

---

# 23. Forbidden scope

IS-14 категорически не реализует:

- `MINDRA-Eval`;
- evaluator Ground Truth injection;
- arbitrary object patching;
- private-state mutation;
- staged module-result interception;
- backend/activation patching;
- composition ablation;
- full counterfactual fork/restore;
- Agent Snapshot/checkpoint;
- Environment clone/reset semantics;
- persistent/scope-bound clamp;
- intervention release lifecycle;
- O1 treatment-value Evidence payload;
- new TraceEventKind;
- retry/rebase;
- async/background intervention;
- global gateway/Service Locator;
- intervention config in TOML;
- CLI (`IS-15`).

Не менять semantic owner StateField.

Не менять Scheduler/CommitCoordinator transaction semantics.

Не менять F31/accepted ADR/version design.

---

# 24. Acceptance statement

IS-14 считается implementation-ready только если coding task может реализовать exact public-state treatment seam без выбора:

- intervention class;
- base identity semantics;
- policy semantics;
- availability semantics;
- lineage behavior;
- provenance encoding;
- evidence ordering;
- composition/runtime integration;
- failure/atomicity boundary.

Этот документ фиксирует все перечисленные choices.
