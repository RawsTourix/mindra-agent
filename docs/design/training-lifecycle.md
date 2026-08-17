# Training Lifecycle MINDRA

## Статус документа

**Design Update:** `DU-26 — Training Lifecycle`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет каноническую семантику обучения и изменения trainable state MINDRA поверх уже принятой архитектуры `DU-01 … DU-25`.

Ключевое решение `DU-26`:

- `Training Runtime` находится **вне agent-owned cognition**, хотя изменяемые параметры принадлежат соответствующим компонентам Agent;
- `runtime/adaptive state update`, `Memory Consolidation`, `Replay Step` и `Learning Update` — разные causal events;
- ordinary cognitive `compute()` не выполняет скрытый `optimizer.step()`;
- Training Runtime обучает **явно объявленный Trainable Revision Bundle**, привязанный к конкретным base revisions;
- результат optimization сначала является **candidate revision**, затем проходит validation/acceptance и только после этого может быть атомарно активирован как новая `agent_revision`/component revisions;
- уже выполняющаяся cognition не меняет параметры задним числом при online learning;
- source `TrainingSample`/Replay provenance из `DU-25` сохраняется до конкретного `LearningUpdateRecord`;
- supervised/self-supervised/RL/distillation/adapter tuning являются разными training conditions, но используют одну общую lifecycle boundary;
- privileged supervision допустим только явно и не может маскироваться под natural agent-visible learning;
- joint optimization, отдельные optimizers, LoRA/PEFT, full fine-tuning, конкретные losses и algorithms намеренно не фиксируются.

Документ опирается на:

- [`system-context.md`](system-context.md) — Training Runtime вне Agent boundary;
- [`execution-model.md`](execution-model.md) — `Learning Update` как отдельное logical event;
- [`cognitive-state.md`](cognitive-state.md) — committed runtime state/revision semantics;
- [`module-lifecycle.md`](module-lifecycle.md) — runtime module lifecycle;
- [`observability-and-intervention.md`](observability-and-intervention.md) — evidence/intervention;
- [`experience-data-replay.md`](experience-data-replay.md) — source experience, `TrainingSample`, replay provenance;
- [`modules/cortex.md`](modules/cortex.md) — frozen/adapted Cortex boundary;
- [`modules/perception.md`](modules/perception.md) — representation revision/drift;
- [`modules/memory.md`](modules/memory.md) — Memory representation compatibility;
- [`modules/world-model.md`](modules/world-model.md) — model revision/belief semantics;
- [`modules/self-model.md`](modules/self-model.md) — competence staleness при смене `agent_revision`;
- [`modules/policy-planner.md`](modules/policy-planner.md) — behavior revision attribution.

Документ намеренно **не** определяет:

- binary checkpoint format и exact restore protocol — `DU-27`;
- evaluation benchmark/metrics — `DU-28`;
- concrete PyTorch/JAX/Lightning/Transformers trainer;
- Adam/AdamW/SGD/Adafactor/8-bit optimizer;
- PPO/DQN/SAC/GRPO/BC/DPO/SFT как обязательный algorithm;
- LoRA/QLoRA/full fine-tuning как обязательный adaptation method;
- concrete batch size/lr/gradient accumulation/mixed precision;
- конкретный loss weighting algorithm;
- конкретный continual-learning method;
- конкретный distributed actor/learner topology.

---

# 1. Цель DU-26

До этого MINDRA уже умеет:

```text
experience
→ DatasetManifest
→ TrainingSample
→ ReplaySelection
```

Но ещё не определено:

```text
что именно является trainable
кто вычисляет loss/gradients
кто владеет optimizer state
когда update становится частью Agent
как online update взаимодействует с in-flight cognition
как version/revision provenance сохраняется
```

`DU-26` закрывает именно эту boundary.

---

# 2. Training Runtime находится вне cognition

Каноническая системная форма:

```text
Experience / Dataset Plane
          ↓
     Training Runtime
          ↓
 candidate trainable revisions
          ↓
 validation / acceptance
          ↓
 Revision Activation Boundary
          ↓
       MINDRA Agent
```

`Training Runtime` может физически работать:

- в том же Python process;
- отдельным worker/process;
- локально;
- в Google Colab;
- на remote GPU;

но deployment topology не меняет логическую границу.

Главный invariant:

> Training Runtime не является cognitive module и не читает/мутирует Agent state ambient способом.

