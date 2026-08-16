# ADR-0004 — Версионированный committed CognitiveState вместо общего mutable bus

## Статус

`accepted`

## Связанный Design Update

`DU-04 — CognitiveState Semantics`

## Канонический документ-владелец

[`../cognitive-state.md`](../cognitive-state.md)

---

# 1. Контекст

После `DU-01`–`DU-03` MINDRA уже различает:

- логическую границу Agent и внешней инфраструктуры;
- explicit Composition Root и запрет hidden Service Locator;
- hierarchical logical time;
- `Cognitive Cycle`, `Action Commit`, `Outcome Commit` и `Learning Update`;
- необходимость causal replay и counterfactual experiments.

Следующий фундаментальный вопрос — каким образом cognitive modules должны видеть и изменять общее внутреннее состояние.

Исследовательские требования особенно строгие:

- значение должно быть связано с конкретным causal context;
- module contribution должен быть диагностируем;
- evaluator должен уметь clone/intervene без скрытого изменения исходного состояния;
- async/concurrent execution не должно создавать случайный `last-write-wins`;
- hidden inplace mutation не должна менять уже записанную trajectory;
- смена state framework не должна менять canonical semantics.

---

# 2. Проблема

Нужно выбрать canonical state mutation model, который:

1. поддерживает явное ownership;
2. не создаёт shared mutable global state;
3. позволяет несколько внутренних module computations;
4. совместим с causal ordering `DU-03`;
5. поддерживает clone/fork/replay;
6. позволяет обнаруживать stale updates и write conflicts;
7. не требует конкретного container framework;
8. остаётся эффективным для tensor workloads.

---

# 3. Рассмотренные варианты

## Вариант A — общий mutable dictionary/state bus

Семантика:

```text
module A → state["x"] = ...
module B → state["y"] = ...
module C → читает текущее содержимое
```

### Плюсы

- минимальный implementation overhead;
- естественно для раннего прототипа;
- легко использовать обычный dict/TensorDict inplace.

### Минусы

- порядок writes становится скрытой semantics;
- потребитель может увидеть partially updated state;
- inplace tensor mutation может изменить старое состояние задним числом;
- difficult causal replay;
- difficult counterfactual clone;
- write ownership трудно проверять;
- async computation усиливает race/conflict risk;
- trajectory snapshot может перестать соответствовать фактически использованным данным.

**Решение:** отклонён как canonical model.

---

## Вариант B — mutable bus с locks/single-writer discipline

Семантика:

- state остаётся mutable;
- writes защищаются lock/ownership rules;
- модули меняют state непосредственно в разрешённых фазах.

### Плюсы

- дешевле по памяти, чем наивный deep-copy snapshot;
- можно обеспечить часть atomicity;
- относительно просто реализовать.

### Минусы

- semantic correctness начинает зависеть от lock discipline;
- retained references/inplace tensor writes всё ещё опасны;
- clone/fork требует специальной логики;
- state before/after difficult to reason about без explicit revisions;
- physical concurrency начинает сильнее определять cognition semantics;
- debugging требует реконструировать последовательность mutations.

**Решение:** не принимается как canonical semantics. Locks/copy-on-write могут использоваться как implementation mechanism под snapshot abstraction.

---

## Вариант C — committed immutable snapshots + staged owner-scoped updates

Семантика:

```text
Committed Rn
   ↓ read
compute proposed updates
   ↓ validate
atomic logical commit
   ↓
Committed Rn+1
```

### Плюсы

- state имеет ясную causal identity;
- already committed revision не меняется;
- естественная основа для replay/counterfactual;
- stale-base updates можно обнаружить;
- write ownership можно валидировать;
- conflicts не маскируются `last-write-wins`;
- partial update не виден до commit;
- физическая async/concurrency может быть скрыта за deterministic commit semantics;
- container/framework можно заменить.

### Минусы

- требуется explicit commit coordinator;
- нужен design patch/update objects;
- наивная реализация может быть дорогой по памяти;
- нужно продумать structural sharing/copy-on-write;
- commit granularity и scheduler становятся отдельным архитектурным вопросом.

**Решение:** принят.

---

## Вариант D — event sourcing без канонического current snapshot

Семантика:

```text
event log
→ текущий state всегда является projection/reduction истории
```

### Плюсы

