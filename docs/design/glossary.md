# Глоссарий MINDRA

## Назначение

Короткие рабочие определения устойчивых терминов MINDRA. При конфликте приоритет имеют accepted ADR и специализированный canonical design.

---

# Система и execution

## MINDRA Agent

Логическая agent-owned когнитивная система. Не равна process/GPU/VM/Cortex.

## CognitiveState

Committed versioned shared-state surface между модулями. Не полный Agent state, mutable bus или Workspace.

## Agent Snapshot

Логический causally relevant снимок самого Agent для clone/restore. Не persistent Checkpoint и не ExperimentManifest.

## Agent revision

Версия behavior-relevant composition/parameters Agent.

## Cognitive Scheduler

Agent-owned механизм declared scheduling/waves/commits. Не cognitive module, Executive Control или Policy.

## Decision Window

Логический интервал от agent-visible observation/outcome до следующего `Action Commit`.

## Cognitive Cycle

Одна причинно различимая внутренняя итерация cognition внутри Decision Window.

---

# Environment / Perception

## Raw Observation

Agent-visible Environment observation до Perception normalization.

## Canonical Percept

Стабильное internal representation текущего observation.

## Feature View

Optional derived representation с explicit feature-space/encoder revision.

## Hidden World State

Privileged Environment state, недоступный Agent normal runtime способом.

## World Manifest

Versioned identity/configuration world instance/family сверх одного seed.

---

# Goals / Cortex / Memory

## Goal Proposal

Кандидат на цель; ещё не committed Goal.

## Committed Goal

Цель, принятая Goal System и существующая в Goal Graph.

## Cortex

Заменяемая semantic/language/reasoning capability; не вся MINDRA и не central orchestrator.

## MemoryRecord

Каноническое agent-owned воспоминание со stable identity/provenance; не embedding/index slot или research trajectory.

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

# Intrinsic / Motivation / Appraisal

## Intrinsic Signal

Typed нейтральное измерение свойства опыта. Не Reward/Drive/Utility автоматически.

## Drive State

Persistent regulatory состояние конкретного Drive.

## AppraisalRecord

Versioned оценка causally identifiable target относительно current Agent context.

## Affect State

Persistent history-dependent modulation state. Не emotion label, Drive State или Utility.

## ValueProfile

Structured multi-objective representation decision-relevant ценности target до обязательной scalarization.

## SalienceProfile

Structured representation причин processing priority target. Не обязан быть scalar и не равен AttentionAllocation.

---

# Memory Regulation / Workspace / Executive

## Memory Regulation

Policy responsibility поверх Memory Core для admission/retention/forgetting/eviction/replay/consolidation. Не второй owner Store.

## Memory Replay / Reactivation

Agent-owned re-presentation `MemoryRecord`. Не Training Replay и не новый natural experience.

## Consolidation Event

Causal событие memory derivation/maintenance. Не Learning Update.

## Workspace

Bounded temporary shared-access/broadcast capability для dynamically admitted subset информации. Не `CognitiveState`, Memory или Cortex context.

## Executive Control

Agent-owned control optional internal operations/resources и continue/yield cognition. Не Scheduler и не Policy/Planner.

## Internal MetaAction

Решение разрешить/инициировать внутреннюю cognitive operation. Не Environment Action.

---

# Policy / Action

## Policy System

Обязательный owner финального behavioral selection до Action Boundary.

## Planner

Optional/falsifiable provider multi-step/contingent plans и action candidates. Не World Model и не final selection owner.

## ActionCandidate

Предложение behavior с source/provenance. Ещё не выбрано Policy.

## SelectedActionIntent

Выбранное Policy behavioral intention до Action Boundary. Не authorized/committed/dispatched/executed action.

## AuthorizedAction

Final semantic action после успешной authorization, до `Action Commit`.

## Action Commit

Необратимая causal boundary final authorized Environment action после authorization и до dispatch.

## ActionCommitRecord

Immutable evidence committed action с intent/authorization/revision/dispatch lineage.

## DispatchAttempt

Одна transport/adapter попытка отправить уже committed action. Retry того же logical dispatch не создаёт новый Action Commit.

## execution_unknown

Неизвестно, был ли dispatched action применён. Не эквивалентно `not_executed`.

---

# Experience / Data / Replay

## Experience Data Plane

Внешняя относительно cognition responsibility записи causal experience, построения datasets и Training Replay inputs.

## ExperienceEvent

Immutable по смыслу typed causal data event со stable identity, logical scope, causal parents, revisions, visibility и provenance.

## Experience Journal

