# ADR-0031 — Semantic contract consistency freeze перед Version Roadmap

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-31 — Contract + ADR Consistency Freeze`

---

# 1. Контекст

После `DU-01 … DU-30` MINDRA имеет:

- foundation/system semantics;
- cognitive/runtime boundaries;
- Experience/Data, Training, Checkpoint, Evaluation, Verification и Claims planes;
- 30 accepted ADR;
- 24 candidate machine-facing semantic contracts для `DU-07 … DU-30`.

Каждый отдельный DU был принят последовательно, но перед version roadmap требуется проверить весь набор как одну архитектуру.

Без общего freeze Codex мог бы столкнуться с несколькими классами неоднозначности:

- ранняя generic формулировка и более поздний специализированный contract используют один термин шире/уже;
- candidate contract подробен, но неясно, какие его части semantic-frozen, а какие implementation-level;
- version roadmap начинает выбирать package/API решения и незаметно меняет ownership/lifecycle;
- conditional research module ошибочно воспринимается как empirically proven mandatory mechanism;
- старый happy-path текст используется вместо более поздней failure semantics.

Нужно зафиксировать единый semantic baseline перед `DU-32`.

---

# 2. Вариант A — Немедленно перейти к roadmap без freeze

## Плюсы

- меньше документационной работы;
- быстрее начать декомпозицию версий.

## Минусы

- implementation planning становится местом скрытых архитектурных решений;
- ранние generic формулировки могут интерпретироваться буквально вопреки поздним ADR;
- exact Python shape может быть ошибочно принят за semantic contract;
- трудно понять, является ли open question blocker или нормальным version choice.

**Решение:** отклонён.

---

# 3. Вариант B — Заморозить все candidate contracts как exact API

То есть объявить текущие field names/status enums/структуры практически готовым Python API.

## Плюсы

- максимальная определённость для Codex;
- минимальное пространство implementation choice.

## Минусы

- многие contracts намеренно semantic, а не language/framework-specific;
- version roadmap ещё не выбрал dataclass/Pydantic/TensorDict/Protocol и physical schema;
- premature API freeze создаст лишний rewrite;
- backend/runtime constraints ещё неизвестны.

**Решение:** отклонён.

---

# 4. Вариант C — Не фиксировать contracts до первой реализации

Считать contracts лишь заметками и позволить first version выбрать структуру по месту.

## Плюсы

- максимальная гибкость реализации.

## Минусы

- Codex вынужден будет решать ownership/lifecycle/visibility semantics;
- семантическая модульность перестанет быть гарантированной;
- testing/verification obligations не к чему привязать;
- research attribution может зависеть от случайного implementation design.

**Решение:** отклонён.

---

# 5. Вариант D — Semantic freeze + deferred exact API

Принять общий baseline:

```text
accepted ADR/design semantics
+
consistency resolutions
+
semantic contract entities/invariants
        ↓
Semantic Freeze Baseline F31
        ↓
DU-32 Version Roadmap
        ↓
