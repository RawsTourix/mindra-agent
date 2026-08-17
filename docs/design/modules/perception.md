# Perception и canonical representation MINDRA

## Статус документа

**Design Update:** `DU-08 — Perception / Canonical Representation`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет:

- границу между `Raw Observation` Environment и внутренним perceptual representation Agent;
- семантику `Canonical Percept`;
- разделение structured semantic core и optional learned feature views;
- entity/relation/modality semantics;
- missingness/partial-observation semantics;
- normalization и learned perception boundary;
- representation identity/versioning/drift;
- device/batch/backend independence;
- границу будущего Cortex adapter;
- observability/intervention requirements Perception.

Документ опирается на:

- [`environment.md`](environment.md) — `Raw Observation` является agent-visible проекцией Environment, но не внутренним representation;
- [`../cognitive-state.md`](../cognitive-state.md) — published state имеет owner/provenance/freshness/scopes и committed revision semantics;
- [`../module-lifecycle.md`](../module-lifecycle.md) — module execution следует declared dependencies/waves/atomic commit;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — passive evidence отделено от active intervention.

Документ намеренно **не** определяет:

- exact Python API;
- конкретный tensor/container framework;
- окончательные dtype/shape latent vectors;
- конкретную neural encoder architecture;
- точный MicroWorld wire-format;
- конкретный Cortex backend или embedding model;
- Goal semantics — это `DU-09`;
- Cortex contract — это `DU-10`;
- Memory indexing — это `DU-11`;
- World Model latent dynamics — это `DU-12`;
- training lifecycle/optimizer semantics — это `DU-26`.

---

# 1. Цель DU-08

Независимые модули MINDRA не должны зависеть:

- от конкретной encoding `Raw Observation` MicroWorld;
- от object enum конкретной Environment implementation;
- от hidden size конкретной LLM;
- от случайной формы tensor конкретного encoder;
- от исследовательских privileged полей Environment.

При этом representation должна быть:

- достаточно структурированной для диагностики и causal intervention;
- достаточно общей для будущих модальностей;
- пригодной для neural computation;
- совместимой с partial observability;
- versioned и reproducible;
- независимой от Cortex;
- не превращённой в hand-authored полный world model.

Поэтому MINDRA принимает **гибридную canonical representation**:

```text
Raw Observation
      ↓
Perception ingress
      ↓
Canonical Percept
├── Semantic Core
└── Optional Feature Views
      ├── learned latent view
      ├── modality-specific view
      └── future Cortex-derived view
```

`Semantic Core` является канонической интерпретируемой поверхностью текущего восприятия.

`Feature View` является optional вычислительным представлением конкретного feature space и не заменяет Semantic Core как единственный источник смысла.

Это решение дополнительно зафиксировано в `ADR-0008`.

---

# 2. Perception как ответственность

Perception отвечает за преобразование **текущего agent-visible sensory input** в внутреннее представление текущего наблюдения.

Perception может включать:

- validation входной observation schema;
- deterministic normalization;
- modality adaptation;
- extraction наблюдаемых entities/relations;
- learned perception для необработанных модальностей;
- optional feature encoding;
- uncertainty/quality metadata;
- representation provenance/version metadata.

Perception **не** отвечает за:

- восстановление скрытой карты из памяти;
- хранение прошлого опыта;
- долгосрочную object identity по умолчанию;
- предсказание будущего world state;
- определение utility;
- превращение task specification во внутреннюю Goal representation;
- выбор action;
- раскрытие Research Ground Truth.

Главный invariant:

```text
current percept
≠
belief about hidden world
≠
memory of past world
≠
prediction of future world
```

Поздние модули могут объединять эти источники, но Perception сама не должна маскировать inferred hidden state под непосредственно наблюдаемое.

---

# 3. Входы Perception

## 3.1. Raw Observation

Основной input — `Raw Observation` из Agent Interaction Plane Environment.

Она приходит вместе с достаточной causal/schema provenance, чтобы определить:

- source Environment/observation schema;
- `episode_id`/`environment_transition_id`/observation identity;
- availability модальностей;
- observation-contract version.

Research-only world state/manifest/oracle данные не являются входом Perception normal runtime.

## 3.2. Task и feedback не поглощаются Perception

Канонически:

```text
Raw Observation
→ Perception

External Task Specification
→ будущая Goal ingress boundary

External Task Feedback
→ отдельный external-signal ingress
```

Если текст является **самой наблюдаемой модальностью мира** (например, сообщение другого объекта), он может входить в Raw Observation.

