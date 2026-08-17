# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-19` завершены и приняты. Реализация ещё не начата.**

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
- 19 accepted ADR;
- candidate semantic contracts для subsystem boundaries `DU-07 … DU-19`.

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
```

---

# 3. DU-19

Canonical design:

- [`modules/salience.md`](modules/salience.md)

Candidate contract:

- [`contracts/salience.md`](contracts/salience.md)

Accepted decision:

- [`ADR-0019`](decisions/ADR-0019-budgeted-contextual-salience-allocation.md)

Research pass:

- [`../research/literature/DU-19-salience-attention-landscape-2026-08.md`](../research/literature/DU-19-salience-attention-landscape-2026-08.md)

Главные результаты:

```text
Appraisal relevance ≠ Salience
Value ≠ Salience
Intrinsic novelty ≠ Salience
SalienceProfile ≠ AttentionAllocation
AttentionAllocation ≠ Workspace admission
AttentionAllocation ≠ Executive compute decision
AttentionAllocation ≠ Policy decision
Cortex attention weight ≠ MINDRA Salience
```

- принят отдельный `Salience System` как boundary priority/allocation;
- Salience работает только с explicit `SalienceCandidateSet`;
- Salience является purpose/context dependent;
- canonical intermediate — typed `SalienceProfile`, а не обязательный scalar;
- budget приходит от explicit consumer/context;
- `AllocationPolicy` versioned и отделена от profile;
- ranking, gating и allocation различаются;
- bottom-up/signal-driven и top-down/concern-driven evidence остаются различимыми;
- optional focus persistence/inhibition/habituation state допустим;
- Salience не выполняет Memory retention, Workspace admission, Cortex invocation, scheduler mutation или final action selection;
- actual/predicted/imagined/intervened provenance сохраняется;
- functional gate требует реального downstream allocation/processing effect;
- обязательны `NoSalience`, uniform/random/shuffled/source-only и matched controls.

---

# 4. Следующий допустимый Design Update

```text
DU-20 — Memory Regulation / Consolidation
```

Цель `DU-20` — расширить нейтральный `Memory Core` механизмами управляемого сохранения, забывания, eviction, replay selection и consolidation, используя explicit evidence вроде Salience без превращения Memory в скрытую Valuation или Training Runtime.

Обязательные вопросы:

```text
memory admission
retention
aging / forgetting
eviction
capacity pressure
salience integration
recency/diversity/value conflicts
retrieval-history influence?
replay candidate selection
Agent memory replay ≠ Training replay
consolidation event semantics
episodic → derived/semantic memory
source preservation / provenance
contradiction/supersession
representation drift / re-encoding
slow learned structures boundary
catastrophic forgetting
logical time
snapshot/revision
failure/degradation
NoRegulation / random / recency / shuffled / matched controls
```

Нужно особенно определить:

- где заканчивается Memory Core и начинается regulation;
- кто принимает `MemoryWriteProposal` при ограниченной capacity;
- может ли Salience быть одним из signals, но не единственным определением retention;
- чем forgetting отличается от physical deletion;
- когда derived summary/semantic record становится новым `MemoryRecord`;
- как сохраняется lineage исходного episodic evidence;
- чем internal memory replay/consolidation отличается от `Training Runtime Replay`;
- допускаются ли learned slow-weight updates в DU-20 или только создаётся evidence для `DU-26`;
- как проверить, что regulation лучше random/recency baseline и не создаёт confirmation bias.

После принятия `DU-20` допускается:

```text
DU-21 — Workspace
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

- Memory Regulation / Consolidation;
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
