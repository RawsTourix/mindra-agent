# V0.1-IS-07 — Exact Execution Plan clarification

## Статус

**Статус:** `accepted`  
**Область:** только `V0.1-IS-07 — Execution Plan Compiler`  
**Baseline:** accepted `v0.1/README.md` + `implementation-sequence.md` + `F31`

Этот документ устраняет implementation-level неоднозначности перед реализацией `IS-07`. Он не меняет `F31`, `DU-02`, `DU-03`, `DU-05` или смысл accepted `v0.1`; он фиксирует exact Python-facing shape immutable execution plan и compiler boundary первой версии.

При конфликте приоритет имеют `F31` и canonical design; в таком случае implementation останавливается с blocker report.

---

# 1. Граница шага

`IS-07` только **компилирует и валидирует** execution DAG из уже существующих `ModuleDescriptor` и `StateSchema`.

Он не:

- выполняет modules;
- создаёт `ModuleComputeRequest`;
- читает `CognitiveState`;
- изменяет public/private state;
- commit'ит proposals;
- создаёт `PrivateStateStore`;
- реализует scheduler/executor;
- знает concrete module objects;
- знает Composition Root/registry/config.

Compiler работает только с immutable contracts и metadata, переданными явно.

---

# 2. Exact runtime types

Physical owner: `mindra.runtime.planning` или эквивалентный file split внутри `mindra.runtime`.

Минимальный набор:

```text
PlanFingerprint
ExecutionDependency
ExecutionWave
ExecutionPlan
ExecutionPlanCompiler
```

## 2.1. `PlanFingerprint`

Frozen value object:

```text
PlanFingerprint
└── value: str
```

`value` — lowercase hex SHA-256 (`64` hex symbols) canonical execution-plan semantics.

Fingerprint не является causal identity и не заменяет `ExecutionPlanId`/`ExecutionPlanRevision`.

## 2.2. `ExecutionDependency`

Frozen value object:

```text
ExecutionDependency
├── producer: ModuleId
├── consumer: ModuleId
└── path: StatePath
```

Dependency означает explicit same-cycle data edge, выведенный из `CURRENT_CYCLE` read.

## 2.3. `ExecutionWave`

Frozen value object:

```text
ExecutionWave
├── index: int
└── module_ids: tuple[ModuleId, ...]
```

Semantics:

- `index >= 0`;
- `module_ids` непустой;
- внутри wave IDs уникальны;
- `module_ids` всегда отсортированы по canonical `ModuleId.value`;
- wave не содержит `WaveId`: runtime causal `WaveId` относится к будущему execution attempt, а не к static compiled plan.

## 2.4. `ExecutionPlan`

Frozen value object минимум:

```text
ExecutionPlan
├── plan_id: ExecutionPlanId
├── revision: ExecutionPlanRevision
├── fingerprint: PlanFingerprint
├── composition_revision: CompositionRevision
├── schema_revision: SchemaRevision
├── phase: ExecutionPhase
├── descriptors: tuple[ModuleDescriptor, ...]
├── dependencies: tuple[ExecutionDependency, ...]
└── waves: tuple[ExecutionWave, ...]
```

Semantics:

- `phase` в `v0.1` всегда `COGNITIVE_CYCLE`;
- descriptors canonical-sorted по `module_id.value` независимо от input order;
- dependencies canonical-sorted по `(producer.value, consumer.value, path.dotted)`;
- waves ordered by `index` начиная с `0` без gaps;
- каждый active descriptor встречается ровно в одной wave;
- plan не хранит concrete `CognitiveModule` objects, registry, config или Composition Root.

Пустой active descriptor set разрешён только если compiler может построить корректный empty plan; в таком случае `waves == ()` и `dependencies == ()`. Это deterministic structural result, а не runtime execution.

---

# 3. Compiler boundary

`ExecutionPlanCompiler` stateless относительно compilation history.

Он получает `IdFactory` явно при construction и не использует global UUID API.

Conceptual API:

```text
ExecutionPlanCompiler(id_factory)

compile(
    descriptors,
    schema,
    *,
    composition_revision,
    plan_revision,
) -> ExecutionPlan
```

Exact typing:

```text
descriptors: tuple[ModuleDescriptor, ...]
schema: StateSchema
composition_revision: CompositionRevision
plan_revision: ExecutionPlanRevision
```

Compiler не хранит hidden mutable counter/revision. `ExecutionPlanRevision` и `CompositionRevision` передаются вызывающей стороной явно.

`ExecutionPlanId` создаётся через injected `IdFactory` **только после успешной полной validation/decomposition/fingerprint construction**. Failed compilation не должна расходовать causal plan identity из deterministic ID sequence.

---

# 4. Compile-time validation

Validation fail closed и выполняется до создания успешного plan.

Минимум:

## 4.1. Active module identity

- каждый element является `ModuleDescriptor`;
- `ModuleId` уникален;
- duplicate semantic module identity → `DuplicateIdentityError` или более specific existing typed kernel error, являющийся fail-closed result.

## 4.2. Schema existence

Каждый declared read/write `StatePath` обязан существовать в переданном `StateSchema`.

Structural missing contract path → `ExecutionPlanError`.

## 4.3. Write authority

Для каждого declared write:

```text
StateFieldSpec.owner == descriptor.module_id
```

Иначе → `ExecutionPlanError`/`UnauthorizedWriteError` согласно существующей typed taxonomy.

Compiler проверяет **descriptor write authority**, но не runtime `StateUpdateProposal`: proposal validation остаётся `CommitCoordinator` (`IS-09`).

## 4.4. Writer uniqueness

