# ADR-0016 — Event-centered multidimensional Appraisal без обязательной emotion/utility scalarization

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-16 — Appraisal`

---

# 1. Контекст

После `DU-15` MINDRA уже имеет:

- committed Goals;
- persistent Drive State;
- World/Self Model;
- Memory retrieval;
- Intrinsic Signals.

Следующая ответственность должна оценивать значение **конкретного события или рассматриваемого исхода** относительно текущего состояния Agent.

При этом Affect, Valuation, Salience и Policy ещё не спроектированы.

---

# 2. Проблема

Нужно определить архитектурную форму Appraisal.

Рассматривались варианты:

1. Appraisal как один scalar valence/reward;
2. Appraisal как классификатор human emotion labels;
3. жёстко скопировать одну конкретную психологическую appraisal theory со всеми dimensions;
4. typed multidimensional event-centered `Appraisal Profile` с extensible dimension schema;
5. отказаться от Appraisal и встроить всё сразу в Valuation/Cortex.

---

# 3. Требования

Решение должно:

- быть event-level, а не persistent Affect state;
- зависеть от current Goals/Drives/World/Self context;
- поддерживать actual, predicted, imagined и retrospective targets;
- сохранять target/context/revision provenance;
- не смешивать novelty/surprise с desirability;
- разводить controllability и coping potential;
- не требовать human emotion label;
- не требовать universal scalar valence;
- не выполнять action selection;
- поддерживать partial/unknown dimensions;
- позволять rule-based/learned/Cortex-assisted implementation;
- поддерживать reappraisal без переписывания history;
- быть causally intervenable и observable;
- не использовать evaluator Ground Truth natural способом;
- оставаться совместимым с будущими Affect/Valuation/Salience.

---

# 4. Вариант A — Один scalar appraisal/valence

Conceptually:

```text
event + context
→ appraisal = -0.63
```

## Плюсы

- простой interface;
- легко передать в RL/reward;
- удобно визуализировать.

## Минусы

- теряется причина оценки;
- конфликт Goals/Drives преждевременно scalarize;
- практически сливает Appraisal с Valuation;
- dimension-specific intervention невозможна или искусственна;
- одинаковое число может означать разные механизмы;
- легко превращается в disguised reward model.

**Решение:** отклонён как canonical boundary.

---

# 5. Вариант B — Emotion label classifier

Conceptually:

```text
event + context
→ fear / joy / anger / ...
```

## Плюсы

- интуитивно;
- существует много human-labeled datasets;
- легко демонстрировать результат.

## Минусы

- emotion category является downstream interpretation, а не объясняет appraisal structure;
- human emotion taxonomy не обязана быть функциональной архитектурой Agent;
- скрывает multidimensional causes;
- создаёт антропоморфное впечатление;
- плохо подходит causal intervention отдельных факторов;
- не гарантирует полезность для decision making.

**Решение:** отклонён как canonical output. Emotion mapping допустим только как research/diagnostic layer.

---

# 6. Вариант C — Полностью зафиксировать одну человеческую appraisal theory

Например, напрямую принять полный набор checks конкретной Component Process/OCC/другой модели.

## Плюсы

- сильная психологическая теория;
- готовая терминология;
- можно сравнивать с human data.

## Минусы

- разные appraisal theories используют разные dimension sets и структуры;
- часть human dimensions требует социальных/нормативных representations, которых в MINDRA пока нет;
- architecture API начал бы заранее утверждать психологическую теорию;
- некоторые dimensions могут быть функционально избыточны для MicroWorld;
- сложно отделить полезный механизм от биологической аналогии.

**Решение:** отклонён как rigid universal schema. Человеческие теории используются как evidence/candidate dimensions.

---

# 7. Вариант D — Typed multidimensional event-centered profile

Conceptually:

```text
AppraisalTarget
+
versioned current context
        ↓
Appraisal System
        ↓
