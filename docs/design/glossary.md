# Глоссарий MINDRA

## Назначение

Этот документ фиксирует рабочие значения основных терминов проекта.

Термины могут уточняться вместе с canonical design, но одно слово не должно одновременно использоваться для нескольких существенно разных механизмов без явного пояснения.

Если короткое определение здесь расходится с более конкретным accepted design/ADR, приоритет имеет специализированный канонический документ.

---

# Система и инфраструктура

## Agent

Логическая когнитивная система MINDRA, которая владеет внутренним состоянием, использует cognitive capabilities и выбирает действия при взаимодействии с Environment.

Agent не равен Cortex, одной neural network, process, VM или GPU.

Каноническая system boundary определена в `system-context.md`.

## Agent boundary

Логическая граница ответственности, отделяющая когнитивную систему MINDRA и agent-owned state от Environment, training/evaluation infrastructure, experiment control plane и compute/storage infrastructure.

Agent boundary не обязана совпадать с process/device/network boundary.

## Environment

Внешняя по отношению к Agent система динамики мира, которая принимает actions и возвращает contract-defined observations, внешние task signals и сведения о termination/truncation.

Hidden Environment state не является автоматически доступным Agent.

## Logical boundary

Граница, определяемая responsibility и state ownership, а не физическим размещением кода.

## Deployment topology

Физическая схема размещения компонентов по process/thread/worker/device/machine/provider boundaries.

Deployment topology не определяет architecture semantics, если это отдельно не зафиксировано canonical design.

## Execution Runtime

Внешняя инфраструктурная роль, которая хостит исполнение Agent, соединяет его с Environment и обеспечивает run-level lifecycle, не являясь когнитивным модулем.

## Training Runtime

Внешняя по отношению к Agent инфраструктура обучения, которая работает с опытом, datasets, losses, optimizer state и обновляет agent-owned trainable state через явную update boundary.

Training Runtime не становится частью cognition только потому, что меняет параметры Agent.

## Evaluation Runtime

Внешняя исследовательская инфраструктура, которая запускает controlled evaluation, interventions и измерения поведения Agent.

Evaluation-derived information по умолчанию не является agent-visible input.

## Experiment Runner

Внешний control-plane компонент, задающий идентичность и конфигурацию исследовательского запуска, seed, режим выполнения и orchestration runtime components.

Experiment metadata не должна скрыто влиять на cognition Agent.

## Artifact Collector

Пассивная исследовательская инфраструктура, собирающая logs, trajectories, metrics, snapshots, checkpoints и другие evidence/artifacts.

Artifact Collector не должен быть источником normal decision signals Agent.

## Artifact Storage

Внешнее долговечное хранилище checkpoints, trajectories, logs, experiment manifests и других research/training artifacts.

Artifact Storage не является синонимом активной Memory Agent.

## Compute Substrate

Физические вычислительные ресурсы, на которых размещаются логические компоненты: CPU/GPU, process, VM, local machine, notebook runtime, remote host или future distributed infrastructure.

Compute Substrate не является когнитивной архитектурой.

## Research Control Plane

Внешняя область orchestration и experiment integrity, включающая researcher/operator, Experiment Runner, Evaluation Runtime и evidence pipeline.

Она управляет постановкой эксперимента, но не должна скрыто решать задачи за Agent.

---

# Композиция и зависимости

## Composition Root

Логическая bootstrap/composition boundary, в которой разрешаются symbolic implementation identifiers, создаются concrete implementations и собирается конкретная конфигурация Agent/runtime/evaluation для запуска.

Composition Root знает о concrete implementations, но не является когнитивным модулем и не должен содержать decision logic Agent.

## Dependency Injection

Принцип явной передачи уже разрешённой зависимости потребителю через constructor/factory/contract boundary вместо самостоятельного поиска зависимости потребителем.

В MINDRA термин не означает обязательное использование конкретного DI-framework.

## Service Locator

Pattern, при котором потребитель во время работы самостоятельно обращается к общему registry/container для поиска нужной зависимости, например `services.get(...)` или `container.resolve(...)`.

Runtime Service Locator запрещён для cognitive/runtime code MINDRA по `DU-02`.

## Registry

Каталог symbolic identifiers и factories/providers, который может использоваться на composition/discovery boundary для выбора concrete implementation.

