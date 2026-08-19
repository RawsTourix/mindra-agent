# V0.1-IS-06 — Exact module contract clarification

## Статус

**Статус:** `accepted`  
**Область:** только `V0.1-IS-06 — Module contracts & proposals`  
**Baseline:** accepted `v0.1/README.md` + `implementation-sequence.md` + `F31`

Этот документ устраняет implementation-level неоднозначности, обнаруженные перед открытием `IS-06`. Он не меняет `F31`, `DU-05` или смысл accepted `v0.1`; он фиксирует exact Python-facing shape тех primitives, которые впервые должны появиться в `IS-06`.

Если этот документ конфликтует с canonical semantic design, приоритет имеет `F31`/canonical design и работа останавливается с blocker report.

---

# 1. Implementation revision

Поле `ModuleDescriptor.implementation_revision` не является causal identity и не является monotonic kernel revision.

Для `v0.1` вводится отдельный frozen value object:

```text
ImplementationRevision
└── value: str
```

Semantics:

- opaque provenance/version token concrete implementation;
- непустой;
- без leading/trailing whitespace;
- equality semantics only;
- numerical ordering/increment semantics отсутствуют;
- допустимы version-like или source-revision-like значения (`v1`, `1.2.0`, short/full revision token), если они проходят простую fail-closed validation;
- не использовать `StateRevision`, `CompositionRevision`, `AgentRevisionId` или `ImplementationId` вместо него.

Physical owner: `mindra.contracts.modules` (или эквивалентный file split внутри `mindra.contracts`).

---

# 2. Phase и execution traits

Exact foundation types `IS-06`:

```text
ExecutionPhase
└── COGNITIVE_CYCLE

ModuleStatefulness
├── STATELESS
└── STATEFUL

DeterminismMode
├── DETERMINISTIC
└── STOCHASTIC

ExecutionTraits
├── statefulness: ModuleStatefulness
└── determinism: DeterminismMode
```

Все объекты immutable.

`IS-06` не вводит resource hints, batching traits, async traits или optional/skippable policy.

---

# 3. Private-state contract foundation

Вводится structural contract:

```text
PrivateStateContract[T]
├── validate(value) -> None
└── freeze(value) -> T
```

Он описывает snapshot-safety/validation private payload и не является store.

`ValueContract[T]` может структурно удовлетворять этому Protocol, но shared-state `StateFieldSpec` и private-state descriptor остаются разными semantic boundaries.

Exact descriptor:

```text
PrivateStateDescriptor[T]
└── contract: PrivateStateContract[T]
```

Consistency invariant `ModuleDescriptor`:

```text
STATELESS -> private_state is None
STATEFUL  -> private_state is PrivateStateDescriptor
```

`IS-06` не создаёт `PrivateStateStore` и не выполняет initialization lifecycle.

---

# 4. Private-state snapshot/proposal

Exact foundation shape:

```text
PrivateStateSnapshot[T]
├── module_id: ModuleId
├── revision: PrivateStateRevision
└── value: T

PrivateStateProposal[T]
├── module_id: ModuleId
├── base_revision: PrivateStateRevision
├── module_attempt_id: ModuleAttemptId
└── value: T
```

Это immutable staged values.

Validation against concrete `PrivateStateContract`/store ownership выполняется позднее соответствующим runtime boundary (`IS-08/IS-09`); `IS-06` не commit'ит private proposal.

Stateful module input имеет type-level semantics:

```text
PrivateStateSnapshot[object] | Unavailable
```

Модуль получает только собственный snapshot/unavailable. Cross-module private snapshot в request запрещён semantic contract и позднее проверяется runtime.

---

# 5. ModuleExecutionContext

Exact минимальный context `v0.1`:

```text
ModuleExecutionContext
├── module_attempt_id: ModuleAttemptId
├── base_state_revision: StateRevision
├── logical_time: LogicalTime
└── phase: ExecutionPhase
```

Не добавлять в context:

- Composition Root;
- registry;
- raw config;
- concrete other modules;
- evaluator/research ground truth;
- service container;
- profile/experiment labels;
- wall-clock time.

