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

Логический causally relevant снимок Agent для clone/restore. Не persistent Checkpoint.

## Agent revision

Версия behavior-relevant composition/parameters Agent.

## Cognitive Scheduler

Механизм declared scheduling/waves/commits. Не cognitive module, Executive Control или Policy.

## Decision Window

Логический интервал от agent-visible observation/outcome до следующего `Action Commit`.

## Cognitive Cycle

Одна причинно различимая внутренняя итерация cognition.

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

Цель, принятая Goal System.

## Cortex

Заменяемая semantic/language/reasoning capability; не вся MINDRA и не central orchestrator.

## MemoryRecord

Каноническое agent-owned воспоминание со stable identity/provenance; не embedding/index slot.

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

Versioned оценка identifiable target относительно current Agent context.

## Affect State

Persistent history-dependent modulation state. Не emotion label, Drive State или Utility.

## ValueProfile

Structured multi-objective representation decision-relevant ценности target до обязательной scalarization.

## SalienceProfile

Structured representation причин processing priority target. Не AttentionAllocation.

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

Optional/falsifiable provider multi-step/contingent plans и action candidates. Не final selection owner.

## ActionCandidate

Предложение behavior с source/provenance. Ещё не выбрано Policy.

## SelectedActionIntent

Выбранное Policy behavioral intention до Action Boundary.

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

Отдельная evaluator/research-only annotation. Не обычный agent-visible payload.

## DataVisibilityPolicy

Versioned правила включения visibility/trust classes в derived dataset/training condition.

## DatasetManifest

Versioned описание source journals/projections, schemas, transforms, splits, revisions и quality data product.

## TrainingSample

Derived training data product со source refs и transformation lineage. Не historical source experience.

## Training Replay

Повторное использование training data внешним Training Runtime. Не Agent Memory Replay.

## ReplaySelectionRecord

Evidence конкретного training replay selection.

## Privileged supervision

Training condition, явно разрешающая evaluator/research-only data.

---

# Training Lifecycle

## Training Runtime

Внешняя optimization responsibility, создающая candidate trainable revisions. Не cognitive module.

## Runtime State Update

Изменение ordinary agent runtime/adaptive state без optimizer semantics.

## Learning Update

Явное parameter/model-fitting изменение через Training Runtime.

## TrainingPlan

Versioned training condition: targets, pinned base revisions, data, objectives, gradient/optimizer, validation и activation semantics.

## Training Objective

Внешняя optimization semantics. Не Agent Goal, Drive, Intrinsic Signal или ValueProfile.

## GradientFlowPolicy

Versioned правила trainable groups, cross-component gradient edges и stop-gradient boundaries.

## BaseRevisionBundle

Pinned revisions, от которых начинается TrainingAttempt.

## CandidateRevisionBundle

Staged набор новых revisions после optimization, но до activation.

## LearningUpdateRecord

Immutable evidence training update; не automatic activation.

## RevisionActivationRecord

Causal запись перевода compatible revision bundle в active Agent revision.

## Behavior revision

Revision, реально породившая source action/trajectory.

## Learner revision

Revision, относительно которой Trainer вычисляет update/target.

## Rollback

Новая causal activation предыдущего/исправленного revision bundle. Не rewrite истории.

---

# Checkpoint / Reproducibility / Compute

## Checkpoint

Persistent manifest-driven набор verified artifacts относительно explicit causal capture boundary и scope.

## CheckpointScope

Intended use и required/optional state classes checkpoint.

## CheckpointManifest

Committed descriptor checkpoint после verification обязательных artifacts.

## TrainingResumeCheckpoint

Checkpoint scope с training state для заявленного continuation.

## FullSystemCheckpoint

Checkpoint scope с causally aligned Agent + Environment/runtime state.

## CaptureBoundary

Committed causal cut, относительно которого pin'ятся revisions/state при capture.

## ArtifactRef

Stable logical/content/integrity identity artifact, отделённая от physical path.

## RestoreProfile

Versioned requested restore semantics: exact/compatible/portable/approximate.

## ReproducibilityClaim

Scoped evidence-backed утверждение о воспроизводимости. Не boolean.

## DeterminismPolicy

Versioned framework/runtime/precision/parallelism условия deterministic claim.

## ComputeManifest

