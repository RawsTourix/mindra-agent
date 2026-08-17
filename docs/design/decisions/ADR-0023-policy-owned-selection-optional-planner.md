# ADR-0023 — Policy-owned final behavioral selection с optional Planner provider

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-23 — Policy / Planner`

---

# 1. Контекст

После `DU-12/18/22` MINDRA имеет:

- World Model для belief/prediction/imagination;
- Valuation для structured value/risk/constraint comparison;
- Executive Control для optional cognitive resource allocation.

Но отсутствует canonical owner финального behavioral choice перед будущей Action Gate boundary.

Нужно решить:

- является ли Policy отдельной responsibility;
- нужен ли отдельный Planner;
- кто владеет final selected-action intention;
- как Planner связан с World Model;
- как использовать Valuation, не превращая её в selector;
- как сохранять reactive baseline;
- как обрабатывать partial observability, incomparability и replanning.

---

# 2. Рассмотренные варианты

1. `Valuation argmax` непосредственно выбирает action;
2. Planner является owner планирования и final action selection;
3. один monolithic Policy/Planner module;
4. только reactive Policy, Planner отсутствует архитектурно;
5. обязательный Policy owner + optional Planner как provider plan/action candidates.

---

# 3. Требования

Решение должно:

- иметь единственный owner selected behavioral intention;
- сохранять `Valuation ≠ Policy Decision`;
- сохранять `World Model ≠ Planner`;
- сохранять `Executive ≠ Policy`;
- отделять selected intention от execution/Action Commit;
- поддерживать reactive behavior без Planner;
- поддерживать explicit multi-step/contingent planning;
- поддерживать partial observability через World Belief;
- не давать Planner мутировать Goal Graph;
- сохранять Cortex как optional helper;
- поддерживать stochastic selection;
- поддерживать matched controls и отрицательный Planner gate;
- не фиксировать конкретный search/Policy algorithm.

---

# 4. Вариант A — Valuation напрямую выбирает action

Conceptually:

```text
ValueProfile[]
→ argmax / preferred
→ selected action
```

## Плюсы

- мало компонентов;
- простая реализация.

## Минусы

- нарушает `DU-18`: Valuation должна сохранять incomparability и structured evidence;
- Policy-specific exploration/tie-break/deferral semantics исчезают;
- constraints и incomplete ordering скрыто превращаются в scalar selection;
- невозможно независимо тестировать качество valuation и selection.

**Решение:** отклонён.

---

# 5. Вариант B — Planner владеет и планом, и final action selection

## Плюсы

- естественно для классических online planners;
- меньше handoff между subsystems;
- search может сразу вернуть root action.

## Минусы

- reactive/no-planner configuration теряет общий selection owner;
- difficult ablation: отключение Planner одновременно удаляет и planning, и selection semantics;
- Planner начинает поглощать Policy;
- Cortex/search-specific implementation легко становится canonical behavior owner;
- сравнение Planner vs Reactive Policy становится нечистым.

**Решение:** отклонён как canonical ownership.

Planner может выдавать рекомендуемый root action/candidate, но final `SelectedActionIntent` создаёт Policy.

---

# 6. Вариант C — Monolithic Policy/Planner

## Плюсы

- совместное обучение;
- можно скрыть planning внутри network;
- меньше interface overhead.

## Минусы

- невозможно различить reactive и planning contribution;
- World Model search, candidate generation и final selection становятся трудно наблюдаемыми;
- `NoPlanner`/matched controls усложняются;
- plan persistence/subgoal/Cortex dependencies могут протечь в final Policy boundary;
- implementation architecture начинает определять semantic architecture.

**Решение:** отклонён как canonical boundary.

Concrete implementation может совместно обучать Policy/Planner backend, но semantic outputs/responsibilities должны оставаться различимыми.

---

# 7. Вариант D — Только Reactive Policy

## Плюсы

- минимальная архитектура;
- быстрый inference;
- сильный обязательный baseline;
- model-free/direct policies являются полноценным классом решений.

## Минусы

- нет explicit long-horizon search;
- contingent planning не имеет отдельной representation;
- трудно исследовать model-based planning causal contribution;
- сложнее повторно использовать plan across decisions.

**Решение:** отклонён как единственная architecture, но принят как first-class `NoPlanner` baseline.

---

# 8. Вариант E — Policy owner + optional Planner provider

Conceptually:

```text
Reactive candidate source ─┐
Planner ───────────────────┤
Cortex-assisted source ────┤
Control source ────────────┘
            ↓
    PolicyCandidateSet
            ↓
       Valuation
            ↓
        Policy
            ↓
 SelectedActionIntent
