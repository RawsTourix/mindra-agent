# Experience / Data / Replay MINDRA

## Статус документа

**Design Update:** `DU-25 — Experience / Data / Replay`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет каноническую семантику опыта, траекторий, dataset projections и Training Replay MINDRA после того, как `DU-01 … DU-24` зафиксировали причинные границы cognition и interaction.

Ключевое решение `DU-25`:

- source of truth для записанного опыта — **append-only causal `Experience Journal`** из immutable по смыслу typed events;
- обычные episode/transition/sequence datasets являются **derived projections** этого журнала, а не альтернативной истиной;
- `TraceEvent` из Evidence Plane и `ExperienceEvent` различаются: не каждый диагностический trace обязан становиться canonical data event;
- `TrainingSample` всегда является derived data product и не переписывает source experience;
- hindsight/relabeling/feature extraction/windowing создают новый sample с explicit transformation lineage;
- `Agent Memory`, `Agent Memory Replay`, `Research Trajectory`, `Training Dataset` и `Training Replay` остаются разными сущностями;
- evaluator-only/Research Ground Truth хранится отдельными annotation records и не попадает в agent-visible/training features без explicit data policy;
- causality определяется logical identities/parent links/revisions, а не порядком физической записи или wall-clock;
- unresolved execution (`execution_unknown`), dispatch failure и partial execution являются first-class data cases и не насильно сворачиваются в RL transition;
- storage format, replay library и конкретная training schema намеренно не фиксируются.

Документ опирается на:

- [`execution-model.md`](execution-model.md) — logical time, Decision Window, Action/Outcome Commit, Replay Step;
- [`cognitive-state.md`](cognitive-state.md) — state/revision/provenance semantics;
- [`module-lifecycle.md`](module-lifecycle.md) — module/wave attempts и atomic commit;
- [`observability-and-intervention.md`](observability-and-intervention.md) — Evidence Plane, Trace Events, intervention lineage;
- [`modules/environment.md`](modules/environment.md) — Episode, World Manifest, hidden Research Ground Truth;
- [`modules/memory.md`](modules/memory.md) — Agent Memory отдельно от trajectory/replay;
- [`modules/memory-regulation.md`](modules/memory-regulation.md) — Agent Memory Replay отдельно от Training Replay;
- [`modules/world-model.md`](modules/world-model.md) — actual vs imagined trajectories;
- [`modules/policy-planner.md`](modules/policy-planner.md) — candidate/intent selection provenance;
- [`modules/action-boundary.md`](modules/action-boundary.md) — authorization/commit/dispatch/execution/outcome chain.

Документ намеренно **не** определяет:

- concrete optimizer/loss/training schedule — `DU-26`;
- checkpoint binary format и exact restore protocol — `DU-27`;
- evaluator metrics/splits — `DU-28`;
- конкретную database/Arrow/Parquet/HDF5/TFRecord/SQLite implementation;
- обязательный RLDS/Minari/Reverb backend;
- exact Python classes;
- конкретный reward definition;
- конкретный replay priority algorithm;
- universal feature set для любого training task.

---

# 1. Цель DU-25

После `DU-24` MINDRA имеет полную причинную цепочку:

```text
Observation
→ cognition
→ Policy candidates
→ SelectedActionIntent
→ Authorization
→ Action Commit
→ Dispatch
→ execution / transition
→ Outcome Commit
```

Внутри Decision Window дополнительно существуют:

```text
module attempts
wave commits
Memory retrieval
Workspace admission
Executive decisions
planning/imagination
interventions
state revisions
```

Классическая RL-структура:

```text
(s_t, a_t, r_t, s_(t+1))
```

не может быть единственным каноническим представлением этого опыта.

`DU-25` отвечает на вопросы:

1. что является immutable source experience;
2. как хранить причинные связи и revisions;
3. как получать Episode/Transition/Sequence projections;
4. как отличать actual/replayed/imagined/counterfactual/intervened data;
5. как хранить privileged research annotations без leakage;
6. как создавать derived training samples;
7. как Training Replay ссылается на source experience;
8. как представлять incomplete/unknown execution;
9. как переживать schema evolution и changing `agent_revision`;
10. как отделить core causal metadata от тяжёлых artifacts.

---

