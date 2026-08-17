# Research pass — Memory Regulation / Consolidation landscape

## Статус

**Связанный Design Update:** `DU-20 — Memory Regulation / Consolidation`  
**Дата среза:** 2026-08-17  
**Статус:** non-canonical research evidence

Этот документ фиксирует внешний исследовательский контекст, использованный при проектировании `DU-20`.

Он не выбирает конкретную forgetting curve, LLM summarizer, replay priority formula, clustering algorithm, generative replay model или continual-learning method как обязательную реализацию MINDRA.

---

# 1. Исследовательские вопросы

Проверялись вопросы:

1. Нужно ли разделять fast episodic storage и slower consolidation?
2. Следует ли consolidation запускать после каждого опыта?
3. Должны ли raw episodic records сохраняться после derivation?
4. Как memory budget влияет на выбор retain vs consolidate?
5. Чем replay внутри Agent отличается от training replay?
6. Как prioritization может влиять на replay efficiency?
7. Какие риски создаёт LLM-based continuous rewriting memories?
8. Как сохранить provenance/contradictions при semantic abstraction?
9. Где проходит граница consolidation и slow-weight learning?
10. Какие controls нужны, чтобы consolidation не получала credit за простое compression/context reduction?

---

# 2. Complementary Learning Systems

James L. McClelland, Bruce L. McNaughton, Randall C. O'Reilly.  
**Why There Are Complementary Learning Systems in the Hippocampus and Neocortex.**  
Psychological Review, 1995.

Классическая CLS-гипотеза мотивирует две complementary функции:

```text
быстрое сохранение конкретных episodes
+
более медленное interleaved извлечение общей структуры
```

В исходной computational логике rapid storage помогает избегать вмешательства новых эпизодов в уже сформированное distributed knowledge, а replay/interleaving позволяет постепенно интегрировать новое.

Вывод для MINDRA:

- быстрый canonical episodic `MemoryRecord` и derived/consolidated knowledge полезно архитектурно разделять;
- consolidation не обязана заменять episodic evidence;
- slow-weight/neural integration логично отделять от immediate memory write;
- биологические hippocampus/neocortex не копируются буквально как модули.

---

# 3. Generalization-optimized systems consolidation

Работа **Organizing memories for generalization in complementary learning systems** (2023) показывает computational tension: неограниченный перенос episodic memories в slow/generalized system способен ухудшать generalization; consolidation полезно регулировать по её влиянию на generalization, а не автоматически переносить всё.

Вывод:

> `all episodic memories → consolidate` не является безопасным canonical default.

Для MINDRA нужны gated consolidation и `NoConsolidation` control.

---

# 4. Similarity-weighted interleaved learning

Работа 2022 года **Learning in deep neural networks and brains with similarity-weighted interleaved learning** показывает, что для gradual integration не обязательно replay'ить весь старый dataset: interleaving subset старых, representationally related items может снизить catastrophic interference при меньшей стоимости.

Вывод:

- replay selection действительно может иметь functional value;
- similarity/coverage может быть одним из candidate evidence;
- конкретный SWIL algorithm не становится Memory Regulation MINDRA;
- actual gradient learning остаётся `DU-26`.

---

# 5. Prioritized Experience Replay

Tom Schaul, John Quan, Ioannis Antonoglou, David Silver.  
**Prioritized Experience Replay.**  
2015.

PER показывает, что sampling past transitions не обязан быть uniform: выбор более informative/learning-relevant transitions способен улучшать RL learning efficiency.

Для MINDRA важно только общее evidence:

```text
which past items are replayed
→ может иметь causal effect
```

Но:

```text
Agent Memory Replay
≠
DQN replay buffer
```

TD-error priority не становится canonical memory importance.

---

# 6. Generative Replay и catastrophic forgetting

Deep Generative Replay (2017) и related dual-memory continual-learning approaches используют generated/replayed old experience для уменьшения catastrophic forgetting при sequential learning.

Вывод:

- replay/consolidation может быть мостом к future continual learning;
- source-preserving memory может поставлять evidence для такого training;
- generative replay model и optimizer update относятся к `DU-26`, а не к DU-20.

---

# 7. Generative Agents / reflection

**Generative Agents: Interactive Simulacra of Human Behavior** (2023) использует memory stream, retrieval и higher-level reflection over observations. Эта работа является важным precedent того, что derived higher-level records способны улучшать agent behavior.

Но для MINDRA:

- reflection является возможной family consolidation;
- human-believability objective не является нашим evaluation target;
- importance/recency/relevance formula не становится canonical;
- raw/source lineage должна быть строже, чем в narrative agent prototypes.

---

# 8. MemoryBank / forgetting curves

**MemoryBank** (2023) использует механизм forgetting/reinforcement, вдохновлённый Ebbinghaus forgetting curve и memory significance.

Вывод:

- explicit aging/forgetting policy технически реализуема;
- anthropomorphic forgetting curve не следует принимать universal законом;
- logical time, source type и task context MINDRA требуют собственной evaluation.

---

# 9. RecMem 2026 — consolidation по recurrence

**RecMem: Recurrence-based Memory Consolidation for Efficient and Effective Long-Running LLM Agents** (2026) предлагает не обрабатывать каждый incoming interaction дорогой LLM consolidation. Сначала interactions остаются в lightweight memory, а episodic/semantic extraction запускается при устойчивой recurrence семантически похожего опыта.

Авторы сообщают существенное снижение construction token cost при сохранении/улучшении accuracy относительно сравниваемых систем.

Вывод для MINDRA:

- consolidation timing является самостоятельной policy;
- recurrence — разумный candidate trigger/evidence;
- eager consolidation не обязательна;
- concrete RecMem architecture не принимается.

---

# 10. Useful Memories Become Faulty When Continuously Updated by LLMs — 2026

Работа **Useful Memories Become Faulty When Continuously Updated by LLMs** исследует continuous textual consolidation agent memories.

Ключевой результат для DU-20: даже из полезного/правильного опыта repeatedly consolidated textual memories могут деградировать; utility сначала растёт, а затем падает, причём episodic-only control оказывается конкурентоспособным, а forced consolidation может вредить.

Вывод:

```text
consolidation
≠
automatic improvement
```

Это сильная мотивация для:

- source/raw retention;
- gated consolidation;
- historical derived records вместо overwrite;
- `NoConsolidation` baseline;
- evaluation false-memory/regression rate.

---

# 11. Retain or Consolidate? — 2026

**Retain or Consolidate? Budget-Dependent Operator Selection for Language Agent Memory** формализует trade-off raw retention и consolidation при ограниченном context/memory budget.

Работа показывает budget-dependent crossover: под tight budget abstraction/consolidation может повышать coverage и accuracy, а при более свободном budget retention raw evidence может быть предпочтительнее.

Вывод для MINDRA:

- explicit `MemoryBudget` должен быть частью decision context;
- «consolidation лучше retention» не является универсальным утверждением;
- разные consolidation operators могут иметь разный replacement harm;
- budget-aware policy лучше hard-coded always-consolidate.

---

# 12. Episodic-to-Semantic Consolidation Without Identity Drift — 2026

Работа предлагает deterministic episodic→semantic derivation как separately addressable semantic layer с explicit supporting-event provenance, не изменяя основной certified identity агента.

Для MINDRA особенно полезен общий pattern:

```text
episodic evidence
→ new semantic records
```

а не:

```text
rewrite planner/prompt/identity
```

Мы переносим принцип source-addressable derived records, но не cryptographic identity model конкретной работы.

---

# 13. Provenance laundering risk — 2026

Работа **Memory Provenance Laundering in LLM Agents** описывает риск, когда consolidation сохраняет содержимое/trigger, но стирает происхождение и authority source, после чего derived memory выглядит более доверенной, чем исходное наблюдение.

Вывод для MINDRA:

- derivation не должна повышать provenance/authority автоматически;
- platform/architecture-owned provenance нельзя заменять LLM-generated prose;
- consolidated record должен ссылаться на sources и сохранять authority constraints;
- source deletion требует обновления support status derived records.

---

# 14. Основной research вывод DU-20

Evidence поддерживает не один algorithm, а архитектурную дисциплину:

```text
rapid source-preserving episodic storage
+
explicit budget-aware regulation
+
selective replay
+
gated source-preserving consolidation
+
separate future slow-weight learning
```

Наиболее опасные shortcuts:

```text
one memory importance score
always consolidate
rewrite old memory in place
retrieval count = importance
summary = truth
consolidation = training
```

---

# 15. Что должно проверяться экспериментально

Future MINDRA-Eval должен отдельно проверять:

```text
retention under fixed memory budget
raw episodic vs consolidated accuracy
source-detail loss
false derived memory rate
contradiction retention
generalization
retrieval usefulness
behavioral outcome
compression/context efficiency
policy sensitivity to Salience/value/internal state
confirmation/popularity bias
```

Нужны matched conditions, где одинаковы:

- Agent/Cortex;
- memory budget;
- retrieval budget;
- environment distribution;
- compute allowance;
- source experience.

---

# 16. Non-canonical implementations/candidates

На будущих version stages можно исследовать:

- FIFO/LRU/random;
- weighted multi-signal retention;
- diversity-aware selection;
- reservoir sampling;
- prioritized replay variants;
- recurrence-triggered consolidation;
- structured deterministic aggregation;
- LLM summarization/reflection;
- clustering/prototypes;
- rule extraction;
- generative replay;
- learned memory-management policy.

Ни один из этих вариантов не становится обязательным из-за этого research pass.
