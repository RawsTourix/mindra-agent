# Memory Core MINDRA

## Статус документа

**Design Update:** `DU-11 — Memory Core`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет нейтральную базовую Memory subsystem MINDRA до появления Salience, Affect-driven retention и Consolidation.

После `DU-20` и consistency freeze `F31` терминология этого документа читается однозначно:

```text
Memory Core
→ structural eligibility / schema / authority / provenance validation
→ canonical Memory Store / record identity / retrieval / commit

Memory Regulation
→ policy admission / retention / forgetting / eviction
→ replay / consolidation selection и regulation state
```

Следовательно, `Memory Core` **не является вторым владельцем policy admission**. Если Memory Regulation отключена в раннем/control profile, используется явно объявленная baseline control policy, а не скрытая admission-логика внутри Core.

Документ определяет:

- ownership памяти;
- различие `Memory Store`, `Memory Record`, derived representation и retrieval index;
- write/structural-eligibility boundary;
- retrieval request/result semantics;
- representation drift/versioning;
- hard-capacity/degradation semantics Core;
- temporal scope/persistence;
- snapshot/restore/counterfactual requirements;
- связь Memory с Cortex без ambient context injection;
- различие Memory, trajectory/replay и Cortex context;
- `NoMemory`/Dummy/Control configurations;
- observability/intervention/failure semantics.

Документ опирается на:

- [`../system-context.md`](../system-context.md) — активная Memory является agent-owned state и не равна Artifact Storage;
- [`../cognitive-state.md`](../cognitive-state.md) — `CognitiveState` не является всем Agent-owned state;
- [`../module-lifecycle.md`](../module-lifecycle.md) — causally relevant updates публикуются через явные commit boundaries;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — наблюдение и intervention разделены;
- [`perception.md`](perception.md) — canonical percept и learned Feature Views имеют provenance/version semantics;
- [`goals.md`](goals.md) — Goal state существует отдельно от Memory;
- [`cortex.md`](cortex.md) — Cortex не получает ambient access к Memory и использует только явно подготовленный context;
- [`memory-regulation.md`](memory-regulation.md) — policy admission/retention/forgetting/eviction и consolidation принадлежат отдельной responsibility после `DU-20`;
- [`../contract-adr-consistency-freeze.md`](../contract-adr-consistency-freeze.md) — нормативное чтение `CR-02`/`CR-03`/`CR-04` для baseline `F31`.

Документ намеренно **не** определяет:

- Salience-based policy admission/retention/forgetting — `DU-19/20`;
- emotional memory semantics — `DU-16/17/20`;
- semantic consolidation/knowledge extraction algorithm — `DU-20`;
- training replay/data pipeline — `DU-25/26`;
- конкретный vector database/SQL database;
- FAISS/HNSW/SQLite как обязательную технологию;
- конкретный embedding encoder;
- конкретный retrieval ranker;
- exact Python API;
- exact serialization/checkpoint format — `DU-27`.

---

# 1. Цель DU-11

MINDRA нужна память, доступная будущему поведению после исчезновения информации из текущего `Canonical Percept` и краткоживущего `CognitiveState`.

При этом Memory не должна преждевременно становиться:

- «эмоциональной памятью»;
- vector database как единственным источником истины;
- копией всего trajectory log;
- неограниченным Cortex context window;
- hidden retrieval mechanism внутри Cortex Gateway;
- training replay buffer;
- learned neural memory, без которой невозможно заменить implementation.

Канонические отношения:

```text
Memory Record
≠
CognitiveState field
≠
trajectory/replay sample
≠
Cortex context fragment
≠
embedding/index entry
```

---

# 2. Главное архитектурное решение

MINDRA принимает **versioned canonical Memory Store с устойчивыми semantic records и производными перестраиваемыми retrieval representations/indexes**.

После F31 write path conceptually выглядит так:

```text
MemoryWriteProposal
       ↓
Memory Core
→ structural eligibility / schema / authority /
  provenance / visibility validation
       ↓
eligible proposal
       ↓
Memory Regulation или explicit baseline control policy
→ policy admission decision
       ↓
Memory Core
→ canonical commit / Memory revision
       ↓
┌────────────────────────────┐
│ Canonical Memory Store     │
│ MemoryRecord               │
│ stable id + source payload │
│ provenance + relations     │
└─────────────┬──────────────┘
              │ derive
              ▼
┌────────────────────────────┐
│ Memory Representations     │
│ embeddings / features      │
│ versioned feature spaces   │
└─────────────┬──────────────┘
              │ index
              ▼
┌────────────────────────────┐
│ Retrieval Indexes          │
│ structured/vector/hybrid   │
└─────────────┬──────────────┘
              │
      RetrievalRequest
              ↓
       RetrievalResult
              ↓
       cognitive consumer
```

Ключевые invariants:

> Потеря/перестройка derived index не должна уничтожать каноническое содержание воспоминания.

> Structural eligibility в Memory Core не является policy admission.

Решение дополнительно фиксируется в `ADR-0011`, а разделение Core/Regulation — в `ADR-0020` и `CR-02` baseline `F31`.

---

# 3. Memory Core как ответственность

## 3.1. Логическая принадлежность

Memory является частью MINDRA Agent и содержит agent-owned state.

Физически её данные могут храниться:

- в RAM;
- на диске;
- в embedded database;
- во внешнем storage service;
- в нескольких storage tiers.

Физическое размещение не меняет logical ownership.

## 3.2. Memory Core отвечает за

- canonical identity memory records;
- structural validation/eligibility write proposals;
- canonical commit после допустимого regulation/control decision;
- versioned logical store state;
- provenance/source references;
- record lifecycle metadata в пределах Core ownership;
- explicit retrieval capability;
- derived retrieval representations;
- indexes и их compatibility metadata;
- snapshot/restore logical Memory state;
- observability/research probes;
- Memory-specific intervention boundary.

## 3.3. Memory Core не отвечает за

- policy admission по значимости/бюджету;
- retention/forgetting/eviction policy;
- решение, насколько событие эмоционально важно;
- dynamic utility;
- goal arbitration;
- action selection;
- salience-based forgetting;
- автоматическое summarization всего опыта;
- training replay sampling;
- скрытое формирование Cortex prompt;
- evaluator-only truth storage normal runtime способом.

Policy admission/retention/forgetting/eviction принадлежат [`memory-regulation.md`](memory-regulation.md).

---

# 4. Memory Store отдельно от CognitiveState

Полный `Memory Store` не должен копироваться в каждую revision `CognitiveState`.

Conceptually:

```text
Agent-owned state
├── CognitiveState
│   ├── current percept
│   ├── goals
│   ├── lightweight memory status/references?
│   └── retrieval results, если соответствующий owner публикует их
│
└── Memory Store
    ├── records
    ├── relations
    ├── representations
    └── retrieval indexes
```

`CognitiveState` может содержать:

- `memory_revision`/capability status;
- ссылки на retrieval results;
- ограниченные runtime outputs Memory;

но не обязан материализовать весь store.

Для полного `Agent Snapshot` Memory Store является causally relevant частью Agent state.

---

# 5. Memory Revision

Memory Core имеет собственную логическую revision.

Она отличается от:

```text
state_revision
agent_revision
feature_space_revision
index_revision
```

Conceptually:

```text
memory_revision M17
→ committed write / Core-owned lifecycle transition
→ memory_revision M18
```

Read-only retrieval не обязано создавать новую Memory revision.

Любой retrieval result должен быть связан как минимум с base `memory_revision`, чтобы было понятно, против какого логического содержания выполнялся запрос.

---

# 6. Memory Record

`MemoryRecord` — устойчивый агент-доступный логический объект памяти.

Conceptually record должен уметь содержать:

```text
MemoryRecord
├── memory_id
├── content_kind
├── semantic_payload / source-preserving content
├── source references
├── provenance
├── causal creation identity
├── source agent_revision
├── scope/persistence metadata
├── content schema revision
├── relations
├── lifecycle/status metadata
└── intervention provenance?
```

Exact field names/types не frozen.

## 6.1. Stable identity

`memory_id` является логической identity record.

Нельзя использовать как semantic identity:

