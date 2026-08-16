# AGENTS.md — правила работы с MINDRA

## Назначение

Этот файл содержит обязательные правила для Codex, ChatGPT и других coding agents, работающих с репозиторием MINDRA.

Краткий task prompt не заменяет repository design context. Перед изменением кода или канонической документации agent обязан восстановить актуальный контекст проекта из `docs/`.

---

# 1. Язык

Обязательное правило проекта:

- документация пишется на русском языке;
- комментарии в исходном коде пишутся на русском языке;
- пользовательские и исследовательские пояснения в репозитории пишутся на русском языке;
- технические идентификаторы остаются на английском: имена переменных, классов, функций, методов, протоколов, типов, модулей, package names, API names и другие machine-facing identifiers;
- общепринятый технический термин допустимо оставить на английском, если перевод ухудшает точность или создаёт двусмысленность.

Не переводить технические идентификаторы ради формального соблюдения русскоязычности.

---

# 2. Перед любой работой

Перед изменением production/research-кода или canonical design:

1. проверить фактический HEAD/status/diff;
2. прочитать `docs/README.md`;
3. прочитать `docs/design/current.md`;
4. определить, является ли задача documentation, design, implementation или research change;
5. прочитать релевантный canonical design;
6. прочитать все релевантные accepted/non-superseded ADR;
7. прочитать релевантные exact internal contracts, если они уже существуют;
8. проверить границы текущего разрешённого scope;
9. только после этого изменять код или документацию.

Если нужное архитектурное решение ещё не принято, agent не должен молча выбирать удобный вариант и превращать его в фактический стандарт.

---

# 3. Главный принцип

> Реализовывать принятую архитектуру и проверяемую исследовательскую гипотезу, а не переизобретать MINDRA из одного task prompt.

Нельзя без explicit design change:

- менять границы модулей;
- создавать скрытые зависимости между модулями;
- связывать архитектуру с конкретной LLM, если контракт требует заменяемый Cortex backend;
- добавлять функциональность будущих этапов «заодно»;
- заменять исследовательский механизм более простым shortcut только потому, что он быстрее реализуется;
- скрывать unresolved design question внутри implementation detail;
- менять экспериментальную методологию после просмотра результата без фиксации причины.

---

# 4. Три разных слоя истины

Всегда разделять:

```text
Design
≠
Implementation
≠
Research evidence
```

- **Design** — что решено построить и какие инварианты приняты.
- **Implementation** — что фактически реализовано в конкретном commit.
- **Research evidence** — что показали измерения и эксперименты.

Нельзя выдавать design intention за работающий механизм.

Нельзя выдавать наличие реализации за подтверждение исследовательской гипотезы.

Нельзя по одному поведенческому результату делать вывод о наличии сознания, субъективного опыта, эмоций или иных феноменальных состояний.

---

# 5. Документация как source of truth

Канонические знания проекта должны жить в `docs/`, а не только в чатах, issue или prompt history.

Если принято новое существенное решение:

1. оформить или обновить ADR, если существовало несколько реалистичных вариантов;
2. обновить канонический документ-владелец темы;
3. обновить exact contracts, если решение меняет интерфейс;
4. обновить current/status и будущий implementation plan, если они затронуты;
5. только после consistency patch реализовывать изменение.

Не оставлять два одновременно действующих противоречащих описания.

---

# 6. Research discipline

Исследовательские изменения должны следовать `docs/research-methodology.md`.

Обязательные принципы:

- заранее формулировать проверяемую гипотезу;
- иметь baseline/control, когда это применимо;
- использовать ablation и causal intervention для утверждений о вкладе модулей;
- фиксировать seed/config/environment/checkpoint;
- отделять exploratory run от подтверждающего эксперимента;
- не подбирать критерий успеха после просмотра результата без явной пометки post-hoc;
- сохранять отрицательные результаты, если они информативны.

---

# 7. Модульность

Модуль должен быть заменяемым и диагностируемым настолько, насколько это определено design.

В частности, будущая архитектура должна позволять:

- включать и отключать модуль через явную composition/configuration boundary;
- использовать baseline/no-op/dummy/control реализации, когда это нужно для оценки;
- заменять Cortex backend без переписывания независимых подсистем;
- проводить ablation без специальных одноразовых веток кода;
- сохранять наблюдаемость входов, выходов и relevant internal state для экспериментов.

Точные module contracts определяются соответствующими Design Updates и не должны угадываться заранее.

---

# 8. Dependency и composition discipline

Обязательны [`docs/design/dependency-rules.md`](docs/design/dependency-rules.md) и `ADR-0002`.

До их явного изменения запрещается:

- cognitive module → concrete peer dependency;
- Agent/core → Training Runtime или Evaluation Runtime dependency;
- независимый consumer → concrete Cortex/provider SDK dependency;
- runtime Service Locator вида `registry.get(...)`/`container.resolve(...)` внутри cognitive/runtime code;
- shared mutable globals как средство межмодульной коммуникации;
- direct mutation чужого module-private state;
- scattered `disable_x`/`ablation_x` branches по независимым потребителям вместо composition substitution;
- hidden behavior-changing fallback;
- dynamic plugin discovery внутри cognitive step.

