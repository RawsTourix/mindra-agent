# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, cognitive/runtime/data/training/reproducibility boundaries, contracts, ADR и будущие version plans.

На текущем этапе приняты `DU-01 … DU-27`. Реализация ещё не начата.

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

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0027` — accepted.

Последнее решение:

- [`ADR-0027`](decisions/ADR-0027-manifest-driven-causal-checkpoint-restore.md) — manifest-driven causal checkpoint с explicit scope, integrity, restore profile и scoped reproducibility guarantees.

## Candidate contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Последний добавленный contract:

- [`contracts/checkpoint-reproducibility-compute.md`](contracts/checkpoint-reproducibility-compute.md).

Exact Python API ещё не frozen.

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Каждый DU закрывает ограниченный scope, исследует альтернативы, фиксирует responsibilities/invariants, создаёт ADR при существенном выборе и заканчивается consistency review.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-28 — MINDRA-Eval
```

---

# Ключевые инварианты после DU-27

```text
AgentSnapshot ≠ persistent Checkpoint
Checkpoint ≠ TrainingResumeCheckpoint ≠ ExperimentManifest
same seed ≠ same RNG state ≠ guaranteed same execution
semantic restore ≠ bitwise reproducibility
active revision ≠ candidate revision
artifact identity ≠ physical path
Agent checkpoint ≠ Environment snapshot
infrastructure ComputeManifest ≠ CognitiveResourceEnvelope
```

- checkpoint имеет explicit scope и required/optional state classes;
- capture относится к согласованной causal boundary;
- final manifest commit происходит только после required artifact verification;
- `execution_unknown` блокирует unsafe retry/branch semantics до reconciliation;
- full-system restore использует causally aligned Agent/Environment state;
- exact/compatible/portable/approximate restore различаются;
- reproducibility claim всегда scoped и evidence-backed;
- software/hardware/determinism manifests входят в сильные reproducibility claims;
- training-resume state интегрирован с `DU-26`;
- migration/delta chains имеют explicit lineage/integrity;
- concrete serialization/hash/storage/profiler implementation не выбран.

Фактический статус: [`current.md`](current.md).
