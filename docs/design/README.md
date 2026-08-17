# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, границы модулей, internal contracts, архитектурные решения и будущие version plans.

На текущем этапе сформирован documentation foundation и приняты `DU-01` … `DU-16`. Детальные subsystem design добавляются последовательно после отдельного исследования вариантов.

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
- [`modules/intrinsic-signals.md`](modules/intrinsic-signals.md) — `DU-14`: typed multi-provider Intrinsic Signal Layer без обязательного intrinsic reward/scalarization;
- [`modules/drives.md`](modules/drives.md) — `DU-15`: typed persistent Drive System, homeostatic/adaptive dynamics и explicit Goal/Valuation boundaries;
- [`modules/appraisal.md`](modules/appraisal.md) — `DU-16`: event-centered multidimensional Appraisal Profile, context/reappraisal semantics и границы с Intrinsic Signals/Drives/Affect/Valuation.

## Карта модулей

- [`modules/README.md`](modules/README.md) — предварительная карта архитектурных областей.

`Environment`, `Perception`, `Goal System`, `Cortex`, `Memory Core`, `World Model`, `Self Model`, `Intrinsic Signals`, `Drive System` и `Appraisal System` уже имеют accepted semantic design. Остальные области проектируются последовательно.

## Decision records

- [`decisions/README.md`](decisions/README.md);
- `ADR-0001` … `ADR-0016` — accepted.

Последнее решение:

- [`ADR-0016`](decisions/ADR-0016-multidimensional-event-centered-appraisal.md) — event-centered typed multidimensional Appraisal без mandatory emotion label/global utility scalar.

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
- [`contracts/appraisal.md`](contracts/appraisal.md).

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

Текущий следующий update: `DU-17 — Affect Dynamics`.

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

`Cortex` принят как shared capability boundary. `Intrinsic Signals` приняты как семейство independently configurable providers. `Drive System` принят как единый ownership boundary persistent typed drive states с pluggable drive components. `Appraisal System` принят как event-centered multidimensional evaluation boundary, а не emotion-label/reward classifier.

---

# 5. Текущие ключевые инварианты

В дополнение к предыдущим DU теперь зафиксировано:

```text
Appraisal ≠ Intrinsic Signal ≠ Drive ≠ Affect ≠ Valuation
Appraisal Target ≠ Appraisal Context
relevance ≠ Salience ≠ novelty ≠ utility
goal congruence ≠ global Goal priority/value
drive conduciveness ≠ committed Drive update
expectedness ≠ novelty ≠ prediction discrepancy ≠ predictive surprisal
controllability ≠ coping potential
urgency ≠ Salience ≠ action priority
Appraisal local polarity ≠ Utility/Value/Reward
reappraisal ≠ mutation of historical AppraisalRecord
```

- Appraisal оценивает causally identifiable target относительно explicit committed context;
- actual/predicted/imagined/retrospective/intervened targets сохраняют разную provenance;
- Appraisal Profile многомерный и не имеет mandatory emotion label/global scalar;
- relevance не становится attention allocation;
- per-goal congruence не решает Goal conflict;
- per-drive conduciveness не меняет Drive State;
- controllability относится к возможности влиять действиями на ситуацию, coping potential — к способности текущего Agent справиться/адаптироваться;
- expectedness использует prior expectation evidence, а не переименовывает novelty/surprise;
- normative dimension не существует без отдельной agent-owned norm semantics;
- reappraisal создаёт новый historical record;
- Memory retrieval/Cortex usage остаются explicit causal operations;
- partial/unknown dimensions и failure являются first-class states;
- Appraisal не хранит hidden persistent Affect и не выполняет Valuation/Policy.

Human appraisal theories, emotion taxonomies и конкретные LLM appraisal frameworks являются research evidence/candidate approaches, но не canonical implementation requirements.

Фактический статус: [`current.md`](current.md).