# 2. System boundary: Experience Data Plane находится вне cognition

`Experience Journal` не является частью agent-owned cognition state.

Conceptually:

```text
Agent / Environment / Runtime
          ↓
      Evidence Plane
          ↓
   Experience Recorder
          ↓
    Experience Journal
          ↓
   Projection / Dataset Builder
          ↓
 Derived Dataset / Samples
          ↓
      Training Runtime
```

`Experience Recorder` — внешняя data/evidence responsibility. Физически она может быть частью `Artifact Collector`, того же process или отдельного writer worker.

Главный invariant:

> запись опыта не должна скрыто менять cognition Agent.

Если recorder/storage недоступен:

```text
Agent/runtime status
≠
Experience recording status
≠
Research/training data validity
```

Agent может продолжить execution, если runtime policy это допускает, но соответствующая trajectory получает explicit completeness degradation.

---

# 3. Experience Journal — source of truth

## 3.1. Семантика

`Experience Journal` — append-only логическая коллекция typed `ExperienceEvent`.

Append-only означает **семантическую неизменяемость уже записанного факта**, а не запрет на физическую compaction/migration storage.

Нельзя делать:

```text
старый event
→ hindsight/relabel
→ переписать старый event
```

или:

```text
execution_unknown
→ позднее выяснили outcome
→ стереть unknown event
```

Правильно:

```text
E100 = execution_unknown
E147 = reconciliation result
E147 resolves E100
```

## 3.2. Experience Journal не делает Agent event-sourced

Очень важное различие:

```text
Experience data is event-sourced
≠
Agent runtime state is reconstructed only from events
```

`CognitiveState`, module-private state, Memory и другие runtime mechanisms остаются такими, как определено предыдущими DU.

Experience Journal — внешняя долговременная causal запись, а не primary runtime state container.

---

# 4. `TraceEvent` и `ExperienceEvent` — разные сущности

`DU-06` допускает очень глубокий tracing:

```text
module attempt
wave attempt
Cortex activation artifact
profiler event
raw tensor dump
...
```

Не всё это обязано входить в canonical experience dataset.

Канонически:

```text
TraceEvent
→ observability evidence

ExperienceEvent
→ durable normalized causal data event
```

`ExperienceEvent` может иметь:

```text
trace_refs[]
artifact_refs[]
```

и тем самым связываться с тяжёлой диагностикой без копирования её в core journal.

Обязательные event classes определяются semantic schema/version, а sampling raw activations не меняет саму interaction history.

---

# 5. Canonical `ExperienceEvent`

Каждый event conceptually имеет стабильный envelope:

```text
ExperienceEvent
├── event_id
├── event_schema_id / revision
├── event_kind
├── causal lineage identity
├── causal_parent_ids[]
├── logical time / scope identities
├── producer / owner boundary
├── source mode
├── intervention refs[]
├── visibility / trust class
├── revision references
├── semantic payload or payload ref
├── trace/artifact refs[]
├── completeness / integrity status
└── provenance
```

Exact serialization не фиксируется.

## 5.1. `event_id`

Должен быть устойчивым идентификатором конкретного записанного события и не зависеть от file offset/database row.

## 5.2. `event_kind`

Typed discriminator payload schema.

Примеры классов:

```text
session/episode/decision lifecycle
observation commit
state revision commit/ref
executive decision
policy candidate/selection/deferral
action authorization
action commit
dispatch/execution/reconciliation
environment transition
outcome commit
intervention
replay/consolidation reference
learning-update reference (после DU-26)
```

Список расширяемый и versioned.

## 5.3. Causal parents

Физический append order не является causal truth.

Например parallel module attempts могут быть записаны writer'ом в любом порядке.

Поэтому event должен иметь explicit причинные связи там, где они необходимы:

```text
E_action_commit
parent → E_authorization
parent → E_policy_selection
```

А `journal_position`/ingest sequence, если существует, является storage metadata, а не универсальным logical clock.

---

# 6. Temporal identities и scopes

Event по применимости связывается с:

```text
run_id
agent_session_id
episode_id
decision_window_id
cognitive_cycle_id
wave/attempt ids
environment_transition_id
replay_step_id
consolidation_event_id
learning_update_id
```

Не каждый event принадлежит всем scopes.

