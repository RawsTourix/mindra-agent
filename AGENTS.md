# AGENTS.md — правила работы с MINDRA

## Назначение

Этот файл — карта обязательного контекста для Codex, ChatGPT и других coding agents. Канонические знания проекта находятся в `docs/`.

## Язык

- документация и комментарии — на русском;
- technical identifiers/API/package/class/function/type names — на английском.

## Перед любой работой

1. Проверить repository status/HEAD.
2. Прочитать `docs/README.md` и `docs/design/current.md`.
3. Определить scope задачи.
4. Прочитать релевантный canonical design owner, accepted ADR и candidate contract.
5. Не выходить за разрешённый DU/version scope.

## Source of truth

```text
accepted ADR + canonical design
→ candidate/exact contracts
→ version specification
→ implementation sequence
→ implementation
→ engineering/research evidence
```

Research result меняет architecture только через design review/ADR.

## Фундамент

Перед subsystem/data/training/checkpoint changes обязательны:

- `docs/design/system-context.md`;
- `docs/design/dependency-rules.md`;
- `docs/design/execution-model.md`;
- `docs/design/cognitive-state.md`;
- `docs/design/module-lifecycle.md`;
- `docs/design/observability-and-intervention.md`.

## Принятые boundaries

| Область | Design | Contract | ADR |
|---|---|---|---|
| Environment | `docs/design/modules/environment.md` | `docs/design/contracts/environment.md` | `ADR-0007` |
| Perception | `docs/design/modules/perception.md` | `docs/design/contracts/perception.md` | `ADR-0008` |
| Goals | `docs/design/modules/goals.md` | `docs/design/contracts/goals.md` | `ADR-0009` |
| Cortex | `docs/design/modules/cortex.md` | `docs/design/contracts/cortex.md` | `ADR-0010` |
| Memory Core | `docs/design/modules/memory.md` | `docs/design/contracts/memory.md` | `ADR-0011` |
| World Model | `docs/design/modules/world-model.md` | `docs/design/contracts/world-model.md` | `ADR-0012` |
| Self Model | `docs/design/modules/self-model.md` | `docs/design/contracts/self-model.md` | `ADR-0013` |
| Intrinsic Signals | `docs/design/modules/intrinsic-signals.md` | `docs/design/contracts/intrinsic-signals.md` | `ADR-0014` |
| Drives | `docs/design/modules/drives.md` | `docs/design/contracts/drives.md` | `ADR-0015` |
| Appraisal | `docs/design/modules/appraisal.md` | `docs/design/contracts/appraisal.md` | `ADR-0016` |
| Affect | `docs/design/modules/affect.md` | `docs/design/contracts/affect.md` | `ADR-0017` |
| Valuation | `docs/design/modules/valuation.md` | `docs/design/contracts/valuation.md` | `ADR-0018` |
| Salience | `docs/design/modules/salience.md` | `docs/design/contracts/salience.md` | `ADR-0019` |
| Memory Regulation | `docs/design/modules/memory-regulation.md` | `docs/design/contracts/memory-regulation.md` | `ADR-0020` |
| Workspace | `docs/design/modules/workspace.md` | `docs/design/contracts/workspace.md` | `ADR-0021` |
| Executive Control | `docs/design/modules/executive-control.md` | `docs/design/contracts/executive-control.md` | `ADR-0022` |
| Policy / Planner | `docs/design/modules/policy-planner.md` | `docs/design/contracts/policy-planner.md` | `ADR-0023` |
| Action Boundary | `docs/design/modules/action-boundary.md` | `docs/design/contracts/action-boundary.md` | `ADR-0024` |
| Experience / Data / Replay | `docs/design/experience-data-replay.md` | `docs/design/contracts/experience-data-replay.md` | `ADR-0025` |
| Training Lifecycle | `docs/design/training-lifecycle.md` | `docs/design/contracts/training-lifecycle.md` | `ADR-0026` |
| Checkpoint / Reproducibility / Compute | `docs/design/checkpoint-reproducibility-compute.md` | `docs/design/contracts/checkpoint-reproducibility-compute.md` | `ADR-0027` |

Следующий разрешённый DU брать только из `docs/design/current.md`.

## Общие запреты