- позицию строки в database;
- FAISS ordinal;
- Python object id;
- memory address;
- vector-index slot.

Index может быть полностью перестроен, сохранив те же `memory_id`.

## 6.2. Source fidelity

Memory должна сохранять достаточно source/provenance information, чтобы отличить:

```text
observed experience
agent-derived inference
Cortex-produced interpretation
explicit external feedback
derived summary
research intervention
```

Cortex-generated утверждение не превращается после записи в `observed fact`.

## 6.3. Agent-visible information discipline

Normal Memory write не должна захватывать:

- Environment Research Ground Truth;
- evaluator-only Objective Task Metric;
- hidden experiment split;
- oracle path;

если эти данные не были agent-visible или явно введены как research intervention.

---

# 7. Episodic, semantic и procedural distinctions

`DU-11` не создаёт три обязательных отдельных memory modules.

Memory Store должен допускать typed records.

Минимально архитектура должна быть совместима с:

```text
episodic/event-linked record
explicit declarative/fact-like record
derived/summarized record
```

Но:

- основной reference-use DU-11 — episodic/event-linked memory;
- automatic semantic consolidation проектируется в Memory Regulation;
- procedural skill в trainable weights Policy/Cortex не считается `MemoryRecord` автоматически.

То есть:

```text
Memory Core supports record kinds
≠
Memory Core owns semantic consolidation policy
```

---

# 8. Record immutability и corrections

После committed write canonical source payload и identity record не должны молча переписываться задним числом.

Если новое знание уточняет/опровергает старое, предпочтительна модель:

```text
old MemoryRecord
    ↑
new MemoryRecord
relations:
- supersedes
- contradicts
- derived_from
- corroborates
```

Точный набор relation kinds не frozen.

Memory-owned lifecycle metadata может изменяться через новые Memory revisions, но history должна оставаться восстановимой.

Это важно для:

- causal replay;
- intervention;
- оценки memory errors;
- предотвращения скрытой post-hoc правки прошлого.

---

# 9. Memory Write Proposal

Любой producer, имеющий соответствующую capability, создаёт **proposal**, а не напрямую пишет record.

После F31 канонический путь:

```text
producer
  ↓
MemoryWriteProposal
  ↓
Memory Core
  ↓
structural validate / eligible / structurally reject
  ↓
eligible proposal
  ↓
Memory Regulation или declared baseline control policy
  ↓
admit / reject по policy
  ↓
Memory Core canonical commit
```

Potential sources могут включать:

- deterministic experience capture;
- Perception/event capture;
- Goal/history mechanism;
- World/Self/Appraisal mechanisms;
- Cortex-derived interpretation через semantic owner;
- Consolidation-derived proposal;
- research intervention.

Proposal capability не даёт direct write authority Store.

## 9.1. Structural eligibility Core

Memory Core проверяет только то, что относится к его ownership, например conceptually:

- schema compatibility;
- producer/write authority;
- required provenance/source metadata;
- visibility/trust restrictions;
- record-kind structural validity;
- compatibility с canonical store revision.

Эта проверка отвечает на вопрос:

> «может ли такой proposal вообще быть корректным кандидатом на Memory commit?»

Она **не** отвечает на вопрос:

> «стоит ли сохранять этот допустимый proposal с учётом значимости, бюджета и retention policy?»

Второй вопрос принадлежит Memory Regulation.

## 9.2. Baseline/control policy до substantial Memory Regulation

Ранний software milestone может использовать explicit baseline policy, например:

- accept all structurally eligible proposals, пока hard capacity не исчерпана;
- deterministic configured sampling/control;
- explicit reject-new при hard limit.

Такой profile является control/no-regulation behavior и не делает Memory Core владельцем policy admission.

---

# 10. Capacity и baseline behavior

Memory не может предполагаться физически бесконечной.

Memory Core обязан уметь обнаружить и явно представить storage/capacity constraint, но policy того, **какие** records сохранять, вытеснять или забывать, принадлежит Memory Regulation.

При отсутствии substantial regulation допустим explicit control profile:

```text
accept_eligible_until_limit
reject_new_after_limit
```

или другой заранее объявленный deterministic baseline.

