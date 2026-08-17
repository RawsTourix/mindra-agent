# Исследовательский журнал MINDRA

## Назначение

Этот каталог предназначен для фиксации проверяемых гипотез, протоколов экспериментов, результатов, внешней верификации и датированных research/literature pass, используемых при проектировании MINDRA.

Каноническая архитектура живёт в `docs/design/`. Материалы этого каталога являются evidence/context и сами по себе не меняют design.

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
│   └── DU-18-valuation-landscape-2026-08.md
├── hypotheses.md          # появится позже
├── experiments/           # появится позже
├── results/               # появится позже
└── verification/          # появится позже
```

Точная структура будущих hypothesis/experiment/result records будет определена соответствующими Design Updates.

---

# Разделение ответственности

```text
docs/design/
→ что решено построить и как это должно работать

docs/research/
→ какие внешние данные/подходы изучались и что фактически проверялось
```

Research evidence не переписывает canonical architecture автоматически.

Правильная последовательность:

```text
research evidence / experiment result
→ interpretation
→ design review
→ ADR при существенном выборе
→ canonical design update
→ implementation/version update
```

---

# Literature research pass

Для быстро меняющихся технологий и исследовательских областей допускаются отдельные датированные документы в `literature/`.

Текущие research pass:

- [`literature/DU-10-cortex-landscape-2026-08.md`](literature/DU-10-cortex-landscape-2026-08.md) — Cortex candidates/tooling;
- [`literature/DU-11-memory-landscape-2026-08.md`](literature/DU-11-memory-landscape-2026-08.md) — Memory/retrieval/indexes;
- [`literature/DU-12-world-model-landscape-2026-08.md`](literature/DU-12-world-model-landscape-2026-08.md) — world models/uncertainty;
- [`literature/DU-13-self-model-landscape-2026-08.md`](literature/DU-13-self-model-landscape-2026-08.md) — competence/calibration/self-modeling;
- [`literature/DU-14-intrinsic-signals-landscape-2026-08.md`](literature/DU-14-intrinsic-signals-landscape-2026-08.md) — novelty/information/learning progress;
- [`literature/DU-15-drives-landscape-2026-08.md`](literature/DU-15-drives-landscape-2026-08.md) — drive/homeostatic dynamics;
- [`literature/DU-16-appraisal-landscape-2026-08.md`](literature/DU-16-appraisal-landscape-2026-08.md) — multidimensional appraisal;
- [`literature/DU-17-affect-dynamics-landscape-2026-08.md`](literature/DU-17-affect-dynamics-landscape-2026-08.md) — persistent affect dynamics;
- [`literature/DU-18-valuation-landscape-2026-08.md`](literature/DU-18-valuation-landscape-2026-08.md) — MORL, scalarization, Pareto/lexicographic/constraints, distributional/risk-sensitive value и preference controllability.

Эти документы **не выбирают** canonical implementation model/framework/taxonomy/estimator/dynamics/scalarization/risk policy.

---

# Будущая гипотеза

Каждая существенная гипотеза должна иметь стабильный идентификатор, однозначную формулировку и статус.

Для Valuation особенно важно различать:

```text
source objective/value evidence
comparison/scalarization policy
Policy decision
behavioral result
```

Чтобы improvement не приписывался structured valuation, если его объясняет arbitrary extra scalar/network capacity.

---

# Будущий протокол эксперимента

До подтверждающего запуска желательно фиксировать:

- проверяемую гипотезу;
- независимые переменные;
- контролируемые условия;
- baseline и control configurations;
- метрики;
- критерий успеха или опровержения;
- policy для random seeds;
- версию среды/данных;
- способ анализа.

Для Affect важны matched recurrent/history controls.

Для Valuation важны weighted-scalar, shuffled/matched aggregation и preference-intervention controls.

---

# Результаты

Результат должен ссылаться на конкретные:

- commit;
- конфигурацию;
- checkpoint;
- seed;
- версию среды/данных;
- исходные артефакты;
- метрики;
- известные ограничения.

Отрицательные результаты сохраняются так же, как положительные.

---

# Текущий статус

Experiment/hypothesis registry ещё не создан. На текущем design этапе журнал используется для датированных research/literature pass, которые не должны смешиваться с canonical design.
