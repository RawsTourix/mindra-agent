# V0.1-IS-09 — Exact Atomic CommitCoordinator clarification

## Статус

**Статус:** `accepted`  
**Область:** только `V0.1-IS-09 — Atomic CommitCoordinator`  
**Baseline:** accepted `v0.1/README.md` + `implementation-sequence.md` + `is-06-contract-shape.md` + `is-08-private-state-store-shape.md` + `F31`

Этот документ устраняет implementation-level неоднозначности atomic public/private commit перед реализацией `IS-09`. Он не меняет F31, wave semantics или Evidence design; он фиксирует exact runtime transaction boundary, на которую позднее опираются Scheduler и O0 Evidence.

При конфликте приоритет имеют canonical design/F31, и implementation останавливается с blocker report.

---

# 1. Граница шага

`CommitCoordinator` является единственной поддерживаемой runtime boundary публикации staged module effects.

`IS-09`:

- валидирует `ModuleComputeResult`/public/private proposals;
- строит следующий immutable `CognitiveState`, если есть public writes;
- подготавливает private updates через `PrivateStateStore`;
- публикует private updates только после полной validation public+private transaction;
- присваивает successful commit отдельный `CommitId`;
- возвращает immutable commit result/record.

`IS-09` не:

- выполняет modules;
- строит execution plan;
- реализует Scheduler/WaveExecutor;
- пишет Evidence events;
- реализует retry/rebase;
- допускает partial-success subset;
- вводит background/concurrent mutation.

---

# 2. Exact runtime types

Physical owner: `mindra.runtime.commit` или эквивалентный file split внутри `mindra.runtime`.

Минимальный public runtime набор:

```text
PrivateStateRevisionTransition
CommitRecord
CommitResult
CommitCoordinator
```

## 2.1. PrivateStateRevisionTransition

Frozen value object:

```text
PrivateStateRevisionTransition
├── module_id: ModuleId
├── before: PrivateStateRevision
└── after: PrivateStateRevision
```

`after == before.next()` для фактически committed private update.

## 2.2. CommitRecord

Frozen structural record successful commit:

```text
CommitRecord
├── commit_id: CommitId
├── base_state_revision: StateRevision
├── resulting_state_revision: StateRevision
├── logical_time: LogicalTime
├── module_attempt_ids: tuple[ModuleAttemptId, ...]
├── public_paths: tuple[StatePath, ...]
└── private_revisions: tuple[PrivateStateRevisionTransition, ...]
```

Canonical ordering:

- `module_attempt_ids` — deterministic order результатов commit input после canonical ordering по producer `ModuleId.value`;
- `public_paths` — unique canonical sort по `StatePath.dotted`;
- `private_revisions` — canonical sort по `module_id.value`.

`CommitRecord` не является Evidence event и не содержит physical timestamps/error text/profile metadata.

## 2.3. CommitResult

Frozen:

```text
CommitResult
├── state: CognitiveState
└── record: CommitRecord
```

Private store не возвращается через result и остаётся runtime-owned object.

---

# 3. Coordinator construction

Conceptual API:

```text
CommitCoordinator(
    *,
    schema: StateSchema,
    descriptors: tuple[ModuleDescriptor, ...],
    private_store: PrivateStateStore,
    id_factory: IdFactory,
)
```

Semantics:

- coordinator не является Service Locator;
- descriptor `ModuleId` уникальны;
- schema/descriptors/private store являются active composition boundary;
- coordinator не хранит hidden mutable `StateRevision` counter;
- committed public state передаётся явно в каждый `commit()` как current base snapshot;
- private-store mutation доступна coordinator только через internal prepared/apply boundary `IS-08`.

---

# 4. Commit API

Conceptual API:

```text
commit(
    *,
    current_state: CognitiveState,
    results: tuple[ModuleComputeResult, ...],
    logical_time: LogicalTime,
) -> CommitResult
```

`current_state` считается current committed public snapshot, предоставленным owning runtime/Scheduler. Coordinator fail-closed проверяет proposals относительно его `StateRevision`.

`results` — результаты одной будущей wave; `IS-09` не выполняет их compute.

Empty `results=()` допустим как successful no-op transaction boundary и может получить отдельный `CommitId`; public/private state при этом не меняются.

---

# 5. Canonical transaction pipeline

Успешный `commit()` conceptually выполняется строго в порядке:

```text
validate coordinator/base inputs
→ canonicalize/validate result participants
→ validate all public proposals/writes/provenance
→ prepare ALL private proposals (без mutation)
→ construct ALL public replacements
→ preconstruct resulting CognitiveState (если public writes есть)
→ preconstruct revision-transition metadata
→ allocate CommitId
→ preconstruct CommitRecord + CommitResult
→ internal all-or-nothing private apply
→ return already-constructed CommitResult
```

Критический invariant:

> До internal private apply не публикуется и не мутируется никакой canonical public/private state.