Но текстовая формулировка задания не становится «сенсорным объектом» только потому, что представлена строкой.

Это необходимо, чтобы не смешивать:

```text
что Agent видит
≠
что Agent должен сделать
≠
как Agent оценивает результат
```

---

# 4. Canonical Percept

`Canonical Percept` — опубликованное представление **одного causal observation context**.

Conceptually он состоит из:

```text
Canonical Percept
├── Percept Envelope
├── Semantic Core
├── Modality Status
└── Feature Views[]
```

Точная machine-facing форма будет уточняться candidate contract.

`Canonical Percept` может быть опубликован в `CognitiveState` как owner-scoped state Perception, но exact namespace/path пока не frozen.

---

# 5. Percept Envelope

Envelope хранит control/provenance metadata, а не task semantics.

Он должен позволять определить минимум:

- percept identity;
- source observation identity;
- temporal causal context;
- source Environment/observation schema identity;
- `percept_schema_revision`;
- perception pipeline/implementation revision;
- `agent_revision`, под которой percept был вычислен, если learned Agent-owned encoder влияет на результат;
- intervention provenance, если representation была изменена экспериментально;
- availability/quality summary.

Envelope не является автоматически input всем cognitive modules. Consumers читают только declared semantic dependencies.

---

# 6. Semantic Core

## 6.1. Назначение

Semantic Core — типизированное, структурированное представление того, что Perception утверждает о **текущем observation**.

Оно должно быть достаточно общим, чтобы независимые модули не знали wire-format Environment, но не обязано быть универсальной онтологией мира.

Для MicroWorld canonical semantic core должен уметь выразить по меньшей мере:

```text
observed self/world-side state
observed entities
observed relations/spatial facts
observed events/consequences
modality/visibility state
```

Точные поля/enum определяются позднее.

## 6.2. Entity collection

Наблюдаемые entities conceptually представлены как collection/set.

По умолчанию:

```text
entity order
≠
semantic information
```

Если порядок важен, это должно быть отдельным явным полем/отношением.

Padding/sorting, используемые ради batching, не создают semantic order.

## 6.3. Entity identity

Perception не получает бесплатную persistent object identity.

По умолчанию `percept_entity_id`:

- идентифицирует элемент внутри конкретного percept;
- не обещает совпадение между Environment Transitions;
- не является hidden Environment object ID.

Если task contract действительно делает стабильный identifier наблюдаемым, его можно представить как наблюдаемый attribute.

Если Perception позднее реализует tracking, track identity должна быть явно маркирована как **inferred**, иметь собственную provenance/confidence и не считаться ground-truth identity.

Persistent belief/entity tracking может также относиться к World Model/Memory и не принимается этим DU как обязательная часть Perception.

## 6.4. Relations и spatial facts

Отношения должны быть explicit data, а не зависеть от позиции объекта в массиве.

Conceptually допустимы:

- relative position;
- adjacency;
- containment;
- visibility relation;
- interaction reachability, только если она непосредственно наблюдаема/выводима из разрешённой сенсорной информации;
- modality-specific relations.

Absolute/global coordinates не появляются автоматически, если Environment их не раскрывает.

---

# 7. Direct, normalized и inferred perceptual facts

Все semantic claims из текущего observation должны сохранять происхождение.

Conceptually различаются:

```text
direct
→ значение непосредственно присутствует в agent-visible observation

normalized/derived
→ deterministic преобразование разрешённых входных данных

perceptually inferred
→ learned/algorithmic inference из текущей модальности
```

Например, в символическом MicroWorld `color=blue` может быть direct/normalized.

В camera-based Environment `object_kind=door` может быть learned inference с confidence.

Важно:

```text
perceptual inference from current observation
≠
World Model prediction
```

и:

```text
perceptual inference
≠
retrieved memory
```

Эти source classes не должны смешиваться без provenance.

---

# 8. Partial observation и missingness

Partial observability является первым классом семантики.

## 8.1. Ненаблюдаемый объект не создаётся как hidden placeholder

Если Agent не видит объект и не имеет agent-visible свидетельства о его существовании, Perception **не создаёт**:

```text
entity_X = unknown
```

только потому, что Research Ground Truth знает об entity_X.

Сведения о невидимом мире могут появиться позже через Memory/World Model, но это уже другой source/provenance.

## 8.2. Наблюдаемый entity с неизвестным attribute

Если сам entity наблюдаем, но конкретное свойство сенсорно неразличимо, property может иметь semantic availability вроде:

```text
unknown
unavailable
occluded/low-quality
```

точная representation уточняется contract.

Нельзя использовать универсальные magic sentinels без schema semantics.

