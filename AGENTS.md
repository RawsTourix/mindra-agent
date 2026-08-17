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
SalienceProfile/AttentionAllocation ≠ Workspace admission
WorkspaceBudget ≠ AttentionBudget ≠ MemoryBudget ≠ Executive budget
WorkspaceItem ≠ source truth
Workspace ≠ Memory ≠ Cortex context
Workspace eviction ≠ Memory forgetting
broadcast ≠ callback/module execution
imagined Workspace ≠ real Workspace
Workspace ≠ Policy/Executive Control
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

- Workspace не является alias `CognitiveState` и не заменяет dependency contracts;
- Workspace работает только с explicit proposals/candidates;
- producers не мутируют Workspace напрямую;
- capacity/bandwidth explicit; unbounded buffer не считается эквивалентным Workspace автоматически;
- Salience/AttentionAllocation — evidence/hint, а не готовое admission decision;
- Workspace AdmissionPolicy versioned и отдельна;
- `WorkspaceItem` сохраняет source ref/revision/provenance/authority;
- admission/compression не превращает prediction/retrieval/Cortex inference в observed fact;
- source update не переписывает admitted item задним числом;
- consumer access должен быть declared; Workspace не ambient global dictionary;
- broadcast означает read availability, а не callback, interrupt или automatic module invocation;
- Workspace не меняет scheduler graph;
- Memory retrieval не попадает в Workspace автоматически;
- Workspace eviction не удаляет/забывает source MemoryRecord;
- Workspace не является Cortex prompt; context packing выполняется explicit consumer/Gateway path;
- Workspace не выбирает Environment action и не владеет Executive compute budget;
- imagined/branch-local Workspace не мутирует real Workspace автоматически;
- failure/unavailable нельзя маскировать fake empty Workspace без traced degradation;
- Workspace не считается evidence consciousness.

## Research discipline

Для Workspace минимум сравнивать:

```text
Full Workspace
vs NoWorkspace / DirectReads
vs Random/Shuffled/Fixed admission
vs UnboundedWorkspace
vs WorkspaceWithoutBroadcast
vs MatchedSharedBuffer
vs MatchedRecurrentBuffer
```

Обязательны capacity sweep и causal checks:

```text
admission/broadcast intervention
→ WorkspaceSnapshot/read access changed
→ actual downstream processing changed
→ measurable coordination/behavior effect
```

Если matched controls объясняют эффект, отдельная Workspace boundary должна быть пересмотрена.

## Implementation scope

Пока `docs/design/current.md` не разрешает version/implementation work, detailed design не является разрешением писать production architecture. Не превращать research candidates в implicit contracts.
