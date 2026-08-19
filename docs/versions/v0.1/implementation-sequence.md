# MINDRA v0.1 — Implementation Sequence

## Статус

**Software milestone:** `v0.1 — Core Kernel`  
**Статус:** `accepted`  
**Version design:** [`README.md`](README.md) — `accepted`  
**Semantic baseline:** `F31`  
**Implementation:** не начата

Этот документ разбивает принятый design `v0.1` на небольшие dependency-ordered implementation steps для Codex.

Он **не является новым архитектурным design**. Если какой-либо шаг требует изменить `F31` или принятый `v0.1/README.md`, coding останавливается и проводится design review.

---

# 1. Общие правила исполнения

## 1.1. Один шаг за один coding task

Codex получает только один `V0.1-IS-XX` за задачу.

После выполнения шага:

```text
Codex implementation
→ предусмотренные проверки
→ отчёт Codex
→ audit ChatGPT
→ при необходимости correction patch
→ только затем следующий IS
```

Не реализовывать последующие шаги «заодно».

## 1.2. Обязательный контекст перед каждым шагом

Перед изменениями Codex читает минимум:

```text
AGENTS.md
docs/design/current.md
docs/design/contract-adr-consistency-freeze.md
docs/design/contracts/semantic-freeze-manifest.md
docs/design/version-roadmap.md
docs/versions/v0.1/README.md
этот implementation-sequence.md
```

И дополнительно — canonical design/ADR, перечисленные у конкретного шага.

## 1.3. Stop conditions

Codex **не принимает самостоятельное решение**, если обнаружены:

- противоречие accepted documentation;
- необходимость изменить semantic ownership/boundary/commit semantics;
- отсутствующий prerequisite предыдущего шага;
- необходимость выйти за scope `v0.1`;
- решение, которое version design сознательно оставляет будущей версии;
- невозможность выполнить обязательную VerificationObligation без изменения design.

В этих случаях работа останавливается с blocker report.

## 1.4. Нельзя ослаблять verification

Запрещено ради зелёного результата:

- удалять или ослаблять требуемый test;
- добавлять broad `noqa`, blanket `type: ignore`, `ignore_missing_imports`;
- переводить failing test в `skip`/`xfail`/quarantine без отдельного решения;
- уменьшать Import Linter boundaries;
- делать test-only обход production contracts;
- подменять semantic assertion более слабой проверкой implementation detail.

## 1.5. Язык

- documentation/comments/docstrings — русский;
- package/module/class/function/type/variable identifiers — английский.

## 1.6. Definition of done отдельного шага

Шаг завершён только если одновременно:

1. реализован ровно его scope;
2. добавлены/обновлены указанные tests;
3. targeted verification green;
4. уже существующие tests не сломаны;
5. Codex перечислил changed files и результаты commands;
6. не начат следующий шаг;
7. ChatGPT audit не выявил blocker/regression.

---

# 2. Базовые команды verification

По мере появления tooling используются три профиля.

## `FAST`

```text
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked pytest <targeted paths>
```

## `ARCH`

```text
uv run --locked lint-imports
```

