# DU-11 — Memory landscape, август 2026

## Статус

**Тип:** dated research evidence  
**Дата проверки:** 17 августа 2026 года  
**Статус:** non-canonical evidence

Этот документ фиксирует внешний research/implementation landscape, использованный при проектировании `DU-11 — Memory Core`.

Он **не является source of truth архитектуры**. Канонический design находится в `docs/design/modules/memory.md` и `ADR-0011`.

---

# 1. Задача исследования

Нужно было проверить, насколько практически и научно обоснованы следующие design-идеи:

- отделение long-term Memory от Cortex context window;
- отдельный canonical store и retrieval layer;
- structured + vector retrieval;
- сохранение source content отдельно от embedding/index;
- explicit memory retrieval;
- проблемы representation drift;
- возможность нейтрального Memory Core до importance/salience/consolidation.

---

# 2. MemGPT

Источник:

- Packer et al., **MemGPT: Towards LLMs as Operating Systems**, arXiv:2310.08560.

Ключевая идея работы — отделение ограниченного active context LLM от более крупной внешней памяти и явное управление переносом информации между memory tiers.

Для MINDRA это полезно как evidence того, что:

```text
Cortex context window
≠
long-term agent memory
```

Но MINDRA не принимает OS/virtual-context abstraction MemGPT как canonical architecture.

---

# 3. MemoryBank

Источник:

- Zhong et al., **MemoryBank: Enhancing Large Language Models with Long-Term Memory**, arXiv:2305.10250.

MemoryBank демонстрирует внешний long-term memory bank с retrieval и отдельной memory-update/forgetting логикой.

Для DU-11 полезно само разделение:

```text
stored memory
retrieval
update/forgetting policy
```

Однако importance/forgetting mechanism MemoryBank **не переносится** в DU-11: MINDRA специально откладывает salience/retention/forgetting до `DU-19/20`.

---

# 4. LongMem

Источник:

- Wang et al., **Augmenting Language Models with Long-Term Memory**, arXiv:2306.07174.

LongMem использует decoupled memory architecture: frozen backbone выступает memory encoder, а отдельная сеть выполняет retrieval/reading.

Для MINDRA особенно полезна сама идея decoupling memory storage/retrieval от backbone behavior.

При этом DU-11 идёт дальше в сторону backend independence: canonical MemoryRecord не должен зависеть от конкретного frozen encoder.

---

# 5. Titans и neural memory

Источник:

- Behrouz et al., **Titans: Learning to Memorize at Test Time**, arXiv:2501.00663.

Titans рассматривает learned neural long-term memory как часть sequence-model architecture и показывает, что test-time neural memorization является практически значимым направлением.

Для MINDRA вывод следующий:

> neural memory является реалистичной future implementation family, но её не следует делать единственным canonical Memory representation на базовом архитектурном уровне.

Причины:

- труднее получить stable semantic identity отдельного memory item;
- сложнее провести record-level deletion/shuffle/intervention;
- storage, learning и retrieval сильнее смешиваются;
- source/provenance сложнее сохранять независимо от neural state.

Поэтому neural memory остаётся future candidate capability/implementation после отдельного design review.

---

# 6. Neuro-symbolic memory

Источник:

- Jiang et al., **Advancing Multimodal Agent Reasoning with Long-Term Neuro-Symbolic Memory**, arXiv:2603.15280.

Работа NS-Mem сочетает episodic, semantic и logic layers, а retrieval объединяет neural similarity и symbolic query mechanisms.

Для MINDRA это важное evidence против архитектуры:

```text
Memory = только vector similarity
```

Hybrid structured/vector retrieval является реалистичным и полезным направлением.

Однако DU-11 не принимает конкретную трёхслойную схему NS-Mem и не вводит logic-rule memory как обязательный модуль.

---

# 7. Proactive memory

Источник:

- Wu et al., **Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents**, arXiv:2607.08716.

Работа показывает, что selective/proactive injection памяти может отличаться по эффекту от always-on exposure или пассивного retrieval.

Для MINDRA это является аргументом **не помещать proactive reminder policy внутрь нейтрального Memory Core**.

Такой механизм затрагивает:

- Salience;
- Executive Control;
- context allocation;
- Policy.

Поэтому он относится к более поздним DU.

---

# 8. Representation drift

Источник:

- van der Veldt et al., **Learning continually with representational drift**, arXiv:2512.22045.

Работа подчёркивает, что learned representations в continual systems могут изменяться со временем.

Для MINDRA это усиливает requirement:

```text
canonical memory content
≠
current embedding representation
```

Если encoder адаптируется, старые embeddings не должны считаться автоматически совместимыми с новыми.

Поэтому DU-11 требует versioned feature spaces и сохранение semantic/source content, позволяющего re-encoding или migration.

---

# 9. FAISS как implementation evidence

Источник:

- `facebookresearch/faiss`, официальная wiki документация.

Актуальная документация показывает несколько разных типов индексов:

- exact `IndexFlat`;
- HNSW;
- IVF;
- PQ/quantized variants;
- разные distance metrics.

FAISS отдельно различает index structure и ID mapping; cosine similarity требует определённой normalization/metric semantics.

Для MINDRA это подтверждает:

> vector index является поисковой implementation structure с собственной metric/config/version semantics, а не естественным semantic identity layer Memory.

Конкретно FAISS пока не выбран.

---

# 10. Архитектурный вывод

Исследованный landscape показывает несколько независимых memory paradigms:

```text
context management
external memory banks
vector retrieval
structured/symbolic retrieval
neural test-time memory
proactive memory control
consolidated episodic/semantic memory
```

Нет оснований делать одну из них определением Memory MINDRA.

Для базовой архитектуры наиболее устойчивой является схема:

```text
canonical source-preserving MemoryRecord
        ↓
derived versioned representations
        ↓
replaceable retrieval indexes/strategies
        ↓
explicit RetrievalRequest/Result
```

Она оставляет открытыми future implementations и сохраняет research interpretability.

---

# 11. Что требуется перепроверить перед implementation version

Поскольку технологии быстро меняются, перед выбором concrete Memory stack потребуется заново проверить:

- актуальное состояние FAISS/HNSW/vector database libraries;
- local embedded stores;
- metadata-filtering support;
- deterministic snapshot/rebuild properties;
- embedding models и multilingual performance;
- возможные lightweight learned retrieval approaches;
- GPU/CPU/RAM trade-offs для Colab и локального режима.
