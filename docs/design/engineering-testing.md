# Engineering Testing MINDRA

## Статус документа

**Design Update:** `DU-29 — Engineering Testing`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет каноническую семантику инженерной проверки реализации MINDRA поверх `DU-01 … DU-28`.

Ключевое решение `DU-29`:

- Engineering Testing является **внешним Verification Plane**, а не cognitive module и не `MINDRA-Eval`;
- research usefulness и engineering correctness проверяются разными системами;
- accepted architectural invariants должны иметь явный `VerificationObligation`, а где практически возможно — machine-checkable enforcement/test;
- testing строится слоями: static architecture, unit, contract/conformance, property/state-machine, integration/runtime, fault/recovery, persistence/migration и system/backend suites;
- failure semantics тестируются намеренно, а не считаются второстепенным edge case;
- test oracle может видеть privileged state только внутри Testing Plane и не должен создавать production-path leakage;
- exact/bitwise assertions разрешены только там, где соответствующий contract/reproducibility claim действительно этого требует;
- golden artifacts ограничиваются стабильными contract surfaces и не используются как основной oracle для stochastic neural behavior;
- flaky test не является нормальным состоянием CI и требует отдельной quarantine/repair semantics;
- concrete test framework, CI provider, property-testing library, import linter и coverage tool намеренно не фиксируются.

Документ опирается на:

- [`dependency-rules.md`](dependency-rules.md) — import/composition/Service Locator invariants;
- [`execution-model.md`](execution-model.md) — logical time и causal boundaries;
- [`cognitive-state.md`](cognitive-state.md) — ownership/revisions/staleness;
- [`module-lifecycle.md`](module-lifecycle.md) — module protocol/scheduling/atomic commits;
- [`observability-and-intervention.md`](observability-and-intervention.md) — passive evidence и declared interventions;
- [`modules/action-boundary.md`](modules/action-boundary.md) — authorization/commit/dispatch/reconciliation;
- [`experience-data-replay.md`](experience-data-replay.md) — immutable data lineage и leakage boundaries;
- [`training-lifecycle.md`](training-lifecycle.md) — candidate/validation/activation/rollback;
- [`checkpoint-reproducibility-compute.md`](checkpoint-reproducibility-compute.md) — restore/integrity/reproducibility;
- [`mindra-eval.md`](mindra-eval.md) — research evaluation, которое Engineering Testing не заменяет.

Документ намеренно **не** выбирает:

- `pytest`, `unittest` или другой test runner;
- Hypothesis/другую property-testing library;
- Import Linter/другой architecture-test tool;
- GitHub Actions/другой CI provider;
- конкретный coverage percentage;
- обязательное mutation-testing средство;
- точные CI timing thresholds;
- конкретный mocking framework;
- конкретный accelerator matrix;
- exact directory layout будущих tests.

---

# 1. Цель DU-29

`DU-28` отвечает на вопрос:

> существует ли функциональный/исследовательский эффект?

`DU-29` отвечает на другой:

> соблюдает ли конкретная реализация MINDRA принятые contracts, invariants и failure semantics?

Канонически:

```text
Engineering correctness
≠
Research validity
```

Примеры:

- Workspace может идеально проходить contract tests и не дать полезного research effect;
- эксперимент может показать интересный эффект, но быть недействительным из-за race/stale-state bug;
- Policy unit test не доказывает качество поведения;
- высокий benchmark score не доказывает, что `Action Commit` или provenance реализованы правильно.

---

# 2. Verification Plane boundary

Engineering Testing находится **вне Agent cognition**.

Testing Runtime может:

- создавать deterministic test compositions;
- подменять implementations test doubles;
- генерировать inputs/sequences;
- читать Evidence Plane;
- использовать test-only oracle state;
- инъецировать declared faults;
- проверять snapshots/manifests/artifacts;
- запускать migration/compatibility tests;
- измерять invariant coverage.

Testing Runtime не может normal-production способом:

