# ADR-0028 — Multi-layer causal Evaluation Harness вместо universal leaderboard score

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-28 — MINDRA-Eval`

---

# 1. Контекст

После `DU-27` MINDRA имеет:

- modular cognitive boundaries;
- explicit controls/ablations/interventions;
- immutable Experience/Evidence lineage;
- Training Runtime и revision lifecycle;
- verified checkpoints/restore profiles;
- software/hardware/compute manifests.

Нужно определить evaluation architecture, способную ответить не только:

> «какая configuration получила больший task score?»

но и:

- какой механизм дал causal functional effect;
- не объясняется ли effect дополнительной capacity/compute/data/context;
- сохраняется ли effect по stochastic replicates/world distributions/Cortex conditions;
- насколько subsystem predictions calibrated;
- сколько реально стоил результат;
- достаточно ли evidence для конкретного research claim.

---

# 2. Вариант A — Universal leaderboard score

Conceptually:

```text
all metrics
→ weighted aggregation
→ MINDRA Score = 87.4
```

## Плюсы

- очень просто сравнивать configurations;
- удобно строить leaderboard;
- легко оптимизировать одну objective.

## Минусы

- скрывает trade-offs;
- смешивает task success, calibration, compute, safety/constraints и causal evidence;
- требует arbitrary weights/normalization;
- позволяет улучшить composite score, ухудшив критически важный subsystem;
- не доказывает вклад конкретных boundaries;
- создаёт Goodhart-like pressure на один показатель.

**Решение:** отклонён как canonical architecture. Optional aggregate score разрешён как derived policy конкретного suite.

---

# 3. Вариант B — End-task benchmark + обычные ablations

Conceptually:

```text
Full score
vs
Full - Module X score
```

## Плюсы

- значительно лучше universal score;
- простой research workflow;
- понятный contribution estimate.

## Минусы

Ablation часто одновременно меняет:

- parameter count;
- recurrent state capacity;
- compute;
- context;
- information routing;
- training dynamics.

Поэтому:

```text
Full > NoX
```

не всегда означает:

> semantics X полезна.

Также обычная ablation:

- не проверяет intervention specificity;
- не использует сильную checkpoint branching capability MINDRA;
- плохо отделяет Policy от Action Gate;
- не решает nested stochastic replicate problem.

**Решение:** ablation остаётся обязательным инструментом, но недостаточна как общая evaluation architecture.

---

# 4. Вариант C — Module-local metrics без общей Evaluation Runtime

Каждый subsystem сам определяет и вычисляет свои metrics.

## Плюсы

- близко к semantic owner;
- удобно для локальной диагностики;
- меньше центральной infrastructure.

## Минусы

- metrics начинают видеть разный Ground Truth/context;
- сложно обеспечить test isolation;
- трудно сравнивать conditions и matched resources;
- повышается риск скрытого leakage evaluator data в cognition;
- statistical/reproducibility protocol фрагментируется;
- end-to-end attribution становится неясной.

**Решение:** module design определяет metric semantics, но execution/ground-truth access/statistical/report infrastructure принадлежит общей Evaluation Plane.

---

# 5. Вариант D — Multi-layer causal Evaluation Harness

Conceptually:

```text
EvaluationStudyPlan
       ↓
fully specified EvaluationCondition(s)
       ↓
Evaluation Runtime
       ↓
raw run / unit / metric evidence
       ↓
controls + matched controls
       ↓
paired interventions where possible
       ↓
statistical analysis
       ↓
