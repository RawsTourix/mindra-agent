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
│   └── DU-17-affect-dynamics-landscape-2026-08.md
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

Они должны явно указывать:

- дату среза;
- назначение;
- первичные/официальные источники;
- какие выводы относятся только к текущему landscape;
- какие canonical design conclusions поддержаны evidence;
- что нужно перепроверить перед implementation/version selection.

Текущие research pass:

- [`literature/DU-10-cortex-landscape-2026-08.md`](literature/DU-10-cortex-landscape-2026-08.md) — small/open-weight Cortex candidates и tooling evidence;
- [`literature/DU-11-memory-landscape-2026-08.md`](literature/DU-11-memory-landscape-2026-08.md) — external/neural/hybrid Memory, representation drift и retrieval indexes;
- [`literature/DU-12-world-model-landscape-2026-08.md`](literature/DU-12-world-model-landscape-2026-08.md) — RSSM/Dreamer, decoder-free, Transformer world models, uncertainty и tooling;
- [`literature/DU-13-self-model-landscape-2026-08.md`](literature/DU-13-self-model-landscape-2026-08.md) — confidence calibration, competence awareness и functional self-modeling;
- [`literature/DU-14-intrinsic-signals-landscape-2026-08.md`](literature/DU-14-intrinsic-signals-landscape-2026-08.md) — prediction-error, novelty, density/count, information-gain и learning-progress;
- [`literature/DU-15-drives-landscape-2026-08.md`](literature/DU-15-drives-landscape-2026-08.md) — Homeostatic RL, continuous drive dynamics и alternative motivational frameworks;
- [`literature/DU-16-appraisal-landscape-2026-08.md`](literature/DU-16-appraisal-landscape-2026-08.md) — multidimensional appraisal, EMA, appraisal+RL, LLM appraisal reasoning и trajectories;
- [`literature/DU-17-affect-dynamics-landscape-2026-08.md`](literature/DU-17-affect-dynamics-landscape-2026-08.md) — persistent affect/mood dynamics, valence-arousal/PAD candidates, appraisal-history integration и modern dynamic agent approaches.

Эти документы **не выбирают** canonical implementation model/framework/taxonomy/estimator/dynamics.

---

# Будущая гипотеза

Каждая существенная гипотеза должна иметь стабильный идентификатор, однозначную формулировку и статус.

Особенно для falsifiable boundaries вроде Affect будущий experiment registry должен уметь отличать:

```text
architectural hypothesis
implementation
control configuration
experimental evidence
interpretation
```

Конкретная схема идентификаторов и статусов будет определена позже.

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

Для Affect особенно важны matched recurrent/history controls, чтобы не спутать temporal semantics с дополнительной memory/parameter capacity.

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
