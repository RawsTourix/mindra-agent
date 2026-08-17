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
│   ├── DU-24-action-boundary-landscape-2026-08.md
│   └── DU-25-experience-data-replay-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
└── verification/          # появится позже
```

---

# Literature research pass

Текущие pass `DU-10 … DU-25` находятся в [`literature/`](literature/).

Последние:

- [`literature/DU-23-policy-planner-landscape-2026-08.md`](literature/DU-23-policy-planner-landscape-2026-08.md) — reactive/direct Policy, online planning/search, belief-space planning, LLM-assisted planning и action-grounding boundaries;
- [`literature/DU-24-action-boundary-landscape-2026-08.md`](literature/DU-24-action-boundary-landscape-2026-08.md) — shielding/runtime assurance, action lifecycle/correlation, authorization placement и retry/idempotency semantics;
- [`literature/DU-25-experience-data-replay-landscape-2026-08.md`](literature/DU-25-experience-data-replay-landscape-2026-08.md) — RLDS/Minari episode-step datasets, Reverb replay infrastructure, hindsight relabeling, provenance и causal source/projection separation.

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

Для Experience / Data / Replay особенно проверять:

```text
full causal projection
vs transition-only projection

agent-visible-only dataset
vs explicit privileged-supervision dataset

natural-only source
vs mixed intervention/replay data

correct sequence
vs shuffled sequence

uniform replay
vs prioritized/other replay
```

Обязательные data-quality проверки:

- source event immutability;
- source→derived transformation lineage;
- privileged annotation leakage;
- changing `agent_revision` attribution;
- `execution_unknown`/no-transition handling;
- termination vs truncation;
- late/out-of-order event correlation;
- schema migration;
- representation revision preservation;
- dataset split/source-group leakage;
- deterministic extraction/sampling metadata;
- replay population/sampler revision;
- required causal event vs optional artifact completeness.

Training improvement не считается чистым результатом конкретного algorithm, если он объясняется скрытым privileged data, different source population или дополнительной relabeling/transformation policy.

---

# Результаты

Любой result должен быть связан с конкретными commit/config/checkpoint/seed/environment version/raw artifacts/dataset manifest/metrics/limitations.

Отрицательные результаты сохраняются наравне с положительными.

---

# Текущий статус

Experiment/hypothesis registry ещё не создан. Сейчас журнал используется в основном для датированных literature pass и не должен смешиваться с canonical design.
