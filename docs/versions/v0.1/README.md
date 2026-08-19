# MINDRA v0.1 — Core Kernel

## Статус

**Software milestone:** `v0.1 — Core Kernel`  
**Статус design:** `accepted`  
**Semantic baseline:** `F31`  
**Roadmap owner:** `docs/design/version-roadmap.md`  
**Implementation sequence:** [`implementation-sequence.md`](implementation-sequence.md) — `accepted`  
**Implementation:** не начата

Этот документ конкретизирует foundation semantics `DU-01 … DU-06` и Engineering Verification foundation `DU-29` в exact software profile первой версии.

Он не меняет `F31` и не вводит новую cognitive semantics.

Перед реализацией обязательны:

- этот README со статусом `accepted`;
- `implementation-sequence.md` со статусом `accepted`.

Оба условия выполнены. Coding выполняется только по одному implementation step за задачу, начиная с `V0.1-IS-01`.

---

# 1. Цель версии

`v0.1` должна создать небольшой, deterministic и машинно проверяемый runtime kernel, на который последующие software versions смогут накладывать cognitive boundaries без изменения базовой causal semantics.

Главный результат:

```text
resolved composition
      ↓
immutable committed CognitiveState
      ↓
contract-declared modules
      ↓
compiled DAG / execution waves
      ↓
same-base module compute
      ↓
staged public/private updates
      ↓
validate all
      ↓
atomic commit
      ↓
causal structural trace
```

`v0.1` не решает Environment task и не содержит LLM/ML.

---

# 2. Scope F31

Substantial implementation:

```text
DU-01 — System Context foundation
DU-02 — Dependency / Composition
DU-03 — Logical Time foundation
DU-04 — CognitiveState
DU-05 — Module Protocol / Scheduler
DU-06 — O0 Evidence + basic Intervention seam
DU-29 — Engineering Verification foundation
```

Только необходимые future-facing primitives допускаются для совместимости с roadmap.

Не реализуются cognitive contracts `DU-07+` как реальные subsystems.

---

# 3. Concrete technology profile

## 3.1. Python

Принято для `v0.1`:

```text
CPython 3.14.x
обычная GIL-сборка
requires-python = ">=3.14,<3.15"
```

Причины:

- актуальная bugfix-supported ветка;
- современный stdlib typing/dataclasses/TOML;
- stdlib `uuid7()`;
- совместимость с актуальным PyTorch line достаточна для будущих milestones;
- отсутствие необходимости поддерживать несколько Python feature versions в первой research release line.

Free-threaded CPython не входит в reference profile `v0.1`.

## 3.2. Project/dependency manager

```text
uv
pyproject.toml
uv.lock committed
.python-version
```

`uv.lock` является exact dependency resolution текущей implementation revision.

`uv run --locked` используется для verification/CI commands.

В `pyproject.toml` задаётся compatible `tool.uv.required-version`; точный patch uv фиксируется implementation evidence/CI environment.

## 3.3. Build backend

```text
uv_build
src/ package layout
```

Distribution name:

```text
mindra-agent
```

Import package:

```text
mindra
```

Package version первой реализации:

```text
0.1.0
```

До отдельного release decision package не предназначен для публикации в PyPI.

## 3.4. Runtime dependencies

**Обязательных third-party runtime dependencies: 0.**

Core Kernel использует Python stdlib.

## 3.5. Development / verification tools

Приняты:

```text
Ruff          — formatter + linter
mypy --strict — static typing
pytest        — test runner
Hypothesis    — property/state-machine tests
Import Linter — package dependency contracts
GitHub Actions — CI provider v0.1
```

Exact resolved versions фиксируются `uv.lock`.

Не вводятся `black`, `isort`, `flake8` параллельно Ruff.

---

# 4. Supported engineering environments

Обязательный C0 profile:

```text
CPU-only
no network required
no GPU required
no provider credentials
```

Поддерживаемые development/verification OS первой версии:

```text
Windows x86_64
Linux x86_64
```

macOS не является release blocker `v0.1`, хотя pure-Python code не должен намеренно зависеть от Windows/Linux-specific behavior.

Core tests не должны обращаться в интернет.

---

# 5. Repository/package layout

После реализации ожидается структура минимум:

