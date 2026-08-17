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

## Agent runtime core

Некогнитивная внутренняя runtime-часть Agent, обеспечивающая исполнение принятых module/state semantics.

В `DU-05` к ней относится `Cognitive Scheduler`: он координирует выполнение модулей и state commits, но не выбирает task-level решения за когнитивные модули.

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

Execution Runtime может физически хостить Agent runtime core, но не владеет внутренней scheduling semantics MINDRA.

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

# Environment и MicroWorld

## Agent Interaction Plane

Agent-facing поверхность Environment, через которую Agent получает только contract-defined `Raw Observation`, `External Task Specification`, разрешённый `External Task Feedback` и termination/truncation semantics, а Environment получает committed action.

Эта boundary не включает research-only hidden state, oracle data или evaluator metrics.

## Environment Research Plane

Привилегированная research-facing поверхность Environment для hidden ground truth, authoritative transition evidence, snapshot/restore/clone/fork, generation metadata, solver/validity information и controlled Environment interventions.

Research Plane не является normal Agent input.

## Hidden World State

Authoritative полное состояние Environment, включающее скрытые entities/properties/rules, task state, world-side embodiment state, stochastic state и другие переменные, определяющие будущую динамику мира.

Hidden World State принадлежит Environment и не равен `Raw Observation`.

## Raw Observation

Agent-visible проекция Environment state до обработки Perception/Representation layer.

`Raw Observation` не является canonical internal representation MINDRA.

## Research Ground Truth

Privileged данные Environment, доступные evaluator/diagnostics для измерения и causal analysis: полный world state, true hidden rules, oracle/solver information, authoritative outcome reason и другие данные, не предназначенные Agent.

## External Task Specification

Внешнее описание задачи, предъявляемое Environment Agent в соответствии с task contract.

Не является внутренним `Goal` state MINDRA; преобразование во внутренние цели проектируется отдельно.

## External Task Feedback

Contract-defined сигнал от Environment/task, который намеренно доступен Agent после действия или события.

Может быть scalar, vector, sparse event или structured value и не является автоматически `Internal Utility`.

## Objective Task Metric

Research-only объективная метрика выполнения задачи, используемая evaluator для оценки поведения.

Не становится Agent-visible feedback автоматически.

## World Instance

Конкретный сгенерированный или загруженный экземпляр мира с определёнными geometry/content/rules/task configuration.

Один seed без version/generator identity недостаточен для однозначного определения World Instance.

## World Manifest

Версионируемый research artifact, описывающий конкретно сгенерированный world instance и его generation provenance настолько полно, насколько требуется воспроизводимость/аудит.

Может содержать hidden information и поэтому не передаётся Agent автоматически.

## World Distribution

Версионируемое распределение generation factors, из которого выбираются world/task instances для train/validation/test или специальных evaluation conditions.

Distribution identity не является normal Agent observation.

## Environment Snapshot

Семантически целостный снимок causally relevant Environment state, достаточный для восстановления будущей world dynamics при совместимых версиях.

Exact snapshot включает не только видимую карту, но также hidden/task/pending state и все Environment RNG states, влияющие на будущее.

## Environment clone

Независимый Environment instance, созданный из snapshot. Изменение clone не должно менять исходный instance.

## Environment fork

Новая research lineage Environment, созданная от конкретного snapshot с явной parent relation для control/treatment или другого counterfactual branching.

## Environment intervention

Привилегированное controlled изменение Environment state/rule/task/dynamics через research boundary с explicit target, base snapshot/revision, treatment и provenance.

Не является Agent action и не маскируется под natural world transition.

## MicroWorld

Первая reference Environment family MINDRA: минималистичный 2D symbolic world с partial observability, compositional entities, hidden causal rules, procedural generation и snapshot/fork support.

MicroWorld не является универсальным определением любого будущего Environment MINDRA.

## Procedural generation

Программное создание world/task instances из versioned configuration, factors и controlled RNG.

В MINDRA generator должен позволять отделять geometry, observable appearance, causal rules, task structure, stochasticity и другие relevant factors настолько, насколько это требуется исследовательскому design.

## Solvability / task validity

Свойство generated task instance, показывающее, соответствует ли он правилам family и существует ли решение там, где benchmark предполагает решаемую задачу.

Research oracle/validator может проверять solvability, но его данные не передаются Agent.

---

# Perception и representation

## Perception