version-specific exact contracts/API
```

## Плюсы

- ownership/lifecycle/source-of-truth больше не являются implementation guess;
- exact Python/framework choices остаются свободными;
- поздние specialized ADR однозначно уточняют generic ранние формулировки;
- first version можно сделать минимальной без смыслового rewrite;
- breaking semantic changes становятся reviewable;
- VerificationObligation можно выводить из frozen invariants.

## Минусы

- нужен отдельный governance слой;
- version specification обязана различать semantic и representational choices;
- при будущем breaking change потребуется ADR/update freeze baseline.

**Решение:** принят.

---

# 6. Принятое понятие freeze

`F31` означает:

> Семантика boundaries/ownership/lifecycle/causal ordering/source/provenance/visibility и machine-facing meaning contracts `DU-01 … DU-30` достаточно согласована, чтобы проектировать concrete software versions без самостоятельного архитектурного выбора со стороны implementation agent.

`F31` **не означает**:

- frozen Python API;
- frozen file/package layout;
- frozen tensor shapes;
- frozen algorithms/models/frameworks;
- доказанную функциональную полезность всех conditional modules.

---

# 7. Consistency resolutions

Freeze принимает explicit resolutions, подробно описанные в canonical `contract-adr-consistency-freeze.md`:

```text
CR-01 Action lifecycle
CR-02 Memory admission ownership
CR-03 Replay taxonomy
CR-04 Consolidation vs Learning Update
CR-05 candidate/validated/activated revision lifecycle
```

Эти resolutions не вводят новую architecture. Они закрепляют поздние accepted semantics:

- `ADR-0020` для Memory Regulation/Consolidation;
- `ADR-0024` для Action Commit/dispatch;
- `ADR-0025/26` для replay/training/revision lifecycle.

---

# 8. Contract status после ADR

Contracts `DU-07 … DU-30` получают статус:

```text
semantic-frozen for roadmap baseline F31
exact implementation/API: not frozen
```

То есть version design может выбрать concrete representation, но не может без нового ADR:

- сменить semantic owner;
- объединить различённые responsibilities;
- изменить causal ordering;
- изменить source-of-truth/visibility;
- превратить derived entity в source entity;
- удалить required provenance/lineage semantics;
- изменить module gate/claim boundary.

---

# 9. Deferred implementation choices

Без нового ADR разрешено выбирать в version specification, если semantic invariants сохраняются:

- Python object model;
- exact enum/string names;
- library/framework;
- Cortex/model/backend;
- algorithm family;
- storage/index/checkpoint format;
- optimizer/training method;
- concrete Environment/tasks;
- budgets/horizons/default values;
- testing/evaluation tooling;
- deployment/hardware topology.

---

# 10. Breaking change governance

После F31 semantic breaking change идёт только через:

```text
issue/evidence/blocker
→ design review
→ new ADR
→ supersede/supersede-in-part status при необходимости
→ canonical owner update
→ contract update
→ freeze baseline revision
→ VerificationObligation update
→ version plan/code
```

Implementation commit не может сам стать архитектурным решением.

---

# 11. Conditional modules после freeze

Affect, Workspace, adaptive Executive Control и Planner сохраняются в accepted design в соответствии со своими ADR, но остаются falsifiable.

Freeze означает:

- их semantic boundary определена;
- их empirical necessity/usefulness не объявлена доказанной;
- version roadmap может использовать `No*`/control configurations;
- отрицательный module gate способен инициировать новый design review/ADR.

---

# 12. Verification implication

После F31 существенный frozen invariant должен иметь implementation-facing `VerificationObligation` в конкретной software version там, где он machine-checkable.

Особо важны:

- dependency/Service Locator restrictions;
- ownership/write authority;
- stale/atomic commit;
- privileged leakage;
- Action Commit/dispatch/retry;
- Memory Replay vs Training Replay;
- Consolidation vs Learning Update;
- candidate vs active revision;
- checkpoint integrity/restore;
- Evaluation/Verification/Claims separation.

---

# 13. Что audit установил

На момент принятия ADR:

```text
accepted ADR: 30
candidate semantic boundary contracts: 24
proposed ADR: 0
superseded ADR: 0
blocking semantic TODO: 0
```

Найденные cross-DU wording ambiguities разрешаются CR-01 … CR-05 без создания новой subsystem architecture.

---

# 14. Последствия

После ADR:

- `DU-01 … DU-30` образуют baseline `F31`;
- project status становится `ready for version planning`;
- `DU-32 — Version Roadmap` разрешён;
- Codex не должен самостоятельно решать semantic architecture первого milestone;
- exact implementation/API contracts будут конкретизироваться version specification;
- любые future semantic breaks требуют нового ADR;
- old historical wording читается только в согласовании с freeze resolutions и canonical late owners.

---

# 15. Что ADR не фиксирует

- software version numbering;
- milestone decomposition;
- first-version scope;
- package layout;
- Python API;
- chosen neural/RL algorithms;
- concrete Cortex;
- exact test/eval stack;
- storage formats;
- hardware/deployment.

Это задача `DU-32` и последующих version specifications.

---

# 16. Принятое решение

```text
DU-01 … DU-30
        ↓
consistency audit + resolutions
        ↓
Semantic Freeze Baseline F31
        ↓
ready for version planning
        ↓
DU-32 — Version Roadmap
```
