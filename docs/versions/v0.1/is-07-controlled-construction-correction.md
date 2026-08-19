# V0.1-IS-07 — Controlled construction correction

## Статус

**Статус:** `accepted correction clarification`  
**Область:** только correction `V0.1-IS-07 — Execution Plan Compiler`  
**Baseline:** accepted `v0.1/README.md` + `implementation-sequence.md` + `is-07-execution-plan-shape.md` + `F31`

Этот документ фиксирует implementation-level correction, обнаруженную ChatGPT audit после первой реализации `IS-07`. Он не меняет `F31`, DAG semantics, fingerprint semantics или публичный набор полей `ExecutionPlan`; он закрывает construction boundary до появления Scheduler.

---

# 1. Обнаруженный defect

Первая реализация `ExecutionPlan` использует обычный публичный dataclass constructor. `__post_init__` проверяет типы, canonical ordering, wave indices и то, что каждый active module встречается ровно в одной wave, но не может доказать полную compile-time causal consistency, которая зависит от `StateSchema` и compiler validation.

Поэтому внешняя runtime-кодовая область способна напрямую создать объект типа `ExecutionPlan`, который формально проходит constructor, но не является результатом валидной compilation. Например conceptually:

```text
descriptors: A, B
dependency: A -> B
waves: [A, B]
```

Такой plan нарушает same-cycle dependency semantics: `B` не может находиться в одной wave с `A` при edge `A -> B`.

Аналогично можно вручную передать dependency на module, отсутствующий среди descriptors, либо корректно выглядящий, но не соответствующий plan semantics `PlanFingerprint`.

Будущий Scheduler не должен повторять `ExecutionPlanCompiler` validation и не должен принимать причинно некорректный plan только потому, что caller вызвал public dataclass constructor напрямую.

---

# 2. Принятое correction-решение

`ExecutionPlan` становится **runtime-controlled construction value object**.

Для `v0.1`:

- public field shape `ExecutionPlan` не меняется;
- object остаётся immutable/frozen;
- обычный прямой `ExecutionPlan(...)` construction не является поддерживаемым public path;
- canonical creation выполняет только `ExecutionPlanCompiler` через internal/private construction helper в `mindra.runtime.planning`;
- helper не экспортируется как public runtime API;
- Scheduler/Composition в последующих шагах получают уже compiled `ExecutionPlan` и имеют право доверять compiler-established invariants;
- не добавлять повторную schema/DAG compilation в Scheduler.

Предпочтительная реализация:

```text
@dataclass(frozen=True, slots=True, init=False)
class ExecutionPlan:
    ... existing fields ...

internal _build/_from_compiler helper
    -> устанавливает поля только после compiler validation/decomposition/fingerprint
```

Эквивалентный internal mechanism допустим только если обычный внешний constructor больше не позволяет создать произвольный `ExecutionPlan` с неподтверждёнными compile invariants.

Не вводить global registry, construction service или новый public factory abstraction.

---

# 3. Compiler semantics сохраняются

Порядок successful compilation остаётся:

```text
validate descriptors/schema
-> derive dependencies
-> deterministic wave decomposition
-> build canonical fingerprint
-> allocate ExecutionPlanId
-> internal construction ExecutionPlan
```

Failed semantic compilation по-прежнему не расходует `ExecutionPlanId`.

Internal construction не должен самостоятельно выбирать другую DAG/fingerprint semantics.

---

# 4. Verification correction

Добавить regression evidence минимум для следующего:

1. обычный внешний `ExecutionPlan(...)` construction недоступен/отклоняется;
2. `ExecutionPlanCompiler.compile(...)` по-прежнему возвращает корректный immutable `ExecutionPlan` с тем же exact field shape;
3. linear/diamond/independent/empty plans не регрессируют;
4. failed compile по-прежнему не расходует deterministic `ExecutionPlanId`;
5. fingerprint semantics и input-order independence не меняются;
6. future caller не получает public bypass, позволяющий вручную подставить dependency/wave/fingerprint вместо compiler result.

`V01-007` нельзя считать окончательно закрытой до прохождения этого correction и полного verification gate.

---

# 5. Forbidden scope correction

Correction не должен добавлять:

- Scheduler;
- WaveExecutor;
- module execution;
- `PrivateStateStore`;
- `CommitCoordinator`;
- Composition Root;
- evidence recorder;
- state mutation;
- новый public plan builder/service;
- изменение DAG/fingerprint semantics, кроме необходимого controlled-construction boundary.
