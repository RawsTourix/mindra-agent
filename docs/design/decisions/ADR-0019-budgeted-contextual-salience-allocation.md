# ADR-0019 — Contextual Salience Profiles + explicit budgeted Attention Allocation

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-19 — Salience / Attention`

---

# 1. Контекст

После `DU-18` MINDRA имеет отдельные:

- Perception;
- Goals;
- Memory;
- World/Self Model;
- Intrinsic Signals;
- Drives;
- Appraisal;
- Affect;
- Valuation.

Но отсутствует отдельная responsibility, распределяющая ограниченное processing между множеством одновременно доступных candidates.

Нужно определить, является ли Salience самостоятельной boundary и в какой форме.

---

# 2. Проблема

Рассматривались варианты:

1. один global scalar `salience_score`;
2. каждый consumer самостоятельно вычисляет собственную priority;
3. merged `Appraisal + Salience`;
4. merged `Valuation + Salience`;
5. merged `Workspace/Executive router`;
6. отдельный `Salience System`: typed contextual profiles + explicit purpose/budget + versioned allocation policy.

---

# 3. Требования

Решение должно:

- отделять relevance от allocation priority;
- отделять desirability/value от processing priority;
- позволять novelty/urgency/risk/value конкурировать без universal hidden scalar;
- быть purpose-dependent;
- работать только с explicit candidate set;
- не получать ambient access всему Agent state/Memory;
- не владеть global compute budget;
- поддерживать ranking/gating/allocation;
- поддерживать stateful inhibition/persistence при необходимости;
- не становиться Workspace/Executive/Policy;
- не путать Cortex internal attention с canonical Salience;
- поддерживать controls/interventions/snapshot;
- иметь measurable downstream effect.

---

# 4. Вариант A — Один global salience scalar

```text
all evidence
→ salience ∈ R
```

## Плюсы

- простой API;
- легко сортировать;
- удобно для top-K.

## Минусы

- скрытая scalarization разнородных sources;
- теряется purpose;
- одинаковый score между Workspace/Memory/Planning не имеет гарантированного смысла;
- novelty/value/risk смешиваются;
- сложно диагностировать причину priority;
- scale drift становится глобальной проблемой.

**Решение:** отклонён как canonical representation. Derived score допустим внутри конкретной AllocationPolicy.

---

# 5. Вариант B — Priority внутри каждого consumer

Каждый consumer самостоятельно вычисляет:

```text
Memory priority
Workspace priority
Planner priority
...
```

## Плюсы

- локальная простота;
- purpose естественно встроен.

## Минусы

- одна и та же evidence integration дублируется;
- невозможно централизованно диагностировать/интервенировать salience semantics;
- consumers могут скрыто использовать несовместимые relevance/value mappings;
- трудно сделать matched controls;
- Salience перестаёт иметь отдельный causal contract.

**Решение:** отклонён как основной подход. Consumers сохраняют свои final admission/action semantics, но получают explicit salience evidence/allocation.

---

# 6. Вариант C — Объединить Appraisal и Salience

## Плюсы

- Appraisal уже вычисляет relevance/urgency;
- меньше модулей.

## Минусы

- relevance не определяет ограниченный resource allocation;
- high relevance не всегда требует дополнительного processing;
- novelty/rarity и purpose-specific budget не относятся к Appraisal responsibility;
- Workspace/Memory/Executive integration начинает протекать в Appraisal.

**Решение:** отклонён.

---

# 7. Вариант D — Объединить Valuation и Salience

## Плюсы

- value часто влияет на priority;
- удобно ранжировать candidates.

## Минусы

- high value ≠ high processing need;
- adverse/risky/low-value events могут требовать высокого attention;
- uncertainty/novelty могут быть salient до формирования utility;
- Valuation начинает владеть compute allocation.

**Решение:** отклонён.

---

# 8. Вариант E — Сразу Workspace/Executive router

## Плюсы

- decision и execution в одном месте;
- проще end-to-end learned router.

## Минусы

- невозможно отделить priority evidence от actual resource decision;
- Salience нельзя проверить отдельно;
- Workspace и Executive ещё не спроектированы;
- router начинает скрыто менять scheduler/compute policy.

**Решение:** отклонён.

---

# 9. Вариант F — Typed contextual profiles + budgeted allocation

Conceptually:

```text
explicit candidates
+
typed evidence
+
purpose
→ SalienceProfile[]

