# Исследовательская методология MINDRA

## Статус документа

Этот документ фиксирует общие правила постановки, проведения и интерпретации исследований MINDRA.

Он не задаёт concrete benchmark/library/statistical implementation. После `DU-28` evaluation semantics определяется [`design/mindra-eval.md`](design/mindra-eval.md), Engineering Verification — [`design/engineering-testing.md`](design/engineering-testing.md), а конкретная discipline формирования/пересмотра claims и limitations — [`design/research-claims-limitations.md`](design/research-claims-limitations.md).

---

# 1. Главный принцип

MINDRA развивается не по схеме «добавили модуль — стало сложнее — значит стало лучше», а:

```text
гипотеза
→ контролируемый design
→ реализация
→ experiment
→ evidence
→ observation / interpretation
→ scoped claim
→ design review при необходимости
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

# 2. Engineering correctness ≠ research validity ≠ claim strength

Корректно реализованный модуль может не подтверждать research hypothesis.

Интересный единичный результат не является достаточным evidence, если implementation/protocol/reproducibility нарушены.

Даже валидный result не разрешает claim шире, чем поддерживают scope/design/evidence.

```text
Engineering Testing (DU-29)
≠
MINDRA-Eval (DU-28)
≠
Research Claim discipline (DU-30)
```

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

Causal wording в отчёте затем ограничивается правилами `DU-30`.

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

Claim generalization scope не расширяется дальше реально поддержанного target scope.

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

Architecture gain, существующий только с одним Cortex, формулируется узко и получает соответствующую limitation/ClaimScope.

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

Если perfect matching невозможно, показывается trade-off/frontier и limitation.

Compute provenance определяется `DU-27`, comparison semantics — `DU-28`, wording/claim scope — `DU-30`.

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

DU-30 дополнительно запрещает выдавать exploratory interpretation за заранее подтверждавшийся confirmatory claim.

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

Independent replication scientific effect остаётся отдельным evidence question.

---

# 15. Privileged Ground Truth

Evaluator может иметь доступ к hidden Environment state/ResearchAnnotation.

Но:

```text
Evaluator Ground Truth
≠ Agent input
```

Использование privileged data в training разрешено только explicit privileged-supervision condition.

Research Claim обязан учитывать privileged condition в scope/limitations, если она material.

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

Claim о Policy и claim о full-system behavior являются разными claims.

---

# 17. Отрицательные, null и inconclusive результаты

Отрицательный result — полноценный evidence.

Но различаются:

```text
negative evidence
null estimate
inconclusive
invalid
not measured
```

Если module effect объясняется matched control или negative gate выполняется, это основание для `ClaimReview` и design review.

Architecture меняется только через ADR.

---

# 18. Антропоморфные / phenomenological ограничения

Запрещены inference leaps:

```text
valence/Affect → доказано чувство
Self Model → доказано самосознание
Workspace → доказано сознание
Cortex first-person text → достоверный phenomenal self-report
human-like behavior → human-like phenomenology
functional analogy → biological identity
```

MINDRA использует functional cognitive terms; phenomenological claims требуют отдельного bridge evidence, которого architecture сама по себе не предоставляет.

Это не утверждение об отсутствии subjective experience; это ограничение допустимой научной формулировки при текущем evidence.

---

# 19. Claim scope / limitations / known unknowns

После `DU-30` substantial claim оформляется как versioned artifact с:

```text
ClaimScope
supporting/challenging evidence
assumptions
Limitations
KnownUnknowns
status / reviews / supersession
```

Обязательный принцип:

```text
claim strength ≤ evidence strength
claim generality ≤ supported scope
```

Old claim не переписывается молча при новом evidence; используется review/weaken/narrow/supersede lifecycle.

---

# 20. Текущая граница

После `DU-28 … DU-30` приняты semantic requirements для:

- evaluation conditions/suites/runs/units;
- controls/matched controls;
- causal interventions;
- module gates;
- metric/statistical protocol;
- reproducibility/compute attribution;
- engineering verification obligations/evidence;
- scoped versioned research claims;
- limitations/known unknowns;
- negative evidence и claim supersession;
- consciousness/anthropomorphic claim boundaries.

По-прежнему **не фиксируются до version design**:

- конкретный benchmark suite/task catalog;
- exact number of seeds;
- universal statistical test/threshold;
- universal evidence-strength score;
- universal composite score;
- paper/preregistration/tracking framework;
- implementation storage format.

Следующий design scope — `DU-31 — Contract + ADR Consistency Freeze`.
