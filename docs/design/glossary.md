# Глоссарий MINDRA

## Назначение

Короткие рабочие определения устойчивых терминов MINDRA. При конфликте приоритет имеют accepted ADR и специализированный canonical design.

---

# Система и execution

## MINDRA Agent

Логическая agent-owned когнитивная система. Не равна process/GPU/VM/Cortex.

## CognitiveState

Committed versioned shared-state surface между модулями. Не полный Agent state, не mutable bus и не Workspace.

## Agent Snapshot

Полный causally relevant снимок Agent: shared/private state, Memory, Workspace, Executive/Policy/Planner/Action state, parameters, RNG и другие stateful mechanisms.

## Agent revision

Версия behavior-relevant composition/parameters Agent.

## Cognitive Scheduler

Agent-owned механизм declared scheduling/waves/commits. Не cognitive module, Executive Control или Policy.

## Decision Window

Логический интервал от agent-visible observation/outcome до следующего `Action Commit`.

## Cognitive Cycle

Одна причинно различимая внутренняя итерация cognition внутри Decision Window.

## Action Commit

Необратимая граница final authorized Environment action данного Decision Window. После `DU-24` находится после authorization и до dispatch.

## Outcome Commit

Момент, когда фактический outcome Environment transition становится записанным observed fact trajectory.

---

# Environment / Perception

## Raw Observation

Agent-visible Environment observation до Perception normalization.

## Canonical Percept

Стабильное internal representation текущего observation.

## Feature View

Optional derived representation с explicit feature-space/encoder revision.

## Hidden World State

Privileged internal state Environment, недоступный Agent normal runtime способом.

## World Manifest

Versioned identity/configuration конкретного generated world instance/family сверх одного seed.

---

# Goals / Cortex / Memory

## Goal Proposal

Кандидат на цель; ещё не committed Goal.

## Committed Goal

Цель, принятая Goal System и существующая в Goal Graph.

## Cortex

Заменяемая semantic/language/reasoning capability; не вся MINDRA и не central orchestrator.

## MemoryRecord

Каноническое agent-owned воспоминание со stable identity/provenance; не embedding/index slot и не research trajectory.

## RetrievalResult

Результат явного query-driven Memory retrieval event.

---

# World / Self

## World Belief

Текущая интегрированная оценка мира при partial observability.

## World Prediction

Prediction будущего без нового actual observation; не observed fact.

## Imagination

Predicted/counterfactual rollout World Model; не Environment trajectory.

## Self Belief

Committed context-conditioned модель собственной competence/limitations.

## Self Prediction

Прогноз собственного outcome/cost/state относительно explicit target/context.

---

# Intrinsic Signals / Drives

## Intrinsic Signal

Typed нейтральное измерение свойства опыта. Не Reward/Drive/Utility автоматически.

## Novelty

Новизна относительно explicit history/representation/reference scope.

## Information gain

Изменение meaningful knowledge/belief state между before/after.

## Drive State

Текущее persistent regulatory состояние конкретного Drive.

## Drive Pressure

Производная интенсивность regulation конкретного Drive; не Utility.

---

# Appraisal / Affect

## AppraisalRecord

Versioned результат оценки causally identifiable target относительно current Agent context.

## AppraisalProfile

Typed multidimensional профиль оценки без mandatory emotion label/global scalar.

## Relevance

Связь target с текущими concerns Agent. Не Salience/Value.

## Controllability

Насколько развитие ситуации чувствительно к доступным действиям Agent.

## Coping potential

Насколько текущий Agent способен эффективно изменить, выдержать или обойти последствия.

## Affect State

Persistent history-dependent modulation state. Не emotion label, Drive State или Utility.

## Simulated Affect

Branch-local Affect в imagination/counterfactual path; не real committed Affect.

---

# Valuation

## ValueProfile

Structured multi-objective representation decision-relevant ценности target до обязательной scalarization.

## RiskProfile

Decision-relevant downside profile; не predictive uncertainty.

## ComparisonPolicy

Versioned rule сравнения `ValueProfile`.

## ScalarizedValue

Derived scalar под конкретной `ComparisonPolicy`. Не universal currency и не Training Reward автоматически.

## Incomparable

Валидный result, когда explicit comparison policy не даёт полного ordering.

---

# Salience / Attention

## Salience System

Agent-owned responsibility purpose-dependent priority ограниченного processing для explicit candidates.

## SalienceProfile

Structured representation причин processing priority target. Не обязан быть scalar.

## AttentionBudget

Explicit ограничение ресурса, предоставляемое consumer/context. Не global Executive budget.

## AttentionAllocation

