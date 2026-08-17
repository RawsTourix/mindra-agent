# Candidate contract Environment MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-07 — Environment / MicroWorld Contract`

Этот документ уточняет machine-facing **классы операций и данных**, которые будущая реализация Environment должна уметь выразить.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- имена конкретных методов;
- Gymnasium как dependency;
- concrete dataclass/TensorDict/Pydantic types;
- dtype/shape;
- serialization encoding;
- exception hierarchy.

Приоритет семантики имеет [`../modules/environment.md`](../modules/environment.md).

---

# 1. Две capability surfaces

Future Environment implementation должна логически разделять:

```text
Agent-facing interaction capability
Research-facing environment capability
```

Один concrete object может физически реализовывать обе capability, но consumer rights остаются разными.

Agent и cognitive modules не получают research-facing capability.

---

# 2. Agent-facing capability

Минимально должна быть выразима следующая семантика.

## Describe interaction

Получить стабильное описание agent-visible contract:

- observation schema identity;
- action schema identity;
- task-feedback schema identity;
- supported interaction capabilities;
- semantic Environment version.

Описание не включает hidden rule mapping или split metadata, если они не являются agent-visible по task design.

## Reset Episode

Conceptual input:

```text
EpisodeStartRequest
```

Research/runtime может передать world/task selection и seed bundle через control boundary, но эти control fields не становятся автоматически Agent-visible.

Conceptual agent-facing output:

```text
EpisodeStartResult
├── raw_observation
├── external_task_specification? 
├── external_task_feedback? 
├── terminated = false
└── truncated = false
```

Research-only reset evidence возвращается/публикуется через отдельную boundary.

## Apply committed action

Conceptual input:

```text
CommittedAction
├── action_schema_revision
├── action_payload
└── causal identity
```

Conceptual agent-facing output:

```text
InteractionResult
├── raw_observation
├── external_task_feedback?
├── agent_visible_action_outcome?
├── terminated
└── truncated
```

`agent_visible_action_outcome` не обязан содержать privileged failure reason.

---

# 3. Research-facing capability

Evaluation/Experiment infrastructure должна иметь отдельную capability для операций класса:

- inspect Environment identity/version;
- получить authoritative transition evidence;
- snapshot;
- restore;
- clone;
- fork;
- controlled intervention;
- получить generation/world manifest metadata;
- проверить task validity/solvability, если family это поддерживает;
- получить research-only objective metrics/oracle information.

Эти операции не являются Agent actions.

---

# 4. Environment identity

Future Environment descriptor должен позволять восстановить минимум:

```text
environment_family
environment_semantic_version
engine_version
generator_version
task_family
task_version
distribution_id
distribution_version
world_instance_id
world_manifest_identity?
```

Конкретный identifier format определяется позднее.

---

# 5. RNG identity/state

Future contract должен позволять независимо учитывать causally relevant Environment random streams.

Минимальные semantic roles:

```text
generation_rng
dynamics_rng
task_rng? 
```

Snapshot обязан включать текущее состояние всех streams, влияющих на future Environment transitions.

Seed bundle используется для создания/reproduction, но не заменяет snapshot.

---

# 6. Environment Snapshot candidate semantics

`EnvironmentSnapshot` conceptually должен содержать или однозначно ссылаться на:

```text
snapshot_identity
parent_lineage
Environment/world/task versions
World Manifest identity
complete hidden world state
embodiment/world-side state
task state
episode counters
pending events
RNG states
termination/truncation state
intervention provenance
compatibility metadata
```

Snapshot должен быть semantically immutable после создания.

Exact binary/text representation определяется в `DU-27`.

---

# 7. Clone / restore / fork

## Restore

Восстановить Environment instance из совместимого snapshot.

Requirements:

- validate semantic/version compatibility;
- не смешивать прежнюю и restored lineage;
- восстановить causally relevant RNG state;
- не публиковать restore как natural Environment Transition.

## Clone

Создать независимый instance из snapshot.

Изменения clone не должны менять original instance.

## Fork

Создать независимую research lineage с явной parent snapshot relation.

Fork identity должна попадать в transition evidence.

---

