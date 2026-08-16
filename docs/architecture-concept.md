# Архитектурная концепция MINDRA

## Статус документа

Этот документ фиксирует макроархитектуру и основные границы ответственности MINDRA.

Он намеренно не задаёт точные Python-интерфейсы, размеры тензоров, библиотеки, модели, loss-функции или version scope. Эти решения относятся к будущему canonical design и ADR.

Если concept-level описание расходится с более поздним accepted Design/ADR/contract, приоритет имеет более конкретная каноническая документация.

---

# 1. Главный принцип структуры

MINDRA строится как модульная когнитивная система, а не как монолитный wrapper вокруг одной LLM.

Архитектура должна отражать:

- границы ответственности;
- владение state;
- направления потоков данных;
- точки обучения;
- точки наблюдаемости;
- возможность замены и отключения компонентов.

Список используемых библиотек не является архитектурой.

---

# 2. Макроархитектура

Conceptually:

```text
Environment
    ↓
Observation / Perception
    ↓
Canonical CognitiveState / state exchange boundary
    ├── Cortex
    ├── World Model
    ├── Self Model
    ├── Drives
    ├── Appraisal
    ├── Salience
    ├── Memory
    ├── Workspace / integration mechanism
    └── Policy / Planner
              ↓
            Action
              ↓
          Environment
```

Это не фиксирует окончательный runtime schedule и не означает, что каждый блок обязательно будет отдельной нейросетью.

Некоторые компоненты могут быть:

- neural;
- algorithmic;
- rule-based;
- storage-backed;
- hybrid.

---

# 3. Центральная граница обмена состоянием

Компоненты не должны образовывать неуправляемую сеть скрытых прямых зависимостей.

Канонической shared-state границей является `CognitiveState`, детальная семантика которого определена в `docs/design/cognitive-state.md`.

На concept-уровне важно:

- `CognitiveState` содержит опубликованное межмодульное runtime state, а не всё `Agent-owned state`;
- committed state revision не должна изменяться задним числом;
- будущие модули читают и публикуют данные через явные semantic contracts;
- model/backend-specific private state не должен без необходимости протекать через общую границу.

Точное container/API representation пока не выбрано.

Важно сохранить invariant:

> Независимый модуль не должен знать внутреннюю реализацию другого модуля, если взаимодействие может быть выражено через стабильный контракт состояния.

---

# 4. Cortex boundary

Cortex предоставляет богатые pretrained capabilities, например язык, semantic representations и часть сложного reasoning.

При этом:

- Cortex backend заменяем;
- конкретная модель не должна протекать во всю архитектуру через model-specific hidden shapes и приватные API;
- MINDRA должна иметь собственную canonical integration boundary;
- возможность `DummyCortex`/`NoCortex` рассматривается как важный диагностический инструмент;
- обучение Cortex и обучение остальных модулей не обязаны происходить одинаково или одновременно.

Конкретный adapter contract будет спроектирован отдельно.

---

# 5. World Model

World Model conceptually отвечает за прогнозирование динамики среды и/или последствий возможных действий.

Его назначение:

- предсказывать следующее состояние или релевантные его свойства;
- предоставлять prediction error/uncertainty там, где это обосновано;
- поддерживать planning/model-based evaluation, если такой механизм будет принят.

Не фиксируется, будет ли это RSSM, recurrent model, Transformer, MLP или другой подход.

---

# 6. Self Model

Self Model conceptually представляет информацию о собственных возможностях и динамике агента.

К потенциальным задачам относятся:

- оценка вероятности успеха;
- оценка собственной uncertainty;
- прогноз resource/cost;
- tracking competence;
- моделирование собственных ограничений.

Он не является текстовым описанием «кто я» и не должен считаться доказательством самосознания.

---

# 7. Drives

Drives представляют внутренние переменные, которые могут менять относительную ценность возможных состояний и действий.

Ключевая идея:

```text
одинаковое внешнее observation
+
разный internal drive state
→
потенциально разная оценка и policy
```

Конкретный набор drives, их динамика и способ обучения пока не определены.

---

# 8. Appraisal

Appraisal conceptually преобразует событие и контекст в внутреннюю оценку его значения для текущего агента.

Он должен рассматриваться как функциональный вычислительный механизм, а не как декларация наличия эмоции.

Appraisal может зависеть от:

- внешнего состояния;
- целей;
- drives;
- world/self predictions;
- memory;
- uncertainty;
- результатов действия.

Точный output space определяется позднее.

---

# 9. Salience

Salience conceptually отвечает за относительную значимость информации для внимания, памяти или последующего обучения.

Основной исследовательский смысл — проверить, может ли learned/structured salience улучшать выбор того, что стоит:

- сохранить;
- replay/consolidate;
- предоставить workspace;
- использовать при будущих решениях.

Salience не должна считаться полезной только потому, что её значения выглядят интуитивно правдоподобно.

---

# 10. Memory

Memory рассматривается как отдельная подсистема, а не просто дополнительный текст в prompt.

Conceptually могут существовать разные временные масштабы:

```text
working state
→ episodic memory
→ replay / consolidation
→ long-term learned representations
```

Фактические типы памяти и storage backend будут выбраны позднее.

Полный Memory store не обязан входить в `CognitiveState`; shared state должен публиковать только contract-defined результаты/representations, необходимые другим подсистемам.

---

# 11. Workspace / integration

MINDRA исследует ограниченный механизм интеграции информации между специализированными подсистемами.

Он может выполнять функции:

- конкуренции relevant representations;
- временного общего контекста;
- маршрутизации информации к planning/policy/Cortex;
- ограниченной глобальной доступности выбранного состояния.

Это рабочая функциональная аналогия и не является утверждением о реализации сознания.

---

# 12. Policy / Planner

Policy/Planner отвечает за выбор действия на основе доступного внутреннего и внешнего состояния.

Важно, чтобы архитектура позволяла измерить вклад отдельных сигналов в этот выбор.

Конкретная граница между policy, planner и Cortex reasoning будет отдельным design-вопросом.

---

# 13. Обучение и временные масштабы

Архитектура должна допускать разделение:

```text
runtime state updates
online learning
experience replay
consolidation
periodic module training
optional Cortex adaptation
```

Не предполагается, что вся система обязана обучаться end-to-end на каждом шаге.

Точный training lifecycle является отдельным canonical design topic.

---

# 14. Наблюдаемость и вмешательство

Исследовательская архитектура должна быть наблюдаемой.

Для relevant модулей должны быть доступны механизмы, позволяющие:

- сохранять входы/выходы;
- фиксировать internal state;
- повторять эпизод;
- отключать компонент;
- подменять его baseline/dummy реализацией;
- выполнять controlled intervention;
- сравнивать trajectories.

Если модуль нельзя независимо исследовать, его вклад трудно отличить от общей capacity системы.

---

# 15. Заменяемость

Модульность считается архитектурным свойством только если замена компонента не требует ручного переписывания всех его потребителей.

Поэтому будущие contracts должны явно определять:

- inputs;
- outputs;
- lifecycle;
- persistence;
- training/update semantics;
- error/degradation behavior;
- observability hooks.

Точная форма будет спроектирована в `docs/design/`.

---

# 16. Текущие открытые области

На concept-уровне намеренно не определены:

- concrete `CognitiveState` container/framework;
- exact shared-state API;
- latent dimensions;
- scheduling graph;
- concrete module protocols;
- конкретный Cortex;
- конкретные RL/model-based algorithms;
- memory backend;
- training stack;
- compute environment;
- version roadmap.

Эти вопросы должны решаться последовательно после отдельного анализа вариантов.