Training Runtime получает только explicit training inputs/manifests/snapshots и публикует explicit training/update artifacts.

---

# 3. Четыре разных вида изменения

Канонически:

```text
Runtime State Update
≠
Memory Consolidation Event
≠
Replay Step
≠
Learning Update
```

## 3.1. Runtime State Update

Например:

```text
DriveState D_t → D_(t+1)
WorldBelief B_t → B_(t+1)
AffectState A_t → A_(t+1)
```

Это изменение текущего agent-owned runtime state без optimizer/gradient semantics.

## 3.2. Memory Consolidation Event

Создаёт/регулирует `MemoryRecord` и derived memory state согласно `DU-20`.

Не является параметрическим обучением.

## 3.3. Replay Step

Training Runtime повторно выбирает уже существующий source/derived sample.

Сам по себе replay ещё не меняет параметры.

## 3.4. Learning Update

Явное изменение trainable parameter/state revision через Training Runtime.

Только этот класс события может означать optimizer/gradient/model-fitting update в рамках `DU-26`.

---

# 4. Классы state: не всё изменяемое является trainable

MINDRA различает минимум:

```text
runtime mutable state
trainable parameter state
optimizer/trainer state
frozen parameter state
external artifact/checkpoint state
```

## 4.1. Runtime mutable state

Examples:

```text
World Belief
Self Belief
Memory Store
DriveStateSet
AffectStateSet
Workspace
Executive ledger
PlanState
```

Это не optimizer-owned parameters автоматически.

## 4.2. Trainable parameter state

Examples future implementations:

```text
Perception encoder weights
World Model weights
Self Model estimator weights
Policy weights
Planner learned controller weights
Intrinsic provider predictor weights
Cortex adapter weights
```

Только явно объявленные parameter groups trainable в данном `TrainingPlan`.

## 4.3. Optimizer/trainer state

Examples:

```text
Adam moments
learning-rate scheduler state
gradient scaler
EMA of training statistics
sampler counters
loss-scaling state
```

Этот state принадлежит Training Runtime/training artifact boundary, а не ordinary cognition.

## 4.4. Frozen parameter state

Например frozen Cortex base model может быть частью текущего Agent revision, но не входить в trainable set конкретного update.

---

# 5. `TrainableComponentDescriptor`

Каждый потенциально обучаемый component обязан уметь объявить semantic descriptor:

```text
TrainableComponentDescriptor
├── component_id
├── component_kind
├── current_component_revision
├── parameter/topology manifest ref
├── trainable capabilities
├── allowed training modes
├── compatible input/output contract revisions
├── parameter-group declarations
├── gradient-boundary declarations
├── activation constraints
├── snapshot/checkpoint hooks
└── provenance
```

Это не означает, что module предоставляет `optimizer.step()`.

Descriptor описывает **что Training Runtime может обучать**, а не выполняет обучение сам.

---

# 6. `TrainingPlan` — explicit training condition

Training Runtime никогда не получает неявную команду:

```text
train_everything()
```

Используется versioned `TrainingPlan`:

```text
TrainingPlan
├── plan_id / revision
├── training mode
├── target component(s)
├── base revision bundle
├── DatasetManifest / Replay source refs
├── DataVisibilityPolicy
├── objective/loss specification
├── optimizer/parameter-group policy
├── gradient-flow policy
├── schedule/budget
├── validation policy
├── activation policy
├── continual-learning/retention policy
├── determinism/RNG policy
└── provenance
```

`TrainingPlan` является research/version configuration, не cognitive Goal.

---

# 7. Base revision pinning

Каждый training attempt обязан знать, **от какой версии** он начал обновление.

```text
BaseRevisionBundle
├── agent_revision
├── target component revisions
├── representation revisions
├── parameter topology refs
└── compatibility refs
```

Нельзя:

```text
start training on W17
runtime silently updates to W18
optimizer continues as if base still W17
```

без explicit rebase/restart policy.

Если base revision устарела до candidate activation:

```text
candidate
→ validate compatibility
→ activate / rebase explicitly / reject stale
```

Silent stale rebase запрещён.

---

# 8. Training samples и behavior provenance

`DU-25` остаётся источником training data semantics.

Каждый update должен ссылаться минимум на:

```text
DatasetManifest / ReplaySelection
TrainingSample IDs
sample transformation lineage
source behavior revisions
visibility / privileged status
sampling probabilities / importance weights, если определены
```