Новые context fields требуют отдельного version-design clarification.

---

# 6. StateWrite и StateUpdateProposal

Exact shape `IS-06`:

```text
StateWrite[T]
├── key: StateKey[T]
├── availability: Availability[T]
└── provenance: StateProvenance

StateUpdateProposal
├── base_state_revision: StateRevision
├── producer: ModuleId
├── module_attempt_id: ModuleAttemptId
└── writes: tuple[StateWrite[object], ...]
```

Semantics:

- immutable;
- proposal остаётся uncommitted;
- duplicate write path внутри одного proposal fail closed;
- proposal не проверяет write authority/schema ownership/stale base — это `CommitCoordinator` (`IS-09`);
- `StateWrite` не изменяет `CognitiveState`;
- payload должен уже удовлетворять базовой snapshot-safety `StateEntry`/availability semantics, но schema-specific `ValueContract` validation окончательно выполняется commit boundary;
- provenance может быть создана module compute и позднее обязана быть проверена runtime against descriptor/context.

---

# 7. ModuleDescriptor

Exact минимальный shape:

```text
ModuleDescriptor
├── module_id: ModuleId
├── implementation_id: ImplementationId
├── implementation_revision: ImplementationRevision
├── reads: tuple[ReadSpec[object], ...]
├── writes: tuple[StateKey[object], ...]
├── private_state: PrivateStateDescriptor[object] | None
├── phases: frozenset[ExecutionPhase]
└── traits: ExecutionTraits
```

Required validation:

- descriptor immutable;
- `reads`/`writes` не содержат duplicate `StatePath`;
- `phases` непустой и для `v0.1` содержит только `COGNITIVE_CYCLE`;
- statefulness/private-state consistency из раздела 3;
- descriptor ничего не знает о runtime registry/composition objects;
- write ownership относительно `StateSchema` пока не проверяется: это `IS-07`.

Read/write overlap сам по себе не запрещён: feedback через предыдущий committed state может быть допустим согласно freshness semantics.

---

# 8. ModuleComputeRequest / Result

Exact request:

```text
ModuleComputeRequest
├── state: StateProjection
├── private_state: PrivateStateSnapshot[object] | Unavailable
└── context: ModuleExecutionContext
```

Никаких других ambient dependencies в request нет.

Exact result `IS-06`:

```text
ModuleComputeResult
├── state_update: StateUpdateProposal
└── private_state_update: PrivateStateProposal[object] | None
```

Accepted `v0.1` допускает optional bounded diagnostics, но `IS-06` **не фиксирует ad-hoc diagnostic payload**. Diagnostic/evidence representation появляется в соответствующем Evidence step; до этого не добавлять `dict[str, Any]`, logger payload или новый diagnostic contract только ради будущего использования.

---

# 9. CognitiveModule Protocol

Structural Protocol:

```text
CognitiveModule
├── descriptor: ModuleDescriptor
└── compute(ModuleComputeRequest) -> ModuleComputeResult
```

`compute` синхронный в `v0.1` contract. Async/thread/process execution не входит в `IS-06`.

`compute` не получает store и не выполняет commit.

Test-only module fixtures допустимы только для проверки structural Protocol/request/result и не являются reference synthetic modules из `IS-12`.

---

# 10. Verification focus

Помимо tests из `implementation-sequence.md`, `IS-06` обязан проверить:

- structural Protocol conformance test-only module;
- request не exposes full `CognitiveState`, registry/config/evaluator/service locator;
- descriptor duplicate reads/writes reject;
- descriptor statefulness/private-state mismatch reject;
- unsupported/empty phase set reject;
- proposal duplicate writes reject;
- result/proposals immutable;
- public/private proposals остаются staged и сами не меняют state/store;
- `V01-012` no-Service-Locator проверяется структурой public request/descriptor API, без добавления runtime locator.

`IS-06` не выполняет module compute через scheduler/executor и не проверяет actual atomic commit — это последующие steps.
