# Глоссарий MINDRA

## Назначение

Этот документ фиксирует **короткие рабочие значения устойчивых терминов MINDRA**.

Глоссарий не заменяет канонические subsystem design.

При конфликте приоритет имеет:

```text
accepted ADR
+
специализированный canonical design owner
→ candidate/exact contract
→ glossary
```

Термин не должен использоваться в двух существенно разных смыслах без явного уточнения.

---

# 1. Система и инфраструктура

## MINDRA Agent

Логическая когнитивная система MINDRA, владеющая agent-owned state и взаимодействующая с Environment.

Agent не равен Cortex, одной neural network, process, VM, GPU или notebook runtime.

## Agent boundary

Логическая граница ответственности Agent.

Определяется ownership/responsibility, а не deployment topology.

## Agent-owned state

Всё causally relevant состояние, принадлежащее Agent, включая при необходимости:

- `CognitiveState`;
- module-private state;
- Memory;
- World/Self/Drive private state;
- trainable parameters;
- Cortex-private state;
- RNG;
- другое состояние, влияющее на поведение.

`Agent-owned state` шире `CognitiveState`.

## Agent runtime core

Некогнитивная внутренняя runtime-часть Agent, реализующая принятые state/scheduler/lifecycle semantics.

`Cognitive Scheduler` относится к Agent runtime core.

## Environment

Внешняя по отношению к Agent система динамики мира, принимающая actions и формирующая agent-visible observations/task signals/outcomes.

## Execution Runtime

Внешняя инфраструктура, хостящая исполнение Agent и связь с Environment.

Не владеет когнитивной scheduling semantics.

## Training Runtime

Внешняя инфраструктура parameter learning, optimizer state, replay/datasets и Learning Updates.

Не является когнитивным модулем Agent.

## Evaluation Runtime

Внешняя исследовательская инфраструктура controlled evaluation/interventions/measurement.

Evaluator-only данные не становятся normal Agent input.

## Experiment Runner

Control-plane компонент, задающий run configuration, seeds, conditions и orchestration.

## Artifact Collector

Пассивный сборщик traces/metrics/snapshots/artifacts.

Не является источником normal decision signals.

## Artifact Storage

Долговечное внешнее хранилище experiment/checkpoint/log artifacts.

Не является активной Memory Agent.

## Compute Substrate

Физические CPU/GPU/process/VM/machine/provider ресурсы.

Compute topology не определяет cognitive semantics.

## Research Control Plane

Внешняя область experiment orchestration, Evaluation Runtime, researcher/operator и evidence pipeline.

---

# 2. Время и причинность

## Run

Один orchestrated запуск конкретной experiment/configuration identity.

## Agent Session

Непрерывная логическая жизнь одного Agent instance, способная содержать несколько Episodes.

## Episode

Один ограниченный цикл взаимодействия с Environment/task.

`Environment.reset()` не означает полный reset Agent.

## Decision Window

Интервал внутренней обработки между доступным observation/context и `Action Commit`.

Может содержать несколько Cognitive Cycles.

## Cognitive Cycle

Один внутренний логический цикл cognition.

Не равен Environment Transition.

## Environment Transition

Фактическое изменение Environment после committed action.

## Action Commit

Причинная граница, после которой выбранное действие считается committed частью trajectory.

## Outcome Commit

Граница, после которой фактический Environment outcome становится authoritative observed evidence Agent.

## Learning Update

Изменение trainable agent-owned parameters/adapters.

Не равно обычному runtime state update.

## Agent revision

Версия behavior-relevant trainable/configurable состояния Agent, необходимая для attribution действий/прогнозов.

## Logical time

Каноническое причинное время MINDRA.

Не равно wall-clock latency.

## Causal replay

Воспроизведение совместимой causal history/order/revisions/RNG условий.

Не означает гарантированную bitwise идентичность на любой платформе.

---

# 3. CognitiveState

## CognitiveState

Каноническое опубликованное shared runtime state MINDRA для межмодульного обмена contract-defined значениями.

`CognitiveState` не является всем состоянием Agent.

## Committed State

Семантически неизменяемая опубликованная revision `CognitiveState`.

## State revision

Логическая версия committed `CognitiveState` внутри causal lineage.

## State lineage

Причинная история state revisions и forks.

## State schema

Описание canonical state paths, owners, scopes, availability/type/shape requirements.

## State envelope

Control/provenance metadata committed snapshot.

Не является автоматически cognitive payload.

## Proposed update

Staged owner-scoped изменение относительно конкретной base revision до commit.

## State scope

Semantic lifetime значения:

```text
cycle-scoped
decision-scoped
episode-scoped
session-scoped
agent-long-lived
```

Scope не равен historical retention/checkpoint policy.

## Module-private state

Agent-owned состояние конкретного subsystem, не опубликованное как shared CognitiveState.

Если causally relevant, обязано иметь lifecycle/snapshot semantics.

## Agent Snapshot

Полный снимок causally relevant Agent state, достаточный для restore/counterfactual в пределах соответствующего contract.

Шире `CognitiveState` snapshot.

---

# 4. Availability

## `available`

Значение применимо и пригодно в текущем causal context.

## `unknown`

Значение применимо, но Agent его не знает/не оценил.

## `stale`

Ранее существовавшее значение больше не удовлетворяет freshness/current-context requirements.

## `unavailable`

Capability/значение намеренно недоступно или неприменимо.

## `missing`

Required contract value отсутствует структурно.

Обычно contract/initialization error, а не epistemic unknown.

## Freshness

Соответствие значения текущему допустимому temporal/causal context.

---

# 5. Композиция и scheduling

## Composition Root

Bootstrap boundary, где concrete implementations выбираются и явно собираются в конфигурацию.

Не является когнитивным orchestrator.

## Dependency Injection

Явная передача зависимости потребителю вместо runtime-поиска.

Не означает обязательный DI-framework.

## Service Locator

Runtime pattern, при котором потребитель ищет dependency через глобальный container/registry.

Запрещён внутри cognition/runtime MINDRA.

## Registry

Каталог identifiers/factories на composition/discovery boundary.

Не является runtime state bus.

## Adapter / Provider

Concrete implementation, изолирующая backend-specific model/library/service/storage за стабильной semantic capability boundary.

## Module

Компонент с самостоятельной responsibility, state/lifecycle и diagnostic boundary.

Не обязан быть neural network.

## Module Descriptor

Декларативное описание identity, reads/writes, lifecycle и scheduler-relevant properties.

## Execution Plan

Скомпилированный active module/dependency/lifecycle plan.

## Execution Wave

Множество ready computations, читающих одну committed base revision и не требующих current-wave outputs друг друга.

## Wave commit

Atomic validation/publication staged public/private effects текущей wave.

## Staged private update

Causally relevant private-state effect, который становится видимым только при связанном successful commit.

## Stale-base result

Result, вычисленный относительно уже недопустимой base revision.

Не rebased молча.

## Cognitive Scheduler

Некогнитивный Agent runtime mechanism, исполняющий Execution Plan и commits.

Не выбирает goals/value/actions.

## Disabled capability

Capability отсутствует в active composition.

## NoOp / `No*` configuration

Специальная baseline semantics отсутствующей/нейтральной capability согласно конкретному contract.

Не должна имитировать fake success.

## Dummy implementation

Deterministic engineering implementation для integration/lifecycle tests.

## Control implementation

Research implementation того же semantic contract для исключения альтернативных объяснений эффекта.

---

# 6. Observability и intervention

## Evidence Plane

Однонаправленная passive research boundary для traces/metrics/probes/artifacts.

Не даёт observer mutation authority.

## Trace Event

Структурированное causal execution event с идентичностями/revisions.

## Module Attempt

Факт computation модуля независимо от того, стал ли его effect committed.

## Research Probe

Declared read-only semantic projection private state для исследования.

Не становится runtime dependency.

## Intervention Gateway

Привилегированная external boundary controlled interventions.

## Intervention Target

Явно определённое состояние/result/representation, допускающее treatment.

## Treatment

Конкретное controlled изменение в experimental condition.

## Intervened lineage

Causal branch/history после intervention с explicit provenance.

## Approximate counterfactual

Controlled re-execution, где восстановлено не всё causally relevant state.

Не называется exact counterfactual.

## Intervention validity

Степень, в которой treatment допускает содержательную causal interpretation без неконтролируемого OOD/off-target corruption.

---

# 7. Environment и MicroWorld

## Agent Interaction Plane

Agent-facing surface Environment.

Содержит только contract-defined observations/tasks/feedback/action outcomes.

## Environment Research Plane

Research-only hidden state/oracle/snapshot/fork/intervention surface.

## Hidden World State

Authoritative полное состояние Environment.

Не является normal Agent input.

## Raw Observation

Agent-visible проекция Environment до Perception.

## Research Ground Truth

Privileged evaluator-only truth.

## External Task Specification

Внешнее описание задачи.

Не является committed Goal.

## External Task Feedback

Task/environment signal, намеренно доступный Agent.

Не равен Objective Task Metric или Internal Utility.

## Objective Task Metric

Research-only метрика качества выполнения.

## World Instance