Особенно для RL:

```text
behavior policy revision
≠
current learner policy revision
```

является normal case, а не metadata noise.

On-policy/off-policy semantics определяются конкретным TrainingPlan/algorithm и должны быть проверяемы по provenance.

---

# 9. Training Objective ≠ internal Utility

Канонически:

```text
Training Objective
≠
External Task Feedback
≠
Intrinsic Signal
≠
Drive
≠
ValueProfile
≠
Agent Goal
```

Training Objective — **внешне заданная optimization semantics**, описывающая, как изменить параметры.

Она может использовать derived targets из:

```text
External Task Feedback
Goal outcomes
World Model prediction targets
Self calibration outcomes
Intrinsic Signals
Value components
Research annotations
```

но каждое включение должно быть explicit в `TrainingTargetMapping`/`TrainingObjectiveSpec`.

Нельзя считать:

```text
novelty
→ intrinsic reward
→ training reward
```

автоматическим законом.

---

# 10. Multi-objective losses и aggregation

Training Runtime может иметь несколько loss/objective components:

```text
LossBundle
├── policy loss
├── value/prediction loss
├── representation loss
├── regularization
├── calibration loss
└── retention/anti-forgetting term
```

Но MINDRA не принимает universal:

```text
loss = Σ w_i loss_i
```

как архитектурный invariant.

Допускаются:

- explicit weighted aggregation;
- alternating objectives;
- separate optimizers/steps;
- constrained optimization;
- gradient surgery/multi-objective methods;
- module-specific objectives.

Любая aggregation/gradient policy имеет собственную identity/revision/provenance.

---

# 11. Gradient-flow boundary

Module dependency graph и gradient graph — **разные вещи**.

Например runtime:

```text
Perception → World Model
```

не означает автоматически:

```text
World Model loss
→ gradient through Perception encoder
```

TrainingPlan обязан явно объявить:

```text
GradientFlowPolicy
├── trainable parameter groups
├── allowed cross-component gradient edges
├── stop-gradient boundaries
├── shared parameter ownership
└── joint-update atomicity
```

Это предотвращает hidden training coupling, которое невозможно увидеть из runtime dependency graph.

---

# 12. Отдельные optimizers vs joint optimization

Ни один вариант не canonical по умолчанию.

Допустимо:

```text
Optimizer A → Perception
Optimizer B → World Model
Optimizer C → Policy
```

или explicit joint update:

```text
Perception + World Model
→ shared objective / coordinated gradients
→ one atomic RevisionBundle
```

Правило:

> один parameter tensor/semantic parameter group не должен независимо принадлежать двум конфликтующим optimizer owners без explicit coordination policy.

Joint optimization должна фиксировать coupling и активировать совместимый revision bundle атомарно.

---

# 13. Cortex training modes

Cortex boundary допускает минимум:

```text
frozen base
frozen base + fixed adapter
frozen base + trainable adapter
partial trainable backend
full trainable backend
```

`DU-26` не выбирает один режим.

Для домашнего/Colab prototype PEFT/LoRA является сильным practical candidate, потому что позволяет обучать небольшое число дополнительных параметров при frozen base model, но это implementation/version choice.

Base Cortex revision и adapter revision всегда различаются.

---

# 14. TrainingAttempt lifecycle

Conceptual lifecycle:

```text
TrainingPlan
      ↓
TrainingAttempt created
      ↓
base revisions pinned
      ↓
samples selected/materialized
      ↓
forward/objective computation
      ↓
gradient/update computation
      ↓
CandidateRevisionBundle
      ↓
numerical/integrity validation
      ↓
optional task/retention validation
      ↓
accept / reject
      ↓
LearningUpdateRecord
      ↓
Revision Activation
```

Не каждый optimizer step обязан сразу активироваться в live Agent.

Training Runtime может выполнять множество internal optimization steps до одного accepted revision candidate.

---

# 15. Candidate revision и active revision различаются

```text
CandidateRevisionBundle
≠
ActiveAgentRevision
```

Candidate может быть:

```text
pending_validation
accepted_for_activation
rejected
superseded
failed
```

Параметры не становятся частью live Agent только потому, что training loss уменьшился.

---

# 16. `LearningUpdateRecord`

После accepted training attempt создаётся immutable causal record:

```text
LearningUpdateRecord
├── learning_update_id
├── TrainingPlan ref
├── base revision bundle
├── target components
├── source dataset/replay refs
├── objective/optimizer revisions
├── update statistics
├── candidate component revisions
├── validation results
├── privileged-supervision status
├── RNG/determinism refs
├── artifacts/checkpoint refs
└── provenance
```

Это record **факта обучения**, но ещё не обязательно факт активации live Agent.

`DU-25 Experience Journal` после `DU-26` может ссылаться на такие records/events.

---

# 17. Revision Activation — отдельная causal boundary

Активация новых параметров должна происходить атомарно относительно совместимого bundle.

```text
AgentRevision A17
        ↓
accepted candidate bundle C18
        ↓
RevisionActivation
        ↓
AgentRevision A18
```

`A18` явно перечисляет component revisions, которые образуют совместимую композицию.

Нельзя активировать:

```text
new Perception encoder
+
old incompatible Memory embeddings
```

без explicit compatibility/degradation/migration semantics.

---

# 18. Online learning: никаких mid-decision mutations

Если Training Runtime работает параллельно с cognition:

```text
Decision Window D10
uses Agent A17

Training Runtime
creates A18 candidate
```

то D10 не меняется на A18 посередине.

Default semantic rule:

> in-flight causal segment продолжает использовать pinned active revision; новая revision активируется только на explicit safe activation boundary.

Возможные safe boundaries конкретной версии:

- между Decision Windows;
- между Episodes;
- между Agent Sessions;

выбираются позже.

После activation новые decision windows используют новую revision.

---

# 19. Policy lag и mixed-revision experience

Decoupled online actor/learner является допустимым architecture pattern.

При этом:

```text
behavior_revision
≠
learner_revision
```

может быть ожидаемым состоянием.

Training algorithm обязан либо:

- быть корректным для такого off-policy lag;
- иметь explicit correction;
- ограничивать допустимый lag;
- либо отклонять несовместимые samples.

Сам Training Lifecycle не выбирает конкретную correction formula.

---

# 20. Offline, batch-online и continuous-online режимы

Канонически различаются:

## Offline

```text
frozen source dataset
→ training
→ candidate revision
→ validation
→ activation later
```

## Interleaved / batch-online

```text
collect experience
→ pause/trigger Learning Update
→ activate at safe boundary
→ continue collection
```

## Decoupled continuous-online

```text
Actor/Agent A_n continuously acts
Learner asynchronously trains A_(n+1)...
Revision activation occurs through explicit boundary
```

Все три используют одну revision/provenance model.

---

# 21. Privileged supervision

`ResearchAnnotationRecord` из `DU-25` может использоваться только если TrainingPlan явно объявляет:

```text
privileged_supervision = true
```

и фиксирует:

- какие annotation classes использованы;
- какие target fields из них выведены;
- какой claim разрешён после такого обучения.

Нельзя сравнивать privileged-trained и natural-only agent как будто они получили одинаковую information budget.

---

# 22. Representation drift после Learning Update

Если обучается encoder/World Model/Cortex adapter, новый update может изменить representation space.

Поэтому Learning Update обязан объявить effects на:

```text
feature_space_revision
encoder revision
representation compatibility
Memory representation validity
World/Self competence compatibility
Planner/Policy input compatibility
```

Нельзя молча активировать новый encoder и продолжить читать старые embeddings как будто coordinate system не изменился.

Possible later/version policies:

```text
freeze downstream consumers
re-encode stored sources
compatibility adapter
mixed-revision support
joint retraining
reject activation
```

---

# 23. Self Model после обучения

Изменение Agent revision делает старые competence estimates потенциально stale.

После activation:

```text
Self Model
→ invalidate / transfer / recalibrate
```

согласно explicit compatibility policy.

Новая revision не получает автоматически старую self-confidence как истину.

---

# 24. Continual learning и catastrophic forgetting

Онлайн/последовательное обучение обязано рассматривать два разных риска:

```text
plasticity failure
catastrophic forgetting
```

Но `DU-26` не принимает конкретный mitigation algorithm.

TrainingPlan может иметь explicit retention policy/evaluation suite:

```text
previous-task validation
behavioral KL/drift diagnostics
replay of retained data
regularization
frozen subsets
adapter isolation
rollback threshold
```

Положительное обучение на новой задаче само по себе не считается успешным, если неприемлемо разрушены ранее проверенные capabilities.

---

# 25. Validation before activation

Minimum validation classes conceptually:

```text
numerical integrity
schema/contract compatibility
parameter topology compatibility
finite outputs/losses
required capability smoke tests
representation compatibility
regression/retention checks
training-condition-specific metrics
```

Evaluation Harness `DU-28` позже определит полную benchmark semantics.

`DU-26` фиксирует лишь правило:

> новая candidate revision не обязана и не должна активироваться без explicit acceptance policy.

---

# 26. Rollback semantics

Rollback не удаляет исторический Learning Update.

Conceptually:

```text
A17
→ LearningUpdate L18
→ activate A18
→ regression detected
→ RevisionActivation A17-compatible / A19 rollback bundle
```

История сохраняет:

```text
L18 happened
A18 was active
rollback happened later
```

Нельзя переписывать журнал так, будто плохой update никогда не существовал.

Exact checkpoint restore mechanics — `DU-27`.

---

# 27. Training failure/degradation

Нужно различать минимум:

```text
data unavailable/corrupt
sample incompatibility
privileged-policy violation
OOM/resource exhaustion
numerical divergence / NaN
optimizer failure
candidate validation failure
stale base revision
activation incompatibility
checkpoint/artifact failure
```

Failure Training Runtime не должен автоматически мутировать live Agent.

Если candidate failed:

```text
active agent revision remains unchanged
```

до explicit degradation/activation policy.

---

# 28. RNG и determinism

TrainingPlan/Attempt должен фиксировать causally relevant RNG semantics:

```text
data sampling RNG
augmentation/transform RNG
parameter initialization RNG
stochastic layer RNG
optimizer-related stochasticity
replay sampler RNG
```

Но exact reproducibility across hardware/framework kernels откладывается в `DU-27`.

`DU-26` требует как минимум manifest/trace identity того, что контролировалось.

---

# 29. Training metrics не становятся cognitive signals

Training Runtime может вычислять:

```text
loss
accuracy
KL
gradient norm
validation score
learning rate
replay priority
```

Они находятся во внешнем Training/Evidence Plane.

Нельзя автоматически делать:

```text
loss spike → Intrinsic Signal
validation score → Self Belief
replay priority → Salience
```

Для такого crossover нужен отдельный explicit agent-visible contract/design decision.

---

# 30. Optimizer state ownership

Optimizer state относится к конкретному:

```text
optimizer identity/revision
parameter-group topology
base/candidate training lineage
```

При изменении topology/adapter composition нельзя молча продолжать старый optimizer state.

Допустимы explicit policies:

```text
preserve compatible state
migrate state
reset selected groups
start new optimizer lineage
```

Exact checkpoint semantics — `DU-27`.

---

# 31. Snapshot/checkpoint boundary

`DU-26` определяет, **что Training Lifecycle создаёт causally relevant state**, который будущий checkpoint должен уметь сохранить:

```text
active/candidate component revisions
TrainingPlan/Attempt state
optimizer/trainer state
scheduler state
RNG state
sample/replay cursor refs
validation/activation state
```

Как именно это сериализуется и восстанавливается — `DU-27`.

---

# 32. Controls / research design

Training subsystem должен позволять сравнить минимум:

```text
FrozenAgent / NoLearning
vs
OfflineLearning
vs
InterleavedOnlineLearning
vs
DecoupledOnlineLearning
```

Для trainable Cortex:

```text
Frozen Cortex
vs
Adapter-only
vs
larger trainable subset/full fine-tune
```

При multi-module training:

```text
independent training
vs
joint training
vs
matched compute/parameter controls
```

А для continual learning:

```text
new-task improvement
+
old-capability retention
```

измеряются отдельно.

---

# 33. Completion gate DU-26

`DU-26` считается закрытым, если:

- Training Runtime однозначно отделён от Agent cognition;
- `Learning Update` отделён от runtime update/consolidation/replay;
- trainable parameters, optimizer state и runtime state имеют разных owners;
- TrainingPlan pin'ит base revisions/data/objectives/gradient boundaries;
- source TrainingSample provenance доходит до LearningUpdateRecord;
- candidate revision отделена от active revision;
- activation атомарна и не меняет in-flight cognition задним числом;
- online mixed-revision/off-policy data representable;
- privileged supervision explicit;
- representation drift/compatibility учитываются до activation;
- rollback/rejection не переписывают историю;
- concrete optimizer/framework/algorithm остаются unfrozen;
- `DU-27` может проектировать complete checkpoint/reproducibility semantics поверх определённого training state.