Agent-owned capability, преобразующая текущую agent-visible `Raw Observation` в `Canonical Percept`, сохраняя provenance, missingness и representation identity.

Perception не является Memory, World Model или Goal System.

## Canonical Percept

Каноническое внутреннее представление текущего observation context после Perception processing.

Состоит conceptually из `Percept Envelope`, structured `Semantic Core`, modality status и optional `Feature Views`.

`Canonical Percept` не равен одному latent vector и не равен Cortex hidden state.

## Percept Envelope

Control/provenance metadata Canonical Percept: source observation identity, causal context, representation/schema revisions, pipeline identity и intervention provenance, если применимо.

Envelope не является автоматически cognitive input всех modules.

## Semantic Core

Структурированная semantic surface Canonical Percept, описывающая то, что Perception утверждает о **текущем agent-visible observation**: наблюдаемый self/world-side state, entities, relations, events и relevant modality state.

Semantic Core не является hidden-world belief и не включает Memory/World Model prediction без отдельной provenance/boundary.

## Feature View

Optional вычислительное представление Semantic Core и/или разрешённой Raw Observation в конкретном feature space.

Может быть learned latent, entity embedding set, spatial map или другой representation. Feature View не заменяет Semantic Core как единственный canonical source of meaning.

## Percept Entity Identity

Identity элемента entity collection внутри конкретного percept.

По умолчанию является observation-local и не гарантирует persistent identity одного объекта между Environment Transitions.

## Perceptual inference

Inference о свойствах текущего observation, полученный learned/algorithmic Perception из текущей разрешённой sensory modality.

Отличается от direct observation, deterministic normalization, Memory retrieval и World Model prediction и должен иметь соответствующую provenance.

## Modality Status

Explicit representation доступности/качества sensory modality в конкретном percept.

Отсутствующая/unavailable modality не должна кодироваться только «нулевым tensor» без contract semantics.

## Feature Space

Семантически идентифицируемое пространство признаков конкретного `Feature View`.

Совместимость определяется identity/revision/contract, а не только dimensionality tensor.

## Feature Space Revision

Версия semantic/geometry feature space, необходимая для определения совместимости stored/current embeddings.

Одинаковая размерность двух revisions не делает их автоматически совместимыми.

## Encoder Revision

Идентичность версии trainable/algorithmic encoder, которая влияет на получаемый Feature View или perceptual inference.

Update encoder, меняющий behavior/representations, должен быть воспроизводимо versioned.

## Representation Drift

Изменение representation одного и того же входа после изменения learned encoder/pipeline.

Drift не является автоматически ошибкой, но должен быть измеримым и не позволяет молча смешивать несовместимые embeddings.

## Sensor / Input Intervention

Controlled research treatment, изменяющий agent-visible Raw Observation после Environment projection, но не изменяющий Hidden World State.

Отличается от Environment world-state intervention и от semantic/feature intervention после Perception.

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

# Module protocol и scheduling

## Module

Компонент с явной responsibility, входами, выходами, state/lifecycle и диагностической границей.

Модуль не обязан быть нейросетью.

## Semantic module identity

Идентичность роли/экземпляра модуля в active Agent composition, не зависящая от конкретной implementation.

## Implementation identity

Идентичность concrete implementation, подключённой к semantic module role в конкретном run, например learned/NoOp/control implementation.

## Module Descriptor

Декларативное описание модуля, достаточное для composition/scheduling validation: identity, reads, writes, lifecycle participation, private-state traits и другие scheduler-relevant свойства.

Exact Python representation пока не определена.

## Declared read

State dependency, которую module contract явно разрешает модулю читать.

Наличие поля в container само по себе не создаёт dependency.

## Declared write

Canonical path/namespace, которым module contract предоставляет write authority для proposed updates.

Declared write не даёт права мутировать committed snapshot напрямую.

## Execution Plan

Скомпилированное представление active module composition, dependency graph, lifecycle phases, execution waves и compatibility/failure constraints для конкретного режима исполнения.

## Instantaneous dependency graph

Граф зависимостей module computations в одном causal scheduler segment.

В MINDRA он должен быть DAG. Feedback между модулями выражается через logical time/state revisions, а не instantaneous cycle.

## Execution Wave

Множество ready modules, которые могут вычисляться относительно одной committed base `state_revision` и `agent_revision`, не требуя current-wave outputs друг друга.

Physical completion order modules внутри wave не является cognitive semantics.

## Wave commit

