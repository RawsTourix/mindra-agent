# AGENTS.md — правила работы с MINDRA

## Назначение

Этот файл — **карта обязательного контекста** для Codex, ChatGPT и других coding agents.

Он не дублирует всю архитектурную документацию. Канонические знания проекта находятся в `docs/`.

Краткий task prompt не заменяет repository design context.

---

# 1. Язык

Обязательное правило проекта:

- документация пишется на русском языке;
- комментарии в исходном коде пишутся на русском языке;
- пользовательские и исследовательские пояснения в репозитории пишутся на русском языке;
- технические идентификаторы остаются на английском: имена переменных, классов, функций, методов, протоколов, типов, модулей, package/API names и другие machine-facing identifiers;
- общепринятый технический термин допустимо оставить на английском, если перевод ухудшает точность.

---

# 2. Перед любой работой

Перед изменением production/research-кода или canonical design обязательно:

1. проверить фактический HEAD/status/diff;
2. прочитать [`docs/README.md`](docs/README.md);
3. прочитать [`docs/design/current.md`](docs/design/current.md);
4. определить тип задачи: documentation, design, implementation или research;
5. прочитать релевантный canonical design owner;
6. прочитать все релевантные accepted/non-superseded ADR;
7. прочитать релевантные candidate/exact contracts;
8. проверить границы текущего разрешённого scope;
9. только после этого вносить изменение.

Если документация не определяет значимое решение, не превращать удобный implementation choice в implicit architecture contract.

---

# 3. Иерархия source of truth

```text
accepted non-superseded ADR
+
canonical design semantics
        ↓
candidate/exact contracts
        ↓
future version specification
        ↓
implementation sequence
        ↓
implementation
        ↓
engineering/research evidence
```

Research result не меняет architecture напрямую:

```text
result
→ interpretation/design review
→ ADR/design update
→ implementation change
```

---

# 4. Три разных слоя истины

```text
Design
≠
Implementation
≠
Research evidence
```

Наличие механизма или поведенческого эффекта не является доказательством сознания, субъективного опыта или феноменальной эмоции.

---

# 5. Фундаментальные документы

Перед изменением соответствующей области обязательны:

- [`docs/design/system-context.md`](docs/design/system-context.md);
- [`docs/design/dependency-rules.md`](docs/design/dependency-rules.md);
- [`docs/design/execution-model.md`](docs/design/execution-model.md);
- [`docs/design/cognitive-state.md`](docs/design/cognitive-state.md);
- [`docs/design/module-lifecycle.md`](docs/design/module-lifecycle.md);
- [`docs/design/observability-and-intervention.md`](docs/design/observability-and-intervention.md).

Accepted foundation decisions: `ADR-0001` … `ADR-0006`.

---

# 6. Принятые subsystem boundaries

| Область | Design | Contract | ADR |
|---|---|---|---|
| Environment | `docs/design/modules/environment.md` | `docs/design/contracts/environment.md` | `ADR-0007` |
| Perception | `docs/design/modules/perception.md` | `docs/design/contracts/perception.md` | `ADR-0008` |
| Goal System | `docs/design/modules/goals.md` | `docs/design/contracts/goals.md` | `ADR-0009` |
| Cortex | `docs/design/modules/cortex.md` | `docs/design/contracts/cortex.md` | `ADR-0010` |
| Memory Core | `docs/design/modules/memory.md` | `docs/design/contracts/memory.md` | `ADR-0011` |
| World Model | `docs/design/modules/world-model.md` | `docs/design/contracts/world-model.md` | `ADR-0012` |
| Self Model | `docs/design/modules/self-model.md` | `docs/design/contracts/self-model.md` | `ADR-0013` |
| Intrinsic Signals | `docs/design/modules/intrinsic-signals.md` | `docs/design/contracts/intrinsic-signals.md` | `ADR-0014` |
| Drives | `docs/design/modules/drives.md` | `docs/design/contracts/drives.md` | `ADR-0015` |
| Appraisal | `docs/design/modules/appraisal.md` | `docs/design/contracts/appraisal.md` | `ADR-0016` |
| Affect | `docs/design/modules/affect.md` | `docs/design/contracts/affect.md` | `ADR-0017` |