## `FULL-C0`

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked lint-imports
uv run --locked pytest
uv build
```

До появления соответствующего инструмента/конфигурации шаг выполняет только уже существующую применимую часть. `V0.1-IS-01` обязан создать полный toolchain, после него отсутствие команды считается blocker.

Core tests после dependency installation не обращаются в интернет.

---

# 3. Карта шагов

| Шаг | Название | Основной результат |
|---|---|---|
| `V0.1-IS-01` | Project bootstrap & verification shell | устанавливаемый typed package + locked toolchain + CI |
| `V0.1-IS-02` | Identity / revision / logical time | causal IDs, typed revisions, temporal primitives |
| `V0.1-IS-03` | Availability / provenance / error foundation | explicit availability, provenance и typed failures |
| `V0.1-IS-04` | State schema primitives | `StatePath`, `StateKey`, `ValueContract`, schema/entry types |
| `V0.1-IS-05` | CognitiveState & projection | immutable committed state + declared-read projection |
| `V0.1-IS-06` | Module contracts & proposals | `CognitiveModule`, descriptors, public/private proposals |
| `V0.1-IS-07` | Execution plan compiler | validated DAG + deterministic waves |
| `V0.1-IS-08` | PrivateStateStore | explicit per-module private state snapshots/revisions |
| `V0.1-IS-09` | Atomic CommitCoordinator | authority/stale validation + public/private atomic commit |
| `V0.1-IS-10` | O0 Evidence Plane | typed structural trace + isolated recorder |
| `V0.1-IS-11` | WaveExecutor & Scheduler | same-base execution, failure semantics, cycle execution |
| `V0.1-IS-12` | Reference synthetic modules | pure deterministic source/double/triple/join implementations |
| `V0.1-IS-13` | Configuration & Composition Root | strict TOML, registry, resolved runtime, reference profile |
| `V0.1-IS-14` | InterventionGateway | controlled state intervention with explicit provenance |
| `V0.1-IS-15` | CLI & deterministic end-to-end smoke | runnable 3-wave kernel profile and validation CLI |
| `V0.1-IS-16` | Version acceptance hardening | full obligations matrix, CI/build audit, release candidate evidence |

---

# 4. `V0.1-IS-01 — Project bootstrap & verification shell`

## Цель

Создать минимальный устанавливаемый Python project и blocking engineering toolchain **до** появления kernel semantics.

## Prerequisites

- clean documentation-only repository;
- `v0.1/README.md` и этот sequence имеют `accepted` status.

## Обязательный контекст

- `docs/design/system-context.md`;
- `docs/design/dependency-rules.md`;
- `docs/design/engineering-testing.md`;
- `ADR-0001`, `ADR-0002`, `ADR-0029`.

## Реализовать

Минимум:

```text
pyproject.toml
uv.lock
.python-version
src/mindra/__init__.py
src/mindra/__main__.py
src/mindra/contracts/__init__.py
src/mindra/runtime/__init__.py
src/mindra/reference/__init__.py
src/mindra/composition/__init__.py
src/mindra/entrypoints/__init__.py
tests/... package/test skeleton
architecture import-contract configuration
.github/workflows/ci.yml
```

Принятые choices:

```text
CPython >=3.14,<3.15
uv + uv_build
runtime third-party dependencies = 0
Ruff
mypy --strict
pytest
Hypothesis
Import Linter
GitHub Actions
```

CI:

- Linux x86_64 / Python 3.14 — полный доступный verification;
- Windows x86_64 / Python 3.14 — locked install + tests/type/lint/build;
- tests не используют network после installation.

`mindra.__main__` пока может только делегировать ещё пустому/минимальному entrypoint либо возвращать понятное сообщение; `kernel-smoke` ещё не реализуется.

## Tests / verification

Добавить минимальные tests, подтверждающие:

- `import mindra`;
- package metadata/version `0.1.0`;
- build wheel/sdist;
- Import Linter видит принятые package layers;
- `contracts` не имеет upward dependency;
- `runtime` и `reference` независимы.

Запустить `FULL-C0` локально в доступной среде; Windows подтверждается CI, если текущая среда не Windows.

## VerificationObligations

- `V01-012` — foundation/partial;
- `V01-014` — foundation/partial.

## Forbidden scope

Не создавать state/module/scheduler semantics, synthetic cognitive modules, Environment, Memory, Cortex или ML dependencies.

---

# 5. `V0.1-IS-02 — Identity / revision / logical time`

## Цель

Создать type-safe causal identity и revision foundation, от которого будут зависеть все последующие records.

## Обязательный контекст

- `docs/design/system-context.md`;
- `docs/design/execution-model.md`;
- `docs/design/cognitive-state.md`;
- `ADR-0001`, `ADR-0003`, `ADR-0004`.

## Реализовать

В `mindra.contracts`:

- typed UUID identities из version README;
- semantic string IDs: `ModuleId`, `ImplementationId`, `ProfileId`, `StateNamespace`;
- `IdFactory` Protocol;
- immutable `LogicalTime`/`TemporalContext`;
- frozen revision value objects:
  - `SchemaRevision`;
  - `StateRevision`;
  - `PrivateStateRevision`;
  - `ExecutionPlanRevision`;
  - `CompositionRevision`.

Concrete factories разместить в kernel implementation layer без нарушения imports:

- `Uuid7IdFactory`;
- `DeterministicIdFactory`.

Точная physical file split допустима в пределах package layers, но identity contract не должен зависеть от `runtime`/`composition`.

## Required semantics

- semantic IDs validated/canonical;
- revision types не взаимозаменяемы в public API;
- отрицательная revision запрещена;
- `initial()`/`next()`;
- deterministic factory воспроизводит одну identity sequence при одинаковой seed/namespace/counter configuration;
- modules в будущем получают factory/injected IDs, а не вызывают UUID API напрямую;
- wall clock отсутствует из logical time.

## Tests

Минимум:

```text
tests/unit/test_identity.py
tests/unit/test_revisions.py
tests/unit/test_time.py
```

Проверить type/runtime validation и deterministic factory behavior.

## Verification

`FAST + ARCH`.

## Forbidden scope

Не создавать `CognitiveState`, `ModuleDescriptor`, DAG или Evidence events.

---

# 6. `V0.1-IS-03 — Availability / provenance / error foundation`

## Цель

Зафиксировать explicit `Available / Unknown / Stale / Unavailable`, foundational provenance и typed error taxonomy **до** реализации state store.

## Обязательный контекст

- `docs/design/cognitive-state.md`;
- `docs/design/observability-and-intervention.md`;
- `docs/design/module-lifecycle.md`;
- `ADR-0004`, `ADR-0005`, `ADR-0006`.

## Реализовать

В contracts:

```text
Available[T]
Unknown
Stale[T]
Unavailable
StateProvenance
```

Минимальные provenance fields соответствуют `v0.1/README.md`: producer/runtime boundary identity, implementation identity where relevant, base revision, module attempt, logical context, source/parent refs, intervention refs.

Добавить typed kernel errors из `v0.1` постепенно, но уже на этом шаге должна существовать общая fail-closed taxonomy foundation, достаточная для последующих state/projection/plan/commit errors.

## Required semantics

- `missing` не представлен availability variant;
- `Unknown`/`Unavailable` не имеют semantic payload;
- `Stale[T]` хранит last known value + freshness metadata;
- availability/provenance objects immutable;
- diagnostic metadata не смешивается с cognitive provenance payload;
- generic `success=False` не используется вместо typed reason/error.

## Tests

Минимум:

```text
tests/unit/test_availability.py
tests/unit/test_provenance.py
tests/unit/test_errors.py
```

Проверить, в частности:

- `Unknown != Unavailable`;
- structural missing не кодируется `Unknown`;
- stale сохраняет value и freshness;
- frozen value objects нельзя мутировать.

## VerificationObligations

- `V01-005` — semantic foundation/partial;
- `V01-010` — provenance/isolation foundation/partial.

## Verification

`FAST + ARCH`.

## Forbidden scope

Не добавлять state mapping/store, module protocol или trace recorder.

---

# 7. `V0.1-IS-04 — State schema primitives`

## Цель

Создать immutable typed schema model без mutable runtime store.

## Обязательный контекст

- `docs/design/cognitive-state.md`;
- `docs/design/dependency-rules.md`;
- `ADR-0004`.

## Реализовать

Минимум:

```text
StatePath
StateKey[T]
StateFieldSpec[T]
ValueContract[T]
StateSchema
StateEntry[T]
StateEnvelope
ReadSpec
FreshnessMode {ANY_COMMITTED, CURRENT_CYCLE}
```

Reference/default `ValueContract` принимает snapshot-safe immutable values/frozen dataclasses и fail-closed отклоняет известные mutable builtins (`list`, mutable `dict`, `set`) как canonical payload.

`StateSchema`:

- immutable после создания;
- duplicate path запрещён;
- owner берётся explicit `ModuleId` из spec;
- runtime ad-hoc canonical key creation после compile не поддерживается.

## Tests

Минимум:

```text
tests/unit/test_state_path.py
tests/unit/test_state_schema.py
tests/unit/test_value_contract.py
```

Проверить canonical dotted path, duplicate rejection, mutable payload rejection, schema lookup и structural missing.

## VerificationObligations

- `V01-005` — substantial.

## Verification

`FAST + ARCH`.

## Forbidden scope

Не создавать state commit, module execution или composition root.

---

# 8. `V0.1-IS-05 — CognitiveState & StateProjection`

## Цель

Реализовать immutable-by-interface committed state и механически enforce declared reads.

## Обязательный контекст

- `docs/design/cognitive-state.md`;
- `docs/design/execution-model.md`;
- `ADR-0003`, `ADR-0004`.

## Реализовать

Минимум:

```text
CognitiveState
read-only StateEntry mapping
copy-on-commit state construction primitive
StateProjection
projection builder/factory controlled by runtime
```

`StateProjection` создаётся только из explicit `ReadSpec` и base committed state.

## Required semantics

- module-facing API не выдаёт underlying mutable dict;
- `projection.read(key)` отвергает undeclared key;
- structurally missing key отличается от explicit availability;
- disallowed availability/freshness fail closed;
- `CURRENT_CYCLE` freshness проверяемо по provenance/logical context;
- snapshot payload проходит `ValueContract.freeze()`;
- physical diagnostic metadata не становится state field автоматически.

## Tests

Минимум:

```text
tests/unit/test_cognitive_state.py
tests/contract/test_state_projection.py
tests/property/test_state_snapshot_immutability.py
```

## VerificationObligations

- `V01-004` — closed at projection layer;
- `V01-005` — closed;
- `V01-010` — partial.

## Verification

`FAST + ARCH`.

## Forbidden scope

Не реализовывать module scheduler/commit coordinator.

---

# 9. `V0.1-IS-06 — Module contracts & proposals`

## Цель

Создать structural module API и staged proposal contracts без выполнения modules.

## Обязательный контекст

- `docs/design/module-lifecycle.md`;
- `docs/design/cognitive-state.md`;
- `docs/design/dependency-rules.md`;
- `ADR-0002`, `ADR-0004`, `ADR-0005`.

## Реализовать

Минимум:

```text
CognitiveModule Protocol
ModuleDescriptor
ModuleExecutionContext
ModuleComputeRequest
ModuleComputeResult
StateWrite
StateUpdateProposal
PrivateStateContract
PrivateStateSnapshot
PrivateStateProposal
private-state descriptor
execution traits
COGNITIVE_CYCLE phase marker
```

## Required semantics

`ModuleComputeRequest` содержит только:

```text
StateProjection
own private snapshot / unavailable
ModuleExecutionContext
```

Не содержит registry/config/other modules/evaluator/Service Locator.

`ModuleComputeResult` остаётся uncommitted proposal.

Descriptor explicit объявляет reads/writes/stateful/deterministic traits.

## Tests

Минимум:

```text
tests/contract/test_module_protocol.py
tests/unit/test_module_descriptor.py
tests/unit/test_update_proposals.py
```

Добавить минимальные test-only module fixtures, но не reference synthetic graph.

## VerificationObligations

- `V01-003` — contract foundation;
- `V01-004` — module boundary integration;
- `V01-008` — contract foundation;
- `V01-012` — no Service Locator structural check.

## Verification

`FAST + ARCH`.

## Forbidden scope

Не выполнять modules и не commit'ить proposals.

---

# 10. `V0.1-IS-07 — Execution Plan Compiler`

## Цель

Компилировать immutable validated DAG и deterministic waves только из declared contracts.

## Обязательный контекст

- `docs/design/dependency-rules.md`;
- `docs/design/execution-model.md`;
- `docs/design/module-lifecycle.md`;
- `ADR-0002`, `ADR-0003`, `ADR-0005`.

## Реализовать

В `mindra.runtime.planning` или эквивалентном runtime file split:

```text
ExecutionPlanCompiler
ExecutionPlan
ExecutionWave
plan validation/fingerprint helpers
```

## Compile-time checks

Обязательны:

- unique `ModuleId`;
- schema keys существуют;
- writer == semantic owner;
- duplicate/ambiguous writer reject;
- required `CURRENT_CYCLE` read имеет producer;
- producer/output совместим;
- unsupported phase reject;
- cycle reject;
- deterministic topological wave decomposition;
- tie-break independent modules по canonical `ModuleId` только для deterministic physical ordering/evidence.

## Tests

Минимум:

```text
tests/unit/test_execution_plan.py
tests/property/test_dag_decomposition.py
tests/contract/test_plan_validation.py
```

Обязательные fixtures: linear chain, diamond, independent modules, missing producer, duplicate writer, cycle.

## VerificationObligations

- `V01-007` — closed.

## Verification

`FAST + ARCH`.

## Forbidden scope

Не выполнять wave и не mutate state.

---

# 11. `V0.1-IS-08 — PrivateStateStore`

## Цель

Создать explicit per-module private state storage до объединения с public commit.

## Обязательный контекст

- `docs/design/cognitive-state.md`;
- `docs/design/module-lifecycle.md`;
- `ADR-0004`, `ADR-0005`.

## Реализовать

Минимум:

```text
PrivateStateSlot
PrivateStateStore
PrivateStateSnapshot retrieval by owner ModuleId
private proposal validation primitives
```

## Required semantics

- каждый stateful module имеет отдельный slot;
- peer module не может получить чужой private snapshot через public API;
- private revision explicit;
- payload snapshot-safe через private contract;
- proposal привязан к base private revision;
- actual mutation пока выполняется только внутренним primitive, который в следующем шаге будет закрыт `CommitCoordinator`.

## Tests

Минимум:

```text
tests/unit/test_private_state_store.py
tests/contract/test_private_state_isolation.py
```

## VerificationObligations

- `V01-008` — substantial/partial.

## Verification

`FAST + ARCH`.

## Forbidden scope

Не давать модулям direct mutable slot/store и не реализовывать scheduler.

---

# 12. `V0.1-IS-09 — Atomic CommitCoordinator`

## Цель

Сделать единственную runtime boundary публикации staged public/private state updates.

## Обязательный контекст

- `docs/design/cognitive-state.md`;
- `docs/design/module-lifecycle.md`;
- `docs/design/execution-model.md`;
- `ADR-0003`, `ADR-0004`, `ADR-0005`;
- F31 CR-01/CR-05 только как общая causal discipline; action/training semantics здесь не реализуются.

## Реализовать

Минимум:

```text
CommitCoordinator
commit validation result/record primitives
public StateUpdateProposal validation
PrivateStateProposal validation
atomic staged application
CommitId assignment
```

## Required checks

- base `StateRevision` актуальна;
- private base revisions актуальны;
- key существует;
- producer == owner;
- write declared;
- duplicate/conflicting staged write rejected;
- `ValueContract` проходит;
- temporal context compatible;
- все validation выполнены до публикации;
- failure любого required proposal оставляет public/private state неизменным;
- stale proposal не rebased silently;
- private-only successful commit не обязан увеличивать public `StateRevision`, но имеет отдельный `CommitId`.

## Tests

Минимум:

```text
tests/contract/test_commit_authority.py
tests/property/test_atomic_commit.py
tests/property/test_stale_proposals.py
tests/state-machine/test_commit_state_machine.py
```

State-machine sequence должна включать successful commit, stale apply, invalid write, private update и failure rollback.

## VerificationObligations

- `V01-002` — commit layer;
- `V01-003` — closed;
- `V01-006` — closed;
- `V01-008` — closed at commit layer.

## Verification

`FAST + ARCH`.

## Forbidden scope

Не добавлять retry/rebase policy, partial-success commit или background mutation.

---

# 13. `V0.1-IS-10 — O0 Evidence Plane`

## Цель

Создать passive typed structural evidence до scheduler integration.

## Обязательный контекст

- `docs/design/observability-and-intervention.md`;
- `docs/design/execution-model.md`;
- `ADR-0003`, `ADR-0006`.

## Реализовать

Минимум:

```text
TraceEventEnvelope
frozen typed TraceEvent payload variants
EvidenceRecorder Protocol
InMemoryEvidenceRecorder
```

Подготовить event kinds из version README:

```text
composition_resolved
plan_compiled
cycle_started
wave_started
module_attempt_started
module_attempt_finished
commit_attempted
commit_succeeded
commit_failed
state_revision_committed
intervention_applied
cycle_finished
cycle_failed
```

Не все producers ещё существуют; payload contracts создаются сейчас, emit integration — в следующих шагах.

## Required semantics

- recorder append-only по API;
- event records immutable/snapshot-safe;
- recorder не имеет state/private write authority;
- physical timestamp, если записывается, diagnostic-only;
- evidence metadata не появляется в `StateProjection`.

## Tests

Минимум:

```text
tests/unit/test_evidence_records.py
tests/contract/test_evidence_isolation.py
```

## VerificationObligations

- `V01-009` — foundation;
- `V01-010` — substantial.

## Verification

`FAST + ARCH`.

## Forbidden scope

Не реализовывать exporter/network logging/Experience Journal.

---

# 14. `V0.1-IS-11 — WaveExecutor & Scheduler`

## Цель

Соединить plan, projections, modules, private state, commit и evidence в один deterministic `COGNITIVE_CYCLE` runtime.

## Обязательный контекст

- `docs/design/execution-model.md`;
- `docs/design/module-lifecycle.md`;
- `docs/design/cognitive-state.md`;
- `docs/design/observability-and-intervention.md`;
- `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006`.

## Реализовать

Минимум:

```text
WaveExecutor Protocol
SequentialWaveExecutor
ModuleAttempt request/result/record runtime forms
CognitiveScheduler
cycle execution result
```

## Required semantics

Для каждой wave:

1. pin один public base `StateRevision`;
2. pin own private snapshot каждого module до wave;
3. создать per-module `StateProjection`;
4. выполнить attempts через `SequentialWaveExecutor`;
5. sibling proposal не виден sibling attempt;
6. exception превращается в failed attempt evidence;
7. required failure → no wave commit;
8. successful wave → один atomic `CommitCoordinator` call;
9. следующая wave видит committed предыдущую;
10. completion/physical execution order не создаёт semantic dependency;
11. emit structural O0 trace на попытки и commit boundaries.

## Tests

Минимум:

```text
tests/integration/test_scheduler_wave_semantics.py
tests/property/test_same_base_wave.py
tests/integration/test_wave_failure_atomicity.py
tests/integration/test_scheduler_trace.py
```

Использовать test-only modules, не reference production graph из следующего шага.

## VerificationObligations

- `V01-001` — closed;
- `V01-002` — closed at runtime wave level;
- `V01-008` — runtime closed;
- `V01-009` — substantial;
- `V01-010` — closed.

## Verification

`FAST + ARCH`, затем весь существующий pytest suite.

## Forbidden scope

Не добавлять asyncio/thread/process executor, retries, optional degradation или Environment phases.

---

# 15. `V0.1-IS-12 — Reference synthetic modules`

## Цель

Создать deterministic pure reference implementations, не зависящие от runtime internals.

## Обязательный контекст

- `docs/design/module-lifecycle.md`;
- `docs/design/dependency-rules.md`;
- `ADR-0002`, `ADR-0005`.

## Реализовать

В `mindra.reference`:

```text
SyntheticSourceModule
SyntheticDoubleModule
SyntheticTripleModule
SyntheticJoinModule
```

Descriptor graph должен приводить к:

```text
Wave 0: source
Wave 1: double | triple
Wave 2: join
```

Reference modules:

- deterministic;
- pure относительно canonical Agent state;
- используют только contracts;
- не импортируют `mindra.runtime`;
- source value получают через immutable constructor settings;
- возвращают normal proposals, не special initialization mutation.

Test/failure/stateful fixtures остаются в `tests/fixtures`, если не являются частью reference profile.

## Tests

Минимум:

```text
tests/contract/test_reference_modules.py
tests/architecture/test_reference_independence.py
```

## VerificationObligations

- `V01-012` — reference/runtime independence;
- `V01-013` — foundation.

## Verification

`FAST + ARCH`.

## Forbidden scope

Не создавать Composition Root/CLI внутри `reference`.

---

# 16. `V0.1-IS-13 — Configuration & Composition Root`

## Цель

Собрать весь kernel только через explicit composition boundary.

## Обязательный контекст

- `docs/design/system-context.md`;
- `docs/design/dependency-rules.md`;
- `docs/design/execution-model.md`;
- `docs/design/cognitive-state.md`;
- `docs/design/module-lifecycle.md`;
- `ADR-0001 … ADR-0005`.

## Реализовать

Минимум:

```text
KernelProfile schema mindra.kernel-profile/v1
strict stdlib TOML parser
ImplementationRegistry
factory descriptors
build_reference_registry()
CompositionRoot
composition fingerprint
initial schema-complete CognitiveState
initial PrivateStateStore
KernelRuntime facade
configs/v0.1/reference.toml
```

`KernelRuntime` содержит compiled plan/state/private store/scheduler/evidence/composition metadata и `run_cycle()`; cognitive modules не получают facade.

## Required semantics

- unknown profile top-level keys reject;
- implementation settings strict-validated factory;
- duplicate implementation IDs fail-fast;
- no import-time decorator registration;
- registry immutable после build;
- module не читает TOML/global config;
- `CompositionRoot` — единственное место сборки;
- registered state fields schema-complete: initial `Unknown/Unavailable`, не missing;
- initial public revision = `0`;
- composition fingerprint deterministic SHA-256 над behavior-relevant normalized representation;
- `AgentRevisionId` не равен fingerprint;
- compile plan до normal run;
- emit `composition_resolved`/`plan_compiled` evidence.

## Tests

Минимум:

```text
tests/unit/test_kernel_profile.py
tests/unit/test_registry.py
tests/integration/test_composition_root.py
tests/property/test_composition_fingerprint.py
```

## VerificationObligations

- `V01-007` — composition integration;
- `V01-012` — closed architecture/composition semantics;
- `V01-013` — substantial.

## Verification

`FAST + ARCH` + integration suite.

## Forbidden scope

Не вводить DI framework, plugin discovery, global registry или Environment configuration.

---

# 17. `V0.1-IS-14 — InterventionGateway`

## Цель

Реализовать минимальную explicit research/test intervention seam без evaluator/runtime mixing.

## Обязательный контекст

- `docs/design/observability-and-intervention.md`;
- `docs/design/cognitive-state.md`;
- `ADR-0004`, `ADR-0006`.

## Реализовать

Минимум:

```text
StateInterventionSpec
InterventionPolicy / allowlist
InterventionGateway
intervention result/record
```

## Required semantics

- default reference runtime: interventions disabled;
- test/research runtime: explicit allowlist;
- intervention применяется только к committed safe boundary;
- schema/value validation сохраняется;
- создаётся новая committed state revision;
- semantic owner field не меняется;
- provenance показывает `InterventionId`, natural/base state ref и intervention source;
- intervention не masquerade как natural module write;
- Evidence Plane получает `intervention_applied`;
- private arbitrary mutation отсутствует.

## Tests

Минимум:

```text
tests/contract/test_intervention_gateway.py
tests/integration/test_intervention_lineage.py
tests/state-machine/test_intervention_commit_sequence.py
```

## VerificationObligations

- `V01-011` — closed;
- `V01-009` — intervention lineage extension.

## Verification

`FAST + ARCH` + targeted state-machine tests.

## Forbidden scope

Не реализовывать `MINDRA-Eval`, evaluator Ground Truth injection или arbitrary object patching.

---

# 18. `V0.1-IS-15 — CLI & deterministic end-to-end smoke`

## Цель

Доказать, что kernel устанавливается и запускается пользователем как целый vertical foundation slice.

## Обязательный контекст

- весь accepted `v0.1/README.md`;
- `docs/design/execution-model.md`;
- `docs/design/engineering-testing.md`.

## Реализовать

Минимум:

```text
mindra kernel-smoke --profile configs/v0.1/reference.toml
mindra validate-profile --profile ...
python -m mindra ...
```

CLI — stdlib `argparse`, делегирует composition/runtime API и не собирает modules вручную.

Reference smoke при source `2` обязан получить:

```text
Wave 0: source
Wave 1: double | triple
Wave 2: join
final join = 10
```

Добавить deterministic repeat test с `DeterministicIdFactory`:

- same semantic plan;
- same wave structure;
- same state payload/revisions;
- same logical event-kind/causal sequence;
- physical timestamps исключены из equality claim.

## Tests

Минимум:

```text
tests/integration/test_reference_profile.py
tests/integration/test_cli.py
tests/property/test_reference_determinism.py
```

## VerificationObligations

- `V01-009` — closed;
- `V01-013` — closed.

## Verification

`FULL-C0` в доступной local OS + CI evidence другой declared OS.

## Forbidden scope

Не добавлять Environment/Policy/Experience Journal или stable public SDK promises.

---

# 19. `V0.1-IS-16 — Version acceptance hardening`

## Цель

Не добавить новую feature, а доказать, что `v0.1` удовлетворяет собственному design.

## Обязательный контекст

- `docs/design/engineering-testing.md`;
- `docs/design/current.md`;
- `docs/versions/v0.1/README.md`;
- все предыдущие sections этого sequence.

## Реализовать/оформить

1. Исправить только выявленные implementation defects внутри accepted semantics.
2. Создать:

```text
docs/versions/v0.1/verification-matrix.md
```

с mapping:

```text
V01-001 … V01-014
→ concrete test/spec/command refs
→ environment profile
→ latest result/evidence refs
```

3. Проверить, что CI Linux/Windows выполняет declared gates.
4. Проверить package build из clean locked environment.
5. Проверить runtime dependency list = 0 third-party packages.
6. Проверить source documentation/comments language policy.
7. Проверить отсутствие будущих cognitive responsibilities.

## Mandatory final gate

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked lint-imports
uv run --locked pytest
uv build
```

