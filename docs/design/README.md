# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, cognitive/runtime/data/training/reproducibility/evaluation/testing/research-claim boundaries, contracts, ADR и будущие version plans.

На текущем этапе приняты `DU-01 … DU-30`. Реализация ещё не начата.

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

- [`research-claims-limitations.md`](research-claims-limitations.md) — `DU-30`: versioned claims, explicit scope/evidence/limitations/known unknowns, negative results и claim lifecycle.

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0030` — accepted.

Последнее решение:

- [`ADR-0030`](decisions/ADR-0030-versioned-evidence-bounded-research-claims.md) — versioned evidence-bounded Research Claims вместо свободного reporting prose.

## Candidate contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Последний добавленный contract:

- [`contracts/research-claims-limitations.md`](contracts/research-claims-limitations.md).

Exact Python API ещё не frozen.

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-31 — Contract + ADR Consistency Freeze
```

---

# Ключевые инварианты после DU-30

```text
Observation ≠ Interpretation ≠ ResearchClaim
claim scope ≠ universal scope
association ≠ causation
engineering verified ≠ functionally useful
null/inconclusive/invalid ≠ one result class
functional similarity ≠ phenomenological equivalence
supersession ≠ history rewrite
publication prose ≠ claim source of truth
```

- `ResearchClaim` имеет stable identity/revision и explicit `ClaimScope`;
- supporting/challenging evidence сохраняется;
- causal/generalization/architecture/efficiency claims требуют соответствующего evidence;
- limitations и known unknowns first-class;
- negative/null/inconclusive evidence сохраняется наравне с positive;
- failed module gate инициирует claim/design review, а не silent architecture mutation;
- Cortex/provider/compute/data/tuning dependence входит в scope/limitations;
- Workspace/Affect/Self Model/first-person Cortex output не являются сами по себе evidence consciousness/subjective experience;
- old claims weaken/supersede с сохранением lineage;
- public/report wording traceable до canonical claim revision;
- concrete paper/report/preregistration/evidence-score implementation не выбран.

Фактический статус: [`current.md`](current.md).
