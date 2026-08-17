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

Полный causally relevant снимок Agent: shared/private state, Memory, parameters, RNG, Workspace и другие stateful mechanisms.

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

Versioned policy, принимающая решения admission/retain/replace/expire при текущем budget/context. Salience может быть evidence, но не является самой policy.

## WorkspaceItem

Admitted temporary shared item со stable workspace identity, source ref/revision/provenance, semantic payload/projection и lifetime. Не новый factual authority.

## WorkspaceSnapshot

Committed immutable по смыслу состояние Workspace на конкретной `workspace_revision`.

## Broadcast

В контексте MINDRA — доступность admitted Workspace content всем declared eligible consumers при их обычном scheduled compute. Не callback, interrupt или automatic module execution.

## WorkspaceReadCapability

Declared contract consumer, определяющий какие Workspace content kinds/projections он имеет право читать.

## Branch-local Workspace

Клон Workspace внутри imagination/counterfactual branch. Его updates не мутируют real Workspace автоматически.

## NoWorkspace

Конфигурация отсутствующей Workspace capability; consumers используют ordinary declared inputs/direct reads.

## Matched Workspace control

Control с сопоставимой state/parameter/compute capacity, но без целевой competition/broadcast semantics; нужен для проверки отдельного causal вклада Workspace.

---

# Будущие области

## Executive Control

Будущая agent-owned regulation cognitive process: выбор допустимых internal operations и allocation global compute/resource budget. Не Cognitive Scheduler. `DU-22`.

## Policy / Planner

Будущая boundary планирования/final behavior selection. `DU-23`.

## Action Gate / Executor

Будущая boundary между selected action, execution и observed outcome. `DU-24`.

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
