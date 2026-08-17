# Exact internal contracts MINDRA

## Назначение

Этот каталог предназначен для точных machine-facing контрактов между подсистемами MINDRA.

Контракт создаётся **после** semantic design соответствующей области и не должен преждевременно определять архитектуру только потому, что конкретный Python API удобен для реализации.

---

# Что относится к exact internal contracts

В будущем здесь могут появиться спецификации уровня:

- `CognitiveState` schema;
- `ModuleProtocol`;
- `ModuleDescriptor`;
- observability event/trace schema;
- module research probe contract;
- intervention request/result contract;
- Cortex Gateway/backend contract;
- Environment API;
- Perception/Canonical Percept contract;
- Goal System/Goal Graph contract;
- checkpoint format;
- experiment record format;
- module state serialization;
- configuration schema.

Это предварительный список типов контрактов, а не утверждённый catalog.

---

# Текущие candidate contracts

- [`environment.md`](environment.md) — candidate semantic machine-facing contract после `DU-07`: agent-facing/research-facing Environment operations, snapshot/clone/fork/intervention и transition-evidence requirements;
- [`perception.md`](perception.md) — candidate semantic contract после `DU-08`: Perception input, `Canonical Percept`, Semantic Core, Feature Views, representation identity/versioning и research capabilities;
- [`goals.md`](goals.md) — candidate semantic contract после `DU-09`: Goal Proposal, Committed Goal, Goal Graph, lifecycle/scope, transition authority, progress/priority/commitment и research capabilities;
- [`cortex.md`](cortex.md) — candidate semantic contract после `DU-10`: Cortex descriptor, capability negotiation, semantic request/context/result, backend adapter/provider provenance, optional research/adaptation capabilities и failure/resource semantics.

Эти документы **не** являются frozen Python API и могут уточняться последующими DU до общего contract freeze.

---

# Правила

Exact contract должен фиксировать, где применимо:

- поля и типы;
- required/optional semantics;
- shape/dtype/device semantics для tensor data;
- ownership;
- declared reads/writes;
- freshness/availability requirements;
- lifecycle;
- private-state/snapshot obligations;
- observability/probe capabilities;
- intervention target/phase/provenance semantics;
- error/degradation behavior;
- versioning;
- serialization;
- backward/forward compatibility expectations;
- invariants, которые можно проверить автоматическими tests.

Contract не должен протаскивать private implementation detail одного backend во всю систему без design justification.

Research observability contract не должен автоматически давать runtime consumers доступ к private state.

Intervention contract не должен быть скрытым extension обычного logging callback.

Environment research capability не должна автоматически становиться agent-facing capability.

Perception contract не должен превращать конкретный encoder/Cortex hidden state в универсальный canonical representation.

Goal contract не должен давать Cortex/Planner/Drives прямую mutation authority committed Goal Graph или смешивать structural priority с future dynamic valuation.

Cortex contract не должен:

- фиксировать конкретную model family/provider как architecture requirement;
- давать Gateway ambient access ко всему Agent state;
- требовать hidden states/gradients/CoT от любого backend;
- протаскивать model-specific chat template/tokenizer в cognitive consumers;
- превращать Cortex result в direct Goal/Memory/Action write;
- скрывать fallback/context truncation/provider substitution.

---

# Иерархия

```text
canonical semantic design
→ accepted ADR
→ candidate/exact internal contract
→ implementation
```

Exact contract уточняет форму принятой семантики, но не может сам молча изменить её смысл.

---

# Текущий статус

После `DU-04` … `DU-10` уже приняты semantic requirements для:

- versioned committed `CognitiveState`;
- state ownership/provenance/scopes;
- module descriptors и declared dependencies;
- DAG/wave scheduling;
- staged public/private effects;
- lifecycle/failure semantics;
- causal execution tracing;
- passive Evidence Plane и explicit Intervention Gateway;
- Environment/Perception/Goal boundaries;
- Goal Graph/lifecycle/scope/dependency/conflict semantics;
- Cortex как agent-owned shared pretrained capability;
- backend-neutral Cortex Gateway;
- semantic Request/Context/Result boundary;
- backend-specific prompt/chat-template/tokenizer/provider isolation;
- local/remote provider compatibility с explicit capability/provenance;
- optional hidden-state/embedding/gradient/multimodal/adapter capabilities;
- `NoCortex`/Dummy/Control distinctions;
- model/adapter/template behavior-revision provenance;
- explicit context overflow/truncation/failure/degradation semantics;
- Goal Proposal и Feature View boundaries для Cortex-derived outputs.

Однако **общий exact Python contract set пока намеренно не зафиксирован**.

`environment.md` остаётся candidate, поскольку `DU-24`, `DU-25`, `DU-27` и `DU-28` ещё могут уточнить exact action/data/snapshot forms.

`perception.md` остаётся candidate, поскольку `DU-11` … `DU-13`, `DU-25` … `DU-28` могут уточнить exact Memory/World Model representation потребности, persistence и evaluation contracts.

`goals.md` остаётся candidate, поскольку `DU-12` … `DU-18`, `DU-22`, `DU-23`, `DU-25` … `DU-28` ещё уточнят feasibility, autonomous proposal, valuation, focus/planning, data и evaluation semantics.

`cortex.md` остаётся candidate, поскольку `DU-11`, `DU-21` … `DU-23`, `DU-26` … `DU-28` ещё уточнят Memory/Workspace context, invocation control, Policy usage, adaptation, checkpoint и evaluation requirements.

Будущие module-specific Design Updates должны продолжать проверять semantic protocol реальными требованиями.

До contract freeze запрещено считать обсуждавшиеся `Protocol`, ABC, TensorDict `in_keys/out_keys`, dataclass schemas, OpenTelemetry span model, PyTorch hooks, pyvene API, Gymnasium `Env`, Transformers/vLLM/SGLang, конкретный Cortex backend, PEFT method или scheduler/intervention result type каноническими.

Exact contracts создаются тогда, когда соответствующая семантика достаточно устойчива и есть основания зафиксировать machine-facing форму.