AppraisalProfile
├── relevance
├── goal congruence
├── drive conduciveness
├── expectedness
├── controllability
├── coping potential
├── urgency
└── extensions
```

## Плюсы

- сохраняет причины оценки;
- не требует premature scalarization;
- поддерживает different estimators;
- легко интервенировать отдельные dimensions;
- schema extensible;
- совместимо с human appraisal literature без полного копирования;
- естественно отделяется от Affect и Valuation;
- позволяет partial profile/availability semantics.

## Минусы

- interface сложнее;
- downstream modules должны явно решать, какие dimensions нужны;
- calibration разных dimensions потребует разных методов;
- first version придётся ограничить минимальным subset.

**Решение:** принято.

---

# 8. Вариант E — Встроить всё в Valuation/Cortex

## Плюсы

- меньше компонентов;
- сильная LLM потенциально может сразу рассуждать о значимости события.

## Минусы

- нельзя отделить event interpretation от final decision value;
- Cortex становится скрытым owner внутренней оценки;
- сложнее ablation/intervention;
- невозможно независимо проверить влияние Goals/Drives на appraisal;
- persistent Affect позднее не получает чистый event-level input;
- исчезает одна из центральных исследовательских гипотез MINDRA.

**Решение:** отклонён.

---

# 9. Принятое решение

MINDRA использует **event-centered multidimensional `Appraisal System`**.

Канонически:

```text
Appraisal ≠ Intrinsic Signal
Appraisal ≠ Drive
Appraisal ≠ Affect
Appraisal ≠ Valuation
Appraisal ≠ Salience
Appraisal ≠ Policy
```

Appraisal оценивает target относительно explicit committed context.

---

# 10. Dimension semantics

Core design поддерживает прежде всего:

- relevance;
- per-goal congruence;
- per-drive conduciveness;
- expectedness;
- controllability;
- coping potential;
- urgency.

Agency/attribution и normative compatibility являются optional/extension dimensions.

Обязательный exact subset первой software version определяется позднее.

---

# 11. Expectedness и Intrinsic Signals

Expectedness не дублирует novelty/prediction error.

```text
Intrinsic Signals
→ нейтральное evidence о novelty/surprisal/discrepancy

Appraisal expectedness
→ relation target ↔ prior expectation в текущем appraisal context
```

Если prior prediction отсутствует, dimension может быть unknown/unavailable.

---

# 12. Controllability и coping potential

Они принимаются как разные dimensions.

```text
controllability
→ насколько situation/consequence чувствительна к available actions

coping potential
→ насколько текущий Agent способен эффективно справиться/адаптироваться
```

Это позволяет объединять World Model и Self Model без смешения их responsibilities.

---

# 13. Valence/scalarization

Mandatory global valence scalar не принимается.

Optional local event polarity summary допустим только как derived representation с explicit aggregator identity/revision.

Он не является Utility/Value/Reward.

---

# 14. Reappraisal

Повторная оценка target создаёт новый `AppraisalRecord` с relation к предыдущему.

```text
old appraisal
≠
mutable object, который переписывается новой интерпретацией
```

Так сохраняется temporal history изменения смысла события для Agent.

---

# 15. Последствия

Положительные:

- Goals и Drives получают чистую точку интеграции;
- future Affect может интегрировать event-level profiles;
- Valuation сможет агрегировать многомерные факторы позже;
- Appraisal можно тестировать independently;
- можно использовать rule-based baseline до neural implementation;
- Cortex остаётся optional capability;
- human appraisal literature используется без заявления о human-like feelings.

Цена:

- требуется versioned dimension schema;
- нужно проектировать partial-profile compatibility;
- evaluation разных dimensions будет сложнее одного reward score;
- first implementation должна строго ограничить scope.

---

# 16. Что решение намеренно не определяет

ADR не фиксирует:

- exact dimension numeric domains;
- mandatory first-version dimension set;
- neural architecture;
- local polarity formula;
- Affect Dynamics;
- Valuation aggregation;
- emotion taxonomy;
- concrete training labels/losses;
- Python types.

---

# 17. Обновляемые документы

Принятие ADR требует согласования:

- `docs/design/modules/appraisal.md`;
- `docs/design/contracts/appraisal.md`;
- `docs/design/current.md`;
- `docs/design/README.md`;
- decision/contract/research indexes;
- coding-agent safeguards по мере необходимости.
