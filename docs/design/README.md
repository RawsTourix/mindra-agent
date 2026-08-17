# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь фиксируются принятые семантики, invariants, границы модулей, internal contracts, архитектурные решения и будущие version plans.

На текущем этапе сформирован documentation foundation и приняты `DU-01` … `DU-09`. Детальные subsystem design добавляются последовательно после отдельного исследования вариантов.

---

# 1. Иерархия

```text
Concept
→ Design semantics / invariants
→ ADR
→ Candidate / exact internal contracts
→ Version specification
→ Implementation sequence
→ Engineering/research acceptance evidence
```

Research evidence не переписывает design напрямую: противоречащий результат инициирует design review.

---

# 2. Текущая навигация

## Foundation

- [`principles.md`](principles.md) — устойчивые инженерные и исследовательские принципы;
- [`glossary.md`](glossary.md) — канонические значения терминов;
- [`documentation-plan.md`](documentation-plan.md) — канонический порядок `DU-00` … `DU-32`;
- [`current.md`](current.md) — фактический статус и следующий допустимый шаг.

## Canonical system design

- [`system-context.md`](system-context.md) — `DU-01`: логические границы Agent, Environment, training/evaluation infrastructure, artifact/storage/compute и разрешённые потоки данных;
- [`dependency-rules.md`](dependency-rules.md) — `DU-02`: dependency directions, Composition Root, dependency inversion, backend isolation и запрет runtime Service Locator/shared mutable globals;
- [`execution-model.md`](execution-model.md) — `DU-03`: иерархическое логическое время, Agent Session/Episode/Decision Window/Cognitive Cycle, causal commit boundaries, async semantics и replay requirements;
- [`cognitive-state.md`](cognitive-state.md) — `DU-04`: committed state snapshots, namespaces/ownership, availability/freshness, temporal scopes, provenance, private-state boundary и clone/counterfactual requirements;
- [`module-lifecycle.md`](module-lifecycle.md) — `DU-05`: module descriptors, declared reads/writes, DAG/wave scheduling, transactional public/private effects, lifecycle/failure semantics и граница будущего Executive Control;
- [`observability-and-intervention.md`](observability-and-intervention.md) — `DU-06`: passive Evidence Plane, causal tracing, private-state probes, observability depth, explicit Intervention Gateway, branch/provenance semantics и counterfactual requirements.

## Спроектированные subsystem boundaries

- [`modules/environment.md`](modules/environment.md) — `DU-07`: общий Environment contract, Agent Interaction Plane/Research Plane, hidden/raw/task/feedback boundaries, snapshot/clone/fork, procedural generation, distributions и reference `MicroWorld`;
- [`modules/perception.md`](modules/perception.md) — `DU-08`: Perception boundary, `Canonical Percept`, structured Semantic Core, optional Feature Views, entity/missingness semantics, representation versioning/drift и Cortex/no-Cortex independence;
- [`modules/goals.md`](modules/goals.md) — `DU-09`: Goal Proposal, Committed Goal, Goal Graph, lifecycle/scope, subgoal/dependency/conflict semantics, priority/commitment/progress и goal ownership.

## Карта модулей

- [`modules/README.md`](modules/README.md) — предварительная карта архитектурных областей, их responsibilities, различий и зависимостей.

Наличие области в карте не означает, что отдельный модуль уже принят. Соответствующий Design Update может объединить, разделить, отложить или отвергнуть кандидатную ответственность.

`Environment`, `Perception / Representation` и `Goal System` уже имеют accepted semantic design в отдельных документах; остальные области карты проектируются последовательно.

## Decision records

- [`decisions/README.md`](decisions/README.md);
- [`ADR-0001`](decisions/ADR-0001-logical-boundaries-independent-of-deployment.md) — logical responsibility boundary independent of deployment topology;
- [`ADR-0002`](decisions/ADR-0002-explicit-composition-no-runtime-service-locator.md) — explicit Composition Root и запрет runtime Service Locator;
- [`ADR-0003`](decisions/ADR-0003-hierarchical-logical-time.md) — hierarchical logical time и causal commit boundaries;
- [`ADR-0004`](decisions/ADR-0004-versioned-committed-cognitive-state.md) — versioned committed CognitiveState, staged owner-scoped updates и запрет hidden mutable bus semantics;
- [`ADR-0005`](decisions/ADR-0005-wave-scheduled-module-protocol.md) — declared DAG scheduling, execution waves и atomic public/private module commit;
- [`ADR-0006`](decisions/ADR-0006-separated-evidence-plane-and-intervention-gateway.md) — passive Evidence Plane отдельно от privileged Intervention Gateway;
- [`ADR-0007`](decisions/ADR-0007-two-plane-environment-boundary.md) — agent-visible Environment interaction отдельно от research-only world control/snapshot/intervention;
- [`ADR-0008`](decisions/ADR-0008-hybrid-canonical-percept.md) — structured Semantic Core + optional revisioned Feature Views вместо одного universal latent/Cortex hidden space;
- [`ADR-0009`](decisions/ADR-0009-committed-goal-graph.md) — Goal Proposal → Goal System → Committed Goal Graph; source capability не получает direct ownership Goal state.

