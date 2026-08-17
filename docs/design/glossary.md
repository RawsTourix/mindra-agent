# Глоссарий MINDRA

## Назначение

Короткие рабочие определения устойчивых терминов MINDRA. При конфликте приоритет имеют accepted ADR и специализированный canonical design.

---

# Система

## MINDRA Agent

Логическая agent-owned когнитивная система. Не равна процессу, GPU, VM или Cortex.

## CognitiveState

Committed versioned shared-state surface между модулями. Не полный Agent state и не mutable bus.

## Agent Snapshot

Полный causally relevant снимок Agent: shared/private state, Memory, parameters, RNG и другие stateful mechanisms.

## Cognitive Scheduler

Agent-owned механизм declared scheduling/waves/commits. Не cognitive module.

## Agent revision

Версия behavior-relevant composition/parameters Agent.

---

# Environment / Perception

## Raw Observation

Agent-visible Environment observation до Perception normalization.

## Canonical Percept

Стабильное internal representation текущего observation.

## Semantic Core

Структурированная interpretable часть Canonical Percept.

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

Результат явного Memory retrieval event.

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

# Intrinsic Signals

## Intrinsic Signal

Typed нейтральное измерение свойства опыта. Не Reward/Drive/Utility автоматически.

## Novelty

Новизна относительно explicit history/representation/reference scope.

## Predictive surprisal

Информационная неожиданность относительно meaningful predictive probability.

## Information gain

Изменение meaningful knowledge/belief state между before/after.

---

# Drives

## Drive System

Owner committed `DriveStateSet` persistent typed regulatory states.

## Drive State

Текущее persistent regulatory состояние конкретного Drive.

## Drive Pressure

Производная интенсивность regulation в semantics конкретного Drive; не общая валюта и не Utility.

## Homeostatic Drive

Drive с meaningful regulated variable и target/range.

## Adaptive Motivational Drive

Persistent Drive без обязательного homeostatic set-point.

---

# Appraisal

## Appraisal System

Event-level subsystem оценки значения causally identifiable target относительно current committed Agent context.

## Appraisal Target

Событие/outcome/prediction/imagined/retrieved event или другой причинно идентифицируемый объект оценки.

## Appraisal Context

Versioned declared context оценки: Goals, Drives, World/Self evidence, explicit Memory retrieval, Intrinsic Signals и при необходимости previous committed Affect.

## AppraisalRecord

Versioned результат конкретного appraisal computation с target/context/provenance.

## AppraisalProfile

Typed multidimensional профиль оценки без mandatory emotion label/global scalar.

## Relevance

Связь target с текущими concerns Agent. Не Salience, novelty или Utility.

## Goal congruence

Отношение target к конкретной committed Goal.

## Drive conduciveness

Отношение target к regulation конкретного Drive; не committed Drive update.

## Expectedness

Согласованность target с prior expectations; не novelty/surprisal/error.

## Controllability

Насколько развитие ситуации чувствительно к доступным действиям Agent.

## Coping potential

Насколько текущий Agent способен эффективно изменить, выдержать или обойти последствия.

## Urgency

Temporal pressure потенциальной реакции; не Salience/action priority/Utility.

## Reappraisal

Новый AppraisalRecord при новом context; не mutation исторического record.

---

# Affect

## Affect System

Persistent history-dependent subsystem, интегрирующий eligible Appraisal Records во времени.

## Affect State

Текущее persistent состояние Affect. Не emotion label, Drive State или Utility.

## AffectStateSet

Committed набор typed Affect channel states с собственной revision.

## Affect Channel

Typed компонент Affect с собственной state/dynamics/source semantics.

## Affect Dynamics

Versioned update `Affect_t + Appraisal(s) + logical time → Affect_(t+1)`.

## AffectView

Derived representation AffectStateSet, например valence-arousal view. Не source of truth.

## Anticipatory Affect

Current Affect update от explicit predicted Appraisal source; prediction не становится фактом.

