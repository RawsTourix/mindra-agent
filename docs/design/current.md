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
V0.1-IS-11: OPEN
V0.1-IS-12+: CLOSED
```

Общий архитектурный цикл `DU-00 … DU-32` завершён и принят.

`V0.1-IS-10 — O0 Evidence Plane` принят после independent audit implementation commit:

```text
510aad6f5dd98c572ff4cf832e72a469ecd4ebc5
feat(evidence): add passive O0 evidence plane
```

Final audit подтвердил:

- scope только `IS-10`, без leakage в Scheduler/Composition/Intervention;
- exact 13 typed O0 payload variants и derived `TraceEventKind`;
- immutable `TraceEventEnvelope` и structural helper records;
- passive `EvidenceRecorder` Protocol;
- append-only process-local `InMemoryEvidenceRecorder`;
- evidence/cognition isolation и отсутствие automatic producer emission;
- targeted verification `PASS`, `30 passed`;
- полный local `FULL-C0`: `PASS`, полный suite `260 passed`;
- build: `PASS`;
- GitHub Actions run `33166873106`, exact head `510aad6f5dd98c572ff4cf832e72a469ecd4ebc5`, event `push`: `PASS`;
- Ubuntu `FULL-C0 (ubuntu-latest, Python 3.14)`: `PASS`;
- Windows `FULL-C0 (windows-latest, Python 3.14)`: `PASS`.

Verdict:

```text
AUDIT-PASS
V0.1-IS-10: accepted
```

VerificationObligations на предусмотренном `IS-10` уровне:

- `V01-009` — `foundation`;
- `V01-010` — `substantial`.

Полное закрытие этих obligations остаётся за последующей runtime producer integration согласно accepted sequence.

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
- [`../versions/v0.1/is-11-wave-scheduler-shape.md`](../versions/v0.1/is-11-wave-scheduler-shape.md) — accepted exact clarification текущего `IS-11`;
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
| `IS-11` | OPEN | implementation not started |

---

# 4. Разрешённая текущая работа

Открыт ровно один feature coding step:

```text
V0.1-IS-11 — WaveExecutor & Scheduler
```

Prerequisites `IS-01 … IS-10` приняты.

Для `IS-11` принят exact clarification:

- [`../versions/v0.1/is-11-wave-scheduler-shape.md`](../versions/v0.1/is-11-wave-scheduler-shape.md).

Clarification фиксирует:

- exact runtime forms `ModuleAttemptExecutionRequest`, `ModuleAttemptRecord`, `WaveExecutor`, `SequentialWaveExecutor`, `CycleExecutionOutcome`, `CycleExecutionResult`, `CognitiveScheduler`;
- caller-owned `CognitiveCycleId` и scheduler-owned `WaveId`/`WaveAttemptId`/`ModuleAttemptId`;
- same-base public snapshot и pre-wave own-private snapshot pinning;
- current-wave logical time для `StateProjection`/`CURRENT_CYCLE` freshness;
- narrow refinement `IS-09` temporal compatibility: new cycle commit может использовать новый `cognitive_cycle_id` под тем же run/session/episode/decision context без fake public revision;
- exact active plan/module/private-store/commit-coordinator binding;
- exact deterministic O0 ordering и producer ownership;
- failure semantics: module failure -> no commit; commit failure -> no state transition; earlier successful waves не rollback;
- отсутствие retries/degradation/parallel executor/Composition Root/reference modules/intervention в этом step.

Перед implementation обязательны section `V0.1-IS-11` в `implementation-sequence.md`, exact clarification и перечисленные там canonical design/ADR.

Targeted verification минимум:

```text
tests/integration/test_scheduler_wave_semantics.py
tests/property/test_same_base_wave.py
tests/integration/test_wave_failure_atomicity.py
tests/integration/test_scheduler_trace.py
```

После targeted green обязателен `FULL-C0` и `git diff --check`.

`V0.1-IS-12` и последующие steps остаются CLOSED.

---

# 5. VerificationObligations текущего step

Ожидаемый уровень после accepted `IS-11`:

- `V01-001` — closed;
- `V01-002` — closed at runtime wave level;
- `V01-008` — runtime closed;
- `V01-009` — substantial;
- `V01-010` — closed.

`V01-009` полностью не закрывается до последующей composition/intervention producer integration.

---

# 6. Operational prompt

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

Applicability check после принятия `IS-11` clarification:

- verification semantics не изменились;
- CI semantics не изменились;
- reporting fields не изменились;
- commit/push policy не изменился;
- mandatory source-of-truth paths сохраняются;
- step-specific exact API/invariants полностью добавляются поверх template через clarification.

Результат:

```text
CSPT-02: applicable
MODE-INSTRUCTION разрешён только для V0.1-IS-11
```

Codex не открывает следующий implementation step самостоятельно.

---

# 7. Ограничения

- не переходить к `V0.1-IS-12` до independent acceptance `IS-11`;
- не реализовывать `mindra.reference` production graph заранее;
- не реализовывать Composition Root/KernelRuntime/Intervention Gateway в `IS-11`;
- implementation-level correction допустима только внутри accepted `v0.1` semantics;
- semantic blocker требует design review и нового ADR/freeze update;
- Codex не меняет самостоятельно accepted version design/F31 и не открывает следующий implementation step;
- live current status не дублировать в `AGENTS.md`, `docs/README.md` или `docs/versions/README.md`.