Один `StatePath` не может иметь более одного active writer descriptor.

Ambiguous/duplicate writer → `ExecutionPlanError`.

## 4.5. Phase

Каждый active descriptor обязан участвовать в `ExecutionPhase.COGNITIVE_CYCLE`.

Unsupported/missing applicable phase → `ExecutionPlanError`.

## 4.6. `CURRENT_CYCLE`

Для каждого `ReadSpec` с `FreshnessMode.CURRENT_CYCLE`:

- если active writer этого path существует, создаётся edge `writer → consumer`;
- writer обязан declared-write этот exact path и быть semantic owner schema field;
- если `read.required is True`, active producer обязателен;
- required `CURRENT_CYCLE` без active producer → `ExecutionPlanError`;
- optional `CURRENT_CYCLE` без active producer допустим и не создаёт edge;
- `CURRENT_CYCLE` self-dependency создаёт self-edge и поэтому является cycle/error, а не silently превращается в `ANY_COMMITTED`.

## 4.7. `ANY_COMMITTED`

`FreshnessMode.ANY_COMMITTED` не создаёт same-cycle DAG edge автоматически, даже если active writer этого field существует.

Read/write overlap одного module допустим при `ANY_COMMITTED`.

---

# 5. DAG и deterministic wave decomposition

DAG строится только из explicit `CURRENT_CYCLE` dependencies текущего plan segment.

Используется deterministic topological wave decomposition:

1. вычислить indegree всех active modules;
2. ready set = все nodes с indegree `0`;
3. одна wave содержит **весь текущий ready set**;
4. IDs внутри wave сортируются по `ModuleId.value`;
5. удалить edges из всей wave;
6. повторить;
7. если после исчерпания ready sets остаются nodes → `DependencyCycleError`.

Tie-break не создаёт dependency semantics. Он определяет только canonical representation/будущий deterministic physical order.

Input order descriptors не должен влиять на:

- dependencies;
- wave partition;
- order module IDs внутри wave;
- fingerprint.

---

# 6. Fingerprint semantics

Fingerprint строится stdlib `hashlib.sha256` над deterministic canonical byte representation.

Canonical representation должна включать execution semantics минимум:

- `phase`;
- canonical sorted descriptors:
  - `module_id`;
  - `implementation_id`;
  - `implementation_revision.value`;
  - reads: path, `required`, allowed availability kinds, freshness;
  - writes paths;
  - statefulness/determinism traits;
  - наличие private-state descriptor;
  - phases;
- canonical dependency edges;
- canonical waves.

Не включать:

- `ExecutionPlanId`;
- `ExecutionPlanRevision`;
- `CompositionRevision`;
- wall-clock;
- Python object addresses;
- input iteration order;
- concrete contract object `repr()` с нестабильными адресами.

Причина: fingerprint описывает **структурную execution semantics**, тогда как causal/revision metadata хранится отдельными typed fields plan.

Одинаковая семантическая plan structure при одинаковых descriptors должна давать одинаковый fingerprint независимо от random/deterministic `ExecutionPlanId` и input order.

Изменение implementation identity/revision, read/write/freshness/trait/dependency/wave semantics обязано менять fingerprint.

Schema revision сама по себе не включается в fingerprint: plan отдельно хранит `schema_revision`; fingerprint отражает использованную структурную contract semantics, а не произвольное увеличение revision counter.

---

# 7. Error semantics

Использовать существующую typed taxonomy:

- `ExecutionPlanError` — невозможная/несовместимая plan configuration;
- `DependencyCycleError` — cycle/self-cycle;
- `DuplicateIdentityError` — duplicate active `ModuleId`, если существующий тип подходит exact case;
- `UnauthorizedWriteError` — только если его existing constructor/semantics естественно подходят compile-time descriptor authority violation; иначе использовать `ExecutionPlanError`, не меняя чужую taxonomy ради шага.

Никаких generic `success=False`.

Failed compile:

```text
no ExecutionPlan
no ExecutionPlanId allocation
no state mutation
```

---

# 8. Verification focus

Помимо tests из `implementation-sequence.md`, обязательно проверить:

- linear chain → последовательные waves;
- diamond → ожидаемый fan-out/fan-in;
- independent modules → одна wave с canonical `ModuleId` order;
- permutation input descriptors → идентичные dependencies/waves/fingerprint;
- duplicate `ModuleId` reject;
- read path отсутствует в schema → reject;
- write path отсутствует в schema → reject;
- writer != schema owner → reject;
- duplicate/ambiguous writer → reject;
- required `CURRENT_CYCLE` without producer → reject;
- optional `CURRENT_CYCLE` without producer → compile succeeds without edge;
- `ANY_COMMITTED` не создаёт edge;
- self `CURRENT_CYCLE` dependency → cycle reject;
- multi-node cycle → `DependencyCycleError`;
- empty descriptor set → deterministic empty plan;
- failed compile не расходует `ExecutionPlanId` у `DeterministicIdFactory`;
- same semantic plan with another `ExecutionPlanId`/plan revision/composition revision → same fingerprint;
- implementation/read/write/freshness semantic change → different fingerprint;
- compiled plan immutable;
- plan не содержит concrete module objects/registry/config.

`V01-007` закрывается этим шагом только после прохождения required unit/property/contract verification.

---

# 9. Forbidden scope

Не реализовывать:

- module execution;
- `PrivateStateStore`;
- `CommitCoordinator`;
- `WaveExecutor`;
- Scheduler;
- evidence events/recorder;
- Composition Root/registry/config parsing;
- runtime `WaveId` allocation;
- state mutation;
- proposal validation/commit;
- parallelism/async/thread/process execution.
