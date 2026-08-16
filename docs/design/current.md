# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта.

Этот файл не переопределяет канонический design. Он показывает, что фактически уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Фундамент документации создан. `DU-01 — System Context` завершён и принят. Реализация ещё не начата.**

На текущем этапе зафиксированы:

- концепция проекта;
- архитектурная концепция;
- исследовательская методология;
- базовые принципы проектирования;
- глоссарий;
- правила для агентов разработки;
- реестры ADR, точных контрактов и будущих версий;
- карта кандидатных модулей и архитектурных областей;
- канонический порядок `DU-00` … `DU-32` в `documentation-plan.md`;
- системный контекст MINDRA;
- логические границы Agent, Environment, training/evaluation infrastructure, artifact/storage/compute;
- независимость logical ownership от process/device/provider topology;
- первый accepted ADR.

---

# 2. Завершённые Design Updates

```text
DU-00 — Documentation Foundation
DU-01 — System Context
```

## DU-00

Зафиксировал общие правила, исследовательскую дисциплину и карту дальнейшей работы, но не принял детальные module semantics.

## DU-01

Канонический документ:

- [`system-context.md`](system-context.md).

Приняты основные invariants:

- `MINDRA Agent` является логической когнитивной системой, а не процессом/VM/GPU;
- `Environment` находится вне Agent boundary;
- Cortex является внутренней logical capability, хотя backend может физически выполняться удалённо;
- `Execution Runtime` хостит Agent, но не является когнитивным модулем;
- `Training Runtime` и `Evaluation Runtime` находятся вне Agent boundary;
- `Experiment Runner` и artifact pipeline относятся к external research control/infrastructure plane;
- deployment topology не определяет architecture semantics;
- logical state ownership не зависит от physical storage location;
- evaluation-derived information не является normal agent-visible input;
- Agent должен иметь корректный execution mode без trainer/evaluator.

Accepted decision:

- [`ADR-0001 — Логические границы независимы от deployment topology`](decisions/ADR-0001-logical-boundaries-independent-of-deployment.md).

---

# 3. Следующий допустимый Design Update

```text
DU-02 — Dependency & Composition Rules
```

Цель `DU-02` — превратить принятые логические границы `DU-01` в явные правила зависимостей и композиции:

- допустимые dependency directions;
- shared contracts;
- composition root;
- abstract vs concrete dependencies;
- правила Cortex backend isolation;
- взаимодействие runtime и training code;
- evaluator access;
- module-private state;
- disabled/control implementations;
- предотвращение circular hidden coupling.

После принятия `DU-02` допускается:

```text
DU-03 — Runtime / Temporal Model
```

Детальный design когнитивных модулей до завершения фундаментальной цепочки:

```text
DU-02 Dependency & Composition Rules
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

# 5. Что уже принято на system-context уровне

Канонически различаются:

```text
MINDRA Agent
Environment
Execution Runtime
Training Runtime
Evaluation Runtime
Experiment Runner
Artifact Collector
Artifact Storage
Compute Substrate
Cortex Execution Provider
Researcher / Operator
```

Принцип:

```text
logical architecture boundary
≠
process / device / machine boundary
```

Active Agent Memory и Artifact Storage также считаются разными логическими сущностями даже при физическом использовании одного storage backend.

---

# 6. Что ещё не принято

Пока отсутствуют accepted решения по:

- dependency/composition rules;
- runtime/temporal model;
- canonical `CognitiveState`;
- module lifecycle/scheduling;
- observability/intervention contract;
- Environment/MicroWorld;
- Perception representation;
- Goal System;
- exact Cortex contract/backend;
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

# 7. Статус реализации

```text
Исследовательская и программная реализация: не начата
Дорожная карта версий: не спроектирована
Текущая software version: отсутствует
Принятый implementation HEAD: отсутствует
```

Завершение `DU-01` не является разрешением Codex начать реализацию.

---

# 8. Запрещённый преждевременный scope

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
- отдельный Workspace/Affect/Executive Control только на основании когнитивной аналогии;
- конкретный process/thread/distributed graph;
- конкретный cloud/storage provider.

Эти варианты являются кандидатами для будущего targeted research/design comparison.

---

# 9. Канонические ссылки

- системный контекст: [`system-context.md`](system-context.md);
- `ADR-0001`: [`decisions/ADR-0001-logical-boundaries-independent-of-deployment.md`](decisions/ADR-0001-logical-boundaries-independent-of-deployment.md);
- порядок Design Updates: [`documentation-plan.md`](documentation-plan.md);
- карта областей: [`modules/README.md`](modules/README.md);
- общие принципы: [`principles.md`](principles.md);
- термины: [`glossary.md`](glossary.md);
- исследовательская дисциплина: [`../research-methodology.md`](../research-methodology.md).