Без explicit design change запрещаются concrete peer coupling, runtime Service Locator, mutable global state bus, hidden mutation чужого state, Agent dependency на Training/Evaluation Runtime, hidden oracle input, ad-hoc scheduler order, partial causal commit, silent stale rebase и смешение natural/replayed/imagined/intervened/counterfactual provenance.

## Ключевые различия

```text
CognitiveState ≠ full Agent Snapshot
Goal Proposal ≠ Committed Goal
MemoryRecord ≠ embedding/index
World Prediction ≠ observed fact
Intrinsic Signal ≠ Reward/Drive/Value
Appraisal ≠ Affect ≠ Valuation
ValueProfile ≠ Training Objective ≠ Training Reward ≠ Policy Decision
SalienceProfile ≠ AttentionAllocation
Retrieval ≠ Agent Memory Replay ≠ Training Replay
Consolidation ≠ Learning Update
CognitiveState ≠ Workspace
Executive Control ≠ Cognitive Scheduler ≠ Policy
Policy ≠ Planner
Plan ≠ ImaginedTrajectory
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
TraceEvent ≠ ExperienceEvent
Experience Journal ≠ Agent runtime state
Source Experience ≠ TrainingSample
ResearchAnnotation ≠ agent-visible payload
Training Runtime ≠ cognitive module
Runtime State Update ≠ Learning Update
ReplaySelection ≠ Learning Update
runtime dependency graph ≠ gradient graph
optimizer/trainer state ≠ CognitiveState
CandidateRevisionBundle ≠ Active AgentRevision
LearningUpdateRecord ≠ RevisionActivationRecord
AgentSnapshot ≠ persistent Checkpoint
Checkpoint ≠ TrainingResumeCheckpoint ≠ ExperimentManifest
same seed ≠ same RNG state ≠ guaranteed same execution
semantic restore ≠ bitwise reproducibility
artifact identity ≠ physical path
ComputeManifest ≠ CognitiveResourceEnvelope
```

## Memory / Workspace / Executive safeguards

- Memory Regulation не владеет canonical Store;
- consolidation создаёт новый derived record и не выполняет optimizer update;
- Workspace не alias `CognitiveState`; producers работают через proposals;
- broadcast означает availability, а не callback/automatic invocation;
- Executive не Service Locator, не изменяет Scheduler graph и не выбирает Environment action;
- hard cognitive budget не увеличивается Executive самостоятельно.

## Policy / Action safeguards

- Policy — единственный normal-runtime owner `SelectedActionIntent`;
- Planner/Cortex/Valuation/World Model не создают final intent напрямую;
- Valuation evidence не превращается автоматически в `argmax` action;
- `SelectedActionIntent` не dispatch'ится напрямую;
- normal Action Gate не hidden Policy/Environment oracle;
- behavior-changing substitution имеет explicit override provenance;
- `Action Commit` после authorization и до dispatch;
- post-commit failure не отменяет commit;
- blind retry запрещён при `execution_unknown` без explicit dedup/idempotency evidence.

## Experience / Data / Replay safeguards

До пересмотра `DU-25`:

- source of truth записанного опыта — append-only causal `Experience Journal`, не replay buffer;
- event-sourced только data plane, не ordinary Agent runtime;
- source `ExperienceEvent` immutable по смыслу;
- hindsight/relabeling/re-encoding создают derived sample, не rewrite source history;
- evaluator-only Ground Truth хранится separate `ResearchAnnotationRecord`;
- privileged inclusion только через explicit `DataVisibilityPolicy`;
- `execution_unknown` не получает fake next state;
- mixed agent/component revisions не скрываются;
- `DatasetManifest` фиксирует source/schema/transforms/revisions/splits/quality/determinism;
- `TrainingSample` всегда derived и имеет source/transform lineage;
- ReplayItem eviction не удаляет source experience;
- Agent Memory Replay и Training Replay не смешивать;
- replay priority/sampling frequency не становится Salience/Memory importance/Valuation автоматически;
- storage technology не принимать как canonical до version design.

## Training Lifecycle safeguards

До пересмотра `DU-26`:

- `Training Runtime` не является cognitive module и не получает ambient mutable access к live Agent;
- ordinary module `compute()`/`observe_outcome()` не выполняет скрытый `optimizer.step()`;
- runtime/adaptive state, trainable parameters и optimizer/trainer state не смешиваются;
- optimizer/scheduler/scaler state не публикуется в `CognitiveState`;
- каждый `TrainingAttempt` pin'ит explicit `BaseRevisionBundle`;
- stale base revision не rebased молча;
- `TrainingPlan` явно указывает target components, data visibility, objectives, optimizer ownership и gradient policy;
- runtime dependency edge не создаёт gradient edge автоматически;
- cross-component backprop разрешён только через `GradientFlowPolicy`;
- shared parameter group не имеет конфликтующих независимых optimizer owners без coordination policy;
- Training Objective не считается Agent Goal/Value/Drive/Intrinsic Signal;
- external feedback/intrinsic/value становится training target/reward только через explicit mapping;
- source Dataset/Replay/TrainingSample provenance сохраняется до `LearningUpdateRecord`;
- behavior revision и learner revision не подменяются одной «current policy» revision;
- privileged `ResearchAnnotation` используется только при explicit privileged-supervision condition;
- `CandidateRevisionBundle` не является active Agent только потому, что training завершился;
- candidate проходит explicit validation/acceptance;
- activation новой Agent revision выполняется только на allowed causal boundary;
- in-flight Decision/Cognitive segment не меняет weights/revision задним числом;
- совместно обученные incompatible компоненты активируются атомарным compatible bundle;
- representation-breaking update не активируется без compatibility/migration semantics;
- update encoder/Cortex adapter требует новой representation/feature-space revision там, где меняется пространство;
- Self Model competence после change `agent_revision` не остаётся автоматически valid;
- new-task gain не считается training success без требуемых retention/regression checks;
- failed/rejected candidate не мутирует live Agent;
- rollback не удаляет historical LearningUpdate/Activation evidence;
- training loss/accuracy/KL/gradient norm/replay priority не становятся cognitive signals автоматически;
- concrete optimizer/PyTorch/LoRA/PPO/GRPO/SFT/etc. не превращать в architecture invariant до version design.

## Checkpoint / Reproducibility / Compute safeguards

До пересмотра `DU-27`:

- `AgentSnapshot` не считать persistent checkpoint или ExperimentManifest;
- weights-only artifact не называть full/training-resume checkpoint без required state;
- `seed` не использовать вместо current RNG states;
- одинаковый seed не является доказательством identical execution;
- final `CheckpointManifest` не commit'ить до verification обязательных artifacts;
- physical file path/URI не использовать как единственную artifact identity;
- content/integrity mismatch fail closed;
- active и candidate revisions сохранять раздельно; restore candidate не активирует её автоматически;
- `execution_unknown` не разрешает blind retry/naive branch после restore;
- full-system exact restore требует causally aligned Agent + Environment state;
- requested exact restore не downgraded молча до approximate/portable;
- migration создаёт новый explicit lineage и не переписывает source checkpoint;
- missing required delta/base checkpoint fail closed;
- optional artifact loss не masquerade как наличие required causal state;
- remote provider state unavailable/partial должен ограничивать reproducibility claim;
- software/hardware/determinism conditions фиксируются для сильных reproducibility claims;
- raw GPU/CPU/network/storage telemetry не публикуется в `CognitiveState` автоматически;
- `ComputeManifest`/device-hours/FLOPs/VRAM не подменяют `CognitiveResourceEnvelope`/Executive ledger;
- estimated/measured/provider-reported compute не смешивать без provenance;
- `torch.save`/safetensors/DCP/Accelerate/hash/storage/container technology не превращать в architecture invariant до version design.

## Research discipline

Для Training Lifecycle минимум сравнивать, где применимо:

```text
Frozen / NoLearning
vs Offline
vs Interleaved Online
vs Decoupled Online
```

и учитывать **одновременно** новую capability и retention прежних capabilities.

После `DU-27` любой сильный experiment/result должен иметь explicit checkpoint/base condition, restore profile, software/hardware/determinism/RNG/compute provenance. `same seed` недостаточно.

Training/evaluation improvement нельзя приписывать algorithm/module, если condition получила другой dataset, privileged labels, больший фактический compute/data budget, другой restore state или более слабую validation/reproducibility policy без отдельной attribution.

## Implementation scope

Пока `docs/design/current.md` не разрешает version/implementation work, detailed design не является разрешением писать production architecture. Не превращать research candidates в implicit contracts.