Registry не является Agent state и не должен использоваться cognitive modules как runtime Service Locator.

## Adapter / Provider

Concrete implementation, изолирующая backend-specific library, SDK, storage, model или external service за более стабильной capability/contract boundary.

---

# Временная модель

## Run

Один orchestrated запуск MINDRA в рамках определённой experiment/configuration identity.

Run может содержать одну или несколько Agent Sessions, training/evaluation phases и связанные artifacts.

## Agent Session

Непрерывная логическая жизнь одного экземпляра Agent в рамках runtime, способная включать несколько Environment Episodes.

Agent Session не равна Episode и не обязана завершаться при `Environment.reset()`.

## Episode

Один ограниченный отрезок взаимодействия с Environment между reset/start и termination/truncation.

## Decision Window

Логический интервал между ingest текущего наблюдения и `Action Commit`, внутри которого может происходить один или несколько Cognitive Cycle.

## Cognitive Cycle

Один внутренний цикл когнитивного вычисления Agent внутри Decision Window.

Cognitive Cycle не является Environment Transition и сам по себе не продвигает внешний мир.

## Action Commit

Причинная boundary, после которой выбранное действие считается окончательно зафиксированным для соответствующего Environment Transition.

До commit action candidate может изменяться; после commit его нельзя ретроактивно переписать.

## Environment Transition

Фактический переход Environment в ответ на committed action.

## Outcome Commit

Причинная boundary, на которой результат Environment Transition становится зафиксированным observed outcome для последующей обработки.

## Learning Update

Отдельное causally identifiable изменение trainable/learned state Agent.

Learning Update не является обычным runtime state update и не должен скрываться внутри якобы frozen execution.

## Replay Step

Отдельный шаг повторного использования ранее сохранённого опыта.

Replay Step не создаёт новый observed Environment Transition.

## Consolidation Event

Отдельная maintenance/training phase, в которой накопленный опыт может изменять более долговременное состояние/representations/weights.

## Agent revision

Идентичность causally relevant набора trainable/behavioral параметров Agent, под которым выполнялось конкретное cognition/action.

Agent revision необходима для provenance при online/async learning.

---

# Состояние Agent

## Agent-owned state

Всё состояние, которое семантически принадлежит Agent независимо от физического места хранения.

Оно шире `CognitiveState` и conceptually может включать:

- canonical shared runtime state;
- module-private state;
- trainable parameters;
- active Memory storage;
- Cortex-private/backend state;
- RNG/stochastic state;
- другое causally relevant state.

## CognitiveState

Каноническое **опубликованное shared runtime state** MINDRA, через которое будущие когнитивные компоненты обмениваются contract-defined значениями.

`CognitiveState` представлен семантически неизменяемыми committed revisions и **не равен** полному `Agent-owned state`.

Каноническая семантика определена в `cognitive-state.md`.

## Committed state snapshot

Логически целостная revision `CognitiveState`, опубликованная на commit boundary и недоступная для задним числом видимой mutation.

Concrete implementation может использовать structural sharing/copy-on-write, если semantic immutability сохраняется.

## State revision

Логическая версия committed `CognitiveState` внутри causal lineage.

State revision не обязана совпадать с `cognitive_cycle_id`, `environment_transition_id` или wall-clock временем.

## State schema / schema revision

Каноническое описание допустимых state paths, semantic owners, scopes, availability/type/shape requirements и версия этого описания.

Новый произвольный runtime key не становится частью canonical schema автоматически.

## State lineage

Причинная история committed state revisions, включая parent relation и forks при counterfactual branching.

## State envelope

Control/provenance metadata, необходимая для интерпретации snapshot: temporal identities, state/schema/agent revision, lineage и другие служебные сведения.

Envelope не является автоматически cognitive input.

## Cognitive payload

Contract-defined значения `CognitiveState`, которые могут быть доступны когнитивным компонентам через declared read dependencies.

## Proposed update

Неприменённое изменение canonical state, вычисленное относительно конкретной base revision и ожидающее validation/commit.

Proposed update не является committed state.

## State scope

Semantic lifetime опубликованного значения.

На уровне `DU-04` различаются:

- `cycle-scoped`;
- `decision-scoped`;
- `episode-scoped`;
- `session-scoped`;
- `agent-long-lived`.

Scope не равен historical retention или checkpoint policy.

## Module-private state

