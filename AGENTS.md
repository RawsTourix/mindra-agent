# AGENTS.md — правила работы с MINDRA

## Назначение

Карта обязательного контекста для Codex, ChatGPT и других coding agents. Канонические знания находятся в `docs/`; этот файл не дублирует полный design.

## Язык

- документация и комментарии — на русском;
- technical identifiers/API/package/class/function/type names — на английском.

## Перед любой работой

1. Проверить repository status/HEAD.
2. Прочитать `docs/README.md` и `docs/design/current.md`.
3. Определить разрешённый scope.
4. Прочитать релевантный canonical design owner + accepted ADR + candidate contract.
5. Не выходить за текущий DU/version scope.

## Source of truth

```text
accepted ADR + canonical design
→ candidate/exact contracts
→ version specification
→ implementation sequence
→ implementation
→ engineering/research evidence
```

Research evidence меняет architecture только через design review/ADR.

## Принятые boundaries

| Область | Canonical design | Contract | ADR |
|---|---|---|---|
| Environment | `docs/design/modules/environment.md` | `contracts/environment.md` | `ADR-0007` |
| Perception | `docs/design/modules/perception.md` | `contracts/perception.md` | `ADR-0008` |
| Goals | `docs/design/modules/goals.md` | `contracts/goals.md` | `ADR-0009` |
| Cortex | `docs/design/modules/cortex.md` | `contracts/cortex.md` | `ADR-0010` |
| Memory Core | `docs/design/modules/memory.md` | `contracts/memory.md` | `ADR-0011` |
| World Model | `docs/design/modules/world-model.md` | `contracts/world-model.md` | `ADR-0012` |
| Self Model | `docs/design/modules/self-model.md` | `contracts/self-model.md` | `ADR-0013` |
| Intrinsic Signals | `docs/design/modules/intrinsic-signals.md` | `contracts/intrinsic-signals.md` | `ADR-0014` |
| Drives | `docs/design/modules/drives.md` | `contracts/drives.md` | `ADR-0015` |
| Appraisal | `docs/design/modules/appraisal.md` | `contracts/appraisal.md` | `ADR-0016` |
| Affect | `docs/design/modules/affect.md` | `contracts/affect.md` | `ADR-0017` |
| Valuation | `docs/design/modules/valuation.md` | `contracts/valuation.md` | `ADR-0018` |
| Salience | `docs/design/modules/salience.md` | `contracts/salience.md` | `ADR-0019` |
| Memory Regulation | `docs/design/modules/memory-regulation.md` | `contracts/memory-regulation.md` | `ADR-0020` |
| Workspace | `docs/design/modules/workspace.md` | `contracts/workspace.md` | `ADR-0021` |
| Executive Control | `docs/design/modules/executive-control.md` | `contracts/executive-control.md` | `ADR-0022` |
| Policy / Planner | `docs/design/modules/policy-planner.md` | `contracts/policy-planner.md` | `ADR-0023` |
| Action Boundary | `docs/design/modules/action-boundary.md` | `contracts/action-boundary.md` | `ADR-0024` |
| Experience/Data/Replay | `docs/design/experience-data-replay.md` | `contracts/experience-data-replay.md` | `ADR-0025` |
| Training Lifecycle | `docs/design/training-lifecycle.md` | `contracts/training-lifecycle.md` | `ADR-0026` |
| Checkpoint/Reproducibility/Compute | `docs/design/checkpoint-reproducibility-compute.md` | `contracts/checkpoint-reproducibility-compute.md` | `ADR-0027` |
| MINDRA-Eval | `docs/design/mindra-eval.md` | `contracts/mindra-eval.md` | `ADR-0028` |

`contracts/...` выше означает `docs/design/contracts/...`. Следующий DU — только из `docs/design/current.md`.

## Cross-cutting stop-signs

```text
CognitiveState ≠ full Agent Snapshot
Goal Proposal ≠ Committed Goal
MemoryRecord ≠ embedding/index
World Prediction ≠ observed fact
Intrinsic Signal ≠ Reward/Drive/Value
Appraisal ≠ Affect ≠ Valuation
SalienceProfile ≠ AttentionAllocation
Retrieval ≠ Agent Memory Replay ≠ Training Replay
Consolidation ≠ Learning Update
CognitiveState ≠ Workspace
Executive Control ≠ Scheduler ≠ Policy
Policy ≠ Planner
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
Experience Journal ≠ Agent runtime state
Source Experience ≠ TrainingSample
Training Runtime ≠ cognitive module
runtime dependency graph ≠ gradient graph
CandidateRevisionBundle ≠ Active AgentRevision
AgentSnapshot ≠ persistent Checkpoint
same seed ≠ same RNG state ≠ guaranteed same execution
ComputeManifest ≠ CognitiveResourceEnvelope
Evaluation Runtime ≠ Agent cognition
Task score ≠ module/causal/calibration evidence
nested episode ≠ independent training replicate
Policy pre-Gate quality ≠ post-Gate system quality
Engineering Testing ≠ MINDRA-Eval
```

