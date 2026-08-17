# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-20` завершены и приняты. Реализация ещё не начата.**

Приняты:

- foundation/system boundaries `DU-01 … DU-06`;
- Environment/MicroWorld;
- Perception;
- Goal System;
- Cortex boundary;
- Memory Core;
- World Model;
- Self Model;
- Intrinsic Signals;
- Drives;
- Appraisal;
- Affect;
- Valuation;
- Salience / Attention;
- Memory Regulation / Consolidation;
- 20 accepted ADR;
- candidate semantic contracts для subsystem boundaries `DU-07 … DU-20`.

---

# 2. Завершённые Design Updates

```text
DU-00 — Documentation Foundation
DU-01 — System Context
DU-02 — Dependency & Composition Rules
DU-03 — Runtime / Temporal Model
DU-04 — CognitiveState Semantics
DU-05 — Module Protocol & Scheduling
DU-06 — Observability & Intervention
DU-07 — Environment / MicroWorld Contract
DU-08 — Perception / Canonical Representation
DU-09 — Goal System
DU-10 — Cortex Boundary
DU-11 — Memory Core
DU-12 — World Model
DU-13 — Self Model
DU-14 — Intrinsic Signals
DU-15 — Drives
DU-16 — Appraisal
DU-17 — Affect Dynamics
DU-18 — Valuation
DU-19 — Salience / Attention
DU-20 — Memory Regulation / Consolidation
```

---

# 3. DU-20

Canonical design:

- [`modules/memory.md`](modules/memory.md) — нейтральный Memory Core `DU-11`;
- [`modules/memory-regulation.md`](modules/memory-regulation.md) — regulation/consolidation extension `DU-20`.

Candidate contracts:

- [`contracts/memory.md`](contracts/memory.md);
- [`contracts/memory-regulation.md`](contracts/memory-regulation.md).

Accepted decision:

- [`ADR-0020`](decisions/ADR-0020-source-preserving-budget-aware-memory-regulation.md).

Research pass:

- [`../research/literature/DU-20-memory-regulation-consolidation-landscape-2026-08.md`](../research/literature/DU-20-memory-regulation-consolidation-landscape-2026-08.md).

Главные результаты:

```text
Memory Core validation ≠ Regulation admission
Memory Core owner ≠ Memory Regulation policy owner
SalienceProfile ≠ retention/eviction decision
forgetting ≠ physical deletion
retrieval ≠ Agent Memory Replay ≠ Training Replay
consolidation ≠ in-place rewrite
consolidation ≠ Learning Update
representation maintenance ≠ semantic consolidation
```

- Memory Core остаётся единственным owner canonical Store и lifecycle commit;
- Memory Regulation является отдельной policy responsibility, но не вторым Store owner;
- admission/retention/eviction/replay/consolidation имеют разные purpose-specific policies;
- принят explicit multi-dimensional `MemoryBudget`;
- universal `memory_importance` scalar не является canonical representation;
- Salience является одним из evidence sources, но не final memory authority;
- retrieval/access history не становится importance автоматически;
- aging использует logical time, а не GPU/network/Colab latency;
- cognitive forgetting отделено от physical deletion;
- replay/reactivation запускается только в explicit causal context и не считается новым natural experience;
- Agent Memory Replay не является Training Runtime replay;
- consolidation gated и может быть полностью отключена;
- derived/semantic memory создаётся как новый `MemoryRecord`;
- source episodes не переписываются inplace;
- `derived_from`, support/conflict и derivation provenance сохраняются;
- consolidation не повышает source authority/trust автоматически;
- contradiction/minority evidence должно быть представимо без hidden majority-vote;
- representation re-encoding/index rebuild не создаёт semantic memory;
- optimizer/slow-weight update отложен до `DU-26`;
- episodic-only/`NoConsolidation` является обязательным control;
- compression ratio сам по себе не считается evidence полезной consolidation.

---

# 4. Следующий допустимый Design Update

```text
DU-21 — Workspace
```

Цель `DU-21` — проверить, нужен ли MINDRA отдельный ограниченный temporary global-access mechanism сверх versioned `CognitiveState`, Salience allocation и обычных explicit module dependencies.

Обязательные вопросы:

```text
Workspace module gate
Workspace candidate/admission boundary
Workspace ≠ CognitiveState
Workspace ≠ Salience
Workspace ≠ Cortex context
Workspace ≠ Memory
capacity / slots / token-like budget?
persistence / replacement
broadcast/read semantics
consumer eligibility
producer authority
competition/admission
Salience integration
Goal/Affect/Valuation relation
Cortex context packing boundary
Memory retrieval → Workspace boundary
multi-cycle persistence
branch/imagination workspace
observability/intervention
NoWorkspace / matched control
snapshot/revision/degradation
```

Нужно особенно определить:

- существует ли measurable функция Workspace сверх общего committed state;
- должен ли Workspace хранить ограниченный subset уже доступного information;
- является ли global availability отдельной capability или достаточно declared reads `CognitiveState`;
- как Salience предлагает priority, но Workspace сам принимает admission;
- могут ли modules читать Workspace только через declared dependency;
- должен ли Workspace переживать несколько Cognitive Cycles/Decision Window;
- как избежать превращения Workspace в giant prompt Cortex;
- как сравнить Workspace с parameter/state-capacity-matched recurrent/shared-state control;
- при каком отрицательном результате отдельный Workspace должен быть отклонён.

После принятия `DU-21` допускается:

```text
DU-22 — Metacognitive / Executive Control
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

- Workspace;
- Metacognitive / Executive Control;
- Policy / Planner;
- Action Gate / Executor;
- Experience / Data / Replay schema;
- Training Lifecycle;
- Checkpoint / Reproducibility / Compute;
- MINDRA-Eval;
- Engineering Testing;
- Research Claims / Limitations;
- Contract + ADR Freeze;
- Version Roadmap;
- implementation sequences.

Также не выбраны concrete Python/framework/model/algorithm implementations.

---

# 6. Implementation status

```text
Исследовательская/production реализация: не начата
Дорожная карта версий: не спроектирована
Software version: отсутствует
Implementation HEAD: отсутствует
```

Detailed design сам по себе не разрешает Codex начинать implementation до `DU-32` и соответствующего version/implementation sequence.
