# ADR-0032 — Vertical capability version roadmap вместо module-order implementation

## Статус

**Статус:** accepted  
**Дата:** 2026-08-18  
**Связанный Design Update:** `DU-32 — Version Roadmap`

---

# 1. Контекст

После `DU-31` MINDRA имеет semantic freeze baseline `F31`:

- foundation/system semantics;
- cognitive/runtime boundaries;
- Experience/Data, Training, Checkpoint, Evaluation, Verification и Claims planes;
- 31 accepted ADR;
- 24 semantic-frozen boundary contracts;
- отсутствие blocking architectural TODO.

Нужно определить software roadmap, который:

- можно реализовать на ограниченном consumer compute;
- даёт runnable system на раннем этапе;
- не требует переписывать предыдущие версии;
- позволяет вводить learned mechanisms постепенно;
- сохраняет исследовательскую диагностируемость;
- подходит для ChatGPT/Codex workflow с version-specific instructions.

---

# 2. Вариант A — Реализовывать строго в порядке Design Updates

```text
DU-01 implementation
→ DU-02 implementation
→ ...
→ DU-32
```

## Плюсы

- простой mapping design → code sequence;
- легко объяснить историю проекта.

## Минусы

- Policy/Action Boundary появляются слишком поздно;
- ранние milestones долго не имеют end-to-end Agent loop;
- трудно проверять реальные cross-boundary assumptions;
- появляется риск писать много horizontal infrastructure без runnable vertical slice.

**Решение:** отклонён.

---

# 3. Вариант B — Сразу реализовать full MINDRA end-to-end

То есть собрать все modules, Training Runtime и Eval в одной большой версии.

## Плюсы

- быстро получаем визуально «полную» систему;
- меньше временных control implementations.

## Минусы

- слишком большой integration surface;
- невозможно локализовать ошибки;
- learned и architectural effects смешиваются;
- высокий риск скрытых deviations от F31;
- плохо подходит ограниченному compute;
- задания Codex становятся слишком большими;
- почти гарантирован крупный rewrite.

**Решение:** отклонён.

---

# 4. Вариант C — Сначала только neural prototype, потом архитектура

Например быстро обучить small LLM/agent и постепенно оборачивать его модулями.

## Плюсы

- рано появляется впечатляющее поведение;
- можно быстро пробовать ML ideas.

## Минусы

- Cortex/Policy легко становятся скрытым монолитом;
- architecture начинает подстраиваться под accidental neural implementation;
- causality/evidence/checkpoint contracts появляются задним числом;
- сложно доказать вклад MINDRA mechanisms.

**Решение:** отклонён.

---

# 5. Вариант D — Vertical capability ladder

Принять последовательность:

```text
deterministic contract/runtime kernel
        ↓
minimal complete Environment interaction
        ↓
replaceable Cortex
        ↓
persistent Memory/restore
        ↓
World/Self
        ↓
internal dynamics
        ↓
regulated Memory/Workspace
        ↓
Executive/Planner
        ↓
Training lifecycle
        ↓
research-grade harness
        ↓
integration hardening
        ↓
v1.0 Research Baseline
```

Ещё не реализованные F31 boundaries представлены только explicit `No*`/Dummy/control implementations либо отсутствуют из конкретной composition, если contract допускает optional capability.

## Плюсы

- runnable system появляется рано;
- каждая версия имеет meaningful acceptance gate;
- deterministic reference implementations существуют до сложного learning;
- Cortex подключается рано, но остаётся replaceable;
- Experience/Verification/Checkpoint semantics вводятся вместе с causally relevant state;
- training откладывается до появления хорошей attribution infrastructure;
- consumer hardware достаточно для core development;
- version-specific Codex instructions остаются небольшими.

## Минусы

- один semantic module может получить baseline implementation раньше, чем все его upstream advanced mechanisms;
- часть boundaries развивается в несколько milestones;
- требуется дисциплина, чтобы control implementation не превратился в alternate architecture.

**Решение:** принят.

---

# 6. Принятое roadmap sequence

```text
v0.1  Core Kernel
v0.2  MicroWorld Interaction
v0.3  Cortex Gateway
v0.4  Memory & Restore
v0.5  World & Self
v0.6  Intrinsic / Drives / Appraisal
v0.7  Affect / Valuation / Salience
v0.8  Memory Regulation / Workspace
v0.9  Executive / Planner
v0.10 Training & Revision Lifecycle
v0.11 Research Harness
v0.12 Integration Hardening
v1.0  MINDRA Research Baseline
```

Подробный scope принадлежит `docs/design/version-roadmap.md`.

---

# 7. Deterministic-first principle

Для substantial learned responsibility, где practically возможно, сначала должен существовать:

- deterministic/rule-based reference;
- Dummy/No*/control implementation;
- measurable responsibility-specific target;
- verification/evaluation path.

Это не означает, что reference heuristic считается желаемой финальной intelligence.

Её роль:

> дать test oracle и causal comparison до появления learned provider.

---

# 8. Compute principle

Core correctness не зависит от GPU.

Roadmap использует planning classes:

```text
C0 — CPU core
C1 — consumer GPU class
C2 — burst/notebook accelerator
C3 — optional larger compute
```

Neural/Cortex workloads могут использовать C1/C2/C3, но absence конкретного accelerator не меняет architecture semantics.

Hosted notebook GPU не должен hardcode'иться как обязательный device/provider.

---

# 9. Training placement

Серьёзный Training Runtime появляется только после того, как существуют:

- causal runtime;
- Environment;
- Experience Journal;
- snapshot/restore;
- module boundaries;
- action attribution;
- enough module-specific metrics.

Поэтому first training milestone — `v0.10`.

Это не запрещает использовать pretrained Cortex inference в `v0.3+`.

---

# 10. Cross-cutting responsibilities

Engineering Verification, observability, provenance, Experience и checkpoint support не трактуются как «поздняя инфраструктура».

Они появляются по мере возникновения соответствующего causally relevant state.

`v0.11` завершает generic research-grade workflow, но не является первым моментом, когда система получает tests/evidence.

---

# 11. Version design before coding

Roadmap не является прямым implementation spec.

Для каждого milestone обязательны:

```text
docs/versions/vX.Y/README.md
docs/versions/vX.Y/implementation-sequence.md
```

Сначала принимается version-specific design и exact choices, затем последовательность задач Codex, затем код.

---

# 12. Последствия

После `ADR-0032`:

- общий DU design cycle можно завершить;
- первым version-design этапом становится `v0.1`;
- implementation всего roadmap одним PR/заданием запрещена;
- отсутствие GPU не блокирует `v0.1/v0.2`;
- Cortex model/provider не фиксируется roadmap;
- end-to-end training не является prerequisite для первых behavioural experiments;
- conditional Affect/Workspace/Executive/Planner boundaries сохраняют `No*`/matched controls;
- `v1.0` означает research platform baseline, а не AGI/consciousness claim.

---

# 13. Breaking roadmap vs breaking architecture

Изменить grouping/version order можно без нового architecture ADR, если F31 semantics не меняются.

Если implementation blocker требует изменить owner/source-of-truth/commit/visibility/module semantics:

```text
blocker
→ design review
→ новый ADR
→ новая semantic freeze baseline
→ roadmap revision
```

Roadmap не имеет права silently supersede F31.