- публиковать test oracle в `CognitiveState`;
- добавлять test-only Service Locator;
- давать cognitive modules прямой доступ к mocks/fault controller;
- менять production semantics ради удобства тестирования;
- скрыто ослаблять contract в test profile.

Test hooks допустимы только как explicit infrastructure boundary, не как второй production API.

---

# 3. Verification Obligation

Каждый accepted invariant, который имеет engineering manifestation, должен получить `VerificationObligation`.

Conceptually:

```text
accepted invariant
      ↓
VerificationObligation
├── source design / ADR
├── target boundary
├── enforcement class
├── required test classes
├── failure examples
├── supported profiles
└── evidence refs
```

Не каждый invariant обязан иметь обычный unit test.

Допустимые enforcement classes:

```text
static
schema/type
runtime assertion
contract/conformance
property/invariant
state-machine/model-based
integration
fault injection
round-trip/migration
manual review only
not currently machine-checkable
```

Если invariant пока нельзя разумно автоматизировать, это должно быть явно известно, а не молча считаться covered.

---

# 4. Verification Matrix

Проект должен иметь versioned `VerificationMatrix`, связывающую:

```text
DU / ADR / Contract invariant
        ↓
verification obligation
        ↓
test specs
        ↓
CI tiers / environments
        ↓
latest evidence
```

Цель — не максимальный line coverage, а **coverage архитектурных обязательств**.

Канонически:

```text
line coverage
≠
invariant coverage
```

Высокое покрытие строк не доказывает, что проверены:

- illegal dependency;
- atomic commit;
- staleness;
- privileged leakage;
- duplicate dispatch;
- candidate activation boundary;
- restore integrity.

---

# 5. Слои инженерного тестирования

## 5.1. Static architecture tests

Проверяют свойства, не требующие запуска полноценного Agent:

- import directions;
- forbidden dependencies;
- acyclic/layer rules;
- отсутствие concrete provider SDK в независимом core;
- отсутствие Training/Evaluation imports в Agent runtime там, где они запрещены;
- composition-only registry usage;
- schema/contract registry consistency;
- forbidden global mutable/service-locator patterns, где их можно обнаружить статически.

Static architecture test не заменяет runtime ownership test.

## 5.2. Unit tests

Проверяют локальную семантику небольшого компонента с минимальным context.

Подходят для:

- deterministic transforms;
- validation;
- comparison/normalization policies;
- serialization helpers;
- pure state transitions;
- known failure classifications.

Не являются evidence функциональной полезности subsystem.

## 5.3. Contract / conformance tests

Любая заменяемая implementation должна проходить общий conformance suite своего semantic contract.

Примеры:

```text
Cortex backend
Memory backend
Environment adapter
Policy implementation
Checkpoint storage
No*/Dummy/control implementation
```

Conformance suite проверяет observable contract, а не private implementation details.

Capability-dependent проверки применяются только если implementation заявляет соответствующую capability.

## 5.4. Property / invariant tests

Проверяют свойства на широком пространстве автоматически генерируемых inputs.

Особенно подходят для:

- revision monotonicity;
- stable identities;
- no in-place rewrite;
- deterministic normalization;
- serialization round-trip;
- provenance preservation;
- valid/invalid schema combinations;
- idempotency/deduplication laws.

## 5.5. Stateful / model-based tests

Проверяют последовательности операций относительно упрощённой reference model.

Приоритетные targets MINDRA:

```text
CognitiveState revisions
Scheduler waves / commits
Goal lifecycle
Memory lifecycle
Workspace admission/eviction
Executive budget ledger
Action commit/dispatch/retry/reconcile
Experience Journal append/derive
Training candidate/activate/rollback
Checkpoint capture/restore/migrate
```

Stateful tester должен уметь проверять invariant после каждого шага/commit boundary.

## 5.6. Integration tests

Проверяют несколько boundaries вместе без требования research-scale task quality.

Например:

```text
Perception → CognitiveState → World Model
Policy → Action Gate → Environment
Experience Journal → Dataset Builder → Training Runtime
Training Runtime → candidate → activation
Checkpoint → restore → continuation
EvaluationCondition → Evaluation Runtime → report
```

Integration test отвечает на вопрос «правильно ли компоненты стыкуются», а не «полезна ли архитектура».

## 5.7. Fault-injection / recovery tests

Failure semantics являются first-class.

Testing Plane должен уметь намеренно создавать faults на declared boundaries:

- Cortex timeout/provider unavailable/invalid output;
- storage read/write/corruption failure;
- stale revision;
- module compute failure до commit;
- OOM/resource exhaustion;
- dispatch definite failure;
- lost acknowledgement / `execution_unknown`;
- duplicate dispatch/retry;
- partial execution model, где environment это поддерживает;
- checkpoint interruption/corruption/missing delta base;
- optimizer/training NaN/failure;
- candidate validation failure;
- migration incompatibility;
- evaluator artifact incompleteness.

Fault injector не должен создавать production path, которого нет без тестов.

## 5.8. Persistence / migration / compatibility tests

Обязательные классы:

- serialize → deserialize semantic round-trip;
- checkpoint capture → restore;
- full-system clone/branch где scope это обещает;
- old schema → migration → new schema;
- missing/unknown revision failure;
- representation revision compatibility;
- index rebuild preserving canonical Memory identity;
- candidate revision остаётся candidate после restore;
- corrupted artifact fail-closed.

---

# 6. Architecture/dependency verification

`DU-02` должен стать машинно enforceable настолько, насколько позволяет будущая package structure.

Проверяются минимум:

```text
no forbidden import
no forbidden dependency cycle
no runtime Service Locator access
no cognitive import of Evaluation/Training owner
provider SDK isolated to adapter/provider boundary
Composition Root may know concrete implementations
```

Конкретный import graph tool не фиксируется.

Architecture exceptions нельзя оформлять случайным test ignore. Они требуют explicit reviewed exception/ADR/design update, если меняют semantic rule.

---

# 7. Ownership и write-authority tests

Недостаточно проверить только imports.

Runtime tests должны доказывать, что:

- модуль не коммитит чужой namespace;
- failed attempt не частично мутирует committed state;
- stale proposal не silently rebase'ится;
- Memory Regulation не пишет Store напрямую в обход Memory Core;
- Planner не создаёт `SelectedActionIntent`;
- Action Gate не переписывает Policy intent без override provenance;
- Training Runtime не мутирует live active revision до activation;
- Evaluation/Testing Plane не пишет privileged data в Agent state.

Предпочтительна fail-closed semantics для illegal write.

---

# 8. Scheduler / temporal / atomicity tests

Для `DU-03 … DU-05` обязательны сценарии:

```text
valid DAG
cycle rejection
parallel wave reads same base revision
atomic multi-output commit
one attempt fails → no partial commit
stale base revision → explicit rejection/recompute
logical time monotonicity
Decision Window boundaries
Action Commit uniqueness
Outcome Commit ordering
```

Wall-clock ordering не должен использоваться как oracle logical causality.

При параллельной implementation tests должны намеренно варьировать physical completion order и проверять одинаковую committed semantics там, где она заявлена deterministic.

---

# 9. Data visibility / oracle leakage tests

Это обязательный cross-plane class.

Testing Runtime должен уметь доказать, что normal Agent composition не получает:

- `Hidden World State`;
- ResearchAnnotation/evaluator-only fields;
- future outcome;
- oracle action;
- test expected value;
- hidden intervention metadata, если она не agent-visible по condition.

Рекомендуемый pattern:

```text
privileged sentinel value
        ↓
Research/Test Plane only
        ↓
run normal Agent path
        ↓
assert sentinel absent from all agent-visible boundaries
```

