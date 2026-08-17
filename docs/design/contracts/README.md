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
- Cortex backend contract;
- Environment API;
- checkpoint format;
- experiment record format;
- module state serialization;
- configuration schema.

Это предварительный список типов контрактов, а не утверждённый catalog.

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

---

# Иерархия

```text
canonical semantic design
→ accepted ADR
→ exact internal contract
→ implementation
```

Exact contract уточняет форму принятой семантики, но не может сам молча изменить её смысл.

---

# Текущий статус

После `DU-04` … `DU-06` уже приняты semantic requirements для:

- versioned committed `CognitiveState`;
- state ownership/provenance/scopes;
- module descriptors и declared dependencies;
- DAG/wave scheduling;
- staged public/private effects;
- lifecycle/failure semantics;
- causal execution tracing;
- passive Evidence Plane;
- declared private-state research probes;
- explicit Intervention Gateway;
- intervention lineage/provenance;
- exact-vs-approximate counterfactual distinction.

Однако **exact Python contracts пока намеренно не зафиксированы**.

Причина: будущие module-specific Design Updates (`DU-07` … `DU-24`) должны сначала проверить semantic protocol реальными требованиями Environment, Cortex, Memory, World Model, Policy и других подсистем. В частности, только они покажут:

- какие public/private probes реально нужны;
- какие intervention targets являются осмысленными;
- какие данные слишком велики для общего trace contract;
- какие backend-specific research adapters потребуются.

До contract freeze запрещено считать обсуждавшиеся `Protocol`, ABC, TensorDict `in_keys/out_keys`, dataclass schemas, OpenTelemetry span model, PyTorch hooks, pyvene API или конкретный scheduler/intervention result type каноническими.

Exact contracts создаются тогда, когда соответствующая семантика достаточно устойчива и есть основания зафиксировать machine-facing форму.
