# Research pass — Intrinsic Signals / intrinsic motivation landscape

## Статус

**Связанный Design Update:** `DU-14 — Intrinsic Signals`  
**Дата среза:** 2026-08-17  
**Статус:** non-canonical research evidence

Этот документ фиксирует внешний исследовательский контекст, использованный при проектировании `DU-14`.

Он не выбирает concrete Intrinsic Signal provider и не переопределяет `docs/design/`.

---

# 1. Основные исследовательские вопросы

Проверялись следующие вопросы:

1. Можно ли считать prediction error, novelty и surprise одним сигналом?
2. Какие intrinsic approaches требуют history/density/belief state?
3. Как information gain отличается от prediction error?
4. Как competence/learning progress может стать отдельным signal family?
5. Как stochastic noise ломает простые curiosity bonuses?
6. Почему representation choice является частью signal semantics?
7. Следует ли intrinsic layer сразу возвращать scalar reward?

---

# 2. ICM — prediction error в learned controllable representation

## Curiosity-driven Exploration by Self-supervised Prediction

Deepak Pathak, Pulkit Agrawal, Alexei A. Efros, Trevor Darrell, 2017.  
`arXiv:1705.05363`

ICM формирует curiosity reward из ошибки предсказания последствий действий в feature space, обученном через inverse dynamics.

Вывод для MINDRA:

- prediction discrepancy может быть полезным внутренним signal;
- representation, в которой считается ошибка, является частью semantics;
- сам error не следует архитектурно называть универсальной novelty/utility.

---

# 3. Large-Scale Curiosity — stochastic limitation

## Large-Scale Study of Curiosity-Driven Learning

Yuri Burda, Harri Edwards, Deepak Pathak и др., 2018.  
`arXiv:1808.04355`

Работа сравнивает curiosity-driven learning в большом наборе environments и отдельно демонстрирует ограничения prediction-based curiosity в stochastic settings.

Вывод:

```text
persistent prediction error
≠
persistent useful learning opportunity
```

Это поддерживает разделение raw discrepancy и information/learnability-oriented signals.

---

# 4. RND — novelty-like signal через distillation error

## Exploration by Random Network Distillation

Yuri Burda, Harrison Edwards, Amos Storkey, Oleg Klimov, 2018.  
`arXiv:1810.12894`

RND использует ошибку predictor network относительно fixed random target network как exploration bonus.

Для MINDRA важно:

- численно это prediction error, но semantics отличается от World Model prediction error;
- estimator identity должна быть частью provenance;
- один и тот же математический вид ошибки не доказывает одинаковый смысл signal.

---

# 5. Pseudo-count / visitation rarity

## Unifying Count-Based Exploration and Intrinsic Motivation

Marc G. Bellemare, Sriram Srinivasan, Georg Ostrovski и др., 2016.  
`arXiv:1606.01868`

Работа выводит pseudo-count из density model для переноса count-based exploration в high-dimensional observations.

Вывод для MINDRA:

- visitation rarity является самостоятельным signal family;
- «состояние уже встречалось» зависит от density/representation model;
- scope/count state обязаны быть versioned и snapshot-able.

---

# 6. VIME — information gain

## VIME: Variational Information Maximizing Exploration

Rein Houthooft, Xi Chen, Yan Duan, John Schulman, Filip De Turck, Pieter Abbeel, 2016.  
`arXiv:1605.09674`

VIME мотивирует exploration через information gain о belief динамической модели после нового опыта.

Вывод:

- information gain имеет before/after knowledge semantics;
- он принципиально отличается от простой ошибки прогноза;
- meaningful IG требует estimator, который действительно представляет uncertainty/belief update.

---

# 7. NGU — episodic novelty и multiple timescales

## Never Give Up: Learning Directed Exploration Strategies

Adrià Puigdomènech Badia и др., 2020.  
`arXiv:2002.06038`

NGU использует episodic kNN novelty в learned representation и сочетает разные exploratory policies.

Вывод для MINDRA:

- novelty имеет explicit reference scope;
- episodic novelty не равна lifetime rarity;
- representation и history scope являются частью signal identity.

---

# 8. RIDE — impact/change signal

## RIDE: Rewarding Impact-Driven Exploration for Procedurally-Generated Environments

Roberta Raileanu, Tim Rocktäschel, 2020.  
`arXiv:2002.12292`

