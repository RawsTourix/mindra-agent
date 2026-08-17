# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, границы модулей, internal contracts, архитектурные решения и будущие version plans.

На текущем этапе сформирован documentation foundation и приняты `DU-01` … `DU-18`. Реализация ещё не начата.

---

# 1. Иерархия

```text
Concept
→ Design semantics / invariants
→ ADR
→ Candidate / exact internal contracts
→ Version specification
→ Implementation sequence
→ Engineering/research acceptance evidence
```

Research evidence не переписывает design напрямую: противоречащий результат инициирует design review.

---

# 2. Навигация

## Foundation

- [`principles.md`](principles.md);
- [`glossary.md`](glossary.md);
- [`documentation-plan.md`](documentation-plan.md);
- [`current.md`](current.md).

## Canonical system design

- [`system-context.md`](system-context.md) — `DU-01`;
- [`dependency-rules.md`](dependency-rules.md) — `DU-02`;
- [`execution-model.md`](execution-model.md) — `DU-03`;
- [`cognitive-state.md`](cognitive-state.md) — `DU-04`;
- [`module-lifecycle.md`](module-lifecycle.md) — `DU-05`;
- [`observability-and-intervention.md`](observability-and-intervention.md) — `DU-06`.

## Принятые subsystem boundaries

- [`modules/environment.md`](modules/environment.md) — `DU-07`;
- [`modules/perception.md`](modules/perception.md) — `DU-08`;
- [`modules/goals.md`](modules/goals.md) — `DU-09`;
- [`modules/cortex.md`](modules/cortex.md) — `DU-10`;
- [`modules/memory.md`](modules/memory.md) — `DU-11`;
- [`modules/world-model.md`](modules/world-model.md) — `DU-12`;
- [`modules/self-model.md`](modules/self-model.md) — `DU-13`;
- [`modules/intrinsic-signals.md`](modules/intrinsic-signals.md) — `DU-14`;
- [`modules/drives.md`](modules/drives.md) — `DU-15`;
- [`modules/appraisal.md`](modules/appraisal.md) — `DU-16`;
- [`modules/affect.md`](modules/affect.md) — `DU-17`;
- [`modules/valuation.md`](modules/valuation.md) — `DU-18`: typed multi-objective `ValueProfile`, explicit `ComparisonPolicy`, risk/constraint/feasibility и optional scalarization.

## Карта модулей

- [`modules/README.md`](modules/README.md).

## Decision records

- [`decisions/README.md`](decisions/README.md);
- `ADR-0001` … `ADR-0018` — accepted.

Последнее решение:

- [`ADR-0018`](decisions/ADR-0018-typed-multi-objective-valuation.md) — typed multi-objective Valuation с explicit comparison/scalarization boundary.

## Candidate contracts

- [`contracts/README.md`](contracts/README.md);
- [`contracts/environment.md`](contracts/environment.md);
- [`contracts/perception.md`](contracts/perception.md);
- [`contracts/goals.md`](contracts/goals.md);
- [`contracts/cortex.md`](contracts/cortex.md);
- [`contracts/memory.md`](contracts/memory.md);
- [`contracts/world-model.md`](contracts/world-model.md);
- [`contracts/self-model.md`](contracts/self-model.md);
- [`contracts/intrinsic-signals.md`](contracts/intrinsic-signals.md);
- [`contracts/drives.md`](contracts/drives.md);
- [`contracts/appraisal.md`](contracts/appraisal.md);
- [`contracts/affect.md`](contracts/affect.md);
- [`contracts/valuation.md`](contracts/valuation.md).

Candidate contracts определяют semantic machine-facing requirements, но exact Python API ещё не frozen.

## Versions

- [`versions/README.md`](versions/README.md).

---

# 3. Design Update discipline

`DU-xx` — самостоятельный архитектурный documentation update, а не software version.

Каждый update должен:

- иметь prerequisites;
- закрывать ограниченный набор design questions;
- проводить targeted research при реальном выборе;
- фиксировать responsibilities/non-goals/invariants;
- создавать ADR при существенном выборе;
- обновлять canonical owner;
- не протаскивать downstream decisions;
- завершаться consistency review и обновлением `current.md`.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update: `DU-19 — Salience / Attention`.

---

# 4. Правило существования отдельного модуля

Когнитивная аналогия сама по себе не является основанием для module boundary.

Отдельная ответственность должна иметь:

1. самостоятельную вычислительную роль;
2. явные input/output/state semantics;
3. независимый lifecycle/update boundary;
4. возможность отключения/подмены;
5. diagnostic/evaluation strategy;
6. функциональную роль, не дублирующую соседнюю.

`Valuation System` принят как отдельная boundary, потому что он единственный владеет semantics построения decision-relevant `ValueProfile` и explicit comparison между разнородными concerns, не выполняя final action selection.

---

# 5. Ключевые инварианты после DU-18

```text
ValueProfile ≠ ScalarizedValue
ValueProfile ≠ Training Reward
ValueProfile ≠ Critic Value
ValueProfile ≠ Policy Decision
predictive uncertainty ≠ RiskProfile
P(success) ≠ Utility/Value
External Task Feedback ≠ internal utility
Intrinsic Signal ≠ decision value
incomparable valuation ≠ technical failure
```

- multi-Goal/multi-Drive conflict сохраняется до explicit comparison;
- scalarization разрешена только через versioned `ComparisonPolicy`;
- weighted sum является policy/baseline, не universal architecture;
- Pareto/dominance, lexicographic, constraint-first, nonlinear и learned comparison families допустимы;
- hard constraints не обязаны кодироваться reward penalties;
- Risk требует outcome/downside semantics и explicit measure;
- feasibility/cost Self Model не являются value автоматически;
- prospective valuation имеет explicit horizon/temporal policy;
- imagined/counterfactual value сохраняет branch provenance;
- RL critic/reward остаются implementation/training choices;
- normalization/units/revisions не скрываются.

Фактический статус: [`current.md`](current.md).