## Cognitive/runtime safeguards

- никакого runtime Service Locator, mutable global bus, hidden peer mutation или oracle input;
- Memory Regulation не владеет canonical Store;
- consolidation создаёт derived record и не делает optimizer update;
- Workspace — bounded proposal/admission surface, не alias `CognitiveState`;
- Executive выбирает internal meta-actions/resources, но не меняет Scheduler graph и не выбирает Environment action;
- Policy — normal-runtime owner `SelectedActionIntent`;
- Action Gate не hidden Policy/oracle; override имеет explicit provenance;
- `Action Commit` после authorization и до dispatch;
- post-commit failure не отменяет commit;
- blind retry при `execution_unknown` запрещён без dedup/idempotency evidence.

## Data/training safeguards

- `Experience Journal` append-only source; replay buffer не source truth;
- evaluator-only Ground Truth хранится отдельно;
- hindsight/relabel/re-encode создают derived sample, не rewrite source;
- Training Runtime не имеет ambient mutable access к live Agent;
- ordinary cognition не выполняет hidden `optimizer.step()`;
- `TrainingPlan` pin'ит base revisions/data/objectives/gradient policy;
- runtime edge не создаёт gradient edge;
- privileged supervision только explicit;
- candidate revision проходит validation до activation;
- activation только на causal boundary; in-flight decision не меняет revision;
- failed candidate не мутирует live Agent;
- training metrics/replay priority не становятся cognitive signals автоматически.

## Checkpoint safeguards

- weights-only не называть full/training-resume checkpoint;
- seed не заменяет current RNG state;
- final manifest commit только после verification required artifacts;
- content identity не равна physical path;
- active/candidate revisions restore'ятся раздельно;
- full-system exact restore требует aligned Agent + Environment state;
- exact restore не downgraded молча;
- `execution_unknown` блокирует unsafe retry/branch;
- migration/delta dependency имеют explicit lineage/integrity;
- raw infrastructure telemetry не публикуется в cognition автоматически.

## MINDRA-Eval safeguards

- evaluator score/Ground Truth не писать в `CognitiveState` normal runtime способом;
- `EvaluationCondition` pin'ит checkpoint/world/Cortex/composition/interventions/data/resources/software/hardware context;
- confirmatory hypothesis/primary metrics/contrasts/statistical plan фиксируются до confirmatory outcome;
- exploratory result не выдавать за preregistered confirmatory;
- experimental/statistical unit и replicate nesting explicit;
- episodes одного checkpoint не считать independent training replicates;
- stochastic aggregate claim требует uncertainty/distribution evidence, не только point estimate;
- `NoX` не называть matched control, если изменились capacity/compute/context/data;
- baseline/treatment tuning budget match либо deviation explicit;
- paired counterfactual only from sufficient verified DU-27 base state;
- evaluator intervention только через declared Intervention Gateway;
- Policy quality измерять до Gate отдельно от Gate/post-Gate outcome;
- strong Gate не является evidence хорошей Policy;
- `execution_unknown`/censored/invalid/unavailable не сворачивать в failure/0 без MetricSpec policy;
- probability claim оценивать metric, соответствующей probability semantics; ECE alone не universal proof;
- actual compute/data/context/parameter differences входят в attribution;
- composite score derived и не удаляет source metrics;
- oracle conditions privileged;
- Affect/Workspace/Planner/Executive имеют explicit negative module gates;
- strength research claim не превышает supporting evidence level;
- benchmark/rliable/t-test/bootstrap/Brier/tracker/plot stack не architecture invariant до version design.

## Research discipline

Сильный result после `DU-28` должен ссылаться на:

```text
EvaluationStudyPlan / EvaluationCondition
checkpoint + RestoreProfile
world/task distribution
controls/interventions
ReplicateStructure
MetricSpec(s)
StatisticalAnalysisPlan
software/hardware/RNG/compute provenance
```

Improvement нельзя приписывать module/algorithm, если treatment получил другой dataset, privileged labels, больший compute/data/tuning budget, другой restore state или более сильный Action Gate без отдельной attribution.

Отрицательный module-gate result инициирует interpretation/design review; architecture меняется только через ADR.

## Implementation scope

До `DU-32` detailed design не является разрешением начинать production/research implementation. Не превращать research candidates в implicit contracts.