```text
mindra-agent/
├── pyproject.toml
├── uv.lock
├── .python-version
├── src/
│   └── mindra/
│       ├── __init__.py
│       ├── __main__.py
│       ├── contracts/
│       │   ├── identity.py
│       │   ├── revisions.py
│       │   ├── time.py
│       │   ├── availability.py
│       │   ├── provenance.py
│       │   ├── state.py
│       │   ├── modules.py
│       │   ├── evidence.py
│       │   └── intervention.py
│       ├── runtime/
│       │   ├── state_store.py
│       │   ├── private_state.py
│       │   ├── planning.py
│       │   ├── commit.py
│       │   ├── scheduler.py
│       │   ├── executor.py
│       │   ├── evidence.py
│       │   ├── intervention.py
│       │   └── errors.py
│       ├── reference/
│       │   └── synthetic.py
│       ├── composition/
│       │   ├── profile.py
│       │   ├── registry.py
│       │   └── root.py
│       └── entrypoints/
│           └── cli.py
├── configs/
│   └── v0.1/
│       └── reference.toml
└── tests/
    ├── unit/
    ├── contract/
    ├── property/
    ├── integration/
    ├── architecture/
    └── fixtures/
```

Точные file splits могут быть слегка скорректированы implementation sequence без semantic change, но package-layer boundaries ниже являются частью accepted version design.

---

# 6. Import/dependency layers v0.1

Принята machine-checkable структура:

```text
mindra.entrypoints
        ↓
mindra.composition
        ↓
┌─────────────────────────┐
│ mindra.runtime           │
│ mindra.reference         │  sibling/independent
└─────────────────────────┘
        ↓
mindra.contracts
```

Правила:

1. `contracts` импортирует только stdlib;
2. `runtime` зависит от `contracts`, но не от `composition`, `entrypoints` или `reference`;
3. `reference` реализует semantic contracts и не импортирует `runtime`;
4. `runtime` и `reference` не импортируют друг друга;
5. `composition` знает concrete reference factories и runtime constructors;
6. `entrypoints` знает composition API, но не собирает Agent вручную;
7. runtime Service Locator отсутствует;
8. global mutable registry отсутствует.

Эти rules проверяются Import Linter.

---

# 7. Identity primitives

## 7.1. Почему identity отделена от revision

```text
entity/event identity
≠
monotonic state revision
```

UUID применяется к identities; integer-like wrappers — к локальным monotonic revisions.

## 7.2. Typed identities

Используются `typing.NewType` поверх `uuid.UUID` для разных causal identities, минимум:

```text
RunId
AgentSessionId
EpisodeId
DecisionWindowId
CognitiveCycleId
ExecutionPlanId
WaveId
WaveAttemptId
ModuleAttemptId
CommitId
InterventionId
LineageId
BranchId
AgentRevisionId
```

Не все identities активно используются reference smoke-run, но foundation types определяются сразу, чтобы `v0.2` не заменял generic string IDs.

## 7.3. IdFactory

Создание IDs идёт только через injected `IdFactory` contract.

Concrete implementations `v0.1`:

```text
Uuid7IdFactory
DeterministicIdFactory
```

`Uuid7IdFactory` использует stdlib UUIDv7 для normal runtime evidence identity.

`DeterministicIdFactory` использует deterministic namespace/counter semantics и применяется в reproducible tests/reference smoke profile.

Модули не вызывают `uuid.uuid7()` самостоятельно.

---

# 8. Revision primitives

Revision types являются отдельными frozen value objects с runtime validation неотрицательного значения.

Минимум:

```text
SchemaRevision
StateRevision
PrivateStateRevision
ExecutionPlanRevision
CompositionRevision
```

Они не являются interchangeable integers в public kernel API.

Required operations:

```text
initial()
next()
comparison within same revision type
```

Нельзя сравнивать/складывать semantic revisions разных типов как одно число.

`AgentRevisionId` остаётся identity, а не `StateRevision`.

---

# 9. Logical temporal context

`v0.1` реализует foundation hierarchical temporal envelope без Environment transitions.

Immutable `LogicalTime`/`TemporalContext` должен уметь нести применимые identities:

```text
run_id
agent_session_id
episode_id?
decision_window_id?
cognitive_cycle_id?
wave_id?
```

Поля downstream scopes могут быть `None`, пока соответствующая scope ещё не существует.

Wall-clock timestamp не входит в cognitive logical time.

Physical timestamps могут существовать только в diagnostic metadata Evidence Plane.

---

# 10. Semantic string identifiers

Отдельные frozen/validated identifiers используются минимум для:

```text
ModuleId
ImplementationId
ProfileId
StateNamespace
```

Они имеют canonical lowercase dotted/snake-compatible textual representation и не используют arbitrary human labels как identity.

Examples:

```text
synthetic.source
synthetic.double
reference.synthetic_source.v1
```

---

# 11. Availability model

`missing` **не является availability value**.

`missing` означает, что required structural field/key отсутствует в active schema/config и является structural error.

Для существующего schema field приняты explicit variants:

```text
Available[T]
Unknown
Stale[T]
Unavailable
```

## 11.1. Available

Содержит применимое текущее `value: T`.

## 11.2. Unknown

Значение применимо, но не известно/не вычислено. Payload отсутствует; допускается typed reason metadata.

## 11.3. Stale

Содержит последнее известное значение и freshness metadata, но contract признаёт его недостаточно свежим для некоторых consumers.

## 11.4. Unavailable

Capability/value неприменимы или намеренно отсутствуют в текущем profile. Payload отсутствует.

`None` не используется как универсальная кодировка этих состояний.

---

# 12. StatePath, StateKey и schema

## 12.1. StatePath

`StatePath` — immutable validated tuple semantic segments с canonical dotted form.

Examples:

```text
synthetic.source.value
synthetic.double.value
```

Runtime ad-hoc создание новых canonical keys после composition compile запрещено.

## 12.2. StateKey[T]

Typed key связывает semantic path с ожидаемым Python type на уровне static API.

Conceptually:

```text
StateKey[T]
└── path: StatePath
```

## 12.3. StateFieldSpec[T]

Active `StateSchema` содержит immutable specs:

```text
key
semantic owner ModuleId
ValueContract[T]
scope/freshness metadata, если применимо
```

Owner хранится в schema/spec, а не выводится из имени Python class.

## 12.4. ValueContract[T]

Version-level helper contract отвечает за:

```text
validate(value)
freeze(value) -> snapshot-safe value
```

Он не является serialization codec.

Reference `v0.1` использует immutable Python values/frozen dataclasses.

Known mutable builtins (`list`, mutable `dict`, `set`) не принимаются default value contract как snapshot-safe canonical payload.

Поздняя version может добавить Tensor-specific ValueContract без изменения CognitiveState semantics.

---

# 13. StateEntry и provenance

Каждый canonical field хранится как immutable `StateEntry[T]`:

```text
StateEntry
├── semantic value/availability variant
└── StateProvenance
```

`StateProvenance` минимум умеет представить:

```text
producer ModuleId / runtime boundary
implementation identity where relevant
base StateRevision
module_attempt_id where relevant
logical temporal context
source/parent refs
intervention refs
```

Research/run metadata, не предназначенная cognition, хранится в envelope/evidence и не добавляется модулю как feature.

---

# 14. CognitiveState exact representation

`CognitiveState` реализуется immutable-by-interface dataclass/value object:

```text
CognitiveState
├── StateEnvelope
└── immutable mapping StatePath → StateEntry
```

`StateEnvelope` минимум:

```text
schema_revision
state_revision
parent_state_revision?
lineage_id
branch_id
agent_revision_id
logical_time
composition_revision
```

## 14.1. Storage implementation v0.1

Reference implementation использует copy-on-commit обычного Python `dict` с read-only `Mapping`/`MappingProxyType` exposure.

Полный deep copy каждого payload не является contract.

Snapshot safety обеспечивает `ValueContract.freeze()`.

## 14.2. No ambient mutable access

Внутреннее mutable storage не выдаётся модулям.

Модуль не получает `CognitiveState` целиком как обычный mapping.

---

# 15. StateProjection

Scheduler создаёт для каждого module attempt отдельный immutable `StateProjection` только из declared reads.

API должен обеспечивать:

```text
projection.read(key)
```

и reject:

```text
read undeclared key
read structurally missing key
read status disallowed ReadSpec
```

Таким образом архитектурное правило declared reads проверяется runtime-механически, а не convention-only.

---

# 16. ReadSpec

Каждый read dependency объявляется типизированным `ReadSpec`.

Минимальная semantics `v0.1`:

```text
key
required: bool
allowed_availability
freshness
```

Freshness modes первой версии:

```text
ANY_COMMITTED
CURRENT_CYCLE
```

`CURRENT_CYCLE` означает, что active plan обязан иметь producer этого key в текущем cycle/segment до consumer; возникает DAG edge.

`ANY_COMMITTED` разрешает чтение допустимого значения из base committed state и не создаёт same-cycle producer edge автоматически.

Будущие более точные Decision/Outcome freshness modes могут быть добавлены совместимо.

---

# 17. Proposed public update

Модуль не получает mutable state store.

Он возвращает immutable:

