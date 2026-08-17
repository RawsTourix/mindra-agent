# Research pass — Drives / homeostatic motivation landscape

## Статус

**Связанный Design Update:** `DU-15 — Drives`  
**Дата среза:** 2026-08-17  
**Статус:** non-canonical research evidence

Этот документ фиксирует внешний исследовательский контекст, использованный при проектировании `DU-15`.

Он не выбирает concrete drive list/dynamics и не переопределяет `docs/design/`.

---

# 1. Основные исследовательские вопросы

Проверялись следующие вопросы:

1. Должен ли Drive быть просто intrinsic reward?
2. Насколько полезна homeostatic/set-point модель?
3. Нужно ли заставлять все drives иметь homeostatic target?
4. Может ли внутреннее состояние изменять поведение независимо от внешнего состояния?
5. Как моделировать несколько конкурирующих motivational systems?
6. Должен ли Drive State развиваться непрерывно/во времени?
7. Как curiosity/information-related signals соотносятся с persistent drive?
8. Стоит ли использовать Active Inference как универсальную замену отдельным Drive/Valuation слоям?

---

# 2. Homeostatic RL — базовая вычислительная идея

## A Reinforcement Learning Theory for Homeostatic Regulation

Mehdi Keramati, Boris S. Gutkin, NeurIPS 2011.

Работа связывает reinforcement learning и negative-feedback homeostatic regulation.

Ключевые идеи для MINDRA:

- internal state может модифицировать мотивированное поведение;
- drive можно формализовать через отклонение регулируемых внутренних переменных от желательного состояния;
- несколько motivational systems могут взаимодействовать;
- anticipatory behavior и risk sensitivity могут возникать из internal-state-regulated learning.

Вывод:

> Homeostatic semantics является сильным кандидатом для drives с настоящей регулируемой переменной, но не доказывает, что любой будущий drive MINDRA обязан иметь set-point.

---

# 3. Homeostatic reinforcement learning 2014

## Homeostatic reinforcement learning for integrating reward collection and physiological stability

Mehdi Keramati, Boris Gutkin, eLife, 2014.  
DOI: `10.7554/eLife.04811`

Работа развивает идею primary reward как результата, уменьшающего физиологическую потребность, и показывает связь reward acquisition с поддержанием homeostatic stability.

Для MINDRA важно:

- internal regulated state может давать principled context-dependence ценности одного и того же outcome;
- drive reduction может быть связано с reinforcement objective;
- predictive/anticipatory regulation функционально возможна.

Но MINDRA сохраняет архитектурное различие:

```text
Drive State / regulatory deviation
≠
RL reward
```

Преобразование drive dynamics в learning objective относится к будущим `Valuation/Training` decisions.

---

# 4. Continuous Homeostatic Reinforcement Learning

## Continuous Homeostatic Reinforcement Learning for Self-Regulated Autonomous Agents

Hugo Laurençon, Charbel-Raphaël Ségerie, Johann Lussange, Boris S. Gutkin, 2021.  
`arXiv:2109.06580`

Работа подчёркивает, что internal state может иметь собственную dynamics, меняющуюся непрерывно, а агенту приходится действовать, чтобы поддерживать homeostasis.

Ключевой вывод для MINDRA:

> Drive не должен быть простой мгновенной функцией последнего observation/signal; persistent dynamics является самостоятельной частью механизма.

Это поддерживает `Drive State`, recovery/decay/accumulation и explicit temporal update semantics.

---

# 5. CTCS-HRRL

## Continuous Time Continuous Space Homeostatic Reinforcement Learning

Hugo Laurençon и др., 2024.  
`arXiv:2401.08999`

Работа расширяет HRRL на continuous time/space и снова моделирует собственную динамику внутренних регулируемых переменных.

Для MINDRA это evidence в пользу отделения:

```text
external world dynamics
≠
internal regulatory dynamics
```

Но MINDRA использует logical time из `DU-03`, а не делает физический continuous wall-clock обязательной архитектурой.

---

# 6. Современная перспектива HRRL

## Linking Homeostasis to Reinforcement Learning: Internal State Control of Motivated Behavior

Naoto Yoshida, Henning Sprekeler, Boris Gutkin, 2025.  
`arXiv:2507.04998`

Perspective рассматривает HRRL как framework motivated behavior через регулирование internal state и обсуждает:

- risk aversion;
- anticipatory regulation;
- adaptive movement;
- deep-RL extensions;
- exploration/hierarchical behavior;
- robotics applications.

