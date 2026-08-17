# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-24` завершены и приняты. Реализация ещё не начата.**

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
- Metacognitive / Executive Control;
- Policy / Planner;
- Action Boundary / Gate / Executor;
- 24 accepted ADR;
- candidate semantic contracts для subsystem boundaries `DU-07 … DU-24`.

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
DU-22 — Metacognitive / Executive Control
DU-23 — Policy / Planner
DU-24 — Action Boundary / Gate / Executor
```

---

# 3. DU-24

Canonical design:

- [`modules/action-boundary.md`](modules/action-boundary.md)

Candidate contract:

- [`contracts/action-boundary.md`](contracts/action-boundary.md)

Accepted decision:

- [`ADR-0024`](decisions/ADR-0024-post-authorization-pre-dispatch-action-commit.md)

Research pass:

- [`../research/literature/DU-24-action-boundary-landscape-2026-08.md`](../research/literature/DU-24-action-boundary-landscape-2026-08.md)

Главные результаты:

```text
SelectedActionIntent
≠ AuthorizedAction
≠ Action Commit
≠ Dispatch
≠ Execution
≠ Environment Transition
≠ Outcome Commit
```

- обязательная `Action Boundary` отделяет Policy selection от внешнего воздействия;
- базовый `Action Gate` является invariant agent-runtime boundary, а не второй Policy;
- Gate проверяет schema/freshness/capability/preconditions/explicit constraints;
- hidden evaluator/Environment Ground Truth не используется normal authorization способом;
- default Gate может accept/reject и выполнять только semantics-preserving normalization;
- behavior-changing substitution допускается только через explicit `ActionOverridePolicy`/runtime-assurance stage;
- override сохраняет исходный Policy intent и отдельную external/intervention provenance;
- `Action Commit` происходит после финальной authorization и до dispatch;
- после commit semantic action не меняется задним числом;
- dispatch/execution failure не удаляет `ActionCommitRecord`;
- `definitely_not_sent`, `execution_unknown`, Environment `no_effect` и partial execution различаются;
- retry того же logical dispatch использует стабильный `dispatch_id` и не создаёт новый Action Commit;
- blind retry запрещён при неизвестном выполнении non-idempotent action;
- universal physical exactly-once не обещается;
- synchronous MicroWorld может дать stronger dedup semantics по `action_commit_id`;
- dispatcher/transport принадлежат Execution Runtime integration, Environment владеет фактическим transition/outcome;
- terminal outcome фиксируется до reset;
- causal trace связывает candidate → intent → authorization → commit → dispatch → execution → transition → outcome.

---

# 4. Следующий допустимый Design Update

```text
DU-25 — Experience / Data / Replay
```

Цель `DU-25` — спроектировать **каноническую схему опыта и данных MINDRA**, которая сможет сохранять полную причинную историю interaction/cognition/training evidence без смешивания Agent Memory, research trajectory и Training Replay.

Обязательные вопросы:

```text
Experience Event / Transition / Trajectory hierarchy
natural ≠ replayed ≠ imagined ≠ intervened ≠ counterfactual
Action candidate / intent / commit / dispatch / outcome linkage
state_revision / agent_revision / memory/world/self revisions
Environment manifest / episode / decision identities
module/wave/executive/planner evidence refs
what belongs in canonical dataset vs heavy artifacts
agent-visible vs evaluator-only fields
Training sample ≠ raw experience record
Replay sample provenance
sequence/window extraction
terminal/truncated transitions
failed dispatch / execution_unknown / no-transition records
online collection under changing agent revisions
schema/version compatibility
compression/storage tiers
privacy/security boundaries if external data later appears
deterministic sampling / RNG
snapshot links
intervention links
quality/completeness flags
```

Нужно особенно определить:

- является ли canonical experience event-sourced log, transition table или гибрид;
- как из causal event stream получать RL-like transition samples без потери промежуточных MINDRA events;
- как не смешать `Agent Memory Replay` из `DU-20` с `Training Replay`;
- как хранить committed action, если dispatch не привёл к Environment Transition;
- как представить `execution_unknown` и partial execution;
- как сохранить evaluator-only ground truth для анализа, не делая его agent-visible training input автоматически;
- как dataset знает, какая `agent_revision`, policy/world/self/memory revision породила каждый action;
- какие минимальные поля обязательны для causal replay и какие могут быть optional/heavy artifacts;
- как extraction/relabeling/hindsight создаёт **derived training sample**, не переписывая source experience.

После принятия `DU-25` допускается:

```text
DU-26 — Training Lifecycle
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

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