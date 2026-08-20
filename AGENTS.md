# AGENTS.md — правила работы с MINDRA

## Назначение

Карта обязательного контекста для Codex, ChatGPT и других coding agents. Канонические знания находятся в `docs/`; этот файл не дублирует полный design и **не хранит копию текущего номера implementation step**.

Текущий разрешённый milestone/step определяется только:

```text
docs/design/current.md
```

Operational workflow и постоянный handoff определяются:

```text
docs/process/README.md
```

Mode-specific правила:

- independent implementation/correction audit — `docs/process/independent-audit.md`;
- opening next step + Codex instruction authoring — `docs/process/codex-instruction-authoring.md`;
- canonical Codex task content — `docs/versions/codex-step-prompt-template.md`.

История чата не является source of truth для этих правил.

## Язык

- документация и комментарии — на русском;
- technical identifiers/API/package/class/function/type names — на английском.

---

# Перед любой работой

1. Проверить repository status/HEAD.
2. Прочитать `docs/README.md`, `docs/process/README.md` и `docs/design/current.md`.
3. Выбрать operational mode по `docs/process/README.md`:
   - audit/correction → прочитать `docs/process/independent-audit.md`;
   - opening next step / Codex prompt → прочитать `docs/process/codex-instruction-authoring.md`;
   - design/clarification → соблюдать transition/design rules из `docs/process/codex-instruction-authoring.md`.
4. Обязательно прочитать:
   - `docs/design/contract-adr-consistency-freeze.md`;
   - `docs/design/contracts/semantic-freeze-manifest.md`;
   - `docs/design/version-roadmap.md`.
5. Определить разрешённый version scope и implementation step **только по `current.md`**.
6. Прочитать релевантный canonical design owner + accepted ADR + semantic contract.
7. Для implementation обязательно прочитать:
   - `docs/versions/codex-step-prompt-template.md`;
   - `docs/versions/vX.Y/README.md`;
   - `docs/versions/vX.Y/implementation-sequence.md`;
   - section текущего `Vx.y-IS-XX`;
   - все accepted step-specific clarification/correction docs, перечисленные в `current.md`;
   - перечисленный там canonical context.
8. Проверить prerequisites/VerificationObligations текущего step.
9. Не выходить за разрешённый scope и не начинать следующий `IS` заранее.

Если version-specific документы ещё не приняты, coding не начинается.

Один coding task выполняет **только один implementation step**. Завершение Codex task не открывает следующий step автоматически: между шагами обязателен independent ChatGPT audit.

Каждый implementation prompt строится по актуальной revision `docs/versions/codex-step-prompt-template.md`. Не использовать старую копию prompt из чата или embedded example, если она расходится с canonical template.

---

# Operational modes

Canonical definitions находятся в `docs/process/README.md`.

```text
MODE-DESIGN
→ exact version/step clarification до coding

MODE-INSTRUCTION
→ copy-ready Codex instruction для уже OPEN step

MODE-AUDIT
→ independent review remote implementation/correction

MODE-CORRECTION
→ минимальная correction-инструкция; next step CLOSED

MODE-TRANSITION
→ acceptance текущего step и только затем opening следующего
```

Нельзя смешивать незавершённый audit с автоматическим opening следующего step.

При потере контекста чата использовать recovery protocol из `docs/process/README.md`, а не создавать новый ad-hoc handoff по памяти.

---

# Source of truth

```text
accepted ADR + canonical design
        ↓
Semantic Freeze Baseline F31
        ↓
semantic-frozen contracts
        ↓
DU-32 Version Roadmap
        ↓
version specification / exact contracts
        ↓
implementation sequence
        ↓
step-specific accepted clarification/correction
        ↓
docs/design/current.md
        ↓
current OPEN implementation step
        ↓
canonical Codex step prompt
        ↓
implementation
        ↓
verification evidence
        ↓
independent ChatGPT audit
        ↓
correction ИЛИ acceptance/transition
        ↓
engineering/research evidence
        ↓
versioned research claims
```

`F31` freezing означает semantic meaning, **не exact Python API**.

Roadmap определяет sequencing, **не имеет права переопределять F31**.

