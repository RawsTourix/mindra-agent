# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-25` завершены и приняты. Реализация ещё не начата.**

Приняты:

- foundation/system boundaries `DU-01 … DU-06`;
- cognitive/subsystem boundaries `DU-07 … DU-24`;
- Experience / Data / Replay;
- 25 accepted ADR;
- candidate semantic contracts для subsystem/data boundaries `DU-07 … DU-25`.

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
```

---

# 3. DU-25

Canonical design:

- [`experience-data-replay.md`](experience-data-replay.md)

Candidate contract:

- [`contracts/experience-data-replay.md`](contracts/experience-data-replay.md)

Accepted decision:

- [`ADR-0025`](decisions/ADR-0025-causal-experience-journal-derived-projections.md)

Research pass:

- [`../research/literature/DU-25-experience-data-replay-landscape-2026-08.md`](../research/literature/DU-25-experience-data-replay-landscape-2026-08.md)

Главные результаты:

```text
TraceEvent
≠ ExperienceEvent

Experience Journal
≠ Agent runtime state
≠ Replay Buffer
≠ Agent Memory

Source Experience
≠ TrainingSample
```

- source of truth записанного опыта — append-only causal `Experience Journal`;
- event-sourced именно data plane, а не runtime `CognitiveState`/Agent;
- physical append order не определяет causal order;
- stable IDs, causal parent refs и logical scopes являются основой correlation;
- standard Episode/Decision/Transition/Sequence representations — derived projections;
- `InteractionTransitionView` допускает `Action Commit` без Environment transition;
- `execution_unknown`/definite dispatch failure/partial execution не fabricatе fake next state;
- evaluator-only/Research Ground Truth хранится отдельными `ResearchAnnotationRecord`;
- inclusion privileged data требует explicit `DataVisibilityPolicy`;
- actual/imagined/replayed/counterfactual/intervened provenance хранится без комбинаторного смешения;
- source `agent_revision` и component revisions сохраняются на соответствующих causal events;
- online action может быть выбран одной Agent revision, а outcome обработан другой — это не скрывается;
- `DatasetManifest` фиксирует source manifests, schema, transforms, revisions, splits, quality и determinism policy;
- `TrainingSample` всегда derived и хранит source/transform lineage;
- hindsight/relabeling/re-encoding не переписывают source experience;
- Training Replay работает поверх source/derived samples, но replay table не source of truth;
- `Agent Memory Replay ≠ Training Replay`;
- replay priority/sampling frequency не становится cognitive importance автоматически;
- core causal events отделены от heavy artifacts;
- completeness/integrity является structured property;
- storage/backend/file format намеренно не выбран.

---

# 4. Следующий допустимый Design Update

```text
DU-26 — Training Lifecycle
```

Цель `DU-26` — спроектировать **явную optimization/learning boundary MINDRA** поверх уже принятой data semantics: когда и что можно обучать, кто владеет optimizer state, как формируется Learning Update, как trainable state переходит между revisions и как online/offline learning не нарушает causal runtime.

Обязательные вопросы:

```text
Training Runtime ownership
trainable vs runtime/adaptive state
Learning Objective / Loss composition
TrainingSample consumption
batch/sequence/replay semantics
optimizer state ownership
parameter/update proposal
atomic Learning Update
agent_revision activation
in-flight cognition under old revision
online vs offline training
on-policy vs off-policy provenance
frozen Cortex vs adapters vs trainable modules
module-specific optimizers vs joint optimization
multi-objective losses / loss weighting
supervised / self-supervised / RL / distillation boundaries
privileged supervision flags
replay priorities / importance weights
representation drift after update
Memory/World/Self/Policy training interactions
catastrophic forgetting controls
rollback/reject failed update
validation before activation
RNG / determinism
training metrics vs agent-visible signals
checkpoint hooks
training failure/degradation
```

Особенно нужно определить:

- `Learning Update ≠ runtime state update ≠ Consolidation Event`;
- Training Runtime остаётся вне Agent cognition, хотя обновляемые parameters принадлежат Agent;
- optimizer/loss не должен скрыто жить внутри ordinary module `compute()`;
- Learning Update создаёт новую `agent_revision`/component revisions и не меняет in-flight computation задним числом;
- source `TrainingSample` provenance из `DU-25` сохраняется до конкретного update;
- privileged annotations допустимы только при explicit training condition;
- один universal optimizer для всех модулей не принимается заранее;
- Cortex fine-tuning/LoRA/QLoRA, RL, supervised и self-supervised algorithms остаются implementation/version choices до их анализа;
- update activation/rollback должен быть причинно наблюдаемым.

После принятия `DU-26` допускается:

```text
DU-27 — Checkpoint / Reproducibility / Compute
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

- Training Lifecycle;
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
