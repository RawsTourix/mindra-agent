# ADR-0014 — Многопровайдерный Intrinsic Signal Layer без обязательной scalarization

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-14 — Intrinsic Signals`

---

# 1. Контекст

После `DU-12` и `DU-13` MINDRA уже может получать evidence о prediction error/uncertainty внешнего мира и о собственной competence/calibration.

Следующий слой должен уметь вычислять внутренние свойства опыта: novelty, rarity, information gain, competence change и другие сигналы.

При этом будущие Drives и Valuation ещё не спроектированы.

---

# 2. Проблема

Нужно выбрать архитектурную форму Intrinsic Signals.

Рассматривались варианты:

1. один scalar `intrinsic_reward`;
2. один монолитный `IntrinsicMotivationModule` с несколькими внутренними heuristics;
3. несколько независимых providers с typed outputs и без обязательного объединения;
4. встроить intrinsic bonus непосредственно в Policy/Training Runtime.

---

# 3. Требования

Решение должно:

- не смешивать signal с reward/drive/value;
- сохранять различие signal semantics;
- позволять несколько estimators одной signal family;
- поддерживать ablation/control;
- сохранять source/provenance/revisions;
- поддерживать stateful baselines/history;
- учитывать representation drift;
- не требовать evaluator ground truth;
- позволять future normalization/scalarization без redesign providers;
- быть совместимым с `NoSignal` configuration;
- не создавать скрытый Service Locator/ambient dependency.

---

# 4. Вариант A — Один scalar intrinsic_reward

## Плюсы

- простой interface с классическим RL;
- легко суммировать с extrinsic reward;
- минимальный downstream contract.

## Минусы

- теряется причина сигнала;
- трудно различить novelty, surprise и learning progress;
- scale/normalization решения преждевременно становятся архитектурными;
- Drive/Valuation фактически проектируются заранее;
- causal intervention становится слабее;
- debugging representation drift/стохастического шума затрудняется.

**Решение:** отклонён как canonical architecture.

---

# 5. Вариант B — Один монолитный IntrinsicMotivationModule

## Плюсы

- одна точка интеграции;
- удобно держать общие normalization/history mechanisms.

## Минусы

- скрытые зависимости между estimators;
- сложнее independently disable/replace provider;
- module быстро превращается в смесь novelty, reward shaping и curriculum logic;
- ухудшается исследовательская атрибуция вклада.

**Решение:** отклонён как обязательная форма.

---

# 6. Вариант C — Independent typed providers

Семантика:

```text
explicit causal sources
      ↓
Signal Provider A ──→ typed signal A
Signal Provider B ──→ typed signal B
Signal Provider C ──→ typed signal C
      ↓
IntrinsicSignalBundle / shared signal surface
```

Provider может иметь собственный private estimator/history state.

Bundle не scalarize сигналы и не определяет desirability.

**Решение:** принято.

---

# 7. Вариант D — Встроить bonus в Policy/Training

## Плюсы

- минимум архитектурных объектов;
- соответствует некоторым простым RL implementations.

## Минусы

- intrinsic signal невозможно анализировать отдельно от learning/decision mechanism;
- невозможно использовать один signal в разных Drives/Valuation policies;
- training-specific решение становится cognitive architecture;
- ухудшается `NoSignal`/control evaluation.

**Решение:** отклонён.

---

# 8. Evidence

Решение поддерживается разнообразием существующих intrinsic-motivation estimators:

- ICM использует prediction error в learned controllable feature space;
- RND использует prediction error фиксированной random-target representation как novelty-like signal;
- VIME использует information gain о dynamics belief;
- pseudo-count методы используют visitation/density rarity;
- NGU комбинирует episodic novelty с learned representations;
- CURIOUS использует learning progress по goal competence;
- Plan2Explore использует disagreement/expected novelty world-model ensemble;
- RIDE использует impact/change в learned representation.

Эти методы измеряют разные свойства и не дают основания считать их одним универсальным signal.

Датированный срез сохранён в `docs/research/literature/DU-14-intrinsic-signals-landscape-2026-08.md`.

---

# 9. Принятое решение

MINDRA использует **многопровайдерный typed Intrinsic Signal Layer**.

Канонически:

1. Intrinsic Signal не является reward/value/drive;
2. providers независимо объявляют sources/state/signal kinds;
3. signal record сохраняет provider/source/revision/reference scope;
4. общего mandatory scalar нет;
5. normalization provider-specific и versioned;
6. prediction discrepancy, surprisal, novelty, rarity, information gain, uncertainty change и competence change не смешиваются по названию;
7. stateful providers входят в Agent snapshot;
8. replay/imagined/intervened signal provenance различается;
9. evaluator-only data разрешены только explicit research controls/supervision;
10. concrete estimator выбирается позже.

---

# 10. Последствия

## Положительные

- сильная модульность и причинная диагностируемость;
- можно независимо сравнивать RND-like, count-like, information-gain и competence-progress providers;
- future Drives/Valuation получают богатый typed input;
- scale/normalization проблемы не маскируются scalar sum;
- representation drift можно диагностировать per provider;
- проще строить shuffled/constant/noise controls.

## Отрицательные

- downstream integration сложнее одного reward scalar;
- понадобится явная политика normalization/scalarization позднее;
- provider-specific snapshot/state увеличивают contract complexity;
- некоторые classic RL libraries ожидают scalar reward и потребуют adapter на training boundary.

---

# 11. Что решение намеренно не определяет

Не определены:

- какие providers войдут в первую software version;
- RND/ICM/VIME/RIDE/NGU/Plan2Explore implementation;
- exact formulas;
- common normalization;
- intrinsic reward composition;
- Drives;
- Valuation;
- learning losses;
- provider framework/API.

---

# 12. Обновляемые документы

Решение отражается в:

- `docs/design/modules/intrinsic-signals.md`;
- `docs/design/contracts/intrinsic-signals.md`;
- `docs/design/decisions/README.md`;
- `docs/design/README.md`;
- `docs/design/current.md`;
- `docs/research/README.md`;
- `AGENTS.md`.
