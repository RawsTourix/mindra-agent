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

Перед subsystem/data changes обязательны:

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

Следующий разрешённый DU брать только из `docs/design/current.md`.

## Общие запреты

Без explicit design change запрещаются concrete peer coupling, runtime Service Locator, mutable global state bus, hidden mutation чужого state, Agent dependency на Training/Evaluation Runtime, hidden oracle input, ad-hoc scheduler order, partial causal commit, silent stale rebase и смешение natural/replayed/imagined/intervened/counterfactual provenance.

## Ключевые различия

```text
CognitiveState ≠ full Agent Snapshot
Goal Proposal ≠ Committed Goal
MemoryRecord ≠ embedding/index
Memory ≠ trajectory/Training Replay
World Prediction ≠ observed fact
Intrinsic Signal ≠ Reward/Drive/Value
Drive State ≠ Value
Appraisal ≠ Affect ≠ Valuation
ValueProfile ≠ ScalarizedValue ≠ Training Reward ≠ Policy Decision
SalienceProfile ≠ AttentionAllocation
Memory Core validation ≠ Regulation admission
cognitive forgetting ≠ physical storage removal
Retrieval ≠ Agent Memory Replay ≠ Training Replay
Consolidation ≠ in-place rewrite ≠ Learning Update
CognitiveState ≠ Workspace
Workspace ≠ Memory ≠ Cortex context
Executive Control ≠ Cognitive Scheduler ≠ Policy
Policy ≠ Planner
Planner ≠ World Model
Plan ≠ ImaginedTrajectory
ActionCandidate ≠ SelectedActionIntent
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
Policy choice ≠ external override
transport failure ≠ Environment no-effect
execution_unknown ≠ definitely_not_sent
TraceEvent ≠ ExperienceEvent
Experience Journal ≠ Agent runtime state
Experience Journal ≠ Replay Buffer ≠ Agent Memory
Source Experience ≠ TrainingSample
ResearchAnnotation ≠ agent-visible payload
Agent Memory Replay ≠ Training Replay
```

## Memory Regulation safeguards

До пересмотра `DU-20`:

- Memory Regulation не владеет canonical Store;
- structural validation нельзя обходить Salience/Value;
- universal `memory_importance` не canonical;
- retrieval/access frequency не automatic importance;
- cognitive forgetting отделено от physical removal;
- consolidation создаёт новый derived record и сохраняет source/support/conflict provenance;
- source authority не повышается после summarization;
- re-encoding/index rebuild не semantic consolidation;
- Agent Memory Replay не равен Training Replay;
- consolidation не выполняет optimizer/gradient update.

## Workspace safeguards

До пересмотра `DU-21`:

- Workspace не alias `CognitiveState`;
- producers работают через explicit proposals/candidates;
- Salience/AttentionAllocation — evidence, а не admission decision;
- WorkspaceItem сохраняет source/provenance/authority;
- broadcast означает availability, а не callback/automatic invocation;
- Memory retrieval не попадает в Workspace автоматически;
- Workspace eviction не удаляет source memory;
- Workspace не является Cortex prompt;
- imagined/branch-local Workspace не мутирует real Workspace;
- Workspace не считается evidence consciousness.

## Executive Control safeguards

До пересмотра `DU-22`:

- Executive не изменяет dependency graph/write authority/atomic commits Scheduler;
- Executive не Service Locator и не получает direct handles на Memory/Cortex/World Model/Workspace;
- optional work поступает через `MetaActionProposal` + `InternalOperationCatalog`;
- `ExecutiveDecision` проходит Scheduler/runtime validation;
- Executive не выбирает Environment action;
- monitoring evidence не является control command;
- hard `CognitiveResourceEnvelope` не увеличивается Executive;
- estimate/reservation/actual consumption различаются;
- budget exhaustion не разрешает hidden extra compute;
- Goal focus не мутирует Goal Graph;
- real imagination compute учитывается в real ledger;
- fallback/degradation explicit и traced.

## Policy / Planner safeguards

До пересмотра `DU-23`:

- Policy — единственный normal-runtime owner `SelectedActionIntent`;
- Planner/Cortex/Valuation/World Model не создают final intent напрямую;
- Policy не dispatch'ит Environment action;
- Planner не World Model и не читает hidden Environment Ground Truth;
- candidate generation сохраняет provenance и входит в `PolicyCandidateSet`;
- Planner subgoal проходит Goal Proposal boundary;
- Valuation evidence не превращается автоматически в `argmax` action;
- `incomparable` допускается без fake scalarization;
- `DecisionDeferral` не вызывает Executive рекурсивно;
- planning compute связан с Executive accounting;
- stale plan/candidates не rebased молча;
- stochastic Policy сохраняет RNG provenance;
- hidden random/default fallback запрещён.

## Action Boundary safeguards

До пересмотра `DU-24`:

- `SelectedActionIntent` не dispatch'ится напрямую;
- stale/malformed/unauthorized intent не получает `ActionCommitRecord`;
- normal Gate не hidden Policy;
- semantics-preserving normalization имеет transformation provenance;
- behavior-changing substitution только через explicit override record;
- original Policy intent и committed override сохраняются раздельно;
- Gate не читает hidden evaluator/Environment Ground Truth normal runtime способом;
- `Action Commit` после authorization и до dispatch;
- post-commit failure не отменяет commit;
- Dispatcher не выбирает fallback action;
- retry не создаёт новый Action Commit;
- stable `dispatch_id` используется для same logical retry;
- blind retry запрещён при `execution_unknown` без dedup/idempotency/definite-non-send evidence;
- universal physical exactly-once не предполагается;
- accepted receipt не означает execution success;
- transport failure/no-effect/partial/unknown различаются;
- terminal outcome фиксируется до reset;
- provider-native transport payload не становится Policy semantic contract.

## Experience / Data / Replay safeguards

До пересмотра `DU-25`:

- source of truth записанного опыта — append-only causal `Experience Journal`, а не transition table/replay buffer;
- event-sourced только data plane; не реконструировать ordinary Agent runtime из journal вопреки `CognitiveState`/snapshot semantics;
- `TraceEvent` и `ExperienceEvent` не считать синонимами;
- source `ExperienceEvent` immutable по смыслу;
- hindsight/relabeling/target recomputation/re-encoding создают derived sample/artifact, а не rewrite source history;
- physical append order/wall-clock не использовать как единственное causal ordering evidence;
- causal parent refs/logical scopes/revision refs сохраняются;
- evaluator-only/Research Ground Truth не класть в обычный agent-visible `info`/payload;
- privileged data хранить отдельным `ResearchAnnotationRecord` и включать только через explicit `DataVisibilityPolicy`;
- `ActionCommitRecord` без Environment transition является валидным source case;
- при `execution_unknown` запрещено fabricatе `next_state = state_before` или `executed=false`;
- terminated/truncated различать до explicit training transform;
- changing `agent_revision`/component revisions не скрывать;
- `DatasetManifest` обязан фиксировать source selection/schema/transforms/revisions/splits/quality/determinism;
- `TrainingSample` всегда derived и имеет source + transform lineage;
- replay buffer/table не archival source of truth;
- replay item eviction не удаляет source experience;
- Training Replay selection не создаёт natural experience;
- Agent Memory Replay и Training Replay не смешивать даже при общем source episode;
- replay priority/loss/TD-error/sampling frequency не становились Salience/Memory importance/Valuation автоматически;
- heavy artifact loss и core causal event loss различаются;
- lossy transform маркируется и не masquerade как исходное evidence;
- storage technology/RLDS/Minari/Reverb/Arrow/HDF5 не принимать как canonical до version design.

## Research discipline

Для Experience/Data минимум проверять:

```text
full causal projection
vs transition-only projection

agent-visible-only data
vs explicit privileged supervision

correct sequence
vs shuffled sequence

uniform replay
vs prioritized/other replay
```

Обязательны leakage, source→derived lineage, revision attribution, unresolved execution, split leakage, schema migration и deterministic extraction tests.

Training improvement нельзя приписывать algorithm, если condition получила другую source population, hidden privileged fields или дополнительный transform/relabel policy без отдельной attribution.

## Implementation scope

Пока `docs/design/current.md` не разрешает version/implementation work, detailed design не является разрешением писать production architecture. Не превращать research candidates в implicit contracts.