Результат распределения budget между candidates. Не Workspace admission и не Policy decision.

---

# Memory Regulation / Consolidation

## Memory Regulation

Agent-owned policy responsibility поверх Memory Core, управляющая admission/retention/forgetting/eviction/replay/consolidation. Не второй owner Store.

## MemoryBudget

Explicit resource constraints Memory subsystem. Не global Executive compute budget.

## Cognitive forgetting

Изменение agent-accessibility/retention state memory. Не обязательно physical deletion.

## Memory Replay / Reactivation

Agent-owned re-presentation существующего `MemoryRecord` для memory dynamics/consolidation. Не Training Replay и не новый natural experience.

## Consolidation Event

Отдельное causal событие memory derivation/maintenance. Не Cognitive Cycle и не Learning Update.

## Derived MemoryRecord

Новый canonical record из source records с source/support/conflict/provenance. Не переписанный source episode.

## Representation maintenance

Re-encoding/reindexing существующего MemoryRecord. Не semantic consolidation.

---

# Workspace

## Workspace

Bounded temporary shared-access/broadcast capability для dynamically admitted subset информации. Не `CognitiveState`, Memory, Cortex context или доказательство сознания.

## WorkspaceProposal

Предложение producer поместить source-linked semantic content/projection в Workspace. Не direct write.

## WorkspaceCandidateSet

Explicit набор Workspace proposals для admission на конкретной base revision.

## WorkspaceBudget

Explicit capacity/bandwidth constraint Workspace. Не `AttentionBudget`, `MemoryBudget` или global Executive compute budget.

## Workspace AdmissionPolicy

Versioned policy admission/retain/replace/expire. Salience может быть evidence, но не является admission decision.

## WorkspaceItem

Admitted temporary shared item со stable identity/source/provenance. Не новый factual authority.

## WorkspaceSnapshot

Committed immutable по смыслу состояние Workspace на конкретной `workspace_revision`.

## Broadcast

Доступность admitted content declared eligible consumers при обычном scheduled compute. Не callback/interrupt/module execution.

## Branch-local Workspace

Workspace clone imagination/counterfactual branch, не мутирующий real Workspace автоматически.

## NoWorkspace

First-class configuration без Workspace capability.

---

# Metacognitive / Executive Control

## Executive Control

Agent-owned control responsibility, выбирающая optional internal operations, распределяющая предоставленный cognitive resource envelope и решающая continue/yield cognition. Не Scheduler и не Policy/Planner.

## Metacognitive monitoring

Declared evidence о состоянии собственного cognition. Monitoring само по себе не control decision.

## Internal MetaAction

Решение инициировать/разрешить внутреннюю cognitive operation. Не Environment Action.

## MetaActionProposal

Explicit предложение выполнить optional internal operation с payload ref/cost/evidence/provenance. Ещё не execution.

## InternalOperationCatalog

Versioned declarative описание доступных Executive semantic operations. Не Service Locator/live handles.

## CognitiveResourceEnvelope

Hard/soft cognitive resource limits, предоставленные Executive. Executive не увеличивает их самостоятельно.

## ExecutiveBudgetLedger

Учёт granted/reserved/consumed/remaining cognitive resources.

## ResourceCostProfile

Versioned estimate стоимости proposed internal operation. Не actual consumption.

## ActualResourceCost

Фактически зарегистрированное resource consumption выполненной operation.

## ExecutiveObservation

Declared read-only projection monitoring evidence. Не ambient dump `CognitiveState`.

## Executive Control Point

Causal boundary относительно committed state, где Executive принимает control decision.

## ExecutiveDecision

Versioned выбор MetaActionRequests/budget reservations/focus/disposition. Сам по себе operation не исполняет.

## GoalFocusDirective

Temporary focus refs на committed Goals. Не изменяет Goal Graph.

## NoExecutive

Configuration без adaptive meta-control; optional cognition определяется fixed schedule.

---

# Policy / Planner

## Policy System

Обязательный agent-owned semantic owner финального behavioral selection до Action Boundary.

## Planner

Optional/falsifiable provider multi-step/contingent plans и action candidates. Не World Model и не final selection owner.

## BehavioralContext

Declared read projection контекста Policy/Planner. Не ambient dump `CognitiveState`.

## ActionCandidate

Предложение возможного behavior с source/provenance. Ещё не выбрано Policy.

## PolicyCandidateSet

Versioned explicit набор `ActionCandidate` конкретного selection attempt.

## Plan

Prescriptive/conditional структура behavior с steps/branches/assumptions/validity. Не `ImaginedTrajectory`.

## PlanState

Persistent state active plan, включая progress/validity/staleness/replanning context.

