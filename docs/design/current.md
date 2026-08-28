# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какая implementation-работа разрешена следующей.

Operational workflow не хранится в истории чата. Его canonical entry points:

- [`../process/README.md`](../process/README.md) — durable handoff, роли, modes и acceptance lifecycle;
- [`../process/independent-audit.md`](../process/independent-audit.md) — independent implementation/correction audit;
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md) — opening next step и authoring copy-ready Codex instructions.

---

# 1. Общий статус

```text
Semantic Freeze Baseline F31: accepted
Version Roadmap DU-32: accepted
Current milestone: v0.1 Core Kernel
v0.1 exact design: accepted
v0.1 implementation-sequence: accepted
V0.1-IS-01 … V0.1-IS-10: accepted
V0.1-IS-11: CORRECTION REQUIRED
V0.1-IS-12+: CLOSED
```

`V0.1-IS-11 — WaveExecutor & Scheduler` implementation существует:

```text
e8aa2fa8528b2875c54c010de0777dd266e5bd49
feat(runtime): add wave executor and cognitive scheduler
```

Independent audit подтвердил основной scope/runtime design, local verification report и post-push GitHub Actions, но обнаружил blocking causal binding defect между фактически dispatched module attempt и identities, заявленными returned `ModuleComputeResult`.

Remote CI implementation commit:

```text
GitHub Actions run 33170740949
head e8aa2fa8528b2875c54c010de0777dd266e5bd49
Ubuntu Python 3.14: PASS
Windows Python 3.14: PASS
```

Green CI не закрывает найденный boundary defect.

Для defect принят correction clarification:

- [`../versions/v0.1/is-11-attempt-result-binding-correction.md`](../versions/v0.1/is-11-attempt-result-binding-correction.md).

Текущий verdict:

```text
CORRECTION-REQUIRED
V0.1-IS-11: not accepted
V0.1-IS-12: CLOSED
```

---

# 2. Канонические входные точки

Semantic baseline:

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md);
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md);
- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md).

Operational workflow:

- [`../process/README.md`](../process/README.md);
- [`../process/independent-audit.md`](../process/independent-audit.md);
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md).

Version-specific source of truth:

- [`../versions/v0.1/README.md`](../versions/v0.1/README.md) — accepted exact design;
- [`../versions/v0.1/implementation-sequence.md`](../versions/v0.1/implementation-sequence.md) — accepted dependency-ordered implementation plan;
- [`../versions/v0.1/is-06-contract-shape.md`](../versions/v0.1/is-06-contract-shape.md) — accepted clarification `IS-06`;
- [`../versions/v0.1/is-07-execution-plan-shape.md`](../versions/v0.1/is-07-execution-plan-shape.md) — accepted clarification `IS-07`;
- [`../versions/v0.1/is-07-controlled-construction-correction.md`](../versions/v0.1/is-07-controlled-construction-correction.md) — accepted correction `IS-07`;
- [`../versions/v0.1/is-08-private-state-store-shape.md`](../versions/v0.1/is-08-private-state-store-shape.md) — accepted clarification `IS-08`;
- [`../versions/v0.1/is-09-commit-coordinator-shape.md`](../versions/v0.1/is-09-commit-coordinator-shape.md) — accepted exact clarification `IS-09`;
- [`../versions/v0.1/is-09-active-boundary-consistency-correction.md`](../versions/v0.1/is-09-active-boundary-consistency-correction.md) — accepted correction clarification `IS-09`;
- [`../versions/v0.1/is-10-evidence-plane-shape.md`](../versions/v0.1/is-10-evidence-plane-shape.md) — accepted exact clarification `IS-10`;
- [`../versions/v0.1/is-11-wave-scheduler-shape.md`](../versions/v0.1/is-11-wave-scheduler-shape.md) — accepted exact clarification `IS-11`;
- [`../versions/v0.1/is-11-attempt-result-binding-correction.md`](../versions/v0.1/is-11-attempt-result-binding-correction.md) — accepted correction clarification текущего audit defect;
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md) — canonical operational prompt template, revision `CSPT-02`.

---

# 3. Implementation checkpoints

| Step | Статус | Implementation/correction |
|---|---|---|
| `IS-01` | accepted | bootstrap + correction `584db766...` |
| `IS-02` | accepted | `e457ada1...` |
| `IS-03` | accepted | `a5c9f314...` |
| `IS-04` | accepted | `86d38ff6...` + `afc1937b...` |
| `IS-05` | accepted | `df602abb...` |
| `IS-06` | accepted | `633babaf...` |
| `IS-07` | accepted | `c8852930...` + `5b60d001...` |
| `IS-08` | accepted | `92a2dd75...` |
| `IS-09` | accepted | `c11d79e7...` + clarification/correction `a4e99807...` / `978897ad...` |
| `IS-10` | accepted | `510aad6f...` |
| `IS-11` | correction required | implementation `e8aa2fa...`; correction pending |

---

# 4. Найденный IS-11 defect

Authoritative execution origin существует в Scheduler/Executor records:

```text
actual scheduled ModuleId
actual scheduler-created ModuleAttemptId
```

Но current implementation не подтверждает перед commit, что successful returned `StateUpdateProposal` сохраняет именно эти identities.

Поэтому возможна causal divergence:

```text
module_attempt_started(A)
module_attempt_finished(A, SUCCEEDED)
commit_attempted(A)

returned staged result claims attempt B

commit_succeeded(B)
```

и аналогичный producer spoof между active modules.

`CommitCoordinator` не может самостоятельно восстановить actual execution origin, потому что получает только `ModuleComputeResult`, а не execution request/record.

Correction фиксирует responsibility split:

```text
CognitiveScheduler
→ bind returned staged result to actual dispatched ModuleId/ModuleAttemptId

CommitCoordinator
→ validate staged transaction authority/provenance/revisions/atomicity
```

Binding mismatch должен fail closed после successful physical compute, но до actual commit call:

```text
module_attempt_finished(SUCCEEDED)
# no commit_attempted
cycle_failed
```

Current-wave public/private state не меняется; earlier successful waves не rollback.

---

# 5. Разрешённая текущая работа

Разрешена только минимальная correction текущего `IS-11` согласно:

- `is-11-wave-scheduler-shape.md`;
- `is-11-attempt-result-binding-correction.md`.

Нельзя:

- повторно реализовывать IS-11 целиком;
- менять `CommitCoordinator.commit()` signature;
- менять commit transaction pipeline;
- открывать или реализовывать IS-12;
- добавлять reference production modules;
- реализовывать Composition Root/KernelRuntime/Intervention;
- менять F31/ADR/version semantics.

После correction обязательны targeted regression, полный `FULL-C0`, push и новый independent audit correction diff.

---

# 6. VerificationObligations

До correction final acceptance предыдущие заявленные уровни IS-11 считаются **непринятыми audit gate**, даже при green tests/CI.

Ожидаемый уровень после successful correction + re-audit:

- `V01-001` — closed;
- `V01-002` — closed at runtime wave level;
- `V01-008` — runtime closed;
- `V01-009` — substantial;
- `V01-010` — closed.

`V01-009` полностью не закрывается до последующей composition/intervention producer integration.

---

# 7. Operational mode

```text
MODE-CORRECTION — V0.1-IS-11 attempt/result causal binding
```

`CSPT-02` остаётся применимым: verification/CI/reporting/commit policy не изменились.

Следующий step остаётся:

```text
V0.1-IS-12: CLOSED
```
