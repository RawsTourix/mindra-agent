# Карта проектирования модулей MINDRA

## Статус

Этот документ — карта принятых cognitive/runtime boundaries и внешних data/training областей. Канонический статус определяется специализированными design docs и [`../current.md`](../current.md).

Отдельный cognitive module существует только при самостоятельной ответственности, явной boundary/state semantics и независимо проверяемом causal вкладе.

`DU-25/26` находятся **вне cognitive module chain**: это Experience/Data и Training planes.

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

# 3. Experience/Data и Training находятся вокруг cognition

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
```

Canonical owners:

- [`../experience-data-replay.md`](../experience-data-replay.md) — `DU-25`;
- [`../training-lifecycle.md`](../training-lifecycle.md) — `DU-26`.

Ключевые различия:

```text
Experience Journal ≠ Agent runtime state
Agent Memory Replay ≠ Training Replay
Training Runtime ≠ cognitive module
Runtime State Update ≠ Learning Update
Training Objective ≠ Agent Goal / ValueProfile
runtime dependency graph ≠ gradient graph
CandidateRevisionBundle ≠ Active AgentRevision
```

---

# 4. DU-26 — Training Lifecycle

Training Runtime:

- работает только по explicit `TrainingPlan`;
- pin'ит base revisions и source datasets/samples;
- владеет optimizer/trainer state;
- использует explicit `GradientFlowPolicy`;
- создаёт candidate component/agent revisions;
- не мутирует in-flight cognition;
- валидирует candidate до activation;
- активирует совместимые revision bundles на explicit safe boundary;
- сохраняет behavior/learner revision provenance;
- требует explicit privileged-supervision status;
- учитывает representation drift/continual retention;
- не фиксирует конкретный optimizer/framework/algorithm.

---

# 5. Первый ещё не спроектированный блок — Checkpoint / Reproducibility / Compute

Следующий Design Update:

```text
DU-27 — Checkpoint / Reproducibility / Compute
```

Предварительная responsibility:

> определить полный persistent snapshot/checkpoint, restore/reproducibility levels и compute/environment manifests для runtime и training state MINDRA.

Особенно нужны:

- Agent Snapshot vs persistent Checkpoint;
- active/candidate revision manifests;
- optimizer/trainer/RNG state;
- Memory/Workspace/private module state;
- Environment snapshot/world manifest;
- dataset/journal/checkpoint artifact refs;
- exact vs approximate restore;
- content identity/integrity;
- hardware/framework manifests;
- compute accounting;
- migration/compatibility;
- resume training vs inference-only scope.

---

# 6. Оставшиеся Design Updates

```text
DU-27 — Checkpoint / Reproducibility / Compute
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

Следующий допустимый этап определяется только [`../current.md`](../current.md).
