# Checkpoint / Reproducibility / Compute MINDRA

## Статус документа

**Design Update:** `DU-27 — Checkpoint / Reproducibility / Compute`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет каноническую семантику snapshot/checkpoint, restore, reproducibility claims и compute manifests MINDRA поверх `DU-01 … DU-26`.

Ключевое решение `DU-27`:

- `AgentSnapshot`, persistent `Checkpoint`, `TrainingResumeCheckpoint` и `ExperimentManifest` — разные сущности;
- checkpoint является **manifest-driven набором content-identified artifacts**, а не одним обязательным файлом;
- exact causal restore требует всех causally relevant public/private/RNG/pending states, но не обещает bitwise reproducibility на другой software/hardware stack;
- restore имеет явный `RestoreProfile` и не маскирует approximate/portable migration под exact restore;
- consistent checkpoint создаётся на explicit causal capture boundary; manifest commit происходит только после успешной materialization/verification обязательных artifacts;
- Environment state и pending external action lifecycle входят в full-system restore semantics;
- `execution_unknown`/in-flight external effect может сделать checkpoint непригодным для безопасного branch restore до reconciliation;
- Training-resume checkpoint дополнительно сохраняет optimizer/scheduler/scaler/trainer/replay/data-cursor/candidate-revision state из `DU-26`;
- content identity отделена от physical path/storage backend;
- schema/code/software/hardware/environment manifests являются частью воспроизводимости;
- `seed` сам по себе не является доказательством reproducibility;
- compute accounting отделено от agent-visible `CognitiveResourceEnvelope`: infrastructure telemetry не становится cognition автоматически;
- exact format (`safetensors`, `torch.save`, DCP, SQLite, object storage и т.п.) намеренно не фиксируется.

Документ опирается на:

- [`system-context.md`](system-context.md) — Artifact Storage/Compute Substrate вне Agent boundary;
- [`execution-model.md`](execution-model.md) — causal/logical boundaries;
- [`cognitive-state.md`](cognitive-state.md) — committed state/snapshot semantics;
- [`observability-and-intervention.md`](observability-and-intervention.md) — snapshot/counterfactual evidence;
- [`modules/environment.md`](modules/environment.md) — world clone/restore/manifest;
- [`modules/memory.md`](modules/memory.md) — Memory snapshot/private/index state;
- [`modules/world-model.md`](modules/world-model.md) — hidden recurrent/belief state;
- [`modules/workspace.md`](modules/workspace.md) — Workspace snapshot;
- [`modules/executive-control.md`](modules/executive-control.md) — cognitive budget ledger;
- [`modules/policy-planner.md`](modules/policy-planner.md) — stochastic Policy/Planner state;
- [`modules/action-boundary.md`](modules/action-boundary.md) — committed/pending dispatch/execution lifecycle;
- [`experience-data-replay.md`](experience-data-replay.md) — journal/dataset/replay manifests;
- [`training-lifecycle.md`](training-lifecycle.md) — candidate revisions, optimizer/trainer state и activation.

Документ намеренно **не** выбирает:

- serialization framework/extension;
- tensor format;
- compression algorithm;
- object store/database;
- distributed checkpoint library;
- exact hash algorithm;
- exact retention policy;
- concrete container technology;
- конкретный determinism framework;
- exact FLOP/energy profiler;
- benchmark/evaluation semantics — `DU-28`.

---

# 1. Цель DU-27

После `DU-26` существует причинно богатая система:

```text
active AgentRevision
candidate AgentRevision(s)
CognitiveState + private states
Memory / Workspace / Executive state
Environment/world state
pending action lifecycle
Experience Journal / Dataset / Replay
Training Runtime + optimizer state
RNG state
```

Недостаточно сохранить только:

```text
model.pt
```

Нужно определить:

1. **что именно сохраняется**;
2. **какой causal moment фиксируется**;
3. **что означает restore**;
4. **какой уровень воспроизводимости реально обещан**;
5. **какие внешние artifacts/manifests нужны для проверки результата**;
6. **как считать compute без смешения infrastructure и cognition**.

---