Leakage test должен проверять не только final observation, но и Cortex context, Workspace, Memory writes, TrainingSample visibility policy и logs/artifacts, которые могут быть случайно возвращены Agent.

---

# 10. Cortex/backend conformance

Каждый Cortex adapter проверяется на заявленные capabilities.

Обязательные classes где применимо:

- semantic request normalization;
- backend-specific formatting stays inside adapter;
- structured output success/failure;
- unsupported capability fail explicitly;
- timeout/provider failure semantics;
- context overflow semantics;
- model/backend/adapter revision provenance;
- no silent provider fallback;
- no hidden Memory/state access;
- multilingual test fixtures для заявленных validated languages.

Neural output exact string не является универсальным golden oracle.

---

# 11. Representation / Memory tests

Обязательные properties:

```text
MemoryRecord identity survives index rebuild
re-encoding ≠ new semantic memory
feature-space revision mismatch detected
old/new embeddings not silently mixed
consolidation creates derived record
raw episode not rewritten
source/support/conflict lineage preserved
retrieval does not mutate source record
Agent Memory Replay ≠ new natural experience
```

Если approximate retrieval backend stochastic, test должен проверять contract properties/tolerances, а не один конкретный ordering без соответствующей гарантии.

---

# 12. Action lifecycle tests

`DU-24` требует отдельной state-machine suite.

Минимальные transitions:

```text
intent → reject
intent → authorize → commit → dispatch → success
intent → authorize → commit → definite dispatch failure
intent → authorize → commit → execution_unknown
execution_unknown → reconcile applied
execution_unknown → reconcile not applied
same dispatch_id retry with idempotent adapter
stale intent → reject/reselect
normalization preserves semantics
behavior-changing override has explicit record
```

Ключевые invariants:

- один logical `Action Commit` не дублируется retry;
- post-commit failure не удаляет commit;
- `execution_unknown` не treated as not-executed;
- blind retry запрещён без declared safety semantics;
- accepted acknowledgement не приравнивается success.

---

# 13. Training lifecycle tests

Обязательны:

- pinned base revisions;
- dataset/data-visibility lineage;
- explicit GradientFlowPolicy;
- frozen groups действительно не обновляются;
- forbidden cross-module gradient не проходит;
- failed/OOM/NaN attempt не мутирует active Agent;
- candidate revision не active до validation/activation;
- in-flight Decision Window не получает mid-window revision swap;
- rejected candidate остаётся inactive;
- rollback является новым activation event;
- behavior revision source experience сохраняется;
- privileged supervision требует explicit profile.

Numeric learning quality относится к MINDRA-Eval, если вопрос не является чистым implementation sanity check.

---

# 14. Checkpoint / reproducibility tests

Проверяются отдельно promises конкретного scope/profile.

Минимально:

```text
weights-only != training-resume
manifest commit only after required artifact verification
corruption detected
missing artifact fails
missing delta base fails
active/candidate restore separately
RNG current state restored where claimed
Agent/Environment causal cut aligned for full-system scope
execution_unknown preserved
migration lineage preserved
exact profile not silently downgraded
portable restore tested only against declared compatibility
```

Bitwise comparison используется только для profile, который его обещает.

Для stochastic/accelerator code deterministic test mode может быть отдельным CI profile и не обязан совпадать по performance с production mode.

---

# 15. Evaluation infrastructure tests

`MINDRA-Eval` само является software и поэтому тоже требует engineering tests.

Проверяются:

- `EvaluationCondition` manifest completeness;
- invalid condition detection;
- Ground Truth isolation;
- replicate/nesting schema validation;
- MetricSpec availability/censoring semantics;
- no `execution_unknown → 0` implicit coercion;
- Policy/Gate attribution linkage;
- ResourceMatchProfile фактическая проверка;
- confirmatory plan immutability/versioning;
- result lineage до source events/artifacts;
- composite score не уничтожает typed metrics.

Эти tests не доказывают научную корректность конкретного statistical method; они доказывают соблюдение его заявленного contract.

---

