# Candidate contract Cortex MINDRA

## Статус

**Статус:** candidate semantic contract  
**Основание:** `DU-10 — Cortex Boundary`

Этот документ уточняет machine-facing классы данных и capabilities, необходимые будущей реализации Cortex boundary.

Он **не является frozen Python API** и не фиксирует:

- `Protocol`/ABC;
- exact class/method names;
- dataclass/TensorDict/Pydantic;
- concrete tokenizer/processor;
- exact operation enum;
- exact structured-output format;
- Transformers/vLLM/SGLang/llama.cpp/provider SDK;
- quantization/adaptation method;
- конкретную LLM.

Приоритет семантики имеет [`../modules/cortex.md`](../modules/cortex.md).

---

# 1. Основные capability surfaces

Future Cortex boundary должна уметь выразить минимум:

```text
describe capabilities
validate semantic request
execute request through selected backend
return normalized result/status/provenance
expose optional research capabilities
report resource/context constraints
```

Concrete backend/provider selection происходит через composition/configuration boundary, а не runtime Service Locator.

---

# 2. Cortex descriptor

Conceptually descriptor должен позволять выразить:

```text
semantic_role
implementation_identity
backend_family
base_model_identity
base_model_revision?
processor/tokenizer/template_identity?
active_adaptation_identity/revision?
provider_identity?
required/core capabilities
optional capabilities
language capabilities
input modality capabilities
context/output limits
batch/streaming support
adaptation capabilities
research probe/intervention capabilities
reproducibility/opacity metadata
```

Не все поля могут быть известны remote backend; unknown/opaque status должен быть explicit.

---

# 3. Cortex Request

Conceptually:

```text
CortexRequest
├── request_id
├── operation_kind
├── required_capabilities[]
├── semantic_context_fragments[]
├── requested_output_contract
├── language/locale?
├── generation/compute budget?
├── stochastic policy / seed metadata?
├── base state / agent / module-attempt causal identities
└── intervention provenance?
```

Request не содержит обязательный model-specific prompt/token sequence.

---

# 4. Semantic context fragment

Conceptually fragment должен позволять выразить:

```text
fragment_id
fragment_kind
semantic payload or reference
source semantic owner
source object/state identity
source revision/provenance
availability/freshness
language/modality metadata?
importance/requiredness metadata?
```

Точная representation не frozen.

Consumer может передавать только те fragments, источники которых входят в его declared dependencies.

Gateway не должен самостоятельно получать произвольные дополнительные fragments из Agent state.

---

# 5. Requested output contract

Request должен позволять указать требуемый класс результата, например conceptually:

```text
free semantic/text result
structured semantic result
classification-like result
representation/embedding result
```

Если requested capability отсутствует у backend, результат должен быть `unsupported capability`, а не best-effort скрытой подменой без provenance.

---

# 6. Cortex Result

Conceptually:

```text
CortexResult
├── request_id
├── status
├── semantic_text?
├── structured_payload?
├── feature_payloads[]?
├── backend/model/adaptation provenance
├── inference/generation config identity
├── resource/usage evidence?
├── truncation/degradation metadata?
├── raw artifact reference?
└── intervention provenance?
```

Result сам по себе не имеет write authority в чужих `CognitiveState` namespaces.

---

# 7. Candidate status semantics

Contract должен сохранять различия минимум между классами:

```text
success
capability_unavailable
unsupported_capability
invalid_request
context_overflow
provider_unavailable
timeout
resource_exhausted
generation_truncated
invalid_structured_output
revision_mismatch
backend_error
```

Exact enum names не frozen.

Пустой payload не должен использоваться как универсальный failure sentinel.

---

# 8. Capability categories

Candidate core capability:

```text
semantic/language inference
```

Optional capability classes:

```text
structured_generation
embedding_or_representation
hidden_state_export
attention_export
logits_or_token_scores
multimodal_input
latent_or_soft_input
gradient_access
trainable_backend
adapter_management
raw_representation_intervention
batch_inference
streaming
```

