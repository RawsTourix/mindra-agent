# V0.1-IS-13 — Configuration & Composition Root exact shape

## Статус

**Статус:** `accepted exact clarification`  
**Область:** `V0.1-IS-13 — Configuration & Composition Root`  
**Baseline:** F31 + accepted v0.1 design + accepted IS-01 … IS-12

Этот документ фиксирует implementation-level choices Configuration/Composition Root, которые нельзя оставлять Codex на самостоятельный архитектурный выбор.

Он не меняет F31, scheduler/commit semantics, cognitive contracts, Evidence Plane taxonomy или Intervention semantics. Он задаёт strict composition boundary первой runnable reference composition.

---

# 1. Documentation consistency note

Accepted `v0.1/README.md` содержит conceptual example:

```toml
profile_id = "v0.1-reference"
```

Но canonical `ProfileId` уже принят как lowercase dotted/snake semantic identity и не допускает `-`.

Для `v0.1` exact reference profile identity:

```text
ProfileId("v0_1.reference")
```

и TOML использует:

```toml
profile_id = "v0_1.reference"
```

Это supersedes только невалидный textual conceptual example. `ProfileId` contract/F31 не меняются.

---

# 2. Physical layout

Использовать существующий package `mindra.composition`.

Exact production split:

```text
src/mindra/composition/
├── __init__.py
├── profile.py
├── registry.py
├── root.py
└── runtime.py

configs/v0.1/reference.toml
```

Responsibilities:

```text
profile.py  -> immutable profile values + strict TOML parsing
registry.py -> immutable implementation registry + reference factories
root.py     -> one explicit assembly boundary
runtime.py  -> narrow composed KernelRuntime facade
```

`mindra.composition` может импортировать `mindra.runtime`, `mindra.reference`, `mindra.contracts`.

`runtime` и `reference` по-прежнему не импортируют `composition`.

Не переносить Composition Root logic в entrypoints.

---

# 3. Kernel profile schema

Exact schema token:

```text
mindra.kernel-profile/v1
```

В `profile.py` определить:

```text
KERNEL_PROFILE_SCHEMA_V1 = "mindra.kernel-profile/v1"
ProfileSettingValue = str | int | float | bool
ModuleProfile
KernelProfile
parse_kernel_profile_toml(text: str) -> KernelProfile
load_kernel_profile(path: str | Path) -> KernelProfile
```

Все value objects frozen + slots.

## 3.1. ModuleProfile

Exact fields:

```text
module_id: ModuleId
implementation_id: ImplementationId
settings: tuple[tuple[str, ProfileSettingValue], ...]
```

`settings`:

- canonical order по key;
- duplicate keys impossible/rejected;
- keys canonical lowercase snake: `[a-z][a-z0-9_]*`;
- допустимы только TOML scalar `str/int/finite float/bool`;
- nested tables, arrays, date/time values для v0.1 reject;
- `bool` остаётся отдельным scalar и не masquerade как `int` в implementation validation.

## 3.2. KernelProfile

Exact fields:

```text
schema: str
profile_id: ProfileId
modules: tuple[ModuleProfile, ...]
```

Requirements:

- schema ровно `mindra.kernel-profile/v1`;
- modules non-empty;
- ModuleId unique;
- modules canonical order по `module_id.value` независимо от TOML order.

ImplementationId может повторяться в общем schema; concrete factory сама определяет допустимые semantic ModuleId. Reference profile использует четыре разные implementations.

---

# 4. Strict TOML surface

Top-level разрешены ровно:

```text
schema
profile_id
modules
```

Каждый `[[modules]]` разрешает ровно:

```text
module_id
implementation
settings   # optional table, default empty
```

Unknown top-level/module keys -> `ConfigurationError`.

Wrong type/missing required key/malformed semantic id/malformed TOML -> `ConfigurationError`.

`load_kernel_profile()` читает локальный filesystem через stdlib и оборачивает TOML/IO/config failures в `ConfigurationError` с diagnostic context.

Parser не знает reference factory settings semantics кроме generic scalar shape. Implementation-specific unknown/missing settings проверяет factory descriptor.

---

# 5. Exact reference TOML

Создать `configs/v0.1/reference.toml`:

```toml
schema = "mindra.kernel-profile/v1"
profile_id = "v0_1.reference"

[[modules]]
module_id = "synthetic.source"
implementation = "reference.synthetic_source.v1"

[modules.settings]
value = 2

[[modules]]
module_id = "synthetic.double"
implementation = "reference.synthetic_double.v1"

[[modules]]
module_id = "synthetic.triple"
implementation = "reference.synthetic_triple.v1"

[[modules]]
module_id = "synthetic.join"
implementation = "reference.synthetic_join.v1"
```

Order файла не является execution semantics; `KernelProfile` canonicalize modules.

---

# 6. Resolved factory records

В `registry.py` определить composition-only immutable records.

## 6.1. ResolvedStateField

```text
ResolvedStateField
├── spec: StateFieldSpec[object]
└── initial_availability: Unknown | Unavailable
```

Public initial `Available` через factory запрещён в IS-13: reference values должны появляться normal module proposal/commit path.

## 6.2. InitialPrivateState

```text
InitialPrivateState
└── value: object
```

Wrapper отличает отсутствие private slot от legitimate private payload `None` в будущей compatible implementation.

Reference modules stateless, поэтому используют `None` как отсутствие `InitialPrivateState` wrapper.

## 6.3. ResolvedModule

Exact fields:

```text
module: CognitiveModule
state_fields: tuple[ResolvedStateField, ...]
resolved_settings: tuple[tuple[str, ProfileSettingValue], ...]
initial_private_state: InitialPrivateState | None
```

Requirements:

- state_fields canonical по `spec.key.path.dotted`;
- каждый field owner == `module.descriptor.module_id`;
- set state field keys == set `descriptor.writes`;
- stateless module -> `initial_private_state is None`;
- stateful module -> explicit `InitialPrivateState` обязателен;
- resolved_settings canonical и уже strict-validated implementation factory.

---

# 7. Implementation factory descriptor

Exact composition API:

```text
ModuleFactory = Callable[[ModuleProfile], ResolvedModule]

ImplementationFactoryDescriptor
├── implementation_id: ImplementationId
└── factory: ModuleFactory
```

Descriptor frozen + slots; factory callable required.

Factory получает только immutable `ModuleProfile` и возвращает полностью resolved module assembly metadata.

Factory не получает CompositionRoot/runtime/store/registry reference.

---

# 8. ImplementationRegistry

Exact public surface:

```text
ImplementationRegistry(
    descriptors: tuple[ImplementationFactoryDescriptor, ...]
)

resolve(implementation_id: ImplementationId, /) -> ImplementationFactoryDescriptor
__len__() -> int
```

Semantics:

- immutable mapping после construction;
- duplicate ImplementationId -> `DuplicateIdentityError`;
- unknown implementation -> `ConfigurationError`;
- нет `register/add/remove/replace` public mutation;
- нет import-time decorator registration;
- нет plugin discovery/entry points.

---

# 9. build_reference_registry()

`build_reference_registry()` explicit создаёт registry из четырёх factories:

```text
reference.synthetic_source.v1
reference.synthetic_double.v1
reference.synthetic_triple.v1
reference.synthetic_join.v1
```

Reference factory validation:

## source

Exact ModuleId:

```text
synthetic.source
```

Exact settings:

```text
{"value": int}
```

- key `value` обязателен;
- extra key reject;
- `type(value) is int`, bool reject;
- создаёт `SyntheticSourceModule(value=value)`.

## double/triple/join

- exact semantic ModuleId из IS-12;
- settings обязаны быть пустыми;
- extra/unknown settings reject;
- создают соответствующий no-arg module.

Для каждого output field factory создаёт:

```text
StateFieldSpec(
    key=<own exact IS-12 StateKey>,
    owner=<own ModuleId>,
    value_contract=ValueContract(int),
)
```

и:

```text
initial_availability = Unknown()
```

Все четыре reference modules:

```text
initial_private_state = None
```

---

# 10. Composition metadata

В `root.py` или `runtime.py` определить frozen:

```text
CompositionMetadata
├── profile_id: ProfileId
├── composition_revision: CompositionRevision
├── schema_revision: SchemaRevision
├── agent_revision_id: AgentRevisionId
├── fingerprint: str
└── descriptors: tuple[ModuleDescriptor, ...]
```

Requirements:

