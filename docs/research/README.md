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
│   ├── DU-27-checkpoint-reproducibility-compute-landscape-2026-08.md
│   ├── DU-28-mindra-eval-landscape-2026-08.md
│   └── DU-29-engineering-testing-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
└── verification/          # появится позже
```

---

# Literature / tool research pass

Текущие pass `DU-10 … DU-29` находятся в [`literature/`](literature/).

Последние:

- [`literature/DU-27-checkpoint-reproducibility-compute-landscape-2026-08.md`](literature/DU-27-checkpoint-reproducibility-compute-landscape-2026-08.md) — reproducibility/checkpoint/compute evidence;
- [`literature/DU-28-mindra-eval-landscape-2026-08.md`](literature/DU-28-mindra-eval-landscape-2026-08.md) — reliable evaluation/statistics/calibration/matched-control evidence;
- [`literature/DU-29-engineering-testing-landscape-2026-08.md`](literature/DU-29-engineering-testing-landscape-2026-08.md) — property/state-machine testing, architecture dependency checks, flaky/determinism guidance и engineering-verification implications.

Эти документы **не выбирают** canonical implementation framework/algorithm/tool.

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

Для будущих confirmatory experiments действуют requirements `DU-28`.

Engineering evidence `DU-29` хранится отдельно от research evidence:

```text
contract/invariant test passed
≠
mechanism functionally useful
```

и наоборот research result не отменяет необходимость machine-checkable correctness.

После реализации Verification Plane должен позволять трассировать:

```text
accepted design/ADR invariant
→ VerificationObligation
→ EngineeringTestSpec
→ EngineeringTestRun
→ VerificationEvidence
```

При этом research result продолжает трассироваться через `EvaluationStudyPlan / EvaluationCondition / MetricSpec / StatisticalAnalysisPlan`.

---

# Результаты

Любой research result должен быть связан с конкретными commit/config/checkpoint/restore profile/agent revision/environment distribution/evaluation condition/raw artifacts/data/training refs/software/hardware/compute manifests/metric+analysis revisions/limitations.

Любой engineering verification result должен быть связан минимум с repository revision, test spec, relevant environment profile и obligation refs.

Отрицательные research results и engineering failures сохраняются; ни одни из них не переписывают design автоматически.

---

# Текущий статус

Experiment/hypothesis registry ещё не создан. Сейчас журнал используется в основном для датированных research/tool pass и не должен смешиваться с canonical design.
