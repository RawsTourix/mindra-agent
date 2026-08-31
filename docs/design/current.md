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
V0.1-IS-01 … V0.1-IS-14: accepted
V0.1-IS-15: OPEN
V0.1-IS-16+: CLOSED
```

Последний accepted implementation step:

```text
V0.1-IS-14 — InterventionGateway
9b6ca91389dcd05653ef1d8e072fe75984090749
feat(runtime): add controlled state intervention gateway
```

Independent acceptance evidence:

```text
Targeted verification: PASS — 27 passed
FULL-C0 local: PASS — 350 passed
build: PASS
git diff --check: PASS
GitHub Actions run 33382166078
head 9b6ca91389dcd05653ef1d8e072fe75984090749
Ubuntu Python 3.14: PASS — 350 passed
Windows Python 3.14: PASS
AUDIT-PASS
```

VerificationObligations после IS-14:

- `V01-011` — closed;
- `V01-009` — intervention lineage extension substantial/closed for v0.1 intervention producer.

Overall `V01-009` final closure остаётся за deterministic end-to-end integration (`IS-15`) и version hardening (`IS-16`).

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
- [`../versions/v0.1/is-14-intervention-gateway-shape.md`](../versions/v0.1/is-14-intervention-gateway-shape.md);
- [`../versions/v0.1/is-15-cli-smoke-shape.md`](../versions/v0.1/is-15-cli-smoke-shape.md) — accepted exact clarification текущего step;
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
| `IS-14` | accepted | `9b6ca913...` |
| `IS-15` | OPEN | implementation not started |

---

# 4. Разрешённая текущая работа

Открыт ровно один feature coding step:

```text
V0.1-IS-15 — CLI & deterministic end-to-end smoke
```

Accepted exact clarification:

- [`../versions/v0.1/is-15-cli-smoke-shape.md`](../versions/v0.1/is-15-cli-smoke-shape.md).

Clarification фиксирует:

- exact `entrypoints/cli.py` + shared `main(argv)` boundary;
- stdlib argparse surface только `validate-profile --profile` и `kernel-smoke --profile`;
- standard argparse usage exit `2`;
- deterministic CLI factories через `NAMESPACE_URL` и fixed v0.1 seeds;
- `validate-profile` = full CompositionRoot validation без cognitive cycle;
- `kernel-smoke` = ровно один normal deterministic cycle;
- canonical success output lines;
- domain/config failures = stderr + exit `2` без traceback;
- normal smoke/internal failure = exit `1`;
- canonical reference output `waves=3 revision=3 join=10`;
- deterministic repeat normalization plan/state/O0 trace без physical timestamps;
- behavioral equivalence `mindra` и `python -m mindra`;
- subprocess installed-console tests внутри locked environment;
- запрет на duplicate assembly, new runtime semantics и stable SDK/output promises.

`V0.1-IS-16` и последующие steps остаются CLOSED.

---

# 5. VerificationObligations IS-15

Expected level после independent acceptance:

- `V01-009` — closed at deterministic v0.1 end-to-end O0 integration;
- `V01-013` — closed at deterministic runnable reference profile/CLI layer.

Final milestone acceptance/reconciliation остаётся за `IS-16` verification matrix/hardening.

---

# 6. Operational mode

```text
CSPT-02: applicable
MODE-INSTRUCTION — V0.1-IS-15 only
```

Codex не меняет этот status и не открывает `IS-16` самостоятельно.
