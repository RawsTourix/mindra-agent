# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, subsystem/data boundaries, contracts, ADR и будущие version plans.

На текущем этапе приняты `DU-01 … DU-25`. Реализация ещё не начата.

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

## Принятые subsystem boundaries

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
- [`modules/action-boundary.md`](modules/action-boundary.md) — `DU-24`.

Карта областей: [`modules/README.md`](modules/README.md).

## Experience / Data Plane

- [`experience-data-replay.md`](experience-data-replay.md) — `DU-25`: append-only causal `Experience Journal`, derived trajectory/dataset/sample projections и отдельная Training Replay semantics.

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0025` — accepted.

Последнее решение:

- [`ADR-0025`](decisions/ADR-0025-causal-experience-journal-derived-projections.md) — causal Experience Journal как source of truth записанного опыта + versioned derived projections/samples.

## Candidate contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Последний добавленный contract:

- [`contracts/experience-data-replay.md`](contracts/experience-data-replay.md).

Exact Python API ещё не frozen.

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Каждый DU должен закрывать ограниченный scope, исследовать реальные альтернативы, фиксировать responsibilities/invariants, создавать ADR при существенном выборе, синхронизировать contracts/status и завершаться consistency review.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-26 — Training Lifecycle
```

---

# Ключевые инварианты после DU-25

```text
TraceEvent ≠ ExperienceEvent
Experience Journal ≠ Agent runtime state
Experience Journal ≠ Replay Buffer ≠ Agent Memory
Source Experience ≠ TrainingSample
ResearchAnnotation ≠ agent-visible payload
Agent Memory Replay ≠ Training Replay
```

- source events immutable по смыслу и append-only;
- physical append order не является causal order;
- stable IDs/logical scopes/causal parents/revisions сохраняют history;
- Episode/Decision/Transition/Sequence — derived projections;
- `Action Commit` может существовать без Environment transition;
- `execution_unknown` не fabricatе next state;
- Research Ground Truth хранится отдельными annotations;
- privileged dataset inclusion только explicit policy;
- hindsight/relabeling/re-encoding создают derived lineage;
- mixed `agent_revision` не скрывается;
- DatasetManifest фиксирует source selection/schema/transforms/splits/quality;
- Training Replay работает поверх source/derived samples и не создаёт natural experience;
- heavy artifacts могут храниться отдельно от core journal;
- storage/replay backend намеренно не выбран.

Фактический статус: [`current.md`](current.md).