Отсутствие scope должно быть семантически явным:

```text
not_applicable
unavailable
missing
```

не должны молча схлопываться в `None` без contract semantics.

---

# 7. Revision references

Каждый causal event должен позволять установить behavior-relevant revisions, которые действительно относятся к нему.

Conceptually используется `CausalRevisionSet`:

```text
agent_revision
state_revision
memory_revision
world_belief/world_model_revision
self_belief/self_model_revision
goal revision
drive revision
affect revision
workspace revision
executive revision
policy revision
planner revision
action-boundary revision
environment/world manifest revision
representation/feature-space revisions, где применимо
```

Это **не означает**, что каждый event физически хранит десятки обязательных строк. Допустим shared revision bundle/manifest reference.

Главный invariant:

> derived sample обязан уметь восстановить, какая behavior-relevant версия породила source decision/action/evidence.

---

# 8. Online collection при changing Agent revisions

Рассмотрим:

```text
Policy выбирает action под Agent A17
→ Action Commit
→ online Learning Update
→ Agent становится A18
→ Environment outcome приходит позже
```

Нельзя записать весь transition как будто он произведён единой A18.

Нужно сохранить как минимум:

```text
behavior_agent_revision = A17
outcome_ingest/processing revision = A18   # если действительно так
```

и ссылки на точные causal events.

Derived dataset может содержать много `agent_revision`, но manifest должен явно объявлять heterogeneity. Нельзя маскировать mixed-policy/mixed-model data как dataset одного frozen Agent.

---

# 9. Provenance modes: не один комбинаторный enum

Состояния:

```text
natural
replayed
imagined
counterfactual
intervened
```

не всегда взаимоисключающие.

Например возможна:

```text
counterfactual + intervened
```

или:

```text
actual evaluation trajectory + intervention
```

Поэтому provenance должна быть многомерной, например conceptually:

```text
reality/source mode:
  actual | imagined | memory_reactivation | training_replay | counterfactual

intervention state:
  natural | intervention refs[]

execution context:
  normal_runtime | evaluation | offline_processing | training
```

Exact enum names позже могут измениться; канонично именно **несмешение ортогональных provenance dimensions**.

---

# 10. Agent-visible data и Research Ground Truth

Одна из самых опасных ошибок dataset design:

```text
agent-visible observation
+
hidden evaluator labels
→ один бесформенный info dict
```

MINDRA это запрещает.

## 10.1. Primary experience payload

Содержит normal causal data соответствующей boundary:

- то, что Agent действительно видел;
- то, что Agent действительно вычислил/выбрал;
- runtime state/effect references;
- external task feedback, если оно agent-visible;
- execution statuses.

## 10.2. `ResearchAnnotationRecord`

Evaluator-only/ground-truth данные записываются **отдельной сущностью**, которая ссылается на source events/trajectory:

```text
ResearchAnnotationRecord
├── annotation_id
├── target event/sample refs
├── visibility = evaluator_only
├── source/trust boundary
├── annotation schema/revision
├── payload / artifact ref
└── provenance
```

Например:

```text
true hidden world rule
shortest path
oracle success label
exact hidden object identity
counterfactual oracle
```

не становятся field'ами обычного Agent observation.

## 10.3. Privileged supervision

Training Runtime может использовать evaluator-only annotation **только через explicit dataset/training policy**.

Такой experiment должен быть маркирован как privileged/research-supervised.

Нельзя затем утверждать, что capability возникла только из natural agent-visible experience.

---

# 11. Core journal vs heavy artifacts

Нельзя требовать, чтобы каждый event физически содержал:

```text
full CognitiveState
all Cortex activations
all gradients
all images
all snapshots
```

Вводятся уровни:

```text
Core Event Envelope
→ маленькая причинная запись

Semantic Payload
→ structured data умеренного размера

Heavy Artifact
→ tensor/image/full snapshot/log blob
```

Event хранит `ArtifactRef`, conceptually содержащий:

```text
artifact_id
content identity/hash, если применимо
artifact schema/revision
codec/format
size
storage locator abstraction
availability/integrity
provenance
```

Физический storage backend остаётся deployment detail.

---

# 12. Experience projections

Source journal не обязан быть удобным training API.

