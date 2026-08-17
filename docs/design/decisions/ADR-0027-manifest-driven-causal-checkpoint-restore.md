# ADR-0027 — Manifest-driven causal checkpoint с явными restore/reproducibility guarantees

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-27 — Checkpoint / Reproducibility / Compute`

---

# 1. Контекст

После `DU-26` MINDRA имеет:

```text
active AgentRevision
candidate revisions
runtime/private cognitive state
Environment state
pending action lifecycle
Experience/Data state
Training Runtime + optimizer/trainer state
```

Нужно сохранить и восстановить систему так, чтобы:

- не путать weights-only artifact с exact resume;
- causal cut Agent/Environment был согласован;
- candidate revision не активировалась случайно;
- `execution_unknown` не приводил к duplicate external effect;
- Training Resume сохранял optimizer/RNG/data-cursor state;
- reproducibility claim соответствовал реальным software/hardware ограничениям;
- checkpoint integrity можно было проверить независимо от пути хранения;
- sharding/storage/backend оставались implementation detail.

---

# 2. Вариант A — Один monolithic checkpoint file

Conceptually:

```text
save_everything("checkpoint.bin")
```

## Плюсы

- простой mental model;
- удобен для маленького prototype;
- простая копия/архивация.

## Минусы

- physical format начинает определять architecture;
- плохо масштабируется на большие/sharded artifacts;
- неудобно переиспользовать общие immutable artifacts;
- weights/runtime/trainer/environment/data lineage смешиваются;
- сложно отличить required/optional pieces;
- corruption одного файла затрагивает всё;
- delta/incremental/remote storage плохо выражаются.

**Решение:** допустим как implementation одного `CheckpointManifest`, но отклонён как canonical architecture.

---

# 3. Вариант B — Weights + config + seed

Conceptually:

```text
model weights
config
seed
```

## Плюсы

- очень компактно;
- достаточно для многих inference use cases;
- легко переносить.

## Минусы

- не восстанавливает private runtime state;
- seed не равен current RNG state;
- training resume теряет optimizer/sampler/cursor state;
- World/Memory/Workspace/Executive state пропадает;
- не решает Environment causal cut;
- не решает pending Action Commit/dispatch state;
- создаёт ложное впечатление reproducibility.

**Решение:** принимается только как явно ограниченный weights/inference checkpoint scope, отклонён как общий checkpoint contract.

---

# 4. Вариант C — Полная process/VM snapshot как определение checkpoint

Conceptually:

```text
freeze whole process/container/VM memory
```

## Плюсы

- потенциально захватывает много скрытого runtime state;
- может давать сильный same-host continuation;
- не требует ручной сериализации каждого subsystem.

## Минусы

- сильно привязано к deployment topology;
- плохо переносимо;
- external providers/Environment effects всё равно не обязательно captured;
- не даёт хорошей semantic inspection/migration;
- смешивает incidental process state с causally relevant Agent state;
- противоречит принципу logical boundaries independent of deployment.

**Решение:** может быть experimental backend/capture technique, но отклонён как canonical semantic architecture.

---

# 5. Вариант D — Manifest-driven causal checkpoint

Conceptually:

```text
explicit causal CaptureBoundary
        ↓
pin required logical state/revisions
        ↓
materialize content-identified artifacts
        ↓
verify integrity/completeness
        ↓
commit CheckpointManifest LAST
        ↓