## 8.3. Modality status

Percept должен позволять отличать:

- modality присутствует и валидна;
- modality отсутствует по contract;
- modality временно unavailable;
- данные повреждены/invalid;
- modality намеренно masked в experiment;
- perceptual quality ограничена.

`zero tensor` сам по себе не является корректным обозначением отсутствующей modality.

---

# 9. Deterministic normalization

До learned encoding допускается стабильный deterministic adaptation layer.

Он может выполнять:

- schema validation;
- единицы измерения;
- canonical category mapping;
- координатные преобразования, если они не раскрывают скрытое состояние;
- числовое scaling/clipping согласно versioned policy;
- sorting только как implementation normalization без semantic order;
- representation явной missingness.

Normalization должна быть versioned и воспроизводимой.

Если normalization использует dataset statistics, они:

- вычисляются только из разрешённой training distribution;
- имеют собственную identity/version;
- не используют validation/test leakage;
- сохраняются в training/checkpoint provenance.

Конкретные статистические процедуры определяются позднее.

---

# 10. Learned Perception

MINDRA допускает trainable perceptual encoders, но они не обязательны для первого MicroWorld baseline.

Learned Perception нужна, когда Raw Observation сама не предоставляет достаточную structured semantics, например для:

- image;
- audio;
- сложного текста как sensory modality;
- другой raw high-dimensional modality.

Trainable encoder обязан иметь:

- implementation/model identity;
- encoder revision;
- declared source modalities;
- output schema/feature-space identity;
- training/eval mode;
- uncertainty/quality semantics там, где они заявляются;
- snapshot/checkpoint obligations, если его weights Agent-owned;
- observability и intervention boundary.

Learned encoder не получает Research Ground Truth во время normal inference только потому, что такой target использовался при supervised training.

---

# 11. Feature Views

## 11.1. Назначение

`Feature View` — optional вычислительное представление Semantic Core и/или разрешённой Raw Observation.

Примеры conceptually:

- entity embedding set;
- scene/global latent;
- spatial feature map;
- modality embedding;
- future Cortex-derived semantic embedding.

Canonical architecture не требует одного универсального view.

## 11.2. Feature View не является semantic source of truth

Один latent vector может быть удобен для Policy или World Model, но он:

- плохо диагностируется;
- зависит от encoder weights;
- может drift при continual training;
- часто привязан к dimensionality/backend;
- плохо выражает partial/missing semantics без дополнительного contract.

Поэтому:

```text
Feature View
≠
весь Canonical Percept
```

## 11.3. Feature-space identity

Каждый learned/encoded view должен иметь identity, достаточную для проверки совместимости.

Conceptually:

```text
view_kind
feature_space_id
feature_space_revision
encoder_identity
encoder_revision
source references
```

Равенство dimensionality **не** означает совместимость feature spaces.

---

# 12. Representation versioning и drift

Нужно различать минимум:

```text
percept_schema_revision
→ изменился смысл/структура canonical semantic representation

normalization_revision
→ изменилась deterministic adaptation policy

encoder_revision
→ изменились параметры/алгоритм learned encoder

feature_space_revision
→ изменилась семантика/геометрия конкретного Feature View
```

## 12.1. Drift

Если trainable encoder обновился, один и тот же исходный observation может получить другое latent representation.

Это нормальное явление, но оно должно быть наблюдаемым и versioned.

Старые stored embeddings нельзя молча сравнивать с новыми как будто space не изменился.

Default policy:

```text
feature vectors разных incompatible revisions
→ не считаются взаимозаменяемыми
```

Возможные будущие решения:

- re-encoding из сохранённого source;
- frozen encoder;
- compatibility adapter;
- jointly trained mixed-version consumer;
- explicit drift compensation.

Они не выбираются в `DU-08`.

## 12.2. Frozen evaluation

Confirmatory frozen evaluation должна pin'ить relevant representation/encoder revisions.

Изменение perception weights в ходе supposedly frozen run является `Learning Update`, а не незаметной runtime adaptation.

---

# 13. Canonical representation и Cortex

Cortex не является обязательной частью Perception.

Главный invariant:

```text
Canonical Percept
≠
Cortex hidden state
```

Будущий Cortex adapter сможет:

- читать разрешённые части Canonical Percept;
- создавать optional Cortex-derived Feature View;
- кодировать текстовую sensory modality;
- предоставлять semantic interpretation capability.

Но:

- Cortex backend не становится semantic owner Semantic Core;
- hidden size/tokenization/model family не протекают в contracts независимых modules;
- `NoCortex` configuration должна сохранять рабочую Perception boundary;
- замена Cortex не меняет `percept_schema_revision` сама по себе.

