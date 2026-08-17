# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, cognitive/runtime/data/training/reproducibility/evaluation/testing/research-claim boundaries, contracts, ADR, consistency freeze и будущие version plans.

На текущем этапе приняты `DU-01 … DU-31`. Реализация ещё не начата.

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

## Cognitive/runtime subsystem boundaries

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

- [`experience-data-replay.md`](experience-data-replay.md) — `DU-25`.

## Training Plane

- [`training-lifecycle.md`](training-lifecycle.md) — `DU-26`.

## Checkpoint / Reproducibility / Compute Plane

- [`checkpoint-reproducibility-compute.md`](checkpoint-reproducibility-compute.md) — `DU-27`.

## Evaluation Plane

- [`mindra-eval.md`](mindra-eval.md) — `DU-28`.

## Engineering Verification Plane

- [`engineering-testing.md`](engineering-testing.md) — `DU-29`.

## Research Claims / Limitations Plane

- [`research-claims-limitations.md`](research-claims-limitations.md) — `DU-30`.

## Semantic consistency freeze

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md) — `DU-31`;
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md) — machine-facing baseline `F31`.

Статус после `DU-31`:

```text
DU-01 … DU-30 semantic design
= baseline F31
= ready for version planning
```

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0031` — accepted.

Последнее решение:

- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md) — semantic contract consistency freeze перед Version Roadmap.

## Semantic contracts

Каталог: [`contracts/README.md`](contracts/README.md).

После `DU-31` contracts `DU-07 … DU-30` считаются **semantic-frozen for roadmap baseline F31**, но exact Python/API/serialization representation ещё не frozen.

Freeze manifest:

- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md).

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-32 — Version Roadmap
```

---

# Ключевые инварианты после DU-31

```text
semantic ownership frozen
exact Python API not frozen

CognitiveState ≠ AgentSnapshot ≠ Checkpoint
Memory Core ≠ Memory Regulation
Retrieval ≠ Memory Replay ≠ Training Replay
Consolidation ≠ Learning Update
Scheduler ≠ Executive ≠ Policy
Planner ≠ Policy ≠ Action Boundary
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
Evaluation ≠ Engineering Verification ≠ Research Claims
```

- `F31` закрепляет normative reading `DU-01 … DU-30`;
- CR-01 … CR-05 разрешают накопленные generic→specialized wording ambiguities;
- 24 semantic boundary contracts покрывают `DU-07 … DU-30`;
- breaking semantic change после freeze требует нового ADR;
- version roadmap может выбирать framework/model/algorithm/storage/API только при сохранении frozen meaning;
- conditional Affect/Workspace/Executive/Planner остаются falsifiable и не объявляются empirically proven;
- implementation начинается только после `DU-32` и version-specific implementation sequence.

Фактический статус: [`current.md`](current.md).
