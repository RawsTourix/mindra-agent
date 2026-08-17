# DU-29 — Engineering Testing: research/tool pass 2026-08

## Статус

**Дата:** 2026-08-17  
**Тип:** non-canonical research/tool evidence  
**Связанный Design Update:** `DU-29 — Engineering Testing`

Документ не выбирает test framework, CI provider, property-testing library, import linter, coverage threshold или mutation-testing tool.

---

# 1. Исследовательский вопрос

Нужно проверить, какие современные testing techniques подходят архитектуре с:

```text
versioned committed state
state-machine lifecycle
replaceable backends
causal action execution
fault/recovery semantics
training/checkpoint revisions
privileged research planes
```

Главный вывод:

> для MINDRA недостаточно example-based unit tests; нужны layered contract/property/state-machine/fault/architecture tests с явной связью с accepted invariants.

---

# 2. Property-based testing — Hypothesis

Официальная документация:

- https://hypothesis.readthedocs.io/en/latest/
- https://hypothesis.readthedocs.io/en/latest/stateful.html

Hypothesis формулирует property-based testing как проверку свойств на автоматически выбираемых inputs, включая edge cases. Stateful API позволяет генерировать **последовательности операций**, а `invariant` проверяется после каждого шага state machine.

Для MINDRA это особенно подходит к:

```text
Scheduler/CognitiveState revisions
Action commit/retry/reconcile
Memory lifecycle
Training candidate/activation/rollback
Checkpoint capture/restore/migration
```

Важный engineering pattern:

```text
production implementation
vs
simple reference model
```

на generated operation sequences.

Hypothesis не становится architecture requirement; нужна сама capability property/state-machine generation + shrinking/minimal counterexample там, где выбранный tool это поддерживает.

---

# 3. Architecture dependency tests — Import Linter

Официальная документация:

- https://import-linter.readthedocs.io/en/stable/get_started/run/
- https://import-linter.readthedocs.io/en/v2.8/contract_types/

Import Linter поддерживает contracts классов:

```text
forbidden dependencies
protected imports
layers
independence
acyclic siblings
```

и проверяет import graph проекта командой `lint-imports`.

Это practical evidence, что `DU-02` rules вида:

```text
Agent core ─X→ Evaluation Runtime
Policy ─X→ concrete Cortex SDK
cognitive siblings ─X→ hidden cycles
```

могут быть machine-enforced после определения concrete package layout.

MINDRA не фиксирует Import Linter: будущая implementation может использовать другой graph/static-analysis mechanism.

---

# 4. Flaky tests — pytest guidance

Официальная документация:

- https://pytest.org/en/stable/explanation/flaky.html

Pytest отдельно предупреждает о flaky behavior из-за uncontrolled state/concurrency и отмечает, что permanent `xfail`/quarantine-like usage опасен.

Для MINDRA это особенно важно, потому что flaky test может быть симптомом:

- race в scheduler;
- скрытого global state;
- uncontrolled RNG;
- provider instability;
- nondeterministic accelerator operation.

Следовательно:

```text
rerun passed
≠
verification obligation satisfied
```

---

# 5. Test selection / tiers — pytest markers как precedent

Официальная документация:

- https://docs.pytest.org/en/latest/how-to/mark.html

Pytest позволяет назначать custom markers и выбирать subsets tests.

Для MINDRA это подтверждает практичность CI tier semantics:

```text
fast/static
CPU core
stateful/fault
accelerator
remote provider
```

Но exact marker names/test runner не являются canonical design.

---

# 6. Deterministic debug mode — PyTorch

Официальная документация:

- https://docs.pytorch.org/docs/stable/notes/randomness
- https://docs.pytorch.org/docs/stable/generated/torch.use_deterministic_algorithms.html

PyTorch документирует две важные вещи:

1. complete reproducibility не гарантируется между releases/platforms/CPU-GPU;
2. `torch.use_deterministic_algorithms(True)` может заставлять использовать deterministic implementations и выдавать ошибку для известных nondeterministic operations, но одного этого недостаточно для полной reproducibility.

Для DU-29:

```text
same seed
≠
universal exact test oracle
```

и deterministic framework mode полезен как **debug/test profile**, а не как общая production requirement.

---

# 7. Why state-machine tests matter for Action Boundary

DU-24 имеет lifecycle:

```text
intent
→ authorize
→ commit
→ dispatch
→ receipt/execution
→ reconciliation
```

Ошибки часто требуют последовательности:

```text
commit
→ request sent
→ response lost
→ restore
→ retry
```

Обычный unit test одного метода может не обнаружить duplicate external effect.

Поэтому Action Boundary является приоритетным объектом model/state-machine testing.

Это MINDRA-derived requirement, а не требование конкретного внешнего framework.

---

# 8. Failure injection как часть correctness

Уже принятые contracts содержат first-class failures:

```text
Cortex timeout/context overflow/provider failure
module attempt failure
execution_unknown
checkpoint corruption
training OOM/NaN
migration incompatibility
```

Следовательно failure tests нельзя откладывать до deployment chaos testing.

DU-29 делает distinction:

```text
boundary-level deterministic fault injection
≠
large-scale production chaos engineering
```

Первое требуется для contract correctness ранних версий; второе может появиться позднее при соответствующем deployment.

---

# 9. Golden tests и ML behavior

Для deterministic serialization/schema/migration small goldens полезны.

Но exact output neural system часто зависит от:

```text
backend revision
precision
platform
sampling/RNG
parallelism
```

Поэтому для neural paths preferred engineering oracle:

```text
contract property
shape/schema
capability/failure semantics
invariant
bounded tolerance where justified
```

а не автоматически exact text/logit snapshot.

---

# 10. Coverage

Обычный code coverage полезен для обнаружения совершенно непроверенных веток, но архитектурно недостаточен.

MINDRA имеет отдельные coverage dimensions:

```text
architectural invariant coverage
contract implementation coverage
failure-mode coverage
schema/migration coverage
backend capability matrix
```

Конкретный coverage tool/threshold не выбирается.

---

# 11. Test doubles

Modular design MINDRA требует общих conformance suites для:

```text
real implementation
Dummy implementation
Control implementation
provider adapter
```

При этом `NoX` должен корректно объявлять отсутствие capability, а не симулировать успех фиктивным пустым результатом.

Это особенно важно для Cortex/Memory/Workspace/Planner controls и напрямую следует из accepted designs.

---

# 12. Engineering tests vs research evaluation

Внешние testing tools по природе обычно отвечают:

```text
implementation satisfies asserted property?
```

MINDRA-Eval отвечает:

```text
does mechanism provide functional/causal benefit?
```

Поэтому DU-29 намеренно не добавляет research benchmark assertions в обычный CI:

```text
assert agent_success_rate > 0.8
```

может быть smoke/regression check конкретной version позже, но не universal proof subsystem usefulness.

---

# 13. Вывод для DU-29

Наиболее устойчивое направление:

```text
accepted invariant registry
+
static architecture enforcement
+
contract conformance
+
property/state-machine testing
+
integration
+
fault/recovery
+
round-trip/migration
+
explicit CI/environment tiers
→
Engineering Verification Plane
```

а не просто большая коллекция hand-written unit tests.

---

# 14. Что research pass не фиксирует

Не фиксируются:

- pytest;
- Hypothesis;
- Import Linter;
- GitHub Actions;
- coverage.py;
- mutation framework;
- test count;
- coverage percentage;
- CI timing;
- accelerator/provider matrix;
- конкретные test directory conventions.