# 8. Environment intervention candidate

`EnvironmentIntervention` conceptually содержит:

```text
intervention_id
base_snapshot_or_revision
target
treatment
persistence/duration
provenance
```

Результат intervention:

- проходит validation;
- создаёт identifiable intervened state/lineage;
- не маскируется под natural world transition;
- не сообщает Agent privileged treatment metadata автоматически.

Exact intervention target vocabulary определяется конкретной Environment family.

---

# 9. Transition Evidence candidate

Authoritative `EnvironmentTransitionRecord` conceptually содержит:

```text
run/session/episode identity
environment identity
world instance identity
transition identity
pre-state/snapshot reference
committed action
structural action validation status
full world-level action outcome
dynamics RNG provenance
external task feedback
objective research events/metrics
termination/truncation + reason
post-state/snapshot reference
intervention lineage/provenance
```

Record является research evidence и **не передаётся Agent целиком**.

---

# 10. Action semantics candidate

Future action contract обязан различать:

```text
schema-invalid action
valid action attempt
valid-but-ineffective action
stochastic action failure
successful world effect
```

Concrete task family может иметь более богатую outcome taxonomy.

Structural schema error не должен маскироваться под нормальный no-op world outcome.

---

# 11. Termination contract

Interaction result обязан отдельно выражать:

```text
terminated
truncated
```

Research evidence дополнительно сохраняет machine-readable reason/category.

Final observation/outcome должен быть доступен evidence pipeline до reset следующего Episode.

---

# 12. Observation privacy candidate

Agent-facing observation type не должен содержать research-only fields даже если concrete implementation хранит всё в одном object.

Нужна enforceable boundary между:

```text
RawObservation
ResearchGroundTruth
```

Не полагаться только на соглашение «Agent просто не читает ключ `_hidden`».

Точный enforcement mechanism определяется implementation design.

---

# 13. Split/distribution semantics candidate

Research-facing descriptor должен позволять идентифицировать distribution class и factor configuration.

Agent-facing observation не получает split metadata по умолчанию.

Будущие manifests должны уметь выразить:

- in-distribution train set/distribution;
- validation distribution;
- unseen test instances;
- compositional holdout;
- rule remapping;
- difficulty/scale shift;
- structural OOD, если используется.

---

# 14. World Manifest candidate

Для procedural environment future artifact должен уметь зафиксировать generated world независимо от одного seed.

Conceptual `WorldManifest` может включать:

```text
generator/version identity
factor configuration
world topology/content
observable appearance mapping
hidden rule mapping
task instance specification
initial embodiment state
content hash
solvability/validator status
```

Agent не получает hidden manifest автоматически.

---

# 15. Batch/vectorized semantics candidate

Vectorized wrapper должен сохранять отдельную identity для каждого Environment instance.

Batch API не имеет права:

- объединять RNG streams;
- терять final outcome при autoreset;
- использовать physical completion order как logical transition order;
- смешивать snapshots/lineages между batch items.

---

# 16. Gymnasium adapter candidate

Будущий adapter может отображать MINDRA Environment на Gymnasium-style:

```text
reset() -> observation, info
step(action) -> observation, reward, terminated, truncated, info
```

Но mapping обязан явно определить:

- какой компонент External Task Feedback становится `reward`;
- какие research-only данные допустимы только во внешнем `info` consumer path;
- что Agent wrapper фактически получает;
- как snapshot/restore/fork остаются вне обычного Gym API;
- как предотвращается privileged `info` leakage.

Gymnasium adapter не становится source of truth Environment semantics.

---

# 17. Статус exact contract

После `DU-07` этот документ является **candidate contract**, потому что:

- `DU-08` ещё не определил exact Raw Observation representation boundary;
- `DU-09` ещё не определил Goal ingestion;
- `DU-24` ещё не определил final Agent Action boundary;
- `DU-25` ещё не определил exact trajectory schema;
- `DU-27` ещё не определил snapshot serialization;
- `DU-28` ещё не определил benchmark manifests/evaluation harness.

Следовательно, Codex не должен превращать перечисленные conceptual type names в окончательный Python API раньше version planning/contract freeze.
