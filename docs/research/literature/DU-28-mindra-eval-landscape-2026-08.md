# DU-28 — MINDRA-Eval: research pass 2026-08

## Статус

**Дата:** 2026-08-17  
**Тип:** non-canonical research evidence  
**Связанный Design Update:** `DU-28 — MINDRA-Eval`

Документ не выбирает benchmark framework, statistical library, metric package, number of seeds, significance threshold или universal score.

---

# 1. Исследовательский вопрос

Нужно спроектировать evaluation architecture, способную одновременно измерять:

```text
end-task performance
module-specific functional quality
causal contribution
calibration
robustness/generalization
compute/resource efficiency
reproducibility
```

и исключать альтернативные объяснения improvement:

```text
more parameters
more state capacity
more context
more data
more tuning
more compute
stronger Cortex
stronger Action Gate
lucky seed
other checkpoint/world distribution
```

---

# 2. Reliable RL evaluation — point estimates недостаточны

## Deep Reinforcement Learning at the Edge of the Statistical Precipice

Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro, Aaron Courville, Marc Bellemare, NeurIPS 2021.

- https://proceedings.neurips.cc/paper/2021/hash/f514cec81cb148559cf475e7426eed5e-Abstract.html
- https://arxiv.org/abs/2108.13264

Работа показывает, что few-run RL comparisons могут давать существенно разные выводы, если смотреть только на point estimates. Авторы рекомендуют interval estimates aggregate performance, performance profiles и более robust aggregate metrics, включая interquartile mean; опубликована библиотека `rliable`.

Для MINDRA вывод:

```text
stochastic aggregate result
→ distribution/uncertainty evidence required
```

Но `rliable` и IQM не становятся architecture requirement.

---

# 3. Evaluating the Performance of RL Algorithms

Scott Jordan, Yash Chandak, Daniel Cohen, Mengxue Zhang, Philip Thomas, ICML 2020.

- https://proceedings.mlr.press/v119/jordan20a.html
- https://arxiv.org/abs/2006.16958

Работа мотивирует более систематическую evaluation methodology как для одного environment, так и для агрегирования по нескольким environments.

Для MINDRA важен principle:

```text
metric/aggregation semantics
являются частью experiment protocol,
а не косметикой report
```

---

# 4. How Many Random Seeds?

Cédric Colas, Olivier Sigaud, Pierre-Yves Oudeyer, 2018.

- https://arxiv.org/abs/1806.08295

Работа связывает число random seeds, statistical power и вероятность ошибок вывода и обсуждает t-test/bootstrap assumptions.

Для MINDRA:

- нельзя архитектурно зафиксировать магическое число seeds;
- sample/replicate count должен соответствовать effect/question/budget;
- assumptions statistical test должны быть явными.

Особенно важно дополнение MINDRA:

```text
many episodes from one trained checkpoint
≠
many independent training seeds
```

---

# 5. Task underspecification / distribution-level evaluation

## The Impact of Task Underspecification in Evaluating Deep Reinforcement Learning

Vindula Jayawardana et al., NeurIPS 2022.

- https://proceedings.neurips.cc/paper_files/paper/2022/hash/96ca792fddef7c1e3366c405022463cb-Abstract-Conference.html

Авторы показывают, что evaluation на нескольких selected MDP instances может давать иное ranking, чем evaluation по parameterized family of MDPs.

Для MINDRA:

```text
performance on world instance
≠
performance over world distribution
```

Поэтому EvaluationSuite должен иметь explicit world/task distributions и held-out axes.

---

# 6. Procgen / generalization

## Measuring Sample Efficiency and Generalization in Reinforcement Learning Benchmarks

Sharada Mohanty et al., PMLR 2021 / NeurIPS Procgen competition.

- https://proceedings.mlr.press/v133/mohanty21a.html

Полезен как precedent централизованной evaluation sample efficiency/generalization по procedural environments.

MINDRA не принимает Procgen как benchmark, но сохраняет separation:

```text
training distribution
validation distribution
test/generalization distribution
```

---