RIDE поощряет действия, вызывающие существенные изменения в learned state representation.

Вывод:

- кроме novelty/surprise существуют другие experience-derived signal families;
- Intrinsic Signal architecture должна быть extensible и не ограничиваться одним заранее выбранным scalar.

`Impact` не становится обязательным core signal DU-14, но architecture должна позволять такой provider.

---

# 9. Plan2Explore — expected novelty через world model disagreement

## Planning to Explore via Self-Supervised World Models

Ramanan Sekar, Oleh Rybkin, Kostas Daniilidis, Pieter Abbeel, Danijar Hafner, Deepak Pathak, 2020.  
`arXiv:2005.05960`

Plan2Explore использует disagreement ensemble world models для планирования в направлении ожидаемой novelty.

Вывод для MINDRA:

- actual intrinsic signal и predicted future signal следует различать;
- World Model может позднее прогнозировать/поддерживать exploration-relevant quantities;
- planning responsibility не должна поглощаться Intrinsic Signal Provider.

---

# 10. CURIOUS — learning progress / competence progress

## CURIOUS: Intrinsically Motivated Modular Multi-Goal Reinforcement Learning

Cédric Colas, Pierre Fournier, Olivier Sigaud, Mohamed Chetouani, Pierre-Yves Oudeyer, 2018.  
`arXiv:1810.06284`

CURIOUS выбирает цели, ориентируясь на absolute learning progress, и возвращается к забываемым goals.

Вывод для MINDRA:

- изменение competence во времени является отдельным signal family;
- signed improvement/degradation evidence полезно сохранять до downstream choice;
- absolute magnitude является возможной derived semantics, но не должна уничтожать знак исходного изменения.

---

# 11. Современные information-oriented approaches

## On Efficient Bayesian Exploration in Model-Based Reinforcement Learning

Alberto Caron, Chris Hicks, Vasilios Mavroudis, 2025.  
`arXiv:2507.02639`

Работа исследует information-theoretic bonuses, направленные на epistemic uncertainty, и подчёркивает важность отделения reducible knowledge uncertainty от irreducible noise.

Вывод для MINDRA:

- ярлык `epistemic information gain` требует formal estimator semantics;
- raw uncertainty magnitude нельзя автоматически трактовать как learnability.

## Information-Based Exploration via Random Features for Reinforcement Learning

Waris Radji, Odalric-Ambrym Maillard, 2026.  
`arXiv:2607.17981`

На дату среза это свежий подход, использующий random features для приближённого information gain с теоретической интерпретацией.

Вывод:

- information-gain providers остаются активной областью исследований;
- MINDRA не должна зашивать конкретную neural estimator architecture в canonical contract.

---

# 12. Prediction-error improvement вместо raw error

## Curiosity-Critic: Cumulative Prediction Error Improvement as a Tractable Intrinsic Reward for World Model Training

Vin Bhaskara, Haicheng Wang, 2026.  
`arXiv:2604.18701`

Работа предлагает ориентироваться не только на текущую prediction error, а на improvement относительно learned asymptotic error baseline, чтобы меньше застревать на stochastic transitions.

Для MINDRA это non-canonical evidence в пользу более общего принципа:

```text
raw error
≠
learnability / reducible error
```

Concrete Curiosity-Critic не становится обязательным provider.

---

# 13. Архитектурные выводы для DU-14

Исследование поддерживает следующие canonical conclusions:

1. intrinsic signal families функционально различны;
2. один scalar reward является слишком ранней aggregation boundary;
3. provider identity и estimator semantics обязаны сохраняться;
4. representation/history/reference scope входят в meaning novelty/rarity signals;
5. information gain требует meaningful before/after knowledge state;
6. prediction error уязвим к stochastic noise;
7. competence progress требует temporal window/baseline;
8. actual, predicted и replay-computed signals следует различать;
9. normalization/revision state является частью reproducibility;
10. specific algorithm должен выбираться позднее по требованиям version/experiment.

---

# 14. Что нужно перепроверить перед implementation

Перед выбором provider для конкретной software version нужно заново проверить:

- актуальные implementations/tooling;
- compute/memory cost;
- robustness на выбранных MicroWorld families;
- поведение при representation drift;
- compatibility с выбранным World/Self Model;
- normalization requirements;
- availability готовых open-source implementations;
- recent exploration/intrinsic-motivation work после даты этого документа.