Task + Diagnostic + Causal + Compute + Reproducibility profile
```

Основные свойства:

1. `Evaluation Runtime` вне Agent;
2. condition pin'ит checkpoint/world/revisions/resources/data/software/hardware;
3. one-number score optional, не canonical;
4. typed metrics;
5. explicit experimental/statistical units;
6. stochastic interval/distribution evidence;
7. `No*`/random/shuffled/matched controls first-class;
8. paired counterfactual interventions поверх verified checkpoints;
9. actual compute/resource normalization;
10. Policy pre-Gate и post-Gate system attribution отдельно;
11. confirmatory study имеет pre-specified primary analysis;
12. conditional module boundaries имеют explicit negative gates;
13. result/report имеет lineage до raw Experience/Evidence;
14. claim strength bounded evidence strength.

## Плюсы

- соответствует исследовательской цели MINDRA;
- использует уже спроектированные interventions/checkpoints/manifests;
- различает semantic contribution и generic capacity;
- позволяет сохранить отрицательные результаты;
- подходит для маленького MicroWorld и будущих больших environments;
- не зависит от конкретной metrics/statistics library.

## Минусы

- сложнее обычного benchmark runner;
- требует аккуратной experiment planning;
- matched controls могут быть дорогими;
- paired causal restore возможен не для всех external environments/providers;
- некоторые claims потребуют много compute/seeds.

**Решение:** принят.

---

# 6. Почему EvaluationCondition — first-class

Главная единица сравнения — не название architecture, а fully specified condition.

Две configurations нельзя считать отличающимися «только Module X», если одновременно изменились:

- Cortex;
- checkpoint;
- training seed;
- tuning budget;
- data;
- actual compute;
- action shield;
- world distribution.

Поэтому `EvaluationCondition` и `ResourceMatchProfile` являются частью architecture evaluation contract.

---

# 7. Почему experimental unit explicit

MINDRA имеет nested stochasticity:

```text
training seed
  ↓
checkpoint
  ↓
world seed
  ↓
episode
  ↓
decision windows
```

100 episodes одного checkpoint не дают 100 independent training algorithm replicates.

Следовательно statistical plan обязан указывать analysis unit, nesting/blocking и replicate axis.

---

# 8. Почему paired counterfactual — отдельный сильный режим

`DU-27` позволяет в clonable MicroWorld восстанавливать один causal base state.

Это позволяет:

```text
same checkpoint + same world
        ↓
control branch
vs
intervention branch
```

и существенно сильнее обычного сравнения двух независимо прожитых trajectories.

Но если restore requirements не выполняются, study не имеет права называть independent runs exact counterfactual branches.

---

# 9. Почему matched controls обязательны не всегда, но first-class

Для некоторых questions `NoX` достаточно.

Но условные boundaries вроде:

- Affect;
- Workspace;
- Planner;
- Executive Control

по своей природе добавляют persistent state/compute/routing capacity.

Поэтому architecture должна уметь сравнить их с generic matched-capacity/compute controls, иначе functional semantics нельзя отделить от дополнительной мощности.

---

# 10. Почему Policy и Action Gate оцениваются отдельно

Сильный Gate может исправить плохую Policy.

Если смотреть только final success:

```text
poor Policy
+
strong shield
→ high system success
```

может выглядеть как хорошая Policy.

MINDRA-Eval поэтому обязательно сохраняет:

```text
SelectedActionIntent metrics
Gate metrics
post-Gate committed/executed outcome metrics
```

---

# 11. Почему no fixed statistics

Разные claims имеют разные units/distributions/dependence structures.

Например:

- paired branch contrast;
- training-replicate comparison;
- task-family aggregate;
- calibration probability scoring;
- performance/compute frontier

не обязаны использовать один statistical test.

Поэтому canonical boundary фиксирует `StatisticalAnalysisPlan`, а не t-test/bootstrap/alpha.

---

# 12. Последствия

После принятия ADR:

- новый benchmark result без `EvaluationCondition` provenance считается неполным;
- stochastic claim без uncertainty/distribution evidence недостаточен;
- сильный module claim требует соответствующих controls/interventions;
- composite score не является source of truth research evidence;
- evaluator Ground Truth остаётся privileged;
- condition tuning/data/compute differences входят в attribution;
- module gates могут дать отрицательный result и инициировать design review;
- exact implementation library выбирается позднее.

---

# 13. Что ADR не фиксирует

- concrete benchmark suite;
- exact number of seeds;
- exact statistical tests;
- alpha/multiplicity correction;
- plotting/report format;
- database/artifact store;
- evaluation framework;
- universal score;
- exact MicroWorld tasks;
- exact CI/permutation/bootstrap implementation.

---

# 14. Принятое решение

```text
EvaluationStudyPlan
        ↓
EvaluationCondition(s)
        ↓
Evaluation Runtime
        ↓
Typed evidence/metrics
        ↓
Controls + paired interventions
        ↓
StatisticalAnalysisPlan
        ↓
Multi-layer EvaluationReport
```

с optional derived aggregate scores, но без universal leaderboard semantics.