Конкретный экземпляр мира.

Seed без version/generator identity недостаточен для полной identity.

## World Manifest

Версионируемое описание generation provenance конкретного world instance.

## World Distribution

Версионированное распределение генерации train/validation/test worlds.

## Environment Snapshot

Полный causally relevant снимок Environment, включая hidden/task/pending/RNG state.

## Environment clone

Независимая копия из snapshot.

## Environment fork

Новая causal lineage Environment от конкретного snapshot.

## Environment intervention

Controlled research-only изменение мира/правил/task dynamics.

## MicroWorld

Первая reference 2D symbolic Environment family MINDRA с partial observability, hidden rules, procedural generation и snapshot/fork support.

---

# 8. Perception

## Perception

Agent-owned преобразование Raw Observation в `Canonical Percept`.

## Canonical Percept

Каноническое представление **текущего наблюдения** после Perception.

Не равно Memory или World Belief.

## Semantic Core

Structured semantic surface Canonical Percept.

## Feature View

Optional learned/algorithmic representation в конкретном versioned feature space.

Не заменяет Semantic Core как единственный источник значения.

## Percept Entity Identity

Identity entity внутри percept.

По умолчанию не гарантирует persistent physical-object identity между transitions.

## Perceptual inference

Вывод о текущем observation из разрешённой sensory modality.

Не равен Memory retrieval или World Model prediction.

## Modality Status

Explicit availability/quality semantics входной modality.

## Feature Space

Семантически идентифицируемое пространство признаков.

## Feature Space Revision

Версия feature-space semantics/geometry.

Одинаковая размерность не гарантирует совместимость.

## Encoder Revision

Версия encoder/pipeline, влияющая на representations.

## Representation Drift

Изменение representation одного входа после изменения encoder/pipeline.

---

# 9. Goal System

## Goal Proposal

Кандидат на цель, предложенный внешним/internal/planner/drive/research source.

Ещё не является committed целью Agent.

## Committed Goal

Goal, принятая Goal System и существующая в canonical Goal Graph.

## Goal Graph

Committed graph целей, subgoals, dependencies/conflicts и lifecycle state.

## Goal System

Semantic owner Goal Graph и adoption/lifecycle boundary.

## Goal focus

Текущий предмет приоритетной обработки среди существующих Goals.

Не означает удаления остальных целей.

## Goal priority

Structural/declarative приоритет Goal.

Не равен dynamic value.

## Goal commitment

Persistence принятой Goal несмотря на локальные изменения context.

Не равен priority/value.

## Goal progress

Состояние продвижения к Goal.

Может быть structured/unknown; не обязан быть scalar `[0,1]`.

---

# 10. Cortex

## Cortex

Заменяемая pretrained semantic/language/reasoning capability внутри Agent boundary.

Не является самой архитектурой MINDRA.

## Cortex Gateway

Backend-neutral semantic request/result boundary Cortex.

## Cortex backend

Concrete model/runtime implementation Cortex capability.

## Cortex Adapter

Слой, преобразующий semantic request в backend-specific prompt/tokenization/API и нормализующий result.

## Cortex capability

Явно объявленная возможность backend, например structured output, embeddings, hidden states или gradients.

Optional research capabilities не обязательны для любого Cortex.

## NoCortex

Конфигурация отсутствующей Cortex capability.

Не fake empty-string backend.

---

# 11. Memory

## Memory Core

Agent-owned subsystem сохранения и explicit retrieval прошлого опыта.

## MemoryRecord

Каноническая stable identity воспоминания с source content/provenance.

Не равен embedding/index slot.

## MemoryRepresentation

Derived representation MemoryRecord для retrieval/indexing.

Может быть перестроено без создания нового воспоминания.

## RetrievalIndex

Поисковая структура над derived representations/metadata.

Не является source of truth Memory.

## RetrievalRequest

Явный запрос к Memory из declared consumer context.

## RetrievalResult

Результат конкретного retrieval event с memory IDs, scores и provenance.

## Retrieval relevance

Мера соответствия query конкретному retrieval estimator.

Не равна salience/utility/truth.

## Episodic Memory

MemoryRecords, связанные с конкретными событиями/эпизодами опыта.

## Consolidation

Будущий процесс преобразования/переиспользования опыта для более устойчивых structures/parameters.

Точная semantics — `DU-20/26`.

---

# 12. World Model

## World Model

Agent-owned subsystem belief-state estimation и prediction dynamics внешнего мира.

## World Belief

Текущая интегрированная оценка состояния мира при partial observability.

Не равна Hidden World State или текущему Canonical Percept.

## Assimilation