```text
StateUpdateProposal
├── base_state_revision
├── producer ModuleId
├── module_attempt_id
└── writes: tuple[StateWrite, ...]
```

Каждый `StateWrite` содержит:

```text
StateKey
new availability/value
provenance additions
```

Commit Coordinator проверяет:

- key существует в schema;
- producer имеет write authority;
- key declared в ModuleDescriptor writes;
- base revision актуальна;
- ValueContract проходит;
- conflict отсутствует;
- temporal context совместим.

---

# 18. Module-private state

`v0.1` сразу поддерживает causally relevant private state, но не помещает его в `CognitiveState`.

Runtime хранит:

```text
PrivateStateStore
ModuleId → PrivateStateSlot
```

`PrivateStateSlot` содержит:

```text
PrivateStateRevision
snapshot-safe private value
```

ModuleDescriptor явно объявляет stateless/stateful semantics и optional `PrivateStateContract`.

Stateful module получает только **собственный** private snapshot.

Он возвращает `PrivateStateProposal` относительно конкретной private revision.

Модуль не получает private state других modules.

---

# 19. Atomic public + private commit

Один успешный wave commit может атомарно изменить:

```text
CognitiveState
+
one or more module-private states
```

Validation выполняется полностью **до** публикации любого результата.

Если любой required result/validation fails:

```text
public state unchanged
private states unchanged
```

Если wave меняет только private state, `StateRevision` CognitiveState не обязана увеличиваться; trace commit всё равно получает отдельный `CommitId` и фиксирует private revisions before/after.

Это сохраняет distinction:

```text
CognitiveState revision
≠ full Agent runtime commit identity
```

---

# 20. Module protocol v0.1

Принят structural typing через Python `Protocol`.

Semantic interface:

```text
CognitiveModule
├── descriptor: ModuleDescriptor
└── compute(ModuleComputeRequest) -> ModuleComputeResult
```

## 20.1. ModuleComputeRequest

Содержит только:

```text
StateProjection declared reads
own PrivateStateSnapshot / unavailable
ModuleExecutionContext
```

Не содержит:

- full Composition Root;
- registry;
- raw config;
- other module objects;
- evaluator;
- global service container.

## 20.2. ModuleComputeResult

Содержит:

```text
StateUpdateProposal
PrivateStateProposal?
optional bounded diagnostics
```

Module result ещё **не committed**.

## 20.3. Compute side-effect rule

Cognitive module compute обязан быть side-effect free относительно canonical Agent state.

Он не изменяет shared/private store сам.

External service side effects в будущих modules будут проектироваться через их specialized boundaries; `v0.1` reference modules pure.

---

# 21. ModuleDescriptor

Immutable descriptor минимум содержит:

```text
module_id
implementation_id
implementation_revision
reads
writes
private_state descriptor
lifecycle phase participation
execution traits
```

Execution traits первой версии:

```text
stateless/stateful
deterministic/stochastic declaration
```

Reference profile принимает только deterministic implementations.

`disabled` module отсутствует из active composition; если его output required consumer'у, plan compilation fails.

NoOp/Control implementation является обычной concrete implementation semantic module role, а не специальной scheduler веткой.

---

# 22. Execution phase v0.1

Первая версия реализует один scheduler segment type:

```text
COGNITIVE_CYCLE
```

Environment observation/action phases появляются в `v0.2`.

ModuleDescriptor может участвовать только в поддерживаемой phase; unsupported phase — composition error.

Это version limitation, не утверждение, что MINDRA имеет только одну lifecycle phase.

---

# 23. Execution Plan Compiler

`ExecutionPlanCompiler` получает:

```text
active ModuleDescriptors
StateSchema
composition metadata
```

и строит immutable `ExecutionPlan`.

Compile-time validation минимум:

- unique semantic `ModuleId`;
- implementation descriptor compatibility;
- all write keys exist in StateSchema;
- writer == semantic owner;
- duplicate/ambiguous writer rejected;
- required CURRENT_CYCLE read имеет producer;
- declared producer/output compatibility;
- unsupported phase rejected;
- instantaneous dependency cycle rejected;
- deterministic wave decomposition.

Plan identity содержит:

```text
ExecutionPlanId
ExecutionPlanRevision
stable plan fingerprint
composition revision
```

---

# 24. DAG и wave decomposition

Same-cycle edge возникает из explicit `CURRENT_CYCLE` dependency.

Compiler строит DAG и детерминированно делит его на topological waves.

Tie-breaker внутри логически независимого множества — canonical `ModuleId` order только для **physical deterministic execution/evidence**, а не для data dependency semantics.