Operational prompt template не определяет архитектуру: он заставляет Codex прочитать и исполнить актуальные accepted sources of truth и verification rules.

---

# Roadmap

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

Нельзя реализовывать roadmap или даже всю текущую version одним change/PR/task.

---

# Принятые boundaries

| Область | Canonical design | Contract | ADR |
|---|---|---|---|
| Environment | `docs/design/modules/environment.md` | `contracts/environment.md` | `ADR-0007` |
| Perception | `docs/design/modules/perception.md` | `contracts/perception.md` | `ADR-0008` |
| Goals | `docs/design/modules/goals.md` | `contracts/goals.md` | `ADR-0009` |
| Cortex | `docs/design/modules/cortex.md` | `contracts/cortex.md` | `ADR-0010` |
| Memory Core | `docs/design/modules/memory.md` | `contracts/memory.md` | `ADR-0011` |
| World Model | `docs/design/modules/world-model.md` | `contracts/world-model.md` | `ADR-0012` |
| Self Model | `docs/design/modules/self-model.md` | `contracts/self-model.md` | `ADR-0013` |
| Intrinsic Signals | `docs/design/modules/intrinsic-signals.md` | `contracts/intrinsic-signals.md` | `ADR-0014` |
| Drives | `docs/design/modules/drives.md` | `contracts/drives.md` | `ADR-0015` |
| Appraisal | `docs/design/modules/appraisal.md` | `contracts/appraisal.md` | `ADR-0016` |
| Affect | `docs/design/modules/affect.md` | `contracts/affect.md` | `ADR-0017` |
| Valuation | `docs/design/modules/valuation.md` | `contracts/valuation.md` | `ADR-0018` |
| Salience | `docs/design/modules/salience.md` | `contracts/salience.md` | `ADR-0019` |
| Memory Regulation | `docs/design/modules/memory-regulation.md` | `contracts/memory-regulation.md` | `ADR-0020` |
| Workspace | `docs/design/modules/workspace.md` | `contracts/workspace.md` | `ADR-0021` |
| Executive Control | `docs/design/modules/executive-control.md` | `contracts/executive-control.md` | `ADR-0022` |
| Policy / Planner | `docs/design/modules/policy-planner.md` | `contracts/policy-planner.md` | `ADR-0023` |
| Action Boundary | `docs/design/modules/action-boundary.md` | `contracts/action-boundary.md` | `ADR-0024` |
| Experience/Data/Replay | `docs/design/experience-data-replay.md` | `contracts/experience-data-replay.md` | `ADR-0025` |
| Training Lifecycle | `docs/design/training-lifecycle.md` | `contracts/training-lifecycle.md` | `ADR-0026` |
| Checkpoint/Reproducibility/Compute | `docs/design/checkpoint-reproducibility-compute.md` | `contracts/checkpoint-reproducibility-compute.md` | `ADR-0027` |
| MINDRA-Eval | `docs/design/mindra-eval.md` | `contracts/mindra-eval.md` | `ADR-0028` |
| Engineering Testing | `docs/design/engineering-testing.md` | `contracts/engineering-testing.md` | `ADR-0029` |
| Research Claims / Limitations | `docs/design/research-claims-limitations.md` | `contracts/research-claims-limitations.md` | `ADR-0030` |
| Semantic Freeze | `docs/design/contract-adr-consistency-freeze.md` | `contracts/semantic-freeze-manifest.md` | `ADR-0031` |
| Version Roadmap | `docs/design/version-roadmap.md` | — | `ADR-0032` |

`contracts/...` означает `docs/design/contracts/...`.

---

# F31 consistency resolutions

```text
CR-01 Action lifecycle
CR-02 Memory admission ownership
CR-03 Replay taxonomy
CR-04 Consolidation vs Learning Update
CR-05 candidate/validated/activated revision lifecycle
```

Нельзя выбирать старую generic формулировку вместо F31 resolution.

---

# Cross-cutting stop-signs