Обновление World Belief на основании фактически полученного Agent evidence.

## World Prediction

Action/context-conditioned prediction будущего без нового actual observation.

Не является observed fact.

## Imagination

Multi-step predicted/counterfactual rollout World Model.

Не является Environment trajectory.

## Prediction Error Evidence

Явное сравнение prediction с фактическим committed outcome.

Не является reward автоматически.

## Predictive uncertainty

Оценка неопределённости World Model prediction.

Не равна risk/value.

---

# 13. Self Model

## Agent Capability Manifest

Versioned self-observable факты о намеренно доступных Agent capabilities/configuration.

Не dump всей host/runtime telemetry.

## Self Evidence

Causal evidence о фактических возможностях/результатах самого Agent.

Evaluator-only truth не является natural Self Evidence.

## Self Belief

Committed context-conditioned модель собственной competence/limitations.

## Competence

Оценка функциональной способности Agent в определённом domain/context.

Не один global confidence scalar.

## Self Prediction

Прогноз собственного outcome/cost/state относительно explicit target/context/horizon.

## `P(success)`

Вероятность определённого success event при заданном context/horizon.

Не равна uncertainty/support самой оценки.

## Estimate uncertainty / support

Насколько Self Model имеет основания доверять своей собственной оценке.

## SelfPredictionResolution

Связь ранее сделанного Self Prediction с фактическим outcome для calibration evidence.

## Calibration

Соответствие вероятностных self-predictions фактическим частотам outcomes в определённом domain.

## Cortex self-report

Текстовая/semantic self-assessment Cortex.

Может быть derived evidence, но не authoritative Self Belief.

---

# 14. Intrinsic Signals

## Intrinsic Signal

Typed нейтральное измерение свойства собственного опыта Agent.

Не является reward/Drive/Utility автоматически.

## Intrinsic Signal Provider

Независимый agent-owned estimator конкретного signal family.

## IntrinsicSignalBundle

Коллекция typed outputs providers без mandatory scalarization.

## Prediction discrepancy

Измерение расхождения prediction и actual outcome.

Не равно probabilistic surprisal или novelty.

## Predictive surprisal

Информационная неожиданность outcome относительно meaningful predictive probability, conceptually `-log p(outcome | context)`.

Недоступна без соответствующей probabilistic semantics.

## Novelty

Новизна относительно явно заданной history/representation/reference scope.

Не равна visitation rarity.

## Visitation rarity

Редкость посещения state/event относительно versioned count/density/reference model.

## Information gain

Изменение knowledge/belief state, требующее meaningful before/after semantics.

Не равен любой uncertainty reduction.

## Uncertainty change

Signed изменение совместимой uncertainty estimate между двумя состояниями знания.

## Competence change

Signed изменение competence estimate Self Model относительно определённого domain/window.

Improvement и degradation не смешиваются автоматически через `abs()`.

---

# 15. Drives

## Drive System

Agent-owned subsystem, владеющий committed набором persistent typed regulatory states — `DriveStateSet`.

Не является global motivation scalar или Policy.

## Drive

Отдельный typed persistent regulatory component внутри Drive System с собственной state/dynamics semantics.

Drive не является Intrinsic Signal или reward weight.

## DriveDescriptor

Versioned описание semantic identity, dynamics kind, update sources, persistence, target/range/coupling capabilities конкретного drive.

## Drive State

Текущее persistent внутреннее состояние конкретного drive.

Может быть structured и не обязано быть одним scalar.

## DriveStateSet

Committed набор states всех активных drives с собственной revision.

Не scalarize их автоматически.

## Drive Pressure

Производная текущая интенсивность regulatory deviation/activation **в собственной семантике конкретного drive**.

Не является общей валютой между drives и не равна Utility.

## Homeostatic Drive

Drive с реально определённой регулируемой переменной и meaningful target/range semantics.

## Regulated variable

Внутренняя величина, которую homeostatic drive стремится удерживать в определённом диапазоне на уровне его dynamics semantics.

## Homeostatic target / range

Versioned желательный диапазон регулируемой переменной homeostatic drive.

Не является универсальным требованием ко всем drives.

## Regulatory deviation / deficit

Отклонение регулируемой переменной от target/range согласно конкретной drive semantics.

Не является RL reward автоматически.

## Adaptive Motivational Drive

Persistent drive без обязательного физиологически/homeostatically осмысленного set-point.

Может иметь accumulation/satiation/recovery/habituation dynamics.

## Drive dynamics

Versioned правило изменения Drive State из предыдущего committed state, explicit inputs и logical time/lifecycle events.

## Drive coupling

Явно определённое влияние одного drive state на dynamics другого.

