# DU-23 — Policy / Planner: research pass 2026-08

## Статус

**Дата:** 2026-08-17  
**Тип:** non-canonical research evidence  
**Связанный Design Update:** `DU-23 — Policy / Planner`

Этот документ фиксирует исследовательские ориентиры, использованные при проектировании `DU-23`.

Он **не выбирает** canonical Planner algorithm, Policy architecture, action representation, value scalarization или training objective.

---

# 1. Исследовательский вопрос

Нужно определить, как разделить:

```text
prediction / imagination
planning / search
candidate generation
valuation
final behavioral selection
actual action execution
```

и нужен ли Planner как отдельная boundary поверх обязательной Policy responsibility.

---

# 2. MuZero — planning с learned model

## Schrittwieser et al. — Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model

- arXiv: `1911.08265`
- https://arxiv.org/abs/1911.08265

MuZero показывает, что сильное behavior может сочетать:

```text
learned model
+
tree search/planning
+
policy/value predictions
```

при этом learned model не обязан reconstruct всю физическую среду; достаточно представлять quantities, полезные для planning.

Для MINDRA это evidence, что:

- planning может быть отдельной online computation;
- learned World Model и Planner могут взаимодействовать без полного symbolic simulator;
- search output/root policy не обязан совпадать с raw network policy.

Ограничение переноса:

- MuZero тесно объединяет model/policy/value/search в конкретном RL algorithm;
- MINDRA намеренно разводит World Model, Valuation, Policy и Planner для ablation/intervention.

---

# 3. DreamerV3 — policy через imagined futures без explicit tree planner

## Hafner et al. — Mastering Diverse Domains through World Models

- arXiv: `2301.04104`
- https://arxiv.org/abs/2301.04104

DreamerV3 обучает behavior на imagined latent trajectories World Model и показывает, что model-based control не обязан использовать explicit MCTS/graph search на каждом action.

Для MINDRA это важно как контрпример тезису:

> «Если есть World Model, обязательно нужен отдельный explicit Planner».

Dreamer-подобная architecture может иметь:

```text
World Model
→ imagined training/evaluation evidence
→ learned Policy
```

без отдельного online Planner.

Поэтому `NoPlanner / Reactive-or-direct Policy` должен быть first-class configuration.

---

# 4. TD-MPC2 — online trajectory optimization в learned latent model

## Hansen, Su, Wang — TD-MPC2: Scalable, Robust World Models for Continuous Control

- arXiv: `2310.16828`
- https://arxiv.org/abs/2310.16828

TD-MPC2 использует local trajectory optimization в latent space learned world model.

Для MINDRA это evidence в пользу interface:

```text
World Model prediction primitive
+
separate planning/search procedure
→ action candidate
```

Также TD-MPC2 подчёркивает practical value receding/local planning: action можно выбирать после локального horizon search и затем replanning делать после нового actual observation.

Но TD-MPC2 не принимается как canonical Planner.

---

# 5. POMCP — planning в belief space при partial observability

## Silver, Veness — Monte-Carlo Planning in Large POMDPs

- NeurIPS 2010
- https://proceedings.neurips.cc/paper/2010/hash/edfbe1afcf9246bb0d40eb4d8027d90f-Abstract.html

POMCP сочетает belief-state update и Monte-Carlo tree search для online planning в large POMDPs.

Для MINDRA особенно важен общий принцип:

```text
partial observability
→ plan/search относительно belief/history
→ contingent next action
```

а не hidden ground truth.

Это поддерживает boundary:

```text
World Belief
→ Planner
```

и conditional plans по будущим observations.

MINDRA не принимает POMCP algorithm/UCT как обязательный implementation.

---

# 6. Decision Transformer — полноценное behavior без explicit Planner

## Chen et al. — Decision Transformer: Reinforcement Learning via Sequence Modeling

- arXiv: `2106.01345`
- https://arxiv.org/abs/2106.01345

Decision Transformer формулирует behavior generation как conditional sequence modeling и напрямую генерирует actions по history/desired-return context без explicit online search tree.

Для MINDRA это дополнительное evidence, что:

- Policy semantic responsibility не должна зависеть от наличия Planner;
- concrete Policy может быть sequence-model/recurrent/neural;
- Planner должен оставаться optional capability.

MINDRA при этом не принимает return-to-go как universal Goal/Valuation representation.

---

# 7. Tree of Thoughts — explicit branching поверх LLM

## Yao et al. — Tree of Thoughts: Deliberate Problem Solving with Large Language Models

- arXiv: `2305.10601`
- https://arxiv.org/abs/2305.10601

Tree of Thoughts показывает practical pattern:

```text
candidate intermediate states/thoughts
→ branching search
→ evaluation
→ backtracking / path selection
```

Для MINDRA это evidence, что Cortex-assisted Planner может использовать LLM для candidate generation/semantic search, а не только `generate one answer`.

Но:

- ToT search space — textual reasoning, не Environment action space;
- self-evaluation LLM не становится canonical Valuation;
- search result всё равно должен пройти Policy boundary.

---

# 8. RAP — reasoning via planning

## Hao et al. — Reasoning with Language Model is Planning with World Model

- arXiv: `2305.14992`
- https://arxiv.org/abs/2305.14992

RAP использует LLM и как reasoning agent, и как world-model-like simulator внутри MCTS-style planning.

Для MINDRA важен general pattern:

```text
semantic candidate generation
+
state transition prediction
+
search
```

может быть эффективен для compositional reasoning.

Но MINDRA намеренно **не** объединяет Cortex и World Model по умолчанию: RAP является candidate backend strategy для конкретного Planner/Cortex configuration, а не architecture owner.

---

# 9. SayCan — semantic proposal отдельно от feasibility grounding

## Ahn et al. — Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

- arXiv: `2204.01691`
- https://arxiv.org/abs/2204.01691

SayCan сочетает semantic high-level proposals LLM с grounded skill/value evidence реального embodied agent.

Для MINDRA это поддерживает идею:

```text
Cortex semantic proposal
≠
automatically executable/selectable action
```

Semantic candidate должен быть grounded через agent capabilities/World/Self/Valuation и только затем участвовать в Policy selection.

MINDRA не принимает SayCan skill-value multiplication как universal selection rule.

---

# 10. Hierarchical DQN — temporal abstraction и subgoals

## Kulkarni et al. — Hierarchical Deep Reinforcement Learning: Integrating Temporal Abstraction and Intrinsic Motivation

- arXiv: `1604.06057`
- https://arxiv.org/abs/1604.06057

h-DQN разделяет high-level goal/subgoal decisions и low-level actions на разных temporal scales.

Для MINDRA это evidence, что planning/hierarchical control может использовать subgoals как отдельные semantic objects.

Но MINDRA сохраняет принятый ownership:

```text
Planner → Goal Proposal → Goal System
```

а не direct mutation Goal Graph.

---

# 11. Receding horizon / adaptive horizon

## Bøhn et al. — Reinforcement Learning of the Prediction Horizon in Model Predictive Control

- arXiv: `2102.11122`
- https://arxiv.org/abs/2102.11122

Работа показывает, что prediction horizon MPC сам по себе создаёт performance/compute trade-off и может адаптироваться к state.

Для MINDRA важно разделение:

```text
Executive
→ сколько planning resource/horizon разрешить

Planner
→ как использовать этот horizon/search budget
```

и receding-horizon principle:

```text
plan
→ execute/select first action intention
→ observe actual outcome
→ replan/revalidate
```

Конкретный MPC horizon algorithm не принимается.

---

# 12. Safe POMDP planning / shielding как boundary evidence

## Sheng, Parker, Feng — Safe POMDP Online Planning via Shielding

- arXiv: `2309.10216`
- https://arxiv.org/abs/2309.10216

Работа интегрирует safety shields с online POMDP planning и показывает, что planning objective и отдельное action admissibility/safety restriction могут существовать раздельно.

Для MINDRA это поддерживает будущую границу:

```text
Policy SelectedActionIntent
≠
DU-24 Action Gate approval
```

`DU-23` не переносит shielding algorithm в Policy.

---

# 13. Основной вывод для MINDRA

Исследовательский landscape поддерживает не один «правильный Planner», а несколько функционально разных архитектур:

```text
reactive/direct Policy
world-model-trained Policy
online MPC/trajectory optimization
MCTS/tree/graph search
belief-space planning
LLM-assisted branching planning
hierarchical/subgoal planning
```

Поэтому semantic architecture должна фиксировать **границы и outputs**, а не конкретный planning algorithm.

Главный вывод `DU-23`:

```text
Policy owner final behavioral intention
+
Planner optional provider plan/action candidates
+
World Model prediction primitive
+
Valuation comparison evidence
+
Executive planning-resource control
```

---

# 14. Что не следует из research evidence

Эти работы не доказывают, что:

- Planner обязателен для MINDRA;
- MCTS лучше MPC для MicroWorld;
- Cortex должен быть Planner;
- World Model должна выдавать reward/value;
- final action обязан быть `argmax`;
- explicit plan всегда лучше learned reactive policy;
- planning означает сознательное рассуждение;
- больше search compute автоматически означает более сильный architecture contribution.

Эти вопросы должны проверяться экспериментально с matched controls.
