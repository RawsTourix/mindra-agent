# ADR-0020 — Source-preserving budget-aware Memory Regulation с gated consolidation

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-20 — Memory Regulation / Consolidation`

---

# 1. Контекст

После `DU-11` MINDRA имеет нейтральный `Memory Core`, где canonical `MemoryRecord` отделён от retrieval representations/indexes. После `DU-19` существует purpose-dependent Salience/Attention boundary.

Нужно добавить ограниченную memory management semantics:

- admission;
- retention;
- forgetting/eviction;
- replay/reactivation;
- consolidation;
- episodic → derived/semantic memory.

При этом нельзя:

- разрушить source fidelity;
- сделать Salience единственной «важностью»;
- смешать Agent Memory Replay и Training Replay;
- превратить consolidation в hidden optimizer update;
- rewrite historical memories inplace.

---

# 2. Рассмотренные варианты

1. оставить Memory Core нейтральным навсегда и управлять capacity только FIFO/LRU;
2. один universal `memory_importance` scalar;
3. Salience напрямую владеет retention/eviction;
4. LLM eager-consolidation после каждого события с заменой raw memories summary;
5. Memory Regulation как отдельный второй store owner;
6. source-preserving, budget-aware regulation responsibility поверх Memory Core с purpose-specific policies и gated consolidation.

---

# 3. Требования

Решение должно:

- сохранять единого owner canonical Memory Store;
- различать validation и policy admission;
- иметь explicit capacity/budget semantics;
- разделять admission/retention/eviction/replay/consolidation purposes;
- поддерживать Salience как evidence, а не final authority;
- сохранять raw/source provenance;
- не переписывать historical records inplace;
- различать forgetting и physical deletion;
- различать retrieval, Agent Memory replay и Training Replay;
- допускать episodic-only/no-consolidation control;
- поддерживать contradiction preservation;
- не выполнять Learning Update;
- поддерживать intervention/snapshot/reproducibility;
- позволять rule-based и learned implementations позднее.

---

# 4. Вариант A — Только FIFO/LRU

## Плюсы

- минимальная сложность;
- легко реализовать;
- хорошая baseline semantics.

## Минусы

- не использует значимость/coverage/diversity;
- не поддерживает semantic consolidation;
- не решает conflict/redundancy;
- не позволяет исследовать memory regulation как cognitive function.

**Решение:** отклонён как full architecture; FIFO/recency остаются обязательными controls.

---

# 5. Вариант B — Universal memory importance scalar

```text
all evidence
→ importance ∈ R
→ retain/evict/replay/consolidate
```

## Плюсы

- простой ranking;
- один API;
- удобно для top-K.

## Минусы

- admission, replay и consolidation имеют разные цели;
- source diversity/contradiction/cost теряются;
- scalarization Appraisal/Value/Salience становится скрытой;
- одинаковый score между policy purposes не имеет гарантированной semantics;
- создаёт feedback loops через retrieval frequency.

**Решение:** отклонён как canonical representation. Derived score возможен внутри конкретной RegulationPolicy.

---

# 6. Вариант C — Salience напрямую управляет Memory

```text
SalienceProfile
→ save/delete/replay
```

## Плюсы

- мало компонентов;
- использует уже существующую priority boundary.

## Минусы

- Salience не знает memory-specific redundancy, coverage, storage cost, lineage;
- нарушается boundary `AttentionAllocation ≠ consumer decision`;
- retention и processing priority смешиваются;
- Salience становится owner Memory lifecycle.

**Решение:** отклонён. Salience — один из explicit evidence sources.

---

# 7. Вариант D — Eager LLM consolidation с заменой raw records

```text
incoming episode
→ LLM summary/reflection
→ replace/merge old memory
```

## Плюсы

- быстро уменьшает объём;
- удобный LLM-readable representation;
- часто используется в agent-memory prototypes.

## Минусы

- loss of source details;
- hallucination/semantic drift;
- consolidation schedule влияет на output;
- provenance laundering;
- невозможность пересчитать derivation после потери raw evidence;
- плохо подходит для causal research.

**Решение:** отклонён как canonical behavior.

LLM может быть optional derivation backend, но raw/source lineage сохраняется и consolidation gated.

---

# 8. Вариант E — Memory Regulation как второй owner Store

## Плюсы

- policy может напрямую делать операции;
- меньше proposal/commit plumbing.

## Минусы

- два owners одного canonical state;
- conflict с `DU-04/05`;
- трудно восстановить transaction provenance;
- Core validation можно обойти policy implementation.

**Решение:** отклонён.

---

# 9. Вариант F — Source-preserving budget-aware regulation

Conceptually:

```text
Memory Core
→ canonical store ownership

Memory Regulation
→ profiles / policies / decisions
→ lifecycle/consolidation proposals

Memory Core
→ validation / atomic commit
```

Consolidation:

```text
raw episodic sources
→ gated derivation
→ new derived MemoryRecord
→ explicit derived_from/support/conflict lineage
```

## Плюсы

- сохраняет source evidence;
- budget/capacity explicit;
- purpose-specific policies;
- Salience/Value/Appraisal evidence можно подключать без ownership leakage;
- episodic-only control естественен;
- consolidation можно пересчитывать/сравнивать;
- compatible с future learning без hidden optimizer;
- хорошо диагностируется/intervened.

## Минусы

- больше metadata;
- storage raw + derived memory может быть дороже;
- требуется lifecycle/lineage discipline;
- первая реализация должна ограничить policy space.

**Решение:** принято.

---

# 10. Принятое решение

MINDRA использует **Memory Regulation responsibility поверх единого Memory Core**.

Канонически:

```text
Memory Core validation
≠
Regulation admission

SalienceProfile
≠
Retention decision

Forgetting
≠
Physical deletion

Retrieval
≠
Memory Replay
≠
Training Replay

Consolidation
≠
In-place rewrite
≠
Learning Update
```

Consolidation создаёт новый derived `MemoryRecord` со stable source lineage.

---

# 11. Последствия

## Положительные

- можно честно сравнивать raw retention и consolidation;
- false consolidation не уничтожает историческое evidence автоматически;
- regulation policies можно менять независимо от Store backend;
- подходит для memory budgets;
- позволяет изучать влияние Appraisal/Affect/Salience на memory без магического emotional-memory score;
- prepared boundary для continual learning `DU-26`.

## Отрицательные

- больше storage/provenance metadata;
- raw retention может быть дорогой;
- нужна стратегия eventual physical deletion при жёстких ресурсных ограничениях;
- derived knowledge не становится автоматически компактной «истиной».

---

# 12. Что решение не определяет

ADR не выбирает:

- конкретный forgetting curve;
- exact lifecycle enum;
- MemoryBudget первой версии;
- retention/replay score;
- clustering;
- LLM prompt/model;
- generative replay;
- semantic memory schema;
- learned policy;
- optimizer/continual-learning method;
- checkpoint storage format.

---

# 13. Evaluation obligations

Нужно сравнивать минимум:

```text
Full Regulation
NoRegulation / capacity baseline
FIFO/recency
Random/Shuffled
NoConsolidation / episodic-only
Matched compression/consolidation controls
```

Для consolidation отдельно измерять:

- downstream utility;
- source fidelity;
- contradiction preservation;
- false/incorrect derived memory rate;
- budget efficiency;
- generalization;
- behavior under distribution shift.

Улучшение compression ratio само по себе не считается доказательством полезной consolidation.
