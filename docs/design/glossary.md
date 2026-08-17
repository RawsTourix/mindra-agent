# Глоссарий MINDRA

## Назначение

Короткие рабочие определения устойчивых терминов MINDRA. При конфликте приоритет имеют accepted ADR и специализированный canonical design.

---

# Система

## MINDRA Agent

Логическая agent-owned когнитивная система. Не равна процессу, GPU, VM или Cortex.

## CognitiveState

Committed versioned shared-state surface между модулями. Не полный Agent state, не mutable bus и не Workspace.

## Agent Snapshot

Полный causally relevant снимок Agent: shared/private state, Memory, Workspace, Executive/Policy/Planner state, pending Action Boundary state, parameters, RNG и другие stateful mechanisms.

## Cognitive Scheduler

Agent-owned механизм declared scheduling/waves/commits. Не cognitive module и не Executive Control.

## Agent revision

Версия behavior-relevant composition/parameters Agent.

---

# Environment / Perception

## Raw Observation

Agent-visible Environment observation до Perception normalization.

## Canonical Percept

Стабильное internal representation текущего observation.

## Feature View

Optional derived representation с explicit feature-space/encoder revision.

## Hidden World State

Privileged internal state Environment, недоступный Agent без explicit boundary.

---

# Goals / Cortex / Memory

## Goal Proposal

Кандидат на цель; ещё не committed Goal.

## Committed Goal

Цель, принятая Goal System и существующая в Goal Graph.

## Cortex

Заменяемая semantic/language/reasoning capability; не вся MINDRA.

## MemoryRecord

Каноническое воспоминание со stable identity/provenance; не embedding/index slot.

## RetrievalResult

Результат явного query-driven Memory retrieval event.

---

# World / Self

## World Belief

Текущая интегрированная оценка мира при partial observability.

## World Prediction

Prediction будущего без нового actual observation; не факт.

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

Валидный result, когда explicit policy не даёт полного ordering.

---

# Salience / Attention

## Salience System

Agent-owned subsystem purpose-dependent priority ограниченного processing для explicit candidates.

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

Explicit agent-owned re-presentation существующего `MemoryRecord` для consolidation/maintenance. Не Training Replay и не новый natural experience.

## Consolidation Event

Отдельное causal событие memory derivation/maintenance. Не Cognitive Cycle и не Learning Update.

## Derived MemoryRecord

Новый canonical record из source records с `derived_from`/support/conflict/provenance. Не переписанный source episode.

## Representation maintenance

Re-encoding/reindexing существующего MemoryRecord. Не semantic consolidation.

---

# Workspace

## Workspace

Bounded temporary shared-access/broadcast capability MINDRA для dynamically admitted subset информации. Не `CognitiveState`, Memory, Cortex context или доказательство сознания.

## WorkspaceProposal

Предложение producer поместить source-linked semantic content/projection в Workspace. Не direct write.

## WorkspaceCandidateSet

Explicit набор Workspace proposals для admission на конкретной base revision. Workspace не сканирует Agent state ambient способом.

## WorkspaceBudget

Explicit capacity/bandwidth constraint Workspace. Не `AttentionBudget`, `MemoryBudget` или global Executive compute budget.

## Workspace AdmissionPolicy

Versioned policy admission/retain/replace/expire при текущем budget/context. Salience может быть evidence, но не является самой policy.

## WorkspaceItem

Admitted temporary shared item со stable workspace identity, source ref/revision/provenance, semantic payload/projection и lifetime. Не новый factual authority.

## WorkspaceSnapshot

Committed immutable по смыслу состояние Workspace на конкретной `workspace_revision`.

## Broadcast

Доступность admitted Workspace content всем declared eligible consumers при их обычном scheduled compute. Не callback, interrupt или automatic module execution.

## Branch-local Workspace

Клон Workspace внутри imagination/counterfactual branch. Его updates не мутируют real Workspace автоматически.

## NoWorkspace

Конфигурация отсутствующей Workspace capability; consumers используют ordinary declared inputs/direct reads.

---

# Metacognitive / Executive Control

## Executive Control

Agent-owned control responsibility, выбирающая допустимые optional internal operations, распределяющая предоставленный cognitive resource envelope и решающая continue/yield cognition. Не Cognitive Scheduler и не Policy/Planner.

## Metacognitive monitoring

Declared evidence о состоянии собственного cognition — competence, uncertainty, progress, failures, resource state и т.п. Monitoring само по себе не является control decision.

## Internal MetaAction

Решение инициировать/разрешить внутреннюю cognitive operation. Не Environment Action.

## MetaActionProposal

Explicit предложение выполнить optional internal operation с semantic payload ref, prerequisites, cost/evidence и provenance. Ещё не reservation и не execution.

## InternalOperationCatalog

Versioned declarative описание доступных Executive semantic operations и constraints. Не runtime Service Locator и не набор live service handles.

## CognitiveResourceEnvelope

