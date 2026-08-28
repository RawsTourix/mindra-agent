# V0.1-IS-11 — Attempt/result causal binding correction

## Статус

**Статус:** `accepted correction clarification`  
**Область:** только correction `V0.1-IS-11 — WaveExecutor & Scheduler`  
**Baseline:** accepted `is-11-wave-scheduler-shape.md` + `is-09-commit-coordinator-shape.md` + `F31`

Этот документ закрывает implementation-level defect, обнаруженный independent ChatGPT audit implementation commit `e8aa2fa8528b2875c54c010de0777dd266e5bd49`.

Он не меняет F31, module ownership, commit atomicity, O0 taxonomy или scheduler semantics. Он уточняет границу между фактически dispatched module attempt и staged result, которую невозможно доказать внутри `CommitCoordinator` после потери execution-origin context.

---

# 1. Defect

`CognitiveScheduler` создаёт authoritative runtime identities:

```text
actual ModuleId from ExecutionWave / concrete module binding
actual ModuleAttemptId from scheduler IdFactory
```

`WaveExecutor` возвращает `ModuleAttemptRecord`, который сохраняет эти actual identities из request.

Однако successful `ModuleComputeResult` внутри record содержит собственный `StateUpdateProposal` с полями:

```text
producer
module_attempt_id
```

Текущая implementation передаёт results в `CommitCoordinator` без проверки, что эти proposal identities совпадают с actual dispatched attempt.

`CommitCoordinator` не может восстановить эту связь самостоятельно: его `commit()` получает только `ModuleComputeResult`, но не execution requests/records.

Следовательно, module может вернуть internally self-consistent staged result с другим `module_attempt_id` или с identity другого active producer. Такой result способен пройти existing coordinator validation, хотя causal origin staged effect не совпадает с реально dispatched module attempt.

Минимальный наблюдаемый дефект:

```text
module_attempt_started(actual_attempt=A)
module_attempt_finished(actual_attempt=A, SUCCEEDED)
commit_attempted(module_attempt_ids=(A,))

module result заявляет module_attempt_id=B
CommitCoordinator принимает B как proposal identity

commit_succeeded(module_attempt_ids=(B,))
```

Это нарушает causal trace consistency и fail-closed execution ownership.

Для producer spoof возможна аналогичная потеря связи:

```text
actual concrete module X
→ returns StateUpdateProposal(producer=Y)
```

если Y является другим active descriptor и staged result самосогласован относительно Y.

---

# 2. Required correction

Execution-origin binding обязан проверяться там, где одновременно известны:

- actual `ModuleAttemptRecord.module_id`;
- actual `ModuleAttemptRecord.module_attempt_id`;
- successful `ModuleComputeResult`.

Этой boundary является `CognitiveScheduler` после validation/canonicalization executor records и до commit call.

Для каждого successful record Scheduler обязан fail closed проверить минимум:

```text
record.result.state_update.producer == record.module_id
record.result.state_update.module_attempt_id == record.module_attempt_id
```

Если `private_state_update` существует, existing `CommitCoordinator` по-прежнему проверяет его consistency с public proposal. После двух checks выше это transitively связывает private proposal с actual execution attempt.

Допустимо также явно проверить private proposal against actual record как defense-in-depth, если это не дублирует payload contract validation и не меняет ownership boundary.

---

# 3. Responsibility split

Эта correction уточняет одну формулировку `is-11-wave-scheduler-shape.md §8`.

Канонический split после correction:

```text
CognitiveScheduler
→ actual execution-origin binding:
   concrete scheduled ModuleId
   actual scheduler-created ModuleAttemptId
   ↕
   returned staged result identities

CommitCoordinator
→ staged transaction validation:
   active producer registration
   base StateRevision
   write authority/schema owner
   provenance against proposal/descriptor/logical time
   public/private proposal internal consistency
   stale/private revisions
   atomic publication
```

То есть `CommitCoordinator` не получает новый execution-request API и не должен угадывать origin, который ему не передан.

Не изменять `CommitCoordinator.commit()` signature ради этой correction.

Не переносить module execution или EvidenceRecorder внутрь coordinator.

---

# 4. Failure semantics

Binding mismatch является scheduler/wave validation failure **после successful physical compute, но до commit attempt**.

Поэтому exact O0 semantics:

```text
module_attempt_started(actual)
module_attempt_finished(actual, SUCCEEDED)
# binding validation fails
# no commit_attempted
# no commit_succeeded / commit_failed
cycle_failed
```

Причина:

- `module.compute()` действительно вернул `ModuleComputeResult`, поэтому compute attempt не переписывается задним числом в FAILED;
- commit boundary фактически не была вызвана, поэтому `commit_attempted` запрещён;
- public/private state current wave остаётся unchanged;
- earlier successful waves не rollback.

Cycle-level diagnostic должен быть deterministic `WaveExecutionError`-class/существующий typed runtime diagnostic с указанием wave/module и вида identity mismatch.

Если mismatches несколько, deterministic failure summary выбирается по canonical plan module order.

---

# 5. Required regression tests

Добавить минимум regression coverage:

1. module возвращает correct producer, но другой `StateUpdateProposal.module_attempt_id`, при этом provenance/internal proposal self-consistent с forged id:
   - `module_attempt_finished(SUCCEEDED)` существует для actual attempt;
   - no `commit_attempted`;
   - cycle FAILED;
   - public/private state unchanged для current wave;
   - `CommitId` не расходуется, поскольку coordinator не вызывается.

2. active modules возвращают results с producer identities, не совпадающими с actual concrete scheduled modules, но arranged так, чтобы producer set оставался unique и coordinator без scheduler binding мог бы принять transaction:
   - fail closed до commit;
   - no partial mutation;
   - canonical deterministic failure.

3. valid normal path:
   - `CommitAttemptedEvent.module_attempt_ids` и `CommitSucceededEvent.module_attempt_ids` совпадают exact tuple;
   - IDs относятся к actual scheduler-created attempts в canonical scheduled/producer order.

4. existing malformed provenance/base/private proposal scenarios по-прежнему доходят до `CommitCoordinator` и fail closed на его responsibility boundary; correction не должна превращать Scheduler в duplicate commit validator.

5. existing IS-09 atomicity и IS-11 same-base/failure/O0 tests не регрессируют.

---

# 6. Forbidden scope

Correction не должна:

- менять public `CognitiveModule`/`ModuleComputeRequest` contracts;
- менять `CommitCoordinator.commit()` signature;
- менять commit transaction pipeline/CommitId allocation semantics;
- добавлять retry/rebase/degradation;
- добавлять новый TraceEventKind;
- превращать successful physical compute в failed module attempt только из-за later binding validation;
- добавлять IS-12 reference modules;
- реализовывать Composition Root/KernelRuntime/Intervention;
- менять F31/ADR/version-wide semantics.

---

# 7. Verification

После correction выполнить targeted минимум:

```text
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked lint-imports
uv run --locked pytest \
  tests/integration/test_scheduler_wave_semantics.py \
  tests/property/test_same_base_wave.py \
  tests/integration/test_wave_failure_atomicity.py \
  tests/integration/test_scheduler_trace.py \
  tests/unit/test_wave_executor.py \
  tests/contract/test_commit_authority.py \
  tests/property/test_atomic_commit.py
```

Затем полный `FULL-C0` и `git diff --check`.

Следующий `V0.1-IS-12` остаётся CLOSED до correction push + independent re-audit + final acceptance `IS-11`.
