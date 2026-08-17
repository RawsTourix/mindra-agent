# Cortex Boundary MINDRA

## Статус документа

**Design Update:** `DU-10 — Cortex Boundary`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет:

- место `Cortex` в логической архитектуре MINDRA;
- backend-neutral semantic capability boundary;
- различие `Cortex Gateway`, backend adapter и physical execution provider;
- обязательные и optional capabilities;
- semantic request/context/result boundary;
- правила доступа к `Canonical Percept`, Goal state и будущим Memory/Workspace данным;
- text/structured/feature/latent semantics;
- local/remote execution;
- frozen/adapted modes;
- identity/revision/provenance;
- multilingual requirements;
- resource/context/failure semantics;
- `NoCortex`/`DummyCortex`/control configurations;
- observability/intervention requirements.

Документ опирается на:

- [`../system-context.md`](../system-context.md) — Cortex является логической capability внутри Agent независимо от физического provider;
- [`../dependency-rules.md`](../dependency-rules.md) — consumers зависят от stable capability contract, а не concrete backend/SDK;
- [`../execution-model.md`](../execution-model.md) — Cortex computation принадлежит определённому causal context и `agent_revision`;
- [`../cognitive-state.md`](../cognitive-state.md) — Cortex не получает ambient access ко всему shared/private state;
- [`../module-lifecycle.md`](../module-lifecycle.md) — dependency/lifecycle/failure semantics остаются явными;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — passive evidence отделено от active intervention;
- [`perception.md`](perception.md) — Cortex hidden space не является `Canonical Percept`;
- [`goals.md`](goals.md) — Cortex может участвовать в grounding/proposal generation, но не владеет `Goal Graph`.

Документ намеренно **не** определяет:

- конкретную LLM как canonical Cortex;
- exact Python `Protocol`/ABC;
- Transformers/vLLM/SGLang/llama.cpp/API provider как обязательный runtime;
- prompt templates конкретной модели;
- точные token budgets;
- конкретный quantization format;
- LoRA/QLoRA как обязательный training mechanism;
- точный механизм Memory retrieval — `DU-11`;
- World Model/Self Model — `DU-12/13`;
- policy/planner semantics — `DU-23`;
- training/update lifecycle Cortex — `DU-26`;
- checkpoint packaging — `DU-27`.

---

# 1. Цель DU-10

MINDRA нужен доступ к богатой pretrained semantic/language/reasoning capability, но архитектура не должна превращаться в оболочку вокруг одной LLM.

Канонический invariant:

```text
MINDRA Agent
≠
Cortex
≠
конкретная LLM
```

Cortex — **заменяемая agent-owned capability**, которую независимые cognitive components могут использовать через stable semantic boundary.

Cortex не является:

- владельцем всего `CognitiveState`;
- Goal System;
- Memory;
- Policy;
- World Model;
- универсальным representation space;
- скрытым central orchestrator;
- обязательным условием существования MINDRA.

`NoCortex` остаётся архитектурно полноценной конфигурацией.

---

# 2. Главное архитектурное решение

MINDRA принимает **capability-negotiated Cortex Gateway с semantic request/result contract и backend-specific adapter/provider boundary**.

Conceptually:

```text
Cognitive consumer
  declared inputs only
        ↓
Cortex semantic request
        ↓
┌──────────────────────────┐
│      Cortex Gateway      │
│ stable semantic boundary │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Cortex Backend Adapter   │
│ context rendering        │
│ chat template/tokenizer  │
│ provider/model mapping   │
│ output parsing           │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Execution Provider       │
│ local model / server/API │
└────────────┬─────────────┘
             ↓
       backend result
             ↓
 semantic validation
             ↓
      Cortex Result
             ↓
Cognitive consumer
```

Это решение дополнительно фиксируется в `ADR-0010`.

---

# 3. Cortex — capability, а не semantic owner чужого state

## 3.1. Логическая принадлежность

Cortex относится к MINDRA Agent по `DU-01`.

Его physical execution может происходить:

- в том же process;
- на локальном GPU;
- в отдельном worker;
- на другом host/GPU;
- через self-hosted inference server;
- через remote provider, если contract/research requirements это допускают.

