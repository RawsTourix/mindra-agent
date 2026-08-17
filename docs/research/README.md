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
│   ├── DU-11-memory-landscape-2026-08.md
│   ├── DU-12-world-model-landscape-2026-08.md
│   ├── DU-13-self-model-landscape-2026-08.md
│   ├── DU-14-intrinsic-signals-landscape-2026-08.md
│   ├── DU-15-drives-landscape-2026-08.md
│   ├── DU-16-appraisal-landscape-2026-08.md
│   ├── DU-17-affect-dynamics-landscape-2026-08.md
│   ├── DU-18-valuation-landscape-2026-08.md
│   ├── DU-19-salience-attention-landscape-2026-08.md
│   ├── DU-20-memory-regulation-consolidation-landscape-2026-08.md
│   ├── DU-21-workspace-landscape-2026-08.md
│   └── DU-22-executive-control-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
└── verification/          # появится позже
```

---

# Literature research pass

Текущие pass `DU-10 … DU-22` находятся в [`literature/`](literature/).

Последние:

- [`literature/DU-20-memory-regulation-consolidation-landscape-2026-08.md`](literature/DU-20-memory-regulation-consolidation-landscape-2026-08.md) — retention/forgetting/replay/consolidation;
- [`literature/DU-21-workspace-landscape-2026-08.md`](literature/DU-21-workspace-landscape-2026-08.md) — bounded workspace/broadcast и ограничения consciousness claims;
- [`literature/DU-22-executive-control-landscape-2026-08.md`](literature/DU-22-executive-control-landscape-2026-08.md) — adaptive computation, metareasoning, competence-aware control, tool-use triggers, budget allocation и stopping.

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

Для будущих экспериментов заранее фиксировать hypothesis, independent variables, baselines/controls, seeds, environment/data versions, metrics, success/falsification criterion и analysis policy.

Для Executive Control особенно важны:

```text
Adaptive Executive
vs NoExecutive / fixed schedule
vs FixedBudget
vs Random allocation
vs SimpleThreshold
vs SalienceOnly / uncertainty-only
vs CostUnaware
vs Matched learned router
```

Сравнение обязательно вести по:

```text
task performance
vs
actual cognitive resource consumption
```

а не только по accuracy.

Нужны budget sweeps, competence/uncertainty/cost interventions, capability degradation tests, operation-selection/stopping distributions и controller-overhead accounting.

Positive result не считается доказанным, если adaptive system просто использовал больше Cortex calls/rollout steps/total compute.

---

# Результаты

Любой result должен быть связан с конкретными commit/config/checkpoint/seed/environment version/raw artifacts/metrics/limitations.

Отрицательные результаты сохраняются наравне с положительными.

---

# Текущий статус

Experiment/hypothesis registry ещё не создан. Сейчас журнал используется в основном для датированных literature pass и не должен смешиваться с canonical design.
