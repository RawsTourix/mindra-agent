# Исследовательская методология MINDRA

## Статус документа

Этот документ фиксирует общие правила постановки, проведения и интерпретации исследований MINDRA.

Он не задаёт конкретные benchmark, dataset, environment, statistical test или threshold для будущих версий. Эти детали должны появляться в соответствующих design/experiment documents.

---

# 1. Главный принцип

MINDRA развивается не по схеме «добавили модуль — стало сложнее — значит стало лучше», а по схеме:

```text
гипотеза
→ контролируемый design
→ реализация
→ experiment
→ evidence
→ вывод
```

Любой заявляемый вклад механизма должен быть по возможности отделён от:

- увеличения общего числа параметров;
- дополнительного compute;
- дополнительного контекста;
- случайного seed;
- особенностей конкретного Cortex;
- изменения environment/dataset;
- скрытого изменения training procedure.

---

# 2. Engineering correctness и research validity

Это независимые требования.

```text
Engineering correctness
≠
Research validity
```

Модуль может быть корректно реализован по design и не подтверждать исследовательскую гипотезу.

И наоборот, интересный единичный результат не считается достаточным, если experiment pipeline не воспроизводим или реализация нарушает контракт.

---

# 3. Гипотезы

Перед подтверждающим экспериментом гипотеза должна быть сформулирована так, чтобы существовал наблюдаемый результат, способный её опровергнуть или существенно ослабить.

Плохая формулировка:

> Appraisal делает агента более похожим на человека.

Лучше:

> При фиксированном внешнем observation контролируемое изменение appraisal state статистически значимо меняет целевую часть action distribution, при этом off-target effects остаются ограниченными.

Точные формы гипотез будут зависеть от исследуемого механизма.

---

# 4. Baseline

Для каждого существенного исследования должен существовать понятный baseline, когда это практически возможно.

Кандидаты:

- минимальный agent без исследуемого модуля;
- Cortex-only;
- no-Cortex;
- предыдущая accepted architecture;
- стандартный RL/model-based agent;
- rule-based control;
- no-op module.

Baseline должен отвечать на конкретный исследовательский вопрос, а не добавляться формально.

---

# 5. Ablation

Если утверждается, что конкретный модуль полезен, основной контроль — его удаление или замена при максимально неизменных остальных условиях.

Conceptually:

```text
Full architecture
vs
Full architecture - Module X
```

Ablation должен быть предусмотрен архитектурой заранее, а не реализовываться отдельным одноразовым fork.

---

# 6. Control implementations

Для отличия семантического эффекта от простой дополнительной capacity могут использоваться:

- `NoOp` control;
- constant output control;
- random output control;
- shuffled memory/retrieval;
- parameter-matched generic network;
- compute-matched control.

Если learned module показывает примерно тот же результат, что random или generic control, нельзя приписывать выигрыш предполагаемой семантике модуля без дополнительного evidence.

---

# 7. Causal intervention

Корреляция внутреннего state с поведением недостаточна для сильного утверждения о функциональной роли.

Где возможно, нужно проводить intervention:

```text
clone/fix external state
→ изменить одну internal variable / representation
→ оставить остальные условия неизменными
→ измерить изменение поведения
```

Нужно различать:

- target effect;
- off-target effect;
- intervention specificity.

---

# 8. Counterfactual experiments

В искусственной среде MINDRA может иметь преимущество, недоступное при исследованиях человека: состояние можно сохранять, клонировать и воспроизводить.

Желательный pattern:

```text
один checkpoint + один environment state
→ branch A
→ branch B с контролируемым изменением
→ сравнение trajectories
```

Такой подход особенно важен для drives, appraisal, memory и self-model.

---

# 9. Factorial interactions

Модули могут быть полезны не отдельно, а только во взаимодействии.

Поэтому при достаточном compute следует исследовать не только одиночные ablation, но и взаимодействия:

```text
A
B
A + B
none
```

Это позволяет отличить независимый вклад от системной синергии.

---

# 10. Multiple seeds

Серьёзный вывод не должен опираться на один удачный training seed.