Точные права Cortex определит `DU-10`.

---

# 14. Batch и variable-size semantics

Batching является execution optimization, а не cognitive semantics.

Каждый batch item относится к независимому causal observation/percept lineage.

Для variable-size entity collections:

- padding является implementation detail;
- padding mask не является entity;
- batch index не является semantic identity;
- порядок completion GPU kernels не создаёт causal order;
- cross-item attention/aggregation запрещены по умолчанию, если конкретный module contract не описывает такой смысл явно.

Entity-set consumers должны по возможности не зависеть от произвольной перестановки entities.

Архитектурно это оставляет возможность использовать set/graph/object-centric модели без фиксации конкретной neural architecture.

---

# 15. Device и backend independence

Перенос representation между CPU/GPU/remote execution не меняет её semantic identity сам по себе.

Concrete tensor layout/dtype/device metadata могут отличаться, но canonical semantics сохраняются.

Нельзя использовать:

- device id;
- memory address;
- Python object identity;
- backend-specific tensor subclass

как semantic identity percept/entity/feature view.

---

# 16. Lifecycle

Для одного нового Environment observation canonical flow conceptually:

```text
Outcome/Initial Observation Commit
        ↓
Perception ingress
        ↓
validation / normalization
        ↓
semantic extraction
        ↓
optional feature encoding
        ↓
staged Canonical Percept
        ↓
commit
        ↓
downstream cognitive modules
```

Один committed percept может использоваться несколькими Cognitive Cycles одного Decision Window, пока:

- не появился новый observation;
- не произошло explicit perception intervention/re-encoding;
- freshness contract не сделал view stale.

Perception не обязана бессмысленно пересчитываться в каждом Cognitive Cycle.

Если learned Perception обновилась после создания percept, уже committed percept не переписывается задним числом.

---

# 17. Failure и degradation

Нужно различать:

## Raw observation contract failure

Observation malformed относительно declared Environment schema.

Это integration/runtime error, а не `unknown perception`.

## Unsupported modality

Если active Perception implementation не поддерживает required modality:

- composition может быть invalid;
- либо capability явно `unavailable`, если task допускает отсутствие.

Hidden fallback на Cortex/другой encoder запрещён.

## Learned encoder failure

Не приводит к скрытому использованию Research Ground Truth или другой implementation.

Допустимая degradation policy должна быть заранее объявлена.

Например, configuration может явно разрешать:

```text
Semantic Core available
Learned Feature View unavailable
```

если downstream dependencies допускают это.

---

# 18. Observability

Research evidence Perception должна позволять связать:

```text
source Raw Observation identity
→ Perception attempt
→ normalization/encoder revisions
→ Semantic Core
→ Feature Views
→ committed CognitiveState revision
```

По необходимости research probes могут экспортировать:

- semantic percept;
- modality status;
- feature-view metadata;
- uncertainty/quality;
- learned encoder activations — только opt-in backend research capability.

Research observer не получает mutable reference на canonical/encoder-private state.

---

# 19. Intervention

MINDRA различает несколько intervention boundaries.

## 19.1. Sensor/input intervention

Изменение agent-visible Raw Observation **после** Environment projection, не меняющее Hidden World State.

Это отдельный experimental treatment, например:

- masking modality;
- удаление observable attribute;
- controlled sensory corruption.

Такое вмешательство не называется Environment world-state intervention.

## 19.2. Semantic percept intervention

Controlled override конкретного Canonical Percept field после Perception processing.

Provenance обязана показывать intervention origin.

## 19.3. Feature-view intervention

Изменение learned latent/view representation.

Для сильных latent interventions действуют OOD/off-target ограничения `DU-06`.

Natural percept не переписывается задним числом; confirmatory experiment предпочитает branch/fork.

---

# 20. Исследовательские controls и ablation

Perception должна поддерживать сравнения класса:

```text
structured Semantic Core only
vs
Semantic Core + learned Feature View
```

```text
full Perception
vs
NoOp/limited modality condition
```

```text
entity-aware representation
vs
parameter/compute-matched flattened representation
```

```text
partial observation
vs
full-observation Environment control
```

Позднее:

```text
NoCortex
vs
Cortex-derived view
```

Control implementation подключается через composition, а не скрытой веткой downstream module.

---

# 21. Evaluation implications

Будущий MINDRA-Eval должен уметь проверять как минимум:

## Schema fidelity

Perception выдаёт только contract-valid semantic data и корректную missingness/provenance.