# 7. Calibration — accuracy недостаточно

## Calibrated Language Models and How to Find Them with Label Smoothing

Jerry Huang, Peng Lu, Qiuhao Zeng, ICML 2025.

- https://proceedings.mlr.press/v267/huang25w.html

Работа показывает, что instruction tuning может ухудшать calibration даже при сохранении task capability.

Для MINDRA это усиливает разделение:

```text
accuracy / competence
≠
confidence calibration
```

особенно для Self Model.

---

# 8. Agent/tool confidence calibration

## MICE for CATs: Model-Internal Confidence Estimation for Calibrating Agents with Tools

Nishant Subramani et al., NAACL 2025.

- https://aclanthology.org/2025.naacl-long.615/

Работа оценивает calibration confidence именно в tool-using agent setting и использует smoothed ECE среди metrics.

Для MINDRA это useful evidence того, что action/tool context требует отдельного calibration evaluation, но hidden-state estimator MICE не становится частью architecture.

---

# 9. Confidence in multi-turn interactions

## Confidence Estimation for LLMs in Multi-turn Interactions

Caiqi Zhang et al., Findings of ACL 2026.

- https://aclanthology.org/2026.findings-acl.1280/

Работа показывает, что распространённые confidence methods могут плохо работать по calibration/monotonicity в multi-turn setting и отдельно рассматривает tracking evidence accumulation.

Для MINDRA:

- trajectory/prefix confidence не должен оцениваться только одним final scalar;
- нужно определять conditioning history и resolution event.

---

# 10. Proper scoring rules for agentic uncertainty

## Proper Scoring Rules for Agentic Uncertainty Quantification

Suresh Raghu, Satwik Pandey, Shashwat Pandey, 2026.

- https://arxiv.org/abs/2605.24756

Работа различает ranking/calibration summaries и strictly proper trajectory-level scoring для prefix-conditioned success probability.

Для MINDRA полезен общий principle:

```text
если subsystem заявляет meaningful probability,
metric должен оценивать именно заявленную probability semantics
```

а ECE/rank metric не всегда достаточно.

Конкретный TPS не становится mandatory metric.

---

# 11. ConfidenceBench 2026

Matthew ffrench-Constant, Daniel Yang, Xinmeng Huang, Sanyam Kapoor.

- https://arxiv.org/abs/2607.20526

Benchmark использует Brier score для verbalized confidence и подчёркивает расхождение accuracy и calibration.

Для MINDRA важна сама идея proper score и separate axis, но verbal confidence Cortex не является Self Model probability автоматически.

---

# 12. Calibration robustness beyond ECE

## Calibration Is Not Enough: Evaluating Confidence Estimation Under Language Variations

Yuxi Xia et al., 2026.

- https://arxiv.org/abs/2601.08064

Авторы предлагают дополнительно оценивать robustness/stability/sensitivity confidence estimates к semantic-preserving и semantic-changing variations.

Для MINDRA это поддерживает multi-dimensional calibration diagnostics:

```text
calibration
≠ discrimination
≠ robustness
≠ semantic sensitivity
```

---

# 13. Controlled matched-compute agent evaluation

## Capable language models can outgrow the benefits of collaboration

Nature Machine Intelligence, 2026.

- https://www.nature.com/articles/s42256-026-01268-y

Работа проводит controlled evaluation agent coordination с одинаковыми task prompts, tools и computational budgets, варьируя coordination structure/model capability.

Для MINDRA это сильный современный precedent принципа:

```text
architectural effect
нужно отделять от compute/model capability confounds
```

и мотивирует `ResourceMatchProfile` / actual compute evidence.

---

# 14. Robustness и resilience как отдельные оси

## Empirical Study on Robustness and Resilience in Cooperative Multi-Agent Reinforcement Learning

Simin Li et al., NeurIPS 2025.

- https://proceedings.neurips.cc/paper_files/paper/2025/hash/3e8d9bf1dd1eb9d3d9d500fb3543c87b-Abstract-Conference.html

