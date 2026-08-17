# AGENTS.md — правила работы с MINDRA

## Назначение

Карта обязательного контекста для Codex, ChatGPT и других coding agents. Канонические знания находятся в `docs/`; этот файл не дублирует полный design.

## Язык

- документация и комментарии — на русском;
- technical identifiers/API/package/class/function/type names — на английском.

## Перед любой работой

1. Проверить repository status/HEAD.
2. Прочитать `docs/README.md` и `docs/design/current.md`.
3. После `DU-31` обязательно прочитать:
   - `docs/design/contract-adr-consistency-freeze.md`;
   - `docs/design/contracts/semantic-freeze-manifest.md`.
4. Определить разрешённый DU/version scope.
5. Прочитать релевантный canonical design owner + accepted ADR + semantic contract.
6. Для implementation дополнительно прочитать `DU-32` roadmap, version specification и `implementation-sequence.md` соответствующей версии.
7. Не выходить за разрешённый scope.

## Source of truth после DU-31

```text
accepted ADR + canonical design
        ↓
Semantic Freeze Baseline F31
        ↓
semantic-frozen contracts
        ↓
version specification / exact contracts
        ↓
implementation sequence
        ↓
implementation
        ↓
engineering/research evidence
        ↓
versioned research claims
```

Research/engineering evidence меняет architecture только через design review/ADR. Research claim не заменяет evidence source.

`F31` freezing означает semantic meaning, **не exact Python API**.

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
| Engineering Testing | `docs/design/engineering-testing.md` | `contracts/engineering-testing.md` | `ADR-0029` |
| Research Claims / Limitations | `docs/design/research-claims-limitations.md` | `contracts/research-claims-limitations.md` | `ADR-0030` |
| Semantic Freeze | `docs/design/contract-adr-consistency-freeze.md` | `contracts/semantic-freeze-manifest.md` | `ADR-0031` |

`contracts/...` означает `docs/design/contracts/...`.

## F31 consistency resolutions

Следующие resolutions обязательны при чтении ранних docs:

```text
CR-01 Action lifecycle
CR-02 Memory admission ownership
CR-03 Replay taxonomy
CR-04 Consolidation vs Learning Update
CR-05 candidate/validated/activated revision lifecycle
```

Подробности — `docs/design/contract-adr-consistency-freeze.md`.

Нельзя выбирать старую generic формулировку вместо F31 resolution.

## Cross-cutting stop-signs

```text
CognitiveState ≠ full Agent Snapshot ≠ Checkpoint
Goal Proposal ≠ Committed Goal
MemoryRecord ≠ embedding/index
Memory Core ≠ Memory Regulation
World Prediction ≠ observed fact
Intrinsic Signal ≠ Reward/Drive/Value
Appraisal ≠ Affect ≠ Valuation
SalienceProfile ≠ AttentionAllocation
Retrieval ≠ Agent Memory Replay ≠ Training Replay
Consolidation ≠ Learning Update
CognitiveState ≠ Workspace
Executive Control ≠ Scheduler ≠ Policy
Planner ≠ Policy
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
Experience Journal ≠ Agent runtime state
Source Experience ≠ TrainingSample
Training Runtime ≠ cognitive module
runtime dependency graph ≠ gradient graph
CandidateRevisionBundle ≠ Active AgentRevision
same seed ≠ same RNG state ≠ guaranteed same execution
ComputeManifest ≠ CognitiveResourceEnvelope
Evaluation Runtime ≠ Agent cognition
Task score ≠ module/causal/calibration evidence
Engineering Testing ≠ MINDRA-Eval
Observation ≠ Interpretation ≠ ResearchClaim
ClaimScope ≠ universal scope
association ≠ causation
functional similarity ≠ phenomenological equivalence
publication prose ≠ claim source of truth
```

## Cognitive/runtime safeguards

- никакого runtime Service Locator, mutable global bus, hidden peer mutation или oracle input;
- Memory Core владеет Store/identity/structural validation/commit; Memory Regulation — policy admission/retention/eviction/replay/consolidation decisions;
- consolidation создаёт derived MemoryRecord/maintenance effect и не делает optimizer update;
- Workspace — bounded proposal/admission surface, не alias `CognitiveState`;
- Executive выбирает internal meta-actions/resources, но не меняет Scheduler graph и не выбирает Environment action;
- Policy — normal-runtime owner `SelectedActionIntent`;
- Planner — optional provider, не final selection owner;
- Action Gate не hidden Policy/oracle; override имеет explicit provenance;
- `Action Commit` после authorization и до dispatch;
- post-commit failure не отменяет commit;
- blind retry при `execution_unknown` запрещён без dedup/idempotency evidence.

