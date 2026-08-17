# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, subsystem/data/training boundaries, contracts, ADR и будущие version plans.

На текущем этапе приняты `DU-01 … DU-26`. Реализация ещё не начата.

---

# Навигация

## Foundation

- [`principles.md`](principles.md)
- [`glossary.md`](glossary.md)
- [`documentation-plan.md`](documentation-plan.md)
- [`current.md`](current.md)

## Canonical system design

- [`system-context.md`](system-context.md) — `DU-01`
- [`dependency-rules.md`](dependency-rules.md) — `DU-02`
- [`execution-model.md`](execution-model.md) — `DU-03`
- [`cognitive-state.md`](cognitive-state.md) — `DU-04`
- [`module-lifecycle.md`](module-lifecycle.md) — `DU-05`
- [`observability-and-intervention.md`](observability-and-intervention.md) — `DU-06`

## Принятые cognitive/runtime subsystem boundaries

- [`modules/environment.md`](modules/environment.md) — `DU-07`
- [`modules/perception.md`](modules/perception.md) — `DU-08`
- [`modules/goals.md`](modules/goals.md) — `DU-09`
- [`modules/cortex.md`](modules/cortex.md) — `DU-10`
- [`modules/memory.md`](modules/memory.md) — `DU-11`
- [`modules/world-model.md`](modules/world-model.md) — `DU-12`
- [`modules/self-model.md`](modules/self-model.md) — `DU-13`
- [`modules/intrinsic-signals.md`](modules/intrinsic-signals.md) — `DU-14`
- [`modules/drives.md`](modules/drives.md) — `DU-15`
- [`modules/appraisal.md`](modules/appraisal.md) — `DU-16`
- [`modules/affect.md`](modules/affect.md) — `DU-17`
- [`modules/valuation.md`](modules/valuation.md) — `DU-18`
- [`modules/salience.md`](modules/salience.md) — `DU-19`
- [`modules/memory-regulation.md`](modules/memory-regulation.md) — `DU-20`
- [`modules/workspace.md`](modules/workspace.md) — `DU-21`
- [`modules/executive-control.md`](modules/executive-control.md) — `DU-22`
- [`modules/policy-planner.md`](modules/policy-planner.md) — `DU-23`
- [`modules/action-boundary.md`](modules/action-boundary.md) — `DU-24`

Карта областей: [`modules/README.md`](modules/README.md).

## Experience / Data Plane

- [`experience-data-replay.md`](experience-data-replay.md) — `DU-25`: append-only causal `Experience Journal`, derived projections/samples и Training Replay provenance.

## Training Plane

- [`training-lifecycle.md`](training-lifecycle.md) — `DU-26`: external Training Runtime, pinned base revisions, explicit objectives/gradient flow, candidate revisions, validation и atomic activation.

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0026` — accepted.

Последнее решение:

- [`ADR-0026`](decisions/ADR-0026-candidate-revision-validated-activation-training-lifecycle.md) — Training Runtime обучает pinned base revision в candidate state; validation предшествует atomic activation новой Agent revision.

## Candidate contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Последний добавленный contract:

- [`contracts/training-lifecycle.md`](contracts/training-lifecycle.md).

Exact Python API ещё не frozen.

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Каждый DU закрывает ограниченный scope, исследует альтернативы, фиксирует responsibilities/invariants, создаёт ADR при существенном выборе и заканчивается consistency review.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-27 — Checkpoint / Reproducibility / Compute
```

---

# Ключевые инварианты после DU-26

```text
TraceEvent ≠ ExperienceEvent
Experience Journal ≠ Agent runtime state
Source Experience ≠ TrainingSample
Training Runtime ≠ cognitive module
Runtime State Update ≠ Learning Update
Consolidation Event ≠ Learning Update
Replay Selection ≠ Learning Update
Training Objective ≠ Agent Goal ≠ ValueProfile
runtime dependency graph ≠ gradient graph
optimizer state ≠ CognitiveState
CandidateRevisionBundle ≠ Active AgentRevision
behavior revision ≠ learner revision допускается явно
```

- TrainingPlan pin'ит base revisions/data/visibility/objectives/gradient policies;
- source sample provenance доходит до LearningUpdateRecord;
- candidate update не становится live Agent автоматически;
- activation происходит только на explicit safe boundary;
- in-flight cognition не меняет revision задним числом;
- joint coupled revisions активируются атомарно;
- privileged supervision всегда explicit;
- representation-breaking update требует compatibility/migration semantics;
- failed candidate не мутирует live Agent;
- rollback не стирает историю update/activation;
- concrete optimizer/framework/algorithm/PEFT method не выбран.

Фактический статус: [`current.md`](current.md).
