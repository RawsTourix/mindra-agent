# Exact internal contracts MINDRA

## Назначение

Этот каталог предназначен для точных machine-facing контрактов между подсистемами MINDRA.

Контракт создаётся **после** semantic design соответствующей области и не должен преждевременно определять архитектуру только потому, что конкретный Python API удобен для реализации.

---

# Что относится к exact internal contracts

В будущем здесь могут появиться спецификации уровня:

- `CognitiveState` schema;
- module protocol;
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
- lifecycle;
- versioning;
- serialization;
- error/degradation behavior;
- backward/forward compatibility expectations;
- invariants, которые можно проверить автоматическими tests.

Contract не должен протаскивать private implementation detail одного backend во всю систему без design justification.

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

# Состояние

На стадии documentation foundation exact internal contracts отсутствуют.

Они будут создаваться после проектирования соответствующих semantic boundaries.
