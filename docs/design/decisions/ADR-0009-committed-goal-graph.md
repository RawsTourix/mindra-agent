# ADR-0009 — Committed Goal Graph с явной proposal/adoption boundary

## Статус

`accepted`

## Контекст

После `DU-07` Environment может предъявлять `External Task Specification`, а после `DU-08` Perception уже отделяет sensory input от task semantics.

До проектирования Cortex, Memory, Drives, Valuation и Policy необходимо определить, где в MINDRA существует сама цель и кто владеет её lifecycle.

Если этого не сделать, каждый downstream компонент может начать использовать собственное понятие goal:

- Cortex — текст instruction;
- Policy — goal embedding;
- RL algorithm — reward function;
- Planner — текущий subgoal;
- Drives — желаемое состояние;
- Environment — task object.

Это разрушит модульность и причинную наблюдаемость.

---

## Проблема

Нужно выбрать canonical модель целей, которая:

- допускает внешние и внутренние цели;
- поддерживает несколько simultaneous goals;
- поддерживает subgoals/dependencies;
- не сводит цель к reward/value;
- сохраняет lifecycle и persistence;
- позволяет Cortex/Planner/Drives предлагать цели без direct ownership;
- позволяет causal intervention/ablation;
- не требует конкретной LLM или RL algorithm.

---

## Рассмотренные варианты

### Вариант A — Goal как alias внешней Task Specification / reward

```text
Environment Task/Reward
=
Goal
```

Плюсы:

- минимальная архитектура;
- удобно для классического single-task RL;
- не нужен отдельный Goal System.

Минусы:

- internal goals практически невозможны;
- Goal смешивается с training signal;
- session-level persistence зависит от Environment;
- subgoals приходится прятать в Planner/Policy;
- autonomous motivation нельзя отделить от внешней задачи;
- evaluator/task provider фактически владеет внутренними целями Agent.

**Отклонено.**

---

### Вариант B — единственный `current_goal` / LIFO Goal Stack

```text
current_goal
или
Goal Stack
```

Плюсы:

- просто реализовать;
- естественно для рекурсивного planning;
- легко понимать active focus.

Минусы:

- плохо поддерживает несколько одновременно действующих целей;
- один subgoal может поддерживать несколько parent goals;
- conflict/dependency semantics быстро становятся ad-hoc;
- переключение focus может случайно уничтожать long-term commitment;
- stack order начинает смешивать structural dependency и motivational priority.

**Отклонено как универсальная модель.** Stack может быть локальной planner structure, но не canonical Goal state.

---

### Вариант C — Goal state полностью внутри Cortex/Policy hidden representation

Плюсы:

- минимальный explicit state;
- pretrained LLM может уже понимать инструкции и планы;
- не нужен отдельный goal schema.

Минусы:

- goal невозможно надёжно наблюдать/аблировать/подменять;
- Cortex становится обязательным;
- swap backend меняет goal semantics;
- provenance/lifecycle неустойчивы;
- prompt/instruction легко путается с внутренним commitment;
- невозможно отделить architecture gain Goal System от capability backbone.

**Отклонено.**

---

### Вариант D — Goal Proposals + Goal System + Committed Goal Graph

```text
Goal sources
   ↓
Goal Proposals
   ↓
Goal System
   ↓
Committed Goal Graph
```

Плюсы:

- один semantic owner Goal state;
- источники целей остаются заменяемыми;
- Cortex/Drives/Planner могут предлагать goals без direct mutation;
- несколько goals естественны;
- parent/subgoal/dependency relations выразимы;
- lifecycle/persistence/provenance доступны явно;
- research intervention и ablation естественны;
- Goal отделяется от reward/value/policy.

Минусы:

- требуется отдельный lifecycle и graph validation;
- contract сложнее одного goal embedding;
- dynamic arbitration всё равно потребует будущих Valuation/Executive mechanisms;
- decomposition semantics нужно проектировать аккуратно.

**Принято.**

---

## Принятое решение

MINDRA использует:

1. `Goal Proposal` как непринятый кандидат;
2. `Goal System` как единственный semantic owner committed Goal state;
3. `Committed Goal` как стабильный goal instance;
4. `Goal Graph` как canonical множество goals и relations.

Канонически:

```text
External Task / Cortex / Drives / Planner / Control
                 ↓
             Goal Proposal
                 ↓
             Goal System
                 ↓
          Committed Goal Graph
```

### Goal Graph

Поддерживает:

- несколько committed/active goals;
- parent/subgoal relations;
- dependency relations;
- conflict metadata;
- lifecycle/scope/provenance каждого goal instance.

Dependency relation должна оставаться ацикличной в пределах committed graph semantics.

### Goal lifecycle

Должны быть различимы как минимум:

```text
pending
active
suspended
achieved
failed
abandoned
expired
invalidated
```

Точные enum identifiers могут уточняться exact contract, но семантические различия сохраняются.

### Goal sources

Источник goal proposal не становится owner Goal state.

Cortex, Planner, Drives и Research Runtime не мутируют committed Goal Graph напрямую.

### Priority / Value

Structural/declarative priority остаётся Goal metadata.

Dynamic desirability/value будет проектироваться отдельно в `DU-18`.

### Commitment

Commitment является persistence/lifecycle semantics и не сводится к scalar reward/value.

---

## Последствия

### Положительные

- Goal становится независимой архитектурной сущностью;
- external и autonomous goals проходят одну boundary;
- можно сравнивать same Goal System с разными Cortex backends;
- несколько simultaneous objectives не требуют hidden stack tricks;
- long-term goal можно сохранять при временном focus switch;
- causal interventions получают чистый target;
- planner decomposition не захватывает ownership целей;
- будущие Drives/Valuation подключаются без переписывания Goal semantics.

### Отрицательные

- требуется graph/lifecycle validation;
- нужно различать goal existence, focus, priority, commitment и value;
- exact goal objective DSL остаётся отдельной сложной задачей;
- некоторые простые RL baselines потребуют adapter/minimal Goal System.

---

## Что решение намеренно не определяет

ADR не фиксирует:

- Python classes/Protocol;
- exact Goal DSL;
- конкретный graph library;
- numerical priority/commitment representation;
- natural-language grounding method;
- internal goal-generation algorithm;
- conflict arbitration algorithm;
- Planner implementation;
- reward/utility function;
- training method.

---

## Затронутые документы

- `docs/design/modules/goals.md`;
- `docs/design/contracts/goals.md`;
- `docs/design/decisions/README.md`;
- `docs/design/README.md`;
- `docs/design/current.md`;
- `docs/design/glossary.md`;
- `AGENTS.md`.
