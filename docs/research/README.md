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
│   ├── DU-23-policy-planner-landscape-2026-08.md
│   └── DU-24-action-boundary-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
└── verification/          # появится позже
```

---

# Literature research pass

Текущие pass `DU-10 … DU-24` находятся в [`literature/`](literature/).

Последние:

- [`literature/DU-22-executive-control-landscape-2026-08.md`](literature/DU-22-executive-control-landscape-2026-08.md) — adaptive computation, metareasoning, budget allocation и stopping;
- [`literature/DU-23-policy-planner-landscape-2026-08.md`](literature/DU-23-policy-planner-landscape-2026-08.md) — reactive/direct Policy, online planning/search, belief-space planning, LLM-assisted planning и action-grounding boundaries;
- [`literature/DU-24-action-boundary-landscape-2026-08.md`](literature/DU-24-action-boundary-landscape-2026-08.md) — shielding/runtime assurance, action lifecycle/correlation, authorization placement и retry/idempotency semantics.

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

Для Action Boundary особенно важны:

```text
PassThrough/SchemaOnly Gate
vs Capability/Constraint Gate
vs explicit Shield/RuntimeAssurance
vs Random/Shuffled rejection controls
```

Нужно отдельно измерять:

- Policy quality **до** Gate по `SelectedActionIntent`;
- Gate accept/reject/override behavior;
- stale/malformed/capability rejection rate;
- false/over-conservative rejection;
- предотвращённые constraint violations;
- external override rate и attribution;
- dispatch attempts/retries;
- duplicate suppression;
- `execution_unknown` frequency;
- Environment no-effect/partial/abort outcomes;
- complete intent→outcome correlation.

Для retry/idempotency нужны failure-injection experiments:

```text
definitely-not-sent
acknowledgement lost after possible send
duplicate retry attempt
partial execution
```

Policy нельзя считать успешной за behavior-changing action, созданный external shield/override, без отдельной attribution analysis.

Сложный Gate/override не считается обоснованным, если simpler pass-through/schema/capability controls дают тот же safety/validity result.

---

# Результаты

Любой result должен быть связан с конкретными commit/config/checkpoint/seed/environment version/raw artifacts/metrics/limitations.

Отрицательные результаты сохраняются наравне с положительными.

---

# Текущий статус

Experiment/hypothesis registry ещё не создан. Сейчас журнал используется в основном для датированных literature pass и не должен смешиваться с canonical design.
