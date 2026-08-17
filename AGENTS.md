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
AttentionAllocation ≠ Workspace/Executive/Policy decision
Memory Core validation ≠ Regulation admission
SalienceProfile ≠ Memory lifecycle decision
cognitive forgetting ≠ physical storage removal
Retrieval ≠ Agent Memory Replay ≠ Training Replay
Consolidation ≠ in-place rewrite ≠ Learning Update
Representation maintenance ≠ semantic consolidation
Derived MemoryRecord ≠ source episode
```

## Memory Regulation safeguards

До пересмотра `DU-20`:

- Memory Regulation не владеет canonical Store и публикует lifecycle/consolidation proposals через Memory Core;
- structural validation нельзя обходить высоким Salience/Value;
- universal `memory_importance` не является canonical state;
- Salience — evidence, а не готовое retention/eviction решение;
- retrieval/access frequency не является automatic importance;
- memory aging использует logical time;
- cognitive forgetting отделено от physical storage removal;
- consolidation создаёт новый derived record, а не изменяет source payload задним числом;
- derived record обязан сохранять source/support/conflict/derivation provenance;
- source authority не повышается автоматически после summarization/consolidation;
- contradictions не исчезают без explicit versioned policy;
- re-encoding/index rebuild не считается semantic consolidation;
- Agent Memory Replay не является новым natural experience и не равен Training Replay;
- replay/consolidation выполняются только в explicit causal context;
- consolidation не выполняет optimizer/gradient update;
- concrete forgetting curve, FIFO/LRU/top-K, LLM summarizer, clustering и generative replay не становятся canonical только из research literature.

## Research discipline

Для Memory Regulation сравнивать минимум:

```text
Full Regulation
vs NoRegulation
vs FIFO/recency/random/shuffled

Full Consolidation
vs episodic-only
vs matched/random consolidation/compression
```

Измерять source fidelity, contradiction preservation, false derived memories, retrieval/behavioral utility, generalization и budget efficiency; compression ratio отдельно недостаточен.

## Implementation scope

Пока `docs/design/current.md` не разрешает version/implementation work, detailed design не является разрешением писать production architecture. Не превращать research candidates в implicit contracts.
