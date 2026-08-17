# Research pass — Salience / Attention / resource allocation

## Статус

**Связанный Design Update:** `DU-19 — Salience / Attention`  
**Дата среза:** 2026-08-17  
**Статус:** non-canonical research evidence

Этот документ фиксирует внешний исследовательский контекст, использованный при проектировании `DU-19`.

Он не выбирает human visual-attention model, Transformer attention, конкретный router, top-K policy или neural architecture как обязательную реализацию MINDRA.

---

# 1. Исследовательские вопросы

Проверялись вопросы:

1. Нужно ли Salience представлять одним scalar?
2. Насколько полезно различать bottom-up и top-down priority sources?
3. Должна ли Salience сама владеть ограниченным resource budget?
4. Как отличить salience representation от actual attention allocation?
5. Нужен ли stateful механизм persistence/inhibition?
6. Можно ли адаптивно распределять количество compute по difficulty/importance?
7. Являются ли Transformer attention weights подходящим canonical proxy Salience?
8. Какие controls нужны, чтобы доказать функциональность allocation, а не декоративного score?

---

# 2. Itti, Koch, Niebur 1998 — bottom-up saliency map

Laurent Itti, Christof Koch, Ernst Niebur.  
**A Model of Saliency-Based Visual Attention for Rapid Scene Analysis.**  
IEEE TPAMI, 1998.  
DOI: `10.1109/34.730558`.

Классическая computational saliency model объединяет несколько feature-specific conspicuity maps в общий saliency map и использует competitive selection/inhibition для последовательного переноса visual attention.

Вывод для MINDRA:

- salience как mechanism priority/competition имеет давний computational precedent;
- inhibition-of-return является разумным candidate stateful mechanism;
- однако visual-feature scalar map нельзя переносить как universal cognitive Salience representation MINDRA;
- наши targets выходят далеко за visual locations и включают Goals/Memory/hypotheses/plan candidates.

---

# 3. SUN 2008 — bottom-up information и top-down task relation

Lingyun Zhang, Matthew H. Tong, Tim K. Marks, Honghao Shan, Garrison W. Cottrell.  
**SUN: A Bayesian Framework for Saliency Using Natural Statistics.**  
Journal of Vision, 2008.  
DOI: `10.1167/8.7.32`.

Работа связывает bottom-up saliency с self-information features, а task-conditioned saliency — с information relation feature к target.

Вывод для MINDRA:

- novelty/information-related evidence может влиять на priority;
- task relevance может radically изменить salience того же input;
- это поддерживает `salience(target | purpose/context)`, а не global timeless score;
- конкретная Bayesian formula не принимается.

---

# 4. Mnih et al. 2014 — selective attention как ограниченное processing

Volodymyr Mnih, Nicolas Heess, Alex Graves, Koray Kavukcuoglu.  
**Recurrent Models of Visual Attention.**  
`arXiv:1406.6247`.

Модель адаптивно выбирает последовательность visual glimpses и обрабатывает только выбранные regions с высоким resolution, что позволяет контролировать compute независимо от полного размера input.

Вывод для MINDRA:

```text
priority / selection
→ реально меньше/другое processing
```

является сильнее декоративной saliency map.

Это поддерживает наш causal gate: Salience должна иметь measurable downstream resource-allocation effect.

Конкретный recurrent visual-attention/RL algorithm не принимается.

---

# 5. Graves 2016 — Adaptive Computation Time

Alex Graves.  
**Adaptive Computation Time for Recurrent Neural Networks.**  
`arXiv:1603.08983`.

ACT позволяет модели адаптивно выбирать количество internal computational steps на input и показывает, что более трудные/непредсказуемые элементы могут получать больше compute.

Вывод для MINDRA:

- adaptive compute allocation является практически реализуемым принципом;
- priority и количество processing можно связывать;
- однако actual choice числа Cognitive Cycles/Cortex calls должен принадлежать будущему Executive Control, а не Salience;
- Salience может предоставлять priority evidence внутри explicit budget.

---

# 6. Jain & Wallace 2019 — attention weights не являются объяснением

Sarthak Jain, Byron C. Wallace.  
**Attention is not Explanation.**  
`arXiv:1902.10186`.

Авторы показывают, что learned NLP attention weights могут плохо коррелировать с другими feature-importance measures и что существенно разные attention distributions способны давать близкие predictions.

Вывод для MINDRA:

> internal Transformer attention weight нельзя автоматически интерпретировать как canonical importance/Salience.

Следовательно:

- Cortex attention остаётся backend-specific internal mechanism;
- такие weights допустимы как Research Probe/evidence только после explicit validation;
- Salience contract не зависит от наличия attention tensors у Cortex.

---

# 7. Budgeted Attention Allocation 2026

Amrit Nidhi.  
**Budgeted Attention Allocation: Cost-Conditioned Compute Control for Efficient Transformers.**  
`arXiv:2605.05697`.

