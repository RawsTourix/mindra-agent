# Глоссарий MINDRA

## Назначение

Короткие рабочие определения устойчивых терминов MINDRA после `DU-32`.

При конфликте приоритет имеют accepted ADR, специализированный canonical design, [`contract-adr-consistency-freeze.md`](contract-adr-consistency-freeze.md) и version-specific design текущего milestone.

Exact Python/API names могут отличаться; здесь фиксируется смысл.

---

# Semantic Freeze / roadmap / governance

## Semantic Freeze Baseline F31

Согласованный semantic baseline `DU-01 … DU-30`, принятый `DU-31`. Замораживает ownership/lifecycle/source/provenance/causal meaning, но не exact Python API/algorithm.

## Semantic-frozen contract

Machine-facing contract, смысл которого нельзя менять в version implementation без нового ADR.

## Breaking Semantic Change

Изменение owner, source-of-truth, visibility, causal ordering, lifecycle или другой frozen semantics. После F31 требует нового ADR и новой freeze baseline revision.

## Deferred Implementation Choice

Framework/API/algorithm/storage/default, который version specification может выбрать без изменения F31 semantics.

## Version Roadmap

Принятая `DU-32` последовательность software milestones `v0.1 … v1.0`. Определяет implementation sequencing, но не переопределяет F31.

## Software Milestone

Вертикально запускаемый и проверяемый version scope с explicit acceptance gate и non-goals.

## Version Design

Подробная specification конкретного milestone: selected stack, exact representations, implementations, config, VerificationObligations и acceptance criteria.

## Implementation Sequence

Dependency-ordered набор reviewable шагов Codex для уже принятого Version Design. Не место выбора архитектуры.

## Reference Composition

Явный composition profile конкретной версии, используемый как воспроизводимый implementation/evaluation reference.

## Compute Profile

Version-level planning class доступного compute (`C0…C3` в DU-32). Не cognitive resource и не architecture identity.

---

# Система и execution

## MINDRA Agent

Логическая agent-owned когнитивная система. Не равна process/GPU/VM/Cortex.

## CognitiveState

Committed versioned shared-state surface между модулями. Не полный Agent state, mutable bus или Workspace.

## Agent Snapshot

Логический causally relevant снимок Agent для clone/restore. Не persistent Checkpoint.

## Checkpoint

Persistent manifest-driven набор verified artifacts относительно explicit causal capture boundary/scope.

## AgentRevision

Версия behavior-relevant composition/parameters Agent.

## CandidateRevisionBundle

Staged набор новых component/Agent revisions после training, но до activation.

## RevisionActivationRecord

Causal запись перевода compatible revision bundle в active Agent revision.

## Cognitive Scheduler

Runtime-core механизм DAG/waves/read-write validation/atomic commits. Не cognitive module, Executive Control или Policy.

## Decision Window

Логический интервал от agent-visible observation/outcome до следующего `Action Commit`.

## Cognitive Cycle

Одна причинно различимая внутренняя итерация cognition.

## Runtime State Update

Изменение ordinary agent runtime/adaptive state без optimizer semantics.

## Learning Update

Явное parameter/model-fitting изменение через внешний Training Runtime.

---

# Availability / status semantics

## available

Применимое актуальное значение существует.

## unknown

Значение применимо, но Agent/система его не знает или не оценила. Не ошибка и не `false`.

## stale

Значение существует, но validity horizon не покрывает текущий causal context.

## unavailable

Capability/value намеренно недоступны или неприменимы в текущей composition/phase.

## missing

Required structural contract element отсутствует. Обычно contract/configuration error.

## execution_unknown

Неизвестно, был ли dispatched external action применён. Не синоним epistemic `unknown` и не эквивалент `not_executed`.

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

## Memory Core

Owner canonical Memory Store/record identity/structural validation/retrieval/representation/index/commit. Не owner policy admission после DU-20.

## Memory Regulation

Policy responsibility admission/retention/forgetting/eviction/replay/consolidation поверх Memory Core. Не второй owner Store.

## MemoryRecord

Каноническое agent-owned воспоминание со stable identity/provenance; не embedding/index slot.

## RetrievalResult

Результат явного query-driven Memory retrieval event.

## Memory Replay / Reactivation

Agent-owned повторная активация существующего `MemoryRecord`. Не Training Replay и не новый natural experience.

## Consolidation Event

Causal memory derivation/maintenance event. Не optimizer `Learning Update`.

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

# Intrinsic / Motivation / Appraisal / Value

## Intrinsic Signal

Typed нейтральное измерение свойства опыта. Не Reward/Drive/Utility автоматически.

## Drive State

Persistent regulatory/motivational состояние конкретного Drive.

## AppraisalRecord

Versioned оценка identifiable target относительно current Agent context.

## Affect State

Persistent history-dependent modulation state. Не emotion label, Drive State или Utility.

## ValueProfile

Structured multi-objective representation decision-relevant ценности target до optional scalarization/comparison policy.

## SalienceProfile

Structured representation причин processing priority target. Не AttentionAllocation.

## AttentionAllocation

Результат allocation конкретного AttentionBudget между explicit candidates. Не фактическое исполнение consumer operation.

---

# Workspace / Executive

## Workspace

Bounded temporary shared-access/broadcast capability для dynamically admitted subset информации. Не `CognitiveState`, Memory или Cortex context.

## WorkspaceItem

Admitted source-preserving item Workspace. Admission не повышает factual authority источника.

## Executive Control

Agent-owned control optional internal operations/resources и continue/yield cognition. Не Scheduler и не Policy/Planner.

## Internal MetaAction

Решение разрешить/инициировать внутреннюю cognitive operation. Не Environment Action.

