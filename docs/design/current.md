# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-30` завершены и приняты. Реализация ещё не начата.**

Приняты:

- foundation/system boundaries `DU-01 … DU-06`;
- cognitive/runtime boundaries `DU-07 … DU-24`;
- Experience / Data / Replay `DU-25`;
- Training Lifecycle `DU-26`;
- Checkpoint / Reproducibility / Compute `DU-27`;
- MINDRA-Eval `DU-28`;
- Engineering Testing `DU-29`;
- Research Claims / Limitations `DU-30`;
- 30 accepted ADR;
- candidate semantic contracts для boundaries `DU-07 … DU-30`.

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
```

---

# 3. DU-30

Canonical design:

- [`research-claims-limitations.md`](research-claims-limitations.md)

Candidate contract:

- [`contracts/research-claims-limitations.md`](contracts/research-claims-limitations.md)

Accepted decision:

- [`ADR-0030`](decisions/ADR-0030-versioned-evidence-bounded-research-claims.md)

Research pass:

- [`../research/literature/DU-30-research-claims-limitations-landscape-2026-08.md`](../research/literature/DU-30-research-claims-limitations-landscape-2026-08.md)

Главные результаты:

```text
Observation
≠ Interpretation
≠ ResearchClaim

claim strength ≤ evidence strength
claim generality ≤ supported ClaimScope

functional similarity
≠ phenomenological equivalence
```

- `ResearchClaim` является versioned first-class artifact с explicit `ClaimScope`;
- supporting и challenging evidence сохраняются одновременно;
- causal, generalization, efficiency и architecture-contribution claims имеют разные support requirements;
- `null`, `negative evidence`, `inconclusive`, `invalid` и `not measured` не смешиваются;
- `LimitationRecord` и `KnownUnknownRecord` first-class;
- failed module gate создаёт claim/design review, но не меняет accepted architecture автоматически;
- old claim weakening/supersession сохраняет historical lineage;
- publication/report wording traceable до canonical claim revision;
- Cortex/data/compute/tuning/provider dependence входит в scope/limitations;
- engineering verification не заменяет evidence функциональной полезности;
- `Self Model`, Drives, Appraisal, Affect, Workspace и first-person Cortex text не являются сами по себе evidence consciousness/subjective experience;
- `AGI` не выводится из одного benchmark/module result;
- concrete paper format, preregistration service и evidence-score taxonomy не выбраны.

---

# 4. Следующий допустимый Design Update

```text
DU-31 — Contract + ADR Consistency Freeze
```

Цель `DU-31` — выполнить **общий consistency/freeze pass по всей принятой архитектуре `DU-01 … DU-30`** перед проектированием software version roadmap.

Это не новый subsystem design. Нужно проверить, что canonical design, ADR, glossary, candidate contracts, dependency/ownership/temporal semantics, Evaluation/Verification/Claims planes и status/index документы образуют один непротиворечивый набор.

Обязательные вопросы:

```text
ADR registry completeness/status
canonical owner uniqueness
contract ↔ design ↔ ADR consistency
terminology/glossary consistency
cross-module ownership conflicts
read/write/dependency graph conflicts
temporal/commit boundary consistency
snapshot/checkpoint completeness
source/provenance/visibility consistency
No*/Dummy/control semantics consistency
module negative-gate consistency
Evaluation ↔ Engineering Testing ↔ Claims boundaries
claim/evidence/verification lineage
candidate contract field naming/revision conventions
unknown/missing/stale/unavailable semantics
error/failure/status taxonomy conflicts
implementation leakage in canonical contracts
orphan docs/obsolete statements
verification obligations required before implementation
freeze status and allowed change procedure
```

Особенно нужно определить:

- какие candidate contracts после consistency pass считаются **semantic-frozen** для первого roadmap;
- какие поля/enum/API детали остаются implementation/version choices;
- какие open questions блокируют `DU-32`, а какие допустимо перенести в version design;
- нет ли двух владельцев одной canonical state/action/data responsibility;
- нет ли contradiction между early DU и поздними уточнениями;
- как после freeze вносится breaking semantic change: только через новый ADR/design update;
- нельзя начинать implementation только потому, что individual contracts уже подробны — сначала требуется общий freeze.

После принятия `DU-31` допускается:

```text
DU-32 — Version Roadmap
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

- Contract + ADR Consistency Freeze;
- Version Roadmap;
- implementation sequences конкретных software versions.

Также не выбраны concrete Python/framework/model/algorithm/storage/evaluation/testing implementations.

---

# 6. Implementation status

```text
Исследовательская/production реализация: не начата
Дорожная карта версий: не спроектирована
Software version: отсутствует
Implementation HEAD: отсутствует
```

Detailed design сам по себе не разрешает Codex начинать implementation до `DU-32` и соответствующего version/implementation sequence.