# 2. Основные сущности

## 2.1. `AgentSnapshot`

`AgentSnapshot` — логический causally relevant снимок состояния **самого Agent** на конкретной допустимой causal boundary.

Он может включать:

```text
AgentSnapshot
├── active agent/component revisions
├── CognitiveState revision
├── module-private state
├── Memory state
├── World/Self state
├── Drives/Appraisal/Affect state
├── Salience provider state
├── Workspace state
├── Executive state + budget ledger
├── Planner/Policy persistent state
├── Action Boundary agent-side pending state
├── component RNG state
└── compatibility/provenance metadata
```

`AgentSnapshot`:

- не обязан быть persistent;
- не обязан включать Environment;
- не обязан включать Training Runtime;
- не является автоматически checkpoint file;
- является semantic объектом, необходимым для clone/intervention/counterfactual semantics.

## 2.2. `Checkpoint`

`Checkpoint` — persistent, verified и versioned artifact set, описанный `CheckpointManifest`.

```text
Checkpoint
=
CheckpointManifest
+
referenced immutable/versioned artifacts
```

Физически это может быть:

- один файл;
- directory;
- несколько tensor shards;
- local + remote artifacts;
- content-addressed objects;
- base checkpoint + delta chain.

Архитектура этого не фиксирует.

## 2.3. `TrainingResumeCheckpoint`

Расширенный checkpoint, пригодный для продолжения Training Attempt/Lifecycle.

Он требует, где применимо:

```text
active/candidate revision state
model/adapter parameters
optimizer state
lr scheduler state
grad scaler/mixed precision state
trainer counters
TrainingPlan / TrainingAttempt refs
replay population/sampler state
sample/dataloader cursor
training RNG
pending validation/activation state
```

Inference-only checkpoint может всего этого не содержать.

## 2.4. `FullSystemCheckpoint`

Checkpoint, который претендует на causal restore Agent + Environment + внешнего runtime state, необходимого для continuation/counterfactual branch.

Дополнительно включает/ссылается на:

```text
EnvironmentSnapshot / WorldManifest
Execution Runtime pending state
Action dispatch/execution reconciliation state
Experience Journal cursor/manifest
external capability compatibility state
```

## 2.5. `ExperimentManifest`

`ExperimentManifest` — не checkpoint и не Agent state.

Он описывает воспроизводимый research/run context:

```text
ExperimentManifest
├── code/repository revision
├── design/version/config manifests
├── checkpoint refs
├── Environment/world manifests
├── Dataset/Experience refs
├── software/runtime manifest
├── hardware/compute manifest
├── determinism/reproducibility policy
├── seed/RNG initialization policy
├── intervention/evaluation condition refs
├── outputs/artifacts/metrics refs
└── provenance
```

---

# 3. Snapshot ≠ Checkpoint ≠ Experiment Manifest

Канонически:

```text
AgentSnapshot
≠ Checkpoint
≠ TrainingResumeCheckpoint
≠ ExperimentManifest
```

Примеры:

- counterfactual clone внутри одного process может использовать `AgentSnapshot` без записи на диск;
- inference artifact может быть checkpoint без optimizer state;
- training resume требует более широкого checkpoint scope;
- ExperimentManifest может ссылаться на несколько checkpoints и datasets;
- один content artifact может переиспользоваться несколькими manifests.

---

# 4. Checkpoint scope должен быть явным

Каждый checkpoint объявляет `CheckpointScope`.

Минимально поддерживаемые semantic scopes:

```text
agent_inference
agent_exact_state
training_resume
full_system_resume
research_archive
```

Exact names не frozen.

Нельзя назвать checkpoint «полным», если отсутствует causally relevant state для заявленного use case.

Например:

```text
weights only
```

может быть корректным `agent_inference` checkpoint, но не `training_resume` и не exact counterfactual restore.

---

# 5. Causal capture boundary

Checkpoint должен относиться к однозначной causal cut.

Предпочтительная семантика:

```text
running system
    ↓
Checkpoint Capture Request
    ↓
reach allowed Capture Boundary
    ↓
freeze/pin logical revisions
    ↓
collect component snapshot descriptors
    ↓
materialize artifacts
    ↓
verify required artifacts
    ↓
commit CheckpointManifest LAST
```

До commit manifest набор artifacts является:

```text
staging / incomplete checkpoint attempt
```

а не валидным checkpoint.

---

# 6. Atomicity: logical two-phase capture

MINDRA принимает conceptual two-phase pattern.

## Phase A — prepare/pin

- определить base logical time/revisions;
- остановить или согласованно pin'ить state mutation на capture boundary;
- получить immutable/copy-on-write/stable snapshot views;
- зафиксировать required artifact set;
- проверить, что нет запрещённого unresolved external state для заявленного restore profile.

## Phase B — materialize/commit

- сохранить artifacts;
- вычислить content identities/integrity metadata;
- проверить обязательные pieces;
- записать/commit'ить final manifest.

Failure между A и B:

```text
CheckpointAttempt failed
→ live Agent не откатывается
→ incomplete artifacts не считаются valid checkpoint
```

Физическая реализация может отличаться.

---

# 7. In-flight cognition

Для exact restore checkpoint должен явно заявлять, допустим ли capture:

- между Decision Windows;
- между Cognitive Cycles;
- внутри scheduler wave;
- во время module compute;
- во время Training Attempt.

Предпочтительный baseline ранних версий:

```text
checkpoint only at committed safe boundaries
```

а не попытка serializовать произвольный Python stack/GPU kernel.

Если future backend умеет coordinated mid-step state capture, это отдельная capability.

---

# 8. External action lifecycle и checkpoint safety

`DU-24` создаёт особенно важный случай.

## 8.1. До `Action Commit`

Checkpoint может восстановить decision state без риска повторного внешнего effect, если остальной state captured согласованно.

## 8.2. После `Action Commit`, но до dispatch

Checkpoint обязан сохранить:

- `ActionCommitRecord`;
- stable dispatch identity;
- dispatch-not-yet-attempted state.

Restore не создаёт новый logical Action Commit.

## 8.3. Dispatch definitely not applied

Можно восстанавливать pending committed action согласно explicit retry semantics.

## 8.4. `execution_unknown`

Критический invariant:

> Checkpoint с unresolved external effect не является безопасной точкой для naive counterfactual branch/retry.

Он должен быть помечен как минимум:

```text
external_effect_status = unresolved
restore_requires_reconciliation = true
```

До reconciliation запрещено слепо отправлять тот же non-idempotent effect как будто он точно не произошёл.

## 8.5. Environment уже изменился

Full-system restore требует согласованного EnvironmentSnapshot того же causal cut. Restore только Agent на старое состояние при живом уже изменившемся внешнем мире — это **новый experiment/intervention**, а не exact continuation.

---

# 9. Environment snapshot

`FullSystemCheckpoint` хранит или ссылается на Environment state, достаточный для заявленной restore guarantee.

Для MicroWorld это может включать:

```text
WorldManifest
hidden world state
Environment RNG
transition counter
pending action/execution state
termination/truncation state
```

Hidden Environment state здесь находится **в research/checkpoint plane**, а не становится agent-visible data.

Checkpoint privilege не меняет normal runtime trust boundary.

---

# 10. RNG: seed недостаточен

Для exact continuation сохраняются, где применимо:

```text
root experiment seed
Environment RNG state
Policy sampling RNG
Planner/search RNG
World Model stochastic RNG
Intrinsic provider RNG
Memory sampling RNG
Training sampler RNG
Python/NumPy/framework RNG state
CPU/device RNG state
worker RNG state
```

Канонический invariant:

```text
same seed
≠
same current RNG state
```

После N случайных выборов два процесса с одинаковым initial seed могут находиться в разных состояниях генераторов.

---

# 11. Determinism policy

Checkpoint/Experiment manifest должен фиксировать `DeterminismPolicy`:

```text
strict requested?
known nondeterministic ops?
framework deterministic flags
algorithm/backend selection policy
precision/dtype policy
compiler/autotuning policy
worker/process count
parallelism topology
```