Номер текущего разрешённого Design Update всегда брать из `docs/design/current.md`.

---

# 7. Общие архитектурные запреты

Без explicit design change запрещается:

- concrete peer dependency между независимыми cognitive modules;
- runtime Service Locator внутри cognition;
- shared mutable globals как межмодульный state bus;
- hidden direct mutation чужого state;
- зависимость Agent от Training/Evaluation Runtime;
- hidden evaluator/oracle input;
- скрытый behavior-changing fallback;
- ad-hoc module ordering вместо declared scheduler semantics;
- partial commit causally relevant public/private state;
- silent stale-result rebase;
- смешивание natural/replayed/imagined/intervened/counterfactual provenance;
- реализация downstream-функциональности до соответствующего DU.

---

# 8. Ключевые действующие отношения

```text
logical architecture boundary ≠ deployment topology
Cognitive Cycle ≠ Environment Transition
CognitiveState ≠ full Agent-owned state
committed state ≠ mutable shared bus
Observability ≠ Intervention
Agent Interaction Plane ≠ Environment Research Plane
Raw Observation ≠ Canonical Percept
External Task Specification ≠ Goal Proposal ≠ Committed Goal
Goal ≠ Reward ≠ Drive ≠ Utility/Value ≠ Policy
MINDRA Agent ≠ Cortex ≠ concrete LLM
MemoryRecord ≠ embedding/index entry
Memory ≠ trajectory/replay
Canonical Percept ≠ World Belief ≠ World Prediction
World Prediction ≠ observed fact
Imagined Transition ≠ Environment Transition
prediction error ≠ reward / intrinsic utility
Agent Capability Fact ≠ Learned Competence Estimate ≠ Self Prediction
Self Model ≠ Cortex self-report ≠ Executive Control
Intrinsic Signal ≠ Reward ≠ Drive ≠ Utility/Value
Drive State ≠ Drive Pressure ≠ Utility/Value
Appraisal ≠ Affect ≠ Valuation
Appraisal Target ≠ Appraisal Context
relevance ≠ Salience ≠ novelty ≠ utility
controllability ≠ coping potential
Appraisal Record ≠ Affect State
Affect State ≠ Drive State
Affect State ≠ Utility/Value/Reward
Affect State ≠ emotion label
Affect history integration ≠ Memory Store
Affect_t → Appraisal_t → Affect_(t+1)
imagined Affect ≠ real committed Affect
Environment reset ≠ Drive reset
Environment reset ≠ Affect reset
```

---

# 9. State/scheduler discipline

Запрещается:

- мутировать committed `CognitiveState` inplace;
- писать в namespace без semantic ownership;
- использовать hidden `last-write-wins`;
- публиковать peer output до commit wave;
- строить instantaneous dependency cycle;
- использовать physical completion order как causal semantics;
- оставлять causally relevant private state изменённым после rejected commit;
- менять `agent_revision` внутри in-flight wave;
- использовать wall-clock как неявное cognitive time.

---

# 10. Observability/intervention discipline

Запрещается:

- давать passive observer mutation authority;
- превращать research probe в runtime dependency;
- выполнять intervention без target/base/provenance;
- скрывать intervention как natural output;
- выдавать partial restore за exact counterfactual;
- смешивать intervened experience с natural experience без provenance.

---

# 11. Environment / Perception / Goal / Cortex safeguards

Запрещается:

- передавать Environment Research Ground Truth Agent как normal input;
- использовать evaluator metric как task feedback;
- передавать raw Environment-specific schema независимым modules;
- делать один learned latent единственным canonical percept;
- давать Cortex/Planner/Drives direct write authority Goal Graph;
- превращать Goal в scalar reward/value;
- делать model-specific prompt/tokenizer/provider API частью cognitive consumer;
- давать Cortex Gateway ambient access ко всему Agent state;
- превращать Cortex output автоматически в Goal/Memory/Action/observed fact;
- делать конкретную LLM частью canonical architecture.

---

# 12. Memory / World Model / Self Model safeguards

Запрещается:

