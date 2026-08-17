# DU-27 — Checkpoint / Reproducibility / Compute: research pass 2026-08

## Статус

**Дата:** 2026-08-17  
**Тип:** non-canonical research evidence  
**Связанный Design Update:** `DU-27 — Checkpoint / Reproducibility / Compute`

Документ не выбирает checkpoint format/library, hash, storage backend, container system или profiler.

---

# 1. Исследовательский вопрос

Нужно спроектировать semantic boundary:

```text
causally relevant state
→ persistent checkpoint
→ verified restore
→ reproducibility claim
```

и отдельно:

```text
run/training/evaluation
→ software/hardware/compute manifests
→ reproducible research condition
```

Ключевой риск — принять `save model weights + seed` за достаточную воспроизводимость сложного stateful Agent.

---

# 2. PyTorch Reproducibility

## Official documentation

- https://docs.pytorch.org/docs/stable/notes/randomness.html
- https://docs.pytorch.org/docs/stable/generated/torch.use_deterministic_algorithms.html

Актуальная документация PyTorch прямо отмечает:

- полная reproducibility не гарантируется между releases/commits/platforms;
- CPU/GPU results могут различаться даже при одинаковых seeds;
- deterministic algorithms помогают только части источников nondeterminism;
- deterministic mode может снижать performance;
- backend/autotuning/precision choices могут влиять на numerics.

Для MINDRA полезен вывод:

```text
seed
≠ reproducibility guarantee
```

и:

```text
bitwise reproducibility
```

должна быть scoped claim относительно конкретного software/hardware stack.

---

# 3. PyTorch saving/loading general checkpoints

## Official tutorial

- https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html

Для training resume PyTorch tutorial рекомендует сохранять не только model `state_dict`, но также optimizer `state_dict`, epoch/other training state.

Это подтверждает общий principle:

```text
inference weights
≠
training-resume checkpoint
```

MINDRA расширяет его на собственные trainer/replay/candidate revision/RNG/data cursor states.

`torch.save` не принимается как canonical format.

---

# 4. Hugging Face Accelerate checkpoint state

## Official documentation

- https://huggingface.co/docs/accelerate/basic_tutorials/migration

Accelerate `save_state()` / `load_state()` сохраняет/восстанавливает state model, optimizer, random generators и scheduler; дополнительные stateful objects могут быть зарегистрированы для checkpointing.

Также stateful DataLoader configuration позволяет сохранять position/cursor по training data.

Для MINDRA это useful implementation evidence для:

```text
optimizer state
+
RNG state
+
data cursor
```

как отдельных training-resume concerns.

Accelerate не становится architecture requirement.

---

# 5. PyTorch Distributed Checkpoint

## Official documentation

- https://docs.pytorch.org/docs/main/distributed.checkpoint.html
- https://docs.pytorch.org/tutorials/recipes/distributed_checkpoint_recipe.html

PyTorch Distributed Checkpoint:

- поддерживает parallel save/load;
- создаёт несколько files/shards;
- поддерживает load-time resharding;
- может загружать checkpoint при другой distributed world size/topology.

Для MINDRA важен общий вывод:

```text
physical shard layout
≠
semantic parameter/checkpoint identity
```

Это поддерживает manifest-driven artifact architecture.

DCP API/format не фиксируется.

---

# 6. Safetensors

## Official documentation

- https://huggingface.co/docs/safetensors/index
- https://huggingface.co/docs/safetensors/api/torch

Safetensors позиционируется как простой безопасный tensor-only format вместо pickle и поддерживает efficient tensor access/sharding patterns.

Практически это интересный candidate для immutable parameter artifacts.

Но:

- tensor-only artifact не решает semantic checkpoint manifest;
- optimizer/trainer/runtime metadata требует дополнительных artifacts;
- concurrent mutation во время save должна учитываться capture implementation.

Поэтому:

```text
safetensors
≠
MINDRA Checkpoint architecture
```

---

# 7. RNG state и activation checkpointing

## PyTorch checkpoint documentation

- https://docs.pytorch.org/docs/stable/checkpoint.html

