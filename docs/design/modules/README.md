# Карта проектирования модулей MINDRA

## Статус

Этот документ — карта принятых cognitive/runtime boundaries и внешних data/training/reproducibility/evaluation областей. Канонический статус определяется специализированными design docs и [`../current.md`](../current.md).

Отдельный cognitive module существует только при самостоятельной ответственности, явной boundary/state semantics и независимо проверяемом causal вкладе.

`DU-25/26/27/28` находятся **вне cognitive module chain**: это Experience/Data, Training, Checkpoint/Reproducibility/Compute и Evaluation planes.

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
                    ┌─────────────────────┐
                    │   Evaluation Plane  │
                    │ conditions/metrics  │
                    │ controls/statistics │
                    └──────────┬──────────┘
                               │ Evidence / Intervention
                               ▼
Environment ↔ MINDRA Agent ↔ Action Boundary
                 │
                 ▼
          Experience Plane
                 │
                 ▼
           Training Plane
                 │
                 ▼
      Candidate / Activation

runtime / training / environment state
                 │
                 ▼
Checkpoint / Reproducibility / Compute Plane
```

Canonical owners:

- [`../experience-data-replay.md`](../experience-data-replay.md) — `DU-25`;
- [`../training-lifecycle.md`](../training-lifecycle.md) — `DU-26`;
- [`../checkpoint-reproducibility-compute.md`](../checkpoint-reproducibility-compute.md) — `DU-27`;
- [`../mindra-eval.md`](../mindra-eval.md) — `DU-28`.

Ключевые различия:

```text
Experience Journal ≠ Agent runtime state
Training Runtime ≠ cognitive module
Runtime State Update ≠ Learning Update
CandidateRevisionBundle ≠ Active AgentRevision
AgentSnapshot ≠ persistent Checkpoint
same seed ≠ same RNG state ≠ guaranteed same execution
ComputeManifest ≠ CognitiveResourceEnvelope
Evaluation Runtime ≠ Agent cognition
Task score ≠ module/causal/calibration evidence
nested episode ≠ independent training replicate
Policy pre-Gate quality ≠ post-Gate system quality
```

---

# 4. DU-28 — MINDRA-Eval

Evaluation Plane:

- работает через explicit `EvaluationStudyPlan`/`EvaluationCondition`;
- использует typed metrics вместо обязательного universal score;
- различает baseline/ablation/semantic/matched/oracle controls;
- поддерживает paired counterfactual interventions только при достаточном restore level;
- сохраняет experimental/statistical unit и replicate nesting;
- требует uncertainty/distribution evidence для stochastic aggregate claims;
- отделяет evaluator Ground Truth от Agent-visible information;
- измеряет Policy до Action Gate отдельно от post-Gate system;
- учитывает actual compute/data/context/tuning differences;
- задаёт negative gates для Affect/Workspace/Planner/Executive;
- связывает report с raw Evidence/Experience/reproducibility manifests;
- не фиксирует benchmark/statistics/plotting framework.

---

# 5. Первый ещё не спроектированный блок — Engineering Testing

Следующий Design Update:

```text
DU-29 — Engineering Testing
```

Предварительная responsibility:

> определить автоматическую проверку реализации MINDRA: contracts, ownership, causal invariants, failure semantics, serialization/restore/migration, data leakage и runtime/training/evaluation integration — отдельно от research utility evaluation.

Особенно нужны:

- architecture/dependency tests;
- unit/contract/property tests;
- scheduler/state/action invariants;
- failure injection;
- checkpoint round-trip/corruption tests;
- data lineage/leakage tests;
- candidate/activation/rollback tests;
- EvaluationManifest validation;
- fast/slow/accelerator CI tiers;
- flaky/golden/fuzz policies.

---

# 6. Оставшиеся Design Updates

```text
DU-29 — Engineering Testing
DU-30 — Research Claims / Limitations
DU-31 — Contract + ADR Consistency Freeze
DU-32 — Version Roadmap
```

Только после `DU-32` появляются concrete software versions и `implementation-sequence.md`.

---

# 7. Diagnostic rule

Для cognitive subsystem требуются, где применимо, `No*`/Dummy/matched controls, observability, interventions, snapshots и causal metrics.

Для Experience/Data требуются lineage/leakage/schema/replay controls `DU-25`.

Для Training Runtime требуются Frozen/NoLearning, offline/online controls, data/compute-matched comparisons, retention diagnostics и explicit revision activation evidence.

Для Checkpoint/Reproducibility обязательны scope/integrity/restore/RNG/Environment causal-cut/compute provenance requirements `DU-27`.

Для Evaluation обязательны condition provenance, replicate/statistical semantics, matched controls, privileged Ground Truth isolation и report lineage `DU-28`.

Следующий допустимый этап определяется только [`../current.md`](../current.md).