Agent-owned state, принадлежащее конкретному модулю и не опубликованное как canonical shared `CognitiveState`.

Если оно causally влияет на поведение, его lifecycle/snapshot/restore semantics не могут оставаться скрытыми.

## Agent Snapshot

Будущий полный снимок causally relevant Agent state, достаточный для restore/counterfactual настолько, насколько это определит checkpoint design.

`Agent Snapshot` шире сериализованного `CognitiveState`.

---

# Availability и свежесть

## Availability

Семантика того, существует ли применимое и пригодное для использования значение canonical field в текущем causal context.

## `available`

Поле имеет допустимое актуальное значение.

## `unknown`

Поле семантически применимо, но Agent не знает или ещё не оценил его значение.

`unknown` является валидным epistemic состоянием, а не ошибкой.

## `stale`

Существует ранее вычисленное значение, но его temporal validity/freshness уже не покрывает текущий causal context.

## `unavailable`

Поле/способность намеренно недоступны в текущей composition/phase, например потому что модуль отключён или значение сейчас неприменимо.

## `missing`

Структурная ситуация, когда required contract ожидает path/value, но его нет.

По умолчанию `missing` является contract/initialization error, а не синонимом `unknown`.

## Freshness

Свойство, показывающее, относится ли значение к текущему допустимому causal context согласно field contract.

---

# Основные когнитивные термины

## Cortex

Заменяемая pretrained capability внутри логической границы Agent, предоставляющая богатые языковые, семантические и/или reasoning capabilities.

Cortex может быть LLM, но MINDRA не должна зависеть от конкретной модели.

Физический backend может исполняться вне основного process/machine boundary.

## Cortex backend

Конкретная реализация Cortex capability.

Примеры конкретных моделей пока не являются частью canonical design.

## Cortex Execution Provider

Внешний физический runtime/provider, который исполняет Cortex backend, когда вычисление вынесено за основной deployment boundary.

Provider не становится отдельным когнитивным модулем MINDRA только из-за физического размещения.

## Module

Компонент с явной responsibility, входами, выходами, state/lifecycle и диагностической границей.

Модуль не обязан быть нейросетью.

## World Model

Механизм, прогнозирующий динамику среды и/или последствия действий.

## Self Model

Механизм, прогнозирующий или представляющий релевантные свойства самого агента: способности, uncertainty, competence, ограничения, cost и другие self-related variables, если они будут приняты design.

Self Model не означает автоматически self-awareness.

## Drive

Внутренняя динамическая переменная или механизм, который способен менять относительную ценность состояний/действий для агента.

Drive не является синонимом reward.

## Appraisal

Функциональный механизм оценки значения события/состояния относительно текущего контекста агента: целей, drives, памяти, прогнозов и других relevant variables.

Appraisal не является доказательством эмоции как субъективного переживания.

## Affect

Рабочий зонтичный термин для внутреннего функционального состояния, возникающего из appraisal и влияющего на другие процессы системы, если такой механизм будет принят.

Не использовать `affect` как автоматический синоним человеческого чувства.

## Salience

Оценка относительной значимости информации для последующего внимания, Memory, replay, Workspace или learning.

Полезность Salience должна проверяться эмпирически.

## Memory

Подсистема сохранения и восстановления информации из предыдущего опыта.

Если Memory является активной частью cognition, её содержимое относится к agent-owned state независимо от физического storage backend.

Полный Memory store не обязан входить в `CognitiveState`.

## Working memory / working state

Краткоживущее состояние, доступное в текущем цикле обработки.

Не фиксируется как отдельный модуль до соответствующего design.

## Episodic memory

Память о конкретных эпизодах/переходах/событиях опыта с достаточным контекстом для последующего retrieval или replay.

## Consolidation

Процесс, при котором накопленный опыт используется для более долгосрочного изменения representations/weights/knowledge системы.

## Replay

Повторное использование ранее сохранённого опыта для обучения, оценки или consolidation.

## Workspace

Рабочее concept-название ограниченного интеграционного механизма, через который selected information может становиться доступной нескольким подсистемам.

Использование термина вдохновлено cognitive architectures, но не означает утверждение о сознании.

## Policy

Механизм выбора action из доступного состояния и контекста.

Policy может включать learned и algorithmic части в зависимости от будущего design.

## Planner