Нельзя утверждать bitwise reproducibility только потому, что сохранён seed.

---

# 12. Reproducibility claim levels

MINDRA не использует одно слово «reproducible» без scope.

`ReproducibilityClaim` должен указывать минимум:

```text
claim level
required manifests
allowed software/hardware differences
comparison criterion
known nondeterminism
validation evidence
```

Рекомендуемая semantic лестница:

## R0 — provenance reproducible

Можно установить:

- какой code/config/data/checkpoint использовался;
- какие revisions и условия породили result.

Не обещается повторение чисел.

## R1 — state-restorable

Checkpoint проходит structural/integrity restore и восстанавливает заявленный semantic state.

Не обещается identical future execution.

## R2 — deterministic-continuation within constrained stack

При фиксированных software/hardware/topology/determinism constraints восстановление должно приводить к одинаковой заявленной causal sequence/outputs в пределах определённого comparison criterion.

## R3 — bitwise-equivalent where supported

Требует exact byte/tensor/observable equivalence для явно ограниченного path и среды.

Это **не universal guarantee** MINDRA.

## R4 — statistically reproducible

Для stochastic experiments повторные runs должны воспроизводить заявленное распределение/aggregate result в рамках заранее определённого statistical criterion.

Нумерация/names candidate и могут быть уточнены до contract freeze; различие уровней является canonical.

---

# 13. Exact restore ≠ portable restore

Различаются минимум:

```text
exact_same_stack_restore
compatible_restore
portable_migrated_restore
approximate_restore
```

Например:

```text
GPU checkpoint → CPU inference
```

может быть semantic-compatible restore параметров, но не bitwise continuation GPU training.

Restore всегда сообщает фактический `RestoreProfile`.

Silent downgrade:

```text
requested exact
→ actually approximate
→ report success
```

запрещён.

---

# 14. Software / dependency manifest

Для reproducibility сохраняется versioned `SoftwareEnvironmentManifest`.

Conceptually:

```text
repository commit / dirty state
Python version
framework/library versions
compiler/runtime versions
CUDA/ROCm/runtime versions
model/tokenizer/backend revisions
relevant environment/config flags
container/image/package-lock identity, если используется
```

Не требуется копировать всю операционную систему в один текстовый файл; необходим reproducible identity/refs.

---

# 15. Hardware / topology manifest

`HardwareTopologyManifest` может включать:

```text
CPU architecture/model class
GPU/accelerator model(s)
VRAM/memory capacities
number of devices
parallelism topology
interconnect information где существенно
precision capabilities
provider/runtime class
```

Hardware metadata является research/infrastructure evidence.

Она **не становится Self Model/CognitiveState автоматически**.

---

# 16. Content identity ≠ physical location

Checkpoint artifact имеет stable logical identity и content/integrity identity.

Conceptually:

```text
ArtifactRef
├── logical_artifact_id
├── artifact_kind
├── content_digest
├── digest_algorithm
├── byte_size
├── schema/format revision
├── storage_location(s)
└── provenance
```

Следовательно:

```text
/mnt/data/model.bin
```

не является достаточной identity.

Один artifact может перемещаться между local disk/object storage без изменения semantic/content identity.

---

# 17. Integrity и authenticity

Минимальная checkpoint integrity требует:

- content digest/hash для immutable artifacts;
- manifest integrity;
- required artifact completeness;
- size/schema checks;
- corruption detection.

Cryptographic signing/authenticity policy может быть добавлена deployment/version design; `DU-27` не делает PKI обязательной.

---

# 18. Serialization safety

Архитектура не выбирает tensor format, но checkpoint contract должен отличать:

```text
passive data artifact
vs
format, способный исполнять/десериализовать код
```

Loader обязан знать trust/format semantics.

Это security/operational metadata, а не cognition.

---

# 19. Full vs incremental/delta checkpoint

Оба подхода допустимы.

## Full

Все необходимые artifacts независимо materialized.

Плюсы:

- простой restore;
- меньше dependency chain.

Минусы:

- больше storage/write cost.

## Incremental/delta

