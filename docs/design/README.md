# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, границы модулей, internal contracts, архитектурные решения и будущие version plans.

На текущем этапе сформирован documentation foundation и приняты `DU-01` … `DU-17`. Детальные subsystem design добавляются последовательно после отдельного исследования вариантов.

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
- [`modules/self-model.md`](modules/self-model.md) — `DU-13`: capability facts, context-conditioned competence, calibrated Self Prediction и self-change semantics;
- [`modules/intrinsic-signals.md`](modules/intrinsic-signals.md) — `DU-14`: typed multi-provider Intrinsic Signal Layer без mandatory intrinsic reward/scalarization;
- [`modules/drives.md`](modules/drives.md) — `DU-15`: typed persistent Drive System, homeostatic/adaptive dynamics и explicit Goal/Valuation boundaries;
- [`modules/appraisal.md`](modules/appraisal.md) — `DU-16`: event-centered multidimensional Appraisal Profile, context/reappraisal semantics и границы с Intrinsic Signals/Drives/Affect/Valuation;
- [`modules/affect.md`](modules/affect.md) — `DU-17`: typed persistent history-dependent Affect State, temporal feedback и falsifiable module gate.

## Карта модулей

- [`modules/README.md`](modules/README.md) — карта принятых boundaries, будущих областей и design dependency graph.

`Environment`, `Perception`, `Goal System`, `Cortex`, `Memory Core`, `World Model`, `Self Model`, `Intrinsic Signals`, `Drive System`, `Appraisal System` и `Affect System` уже имеют accepted semantic design.

## Decision records

- [`decisions/README.md`](decisions/README.md);
- `ADR-0001` … `ADR-0017` — accepted.

Последнее решение:

- [`ADR-0017`](decisions/ADR-0017-typed-persistent-affect-state.md) — typed persistent Affect State с explicit history-dependent dynamics, optional low-dimensional views и обязательным falsification/matched-control gate.

## Candidate / exact internal contracts

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
- [`contracts/affect.md`](contracts/affect.md).

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

Текущий следующий update: `DU-18 — Valuation`.

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

`Cortex` принят как shared capability boundary. `Intrinsic Signals` — как семейство independently configurable providers. `Drive System` — как единый owner persistent typed regulatory states. `Appraisal System` — как event-centered multidimensional evaluation boundary. `Affect System` — как falsifiable persistent temporal-integration boundary, который должен быть пересмотрен, если matched controls не покажут специфической causal роли.

---

# 5. Новые ключевые инварианты DU-17

```text
Appraisal Record ≠ Affect State
Affect State ≠ Drive State
Affect State ≠ Utility/Value/Reward
Affect State ≠ emotion label
Affect history integration ≠ Memory Store
Affect_t → Appraisal_t → Affect_(t+1)
imagined Affect ≠ real committed Affect
Environment reset ≠ Affect reset
```

- Affect интегрирует appraisal-history во времени, но не заменяет Appraisal history/Memory;
- нет обязательного valence/arousal/PAD или discrete emotion representation;
- previous committed Affect может быть input будущего Appraisal, но same-wave recursive cycle запрещён;
- predicted appraisal влияет на current Affect только через explicit anticipatory source policy;
- imagined appraisal по умолчанию изменяет branch-local simulated Affect;
- retrospective current reappraisal может менять current Affect без переписывания прошлого;
- Affect не мутирует Goals/Drives и не вычисляет decision utility;
- будущие Valuation/Salience/Memory Regulation получают Affect только через explicit boundaries;
- logical time используется вместо wall-clock;
- causally relevant private/recurrent/baseline/RNG state включается в Agent Snapshot;
- самостоятельность Affect проверяется через `NoAffect`, `ResetEveryEvent`, shuffled-history и matched recurrent controls.

Valence/arousal/PAD, discrete emotion taxonomies и конкретные neural affect models являются research evidence/candidate approaches, а не canonical implementation requirements.

Фактический статус: [`current.md`](current.md).
