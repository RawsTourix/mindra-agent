# Исследовательская методология MINDRA

## Статус документа

Этот документ фиксирует общие правила постановки, проведения и интерпретации исследований MINDRA.

Он не задаёт concrete benchmark/library/statistical implementation. После `DU-28` точная evaluation semantics определяется [`design/mindra-eval.md`](design/mindra-eval.md), а checkpoint/reproducibility semantics — [`design/checkpoint-reproducibility-compute.md`](design/checkpoint-reproducibility-compute.md).

---

# 1. Главный принцип

MINDRA развивается не по схеме «добавили модуль — стало сложнее — значит стало лучше», а:

```text
гипотеза
→ контролируемый design
→ реализация
→ experiment
→ evidence
→ interpretation
→ design review
```

Любой заявляемый вклад по возможности отделяется от:

- увеличения параметров/state capacity;
- дополнительного compute/context/data;
- tuning budget;
- lucky seed;
- конкретного Cortex;
- изменения Environment distribution;
- скрытого изменения training/action-gate procedure.

---

# 2. Engineering correctness ≠ research validity

Корректно реализованный модуль может не подтверждать research hypothesis.

Интересный единичный результат не является достаточным evidence, если implementation/protocol/reproducibility нарушены.

`DU-29` отдельно проектирует Engineering Testing; `DU-28` — research/functional Evaluation.

---

# 3. Гипотеза должна быть falsifiable

Перед confirmatory experiment формулируется наблюдаемый outcome, способный ослабить/опровергнуть гипотезу.

Плохо:

> Appraisal делает агента более человечным.

Лучше:

> При aligned external state controlled intervention в appraisal dimension систематически меняет заранее указанный downstream outcome при ограниченных off-target effects.

Exact `HypothesisSpec`/module gates задаются `MINDRA-Eval`.

---

# 4. Baseline / ablation / control

Baseline отвечает на конкретный вопрос.

Ablation:

```text
Full
vs
Full - X
```

важна, но может менять capacity/compute.

Поэтому, где требуется claim о **semantic contribution**, используются controls:

- `No*`;
- constant/random/shuffled;
- rule-based;
- parameter/state-capacity matched;
- context/compute/data matched;
- oracle research controls.

Matching factors и deviations описываются `EvaluationCondition/ResourceMatchProfile`.

---

# 5. Causal intervention

Корреляция internal state и behavior недостаточна для сильного causal claim.

Желательный pattern:

```text
verified common base state
→ branch/control
→ branch/treatment with Intervention X
→ compare target + off-target effects
```

Paired counterfactual требует достаточного `DU-27` restore level и explicit `DU-28` intervention/analysis protocol.

---

# 6. Factorial interactions

Если механизм полезен только совместно с другим, допускается:

```text
none
A
B
A+B
```

Full factorial всей MINDRA практически не требуется; используется hypothesis-driven subset.

---

# 7. Replicates и stochasticity

Серьёзный stochastic claim не опирается на один удачный run.

Нужно различать:

```text
training replicate
checkpoint replicate
world replicate
episode replicate
policy stochastic replicate
counterfactual branch
```

Много episodes одного checkpoint не являются independent training replicates.

Количество replicates и statistical method задаются `ReplicateStructure + StatisticalAnalysisPlan` конкретного study, а не глобальным магическим числом seeds.

---

# 8. Train / validation / test separation

Если world/data использованы для training/model selection, confirmatory generalization evaluation включает held-out conditions.

Различаются:

- memorization;
- adaptation;
- in-distribution generalization;
- compositional/generalization shift;
- transfer/OOD.

Использование test outcome для ручной настройки превращает этот test в development evidence.

---

# 9. Cortex transfer

Поскольку Cortex сменный, важный класс evidence:

```text
NoCortex
small Cortex
alternative family/backend
stronger Cortex
```

где feasible.

Architecture gain, существующий только с одним Cortex, формулируется узко и не объявляется universal.

---

# 10. Parameter/compute/data/tuning controls

Improvement нельзя автоматически приписывать architecture, если treatment имеет больше:

- parameters;
- state capacity;
- context;
- Memory/Workspace capacity;
- Cortex calls;
- training data/steps;
- runtime rollout/search;
- tuning budget;
- actual compute.

Если perfect matching невозможно, показывается trade-off/frontier и generic matched control.

Compute provenance определяется `DU-27`, comparison semantics — `DU-28`.

---

# 11. Module-specific metrics

End-task success недостаточен.

Каждый substantial boundary получает metrics своей responsibility, например:

- World Model — prediction/belief/uncertainty;
- Self Model — calibration/competence;
- Memory — retrieval utility/provenance;
- Drives/Appraisal/Affect — intervention response;
- Valuation — preference/constraint behavior;
- Salience/Workspace — resource routing;
- Executive — performance/compute frontier;
- Planner — long-horizon contribution;
- Action Gate — correction/false-rejection attribution.

Каноническая metric architecture — `DU-28`.

---

# 12. Calibration

Accuracy и confidence calibration являются разными axes.

Если subsystem заявляет meaningful probability, evaluation использует metric family, соответствующую probability semantics, где practically possible — proper scoring.

ECE-like summaries могут быть diagnostics, но не считаются universal proof truthful probability.

---

# 13. Exploratory vs confirmatory

Exploratory runs разрешены для debugging/hypothesis generation/range selection.

Confirmatory study заранее фиксирует:

- hypothesis;
- independent variables/controls;
- primary contrasts/metrics;
- replicate/sample policy;
- statistical analysis;
- exclusions/censoring;
- stopping;
- success/falsification criterion.

Post-hoc change создаёт новую revision и не masquerade как preregistered result.

---

# 14. Reproducibility

Каждый значимый result связывается минимум с:

```text
repository/code revision
configuration
Agent/component revision
checkpoint + RestoreProfile
Environment/world distribution
Cortex condition
RNG/seed semantics
Dataset/TrainingPlan refs where relevant
software/hardware manifests
actual compute provenance
EvaluationManifest/metrics/analysis
raw Evidence/Experience artifacts
```

`same seed` недостаточно. Scoped restore/reproducibility claims определены `DU-27`.

---

# 15. Privileged Ground Truth

Evaluator может иметь доступ к hidden Environment state/ResearchAnnotation.

Но:

```text
Evaluator Ground Truth
≠ Agent input
```

Использование privileged data в training разрешено только explicit privileged-supervision condition.

---

# 16. Policy vs Action Gate attribution

Final system success не равен Policy quality.

Отдельно анализируются:

```text
SelectedActionIntent
Action Gate rejection/normalization/override
committed/executed action
final outcome
```

Сильный shield не должен скрывать слабую Policy.

---

# 17. Отрицательные результаты

Отрицательный result — полноценный evidence.

Если module effect объясняется matched control или negative gate выполняется, это основание для interpretation/design review, а не повод скрывать result.

Architecture меняется только через ADR.

---

# 18. Антропоморфные ограничения

Запрещены переходы:

```text
valence → доказано чувство
Self Model → доказано самосознание
Workspace → доказано сознание
```

MINDRA использует functional cognitive terms; phenomenological claims требуют отдельного evidence, которого architecture сама по себе не предоставляет.

---

# 19. Сила claim ограничена силой evidence

Conceptually:

```text
descriptive correlation
< predictive evidence
< ablation/control
< matched intervention
< replicated/generalized causal evidence
```

Exact levels/assumptions определяет конкретный study. Не заявлять causal/general claim сильнее, чем позволяет design.

---

# 20. Текущая граница

После `DU-28` уже приняты semantic requirements для:

- evaluation conditions/suites/runs/units;
- controls/matched controls;
- causal interventions;
- module gates;
- metric/statistical protocol;
- reproducibility/compute attribution.

По-прежнему **не фиксируются до version design**:

- конкретный benchmark suite/task catalog;
- exact number of seeds;
- universal statistical test/threshold;
- universal composite score;
- plotting/tracking framework;
- implementation storage format.

Следующий design scope — `DU-29 — Engineering Testing`.
