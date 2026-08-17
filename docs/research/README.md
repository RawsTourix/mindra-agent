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
│   ├── DU-25-experience-data-replay-landscape-2026-08.md
│   ├── DU-26-training-lifecycle-landscape-2026-08.md
│   └── DU-27-checkpoint-reproducibility-compute-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
└── verification/          # появится позже
```

---

# Literature research pass

Текущие pass `DU-10 … DU-27` находятся в [`literature/`](literature/).

Последние:

- [`literature/DU-25-experience-data-replay-landscape-2026-08.md`](literature/DU-25-experience-data-replay-landscape-2026-08.md) — episode-step datasets, replay infrastructure, hindsight relabeling, provenance и source/projection separation;
- [`literature/DU-26-training-lifecycle-landscape-2026-08.md`](literature/DU-26-training-lifecycle-landscape-2026-08.md) — optimizer/training state ownership, PEFT, actor/learner policy lag, continual forgetting и candidate-revision activation;
- [`literature/DU-27-checkpoint-reproducibility-compute-landscape-2026-08.md`](literature/DU-27-checkpoint-reproducibility-compute-landscape-2026-08.md) — reproducibility constraints, training-resume state, RNG, distributed/sharded checkpointing, artifact manifests и compute provenance.

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

После `DU-27` любой сильный reproducibility claim обязан явно указывать:

```text
checkpoint / base condition
restore profile
software manifest
hardware/topology manifest
determinism policy
RNG state/initialization semantics
compute manifest
comparison/statistical criterion
```

Обязательные checkpoint/reproducibility проверки:

- weights-only vs training-resume distinction;
- seed-only vs current RNG-state restore;
- same-stack deterministic continuation where claimed;
- cross-device portable restore отдельно от bitwise claim;
- Agent/Environment causal-cut alignment;
- `execution_unknown` duplicate-effect safety;
- candidate revision остаётся candidate после restore;
- artifact corruption/integrity detection;
- missing delta-base failure;
- migration lineage;
- actual vs estimated/provider-reported compute provenance.

Training/evaluation improvement не считается чистым результатом algorithm/module, если condition получила больший фактический compute, другой restore state, другую software/hardware topology или менее строгий determinism/data condition без отдельной attribution.

---

# Результаты

Любой result должен быть связан с конкретными commit/config/checkpoint/restore profile/seed+RNG policy/environment version/raw artifacts/dataset manifest/training plan/agent revision/software/hardware/compute manifests/metrics/limitations.

Отрицательные результаты сохраняются наравне с положительными.

---

# Текущий статус

Experiment/hypothesis registry ещё не создан. Сейчас журнал используется в основном для датированных literature pass и не должен смешиваться с canonical design.
