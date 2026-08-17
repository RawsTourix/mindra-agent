# ADR-0011 — Canonical Memory Records отдельно от derived representations/indexes

## Статус

`accepted`

## Контекст

После `DU-08` MINDRA уже различает structured semantic representation и learned Feature Views с revision semantics. После `DU-10` Cortex также является сменной capability и не может владеть всей историей Agent через собственный context window.

Перед World Model/Self Model необходимо определить устойчивую Memory boundary, которая:

- сохраняет agent experience между Cognitive Cycles/Episodes;
- не зависит от одной embedding model;
- допускает structured и vector retrieval;
- переживает representation drift;
- остаётся доступной при замене Cortex;
- пригодна для causal ablation/counterfactual experiments.

---

## Проблема

Нужно выбрать, что является **канонической памятью** MINDRA.

Если принять vector index, prompt history или neural hidden state как единственный source of truth, будущая смена encoder/backend может изменить или уничтожить смысл сохранённого опыта.

---

## Требования

Решение должно:

- иметь stable semantic record identity;
- сохранять source/provenance;
- не смешивать memory content и retrieval representation;
- поддерживать разные retrieval implementations;
- явно обрабатывать representation revision/drift;
- не давать Cortex ambient access к памяти;
- не смешивать Memory с training replay;
- позволять snapshot/restore;
- поддерживать NoMemory/control configurations.

---

## Рассмотренные варианты

### Вариант A — Cortex context/history является Memory

```text
past observations/messages
→ append to Cortex context
```

Плюсы:

- минимальная архитектура;
- естественно для chat-oriented LLM;
- нет отдельного retrieval backend.

Минусы:

- context конечен;
- Memory становится Cortex-dependent;
- NoCortex невозможен;
- difficult causal retrieval evidence;
- provider/template truncation меняет память;
- невозможно нормально разделить remembered content и currently supplied context.

**Отклонено.**

---

### Вариант B — Vector database/index является canonical Memory

```text
experience
→ embedding
→ vector store
```

Плюсы:

- простая retrieval architecture;
- зрелые ANN libraries;
- компактный query interface.

Минусы:

- embedding model становится частью identity памяти;
- representation drift ломает compatibility;
- original semantic/source content может потеряться;
- structured exact queries становятся вторичными;
- index-specific IDs могут случайно стать memory identity;
- difficult migration между models/metrics.

**Отклонено как canonical source of truth.** Vector indexes остаются допустимыми derived retrieval structures.

---

### Вариант C — Полностью differentiable/neural memory как canonical Memory

Memory существует преимущественно как learned recurrent/neural parameters/state.

Плюсы:

- потенциально высокая интеграция с neural computation;
- differentiable retrieval/update;
- возможна компактная learned compression.

Минусы:

- трудно инспектировать source fidelity;
- сложно получить stable memory identities;
- difficult causal deletion/shuffle controls;
- training/retrieval/storage смешиваются;
- backend/architecture становится обязательной частью Memory semantics;
- сложно хранить точную историческую provenance.

**Отклонено как базовый DU-11 contract.** Neural memory может появиться как future implementation/additional representation после отдельного design.

---

### Вариант D — Canonical semantic records + derived representations/indexes

```text
canonical MemoryRecord store
        ↓
optional derived representations
        ↓
structured/vector/hybrid indexes
        ↓
explicit retrieval request/result
```

Плюсы:

- stable record identity;
- source/provenance сохраняются;
- embedding/index можно перестраивать;
- representation drift управляем;
- structured и vector retrieval равноправны;
- Cortex backend остаётся сменным;
- сильные ablation/intervention возможности;
- Memory можно snapshot/restore независимо от inference engine.

Минусы:

- требуется хранить больше metadata;
- migration/re-indexing становится отдельной responsibility;
- semantic store + derived indexes сложнее одного vector DB;
- необходимо строго следить за revision compatibility.

**Принято.**

---

## Принятое решение

MINDRA Memory Core использует:

1. **Canonical Memory Store** как logical agent-owned source of truth;
2. stable `MemoryRecord` identity и source/provenance;
3. optional `MemoryRepresentation` как derived data;
4. versioned `RetrievalIndex` как derived search structure;
5. explicit `RetrievalRequest → RetrievalResult` boundary.

Канонически:

```text
MemoryRecord
≠
embedding
≠
index entry
≠
Cortex context
≠
trajectory/replay sample
```

---

## Representation drift

При изменении encoder/feature space canonical MemoryRecord не переписывается.

Допустимы:

- re-encoding;
- parallel representation revisions;
- compatibility adapters;
- separate indexes.

Несовместимые spaces не смешиваются молча.

---

## Memory access

Cognitive consumer должен сформировать explicit retrieval request.

Memory не читает ambient Agent state для самостоятельного выбора query.

Cortex Gateway не ищет Memory скрыто.

Retrieved record попадает в Cortex context только через явное действие consumer/context builder.

---

## Neutrality before Salience

`DU-11` не определяет importance-driven write/retention/forgetting.

При capacity pressure используется explicit baseline policy либо observable rejection. Salience/Consolidation проектируются позже.

---

## Последствия

Положительные:

- Cortex/encoder replacement не уничтожает semantic memory;
- Memory становится хорошо диагностируемой;
- удобно делать shuffled/random/NoMemory controls;
- source fidelity и temporal provenance доступны напрямую;
- exact/approximate snapshot semantics можно определить явно.

Отрицательные:

- больше schema/version metadata;
- необходимо обслуживать derived indexes;
- storage size выше, чем при vector-only design;
- будущему implementation придётся аккуратно разграничить logical store и physical backends.

---

## Что решение не определяет

ADR не выбирает:

- database;
- vector index;
- embedding encoder;
- ranking formula;
- memory capacity;
- semantic consolidation;
- forgetting mechanism;
- learned retrieval policy;
- exact Python API.

---

## Затронутые документы

Канонические:

- `docs/design/modules/memory.md`;
- `docs/design/current.md`;
- `docs/design/README.md`.

Candidate contract:

- `docs/design/contracts/memory.md`.

Research evidence:

- `docs/research/literature/DU-11-memory-landscape-2026-08.md`.
