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
V0.1-IS-11: CLOSED — exact design clarification required
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
| `IS-11` | CLOSED — clarification required | implementation not started |

---

# 4. Transition gate перед `V0.1-IS-11`

Следующий по accepted sequence:

```text
V0.1-IS-11 — WaveExecutor & Scheduler
```

Prerequisites implementation уровня `IS-01 … IS-10` приняты, однако `IS-11` **пока не открыт для coding**.

При обязательной ambiguity-проверке `MODE-TRANSITION` установлено, что current accepted docs недостаточно точно фиксируют implementation boundary Scheduler/WaveExecutor. До Codex coding нужен step-specific exact clarification минимум для:

- public/internal API `WaveExecutor`, `SequentialWaveExecutor`, `CognitiveScheduler` и cycle result/attempt records;
- ownership concrete module instances относительно compiled `ExecutionPlan`;
- allocation/ownership `CognitiveCycleId`, `WaveId`, `WaveAttemptId`, `ModuleAttemptId`;
- exact same-base snapshot capture и private snapshot pinning;
- executor vs scheduler responsibility за request construction, exception capture и result ordering;
- exact O0 event ordering на cycle/wave/module/commit boundaries;
- failure path: какие events существуют при module failure и commit failure;
- validation active module/plan composition до execution;
- boundary последовательных cognitive cycles.

Особенно важно разрешить temporal boundary: accepted `IS-09` commit clarification сейчас запрещает менять уже установленный `cognitive_cycle_id` base state внутри commit и прямо отмечает, что lifecycle/reset semantics не входят в `IS-09`. `IS-11` должен определить корректный переход между distinct cognitive cycles, не создавая второй `CognitiveState` с тем же `StateRevision` и другой temporal identity и не нарушая ADR-0003/ADR-0004. Если для этого потребуется минимальная correction `IS-09`, она должна быть спроектирована и принята до implementation `IS-11`.

Текущий mode:

```text
MODE-DESIGN — V0.1-IS-11 exact clarification
```

До принятия clarification:

```text
V0.1-IS-11: CLOSED
V0.1-IS-12+: CLOSED
```

Нельзя выдавать Codex implementation prompt на `IS-11` раньше этого gate.

---

# 5. Разрешённая текущая работа

Разрешена только документационная/design работа внутри accepted `v0.1` semantics:

```text
V0.1-IS-11 exact clarification
+
при необходимости minimal prerequisite correction clarification
```

Новый feature coding step сейчас не открыт.

Нельзя:

- начинать Scheduler/WaveExecutor implementation;
- изменять F31 без semantic design review;
- открывать `IS-12`;
- объединять clarification и feature implementation в один Codex task.

---

# 6. Operational prompt

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

`CSPT-02` остаётся применимым, но Codex implementation instruction для `IS-11` появится только после закрытия текущего `MODE-DESIGN` gate и явного открытия `IS-11` в этом файле.
