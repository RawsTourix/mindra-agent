# ADR-0029 — Layered invariant-driven Engineering Verification вместо test-suite-by-convention

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-29 — Engineering Testing`

---

# 1. Контекст

После `DU-28` MINDRA имеет большое число принятых invariants на уровнях:

- dependency/composition;
- temporal/scheduler/state ownership;
- cognitive subsystem contracts;
- action lifecycle;
- data lineage/visibility;
- training revisions;
- checkpoint/restore;
- evaluation infrastructure.

Нужно определить engineering testing architecture, которая будет проверять соответствие реализации design, но не подменять research evaluation.

---

# 2. Вариант A — Обычная пирамидальная test suite

Conceptually:

```text
много unit tests
+ немного integration tests
+ несколько end-to-end tests
```

## Плюсы

- знакомый подход;
- легко начать;
- хорошо работает для обычной application logic.

## Минусы

- архитектурные invariants могут остаться без явного owner/test;
- high line coverage не гарантирует dependency/ownership/causal correctness;
- трудно увидеть, какие ADR реально machine-enforced;
- failure/recovery часто остаются случайными edge cases;
- contract tests заменяемых providers могут фрагментироваться.

**Решение:** недостаточно как canonical verification architecture.

---

# 3. Вариант B — End-to-end/system tests как основной oracle

Запускается полный Agent/MicroWorld и сравниваются ожидаемые trajectories.

## Плюсы

- проверяет много компонентов вместе;
- ловит интеграционные ошибки;
- приближено к реальному использованию.

## Минусы

- плохо локализует root cause;
- stochastic/neural components делают exact goldens хрупкими;
- illegal architecture может давать правильный end result;
- трудно systematically покрыть stale/fault/migration states;
- end-task success начинает смешиваться с research evaluation.

**Решение:** system tests нужны как слой, но не как основа всей verification architecture.

---

# 4. Вариант C — Contracts + examples only

Каждый contract имеет набор hand-written example tests.

## Плюсы

- хорошо соответствует модульности;
- удобно для adapters/backends;
- меньше central infrastructure.

## Минусы

- последовательностные invariants плохо покрываются examples;
- unexpected action sequences/stale states/retries могут не встретиться;
- architecture/dependency и cross-plane leakage остаются отдельно;
- нет общей связи ADR invariant → test evidence.

**Решение:** contract conformance принят как важный слой, но недостаточен отдельно.

---

# 5. Вариант D — Layered invariant-driven Verification Plane

Conceptually:

```text
Accepted Design / ADR / Contracts
             ↓
   VerificationObligation registry
             ↓
      VerificationMatrix
             ↓
┌────────────┼────────────────────────────┐
│ static     │ unit / contract           │
│ property   │ state-machine             │
│ integration│ fault/recovery            │
│ round-trip │ migration/backend/system  │
└────────────┼────────────────────────────┘
             ↓
      CI / Verification Gates
             ↓
      Engineering Evidence
```

## Плюсы

- прямо связывает implementation evidence с accepted design;
- позволяет видеть непокрытые invariants;
- поддерживает architecture/import enforcement;
- property/stateful testing подходит причинно богатому runtime;
- failure semantics first-class;
- одинаковые contract suites применимы к сменным providers/controls;
- CI может gating делать по затронутым obligations;
- не зависит от конкретного test framework.

## Минусы

- требует поддержки registry/matrix;
- сложнее простого `tests/` каталога;
- не каждый conceptual invariant автоматически проверяем;
- stateful/fault/accelerator suites могут быть дорогими;
- плохая формализация invariant может породить бессмысленный test.

**Решение:** принят.

---

# 6. Почему VerificationObligation first-class

MINDRA имеет много правил уровня:

```text
Memory Regulation не владеет Store
Planner не выбирает final intent
Action Commit не отменяется после dispatch failure
candidate revision не active до activation
Research Ground Truth не agent-visible
```

Если эти правила живут только в документации и случайных tests, легко получить ложное ощущение coverage.

Поэтому accepted invariant должен иметь явный статус:

```text
machine-enforced
partially machine-enforced
manual-only
research-only / not engineering obligation
```

---

# 7. Почему property/state-machine testing first-class

Многие ошибки MINDRA существуют только в последовательности операций:

```text
commit
→ lost ack
→ retry
→ restore
→ reconciliation
```

или:

```text
training candidate
→ checkpoint
→ restore
→ validation
→ activation
→ rollback
```

Hand-written examples не гарантируют достаточное исследование пространства последовательностей.

Поэтому canonical architecture требует capability для generated property/state-machine verification, но не выбирает конкретную библиотеку.

---

# 8. Почему fault injection first-class

Failure semantics уже часть design `DU-10/24/26/27`.

Если tests проверяют только happy path, реализация не считается соответствующей design.

Fault injection должен использовать declared adapters/boundaries, а не global test mode, меняющий production semantics.

---

# 9. Почему Engineering Testing отдельно от MINDRA-Eval

Engineering test может доказать:

> при `execution_unknown` runtime не делает blind retry.

Но он не доказывает:

> выбранная Action Boundary улучшает agent capability.

MINDRA-Eval может доказать функциональный effect при controls, но не заменяет atomicity/serialization/illegal-import tests.

Следовательно обе planes обязательны и логически независимы.

---

# 10. Почему line coverage не source of truth

Можно покрыть 95% строк и никогда не проверить:

- cycle rejection;
- stale write;
- Ground Truth leakage;
- corrupted checkpoint;
- duplicate committed action;
- illegal activation.

Поэтому canonical primary coverage concept — `architectural invariant coverage`, а code coverage остаётся вспомогательной метрикой.

---

# 11. Почему golden tests ограничены

Exact snapshots удобны для deterministic contracts, но особенно хрупки для:

- Cortex output;
- stochastic policies;
- approximate retrieval;
- accelerator floating point;
- reports with nondeterministic ordering/metadata.

Поэтому golden artifacts разрешены на стабильных deterministic surfaces, но не становятся универсальным oracle.

---

# 12. Почему flaky test нельзя считать pass через rerun

Rerun может скрыть:

- race;
- global mutable state;
- uncontrolled RNG;
- provider instability;
- недетерминированный bug.

Временная quarantine допустима как operational measure, но не удовлетворяет соответствующий `VerificationObligation`.

---

# 13. CI tiers

Canonical design требует capability различать как минимум смысловые классы:

```text
static/fast
CPU deterministic core
extended stateful/fault/integration
accelerator/local-model
remote/provider compatibility
```

Точные названия, thresholds, provider и schedule выбираются в version design.

---

# 14. Последствия

После ADR:

- accepted invariant должен быть отражён в Verification Matrix или явно классифицирован как non-machine-checkable/research-only;
- сменные implementations получают common conformance suites;
- stateful/fault testing является частью architecture quality, не optional polish;
- skip/quarantine не равны verified pass;
- privileged test oracle остаётся вне Agent;
- CI gating может быть obligation-aware;
- конкретные testing tools остаются implementation choices.

---

# 15. Что ADR не фиксирует

- pytest/unittest;
- Hypothesis;
- Import Linter;
- coverage.py;
- mutation tool;
- GitHub Actions;
- number of tests;
- line coverage threshold;
- concrete directory layout;
- exact CI timings;
- exact environment matrix;
- status enum/exception classes.

---

# 16. Принятое решение

```text
Accepted invariant
      ↓
VerificationObligation
      ↓
VerificationMatrix
      ↓
layered engineering tests
      ↓
VerificationEvidence
      ↓
CI / merge gate
```

при строгом разделении:

```text
Engineering Testing
≠
MINDRA-Eval
```
