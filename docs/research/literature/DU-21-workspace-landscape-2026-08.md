# Research pass — Workspace / Global Workspace / shared bottleneck

## Статус

**Связанный Design Update:** `DU-21 — Workspace`  
**Дата среза:** 2026-08-17  
**Статус:** non-canonical research evidence

Этот документ фиксирует внешний исследовательский контекст, использованный при проектировании Workspace MINDRA.

Он **не утверждает**, что MINDRA сознательна или что Global Workspace Theory/GNWT является доказанной теорией сознания. Для MINDRA рассматриваются только инженерно проверяемые свойства selection, capacity limitation, temporary persistence и shared availability/broadcast.

---

# 1. Исследовательские вопросы

Проверялись:

1. даёт ли shared limited workspace функцию сверх ordinary shared state;
2. есть ли computational evidence в пользу bandwidth-limited communication между specialist modules;
3. нужно ли делать Workspace обязательным global router;
4. чем broadcast отличается от event bus;
5. как Workspace соотносится с working memory/CognitiveState;
6. насколько literal GNWT claims допустимо переносить в engineered Agent;
7. какие controls нужны, чтобы отличить workspace semantics от дополнительной recurrent/state capacity;
8. какие актуальные результаты 2025–2026 требуют осторожности в claims о consciousness.

---

# 2. Global Neuronal Workspace — functional inspiration, не software truth

George Mashour, Pieter Roelfsema, Jean-Pierre Changeux, Stanislas Dehaene и соавторы.  
**Conscious Processing and the Global Neuronal Workspace Hypothesis.**  
Neuron, 2020. DOI: `10.1016/j.neuron.2020.01.026`.

Review описывает центральный GNW pattern:

```text
specialized processors
→ selection/amplification
→ widespread availability/broadcast
```

и отдельно обсуждает relation с attention и working memory.

Вывод для MINDRA:

- global availability можно operationalize как отдельную functional hypothesis;
- selection, maintenance и broadcast лучше не смешивать;
- biological/anatomical claims не переносить в software architecture;
- functional global access не является доказательством phenomenal consciousness.

---

# 3. Goyal et al. — shared global workspace для neural modules

Anirudh Goyal, Aniket Didolkar, Alex Lamb, Kartikeya Badola, Nan Rosemary Ke, Nasim Rahaman, Jonathan Binas, Charles Blundell, Michael Mozer, Yoshua Bengio.  
**Coordination Among Neural Modules Through a Shared Global Workspace.**  
ICLR 2022 Oral / arXiv:`2103.01197`.

Авторы исследуют specialized neural modules, которые взаимодействуют через shared capacity-limited workspace. Modules конкурируют за write access, а workspace используется как общий communication bottleneck.

Reported motivation/results включают:

- coordination independent specialists;
- specialization/compositionality;
- рациональную роль limited bandwidth.

Вывод для MINDRA:

- bounded shared communication является реальным ML design family, а не только психологической метафорой;
- capacity должна быть реальной частью experiment, иначе workspace hypothesis не проверяется;
- neural implementation paper не требует, чтобы MINDRA использовала тот же latent/attention mechanism;
- matched state/compute controls обязательны.

---

# 4. VanRullen & Kanai — Global Latent Workspace

Rufin VanRullen, Ryota Kanai.  
**Deep Learning and the Global Workspace Theory.**  
arXiv:`2012.10390`.

Работа предлагает roadmap с translation между specialist latent spaces и shared amodal latent workspace.

Вывод для MINDRA:

- отдельный shared representation space является возможной implementation family;
- однако MINDRA уже имеет canonical semantic representation boundaries и не должна делать единый learned latent обязательным;
- latent workspace можно позднее сравнить с structured `WorkspaceItem` design как concrete version/control.

---

# 5. LIDA — cognitive architecture precedent

Stan Franklin et al.  
**LIDA: A Computational Model of Global Workspace Theory and Developmental Learning.**  
AAAI Fall Symposium, 2007 (AAAI archive publication page later migrated/republished).

LIDA — пример cognitive architecture, где global workspace встроен в larger cycle perception/memory/action selection.

Вывод для MINDRA:

- Workspace может быть отдельным элементом larger cognitive cycle;
- однако MINDRA не переносит LIDA module taxonomy, artificial emotion model или consciousness terminology;
- scheduler, Memory, Action Selection и Workspace должны сохранять уже принятые MINDRA boundaries.

---

# 6. Selection–broadcast cycle как отдельная engineering hypothesis

Junya Nakanishi, Jun Baba, Yuichiro Yoshikawa, Hiroko Kamide, Hiroshi Ishiguro.  
**Hypothesis on the Functional Advantages of the Selection-Broadcast Cycle Structure: Global Workspace Theory and Dealing with a Real-Time World.**  
arXiv:`2505.13969`, 2025.

Работа рассматривает selection+broadcast именно как функциональную cycle structure для dynamic real-time systems.

Вывод для MINDRA:

- selection и broadcast полезно тестировать не только по отдельности, но и как causal chain;
- paper формулирует hypothesis, а не достаточное empirical proof;
- MINDRA поэтому требует собственных capacity/broadcast lesion experiments.

---

# 7. 2025 adversarial test GNWT vs IIT — важное ограничение claims