# 16. Golden tests

Golden/snapshot artifacts разрешены только для **стабильных contract surfaces**, например:

- canonical serialization fixture;
- small deterministic MicroWorld trajectory;
- manifest/schema fixture;
- known migration result;
- deterministic control implementation.

Не рекомендуется делать главным oracle:

```text
exact LLM response
exact neural logits after unrelated framework update
large opaque binary snapshot
full report HTML bytes
```

Golden update policy:

1. изменение не выполняется автоматически;
2. diff должен быть reviewable;
3. updater обязан указать, какое design/contract изменение делает новый golden правильным;
4. неожиданный массовый golden rewrite считается сигналом regression, а не routine maintenance.

---

# 17. Flaky-test policy

Flaky test не считается «зелёным, если rerun прошёл».

При обнаружении flaky behavior нужно:

1. сохранить evidence/seed/environment;
2. классифицировать источник nondeterminism;
3. отличить production nondeterminism от test harness bug;
4. либо исправить test/system, либо временно quarantine с owner/reason;
5. не оставлять permanent `xfail`/rerun как замену исправлению.

Quarantined test не считается удовлетворённым VerificationObligation.

---

# 18. Determinism и stochastic systems

Engineering test должен объявлять, что именно сравнивается:

```text
bitwise equality
semantic equality
bounded numeric tolerance
same invariant outcome
same distributional property
```

`seed=42` сам по себе не является determinism contract.

Если backend/platform не обещает exact reproducibility, test не должен создавать ложный exact oracle.

При этом deterministic debug/test profile может fail fast на известных nondeterministic operations, если concrete framework это поддерживает.

---

# 19. Test doubles и control conformance

`No*`, Dummy и research controls должны иметь declared `ConformanceProfile`.

Пример:

```text
NoMemory
→ capability absent

DummyMemory
→ Memory contract present, deterministic limited semantics

ShuffledMemoryControl
→ Memory retrieval contract present, deliberately altered ranking semantics
```

Test suite не должна требовать от `NoX` capability, которую он по определению объявляет отсутствующей.

Но control implementation обязана соблюдать остальные boundary/provenance/failure invariants.

---

# 20. Test Environment Profile

Каждый nontrivial test run должен иметь воспроизводимый environment profile по необходимости:

```text
software/runtime revision
OS/platform
CPU/GPU/accelerator class
backend/provider mode
network/offline mode
precision/determinism mode
resource limits
fault profile
```

Это не обязательно полный `ExperimentManifest`, но accelerator/backend-specific failure нельзя считать общим без соответствующего profile evidence.

---

# 21. CI tiers

Точные names/provider не фиксируются, но архитектура CI должна поддерживать классы примерно следующего смысла.

## Tier A — static / very fast

- formatting/lint/type/schema sanity;
- architecture/import contracts;
- docs/registry reference checks;
- pure unit tests.

## Tier B — deterministic CPU core

- contract/conformance suites;
- property tests с bounded workload;
- scheduler/state/action/data/checkpoint small integration;
- deterministic controls/MicroWorld.

## Tier C — extended stateful/fault/integration

- longer generated state machines;
- fault injection;
- migration/backward compatibility;
- restart/restore;
- race/order perturbation;
- soak-like bounded suites.

## Tier D — accelerator / local-model / backend

- GPU-specific paths;
- trainable components;
- local Cortex implementations;
- numeric/dtype/device compatibility;
- accelerator checkpoint/restore.

## Tier E — remote/provider/system compatibility

- remote Cortex/API contracts;
- optional deployment adapters;
- provider-specific retry/rate/error semantics.

Tier membership не является proxy test importance: critical static invariant может жить в самом быстром tier.

---

# 22. CI gating

Для изменения production/research implementation merge gate должен зависеть от релевантных VerificationObligation, а не только от общего числа passing tests.

Conceptually:

```text
changed boundaries
        ↓
required verification set
        ↓
run applicable CI tiers
        ↓
all required obligations satisfied
        ↓
merge eligible
```