Работа исследует attention gating, conditioned на requested budget, и демонстрирует возможность одной модели работать в нескольких cost-quality operating points.

Вывод для MINDRA:

- explicit budget как input allocation mechanism является актуальным engineering pattern;
- budget и priority полезно разделять;
- allocation policy может быть conditioned на budget;
- конкретный head-gating mechanism не принимается.

---

# 8. Reinforced Attention Learning 2026

Bangzheng Li et al.  
**Reinforced Attention Learning.**  
`arXiv:2602.04884`.

Работа оптимизирует internal attention distributions мультимодальной модели вместо только output sequence и показывает, что learned attention allocation itself может быть обучаемой policy surface.

Вывод для MINDRA:

- allocation strategy потенциально может быть learned;
- где смотреть/что обрабатывать является самостоятельным optimization target;
- но MINDRA должна сохранять semantic boundary между learned router и Cortex-internal attention;
- `DU-19` поэтому допускает learned `AllocationPolicy`, но не требует её.

---

# 9. SpotAttention 2026 — query-specific sparse budget

Huzama Ahmad, Se-Young Yun.  
**SpotAttention: Plug-In Block-Sparse Routing for Pretrained Long-Context Transformers.**  
`arXiv:2606.22874`.

Работа использует lightweight selector для query-specific выбора subset past keys и adaptive budget.

Вывод для MINDRA:

- allocation может быть query/context-dependent;
- один fixed global K не обязан быть universal;
- budgeted sparse selection может быть practical backend technique;
- token/key selection конкретного Transformer остаётся ниже Cortex boundary и не является MINDRA Salience автоматически.

---

# 10. Top-down и bottom-up как две причины priority

Психофизические и computational исследования visual attention показывают, что sensory-driven salience и task-driven attention могут одновременно влиять на выбор, причём task demands способны подавлять или переопределять stimulus-driven salience.

Для MINDRA это поддерживает не biological copy, а functional разделение:

```text
signal-driven evidence
≠
concern/task-driven evidence
```

Оба могут попадать в SalienceProfile, не становясь обязательными отдельными neural streams.

---

# 11. Почему один salience scalar не выбран

Literature часто использует scalar maps/scores, но scope MINDRA шире visual fixation.

У нас candidates могут иметь разнородные причины priority:

```text
novelty
urgency
Goal relevance
risk
constraint violation
uncertainty requiring resolution
value
recent selection/inhibition
```

Premature additive scalarization создала бы те же проблемы, которые `DU-18` уже обнаружил для Valuation:

- hidden weights;
- потеря provenance;
- incompatibility scales;
- трудность causal intervention.

Поэтому scalar допускается как derived output `AllocationPolicy`, но не mandatory source of truth.

---

# 12. Почему Salience не владеет compute

ACT и budgeted attention показывают возможность adaptive compute.

Но MINDRA уже имеет отдельные будущие responsibilities:

```text
Salience
→ priority evidence/allocation

Executive Control
→ decide actual Cortex/retrieval/planning/compute use

Scheduler
→ enforce execution invariants
```

Это разделение нужно для диагностируемости и предотвращения скрытого scheduler/router inside Salience.

---

# 13. Stateful attention candidates

Классические saliency systems часто используют inhibition-of-return, а современные routers могут иметь adaptive/history-dependent behavior.

Для MINDRA разумно допустить:

- focus persistence;
- inhibition;
- habituation;
- hysteresis;

но не принимать конкретную equation.

Stateless Salience остаётся обязательным baseline.

---

# 14. Canonical выводы DU-19

Research evidence поддерживает следующие архитектурные conclusions:

1. Salience полезно отделить от event relevance/value.
2. Priority должен иметь реальный allocation/processing effect.
3. Bottom-up и top-down evidence должны быть различимы.
4. Salience должна быть purpose/query dependent.
5. Budget должен быть explicit input, а не скрытая константа.
6. Profile/evidence и actual allocation нужно различать.
7. Scalar score допустим, но не обязателен.
8. Stateful inhibition/persistence допустимы как optional dynamics.
9. Cortex/Transformer attention weights не равны canonical Salience.
10. Learned routing является implementation candidate, а не requirement.

---

# 15. Что перепроверить перед implementation

Перед конкретной software version нужно заново проверить:

- актуальные learned routing/attention allocation методы;
- доступные PyTorch/TorchRL routing primitives;
- sparse/top-K differentiable estimators;
- compute overhead самого Salience router;
- stability/load-balancing issues learned routing;
- concrete budget representation для MicroWorld;
- насколько rule-based baseline уже достаточен для первых causal experiments.

---

# 16. Связанные design документы

- [`../../design/modules/salience.md`](../../design/modules/salience.md);
- [`../../design/contracts/salience.md`](../../design/contracts/salience.md);
- [`../../design/decisions/ADR-0019-budgeted-contextual-salience-allocation.md`](../../design/decisions/ADR-0019-budgeted-contextual-salience-allocation.md).
