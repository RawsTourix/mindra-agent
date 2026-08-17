# Карта проектирования модулей MINDRA

## Статус

Этот документ — карта принятых cognitive/runtime boundaries и внешних data/training/reproducibility областей. Канонический статус определяется специализированными design docs и [`../current.md`](../current.md).

Отдельный cognitive module существует только при самостоятельной ответственности, явной boundary/state semantics и независимо проверяемом causal вкладе.

`DU-25/26/27` находятся **вне cognitive module chain**: это Experience/Data, Training и Checkpoint/Reproducibility/Compute planes.

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
          ↓
      Evidence Plane
          ↓
   Experience Recorder
          ↓
    Experience Journal
          ↓
 Projection / Dataset Builder
          ↓
 TrainingSample / Replay
          ↓
     Training Runtime
          ↓
 Candidate Revision
          ↓
 Validation / Activation
          ↓
       MINDRA Agent

runtime / training / environment state
          ↓
Checkpoint Capture
          ↓
Checkpoint Manifest + Artifacts
          ↓
Restore / Experiment / Compute Manifests
```

Canonical owners:

- [`../experience-data-replay.md`](../experience-data-replay.md) — `DU-25`;
- [`../training-lifecycle.md`](../training-lifecycle.md) — `DU-26`;
- [`../checkpoint-reproducibility-compute.md`](../checkpoint-reproducibility-compute.md) — `DU-27`.

Ключевые различия:

```text
Experience Journal ≠ Agent runtime state
Agent Memory Replay ≠ Training Replay
Training Runtime ≠ cognitive module
Runtime State Update ≠ Learning Update
CandidateRevisionBundle ≠ Active AgentRevision
AgentSnapshot ≠ persistent Checkpoint
Checkpoint ≠ TrainingResumeCheckpoint ≠ ExperimentManifest
same seed ≠ same RNG state ≠ guaranteed same execution
ComputeManifest ≠ CognitiveResourceEnvelope
```

---

# 4. DU-27 — Checkpoint / Reproducibility / Compute

Checkpoint/Reproducibility plane:

- фиксирует explicit causal `CaptureBoundary`;
- различает AgentSnapshot, persistent Checkpoint, TrainingResumeCheckpoint и ExperimentManifest;
- materializes и verifies required content-identified artifacts до final manifest commit;
- сохраняет active/candidate revision separation;
- интегрирует Environment/action pending state для full-system restore;
- не считает seed заменой current RNG state;
- различает exact/compatible/portable/approximate restore;
- задаёт scoped ReproducibilityClaim вместо boolean;
- сохраняет software/hardware/determinism/compute manifests;
- не делает storage/tensor/checkpoint library частью architecture.

---

# 5. Первый ещё не спроектированный блок — MINDRA-Eval

Следующий Design Update:

```text
DU-28 — MINDRA-Eval
```

Предварительная responsibility:

> определить Evaluation Runtime, benchmark/condition manifests, causal ablations/interventions, diagnostic metrics и statistical protocol, позволяющие измерять самостоятельный вклад MINDRA mechanisms при сопоставимых data/compute/base-state условиях.

Особенно нужны:

- end-to-end и module-specific metrics;
- No*/Dummy/random/shuffled/matched controls;
- common checkpoint/counterfactual base state;
- compute-normalized comparisons;
- stochastic evaluation/statistics;
- evaluator-only Ground Truth isolation;
- Policy vs Action Gate attribution;
- negative module gates Workspace/Affect/Planner/Executive;
- training plasticity vs retention;
- EvaluationManifest/report schema;
- evidence threshold для causal claims.

---

# 6. Оставшиеся Design Updates

```text
DU-28 — MINDRA-Eval
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

Для Checkpoint/Reproducibility обязательны scope/integrity/restore/RNG/Environment causal-cut/compute provenance tests из `DU-27`.

Следующий допустимый этап определяется только [`../current.md`](../current.md).