Модули одной wave:

```text
read same CognitiveState base revision
read own private state snapshot before wave
cannot see sibling proposals
```

Следующая wave видит committed результат предыдущей wave.

---

# 25. WaveExecutor abstraction

Physical execution отделено от scheduling semantics.

Version-level contract:

```text
WaveExecutor
→ execute collection of ModuleAttempt requests
→ collection of ModuleAttempt results
```

Concrete `v0.1`:

```text
SequentialWaveExecutor
```

Он выполняет modules последовательно для простоты/debuggability, **но каждый attempt получает одну и ту же base revision**.

Scheduler не делает semantic assumptions из completion order.

Thread/async/process executors не входят в `v0.1`.

---

# 26. Failure semantics wave

Reference `v0.1` modules являются required для своего plan.

Wave behavior:

1. executor пытается вычислить scheduled module attempts против same base;
2. exceptions конвертируются в failed `ModuleAttemptRecord`;
3. staged proposals остаются uncommitted;
4. если хотя бы один required attempt failed — wave commit не происходит;
5. уже вычисленные sibling proposals отбрасываются;
6. committed public/private state остаётся прежним;
7. failure полностью виден O0 trace.

Scheduler не применяет partial success subset как default.

Optional degradation policies относятся к последующим concrete module versions.

---

# 27. Stale proposal semantics

Commit Coordinator всегда сравнивает proposal base revision с допустимой current base.

Stale update нельзя silently rebase.

`v0.1` default:

```text
stale proposal
→ reject
→ StaleProposal error/result
→ no mutation
```

Automatic recompute может быть добавлен будущим runtime policy, но не является default `v0.1`.

Property/state-machine tests обязаны генерировать stale scenarios.

---

# 28. KernelRuntime facade

Composition Root возвращает узкий runtime object, conceptually:

```text
KernelRuntime
├── compiled plan
├── committed CognitiveState
├── PrivateStateStore
├── scheduler
├── evidence recorder
├── active composition metadata
└── run_cycle()
```

Он не является Service Locator: cognitive modules не получают `KernelRuntime` reference.

Public facade первой версии предназначен для entrypoint/tests; stable long-term end-user API ещё не обещается.

---

# 29. Configuration format

Используется stdlib TOML (`tomllib`).

Versioned profile schema:

```text
mindra.kernel-profile/v1
```

Минимальная conceptual структура:

```toml
schema = "mindra.kernel-profile/v1"
profile_id = "v0.1-reference"

[[modules]]
module_id = "synthetic.source"
implementation = "reference.synthetic_source.v1"

[modules.settings]
# implementation-specific, strict-validated composition settings
```

Raw TOML:

```text
read once
→ strict parse/validation
→ immutable KernelProfile
→ Composition Root
→ resolved local settings passed constructors
```

Модули не читают TOML/global config в runtime.

Unknown top-level/profile keys fail closed.

Implementation factory обязана strict-validate own settings и reject unknown keys.

---

# 30. Implementation Registry

`ImplementationRegistry` существует только в `mindra.composition`.

Это immutable mapping:

```text
ImplementationId
→ explicit factory descriptor
```

Правила:

- регистрация происходит explicit function calls при Composition Root setup;
- import-time decorator auto-registration отсутствует;
- duplicate id fail-fast;
- runtime/cognitive module не имеет registry reference;
- plugin discovery/entry points не реализуются `v0.1`.

Reference registry строится explicit `build_reference_registry()`.

---

# 31. Composition Root

`CompositionRoot` отвечает за:

1. parse/receive validated `KernelProfile`;
2. resolve implementation IDs через local registry;
3. construct modules with immutable resolved settings;
4. build StateSchema;
5. build initial `CognitiveState`;
6. create private state slots;
7. compile/validate ExecutionPlan;
8. compute composition fingerprint;
9. assign active `AgentRevisionId`/composition revision identity;
10. create Evidence Recorder;
11. return `KernelRuntime`.

Никакой другой entrypoint не собирает modules вручную.

---

# 32. Composition fingerprint

Resolved composition получает deterministic SHA-256 fingerprint от canonical normalized representation:

```text
profile schema
semantic module IDs
implementation IDs/revisions
resolved behavior-relevant settings
state schema revision
```

Fingerprint является provenance/evidence, а не cognitive input.

`AgentRevisionId` и `composition_fingerprint` различаются:

```text
AgentRevisionId = causal identity
fingerprint = deterministic content evidence
```

---

