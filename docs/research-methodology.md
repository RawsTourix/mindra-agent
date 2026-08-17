# Исследовательская методология MINDRA

## Статус документа

Этот документ фиксирует общие правила постановки, проведения и интерпретации исследований MINDRA.

После принятых design updates:

- evaluation semantics — [`design/mindra-eval.md`](design/mindra-eval.md), `DU-28`;
- Engineering Verification — [`design/engineering-testing.md`](design/engineering-testing.md), `DU-29`;
- claim/limitations discipline — [`design/research-claims-limitations.md`](design/research-claims-limitations.md), `DU-30`;
- semantic consistency baseline — [`design/contract-adr-consistency-freeze.md`](design/contract-adr-consistency-freeze.md), `DU-31`.

Этот документ не задаёт concrete benchmark/library/statistical implementation.

---

# 1. Главный принцип

MINDRA развивается не по схеме «добавили модуль — стало сложнее — значит стало лучше», а:

```text
гипотеза
→ контролируемый design
→ implementation + verification
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

```text
Engineering Testing (DU-29)
≠
MINDRA-Eval (DU-28)
≠
Research Claims / Limitations (DU-30)
```

Корректно реализованный модуль может не подтверждать research hypothesis.

Интересный результат не является sufficient evidence, если implementation/protocol/reproducibility invalid.

Даже валидный result не разрешает claim шире, чем поддерживают scope/design/evidence.

---

# 3. Гипотеза должна быть falsifiable

Перед confirmatory experiment формулируется outcome, способный ослабить/опровергнуть hypothesis.

Плохо:

> Appraisal делает агента более человечным.

Лучше:

> При aligned base state intervention в appraisal dimension систематически меняет заранее указанный downstream outcome при ограниченных off-target effects.

Module gates и EvaluationStudyPlan задаются `DU-28`.

---

# 4. Baseline / ablation / matched control

Ablation:

```text
Full
vs
Full - X
```

полезна, но может менять capacity/compute.

Для claim о **semantic contribution** используются, где feasible:

- `No*`;
- constant/random/shuffled;
- rule-based;
- parameter/state-capacity matched;
- context/compute/data matched;
- oracle research controls.

Matching factors/deviations описываются `EvaluationCondition/ResourceMatchProfile`.

---

# 5. Causal intervention

Корреляция internal state и behavior недостаточна для сильного causal claim.

Желательный pattern:

```text
verified common base state
→ control branch
→ treatment branch with Intervention X
→ compare target + off-target effects
```

Paired counterfactual требует достаточного `DU-27` restore level и explicit `DU-28` protocol.

Causal wording затем ограничивается `DU-30`.

---

# 6. Factorial interactions

Если механизм полезен только совместно с другим, допускается hypothesis-driven subset:

```text
none
A
B
A+B
```

Full factorial всей MINDRA не требуется автоматически.

---

# 7. Replicates и stochasticity

Различаются:

```text
training replicate
checkpoint replicate
world replicate
episode replicate
policy stochastic replicate
counterfactual branch
```

Много episodes одного checkpoint не являются independent training replicates.

Количество replicates/statistical method задаются конкретными `ReplicateStructure + StatisticalAnalysisPlan`, а не глобальным магическим числом seeds.

---

# 8. Train / validation / test separation

Если world/data использованы для training/model selection, confirmatory generalization evaluation использует held-out conditions.

Различаются:

- memorization;
- adaptation;
- in-distribution generalization;
- compositional/generalization shift;
- transfer/OOD.

Использование test outcome для ручной настройки превращает test в development evidence.

Claim scope не расширяется дальше реально поддержанного target scope.

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

Architecture gain, существующий только с одним Cortex, формулируется узко.

---

# 10. Parameter / compute / data / tuning controls

Improvement нельзя автоматически приписывать architecture, если treatment имеет больше:

- parameters/state capacity;
- context/Memory/Workspace capacity;
- Cortex calls;
- training data/steps;
- runtime rollout/search;
- tuning budget;
- actual compute.

Если perfect matching невозможно, показывается trade-off/frontier и limitation.

Compute provenance — `DU-27`, comparison — `DU-28`, wording/scope — `DU-30`.

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

Metric architecture — `DU-28`.

---

# 12. Calibration

Accuracy и confidence calibration — разные axes.

Если subsystem заявляет meaningful probability, evaluation использует metric family, соответствующую probability semantics, где practically possible — proper scoring.

ECE-like summary не является universal proof truthful probability.

---

# 13. Exploratory vs confirmatory

Exploratory runs разрешены для debugging/hypothesis generation/range selection.

Confirmatory study заранее фиксирует:

- hypothesis;
- conditions/controls;
- primary contrasts/metrics;
- replicate/sample policy;
- statistical analysis;
- exclusions/censoring/stopping;
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

Independent replication scientific effect остаётся отдельным evidence question.

---

# 15. Privileged Ground Truth

Evaluator может иметь доступ к hidden Environment state/ResearchAnnotation.

Но:

```text
Evaluator Ground Truth
≠ Agent input
```

Privileged data в training разрешены только explicit privileged-supervision condition.

Claim обязан учитывать такую condition в scope/limitations, если material.

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

# 17. Negative / null / inconclusive

Различаются:

```text
negative evidence
null estimate
inconclusive
invalid
not measured
```

Negative module gate создаёт `ClaimReview` и design review. Architecture меняется только через ADR.

---

# 18. Phenomenological ограничения

Запрещены inference leaps:

```text
Affect/valence → доказано чувство
Self Model → доказано самосознание
Workspace → доказано сознание
Cortex first-person text → reliable phenomenal self-report
human-like behavior → human-like phenomenology
functional analogy → biological identity
```

Это не утверждение об отсутствии subjective experience; это ограничение допустимой формулировки при текущем evidence.

---

# 19. Claim scope / limitations / known unknowns

Substantial claim оформляется как versioned artifact с:

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

Old claim не переписывается молча при новом evidence.

---

# 20. Semantic freeze и research design

После `DU-31` research/version work использует `Semantic Freeze Baseline F31`.

Это означает:

- research condition может включать `No*`/Dummy/control implementation frozen boundary;
- experiment не переопределяет semantic owner/lifecycle;
- отрицательный result может инициировать новый ADR, но не silent architecture mutation;
- concrete implementation choice не повышается до architecture claim автоматически;
- version roadmap обязан сохранять controls и falsifiable module gates.

Breaking semantic change после F31 требует нового ADR.

---

# 21. Что не фиксируется глобально

По-прежнему не существует universal:

- benchmark suite/task catalog;
- exact number of seeds;
- statistical test/threshold;
- evidence-strength score;
- composite score;
- paper/preregistration/tracking framework;
- implementation storage format.

Это выбирается конкретным study/version при сохранении F31 и `DU-28…30` semantics.

---

# 22. Текущий design scope

`DU-31` завершён; baseline `F31` принят.

Следующий допустимый этап:

```text
DU-32 — Version Roadmap
```

Roadmap должен выбрать реалистичные implementation milestones, но не переопределять semantic-frozen architecture без нового ADR.
