# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-26` завершены и приняты. Реализация ещё не начата.**

Приняты:

- foundation/system boundaries `DU-01 … DU-06`;
- cognitive/runtime boundaries `DU-07 … DU-24`;
- Experience / Data / Replay `DU-25`;
- Training Lifecycle `DU-26`;
- 26 accepted ADR;
- candidate semantic contracts для boundaries `DU-07 … DU-26`.

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
```

---

# 3. DU-26

Canonical design:

- [`training-lifecycle.md`](training-lifecycle.md)

Candidate contract:

- [`contracts/training-lifecycle.md`](contracts/training-lifecycle.md)

Accepted decision:

- [`ADR-0026`](decisions/ADR-0026-candidate-revision-validated-activation-training-lifecycle.md)

Research pass:

- [`../research/literature/DU-26-training-lifecycle-landscape-2026-08.md`](../research/literature/DU-26-training-lifecycle-landscape-2026-08.md)

Главные результаты:

```text
Runtime State Update
≠ Consolidation Event
≠ Replay Step
≠ Learning Update

Training Objective
≠ Agent Goal
≠ ValueProfile

CandidateRevisionBundle
≠ Active AgentRevision
```

- `Training Runtime` находится вне agent-owned cognition;
- ordinary module `compute()` не выполняет hidden optimizer update;
- runtime mutable state, trainable parameters и optimizer/trainer state имеют разные ownership semantics;
- `TrainingPlan` явно pin'ит target components, base revisions, data, visibility, objectives, optimizer и gradient-flow policy;
- runtime dependency graph не определяет gradient graph;
- source `TrainingSample`/Replay provenance сохраняется до `LearningUpdateRecord`;
- Training Objective является внешней optimization semantics и не равен internal Utility/Drive/Intrinsic Signal автоматически;
- joint и separate optimization оба допустимы, но shared parameter ownership/gradient coupling explicit;
- frozen Cortex, adapters и частично/полностью trainable Cortex укладываются в одну lifecycle boundary;
- training создаёт `CandidateRevisionBundle`, который проходит validation до activation;
- activation новой `agent_revision` происходит на explicit safe causal boundary;
- in-flight Decision/Cognitive segment сохраняет pinned старую revision;
- behavior revision и learner revision могут различаться при decoupled online learning;
- privileged supervision требует explicit training condition;
- representation drift/Memory downstream compatibility проверяются до activation;
- continual learning обязан отдельно учитывать forgetting/retention;
- failed candidate не мутирует live Agent;
- rollback сохраняет causal history плохого update/activation;
- concrete optimizer/framework/algorithm/PEFT method намеренно не выбран.

---

# 4. Следующий допустимый Design Update

```text
DU-27 — Checkpoint / Reproducibility / Compute
```

Цель `DU-27` — спроектировать **полный воспроизводимый snapshot/checkpoint и compute manifest MINDRA**, способный восстановить не только active Agent, но и causally relevant training/runtime state.

Обязательные вопросы:

```text
Agent Snapshot vs Checkpoint vs Training Checkpoint
active/candidate AgentRevision manifests
component/private state capture
Memory / Workspace / Executive / Planner / Action Boundary pending state
World/Self/Drive/Affect/provider RNG states
optimizer/scheduler/scaler/trainer state
TrainingPlan/Attempt resume state
replay/sample cursors
Environment snapshot/world manifest
Experience Journal / DatasetManifest refs
artifact identity / content hashes
schema/contract/version manifests
exact vs approximate restore
full vs incremental/delta checkpoint
portable vs hardware-specific state
CPU/GPU/dtype/device migration
randomness / deterministic algorithms
framework/library/CUDA/driver/environment manifests
compute accounting
Colab/local/remote topology
checkpoint consistency / two-phase capture
in-flight action/dispatch/execution_unknown
checkpoint corruption/integrity
migration/backward compatibility
retention/garbage collection
resume-training vs inference-only checkpoints
reproducibility claim levels
```

Особенно нужно определить:

- `Agent Snapshot ≠ persistent Checkpoint`;
- exact counterfactual restore требует всех causally relevant private/RNG states;
- checkpoint активного Agent и training-resume checkpoint могут иметь разный scope;
- `DU-26` optimizer/trainer/candidate/activation state должен быть сохраняемым, если заявлен resumable training;
- content identity и manifests важнее physical file path;
- hardware/framework nondeterminism не маскируется утверждением «seed одинаковый»;
- compute budget/usage становится воспроизводимым research metadata, но raw infrastructure telemetry не становится cognition автоматически;
- concrete serialization/storage backend остаётся implementation choice.

После принятия `DU-27` допускается:

```text
DU-28 — MINDRA-Eval
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

- Checkpoint / Reproducibility / Compute;
- MINDRA-Eval;
- Engineering Testing;
- Research Claims / Limitations;
- Contract + ADR Freeze;
- Version Roadmap;
- implementation sequences.

Также не выбраны concrete Python/framework/model/algorithm/storage implementations.

---

# 6. Implementation status

```text
Исследовательская/production реализация: не начата
Дорожная карта версий: не спроектирована
Software version: отсутствует
Implementation HEAD: отсутствует
```

Detailed design сам по себе не разрешает Codex начинать implementation до `DU-32` и соответствующего version/implementation sequence.