```text
CognitiveState ≠ Agent Snapshot ≠ Checkpoint
MemoryRecord ≠ embedding/index
Memory Core ≠ Memory Regulation
World Prediction ≠ observed fact
Intrinsic Signal ≠ Reward/Drive/Value
Appraisal ≠ Affect ≠ Valuation
SalienceProfile ≠ AttentionAllocation
Retrieval ≠ Agent Memory Replay ≠ Training Replay
Consolidation ≠ Learning Update
CognitiveState ≠ Workspace
Executive Control ≠ Scheduler ≠ Policy
Planner ≠ Policy
SelectedActionIntent ≠ AuthorizedAction ≠ Action Commit
Action Commit ≠ Dispatch ≠ Environment Transition
ExperienceEvent ≠ TrainingSample
Training Runtime ≠ cognitive module
runtime dependency graph ≠ gradient graph
CandidateRevisionBundle ≠ Active AgentRevision
same seed ≠ same RNG state ≠ guaranteed same execution
ComputeManifest ≠ CognitiveResourceEnvelope
Evaluation Runtime ≠ Agent cognition
Engineering Testing ≠ MINDRA-Eval
Observation ≠ Interpretation ≠ ResearchClaim
functional similarity ≠ phenomenological equivalence
```

---

# Cognitive/runtime safeguards

- никакого runtime Service Locator, mutable global bus, hidden peer mutation или oracle input;
- Memory Core владеет Store/identity/structural validation/commit; Regulation — policy decisions;
- consolidation не делает optimizer update;
- Workspace не alias `CognitiveState`;
- Executive не меняет Scheduler graph/write authority и не выбирает Environment action;
- Policy — owner `SelectedActionIntent`;
- Planner — optional provider;
- `Action Commit` после authorization и до dispatch;
- post-commit failure не отменяет commit;
- blind retry при `execution_unknown` запрещён без dedup/idempotency evidence.

---

# Data/training/checkpoint safeguards

- `Experience Journal` append-only source;
- evaluator Ground Truth хранится отдельно;
- hindsight/relabel/re-encode создают derived sample;
- Agent Memory Replay не Training Replay;
- ordinary cognition не выполняет hidden `optimizer.step()`;
- runtime edge не создаёт gradient edge;
- candidate revision проходит validation до activation;
- failed candidate не мутирует live Agent;
- weights-only не full checkpoint;
- seed не заменяет current RNG state;
- exact restore не downgraded молча;
- `execution_unknown` блокирует unsafe retry/branch.

---

# Evaluation / Verification / Claims safeguards

- evaluator score/Ground Truth не писать в Agent normal path;
- `NoX` не называть matched control без реально matched confounders;
- episodes одного checkpoint не independent training replicates;
- actual compute/data/context/tuning differences входят в attribution;
- Engineering Verification и MINDRA-Eval создают разные evidence;
- line coverage не заменяет invariant coverage;
- flaky rerun/skip/quarantine не считается выполненной VerificationObligation;
- claim strength не превышает evidence strength/scope;
- negative/null/inconclusive/invalid/not-measured не смешиваются;
- Self Model/Affect/Workspace/first-person Cortex output не являются proof consciousness/subjective experience;
- один benchmark/result не proof AGI.

---

# Roadmap safeguards

- core correctness не должна зависеть от GPU;
- optional real Cortex не должен ломать `NoCortex`/control profile;
- не реализованный пока F31 mechanism представлен честным `No*`/Dummy/control path, а не hidden shortcut;
- новый causally relevant state сразу получает observability + snapshot/restore consideration;
- Experience/Verification не добавляются задним числом;
- neural training не внедряется hidden way до `v0.10` Training Lifecycle;
- hosted notebook/Colab/GPU model не hardcode'ится как architecture;
- tool/framework/model choice version-specific и не становится новым global invariant;
- version milestone не считается завершённым без acceptance/verification gate;
- следующая version design не начинается с намеренного обхода failed previous gate.

---

# Implementation-step safeguards

Operational details определяются `docs/process/README.md`, `docs/process/independent-audit.md` и `docs/process/codex-instruction-authoring.md`.

Обязательные invariants:

- один Codex task = один разрешённый `IS`;
- перед coding проверять prerequisites и current repository state;
- каждый task использует актуальный `docs/versions/codex-step-prompt-template.md`;
- не создавать файлы/abstractions следующего `IS` заранее;
- не ослаблять tests/type/import contracts ради green;
- не использовать hidden test mode, global mutable fixture state или production bypass;
- если документация оставляет semantic/architectural choice нерешённым — blocker, а не самостоятельный выбор;
- implementation-level file split можно уточнить только в пределах accepted package layers/semantics;
- после implementation выполнить targeted verification текущего step;
- затем выполнить полный уже существующий local regression profile текущей версии;
- если изменения находятся на remote commit и Actions доступен — проверить declared CI jobs/OS;
- `CI PENDING`, `CI RUNNING` и `CI NOT AVAILABLE` не считать `PASS`;
- итоговый отчёт должен различать фактически выполненную verification и недоступную/pending verification;
- Codex предлагает Conventional Commit message, но по умолчанию не выполняет commit/push;
- после push обязателен independent ChatGPT audit remote diff/code/tests;
- следующий `IS` открывается только после audit + acceptance gate;
- correction и следующий feature step не объединяются.

Для `v0.1` после создания toolchain в `IS-01` каждый последующий Codex task перед отчётом выполняет `FULL-C0` независимо от более узкого targeted profile текущего step.

---

# Canonical Codex prompt и его актуализация

Canonical operational source:

```text
docs/versions/codex-step-prompt-template.md
```

ChatGPT-side authoring/delivery rules:

```text
docs/process/codex-instruction-authoring.md
```

Правила:

1. prompt из истории чата не является source of truth;
2. embedded version-specific example prompt не имеет приоритета над canonical template;
3. при принятии нового version design обязательно проверить применимость шаблона;
4. при создании/изменении `implementation-sequence.md` обязательно проверить применимость шаблона;
5. перед открытием каждого следующего `IS` после ChatGPT audit проверить актуальность шаблона;
6. при изменении verification profiles, CI provider/jobs, mandatory commands, reporting/evidence semantics или обязательных source paths **в Codex prompt** обновить template тем же documentation patch;
7. если изменения не нужны, не делать фиктивный edit — достаточно подтвердить применимость текущей revision;
8. обязательное новое правило prompt нельзя оставлять только в чате;
9. финальная инструкция Codex в ChatGPT выдаётся как один copy-ready writing/document block по `docs/process/codex-instruction-authoring.md`;
10. если меняется только ChatGPT-side presentation/workflow, а content contract Codex не меняется, CSPT revision не bump'ается формально.

`AGENTS.md` и `docs/process/` проверяются вместе с prompt template при каждом существенном version/implementation workflow update. **Текущий номер implementation step здесь не дублируется:** он всегда читается из `docs/design/current.md`.

---

# Independent audit

После сообщения о push ChatGPT обязан перейти в `MODE-AUDIT` по:

```text
docs/process/independent-audit.md
```

Audit обязан:

- определить remote commit/HEAD;
- проверить diff относительно accepted baseline;
- прочитать changed production code и tests;
- сверить scope/forbidden scope;
- проверить exact accepted design/clarifications;
- искать negative/bypass/invariant defects независимо от отчёта Codex;
- честно различать independently observed CI и operator-confirmed CI;
- при defect оставить следующий `IS` CLOSED и выдать минимальную correction instruction;
- только после `AUDIT-PASS` перейти к `MODE-TRANSITION`.

Codex self-report не заменяет independent audit.

---

# Breaking change

Если implementation требует изменить F31 semantics:

```text
blocker/evidence
→ design review
→ новый ADR
→ canonical owner/contract update
→ новая freeze baseline revision
→ roadmap/version update
→ implementation
```

Не исправлять semantic mismatch только кодом или version README.

---

# Current implementation authority

Для текущей version используются accepted:

```text
docs/versions/vX.Y/README.md
docs/versions/vX.Y/implementation-sequence.md
docs/versions/codex-step-prompt-template.md
```

Разрешённый **сейчас** implementation step, его статус и закрытые/открытые последующие шаги определяются исключительно:

```text
docs/design/current.md
```

Не использовать `AGENTS.md` или index README как копию implementation status.