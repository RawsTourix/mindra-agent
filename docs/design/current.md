# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-21` завершены и приняты. Реализация ещё не начата.**

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
- Workspace;
- 21 accepted ADR;
- candidate semantic contracts для subsystem boundaries `DU-07 … DU-21`.

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
DU-21 — Workspace
```

---

# 3. DU-21

Canonical design:

- [`modules/workspace.md`](modules/workspace.md)

Candidate contract:

- [`contracts/workspace.md`](contracts/workspace.md)

Accepted decision:

- [`ADR-0021`](decisions/ADR-0021-bounded-broadcast-workspace-overlay.md)

Research pass:

- [`../research/literature/DU-21-workspace-landscape-2026-08.md`](../research/literature/DU-21-workspace-landscape-2026-08.md)

Главные результаты:

```text
CognitiveState ≠ Workspace
published state ≠ Workspace admission
SalienceProfile ≠ Workspace admission
WorkspaceBudget ≠ AttentionBudget ≠ MemoryBudget ≠ Executive budget
WorkspaceItem ≠ source truth
Workspace ≠ Memory
Workspace eviction ≠ Memory forgetting
Memory retrieval ≠ Workspace admission
Workspace ≠ Cortex context
broadcast ≠ callback/module execution
imagined Workspace ≠ real Workspace
Workspace ≠ Policy
Workspace ≠ proof of consciousness
```

- Workspace принят как bounded temporary shared broadcast overlay;
- отдельная boundary имеет conditional/falsifiable module gate;
- Workspace работает только с explicit proposals/candidates;
- capacity/bandwidth являются частью functional hypothesis;
- Workspace AdmissionPolicy отделена от Salience;
- admitted item сохраняет source revision/provenance/authority;
- global availability означает доступ declared eligible consumers;
- broadcast не запускает consumers push/callback способом;
- Workspace может поддерживать multi-cycle persistence, но не заменяет long-term Memory;
- Memory retrieval должен отдельно пройти Workspace proposal/admission;
- Cortex context packing остаётся отдельной semantic operation;
- imagined/counterfactual branches используют branch-local Workspace;
- Workspace state входит в causally relevant Agent Snapshot;
- обязательны `NoWorkspace`, DirectReads, Random/Shuffled, Unbounded, no-broadcast и matched buffer controls;
- capacity sweep и broadcast lesions являются обязательными evaluation families;
- если matched controls объясняют эффект, отдельная Workspace boundary должна быть пересмотрена;
- Workspace functionality не является evidence subjective consciousness.

---

# 4. Следующий допустимый Design Update

```text
DU-22 — Metacognitive / Executive Control
```

Цель `DU-22` — спроектировать agent-owned regulation cognitive process: **какие внутренние операции выполнять, сколько вычислительного ресурса им выделять и когда прекращать/продолжать cognition**, не смешивая это с invariant Scheduler и final Policy/Action selection.

Обязательные вопросы:

```text
Executive module gate
metacognitive monitoring ≠ control
Executive Control ≠ Cognitive Scheduler
Executive Control ≠ Policy / Planner
internal/meta action ≠ Environment action
compute/resource budget model
continue / stop Cognitive Cycles
Cortex invocation decision
Memory retrieval decision
planning/imagination depth
consolidation initiation
Workspace budget/admission context control?
Goal focus control
Salience / Workspace / Self Model inputs
uncertainty / competence / cost evidence
resource exhaustion
latency/cost semantics without wall-clock leakage
policy for optional capabilities
fallback/degradation
branch/imagination executive state
observability/intervention
NoExecutive / fixed-budget / random / matched controls
snapshot/revision
```

Нужно особенно определить:

- кто владеет global agent compute/resource budgets;
- является ли Executive Control отдельным module или набором control policies;
- как Scheduler остаётся механикой допустимого исполнения и не принимает cognitive decisions;
- как Executive выбирает **разрешённые** операции, не обходя dependency/ownership invariants;
- когда Agent может решить «мне нужно ещё подумать» до `Action Commit`;
- как выбирать между `Cortex`, retrieval, World Model rollout, Workspace processing и непосредственным действием;
- как Self Model competence/uncertainty и expected costs влияют на control без превращения Self Model в controller;
- как Salience даёт priority evidence, но не сама запускает compute;
- как отделить internal meta-actions от будущих Environment actions;
- какой causal evidence нужен, чтобы доказать пользу adaptive control сверх fixed compute budget;
- при каком отрицательном результате отдельная Executive boundary должна быть упрощена/удалена.

После принятия `DU-22` допускается:

```text
DU-23 — Policy / Planner
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

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