Физическое размещение не меняет logical ownership.

## 3.2. Cortex не получает ambient state access

Запрещён pattern:

```text
Cortex Gateway
→ read entire CognitiveState
→ inspect Memory directly
→ inspect Goal System private state
→ decide what context seems useful
```

Cortex invocation получает **явно подготовленный semantic context**, сформированный из declared inputs вызывающего cognitive computation.

Следовательно:

```text
Cortex knows only provided request/context
```

а не:

```text
Cortex knows everything Agent currently stores
```

Это сохраняет dependency discipline, ablation и causal interpretability.

## 3.3. Cortex Result не становится canonical truth автоматически

Если Cortex выдал утверждение, prediction, interpretation или proposal, это не превращает результат автоматически в:

- observed fact;
- Goal;
- Memory;
- World Model state;
- selected Action.

Consumer обязан интерпретировать результат в рамках собственного semantic contract и при необходимости сформировать owner-authorized proposed update/proposal.

---

# 4. Cortex Gateway

## 4.1. Назначение

`Cortex Gateway` — stable agent-facing capability boundary между cognitive code и concrete pretrained backend.

Он отвечает за:

- capability discovery/validation;
- прием backend-neutral request;
- проверку declared capability requirements;
- передачу semantic context backend adapter;
- вызов execution provider;
- нормализацию status/provenance/resource evidence;
- semantic validation результата настолько, насколько это возможно contract-level;
- возврат backend-neutral `Cortex Result`.

Gateway **не** должен:

- самостоятельно выбирать task-level goal/action;
- читать произвольные Agent fields;
- добавлять скрытые Memory fragments;
- менять Goal Graph;
- скрыто переключать backend;
- использовать evaluator-only data;
- silently retry другим model/provider без explicit policy/provenance.

## 4.2. Shared capability boundary

Cortex не обязан быть отдельным cognitive module, исполняемым своей scheduler wave.

Он может использоваться как **явно injected shared capability** внутри computation другого cognitive component.

При этом:

- dependency должна быть на Cortex semantic contract, не concrete backend;
- Cortex invocation является отдельным traceable sub-operation соответствующего `Module Attempt`;
- invoking module всё равно читает только собственные declared inputs;
- Cortex не получает право вызвать peer module/scheduler recursively;
- любой causally visible canonical effect публикует semantic owner вызывающего/последующего модуля, а не backend.

Если будущий design потребует отдельной request-queue/module scheduling модели Cortex, это будет отдельный design change, а не implicit implementation choice.

---

# 5. Semantic Cortex Request

Cortex не должен принимать model-specific raw prompt как канонический вход MINDRA.

Conceptually:

```text
CortexRequest
├── request identity
├── operation / required capabilities
├── semantic context fragments[]
├── requested output contract
├── language/locale requirements?
├── compute/generation budget?
├── stochastic/deterministic policy?
├── causal identities
└── provenance
```

Exact type/field names не frozen.

## 5.1. Operation semantics

Request должен описывать **что требуется семантически**, а не какой chat template вызвать.

Примеры классов операций:

```text
semantic generation
structured semantic transformation
grounding / interpretation
classification / scoring-like inference
representation / embedding request
```

Это candidate capability classes, не обязательный enum.

## 5.2. Context fragments

Контекст передаётся как typed/revisioned semantic fragments.

Источниками могут быть, если consumer имеет declared access:

- `Canonical Percept` или его часть;
- committed Goal state/selected goal projection;
- External Task Specification через соответствующий ingress/grounding component;
- в будущем Memory retrieval result;
- в будущем Workspace/Executive/Planner state;
- explicit instruction/constraint конкретного consumer.

Каждый fragment должен сохранять достаточную source/provenance identity.

## 5.3. Context selection не является скрытой функцией Gateway

Gateway не должен самостоятельно обходить Agent state в поисках «полезного контекста».

Выбор semantic fragments принадлежит вызывающему cognitive responsibility и его declared dependencies либо будущему отдельно спроектированному context-control mechanism.

Backend adapter может:

- сериализовать;
- форматировать;
- токенизировать;
- применять model-specific chat template;
- преобразовывать structure в поддерживаемое backend представление.

Но adapter не должен молча менять **семантический набор фактов/целей/памяти**, который был передан request.

---

# 6. Backend-specific rendering boundary

Разные chat/instruct models используют разные:

- tokenizers/processors;
- role tokens;
- chat templates;
- reasoning markers;
- multimodal formatting;
- structured-output conventions.

Поэтому model-specific rendering является обязанностью `Cortex Backend Adapter`, а не cognitive consumers.

Правильная схема:

```text
semantic CortexContext
        ↓
backend adapter
        ↓
Qwen/Gemma/Llama/provider-specific prompt/messages/tokens
```

Запрещено:

```text
Goal System / Policy / Memory
→ вручную строит Qwen chat template
```

или:

```text
consumer зависит от tokenizer vocabulary/model special tokens
```

---

# 7. Capability model

## 7.1. Зачем capabilities explicit

Open-weight local model и remote black-box provider могут предоставлять разный уровень доступа.

Поэтому общий Cortex contract не требует максимальной capability каждого backend.

Каждый backend публикует descriptor/capability set.

## 7.2. Core inference capability

Активная normal Cortex implementation должна предоставлять минимум capability класса:

```text
semantic input
→ pretrained semantic/language inference
→ semantic/text result
```

Exact model family не важна.

## 7.3. Optional capabilities

Contract должен допускать, но **не требовать от каждого backend**:

```text
structured generation / constrained output
embedding / representation extraction
hidden-state export
attention export
logits / token-score access
KV/cache inspection
multimodal attachments
latent/soft input injection
raw representation intervention
gradient access
trainable/adaptable weights
adapter management
streaming
batch inference
```

Наличие optional capability должно быть explicit и проверяемо до запуска experiment/composition.

## 7.4. Reasoning trace не является обязательным output

MINDRA не требует chain-of-thought/internal reasoning text как часть Cortex contract.

Cortex может выполнять сложный inference без раскрытия внутренней reasoning trace.

Канонические downstream mechanisms должны зависеть от проверяемого semantic result, а не от наличия приватного CoT конкретной model family/provider.

---

# 8. Cortex Result

Conceptually Cortex возвращает:

```text
CortexResult
├── request identity
├── status
├── semantic/text payload
├── structured payload? 
├── optional feature/representation payloads
├── capability-specific evidence?
├── backend/model/revision provenance
├── generation/inference configuration identity
├── resource/usage evidence
├── truncation/degradation metadata
└── intervention provenance?
```

Result не становится `CognitiveState` автоматически.

Consumer публикует только те owner-scoped effects, которые допускает его собственный contract.

## 8.1. Structured result

Если consumer запросил structured result:

- backend adapter может использовать native structured output, constrained decoding или text parsing;
- результат должен проходить schema/semantic validation;
- invalid parse не должен маскироваться под valid empty result;
- original/raw backend response может сохраняться как diagnostic artifact при допустимой policy.

---

# 9. Goal grounding boundary

`DU-09` установил:

```text
Natural-language instruction
≠
Committed Goal
```

Cortex может участвовать в grounding:

```text
External Task Specification
        ↓
Goal-grounding consumer
        ↓
Cortex semantic inference
        ↓
grounded objective candidate
        ↓
Goal Proposal
        ↓
Goal System
```

Cortex Gateway **не получает write authority** на `Goal Graph`.

Даже если concrete backend умеет tool/function calling, вызов условного `create_goal(...)` не должен bypass `Goal Proposal → Goal System` boundary.

---

# 10. Perception и Cortex-derived representations

`DU-08` установил, что Cortex hidden space не является `Canonical Percept`.

При наличии подходящей capability Cortex может породить optional representation, но она становится MINDRA `Feature View` только через explicit adapter с:

- `feature_space_id`;
- `feature_space_revision`;
- source identities;
- encoder/backend identity/revision;
- compatibility semantics;
- provenance.

Raw hidden-state tensor сам по себе **не является автоматически canonical Feature View**.

Это позволяет:

- использовать rich Cortex features;
- менять Cortex;
- отключать Cortex-derived view;
- измерять representation drift;
- не привязывать весь Agent к hidden dimension одного model family.

---

# 11. Multimodal Cortex

Cortex backend может быть multimodal.

Но multimodal capability не даёт права bypass Perception/Environment boundary.

Допустимы только agent-visible inputs с явной provenance.

Например, future visual attachment может быть передан через Perception-managed/reference boundary, если соответствующий design/contract это разрешает.

Недопустимо:

```text
Cortex directly reads Environment hidden framebuffer/world state
```

только потому, что model умеет принимать изображения.

---

# 12. Local и remote execution

## 12.1. Local backend

Local/open-weight backend потенциально позволяет:

- pin weights/revision;
- использовать hidden states;
- иметь gradients;
- делать PEFT/full adaptation;
- контролировать quantization/inference engine;
- более полно сохранять reproducibility evidence.

Но ни одна из этих возможностей не считается обязательной для semantic Cortex contract.

## 12.2. Remote backend

Remote provider допустим, если нужные для конкретного Run capabilities доступны и research validity не нарушена.

Remote backend может не предоставлять:

- hidden states;
- gradients;
- exact model weights;
- deterministic decoding;
- неизменяемую provider-side revision.

Эти ограничения должны отражаться в capability/provenance и experiment validity.

## 12.3. Opaque provider

Если provider не позволяет надёжно pin model/revision или может менять hidden system behavior, нельзя молча считать два запуска одним Cortex revision.

Для confirmatory experiment, требующего строгой Cortex identity, такой backend может быть непригоден.

Это ограничение research design, а не запрет remote inference вообще.

---

# 13. Identity и revision semantics

Cortex provenance должна позволять различить как минимум концептуальные уровни:

```text
semantic Cortex role
backend implementation identity
base model identity
base model revision / weights identity
processor/tokenizer/chat-template revision
active adaptation / adapter identity+revision
quantization / behavior-relevant conversion identity
provider/inference configuration identity
```

Не каждый backend способен предоставить все поля одинаково точно; неизвестность должна быть explicit.

## 13.1. Cortex behavior revision

Если меняется behavior-affecting состояние Cortex, например:

- base weights;
- active learned adapter;
- trainable Cortex parameters;
- behavior-relevant prompt/template policy;
- model selection;

это должно отражаться в Agent/Cortex revision provenance согласно будущему `DU-26/27`.

## 13.2. Physical engine update

Замена inference engine версии не всегда означает изменение semantic Cortex revision, но должна входить в reproducibility/runtime provenance, если способна влиять на результат.

Точная hashing/revision policy будет определена позже.

---

# 14. Frozen и adapted modes

Cortex architecture должна поддерживать conceptually:

```text
frozen base
frozen base + fixed adapter(s)
adaptable adapter(s)
future full/partial trainable backend
```

`DU-10` не выбирает training method.

Важно:

```text
frozen
≠
no runtime cache
```

Frozen semantics означает отсутствие behavior-affecting learned update в соответствующем evaluation/training phase.

Runtime cache допустим только если не создаёт скрытое session-level cognitive state, влияющее на независимые requests без explicit design.

Adapter activation/deactivation является behavior-affecting configuration и должно быть частью provenance.

---

# 15. Language / multilingual capability

Cortex descriptor должен явно объявлять language capabilities настолько, насколько backend их гарантирует/валидирует.

Нельзя считать:

```text
"multilingual model"
=
одинаково качественная поддержка всех языков
```

Для MINDRA различаются:

- заявленная model/provider language coverage;
- фактически проверенная MINDRA language capability;
- язык конкретного request/experiment.

Проектная политика:

> Если конкретная version/experiment использует естественный язык как значимый cognitive interface, baseline Cortex должна пройти отдельную проверку русского и английского языков.

Это не делает natural language обязательным для всех MicroWorld experiments и не делает русский частью общего Cortex API.

Точные multilingual benchmarks/thresholds принадлежат `DU-28` и version design.

---

# 16. Context budget и compaction

Backend должен уметь сообщить применимые ограничения context/output budget настолько, насколько они известны.

Если semantic context не помещается:

нельзя молча выбросить старые/неудобные fragments и продолжить как будто request не изменился.

Допустимые будущие стратегии:

- explicit failure `context_overflow`;
- заранее объявленная deterministic truncation policy;
- отдельный context-selection/compaction mechanism;
- summarization/retrieval mechanism, если он принят более поздним design.

Любая behavior-relevant compaction/truncation должна иметь provenance.

Gateway/backend adapter не становится скрытым Memory/Salience/Executive Control только потому, что имеет token limit.

---

# 17. Resource и latency evidence

Cortex descriptor/result должен позволять собирать non-cognitive resource evidence, если доступно:

- context/input size;
- output size;
- token counts;
- latency;
- memory/VRAM usage estimate;
- provider usage/cost;
- batch characteristics;
- timeout/resource-limit status.

Эти сведения:

```text
resource evidence
≠
logical cognitive time
```

Wall-clock latency не становится cognitive clock по `DU-03`.

Но resource evidence нужен для сравнения Cortex backends и architecture efficiency.

---

# 18. Failure / timeout / degradation semantics

Cortex failure не должен collapse в пустую строку.

Contract должен различать по смыслу минимум классы:

```text
capability unavailable
unsupported capability
invalid request/context
context overflow
backend/provider unavailable
timeout
resource exhausted
generation truncated
invalid structured output
revision/configuration mismatch
backend execution failure
```

Точные enum names не frozen.

## 18.1. Никакого hidden fallback

Запрещено:

```text
primary Cortex failed
→ silently call another model/provider
→ return result as if primary succeeded
```

Fallback допустим только как заранее объявленная composition/runtime policy с отдельной provenance/degradation status.

## 18.2. Consumer failure policy

Если Cortex optional для конкретного consumer, consumer contract может иметь explicit no-Cortex/degraded path.

Если Cortex capability required, отсутствие capability делает composition invalid либо module attempt failed согласно заранее принятой policy.

---

# 19. NoCortex, DummyCortex и Control Cortex

Эти состояния различаются.

## 19.1. NoCortex

```text
Cortex capability absent
```

Это архитектурно допустимая composition.

Consumer, для которого Cortex optional, обязан иметь contract-valid behavior без него.

Consumer с required Cortex dependency не может быть активирован в несовместимой composition.

## 19.2. DummyCortex

Deterministic/simple implementation Cortex contract для engineering tests.

Dummy не должен masquerade как pretrained capability в research results.

## 19.3. Control Cortex

Research control implementation, например:

- random/irrelevant response control;
- scripted semantic transformer;
- parameter/cost-matched alternative, если возможно;
- weaker/smaller backbone.

Control подключается через ту же semantic boundary.

---

# 20. Observability

Каждый Cortex invocation должен иметь traceable identity и causal parent `Module Attempt`/operation context.

Evidence по возможности включает:

- request identity;
- requesting semantic component;
- required capabilities;
- semantic context source references;
- backend/model/adaptation revision;
- status;
- generation/config identity;
- resource evidence;
- output artifact reference/summary;
- fallback/degradation provenance;
- intervention provenance.

## 20.1. Raw prompt/tokens

Rendered prompt/tokens могут быть полезным diagnostic artifact, но не обязательно должны входить в основной trace из-за размера/privacy/provider constraints.

Если experiment зависит от exact prompt rendering, такой artifact становится evidence-critical.

## 20.2. Hidden state probes

Hidden activations/attentions/logits предоставляются только backend'ами с соответствующей optional research capability.

Их отсутствие не делает backend несовместимым с basic Cortex contract.

---

# 21. Intervention

Interventions делятся минимум на классы:

```text
semantic Cortex request/context intervention
semantic Cortex result intervention
backend configuration/model selection intervention
adapter/adaptation-state intervention
raw/hidden representation intervention (opt-in)
```

Все active interventions следуют `DU-06`:

- explicit target;
- base causal context;
- treatment;
- provenance;
- branch semantics для confirmatory experiments, когда применимо.

Raw hidden-state intervention доступно только там, где backend предоставляет такую capability, и требует OOD/off-target validation.

---

# 22. Checkpoint / artifact implications

