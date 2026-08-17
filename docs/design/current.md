# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-11` завершены и приняты. Реализация ещё не начата.**

На текущем этапе зафиксированы:

- системные/dependency/runtime/state/scheduler boundaries;
- observability/intervention discipline;
- Environment/MicroWorld;
- Perception/Canonical Percept;
- Goal System/Goal Graph;
- Cortex semantic capability boundary;
- Memory Core;
- candidate contracts Environment, Perception, Goals, Cortex и Memory;
- одиннадцать accepted ADR.

---

# 2. Завершённые Design Updates

```text
DU-00 — Documentation Foundation
DU-01 — System Context
DU-02 — Dependency & Composition Rules
DU-03 — Runtime / Temporal Model
DU-04 — CognitiveState Semantics
DU-05 — Module Protocol & Scheduling
DU-06 — Observability & Intervention
DU-07 — Environment / MicroWorld Contract
DU-08 — Perception / Canonical Representation
DU-09 — Goal System
DU-10 — Cortex Boundary
DU-11 — Memory Core
```

## DU-11

Канонический документ:

- [`modules/memory.md`](modules/memory.md).

Candidate contract:

- [`contracts/memory.md`](contracts/memory.md).

Research pass:

- [`../research/literature/DU-11-memory-landscape-2026-08.md`](../research/literature/DU-11-memory-landscape-2026-08.md).

Accepted decision:

- [`ADR-0011`](decisions/ADR-0011-canonical-memory-records-derived-indexes.md).

Главные результаты:

- Memory Core является agent-owned stateful subsystem;
- `Memory Store` отделён от `CognitiveState` и Artifact Storage;
- stable `MemoryRecord` является canonical semantic memory item;
- record identity не зависит от database row/vector slot/index ordinal;
- source payload/provenance сохраняются отдельно от derived retrieval representations;
- `MemoryRepresentation` имеет feature-space/encoder revision;
- `RetrievalIndex` является derived/rebuildable search structure;
- vector database не является canonical source of truth памяти;
- representation drift требует explicit compatibility/re-encoding/separate-index semantics;
- write идёт через `MemoryWriteProposal`, а не direct mutation;
- DU-11 использует neutral admission/capacity semantics без Salience/Valuation;
- hidden importance-based eviction/forgetting пока запрещены;
- retrieval выполняется через explicit `RetrievalRequest → RetrievalResult`;
- Memory не читает весь `CognitiveState` для самостоятельного построения query;
- Cortex Gateway не делает hidden Memory lookup;
- retrieval relevance отделена от utility/salience/importance/truth;
- Memory отличается от trajectory/evidence и training replay;
- episodic/semantic record kinds допускаются, но automatic semantic consolidation отложена;
- procedural skill в weights не является `MemoryRecord` автоматически;
- canonical record history не переписывается задним числом; corrections/supersession имеют provenance;
- episode/session/agent-persistent retention scopes допустимы;
- `Environment.reset()` не означает reset Memory;
- exact Agent counterfactual требует causally relevant Memory snapshot/index/config state;
- `NoMemory`, `DummyMemory`, `ControlMemory` различаются;
- correct-vs-shuffled-vs-NoMemory является обязательным будущим causal evaluation pattern.

---

# 3. Следующий допустимый Design Update

```text
DU-12 — World Model
```

Цель `DU-12` — определить, как MINDRA представляет и обучает **предсказательную модель динамики внешнего мира**, не смешивая prediction с observation, Memory, Utility или Policy.

Обязательные области:

```text
World Model responsibility / ownership
current-state / belief input boundary
action-conditioned transition prediction
one-step vs multi-step rollout
observed vs imagined transition provenance
prediction target representation
partial observability
history / Memory use
stochastic dynamics
uncertainty semantics
prediction error
model revision / training state
rollout horizon
counterfactual action queries
Cortex optional assistance
NoWorldModel / Dummy / Control
observability / intervention
failure / degradation
```

Нужно определить:

- что World Model предсказывает: следующий percept, latent state, structured outcome или несколько представлений;
- как модель работает при partial observability;
- где заканчивается Memory и начинается world belief/model state;
- должен ли World Model иметь собственное recurrent/private belief state;
- как prediction не становится observed fact;
- как real/replayed/imagined transitions остаются различимыми;
- как отделить epistemic uncertainty от aleatoric там, где это действительно возможно;
- как prediction error позже может питать Intrinsic Signals, не становясь reward автоматически;
- как использовать action candidates для counterfactual prediction без Policy ownership;
- какие архитектуры RSSM/Dreamer/recurrent/Transformer являются кандидатами, но не canonical requirement;
- как сравнивать World Model against No/Control variants.

После принятия `DU-12` допускается:

```text
DU-13 — Self Model
```

---

# 4. Действующие фундаментальные отношения

```text
logical architecture boundary ≠ deployment topology
Cognitive Cycle ≠ Environment Transition
CognitiveState ≠ full Agent-owned state
Observability ≠ Intervention
Raw Observation ≠ Canonical Percept
External Task Specification ≠ Committed Goal
Goal Proposal ≠ Committed Goal
Goal ≠ Reward ≠ Drive ≠ Utility/Value ≠ Policy
MINDRA Agent ≠ Cortex ≠ concrete LLM
semantic Cortex context ≠ model-specific prompt/tokens
Cortex Result ≠ canonical truth/state effect
MemoryRecord ≠ embedding/index entry
Memory ≠ trajectory/replay
Memory retrieval ≠ ambient Cortex context
retrieval relevance ≠ salience/value/importance
```

---

# 5. Что ещё не принято

Пока отсутствуют accepted решения по:

- World Model;
- Self Model;
- intrinsic signals;
- Drives;
- Appraisal;
- Affect Dynamics;
- Valuation;
- Salience/Attention;
- Memory Regulation/Consolidation;
- Workspace;
- Metacognitive/Executive Control;
- Policy/Planner;
- Action boundary;
- trajectory/data/replay schema;
- training lifecycle;
- checkpointing/reproducibility;
- exact evaluation harness;
- testing strategy;
- research claims/limitations;
- version roadmap;
- implementation sequences.

Также пока не выбраны exact Python/package/framework решения, concrete Cortex backend, Memory database/index или embedding model.

---

# 6. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начинать implementation до появления version roadmap и implementation sequence.