Принятый принцип:

```text
configuration
    ↓
Composition Root
    ↓
concrete factories/providers
    ↓
explicit assembly / dependency passing
    ↓
Agent + external runtimes
```

Registry допустим как composition-time каталог factories/providers, но не как runtime Service Locator.

Если будущая реализация требует исключения из этих правил, сначала нужен design review и, при значимом выборе, новый/изменяющий ADR.

---

# 9. System boundary discipline

Обязателен [`docs/design/system-context.md`](docs/design/system-context.md).

Помнить:

```text
logical architecture boundary
≠
process / device / machine boundary
```

и:

```text
Agent Memory
≠
Artifact Storage
```

Нельзя считать компонент когнитивным только потому, что он находится в том же процессе или на том же GPU.

Нельзя превращать evaluator/trainer/experiment metadata в normal agent input без явной experimental semantics.

---

# 10. Temporal discipline

Обязательны [`docs/design/execution-model.md`](docs/design/execution-model.md) и `ADR-0003`.

Помнить:

```text
logical causal time
≠
wall-clock
```

```text
Agent Session
≠
Environment Episode
```

```text
Cognitive Cycle
≠
Environment Transition
```

```text
runtime state update
≠
Learning Update
```

До явного изменения canonical design запрещается:

- использовать elapsed wall-clock как неявный cognitive clock;
- считать внутренний reasoning/retrieval cycle новым Environment step;
- ретроактивно менять уже committed action или outcome;
- смешивать observed, replayed, imagined и counterfactual transitions без provenance;
- считать `Environment.reset()` полным reset Agent;
- использовать порядок завершения async workers/batch как causal order независимых trajectories;
- скрывать изменение trainable parameters внутри якобы frozen/normal execution;
- считать partial physical computation committed event без logical commit boundary.

Async execution допустим только при сохранении однозначного causal order и достаточного provenance Agent revision/trajectory.

---

# 11. CognitiveState discipline

Обязательны [`docs/design/cognitive-state.md`](docs/design/cognitive-state.md) и `ADR-0004`.

Помнить:

```text
CognitiveState
≠
full Agent-owned state
```

```text
committed snapshot
≠
mutable shared bus
```

```text
semantic lifetime
≠
historical retention
≠
checkpoint inclusion
```

До явного изменения canonical design запрещается:

- напрямую мутировать уже committed `CognitiveState`;
- изменять canonical tensor/value inplace через retained reference;
- использовать общий mutable dict/singleton как неформальный state bus;
- писать в namespace/field, которым компонент семантически не владеет;
- разрешать conflict через скрытый `last-write-wins`;
- применять proposed update из stale base revision как будто base не изменилась;
- начинать зависеть от произвольного state field только потому, что оно присутствует в container;
- кодировать `unknown`/`unavailable` универсальными magic sentinel вроде `0`, `-1`, `NaN` или `None` без contract;
- смешивать observed, predicted, retrieved и intervened значения без достаточного provenance;
- протаскивать model-specific hidden state, provider clients или live infrastructure objects в canonical shared state;
- считать clone одного `CognitiveState` полным Agent clone, если существует другое causally relevant private state.

Каждый future canonical field должен иметь declared semantic owner, scope/lifetime, availability/freshness semantics и provenance requirements.

Concrete container (`TensorDict`, dataclass и т. п.) пока не выбран и не должен фиксироваться implementation раньше соответствующего version design.

---

# 12. Scope текущего этапа

Фактический текущий scope всегда определяется `docs/design/current.md`.

Не полагаться на старые prompt/chat сообщения или на этот файл для определения номера текущего `DU`.

Пока не появились version roadmap и implementation sequence, наличие подробного design само по себе **не разрешает начинать реализацию**.

До соответствующих Design Updates не превращать обсуждавшиеся кандидаты в обязательные implementation choices, включая:

- конкретный Cortex backend;
- размер canonical latent/state representations;
- state bus framework;
- RL/world-model/curiosity algorithms;
- memory backend;
- training framework;
- Colab/cloud runtime;
- DI/config/plugin framework;
- scheduler/async framework;
- окончательную структуру `src/`.

---

# 13. Поведение при неопределённости

Если документация не определяет важное решение:

- не скрывать неопределённость;
- не создавать implicit contract;
- зафиксировать вопрос как design blocker/open question;
- при необходимости предложить варианты и trade-offs;
- дождаться design decision до реализации зависимой части.

Мелкие локальные implementation details, не влияющие на public/internal contracts, исследовательскую валидность, dependency/temporal/state boundaries или будущую расширяемость, могут выбираться реализацией самостоятельно при сохранении принятых принципов.
