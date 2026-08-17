# Research pass — Valuation / multi-objective value / risk landscape

## Статус

**Связанный Design Update:** `DU-18 — Valuation`  
**Дата среза:** 2026-08-17  
**Статус:** non-canonical research evidence

Этот документ фиксирует внешний исследовательский контекст, использованный при проектировании `DU-18`.

Он не выбирает конкретную scalarization, risk measure, critic architecture или RL algorithm как обязательную реализацию MINDRA.

---

# 1. Исследовательские вопросы

Проверялись вопросы:

1. Нужно ли canonical Valuation сводить к одному scalar?
2. Как сохранить несколько конфликтующих objectives до decision stage?
3. Чем vector-valued value отличается от utility/scalarized preference?
4. Какие scalarization families нужны кроме weighted sum?
5. Как представлять strict priorities/constraints?
6. Чем predictive uncertainty отличается от risk?
7. Нужна ли distributional value representation для risk-sensitive choice?
8. Как различить expected value, nonlinear utility и expected scalarized return?
9. Можно ли использовать RL critic как архитектурный Valuation?
10. Какие controls нужны, чтобы отличить структурированную valuation от эффекта дополнительного scalar/network capacity?

---

# 2. Multi-objective RL как evidence против premature scalarization

Multi-objective reinforcement learning (MORL) формализует задачи с несколькими reward/objective dimensions вместо одного scalar objective.

Для MINDRA важен общий паттерн:

```text
vector/objective-specific evidence
→ preference/scalarization/ordering
→ decision
```

а не обязательное:

```text
all evidence
→ immediate weighted sum
```

Это поддерживает canonical разделение `ValueProfile → ComparisonPolicy`.

---

# 3. Vamplew et al. 2024 — value-function interference

Peter Vamplew, Cameron Foale, Richard Dazeley.  
**Value function interference and greedy action selection in value-based multi-objective reinforcement learning.**  
2024.  
`arXiv:2402.06266`.

Работа рассматривает vector-valued value functions и отдельный scalarisation/ordering operator.

Авторы показывают, что scalarization может создавать interference, особенно если utility mapping сводит существенно разные objective vectors к близким scalar values.

Вывод для MINDRA:

- source/objective decomposition полезно сохранять дольше;
- scalar result не должен быть единственным каноническим evidence;
- comparison policy должна иметь явную identity/revision;
- value representation и action-selection ordering следует архитектурно разделить.

---

# 4. D3PO 2026 — decomposed preference-conditioned optimization

Tanmay Ambadkar, Sourav Panda, Shreyash Kale, Jonathan Dodge, Abhinav Verma.  
**Preference Conditioned Multi-Objective Reinforcement Learning: Decomposed, Diversity-Driven Policy Optimization.**  
2026.  
`arXiv:2602.07764`.

Работа связывает часть проблем preference-conditioned MORL с premature scalarization и destructive gradient interference. Предлагается сохранять objective-specific learning signals в decomposed pipeline, интегрируя preferences позднее.

Вывод для MINDRA:

> preserving decomposed value evidence before preference integration является современно обоснованной design strategy, но конкретный D3PO/PPO pipeline не становится реализацией Valuation MINDRA.

---

# 5. Pareto / Tchebycheff scalarization

Shuang Qiu, Dake Zhang, Rui Yang, Boxiang Lyu, Tong Zhang.  
**Traversing Pareto Optimal Policies: Provably Efficient Multi-Objective Reinforcement Learning.**  
2024.  
`arXiv:2407.17466`.

Работа анализирует разные MORL optimization targets и Tchebycheff scalarization для поиска Pareto-optimal policies.

Вывод:

- linear weighted sum не является единственным reasonable scalarization family;
- dominance/Pareto structure имеет самостоятельный смысл;
- MINDRA должна позволять comparison policy выбирать разные ordering/scalarization approaches;
- Tchebycheff не становится canonical default.

---

# 6. Lexicographic priorities

Joar Skalse, Lewis Hammond, Charlie Griffin, Alessandro Abate.  
**Lexicographic Multi-Objective Reinforcement Learning.**  
2022.  
`arXiv:2212.13769`.

Работа формализует задачи, где objectives имеют строгий priority order: второй objective оптимизируется только при соблюдении первого и т.д.

Вывод для MINDRA:

- Goal priority/constraint semantics нельзя считать эквивалентной просто «очень большому weight»;
- `ComparisonPolicy` должна допускать lexicographic ordering;
- lexicographic policy является одной возможностью, а не универсальной мотивационной теорией Agent.

Свежая LPPG-RL 2025 (`arXiv:2511.08339`) дополнительно показывает продолжающийся интерес к lexicographic optimization в continuous control.

---

# 7. Constraints отдельно от reward

Joshua Achiam, David Held, Aviv Tamar, Pieter Abbeel.  
**Constrained Policy Optimization.**  
2017.  
`arXiv:1705.10528`.

CPO рассматривает setting, где reward objective существует отдельно от constraints.

Для MINDRA важен conceptual вывод:

```text
constraint
≠
обязательно большой negative reward
```