```

Planner:

```text
Goals + WorldBelief + planning budget
→ search / rollout / plan construction
→ PlanCandidate / ActionCandidate
```

## Плюсы

- единый final selection owner при любых configurations;
- Planner можно отключить независимо;
- planning contribution причинно тестируем;
- World Model остаётся prediction primitive;
- Valuation остаётся evaluation boundary;
- Planner может быть symbolic, neural, search-based или Cortex-assisted;
- reactive/direct Policy остаётся first-class;
- Action Gate остаётся downstream.

## Минусы

- больше semantic objects/handoffs;
- возможна дубликация candidate generation;
- требуется явная stale-plan/candidate handling;
- Policy должна корректно обрабатывать heterogeneous candidate sources.

**Решение:** принято.

---

# 9. Принятое решение

MINDRA принимает:

1. **Policy System как обязательный semantic owner final behavioral selection**;
2. **Planner как optional/falsifiable provider** explicit `PlanCandidate`/`ActionCandidate`;
3. `SelectedActionIntent` как Policy output до `DU-24`;
4. `DecisionDeferral` как explicit result, если выбор требует дополнительного cognition;
5. plan/search compute контролируется Executive budget semantics;
6. World Model предоставляет predictions/rollouts, но не владеет Plan;
7. Valuation предоставляет comparison evidence, но не владеет selection;
8. Planner-generated subgoal проходит обычный Goal Proposal boundary.

Канонические отношения:

```text
Policy ≠ Planner
Planner ≠ World Model
Plan ≠ ImaginedTrajectory
Valuation ≠ Policy Decision
Executive Control ≠ Policy
ActionCandidate ≠ SelectedActionIntent
SelectedActionIntent ≠ Action Commit / Executed Action
```

---

# 10. Partial observability

Planning normal runtime способом строится относительно `World Belief`, а не hidden Environment state.

Planner может строить contingent plans по будущим observations/beliefs.

Oracle hidden-state planning допускается только как explicit research control.

---

# 11. Incomparability и deferral

Policy не обязана scalarize `incomparable` candidates.

Допустимы:

- explicit tie-break policy;
- stochastic/exploratory choice;
- constraint-first rule;
- `DecisionDeferral` + `MetaActionProposal` дополнительного cognition;
- explicit fallback после budget exhaustion.

Возврат к Executive идёт через lifecycle/control point, а не direct recursion.

---

# 12. Planner persistence

Planner может поддерживать `PlanState` между Decision Windows.

Plan обязан сохранять base revisions/assumptions и иметь stale/invalidation semantics.

Replanning является explicit optional computation и может требовать Executive allocation.

---

# 13. Module gate Planner

Planner остаётся conditional boundary.

Future evaluation должна сравнивать минимум:

```text
Policy + Planner
vs ReactivePolicy / NoPlanner
vs Depth1 / fixed lookahead
vs Random/Shuffled plans
vs Matched search/recurrent control
```

при matched actual compute/resource настолько, насколько возможно.

Если Planning benefit объясняется только дополнительным compute/state capacity или не проявляется на long-horizon/contingent tasks, Planner boundary пересматривается.

---

# 14. Последствия

## Положительные

- чистый owner final choice;
- Planner заменяем и отключаем;
- explicit causal trail candidate → plan → valuation → selection;
- partial observability planning совместима с World Belief;
- Action Gate остаётся независимой;
- Cortex и neural search не протекают в canonical ownership.

## Отрицательные

- больше contracts/metadata;
- необходимо stale candidate/plan management;
- Policy selection должна поддерживать heterogeneous evidence;
- future implementation потребует аккуратной compute accounting между Executive и Planner.

---

# 15. Не фиксируется ADR-0023

Не выбраны:

- neural Policy architecture;
- MCTS;
- MPC;
- POMCP;
- beam search;
- Tree of Thoughts/RAP;
- Decision Transformer;
- deterministic/stochastic selection algorithm;
- candidate count;
- plan graph representation;
- horizon;
- value scalarization;
- exact Python API;
- training loss.

---

# 16. Условие пересмотра

ADR должен быть пересмотрен, если future experiments показывают, что:

- отдельный Planner не даёт специфического выигрыша против matched reactive/search controls;
- Policy/Planner separation создаёт cost без диагностического/causal преимущества;
- alternative architecture лучше сохраняет ownership и experimental identifiability;
- downstream `DU-24/25/26` выявляет несовместимый semantic conflict.