- fingerprint lowercase 64-char SHA-256;
- descriptors canonical по ModuleId;
- descriptor set соответствует active resolved modules.

---

# 11. Composition fingerprint

Composition fingerprint — content evidence, не causal identity.

Exact canonical normalized object:

```text
{
  "profile_schema": "mindra.kernel-profile/v1",
  "state_schema_revision": 0,
  "modules": [
    {
      "module_id": <str>,
      "implementation_id": <str>,
      "implementation_revision": <str>,
      "settings": {<canonical resolved settings>}
    },
    ... canonical ModuleId order ...
  ]
}
```

Serialization:

```text
json.dumps(
    normalized,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=True,
)
```

Hash:

```text
sha256(serialized.encode("utf-8")).hexdigest()
```

Fingerprint включает:

- profile schema token;
- semantic ModuleId;
- ImplementationId;
- ImplementationRevision;
- resolved behavior-relevant settings;
- SchemaRevision.

Fingerprint НЕ включает:

- ProfileId;
- Run/Session/Episode/Decision/Cycle IDs;
- AgentRevisionId;
- Lineage/Branch IDs;
- ExecutionPlanId;
- physical timestamp;
- TOML ordering/formatting/comments.

Изменение source value меняет fingerprint. Перестановка module tables — нет.

---

# 12. CompositionRoot public API

Exact public surface:

```text
CompositionRoot(*, registry: ImplementationRegistry, id_factory: IdFactory)

build(profile: KernelProfile, /) -> KernelRuntime
```

No implicit global registry/config.

`build()` — единственная production assembly path v0.1.

Entry point в IS-15 позже вызывает parser + registry + root; он не собирает modules вручную.

---

# 13. Assembly order

`CompositionRoot.build()` выполняет fail-closed assembly в таком порядке:

1. validate `KernelProfile`;
2. canonical profile module order;
3. resolve каждый implementation через registry;
4. factory strict-validate module id/settings;
5. validate returned `ResolvedModule` against profile + descriptor;
6. собрать canonical descriptors/state fields/private initial values;
7. build `StateSchema(SchemaRevision.initial(), ...)`;
8. compute composition fingerprint;
9. allocate root causal identities;
10. build schema-complete initial `CognitiveState`;
11. build `PrivateStateStore`;
12. compile `ExecutionPlan` с `CompositionRevision.initial()` и `ExecutionPlanRevision.initial()`;
13. construct `CommitCoordinator`;
14. construct `SequentialWaveExecutor`;
15. construct `InMemoryEvidenceRecorder`;
16. construct `CognitiveScheduler`;
17. construct immutable `CompositionMetadata` + `KernelRuntime`;
18. только после полного successful assembly записать `composition_resolved`;
19. затем записать `plan_compiled`;
20. return `KernelRuntime`.

Если любой step до return падает, частично собранный runtime наружу не публикуется.

Если final evidence record падает, `build()` тоже fail closed и runtime не возвращается.

---

# 14. Root identity ownership

Один shared injected `IdFactory` является единственным source causal UUID identities всей собранной runtime composition.

Exact root allocation order v0.1:

```text
RunId
AgentSessionId
EpisodeId
DecisionWindowId
LineageId
BranchId
AgentRevisionId
```

Затем `ExecutionPlanCompiler` из того же factory создаёт `ExecutionPlanId`.

Позже:

- `KernelRuntime.run_cycle()` создаёт `CognitiveCycleId`;
- Scheduler создаёт Wave/WaveAttempt/ModuleAttempt IDs;
- CommitCoordinator создаёт CommitId.

Modules IDs не создают.

`AgentRevisionId` не выводится из fingerprint.

---

# 15. Temporal context v0.1

Environment transitions отсутствуют, но `LogicalTime` уже требует hierarchy:

```text
EpisodeId -> DecisionWindowId -> CognitiveCycleId -> WaveId
```

Поэтому один composed `KernelRuntime` v0.1 pin'ит на весь lifetime:

```text
run_id
agent_session_id
episode_id
decision_window_id
```

Это fixed reference lifecycle scopes, а не Environment transition API.

Composition/initial-state logical time:

```text
LogicalTime(
    run_id=...,
    agent_session_id=...,
    episode_id=...,
    decision_window_id=...,
    cognitive_cycle_id=None,
    wave_id=None,
)
```

