# Research pass DU-10 — актуальный Cortex landscape

## Статус

**Дата среза:** 2026-08-17  
**Назначение:** исследовательская справка для `DU-10 — Cortex Boundary`  
**Статус:** non-canonical evidence

Этот документ фиксирует актуальное состояние нескольких implementation candidates и tooling на момент проектирования `DU-10`.

Он **не выбирает canonical Cortex backend**. Конкретная model family и размер выбираются позднее в version design после появления точных compute/evaluation requirements.

---

# 1. Почему выбор Cortex нельзя фиксировать в canonical architecture

Актуальные небольшие open-weight models существенно различаются по:

- поддерживаемым языкам;
- context length;
- text-only vs multimodal input;
- лицензии;
- доступности через local libraries/servers/providers;
- hidden-state/gradient access;
- resource profile;
- instruction/reasoning behavior.

Следовательно, архитектура должна фиксировать semantic capabilities и provenance, а model selection — оставаться version-specific.

---

# 2. Qwen3.5-2B

Официальная model card:

- https://huggingface.co/Qwen/Qwen3.5-2B

На дату среза model card указывает:

- 2B language-model parameters;
- 24 language-model layers;
- hidden dimension 2048;
- native context length 262,144;
- unified vision-language capability;
- поддержку 201 языков и диалектов;
- Apache-2.0 license;
- intended use cases, включающие prototyping, task-specific fine-tuning и research/development;
- доступ через Transformers, vLLM, SGLang и inference providers.

Для MINDRA это делает семейство особенно интересным как **будущий small/main experimental Cortex candidate**, но не архитектурным требованием.

Model card также показывает значительный разрыв качества между 0.8B и 2B внутри одной family, что поддерживает идею иметь small debug backbone и более сильный main backbone в version-specific experiments.

---

# 3. Qwen3.5-4B

Официальная model card:

- https://huggingface.co/Qwen/Qwen3.5-4B

4B-вариант представляет естественный scale-up candidate той же family.

Полезность для MINDRA:

- можно сравнивать одну архитектуру с разными backbone scale;
- adapter/rendering semantics остаются близкими внутри family;
- можно отделять architecture gain от raw backbone capability gain.

Конкретное использование 4B зависит от доступного compute и будущего training plan.

---

# 4. Gemma 3 4B

Официальная model card:

- https://huggingface.co/google/gemma-3-4b-it

На дату среза Google указывает для Gemma 3:

- open weights;
- text+image input и text output для соответствующих sizes;
- context window 128K;
- поддержку более 140 языков;
- несколько размеров семейства.

Это полезный alternative-family candidate для transfer tests Cortex boundary.

Особенно важно, что наличие multimodal capability не должно заставлять MINDRA обходить Perception boundary: model capability и архитектурный input contract являются разными уровнями.

---

# 5. Llama 3.2 3B

Официальная model card:

- https://huggingface.co/meta-llama/Llama-3.2-3B

Model card указывает:

- 3.21B parameters для 3B variant;
- text input/output;
- context length 128K;
- instruction-tuned multilingual use cases;
- восемь официально поддерживаемых языков: English, German, French, Italian, Portuguese, Hindi, Spanish и Thai;
- custom Llama 3.2 Community License.

Русский язык не входит в восемь официально поддерживаемых языков model card.

Для MINDRA это хороший пример того, почему нельзя считать label `multilingual` достаточным: project-level evaluation должна отдельно проверять required languages.

---

# 6. Hidden states и local research capabilities

Официальная документация Transformers:

- https://huggingface.co/docs/transformers/main_classes/output

Transformers model outputs могут возвращать `hidden_states` при включённом `output_hidden_states` для поддерживающих model implementations.

Это подтверждает реализуемость local Cortex research adapters для:

- hidden-state inspection;
- representation extraction;
- mechanistic interventions.

Но remote provider может не предоставлять такую surface, поэтому hidden-state access остаётся optional Cortex capability.

---

# 7. Chat templates как backend-specific detail

Официальная документация Transformers:

- https://huggingface.co/docs/transformers/chat_templating

Chat models используют model-specific formatting через tokenizer `chat_template`.

Даже похожая semantic conversation может требовать разного token-level representation для разных models.

Это является прямым evidence в пользу принятой границы:

```text
semantic Cortex context
→ backend adapter
→ model-specific chat template/tokenization
```

а не хранения Qwen/Llama/Gemma prompt conventions внутри cognitive modules.

---

# 8. PEFT/adapters

Официальная документация:

- https://huggingface.co/docs/peft/main/package_reference/lora
- https://huggingface.co/docs/transformers/main_classes/peft

PEFT позволяет:

- загружать adapters поверх base model;
- хранить несколько adapters;
- активировать/деактивировать их;
- переключать active adapter;
- обучать adapter state без обязательного изменения всех base weights.

Это подтверждает, что future MINDRA Cortex identity должна различать:

```text
base model revision
≠
active adaptation/adapter revision
```

Но конкретный PEFT method выбирается только в `DU-26`/version design.

---

# 9. Design conclusions

Research pass поддерживает следующие решения `DU-10`:

1. Cortex нельзя связывать с одной model family.
2. Local и remote execution должны помещаться за одной semantic boundary, но иметь разную capability/reproducibility metadata.
3. Hidden states/gradients являются optional capabilities.
4. Prompt/chat template/tokenization должны принадлежать backend adapter.
5. Multilingual support должна быть explicit и проверяемой, а не выводиться из marketing/model-family label.
6. Cortex identity должна включать base model и active adaptation revisions.
7. `NoCortex` и alternative-family comparisons необходимы для измерения architecture gain.

---

# 10. Что проверить заново перед version selection

Поскольку model landscape быстро меняется, непосредственно перед выбором baseline для первой software version нужно повторно проверить:

- актуальные small open-weight models;
- лицензии;
- поддержку русского/английского;
- reasoning/agent benchmarks;
- context limitations;
- actual VRAM/Colab requirements;
- quantized variants;
- Transformers/PEFT compatibility;
- hidden-state interfaces;
- model-specific quirks;
- availability stable immutable weights/revisions.
