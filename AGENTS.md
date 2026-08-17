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

Перед subsystem changes обязательны:

- `docs/design/system-context.md`;
- `docs/design/dependency-rules.md`;
- `docs/design/execution-model.md`;
- `docs/design/cognitive-state.md`;
- `docs/design/module-lifecycle.md`;
- `docs/design/observability-and-intervention.md`.

## Принятые subsystem boundaries

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
published state ≠ Workspace admission
Workspace ≠ Memory ≠ Cortex context
broadcast ≠ callback/module execution
Executive Control ≠ Cognitive Scheduler
Executive Control ≠ Policy / Planner
Internal MetaAction ≠ Environment Action
MetaActionProposal ≠ executed operation
ExecutiveDecision ≠ direct provider/service call
resource estimate ≠ reservation ≠ actual consumption
Executive yield ≠ Action Commit
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

- Workspace не является alias `CognitiveState`;
- Workspace работает только с explicit proposals/candidates;
- producers не мутируют Workspace напрямую;
- Salience/AttentionAllocation — evidence, а не admission decision;
- WorkspaceItem сохраняет source/provenance/authority;
- consumer access declared;
- broadcast означает availability, а не callback/automatic invocation;
- Memory retrieval не попадает в Workspace автоматически;
- Workspace eviction не удаляет source memory;
- Workspace не является Cortex prompt;
- imagined/branch-local Workspace не мутирует real Workspace;
- Workspace не считается evidence consciousness.

## Executive Control safeguards

До пересмотра `DU-22`:

- Executive Control не изменяет dependency graph, write authority или atomic commit semantics Scheduler;
- Executive не является runtime Service Locator и не получает direct handles на Memory/Cortex/World Model/Workspace services;
- optional work поступает через explicit `MetaActionProposal` + declared `InternalOperationCatalog`;
- `InternalOperationCatalog` содержит semantic descriptors, а не live provider objects;
- `ExecutiveDecision` всегда проходит Scheduler/runtime validation до execution;
- Executive не выбирает Environment action и `yield_to_policy` не является `Action Commit`;
- Self Model, Salience, Workspace, Valuation и uncertainty являются evidence, а не готовыми control commands;
- hard `CognitiveResourceEnvelope` не увеличивается Executive самостоятельно;
- hidden infrastructure quota/latency/GPU telemetry не становится cognitive input без explicit agent-visible contract;
- estimate, reservation и actual resource consumption не смешиваются;
- hard budget exhaustion не разрешает hidden extra Cortex/retrieval/rollout calls;
- Cortex/retrieval/rollout/consolidation не вызываются direct ambient способом;
- Executive не генерирует чужой semantic payload без proposal boundary: Memory query, Cortex request и rollout target остаются responsibility соответствующего producer/consumer;
- Goal focus может ссылаться на committed Goals, но не мутирует Goal Graph/lifecycle;
- Workspace budget/context control не заменяет Workspace AdmissionPolicy;
- real compute, потраченный на imagination, учитывается в real ledger; simulated future budget остаётся branch-local;
- fallback/degradation всегда explicit и traced;
- controller не должен читать весь `CognitiveState` ambient способом — только declared `ExecutiveObservation` projection.

## Research discipline

Для Executive Control минимум сравнивать:

```text
Adaptive Executive
vs NoExecutive / fixed schedule
vs FixedBudget
vs RandomMetaAction
vs SimpleThreshold
vs SalienceOnly / uncertainty-only
vs CostUnaware
vs MatchedLearnedRouter
```

Обязательны equal/matched actual compute accounting, budget sweeps, operation/stopping distributions, competence/uncertainty/cost interventions, capability degradation tests и controller-overhead accounting.

Positive result не считается доказанным, если adaptive configuration просто использовала больше cognitive resource.

## Implementation scope

Пока `docs/design/current.md` не разрешает version/implementation work, detailed design не является разрешением писать production architecture. Не превращать research candidates в implicit contracts.