Поэтому MINDRA принимает **materialized или on-demand derived projections**.

## 12.1. Episode projection

```text
EpisodeTrajectory
→ ordered/causally linked actual interaction events одного Episode
```

Может содержать ссылки на Decision Windows и boundary events, не копируя весь trace.

## 12.2. Decision Window projection

```text
DecisionTrajectory
├── observation/outcome input
├── cognitive revision sequence
├── executive decisions
├── planner/policy evidence refs
├── selected intent
├── authorization/commit
└── execution/outcome refs
```

Очень полезна для behavior analysis и imitation/metacognitive training.

## 12.3. Interaction Transition projection

Более общий объект, чем RL transition:

```text
InteractionTransitionView
├── source observation/state refs
├── selected/committed action refs
├── dispatch/execution status
├── environment transition ref?
├── outcome ref?
├── terminated/truncated
└── completeness status
```

Он может корректно существовать даже если:

```text
Action Commit exists
Environment Transition absent
```

## 12.4. RL-like transition sample

Классический sample создаётся **только когда необходимые semantics доступны**.

Например:

```text
observation_t
action_t
next_observation
training reward/target mapping
terminated
truncated
```

`reward` здесь не является каноническим полем source experience. Он может быть derived из:

```text
External Task Feedback
explicit internal objective mapping
research target
```

с обязательным `target/reward mapping revision`.

## 12.5. Sequence/window sample

Допустимы:

```text
fixed-length windows
full episodes
Decision Window sequences
n-step samples
history-conditioned sequences
```

Window extraction — derived transformation с lineage.

---

# 13. Failed dispatch и `execution_unknown`

Это один из главных аргументов против transition-table source of truth.

## 13.1. Definite non-send

```text
Action Commit AC10
DispatchAttempt D10
status = definitely_not_sent
```

Environment transition отсутствует.

## 13.2. Execution unknown

```text
Action Commit AC11
DispatchAttempt D11
status = execution_unknown
```

Нельзя fabricatе:

```text
next_state = previous_state
```

или:

```text
executed = false
```

До reconciliation это unresolved causal record.

## 13.3. Partial execution

Если Environment реально изменилась частично, сохраняются фактические transition/outcome records с:

```text
execution_status = partial
```

Нельзя отбрасывать partial effect только потому, что action не завершился успешно.

## 13.4. Training extraction

Обычный RL sample extractor может:

- исключить unresolved records;
- создать специальный masked sample;
- использовать их для failure-model training;

но это explicit derived policy.

Source journal остаётся неизменным.

---

# 14. Termination и truncation

`terminated` и `truncated` сохраняются отдельно согласно Environment contract.

Terminal outcome фиксируется **до reset**.

Derived sample не должен делать:

```text
truncated → terminal = true
```

без explicit transformation semantics.

Если episode оборван из-за data/runtime failure, это дополнительно отражается через integrity/completeness status, а не маскируется обычной task truncation.

---

# 15. Derived Dataset — immutable data product

`DatasetManifest` conceptually определяет:

```text
DatasetManifest
├── dataset_id / revision
├── source journal manifests/ranges
├── source environment/world distributions
├── source agent revisions
├── projection/extraction spec
├── visibility policy
├── include/exclude filters
├── transform chain
├── schema revisions
├── feature/representation revisions
├── split identity/policy
├── deterministic sampling/RNG metadata
├── quality/completeness requirements
├── artifact requirements
└── provenance
```

Dataset не должен зависеть от mutable meaning имени вроде:

```text
latest_train_data
```

без versioned manifest.

---

# 16. Training Sample — всегда derived

Канонически:

```text
Source ExperienceEvent(s)
       ↓
DataProjectionSpec
       ↓
SampleTransformationRecord(s)
       ↓
TrainingSample
```

`TrainingSample` имеет stable sample identity или reproducible derivation identity и source refs.

Примеры:

```text
Policy imitation sample
World Model sequence sample
Self Model calibration sample
Goal-conditioned sample
RL transition
n-step return sample
contrastive pair
```

Конкретные training consumers определит `DU-26`.

---

# 17. Hindsight / relabeling

Hindsight не переписывает source trajectory.

Неправильно:

```text
source Goal = G1
training failed
→ изменить source Goal на G2
```

Правильно:

```text
Source Experience
  original Goal = G1
        ↓
HindsightRelabelTransform R7
        ↓
Derived TrainingSample
  source_goal = G1
  relabeled_goal = G2
  achieved-outcome refs
  transform revision = R7
```

То же правило действует для:

- reward relabeling;
- target recomputation;
- synthetic negatives/positives;
- post-hoc annotations;
- feature re-encoding.

Derived target не становится историческим фактом о том, чего Agent хотел в момент действия.

---

# 18. Representation re-encoding

Если Perception/Cortex/Memory encoder изменился:

```text
Source semantic payload
→ encoder E7
→ feature view F7

позже
→ encoder E8
→ feature view F8
```

Source event остаётся тем же.

Re-encoding создаёт:

```text
new derived feature artifact / sample revision
```

и не переписывает старый feature-space provenance.

Это продолжает `DU-08/11` representation drift semantics.

---

# 19. Training Replay

## 19.1. Что это такое

`Training Replay` — повторное использование source/derived training data Training Runtime для Learning Update.

Он не является новым Environment experience.

## 19.2. Replay buffer не source of truth

```text
Experience Journal
→ Dataset / Samples
→ Replay Buffer/Table
→ Replay Selection
→ Training Runtime
```

Replay buffer/table может быть:

```text
FIFO
uniform
prioritized
reservoir
sequence-aware
online queue
```

но это ephemeral/derived training infrastructure.

Удаление item из replay buffer **не удаляет source experience**.

## 19.3. Replay selection provenance

`ReplaySelectionRecord` должен по применимости хранить:

```text
replay_step_id
sampler id/revision
population/buffer revision
selected sample/source ids
priority values
sampling probability, если определена
importance-weight metadata, если определено
RNG/seed semantics
training consumer ref
```

Exact priority algorithm относится к `DU-26`/конкретной версии.

## 19.4. Replay priority ≠ cognitive importance

TD-error, loss, replay priority или sampling frequency являются training-side metadata.

Они не становятся автоматически:

```text
Memory salience
Drive pressure
Valuation
Agent-visible importance
```

---

# 20. Agent Memory Replay и Training Replay

Сохраняется strict boundary `DU-20`:

```text
Agent Memory Replay / Reactivation
→ agent-owned memory dynamics

Training Replay
→ external optimization/data pipeline
```

Если один и тот же source episode используется обоими механизмами, это **два разных causal events** с разными owners/provenance.

Training replay не увеличивает:

```text
natural visitation count
Agent memory access count
Environment transition count
experienced novelty
```

если соответствующий subsystem специально не получает такой явный input.

---

# 21. Research annotation и data leakage safeguards

Dataset builder обязан работать с explicit `DataVisibilityPolicy`.

Conceptually минимум:

```text
agent_visible_only
research_privileged_allowed
public_export
restricted
```

Exact policy names позже могут измениться.

Главное правило:

> отсутствие запрета не означает право включить evaluator-only data.

Normal training dataset для claims о agent-derived cognition должен по умолчанию использовать agent-visible/agent-generated evidence.

Privileged supervision — opt-in condition с отдельным manifest.

---

# 22. Data quality / completeness

Не все journals/trajectories будут идеальны.

Нужна explicit semantics уровня:

```text
complete
partial
unresolved
corrupt
causal_gap
required_payload_missing
optional_artifact_missing
schema_unsupported
```

Точные enum names не frozen.

Очень важно различать:

```text
heavy activation artifact unavailable
```

и:

```text
Action Commit или Outcome event missing
```

Первое может не мешать обычному Policy training.

Второе может разрушить causal transition extraction.

Dataset manifest должен объявлять минимальные completeness requirements.

---

# 23. Late/out-of-order events

В распределённой/асинхронной записи физический writer может получить events не по causal order.

Поэтому допускается:

```text
append/ingest order ≠ logical order
```

Event correlation опирается на stable IDs, parent refs и logical scopes.

Поздно пришедший valid event не должен вынуждать переписывать предыдущие events; создаётся/добавляется новая запись, после чего projection может быть перестроена на новой journal revision/manifest.

---

# 24. Journal / Dataset revisions

Append-only журнал всё равно имеет evolving manifest/revision:

```text
Journal J100
→ добавлены события
→ Journal J101
```

Старые event identities не меняются.

Derived Dataset связывается с конкретным source manifest/range/revision.

Следовательно:

```text
same dataset query today
≠
same dataset tomorrow
```

если source journal вырос и manifest не зафиксирован.

Reproducible dataset требует frozen source selection manifest.

---

# 25. Schema evolution

Канонический event envelope должен быть более стабильным, чем typed payload schemas.

Conceptually:

```text
ExperienceEvent envelope v1
├── ObservationCommit payload schema O3
├── ActionCommit payload schema A2
└── Outcome payload schema U4
```

Reader обязан:

- знать supported schema/revision;
- отличать backward-compatible field addition от semantic breaking change;
- не молча reinterpret старый field под новым смыслом.

## 25.1. Migration

Schema migration может физически создать новый materialized dataset/journal representation.

Но migration должна иметь:

```text
source schema
migration id/revision
target schema
lossless/lossy status
provenance
```

При lossy migration source data нельзя выдавать за неизменённое.

---

# 26. Storage / compression tiers

Semantic architecture не фиксирует storage technology.

Допустима физическая схема:

```text
hot journal index
warm columnar data
cold object artifacts
```

или локальная single-file реализация для MicroWorld.

## 26.1. Lossless compression

Не меняет semantic identity payload.

## 26.2. Lossy compression / summarization

Создаёт derived artifact/data product с explicit loss semantics.

Нельзя silently удалить raw payload и продолжать утверждать, что dataset обладает тем же evidence completeness.

---

# 27. Snapshot links и causal replay

Experience events могут ссылаться на:

```text
Agent Snapshot
Environment Snapshot
World Manifest
checkpoint/artifact manifest
```

Exact checkpoint format — `DU-27`.

`DU-25` фиксирует только:

> replay/analysis должен уметь установить, от какого causally relevant snapshot/manifests начинается нужная ветка.

Полный deterministic replay не гарантируется одним event log, если не сохранены нужные private states/RNG/provider conditions.

Нельзя называть обычное повторное проигрывание events exact counterfactual clone без требований `DU-06/27`.

---

# 28. Deterministic sample extraction

Dataset/sample extraction, где требуется воспроизводимость, должна сохранять:

```text
extractor id/revision
source manifest
filter/order policy
windowing policy
RNG seed/state semantics
shuffle/sampler revision
```

В distributed pipeline exact byte-for-byte ordering может быть не гарантирован конкретной реализацией; тогда determinism level обязан быть объявлен честно.

Нельзя просто написать:

```text
seed=42
```

без версии source population/extractor.

---

# 29. Split provenance

Train/validation/test membership относится к **dataset/research policy**, а не intrinsic property raw event.

Dataset manifest должен уметь ссылаться на:

```text
Environment distribution split
World Manifest family
Episode/session grouping
holdout policy
split policy revision
```

Derived samples одного source trajectory не должны молча попадать в разные splits, если это создаёт leakage.

Точные benchmark split rules принадлежат `DU-28`.

---

# 30. External/human data: зарезервированная security/privacy boundary

Первая MicroWorld версия, вероятно, не содержит персональных данных.

Но schema должна позволять future metadata уровня:

```text
data sensitivity class
access policy ref
redaction/anonymization transform ref
consent/license/source provenance, где применимо
```

Это не делает MINDRA privacy framework.

Главный architectural rule:

> redaction/anonymization является data transformation с provenance, а не скрытым изменением source record.

---

# 31. Что должно быть в core experience, а что может быть artifact-only

## 31.1. Core causal data

Для causally useful trajectory должны сохраняться как минимум идентичности/links, позволяющие восстановить:

```text
observation/outcome commits
Decision Window identity
behavior-relevant revisions
Policy selection/deferral ref
SelectedActionIntent ref
authorization/Action Commit ref
dispatch/execution status
Environment transition/outcome ref
termination/truncation
intervention refs
integrity/completeness
```

## 31.2. Optional/heavy evidence

Могут быть artifact-only:

```text
full module tensors
Cortex hidden states
attention maps
gradients
profiling traces
full snapshots every cycle
rendered videos
```

Конкретный experiment может объявить такие artifacts required.

---

# 32. Experience Recorder failure semantics