После начала successful internal private apply не должно выполняться новое schema/value/provenance validation или иная ожидаемо падающая semantic construction, кроме fail-closed revalidation самого private apply primitive.

Public `CognitiveState` immutable, поэтому «подготовить новый state» не означает его публикацию. Он становится новым committed public snapshot только через успешный return `CommitResult` owning runtime'у.

---

# 6. Base public-state validation

Перед proposals:

- `current_state` — `CognitiveState`;
- `current_state.envelope.schema_revision == schema.revision`;
- active composition/schema assumptions не выводятся из global state;
- `logical_time` — `LogicalTime`.

Temporal compatibility current state → commit time:

- `run_id` и `agent_session_id` обязаны совпадать;
- любой уже установленный (`not None`) `episode_id`, `decision_window_id`, `cognitive_cycle_id` base state не может измениться или стать `None` в commit logical time;
- более глубокий scope может впервые появиться, если в base он был `None`;
- `wave_id` base snapshot не ограничивает следующий commit: commit provenance использует exact переданный `logical_time`.

Это v0.1 causal compatibility, а не lifecycle/reset implementation.

---

# 7. Result participant validation

Каждый item `results` обязан быть `ModuleComputeResult`.

Semantic producer конкретного result определяется его `state_update.producer`.

Для каждого result:

- producer зарегистрирован в active descriptors;
- один producer встречается максимум один раз в transaction;
- `module_attempt_id` одного result уникален внутри transaction;
- `state_update.base_state_revision == current_state.envelope.state_revision`;
- producer участвует в supported `COGNITIVE_CYCLE` phase по descriptor;
- private proposal, если есть, обязан иметь тот же `module_id` и тот же `module_attempt_id`, что public `StateUpdateProposal` этого result.

Stale public base revision → `StaleProposalError`.

Duplicate producer/attempt → existing typed `CommitValidationError`/`DuplicateIdentityError` по естественному смыслу; generic bool не использовать.

---

# 8. Public write authority

Для каждого `StateWrite`:

1. key/path существует в `StateSchema`;
2. `StateFieldSpec.owner == StateUpdateProposal.producer`;
3. exact path объявлен в `ModuleDescriptor.writes` producer;
4. один `StatePath` может встречаться максимум один раз во всей transaction;
5. overlapping/conflicting staged write fail closed;
6. availability остаётся canonical `Available/Unknown/Stale/Unavailable`;
7. payload для `Available/Stale` проходит соответствующий schema `ValueContract.freeze()` через normal CognitiveState construction boundary.

Owner mismatch или path вне descriptor writes → `UnauthorizedWriteError`.

Missing schema field сохраняет structural typed error (`MissingFieldError`/existing schema error).

No `last-write-wins`, merge или reducer logic внутри coordinator.

---

# 9. Public provenance validation

Для module-produced `StateWrite.provenance` coordinator обязан проверить минимум:

```text
provenance.producer == proposal.producer
provenance.implementation_id == active descriptor.implementation_id
provenance.base_state_revision == current public StateRevision
provenance.module_attempt_id == proposal.module_attempt_id
provenance.logical_time == commit logical_time
```

Module-produced write не может использовать `RuntimeBoundaryId` вместо своего semantic `ModuleId`.

`implementation_id=None` для normal module write `IS-09` не допускается.

`source_refs`, `parent_refs`, `intervention_refs` сохраняются как proposal data; coordinator не придумывает их сам.

Provenance mismatch → `CommitValidationError` или более specific existing typed error.

Coordinator не добавляет physical timestamp/evidence metadata в `StateProvenance`.

---

# 10. Private proposal validation

Если `ModuleComputeResult.private_state_update` существует:

- module/attempt consistency уже проверена на participant boundary;
- proposal передаётся `PrivateStateStore._prepare()`;
- private store проверяет registered/stateful owner, base private revision и concrete `PrivateStateContract.freeze()`;
- preparation не мутирует store.

STATELESS result с private proposal fail closed.

STATEFUL result может не предлагать private update: отсутствие private mutation допустимо.

`IS-09` не повторяет concrete private contract внутри coordinator и не обходит `PrivateStateStore`.

---

# 11. Public state construction

Все public writes сначала преобразуются в replacement `StateEntry` objects.

Если хотя бы один public write есть:

```text
new_state_revision = current_state.envelope.state_revision.next()
parent_state_revision = current_state.envelope.state_revision
schema_revision = current_state.envelope.schema_revision
lineage_id = current_state.envelope.lineage_id
branch_id = current_state.envelope.branch_id
agent_revision_id = current_state.envelope.agent_revision_id
composition_revision = current_state.envelope.composition_revision
logical_time = commit logical_time
```

Новый immutable state строится copy-on-commit через существующий runtime/state contract и полностью проходит schema `ValueContract` validation **до private apply**.

Если public writes отсутствуют:

```text
result.state is current_state
resulting_state_revision == base_state_revision
```

Private-only или full no-op transaction не создаёт фиктивный public revision.

Любой accepted public write считается public state transition, даже если semantic payload равен предыдущему: provenance/entry является частью canonical state и новая публикация получает следующую `StateRevision`.

---

# 12. CommitId semantics

`CommitId` создаётся только через injected `IdFactory`.

Для `IS-09`:

- `CommitId` выделяется **после** успешной полной semantic validation и preconstruction public/private result;
- validation failure до этого не расходует deterministic CommitId sequence;
- каждый successful transaction, включая private-only и empty no-op, получает отдельный `CommitId`;
- `CommitId` не равен `StateRevision` и не выводится из неё.

Если внутренний private apply неожиданно fail-closed после allocation (например, revision изменилась между preparation и apply), commit не возвращается как successful; public state остаётся непубликованным, а `PrivateStateStore._apply_prepared()` гарантирует no partial private mutation. Расход такого already-allocated ID допустим как failed late attempt и не меняет semantic state.

---

# 13. Private revision transitions

Для каждого prepared private update successful record содержит:

```text
module_id
before = expected_revision
after = next_revision
```

Если private update отсутствует, transition для module отсутствует.

Private-only successful commit:

- public `StateRevision` не меняется;
- private revision(s) увеличиваются ровно на один;
- отдельный `CommitId` существует;
- record позволяет позднему O0 Evidence восстановить before/after private revisions.

---

# 14. Atomicity

Обязательная failure semantics:

Если **любая** validation/preconstruction fails до private apply:

```text
current CognitiveState unchanged
PrivateStateStore unchanged
```

Если internal private apply fails:

```text
current CognitiveState still unpublished/unchanged
PrivateStateStore all-or-nothing primitive leaves all slots unchanged
```

Никакой partial-success subset не публикуется.

Coordinator не выполняет rollback уже опубликованного public state: public state immutable и до successful return не публикуется.

---

# 15. Error semantics

Использовать существующую taxonomy:

- stale public/private base → `StaleProposalError`;
- owner/descriptor write violation → `UnauthorizedWriteError`;
- conflicting/duplicate staged writes → `CommitValidationError`;
- provenance/attempt/temporal mismatch → `CommitValidationError`;
- missing schema path → existing `MissingFieldError`/schema error;
- private store failures сохраняют свои existing typed errors.

Не вводить generic `success=False`, silent rebase, `except Exception: pass` или ad-hoc last-write-wins.

---

# 16. Verification focus

Помимо tests из `implementation-sequence.md`, обязательно проверить:

1. successful public-only commit → public revision +1, parent=base, private unchanged;
2. successful private-only commit → public object/revision unchanged, private revision +1, CommitId существует;
3. successful public+private commit → оба эффекта видимы только после success;
4. empty successful transaction → same public state, no private change, own CommitId;
5. stale public proposal → no public/private mutation;
6. stale private proposal при валидном public write → public не публикуется;
7. invalid/unauthorized public write при валидном private proposal → private не мутирует;
8. invalid private payload при валидном public write → public не публикуется;
9. unknown schema path reject;
10. owner mismatch reject;
11. path не объявлен descriptor writes reject;
12. duplicate/conflicting path across different results reject;
13. duplicate producer reject;
14. duplicate module attempt reject;
15. private proposal module mismatch reject;
16. private proposal attempt mismatch reject;
17. provenance producer mismatch reject;
18. provenance implementation mismatch reject;
19. provenance base revision mismatch reject;
20. provenance attempt mismatch reject;
21. provenance logical time mismatch reject;
22. base/commit logical-time incompatibility reject;
23. public payload проходит schema ValueContract;
24. private payload проходит private contract;
25. failed semantic validation до allocation не расходует deterministic CommitId;
26. public write с payload, равным старому, всё равно создаёт новую revision из-за новой committed entry/provenance;
27. CommitRecord canonical ordering независимо от input result order;
28. PrivateStateRevisionTransition before/after exact;
29. CommitResult/CommitRecord immutable;
30. no public direct mutation API появляется;
31. state-machine sequence: success → stale apply → invalid write → private update → failure rollback → next success.

VerificationObligations после успешного `IS-09`:

- `V01-002` — closed at commit layer;
- `V01-003` — closed;
- `V01-006` — closed;
- `V01-008` — closed at commit layer.

`V01-001 same-base wave` остаётся Scheduler/WaveExecutor work последующих шагов.

---

# 17. Forbidden scope

Не реализовывать:

- Scheduler/WaveExecutor;
- module compute execution;
- retry/recompute/rebase policy;
- partial-success commit;
- Evidence Recorder/events;
- CompositionRoot/profile parsing;
- intervention;
- lifecycle reset/scopes;
- checkpoint/restore;
- parallelism/thread safety;
- direct mutable state/private store API;
- action/training commit semantics CR-01/CR-05.