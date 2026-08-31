# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какая implementation-работа разрешена следующей.

Operational workflow:

- [`../process/README.md`](../process/README.md);
- [`../process/independent-audit.md`](../process/independent-audit.md);
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md).

---

# 1. Общий статус

```text
Semantic Freeze Baseline F31: accepted
Version Roadmap DU-32: accepted
Current milestone: v0.1 Core Kernel
v0.1 exact design: accepted
v0.1 implementation-sequence: accepted
V0.1-IS-01 … V0.1-IS-13: accepted
V0.1-IS-14: CLOSED — exact design clarification required
V0.1-IS-15+: CLOSED
```

Последний accepted implementation step:

```text
V0.1-IS-13 — Configuration & Composition Root
b2be887c7238d8d97a99f1b550e7ba73da9e6323
feat(composition): add configuration and composition root
```

Independent acceptance evidence:

```text
Targeted verification: PASS — 33 passed
FULL-C0 local: PASS — 330 passed
build: PASS
git diff --check: PASS
GitHub Actions run 33376628360
head b2be887c7238d8d97a99f1b550e7ba73da9e6323
Ubuntu Python 3.14: PASS
Windows Python 3.14: PASS
AUDIT-PASS
```

Final audit подтвердил:

- strict immutable `mindra.kernel-profile/v1` TOML parsing;
- canonical reference profile `ProfileId("v0_1.reference")`;
- immutable explicit `ImplementationRegistry` без global/import-time registration;
- strict reference factory settings validation;
- deterministic normalized SHA-256 composition fingerprint;
- schema-complete initial `CognitiveState` с revision 0 и `Unknown` fields;
- initial runtime-boundary provenance `composition.initial_state`;
- explicit `CompositionRoot` как единственную assembly boundary;
- narrow `KernelRuntime.run_cycle()` с новым `CognitiveCycleId` на cycle и pinned outer scopes;
- failed later wave сохраняет earlier committed state в facade;
- root evidence exact order `composition_resolved -> plan_compiled`;
- reference runtime реально исполняет `2 -> 4/6 -> 10`;
- runtime/reference не импортируют composition, global Service Locator отсутствует.

VerificationObligations после IS-13:

- `V01-007` — composition integration;
- `V01-012` — closed architecture/composition semantics;
- `V01-013` — substantial.

`V01-013` fully closed только после deterministic CLI smoke (`IS-15`) и final hardening.

---

# 2. Canonical entry points

Semantic baseline:

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md);
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md);
- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md).

Version-specific:

- [`../versions/v0.1/README.md`](../versions/v0.1/README.md);
- [`../versions/v0.1/implementation-sequence.md`](../versions/v0.1/implementation-sequence.md);
- [`../versions/v0.1/is-06-contract-shape.md`](../versions/v0.1/is-06-contract-shape.md);
- [`../versions/v0.1/is-07-execution-plan-shape.md`](../versions/v0.1/is-07-execution-plan-shape.md);
- [`../versions/v0.1/is-07-controlled-construction-correction.md`](../versions/v0.1/is-07-controlled-construction-correction.md);
- [`../versions/v0.1/is-08-private-state-store-shape.md`](../versions/v0.1/is-08-private-state-store-shape.md);
- [`../versions/v0.1/is-09-commit-coordinator-shape.md`](../versions/v0.1/is-09-commit-coordinator-shape.md);
- [`../versions/v0.1/is-09-active-boundary-consistency-correction.md`](../versions/v0.1/is-09-active-boundary-consistency-correction.md);
- [`../versions/v0.1/is-10-evidence-plane-shape.md`](../versions/v0.1/is-10-evidence-plane-shape.md);
- [`../versions/v0.1/is-11-wave-scheduler-shape.md`](../versions/v0.1/is-11-wave-scheduler-shape.md);
- [`../versions/v0.1/is-11-attempt-result-binding-correction.md`](../versions/v0.1/is-11-attempt-result-binding-correction.md);
- [`../versions/v0.1/is-12-reference-synthetic-shape.md`](../versions/v0.1/is-12-reference-synthetic-shape.md);
- [`../versions/v0.1/is-13-composition-root-shape.md`](../versions/v0.1/is-13-composition-root-shape.md);
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

---

# 3. Implementation checkpoints

| Step | Status | Implementation/correction |
|---|---|---|
| `IS-01` | accepted | bootstrap + correction `584db766...` |
| `IS-02` | accepted | `e457ada1...` |
| `IS-03` | accepted | `a5c9f314...` |
| `IS-04` | accepted | `86d38ff6...` + `afc1937b...` |
| `IS-05` | accepted | `df602abb...` |
| `IS-06` | accepted | `633babaf...` |
| `IS-07` | accepted | `c8852930...` + correction `5b60d001...` |
| `IS-08` | accepted | `92a2dd75...` |
| `IS-09` | accepted | `c11d79e7...` + correction `978897ad...` |
| `IS-10` | accepted | `510aad6f...` |
| `IS-11` | accepted | `e8aa2fa...` + correction `a0cc9dea...` |
| `IS-12` | accepted | `39f48959...` |
| `IS-13` | accepted | `b2be887c...` |
| `IS-14` | CLOSED — clarification required | implementation not started |

---

# 4. Transition gate перед `V0.1-IS-14`

Следующий по accepted implementation sequence:

```text
V0.1-IS-14 — InterventionGateway
```

Accepted design уже фиксирует крупные semantics:

- interventions default disabled в reference runtime;
- research/test runtime использует explicit allowlist;
- intervention применяется только к committed safe boundary;
- schema/value validation сохраняется;
- public intervention создаёт новую committed `StateRevision`;
- semantic owner StateField не меняется;
- provenance явно содержит `InterventionId` и не masquerade как natural module write;
- Evidence Plane получает `intervention_applied`;
- arbitrary private-state mutation отсутствует.

Перед coding требуется exact clarification минимум для:

- physical contracts/runtime file split;
- exact `StateInterventionSpec` fields и construction invariants;
- exact `InterventionPolicy` / allowlist representation и default-disabled behavior;
- exact `InterventionGateway` constructor/public method surface;
- ownership `InterventionId` и shared `IdFactory` integration;
- exact accepted committed-state base/freshness validation;
- target-path canonicalization, duplicates и multi-write atomicity;
- exact intervention provenance `StateProvenance` fields/source/parent/intervention refs;
- exact result/record shapes и revision semantics;
- exact `InterventionAppliedEvent` timing/payload ordering;
- integration boundary с `KernelRuntime` без cognitive module capability leak;
- failure behavior и no-partial-publication guarantee;
- tests/state-machine coverage и reference runtime disabled path.

Текущий mode:

```text
MODE-DESIGN — V0.1-IS-14 exact clarification
```

До принятия clarification:

```text
V0.1-IS-14: CLOSED
V0.1-IS-15+: CLOSED
```

---

# 5. Разрешённая текущая работа

Разрешена только documentation/design работа внутри accepted v0.1 semantics:

```text
V0.1-IS-14 exact clarification
```

Нельзя:

- начинать production InterventionGateway implementation до accepted clarification;
- реализовывать CLI (`IS-15`);
- менять F31/ADR/version semantics;
- открывать `IS-15`.

---

# 6. Operational mode

Canonical template:

- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

`CSPT-02` остаётся применимым, но `MODE-INSTRUCTION` для `IS-14` разрешён только после accepted exact clarification и явного открытия step в этом файле.