Предпочтительный исследовательский default до полноценной regulation policy:

> не удалять canonical records молча; при достижении hard limit выдавать observable `capacity_exhausted`, если experiment не выбрал explicit baseline control policy.

FIFO/oldest-first допускается только как явно названный control policy, а не как внутреннее поведение Memory Core и не как «биологическое забывание».

---

# 11. Memory Representation

Embedding/latent/vector — **не сам MemoryRecord**.

Один record может иметь ноль, одну или несколько производных representations:

```text
MemoryRepresentation
├── representation_id
├── memory_id
├── representation_kind
├── feature_space_id
├── feature_space_revision
├── encoder identity/revision
├── source content revision
├── data
├── creation provenance
└── compatibility/status
```

Эти representations могут быть:

- удалены;
- перестроены;
- перекодированы;
- заменены;

без изменения identity канонического record.

---

# 12. Representation drift

Если encoder изменился:

```text
Record M42
├── embedding E7 / feature_space F3
└── embedding E8 / feature_space F4
```

Старый и новый vector нельзя молча считать сравнимыми.

Допустимые стратегии:

- freeze retrieval encoder;
- re-encode canonical records;
- maintain separate indexes per feature-space revision;
- compatibility adapter;
- explicit mixed-version retrieval algorithm.

Memory Core не выбирает одну стратегию как universal, но требует:

> несовместимые representations не смешиваются без explicit compatibility semantics.

Preservation canonical payload делает re-encoding возможным, когда источник доступен.

---

# 13. Retrieval Index

Index является производной поисковой структурой.

Conceptually:

```text
RetrievalIndex
├── index_id
├── index_revision
├── strategy/backend identity
├── indexed memory IDs
├── representation space identity
├── distance/scoring semantics
├── build/config revision
└── reproducibility metadata
```

Допустимы разные семейства:

```text
structured exact lookup
lexical/text lookup
vector exact search
approximate nearest-neighbor search
hybrid retrieval
```

Но concrete backend не является частью canonical Memory semantics.

## 13.1. Index не владеет record identity

Если HNSW/FAISS/SQL index перестроен, это не создаёт новые memories.

## 13.2. Index loss

Потеря rebuildable index является infrastructure/degradation event, а не автоматической потерей canonical Memory Store.

---

# 14. Retrieval Request

Consumer не получает automatic «релевантные воспоминания» без causal operation.

```text
cognitive consumer
       ↓
RetrievalRequest
       ↓
Memory retrieval capability
       ↓
RetrievalResult
       ↓
consumer
```

Query conceptually может содержать:

```text
semantic/structured criteria
feature query + feature_space identity
temporal constraints
source/provenance filters
record-kind filters
goal/entity references
requested k/range
retrieval strategy requirements
causal identities
```

Memory не должна читать весь `CognitiveState` и сама решать, чем интересуется consumer.

---

# 15. Retrieval Result

Result должен сохранять происхождение retrieval:

```text
RetrievalResult
├── request identity
├── base memory_revision
├── retrieval/index revision
├── strategy
├── matches[]
│   ├── memory_id
│   ├── score components
│   ├── representation identity?
│   └── reason/match metadata, если доступно
├── truncation/degradation status
└── provenance
```

Retrieval result не становится canonical Memory write автоматически.

Repeated retrieval одного record не создаёт новую memory identity без отдельного write proposal.

---

# 16. Relevance не равна Value/Salience

Retrieval score отвечает на вопрос вида:

> насколько record соответствует query согласно конкретному retrieval strategy?

Он не должен неявно означать:

```text
importance
emotional significance
utility
salience
truth probability
```

Эти значения относятся к другим mechanisms.

Например, cosine similarity 0.91 означает только определённую близость в конкретном feature space при конкретной metric semantics.

---

# 17. Memory и Cortex

Канонически запрещено:

```text
Cortex Gateway
→ search Memory automatically
→ inject hidden memories
```

Правильный путь:

```text
consumer
  ↓ explicit RetrievalRequest
Memory
  ↓ RetrievalResult
consumer
  ↓ selects/structures context
CortexRequest
  ↓
Cortex Gateway
```

