# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01` … `DU-10` завершены и приняты. Реализация ещё не начата.**

На текущем этапе зафиксированы:

- концепция проекта и исследовательская методология;
- системные/dependency/runtime/state/scheduler boundaries;
- observability/intervention discipline;
- Environment/MicroWorld contract;
- Perception/Canonical Percept;
- Goal System/Goal Graph;
- Cortex semantic capability boundary;
- candidate contracts Environment, Perception, Goals и Cortex;
- десять accepted ADR.

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
```

## DU-01 … DU-06

Канонические документы:

- [`system-context.md`](system-context.md);
- [`dependency-rules.md`](dependency-rules.md);
- [`execution-model.md`](execution-model.md);
- [`cognitive-state.md`](cognitive-state.md);
- [`module-lifecycle.md`](module-lifecycle.md);
- [`observability-and-intervention.md`](observability-and-intervention.md).

Accepted decisions:

- `ADR-0001` … `ADR-0006`.

## DU-07

Канонический документ:

- [`modules/environment.md`](modules/environment.md).

Candidate contract:

- [`contracts/environment.md`](contracts/environment.md).

Accepted decision:

- [`ADR-0007`](decisions/ADR-0007-two-plane-environment-boundary.md).

## DU-08

Канонический документ:

- [`modules/perception.md`](modules/perception.md).

Candidate contract:

- [`contracts/perception.md`](contracts/perception.md).

Accepted decision:

- [`ADR-0008`](decisions/ADR-0008-hybrid-canonical-percept.md).

## DU-09

Канонический документ:

- [`modules/goals.md`](modules/goals.md).

Candidate contract:

- [`contracts/goals.md`](contracts/goals.md).

Accepted decision:

- [`ADR-0009`](decisions/ADR-0009-committed-goal-graph.md).

## DU-10

Канонический документ:

- [`modules/cortex.md`](modules/cortex.md).

Candidate contract:

- [`contracts/cortex.md`](contracts/cortex.md).

Research pass:

- [`../research/literature/DU-10-cortex-landscape-2026-08.md`](../research/literature/DU-10-cortex-landscape-2026-08.md).

Главные результаты:

- Cortex является заменяемой agent-owned pretrained capability, а не всей MINDRA;
- принят backend-neutral `Cortex Gateway`;
- semantic `Cortex Request/Context/Result` отделены от model-specific prompt/messages/tokens;
- tokenizer/processor/chat template/provider mapping принадлежат backend adapter;
- local и remote providers допустимы за одной logical boundary;
- Cortex не получает ambient access ко всему `CognitiveState`/Memory/private state;
- Cortex может быть shared injected capability, а не обязательный отдельный scheduler module;
- Cortex invocation является traceable sub-operation cognitive consumer;
- canonical effects публикует semantic owner, а не Cortex backend;
- core semantic inference отделена от optional capabilities;
- hidden states, attentions, logits, embeddings, multimodal/latent input, gradients и adapter management являются optional;
- chain-of-thought не является required Cortex output;
- Cortex Result не становится Goal/Memory/Action/observed fact автоматически;
- Goal grounding через Cortex заканчивается `Goal Proposal` boundary;
- Cortex representation становится Perception Feature View только через explicit versioned adapter;
- `NoCortex`, `DummyCortex` и research `ControlCortex` различаются;
- hidden fallback/model substitution запрещены;
- context overflow/truncation/degradation должны быть observable;
- base model/adaptation/template/provider identity входят в provenance настолько, насколько влияют на поведение;
- language capability должна быть explicit и проверяемой;
- при language-based experiments baseline проверяется минимум для русского и английского согласно будущему evaluation/version design.

Accepted decision:

- [`ADR-0010`](decisions/ADR-0010-capability-negotiated-cortex-gateway.md).

---

# 3. Следующий допустимый Design Update

```text
DU-11 — Memory Core
```

Цель `DU-11` — спроектировать **нейтральную базовую Memory subsystem** до появления Salience/Consolidation: что считается memory item, как хранится provenance/identity, как происходит retrieval и как Memory отделяется от текущего `CognitiveState`, Cortex context и будущего replay/training pipeline.

Обязательные области:

```text
Memory ownership
memory item / record identity
content vs representation
observed / derived / Cortex-produced provenance
write / store boundary
retrieval request / result
query semantics
structured vs vector indexing
representation revisions
capacity
forgetting/eviction baseline semantics
session vs persistent Memory
snapshot/restore
Memory consistency across Agent revisions
Cortex context integration
NoMemory / Dummy / Control Memory
observability / intervention
failure / degradation
```

Нужно определить:

- является ли Memory одним модулем или storage+retrieval capability с отдельным owner;
- что именно можно записывать в Memory и кто имеет право предложить запись;
- чем Memory record отличается от trajectory/replay item;
- хранится ли original semantic source отдельно от embedding/index representation;
- как пережить representation drift после Perception/Cortex adaptation;
- как retrieval не превращается в скрытый ambient context Cortex;
- как Memory не получает Salience/"эмоциональное забывание" раньше `DU-19/20`;
- как сделать честные `NoMemory`, shuffled/random retrieval controls;
- как snapshot/restore Memory участвует в exact counterfactual Agent clone.

После принятия `DU-11` допускается:

```text
DU-12 — World Model
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
NoCortex ≠ DummyCortex ≠ ControlCortex
```

---

# 5. Что ещё не принято

Пока отсутствуют accepted решения по:

- Memory Core;
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

Также пока не выбраны exact Python/package/framework решения и concrete Cortex backend.

---

# 6. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие detailed design не является разрешением Codex начинать implementation до появления version roadmap и implementation sequence.
