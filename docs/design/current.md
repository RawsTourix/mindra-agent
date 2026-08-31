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
V0.1-IS-01 … V0.1-IS-15: accepted
V0.1-IS-16: OPEN — Version acceptance hardening
v0.1 milestone acceptance: NOT YET
```

Последний accepted feature implementation step:

```text
V0.1-IS-15 — CLI & deterministic end-to-end smoke
657b8140e82f73dae14878ada8d788f03069c5cc
feat(cli): add deterministic kernel smoke commands
```

Independent acceptance evidence:

```text
Targeted verification: PASS — 12 passed
FULL-C0 local: PASS — 362 passed
build: PASS
git diff --check: PASS
GitHub Actions run 33405884901
head 657b8140e82f73dae14878ada8d788f03069c5cc
Ubuntu Python 3.14: PASS — 362 passed
Windows Python 3.14: PASS
AUDIT-PASS
```

Final IS-15 audit подтвердил:

- thin stdlib argparse entrypoint поверх public Composition Root/runtime API;
- exact commands `validate-profile --profile` и `kernel-smoke --profile`;
- identical console-script / `python -m mindra` behavior;
- fixed deterministic CLI identity seeds;
- full CompositionRoot validation без cognitive cycle для `validate-profile`;
- ровно один reference cognitive cycle для `kernel-smoke`;
- canonical output `waves=3 revision=3 join=10`;
- expected domain/usage/internal exit semantics без traceback;
- deterministic repeat по semantic plan, state payload/revisions и normalized O0 `(kind, logical_time, payload)` sequence;
- installed console script реально проверяется subprocess test внутри locked environment;
- entrypoints не собирают modules/runtime internals вручную и не создают Service Locator/global registry.

VerificationObligations после IS-15:

- `V01-009` — closed at deterministic v0.1 end-to-end O0 integration;
- `V01-013` — closed at deterministic runnable reference profile/CLI layer.

Final reconciliation всех `V01-001 … V01-014` и milestone acceptance выполняется только через `IS-16` + independent final audit.

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
- [`../versions/v0.1/is-15-cli-smoke-shape.md`](../versions/v0.1/is-15-cli-smoke-shape.md);
- [`../versions/v0.1/is-16-acceptance-hardening-shape.md`](../versions/v0.1/is-16-acceptance-hardening-shape.md) — accepted exact clarification текущего step;
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
| `IS-15` | accepted | `657b8140...` |
| `IS-16` | OPEN | acceptance hardening only |

---

# 4. Разрешённая текущая работа

Открыт ровно один final hardening step:

```text
V0.1-IS-16 — Version acceptance hardening
```

Accepted exact clarification:

- [`../versions/v0.1/is-16-acceptance-hardening-shape.md`](../versions/v0.1/is-16-acceptance-hardening-shape.md).

Clarification фиксирует:

- exact schema/status vocabulary `verification-matrix.md`;
- canonical mapping `V01-001 … V01-014` к tests/commands;
- repository acceptance-scope architecture test;
- mechanical zero-third-party runtime dependency audit;
- clean built-wheel install/smoke в fresh temp Python 3.14 venv;
- extension existing Linux/Windows CI теми же artifact/CLI gates;
- language policy manual-review boundary;
- future cognitive responsibility scope audit;
- minimal-defect-only correction rule;
- `V01-014 = PENDING-CI` до exact post-push candidate run;
- запрет Codex самостоятельно принимать milestone.

Новые features в IS-16 запрещены.

---

# 5. VerificationObligations IS-16

До operator push ожидаемый Codex handoff:

```text
V01-001 … V01-013: PASS
V01-014: PENDING-CI
Post-push CI: PENDING
v0.1 milestone acceptance: NOT YET
```

После operator push independent ChatGPT final audit обязан проверить exact candidate SHA на Ubuntu/Windows и только затем может:

```text
V01-014 -> PASS
V01-001 … V01-014 -> PASS
V0.1-IS-16 -> accepted
v0.1 Core Kernel -> implemented/accepted
```

`v0.2` автоматически не открывается.

---

# 6. Operational mode

```text
CSPT-02: applicable
MODE-INSTRUCTION — V0.1-IS-16 only
```

Codex не меняет этот status и не объявляет milestone accepted самостоятельно.
