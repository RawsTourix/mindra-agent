# Карта проектирования модулей MINDRA

## Статус

Этот документ — карта принятых cognitive/runtime boundaries и внешних data/training/reproducibility/evaluation/testing/research-claim областей. Канонический статус определяется специализированными design docs и [`../current.md`](../current.md).

Отдельный cognitive module существует только при самостоятельной ответственности, явной boundary/state semantics и независимо проверяемом causal вкладе.

`DU-25 … DU-30` находятся **вне cognitive module chain**.

---

# 1. Принятые cognitive/runtime boundaries

```text
DU-07  Environment
DU-08  Perception / Canonical Representation
DU-09  Goal System
DU-10  Cortex Boundary
DU-11  Memory Core
DU-12  World Model
DU-13  Self Model
DU-14  Intrinsic Signals
DU-15  Drives
DU-16  Appraisal
DU-17  Affect Dynamics
DU-18  Valuation
DU-19  Salience / Attention
DU-20  Memory Regulation / Consolidation
DU-21  Workspace
DU-22  Metacognitive / Executive Control
DU-23  Policy / Planner
DU-24  Action Boundary / Gate / Executor
```

---

# 2. Завершённая cognitive interaction chain

```text
Environment
   ↓
Perception
   ↓
Goals / Cortex / Memory Core
   ↓
World + Self
   ↓
Intrinsic Signals
   ↓
Drives
   ↓
Appraisal
   ↓
Affect
   ↓
Valuation
   ↓
Salience
   ↓
Memory Regulation / Consolidation
   ↓
Workspace
   ↓
Executive Control
   ↓
Policy ← Planner(optional)
   ↓
Action Boundary / Gate
   ↓
Environment
```

Это design dependency/causal map, не literal runtime DAG одного Cognitive Cycle.

---

# 3. Внешние planes вокруг cognition

```text
Agent / Environment / Runtime
          │
          ├──→ Evidence / Experience Plane (DU-25)
          │          ↓
          │      Training Plane (DU-26)
          │          ↓
          │   candidate / activation
          │
          ├──→ Checkpoint / Reproducibility / Compute (DU-27)
          │
          ├──→ Evaluation Plane (DU-28)
          │       research evidence
          │
          ├──→ Engineering Verification Plane (DU-29)
          │       contract/invariant evidence
          │
          └──→ Research Claims / Limitations Plane (DU-30)
                  interpretation / scoped claims /
                  limitations / known unknowns
```

Canonical owners:

- [`../experience-data-replay.md`](../experience-data-replay.md) — `DU-25`;
- [`../training-lifecycle.md`](../training-lifecycle.md) — `DU-26`;
- [`../checkpoint-reproducibility-compute.md`](../checkpoint-reproducibility-compute.md) — `DU-27`;
- [`../mindra-eval.md`](../mindra-eval.md) — `DU-28`;
- [`../engineering-testing.md`](../engineering-testing.md) — `DU-29`;
- [`../research-claims-limitations.md`](../research-claims-limitations.md) — `DU-30`.

Ключевые различия:

```text
Experience Journal ≠ Agent runtime state
Training Runtime ≠ cognitive module
Checkpoint ≠ ExperimentManifest
Evaluation Runtime ≠ Agent cognition
Engineering Testing ≠ MINDRA-Eval
ResearchClaim ≠ Evaluation metric
Observation ≠ Interpretation ≠ Claim
Test Oracle ≠ Agent-visible input
functional similarity ≠ phenomenological equivalence
```

---

# 4. Research evidence → claims

После `DU-30` scientific reporting chain conceptually:

```text
Evaluation / Verification Evidence
          ↓
      Observation
          ↓
     Interpretation
          ↓
      ResearchClaim
      + ClaimScope
      + Limitations
      + KnownUnknowns
          ↓
      ClaimReview /
      supersession
```

Engineering Testing и Research Claims не входят в cognition и не получают write authority Agent state.

---

# 5. Следующий блок — общий consistency freeze

Следующий Design Update:

```text
DU-31 — Contract + ADR Consistency Freeze
```

Это не новый subsystem.

Задача:

> проверить всю архитектуру `DU-01 … DU-30` как единый непротиворечивый набор, определить semantic-frozen candidate contracts и правила breaking change перед созданием version roadmap.

---

# 6. Оставшиеся Design Updates

```text
DU-31 — Contract + ADR Consistency Freeze
DU-32 — Version Roadmap
```

Только после `DU-32` появляются concrete software versions и `implementation-sequence.md`.

---

# 7. Diagnostic rule

Для cognitive subsystem требуются, где применимо, `No*`/Dummy/matched controls, observability, interventions, snapshots и causal metrics.

Для Experience/Data — lineage/leakage/schema/replay controls `DU-25`.

Для Training — revision/gradient/data/activation correctness `DU-26`.

Для Checkpoint — scope/integrity/restore/RNG/Environment/compute provenance `DU-27`.

Для Evaluation — condition/replicate/statistics/attribution validity `DU-28`.

Для Engineering Testing — explicit VerificationObligation/Matrix, failure paths и environment-scoped evidence `DU-29`.

Для Research Claims — scope/evidence/limitations/known-unknowns/supersession discipline `DU-30`.

Следующий допустимый этап определяется только [`../current.md`](../current.md).