`DU-10` не определяет final checkpoint format, но устанавливает требования.

Checkpoint/experiment manifest позднее должен уметь сослаться на Cortex достаточно однозначно:

- base model/source;
- revision/weights identity;
- adapter/adaptation state;
- tokenizer/processor/template revision;
- behavior-relevant configuration;
- provider identity/limitations;
- capability descriptor revision.

Большие immutable base weights **не обязаны дублироваться в каждом Agent checkpoint**.

Checkpoint может ссылаться на externally recoverable immutable artifact и хранить только agent-owned adaptation/state, если `DU-27` признает это воспроизводимым.

---

# 23. Backend replacement

Главный критерий модульности:

> Замена Cortex backend не требует переписывать независимые cognitive modules, если новый backend удовлетворяет тем же required semantic capabilities.

Допустимые изменения при swap:

- другой backend adapter;
- другой provider;
- capability descriptor;
- resource profile;
- optional research capabilities;
- feature-space adapter/revision;
- version-specific configuration.

Недопустимо требовать изменения Goal/Memory/Policy semantics только из-за model-specific tokenizer/hidden size.

---

# 24. Transfer / comparison requirements

Будущий MINDRA-Eval должен позволять сравнивать минимум:

```text
NoCortex
Dummy/Control Cortex
small Cortex
main Cortex
larger Cortex
alternative model family
```

При сравнении нужно отделять:

- raw Cortex capability gain;
- MINDRA architecture gain поверх Cortex;
- resource/latency cost;
- multilingual differences;
- optional capability differences.

Если experiment требует hidden-state intervention, нельзя сравнивать backend без этой capability так, будто experiment эквивалентен; нужно менять protocol или маркировать capability mismatch.

---

# 25. Security/trust и remote data

`DU-10` не проектирует полную threat model, но remote provider является отдельной execution/trust boundary.

Нельзя предполагать, что:

- remote provider имеет immutable model;
- provider-side system policy неизменна;
- exact prompt/result можно всегда восстановить;
- private/experimental data допустимо отправлять наружу без отдельной policy.

Version design должен выбирать provider только после проверки исследовательских и data-handling constraints.

---

# 26. Research controls и критерии полезности Cortex

Наличие Cortex оправдано только измеримым вкладом в задачи, где эта capability нужна.

Минимальные будущие сравнения:

```text
same architecture + NoCortex
same architecture + Dummy/Control Cortex
same architecture + candidate Cortex A
same architecture + candidate Cortex B
```

Для language-related claims также нужны multilingual controls.

Для representation-related claims Cortex-derived Feature View сравнивается с:

- no view;
- non-Cortex learned view;
- shuffled/random/control view, где применимо.

---

# 27. Open questions для последующих DU

## DU-11 — Memory Core

- как Memory retrieval result представляется semantic context fragment Cortex;
- где проходит context-size/retrieval boundary;
- хранить ли Cortex outputs в Memory и с какой provenance.

## DU-22 — Executive Control

- кто решает, нужен ли Cortex invocation;
- сколько compute/token budget выделить;
- как выбирать optional Cortex operations.

## DU-23 — Policy / Planner

- как Cortex участвует в planning/action proposals;
- как не дать text generation bypass Action Boundary.

## DU-26 — Training

- какие Cortex parts frozen/trainable;
- PEFT/full adaptation;
- update scheduling;
- representation drift после adaptation.

## DU-27 — Checkpoint

- exact model/adapters manifest;
- remote/provider reproducibility grade;
- artifact recovery policy.

## DU-28 — Evaluation

- language benchmarks;
- backbone transfer;
- architecture gain;
- resource-normalized comparisons.

---

# 28. Что DU-10 намеренно не решает

После принятия этого документа всё ещё не выбраны:

- Qwen/Gemma/Llama/другая model family как обязательная;
- размер Cortex;
- конкретный tokenizer/chat template;
- local inference engine;
- quantization;
- PEFT method;
- cloud/provider;
- exact structured-output implementation;
- exact context compaction algorithm;
- exact Python classes.

Эти choices будут приниматься в version design или соответствующем downstream DU только после появления достаточных требований.
