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

Каноническое воспоминание со stable identity и provenance; не embedding/index slot.

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

Событие, outcome, prediction, imagined/retrieved event или другой причинно идентифицируемый объект оценки.

## Appraisal Context

Versioned declared context оценки: Goals, Drives, World/Self evidence, explicit Memory retrieval, Intrinsic Signals и, после `DU-17`, при необходимости previous committed Affect.

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

## Affect baseline

Optional baseline/recovery state implementation; не обязан означать «нейтральную эмоцию».

## AffectView

Derived representation AffectStateSet, например valence-arousal view. Не source of truth.

## Anticipatory Affect

Current Affect update от explicit predicted Appraisal source; prediction не становится фактом.

## Simulated Affect

Branch-local Affect в imagination/counterfactual path; не real committed Affect.

## NoAffect

Конфигурация отсутствующей Affect capability, не fake zero/neutral state.

---

# Будущие области

## Valuation

Будущая decision-relevant система ценности. Точная semantics — `DU-18`.

## Salience

Будущая priority ограниченного cognitive processing. `DU-19`.

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
