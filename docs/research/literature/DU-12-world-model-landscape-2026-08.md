# Research pass DU-12 — World Model landscape

## Статус

**Дата среза:** 2026-08-17  
**Связанный Design Update:** `DU-12 — World Model`  
**Статус:** research evidence, non-canonical

Этот документ фиксирует внешний research/tooling context, использованный при проектировании `DU-12`.

Он **не выбирает** concrete World Model architecture MINDRA и должен быть перепроверен перед version/implementation selection.

---

# 1. Вопросы исследования

Проверялись следующие вопросы:

1. Нужен ли отдельный belief state при partial observability?
2. Обязателен ли reconstruction decoder?
3. Является ли RSSM единственным разумным вариантом?
4. Как современные world models представляют stochastic dynamics?
5. Как отделять imagination от real experience?
6. Как трактовать predictive uncertainty?
7. Есть ли готовые modular primitives, которые можно использовать позже?

---

# 2. PlaNet / RSSM

**Источник:** Danijar Hafner et al., *Learning Latent Dynamics for Planning from Pixels* (2018).  
https://arxiv.org/abs/1811.04551

PlaNet использует latent dynamics model с deterministic и stochastic transition components и планирует в latent space.

Для MINDRA особенно важна не конкретная сеть, а structural idea:

```text
history/belief
+
action
→ prior prediction

prediction
+
actual observation
→ posterior update
```

Это поддерживает решение отделить actual-evidence assimilation от imagination/prediction.

PlaNet не принимается как canonical MINDRA algorithm.

---

# 3. DreamerV3

**Источник:** Danijar Hafner et al., *Mastering Diverse Domains through World Models* (2023).  
https://arxiv.org/abs/2301.04104

DreamerV3 обучает модель среды и улучшает behavior через imagined future trajectories.

Design relevance:

- multi-step latent imagination практически работоспособна;
- imagined trajectories можно использовать для downstream learning/planning;
- world-model behavior не требует реальных Environment transitions на каждый imagined step.

Для MINDRA это поддерживает строгую provenance boundary:

```text
imagined transition
≠
observed transition
```

Но Dreamer actor/value/reward architecture не является обязательной частью MINDRA.

---

# 4. TD-MPC2

**Источник:** Nicklas Hansen, Hao Su, Xiaolong Wang, *TD-MPC2: Scalable, Robust World Models for Continuous Control* (2023).  
https://arxiv.org/abs/2310.16828

TD-MPC2 использует implicit decoder-free world model и local trajectory optimization в latent space.

Design relevance:

> полезная world model не обязана реконструировать полный observation.

Это поддерживает решение MINDRA не делать observation decoder обязательным contract requirement.

---

# 5. Transformer world models

## TransDreamer

**Источник:** Chang Chen et al., *TransDreamer: Reinforcement Learning with Transformer World Models* (2022).  
https://arxiv.org/abs/2202.09481

TransDreamer заменяет recurrent world-model core Transformer State-Space Model и показывает преимущества на задачах с long-range memory requirements.

## IRIS

**Источник:** Vincent Micheli, Eloi Alonso, François Fleuret, *Transformers are Sample-Efficient World Models* (2022).  
https://arxiv.org/abs/2209.00588

IRIS использует discrete autoencoder + autoregressive Transformer world model.

Design conclusion:

```text
belief/prediction semantics
≠
обязательная recurrent/RSSM implementation
```

Поэтому `DU-12` фиксирует semantic boundary, а не neural architecture.

---

# 6. PETS и uncertainty-aware dynamics

**Источник:** Kurtland Chua et al., *Deep Reinforcement Learning in a Handful of Trials using Probabilistic Dynamics Models* (2018).  
https://arxiv.org/abs/1805.12114

PETS использует probabilistic ensembles и trajectory sampling для uncertainty-aware model-based control.

Design relevance:

- stochastic/predictive uncertainty является полезной capability;
- ensemble/sampling являются возможными implementation strategies;
- неопределённость должна распространяться по rollout осознанно.

Но MINDRA не принимает ensemble как обязательный uncertainty estimator.

---

# 7. Epistemic и aleatoric uncertainty

**Источник:** Bertrand Charpentier et al., *Disentangling Epistemic and Aleatoric Uncertainty in Reinforcement Learning* (2022).  
https://arxiv.org/abs/2206.01558

Работа подчёркивает различие:

- aleatoric uncertainty — irreducible stochasticity;
- epistemic uncertainty — ограниченность знания/данных.

Для MINDRA главный вывод — **не называть любую variance правильной decomposition автоматически**.

`DU-12` поэтому требует generic `predictive uncertainty` по умолчанию, а `epistemic/aleatoric` labels — только при обоснованном estimator и отдельной evaluation.

---

# 8. R2-Dreamer как актуальный decoder-free пример

**Источник:** Naoki Morihira et al., *R2-Dreamer: Redundancy-Reduced World Models without Decoders or Augmentation* (2026).  
https://arxiv.org/abs/2603.18202

Работа продолжает направление decoder-free model-based RL и показывает, что reconstruction objective не является единственным способом обучать полезные representations.

Design relevance:

> MINDRA не должна делать decoder/reconstruction частью canonical World Model contract.

Конкретные результаты статьи требуют независимой проверки перед использованием как implementation argument.

---

# 9. TorchRL tooling evidence

**Официальная документация:**  
https://docs.pytorch.org/rl/stable/reference/modules_models.html

На момент среза TorchRL предоставляет modular model-based components, включая:

- `WorldModel` / `WorldModelWrapper`;
- `RSSMPrior`;
- `RSSMPosterior`;
- `RSSMRollout`;
- Dreamer/DreamerV3 loss components;
- GP-based world-model components.

Особенно полезно, что rollout/environment-level semantics отделены от prediction module abstractions.

Design conclusion:

- необходимые MINDRA primitives технически реализуемы в существующем PyTorch ecosystem;
- использовать TorchRL можно рассмотреть позже;
- TorchRL/TensorDict **не становятся canonical implementation requirements** из-за этого evidence.

---

# 10. Канонические выводы, поддержанные research pass

Research evidence поддерживает следующие решения `DU-12`:

1. partial observability требует явного history/belief mechanism;
2. assimilation actual observation следует отличать от transition prior/prediction;
3. learned latent state полезен, но не обязан быть единственным public contract;
4. observation reconstruction не является обязательным требованием World Model;
5. recurrent/RSSM и transformer/autoregressive architectures являются взаимозаменяемыми design candidates;
6. imagination должна иметь отдельную provenance от real experience;
7. uncertainty является optional/typed capability, а её интерпретация требует discipline;
8. concrete architecture следует выбирать в version design с учётом MicroWorld, compute budget и evaluation goals.

---

# 11. Что перепроверить перед implementation

Перед выбором World Model для первой software version нужно заново проверить:

- актуальные Dreamer/TorchRL implementations;
- hardware/VRAM cost конкретных candidates;
- качество/скорость RSSM vs simpler recurrent baseline на нашем MicroWorld;
- необходимость stochastic latent уже в первой версии;
- доступные uncertainty estimators;
- decoder-free vs reconstruction-based trade-offs;
- training stability на небольших datasets;
- актуальные transformer/SSM world-model implementations;
- лицензии конкретного open-source code, если он будет переиспользован.