Append-only logical collection `ExperienceEvent`, source of truth записанного опыта. Не Agent runtime state, Memory или Replay Buffer.

## CausalRevisionSet

Bundle behavior-relevant Agent/component/environment/representation revisions конкретного causal event.

## ResearchAnnotationRecord

Отдельная evaluator/research-only annotation, ссылающаяся на source events/samples. Не обычный agent-visible payload.

## DataVisibilityPolicy

Versioned правила включения visibility/trust classes в derived dataset/training condition.

## DatasetManifest

Versioned описание source journals/projections, schemas, transforms, splits, revisions, quality и determinism data product.

## TrainingSample

Derived training data product со source refs и transformation lineage. Не historical source experience.

## Training Replay

Повторное использование source/derived training data внешним Training Runtime. Не Agent Memory Replay.

## ReplaySelectionRecord

Evidence конкретного training replay selection: population/sampler revision, selected refs, probability/priority/RNG metadata где применимо.

## Privileged supervision

Training condition, явно разрешающая ResearchAnnotation/evaluator-only data. Не natural agent-visible learning по умолчанию.

---

# Training Lifecycle

## Training Runtime

Внешняя относительно cognition optimization responsibility, потребляющая TrainingSample/Replay data и создающая candidate trainable revisions. Не cognitive module.

## Runtime State Update

Изменение ordinary agent runtime/adaptive state без optimizer semantics. Не Learning Update.

## Learning Update

Явное parameter/model-fitting изменение trainable state через Training Runtime. Не Runtime State Update, Consolidation Event или Replay Step.

## TrainableComponentDescriptor

Semantic descriptor того, какие parameter groups/capabilities компонента могут обучаться и при каких compatibility/activation constraints.

## TrainingPlan

Versioned training condition: targets, pinned base revisions, data/visibility, objectives, optimizer/gradient policy, validation, activation, retention и determinism.

## Training Objective

Внешняя optimization semantics, определяющая training targets/losses. Не Agent Goal, Drive, Intrinsic Signal или ValueProfile.

## GradientFlowPolicy

Versioned правила trainable parameter groups, cross-component gradient edges, stop-gradient boundaries и joint-update atomicity. Runtime dependency graph её не заменяет.

## OptimizerStateLineage

Training-only lineage optimizer/scheduler/scaler state относительно parameter topology/revisions. Не `CognitiveState`.

## BaseRevisionBundle

Pinned Agent/component/representation revisions, от которых начинается TrainingAttempt.

## CandidateRevisionBundle

Совместимый staged набор новых component revisions после optimization, но до activation live Agent.

## LearningUpdateRecord

Immutable evidence завершённого/принятого training update: source data, base revisions, objective/optimizer policies, candidate revisions, validation и provenance. Не automatic activation.

## RevisionActivationRecord

Causal запись перевода совместимого revision bundle в active Agent revision на разрешённой boundary.

## Behavior revision

Agent/Policy revision, которая реально породила source action/trajectory.

## Learner revision

Revision, относительно которой Training Runtime вычисляет текущий update/target. Может отличаться от behavior revision.

## Representation effect

Изменение feature/representation space после Learning Update, требующее новой revision и downstream compatibility/migration semantics.

## Rollback

Новая causal activation предыдущего/исправленного compatible revision bundle после обнаружения проблемы. Не rewrite истории Learning Update.

---

# Checkpoint / Reproducibility / Compute

## Checkpoint

Persistent manifest-driven набор verified artifacts, относящийся к explicit causal capture boundary и объявленному scope. Не синоним одного tensor file.

## CheckpointScope

Явное описание intended use и required/optional state classes checkpoint: например inference, exact agent state, training resume или full-system resume.

## CheckpointManifest

Committed descriptor checkpoint: capture boundary, revisions, artifacts, integrity, Environment/Training refs, compatibility и reproducibility metadata. Коммитится после verification обязательных artifacts.

## TrainingResumeCheckpoint

Checkpoint scope с causally relevant optimizer/scheduler/scaler/trainer/replay/data-cursor/RNG state для заявленного продолжения Training Lifecycle.

## FullSystemCheckpoint

Checkpoint scope, включающий согласованный Agent + Environment/runtime state для заявленного continuation/counterfactual restore.

## CaptureBoundary

Explicit committed causal cut, относительно которого pin'ятся revisions/state при создании checkpoint.

## ArtifactRef

Stable logical/content/integrity identity checkpoint artifact, отделённая от physical path/storage location.

## RestoreProfile

Versioned semantics requested restore: exact/compatible/portable/approximate и соответствующие compatibility/state requirements.

## RestoreRecord