```text
Checkpoint C20
= base C17
+ changed artifacts Δ18..20
```

Требования:

- explicit base manifest refs;
- integrity всей chain;
- retention/GC не может удалить required base;
- restore failure сообщает missing dependency;
- compaction создаёт новый checkpoint/manifest, а не переписывает прошлый.

Конкретная delta algorithm не фиксируется.

---

# 20. Checkpoint retention / garbage collection

Retention policy относится к Artifact/Checkpoint infrastructure.

Она может учитывать:

- last N;
- best validated;
- milestone;
- experiment references;
- base dependencies delta chains;
- storage budget;
- legal/research preservation requirements.

Но:

```text
checkpoint retention priority
≠
Agent Memory importance
≠
Salience
≠
Valuation
```

---

# 21. Training resume semantics

`TrainingResumeCheckpoint` должен быть достаточен для заявленного уровня продолжения обучения.

Для exact-ish same-stack resume обычно causally relevant:

```text
base/active/candidate revisions
parameter values
optimizer slots
scheduler/scaler states
training counters
gradient accumulation state, если checkpoint boundary это допускает
replay/sampler state
DataLoader/sample cursor
training RNG
TrainingPlan/TrainingAttempt
validation/activation pending state
```

Если часть state намеренно не сохраняется, checkpoint обязан заявить:

```text
resume_semantics = warm_restart / approximate / weights_only / ...
```

а не называться exact resume.

---

# 22. Candidate revisions

Checkpoint может содержать/ссылаться одновременно на:

```text
active AgentRevision A17
candidate bundle C18
candidate validation state
activation pending state
```

Restore не активирует candidate автоматически.

Сохраняется инвариант `DU-26`:

```text
CandidateRevisionBundle
≠
Active AgentRevision
```

---

# 23. Experience / Dataset / Replay references

Checkpoint не обязан копировать весь `Experience Journal` внутрь себя.

Он может ссылаться на immutable/versioned manifests:

```text
ExperienceJournalManifest
DatasetManifest
ReplayPopulationManifest
Replay sampler/table revision
cursor/selection state
```

Для reproducible training resume соответствующие source artifacts должны оставаться доступными и integrity-verifiable.

---

# 24. Compute accounting

MINDRA различает два разных слоя.

## 24.1. Agent-visible cognitive resource semantics

Из `DU-22`:

```text
CognitiveResourceEnvelope
ExecutiveBudgetLedger
ActualResourceCost
```

Это agent-owned decision-relevant semantics.

## 24.2. Infrastructure compute evidence

Из `DU-27`:

```text
ComputeManifest
ComputeUsageRecord
```

Это research/runtime evidence, например:

```text
allocated device type/count
actual accelerator time
CPU time
wall-clock phases
peak memory/VRAM
precision/dtype
batch/sequence shapes where relevant
compile/warmup distinction
estimated/measured FLOPs where available
network/storage I/O where relevant
energy/power where available
provider/runtime identity
```

Канонически:

```text
infrastructure compute telemetry
≠
CognitiveResourceEnvelope
```

Если Agent должен учитывать реальный latency/cost/energy, это должно быть отдельной intentional agent-visible contract boundary.

---

# 25. Requested / allocated / consumed compute

Как и в `DU-22`, важно не смешивать:

```text
requested resource
allocated resource
actual consumed resource
estimated compute
measured compute
```

Например заявленные `1000 tokens` не равны фактическим accelerator FLOPs.

Compute metrics обязаны хранить method/provenance:

```text
measured
estimated
provider-reported
derived
unavailable
```

---

# 26. Compute-normalized research

Future `MINDRA-Eval` должен уметь сравнивать конфигурации не только по task score, но и по resource frontier.

Для reproducible result необходимо знать минимум:

- какой budget был разрешён;
- что фактически было потреблено;
- какая hardware/software topology использовалась;
- какие expensive optional operations (Cortex/rollout/training) реально выполнялись.

Но конкретные benchmark metrics определит `DU-28`.

---

# 27. Restore validation

Restore — не просто успешная десериализация.

Минимальные stages:

```text
manifest parse
→ integrity verification
→ schema/contract compatibility
→ artifact availability
→ revision compatibility
→ environment/action pending-state checks
→ state materialization
→ invariant validation
→ optional deterministic probe
→ restore accepted/rejected
```

Каждый restore создаёт `RestoreRecord`.

---

# 28. Schema migration

Старый checkpoint может потребовать migration.

Правильно:

```text
Checkpoint C10
   ↓
MigrationPolicy M3
   ↓
Migrated artifact/checkpoint C10'
   ↓
RestoreRecord
```

Сохраняются:

- original checkpoint identity;
- migration policy/revision;
- transformed artifact identities;
- lossless/lossy classification;
- warnings/limitations.

Silent mutation старого checkpoint запрещена.

---

# 29. Unknown / unsupported state

Если loader не понимает обязательный artifact/state:

```text
restore = rejected / unsupported
```

а не:

```text
skip field
→ pretend exact restore
```

Optional diagnostic artifacts могут отсутствовать отдельно от required causal state.

---

# 30. Approximate restore

Иногда полезно восстановить только часть state, например:

```text
weights + Memory
без optimizer
без old Executive ledger
```

Это допустимо как **явно named approximate/partial restore**.

Такой restore создаёт новый causal lineage/Agent initialization event и не masquerade как exact continuation старого run.

---

# 31. Counterfactual branching

Exact counterfactual branch требует общего verified base state.

Conceptually:

```text
FullSystemCheckpoint C42
        │
        ├── Branch A
        └── Branch B
```

Для причинного сравнения branches должны pin'ить одинаковые required artifacts/revisions/RNG state до intentional intervention.

Если Environment/remote provider не clonable, claim scope ограничивается.

---

# 32. Remote / black-box components

Remote Cortex/API/provider может не позволять сохранить:

- internal hidden state;
- exact model revision;
- backend RNG;
- provider scheduling.

Checkpoint обязан честно отмечать:

```text
external_state_capture = unavailable/partial
provider_revision_guarantee = ...
```

В таком случае нельзя заявлять exact full-system continuation, если результат зависит от недоступного state.

---

# 33. Checkpoint failure semantics

Минимальные классы:

```text
capture_boundary_unavailable
unresolved_external_effect
artifact_write_failure
artifact_corrupt
manifest_incomplete
integrity_mismatch
unsupported_schema
migration_failed
missing_base_checkpoint
missing_external_artifact
restore_invariant_failed
nondeterminism_claim_violation
```

Exact enums не frozen.

Failure checkpoint creation не мутирует live Agent автоматически.

---

# 34. Checkpoint observability

Evidence Plane должен уметь фиксировать:

```text
CheckpointAttempt started
capture boundary
pinned revisions
artifact plan
artifact writes
hash/integrity results
manifest commit
restore attempt
migration
restore validation
reproducibility probe
compute usage
```

Heavy binary contents остаются Artifact Storage references, а не TraceEvent payload.

---

# 35. Intervention и checkpoint

Intervention может intentionally создать branch от checkpoint.

Нужно сохранять:

```text
base_checkpoint_id
intervention_id
modified state targets
pre/post revision refs
branch identity
```

Нельзя изменить checkpoint file inplace и продолжить называть это тем же base condition.

---

# 36. Checkpoint и security/trust

Checkpoint может содержать:

- privileged Environment state;
- private Agent Memory;
- training annotations;
- provider credentials refs;
- potentially unsafe serialization.

Поэтому manifest должен поддерживать visibility/trust classification.

Secrets/credentials по умолчанию **не должны архивироваться как обычный checkpoint payload**; сохраняются safe refs/config requirements, если необходимо.

Полная security threat model остаётся вне DU-27.

---

# 37. Portability

Portability является отдельной характеристикой artifact/checkpoint.

Можно иметь:

```text
portable parameters artifact
+
hardware-specific optimizer shard
+
provider-specific runtime state
```

Поэтому portable/nonportable задаётся по artifacts и restore profile, а не одним boolean для всего checkpoint.

---

# 38. Distributed/sharded checkpoint

