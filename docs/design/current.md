# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какая работа разрешена следующей.

---

# 1. Общий статус

**Общий архитектурный цикл `DU-00 … DU-32` завершён и принят. Реализация ещё не начата.**

Приняты:

- foundation/system boundaries `DU-01 … DU-06`;
- cognitive/runtime boundaries `DU-07 … DU-24`;
- Experience / Data / Replay `DU-25`;
- Training Lifecycle `DU-26`;
- Checkpoint / Reproducibility / Compute `DU-27`;
- MINDRA-Eval `DU-28`;
- Engineering Testing `DU-29`;
- Research Claims / Limitations `DU-30`;
- Contract + ADR Consistency Freeze `DU-31`;
- Version Roadmap `DU-32`;
- 32 accepted ADR;
- semantic contracts `DU-07 … DU-30` frozen по смыслу как baseline `F31`;
- roadmap `v0.1 … v1.0`.

Архитектурная линия имеет статус:

```text
semantic design frozen: F31
version roadmap accepted
ready for version-specific design
```

Exact Python/API/tooling choices будут фиксироваться отдельно в каждой software version.

---

# 2. Завершённые Design Updates

```text
DU-00 — Documentation Foundation
DU-01 — System Context
DU-02 — Dependency & Composition Rules
DU-03 — Runtime / Temporal Model
DU-04 — CognitiveState Semantics
DU-05 — Module Protocol & Scheduling
DU-06 — Observability & Intervention
DU-07 — Environment / MicroWorld Contract
DU-08 — Perception / Canonical Representation
DU-09 — Goal System
DU-10 — Cortex Boundary
DU-11 — Memory Core
DU-12 — World Model
DU-13 — Self Model
DU-14 — Intrinsic Signals
DU-15 — Drives
DU-16 — Appraisal
DU-17 — Affect Dynamics
DU-18 — Valuation
DU-19 — Salience / Attention
DU-20 — Memory Regulation / Consolidation
DU-21 — Workspace
DU-22 — Metacognitive / Executive Control
DU-23 — Policy / Planner
DU-24 — Action Boundary / Gate / Executor
DU-25 — Experience / Data / Replay
DU-26 — Training Lifecycle
DU-27 — Checkpoint / Reproducibility / Compute
DU-28 — MINDRA-Eval
DU-29 — Engineering Testing
DU-30 — Research Claims / Limitations
DU-31 — Contract + ADR Consistency Freeze
DU-32 — Version Roadmap
```

---

# 3. Semantic baseline

Canonical freeze:

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md)
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md)
- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md)

Freeze identity:

```text
Semantic Freeze Baseline F31
scope: DU-01 … DU-30
semantic boundary contracts: 24
status: accepted
```

Version design не может менять F31 semantics без нового ADR и новой freeze baseline revision.

---

# 4. Version Roadmap

Canonical roadmap:

- [`version-roadmap.md`](version-roadmap.md)

Accepted decision:

- [`ADR-0032`](decisions/ADR-0032-vertical-capability-version-roadmap.md)

Version index:

- [`../versions/README.md`](../versions/README.md)

Roadmap:

```text
v0.1  Core Kernel
v0.2  MicroWorld Interaction
v0.3  Cortex Gateway
v0.4  Memory & Restore
v0.5  World & Self
v0.6  Intrinsic / Drives / Appraisal
v0.7  Affect / Valuation / Salience
v0.8  Memory Regulation / Workspace
v0.9  Executive / Planner
v0.10 Training & Revision Lifecycle
v0.11 Research Harness
v0.12 Integration Hardening
v1.0  MINDRA Research Baseline
```

Главный roadmap invariant:

```text
vertical runnable slice
+
No*/Dummy/control implementations
+
F31 semantic contracts
→ следующая версия расширяет capability без semantic rewrite
```

---

# 5. Следующая разрешённая работа

Общий `DU`-цикл завершён.

Следующая работа:

```text
Version Design — v0.1 Core Kernel
```

Нужно создать и принять минимум:

```text
docs/versions/v0.1/README.md
docs/versions/v0.1/implementation-sequence.md
```

Сначала подробно выбираются:

- Python/runtime/tooling stack;
- package structure;
- exact representations foundation contracts;
- config/composition scheme;
- scheduler/state/provenance implementation profile;
- testing stack;
- VerificationObligations;
- acceptance criteria;
- non-goals.

Только после принятия version design и implementation sequence начинается coding `v0.1`.

---

# 6. Implementation status

```text
Исследовательская/production реализация: не начата
Semantic design freeze: F31 accepted
Version roadmap: DU-32 accepted
Current software milestone: v0.1 — design not started
Implementation HEAD: отсутствует
```

Codex не начинает реализовывать roadmap целиком и не выбирает самостоятельно architecture/tooling вне принятого version scope.
