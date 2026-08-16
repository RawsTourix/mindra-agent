# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что фактически уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. Полная последовательность design-обновлений спроектирована. Детальный архитектурный design и реализация ещё не начаты.**

На текущем этапе зафиксированы:

- концепция проекта;
- архитектурная концепция;
- исследовательская методология;
- базовые принципы проектирования;
- глоссарий;
- правила для агентов разработки;
- реестры ADR, точных контрактов и будущих версий;
- карта кандидатных модулей и архитектурных областей;
- канонический порядок `DU-00` … `DU-32` в `documentation-plan.md`.

---

# 2. Завершённые Design Updates

```text
DU-00 — Documentation Foundation
```

`DU-00` зафиксировал общие правила и карту дальнейшей работы, но не принял детальные module semantics.

---

# 3. Следующий допустимый Design Update

```text
DU-01 — System Context
```

Цель `DU-01` — определить MINDRA как систему в окружении Environment, Cortex, training/evaluation runtime, artifact storage и локального/удалённого compute без преждевременного выбора concrete implementation.

После принятия `DU-01` допускается:

```text
DU-02 — Dependency & Composition Rules
```

Детальный design когнитивных модулей до завершения фундаментальной цепочки:

```text
DU-01 System Context
→ DU-02 Dependency & Composition Rules
→ DU-03 Runtime / Temporal Model
→ DU-04 CognitiveState Semantics
→ DU-05 Module Protocol & Scheduling
→ DU-06 Observability & Intervention
```

считается преждевременным.

---

# 4. Карта будущих модульных областей

План проектирования включает, среди прочего:

```text
Environment
Perception / Representation
Goal System
Cortex
Memory Core
World Model
Self Model
Intrinsic Signals
Drives
Appraisal
Affect Dynamics
Valuation
Salience / Attention
Memory Regulation / Consolidation
Workspace
Metacognitive / Executive Control
Policy / Planner
Action Boundary
```

Подробная карта: [`modules/README.md`](modules/README.md).

Наличие области в этой карте не означает, что отдельный module boundary уже принят. Соответствующий `DU` обязан подтвердить необходимость отдельной ответственности или аргументированно объединить/отложить её.

---

# 5. Что ещё не принято

Пока отсутствуют accepted решения по:

- system context;
- dependency rules;
- runtime/temporal model;
- canonical `CognitiveState`;
- module lifecycle/scheduling;
- observability/intervention contract;
- Environment/MicroWorld;
- Perception representation;
- Goal System;
- Cortex contract/backend;
- Memory Core;
- World Model;
- Self Model;
- intrinsic signals;
- Drives;
- Appraisal;
- Affect Dynamics;
- Valuation;
- Salience/Attention;
- Memory Regulation/Consolidation;
- Workspace;
- Metacognitive/Executive Control;
- Policy/Planner;
- Action boundary;
- trajectory/data/replay schema;
- training lifecycle;
- checkpointing/reproducibility;
- exact evaluation harness;
- testing strategy;
- research claims/limitations;
- version roadmap;
- implementation sequences.

---

# 6. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Наличие подробного design-update plan не является разрешением Codex начать писать архитектуру по собственному усмотрению.

---

# 7. Запрещённый преждевременный scope

До соответствующего Design Update не фиксировать как обязательные:

- Qwen/Gemma/Llama или другую конкретную модель Cortex;
- TensorDict или другой framework состояния;
- PPO/GRPO/Dreamer или другой learning algorithm;
- RND/ICM или конкретный curiosity mechanism;
- FAISS/vector DB или конкретный backend памяти;
- PEFT/LoRA/QLoRA как обязательный tuning mechanism;
- Google Colab как единственный runtime;
- конкретные latent dimensions;
- окончательную структуру `src/`;
- отдельный Workspace/Affect/Executive Control только на основании когнитивной аналогии.

Эти варианты являются кандидатами для будущего targeted research/design comparison.

---

# 8. Канонические ссылки

- порядок Design Updates: [`documentation-plan.md`](documentation-plan.md);
- карта областей: [`modules/README.md`](modules/README.md);
- общие принципы: [`principles.md`](principles.md);
- термины: [`glossary.md`](glossary.md);
- исследовательская дисциплина: [`../research-methodology.md`](../research-methodology.md).
