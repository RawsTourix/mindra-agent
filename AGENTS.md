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
7. прочитать релевантные candidate/exact internal contracts, если они уже существуют;
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
3. обновить candidate/exact contracts, если решение меняет интерфейс;
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

---

# 9. System boundary discipline

Обязателен [`docs/design/system-context.md`](docs/design/system-context.md).

Помнить:

```text
logical architecture boundary ≠ process / device / machine boundary
Agent Memory ≠ Artifact Storage
```

Нельзя считать компонент когнитивным только потому, что он находится в том же процессе или на том же GPU.

Нельзя превращать evaluator/trainer/experiment metadata в normal agent input без явной experimental semantics.

---

# 10. Temporal discipline

Обязательны [`docs/design/execution-model.md`](docs/design/execution-model.md) и `ADR-0003`.

Помнить:

```text
logical causal time ≠ wall-clock
Agent Session ≠ Environment Episode
Cognitive Cycle ≠ Environment Transition
runtime state update ≠ Learning Update
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
CognitiveState ≠ full Agent-owned state
committed snapshot ≠ mutable shared bus
semantic lifetime ≠ historical retention ≠ checkpoint inclusion
```

До явного изменения canonical design запрещается:

- напрямую мутировать уже committed `CognitiveState`;
- изменять canonical tensor/value inplace через retained reference;
- использовать общий mutable dict/singleton как неформальный state bus;
- писать в namespace/field, которым компонент семантически не владеет;
- разрешать conflict через скрытый `last-write-wins`;
- применять proposed update из stale base revision как будто base не изменилась;
- начинать зависеть от произвольного state field только потому, что оно присутствует в container;
- кодировать `unknown`/`unavailable` magic sentinel без contract;
- смешивать observed, predicted, retrieved и intervened значения без provenance;
- протаскивать model-specific hidden state/provider clients/live infrastructure objects в canonical shared state;
- считать clone одного `CognitiveState` полным Agent clone при наличии другого causally relevant private state.

Каждый future canonical field должен иметь declared semantic owner, scope/lifetime, availability/freshness semantics и provenance requirements.

Concrete container пока не выбран.

---

# 12. Module protocol и scheduler discipline

Обязательны [`docs/design/module-lifecycle.md`](docs/design/module-lifecycle.md) и `ADR-0005`.

Помнить:

```text
execution order = declared dependencies + freshness + lifecycle constraints
instantaneous scheduler graph = DAG
```

```text
modules одной wave
→ читают одну base state_revision
→ исполняются под одной agent_revision
→ публикуют staged effects
→ commit согласованно
```

До явного изменения canonical design запрещается:

- ad-hoc central main-loop ordering cognitive modules;
- строить ordering на случайном registry/import order;
- создавать instantaneous dependency cycle;
- читать undeclared state fields;
- recursively вызывать peer/scheduler для hidden dependency;
- публиковать output соседу той же wave до commit;
- использовать physical completion order как cognitive semantics;
- overlapping canonical writes без owner/reducer;
- commit causally relevant private state раньше связанного accepted effect;
- оставлять private state изменённым после rejected wave;
- молча rebase stale-base result;
- менять `agent_revision` внутри in-flight wave;
- публиковать partial required-wave state;
- выполнять hidden optimizer update внутри обычного `compute`;
- скрыто переключаться на fallback implementation;
- считать `disabled` и `NoOp` одним состоянием.

`Cognitive Scheduler` относится к Agent runtime core, но не является когнитивным модулем.

---

# 13. Observability и intervention discipline

Обязательны [`docs/design/observability-and-intervention.md`](docs/design/observability-and-intervention.md) и `ADR-0006`.

Помнить:

```text
Observability ≠ Intervention
inspection capability ≠ write authority
natural execution ≠ intervened execution
```

До явного изменения canonical design запрещается:

- использовать logger/Artifact Collector/Evaluation Runtime как normal cognitive dependency;
- давать passive observer mutation authority;
- объединять tracing и mutation в неразличимый callback contract;
- использовать mutable reference как canonical private-state probe;
- делать research-only probe cognitive dependency;
- превращать profiler/experiment metadata в cognitive payload;
- выполнять intervention без explicit target/base/provenance;
- менять semantic owner из-за evaluator override;
- переписывать committed natural history;
- скрывать intervention как natural output;
- выдавать partial restore за exact counterfactual;
- смешивать intervened trajectory с natural experience без provenance;
- считать raw activation access обязательной capability общего contract;
- игнорировать OOD/off-target risk latent intervention;
- молча терять evidence-critical telemetry и использовать Run как полный confirmatory evidence.

---

# 14. Environment discipline

Обязательны [`docs/design/modules/environment.md`](docs/design/modules/environment.md), [`docs/design/contracts/environment.md`](docs/design/contracts/environment.md) и `ADR-0007`.

Помнить:

```text
Agent Interaction Plane ≠ Environment Research Plane
Raw Observation ≠ Hidden World State ≠ Research Ground Truth
External Task Feedback ≠ Objective Task Metric ≠ Internal Utility
seed ≠ complete world identity
```

До явного изменения canonical design запрещается:

- передавать hidden world state/oracle/evaluator metric в normal Agent input;
- передавать framework `info` Agent целиком без explicit schema;
- считать split/distribution/seed частью observation по умолчанию;
- использовать research-only metric как feedback;
- использовать External Task Feedback как определение Internal Utility;
- смешивать malformed action и valid-but-ineffective action;
- раскрывать privileged failure reason без task semantics;
- терять `terminated`/`truncated`;
- считать full hidden map обычной partial observation;
- жёстко кодировать appearance shortcut как causal semantics;
- считать один seed достаточным для exact reproduction;
- называть restore/fork exact без hidden/pending/RNG state;
- использовать research restore/intervention как Agent action;
- смешивать natural/intervened world histories;
- терять terminal outcome при autoreset;
- считать `MicroWorld` universal internal representation;
- фиксировать Gymnasium/MiniGrid/Procgen обязательными только из-за research evidence.