Cogitate Consortium et al.  
**Adversarial testing of global neuronal workspace and integrated information theories of consciousness.**  
Nature 642, 133–142 (2025). DOI: `10.1038/s41586-025-08888-1`.

Large preregistered multimodal adversarial collaboration проверяла differential predictions GNWT и IIT.

Результаты частично согласовались с отдельными predictions, но одновременно существенно оспорили ключевые положения обеих теорий. Для GNWT, в частности, были проблемы с некоторыми ожидаемыми ignition/prefrontal predictions.

Вывод для MINDRA:

- нельзя описывать GNWT как подтверждённый биологический факт;
- нельзя infer consciousness из software workspace;
- сильные claims должны быть hypothesis-specific и pre-registered;
- отрицательные/частичные результаты сохраняются и меняют design только через review/ADR.

---

# 8. AI workspace ablation studies 2025–2026 — использовать осторожно

## 8.1. Phua 2025

**Can We Test Consciousness Theories on AI? Ablations, Markers, and Robustness.**  
arXiv:`2512.19155`.

Работа строит artificial reference agents и использует workspace lesions/capacity interventions. Авторы отдельно подчёркивают, что такие агенты не заявляются как conscious.

Полезный вывод:

- workspace capacity и broadcast можно operationalize через ablations;
- необходимо проверять noise amplification/robustness, а не только средний performance;
- такая работа остаётся preprint/research evidence и не определяет MINDRA architecture.

## 8.2. Shang 2026

**"Theater of Mind" for LLMs: A Cognitive Architecture Based on Global Workspace Theory.**  
arXiv:`2604.08206`.

Предлагается GWT-inspired LLM agent architecture с central broadcast hub и heterogeneous agents.

Вывод для MINDRA:

- GWT-inspired LLM orchestration является активным направлением;
- central event-driven hub не принимается автоматически: MINDRA сохраняет scheduler/dependency semantics;
- конкретные entropy drives/memory mechanisms этой работы не переносятся.

---

# 9. Cognitive Workspace / active context management

Tao An.  
**Cognitive Workspace: Active Memory Management for LLMs — An Empirical Study of Functional Infinite Context.**  
arXiv:`2508.13171`, 2025.

Работа рассматривает active management ограниченного task context поверх внешней памяти.

Вывод для MINDRA:

- dynamic curation context является practical problem для LLM agents;
- однако Workspace MINDRA не равен long-context/RAG manager;
- Memory retrieval, Workspace admission и Cortex context packing остаются тремя отдельными operations.

---

# 10. Shared workspace может создавать process loss

Современные multi-agent/shared-workspace studies показывают общий engineering warning: дополнительный общий канал может не только помогать coordination, но и создавать overhead/process loss.

Для MINDRA это означает обязательные metrics:

```text
coordination gain
communication overhead
noise propagation
contention
capacity sensitivity
robustness under irrelevant candidates
```

Workspace не считается полезным только потому, что архитектура выглядит более «когнитивной».

---

# 11. Почему MINDRA не принимает один neural latent workspace

Возможны implementations:

```text
structured item buffer
slot-based workspace
shared latent bottleneck
cross-attention workspace
recurrent global state
hybrid semantic + latent workspace
```

Canonical design должен пережить замену implementation.

Причины:

- MINDRA уже требует source/provenance semantics;
- learned latent может drift'ить;
- Cortex может быть remote/no-hidden-state;
- causal intervention легче проводить на structured items;
- первая домашняя/Colab версия должна оставаться вычислительно доступной.

---

# 12. Почему broadcast в MINDRA — availability, а не callback

Большая часть biological/cognitive literature использует термин `broadcast` концептуально.

В software architecture push-callback interpretation создала бы:

- hidden execution order;
- recursive module invocation;
- event-bus coupling;
- сложности deterministic replay.

Поэтому MINDRA operationalizes broadcast как:

> committed Workspace content доступен всем declared eligible consumers в их обычной scheduled phase.

Это сохраняет `DU-02/05` invariants.

---

# 13. Evaluation controls, вытекающие из literature

Минимум:

```text
Full Workspace
NoWorkspace / DirectReads
Random admission
Shuffled admission
Fixed recency/latest-K
Unbounded workspace
Workspace without broadcast
Matched shared buffer
Matched recurrent buffer
```

Capacity sweep:

```text
0 → small → medium → large → unbounded
```

Lesions:

```text
selection intact, broadcast removed
broadcast intact, selection randomized
capacity reduced
producer/consumer access selectively removed
```

Это позволяет разделить:

- эффект дополнительного state;
- эффект competition;
- эффект bottleneck;
- эффект shared availability.

---

# 14. Research claim boundary

Даже при положительном результате допустим claim класса:

> bounded temporary shared workspace улучшил cross-module integration при заданных условиях.

Недопустимый leap:

> Workspace доказал сознание/субъективность MINDRA.

Это остаётся общим принципом проекта.

---

# 15. Итог для DU-21

Исследовательский landscape поддерживает **экспериментально проверяемую workspace boundary**, но не требует её безусловного существования и тем более не обосновывает consciousness claim.

Поэтому DU-21 принимает:

```text
bounded
source-preserving
temporary
shared broadcast overlay
+
first-class NoWorkspace
+
matched controls
+
explicit negative gate
```

а конкретный neural/global-workspace algorithm оставляет version design.
