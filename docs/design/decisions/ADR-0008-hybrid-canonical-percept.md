# ADR-0008 — Гибридный Canonical Percept: structured semantic core + optional feature views

## Статус

`accepted`

## Контекст

После `DU-07` Environment предоставляет `Raw Observation`, но downstream modules MINDRA не должны зависеть от конкретной observation encoding среды.

Нужно определить stable internal representation, пригодное одновременно для:

- MicroWorld;
- будущих multimodal environments;
- Memory/World Model/Policy;
- causal diagnostics;
- learned encoders;
- Cortex/no-Cortex configurations;
- continual learning и representation updates.

---

## Проблема

Есть четыре реалистичных класса решений.

### Вариант A — один universal learned latent vector

```text
Raw Observation → Encoder → z
```

Плюсы:

- простая machine-facing форма;
- удобно для neural modules;
- маленькая dimensionality;
- легко batch'ить.

Минусы:

- latent semantics зависят от encoder revision;
- слабая observability/intervention specificity;
- missingness/provenance приходится кодировать неявно;
- entities/relations теряют явную структуру;
- downstream modules привязываются к feature space;
- continual update encoder создаёт drift;
- замена Cortex/encoder способна сломать весь inter-module contract.

**Отклонено как canonical inter-module representation.** Learned global latent остаётся допустимым `Feature View`.

---

### Вариант B — только полностью symbolic structured schema

```text
Raw Observation → deterministic symbolic structure
```

Плюсы:

- высокая интерпретируемость;
- простая provenance;
- удобно для causal tests;
- хорошо подходит MicroWorld.

Минусы:

- плохо переносится на image/audio/сложный raw input;
- требует hand-authored ontology для каждой modality;
- neural modules всё равно создадут собственные embeddings;
- существует риск превратить Perception в ручной world model;
- ограничивает будущие learned perceptual capabilities.

**Отклонено как единственный representation mechanism.** Structured semantics остаются canonical core.

---

### Вариант C — structured Semantic Core + optional revisioned Feature Views

```text
Raw Observation
      ↓
Canonical Percept
├── Semantic Core
└── Feature Views[]
```

Плюсы:

- semantic/provenance/missingness доступны явно;
- neural modules могут использовать compact learned features;
- object/entity structure не теряется;
- Cortex не определяет canonical representation;
- no-Cortex baseline естественен;
- learned views можно независимо менять/ablate;
- drift/compatibility можно отслеживать по feature-space revision;
- representation пригодна и для symbolic, и для raw modalities.

Минусы:

- contract сложнее одного vector;
- нужно versioning нескольких уровней;
- consumers должны явно выбирать semantic core/view dependencies;
- требуется discipline против дублирования одних и тех же данных в разных views.

**Принято.**

---

### Вариант D — использовать Cortex hidden space как canonical representation

Плюсы:

- богатая pretrained semantics;
- не нужен отдельный общий encoder;
- удобно для language-heavy tasks.

Минусы:

- Cortex становится обязательным;
- hidden size/tokenization/model family протекают во всю архитектуру;
- swap Cortex требует миграции всех consumers;
- no-Cortex/ablation становится неестественным;
- backend/raw representation может быть вообще недоступна для remote provider;
- трудно отличить MINDRA architecture gain от capability Cortex.

**Отклонено.** Cortex-derived representation может быть optional Feature View после `DU-10`.

---

## Принятое решение

MINDRA использует `Canonical Percept`, состоящий conceptually из:

```text
Canonical Percept
├── Percept Envelope
├── Semantic Core
├── Modality Status
└── Feature Views[]
```

### Semantic Core

- structured;
- current-observation scoped;
- хранит explicit entities/relations/facts;
- имеет provenance/missingness;
- не содержит скрытый world belief из Memory/World Model;
- не зависит от Cortex hidden space.

### Feature Views

- optional;
- могут быть learned;
- имеют `feature_space_id/revision` и encoder identity;
- не являются универсально взаимозаменяемыми;
- могут заменяться/отключаться через composition;
- допускают future Cortex-derived view.

### Entity semantics

- collection order не несёт смысла по умолчанию;
- identity по умолчанию observation-local;
- persistent tracking не является ground truth capability.

### Versioning

Различаются semantic schema, normalization, encoder и feature-space revisions.

---

## Последствия

### Положительные

- Environment и downstream cognitive modules развязаны;
- object/relational structure остаётся доступной;
- learned representation не запрещена;
- causal intervention можно делать на semantic и latent уровнях отдельно;
- Cortex остаётся replaceable;
- representation drift можно измерять и versioning не даёт молча смешивать несовместимые embeddings;
- baseline MicroWorld можно начать без тяжёлого learned perception.

### Отрицательные

- больше metadata/contract surface;
- потребуется явная compatibility policy Feature Views;
- некоторые neural consumers потребуют adapter/encoder до удобного tensor input;
- нельзя просто передавать один `state_vector` всем модулям.

---

## Research evidence

При выборе учитывались:

- Locatello et al., **Object-Centric Learning with Slot Attention**, arXiv:2006.15055;
- Lee et al., **Set Transformer**, arXiv:1810.00825;
- Battaglia et al., **Relational inductive biases, deep learning, and graph networks**, arXiv:1806.01261;
- Jaegle et al., **Perceiver IO**, arXiv:2107.14795;
- Hafner et al., **DreamerV3**, arXiv:2301.04104.

Эти работы показывают практичность object/set/relational и learned latent representations, но не требуют выбирать один из них как единственный canonical language MINDRA.

---

## Что решение намеренно не определяет

- exact Python types;
- exact entity schema;
- tensor dimensions;
- specific encoder;
- GNN/Slot Attention/Transformer/MLP;
- exact feature-space compatibility metric;
- multimodal fusion;
- Cortex adapter implementation;
- Memory migration при representation drift.

---

## Затронутые документы

- `docs/design/modules/perception.md`;
- `docs/design/contracts/perception.md`;
- `docs/design/README.md`;
- `docs/design/current.md`;
- `docs/design/contracts/README.md`;
- `docs/design/glossary.md`;
- `AGENTS.md`.