PyTorch activation checkpointing отдельно сохраняет/восстанавливает RNG state, чтобы recomputation с random operations не меняла результат относительно обычного forward path.

Это полезный practical precedent:

```text
random generator current state
```

может быть causally significant отдельно от initial seed.

Activation checkpointing не связано напрямую с persistent MINDRA checkpoint semantics и не должно смешиваться терминологически.

---

# 8. Checkpoint terminology ambiguity

В ML термин `checkpoint` используется минимум для:

- persistent training state;
- inference weights;
- distributed/sharded model state;
- activation checkpointing (compute-memory trade-off).

MINDRA поэтому обязана использовать более точные понятия:

```text
AgentSnapshot
CheckpointManifest
TrainingResumeCheckpoint
ReproducibilityClaim
```

а `activation checkpointing` считать отдельной implementation optimization.

---

# 9. Reproducibility levels

Существующая framework documentation показывает, что один universal claim `reproducible=true` слишком сильный.

Для MINDRA целесообразно различать:

```text
provenance reproducibility
state restore
same-stack deterministic continuation
bitwise equality where supported
statistical reproducibility
```

Особенно важно не требовать bitwise equality от cross-device portable restore.

---

# 10. Environment + external effects

Обычные ML checkpoint tutorials в основном предполагают training/model state.

MINDRA дополнительно имеет:

```text
Action Commit
Dispatch
execution_unknown
Environment state
```

Поэтому full-system checkpoint должен учитывать distributed-systems-like problem:

> мог ли внешний effect уже произойти, даже если локальный runtime не получил подтверждение?

Это вывод напрямую из accepted `DU-24`, а не из одного ML framework.

Следствие:

```text
Agent checkpoint
+
live external world
```

не всегда образуют exact continuation point.

---

# 11. Content identity и storage location

Современные model ecosystems используют sharded/multi-file artifacts, remote storage и manifests/indexes.

Для MINDRA полезен architecture-neutral pattern:

```text
logical artifact identity
+
content/integrity digest
+
storage locations
```

Physical path не должен быть semantic identity.

Конкретный digest algorithm выбирается позже.

---

# 12. Atomic capture

Надёжный checkpoint сложной системы требует consistent causal cut.

MINDRA принимает conceptual:

```text
prepare/pin
→ materialize
→ verify
→ manifest commit last
```

Это не утверждение о конкретном distributed transaction protocol. Для первого prototype безопаснее checkpoint только между committed Decision/Training boundaries, чем пытаться serializовать arbitrary in-flight compute.

---

# 13. Compute reproducibility

Task score без compute context недостаточен для сравнения adaptive MINDRA configurations.

Минимально полезно отделять:

```text
requested resource
allocated resource
actual consumed resource
estimated usage
measured/provider-reported usage
```

и сохранять hardware/software topology.

Особенно это нужно для сравнения:

- `NoCortex` vs Cortex;
- fixed vs adaptive Executive Control;
- ReactivePolicy vs Planner;
- different training regimes.

Exact FLOP profiler/energy accounting method не выбирается.

---

# 14. Выводы для DU-27

Research landscape поддерживает решения:

1. weights-only и training-resume checkpoint — разные scopes;
2. current RNG state важнее одного initial seed для continuation;
3. deterministic claim обязан иметь software/hardware scope;
4. sharded storage/layout не должен определять logical checkpoint contract;
5. data/trainer cursor state может быть causally relevant для resume;
6. parameter tensor format не заменяет manifest/provenance layer;
7. MINDRA требует более широкого full-system scope из-за Environment/action lifecycle;
8. reproducibility лучше задавать уровнями/claims, а не boolean;
9. compute context нужен для честных research comparisons.

---

# 15. Не фиксируется

Этот pass **не выбирает**:

- PyTorch как обязательный framework;
- `torch.save`;
- Safetensors;
- Distributed Checkpoint;
- Accelerate;
- конкретный hash;
- конкретный container/package manager;
- конкретный object store;
- exact checkpoint cadence;
- exact determinism settings;
- exact compute profiler.

Все перечисленные инструменты — implementation candidates/evidence.
