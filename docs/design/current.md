# Текущее состояние проектирования MINDRA

## Назначение

Краткий фактический статус проекта. Этот файл не переопределяет canonical design; он определяет, что уже принято и какой следующий Design Update допустим.

---

# 1. Общий статус

**`DU-01 … DU-23` завершены и приняты. Реализация ещё не начата.**

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
- 23 accepted ADR;
- candidate semantic contracts для subsystem boundaries `DU-07 … DU-23`.

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
```

---

# 3. DU-23

Canonical design:

- [`modules/policy-planner.md`](modules/policy-planner.md)

Candidate contract:

- [`contracts/policy-planner.md`](contracts/policy-planner.md)

Accepted decision:

- [`ADR-0023`](decisions/ADR-0023-policy-owned-selection-optional-planner.md)

Research pass:

- [`../research/literature/DU-23-policy-planner-landscape-2026-08.md`](../research/literature/DU-23-policy-planner-landscape-2026-08.md)

Главные результаты:

```text
Policy ≠ Planner
Planner ≠ World Model
Plan ≠ ImaginedTrajectory
Valuation ≠ Policy Decision
Executive Control ≠ Policy
ActionCandidate ≠ SelectedActionIntent
SelectedActionIntent ≠ Action Commit / Executed Action
```

- `Policy System` принят как обязательный semantic owner final behavioral selection;
- `Planner` принят как optional/falsifiable provider планов/action candidates;
- reactive/no-Planner Policy остаётся first-class configuration;
- Planner использует `World Belief`, а не hidden Environment state;
- Planner может строить contingent plans по будущим observations/beliefs;
- World Model предоставляет prediction/imagination primitives, но не владеет Plan;
- `Plan` является agent-owned prescriptive/conditional structure и не равен одному rollout;
- candidate generation допускает reactive, Planner, Cortex-assisted, scripted/control и другие explicit sources;
- все sources входят в explicit `PolicyCandidateSet`;
- Valuation предоставляет `ValueProfile`/`ComparisonResult`, но final selection остаётся Policy;
- `incomparable` является валидным состоянием и не требует fake scalarization;
- Policy может вернуть `DecisionDeferral` + `MetaActionProposal`, если требуется дополнительное cognition;
- возврат к Executive происходит через lifecycle/control point, не recursive direct call;
- Planner-generated subgoal проходит `Goal Proposal → Goal System`;
- planning compute/horizon/branching ограничиваются Executive resource semantics;
- Planner может хранить `PlanState`, но plan имеет revision/assumptions/stale/invalidation/replanning semantics;
- `SelectedActionIntent` является результатом Policy до Action Gate и не означает, что action уже разрешён/committed/executed;
- stochastic Policy должна сохранять selection/RNG provenance;
- обязательны ReactivePolicy/NoPlanner, random/shuffled/depth-1/matched search controls;
- benefit Planner должен проверяться при matched actual compute и на задачах, действительно требующих multi-step/contingent planning;
- если matched controls объясняют эффект, отдельная Planner boundary должна быть пересмотрена.

---

# 4. Следующий допустимый Design Update

```text
DU-24 — Action Boundary / Gate / Executor
```

Цель `DU-24` — спроектировать **границу между выбранным Policy намерением, проверкой/разрешением action, причинным `Action Commit`, dispatch в Environment и фактически наблюдаемым outcome**.

Обязательные вопросы:

```text
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit ≠ Dispatch ≠ Executed Action ≠ Outcome
Action Gate responsibility/module gate
semantic action validation
capability/availability checks
stale selected intent
final precondition validation
hard constraints / safety-policy boundary без evaluator oracle leakage
Action rejection / modification / substitution semantics
who may transform an intent
NoOp / abort / retry semantics
Action Commit exact point
idempotency / duplicate dispatch
Environment acknowledgement
partial execution / execution failure
asynchronous dispatch boundary?
termination/truncation interaction
action/outcome correlation IDs
observability/intervention
Action Gate controls
snapshot/revision
```

Нужно особенно определить:

- где именно находится канонический `Action Commit` из `DU-03`;
- кто имеет authority превратить `SelectedActionIntent` в действие, допустимое для Environment adapter;
- может ли Gate изменить действие или только accept/reject, и как это отражается в provenance;
- как не использовать hidden evaluator/Environment Ground Truth как обычный safety oracle;
- как stale intent обнаруживается после изменения state/action capability;
- как различить malformed action, semantically invalid action, rejected action, dispatch failure и Environment-level no-effect;
- как избежать двойного выполнения при retry/transport error;
- как terminal outcome сохраняется до reset;
- какой causal evidence нужен для связи `intent → authorization → commit → dispatch → outcome`.

После принятия `DU-24` допускается:

```text
DU-25 — Experience / Data / Replay
```

---

# 5. Ещё не приняты

Пока отсутствуют accepted решения по:

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
