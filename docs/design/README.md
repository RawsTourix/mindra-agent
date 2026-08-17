# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, cognitive/runtime/data/training/reproducibility/evaluation boundaries, contracts, ADR и будущие version plans.

На текущем этапе приняты `DU-01 … DU-28`. Реализация ещё не начата.

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

## Checkpoint / Reproducibility / Compute Plane

- [`checkpoint-reproducibility-compute.md`](checkpoint-reproducibility-compute.md) — `DU-27`: manifest-driven checkpoint, causal capture/restore, reproducibility claims, software/hardware/compute manifests.

## Evaluation Plane

- [`mindra-eval.md`](mindra-eval.md) — `DU-28`: versioned evaluation studies/conditions, matched controls, paired interventions, typed metrics, statistical protocol, module gates и compute-normalized attribution.

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0028` — accepted.

Последнее решение:

- [`ADR-0028`](decisions/ADR-0028-multi-layer-causal-evaluation-harness.md) — multi-layer causal Evaluation Harness вместо universal leaderboard score.

## Candidate contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Последний добавленный contract:

- [`contracts/mindra-eval.md`](contracts/mindra-eval.md).

Exact Python API ещё не frozen.

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Каждый DU закрывает ограниченный scope, исследует альтернативы, фиксирует responsibilities/invariants, создаёт ADR при существенном выборе и заканчивается consistency review.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-29 — Engineering Testing
```

---

# Ключевые инварианты после DU-28

```text
Evaluation Runtime ≠ Agent cognition
Task score ≠ module/causal/calibration evidence
EvaluationCondition ≠ architecture name only
nested episode ≠ independent training replicate
ablation ≠ matched semantic control
Policy pre-Gate quality ≠ post-Gate system quality
actual compute evidence ≠ nominal resource budget
invalid/censored/execution_unknown ≠ ordinary failure
```

- evaluation condition pin'ит checkpoint/world/revisions/resources/data/software/hardware context;
- confirmatory primary hypothesis/metrics/statistical plan фиксируются до просмотра outcome;
- stochastic claims требуют distribution/uncertainty evidence;
- experimental/statistical unit и replicate nesting explicit;
- paired causal branches требуют достаточного `DU-27` restore level;
- evaluator Ground Truth остаётся privileged;
- composite score optional и сохраняет lineage source metrics;
- `Affect`, `Workspace`, `Planner`, `Executive Control` имеют explicit negative gates;
- Policy, Action Gate и final system behavior оцениваются раздельно;
- compute/data/context/tuning differences входят в attribution;
- strength research claim не превышает strength evidence;
- concrete benchmark/statistics/plotting implementation не выбран.

Фактический статус: [`current.md`](current.md).
