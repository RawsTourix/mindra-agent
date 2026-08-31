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
V0.1-IS-14: OPEN
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
- [`../versions/v0.1/is-14-intervention-gateway-shape.md`](../versions/v0.1/is-14-intervention-gateway-shape.md) — accepted exact clarification текущего step;
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
| `IS-14` | OPEN | implementation not started |

---

# 4. Разрешённая текущая работа

Открыт ровно один feature coding step:

```text
V0.1-IS-14 — InterventionGateway
```

Accepted exact clarification:

- [`../versions/v0.1/is-14-intervention-gateway-shape.md`](../versions/v0.1/is-14-intervention-gateway-shape.md).

Clarification фиксирует:

- exact contracts/runtime file split;
- only one-shot committed public `Available(value)` treatment in v0.1;
- exact `StateInterventionWrite` / `StateInterventionSpec` base revision+lineage+branch semantics;
- immutable exact-path `InterventionPolicy`, empty = disabled;
- no intervention settings in KernelProfile/composition fingerprint;
- `InterventionRecord` / `InterventionResult`;
- Gateway validation before identity allocation;
- exact `InterventionId -> LineageId -> BranchId` allocation order;
- treatment-derived lineage/branch without claiming paired exact counterfactual clone;
- semantic owner preservation and `evaluation.intervention` provenance;
- multi-target all-or-nothing public state publication;
- exact O0 order `intervention_applied -> state_revision_committed`;
- default-disabled CompositionRoot/KernelRuntime integration;
- between-cycle safe boundary and no cognitive capability leak;
- required contract/integration/state-machine verification.

`V0.1-IS-15` и последующие steps остаются CLOSED.

---

# 5. VerificationObligations IS-14

Expected level после independent acceptance:

- `V01-011` — closed;
- `V01-009` — intervention lineage extension substantial/closed for v0.1 intervention producer.

Overall `V01-009` final closure остаётся за final integration/hardening по implementation sequence.

---

# 6. Operational mode

```text
CSPT-02: applicable
MODE-INSTRUCTION — V0.1-IS-14 only
```

Codex не меняет этот status и не открывает следующий step самостоятельно.