Таким образом retrieval является отдельным traceable causal event.

Cortex context window не является Memory Core.

KV-cache Cortex также не является Memory Record store.

---

# 18. Memory и trajectory/replay

Нужно строго различать:

```text
Agent Memory Retrieval
≠
Agent Memory Replay / Reactivation
≠
Experience/Trajectory Evidence
≠
Training Replay
```

## Retrieval

Query-driven normal cognition operation над Memory Core.

## Agent Memory Replay / Reactivation

Agent-owned повторная активация существующего `MemoryRecord` в memory/consolidation dynamics. Эта responsibility определяется Memory Regulation.

## Experience / Trajectory Evidence

- внешний research/training record;
- может хранить privileged metadata;
- не является normal Agent input.

## Training Replay

- внешний data/training operation;
- повторно использует source/derived training data;
- не является воспоминанием Agent.

Общее правило:

```text
replay ≠ new natural Environment experience
```

Они могут ссылаться на одинаковые causal event IDs, но не должны быть одной скрытой storage boundary.

---

# 19. Memory и Agent revisions

Record, созданный при `agent_revision=A7`, может пережить обновление Agent до `A8`.

Поэтому различаются:

```text
memory identity
source agent_revision
current agent_revision
representation encoder revision
```

После изменения Cortex/Perception encoder старый semantic payload остаётся историческим фактом, а derived representation может требовать migration/re-indexing.

Нельзя молча переписать старое содержание новой моделью и выдавать его за исходную память.

---

# 20. Scope и persistence

Memory Core должен допускать минимум:

```text
episode-scoped records
session-scoped records
agent-persistent records
```

Но source event scope и retention scope — разные вещи.

Событие произошло в Episode, но память о нём может сохраняться между Episodes.

`Environment.reset()` не очищает Memory целиком.

Explicit Memory reset должен иметь собственную operation/provenance semantics.

---

# 21. Snapshot / Restore / Fork

Для exact Agent counterfactual Memory является обязательной частью snapshot.

Logical Memory Core snapshot должен сохранять достаточную информацию для восстановления:

```text
memory_revision
canonical records
relations/Core-owned lifecycle metadata
scope state
structural/capacity state
representation manifests
index manifests
causally relevant RNG state, если есть stochastic retrieval/control
backend/config revisions, влияющие на retrieval
```

Memory Regulation snapshot отдельно сохраняет собственное causally relevant policy/budget/replay/consolidation state согласно её contract.

Derived index может:

- snapshot-иться физически;
- либо deterministic/reproducible rebuild-иться из canonical records/representations.

Если rebuilding/ANN backend способен изменить retrieval outcome, causally relevant index/config/version должна быть сохранена или experiment нельзя называть exact replay.

---

# 22. Observability

Memory evidence должна позволять наблюдать минимум:

```text
write proposal
structural eligibility / structural rejection
regulation/control decision reference, если применимо
record commit
record lifecycle transition
representation build/rebuild
index build/revision
retrieval request
retrieval result
capacity/degradation event
snapshot/restore/fork
```

Для retrieval особенно важны:

- base memory revision;
- query provenance;
- returned memory IDs;
- scoring strategy;
- index/feature-space revision;
- truncation/filtering.

Core evidence не должна приписывать себе policy decision, произведённое Memory Regulation.

---

# 23. Interventions

Research intervention может включать:

```text
inject MemoryWriteProposal
force/add synthetic MemoryRecord
remove/tombstone selected record через explicit intervention boundary
replace record availability
alter RetrievalResult
swap retrieval strategy
shuffle returned records
change capacity/control condition
```

Intervention не должна маскироваться под natural memory operation.

При вмешательстве в record semantic owner остаётся Memory Core, а origin текущего состояния содержит intervention provenance по `DU-06`.

Policy-level вмешательства в admission/retention/forgetting принадлежат Memory Regulation intervention boundary.

---

# 24. NoMemory / Dummy / Control

Различаются:

## `NoMemory`

Memory capability отсутствует.

Consumer с required Memory dependency получает composition/capability error; optional consumer видит `unavailable`.

## `DummyMemory`