## Data/training/checkpoint safeguards

- `Experience Journal` append-only source; replay buffer не source truth;
- evaluator-only Ground Truth хранится отдельно;
- hindsight/relabel/re-encode создают derived sample, не rewrite source;
- Agent Memory Replay не является Training Replay;
- ordinary cognition не выполняет hidden `optimizer.step()`;
- runtime edge не создаёт gradient edge;
- candidate revision проходит validation до activation;
- activation только на causal boundary;
- failed candidate не мутирует live Agent;
- weights-only не называть full/training-resume checkpoint;
- seed не заменяет current RNG state;
- final checkpoint manifest commit только после verification required artifacts;
- active/candidate revisions restore'ятся раздельно;
- exact restore не downgraded молча;
- `execution_unknown` блокирует unsafe retry/branch.

## MINDRA-Eval safeguards

- evaluator score/Ground Truth не писать в `CognitiveState` normal runtime способом;
- `EvaluationCondition` pin'ит checkpoint/world/Cortex/composition/interventions/data/resources/software/hardware context;
- confirmatory hypothesis/metrics/contrasts/statistical plan фиксируются до confirmatory outcome;
- experimental/statistical unit и replicate nesting explicit;
- episodes одного checkpoint не считать independent training replicates;
- stochastic aggregate claim требует uncertainty/distribution evidence;
- `NoX` не называть matched control, если изменились capacity/compute/context/data;
- paired counterfactual only from sufficient verified DU-27 base state;
- Policy quality измерять до Gate отдельно от Gate/post-Gate outcome;
- `execution_unknown`/censored/invalid/unavailable не сворачивать в failure/0 без MetricSpec policy;
- actual compute/data/context/parameter/tuning differences входят в attribution;
- Affect/Workspace/Planner/Executive имеют explicit negative module gates.

## Engineering Testing safeguards

- для изменяемого frozen invariant определить/обновить `VerificationObligation`;
- `VerificationMatrix` не заменять списком случайных tests;
- architecture/import rules проверять статически, где package structure позволяет;
- replaceable implementation должна проходить capability-aware conformance suite;
- sequence-heavy lifecycle проверять property/state-machine подходом, где practically возможно;
- failure semantics намеренно fault-inject'ить; happy path недостаточен;
- test oracle/privileged sentinel не пересекает Agent-visible boundaries;
- stochastic neural output не фиксировать exact golden без deterministic contract;
- flaky rerun/`xfail`/quarantine не считать выполненной obligation;
- `skip`/`not run`/capability unavailable не считать pass;
- corrupted checkpoint, illegal write, privileged leakage, unsafe retry и unauthorized activation fail closed;
- line coverage не заменяет invariant/failure/contract coverage.

## Research Claims / Limitations safeguards

- substantial claim оформлять как versioned `ResearchClaim`;
- Observation/MetricRecord не повышать молча до causal/theoretical claim;
- каждый claim имеет explicit `ClaimScope`; отсутствие поля не означает universal;
- supporting и challenging evidence сохранять одновременно;
- causal wording только при соответствующем intervention/control evidence;
- `NoX` degradation не называть доказательством semantic necessity без confounder controls;
- effect одной implementation не выдавать автоматически за architecture-level effect;
- Cortex/provider/data/compute/tuning dependence отражать в scope/limitations;
- `negative evidence`, `null`, `inconclusive`, `invalid`, `not measured` не смешивать;
- failed module gate создаёт ClaimReview/design review, не silent ADR mutation;
- old claim weaken/narrow/supersede с historical lineage;
- public statement не сильнее canonical claim revision;
- `Self Model` не proof self-awareness/consciousness;
- `Affect`/Appraisal/Drives не proof subjective emotions;
- `Workspace` не proof consciousness;
- first-person Cortex text не reliable phenomenal self-report;
- human-like behavior/function не biological/phenomenological equivalence;
- один benchmark/result не proof AGI;
- `unknown` разрешён и предпочтительнее выдуманной уверенности.

## Semantic freeze safeguards

- version roadmap/implementation не меняет F31 ownership/causal semantics;
- exact API choice не объявляется новым semantic requirement без ADR;
- conditional module можно временно реализовать как `No*`/Dummy/control согласно version scope, но нельзя переопределить его contract;
- breaking semantic change идёт только через новый ADR + canonical owner/contract/freeze update;
- ранний generic wording при конфликте читается через explicit CR-01…CR-05;
- framework/model/tool candidate не становится architecture invariant только потому, что выбран в первой версии.

## Implementation scope

После `DU-31` semantic architecture **готова к version planning, но не к немедленному coding**.

До `DU-32` и version-specific `implementation-sequence.md` не начинать production/research implementation.