Если event, обязательный для causal history, не записан:

```text
Agent outcome может оставаться valid
Experience data = incomplete
training/evaluation use may become invalid
```

Recorder не имеет права fabricate missing event из последующего state без explicit reconstruction record.

Post-hoc reconstruction допустима только как:

```text
Derived/Reconstructed Record
source evidence refs
reconstruction method/revision
uncertainty
```

а не как оригинальный event.

---

# 33. Observability и intervention

Нужно поддерживать research interventions на data layer:

```text
include/exclude event classes
mask agent-visible fields in derived sample
inject privileged label в explicit supervised condition
relabel goal
alter replay priority
shuffle sequence
remove planning evidence
```

Такие операции создают **derived dataset/sample lineage**.

Source Experience Journal не мутируется.

---

# 34. Controls / baselines

Будущая data/evaluation discipline должна позволять сравнивать:

```text
full causal journal projection
vs transition-only projection

natural-only dataset
vs mixed intervention/replay dataset

correct temporal sequence
vs shuffled sequence

original labels/goals
vs relabeled derived samples

uniform replay
vs prioritized replay
```

Важно отдельно измерять, не объясняется ли выигрыш training pipeline privileged leakage или extra data transformations.

---

# 35. Required invariants

Будущая реализация должна проверять автоматически, где применимо:

1. `ExperienceEvent.event_id` уникален в journal namespace;
2. event schema/revision известны reader'у либо явно unsupported;
3. causal parent ref существует или явно external/missing с integrity status;
4. immutable source event не изменяется hindsight/relabeling;
5. derived sample имеет source refs + transform lineage;
6. evaluator-only annotation не входит в agent-visible dataset без explicit policy;
7. `ActionCommitRecord` может существовать без Environment Transition;
8. `execution_unknown` не превращается в `not_executed` автоматически;
9. terminated/truncated различаются;
10. replay selection не создаёт natural experience;
11. Agent Memory Replay и Training Replay имеют разные event kinds/owners;
12. mixed `agent_revision` не скрывается;
13. source feature-space revision сохраняется после re-encoding;
14. dataset manifest фиксирует source selection/schema/transform revisions;
15. lossy transformation маркируется как lossy;
16. sample split сохраняет source-group leakage constraints;
17. physical ingest order не используется как единственное доказательство causal order;
18. missing required causal event влияет на completeness status;
19. replay retry/sampling RNG provenance сохраняется, если требуется воспроизводимость;
20. Research Ground Truth не становится обычным Agent observation через dataset plumbing.

---

# 36. Module / responsibility gate

`DU-25` **не создаёт новый cognitive module**.

Приняты logical responsibilities:

```text
Experience Recorder
Experience Journal / Store
Dataset / Projection Builder
Training Replay infrastructure
```

Они находятся за пределами Agent cognition boundary.

Agent-visible Memory остаётся `DU-11/20`.

Training Runtime — `DU-26`.

Artifact Storage — внешний storage owner физического хранения.

---

# 37. Implementation choices намеренно отложены

`DU-25` не выбирает:

```text
JSONL
SQLite
PostgreSQL
Arrow / Parquet
HDF5
TFRecord / RLDS
Minari
Reverb
TorchRL ReplayBuffer
Kafka
DuckDB
object-store product
```

Не выбран и concrete event serializer.

На version-design этапе допустим максимально простой локальный backend, если он сохраняет canonical semantics.

---

# 38. Completion gate DU-25

`DU-25` считается завершённым, когда однозначно понятно:

- что является source experience;
- как causal events отличаются от traces;
- как actual/intervened/imagined/replayed/counterfactual provenance хранится без смешения;
- как privileged annotations отделены от agent-visible data;
- как получить Episode/Decision/Transition/Sequence projections;
- как представлять no-transition/unknown/partial execution;
- как changing agent revisions сохраняются;
- как derived samples/relabeling сохраняют source lineage;
- как Training Replay отличается от Agent Memory Replay;
- как dataset schema/version/completeness/determinism описываются;
- какие heavy artifacts можно хранить отдельно;
- что должен получить `DU-26 — Training Lifecycle` как стабильную data boundary.

Следующий допустимый update после принятия:

```text
DU-26 — Training Lifecycle
```