## Candidate / exact internal contracts

- [`contracts/README.md`](contracts/README.md);
- [`contracts/environment.md`](contracts/environment.md) — candidate Environment capability/data contract после `DU-07`;
- [`contracts/perception.md`](contracts/perception.md) — candidate Perception/Canonical Percept contract после `DU-08`;
- [`contracts/goals.md`](contracts/goals.md) — candidate Goal System/Goal Graph contract после `DU-09`.

Candidate contracts определяют semantic machine-facing requirements, но exact Python API ещё не frozen.

## Versions

- [`versions/README.md`](versions/README.md).

---

# 3. Design Update discipline

`DU-xx` — идентификатор самостоятельного архитектурного documentation update, а не software version.

Каждый update должен:

- иметь prerequisites;
- закрывать ограниченный набор design questions;
- проводить targeted research там, где есть реальный выбор;
- фиксировать responsibilities/non-goals/invariants;
- создавать ADR при значимом выборе между вариантами;
- обновлять canonical owner темы;
- не протаскивать downstream decisions раньше времени;
- завершаться consistency review и обновлением `current.md`.

Канонический порядок: [`documentation-plan.md`](documentation-plan.md).

Текущий следующий update: `DU-10 — Cortex Boundary`.

---

# 4. Canonical owner

У значимой архитектурной темы должен быть один основной canonical owner.

Общий документ может ссылаться на тему, но не должен независимо определять вторую конкурирующую семантику.

Если ADR меняет принятое решение:

1. обновляется ADR registry;
2. обновляется canonical design owner;
3. обновляются exact/candidate contracts;
4. обновляются затронутые version plans/status;
5. только затем implementation следует новому решению.

---

# 5. Design для coding agents

Implementation-ready design должен минимизировать архитектурные догадки.

Для каждой будущей подсистемы желательно определить:

- назначение;
- responsibilities;
- non-goals;
- inputs/outputs;
- owned state;
- dependencies;
- lifecycle/update semantics;
- training signals;
- persistence/checkpoint semantics;
- observability;
- failure/degradation behavior;
- ablation/control strategy;
- evaluation metrics;
- open questions.

Если существенное решение ещё не принято, оно должно быть обозначено как open question/blocker, а не оставлено на усмотрение Codex.

---

# 6. Правило существования отдельного модуля

Когнитивная аналогия сама по себе не является основанием для нового module boundary.

Отдельный модуль должен иметь:

1. самостоятельную вычислительную ответственность;
2. явные input/output/state semantics;
3. независимый lifecycle или значимую границу обновления;
4. возможность отключения/подмены;
5. собственную diagnostic/evaluation strategy;
6. функциональную роль, не дублирующую соседний модуль.

Если эти условия не выполняются, design должен рассмотреть объединение ответственности.

---

# 7. Текущая граница

Приняты `DU-01` … `DU-09`, но пока не существует frozen exact module contract или version roadmap.

Канонически уже зафиксированы:

- logical architecture boundary не равна deployment topology;
- hidden concrete dependencies/runtime Service Locator запрещены;
- logical causal time не равно wall-clock;
- Cognitive Cycle не равно Environment Transition;
- `CognitiveState` является canonical shared runtime state, а не всем `Agent-owned state`;
- module execution следует declared DAG/wave semantics;
- passive observability отделена от active intervention;
- Environment Agent Interaction Plane отделён от research-only ground truth/control plane;
- `Raw Observation` не равен canonical internal representation;
- External Task Specification не равен internal Goal state;
- External Task Feedback, Objective Task Metric и Internal Utility различаются;
- `Canonical Percept` состоит из structured Semantic Core и optional Feature Views;
- один universal learned latent/Cortex hidden space не является canonical inter-module representation;
- Perception описывает current observation, а не Memory/World Model belief;
- learned feature spaces имеют identity/revision и могут drift;
- Goal отделён от reward, drives, value и Policy;
- `Goal Proposal` не равен `Committed Goal`;
- Goal System является semantic owner committed Goal state;
- несколько active goals допустимы;
- canonical goal structure является Goal Graph, а не обязательный LIFO stack;
- parent/subgoal/dependency/conflict relations имеют явную semantics;
- goal lifecycle различает pending/active/suspended и achieved/failed/abandoned/expired/invalidated states;
- goal scope может переживать Episode reset;
- structural goal priority отделена от future dynamic Valuation;
- commitment отделён от priority/value/focus;
- goal progress не обязан быть scalar `[0,1]` и не использует research-only metric скрыто;
- Cortex/Planner/Drives могут в будущем предлагать goals, но не получают direct Goal write authority.

Обсуждавшиеся ранее Qwen, TensorDict, PPO, Dreamer, RND, ICM, FAISS, PEFT/LoRA, Colab, OpenTelemetry, pyvene, Gymnasium, Slot Attention, GNN/Set Transformer/Perceiver и другие технологии являются кандидатами/evidence для будущего анализа, но не каноническими implementation requirements.

Фактический статус: [`current.md`](current.md).