Количество seeds и способ статистического анализа будут определяться experiment protocol с учётом compute budget.

Минимально необходимо сохранять:

- seed;
- config;
- code commit;
- environment/data version;
- checkpoint identity.

---

# 11. Train / validation / test separation

Если environment или dataset используется для обучения, evaluation должна включать unseen conditions.

Важно различать:

- memorization;
- adaptation;
- generalization;
- transfer.

Например, поведение «красный объект опасен» не доказывает learned risk assessment, если во всех train worlds красный цвет всегда означал опасность.

---

# 12. Cortex transfer

Поскольку Cortex является заменяемым backend, одним из ключевых классов будущих экспериментов должен быть transfer между различными Cortex configurations.

Исследовательские вопросы могут включать:

- сохраняется ли architecture gain при другой base model;
- насколько сильно остальные модули привязаны к model-specific representation;
- что происходит при уменьшении/увеличении Cortex capacity;
- остаются ли функциональные свойства без Cortex.

Конкретные модели не фиксируются этим документом.

---

# 13. Parameter/compute controls

Если новый модуль увеличивает количество trainable parameters или compute, improvement нельзя автоматически считать доказательством правильности его функциональной семантики.

Где возможно, необходимо сравнение с control, имеющим близкие:

- parameter count;
- input information;
- training budget;
- runtime compute.

---

# 14. Отдельные module metrics

End-task success недостаточен для диагностики.

Каждый модуль должен получить собственные метрики, соответствующие его responsibility.

Примеры классов метрик:

- prediction quality для World Model;
- calibration для Self Model;
- retrieval utility для Memory;
- future utility prediction для Salience;
- intervention response для Drives/Appraisal;
- information routing для Workspace.

Точные метрики будут владельцами соответствующих design documents.

---

# 15. Exploratory и confirmatory experiments

Допускаются exploratory runs для поиска гипотез, debugging и выбора разумных диапазонов параметров.

Но exploratory result не должен задним числом оформляться как заранее предсказанный confirmatory result.

Для confirmatory experiment до запуска желательно зафиксировать:

- hypothesis;
- independent variables;
- controls;
- metrics;
- primary success/falsification criterion;
- seed policy;
- environment/data split;
- analysis method.

---

# 16. Воспроизводимость

Каждый значимый experiment должен быть максимально воспроизводим из сохранённых артефактов.

Минимальный future experiment record должен позволять восстановить:

```text
repository commit
configuration
random seeds
runtime/software environment
training/evaluation data or environment version
Cortex identity/configuration
module composition
checkpoint
metrics
raw result artifacts
```

Точный contract будет определён позднее.

---

# 17. Отрицательные результаты

Отрицательный результат не является неудачей проекта.

Если качественно реализованный модуль не улучшает целевую способность или его эффект полностью объясняется control, это важный research evidence.

Не удалять такую информацию из истории исследования ради более красивой narrative.

---

# 18. Антропоморфные ограничения

MINDRA использует термины из cognitive science как функциональные рабочие понятия, но не должен автоматически переносить человеческую феноменологию на искусственную систему.

Запрещён логический переход вида:

```text
есть переменная valence
→ агент чувствует удовольствие/страдание
```

или:

```text
есть Self Model
→ агент обладает самосознанием
```

или:

```text
есть Workspace
→ доказано сознание
```

Допустимы только выводы, поддерживаемые конкретным experiment design.

---

# 19. Изменение design по результатам эксперимента

Research evidence не меняет canonical design автоматически.

Правильный flow:

```text
result
→ interpretation
→ design review
→ ADR при существенном выборе
→ canonical design update
→ next implementation
```

Это сохраняет понятную историю того, почему архитектура менялась.

---

# 20. Текущая граница

На стадии documentation foundation ещё не фиксируются:

- конкретный benchmark suite;
- composite score;
- statistical thresholds;
- minimum seeds;
- конкретные MicroWorld rules;
- training dataset;
- experiment storage format;
- plotting/reporting stack.

Они должны быть спроектированы после определения соответствующих subsystem contracts и compute constraints.