# 33. Initial CognitiveState

Composition Root создаёт schema-complete state.

Registered fields, не имеющие initial applicable value, представлены explicit `Unknown`/`Unavailable`, а не отсутствующим key.

`missing` reserved для structural/schema error.

Initial state:

```text
StateRevision = 0
parent = None
lineage/branch identities assigned
agent_revision pinned
```

Reference synthetic source producer затем публикует first available values через normal scheduler proposal/commit, а не special initialization mutation.

---

# 34. Evidence Plane foundation

`v0.1` реализует mandatory structural O0 trace в памяти.

Core entities:

```text
TraceEventEnvelope
TraceEvent payload variants
EvidenceRecorder Protocol
InMemoryEvidenceRecorder
```

Минимальные event kinds:

```text
composition_resolved
plan_compiled
cycle_started
wave_started
module_attempt_started/finished
commit_attempted
commit_succeeded/failed
state_revision_committed
intervention_applied
cycle_finished/failed
```

Exact event payload classes типизированы frozen dataclasses.

Trace records attempts, а не только successful commits.

---

# 35. Evidence isolation

Evidence Recorder получает **копии/immutable records**.

Он не получает write authority state/private store.

Trace metadata:

```text
run/profile/attempt IDs
physical timestamp if collected
error text
```

не входит автоматически в `StateProjection` cognitive modules.

`v0.1` не реализует networked logger/telemetry exporter.

Reference recorder — process-local in-memory append-only collection.

---

# 36. Basic Intervention seam

Полный Evaluation Runtime отсутствует, но `v0.1` реализует explicit test/research seam.

`InterventionGateway` поддерживает только controlled state override на declared safe boundary:

```text
committed state
→ explicit StateInterventionSpec
→ validation
→ new committed state revision
→ intervention provenance/lineage
```

Default reference run имеет interventions disabled.

Tests могут включить allowlist policy.

Intervention:

- не меняет semantic owner field;
- не masquerade как module write;
- получает `InterventionId`;
- сохраняет natural/base state reference;
- видна Evidence Plane.

Arbitrary private-object mutation не поддерживается.

---

# 37. Reference synthetic composition

`v0.1` обязана иметь один deterministic runnable reference profile.

Recommended graph:

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

Expected waves:

```text
Wave 0: source
Wave 1: double | triple
Wave 2: join
```

Например при configured source value `2`:

```text
double = 4
triple = 6
join = 10
```

Reference profile существует для scheduler/state proof, а не как cognitive task.

---

# 38. Stateful/failure test modules

Дополнительные synthetic implementations для tests могут существовать в `tests/fixtures` или clearly internal reference fixtures:

```text
StatefulCounterModule
FailingModule
IllegalWriterModule
UndeclaredReaderModule
StaleProposal fixture
```

Они не являются cognitive architecture boundaries.

Stateful fixture обязана доказать atomic private-state semantics.

---

# 39. CLI / smoke interface

Минимальный stdlib `argparse` entrypoint:

```text
mindra kernel-smoke --profile configs/v0.1/reference.toml
mindra validate-profile --profile ...
```

`python -m mindra` вызывает тот же entrypoint.

Smoke output содержит только concise execution/result summary; полный typed trace доступен через runtime/test API.

CLI первой версии не объявляется стабильным external API `v1.0`.

---

# 40. Error taxonomy v0.1

Typed exception/result classes минимум различают:

```text
ConfigurationError
CompositionError
DuplicateIdentityError
SchemaError
MissingFieldError
UndeclaredReadError
UnauthorizedWriteError
AvailabilityError
ExecutionPlanError
DependencyCycleError
ModuleExecutionError
WaveExecutionError
CommitValidationError
StaleProposalError
InterventionError
```

Ошибки не кодируются generic boolean `success=False` без причины.

User/config errors не смешиваются с module compute failure.

---

# 41. Static typing policy

`mypy --strict` является blocking gate.

Rules:

- public/internal kernel functions annotated;
- no blanket `Any` at semantic boundaries;
- `Any` допустим только в explicitly isolated type-erasure internals с justification;
- `# type: ignore` требует конкретный error code + комментарий на русском, объясняющий необходимость;
- tests также type-check настолько, насколько practically возможно;
- third-party dev tooling typing gaps не разрешают ослабить whole-package strictness.

---

# 42. Ruff policy

Blocking commands:

```text
ruff check .
ruff format --check .
```

Минимальные lint families должны включать correctness/import/modernization classes (`E/F/I/UP/B/RUF` или актуальный эквивалент выбранной Ruff revision).