Плюс успешный:

```text
mindra validate-profile --profile configs/v0.1/reference.toml
mindra kernel-smoke --profile configs/v0.1/reference.toml
```

и GitHub Actions Linux/Windows evidence для implementation HEAD.

## VerificationObligations

- `V01-001 … V01-014` — все должны иметь explicit PASS evidence;
- `V01-014` — закрывается только на этом шаге после clean/CI build evidence.

## Важное ограничение

Codex **не переводит самостоятельно** `v0.1` в `implemented/accepted` и не открывает `v0.2`.

После отчёта `V0.1-IS-16` выполняется отдельный ChatGPT acceptance audit. Только audit может обновить version status/current documentation.

## Forbidden scope

Никаких новых features, refactor «на будущее», Environment/Cortex/Memory work и проектирования `v0.2`.

---

# 20. Coverage VerificationObligations по шагам

| Obligation | Основные шаги закрытия |
|---|---|
| `V01-001` Same-base wave | `IS-11`, audit `IS-16` |
| `V01-002` Atomic wave commit | `IS-09`, `IS-11`, `IS-16` |
| `V01-003` Single writer authority | `IS-06`, `IS-09`, `IS-16` |
| `V01-004` Declared reads only | `IS-05`, `IS-06`, `IS-16` |
| `V01-005` Missing ≠ availability | `IS-03 … IS-05`, `IS-16` |
| `V01-006` Stale proposal rejected | `IS-09`, `IS-16` |
| `V01-007` DAG validity | `IS-07`, `IS-13`, `IS-16` |
| `V01-008` Private-state transactionality | `IS-08`, `IS-09`, `IS-11`, `IS-16` |
| `V01-009` Evidence reconstructability | `IS-10`, `IS-11`, `IS-14`, `IS-15`, `IS-16` |
| `V01-010` Observability isolation | `IS-03`, `IS-05`, `IS-10`, `IS-11`, `IS-16` |
| `V01-011` Intervention provenance | `IS-14`, `IS-16` |
| `V01-012` Dependency architecture | `IS-01`, `IS-06`, `IS-12`, `IS-13`, `IS-16` |
| `V01-013` Deterministic reference profile | `IS-12`, `IS-13`, `IS-15`, `IS-16` |
| `V01-014` Build/install reproducibility | `IS-01`, final `IS-16` |

