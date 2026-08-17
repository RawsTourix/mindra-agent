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
│   └── DU-20-memory-regulation-consolidation-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
└── verification/          # появится позже
```

---

# Literature research pass

Текущие pass:

- [`literature/DU-10-cortex-landscape-2026-08.md`](literature/DU-10-cortex-landscape-2026-08.md) — Cortex candidates/tooling;
- [`literature/DU-11-memory-landscape-2026-08.md`](literature/DU-11-memory-landscape-2026-08.md) — Memory/retrieval/indexes;
- [`literature/DU-12-world-model-landscape-2026-08.md`](literature/DU-12-world-model-landscape-2026-08.md) — world models/uncertainty;
- [`literature/DU-13-self-model-landscape-2026-08.md`](literature/DU-13-self-model-landscape-2026-08.md) — competence/calibration;
- [`literature/DU-14-intrinsic-signals-landscape-2026-08.md`](literature/DU-14-intrinsic-signals-landscape-2026-08.md) — novelty/information/learning progress;
- [`literature/DU-15-drives-landscape-2026-08.md`](literature/DU-15-drives-landscape-2026-08.md) — drive/homeostatic dynamics;
- [`literature/DU-16-appraisal-landscape-2026-08.md`](literature/DU-16-appraisal-landscape-2026-08.md) — multidimensional appraisal;
- [`literature/DU-17-affect-dynamics-landscape-2026-08.md`](literature/DU-17-affect-dynamics-landscape-2026-08.md) — persistent Affect;
- [`literature/DU-18-valuation-landscape-2026-08.md`](literature/DU-18-valuation-landscape-2026-08.md) — multi-objective valuation/risk;
- [`literature/DU-19-salience-attention-landscape-2026-08.md`](literature/DU-19-salience-attention-landscape-2026-08.md) — salience, selective processing, adaptive compute, budgeted attention и routing;
- [`literature/DU-20-memory-regulation-consolidation-landscape-2026-08.md`](literature/DU-20-memory-regulation-consolidation-landscape-2026-08.md) — episodic retention, forgetting/eviction, replay, source-preserving consolidation и retain-vs-consolidate trade-offs.

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

Для будущих экспериментов заранее фиксировать:

- hypothesis;
- independent variables;
- baseline/control;
- seeds;
- environment/data versions;
- metrics;
- success/falsification criterion;
- analysis policy.

Для Memory Regulation особенно важны:

```text
Full Regulation
vs FIFO/recency/random/shuffled
vs NoRegulation

Full Consolidation
vs episodic-only
vs random/matched compression
```

и раздельные метрики:

```text
behavioral utility
retention efficiency
source fidelity
contradiction preservation
false derived-memory rate
budget efficiency
generalization
```

Compression ratio без functional correctness не считается достаточным evidence полезной consolidation.

---

# Результаты

Любой result должен быть связан с конкретными commit/config/checkpoint/seed/environment version/raw artifacts/metrics/limitations.

Отрицательные результаты сохраняются наравне с положительными.

---

# Текущий статус

Experiment/hypothesis registry ещё не создан. Сейчас журнал используется в основном для датированных literature pass и не должен смешиваться с canonical design.