Не реализуется hidden direct peer mutation.

## Drive Goal Proposal

Goal Proposal, сформированный на основании Drive State через явную proposal boundary.

Drive не commit Goal напрямую.

## Natural Drive update

Обычное causal изменение Drive State через объявленную dynamics.

## Drive intervention

Research treatment Drive State/target/dynamics/coupling через Intervention Gateway.

Не маскируется под natural regulation.

## NoDrives

Конфигурация отсутствующей Drive capability.

Не набор fake zero-pressure states.

---

# 16. Будущие когнитивные термины

Следующие определения **предварительные** до соответствующих DU.

## Appraisal

Будущая event-level контекстная оценка значения события/ситуации относительно Goal, Drives, моделей и другого доступного context.

Точная semantics определяется `DU-16`.

## Affect

Кандидат на persistent внутреннее функциональное состояние, интегрирующее результаты Appraisal во времени.

Не является автоматически человеческим чувством.

Точная semantics/gate — `DU-17`.

## Valuation

Будущая decision-relevant система ценности, объединяющая несколько типов evidence без преждевременного предположения одного reward scalar.

Точная semantics — `DU-18`.

## Salience

Будущая относительная приоритетность информации для ограниченного cognitive processing/memory/replay/workspace.

Точная semantics — `DU-19`.

## Workspace

Кандидат на ограниченную temporary global-access surface.

Не равен CognitiveState по умолчанию.

Точная semantics/gate — `DU-21`.

## Executive Control

Будущая cognitive regulation strategy/compute/retrieval/planning decisions.

Не равна Cognitive Scheduler.

Точная semantics — `DU-22`.

## Policy

Будущий механизм выбора candidate action из state/context/value/predictions.

## Planner

Будущий механизм явного построения/сравнения action/plan sequences.

## Action Gate / Executor

Будущая boundary между selected action, фактическим dispatch/execution и observed outcome.

---

# 17. Сигналы и ценность

## Reward

Training signal конкретного learning algorithm.

Не использовать как универсальное название любого внутреннего значения.

## Extrinsic signal

Внешний task/environment signal.

Нужно различать agent-visible feedback и evaluator-only metric.

## Utility / Value

Рабочий термин decision-relevant ценности.

Точная vector/scalar semantics ещё не принята до `DU-18`.

## Risk

Будущий decision-relevant downside/uncertainty-sensitive construct.

Не равен predictive uncertainty автоматически.

---

# 18. Исследовательские термины

## Baseline

Сравнительная конфигурация, относительно которой оценивается механизм.

## Ablation

Удаление/отключение/замена subsystem для измерения его вклада.

## Control

Конфигурация для исключения альтернативного объяснения эффекта.

Примеры: constant, random, shuffled, parameter/compute-matched implementation.

## Counterfactual experiment

Сравнение causal branches от общего base state с контролируемым различием условий.

## Architecture gain

Рабочее понятие улучшения измеряемой способности относительно baseline.

Точная метрика определяется MINDRA-Eval.

## Provenance

Информация о происхождении state/data/artifact/update/intervention/result.

## Research evidence

Фактический результат воспроизводимого эксперимента с conditions/limitations.

Не равен interpretation и не переписывает design автоматически.

---

# 19. Сознание и функциональные аналогии

## Functional subjectivity

Рабочий термин MINDRA для зависимости внутренних оценок/поведения от собственного состояния и истории конкретного Agent при одинаковом внешнем контексте.

Не означает phenomenal consciousness.

## Consciousness

Широкий научно-философский термин, который MINDRA не объявляет автоматически достигнутым свойством.

## Phenomenal consciousness

Наличие субъективного опыта — условного «как это ощущается изнутри».

Функциональная архитектура сама по себе этого не доказывает.

## Self-reference

Способность ссылаться на себя в representation/language.

Не равна Self Model или self-awareness.

## Self-awareness / самосознание

Не используется как техническая характеристика MINDRA без отдельного operational definition и evidence.

---

# 20. Документационные термины

## Canonical design

Актуальная принятая архитектурная semantics — source of truth реализации.

## ADR

Architecture Decision Record — запись существенного выбора, альтернатив и trade-offs.

## Candidate contract

Machine-facing semantic contract после принятого design, который ещё может уточняться downstream DU.

## Exact internal contract

Frozen machine-facing specification перед implementation/version freeze.

## Design Update (`DU-xx`)

Самостоятельный архитектурный documentation update.

Не является software version.

## Version specification

Будущий документ, фиксирующий scope конкретной software version после `DU-32`.

## Implementation sequence

Patch-oriented последовательность работ Codex для конкретной software version.
