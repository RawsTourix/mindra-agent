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
V0.1-IS-01 … V0.1-IS-11: accepted
V0.1-IS-12: CLOSED — exact design clarification required
V0.1-IS-13+: CLOSED
```

`V0.1-IS-11 — WaveExecutor & Scheduler` принят после implementation + correction cycle.

Implementation:

```text
e8aa2fa8528b2875c54c010de0777dd266e5bd49
feat(runtime): add wave executor and cognitive scheduler
```

Accepted correction clarification:

- [`../versions/v0.1/is-11-attempt-result-binding-correction.md`](../versions/v0.1/is-11-attempt-result-binding-correction.md).

Correction implementation:

```text
a0cc9deae5b35779ffc42d351ed26dea5de30120
fix(runtime): bind staged results to module attempts
```

Final independent correction audit подтвердил:

- Scheduler fail-closed связывает returned staged result с actual dispatched `ModuleId` и scheduler-created `ModuleAttemptId` до `commit_attempted`;
- binding mismatch сохраняет `module_attempt_finished(SUCCEEDED)`, не вызывает `CommitCoordinator` и завершает cycle через deterministic `WaveExecutionError`;
- forged attempt identity не расходует `CommitId` и не мутирует current-wave public/private state;
- forged producer identity отклоняется deterministic canonical order до commit boundary;
- valid path сохраняет exact equality `CommitAttemptedEvent.module_attempt_ids == CommitSucceededEvent.module_attempt_ids == actual scheduler-created attempt IDs`;
- malformed provenance/base/private proposal остаётся responsibility `CommitCoordinator` и по-прежнему проходит `commit_attempted -> commit_failed -> cycle_failed`;
- `CommitCoordinator.commit()` API/transaction pipeline не менялись;
- correction diff ограничен Scheduler + focused regression tests.

Verification evidence:

```text
Targeted verification: PASS — 36 passed
FULL-C0 local: PASS — 281 passed
build: PASS
git diff --check: PASS
GitHub Actions run 33183260302
head a0cc9deae5b35779ffc42d351ed26dea5de30120
Ubuntu Python 3.14: PASS
Windows Python 3.14: PASS
```

Final verdict:

```text
AUDIT-PASS
V0.1-IS-11: accepted
```

VerificationObligations на предусмотренном `IS-11` уровне:

- `V01-001` — closed;
- `V01-002` — closed at runtime wave level;
- `V01-008` — runtime closed;
- `V01-009` — substantial;
- `V01-010` — closed.

`V01-009` полностью не закрывается до последующей composition/intervention producer integration.

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
- [`../versions/v0.1/is-11-attempt-result-binding-correction.md`](../versions/v0.1/is-11-attempt-result-binding-correction.md) — accepted correction clarification `IS-11`;
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
| `IS-11` | accepted | `e8aa2fa...` + correction `a0cc9dea...` |
| `IS-12` | CLOSED — clarification required | implementation not started |

---

# 4. Transition gate перед `V0.1-IS-12`

Следующий по accepted sequence:

```text
V0.1-IS-12 — Reference synthetic modules
```

Accepted sequence и version design уже фиксируют semantic graph:

```text
synthetic.source
       ↓
 ┌─────┴─────┐
 ↓           ↓
synthetic.double
synthetic.triple
 └─────┬─────┘
       ↓
synthetic.join
```

Expected waves:

```text
Wave 0: source
Wave 1: double | triple
Wave 2: join
```

И example behavior для configured source value `2`:

```text
double = 4
triple = 6
join = 10
```

Однако перед coding остаются implementation-level choices, которые нельзя оставлять Codex на самостоятельный выбор. Требуется exact clarification минимум для:

- public package/file layout `mindra.reference`;
- exact constructor/API каждого reference module;
- canonical `ModuleId`, `ImplementationId`, `ImplementationRevision`;
- exact StatePath/StateKey graph для source/double/triple/join;
- exact ReadSpec freshness/required semantics;
- exact descriptors/writes/traits;
- immutable source settings/value validation;
- exact proposal/provenance construction через `ModuleComputeRequest.context`;
- join input ordering/operation semantics;
- public exports;
- architecture rule `reference` imports contracts only and never runtime/composition/entrypoints;
- tests, including graph compatibility with existing `ExecutionPlanCompiler` without prematurely implementing Composition Root (`IS-13`).

Текущий mode:

```text
MODE-DESIGN — V0.1-IS-12 exact clarification
```

До принятия clarification:

```text
V0.1-IS-12: CLOSED
V0.1-IS-13+: CLOSED
```

---

# 5. Разрешённая текущая работа

Разрешена только документационная/design работа внутри accepted `v0.1` semantics:

```text
V0.1-IS-12 exact clarification
```

Нельзя:

- начинать production `mindra.reference` implementation до accepted clarification;
- реализовывать Composition Root/KernelRuntime/profile parsing (`IS-13`);
- реализовывать Intervention (`IS-14`);
- менять F31/ADR/version semantics;
- открывать `IS-13`.

---

# 6. Operational prompt

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

`CSPT-02` остаётся применимым, но `MODE-INSTRUCTION` для `IS-12` разрешён только после принятия exact clarification и явного открытия step в этом файле.