Механизм явного сравнения/построения последовательностей возможных действий, если он будет выделен отдельно от Policy/Cortex.

## Goal

Представление желаемого будущего состояния, результата или ограничения поведения, которое влияет на выбор действий.

Точный lifecycle целей пока не определён.

---

# Сигналы и оценки

## Reward

Внешний или внутренний scalar/vector training signal, используемый конкретным learning algorithm.

Не использовать `reward` как универсальное название любого внутреннего значения.

## Extrinsic signal

Сигнал ценности/успеха, задаваемый внешней средой или задачей.

Если сигнал существует только как evaluation metric и не входит в Environment/task contract, он не является автоматически agent-visible feedback.

## Intrinsic signal

Сигнал, вычисляемый из внутренней динамики агента или его взаимодействия со средой, например из novelty/prediction error, если соответствующий механизм принят.

Intrinsic signal не обязательно является scalar reward.

## Utility

Общее рабочее понятие для функциональной ценности состояния/действия относительно текущей системы целей и внутренних факторов.

Точная математическая форма пока не зафиксирована.

## Novelty

Степень новизны состояния/наблюдения относительно опыта или learned representation агента.

Способ вычисления определяется конкретным design.

## Surprise / prediction error

Расхождение между предсказанием модели и фактическим observation/outcome.

Не считать surprise и novelty автоматически одним и тем же.

## Uncertainty

Оценка недостатка уверенности/информации в prediction, state estimate или decision.

Нужно отличать uncertainty от raw model entropy, если design вводит более точную семантику.

## Competence

Оценка способности агента успешно решать класс задач или выполнять действие.

Если используется, должна иметь измеримую связь с фактическими outcomes.

---

# Сознание и функциональные аналогии

## Functional subjectivity

Рабочий термин MINDRA для свойства, при котором внутренняя оценка и поведение зависят не только от внешней ситуации, но и от собственного состояния/истории конкретного агента.

Не означает phenomenal consciousness.

## Consciousness

Широкий научно-философский термин, который не используется в MINDRA как автоматически достигнутое свойство архитектуры.

Любое более конкретное использование должно указывать, о каком аспекте сознания идёт речь.

## Phenomenal consciousness

Наличие субъективного опыта — условного «как это ощущается изнутри».

MINDRA не предполагает, что функциональные механизмы сами по себе доказывают phenomenal consciousness.

## Self-reference

Способность системы ссылаться на себя в representation или языке.

Не равна Self Model и не равна self-awareness.

## Self-awareness / самосознание

Термин не должен использоваться как техническая характеристика MINDRA без отдельного операционального определения и evidence.

---

# Исследовательские термины

## Ablation

Эксперимент, в котором компонент удаляется, отключается или заменяется control-реализацией для оценки его вклада.

## Intervention

Контролируемое изменение internal variable/representation с последующим измерением причинного эффекта при максимально фиксированных остальных условиях.

Evaluator intervention является специальной experimental operation и не должно смешиваться с normal Agent input.

## Counterfactual experiment

Эксперимент со сравнимыми ветвями, полученными из одного сохранённого causal state, где меняется ограниченный набор факторов.

## Baseline

Сравнительная система/конфигурация, относительно которой оценивается новый механизм.

## Control

Конфигурация, предназначенная для исключения альтернативного объяснения эффекта: например, random/no-op/parameter-matched implementation.

## Architecture gain

Рабочее понятие для улучшения измеряемой способности при добавлении MINDRA architecture относительно выбранного baseline.

Точная метрика будет определена позже.

## Provenance

Информация о происхождении данных, state update, artifact, checkpoint, intervention или experiment result, достаточная для понимания того, откуда объект появился и при каких условиях.

## Research evidence

Фактические результаты воспроизводимого эксперимента вместе с его условиями и ограничениями.

Research evidence не равно interpretation и не меняет design автоматически.

---

# Документационные термины

## Canonical design

Актуальная принятая архитектурная семантика, являющаяся source of truth для реализации.

## ADR

Architecture Decision Record — документ, фиксирующий существенный выбор между несколькими реалистичными вариантами, его причины и trade-offs.

## Exact internal contract

Точная machine-facing спецификация взаимодействия внутри MINDRA после того, как semantic design уже принят.

## Open question

Существенный вопрос, решение по которому ещё не принято.

Open question не должен превращаться в implicit implementation choice без design review.
