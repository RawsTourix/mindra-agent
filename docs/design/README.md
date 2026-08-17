# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, subsystem boundaries, contracts, ADR и будущие version plans.

На текущем этапе приняты `DU-01 … DU-21`. Реализация ещё не начата.

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
- [`modules/workspace.md`](modules/workspace.md) — `DU-21`: bounded temporary shared broadcast Workspace с explicit admission/budget и falsifiable module gate.

Карта областей: [`modules/README.md`](modules/README.md).

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0021` — accepted.

Последнее решение:

- [`ADR-0021`](decisions/ADR-0021-bounded-broadcast-workspace-overlay.md) — bounded broadcast Workspace overlay с first-class `NoWorkspace`, matched controls и negative gate.

## Candidate contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Последний добавленный contract:

- [`contracts/workspace.md`](contracts/workspace.md).

Exact Python API ещё не frozen.

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Каждый DU должен закрывать ограниченный scope, исследовать реальные альтернативы, фиксировать responsibilities/invariants, создавать ADR при существенном выборе, синхронизировать contracts/status и завершаться consistency review.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-22 — Metacognitive / Executive Control
```

---

# Ключевые инварианты после DU-21

```text
CognitiveState ≠ Workspace
published state ≠ Workspace admission
SalienceProfile ≠ Workspace admission
WorkspaceBudget ≠ AttentionBudget ≠ MemoryBudget ≠ Executive budget
WorkspaceItem ≠ source truth
Workspace ≠ Memory
Workspace eviction ≠ Memory forgetting
Memory retrieval ≠ Workspace admission
Workspace ≠ Cortex context
broadcast ≠ callback/module execution
imagined Workspace ≠ real Workspace
Workspace ≠ Policy
Workspace ≠ proof of consciousness
```

- Workspace работает только с explicit proposals/candidates;
- capacity/bandwidth должны быть реальными и наблюдаемыми;
- Salience даёт evidence/hint, но не владеет admission;
- admitted content сохраняет source revision/provenance/authority;
- global availability означает доступ declared consumers, а не unrestricted ambient input;
- Workspace может переживать несколько Cognitive Cycles, но не становится долговременной Memory;
- Cortex context packing остаётся отдельной explicit operation;
- branch/imagination используют branch-local Workspace;
- `NoWorkspace`, DirectReads и matched buffer controls обязательны;
- отрицательный результат может привести к удалению отдельной Workspace boundary.

Фактический статус: [`current.md`](current.md).
