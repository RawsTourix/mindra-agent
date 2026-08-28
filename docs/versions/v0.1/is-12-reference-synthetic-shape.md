# V0.1-IS-12 — Reference synthetic modules exact shape

## Статус

**Статус:** `accepted exact clarification`  
**Область:** `V0.1-IS-12 — Reference synthetic modules`  
**Baseline:** F31 + accepted v0.1 design + `IS-06` module contracts + `IS-07` planner + accepted `IS-11` scheduler semantics

Этот документ фиксирует implementation-level choices reference synthetic graph, которые нельзя оставлять Codex на самостоятельный архитектурный выбор.

Он не меняет F31, execution semantics, ownership, scheduler/commit behavior, configuration model или Composition Root. Он только задаёт exact contracts четырёх deterministic reference modules.

---

# 1. Purpose и boundary

`IS-12` создаёт production reference implementations, пригодные для доказательства contracts/planner/scheduler в следующем composition step.

Reference graph:

```text
synthetic.source
       ↓
 ┌─────┴─────┐
 ↓           ↓
synthetic.double
synthetic.triple
 └─────┬─────┘
       ↓
synthetic.join
```

Expected compiled waves:

```text
Wave 0: synthetic.source
Wave 1: synthetic.double | synthetic.triple
Wave 2: synthetic.join
```

Configured source value `2` означает:

```text
source = 2
double = 4
triple = 6
join = 10
```

`IS-12` не создаёт runnable profile/Composition Root. Полная runnable reference composition появляется в `IS-13`.

---

# 2. Physical layout

Использовать существующий package `mindra.reference`.

Exact production split:

```text
src/mindra/reference/
├── __init__.py
└── synthetic.py
```

Не создавать дополнительные production subpackages/config/registry/schema-builder layers без отдельной необходимости.

`mindra.reference.synthetic` зависит только от stdlib + `mindra.contracts`.

Запрещены production imports:

```text
mindra.runtime
mindra.composition
mindra.entrypoints
```

Existing Import Linter `reference-layers` и `runtime-reference-independence` остаются blocking.

---

# 3. Canonical semantic identities

Exact ModuleIds:

```text
SyntheticSourceModule  -> ModuleId("synthetic.source")
SyntheticDoubleModule  -> ModuleId("synthetic.double")
SyntheticTripleModule  -> ModuleId("synthetic.triple")
SyntheticJoinModule    -> ModuleId("synthetic.join")
```

Exact ImplementationIds:

```text
SyntheticSourceModule  -> ImplementationId("reference.synthetic_source.v1")
SyntheticDoubleModule  -> ImplementationId("reference.synthetic_double.v1")
SyntheticTripleModule  -> ImplementationId("reference.synthetic_triple.v1")
SyntheticJoinModule    -> ImplementationId("reference.synthetic_join.v1")
```

Exact `ImplementationRevision` всех четырёх implementations:

```text
ImplementationRevision("v1")
```

Не вводить новые identity types.

---

# 4. Canonical StateKeys

В `mindra.reference.synthetic` определить и public-export следующие immutable typed keys:

```text
SYNTHETIC_SOURCE_VALUE_KEY = StateKey[int](
    StatePath.from_dotted("synthetic.source.value")
)

SYNTHETIC_DOUBLE_VALUE_KEY = StateKey[int](
    StatePath.from_dotted("synthetic.double.value")
)

SYNTHETIC_TRIPLE_VALUE_KEY = StateKey[int](
    StatePath.from_dotted("synthetic.triple.value")
)

SYNTHETIC_JOIN_VALUE_KEY = StateKey[int](
    StatePath.from_dotted("synthetic.join.value")
)
```

Semantic owner каждого key — module с соответствующим ModuleId.

`IS-12` НЕ создаёт production `StateSchema`/`StateFieldSpec` registry. `IS-13 CompositionRoot` позднее соберёт schema из active composition.

Tests `IS-12` могут построить test-only `StateSchema` для planner/compute verification.

---

# 5. Common descriptor semantics

Все четыре modules:

```text
ExecutionPhase.COGNITIVE_CYCLE only
ModuleStatefulness.STATELESS
DeterminismMode.DETERMINISTIC
private_state = None
```

Exact traits:

```text
ExecutionTraits(
    statefulness=ModuleStatefulness.STATELESS,
    determinism=DeterminismMode.DETERMINISTIC,
)
```

Каждый class предоставляет immutable `descriptor: ModuleDescriptor` как обычный `CognitiveModule` contract.

Descriptor не зависит от source constructor value. Source value является behavior-relevant resolved setting будущей composition fingerprint, но не новым ModuleDescriptor field.

---

# 6. Exact descriptors

