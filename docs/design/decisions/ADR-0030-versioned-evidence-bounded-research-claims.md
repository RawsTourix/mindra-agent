# ADR-0030 — Versioned evidence-bounded Research Claims вместо свободного reporting prose

## Статус

**Статус:** accepted  
**Дата:** 2026-08-17  
**Связанный Design Update:** `DU-30 — Research Claims / Limitations`

---

# 1. Контекст

После `DU-28` MINDRA имеет формальную evaluation architecture, а после `DU-29` — engineering verification architecture.

Но сами выводы всё ещё могли бы существовать как свободный текст в README, issue, статье или презентации.

Это создаёт риски:

- causal wording сильнее experimental design;
- scope creep от одного task/checkpoint к architecture-wide claim;
- publication bias против negative/null evidence;
- anthropomorphic inference из human-inspired module names;
- потеря limitations между отчётами;
- старые claims продолжают циркулировать после противоречащего evidence;
- engineering correctness смешивается с functional usefulness;
- concrete Cortex/compute/data dependence теряется в prose.

Нужно определить canonical research-claim lifecycle до contract freeze и version roadmap.

---

# 2. Вариант A — Claims только в статьях/README

Researcher вручную формулирует выводы в соответствующем документе.

## Плюсы

- минимальная инфраструктура;
- привычный scientific workflow;
- не требует отдельного registry.

## Минусы

- source of truth фрагментируется;
- claims трудно связать с exact evidence revision;
- limitations копируются/теряются вручную;
- old claims трудно supersede;
- automatic consistency checks невозможны;
- wording drift между README/paper/slides остаётся незаметным.

**Решение:** недостаточно.

---

# 3. Вариант B — EvaluationReport является claim source of truth

Все выводы хранятся прямо в `DU-28 EvaluationReport`.

## Плюсы

- близость к evidence;
- меньше новых сущностей;
- удобно для одного experiment.

## Минусы

- claim может объединять evidence из нескольких studies;
- claim lifecycle живёт дольше конкретного EvaluationReport;
- contradictory evidence из новых runs требует меж-study review;
- project-wide limitations/known unknowns плохо помещаются в run/report;
- publication wording всё равно может уйти дальше report.

**Решение:** EvaluationReport остаётся evidence source, но не владельцем research claim lifecycle.

---

# 4. Вариант C — Один narrative Limitations document

Поддерживать центральный `LIMITATIONS.md` и вручную обновлять его.

## Плюсы

- ограничения видимы;
- просто читать человеку;
- легко начать.

## Минусы

- limitation не имеет stable identity/status/target;
- невозможно понять, какие claims она ограничивает;
- resolved/obsolete limitations трудно отслеживать;
- negative results и supersession claims не решаются.

**Решение:** narrative summary может существовать как view, но не как canonical model.

---

# 5. Вариант D — Versioned Claim + Limitation registries с evidence lineage

Conceptually:

```text
Evaluation / Verification Evidence
          ↓
     ObservationRecord
          ↓
    InterpretationRecord
          ↓
       ResearchClaim
       /     |      \
      ↓      ↓       ↓
   Scope  Limitations Unknowns
      \      |       /
       \     |      /
        ClaimReview
            ↓
      revised status / supersession
```

## Плюсы

- claim traceable до evidence;
- scope first-class;
- negative/challenging evidence сохраняется;
- limitations/known unknowns имеют stable identity;
- old claims можно weaken/supersede без history rewrite;
- reporting language можно проверять против canonical claim;
- anthropomorphic/AGI overclaim patterns можно формализовать;
- удобно для future papers/reports и long-lived research program.

## Минусы

- дополнительная документационная/инфраструктурная дисциплина;
- существует риск избыточной бюрократии;
- evidence-strength taxonomy нельзя сделать универсальной;
- часть interpretations останется judgment-dependent.

**Решение:** принят.

---

# 6. Почему Observation ≠ Interpretation ≠ Claim

Одна метрика сама по себе не задаёт теоретический смысл.

Пример:

```text
metric:
Workspace treatment +4% success
```

Возможные interpretations:

- bounded broadcast помог coordination;
- treatment имел больше usable state;
- stochastic variation;
- конкретный implementation router лучше baseline;
- mismatch compute/context остался.

Claim допускается только после explicit interpretation и assessment alternatives.

