# ADR-0017 — Typed persistent Affect State с explicit history-dependent dynamics

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-17 — Affect Dynamics`

---

# 1. Контекст

После `DU-16` MINDRA имеет event-centered multidimensional `AppraisalRecord`, но не имеет отдельного persistent состояния, интегрирующего appraisal-history во времени.

Нужно решить, нужен ли отдельный Affect layer и в какой форме.

При этом `Valuation`, `Salience`, `Memory Regulation`, `Executive Control` и `Policy` ещё не спроектированы.

---

# 2. Проблема

Рассматривались варианты:

1. не иметь отдельного Affect — downstream consumers читают только текущий Appraisal/историю;
2. хранить один low-dimensional valence/arousal или PAD state;
3. хранить набор discrete emotion labels/intensities;
4. объединить Affect с Drive System;
5. использовать typed persistent Affect System с явной history-dependent dynamics и optional derived views.

---

# 3. Требования

Решение должно:

- иметь самостоятельную causal role или быть отклонено;
- поддерживать temporal inertia/history dependence;
- не дублировать event-level Appraisal;
- не дублировать regulatory Drive State;
- не быть готовой Utility/Value;
- не требовать human emotion taxonomy;
- поддерживать actual/predicted/imagined/retrospective provenance;
- соблюдать committed state/scheduler semantics;
- поддерживать reset/persistence/snapshot;
- позволять intervention и causal controls;
- иметь falsification criterion;
- не делать Cortex обязательным.

---

# 4. Вариант A — Без отдельного Affect

Conceptually:

```text
current Appraisal + recent Appraisal history
→ downstream consumers
```

## Плюсы

- меньше модулей;
- нет дополнительного state;
- легче реализовать первую систему.

## Минусы

- каждый downstream consumer начинает самостоятельно интегрировать историю;
- temporal inertia перестаёт иметь единого semantic owner;
- одинаковая history-dependent modulation может дублироваться в Valuation/Salience/Memory;
- сложнее causal intervention именно интегрированного состояния;
- bounded online state заменяется ambient history access.

**Решение:** отклонён как canonical architecture, но сохраняется как обязательный `NoAffect` baseline/control.

Отдельный Affect остаётся falsifiable и может быть удалён будущим ADR при отрицательных результатах.

---

# 5. Вариант B — Обязательный valence/arousal/PAD state

Conceptually:

```text
Affect = [valence, arousal]
```

или:

```text
Affect = [pleasure, arousal, dominance]
```

## Плюсы

- компактность;
- сильная human affect literature;
- удобно визуализировать;
- легко передавать downstream.

## Минусы

- human self-report geometry не обязана быть оптимальным functional state искусственного Agent;
- `dominance` частично пересекается с уже явными controllability/coping/self-capability constructs;
- один space преждевременно scalarize/смешивает разные temporal mechanisms;
- сложно расширять без нарушения compatibility.

**Решение:** отклонён как mandatory canonical state. Допустим как implementation/view/baseline.

---

# 6. Вариант C — Discrete emotion labels/intensities

Conceptually:

```text
fear=0.7
joy=0.1
anger=0.3
```

## Плюсы

- человекочитаемо;
- легко сравнивать с emotion datasets;
- удобно для role-playing/expressive agents.

## Минусы

- human taxonomy становится архитектурой без функционального обоснования;
- label скрывает causal sources;
- создаёт сильную антропоморфную интерпретацию;
- плохо переносится на задачи без социальной/emotion semantics;
- смешивает diagnostic interpretation и agent-owned state.

**Решение:** отклонён как canonical state; допустим только как research/diagnostic mapping.

---

# 7. Вариант D — Affect как часть Drive System

## Плюсы

- оба механизма persistent;
- меньше ownership boundaries;
- можно использовать общую dynamics infrastructure.

## Минусы

- Drive представляет typed regulatory condition, Affect — history-dependent integration appraisals;
- Affect не обязан иметь target/deficit/pressure;
- изменение appraisal-history не обязано менять drive;
- изменение drive не обязано означать изменение affect;
- объединение затрудняет независимые interventions/ablations.

**Решение:** отклонён.

---

# 8. Вариант E — Typed persistent Affect System

Conceptually:

```text
AffectStateSet_t
+
eligible AppraisalRecord(s)
+
logical time
→ Affect Dynamics
→ AffectStateSet_(t+1)
```

Система поддерживает несколько typed channels, но не требует одного emotion/valence representation.

Low-dimensional/diagnostic representations являются derived views.

## Плюсы

- explicit owner temporal integration;
- сохраняется causal provenance appraisal-history;
- поддерживает inertia/decay/recovery/hysteresis;
- не требует human emotion taxonomy;
- подходит для causal intervention;
- не смешивается с Drive/Valuation;
- можно реализовать rule-based или learned;
- поддерживает branch-local affect в imagination.

## Минусы

- добавляет state и complexity;
- требует доказать, что эффект не объясняется простой дополнительной памятью/recurrent capacity;
- downstream DU должны явно решить, где Affect действительно используется;
- конкретная channel semantics пока остаётся открытой.

**Решение:** принято.

---

# 9. Принятое решение

MINDRA использует отдельный **typed persistent `Affect System`** как agent-owned history-dependent state boundary.

Канонически:

```text
Appraisal ≠ Affect
Affect ≠ Drive
Affect ≠ Utility/Value
Affect ≠ emotion label
```

Affect update получает previous committed Affect + eligible Appraisal records + logical-time/lifecycle input и создаёт новую committed Affect revision.

---

# 10. Temporal feedback

Affect может влиять на будущую Appraisal/Valuation/Salience только через explicit previous committed revision.

Canonical order:

```text
Affect A_t
→ Appraisal R_t
→ Affect A_(t+1)
```

Instantaneous cycle запрещён.

---

# 11. Source-mode semantics

Принято:

- actual appraisal — natural eligible source;
- predicted appraisal — может создавать anticipatory Affect только через explicit source policy;
- imagined appraisal — по умолчанию обновляет только branch-local simulated Affect;
- retrospective current reappraisal — может менять current Affect;
- intervened/replayed/offline source сохраняет соответствующую provenance.

---

# 12. Low-dimensional views

Valence/arousal/PAD и emotion labels не являются source of truth.

Они могут существовать как:

- concrete implementation;
- `AffectView`;
- diagnostic mapping;
- baseline/control.

Каждый view versioned относительно source AffectStateSet.

---

# 13. Falsifiability

Отдельный Affect boundary считается исследовательски оправданным только при evidence, что temporal state имеет специфическую causal роль.

Обязательные controls должны включать, где применимо:

```text
NoAffect
ResetEveryEvent
ShuffledHistory
matched recurrent/history control
```

Если полноценный Affect не превосходит/не отличается содержательно от matched controls и interventions не дают ожидаемых специфических downstream effects, решение должно быть пересмотрено новым ADR.

---

# 14. Последствия

Положительные:

- MINDRA получает явную временную инерцию appraisal-history;
- downstream modules не обязаны самостоятельно интегрировать весь Appraisal history;
- possible mood/affect-congruent effects становятся causally testable;
- imagined trajectories могут иметь собственную branch-local Affect dynamics;
- human affect mappings не определяют core architecture.

Отрицательные/стоимость:

- дополнительный state/snapshot burden;
- требуется careful separation от Drives и Valuation;
- нужен matched-control experimental design;
- до `DU-18…23` downstream value Affect ещё не полностью определена.

---

# 15. Что ADR намеренно не определяет

- concrete Affect channel list;
- valence/arousal/PAD geometry;
- exact equations;
- baseline values;
- persistence default первой версии;
- concrete recurrent architecture;
- source weights;
- training objective;
- downstream policies;
- exact Python API.

---

# 16. Требуемые обновления

Решение должно быть отражено в:

- `docs/design/modules/affect.md`;
- `docs/design/contracts/affect.md`;
- `docs/design/current.md`;
- `docs/design/README.md`;
- `docs/design/decisions/README.md`;
- `docs/design/contracts/README.md`;
- `docs/research/README.md`;
- `AGENTS.md`;
- при необходимости `appraisal.md`/глоссарии/карте модулей.