Evidence конкретной попытки restore: requested/actual profile, migrations, integrity/compatibility/invariant checks и результат.

## ReproducibilityClaim

Scoped утверждение о воспроизводимости с required environment constraints, comparison criterion, limitations и validation evidence. Не boolean `reproducible=true`.

## DeterminismPolicy

Versioned набор framework/runtime/precision/autotuning/parallelism условий, под которыми заявляется deterministic behavior.

## SoftwareEnvironmentManifest

Versioned identity code/runtime/framework/library/model/backend окружения experiment/restore.

## HardwareTopologyManifest

Versioned identity CPU/GPU/accelerator/topology ресурсов, релевантных reproducibility claim. Не agent-visible Self state автоматически.

## ComputeManifest

Research/infrastructure описание allocated compute context и способов измерения resource usage. Не `CognitiveResourceEnvelope`.

## ComputeUsageRecord

Evidence фактически/оценочно/provider-reported использованного compute с method/provenance.

## ExperimentManifest

Versioned reproducible run condition, связывающий code/config/checkpoints/Environment/data/software/hardware/compute/determinism/results. Не Agent state.

## Checkpoint migration

Explicit source→migration policy→new artifact/checkpoint lineage. Не silent rewrite старого checkpoint.

---

# Evaluation

## MINDRA-Eval

Внешний Evaluation Plane для task/diagnostic/causal/calibration/resource/reproducibility evidence. Не Agent cognition и не engineering test suite.

## EvaluationStudyPlan

Versioned план исследования: hypotheses, conditions, controls, metrics, replicate/statistical protocol и success/falsification criteria.

## EvaluationSuite

Versioned набор task/world distributions и measurement protocols. Не один Environment instance и не universal leaderboard.

## EvaluationCondition

Полностью определённое условие evaluation: Agent/checkpoint/world/Cortex/composition/interventions/data/resources/software/hardware/metrics context.

## EvaluationRun

Один причинно идентифицируемый запуск конкретной `EvaluationCondition`.

## EvaluationUnit

Семантическая единица measurement, например Episode, Decision Window, prediction resolution или paired branch. Не автоматически independent statistical sample.

## ReplicateStructure

Явная структура training/checkpoint/world/episode/stochastic/counterfactual replicates и их nesting/blocking/independence assumptions.

## MetricSpec

Versioned semantics evaluator metric: target, inputs, visibility, unit, aggregation, missing/censoring и provenance.

## EvaluationScorecard

Typed bundle task/calibration/causal/robustness/resource/reproducibility metrics. Не обязан сворачиваться в scalar.

## StatisticalAnalysisPlan

Versioned confirmatory analysis semantics: analysis unit, contrast, estimator/interval family, dependence/nesting, multiplicity, missing/censoring и stopping policy.

## ControlDescriptor

Описание baseline/ablation/No*/Dummy/random/shuffled/matched/oracle condition и факторов, которые сохраняются/изменяются.

## ResourceMatchProfile

Описание параметров/state/context/data/compute, которые должны быть matched между comparison conditions, и фактических deviations.

## PairedCounterfactualPlan

План control/treatment branching из общего verified checkpoint + Environment base state с explicit intervention и RNG-coupling semantics.

## CausalContrastRecord

Evidence control/treatment effect с base state, intervention, target/off-target effects, matching quality, uncertainty и causal limitations.

## ModuleGateSpec

Заранее определённые support/weakening/falsification criteria условно принятой module boundary.

## PolicyActionAttributionRecord

Связь pre-Gate `SelectedActionIntent` quality, Gate corrections/rejections и post-Gate execution/outcome metrics.

## EvaluationValidityRecord

Отдельный статус protocol validity/leakage/checkpoint/condition integrity. Invalid run не равен failed task.

## EvaluationManifest

Versioned manifest study/suite/conditions/controls/checkpoints/worlds/metrics/statistics/resources/reproducibility context.

## EvaluationReport

Derived report с lineage до raw runs/metrics/Evidence/Experience. Не source of truth сам по себе.

---

# Будущие области

## Engineering Testing

Будущая автоматическая проверка implementation contracts/invariants/failure semantics. `DU-29`.

---

# Research terms

## Baseline

Сравнительная конфигурация.

## Ablation

Отключение/замена subsystem для измерения его вклада.

## Control

Конфигурация для исключения альтернативного объяснения эффекта.

## Matched control

Control с сопоставимыми parameters/compute/state capacity или другими заявленными confounders, но иной целевой semantics.

## Research evidence

Фактический воспроизводимый результат с conditions/limitations; не automatic design change.