- сильная provenance;
- исторические изменения естественно сохраняются;
- удобно для audit/replay.

### Минусы

- cognitive modules постоянно нуждаются в materialized current state;
- значительно усложняется runtime hot path;
- event schema становится слишком ранним фундаментом;
- research logging смешивается с cognition architecture;
- для tensor workloads projection всей истории является ненужной стоимостью.

**Решение:** отклонён как основной state model.

Event/trajectory log остаётся допустимым **дополнением** для observability/evidence, но не заменяет committed current state.

---

# 4. Evidence существующих инструментов

Конкретный framework не выбирается этим ADR.

Однако актуальный TensorDict показывает техническую реализуемость ряда требований:

- nested keys;
- batch dimensions;
- device conversion;
- cloning;
- state serialization.

Источники:

- https://docs.pytorch.org/tensordict/stable/reference/generated/tensordict.TensorDict.html
- https://docs.pytorch.org/tensordict/stable/saving.html

`TensorClass`/`TypedTensorDict` также предоставляют frozen forms, что подтверждает практичность read-only container surface:

- https://docs.pytorch.org/tensordict/stable/reference/generated/tensordict.TensorClass.html
- https://docs.pytorch.org/tensordict/stable/reference/ttd.html

При этом конкретный container lock сам по себе не гарантирует semantic immutability вложенного storage; MINDRA принимает более высокий contract-level invariant.

---

# 5. Принятое решение

MINDRA принимает:

1. `CognitiveState` как versioned committed snapshot;
2. semantic immutability уже committed revision;
3. owner-scoped proposed updates вместо direct mutation;
4. explicit commit boundary для публикации нового состояния;
5. state lineage/base revision для causal provenance;
6. detection конфликтов/stale-base updates вместо silent `last-write-wins`;
7. freedom implementation использовать structural sharing/copy-on-write/locking, если observable semantics сохранена;
8. event/trajectory logging как отдельную evidence layer, а не единственный источник current state.

---

# 6. Дополнительные invariants

## ADR4-01

Read-only semantics относятся и к вложенным tensor values: inplace mutation committed value считается нарушением, даже если container API формально позволяет её.

## ADR4-02

Один canonical path имеет одного semantic write owner, если отдельный design не вводит явный aggregator/reducer owner.

## ADR4-03

Proposed update связан с base revision; update из устаревшей base не применяется молча.

## ADR4-04

Commit создаёт новое логически целостное состояние; consumers не видят partial staged writes.

## ADR4-05

`CognitiveState` не обязан содержать всё causally relevant private state Agent.

## ADR4-06

Полный counterfactual/restore требует отдельного full Agent Snapshot, если private state/parameters/Memory влияют на поведение.

---

# 7. Последствия

## Положительные

- causal replay получает чёткие state anchors;
- controlled intervention может строиться на fork revision;
- hidden shared mutation архитектурно запрещена;
- module ownership становится проверяемым;
- async execution не обязана определять visible update order;
- state framework остаётся заменяемым;
- trajectory artifacts можно связывать с exact state revision;
- становится возможен строгий stale-value/stale-update анализ.

## Отрицательные / стоимость

- потребуется state coordinator/commit semantics;
- необходимо различать shared state и private state;
- потребуется metadata/provenance discipline;
- careless deep-copy implementation может быть слишком дорогой;
- update conflict handling нужно спроектировать до implementation;
- Codex нельзя позволять упрощать систему до shared mutable dict ради скорости разработки.

---

# 8. Что решение намеренно не определяет

ADR не выбирает:

- TensorDict;
- immutable dataclass;
- Pydantic;
- concrete patch/update class;
- state storage layout;
- copy-on-write library;
- exact commit frequency;
- scheduler;
- exact namespace paths;
- field dimensions/dtypes;
- exact availability encoding;
- full checkpoint schema.

---

# 9. Обязательные consistency updates

После принятия ADR должны быть согласованы:

- `docs/design/cognitive-state.md`;
- `docs/design/decisions/README.md`;
- `docs/design/README.md`;
- `docs/design/current.md`;
- `docs/design/glossary.md`;
- `AGENTS.md` в части state mutation discipline.

Exact machine-facing contract пока не создаётся: `DU-05` должен сначала определить module lifecycle/scheduler/commit interaction.
