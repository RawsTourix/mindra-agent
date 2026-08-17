# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-27` завершены и приняты. Реализация ещё не начата.**

Приняты:

- foundation/system boundaries `DU-01 … DU-06`;
- cognitive/runtime boundaries `DU-07 … DU-24`;
- Experience / Data / Replay `DU-25`;
- Training Lifecycle `DU-26`;
- Checkpoint / Reproducibility / Compute `DU-27`;
- 27 accepted ADR;
- candidate semantic contracts для boundaries `DU-07 … DU-27`.

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
```

---

# 3. DU-27

Canonical design:

- [`checkpoint-reproducibility-compute.md`](checkpoint-reproducibility-compute.md)

Candidate contract:

- [`contracts/checkpoint-reproducibility-compute.md`](contracts/checkpoint-reproducibility-compute.md)

Accepted decision:

- [`ADR-0027`](decisions/ADR-0027-manifest-driven-causal-checkpoint-restore.md)

Research pass:

- [`../research/literature/DU-27-checkpoint-reproducibility-compute-landscape-2026-08.md`](../research/literature/DU-27-checkpoint-reproducibility-compute-landscape-2026-08.md)

Главные результаты:

```text
AgentSnapshot
≠ persistent Checkpoint
≠ TrainingResumeCheckpoint
≠ ExperimentManifest

same seed
≠ same RNG state
≠ guaranteed same execution

semantic restore
≠ bitwise reproducibility
```

- checkpoint является manifest-driven набором content-identified artifacts, а не обязательным одним файлом;
- checkpoint scope явно определяет required/optional state;
- training-resume scope включает causally relevant optimizer/scheduler/scaler/trainer/replay/data-cursor state;
- consistent checkpoint относится к explicit causal `CaptureBoundary`;
- используется conceptual prepare/pin → materialize/verify → final manifest commit;
- incomplete artifact set не является valid checkpoint;
- active и candidate revisions сохраняются раздельно, restore candidate не активирует её автоматически;
- full-system restore требует causally aligned Agent + Environment state;
- `execution_unknown`/unresolved external effect может блокировать safe branch/retry до reconciliation;
- `seed` не заменяет current RNG state;
- reproducibility задаётся scoped `ReproducibilityClaim`, а не boolean;
- exact/compatible/portable/approximate restore различаются;
- software/hardware/determinism manifests являются частью сильных reproducibility claims;
- artifact content identity отделена от physical path/storage location;
- full и delta/incremental checkpoint допустимы, но delta dependency chain обязана быть integrity-complete;
- migration создаёт explicit lineage и не переписывает source checkpoint;
- infrastructure `ComputeManifest`/usage отделены от agent-visible `CognitiveResourceEnvelope`;
- concrete serialization/hash/storage/profiler framework намеренно не выбран.

---

# 4. Следующий допустимый Design Update

```text
DU-28 — MINDRA-Eval
```

Цель `DU-28` — спроектировать **канонический Evaluation Harness и measurement protocol MINDRA**, позволяющий измерять не только task performance, но и самостоятельный причинный вклад модулей/границ при сопоставимых условиях и compute.

Обязательные вопросы:

```text
Evaluation Runtime ownership
benchmark/task suite structure
train/validation/test world distributions
evaluation episode/run/condition identity
configuration matrix / ablation matrix
No*/Dummy/control/matched-control semantics
paired counterfactual evaluation
checkpoint/base-state alignment
intervention-based causal tests
module-specific functional metrics
end-to-end task metrics
calibration metrics
world/self-model metrics
memory/retrieval metrics
intrinsic/drive/appraisal/affect/valuation/salience diagnostics
Executive performance-vs-compute frontier
Planner matched-compute controls
Policy vs Action Gate attribution
workspace/affect negative module gates
training plasticity vs retention
reproducibility claim requirements
compute-normalized comparison
stochastic evaluation / seeds
confidence intervals / statistical tests
multiple comparisons / preregistered analysis where needed
oracle/evaluator-only data separation
failure/unknown/unresolved outcomes
report schema / EvaluationManifest
research claim evidence threshold
```

Особенно нужно определить:

- `Evaluation Runtime` остаётся вне Agent и не передаёт evaluator score в cognition normal runtime способом;
- one-number leaderboard score не должен заменять diagnostic causal evaluation;
- baseline/ablation/control должны отличаться по semantic intervention, а не скрытому compute/data budget;
- matched compute/state/parameter controls обязательны там, где иначе эффект объясняется дополнительной capacity;
- Policy quality измеряется до Action Gate отдельно от system-level post-Gate outcome;
- causal intervention требует common verified checkpoint/base state нужного `DU-27` restore level;
- stochastic result требует statistical protocol, а не одного seed;
- evaluation condition обязан ссылаться на exact Agent/Environment/data/checkpoint/revision/software/hardware/compute manifests;
- privileged Ground Truth доступен evaluator'у, но не Agent;
- `DU-28` должен определить falsification criteria для условно принятых Workspace/Affect/Planner/Executive mechanisms;
- конкретный benchmark framework/library остаётся implementation choice.

После принятия `DU-28` допускается:

```text
DU-29 — Engineering Testing
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

- MINDRA-Eval;
- Engineering Testing;
- Research Claims / Limitations;
- Contract + ADR Freeze;
- Version Roadmap;
- implementation sequences.

Также не выбраны concrete Python/framework/model/algorithm/storage/checkpoint implementations.

---

# 6. Implementation status

```text
Исследовательская/production реализация: не начата
Дорожная карта версий: не спроектирована
Software version: отсутствует
Implementation HEAD: отсутствует
```

Detailed design сам по себе не разрешает Codex начинать implementation до `DU-32` и соответствующего version/implementation sequence.
