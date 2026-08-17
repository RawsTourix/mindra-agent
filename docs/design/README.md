# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, границы модулей, internal contracts, архитектурные решения и будущие version plans.

На текущем этапе сформирован documentation foundation и приняты `DU-01` … `DU-13`. Детальные subsystem design добавляются последовательно после отдельного исследования вариантов.

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

# 2. Текущая навигация

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

## Спроектированные subsystem boundaries

- [`modules/environment.md`](modules/environment.md) — `DU-07`: Environment/MicroWorld;
- [`modules/perception.md`](modules/perception.md) — `DU-08`: Perception/Canonical Percept;
- [`modules/goals.md`](modules/goals.md) — `DU-09`: Goal System/Goal Graph;
- [`modules/cortex.md`](modules/cortex.md) — `DU-10`: Cortex Gateway и backend-neutral capability boundary;
- [`modules/memory.md`](modules/memory.md) — `DU-11`: canonical Memory Store, MemoryRecord, derived representations/indexes и explicit retrieval boundary;
- [`modules/world-model.md`](modules/world-model.md) — `DU-12`: World Belief, assimilation, action-conditioned prediction, imagination, uncertainty и prediction-error boundary;
- [`modules/self-model.md`](modules/self-model.md) — `DU-13`: capability facts, context-conditioned competence, calibrated Self Prediction и self-change semantics.

## Карта модулей

- [`modules/README.md`](modules/README.md) — предварительная карта архитектурных областей.

`Environment`, `Perception`, `Goal System`, `Cortex`, `Memory Core`, `World Model` и `Self Model` уже имеют accepted semantic design. Остальные области проектируются последовательно.

## Decision records

- [`decisions/README.md`](decisions/README.md);
- `ADR-0001` … `ADR-0013` — accepted.

Последнее решение:

- [`ADR-0013`](decisions/ADR-0013-hybrid-functional-self-model.md) — hybrid functional Self Model: self-observable capability facts отдельно от learned competence и calibrated predictions.

## Candidate / exact internal contracts

- [`contracts/README.md`](contracts/README.md);
- [`contracts/environment.md`](contracts/environment.md);
- [`contracts/perception.md`](contracts/perception.md);
- [`contracts/goals.md`](contracts/goals.md);
- [`contracts/cortex.md`](contracts/cortex.md);
- [`contracts/memory.md`](contracts/memory.md);
- [`contracts/world-model.md`](contracts/world-model.md);
- [`contracts/self-model.md`](contracts/self-model.md).

Candidate contracts определяют semantic machine-facing requirements, но exact Python API ещё не frozen.

## Versions

- [`versions/README.md`](versions/README.md).

---

# 3. Design Update discipline

`DU-xx` — идентификатор самостоятельного архитектурного documentation update, а не software version.

Каждый update должен:

- иметь prerequisites;
- закрывать ограниченный набор design questions;
- проводить targeted research там, где есть реальный выбор;
- фиксировать responsibilities/non-goals/invariants;
- создавать ADR при значимом выборе между вариантами;
- обновлять canonical owner темы;
- не протаскивать downstream decisions раньше времени;
- завершаться consistency review и обновлением `current.md`.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update: `DU-14 — Intrinsic Signals`.

---

# 4. Правило существования отдельного модуля

Когнитивная аналогия сама по себе не является основанием для module boundary.

Отдельная ответственность должна иметь:

1. самостоятельную вычислительную роль;
2. явные input/output/state semantics;
3. независимый lifecycle или значимую update boundary;
4. возможность отключения/подмены;
5. diagnostic/evaluation strategy;
6. функциональную роль, не дублирующую соседнюю.

`Cortex` принят как shared capability boundary. `Memory Core`, `World Model` и `Self Model` являются отдельными agent-owned responsibilities с независимо проверяемыми ролями.

---

# 5. Текущие ключевые инварианты

В дополнение к предыдущим DU теперь зафиксировано:

```text
MemoryRecord ≠ embedding/index entry
Canonical Percept ≠ World Belief ≠ World Prediction
World Prediction ≠ observed fact
Imagined Transition ≠ Environment Transition
prediction error ≠ reward / intrinsic utility
predictive uncertainty ≠ risk / value
Agent Capability Fact ≠ Learned Competence Estimate ≠ Self Prediction
P(success) ≠ uncertainty/support самой self-estimate
Self Model ≠ Cortex self-report ≠ Executive Control
```

- Self Model использует versioned self-observable capability facts и causal Self Evidence;
- capability availability не означает competence;
- competence context/domain-conditioned, а не один global scalar;
- вероятность успеха требует explicit target/horizon/context;
- calibration является отдельным проверяемым свойством;
- evaluator-only truth не становится natural self-evidence;
- behavior-relevant Agent revision может сделать старые competence estimates stale;
- Self Model оценивает, но не принимает metacognitive/behavior decisions;
- Cortex self-report остаётся optional derived evidence;
- exact Agent snapshot обязан учитывать causally relevant Self Model state;
- `NoSelfModel`, Dummy и Control configurations различаются.

Concrete calibration/competence estimator, task taxonomy и Self Model training algorithm остаются candidate implementation choices.

Фактический статус: [`current.md`](current.md).