Slow/accelerator/provider tests могут использовать отдельные schedules/manual gates, но skipped required test должен быть явно виден как **not verified**, а не pass.

---

# 23. Fault injection и testability hooks

Testability не должна создавать скрытую production architecture.

Допустимы:

- adapter test doubles;
- fake clock/logical clock driver;
- deterministic RNG injection;
- declared fault-capable storage/transport adapters;
- Intervention Gateway;
- simulated Environment failures.

Запрещены:

- global `TEST_MODE` меняющий semantic rules;
- test-only direct mutation чужого private state в normal path;
- production Service Locator ради mocks;
- bypass authorization/commit validation только в tests.

---

# 24. Security-like fail-closed invariants

Некоторые нарушения должны тестироваться как hard failure, а не warning:

- privileged Ground Truth попал в Agent input;
- illegal owner пишет чужой committed namespace;
- corrupted required checkpoint artifact;
- unknown mandatory schema/revision;
- unsafe blind retry `execution_unknown`;
- candidate revision активируется без разрешённой activation boundary;
- hidden concrete dependency нарушает canonical architecture, если правило machine-enforceable.

Точный exception/status API появится позже.

---

# 25. Backward compatibility и migrations

До появления public API compatibility policy всё равно нужна внутренняя дисциплина persisted artifacts.

Каждая migration должна иметь tests минимум на:

```text
old valid fixture
→ migrate
→ new valid fixture

invalid old fixture
→ explicit failure

migration twice
→ declared idempotent/non-idempotent semantics

source lineage
→ preserved
```

Нельзя просто обновить fixture так, чтобы старый persisted format исчез из test history, пока он ещё должен поддерживаться.

---

# 26. Coverage semantics

MINDRA отслеживает минимум три разных понятия:

```text
code coverage
contract/conformance coverage
architectural invariant coverage
```

Дополнительно полезны:

```text
failure-mode coverage
migration/schema coverage
backend/capability matrix coverage
```

Ни один процент line coverage не становится canonical quality gate сам по себе.

---

# 27. Mutation testing

Mutation testing допустим как optional quality instrument:

> сломать условие/invariant намеренно и проверить, что suite это обнаруживает.

Особенно полезно для critical validation/authorization/provenance logic.

Но конкретный mutation tool и required mutation score не фиксируются.

---

# 28. Machine-checkable invariant registry

Перед `DU-31` должна существовать возможность построить отчёт:

```text
Invariant I-0042
source: ADR-0024
status: machine-enforced
checks:
- action state-machine property test
- dispatch dedup integration test
- static schema constraint
latest evidence: ...

Invariant I-0088
source: ADR-0017
status: research-only / not engineering invariant
verification: N/A here
```

Таким образом DU-29 не требует превращать **research hypothesis** в unit test.

---

# 29. Failure semantics Engineering Testing

Test result должен различать:

```text
pass
fail
error in test harness
skipped / capability unavailable
not applicable
quarantined
inconclusive due environment
not run
```

Не считать всё кроме `pass` обычным fail и не считать skip pass.

Exact status enum не frozen.

---

# 30. Completion gate DU-29

`DU-29` считается завершённым, если:

1. `Engineering Testing ≠ MINDRA-Eval` закреплено;
2. существует `VerificationObligation / VerificationMatrix` semantics;
3. architecture/unit/contract/property/stateful/integration/fault/persistence test layers определены;
4. critical cross-plane leakage/ownership/action/training/checkpoint invariants имеют test strategy;
5. deterministic vs stochastic assertion semantics разведены;
6. golden/flaky/migration policy определены;
7. CI tiers/gating определены без выбора provider;
8. test doubles/control conformance определены;
9. candidate machine contract создан;
10. ADR фиксирует выбранную verification architecture;
11. research/tool pass сохранён отдельно;
12. `current.md` переводит проект на `DU-30`.