## Simulated Affect

Branch-local Affect в imagination/counterfactual path; не real committed Affect.

## NoAffect

Конфигурация отсутствующей Affect capability, не fake zero/neutral state.

---

# Valuation

## Valuation System

Decision-relevant subsystem, строящий typed `ValueProfile` и explicit comparison разнородных concerns. Не Policy и не Training Reward generator по умолчанию.

## Valuation Target

State/outcome/action candidate/trajectory/counterfactual branch, относительно которого строится valuation с explicit causal provenance/horizon.

## ValueComponent

Typed decision-relevant contribution конкретной semantics. Не обязана иметь общие units с другими components.

## ValueProfile

Structured multi-objective representation ценности target до обязательной scalarization.

## FeasibilityProfile

Self-related evidence о возможности/стоимости выполнения target. `P(success)`/effort не являются Utility автоматически.

## ConstraintProfile

Explicit representation constraints/thresholds/violation evidence.

## RiskProfile

Decision-relevant downside profile на основе outcome distribution/adverse semantics/explicit risk measure. Не predictive uncertainty.

## ComparisonPolicy

Versioned rule сравнения `ValueProfile`: scalar, dominance/Pareto, lexicographic, constraint-first, nonlinear или learned semantics.

## ComparisonResult

Результат сравнения profiles: preference/order/dominance/tie/incomparability/constraint status и optional scalarized view.

## ScalarizedValue

Derived scalar из `ValueProfile` под конкретной `ComparisonPolicy`. Не universal currency и не Training Reward автоматически.

## Incomparable

Валидный multi-objective result, когда explicit policy не даёт полного ordering. Не technical failure.

---

# Salience / Attention

## Salience System

Agent-owned subsystem, строящий purpose-dependent priority profiles для explicit candidates и распределяющий заданный consumer/context budget через versioned `AllocationPolicy`.

## Salience Target

Causally identifiable semantic object, которому может назначаться processing priority: percept/event, Goal, Memory candidate, World hypothesis, ValueProfile, plan/action candidate и т. п.

## SalienceCandidateSet

Explicit набор targets для конкретного purpose/base revision. Salience не сканирует весь Agent state ambient способом.

## Salience Purpose

Контекст того, **для какого вида processing** строится priority, например Workspace admission hint, Memory regulation hint или planning inspection. Exact enum не frozen.

## Salience Evidence

Typed evidence, влияющее на processing priority: novelty, relevance, urgency, risk, value, uncertainty, Drive/Affect context и другие разрешённые sources. Не общая числовая валюта автоматически.

## SalienceProfile

Structured purpose-dependent representation причин priority target. Не обязан быть одним scalar.

## AttentionBudget

Explicit ограничение ресурса, предоставляемое consumer/context. Salience не владеет global compute budget.

## AllocationPolicy

Versioned policy преобразования `SalienceProfile[] + AttentionBudget` в конкретный ranking/gating/allocation.

## AttentionAllocation

Результат распределения budget между candidates. Сам по себе не выполняет Workspace admission, Cortex invocation, retrieval или Action Commit.

## Ranking

Относительный порядок candidates.

## Gating

Решение, проходит ли candidate дальше в рамках allocation policy.

## Inhibition of return

Optional stateful mechanism временного снижения priority недавно выбранного target; candidate для Salience dynamics, не обязательная реализация.

## NoSalience

Конфигурация отсутствующей Salience capability. Не fake `salience=0` для всех targets.

---

# Будущие области

## Memory Regulation / Consolidation

Будущая admission/retention/forgetting/replay/consolidation semantics поверх Memory Core. `DU-20`.

## Workspace

Кандидат на temporary limited global-access surface. `DU-21`.

## Executive Control

Будущая regulation cognitive process; не Cognitive Scheduler. `DU-22`.

## Policy / Planner

Будущая boundary выбора/планирования поведения. `DU-23`.

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