Следовательно, `ConstraintProfile`/constraint-first comparison является оправданной capability, а не лишней сложностью.

CPO как конкретный policy-search algorithm не принимается.

---

# 8. ESR, nonlinear utility и temporal aggregation

Nianli Peng, Muhang Tian, Brandon Fain.  
**Multi-objective Reinforcement Learning with Nonlinear Preferences: Provable Approximation for Maximizing Expected Scalarized Return.**  
2023.  
`arXiv:2311.02544`.

Работа рассматривает nonlinear utility над накопленным vector return и показывает, что порядок temporal accumulation/scalarization имеет математическое значение.

Conor F. Hayes et al.  
**Expected Scalarised Returns Dominance: A New Solution Concept for Multi-Objective Decision Making.**  
2021.  
`arXiv:2106.01048`.

Эта линия различает utility одного execution и utility, определяемую через expected returns.

Вывод для MINDRA:

- `immediate value`, `trajectory value`, expectation и nonlinear scalarization нельзя скрыто смешивать;
- horizon/temporal aggregation policy должны быть explicit;
- universal discount factor не следует делать архитектурным инвариантом.

---

# 9. Distributional RL — distribution вместо одного expected value

Marc G. Bellemare, Will Dabney, Rémi Munos.  
**A Distributional Perspective on Reinforcement Learning.**  
2017.  
`arXiv:1707.06887`.

Работа моделирует distribution случайного return вместо только expectation.

Will Dabney, Mark Rowland, Marc G. Bellemare, Rémi Munos.  
**Distributional Reinforcement Learning with Quantile Regression.**  
2017.  
`arXiv:1710.10044`.

Вывод для MINDRA:

- stochastic futures полезно уметь представлять distributionally;
- mean value не содержит tail structure;
- optional `ValueDistribution`/`RiskProfile` является обоснованной capability;
- C51/QR-DQN/IQN и конкретные distributional algorithms не становятся canonical implementation.

---

# 10. Risk-sensitive distributional RL

Yu Chen, Xiangcheng Zhang, Siwei Wang, Longbo Huang.  
**Provable Risk-Sensitive Distributional Reinforcement Learning with General Function Approximation.**  
2024.  
`arXiv:2402.18159`.

Работа формализует risk-sensitive decision making поверх return distributions и семейства risk measures.

Вывод:

```text
uncertainty/distribution
+
explicit risk measure
→ risk-sensitive decision value
```

а не:

```text
uncertainty = risk
```

Для MINDRA risk measure должен иметь identity/revision и adverse/downside semantics.

---

# 11. Successor Features / decomposed future value

André Barreto et al.  
**Transfer in Deep Reinforcement Learning Using Successor Features and Generalised Policy Improvement.**  
2019.  
`arXiv:1901.10964`.

Successor-feature line отделяет representation ожидаемых будущих features от task-specific reward/preference mapping.

Для MINDRA полезен общий design pattern:

```text
future consequence representation
≠
current preference weighting
```

Это дополнительно поддерживает разделение World Model/predicted consequences и Valuation preference/comparison semantics.

Successor Features не принимаются как обязательный estimator.

---

# 12. Preference controllability

Pau de las Heras Molins et al.  
**Controllability in preference-conditioned multi-objective reinforcement learning.**  
2026.  
`arXiv:2605.10585`.

Работа подчёркивает, что хорошие стандартные MORL metrics не гарантируют, что изменение preference input действительно управляемо меняет behavior в ожидаемом направлении.

Вывод для MINDRA:

- `ComparisonPolicy`/preference intervention должны проверяться не только по final task score;
- нужно измерять causal sensitivity downstream behavior к изменению valuation preference context;
- preference interface без behavioral controllability может быть декоративным.

---

# 13. Что research evidence поддерживает канонически

Evidence поддерживает следующие решения `DU-18`:

1. multi-objective evidence следует сохранять до explicit comparison;
2. scalarization не обязана быть linear/mandatory;
3. Pareto/dominance, lexicographic и constraint-aware semantics имеют самостоятельное значение;
4. nonlinear utility и temporal aggregation требуют явной semantics;
5. expected value не содержит всю distributional/risk информацию;
6. risk требует отдельной measure/preferences, а не только uncertainty;
7. value estimator/critic и source preference semantics полезно разделять;
8. preference change должно быть causally testable.

---

# 14. Что evidence НЕ определяет

Research pass не выбирает:

- fixed weighted sum;
- Pareto как default;
- Tchebycheff;
- lexicographic ordering;
- CVaR;
- concrete constraint policy;
- distributional critic;
- successor features;
- PPO/DQN/actor-critic;
- exact utility theory;
- human preference dataset;
- first-version component schema.

---

# 15. Что перепроверить перед implementation/version selection

Перед конкретной software version нужно заново проверить:

- актуальные MORL libraries/tooling;
- TorchRL/other multi-objective/distributional primitives;
- available risk-sensitive estimators;
- complexity на выбранном MicroWorld;
- minimal ValueProfile schema;
- предпочтительный baseline scalarization;
- feasibility of vector/distributional critics на доступном compute;
- evaluation metrics для Pareto/preference controllability.
