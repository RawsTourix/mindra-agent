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
│   ├── DU-22-executive-control-landscape-2026-08.md
│   └── DU-23-policy-planner-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
└── verification/          # появится позже
```

---

# Literature research pass

Текущие pass `DU-10 … DU-23` находятся в [`literature/`](literature/).

Последние:

- [`literature/DU-21-workspace-landscape-2026-08.md`](literature/DU-21-workspace-landscape-2026-08.md) — bounded workspace/broadcast и ограничения consciousness claims;
- [`literature/DU-22-executive-control-landscape-2026-08.md`](literature/DU-22-executive-control-landscape-2026-08.md) — adaptive computation, metareasoning, budget allocation и stopping;
- [`literature/DU-23-policy-planner-landscape-2026-08.md`](literature/DU-23-policy-planner-landscape-2026-08.md) — reactive/direct Policy, learned world-model policies, online planning/search, belief-space planning, LLM-assisted planning и action-grounding boundaries.

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

Для Policy / Planner особенно важны:

```text
Policy + Planner
vs ReactivePolicy / NoPlanner
vs Depth1 / fixed-lookahead planner
vs Random/Shuffled plan
vs Matched search/recurrent control
```

Нужно отдельно измерять:

- actual planning compute;
- long-horizon/compositional success;
- contingent planning при partial observability;
- candidate quality/diversity;
- plan validity/replanning;
- robustness к World Model error;
- constraint/risk behavior;
- generalization;
- planning overhead.

Положительный Planner result не считается доказанным, если configuration просто использовала больше compute/state capacity или World Model oracle information.

Для Policy отдельно проверять causal sensitivity selection к `ComparisonPolicy`, risk/constraint evidence и stochastic RNG, не смешивая quality Valuation и quality final selector.

---

# Результаты

Любой result должен быть связан с конкретными commit/config/checkpoint/seed/environment version/raw artifacts/metrics/limitations.

Отрицательные результаты сохраняются наравне с положительными.

---

# Текущий статус

Experiment/hypothesis registry ещё не создан. Сейчас журнал используется в основном для датированных literature pass и не должен смешиваться с canonical design.