profiles
+
AttentionBudget
+
AllocationPolicy
→ AttentionAllocation
```

## Плюсы

- source semantics сохраняются;
- purpose explicit;
- scalar необязателен;
- budget принадлежит consumer/context;
- разные allocation families можно сравнивать;
- Salience остаётся независима от Workspace/Executive/Policy;
- удобно интервенировать profile и allocation отдельно;
- можно поддержать inhibition/focus persistence;
- compatible с rule-based и learned routers.

## Минусы

- API сложнее одного score;
- downstream consumer должен явно применять allocation;
- нужно versioning normalization/policies;
- первая реализация должна ограничить target/purpose subset.

**Решение:** принято.

---

# 10. Принятое решение

MINDRA использует отдельный `Salience System`.

Канонически:

```text
Salience Target
+
Purpose
+
Typed Evidence
→ SalienceProfile

SalienceProfile[]
+
explicit AttentionBudget
+
versioned AllocationPolicy
→ AttentionAllocation
```

При этом:

```text
Relevance ≠ Salience
Value ≠ Salience
SalienceProfile ≠ AttentionAllocation
AttentionAllocation ≠ Workspace admission
AttentionAllocation ≠ Executive compute action
AttentionAllocation ≠ Policy action
```

---

# 11. Budget ownership

Salience не владеет global compute budget.

Budget приходит от explicit consumer/context.

До `DU-22` допускаются абстрактные units вроде:

```text
max_items
normalized mass
context slots
consumer-defined units
```

Physical Cortex calls/FLOPs/Cognitive Cycles не становятся Salience responsibility.

---

# 12. Purpose-specificity

Один target может иметь разные salience profiles для:

```text
workspace admission hint
memory regulation hint
retrieval post-processing
planning inspection
executive attention hint
```

Поэтому global timeless `target.salience` запрещён как universal field.

---

# 13. Stateful Salience

Persistent state не обязателен.

Допускаются explicit mechanisms:

- inhibition of return;
- focus persistence;
- habituation;
- hysteresis;
- refractory state.

Если state causally relevant, он входит в snapshot и staged commit semantics.

---

# 14. Cortex attention

Internal attention weights/heads/masks Cortex не являются canonical Salience автоматически.

Они могут использоваться только как optional backend-specific evidence/probe после explicit validation.

---

# 15. Causal gate

Salience считается функциональной только если:

```text
profile/allocation change
→ actual downstream allocation/processing change
→ measurable effect
```

Логируемый score без processing effect не считается достаточным основанием отдельной boundary.

Обязательны controls вроде:

```text
Uniform
Random
Shuffled
NoveltyOnly
ValueOnly
FixedTopK
MatchedLearnedControl
NoSalience
```

---

# 16. Последствия

Положительные:

- `DU-20` получает чистый salience hint для Memory Regulation;
- `DU-21` получает clean Workspace admission input;
- `DU-22` сможет использовать priority без смешения с fixed scheduler;
- можно отдельно исследовать bottom-up/top-down competition;
- можно измерять полезность adaptive allocation.

Отрицательные:

- требуется отдельный candidate-set/purpose contract;
- появляется policy/revision/normalization state;
- implementation должна избегать скрытой duplicate priority внутри consumers.

---

# 17. Что решение не определяет

Не выбраны:

- concrete target taxonomy;
- exact evidence set;
- scalar formula;
- neural router;
- top-K/threshold/softmax default;
- inhibition equation;
- budget units final form;
- Workspace/Executive integration implementation;
- training losses.

---

# 18. Связанные документы

- [`../modules/salience.md`](../modules/salience.md);
- [`../contracts/salience.md`](../contracts/salience.md);
- `DU-20 — Memory Regulation / Consolidation`;
- `DU-21 — Workspace`;
- `DU-22 — Executive Control`.
