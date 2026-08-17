# ADR-0018 — Typed multi-objective Valuation с explicit comparison/scalarization boundary

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-18 — Valuation`

---

# 1. Контекст

После `DU-17` MINDRA имеет отдельные:

- Goals;
- Drives;
- Appraisal;
- Affect;
- World Model;
- Self Model;
- Intrinsic Signals;
- agent-visible external feedback.

Но ни одна подсистема не должна скрыто превращать эти разнородные sources в final action preference.

Нужно определить отдельную decision-relevant valuation boundary.

---

# 2. Проблема

Рассматривались варианты:

1. один universal scalar utility/reward;
2. fixed weighted sum всех concerns;
3. передать всю scalarization непосредственно Policy/Planner;
4. использовать RL critic scalar как canonical value;
5. typed multi-objective `ValueProfile` + explicit versioned `ComparisonPolicy`;
6. полностью Pareto-only Valuation без scalar/ordering capability.

---

# 3. Требования

Решение должно:

- сохранять конфликт Goals/Drives до explicit comparison;
- поддерживать state/outcome/action/trajectory targets;
- различать actual/predicted/imagined/counterfactual provenance;
- не считать External Feedback/Internal Signal готовой utility;
- не смешивать Appraisal/Affect с value;
- отличать predictive uncertainty от risk/downside;
- учитывать feasibility/cost без скрытого universal formula;
- позволять hard constraints отдельно от soft objectives;
- допускать scalarization, но не требовать её;
- поддерживать разные preference/comparison semantics;
- не выполнять final Policy decision;
- не делать algorithm-specific reward/critic архитектурным source of truth;
- поддерживать intervention/control/reproducibility.

---

# 4. Вариант A — Universal scalar utility

Conceptually:

```text
all evidence
→ value ∈ R
```

## Плюсы

- простой API;
- удобно для `argmax`;
- легко использовать в классическом RL.

## Минусы

- теряется provenance отдельных concerns;
- невозможно понять причину trade-off;
- hard constraints легко превращаются в arbitrary penalty;
- конфликт goals/drives скрывается;
- разные units prematurely смешиваются;
- intervention отдельного value source затрудняется;
- архитектура начинает предполагать конкретную utility theory.

**Решение:** отклонён как canonical representation.

Scalar остаётся допустимым derived view.

---

# 5. Вариант B — Fixed weighted sum

```text
u = Σ w_i x_i
```

## Плюсы

- простота;
- differentiability;
- широко используется в optimization/RL;
- легко задавать preference vector.

## Минусы

- weights становятся hidden definition ценностей;
- линейная scalarization не выражает все виды priorities/constraints/nonlinear preferences;
- меняющийся Agent context плохо выражается fixed vector;
- premature scalarization может уничтожать multi-objective structure;
- разные scales требуют отдельной normalization semantics.

**Решение:** отклонён как universal architecture; сохранён как важный baseline/ComparisonPolicy family.

---

# 6. Вариант C — Scalarization только внутри Policy

## Плюсы

- меньше модулей;
- Policy сразу может выбрать action.

## Минусы

- Policy становится скрытым owner preferences;
- valuation impossible независимо диагностировать;
- разные Policy implementations могут молча по-разному трактовать те же Goals/Drives;
- невозможно чисто интервенировать comparison semantics при fixed Policy;
- усложняется NoValuation/matched control.

**Решение:** отклонён.

Policy потребляет explicit valuation output, но не определяет hidden source semantics.

---

# 7. Вариант D — RL Critic как canonical Value

## Плюсы

- готовая теория `V/Q`;
- эффективная neural implementation;
- напрямую используется actor-critic methods.

## Минусы

- critic обычно определён относительно конкретного reward/return;
- reward function преждевременно становится смыслом внутренних ценностей;
- state/action value смешивается с multi-objective source semantics;
- rule-based/planner implementations оказываются искусственно подчинены RL форме;
- critic может быть training-only и не иметь нужной causal interpretability.

**Решение:** отклонён как canonical definition. Critic допустим как один estimator/backend/view.

---

# 8. Вариант E — Typed ValueProfile + ComparisonPolicy

Conceptually:

```text
sources
→ typed ValueProfile
→ explicit ComparisonPolicy
→ relation / ordering / optional scalar
```

## Плюсы

- сохраняет source/objective semantics;
- scalarization становится явной и versioned;
- поддерживает weighted, nonlinear, Pareto, lexicographic и constraint-first policies;
- позволяет `incomparable`;
- risk/feasibility/constraints не обязаны становиться soft weights;
- хорошо поддерживает intervention и causal controls;
- совместимо с learned и rule-based implementations;
- не привязывает architecture к конкретному RL algorithm.

## Минусы

- сложнее API;
- downstream Policy должен уметь работать с richer result;
- exact normalization/comparison design потребует version-specific решений;
- first implementation придётся сознательно ограничить subset semantics.

**Решение:** принято.

---

# 9. Вариант F — Только Pareto/dominance

## Плюсы

- максимально сохраняет multi-objective structure;
- не требует preference weights.

## Минусы

- часто оставляет много incomparable candidates;
- final action selection всё равно требует дополнительной semantics;
- не выражает natural lexicographic/constraint priorities;
- неудобно для некоторых contexts с explicit preferences.

**Решение:** отклонён как universal policy. Pareto comparison остаётся supported family.

---

# 10. Принятое решение

MINDRA использует **typed multi-objective Valuation**.

Канонически:

```text
ValueProfile
≠
ScalarizedValue
≠
Training Reward
≠
Critic Value
≠
Policy Decision
```

Разнородные concerns сохраняются как typed components до явной comparison boundary.

`ComparisonPolicy` является versioned и observable.

Scalarization разрешена только как explicit derived operation.

---

# 11. Multi-objective conflict

MINDRA допускает:

```text
A preferred B
B preferred A
tie
dominance
incomparable
constraint violation
```

`incomparable` — валидный semantic result.

Policy/Executive Control позднее определят поведение при неполном ordering.

---

# 12. Risk decision

Predictive uncertainty не называется risk автоматически.

Risk появляется только при наличии:

```text
outcome distribution/uncertainty model
+
adverse/downside semantics
+
risk measure/policy
```

Distributional estimate допускается, но не обязателен.

CVaR/quantile/worst-case и другие measures остаются concrete policy choices.

---

# 13. Constraint decision

Hard/structural constraint допускается как отдельный profile/policy concept.

Не требуется кодировать:

```text
constraint violation → reward -= 1000000
```

как universal method.

---

# 14. Temporal decision

Immediate и prospective valuation различаются.

Prospective valuation имеет explicit horizon/temporal aggregation semantics.

Discount factor не является canonical invariant.

---

# 15. Training/RL boundary

Future training может:

- обучать Valuation estimator;
- строить critic;
- производить scalar reward из ValueProfile;
- использовать vector reward;
- использовать auxiliary targets.

Но эти choices принадлежат `DU-26` и не меняют принятую semantic boundary автоматически.

---

# 16. Последствия

Положительные:

- Valuation становится независимо диагностируемой;
- concerns не теряются раньше времени;
- можно менять preference/risk policies без изменения source modules;
- Policy остаётся отдельным owner action selection;
- scalar baseline остаётся легко реализуемым;
- возможны сильные causal preference interventions.

Отрицательные:

- больше metadata/revision overhead;
- необходимо явное управление units/normalization;
- exact Policy integration будет сложнее одного `argmax(Q)`;
- придется решить version-specific minimal component set позднее.

---

# 17. Falsification / controls

Архитектурный вклад structured Valuation должен проверяться не только против `NoValuation`, но и против:

```text
WeightedScalarBaseline
MatchedLinearValuation
ShuffledValuation
Constant/Random controls
```

Если structured ValueProfile/ComparisonPolicy не даёт специфического преимущества или controllable behavior относительно simpler matched alternatives, version design может выбрать простой scalar baseline, не меняя canonical capability boundary.

---

# 18. Что решение намеренно не определяет

ADR не выбирает:

- exact ValueComponent list;
- preference weights;
- default comparison family;
- Pareto/Tchebycheff/lexicographic/CVaR implementation;
- exact risk measure;
- hard safety constraints;
- temporal discounting;
- critic/network architecture;
- RL algorithm;
- human preference model;
- concrete Python API.
