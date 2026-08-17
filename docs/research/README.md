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
│   └── DU-11-memory-landscape-2026-08.md
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

Для быстро меняющихся технологий допускаются отдельные датированные документы в `literature/`.

Они должны явно указывать:

- дату среза;
- назначение;
- первичные/официальные источники;
- какие выводы относятся только к текущему technology landscape;
- какие canonical design conclusions поддержаны evidence;
- что нужно перепроверить перед implementation/version selection.

Текущие research pass:

- [`literature/DU-10-cortex-landscape-2026-08.md`](literature/DU-10-cortex-landscape-2026-08.md) — small/open-weight Cortex candidates и tooling evidence для `DU-10`;
- [`literature/DU-11-memory-landscape-2026-08.md`](literature/DU-11-memory-landscape-2026-08.md) — external/neural/hybrid Memory approaches, representation drift и retrieval-index evidence для `DU-11`.

Эти документы **не выбирают** canonical model/backend/database/index.

---

# Будущая гипотеза

Каждая существенная гипотеза должна иметь стабильный идентификатор, однозначную формулировку и статус.

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

Точная форма будет определена отдельным контрактом.

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

Experiment/hypothesis registry ещё не создан. На текущем design этапе журнал уже используется для датированных research/literature pass, которые не должны смешиваться с canonical design.