Наличие capability проверяется до experiment/active composition там, где оно является required.

---

# 9. Context rendering adapter

Concrete backend adapter conceptually отвечает за:

```text
semantic context
→ backend-specific messages/prompt
→ chat template
→ tokenizer/processor
→ provider request/model tensors
```

и обратное преобразование backend output в `CortexResult`.

Adapter-specific rendering identity/revision должна быть доступна provenance настолько, насколько она влияет на behavior.

---

# 10. NoCortex / Dummy / Control

## NoCortex

Capability отсутствует.

Это не implementation, возвращающая пустую строку.

## DummyCortex

Deterministic test implementation semantic contract.

## ControlCortex

Research control implementation с explicit identity/provenance.

Все compatible implementations подключаются через одну composition boundary.

---

# 11. Feature/embedding outputs

Representation payload Cortex не становится автоматически `Perception Feature View`.

Чтобы использовать его как Feature View, adapter/consumer должен обеспечить semantic requirements `DU-08`:

```text
feature_space_id
feature_space_revision
encoder/backend identity
source references
compatibility semantics
```

Raw hidden tensor без этих данных остаётся backend/research artifact.

---

# 12. Goal-related outputs

Cortex может вернуть grounded objective/subgoal candidate, но canonical route остаётся:

```text
Cortex Result
→ authorized grounding/planning consumer
→ Goal Proposal
→ Goal System
```

Cortex contract не содержит direct mutation операции Goal Graph.

---

# 13. Adaptation state

Descriptor/result/checkpoint provenance должно быть способно различать:

```text
base model revision
active adapter/adaptation revision
frozen vs adaptable mode
behavior-relevant prompt/template policy
```

Exact training/update API определяется `DU-26`.

---

# 14. Language capability

Descriptor должен позволять объявить:

```text
claimed_supported_languages?
validated_languages?
language-specific limitations?
```

Model-card claim и MINDRA-validated capability являются разными metadata.

Если version/experiment использует естественный язык как значимый cognitive interface, required language capability определяется version/evaluation design.

---

# 15. Resource/context descriptor

По возможности должна быть выразима информация класса:

```text
max context / effective context limit
max output limit
batch constraints
latency evidence
input/output token counts
VRAM/memory estimate
provider usage/cost
```

Resource metadata не является cognitive payload автоматически.

---

# 16. Research probes

Optional research probes могут предоставлять:

```text
rendered prompt/messages
raw response
hidden states
attentions
logits
KV/cache diagnostics
adapter/backend state summaries
```

Каждая capability объявляется отдельно.

Доступность probes не даёт cognitive consumers права читать эти данные.

---

# 17. Intervention targets

Candidate intervention classes:

```text
semantic request/context
semantic result
backend selection/configuration
adapter/adaptation state
raw hidden representation
```

Raw representation intervention допустима только для backend с explicit capability и следует `DU-06`.

---

# 18. Snapshot/checkpoint obligations

Cortex boundary должна позволить будущему checkpoint layer восстановить или однозначно сослаться на behavior-relevant state настолько, насколько это возможно:

```text
base model identity/revision
adapter state/revision
processor/template identity
provider/config identity
private persistent state, если такой state вообще разрешён design
```

Exact serialization и artifact pinning определяются `DU-27`.

---

# 19. Invariants для будущих tests

Будущая implementation должна позволять автоматически проверить минимум:

- consumer не зависит от concrete model SDK;
- `NoCortex` не masquerade как успешный empty result;
- unsupported capability обнаруживается явно;
- model-specific chat/template rendering изолирован в adapter;
- Cortex result не пишет Goal/Policy/Memory state напрямую;
- hidden-state capability optional;
- backend swap сохраняет semantic request/result surface;
- failure не вызывает hidden fallback;
- context overflow/truncation observable;
- representation payload имеет compatibility metadata до использования как Feature View;
- behavior-affecting adapter/model switch меняет provenance/revision identity.