---

# 15. Perception и representation discipline

Обязательны [`docs/design/modules/perception.md`](docs/design/modules/perception.md), [`docs/design/contracts/perception.md`](docs/design/contracts/perception.md) и `ADR-0008`.

Помнить:

```text
Raw Observation ≠ Canonical Percept
Canonical Percept = structured Semantic Core + optional Feature Views
Canonical Percept ≠ Cortex hidden state
current percept ≠ Memory / hidden-world belief / World Model prediction
feature dimension equality ≠ feature-space compatibility
```

До явного изменения canonical design запрещается:

- передавать raw Environment-specific schema независимым cognitive modules;
- использовать Research Ground Truth как normal Perception input;
- добавлять unseen hidden entity в Semantic Core из evaluator knowledge;
- использовать hidden persistent Environment object ID как percept identity;
- приписывать смысл порядку entity array/padding;
- смешивать direct/derived/inferred fields без provenance;
- маскировать learned inference как Environment ground truth;
- кодировать missing modality/property universal zero/NaN/None без contract;
- поглощать Task Specification/Feedback в Perception из-за их текстовой формы;
- делать один learned latent единственным canonical inter-module representation;
- протаскивать Cortex embedding/hidden state как mandatory representation;
- делать Cortex обязательным для Perception;
- считать одинаковый shape доказательством compatibility;
- молча смешивать несовместимые `feature_space_revision`;
- переписывать committed percept после encoder update;
- hidden fallback на Cortex/privileged data;
- считать device/object identity semantic representation identity.

`NoCortex` configuration обязана оставаться архитектурно допустимой.

---

# 16. Goal System discipline

Обязательны [`docs/design/modules/goals.md`](docs/design/modules/goals.md), [`docs/design/contracts/goals.md`](docs/design/contracts/goals.md) и `ADR-0009`.

Помнить:

```text
External Task Specification ≠ Goal Proposal ≠ Committed Goal
```

```text
Goal ≠ Reward ≠ Drive ≠ Utility / Value ≠ Policy
```

```text
structural goal priority ≠ dynamic goal value
commitment ≠ focus ≠ priority ≠ value
```

До явного изменения canonical design запрещается:

- использовать `External Task Specification` как прямой mutable alias canonical Goal state;
- хранить единственный authoritative `current_goal` только внутри Policy/Cortex hidden state;
- давать Cortex, Planner, Drives или другим proposal sources direct write authority committed Goal Graph;
- выдавать Goal Proposal за уже принятую цель;
- использовать prompt text как canonical Goal representation без grounding/proposal boundary;
- сводить Goal к scalar reward или reward function;
- сводить Goal Graph к обязательному LIFO stack;
- считать смену focus удалением/abandonment остальных active goals;
- создавать cyclic dependency relation внутри committed Goal Graph;
- считать достижение subgoal автоматическим достижением parent без explicit decomposition semantics;
- сводить `suspended`, `failed`, `expired`, `abandoned`, `invalidated` в один `done`;
- считать truncation автоматическим goal failure;
- очищать session/agent-long-lived goals при каждом `Environment.reset()`;
- использовать structural priority как hidden universal utility;
- использовать commitment как synonym reward weight/value;
- требовать universal scalar progress `[0,1]` для каждой цели;
- вычислять runtime progress/success из research-only `Objective Task Metric` без agent-visible contract;
- позволять consumer мутировать Goal record/graph через retained reference;
- скрыто менять goal objective/lifecycle без proposal/transition provenance;
- использовать hidden Environment task ID как canonical `goal_id`;
- смешивать research Goal intervention с natural lifecycle transition без provenance.

Источники goals должны создавать proposal/transition proposal через declared boundary. Goal System остаётся semantic owner canonical Goal state.

Exact Goal DSL, internal goal generation, dynamic valuation, focus arbitration, planner decomposition algorithm и конкретный graph framework пока не выбраны.

---

# 17. Scope текущего этапа

Фактический текущий scope всегда определяется `docs/design/current.md`.

Не полагаться на старые prompt/chat сообщения или на этот файл для определения номера текущего `DU`.

Пока не появились version roadmap и implementation sequence, наличие подробного design само по себе **не разрешает начинать реализацию**.

До соответствующих Design Updates не превращать обсуждавшиеся кандидаты в обязательные implementation choices, включая:

- конкретный Cortex backend;
- размер canonical latent/state representations;
- state framework;
- RL/world-model/curiosity algorithms;
- Memory backend;
- training framework;
- Colab/cloud runtime;
- DI/config/plugin framework;
- scheduler/async/graph framework;
- telemetry/intervention framework;
- Gymnasium/другой Environment framework;
- конкретный Perception/feature encoder;
- Goal graph/DSL library;
- окончательную структуру `src/`.

---

# 18. Поведение при неопределённости

Если документация не определяет важное решение:

- не скрывать неопределённость;
- не создавать implicit contract;
- зафиксировать вопрос как design blocker/open question;
- при необходимости предложить варианты и trade-offs;
- дождаться design decision до реализации зависимой части.

Мелкие локальные implementation details, не влияющие на public/internal contracts, исследовательскую валидность или принятые boundaries, могут выбираться реализацией самостоятельно при сохранении принятых принципов.
