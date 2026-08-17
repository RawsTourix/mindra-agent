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
│   └── DU-26-training-lifecycle-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
└── verification/          # появится позже
```

---

# Literature research pass

Текущие pass `DU-10 … DU-26` находятся в [`literature/`](literature/).

Последние:

- [`literature/DU-24-action-boundary-landscape-2026-08.md`](literature/DU-24-action-boundary-landscape-2026-08.md) — shielding/runtime assurance, action lifecycle/correlation, authorization placement и retry/idempotency;
- [`literature/DU-25-experience-data-replay-landscape-2026-08.md`](literature/DU-25-experience-data-replay-landscape-2026-08.md) — episode-step datasets, replay infrastructure, hindsight relabeling, provenance и source/projection separation;
- [`literature/DU-26-training-lifecycle-landscape-2026-08.md`](literature/DU-26-training-lifecycle-landscape-2026-08.md) — optimizer/training state ownership, PEFT, actor/learner policy lag, continual forgetting и candidate-revision activation.

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

Для Training Lifecycle особенно проверять:

```text
Frozen / NoLearning
vs Offline Learning
vs Interleaved Online Learning
vs Decoupled Online Learning
```

и, где применимо:

```text
independent module training
vs joint training

frozen Cortex
vs adapter-only Cortex
vs larger trainable subset
```

Обязательные training-validity проверки:

- source sample/behavior revision provenance;
- base revision pinning;
- privileged-supervision leakage;
- new-task improvement отдельно от old-capability retention;
- candidate validation до activation;
- representation drift/compatibility;
- in-flight decision revision stability;
- off-policy/policy-lag assumptions;
- optimizer state lineage;
- actual training compute/data budgets;
- rollback/rejected-update evidence.

Training improvement не считается чистым результатом algorithm, если он объясняется другим source dataset, privileged labels, большим compute/data budget или другим activation/retention policy.

---

# Результаты

Любой result должен быть связан с конкретными commit/config/checkpoint/seed/environment version/raw artifacts/dataset manifest/training plan/agent revision/metrics/limitations.

Отрицательные результаты сохраняются наравне с положительными.

---

# Текущий статус

Experiment/hypothesis registry ещё не создан. Сейчас журнал используется в основном для датированных literature pass и не должен смешиваться с canonical design.
