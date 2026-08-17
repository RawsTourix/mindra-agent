# ADR-0012 — Belief-state World Model с раздельными assimilation, prediction и imagination semantics

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-12 — World Model`

---

# 1. Контекст

MINDRA работает в частично наблюдаемой среде. Текущий `Canonical Percept` описывает только доступное Agent наблюдение и не является полным состоянием мира.

World Model должна:

- интегрировать наблюдения во времени;
- прогнозировать последствия candidate actions;
- поддерживать multi-step imagination;
- не смешивать prediction с observation;
- не зависеть от конкретной архитектуры RSSM/Transformer;
- оставаться исследовательски диагностируемой и заменяемой.

Предыдущие DU уже запрещают использовать Environment hidden state как normal Agent input и запрещают превращать model-specific latent в universal representation.

---

# 2. Проблема

Нужно выбрать semantic architecture World Model.

Рассматривались варианты:

1. next-observation predictor без отдельного belief;
2. opaque latent-dynamics model как единственная каноническая поверхность;
3. полностью explicit symbolic hidden-world reconstruction;
4. belief-state World Model с раздельными update/prediction/imagination и гибридной output surface.

---

# 3. Требования

Решение должно:

- поддерживать partial observability;
- позволять recurrent/history-dependent inference;
- поддерживать deterministic и stochastic implementations;
- не требовать reconstruction всей sensory modality;
- не скрывать observed/predicted/imagined provenance;
- позволять structured diagnostics и learned latents одновременно;
- не привязывать downstream modules к backend hidden space;
- поддерживать counterfactual action queries;
- быть совместимым с Memory, Cortex, будущим Planner и Intrinsic Signals;
- позволять causal ablation/control.

---

# 4. Вариант A — Только next-percept predictor

## Плюсы

- простая training target;
- легко проверить one-step accuracy;
- минимальный state contract.

## Минусы

- плохо выражает partial observability;
- история либо неявно прячется в caller, либо теряется;
- сложнее разделять inferred current world state и future prediction;
- multi-step rollout быстро превращается в рекурсивную генерацию observations.

**Решение:** отклонён как общий canonical design.

---

# 5. Вариант B — Opaque latent dynamics как единственный contract

## Плюсы

- эффективно для neural control;
- совместимо с decoder-free world models;
- компактно для rollouts.

## Минусы

- downstream coupling к latent geometry;
- сложнее причинные interventions/diagnostics;
- representation drift становится архитектурной проблемой всех consumers;
- latent трудно отличить от canonical meaning;
- смена backend может потребовать переписывать остальную MINDRA.

**Решение:** latent допускается как implementation/private/optional feature surface, но не как единственный canonical contract.

---

# 6. Вариант C — Полностью explicit symbolic world reconstruction

## Плюсы

- интерпретируемость;
- удобство проверки против MicroWorld ground truth;
- понятные causal interventions.

## Минусы

- слишком сильное требование для будущих multimodal/continuous сред;
- навязывает ontology мира;
- может быть существенно сложнее, чем нужно для prediction/control;
- плохо масштабируется к perceptual ambiguity и сложным learned representations.

**Решение:** structured hypotheses допускаются как output/probe, но не обязательны как полное внутреннее состояние любого World Model.

---

# 7. Вариант D — Belief-state World Model с гибридной prediction surface

Семантика:

```text
actual evidence
→ assimilation/posterior
→ committed World Belief

World Belief + candidate action
→ prior/transition
→ World Prediction

predicted belief + further actions
→ imagination rollout
```

World Model может иметь private latent/recurrent state, но наружу предоставляет stable prediction/result semantics с provenance/revisions.

Predictions могут включать structured semantic channels и optional versioned learned feature views.

**Решение:** принято.

---

# 8. Evidence

Решение поддерживается несколькими существующими направлениями, не принимая ни одно из них как обязательную реализацию:

- PlaNet/RSSM демонстрирует deterministic + stochastic latent dynamics и posterior/prior state updates при partial observability;
- DreamerV3 показывает практическую эффективность обучения поведения через imagined latent trajectories;
- TD-MPC2 показывает, что полезная implicit world model может быть decoder-free;
- TransDreamer/IRIS показывают жизнеспособность transformer/autoregressive world-model architectures;
- PETS показывает ценность uncertainty-aware probabilistic dynamics/ensemble propagation.

Ссылки и датированный срез сохранены в `docs/research/literature/DU-12-world-model-landscape-2026-08.md`.

---

# 9. Принятое решение

MINDRA использует **belief-state semantic architecture World Model**.

Канонически:

1. текущий percept и World Belief — разные сущности;
2. assimilation actual evidence отделена от prediction без нового observation;
3. candidate-action prediction не является action selection;
4. imagination не является observed trajectory;
5. World Model может иметь private learned state;
6. private latent не становится universal inter-module representation;
7. output surface может быть structured + optional feature/latent views;
8. generic predictive uncertainty допускается, а epistemic/aleatoric decomposition требует отдельного обоснования;
9. prediction error не является reward;
10. concrete RSSM/Transformer/другая architecture выбирается позже.

---

# 10. Последствия

## Положительные

- partial observability получает явную семантику;
- World Model можно менять без переписывания Goal/Memory/Policy;
- imagination становится самостоятельным causal artifact;
- возможно сравнивать recurrent, transformer и decoder-free implementations;
- structured MicroWorld evaluation не требует раскрывать hidden state Agent;
- future Intrinsic Signals получают явный prediction-error source.

## Отрицательные

- contract сложнее next-state predictor;
- требуется отдельная belief revision/snapshot semantics;
- private latent сложнее интерпретировать;
- multi-step uncertainty/error требует отдельной оценки;
- exact implementation откладывается до version design.

---

# 11. Что решение намеренно не определяет

Не определены:

- RSSM/Transformer/SSM/GRU architecture;
- latent distribution;
- decoder/reconstruction;
- loss functions;
- uncertainty estimator;
- action schema;
- rollout planning algorithm;
- training/replay schedule;
- World Model size;
- framework/tooling.

---

# 12. Обновляемые документы

Решение отражается в:

- `docs/design/modules/world-model.md`;
- `docs/design/contracts/world-model.md`;
- `docs/design/decisions/README.md`;
- `docs/design/README.md`;
- `docs/design/current.md`;
- `AGENTS.md`;
- исследовательском literature pass `DU-12`.