## 6.1 SyntheticSourceModule

```text
module_id = synthetic.source
implementation_id = reference.synthetic_source.v1
implementation_revision = v1
reads = ()
writes = (SYNTHETIC_SOURCE_VALUE_KEY,)
private_state = None
phases = {COGNITIVE_CYCLE}
traits = STATELESS + DETERMINISTIC
```

## 6.2 SyntheticDoubleModule

Reads ровно source value:

```text
ReadSpec(
    key=SYNTHETIC_SOURCE_VALUE_KEY,
    required=True,
    allowed_availability=frozenset({Available}),
    freshness=FreshnessMode.CURRENT_CYCLE,
)
```

Descriptor:

```text
reads = (source ReadSpec,)
writes = (SYNTHETIC_DOUBLE_VALUE_KEY,)
```

## 6.3 SyntheticTripleModule

Reads ровно source value с теми же semantics:

```text
required=True
allowed_availability={Available}
freshness=CURRENT_CYCLE
```

Descriptor:

```text
reads = (source ReadSpec,)
writes = (SYNTHETIC_TRIPLE_VALUE_KEY,)
```

## 6.4 SyntheticJoinModule

Exact read order:

```text
1. SYNTHETIC_DOUBLE_VALUE_KEY
2. SYNTHETIC_TRIPLE_VALUE_KEY
```

Для обоих reads:

```text
required=True
allowed_availability=frozenset({Available})
freshness=FreshnessMode.CURRENT_CYCLE
```

Descriptor:

```text
reads = (double ReadSpec, triple ReadSpec)
writes = (SYNTHETIC_JOIN_VALUE_KEY,)
```

Эти dependencies обязаны приводить existing `ExecutionPlanCompiler` к exact waves из раздела 1 независимо от tuple registration/input order.

---

# 7. Class construction и immutability

Все четыре implementations должны быть immutable-by-interface; предпочтительно frozen+slots dataclasses или эквивалентная форма без mutable behavior state.

Exact constructors:

```text
SyntheticSourceModule(*, value: int)
SyntheticDoubleModule()
SyntheticTripleModule()
SyntheticJoinModule()
```

`SyntheticSourceModule.value` — единственная production setting текущего шага.

Validation source value:

```text
type(value) is int
```

`bool` не принимается как source setting, несмотря на Python subtype relation `bool <: int`.

Диапазон не ограничивается: Python `int` используется без artificial v0.1 bounds.

Double/triple/join не имеют settings.

Не вводить generic settings mapping, TOML object, profile object или mutable config reference в `IS-12`.

---

# 8. Compute purity и request boundary

Все modules реализуют exact synchronous contract:

```text
def compute(self, request: ModuleComputeRequest) -> ModuleComputeResult
```

Production reference module:

- не читает global state/config;
- не импортирует runtime;
- не получает registry/services;
- не мутирует request/projection;
- не хранит cross-attempt mutable state;
- не создаёт IDs;
- не commit'ит;
- не пишет Evidence;
- не использует wall clock/RNG/filesystem/network.

Все modules stateless. Valid Scheduler request поэтому содержит `Unavailable` private state.

Reference implementation может fail closed проверить, что stateless request не содержит `PrivateStateSnapshot`; такая проверка должна использовать только contracts и не добавлять новую runtime authority.

---

# 9. Exact computation

## Source

Не читает `StateProjection`.

```text
output = self.value
```

## Double

Читает только `SYNTHETIC_SOURCE_VALUE_KEY` через `request.state.read()`.

```text
output = source * 2
```

## Triple

Читает только `SYNTHETIC_SOURCE_VALUE_KEY`.

```text
output = source * 3
```

## Join

Читает сначала double, затем triple.

```text
output = double + triple
```

`StateProjection` уже fail closed enforce'ит declared availability/freshness. Reference code не должен обходить projection через underlying mappings.

После successful `read()` implementation может дополнительно проверить runtime payload `type(value) is int` и fail closed через existing contracts-level `ModuleExecutionError`/эквивалентный existing typed diagnostic, если malformed test-only projection нарушает expected int payload.

Не вводить новую error taxonomy.

---

# 10. Exact staged result construction

Каждый successful compute возвращает normal `ModuleComputeResult`:

```text
ModuleComputeResult(
    state_update=StateUpdateProposal(...),
    private_state_update=None,
)
```

`StateUpdateProposal`:

```text
base_state_revision = request.context.base_state_revision
producer = self.descriptor.module_id
module_attempt_id = request.context.module_attempt_id
writes = (single StateWrite,)
```

Single `StateWrite`:

```text
key = module own canonical output key
availability = Available(computed_int)
provenance = StateProvenance(...)
```