Работа показывает, что nominal cooperative performance, robustness и resilience могут расходиться в зависимости от uncertainty type/intensity.

Для MINDRA:

```text
nominal task score
≠ robustness
≠ resilience/recovery
```

и stress/shift condition должна быть versioned частью EvaluationSuite.

---

# 15. Replicability vs ordinary reproducibility

## Replicable Reinforcement Learning

Eric Eaton, Marcel Hussing, Michael Kearns, Jessica Sorrell, NeurIPS 2023.

- https://proceedings.neurips.cc/paper_files/paper/2023/hash/313829757739365201b5adb3a1cbd9bd-Abstract-Conference.html

Работа формализует более сильное notion replicability для RL algorithms.

MINDRA не принимает их formal framework как свой universal definition, но сохраняет важное различие:

```text
reproduce same run/checkpoint
≠
replicate effect on new samples/seeds
```

Это согласуется с DU-27 `ReproducibilityClaim` и DU-28 replicated/generalized evidence level.

---

# 16. Causal interventions

## Inducing Causal Structure for Interpretable Neural Networks

Atticus Geiger et al., 2021.

- https://arxiv.org/abs/2112.00826

Interchange intervention training является примером явного causal intervention над internal representations с проверкой counterfactual behavior.

MINDRA не использует IIT как обязательный method, но общий research principle полезен:

```text
internal correlation
<
controlled intervention evidence
```

Особенно для Drives/Appraisal/Affect/Workspace/Self Model.

---

# 17. Почему обычный leaderboard недостаточен для MINDRA

MINDRA имеет boundaries, где один final score не позволяет различить источник улучшения:

```text
Policy intent
→ Action Gate correction
→ final success
```

или:

```text
Planner
→ more rollout compute
→ better score
```

или:

```text
Workspace
→ more recurrent/shared state
→ better score
```

Поэтому нужны attribution/matched controls, а не только end-task outcome.

---

# 18. Conditional module gates

Из accepted design прямо следуют explicit negative controls.

## Affect

```text
Full
NoAffect
ResetEveryEvent
ShuffledHistory
MatchedRecurrentControl
```

## Workspace

```text
Full
NoWorkspace/DirectReads
MatchedSharedBuffer
MatchedRecurrentBuffer
Random/Shuffled admission
capacity sweep
```

## Executive

```text
Adaptive
FixedSchedule
SimpleThreshold
RandomMetaAction
MatchedRouter
```

с performance/actual-compute frontier.

## Planner

```text
Planner
NoPlanner/Reactive
Depth1
Random/Shuffled plan
MatchedSearch control
```

Эти gates являются design-derived, а не взяты из одной внешней статьи.

---

# 19. Statistical design implications

Research pass поддерживает следующие MINDRA requirements:

1. point estimate недостаточен для stochastic claim;
2. statistical unit/nesting explicit;
3. number of seeds не universal constant;
4. task-family distribution matters;
5. proper scoring нужен для probability claims;
6. calibration и accuracy разделены;
7. matched compute/capacity controls важны для architecture claims;
8. robustness/resilience — отдельные axes;
9. replicated effect сильнее single-run causal anecdote;
10. metric/statistical implementation должна быть versioned, но не canonical framework.

---

# 20. Что не следует из research pass

Research pass **не доказывает**, что MINDRA mechanisms полезны.

Он только обосновывает evaluation infrastructure, в которой такие claims можно будет честно проверить.

Не фиксируются:

- `rliable`;
- IQM;
- Brier score как единственный calibration metric;
- bootstrap;
- t-test;
- minimum seeds;
- p-value threshold;
- чужой benchmark suite;
- specific agent benchmark;
- конкретный experiment tracker.

---

# 21. Вывод для DU-28

Наиболее устойчивый design direction:

```text
fully specified conditions
+
explicit replicate structure
+
typed metrics
+
controls/matched controls
+
paired interventions where valid
+
proper probability evaluation
+
compute normalization
+
reproducibility lineage
→
Multi-layer MINDRA-Eval
```

а не один universal leaderboard score.