Архитектура допускает sharded checkpoint и load-time resharding.

Но:

```text
shard layout
≠
semantic Agent parameter topology
```

Physical distributed layout является artifact/backend detail и не должен протекать в cognitive contracts.

---

# 39. Baselines и проверки DU-27

Минимальные engineering/research controls:

## 39.1. Weights-only vs full training resume

Проверить, что weights-only restore честно отличается от resume с optimizer/RNG/cursor state.

## 39.2. Seed-only vs RNG-state restore

Показать, что система не делает ложное утверждение `same seed = same continuation`.

## 39.3. Same-stack deterministic replay

Для поддерживаемого deterministic path сравнить restored continuation с uninterrupted control.

## 39.4. Cross-device portable restore

Отдельно проверить semantic compatibility без обещания bitwise equality.

## 39.5. Corruption test

Изменённый artifact должен быть обнаружен integrity verification.

## 39.6. Missing delta base

Restore обязан fail closed, а не silently продолжать с неполным state.

## 39.7. `execution_unknown`

Checkpoint не должен приводить к duplicate external effect после restore.

## 39.8. Candidate revision restore

Candidate остаётся candidate; restore не активирует его случайно.

## 39.9. Environment/Agent causal cut

Counterfactual branches должны стартовать из согласованного world/Agent state.

---

# 40. Negative gate для exact reproducibility claims

Если система не может показать:

- сохранение causally relevant state;
- integrity manifests;
- explicit deterministic constraints;
- согласованный Environment/Agent cut;
- воспроизводимый continuation probe;

она не имеет права использовать сильную формулировку `exactly reproducible`.

Допустимый результат:

```text
provenance reproducible
but execution nondeterministic
```

лучше ложного exact claim.

---

# 41. Что остаётся implementation choice

До version design не фиксируются:

```text
torch.save
safetensors
PyTorch DCP
Accelerate save_state
pickle
JSON/MsgPack/Protobuf
SQLite/object storage
zstd/gzip
SHA-256/BLAKE3
Docker/Nix/Conda/uv/Poetry
MLflow/W&B
specific profiler
specific cloud provider
```

Каждый concrete choice должен удовлетворять semantic requirements этого DU.

---

# 42. Граница DU-28

`DU-27` определяет:

> **можно ли однозначно установить и восстановить condition/run state и сколько compute он реально использовал?**

`DU-28 — MINDRA-Eval` определит:

> **что именно измерять и как доказать функциональную ценность MINDRA?**

Checkpoint/compute metadata будут входом Evaluation Harness, но метрики/benchmark tasks/statistical protocol не определяются здесь.

---

# 43. Итоговые инварианты DU-27

```text
AgentSnapshot
≠ persistent Checkpoint
≠ TrainingResumeCheckpoint
≠ ExperimentManifest

same seed
≠ same RNG state
≠ guaranteed same execution

semantic restore
≠ bitwise reproducibility

active revision
≠ candidate revision

checkpoint artifact identity
≠ physical path

Agent checkpoint
≠ Environment snapshot

infrastructure compute telemetry
≠ CognitiveResourceEnvelope

weights-only
≠ training-resume state
```

И обязательно:

```text
consistent causal capture
explicit scope
content/integrity identity
restore profile
reproducibility claim scope
software/hardware manifests
RNG provenance
pending external-effect safety
compute provenance
```

---

# 44. Completion gate DU-27

`DU-27` считается завершённым, когда:

- snapshot/checkpoint/manifest semantics разведены;
- checkpoint scope и required-state semantics определены;
- training-resume state интегрирован с `DU-26`;
- Environment/action pending-state restore semantics определены;
- atomic capture/manifest commit model определена;
- RNG/determinism/reproducibility claim levels определены;
- exact/portable/approximate restore разведены;
- artifact identity/integrity/migration semantics определены;
- full/delta checkpoint requirements определены;
- software/hardware/compute manifests определены;
- safeguards/controls определены;
- candidate contract и ADR созданы;
- research pass сохранён;
- repository consistency обновлена;
- следующим допустимым DU становится `DU-28 — MINDRA-Eval`.
