# DU-22 — Metacognitive / Executive Control: research pass 2026-08

## Статус

**Дата:** 2026-08-17  
**Тип:** non-canonical research evidence  
**Связанный Design Update:** `DU-22 — Metacognitive / Executive Control`

Этот документ фиксирует актуальные исследовательские ориентиры, использованные при проектировании `DU-22`.

Он **не выбирает** canonical controller algorithm, training objective, resource units или конкретную LLM.

---

# 1. Исследовательский вопрос

Нужно понять, есть ли основания выделять отдельную функциональную boundary, которая решает:

```text
что ещё вычислить?
сколько compute выделить?
когда остановиться?
какую optional capability вызвать?
```

при этом не смешивая:

```text
execution safety/scheduling
final action policy
self-assessment
salience
workspace
```

---

# 2. Adaptive Computation Time

## Alex Graves — Adaptive Computation Time for Recurrent Neural Networks

- arXiv: `1603.08983`
- https://arxiv.org/abs/1603.08983

Работа показывает, что количество внутренних вычислительных steps может быть **адаптивной переменной**, зависящей от сложности input, а не фиксированным архитектурным числом.

Для MINDRA важен не конкретный differentiable halting mechanism, а общий инженерный принцип:

```text
same architecture
+ different situation
→ different computation depth
```

Ограничение переноса:

- ACT работает внутри конкретной recurrent neural architecture;
- MINDRA управляет более широким набором heterogeneous operations: Cortex, retrieval, rollout, consolidation, cycles;
- поэтому ACT не является direct Executive implementation.

---

# 3. PonderNet

## Banino, Balaguer, Blundell — PonderNet: Learning to Ponder

- arXiv: `2107.05407`
- https://arxiv.org/abs/2107.05407

PonderNet продолжает идею learned adaptive computation и явно оптимизирует trade-off между task performance и computational cost.

Для MINDRA это поддерживает гипотезу:

> stopping/continuation может быть learned decision и должен оцениваться вместе с compute cost.

Но MINDRA не принимает PonderNet halting distribution или loss как canonical mechanism.

---

# 4. Value of Computation / metareasoning

## Can Eren Sezener — Computing the Value of Computation for Planning

- arXiv: `1811.03035`
- https://arxiv.org/abs/1811.03035

Работа формализует различие между внешними actions и **internal computations**, ценность которых возникает опосредованно: computation полезна, если улучшает последующее решение достаточно, чтобы оправдать стоимость.

Это непосредственно поддерживает разделение MINDRA:

```text
Internal MetaAction
≠
Environment Action
```

и мотивирует отдельный decision problem:

```text
expected decision improvement
vs
compute cost
```

Но один scalar Value-of-Computation не принимается как universal representation: MINDRA имеет multi-dimensional resources, constraints, uncertainty и heterogeneous operations.

---

# 5. Rational Metareasoning for LLMs

## De Sabbata, Sumers, Griffiths — Rational Metareasoning for Large Language Models

- arXiv: `2410.05563`
- https://arxiv.org/abs/2410.05563

Работа рассматривает reasoning itself как costly computation и обучает selective use промежуточного reasoning, используя reward, учитывающий unnecessary reasoning cost.

Авторы сообщают снижение generated reasoning tokens при сохранении task performance на нескольких задачах.

Для MINDRA это evidence, что:

- reasoning depth не обязан быть фиксирован;
- over-computation является реальной инженерной проблемой;
- control нужно оценивать по performance/cost frontier, а не только accuracy.

Ограничение:

- работа сфокусирована на reasoning tokens внутри LLM;
- Executive MINDRA должен выбирать между разными subsystem operations, а не только длиной CoT.

---

# 6. MUSE: monitoring отдельно от strategy regulation

## Valiente, Pilly — Metacognition for Unknown Situations and Environments (MUSE)

- arXiv: `2411.13537`
- https://arxiv.org/abs/2411.13537

MUSE рассматривает metacognition как комбинацию:

```text
competence awareness
+
strategy selection / self-regulation
```

Это хорошо поддерживает уже принятое в MINDRA разделение:

```text
Self Model
→ competence monitoring

Executive Control
→ regulation
```

MINDRA при этом не копирует конкретную архитектуру MUSE и сохраняет отдельные ownership boundaries World/Self/Executive.

---

# 7. Adaptive tool use через metacognitive trigger

## Li et al. — Adaptive Tool Use in Large Language Models with Meta-Cognition Trigger

- arXiv: `2502.12961`
- https://arxiv.org/abs/2502.12961

Работа показывает practical pattern:

```text
self-assessment / cognitive signal
→ decide whether tool call is needed
```

Это близко к будущим операциям MINDRA:

```text
competence/uncertainty evidence
→ разрешить или не разрешить Cortex/retrieval/other optional capability
```

Но в MINDRA tool invocation не будет direct output Self Model: Self Model остаётся monitor/evidence provider, Executive — controller.

---

# 8. MetaCogAgent

## Wang, Shu — MetaCogAgent: A Metacognitive Multi-Agent LLM Framework with Self-Aware Task Delegation

