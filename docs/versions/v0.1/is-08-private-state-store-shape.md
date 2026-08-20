# V0.1-IS-08 — Exact PrivateStateStore clarification

## Статус

**Статус:** `accepted`  
**Область:** только `V0.1-IS-08 — PrivateStateStore`  
**Baseline:** accepted `v0.1/README.md` + `implementation-sequence.md` + `is-06-contract-shape.md` + `F31`

Этот документ устраняет implementation-level неоднозначности private-state storage перед реализацией `IS-08`. Он не меняет `F31`, transactional private-state semantics или atomic commit design; он фиксирует exact runtime boundary, необходимый будущему `CommitCoordinator`.

При конфликте приоритет имеют canonical design/F31, и implementation останавливается с blocker report.

---

# 1. Граница шага

`IS-08` создаёт runtime-owned storage causally relevant module-private state.

Он не:

- выполняет cognitive modules;
- создаёт scheduler;
- commit'ит public `CognitiveState`;
- реализует полный public+private atomic `CommitCoordinator`;
- даёт cognitive module ссылку на store/slot;
- реализует reset/lifecycle scopes;
- вводит checkpoint/restore;
- создаёт evidence recorder.

---

# 2. Exact runtime types

Physical owner: `mindra.runtime.private_state` или эквивалентный file split внутри `mindra.runtime`.

Минимальный public runtime набор:

```text
PrivateStateSlot
PrivateStateStore
```

Допустимы private/internal prepared-update helpers, если они не экспортируются через `mindra.runtime` public API.

## 2.1. PrivateStateSlot

Frozen value object:

```text
PrivateStateSlot
├── module_id: ModuleId
├── revision: PrivateStateRevision
└── value: object
```

Semantics:

- slot принадлежит ровно одному semantic `ModuleId`;
- revision explicit и неотрицательна через существующий `PrivateStateRevision`;
- value уже validated/frozen соответствующим `PrivateStateContract`;
- slot не выдаёт mutable access к backing store;
- slot сам ничего не commit'ит.

---

# 3. Store construction / initialization

`PrivateStateStore` строится runtime/composition boundary из active `ModuleDescriptor` и explicit initial private values.

Conceptual API:

```text
PrivateStateStore(
    descriptors: tuple[ModuleDescriptor, ...],
    initial_values: Mapping[ModuleId, object],
)
```

Эквивалентный controlled constructor/classmethod допустим при сохранении semantics ниже.

## 3.1. Registration

- `ModuleId` среди descriptors уникальны;
- каждый descriptor обязан быть `ModuleDescriptor`;
- store знает active semantic modules только из переданных descriptors;
- duplicate identity fail closed;
- unknown key в `initial_values` fail closed.

## 3.2. Stateful initialization

Для каждого descriptor с `ModuleStatefulness.STATEFUL`:

- `private_state` descriptor уже обязан существовать по `IS-06` invariant;
- initial value обязателен в `v0.1`;
- initial value проходит `PrivateStateContract.freeze()`;
- создаётся отдельный `PrivateStateSlot`;
- initial revision = `PrivateStateRevision.initial()`.

Причина: canonical initialization требует, чтобы required private state active composition был инициализирован до execution plan/runtime start.

`IS-08` не вводит module-specific initializer callback или hidden default value.

## 3.3. Stateless modules

Для `STATELESS` descriptor:

- slot не создаётся;
- initial value передавать запрещено;
- runtime snapshot request для зарегистрированного stateless module возвращает canonical `Unavailable()`.

Таким образом `ModuleComputeRequest.private_state` имеет однозначную v0.1 semantics:

```text
STATEFUL  -> own PrivateStateSnapshot
STATELESS -> Unavailable
```

Для active stateful module `Unavailable` после успешной initialization не является нормальным состоянием `v0.1`.

---

# 4. Snapshot retrieval

Runtime API conceptually:

```text
snapshot_for(module_id: ModuleId)
    -> PrivateStateSnapshot[object] | Unavailable
```

Semantics:

- unknown/unregistered `ModuleId` fail closed;
- registered stateless module -> `Unavailable()`;
- registered stateful module -> immutable snapshot только его slot;
- snapshot содержит module_id, current revision и snapshot-safe value;
- caller не получает `PrivateStateSlot`, backing dict или contract object через module-facing API.

Cognitive modules не получают `PrivateStateStore` reference вообще. Scheduler/runtime позднее запрашивает snapshot по module, для которого формирует `ModuleComputeRequest`.

Cross-module private-state access не становится cognitive capability только потому, что runtime store технически умеет lookup по `ModuleId`.

---

# 5. Proposal validation / preparation

`IS-08` должен реализовать private proposal validation primitive, но proposal остаётся staged.

Validation `PrivateStateProposal` минимум проверяет:

- proposal относится к зарегистрированному module;
- module является `STATEFUL`;
- proposal.module_id совпадает с owner slot;
- proposal.base_revision == current slot revision;
- concrete module `PrivateStateContract.freeze(proposal.value)` проходит;
- frozen value является тем значением, которое потенциально может быть committed;
- validation не мутирует store.

Stale base private revision -> существующий typed `StaleProposalError` (или более specific existing typed error, если canonical taxonomy к моменту реализации уже содержит его).

Proposal для stateless/unknown module -> fail closed existing typed kernel/configuration error; не использовать generic `success=False`.

---

# 6. Prepared internal update

Для будущего atomic coordinator validation должна отделяться от mutation.

Допустим internal frozen helper conceptually:

```text
_PreparedPrivateStateUpdate
├── module_id
├── expected_revision
├── next_revision
└── frozen_value
```

Exact private name/file split не является public contract.

Required semantics:

- prepared update создаётся только после successful proposal validation;
- `next_revision == current_revision.next()`;
- helper не экспортируется через `mindra.runtime.__all__`;
- cognitive module никогда его не получает;
- preparation ничего не мутирует.

---

# 7. Internal all-or-nothing apply primitive

`IS-08` может и должен предоставить **только internal runtime primitive**, который следующий `CommitCoordinator` сможет закрыть atomic public+private transaction boundary.

Conceptually:

```text
_apply_prepared(updates)
```

Перед любой mutation primitive повторно проверяет весь batch:

- module IDs уникальны внутри batch;
- каждый module зарегистрирован и stateful;
- current revision каждого slot всё ещё равна `expected_revision`;
- next revision согласована с current.next().

Только после успешной проверки **всего batch** replaces выполняются для всех slots.

Если хотя бы одна проверка fails:

```text
no private slot mutated
```

Primitive не является public cognitive/module API и не экспортируется через `mindra.runtime` facade.

`IS-08` не пытается сам обеспечить атомарность с public `CognitiveState`; это делает `IS-09` после полной public/private validation.

---

# 8. Store encapsulation

Запрещены public/module-facing:

- mutable `dict[ModuleId, PrivateStateSlot]`;
- `slot.value = ...`;
- `store[module_id] = ...`;
- arbitrary `set_private_state()` без validated proposal/revision;
- доступ cognitive module к чужому slot/store;
- direct mutation proposal method.

Если store предоставляет diagnostic read-only representation для tests/runtime, оно не должно выдавать mutable backing storage и не должно становиться module compute input.

---

# 9. Error semantics

Использовать существующую typed taxonomy без расширения ради удобства.

Минимально естественные случаи:

- duplicate active ModuleId -> `DuplicateIdentityError`;
- invalid/unknown initialization -> `ConfigurationError` или другой существующий configuration/runtime typed error;
- private payload contract failure -> исходная typed contract/schema error либо wrapped existing typed kernel error без потери причины;
- stale private proposal -> `StaleProposalError`;
- impossible private-state operation -> existing fail-closed typed error.

Generic bool/status вместо exception/result taxonomy не вводить.

---

# 10. Verification focus

Помимо tests из `implementation-sequence.md`, обязательно проверить:

1. каждый stateful descriptor получает отдельный initial slot revision `0`;
2. stateful module без initial value -> fail closed;
3. initial value проходит contract freeze;
4. mutable/invalid initial payload reject;
5. stateless module не имеет slot и snapshot -> `Unavailable`;
6. initial value для stateless module reject;
7. unknown initial ModuleId reject;
8. duplicate descriptor ModuleId reject;
9. stateful snapshot содержит только own module_id/revision/value;
10. unknown snapshot lookup reject;
11. proposal validation не мутирует store;
12. proposal value проходит private contract freeze;
13. stale base revision reject;
14. proposal stateless module reject;
15. prepared update increments exact private revision by one;
16. internal batch apply updates all prepared slots only after full prevalidation;
17. invalid member одного apply batch leaves **all** slots unchanged;
18. previous `PrivateStateSnapshot` remains immutable/stable after later apply;
19. module-facing request/store boundaries не дают peer private-state access;
20. store/backing slots не exposed as mutable mapping;
21. internal prepared/apply helpers не экспортированы как public `mindra.runtime` API.

`V01-008` достигает этим шагом уровня `substantial/partial`; полное atomic public+private closure остаётся `IS-09`.

---

# 11. Forbidden scope

Не реализовывать:

- public `CognitiveState` commit;
- `CommitCoordinator`;
- scheduler/WaveExecutor;
- module compute execution;
- Evidence Recorder;
- CompositionRoot/profile parsing;
- lifecycle reset/scopes;
- checkpoint/restore;
- parallelism/thread safety;
- hidden defaults/initializers private state;
- direct mutable private-store API.