---

# 21. Стандартный prompt для Codex

Для каждого шага используется форма:

```text
Реализуй только этап V0.1-IS-XX из docs/versions/v0.1/implementation-sequence.md.

Перед изменениями обязательно прочитай:
AGENTS.md,
docs/design/current.md,
docs/design/contract-adr-consistency-freeze.md,
docs/design/contracts/semantic-freeze-manifest.md,
docs/versions/v0.1/README.md,
соответствующий раздел docs/versions/v0.1/implementation-sequence.md,
а также перечисленные для этапа canonical design / ADR.

Сначала сверь scope этапа, prerequisites, acceptance criteria и VerificationObligations с текущим состоянием репозитория.

Не выходи за scope этапа и не реализуй последующие этапы заранее. Не меняй F31, accepted ADR, canonical design или version design, если это прямо не предусмотрено заданием.

Если обнаружится противоречие документации, отсутствующий prerequisite, необходимость semantic change либо решение, которое документация намеренно оставляет архитектору, не выбирай его самостоятельно. Остановись и опиши blocker.

Не упрощай architecture/contracts ради прохождения тестов и не ослабляй проверки. Не скрывай failing/flaky/skipped verification.

Реализуй код, tests и verification, явно требуемые этим этапом. После изменений выполни предусмотренные проверки.

В итоговом отчёте укажи:
- что реализовано;
- какие файлы изменены;
- какие проверки выполнены и их результат;
- какие VerificationObligations закрыты;
- были ли отклонения от implementation sequence;
- остались ли blockers, риски или незакрытые вопросы.

Не начинай следующий implementation step.
```

Для первого запуска заменить `XX` на `01`.

---

# 22. Первый разрешённый coding step

После синхронизации status-документов единственная разрешённая implementation работа:

```text
V0.1-IS-01 — Project bootstrap & verification shell
```

Ни `IS-02`, ни другие шаги не начинаются до завершения и audit `IS-01`.