RestoreProfile + ReproducibilityClaim
```

Дополнительно:

```text
ExperimentManifest
→ code/data/software/hardware/compute context
```

## Плюсы

- отделяет semantic checkpoint от storage format;
- допускает one-file/sharded/remote/delta backends;
- explicit required/optional artifact semantics;
- integrity/content identity;
- хорошо выражает AgentSnapshot/TrainingResume/FullSystem scopes;
- поддерживает migration;
- causal Agent/Environment alignment;
- pending external effect становится first-class;
- candidate/active revisions сохраняются раздельно;
- reproducibility guarantee можно ограничить честным scope;
- подходит Colab/local/distributed future execution.

## Минусы

- больше metadata/infrastructure;
- требуется checkpoint coordinator;
- exact capture всех component-private states требует дисциплины реализации;
- restore/migration testing сложнее простого `torch.save`;
- content-addressed/delta storage потребует GC semantics.

**Решение:** принят.

---

# 6. Accepted decision

MINDRA принимает:

> **manifest-driven checkpoint architecture с explicit causal capture boundary, content/integrity identities, scope-specific required state, explicit RestoreProfile и scoped ReproducibilityClaim.**

Канонически:

```text
AgentSnapshot
≠ Checkpoint
≠ TrainingResumeCheckpoint
≠ ExperimentManifest
```

И:

```text
same seed
≠ same RNG state
≠ guaranteed deterministic execution
```

---

# 7. Capture semantics

Принимается logical two-phase capture:

```text
prepare/pin causal cut
→ materialize/verify artifacts
→ commit final manifest last
```

Незавершённый artifact set не считается valid checkpoint.

Ранние версии могут checkpoint'ить только на заранее разрешённых committed safe boundaries.

---

# 8. Restore semantics

Restore должен иметь explicit profile:

```text
exact same-stack
compatible
portable migrated
approximate/partial
```

Exact names не frozen.

Silent downgrade exact → approximate запрещён.

Restore создаёт отдельный evidence record с actual profile.

---

# 9. External effect semantics

Если checkpoint содержит unresolved:

```text
Action Commit
→ dispatch
→ execution_unknown
```

он не является безопасной naive branch/retry point.

Full-system exact continuation требует reconciliation или environment/runtime mechanism, гарантирующий отсутствие duplicate effect.

---

# 10. Reproducibility semantics

MINDRA принимает несколько уровней claim вместо одного boolean `reproducible`.

Нужно различать:

- provenance reproducibility;
- semantic state restore;
- deterministic continuation в constrained stack;
- bitwise equivalence где реально поддерживается;
- statistical reproducibility stochastic experiments.

Более сильный claim требует более сильного evidence.

---

# 11. Compute semantics

Compute reporting является частью research reproducibility, но:

```text
ComputeManifest / infrastructure telemetry
≠
CognitiveResourceEnvelope / ExecutiveBudgetLedger
```

Raw GPU latency/VRAM/device-hours не становятся cognition без отдельной agent-visible boundary.

---

# 12. Consequences

После ADR-0027:

- checkpoint format/backend не может быть source of truth semantics;
- weights-only artifact должен объявлять ограниченный scope;
- all required artifacts имеют integrity/content identity;
- checkpoint manifest commit — causal event infrastructure;
- candidate revision restore не активирует candidate;
- training-resume checkpoint интегрирует DU-26 state;
- Environment snapshot интегрируется для full-system restore;
- seed-only reproducibility claims запрещены;
- software/hardware manifests обязательны для сильных reproducibility claims;
- migration создаёт explicit lineage;
- compute provenance становится частью reproducible research condition.

---

# 13. Не принято этим ADR

Не выбираются:

- `torch.save`/safetensors/DCP/Accelerate;
- one-file vs directory;
- SHA-256/BLAKE3;
- object storage;
- container system;
- exact reproducibility level names;
- exact deterministic settings;
- profiler/energy meter;
- retention cadence.

---

# 14. Falsification / review triggers

ADR следует пересмотреть, если:

- manifest/artifact separation не даёт практической пользы даже для multi-component Training Resume;
- exact causal capture невозможно реализовать без чрезмерного coupling;
- Environment/external-effect semantics требуют иной transaction model;
- version roadmap показывает, что более простой contract полностью покрывает нужные research claims;
- выбранный framework предоставляет более сильную, но совместимую abstraction, требующую semantic revision.
