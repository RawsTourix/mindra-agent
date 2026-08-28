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
V0.1-IS-12: OPEN
V0.1-IS-13+: CLOSED
```

`V0.1-IS-11 — WaveExecutor & Scheduler` принят после implementation + correction cycle.

Implementation:

```text
e8aa2fa8528b2875c54c010de0777dd266e5bd49
feat(runtime): add wave executor and cognitive scheduler
```

Correction implementation:

```text
a0cc9deae5b35779ffc42d351ed26dea5de30120
fix(runtime): bind staged results to module attempts
```

Final verification evidence:

```text
Targeted correction verification: PASS — 36 passed
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
- [`../versions/v0.1/is-12-reference-synthetic-shape.md`](../versions/v0.1/is-12-reference-synthetic-shape.md) — accepted exact clarification текущего `IS-12`;
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
| `IS-12` | OPEN | implementation not started |

---

# 4. Разрешённая текущая работа

Открыт ровно один feature coding step:

```text
V0.1-IS-12 — Reference synthetic modules
```

Prerequisites `IS-01 … IS-11` приняты.

Для `IS-12` принят exact clarification:

- [`../versions/v0.1/is-12-reference-synthetic-shape.md`](../versions/v0.1/is-12-reference-synthetic-shape.md).

Clarification фиксирует:

- production split `mindra.reference.synthetic`;
- exact classes `SyntheticSourceModule`, `SyntheticDoubleModule`, `SyntheticTripleModule`, `SyntheticJoinModule`;
- canonical ModuleIds `synthetic.source/double/triple/join`;
- canonical ImplementationIds `reference.synthetic_*.v1` и `ImplementationRevision("v1")`;
- exact int StateKeys `synthetic.*.value`;
- source immutable constructor setting `value: int`;
- stateless deterministic `COGNITIVE_CYCLE` descriptors;
- `CURRENT_CYCLE`, required, `Available`-only dependencies;
- exact arithmetic `source`, `*2`, `*3`, `double+triple`;
- ordinary staged proposals/provenance built only from `ModuleComputeRequest.context`;
- reference → contracts-only production dependency;
- graph proof through existing `ExecutionPlanCompiler` without production Composition Root.

Expected plan:

```text
Wave 0: synthetic.source
Wave 1: synthetic.double | synthetic.triple
Wave 2: synthetic.join
```

For source `2`:

```text
source = 2
double = 4
triple = 6
join = 10
```

Required tests минимум:

```text
tests/contract/test_reference_modules.py
tests/architecture/test_reference_independence.py
tests/integration/test_reference_plan.py
```

После targeted green обязателен полный `FULL-C0` и `git diff --check`.

`V0.1-IS-13` и последующие steps остаются CLOSED.

---

# 5. VerificationObligations текущего step

Ожидаемый уровень после accepted `IS-12`:

- `V01-012` — closed at reference/runtime independence layer;
- `V01-013` — foundation.

`V01-013` fully closed не считается до configured runnable reference profile/Composition Root из `IS-13`.

---

# 6. Operational mode

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

Applicability check:

- verification semantics не изменились;
- CI semantics не изменились;
- reporting fields не изменились;
- commit/push policy не изменился;
- step-specific exact API/invariants добавлены clarification поверх template.

Результат:

```text
CSPT-02: applicable
MODE-INSTRUCTION разрешён только для V0.1-IS-12
```

Codex не открывает следующий implementation step самостоятельно.

---

# 7. Ограничения

- не переходить к `V0.1-IS-13` до independent acceptance `IS-12`;
- не реализовывать Configuration/Composition Root/KernelRuntime/profile TOML заранее;
- не создавать production registry/factory/schema builder в `IS-12`;
- не реализовывать Intervention/CLI;
- implementation-level correction допустима только внутри accepted `v0.1` semantics;
- semantic blocker требует design review и нового ADR/freeze update;
- Codex не меняет самостоятельно accepted version design/F31 и не открывает следующий implementation step;
- live current status не дублировать в `AGENTS.md`, `docs/README.md` или `docs/versions/README.md`.
