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
V0.2-IS-01 … V0.2-IS-03: accepted
V0.2-IS-04: OPEN
V0.2-IS-05 … V0.2-IS-14: CLOSED
v0.2 implementation: active, 3 accepted implementation steps
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
ruff / format / mypy / Import Linter: PASS
canonical validate-profile: PASS
canonical kernel-smoke: PASS — waves=3 revision=3 join=10
clean wheel metadata/install verification: PASS
third-party runtime dependencies: 0
future-responsibility scope audit: PASS
language policy review: PASS
GitHub Actions run 33424412605
Ubuntu Python 3.14: PASS
Windows Python 3.14: PASS
AUDIT-PASS
```

Canonical detailed evidence:

- [`../versions/v0.1/verification-matrix.md`](../versions/v0.1/verification-matrix.md).

Post-v0.1 documentation consistency cleanup завершён без изменения F31, roadmap, v0.1 code или accepted semantics.

Рекомендуемый immutable tag target до добавления v0.2 design:

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

Accepted step-specific clarifications:

- [`../versions/v0.2/is-02-lifecycle-runtime-shape.md`](../versions/v0.2/is-02-lifecycle-runtime-shape.md) — accepted exact shape для `V0.2-IS-02`;
- [`../versions/v0.2/is-03-environment-contract-shape.md`](../versions/v0.2/is-03-environment-contract-shape.md) — accepted exact shape для `V0.2-IS-03`;
- [`../versions/v0.2/is-04-microworld-core-shape.md`](../versions/v0.2/is-04-microworld-core-shape.md) — **current mandatory** accepted exact shape для `V0.2-IS-04`.

Canonical owners/contracts обязательные для текущего Environment step:

- `DU-07` Environment / MicroWorld;
- `DU-03` Runtime / Temporal Model;
- `DU-04` CognitiveState;
- `DU-06` Observability / Intervention;
- [`contracts/environment.md`](contracts/environment.md);
- [`ADR-0007`](decisions/ADR-0007-two-plane-environment-boundary.md).

---

# 4. Accepted v0.2 exact design gate

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

# 5. VerificationObligations v0.2

Current obligations:

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

Accepted coverage после `V0.2-IS-03`:

```text
V02-003 — Environment contract foundation accepted
V02-004 — lifecycle foundation coverage accepted
V02-005 — substantial Decision Window multiplicity coverage accepted
V02-010 — Environment action-interface foundation accepted
V02-015 — reset/termination/truncation contract foundation accepted
V02-016 — architecture/scope layer coverage accepted
```

Ни одна `V02-*` пока не имеет final version-wide PASS status. `V02-002` должен закрыться на Environment layer в `IS-04`; end-to-end obligations продолжают наращиваться по sequence до `IS-14`.

---

# 6. v0.2 implementation checkpoints

| Step | Status | Result |
|---|---|---|
| `V0.2-IS-01` | accepted | `5ddc0daff12536e080c9fd1bc50476464109a455` — Interaction temporal & boundary-state foundation |
| `V0.2-IS-02` | accepted | `c3f2dfb411c92d3048bd833732fdc18d696ec282` — Lifecycle phases & KernelRuntime context bridge |
| `V0.2-IS-03` | accepted | `576248fd389a3211adc1d722e1d154c9c0eaabed` — Environment contracts & capability split |
| `V0.2-IS-04` | **OPEN** | Deterministic MicroWorld core, MW0 & snapshot |
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

# 7. Accepted evidence V0.2-IS-01

Implementation:

```text
5ddc0daff12536e080c9fd1bc50476464109a455
feat(v0.2): add interaction state ingress foundation
```

Independent audit:

```text
scope / F31 consistency: PASS
runtime/module ownership separation: PASS
CURRENT_DECISION_WINDOW / CURRENT_EPISODE: PASS
boundary atomicity/stale-base validation: PASS
v0.1 regression: PASS
GitHub Actions 33486615509 — Ubuntu/Windows PASS
AUDIT-PASS
```

---

# 8. Accepted evidence V0.2-IS-02

Implementation:

```text
c3f2dfb411c92d3048bd833732fdc18d696ec282
feat(v0.2): add lifecycle runtime context bridge
```

Independent audit:

```text
scope / exact design: PASS
phase ownership: PASS
LifecycleCoordinator atomicity: PASS
CognitiveScheduler separation: PASS
CognitiveCycleId ownership: PASS
O0 lifecycle evidence: PASS
intervention boundary: PASS
full pytest: 407 passed
GitHub Actions 33494536923 — Ubuntu/Windows PASS
AUDIT-PASS
```

---

# 9. Accepted evidence V0.2-IS-03

Implementation:

```text
576248fd389a3211adc1d722e1d154c9c0eaabed
feat(v0.2): add environment contracts and capability split
```

Independent audit:

```text
repository/commit: PASS
scope: PASS
exact IS-03 contract: PASS
Agent/Research separation: PASS
privacy/escape-hatch audit: PASS
action vocabulary: PASS
ActionCommitId → EnvironmentTransitionId causal seam: PASS
snapshot abstraction without premature serialization: PASS
stdlib/dependency boundary: PASS
v0.1 regression: PASS
AUDIT-PASS
```

Local implementation evidence reported and independently reconciled:

```text
targeted Environment contracts: PASS — 32 passed
affected identity/lifecycle/value subset: PASS — 80 passed
ruff: PASS
format: PASS — 262 files
mypy --strict: PASS — 106 source files
Import Linter: PASS — 3 kept / 0 broken
full pytest: PASS — 439 passed
uv build: PASS — package remains 0.1.0
v0.1 validate-profile: PASS — modules=4 waves=3
v0.1 kernel-smoke: PASS — waves=3 revision=3 join=10
runtime third-party dependencies: 0
```

Remote exact-HEAD CI:

```text
GitHub Actions run 33526074690
head 576248fd389a3211adc1d722e1d154c9c0eaabed
FULL-C0 ubuntu-latest / Python 3.14: PASS — 439 passed
FULL-C0 windows-latest / Python 3.14: PASS
locked install: PASS
ruff / format / mypy / import contracts: PASS
canonical v0.1 CLI: PASS
wheel + sdist build: PASS
clean v0.1 wheel verification: PASS
```

---

# 10. Разрешённая текущая работа

Единственная разрешённая implementation работа:

```text
V0.2-IS-04 — Deterministic MicroWorld core, MW0 & snapshot
```

Обязательные sources текущего step:

- [`../versions/v0.2/implementation-sequence.md`](../versions/v0.2/implementation-sequence.md), section `V0.2-IS-04`;
- [`../versions/v0.2/is-04-microworld-core-shape.md`](../versions/v0.2/is-04-microworld-core-shape.md);
- [`../versions/v0.2/is-03-environment-contract-shape.md`](../versions/v0.2/is-03-environment-contract-shape.md);
- [`modules/environment.md`](modules/environment.md);
- [`contracts/environment.md`](contracts/environment.md);
- [`ADR-0007`](decisions/ADR-0007-two-plane-environment-boundary.md).

Exact accepted direction:

```text
stdlib-only synchronous in-process MicroWorld
private core + physically separate MicroWorldInteraction / MicroWorldResearch wrappers
MW0_DIRECT_REACH only
walls/floor/target + generic portable object primitive
canonical fixed MW0 7x7 fixture + narrow guaranteed-solvable procedural MW0
partial observation radius/occlusion + full-observation control through same safe RawObservation
relative cell coordinates; no hidden/world IDs/seeds in Agent observation
Move/Interact/Pickup/Drop/Wait all handled
blocked movement = natural NO_EFFECT transition
three independent instance-local random.Random streams
exact SHA-256 role seed derivation
staged reset/transition publication
concrete frozen MicroWorldSnapshot with all RNG states
restore exact continuation
clone/fork without mutable world/RNG alias
research transition records and privileged reasons only on Research Plane
no MW1/MW3, door/key/switch/hidden-rule behavior
```

Запрещено в `IS-04` реализовывать `IS-05+`: hidden causal rules, doors/keys/switches, Perception, Goals, Policy, Action Boundary, Dispatcher, Experience Journal, InteractionRuntime, v0.2 composition/profile/CLI или package metadata migration.

Следующий step автоматически не открывается после Codex completion/commit. Нужен independent ChatGPT audit.

---

# 11. Operational governance

```text
CSPT-02: applicable without bump
MODE-AUDIT V0.2-IS-03: AUDIT-PASS
MODE-DESIGN V0.2-IS-04: COMPLETE
MODE-TRANSITION: COMPLETE
OPEN implementation step: V0.2-IS-04 only
```

`CSPT-02` остаётся достаточным: concrete MicroWorld exact shape фиксируется step-specific clarification, а обязательные prompt sections, verification/CI semantics, reporting fields и commit/push policy не изменились.

Workflow после operator push:

```text
MODE-AUDIT
→ remote commit
→ independent diff/code/tests/actions review
→ AUDIT-PASS / AUDIT-PASS-PENDING-CI / CORRECTION-REQUIRED /
   DOCUMENTATION-CLARIFICATION-REQUIRED / SEMANTIC-BLOCKER
```

Только после `AUDIT-PASS` и explicit «Хорошо. Идём дальше.» выполняется next MODE-TRANSITION.