Детерминированная engineering implementation для тестов contract/scheduler.

## `ControlMemory`

Research implementation, например:

```text
random retrieval
shuffled retrieval
recency-only retrieval
parameter/cost-matched retrieval control
```

Control implementation не должна использовать hidden benchmark oracle, если experiment явно не объявлен oracle upper bound.

Policy admission controls оформляются отдельно на Memory Regulation/control boundary.

---

# 25. Failure / Degradation

Нужно различать как минимум классы:

```text
store unavailable
structural write rejection
policy rejection        # Regulation/control decision
capacity exhausted
record/schema incompatibility
representation unavailable
feature-space incompatibility
index stale/unavailable
retrieval timeout
partial/truncated result
snapshot mismatch
restore failure
```

Запрещён hidden fallback:

```text
Memory failed
→ silently ask Cortex to invent context
```

Если fallback существует в конкретной версии, он должен быть explicit, observable и частью experiment configuration.

---

# 26. Минимальные evaluation implications

Точная MINDRA-Eval определена отдельно, но Memory Core обязан позволять измерять:

- retrieval accuracy/recall на задачах с известным target;
- causal utility памяти: correct vs shuffled vs NoMemory;
- source/provenance fidelity;
- robustness к representation revision;
- snapshot/restore equivalence;
- capacity/degradation behavior;
- separation Memory contribution от Cortex capability.

Главный causal pattern:

```text
same Agent/Environment base
├── correct Memory
├── shuffled Memory
└── NoMemory
```

Если `correct` и `shuffled` дают одинаковый эффект, само наличие дополнительного context может объяснять выигрыш лучше, чем содержательная память.

Policy admission/retention quality оценивается отдельно как вклад Memory Regulation.

---

# 27. Что Memory Core намеренно не владеет

К отдельным или version-specific механизмам относятся:

- importance-weighted policy admission;
- emotional retention;
- decay/forgetting policy;
- memory consolidation;
- semantic knowledge extraction;
- dream/reactivation consolidation;
- learned regulation policy;
- proactive reminder policy;
- World Model imagination storage policy;
- training replay sampling;
- exact embedding model;
- exact vector index;
- exact database/storage backend.

Часть этих responsibilities определена `DU-20/25/26`; concrete algorithms остаются version-specific.

---

# 28. Инварианты DU-11 / F31

1. Memory Store является agent-owned state, но не всем `CognitiveState`.
2. `MemoryRecord` имеет stable semantic identity независимо от физического index slot.
3. Canonical source content отделено от derived embeddings/indexes.
4. Derived representation обязана иметь feature-space/encoder revision provenance.
5. Несовместимые representation revisions не смешиваются молча.
6. Retrieval выполняется только через explicit request/result boundary.
7. Memory не имеет ambient access ко всему Agent state.
8. Cortex не имеет ambient access к Memory.
9. Retrieval relevance не равна utility/salience/importance.
10. Memory write producer не получает direct store mutation authority.
11. Memory Core владеет structural eligibility и canonical commit, но не policy admission/retention/forgetting/eviction.
12. Memory Regulation является единственным owner соответствующей policy responsibility после `DU-20`.
13. `Environment.reset()` не означает reset Memory.
14. Retrieval, Agent Memory Replay и Training Replay различаются.
15. Exact Agent snapshot обязан учитывать causally relevant Memory Core и Memory Regulation state согласно scope.
16. Research intervention всегда сохраняет provenance.
17. `NoMemory`, Dummy и Control configurations различаются.

---

# 29. Completion gate DU-11

`DU-11` считается завершённым, когда:

- canonical Memory ownership определён;
- Memory Record/Store/Representation/Index различаются;
- write/structural-eligibility boundary определена;
- neutral baseline/control behavior не создаёт второго policy owner внутри Core;
- retrieval request/result boundary определена;
- representation drift semantics определена;
- Cortex integration не создаёт ambient context;
- Retrieval/Agent Memory Replay/Training Replay разделены;
- snapshot/restore requirements определены;
- ablation/control semantics определены;
- semantic contract согласован с `DU-20` и F31;
- значимый выбор оформлен ADR.