---

# 7. Почему ClaimScope first-class

Основной риск experimental AI — незаметный переход:

```text
работает на одном benchmark
→ работает вообще
```

MINDRA имеет много dimensions variation:

- Cortex;
- world/task distribution;
- training data;
- module implementations;
- compute;
- checkpoint revision;
- interventions;
- hardware/software.

Поэтому scope не является примечанием; это обязательная часть claim identity.

---

# 8. Почему negative/null/inconclusive различаются

Нулевой point estimate при высокой uncertainty и хорошо ограниченный near-zero effect имеют разный evidential meaning.

Также invalid experiment и not-measured вообще не являются null result.

Поэтому canonical reporting различает минимум:

```text
negative evidence
null estimate
inconclusive
invalid
not measured
```

---

# 9. Почему module gate не меняет design автоматически

`DU-17/21/22/23` содержат falsifiable module gates.

Если gate даёт отрицательный evidence:

```text
ModuleGateOutcome
→ ClaimReview
→ design review
→ ADR
```

а не:

```text
experiment failed
→ delete module from docs
```

Это сохраняет разделение evidence и architecture governance.

---

# 10. Почему consciousness claims имеют отдельный stop-sign

MINDRA использует функциональные термины, вдохновлённые когнитивными науками:

- Self Model;
- Appraisal;
- Affect;
- Workspace;
- Drives.

Но функциональная реализация/causal role не является прямым измерением phenomenal consciousness.

Поэтому canonical design запрещает inference leaps:

```text
Workspace → consciousness
Affect → subjective feeling
Self Model → self-awareness proof
first-person Cortex text → phenomenal self-report
```

без отдельного bridge evidence, которого текущая architecture не предоставляет.

Это не claim, что consciousness отсутствует. Это claim discipline: **достаточных оснований утверждать наличие нет**.

---

# 11. Почему architecture-level claim сильнее implementation-level

Одна neural implementation может выигрывать из-за:

- inductive bias;
- hidden capacity;
- optimization;
- preprocessing;
- backend quality.

Поэтому утверждение о semantic architecture требует более широкой robustness/controls evidence, чем утверждение о конкретной implementation.

---

# 12. Claim lifecycle

Accepted lifecycle conceptually поддерживает:

```text
proposed
under evaluation
supported within scope
challenged / weakened
inconclusive
unsupported within scope
superseded / withdrawn
```

Изменение статуса не переписывает предыдущую revision.

---

# 13. Limitations Registry

Limitations становятся stable research artifacts, поскольку:

- одна limitation может затрагивать несколько claims;
- limitation может быть временной или project-wide;
- её можно закрыть новым evidence;
- публикации должны ссылаться на актуальное состояние.

Narrative limitations в paper остаются derived view.

---

# 14. Known unknowns

Вместо принудительного бинарного ответа MINDRA разрешает first-class `unknown`.

Это важно для вопросов, где текущий experiment не идентифицирует механизм, не переносится на новый Cortex или не имеет phenomenological measurement bridge.

---

# 15. Последствия

После ADR:

- substantial future claim должен иметь stable identity/revision;
- claim обязан иметь scope;
- evidence supporting/challenging claim сохраняется;
- limitations и known unknowns first-class;
- publication prose должна быть traceable до canonical claim;
- old claims supersede/weaken, а не silently rewrite;
- negative/null/inconclusive/invalid различаются;
- functional cognition terminology не является consciousness evidence;
- architecture changes по research evidence идут только через design review/ADR.

---

# 16. Что ADR не фиксирует

- exact database/storage;
- exact claim/status enums;
- numeric evidence score;
- p-value/Bayesian threshold;
- automatic NLP linter;
- paper format;
- preregistration platform;
- journal/conference;
- philosophical theory of consciousness;
- operational AGI definition.

---

# 17. Принятое решение

```text
Evidence
→ Observation
→ Interpretation
→ Versioned ResearchClaim + ClaimScope
→ Limitations / KnownUnknowns
→ ClaimReview / Supersession
→ traceable report/publication wording
```

при строгих инвариантах:

```text
claim strength ≤ evidence strength
claim generality ≤ demonstrated/explicitly supported scope
functional similarity ≠ phenomenological equivalence
research evidence changes design only through ADR
```
