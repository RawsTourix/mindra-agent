# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический live status проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какая implementation-работа разрешена следующей.

Operational workflow:

- [`../process/README.md`](../process/README.md);
- [`../process/independent-audit.md`](../process/independent-audit.md);
- [`../process/codex-instruction-authoring.md`](../process/codex-instruction-authoring.md).

---

# 1. Общий статус

```text
Semantic Freeze Baseline F31: accepted
Version Roadmap DU-32: accepted

v0.1 Core Kernel design: accepted
v0.1 implementation-sequence: accepted
V0.1-IS-01 … V0.1-IS-16: accepted
V01-001 … V01-014: PASS
v0.1 Core Kernel: implemented / independently audited / accepted

v0.2 MicroWorld Interaction design: accepted
v0.2 implementation-sequence: accepted
V0.2-IS-01: OPEN
V0.2-IS-02 … V0.2-IS-14: CLOSED
v0.2 implementation: active, no accepted implementation step yet
```

Одновременно `OPEN` только один implementation step.

---

# 2. Immutable historical boundary v0.1

Final accepted implementation candidate:

```text
3c1ec7f746c040ca49f232c12e5c9ba7bf28e597
test(v0.1): add final acceptance hardening
```

Final independent acceptance evidence:

```text
Local FULL-C0: PASS — 366 passed
ruff: PASS
format: PASS — 243 files
mypy: PASS — 91 source files
Import Linter: PASS — 3 kept / 0 broken
canonical validate-profile: PASS
canonical kernel-smoke: PASS — waves=3 revision=3 join=10
clean wheel metadata/install verification: PASS
third-party runtime dependencies: 0
future-responsibility scope audit: PASS
language policy review: PASS
GitHub Actions run 33424412605
exact implementation head 3c1ec7f746c040ca49f232c12e5c9ba7bf28e597
Ubuntu Python 3.14: PASS — 366 passed — clean wheel PASS
Windows Python 3.14: PASS — 366 passed — clean wheel PASS
AUDIT-PASS
```

Canonical detailed evidence:

- [`../versions/v0.1/verification-matrix.md`](../versions/v0.1/verification-matrix.md).

Post-v0.1 documentation consistency cleanup завершён без изменения F31, roadmap, v0.1 code или accepted semantics.

Рекомендуемый immutable tag target **до добавления v0.2 design**:

```text
b6910164fba150a6bf69e05d385827fb4fe064ac
```

Tag name:

```text
v0.1.0
```

Tag не является GitHub Release и не разрешает publication.

---

# 3. Canonical entry points

Semantic baseline:

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md);
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md);
- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md).

Roadmap/version governance:

- [`version-roadmap.md`](version-roadmap.md);
- [`../versions/README.md`](../versions/README.md);
- [`../versions/codex-step-prompt-template.md`](../versions/codex-step-prompt-template.md), revision `CSPT-02`.

Accepted historical `v0.1`:

- [`../versions/v0.1/README.md`](../versions/v0.1/README.md);
- [`../versions/v0.1/implementation-sequence.md`](../versions/v0.1/implementation-sequence.md);
- [`../versions/v0.1/verification-matrix.md`](../versions/v0.1/verification-matrix.md);
- accepted clarification/correction docs in `docs/versions/v0.1/`.

Accepted current `v0.2` design:

- [`../versions/v0.2/README.md`](../versions/v0.2/README.md);
- [`../versions/v0.2/implementation-sequence.md`](../versions/v0.2/implementation-sequence.md).

Canonical owners/contracts обязательные для v0.2:

- `DU-03` Runtime / Temporal Model;
- `DU-04` CognitiveState;
- `DU-05` Module Lifecycle;
- `DU-06` Observability / Intervention;
- `DU-07` Environment;
- `DU-08` Perception;
- `DU-09` Goals;
- `DU-23` Policy / Planner;
- `DU-24` Action Boundary;
- `DU-25` Experience / Data / Replay;
- соответствующие ADR и semantic contracts.

---

# 4. Historical implementation checkpoints v0.1

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
| `IS-16` | accepted | `3c1ec7f7...` |

---

# 5. VerificationObligations v0.1

```text
V01-001: PASS
V01-002: PASS
V01-003: PASS
V01-004: PASS
V01-005: PASS
V01-006: PASS
V01-007: PASS
V01-008: PASS
V01-009: PASS
V01-010: PASS
V01-011: PASS
V01-012: PASS
V01-013: PASS
V01-014: PASS
```

`v0.1` acceptance scope ограничен Core Kernel и не означает реализацию Environment, Cortex, Memory, learning или других roadmap responsibilities.

---

# 6. Accepted v0.2 exact design gate

`v0.2` принято проектировать/реализовывать как:

```text
custom stdlib-only symbolic MicroWorld
strict Agent Interaction Plane / Research Plane capability split
InteractionRuntime owns external Agent↔Environment lifecycle
KernelRuntime owns internal Agent execution
CognitiveScheduler remains COGNITIVE_CYCLE-only
LifecycleCoordinator handles EPISODE_START / POST_OUTCOME module phases
runtime-owned CognitiveState ingress через separate BoundaryCommitCoordinator
structured deterministic CanonicalPercept
external-task-only Goal System subset
deterministic Reference Policy, no Planner
post-authorization pre-dispatch Action Commit
explicit definite failure / execution_unknown / reconciliation semantics
append-only typed InMemoryExperienceJournal
FULL-C0-v0.2 on Ubuntu + Windows / Python 3.14 / CPU-only
```

Runtime third-party dependency target:

```text
0
```

No F31 change/ADR required by accepted design.

---

# 7. VerificationObligations v0.2

Current obligations defined by accepted version design:

```text
V02-001 — Canonical trajectory determinism
V02-002 — Environment snapshot continuation
V02-003 — Agent/Research plane isolation
V02-004 — Session/Episode lifecycle
V02-005 — Decision Window multiplicity
V02-006 — Correct outcome lineage
V02-007 — Percept boundary
V02-008 — Goal authority/lifecycle
V02-009 — Policy isolation
V02-010 — Action causal separation
V02-011 — Action failure taxonomy
V02-012 — No blind retry / immutable post-commit history
V02-013 — Journal append-only lineage
V02-014 — Research annotation isolation
V02-015 — Termination/truncation/reset semantics
V02-016 — Scope negative gate
V02-017 — Build/install/CI reproducibility
```

Ни одна `V02-*` пока не имеет final PASS status; coverage наращивается по implementation sequence и закрывается `V0.2-IS-14`.

---

# 8. v0.2 implementation checkpoints

| Step | Status | Result |
|---|---|---|
| `V0.2-IS-01` | **OPEN** | Interaction temporal & boundary-state foundation |
| `V0.2-IS-02` | CLOSED | Lifecycle phases & KernelRuntime context bridge |
| `V0.2-IS-03` | CLOSED | Environment contracts & capability split |
| `V0.2-IS-04` | CLOSED | Deterministic MicroWorld core, MW0 & snapshot |
| `V0.2-IS-05` | CLOSED | Controlled task families & hidden-rule controls |
| `V0.2-IS-06` | CLOSED | Structured Perception |
| `V0.2-IS-07` | CLOSED | External-task Goal System subset |
| `V0.2-IS-08` | CLOSED | Deterministic Reference Policy |
| `V0.2-IS-09` | CLOSED | Action Boundary, dispatch & reconciliation |
| `V0.2-IS-10` | CLOSED | Append-only Experience Journal |
| `V0.2-IS-11` | CLOSED | InteractionRuntime vertical orchestration |
| `V0.2-IS-12` | CLOSED | v0.2 Composition Root & interaction profile |
| `V0.2-IS-13` | CLOSED | CLI, clean artifact & CI profile |
| `V0.2-IS-14` | CLOSED | Version acceptance hardening |

`CLOSED` означает запрещённую implementation work до отдельного transition после audit предыдущего step.

---

# 9. Разрешённая текущая работа

Единственная разрешённая implementation работа:

```text
V0.2-IS-01 — Interaction temporal & boundary-state foundation
```

Exact scope/forbidden scope/tests:

- [`../versions/v0.2/implementation-sequence.md`](../versions/v0.2/implementation-sequence.md), section `V0.2-IS-01`.

Запрещено в `IS-01` реализовывать Environment/MicroWorld, lifecycle phases, Perception, Goals, Policy, Action subsystem, Experience Journal, InteractionRuntime, v0.2 config или CLI.

Следующий step автоматически не открывается после Codex completion/commit. Нужен independent ChatGPT audit.

---

# 10. Operational governance

```text
CSPT-02: applicable without bump
MODE-DESIGN: COMPLETE
MODE-TRANSITION: COMPLETE
OPEN implementation step: V0.2-IS-01 only
```

`CSPT-02` остаётся достаточным, потому что v0.2-specific verification/evidence rules уже записаны в accepted version README/sequence, а template требует читать их, выполнять targeted + full current regression и честно фиксировать CI evidence.

Workflow после operator push:

```text
MODE-AUDIT
→ remote commit
→ independent diff/code/tests/actions review
→ AUDIT-PASS / AUDIT-PASS-PENDING-CI / CORRECTION-REQUIRED /
   DOCUMENTATION-CLARIFICATION-REQUIRED / SEMANTIC-BLOCKER
```

Только после `AUDIT-PASS` и explicit «Хорошо. Идём дальше.» выполняется next MODE-TRANSITION.