Явно предоставленный Executive набор hard/soft cognitive resource limits. Не raw runtime/GPU telemetry и не ресурс, который Executive может увеличить самостоятельно.

## ExecutiveBudgetLedger

Agent-owned учёт granted/reserved/consumed/remaining cognitive resources внутри `CognitiveResourceEnvelope`.

## ResourceCostProfile

Versioned estimate стоимости proposed internal operation. Не actual consumption.

## ActualResourceCost

Фактически зарегистрированное resource consumption выполненной internal operation.

## ExecutiveObservation

Declared read-only projection monitoring evidence для Executive. Не ambient dump всего `CognitiveState`.

## Executive Control Point

Явная causal boundary относительно committed state, на которой Executive принимает следующее control decision.

## ExecutiveDecision

Versioned решение Executive: выбранные `MetaActionRequest`, budget reservations, optional Goal focus и deliberation disposition. Само по себе не исполняет operation.

## Deliberation disposition

Semantic результат control point: продолжать optional cognition, yield to Policy, budget exhausted/degraded/blocked и т.п. `yield_to_policy` не является `Action Commit`.

## GoalFocusDirective

Temporary Executive-owned focus refs на уже committed Goals. Не изменяет Goal objective/lifecycle/commitment и не заменяет `Goal Proposal`.

## NoExecutive

First-class конфигурация без adaptive agent-owned meta-control: optional cognition определяется fixed version/runtime schedule.

---

# Policy / Planner

## Policy System

Обязательный agent-owned semantic owner финального behavioral selection до Action Gate. Не Planner, Executive Control или Action Executor.

## Planner

Optional/falsifiable provider explicit multi-step/contingent plans и action candidates. Не World Model и не final selection owner.

## BehavioralContext

Declared read projection контекста, разрешённого Policy/Planner в конкретном Decision Window. Не ambient dump `CognitiveState`.

## ActionCandidate

Предложение возможного behavior с explicit source/provenance. Ещё не выбрано Policy и не разрешено Action Gate.

## PolicyCandidateSet

Versioned explicit набор `ActionCandidate` конкретного selection attempt.

## Plan

Agent-owned prescriptive/conditional структура возможного поведения с steps/branches/conditions/assumptions/validity. Не `ImaginedTrajectory`.

## PlanState

Persistent state активного plan, включая progress, validity/staleness и replanning context.

## DecisionDeferral

Явный результат Policy selection attempt, когда selected intention ещё не сформировано и требуется дополнительное cognition или explicit fallback.

## SelectedActionIntent

Выбранное Policy behavioral intention до Action Boundary. Не `AuthorizedAction`, `Action Commit`, dispatch, executed action или observed outcome.

## ReactivePolicy

Policy configuration без отдельного Planner/search, выбирающая behavior непосредственно из разрешённого context/evidence.

## NoPlanner

First-class configuration без Planner capability; Policy продолжает normal behavioral selection reactive/direct способом.

---

# Action Boundary / Gate / Executor

## Action Boundary

Обязательная граница между Policy-selected intent и внешним Environment effect: authorization → `Action Commit` → dispatch/execution correlation.

## Action Gate

Agent-runtime authorization responsibility, проверяющая schema/freshness/capability/preconditions/explicit constraints. Не hidden Policy и не Environment oracle.

## ActionAuthorizationResult

Versioned результат Gate/authorization chain: authorized, rejected/stale/blocked/failed с stage provenance.

## AuthorizedAction

Успешно проверенное final semantic action до `Action Commit`. Может включать semantics-preserving normalization или explicit override lineage.

## ActionOverrideRecord

Явная запись behavior-changing replacement `Policy intent A → external action B` с owner/revision/reason/provenance. Без неё скрытая substitution запрещена.

## Action Commit

Необратимая causal boundary после final authorization и до dispatch. Фиксирует external action для данного Decision Window, но не гарантирует успешное исполнение.

## ActionCommitRecord

Immutable evidence committed action, связывающая intent/authorization/revisions с stable dispatch identity.

## DispatchAttempt

Одна transport/execution-adapter попытка отправить уже committed action. Retry того же logical dispatch не создаёт новый Action Commit.

## EnvironmentActionReceipt

Environment/adapter acknowledgement принятия команды. `accepted` не означает `succeeded`.

## ActionExecutionRecord

Causal evidence фактического lifecycle action: accepted/executing/completed/no-effect/partial/aborted/cancelled/rejected/unknown согласно capabilities среды.

## execution_unknown

Состояние, при котором неизвестно, был ли уже применён dispatched action. Не эквивалентно `not_executed` и не разрешает blind retry без idempotency/dedup/reconciliation guarantee.

## Semantics-preserving normalization

Преобразование representation/units/encoding без изменения behavioral meaning action. Не новый Policy choice.

## Runtime-assurance override

Explicit external/deployment safety correction action. Не приписывается Policy и сохраняет отдельную provenance.

---

# Будущие области

## Experience / Data / Replay

Будущая causal experience/data schema для trajectories и Training Replay. `DU-25`.

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