- arXiv: `2605.17292`
- https://arxiv.org/abs/2605.17292

Работа использует historical capability profiles + self-assessment для task delegation и показывает пользу competence-aware routing относительно нескольких baselines.

Для MINDRA важен общий принцип:

```text
capability/competence profile
→ control/routing decision
```

Но:

- MINDRA не является multi-agent routing framework;
- self-assessment остаётся отдельным Self Model;
- Executive выбирает internal operations, а не назначает задачи другим LLM-agents.

---

# 9. Adaptive test-time compute 2026

## Zhai et al. — Adaptive Test-Time Compute Allocation for Reasoning LLMs via Constrained Policy Optimization

- arXiv: `2604.14853`
- https://arxiv.org/abs/2604.14853

Работа формализует allocation inference compute под ограниченным средним budget и показывает преимущество adaptive allocation над uniform/heuristic baselines на reasoning tasks.

Для MINDRA особенно важны:

- **budget constraint должен быть explicit**;
- performance нужно сравнивать при matched resource;
- learned allocation policy можно отделить от underlying reasoner.

MINDRA не принимает их constrained optimization method как canonical controller.

---

# 10. Uncertainty-aware budget allocation

## Nguyen, Gupta, Le — Uncertainty-Aware Budget Allocation for Adaptive Test-Time Reasoning

- arXiv: `2605.26849`
- https://arxiv.org/abs/2605.26849

Работа распределяет дополнительный sampling budget в зависимости от per-question uncertainty и показывает, что uniform allocation неэффективна при ограниченном compute.

Для MINDRA это поддерживает causal hypothesis:

```text
relevant uncertainty differs
→ optimal compute allocation may differ
```

Но MINDRA не считает uncertainty достаточным единственным control signal: competence, cost, capability, risk, urgency и expected benefit могут расходиться.

---

# 11. Adaptive stopping / overthinking

## Li et al. — Stop When Further Reasoning Won't Help: Attention-State Adaptive Generation in Reasoning Models

- arXiv: `2606.15070`
- https://arxiv.org/abs/2606.15070

Работа исследует early stopping reasoning models и показывает, что чрезмерное reasoning может быть не только дорогим, но иногда ухудшать accuracy.

Для MINDRA это дополнительно мотивирует отдельный stop/continue control point.

Ограничение:

- attention-state конкретной LLM не становится canonical Executive evidence;
- backend-specific signals могут использоваться только через explicit validated adapter/probe.

---

# 12. Основные выводы для архитектуры

Research landscape поддерживает следующие design conclusions.

## 12.1. Adaptive computation — реальная функция

Есть устойчивая линия исследований от ACT/PonderNet до test-time compute allocation, где разные inputs получают разный compute.

Следовательно, fixed cycle count не следует считать единственно естественной архитектурой.

## 12.2. Monitoring и regulation стоит различать

MUSE/MetaCogAgent/tool-use работы поддерживают использование competence/uncertainty evidence для downstream control.

Это согласуется с:

```text
Self Model ≠ Executive Control
```

## 12.3. Compute должен иметь explicit cost/budget semantics

Практически все adaptive-compute методы оцениваются относительно ограниченного resource или trade-off performance/cost.

Следовательно, claim:

> Executive улучшил performance

недостаточен без matched resource accounting.

## 12.4. One-signal control слишком узок

Confidence/uncertainty threshold может быть полезным baseline, но MINDRA имеет heterogeneous operations и multi-dimensional constraints.

Поэтому canonical design не фиксирует один scalar trigger.

## 12.5. Internal computation не равно external action

Metareasoning literature прямо мотивирует отдельную ценность/стоимость computation, которая влияет на качество последующего behavior.

Это поддерживает отдельный `Internal MetaAction` contract.

---

# 13. Кандидаты для будущей реализации

На version-design этапе можно отдельно сравнить:

```text
fixed schedule
simple confidence threshold
uncertainty threshold
rule-based cost/benefit policy
Value-of-Computation estimator
small learned router/controller
supervised imitation of oracle allocation
RL/constrained-RL controller
hybrid rule + learned policy
```

Ни один кандидат не является accepted до конкретного version design/experiment plan.

---

# 14. Обязательные controls из research pass

```text
Adaptive Executive
vs fixed equal-budget schedule
vs random allocation
vs simple threshold
vs uncertainty-only
vs cost-unaware
vs matched learned router
```

Нужно строить:

```text
performance
vs
actual compute/resource
```

а не сравнивать adaptive system с более дешёвым baseline без компенсации.

---

# 15. Открытые вопросы для DU-26/28

Этот pass не решает:

- как обучать Executive controller;
- как получить unbiased oracle allocation labels;
- какие proper metrics использовать для expected benefit/value of computation;
- как учитывать provider monetary cost;
- как normalise heterogeneous resource dimensions;
- как предотвращать reward hacking control policy;
- как оценивать long-term effects дополнительного cognition;
- как строить MINDRA-Eval задачи, где adaptive compute действительно необходим.

Эти вопросы остаются downstream.
