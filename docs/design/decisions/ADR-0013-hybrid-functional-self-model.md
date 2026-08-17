# ADR-0013 — Гибридная функциональная Self Model: capability facts + learned competence + calibrated predictions

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-13 — Self Model`

---

# 1. Контекст

После `DU-12` MINDRA умеет концептуально моделировать внешний мир, но ещё не имеет отдельной модели собственных функциональных возможностей.

Нужно поддержать:

- self-observable capability facts;
- learned competence;
- calibrated probability of success;
- known limitations;
- resource/cost estimates;
- adaptation после изменения Agent;
- causal evaluation роли self-estimates.

При этом нельзя смешивать Self Model с Cortex self-report, World Model, Executive Control или evaluator oracle.

---

# 2. Проблема

Рассматривались четыре архитектурных варианта:

1. natural-language self-reflection через Cortex;
2. только статический capability registry/manifest;
3. считать Agent частью World Model без отдельной Self Model;
4. гибридная Self Model: versioned capability facts + learned context-conditioned competence + explicit calibrated predictions.

---

# 3. Требования

Решение должно:

- отделять известную конфигурацию от learned competence;
- не зависеть от конкретной LLM;
- позволять `NoCortex`;
- не требовать global scalar confidence;
- поддерживать calibration against actual outcomes;
- учитывать behavior-relevant `agent_revision`;
- отделять success probability от uncertainty/support самой оценки;
- не давать Self Model decision authority Executive Control/Policy;
- не использовать evaluator-only truth normal runtime способом;
- поддерживать ablation/intervention/control;
- быть пригодным для snapshot/replay.

---

# 4. Вариант A — Cortex self-reflection как Self Model

Conceptually:

```text
prompt:
"Оцени, справишься ли ты"
        ↓
Cortex text/confidence
```

## Плюсы

- очень просто реализовать;
- использует pretrained знания Cortex;
- natural-language explanation получается автоматически.

## Минусы

- model-specific и плохо заменяемо;
- verbal confidence может быть miscalibrated;
- Cortex может не знать реальную runtime composition;
- самоописание смешивается с canonical self-state;
- трудно отделить competence estimate от prompt artifacts;
- `NoCortex` configuration теряет Self Model полностью.

**Решение:** отклонён как canonical architecture. Cortex может быть optional evidence/assistant, но не owner self-knowledge.

---

# 5. Вариант B — Только статический capability manifest

Conceptually:

```text
installed/enabled capabilities
→ Self state
```

## Плюсы

- достоверно для конфигурационных facts;
- легко версионировать;
- не требует обучения;
- хорошо переживает module swap.

## Минусы

- не знает фактической competence;
- не прогнозирует success/failure;
- не адаптируется к context/domain difficulty;
- не поддерживает calibration;
- capability available не означает capability effective.

**Решение:** manifest принят как один источник Self Model, но недостаточен как полный Self Model.

---

# 6. Вариант C — Self как часть World Model

Conceptually:

```text
world state
includes agent state
→ one unified model
```

## Плюсы

- концептуально единая динамическая модель;
- удобно для embodied physical state;
- меньше отдельных modules.

## Минусы

- смешивает внешний embodiment и внутреннюю competence;
- behavior-relevant Agent revision плохо ложится на world-state semantics;
- capability manifest/availability не является physical world prediction;
- calibration собственной успешности становится скрытой ответственностью World Model;
- сложно независимо ablate self-knowledge.

**Решение:** отклонён как общий boundary. Environment/body state может оставаться в World Model; функциональная competence принадлежит Self Model.

---

# 7. Вариант D — Гибридная функциональная Self Model

Conceptually:

```text
Agent Capability Manifest
       +
Self Evidence from experience
       ↓
Self Model
       ↓
Committed Self Belief
       ↓
context-conditioned Self Prediction
```

Особенности:

- known capability facts отделены от learned estimates;
- competence имеет domain/context;
- probability prediction имеет explicit target/horizon;
- estimate support/uncertainty отделена от probability outcome;
- после Agent revision self-knowledge может стать stale;
- Cortex является optional source/assistant;
- Executive Control остаётся downstream responsibility.

**Решение:** принято.

---

# 8. Evidence

Решение поддерживается существующими направлениями исследований:

- работы по confidence calibration показывают, что вербализованная/модельная уверенность не обязана соответствовать фактической accuracy и должна измеряться отдельно;
- embodied-agent исследования демонстрируют отдельную проблему elicitation/calibration собственной уверенности;
- MUSE и современные metacognitive agent frameworks отдельно моделируют competence awareness и последующее strategy regulation;
- robotic self-modeling показывает, что self-model может быть функциональной предсказательной моделью собственных свойств без утверждений о phenomenal self-awareness.

Датированный research pass сохранён в `docs/research/literature/DU-13-self-model-landscape-2026-08.md`.

---

# 9. Принятое решение

MINDRA использует отдельную **functional Self Model** со следующими принципами:

1. versioned `Agent Capability Manifest` содержит намеренно self-observable configuration/capability facts;
2. capability fact не равен competence;
3. Self Evidence формируется из причинно доступного опыта/operational facts;
4. Self Belief содержит context-conditioned competence/limitations;
5. Self Prediction имеет explicit target/context/horizon;
6. `P(success)` не является универсальным confidence;
7. uncertainty/support самой оценки отделена от probability predicted outcome;
8. behavior-relevant Agent change может инвалидировать/stale старые estimates;
9. Cortex self-report не является canonical self-knowledge;
10. Self Model не принимает решений за Executive Control/Policy;
11. evaluator-only truth не является natural self-evidence;
12. concrete estimator/calibration algorithm выбирается позже.

---

# 10. Последствия

## Положительные

- self-knowledge становится измеримым и причинно тестируемым;
- можно отдельно оценивать calibration и task accuracy;
- Cortex заменяем и не является обязательным;
- module/model swap имеет явную self-knowledge semantics;
- можно создавать overconfidence/underconfidence interventions;
- будущий Executive Control получает чистый input вместо текстовой интроспекции;
- Self Model можно ablate отдельно от World Model.

## Отрицательные

- требуется versioned capability manifest;
- нужна domain/context semantics competence;
- calibration требует накопления/разрешения прогнозов;
- transfer self-estimates между Agent revisions нетривиален;
- exact boundary физических embodiment facts требует дисциплины с World Model.

---

# 11. Что решение намеренно не определяет

Не определены:

- neural/statistical/hybrid estimator;
- task/capability taxonomy;
- calibration algorithm;
- Brier/NLL/ECE exact policy;
- uncertainty estimator;
- resource channel set;
- transfer learning между revisions;
- training loss/schedule;
- Cortex participation policy;
- exact Executive Control usage;
- exact schema/serialization.

---

# 12. Обновляемые документы

Решение отражается в:

- `docs/design/modules/self-model.md`;
- `docs/design/contracts/self-model.md`;
- `docs/design/decisions/README.md`;
- `docs/design/README.md`;
- `docs/design/current.md`;
- `docs/design/contracts/README.md`;
- `docs/research/README.md`;
- `AGENTS.md`.