Validation и согласованная публикация staged public/private effects execution wave.

Required wave не должен оставлять partial committed effects при failure одного обязательного module computation.

## Staged private update

Causally relevant изменение module-private state, подготовленное во время computation, но не становящееся семантически видимым до связанного successful commit.

## Stale-base result

Module result, вычисленный относительно base revision, которая больше не является допустимой для его применения.

По умолчанию такой result не применяется и не rebased молча.

## Cognitive Scheduler

Некогнитивный механизм Agent runtime core, который строит/исполняет Execution Plan, формирует waves, запускает module computations, валидирует proposed effects и координирует commits/lifecycle transitions.

Scheduler не определяет task-level goals/utility/action за когнитивные модули.

## Fixed Scheduler

Scheduler policy, в которой допустимый порядок/число обязательных computations задаются deterministic runtime rules/configuration, а не learned Executive Control.

## Executive Control

Будущая когнитивная ответственность, способная влиять на допустимый optional compute/cycle budget, но не имеющая права bypass scheduler contracts, ownership и commit rules.

Точная семантика определяется в `DU-22`.

## Disabled module

Semantic capability, отсутствующая в active execution plan.

Если downstream dependency требует эту capability и не допускает отсутствие, composition invalid.

## NoOp implementation

Активная concrete implementation semantic module contract, используемая для baseline/ablation и выдающая contract-valid нейтральное/unknown/unavailable поведение согласно design.

`NoOp` не равно `disabled`.

## Control implementation

Concrete implementation того же semantic contract, предназначенная для research control и исключения альтернативного объяснения эффекта.

## Atomic module effect

Требование, согласно которому causally related public `CognitiveState` update и module-private state effect становятся committed согласованно либо не становятся committed как partial effect.

---

# Observability и intervention

## Evidence Plane

Логическая однонаправленная поверхность, через которую Agent/runtime публикуют passive research evidence во внешнюю artifact/evaluation infrastructure.

Evidence Plane не является когнитивным module/state bus и не предоставляет observer write authority.

## Trace Event

Структурированное событие исполнения, связанное с causal identities/revisions и позволяющее реконструировать, что произошло в конкретном Run/Session/Episode/Decision/Cycle/Wave/Module Attempt.

Trace event не является автоматически cognitive input.

## Module Attempt

Факт выполнения конкретного module computation относительно определённых base `state_revision`/`agent_revision`, независимо от того, стал ли результат committed.

Attempt и commit являются разными research facts.

## Research Probe

Declared read-only research boundary, через которую evaluator/collector может получить semantic projection causally relevant private state без arbitrary mutable object access.

Research Probe не создаёт runtime dependency других cognitive modules и не даёт write authority.

## Observability Depth

Рабочее понятие глубины собираемых evidence: от structural tracing и public semantic state до private semantic probes и backend/raw tensors.

Конкретные уровни/названия могут меняться implementation, но raw/backend access не является обязательным для общего contract.

## Evidence-critical telemetry

Evidence, потеря которого делает невозможным проверку конкретной primary hypothesis или causal reconstruction.

Если такое evidence потеряно и не может быть восстановлено, соответствующий research claim считается incomplete/invalid, даже если Agent продолжил execution.

## Intervention Gateway

Привилегированная external research boundary, через которую Evaluation Runtime выполняет active controlled intervention с explicit target, base causal revision, treatment и provenance.

Intervention Gateway отделён от passive Evidence Plane.

## Intervention Target

Явно идентифицируемое состояние/результат/representation, в которое разрешено вмешательство соответствующим research capability.

Target может быть canonical state field, module public result, declared private semantic state или opt-in backend/raw representation.

## Treatment

Конкретное controlled изменение, применённое через Intervention Gateway в рамках experiment condition.

Treatment не маскируется под natural output semantic owner.

## Intervened lineage

Продолжение causal history после controlled intervention, явно помеченное intervention provenance.

По умолчанию confirmatory causal experiment предпочитает отдельную treatment branch от identifiable committed base вместо переписывания natural lineage.

## Approximate counterfactual

Контролируемое повторное выполнение/ветвление, в котором восстановлена только часть causally relevant Agent/Environment state.

Такой experiment не называется exact counterfactual clone.

## Intervention validity

Степень, в которой treatment является осмысленным для causal interpretation и не создаёт неконтролируемое OOD/divergent state или крупные off-target effects.

Особенно важна для raw/latent interventions.

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
