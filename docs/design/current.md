# Текущее состояние проектирования MINDRA

## Назначение

Краткий factual status проекта.

Этот файл не переопределяет canonical design. Он показывает, что фактически уже спроектировано и какой следующий шаг допустим.

---

# 1. Общий статус

**Documentation foundation создана. Детальный архитектурный design и implementation ещё не начаты.**

На текущем этапе зафиксированы:

- project concept;
- architecture concept;
- research methodology;
- базовые design principles;
- glossary;
- documentation plan;
- правила для coding agents;
- пустые registry boundaries для ADR, exact contracts и versions.

---

# 2. Что ещё не принято

Пока отсутствуют accepted решения по:

- system context;
- dependency rules;
- canonical `CognitiveState`;
- module lifecycle/scheduling;
- Cortex contract/backend;
- Environment/MicroWorld;
- World Model;
- Self Model;
- Drives;
- Appraisal;
- Salience;
- Memory/consolidation;
- Workspace;
- Policy/Planner;
- training lifecycle;
- data/replay schema;
- checkpointing;
- exact evaluation harness;
- testing strategy;
- version roadmap;
- implementation sequence.

---

# 3. Implementation status

```text
Production/research implementation: not started
Version roadmap: not designed
Current version: none
Accepted implementation HEAD: none
```

Наличие документации не является разрешением Codex начать писать архитектуру по собственному усмотрению.

---

# 4. Следующий допустимый design step

Согласно `documentation-plan.md`:

```text
system context
→ dependency rules
→ canonical cognitive state
→ module lifecycle
```

Каждый из этих этапов должен проектироваться отдельно с анализом существующих подходов и trade-offs.

---

# 5. Запрещённый premature scope

До соответствующего design decision не фиксировать как обязательные:

- Qwen/Gemma/Llama или другую конкретную Cortex model;
- TensorDict или другой state framework;
- PPO/GRPO/Dreamer или другой learning algorithm;
- RND/ICM или конкретный curiosity mechanism;
- FAISS/vector DB или конкретный memory backend;
- PEFT/LoRA/QLoRA как обязательный tuning mechanism;
- Google Colab как единственный runtime;
- конкретные latent dimensions;
- окончательную структуру `src/`.

Эти варианты могут быть кандидатами для будущего research/design comparison.