Exact rule set фиксируется `pyproject.toml`; массовые broad `noqa` запрещены.

Документация/комментарии в source — русский язык; identifiers — английский.

---

# 43. Import Linter contracts

Blocking `lint-imports` проверяет минимум:

```text
entrypoints → composition → runtime/reference → contracts
runtime ⟂ reference
contracts has no internal upward dependency
runtime cannot import composition/entrypoints/reference
reference cannot import runtime/composition/entrypoints
```

Дополнительно forbidden contract запрещает core packages импортировать future Training/Evaluation packages, если они позже появятся.

На `v0.1` отсутствующий future package не создаётся только ради lint rule.

---

# 44. Test taxonomy

## unit

Value objects, parser, schema, projection, revisions, plan helpers.

## contract

ModuleProtocol behavior, ownership/read/write enforcement, composition profile semantics.

## property

State revisions, immutable snapshots, proposal validation, deterministic plan decomposition.

## state-machine

Sequences:

```text
stage
commit
stale apply
intervention
private-state update
failure
next commit
```

## integration

Full synthetic profile through Composition Root → Scheduler → final state/trace.

## architecture

Import Linter + explicit no-global/service-locator checks where applicable.

---

# 45. VerificationObligations v0.1

Version design вводит обязательный набор.

## `V01-001 — Same-base wave`

Все module attempts одной wave читают одну `StateRevision` и не видят sibling proposals.

## `V01-002 — Atomic wave commit`

Любой required failure/invalid proposal оставляет public/private committed state unchanged.

## `V01-003 — Single writer authority`

Module не может commit key, owner/writes которого ему не принадлежат.

## `V01-004 — Declared reads only`

Module не может через `StateProjection` прочитать undeclared key.

## `V01-005 — No structural missing ambiguity`

`missing` schema field отличается от `Unknown/Stale/Unavailable` existing field.

## `V01-006 — Stale proposal rejected`

Proposal против недопустимой base revision не rebased silently.

## `V01-007 — DAG validity`

Instantaneous dependency cycle/ambiguous writer/missing required current producer fail before normal execution.

## `V01-008 — Private-state transactionality`

Own private state обновляется только при successful atomic commit и не доступен peer modules.

## `V01-009 — Evidence reconstructability`

O0 trace восстанавливает plan/wave/module-attempt/commit lineage, включая failed attempts.

## `V01-010 — Observability isolation`

Trace/profiler/config metadata не появляется в module `StateProjection` без explicit state contract.

## `V01-011 — Intervention provenance`

Controlled override создаёт новую revision/explicit intervention record и не выглядит natural module output.

## `V01-012 — Dependency architecture`

Import graph соблюдает DU-02 layer/independence contracts; runtime Service Locator отсутствует.

## `V01-013 — Deterministic reference profile`

При deterministic ID/profile implementation semantic final state, plan/waves и logical trace sequence повторяются.

## `V01-014 — Build/install reproducibility`

Clean `uv sync --locked` + build + verification проходит в declared Windows/Linux C0 environments.

---

# 46. Verification commands

