# Карта проектирования модулей MINDRA

## Статус

Этот документ — карта принятых cognitive/runtime boundaries и внешних data/training/reproducibility/evaluation/testing/research-claim областей. Канонический статус определяется специализированными design docs, semantic baseline [`../contract-adr-consistency-freeze.md`](../contract-adr-consistency-freeze.md), roadmap [`../version-roadmap.md`](../version-roadmap.md) и [`../current.md`](../current.md).

Отдельный cognitive module существует только при самостоятельной ответственности, явной boundary/state semantics и независимо проверяемом causal вкладе.

`DU-25 … DU-30` находятся вне cognitive module chain. `DU-31` — consistency freeze. `DU-32` — software roadmap.

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

# 2. Cognitive interaction map

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

# 3. Внешние planes

```text
Agent / Environment / Runtime
          │
          ├──→ Experience / Data (DU-25)
          │          ↓
          │      Training (DU-26)
          │
          ├──→ Checkpoint / Reproducibility / Compute (DU-27)
          ├──→ Evaluation (DU-28)
          ├──→ Engineering Verification (DU-29)
          └──→ Research Claims / Limitations (DU-30)
```

Canonical owners:

- [`../experience-data-replay.md`](../experience-data-replay.md)
- [`../training-lifecycle.md`](../training-lifecycle.md)
- [`../checkpoint-reproducibility-compute.md`](../checkpoint-reproducibility-compute.md)
- [`../mindra-eval.md`](../mindra-eval.md)
- [`../engineering-testing.md`](../engineering-testing.md)
- [`../research-claims-limitations.md`](../research-claims-limitations.md)

---

# 4. Semantic Freeze Baseline F31

После `DU-31` карта читается через:

- [`../contract-adr-consistency-freeze.md`](../contract-adr-consistency-freeze.md)
- [`../contracts/semantic-freeze-manifest.md`](../contracts/semantic-freeze-manifest.md)

Frozen:

```text
semantic owner / lifecycle / source / causal boundary
```

Version choice:

```text
exact Python/API/algorithm/storage/backend
```

Обязательные consistency resolutions:

```text
CR-01 Action lifecycle
CR-02 Memory admission ownership
CR-03 Replay taxonomy
CR-04 Consolidation vs Learning Update
CR-05 candidate/validated/activated revision lifecycle
```

---

# 5. Software roadmap

`DU-32` не меняет эту module map. Он определяет порядок **реализации vertical slices**:

```text
v0.1 Core Kernel
→ v0.2 MicroWorld Interaction
→ v0.3 Cortex Gateway
→ v0.4 Memory & Restore
→ v0.5 World & Self
→ v0.6 Intrinsic / Drives / Appraisal
→ v0.7 Affect / Valuation / Salience
→ v0.8 Memory Regulation / Workspace
→ v0.9 Executive / Planner
→ v0.10 Training & Revision Lifecycle
→ v0.11 Research Harness
→ v0.12 Integration Hardening
→ v1.0 MINDRA Research Baseline
```

Canonical roadmap: [`../version-roadmap.md`](../version-roadmap.md).

Ранний milestone может использовать `No*`/Dummy/control implementation поздней boundary, если её semantic contract сохраняется.

---

# 6. Diagnostic rule

Для cognitive subsystem требуются, где применимо, `No*`/Dummy/matched controls, observability, interventions, snapshots и causal metrics.

Для Experience/Data — lineage/leakage/schema/replay controls.

Для Training — revision/gradient/data/activation correctness.

Для Checkpoint — scope/integrity/restore/RNG/Environment/compute provenance.

Для Evaluation — condition/replicate/statistics/attribution validity.

Для Engineering Testing — `VerificationObligation/Matrix`, failure paths и environment-scoped evidence.

Для Research Claims — scope/evidence/limitations/known-unknowns/supersession discipline.

Для version planning — F31 не переопределяется без нового ADR.

---

# 7. Следующий этап

Общий DU-cycle завершён.

Следующая разрешённая работа:

```text
Version Design — v0.1 Core Kernel
```

Фактический статус определяется только [`../current.md`](../current.md).