- считать vector database или embedding канонической Memory;
- использовать hidden Memory retrieval внутри Cortex/consumer;
- смешивать Agent Memory с trajectory/replay;
- записывать imagined World Model rollout как observed trajectory;
- позволять World Model выбирать action вместо Policy/Planner;
- считать prediction error reward автоматически;
- считать Cortex self-report canonical Self Model;
- смешивать capability availability и competence;
- давать Self Model authority выбирать action/goal/compute policy.

---

# 13. Intrinsic Signals / Drives safeguards

Запрещается:

- превращать typed Intrinsic Signals в mandatory `intrinsic_reward`;
- считать высокий signal автоматически желательным;
- смешивать novelty, surprisal, prediction discrepancy и visitation rarity;
- считать replay новым natural visitation;
- превращать `DriveStateSet` в global motivation scalar;
- считать Drive Pressure готовой Utility/action score;
- требовать homeostatic set-point от каждого drive;
- давать Drive direct Goal/Policy authority;
- обновлять Drive по wall-clock/GPU/network latency.

---

# 14. Appraisal safeguards

Запрещается:

- превращать Appraisal в mandatory emotion label/global valence/reward;
- считать Appraisal persistent Affect state;
- создавать Appraisal без target/context/revision provenance;
- смешивать actual/predicted/imagined/retrospective/intervened targets;
- смешивать relevance с Salience;
- scalarize Goal conflicts внутри Appraisal;
- мутировать Goal/Drive state из Appraisal;
- смешивать controllability и coping potential;
- позволять Appraisal выбирать coping strategy/action;
- использовать evaluator-only Ground Truth как natural appraisal evidence;
- выполнять hidden Memory/Cortex operation;
- переписывать historical `AppraisalRecord` при reappraisal.

---

# 15. Affect safeguards

До explicit пересмотра `DU-17` запрещается:

- превращать canonical Affect в human emotion labels;
- требовать mandatory valence/arousal/PAD geometry;
- смешивать Affect State с Drive State или Utility/Reward;
- вычислять action/goal choice внутри Affect System;
- давать Affect direct mutation authority Goals/Drives;
- создавать same-wave recursive cycle Appraisal ↔ Affect;
- позволять Appraisal читать partially updated Affect;
- обновлять real committed Affect из любого imagined appraisal по умолчанию;
- терять provenance actual/predicted/imagined/retrospective/intervened source;
- сбрасывать Affect автоматически на `Environment.reset()`;
- обновлять Affect по wall-clock/latency скрытым background process;
- считать `0`/neutral fake state успешной заменой unavailable/failed;
- продвигать private recurrent Affect state после rejected commit;
- объявлять Affect доказательством субъективного чувства;
- считать separate Affect доказанным без `NoAffect`, temporal-history и matched recurrent controls.

---

# 16. Research discipline

Обязателен [`docs/research-methodology.md`](docs/research-methodology.md).

Для утверждений о функциональном вкладе использовать, где применимо:

- baseline;
- `No*` configuration;
- Dummy/Control implementation;
- shuffled/random control;
- parameter/compute-matched control;
- ablation;
- controlled intervention;
- несколько seeds;
- held-out world distributions;
- заранее определённый criterion.

Отрицательный результат сохраняется и может инициировать design review/ADR.

---

# 17. Scope implementation

Пока `docs/design/current.md` не разрешает implementation/version work, detailed design **не является разрешением писать production architecture**.

До соответствующих DU нельзя превращать candidates в обязательные choices, включая:

- concrete Cortex backend/model;
- concrete Memory backend/index;
- RSSM/Dreamer/Transformer world model;
- concrete Self Model estimator;
- RND/ICM/VIME и common intrinsic formula;
- concrete Drive list/equation;
- concrete Appraisal taxonomy/LLM framework;
- concrete Affect channels, valence-arousal/PAD, recurrent model или decay equation;
- TensorDict/DI/config/scheduler framework;
- PPO и другие learning algorithms;
- Colab/cloud runtime;
- конкретную структуру `src/`.

---

# 18. Поведение при неопределённости

Если документация не определяет существенное решение:

- не скрывать неопределённость;
- не создавать implicit contract;
- зафиксировать вопрос как design blocker/open question;
- предложить варианты/trade-offs, если это часть задачи;
- не реализовывать зависимую архитектуру до design decision.
