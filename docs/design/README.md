# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место общей архитектурной документации MINDRA.

Общий design cycle `DU-00 … DU-32` завершён. Semantic architecture заморожена как baseline `F31`, а software roadmap принят. Реализация ещё не начата.

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

## Cognitive/runtime boundaries

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

Карта: [`modules/README.md`](modules/README.md).

## External planes

- [`experience-data-replay.md`](experience-data-replay.md) — `DU-25`
- [`training-lifecycle.md`](training-lifecycle.md) — `DU-26`
- [`checkpoint-reproducibility-compute.md`](checkpoint-reproducibility-compute.md) — `DU-27`
- [`mindra-eval.md`](mindra-eval.md) — `DU-28`
- [`engineering-testing.md`](engineering-testing.md) — `DU-29`
- [`research-claims-limitations.md`](research-claims-limitations.md) — `DU-30`

## Semantic freeze

- [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md) — `DU-31`
- [`contracts/semantic-freeze-manifest.md`](contracts/semantic-freeze-manifest.md) — baseline `F31`

## Version roadmap

- [`version-roadmap.md`](version-roadmap.md) — `DU-32`
- [`../versions/README.md`](../versions/README.md) — software milestone index

Roadmap:

```text
v0.1 Core Kernel
→ v0.2 MicroWorld Interaction
→ v0.3 Cortex Gateway
→ v0.4 Memory & Restore
→ v0.5 World & Self
→ v0.6 Intrinsic / Drives / Appraisal
→ v0.7 Affect / Valuation / Salience
→ v0.8 Memory Regulation / Workspace
→ v0.9 Executive / Planner
→ v0.10 Training & Revision Lifecycle
→ v0.11 Research Harness
→ v0.12 Integration Hardening
→ v1.0 MINDRA Research Baseline
```

---

# Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0032` — accepted.

Последние решения:

- [`ADR-0031`](decisions/ADR-0031-semantic-contract-consistency-freeze.md) — semantic freeze `F31`;
- [`ADR-0032`](decisions/ADR-0032-vertical-capability-version-roadmap.md) — vertical capability roadmap вместо module-order implementation.

---

# Semantic contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Contracts `DU-07 … DU-30` semantic-frozen для `F31`; exact Python/API/serialization representation определяется version-specific design.

---

# Статус после DU-32

```text
DU-00 … DU-32 complete
F31 semantic architecture accepted
version roadmap accepted
implementation not started
```

Следующая разрешённая работа:

```text
Version Design — v0.1 Core Kernel
```

Для неё сначала создаются:

```text
docs/versions/v0.1/README.md
docs/versions/v0.1/implementation-sequence.md
```

И только после их принятия начинается coding.

Фактический статус: [`current.md`](current.md).
