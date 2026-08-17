# ADR-0015 — Typed stateful Drive System без global motivation scalar

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-15 — Drives`

---

# 1. Контекст

После `DU-14` MINDRA умеет публиковать нейтральные Intrinsic Signals: novelty, prediction discrepancy, information gain, competence change и другие свойства опыта.

Следующий слой должен вводить persistent internal regulation, чтобы одинаковое внешнее событие могло иметь разную функциональную значимость при разном внутреннем состоянии Agent.

При этом `Valuation`, `Appraisal`, `Affect` и `Policy` ещё не спроектированы.

---

# 2. Проблема

Нужно определить архитектурную форму Drives.

Рассматривались варианты:

1. один global motivation scalar;
2. все drives как расстояние до homeostatic set-point;
3. полностью независимые drive modules без общего owner;
4. typed stateful `Drive System` с несколькими drive channels и explicit coupling;
5. отказаться от отдельного Drive layer и встроить всё сразу в Valuation/reward.

---

# 3. Требования

Решение должно:

- сохранять persistent internal state;
- не смешивать Drive с Intrinsic Signal/Reward/Value/Goal/Policy;
- позволять homeostatic и non-homeostatic dynamics;
- поддерживать несколько drives;
- не требовать общей scalar scale;
- поддерживать explicit cross-drive interaction;
- быть совместимым с `CognitiveState`/scheduler atomic commit;
- поддерживать persistence между Decision Window/Episode;
- допускать rule-based и learned dynamics;
- поддерживать `NoDrive`/Dummy/Control configurations;
- быть causally observable/intervenable;
- не создавать hidden runtime cycles;
- позволять будущим Goal Proposal/Appraisal/Valuation использовать Drive State без direct ownership leakage.

---

# 4. Вариант A — Global motivation scalar

Conceptually:

```text
motivation = f(all signals)
```

## Плюсы

- простой downstream interface;
- удобно добавлять в reward;
- легко визуализировать.

## Минусы

- уничтожает различие drive semantics;
- требует преждевременной scalarization;
- смешивает responsibility Drives и Valuation;
- затрудняет causal intervention отдельного drive;
- непонятно, что означает одинаковое числовое значение разных мотиваций;
- создаёт скрытый универсальный reward weight.

**Решение:** отклонён.

---

# 5. Вариант B — Все drives как homeostatic set-point deviation

## Плюсы

- сильная математическая структура;
- хорошо соответствует классической Homeostatic RL для регулируемых внутренних переменных;
- легко определять deficit/drive reduction.

## Минусы

- не у всех возможных мотивационных состояний есть естественный set-point;
- curiosity/learning-related regulation пришлось бы искусственно изображать физиологической переменной;
- API начал бы диктовать психологическую теорию вместо функциональной архитектуры;
- создаёт fake targets только ради единообразия.

**Решение:** отклонён как универсальная форма; принят как поддерживаемая drive family.

---

# 6. Вариант C — Полностью независимые drive modules

## Плюсы

- максимальная локальная модульность;
- каждый drive может иметь свою реализацию.

## Минусы

- нет единого owner `DriveStateSet`;
- сложнее atomic update/counterfactual snapshot;
- cross-drive coupling начинает реализовываться прямыми peer dependencies;
- reset/version/intervention semantics расходятся;
- повышается риск hidden scalarization/arbitration в случайном consumer.

**Решение:** отклонён как ownership model.

---

# 7. Вариант D — Typed stateful Drive System

Conceptually:

```text
Drive System
├── typed Drive A
├── typed Drive B
├── typed Drive C
├── explicit coupling
└── committed DriveStateSet
```

Каждый drive имеет собственную dynamics semantics.

Общий owner обеспечивает:

- identity/versioning;
- atomic update;
- lifecycle/reset;
- snapshot;
- coupling discipline;
- observability/intervention.

При этом не существует обязательного common motivation scalar.

**Решение:** принято.

---

# 8. Вариант E — Drives как часть Valuation/reward

## Плюсы

- меньше архитектурных блоков;
- проще классическая RL-интеграция.

## Минусы

- persistent internal state растворяется в decision function;
- невозможно отдельно проверить causal role dynamics;
- одинаковый signal и длительная потребность начинают смешиваться;
- Appraisal/Valuation получают скрытую историю мотивации;
- нарушается исходная исследовательская гипотеза MINDRA о собственном динамическом внутреннем состоянии.

**Решение:** отклонён.

---

# 9. Принятое решение

MINDRA использует **один semantic ownership boundary `Drive System`**, внутри которого существуют несколько independently configurable typed drive components.

Канонические свойства:

```text
Intrinsic Signal ≠ Drive State
Drive State ≠ Drive Pressure ≠ Value
Drive ≠ Goal ≠ Policy
DriveStateSet не scalarize автоматически
```

Drive components могут быть:

- homeostatic;
- adaptive motivational;
- fixed;
- learned;
- deterministic;
- stochastic.

Каждый обязан явно декларировать dynamics semantics.

---

# 10. Cross-drive update semantics

Взаимодействующие drives читают одну committed предыдущую `DriveStateSet` revision и формируют staged next-state.

Conceptually:

```text
D_t
├── A computes A_(t+1)
├── B computes B_(t+1)
└── C computes C_(t+1)
        ↓
explicit coupling/validation
        ↓
atomic commit D_(t+1)
```

Это предотвращает instantaneous hidden cycle и зависимость от physical completion order.

---

# 11. Homeostatic semantics

Для drive с реальной регулируемой переменной разрешено:

```text
regulated state
+
target/range
→ regulatory deviation
→ pressure
```

Но target/range не обязательны для других drive families.

Homeostatic reduction не становится автоматически reward MINDRA.

---

# 12. Goal и Valuation boundaries

Drive может:

- становиться source для `Goal Proposal`;
- предоставлять committed state будущему `Appraisal`/`Valuation`.

Drive не может:

- напрямую commit Goal;
- выбирать winning goal;
- вычислять action utility;
- выбирать action.

---

# 13. Temporal semantics

Drive dynamics использует logical time/lifecycle events из `DU-03`.

Wall-clock/compute latency не влияет на drive без отдельного agent-visible time input.

Drive может меняться без нового Environment observation через explicit recovery/decay/accumulation update.

---

# 14. Последствия

Положительные:

- persistent motivational state становится independently testable;
- можно сравнить meaningful drive dynamics с constant/shuffled/noise controls;
- несколько drives не теряют identity;
- homeostasis можно использовать там, где она семантически уместна;
- future Valuation получает vector-like internal regulation state;
- exact counterfactual intervention становится возможным.

Цена:

- contract сложнее scalar reward;
- понадобится policy совместимости drive revisions;
- cross-drive coupling требует явного проектирования;
- downstream Valuation должна сама решать конфликт/relative weighting.

---

# 15. Что ADR намеренно не определяет

Не фиксируются:

- конкретный список drives;
- наличие curiosity drive;
- наличие energy/resource drive;
- exact set-point functions;
- exact pressure ranges;
- coupling equations;
- update frequency;
- learned architecture;
- reward shaping;
- training algorithm;
- concrete Python types.

---

# 16. Обновляемые документы

Канонические последствия отражаются в:

- `docs/design/modules/drives.md`;
- `docs/design/contracts/drives.md`;
- `docs/design/current.md`;
- `docs/design/README.md`;
- `docs/design/decisions/README.md`;
- `AGENTS.md`.