Exact provenance:

```text
StateProvenance(
    producer=self.descriptor.module_id,
    implementation_id=self.descriptor.implementation_id,
    base_state_revision=request.context.base_state_revision,
    module_attempt_id=request.context.module_attempt_id,
    logical_time=request.context.logical_time,
)
```

Default empty tuples сохраняются:

```text
source_refs = ()
parent_refs = ()
intervention_refs = ()
```

Не создавать `CommitId`, StateRevision transition или custom source-reference identity внутри module.

Commit authority остаётся у existing `CommitCoordinator`.

---

# 11. Public exports

`mindra.reference.__init__` экспортирует минимум:

```text
SyntheticSourceModule
SyntheticDoubleModule
SyntheticTripleModule
SyntheticJoinModule

SYNTHETIC_SOURCE_VALUE_KEY
SYNTHETIC_DOUBLE_VALUE_KEY
SYNTHETIC_TRIPLE_VALUE_KEY
SYNTHETIC_JOIN_VALUE_KEY
```

Допустимо module-local helper/constants не экспортировать наружу.

Не экспортировать Composition Root/registry/factory/profile APIs — их ещё не существует.

---

# 12. Required tests

Минимальные accepted sequence files:

```text
tests/contract/test_reference_modules.py
tests/architecture/test_reference_independence.py
```

Дополнительно required для mechanical graph proof:

```text
tests/integration/test_reference_plan.py
```

## 12.1 Contract tests

Проверить минимум:

1. все четыре objects structurally satisfy `CognitiveModule`;
2. exact ModuleIds;
3. exact ImplementationIds;
4. exact `ImplementationRevision("v1")`;
5. all stateless + deterministic + COGNITIVE_CYCLE only;
6. exact read/write keys;
7. exact `required=True`, `Available`-only, `CURRENT_CYCLE` reads;
8. source constructor accepts ordinary int;
9. source rejects bool/non-int;
10. source setting immutable после construction;
11. source returns configured value through one normal staged write;
12. double computes `source * 2`;
13. triple computes `source * 3`;
14. join computes `double + triple` in declared input graph;
15. every proposal base revision/producer/attempt identity mirrors request context;
16. every StateWrite provenance mirrors descriptor + request context;
17. private_state_update always None;
18. no module mutates input projection/request.

Direct contract tests may use test-only controlled `StateProjection._from_runtime()` construction; production reference package itself не получает runtime import/constructor authority.

## 12.2 Architecture tests

Проверить минимум:

- `mindra.reference` production imports no `mindra.runtime`;
- no `mindra.composition`;
- no `mindra.entrypoints`;
- reference depends only on contracts + stdlib;
- no Service Locator/global registry/config access;
- existing Import Linter contracts remain green.

## 12.3 Planner compatibility test

Собрать test-only schema с четырьмя exact keys и owners, `ValueContract(int)`, затем compile descriptors existing `ExecutionPlanCompiler`.

Проверить exact waves:

```text
(
    ("synthetic.source",),
    ("synthetic.double", "synthetic.triple"),
    ("synthetic.join",),
)
```

Также проверить, что перестановка input descriptor tuple не меняет compiled wave graph/order.

Не создавать production `build_reference_schema()` или `CompositionRoot` ради этого test.

---

# 13. VerificationObligations

После accepted `IS-12` ожидаемый уровень:

```text
V01-012 — closed at reference/runtime independence layer
V01-013 — foundation
```

`V01-013` не считать fully closed: runnable configured reference profile/Composition Root появляется в `IS-13`.

---

# 14. Forbidden scope

`IS-12` не реализует:

- `KernelProfile`;
- TOML parser;
- `ImplementationRegistry`;
- factory descriptors;
- `build_reference_registry()`;
- `CompositionRoot`;
- composition fingerprint;
- initial `CognitiveState` builder/profile;
- `KernelRuntime` facade;
- `configs/v0.1/reference.toml`;
- automatic `composition_resolved` / `plan_compiled` evidence;
- Intervention;
- CLI/smoke command;
- stateful/failure/illegal-writer production modules;
- retry/degradation;
- runtime imports from reference;
- new causal identities;
- new module/state contracts.

Test-only helpers/fixtures допустимы, если не превращаются в production abstractions будущих steps.

---

# 15. Verification

Targeted минимум:

```text
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked lint-imports
uv run --locked pytest \
  tests/contract/test_reference_modules.py \
  tests/architecture/test_reference_independence.py \
  tests/integration/test_reference_plan.py
```

После targeted green обязателен полный `FULL-C0` и `git diff --check`.

`V0.1-IS-13` остаётся CLOSED до implementation push + independent audit + acceptance `IS-12`.
