# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, subsystem boundaries, contracts, ADR и будущие version plans.

На текущем этапе приняты `DU-01 … DU-20`. Реализация ещё не начата.

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
- [`modules/memory.md`](modules/memory.md) — `DU-11` Memory Core
- [`modules/world-model.md`](modules/world-model.md) — `DU-12`
- [`modules/self-model.md`](modules/self-model.md) — `DU-13`
- [`modules/intrinsic-signals.md`](modules/intrinsic-signals.md) — `DU-14`
- [`modules/drives.md`](modules/drives.md) — `DU-15`
- [`modules/appraisal.md`](modules/appraisal.md) — `DU-16`
- [`modules/affect.md`](modules/affect.md) — `DU-17`
- [`modules/valuation.md`](modules/valuation.md) — `DU-18`
- [`modules/salience.md`](modules/salience.md) — `DU-19`
- [`modules/memory-regulation.md`](modules/memory-regulation.md) — `DU-20`: budget-aware retention/forgetting/replay и source-preserving consolidation поверх Memory Core.

Карта областей: [`modules/README.md`](modules/README.md).

## Decisions

- [`decisions/README.md`](decisions/README.md)
- `ADR-0001 … ADR-0020` — accepted.

Последнее решение:

- [`ADR-0020`](decisions/ADR-0020-source-preserving-budget-aware-memory-regulation.md) — source-preserving budget-aware Memory Regulation с gated consolidation.

## Candidate contracts

Каталог: [`contracts/README.md`](contracts/README.md).

Последний добавленный contract:

- [`contracts/memory-regulation.md`](contracts/memory-regulation.md).

Exact Python API ещё не frozen.

---

# Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Каждый DU должен:

- закрывать ограниченный design scope;
- исследовать реальные альтернативы;
- фиксировать responsibilities/non-goals/invariants;
- создавать ADR при существенном выборе;
- обновлять canonical owner/contracts/status;
- не протаскивать downstream decisions;
- завершаться consistency review.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update:

```text
DU-21 — Workspace
```

---

# Ключевые инварианты после DU-20

```text
MemoryRecord ≠ embedding/index
Memory Core validation ≠ Regulation admission
Memory Core owner ≠ Regulation policy owner
SalienceProfile ≠ memory lifecycle decision
forgetting ≠ physical deletion
retrieval ≠ Agent Memory Replay ≠ Training Replay
consolidation ≠ in-place rewrite
consolidation ≠ Learning Update
representation maintenance ≠ semantic consolidation
Derived MemoryRecord ≠ source episode
```

- Memory Regulation работает через purpose-specific policies, а не universal `memory_importance`;
- `MemoryBudget` explicit и может быть multi-dimensional;
- access/retrieval frequency не считается automatic importance;
- aging использует logical time;
- consolidation gated и может быть отключена;
- episodic-only является first-class baseline/control;
- derived memory создаётся как новый record с `derived_from`/support/conflict provenance;
- consolidation не повышает source authority автоматически;
- contradictions/minority evidence не должны исчезать скрытым majority-vote;
- source retention после consolidation регулируется отдельно;
- re-encoding/index rebuild не создаёт semantic knowledge;
- slow-weight/optimizer learning остаётся downstream `DU-26`;
- compression ratio без source fidelity/behavioral benefit не доказывает полезность consolidation.

Фактический статус: [`current.md`](current.md).