## DecisionDeferral

Результат Policy attempt без selected intention, требующий additional cognition/explicit fallback.

## SelectedActionIntent

Выбранное Policy behavioral intention до Action Boundary. Не authorized/committed/dispatched/executed action.

## ReactivePolicy

Policy configuration без отдельного Planner/search.

## NoPlanner

First-class configuration без Planner capability.

---

# Action Boundary / Gate / Executor

## Action Boundary

Граница между Policy-selected intent и Environment effect: authorization → `Action Commit` → dispatch/execution correlation.

## Action Gate

Agent-runtime authorization responsibility для schema/freshness/capability/preconditions/explicit constraints. Не hidden Policy/Environment oracle.

## AuthorizedAction

Final semantic action после успешной authorization, до `Action Commit`.

## ActionOverrideRecord

Явная запись behavior-changing replacement `Policy intent A → external action B`.

## ActionCommitRecord

Immutable evidence committed external action, связывающая intent/authorization/revisions/dispatch identity.

## DispatchAttempt

Одна transport/adapter попытка отправить уже committed action. Retry того же logical dispatch не создаёт новый Action Commit.

## EnvironmentActionReceipt

Acknowledgement принятия команды. `accepted` не означает `succeeded`.

## ActionExecutionRecord

Evidence фактического lifecycle action: completed/no-effect/partial/aborted/cancelled/rejected/unknown согласно среде.

## execution_unknown

Неизвестно, был ли уже применён dispatched action. Не эквивалентно `not_executed`.

## Semantics-preserving normalization

Изменение encoding/units без изменения behavioral meaning.

## Runtime-assurance override

Explicit external/deployment safety correction, не приписываемая Policy.

---

# Experience / Data / Replay

## Experience Data Plane

Внешняя относительно cognition responsibility записи causal experience, построения datasets и replay inputs. Может физически жить рядом с Artifact Collector.

## ExperienceEvent

Immutable по смыслу typed causal data event со stable identity, logical scope, parent refs, revisions, visibility и provenance. Не любой `TraceEvent`.

## Experience Journal

Append-only logical collection `ExperienceEvent`, являющаяся source of truth записанного опыта. Не Agent runtime state, Memory или Replay Buffer.

## ExperienceJournalManifest

Versioned manifest конкретного состояния/selection журнала, нужный для reproducible projections.

## CausalRevisionSet

Reference bundle behavior-relevant Agent/module/environment/representation revisions конкретного causal event.

## ResearchAnnotationRecord

Отдельная evaluator/research-only annotation, ссылающаяся на source events/samples. Не обычный agent-visible payload.

## DataVisibilityPolicy

Versioned правила, какие visibility/trust classes допускаются в derived dataset/training condition.

## EpisodeTrajectory

Derived projection causal events одного Episode.

## DecisionTrajectory

Derived projection событий одного Decision Window от input до intent/commit/outcome или deferral/failure.

## InteractionTransitionView

Derived interaction view, допускающий action commit без Environment transition и explicit execution status.

## DatasetManifest

Immutable/versioned описание source journals, projections, schemas, transforms, splits, revisions, quality и determinism конкретного data product.

## SampleTransformationRecord

Явная lineage-запись derived transformation: windowing, relabeling, target recomputation, re-encoding, masking и т.п.

## TrainingSample

Derived training data product со source refs и transformation lineage. Не historical source experience.

## Training Replay

Повторное использование source/derived training data внешним Training Runtime. Не Agent Memory Replay и не новое Environment experience.

## ReplayItem

Derived item replay buffer/table, ссылающийся на source sample/projection. Его eviction не удаляет source experience.

## ReplaySelectionRecord

Evidence конкретного Training Replay selection: sampler/table revision, selected sample refs, priority/probability/RNG metadata где применимо.

## Privileged supervision

Training condition, явно разрешающая evaluator-only/research annotations. Не normal agent-visible learning по умолчанию.

## Data completeness

Structured статус пригодности causal/data evidence: complete/partial/unresolved/missing/corrupt и т.п. Отдельный optional artifact loss не равен потере core causal event.

---

# Будущие области

## Training Lifecycle

Будущая boundary external optimization, Learning Update и activation новых agent/component revisions. `DU-26`.

---

# Research terms

## Baseline

Сравнительная конфигурация.

## Ablation

Отключение/замена subsystem для измерения его вклада.

## Control

Конфигурация для исключения альтернативного объяснения эффекта.

## Matched control

Control с сопоставимыми parameters/compute/state capacity, но другой целевой semantics.

## Research evidence

Фактический воспроизводимый результат с conditions/limitations; не automatic design change.