## Observation fidelity

Для MicroWorld deterministic baseline canonical percept соответствует **agent-visible** observation, а не Hidden World State.

## Leakage resistance

Изменение research-only metadata при неизменном Agent Interaction Plane не должно менять natural percept.

## Permutation robustness

Перестановка encoding entities там, где порядок семантически не определён, не должна сама по себе менять meaning/output downstream consumers.

## Representation compatibility

Несовместимые feature revisions обнаруживаются, а не молча смешиваются.

## Drift measurement

Для learned encoder измеряется изменение representation на фиксированном probe set между revisions.

## No-Cortex viability

Базовая Perception boundary работает без Cortex.

## Ablation effect

Выигрыш learned/object-centric representation сравнивается с matched controls, а не только с «ничем».

Точные metrics/statistics появятся в `DU-28`.

---

# 22. Research evidence, учтённое при проектировании

`DU-08` использует следующие существующие идеи как evidence, но не копирует одну конкретную архитектуру:

- **Slot Attention (Locatello et al., 2020, arXiv:2006.15055)** — object-centric set-like representations могут выделять compositional scene elements вместо одного недифференцированного vector;
- **Set Transformer (Lee et al., 2018, arXiv:1810.00825)** — set-structured inputs допускают permutation-invariant attention-based processing;
- **Relational inductive biases / Graph Networks (Battaglia et al., 2018, arXiv:1806.01261)** — явные entities/relations дают полезную структурную bias для combinatorial reasoning;
- **Perceiver IO (Jaegle et al., 2021, arXiv:2107.14795)** — одна вычислительная архитектура может работать с heterogeneous/structured modalities без требования одного fixed input format;
- **DreamerV3 (Hafner et al., 2023, arXiv:2301.04104)** — learned compact latent representations эффективны для world-model-based agents, но это не требует использовать latent конкретной модели как universal inter-module contract;
- continual-representation работы показывают, что feature spaces могут drift при дальнейших updates, поэтому representation revision/compatibility нельзя считать вечной только из-за неизменной dimensionality.

---

# 23. Что принято

После `DU-08` канонически принято:

1. Perception отделяет Raw Observation от internal representation.
2. `Canonical Percept` является гибридом structured Semantic Core и optional Feature Views.
3. Один universal latent vector не является canonical inter-module representation.
4. Semantic Core описывает current observation, а не hidden belief/memory/future prediction.
5. Task Specification и External Task Feedback не поглощаются Perception.
6. Entity order не несёт смысла по умолчанию.
7. Persistent entity identity не предоставляется бесплатно.
8. Direct/normalized/perceptually inferred claims различаются provenance.
9. Невидимый hidden entity не создаётся Perception только из Research Ground Truth.
10. Missingness/modality availability являются explicit semantics.
11. Deterministic normalization и learned Perception различаются и versioned.
12. Feature View имеет собственную feature-space/encoder identity.
13. Равная dimensionality не означает feature compatibility.
14. Representation drift является наблюдаемым versioned явлением.
15. Cortex-derived representation может быть optional view, но не canonical owner Semantic Core.
16. `NoCortex` configuration сохраняет рабочую Perception boundary.
17. Batch/device/layout не определяют semantic identity.
18. Perception observability/interventions следуют отдельным causal boundaries.

---

# 24. Что остаётся открытым

`DU-08` намеренно не решает:

- exact canonical field paths;
- exact entity/relation schema;
- размер любого latent space;
- конкретный encoder architecture;
- нужны ли Slot Attention/GNN/Transformer/MLP;
- хранить ли Raw Observation целиком в runtime state или только в Evidence/trajectory;
- конкретную metric feature-space compatibility;
- policy re-encoding старой Memory после encoder update;
- exact Cortex feature adapter;
- exact multimodal fusion algorithm;
- final normalization constants/statistics;
- exact tensor batching/padding format.

Эти решения принимаются downstream design/version planning там, где появятся реальные требования.

---

# 25. Completion gate DU-08

`DU-08` считается завершённым, если:

- downstream module может зависеть от perceptual semantics, не зная MicroWorld wire-format;
- canonical representation не зависит от Cortex hidden size;
- structured и learned representations могут сосуществовать без смешения semantic ownership;
- partial/missing observation имеет явную семантику;
- representation provenance/version/drift определены;
- no-Cortex baseline архитектурно возможен;
- research intervention можно применить к input/semantic/feature boundaries без hidden mutation;
- не зафиксирована преждевременно конкретная neural/library implementation.

После этого допускается `DU-09 — Goal System`.