Каждый `KernelRuntime.run_cycle()` создаёт новый `CognitiveCycleId`, сохраняя те же outer IDs.

Несколько cycles в одном fixed DecisionWindow допустимы и являются v0.1 reference lifecycle semantics.

Нет API advance episode/decision window в IS-13.

---

# 16. Initial CognitiveState

Initial state:

```text
SchemaRevision = 0
StateRevision = 0
parent_state_revision = None
CompositionRevision = 0
```

`lineage_id`, `branch_id`, `agent_revision_id` создаёт root IdFactory.

Entries schema-complete: каждый `ResolvedStateField` присутствует.

Reference profile:

```text
synthetic.source.value   -> Unknown()
synthetic.double.value   -> Unknown()
synthetic.triple.value   -> Unknown()
synthetic.join.value     -> Unknown()
```

`missing` не используется.

Initial entry provenance не masquerade как module write.

Exact runtime boundary:

```text
RuntimeBoundaryId("composition.initial_state")
```

Initial `StateProvenance`:

```text
producer = RuntimeBoundaryId("composition.initial_state")
implementation_id = None
base_state_revision = StateRevision.initial()
module_attempt_id = None
logical_time = root logical time
source_refs = ()
parent_refs = ()
intervention_refs = ()
```

Source first value появляется только normal scheduler proposal/commit.

---

# 17. Initial private state

`PrivateStateStore` строится из exact active descriptors.

Initial values mapping состоит только из stateful `ResolvedModule.initial_private_state.value`.

Reference profile полностью stateless:

```text
initial_values = {}
```

Не создавать fake private slots для stateless modules.

---

# 18. KernelRuntime ownership и public surface

`KernelRuntime` физически находится в `mindra.composition.runtime`, потому что это composed facade, знающий runtime objects и active composition metadata. `mindra.runtime` не импортирует его.

Exact public surface минимум:

```text
KernelRuntime
├── profile: KernelProfile                 # read-only property
├── composition: CompositionMetadata       # read-only property
├── plan: ExecutionPlan                    # read-only property
├── state: CognitiveState                  # current committed public state
├── evidence_snapshot() -> tuple[TraceEventEnvelope, ...]
└── run_cycle() -> CycleExecutionResult
```

Internal ownership:

```text
PrivateStateStore
CognitiveScheduler
InMemoryEvidenceRecorder
IdFactory
fixed root LogicalTime
```

Не expose private store/CommitCoordinator/module registry как Service Locator API.

---

# 19. KernelRuntime.run_cycle()

Exact no-argument facade:

```text
run_cycle() -> CycleExecutionResult
```

Pipeline:

1. allocate new `CognitiveCycleId` через same IdFactory;
2. build cycle `LogicalTime` из fixed run/session/episode/decision IDs;
3. call existing `CognitiveScheduler.run_cycle(current_state=self._state, cycle_time=cycle_time)`;
4. assign `self._state = result.state` **и при success, и при FAILED result**;
5. return exact `CycleExecutionResult`.

Почему state обновляется при FAILED result: earlier successful waves текущего cycle уже могли быть committed и не rollback'ятся.

Runtime не превращает failed `CycleExecutionResult` в новую exception taxonomy.

Infrastructure-fatal exception Scheduler/Evidence продолжает propagate.

No retry/rebase/degradation.

---

# 20. Composition/plan Evidence

IS-13 становится producer только для:

```text
composition_resolved
plan_compiled
```

Scheduler events остаются responsibility IS-11.

Оба root events:

- `TraceEventEnvelope.logical_time = root LogicalTime`;
- `physical_timestamp_ns = None`;
- записываются только после полного successful assembly непосредственно перед return;
- insertion order exact: `composition_resolved` затем `plan_compiled`.

## CompositionResolvedEvent

Payload зеркалит:

```text
profile_id
CompositionRevision.initial()
SchemaRevision.initial()
agent_revision_id
composition fingerprint
ResolvedModuleTrace для каждого descriptor canonical ModuleId order
```

## PlanCompiledEvent

Payload зеркалит actual compiled `ExecutionPlan`:

```text
plan_id
plan revision
composition revision
schema revision
phase
plan fingerprint.value
canonical dependencies -> PlanDependencyTrace
canonical waves -> PlanWaveTrace
```

Не emit `intervention_applied`.

---

