# DU-26 — Training Lifecycle: research pass 2026-08

## Статус

**Дата:** 2026-08-17  
**Тип:** non-canonical research evidence  
**Связанный Design Update:** `DU-26 — Training Lifecycle`

Документ не выбирает optimizer, RL/SFT algorithm, framework, PEFT method, continual-learning method или distributed topology.

---

# 1. Исследовательский вопрос

Нужно спроектировать lifecycle:

```text
TrainingSample / ReplaySelection
→ optimization
→ candidate parameters
→ validation
→ Learning Update
→ Agent revision activation
```

с чистым разделением training/cognition и revision provenance.

---

# 2. PyTorch optimizer ownership

## PyTorch `torch.optim`

- https://docs.pytorch.org/docs/stable/optim

Optimizer и learning-rate scheduler имеют собственный state/update lifecycle отдельно от model forward state.

Для MINDRA полезен общий pattern:

```text
model parameters
≠ optimizer state
≠ scheduler state
```

PyTorch API не становится canonical contract.

---

# 3. PEFT / LoRA

## Hugging Face PEFT — LoRA

- https://huggingface.co/docs/peft/main/conceptual_guides/lora

LoRA сохраняет base weights frozen и обучает небольшие low-rank update matrices. Это practical candidate для домашнего/Colab Cortex adaptation и естественно поддерживает различие:

```text
base Cortex revision
≠ adapter revision
```

Но LoRA не является обязательным механизмом MINDRA.

---

# 4. IMPALA — actor/learner separation

## Espeholt et al. — IMPALA

- arXiv: `1802.01561`
- https://arxiv.org/abs/1802.01561
- https://research.google/pubs/impala-scalable-distributed-deep-rl-with-importance-weighted-actor-learner-architectures/

IMPALA отделяет actors от learner, из-за чего behavior policy может отставать от learner policy. V-trace используется как конкретная off-policy correction.

Для MINDRA важен более общий вывод:

```text
behavior_revision
≠ learner_revision
```

может быть normal online-training case и обязано сохраняться в provenance.

V-trace не фиксируется.

---

# 5. Ape-X / replay separation

## Horgan et al. — Distributed Prioritized Experience Replay

- arXiv: `1803.00933`
- https://arxiv.org/abs/1803.00933

Architecture отделяет actors, replay и learner. Это поддерживает уже принятое:

```text
experience collection
≠ replay selection
≠ Learning Update
```

Prioritized replay не становится canonical algorithm.

---

# 6. Continual learning и forgetting

## Luo et al. — RL Forgets! Towards Continual Policy Optimization

- arXiv: `2607.04364`
- https://arxiv.org/abs/2607.04364

Работа 2026 года показывает сильное catastrophic forgetting и при reinforcement post-training.

## Lou et al. — Overcoming Catastrophic Forgetting in Visual Continual Learning with Reinforcement Fine-Tuning

- arXiv: `2605.09640`
- https://arxiv.org/abs/2605.09640

Также показывает non-negligible forgetting и связь drift с retention.

Для MINDRA вывод:

```text
new-task improvement
≠ training success автоматически
```

Retention прежних capabilities нужно валидировать отдельно.

---

# 7. Plasticity и forgetting

## Elsayed & Mahmood — Addressing Loss of Plasticity and Catastrophic Forgetting in Continual Learning

- arXiv: `2404.00781`
- https://arxiv.org/abs/2404.00781

Работа различает loss of plasticity и catastrophic forgetting. Это мотивирует отдельные diagnostics, а не единый continual score.

Конкретный UPGD optimizer не фиксируется.

---

# 8. Continual VLM survey

## Continual Learning for VLMs: A Survey and Taxonomy Beyond Forgetting

- arXiv: `2508.04227`
- https://arxiv.org/abs/2508.04227

Survey выделяет replay, regularization и parameter-efficient adaptation как разные семейства решений. MINDRA поэтому не выбирает один universal anti-forgetting method.

---

# 9. MINDRA-specific candidate/activation boundary

Обычный ML loop часто обновляет model object in place, поскольку training и inference разделены.

Для long-lived MINDRA этого недостаточно из-за:

- in-flight Decision Window;
- online actor/learner revisions;
- coupled components;
- representation drift;
- rollback/research reproducibility.

Поэтому `DU-26` вводит MINDRA-specific lifecycle:

```text
pinned base revision
→ candidate revision
→ validation
→ activation
```

---

# 10. Joint vs separate optimization

Frameworks допускают один optimizer с несколькими parameter groups, несколько optimizers, frozen subsets и adapters. Поэтому canonical design не предполагает ни `one module = one optimizer`, ни `one Agent = one optimizer`.

Вместо этого нужен explicit `GradientFlowPolicy` и optimizer ownership.

---

# 11. Training objective vs cognitive value

MINDRA уже разделяет `External Task Feedback`, `Intrinsic Signals`, `Drives` и `ValueProfile`. Training target/reward mapping поэтому должен быть отдельной versioned training configuration, а не implicit equivalence.

---

# 12. Validation / rollback

Ключевой causal invariant:

```text
training produced candidate
≠ candidate became active Agent
```

Это позволяет reject divergent/incompatible update и rollback без rewrite history. Exact checkpoint mechanics — `DU-27`.

---

# 13. Home/Colab implication

Для первой версии practical candidates — small trainable modules и frozen Cortex либо PEFT/LoRA adapter. Full large-model pretraining не требуется архитектурой.

Это future version choice, не canonical решение `DU-26`.

---

# 14. Вывод

Research evidence поддерживает:

1. acting/runtime и learning — разные boundaries;
2. behavior revision нужно сохранять;
3. optimizer state — отдельный training state;
4. frozen/adapters/full tuning должны укладываться в общий lifecycle;
5. continual training требует retention diagnostics;
6. runtime dependency graph ≠ gradient graph;
7. candidate/validation/activation оправдана причинными требованиями MINDRA;
8. конкретный optimizer/framework/algorithm не фиксируется.