Для MINDRA это подтверждает актуальность идеи internal-state-controlled behavior, но не требует копировать конкретный HRRL reward formulation.

---

# 7. Curiosity + homeostatic regulation

## Curiosity-driven reinforcement learning with homeostatic regulation

Ildefons Magrans de Abril, Ryota Kanai, 2018.  
`arXiv:1801.07440`

Работа объединяет information-theoretic curiosity reward с дополнительной homeostatic regulation.

Для MINDRA особенно полезен сам факт разделимости двух механизмов:

```text
information-related signal/objective
+
homeostatic regulation
```

Это поддерживает решение `DU-14/15` не отождествлять:

```text
novelty / information gain
```

с:

```text
persistent drive state
```

и не считать высокий Intrinsic Signal готовой мотивацией.

---

# 8. Scheduled Intrinsic Drive

## Scheduled Intrinsic Drive: A Hierarchical Take on Intrinsically Motivated Exploration

Jingwei Zhang, Niklas Wetzel, Nicolai Dorka, Joschka Boedecker, Wolfram Burgard, 2019.  
`arXiv:1903.07400`

Работа критикует простое суммирование intrinsic и extrinsic reward за получение смешанной policy и использует отдельные intrinsic/extrinsic policies с scheduling.

Для MINDRA это косвенно поддерживает осторожность к:

```text
reward_total = reward_external + reward_intrinsic
```

как универсальной мотивационной архитектуре.

MINDRA идёт ещё дальше и сохраняет Intrinsic Signal, Drive State и Valuation отдельными слоями.

---

# 9. Multiple drives / competition

Homeostatic RL уже допускает взаимодействие нескольких motivational systems.

Для MINDRA это поддерживает vector-like `DriveStateSet`, но не даёт основания заранее выбирать механизм arbitration.

Поэтому принято:

```text
several typed drives
→ preserve separate state
→ explicit coupling if needed
→ conflict resolution later in Valuation/Policy
```

а не:

```text
winning_drive = argmax(pressure)
```

как universal rule.

---

# 10. Homeostasis vs all drives

Исторические drive-reduction/homeostatic theories особенно естественны для переменных вроде энергии, жидкости, температуры и других регулируемых quantities.

Но artificial motivation может включать exploration, competence, control и information-seeking.

Попытка назначить каждому из них фиктивный set-point создаёт сильное теоретическое предположение без необходимости.

Поэтому canonical MINDRA design поддерживает:

```text
Homeostatic Drive
+
Adaptive Motivational Drive
```

как разные semantics внутри общего Drive contract.

---

# 11. Active Inference как альтернативная unified architecture

## Active Inference as a Model of Agency

Lancelot Da Costa, Samuel Tenka, Dominic Zhao, Noor Sajid, 2024.  
`arXiv:2401.12917`

Active Inference предлагает unified normative description поведения через generative model, risk/ambiguity и expected free-energy-like objectives вместо классического reward maximization.

Это важная альтернативная исследовательская линия.

Однако MINDRA уже намеренно проектируется как декомпозируемая architecture с отдельными:

```text
World Model
Intrinsic Signals
Drives
Appraisal
Valuation
Policy
```

Поэтому `DU-15` не заменяет эту структуру Active Inference framework.

Active Inference может позднее использоваться как:

- comparison baseline;
- источник отдельных mathematical ideas;
- alternative implementation в research branch;

но не является canonical drive architecture.

---

# 12. Основные выводы для DU-15

Research evidence поддерживает следующие решения:

1. Internal state должен иметь собственную persistent dynamics.
2. Homeostatic/set-point semantics полезна для реально регулируемых variables.
3. Homeostatic semantics не нужно насильно распространять на все motivation classes.
4. Intrinsic information signal не равен persistent drive.
5. Несколько drives должны сохранять отдельную identity.
6. Простая сумма intrinsic/extrinsic rewards слишком рано смешивает motivation и valuation.
7. Internal dynamics должна быть causally observable/intervenable.
8. Конкретный reward formulation должен оставаться downstream decision.

---

# 13. Что нужно перепроверить перед implementation

Перед version selection нужно заново проверить:

- современные open-source homeostatic RL implementations;
- доступность reusable code для continuous/internal-state dynamics;
- current empirical work по multi-drive agents;
- методы learning drive dynamics;
- benchmark design для drive-specific causal interventions;
- насколько полезен отдельный adaptive curiosity drive по сравнению с direct signal→Valuation baseline;
- compute overhead разных learned drive models.

Ни одна paper из этого research pass не делает конкретный Drive algorithm обязательным для MINDRA.