# 21. Public exports

`mindra.composition.__init__` экспортирует минимум:

```text
KERNEL_PROFILE_SCHEMA_V1
ModuleProfile
KernelProfile
parse_kernel_profile_toml
load_kernel_profile
ResolvedStateField
InitialPrivateState
ResolvedModule
ImplementationFactoryDescriptor
ImplementationRegistry
build_reference_registry
CompositionMetadata
CompositionRoot
KernelRuntime
```

Не экспортировать mutable backing mappings/internal reference factory functions.

---

# 22. Required tests

Минимум:

```text
tests/unit/test_kernel_profile.py
tests/unit/test_implementation_registry.py
tests/integration/test_composition_root.py
tests/integration/test_kernel_runtime_reference.py
tests/architecture/test_composition_boundary.py
```

Required coverage:

## profile

- exact schema token;
- exact reference ProfileId `v0_1.reference`;
- unknown top-level/module keys reject;
- malformed/missing keys reject;
- duplicate ModuleId reject;
- module order canonicalized;
- settings keys canonicalized;
- nested/array/date-time settings reject;
- malformed TOML -> ConfigurationError;
- source bool remains distinguishable from int.

## registry/factories

- registry immutable;
- duplicate implementation reject;
- unknown implementation reject;
- no mutation API;
- source exact module id/settings;
- source unknown/missing/bool settings reject;
- other reference factories require empty settings;
- resolved fields exact int contracts + Unknown;
- resolved descriptor/profile identities match.

## fingerprint

- lowercase SHA-256;
- same resolved composition + different TOML module order -> same fingerprint;
- source value change -> different fingerprint;
- ProfileId-only change -> same fingerprint;
- generated UUID identities do not affect fingerprint.

## root initial state

- exact 4-field schema;
- all fields present Unknown, not missing;
- revision 0 / parent None / composition 0;
- RuntimeBoundaryId initial provenance;
- distinct typed root identities;
- AgentRevisionId is generated identity, not fingerprint-derived;
- stateless reference private store has no slots semantically (snapshot returns Unavailable through scheduler/reference execution path).

## plan/runtime

- compiled exact waves source -> {double,triple} -> join;
- root evidence starts `composition_resolved`, `plan_compiled`;
- root events exact payload copies and physical timestamp None;
- first `run_cycle()` source=2 yields double=4, triple=6, join=10;
- successful first cycle public state revision == 3;
- second cycle uses distinct CognitiveCycleId, same run/session/episode/decision, final revision == 6;
- runtime updates current state to result.state;
- test failed later-wave fixture only если возможно без production fixture leakage: runtime state preserves earlier commits on FAILED cycle;
- evidence snapshot includes root events then scheduler events.

## architecture

- entrypoints не собирает composition вручную в IS-13;
- runtime/reference не импортируют composition;
- reference/runtime independence remains;
- composition has no global mutable registry;
- cognitive modules do not receive KernelRuntime/registry/config.

---

# 23. VerificationObligations

Expected level после accepted IS-13:

```text
V01-007 — composition integration
V01-012 — closed architecture/composition semantics
V01-013 — substantial
```

`V01-013` fully closed только после CLI/deterministic end-to-end smoke (`IS-15`) и final acceptance hardening.

---

# 24. Forbidden scope

Не реализовывать в IS-13:

- InterventionGateway (`IS-14`);
- CLI/argparse commands (`IS-15`);
- `python -m mindra` smoke behavior beyond existing bootstrap;
- Environment observation/action/outcome transitions;
- API advance Episode/DecisionWindow;
- retries/recompute/rebase/degradation;
- O1/O2/O3 evidence;
- network/filesystem telemetry exporter;
- plugin discovery/entry points;
- import-time registration;
- dynamic module loading by Python dotted path;
- global mutable registry;
- Service Locator;
- mutable module settings;
- new cognitive contracts/identities/revision types;
- production stateful/failure test modules;
- IS-14/IS-15 work ahead of sequence.

Не менять F31/accepted ADR/scheduler/commit semantics.

---

# 25. Verification

После implementation:

```text
FAST + ARCH
```

с targeted tests текущего step, затем полный:

```text
FULL-C0
```

и:

```text
git diff --check
```

Post-push обязателен independent GitHub Actions evidence exact implementation commit до acceptance.
