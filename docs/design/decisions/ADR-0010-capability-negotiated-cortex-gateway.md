# ADR-0010 — Capability-negotiated Cortex Gateway с backend-specific adapter boundary

## Статус

`accepted`

## Контекст

После `DU-08` MINDRA имеет backend-independent `Canonical Percept`, а после `DU-09` — explicit `Goal System`.

До проектирования Memory, World Model и остальных когнитивных механизмов нужно определить, как использовать pretrained language/semantic/reasoning model так, чтобы:

- конкретная LLM не стала центром архитектуры;
- backend можно было менять;
- local open-weight и remote black-box варианты могли сосуществовать;
- model-specific prompt/tokenization не протекали в cognitive modules;
- hidden-state/gradient capability не становилась обязательной;
- Cortex мог помогать grounding/reasoning, не получая ownership Goals/Policy/Memory.

---

# Рассмотренные варианты

## Вариант A — конкретная LLM как фактическое ядро MINDRA

```text
Qwen/Gemma/Llama
=
central Agent API/state/reasoning
```

Плюсы:

- минимальная интеграционная работа;
- легко быстро получить сильное поведение;
- можно использовать native prompt/tool conventions model family.

Минусы:

- вся архитектура начинает зависеть от tokenizer/prompt/hidden size;
- backbone swap становится redesign;
- `NoCortex` baseline искусственен;
- трудно отделить architecture gain от capability backbone;
- Cortex легко начинает владеть Goal/Memory/Policy de facto;
- remote provider и local model имеют разные interfaces.

**Отклонено.**

---

## Вариант B — унифицировать всё до `generate(prompt) -> text`

Плюсы:

- почти любой LLM/provider совместим;
- простой API;
- легко тестировать.

Минусы:

- semantic context смешивается с model-specific prompt rendering;
- structured results приходится парсить ad-hoc;
- embeddings/hidden states/adapters невозможно выразить чисто;
- language/feature/research capabilities нельзя нормально согласовать;
- consumer вынужден знать prompt conventions;
- failure/context truncation часто маскируются.

**Отклонено как недостаточно выразительная canonical boundary.**

---

## Вариант C — Cortex как отдельный центральный cognitive module с ambient access ко всему Agent state

Плюсы:

- Cortex сам решает, какой context ему нужен;
- удобно централизовать reasoning;
- меньше явного context routing.

Минусы:

- скрытые зависимости на все остальные modules;
- Cortex превращается в фактический orchestrator;
- трудно проводить ablation и dependency review;
- Memory/Goal/Workspace boundaries размываются;
- remote/local backend differences проникают в scheduler/state;
- противоречит declared-read discipline.

**Отклонено.**

---

## Вариант D — capability-negotiated Cortex Gateway + backend adapter/provider

```text
cognitive consumer
→ semantic Cortex Request
→ Cortex Gateway
→ backend adapter
→ local/remote provider
→ normalized Cortex Result
→ consumer-owned effect
```

Плюсы:

- stable semantic boundary;
- concrete model/provider изолирован;
- local/remote backends совместимы на общей поверхности;
- optional hidden/embedding/gradient capabilities выражаются явно;
- chat template/tokenization остаются backend detail;
- `NoCortex`/Dummy/Control естественны;
- Cortex не получает ambient state access;
- Goals/Policy/Memory сохраняют ownership;
- исследовательские capability requirements можно проверять заранее.

Минусы:

- contract сложнее text-only API;
- требуется capability negotiation;
- backend adapters нужно поддерживать отдельно;
- structured result validation и provenance требуют дополнительной инфраструктуры;
- разные backends не всегда функционально эквивалентны.

**Принято.**

---

# Принятое решение

MINDRA использует `Cortex` как **agent-owned shared capability boundary**, а не как semantic owner глобального когнитивного state.

Каноническая схема:

```text
Declared consumer state/context
        ↓
Semantic CortexRequest
        ↓
Cortex Gateway
        ↓
Backend Adapter
        ↓
Execution Provider
        ↓
Normalized CortexResult
        ↓
Consumer interprets/publishes owner-authorized effect
```

## Cortex Gateway

- знает stable semantic contract;
- проверяет required capabilities;
- не читает весь `CognitiveState`;
- не выбирает Goal/Action;
- не делает hidden fallback;
- нормализует status/provenance/resource evidence.

## Backend Adapter

Изолирует:

- tokenizer/processor;
- chat template;
- prompt rendering;
- provider-specific request/response;
- native structured output;
- model-specific hidden/representation interface.

## Provider

Может быть local или remote.

Physical provider boundary не меняет logical ownership Cortex.

## Capabilities

Core inference capability отделена от optional:

- structured generation;
- embeddings;
- hidden states;
- attentions/logits;
- multimodal input;
- latent input;
- gradients;
- trainability/adapters;
- raw interventions.

`chain-of-thought` не является обязательной capability.

## Consumer ownership

Cortex Result не получает прямой write authority в `Goal Graph`, Memory, Policy или другие namespaces.

---

# Последствия

## Положительные

- модель можно менять без redesign независимых модулей;
- `NoCortex` остаётся first-class baseline;
- local/remote backend различия становятся explicit capabilities;
- model-specific prompt/tokenization не протекают в cognition;
- hidden-state experiments возможны, но не диктуют общий contract;
- PEFT/adaptation может добавляться позднее без изменения смысловой границы;
- Cortex contribution можно измерять отдельно от MINDRA architecture gain.

## Отрицательные

- потребуется поддерживать adapters для разных model families/providers;
- capability matrix усложняет composition/evaluation;
- backend swap не гарантирует одинаковое качество даже при одинаковом semantic contract;
- opaque remote providers дают более слабую reproducibility;
- нужно явно обрабатывать context limits/structured parse failures.

---

# Что решение намеренно не определяет

ADR не выбирает:

- конкретную LLM;
- размер backbone;
- конкретный inference engine;
- конкретный provider;
- quantization;
- LoRA/QLoRA;
- exact Request/Result Python types;
- prompt templates;
- context-compaction algorithm;
- exact multilingual thresholds.

Эти вопросы остаются version-specific/downstream decisions.