Acceptance command family после implementation:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked lint-imports
uv run --locked pytest
uv build
```

Implementation sequence может разделить быстрые/extended test profiles, но final `v0.1` gate запускает полный C0 suite.

---

# 47. CI profile

`v0.1` использует **GitHub Actions** как CI provider.

Минимально:

- Linux x86_64 / Python 3.14 full verification;
- Windows x86_64 / Python 3.14 smoke + test suite;
- locked dependency install;
- build artifact check.

Выбор GitHub Actions является version-level tooling choice и не становится F31 requirement для последующих versions.

Network доступен только dependency installation phase; tests themselves не зависят от network.

---

# 48. Determinism claim v0.1

`v0.1` не обещает universal bitwise reproducibility любых будущих backends.

Reference synthetic profile требует более узкий claim:

```text
same code revision
same locked dependencies
same resolved profile
same deterministic ID factory
same initial state
→ same semantic ExecutionPlan
→ same wave structure
→ same state payload/revisions
→ same logical event-kind/causal sequence
```

Physical timestamps не сравниваются.

---

# 49. Snapshot/checkpoint boundary

`v0.1` **не реализует persistent DU-27 checkpoint**.

Однако kernel data structures обязаны быть snapshot-ready:

- committed state immutable;
- private state explicit;
- IDs/revisions explicit;
- no hidden global mutable cognition;
- composition/profile identity explicit;
- Evidence state отделено от cognition.

Persistent AgentSnapshot/Checkpoint materialization начинается roadmap `v0.4`.

`v0.1` tests могут clone immutable state/private store in-memory для property/intervention tests, но не называют это full Checkpoint.

---

# 50. Security / fail-closed profile

В foundation применяются fail-closed rules для:

- invalid config;
- duplicate implementation ID;
- illegal import architecture at CI;
- missing required schema field;
- unauthorized write;
- stale proposal;
- dependency cycle;
- malformed intervention;
- incompatible plan.

Module compute failure aborts current wave commit.

Не используется `except Exception: pass` в runtime core.

---

# 51. Explicit non-goals

`v0.1` не включает:

- Environment/MicroWorld;
- Observation/Perception;
- real Goal System;
- Cortex/LLM;
- Memory;
- World/Self models;
- Intrinsic/Drive/Appraisal/Affect/Valuation/Salience;
- Workspace/Executive/Planner;
- Policy/Action Boundary;
- Experience Journal;
- Training Runtime;
- PyTorch/NumPy;
- persistent Checkpoint;
- remote providers;
- multiprocessing/threaded scheduler;
- async scheduler;
- distributed execution;
- plugin discovery;
- database/storage backend;
- production telemetry stack;
- stable public SDK.

Synthetic modules существуют только для доказательства kernel semantics.

---

# 52. Deferred choices

Следующие вопросы сознательно остаются будущим versions:

- tensor snapshot/freeze policy;
- async/parallel physical executors;
- Pydantic/other richer config schemas при необходимости;
- persistent serialization schema;
- plugin entry points;
- ML framework;
- device abstraction;
- Environment action/observation lifecycle;
- long-running resource budgets;
- remote evidence exporters.

Deferred choice нельзя реализовать в `v0.1` «заодно» без изменения version design.

---

# 53. Compatibility intent

Следующие `v0.2+` должны **расширять**, а не заменять foundation concepts:

```text
StateKey / StateSchema
CognitiveState / StateProjection
ModuleDescriptor / CognitiveModule
ExecutionPlan / Scheduler
WaveExecutor
StateUpdateProposal
PrivateStateProposal
CommitCoordinator
CompositionRoot / Registry
EvidenceRecorder / TraceEvent
InterventionGateway
```

Exact API может получить additive fields/types, но downstream design не должен требовать перехода к mutable global dict, runtime Service Locator или direct peer calls.

Если implementation показывает, что один из этих exact version choices противоречит F31, coding останавливается и проводится design review; semantic mismatch не чинится hidden workaround.

---

# 54. Acceptance gate v0.1

Design считается реализованным только если одновременно выполнено:

1. package устанавливается из clean checkout через locked environment;
2. reference synthetic profile запускается CPU-only;
3. expected 3-wave DAG получается из descriptors, а не hardcoded list;
4. final synthetic value соответствует profile expectation;
5. все `V01-001 … V01-014` имеют linked verification evidence;
6. Ruff/mypy/import contracts/test suite green;
7. fault tests подтверждают no partial commit;
8. stale/illegal write/undeclared read/cycle fail closed;
9. structural O0 trace содержит attempts + commits;
10. intervention seam создаёт explicit new lineage/revision;
11. no runtime third-party dependency;
12. no hidden global mutable state/service locator;
13. документация/комментарии source на русском, identifiers на английском;
14. implementation не добавляет cognitive responsibilities из `v0.2+`.

---

# 55. Accepted design gate

Следующие concrete решения приняты для `v0.1`:

```text
Python 3.14 + uv + uv_build
stdlib-only runtime
src/mindra package
contracts → runtime/reference → composition → entrypoints layers
NewType UUID identities + injected IdFactory
frozen revision wrappers
StateKey/StateFieldSpec/ValueContract
Available/Unknown/Stale/Unavailable variants
immutable CognitiveState + per-module StateProjection
proposal-based public/private state updates
DAG compiler + SequentialWaveExecutor
atomic CommitCoordinator
TOML profile + explicit immutable registry
in-memory O0 Evidence Recorder
basic explicit InterventionGateway
Ruff + strict mypy + pytest + Hypothesis + Import Linter
GitHub Actions CI
V01-001 … V01-014
```

Dependency-ordered реализация определена в:

```text
docs/versions/v0.1/implementation-sequence.md
```

Первый и единственный разрешённый coding step на старте:

```text
V0.1-IS-01 — Project bootstrap & verification shell
```

Следующий step открывается только после implementation + verification + ChatGPT audit предыдущего шага.