Infrastructure/research описание allocated compute context. Не `CognitiveResourceEnvelope`.

## ComputeUsageRecord

Evidence фактически/оценочно/provider-reported использованного compute.

## ExperimentManifest

Versioned reproducible run condition, связывающий code/config/checkpoints/Environment/data/software/hardware/compute/results.

---

# Evaluation

## MINDRA-Eval

Внешний Evaluation Plane для task/diagnostic/causal/calibration/resource/reproducibility evidence. Не engineering test suite.

## EvaluationStudyPlan

Versioned план исследования: hypotheses, conditions, controls, metrics, replicates/statistics и success/falsification criteria.

## EvaluationSuite

Versioned набор task/world distributions и measurement protocols.

## EvaluationCondition

Полностью определённое условие evaluation.

## EvaluationRun

Один причинно идентифицируемый запуск конкретной condition.

## EvaluationUnit

Единица measurement; не автоматически independent statistical sample.

## ReplicateStructure

Структура training/checkpoint/world/episode/counterfactual replicates и nesting assumptions.

## MetricSpec

Versioned semantics evaluator metric.

## StatisticalAnalysisPlan

Versioned analysis semantics: unit, contrast, estimator/interval family, nesting, missing/censoring и stopping policy.

## ControlDescriptor

Описание baseline/ablation/No*/Dummy/random/shuffled/matched/oracle condition.

## ResourceMatchProfile

Описание confounders/resources, которые должны быть matched между conditions.

## PairedCounterfactualPlan

План control/treatment branching из общего verified base state.

## CausalContrastRecord

Evidence control/treatment effect с assumptions/limitations.

## ModuleGateSpec

Support/weakening/falsification criteria условно принятой module boundary.

## EvaluationValidityRecord

Статус protocol/leakage/checkpoint/condition validity. Invalid run не равен failed task.

## EvaluationReport

Derived report с lineage до raw evidence. Не source of truth сам по себе.

---

# Engineering Testing

## Engineering Verification Plane

Внешняя responsibility проверки implementation contracts/invariants/failure semantics. Не MINDRA-Eval.

## VerificationObligation

Versioned обязанность проверить конкретный accepted engineering invariant, включая допустимый enforcement/test class и automation status.

## VerificationMatrix

Связь accepted design/ADR/contracts с obligations, test specs, CI tiers и latest evidence.

## EngineeringTestSpec

Versioned semantics конкретной engineering проверки: target, class, composition/environment, oracle, faults и assertion semantics.

## ContractConformanceProfile

Capability-aware профиль conformance конкретной real/Dummy/control implementation semantic contract.

## FaultInjectionSpec

Declared fault, injection point и ожидаемые failure/recovery semantics.

## StatefulModelSpec

Упрощённая reference-state model с operations/transitions/invariants для generated sequence testing.

## TestOracleSpec

Test-only expected/invariant source. Privileged oracle не становится Agent-visible input.

## EngineeringTestEnvironmentProfile

Software/hardware/backend/determinism/resource/fault context engineering run.

## VerificationEvidenceRecord

Evidence того, какие obligations проверены в каком environment/capability scope.

## VerificationGate

Набор required obligations/evidence для change/merge scope. Skip/not-run не становятся pass.

## CoverageProfile

Раздельное описание code, contract, invariant, failure-mode, schema/migration и backend-capability coverage.

## FlakyTestRecord

Evidence nondeterministic pass/fail behavior и quarantine/repair state. Quarantine не равна verification pass.

## GoldenArtifactSpec

Reviewable deterministic reference artifact для stable contract surface; не universal neural-output oracle.

---

# Будущие области

## Research Claims / Limitations

Будущая boundary допустимых утверждений, evidence strength, limitations, known unknowns и антропоморфных ограничений. `DU-30`.

---

# Research terms

## Baseline

Сравнительная конфигурация.

## Ablation

Отключение/замена subsystem для измерения его вклада.

## Control

Конфигурация для исключения альтернативного объяснения эффекта.

## Matched control

Control с сопоставимыми заявленными confounders, но иной целевой semantics.

## Research evidence

Воспроизводимый результат с conditions/limitations; не automatic design change.

## Engineering evidence

Результат contract/invariant/failure verification конкретной implementation/revision; не evidence функциональной полезности.
