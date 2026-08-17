# Research pass — Self Model / metacognition landscape

## Статус

**Связанный Design Update:** `DU-13 — Self Model`  
**Дата среза:** 2026-08-17  
**Статус:** non-canonical research evidence

Этот документ фиксирует внешний исследовательский контекст, использованный при проектировании `DU-13`.

Он не выбирает concrete implementation Self Model и не переопределяет `docs/design/`.

---

# 1. Основные исследовательские вопросы

При проектировании проверялись следующие вопросы:

1. Достаточно ли natural-language self-report Cortex для self-knowledge?
2. Нужно ли отделять capability availability от competence?
3. Как измерять confidence/self-prediction calibration?
4. Имеет ли смысл context-conditioned competence вместо одного global score?
5. Следует ли отделять self-monitoring от self-regulation?
6. Как self-model должен реагировать на изменение собственной architecture/capabilities?

---

# 2. Calibration confidence

## On Calibration of Modern Neural Networks

Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger, 2017.  
`arXiv:1706.04599`

Ключевой вывод для MINDRA:

- confidence prediction нужно проверять на соответствие фактической частоте корректности;
- высокая accuracy не гарантирует calibration;
- calibration является отдельным свойством predictor.

Это поддерживает запрет использовать невалидированное verbal `confidence` как Self Model.

## Better Uncertainty Calibration via Proper Scores for Classification and Beyond

Sebastian G. Gruber, Florian Buettner, 2022.  
`arXiv:2203.07835`

Ключевой вывод:

- calibration metrics сами имеют статистические ограничения;
- proper scoring rules дают более устойчивую основу оценки вероятностных прогнозов, чем произвольная bin-based метрика как единственный критерий.

Для MINDRA это означает: exact Brier/NLL/ECE policy нельзя преждевременно закреплять в Self Model; это задача будущего `MINDRA-Eval`.

---

# 3. LLM metacognition и verbal confidence

## Improving Metacognition and Uncertainty Communication in Language Models

Mark Steyvers, Catarina Belem, Padhraic Smyth, 2025.  
`arXiv:2510.05126`

Работа показывает:

- explicit confidence LLM может быть плохо calibrated;
- calibration и discrimination можно улучшать отдельным supervision;
- разные metacognitive tasks не обязаны переноситься друг на друга автоматически.

Вывод для MINDRA:

> self-assessment является отдельной обучаемой capability, а не гарантированным свойством pretrained Cortex.

## Rewarding Doubt: A Reinforcement Learning Approach to Calibrated Confidence Expression of Large Language Models

Paul Stangel и др., 2025.  
`arXiv:2503.02623`

Работа демонстрирует возможность специально обучать LLM выдавать лучше calibrated confidence через scoring-rule-oriented objective.

Для MINDRA это evidence того, что calibration можно обучать, но concrete RL objective не становится canonical Self Model requirement.

---

# 4. Embodied confidence

## Uncertainty in Action: Confidence Elicitation in Embodied Agents

Tianjiao Yu и др., 2025.  
`arXiv:2503.10628`

Авторы исследуют confidence calibration в embodied multimodal setting и показывают, что self-confidence в действующей среде является отдельной проблемой, где uncertainty может исходить из perception, reasoning и action execution.

Вывод для MINDRA:

- self-prediction должна иметь context/target semantics;
- один global confidence плохо описывает competence embodied Agent;
- calibration должна оцениваться относительно реального outcome.

---

# 5. Competence awareness и self-regulation

## Metacognition for Unknown Situations and Environments (MUSE)

Rodolfo Valiente, Praveen K. Pilly, 2024.  
`arXiv:2411.13537`

MUSE разделяет два полезных для MINDRA аспекта:

- competence awareness;
- strategy selection/self-regulation.

Это напрямую поддерживает принятую границу:

```text
Self Model
→ оценивает competence

Executive Control
→ использует оценку для regulation
```

MUSE не принимается как concrete architecture MINDRA.

## MetaCogAgent: A Metacognitive Multi-Agent LLM Framework with Self-Aware Task Delegation

Chenyu Wang, Yang Shu, 2026.  
`arXiv:2605.17292`

Работа использует historical capability profiles и task-capability alignment для self-assessment перед делегированием задач.

Полезный вывод:

- competence profile может быть task/context-conditioned;
- self-assessment может причинно влиять на routing/strategy;
- historical performance evidence полезно отделять от текущего verbal confidence.

Multi-agent delegation не является требованием MINDRA.

---

# 6. Capability-boundary decisions

## Adaptive Tool Use in Large Language Models with Meta-Cognition Trigger

Wenjun Li и др., 2025.  
`arXiv:2502.12961`

Работа показывает практическую ценность отдельного metacognitive signal для решения, когда использовать внешний инструмент.

Для MINDRA это evidence будущей связи:

```text
Self Model
→ competence/limitation estimate
→ Executive Control
→ optional capability use
```

Но Self Model сама не должна принимать tool/compute decision.

---

# 7. Robotic self-modeling

## Self-Modeling Robots by Photographing

Kejun Hu, Peng Yu, Ning Tan, 2025.  
`arXiv:2503.05398`

Работа строит data-driven model собственной morphology/kinematics робота и использует её для downstream planning.

Для MINDRA важен общий принцип:

> `self-model` может означать функциональную предсказательную модель свойств самого агента без утверждений о phenomenal consciousness.

Конкретная morphology architecture к MINDRA не относится.

---

# 8. Выводы для canonical design

Research evidence поддерживает следующие решения `DU-13`:

1. natural-language self-report Cortex недостаточен как authoritative Self Model;
2. self-assessment/calibration является отдельной capability;
3. capability availability и competence нужно разделять;
4. competence должна иметь область применимости, а не один global scalar;
5. success probability и uncertainty/support самой оценки должны быть различимы;
6. self-monitoring нужно отделять от downstream self-regulation;
7. historical experience может обновлять capability/competence profile;
8. функциональная Self Model не означает consciousness/self-awareness в феноменальном смысле.

---

# 9. Что нужно перепроверить перед implementation/version selection

Перед выбором concrete Self Model implementation нужно заново исследовать:

- актуальные competence-estimation architectures;
- calibration methods для online/non-stationary agents;
- transfer/recalibration после model/module updates;
- confidence estimation для small Cortex models;
- statistical vs learned competence predictors;
- OOD detection/applicability estimation;
- lightweight approaches для домашнего/Colab compute budget;
- актуальные open-source metacognition/self-model implementations.

Быстро меняющийся landscape не должен фиксироваться canonical design раньше version selection.