## CognitiveResourceEnvelope

Предоставленный Executive hard/soft envelope agent-visible cognitive resources. Не infrastructure ComputeManifest.

---

# Policy / Action

## Planner

Optional/falsifiable provider multi-step/contingent plans и action candidates. Не final selection owner.

## Policy System

Owner final behavioral selection до Action Boundary.

## ActionCandidate

Предложение behavior с source/provenance. Ещё не выбрано Policy.

## SelectedActionIntent

Выбранное Policy behavioral intention до Action Boundary.

## AuthorizedAction

Final semantic action после authorization, до `Action Commit`.

## Action Commit

Необратимая causal boundary final authorized Environment action после authorization и до dispatch.

## ActionCommitRecord

Immutable evidence committed action с intent/authorization/revision/dispatch lineage.

## DispatchAttempt

Одна transport/adapter попытка отправить уже committed action. Retry того же logical dispatch не создаёт новый Action Commit.

---

# Experience / Data / Replay

## ExperienceEvent

Immutable по смыслу typed causal data event со stable identity, logical scope, causal parents, revisions, visibility и provenance.

## Experience Journal

Append-only logical collection `ExperienceEvent`, source of truth записанного опыта. Не Agent runtime state, Memory или Replay Buffer.

## CausalRevisionSet

Bundle behavior-relevant Agent/component/environment/representation revisions causal event.

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

## Privileged supervision

Training condition, явно разрешающая evaluator/research-only data.

---

# Training Lifecycle

## Training Runtime

Внешняя optimization responsibility, создающая candidate trainable revisions. Не cognitive module.

## TrainingPlan

Versioned training condition: targets, pinned base revisions, data, objectives, gradient/optimizer, validation и activation semantics.

## Training Objective

Внешняя optimization semantics. Не Agent Goal, Drive, Intrinsic Signal или ValueProfile.

## GradientFlowPolicy

Versioned правила trainable groups, cross-component gradient edges и stop-gradient boundaries.

## BaseRevisionBundle

Pinned revisions, от которых начинается TrainingAttempt.

## LearningUpdateRecord

Immutable evidence training update; не automatic activation.

## Behavior revision

Revision, реально породившая source action/trajectory.

## Learner revision

Revision, относительно которой Trainer вычисляет update/target.

## Rollback

Новая causal activation предыдущего/исправленного revision bundle. Не rewrite истории.

---

# Checkpoint / Reproducibility / Compute

## CheckpointScope

Intended use и required/optional state classes checkpoint.

## CheckpointManifest

Committed descriptor checkpoint после verification обязательных artifacts.

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

## EvaluationCondition

Полностью определённое условие evaluation.

## EvaluationUnit

Единица measurement; не автоматически independent statistical sample.

## ReplicateStructure

Структура training/checkpoint/world/episode/counterfactual replicates и nesting assumptions.

## StatisticalAnalysisPlan

Versioned analysis semantics: unit, contrast, estimator/interval family, nesting, missing/censoring и stopping policy.

## Matched control

Control с сопоставимыми заявленными confounders, но иной целевой semantics.

## PairedCounterfactualPlan

План control/treatment branching из общего verified base state.

## ModuleGateSpec

Support/weakening/falsification criteria условно принятой module boundary.

---

# Engineering Testing

## Engineering Verification Plane

Внешняя responsibility проверки implementation contracts/invariants/failure semantics. Не MINDRA-Eval.

## VerificationObligation

Versioned обязанность проверить конкретный frozen engineering invariant.

## VerificationMatrix

Связь design/ADR/contracts с obligations, test specs, CI tiers и latest evidence.

## ContractConformanceProfile

Capability-aware профиль conformance concrete real/Dummy/control implementation semantic contract.

## FaultInjectionSpec

Declared fault, injection point и ожидаемые failure/recovery semantics.

## VerificationGate

Required obligations/evidence для change/merge scope. Skip/not-run не становятся pass.

---

# Research Claims / Limitations

## ObservationRecord

Фиксация непосредственно полученного valid research evidence без усиленной интерпретации.

## InterpretationRecord

Versioned объяснение/смысл evidence с assumptions, competing explanations и scope.

## ResearchClaim

Versioned scoped утверждение, которое проект готов защищать на основании evidence.

## ClaimScope

Явная область применимости ResearchClaim. Отсутствующий dimension не означает universal scope.

## LimitationRecord

Versioned first-class ограничение claim/study/version/project.

## KnownUnknownRecord

Явно зарегистрированный нерешённый вопрос. `unknown ≠ false`.

## UnsupportedClaimPattern

Необоснованный inference leap, например `Workspace → consciousness proof`.

## ClaimRegistry

Versioned registry active/challenged/superseded/unsupported claims и review lineage.

## Functional similarity

Сходство вычислительной/причинной функции. Не означает biological или phenomenological equivalence.

## Phenomenological claim

Утверждение о subjective experience/conscious feeling. Текущая MINDRA architecture сама по себе не предоставляет достаточного bridge evidence.

---

# Research terms

## Baseline

Сравнительная конфигурация.

## Ablation

Отключение/замена subsystem для измерения вклада.

## Control

Конфигурация для исключения альтернативного объяснения эффекта.

## Research evidence

Воспроизводимый результат с conditions/limitations; не automatic design change.

## Engineering evidence

Результат contract/invariant/failure verification implementation; не evidence функциональной полезности.

---

# Текущий этап

Общий architecture/roadmap cycle завершён:

```text
DU-00 … DU-32 complete
```

Следующая разрешённая работа:

```text
Version Design — v0.1 Core Kernel
```

Roadmap конкретизирует implementation milestones, но не переопределяет F31 без нового ADR.
