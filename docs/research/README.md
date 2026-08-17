# Исследовательский журнал MINDRA

## Назначение

Этот каталог хранит датированные literature/research pass, будущие hypotheses, experiments, results и verification evidence.

Каноническая архитектура живёт в `docs/design/`; research evidence само по себе design не меняет.

---

# Текущая структура

```text
research/
├── README.md
├── literature/
│   ├── DU-10-cortex-landscape-2026-08.md
│   ├── ...
│   ├── DU-26-training-lifecycle-landscape-2026-08.md
│   ├── DU-27-checkpoint-reproducibility-compute-landscape-2026-08.md
│   └── DU-28-mindra-eval-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
└── verification/          # появится позже
```

---

# Literature research pass

Текущие pass `DU-10 … DU-28` находятся в [`literature/`](literature/).

Последние:

- [`literature/DU-26-training-lifecycle-landscape-2026-08.md`](literature/DU-26-training-lifecycle-landscape-2026-08.md) — optimizer/training state ownership, PEFT, actor/learner policy lag, continual forgetting и candidate-revision activation;
- [`literature/DU-27-checkpoint-reproducibility-compute-landscape-2026-08.md`](literature/DU-27-checkpoint-reproducibility-compute-landscape-2026-08.md) — reproducibility constraints, training-resume state, RNG, distributed/sharded checkpointing, artifact manifests и compute provenance;
- [`literature/DU-28-mindra-eval-landscape-2026-08.md`](literature/DU-28-mindra-eval-landscape-2026-08.md) — reliable RL statistics, replicate/task-distribution semantics, calibration/proper scoring, matched-compute agent evaluation, robustness и causal intervention principles.

Эти документы **не выбирают** canonical implementation framework/algorithm.

---

# Research discipline

Правильный путь изменения архитектуры:

```text
research evidence / experiment result
→ interpretation
→ design review
→ ADR при существенном выборе
→ canonical design update
→ implementation/version update
```

Для будущих экспериментов заранее фиксировать hypothesis, independent variables, baselines/controls, replicate axes, environment/data versions, metrics, success/falsification criterion и analysis policy.

После `DU-28` confirmatory study должен, где применимо, ссылаться на:

```text
EvaluationStudyPlan / EvaluationManifest
EvaluationCondition(s)
checkpoint + RestoreProfile
world/task distributions
controls/interventions
ReplicateStructure
MetricSpec(s)
StatisticalAnalysisPlan
software/hardware/RNG/compute provenance
```

Обязательные evaluation-validity проверки:

- evaluator Ground Truth leakage;
- experimental/statistical unit correctness;
- nested replicate/pseudo-replication risk;
- matched/unmatched parameters/state/context/data/compute;
- baseline tuning fairness;
- checkpoint/base-state alignment;
- paired intervention restore validity;
- Policy vs Action Gate attribution;
- stochastic uncertainty/interval evidence;
- invalid/censored/`execution_unknown` handling;
- primary vs exploratory metrics;
- module negative gates;
- actual compute attribution;
- report lineage до raw Evidence/Experience.

Training/evaluation improvement не считается чистым результатом algorithm/module, если condition получила больший фактический compute, другой restore state, другую data/tuning condition, privileged labels или более сильный Action Gate без отдельной attribution.

---

# Результаты

Любой result должен быть связан с конкретными commit/config/checkpoint/restore profile/agent revision/environment distribution/evaluation condition/raw artifacts/data/training refs/software/hardware/compute manifests/metric+analysis revisions/limitations.

Отрицательные результаты сохраняются наравне с положительными.

Conditionally accepted module boundary может быть пересмотрена после отрицательного module-gate evidence только через design review/ADR.

---

# Текущий статус

Experiment/hypothesis registry ещё не создан. Сейчас журнал используется в основном для датированных literature pass и не должен смешиваться с canonical design.
