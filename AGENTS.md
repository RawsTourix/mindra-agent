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
- технические идентификаторы остаются на английском: имена переменных, классов, функций, методов, протоколов, типов, модулей, package names, API names и другие machine-facing identifiers;
- общепринятый технический термин допустимо оставить на английском, если перевод ухудшает точность или создаёт двусмысленность.

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

При противоречии experimental result и design:

```text
result
→ interpretation/design review
→ ADR/design update
→ только затем implementation change
```

Нельзя молча менять архитектуру по одному результату эксперимента.

---

# 4. Три разных слоя истины

Всегда разделять:

```text
Design
≠
Implementation
≠
Research evidence
```

Наличие реализации не является подтверждением исследовательской гипотезы.

Поведенческий результат не является доказательством сознания, субъективного опыта или феноменальных эмоций.

---

# 5. Фундаментальные документы

Перед изменением соответствующей области обязательны:

- [`docs/design/system-context.md`](docs/design/system-context.md) — logical boundaries;
- [`docs/design/dependency-rules.md`](docs/design/dependency-rules.md) — dependencies/composition;
- [`docs/design/execution-model.md`](docs/design/execution-model.md) — temporal/causal model;
- [`docs/design/cognitive-state.md`](docs/design/cognitive-state.md) — committed state semantics;
- [`docs/design/module-lifecycle.md`](docs/design/module-lifecycle.md) — scheduler/module lifecycle;
- [`docs/design/observability-and-intervention.md`](docs/design/observability-and-intervention.md) — evidence/intervention.

Accepted foundation decisions: `ADR-0001` … `ADR-0006`.

---

# 6. Принятые subsystem boundaries

Для subsystem-specific работы читать соответствующий design + contract + ADR:

| Область | Design | Contract | ADR |
|---|---|---|---|
| Environment | `docs/design/modules/environment.md` | `contracts/environment.md` | `ADR-0007` |
| Perception | `docs/design/modules/perception.md` | `contracts/perception.md` | `ADR-0008` |
| Goal System | `docs/design/modules/goals.md` | `contracts/goals.md` | `ADR-0009` |
| Cortex | `docs/design/modules/cortex.md` | `contracts/cortex.md` | `ADR-0010` |
| Memory Core | `docs/design/modules/memory.md` | `contracts/memory.md` | `ADR-0011` |
| World Model | `docs/design/modules/world-model.md` | `contracts/world-model.md` | `ADR-0012` |

Номер текущего разрешённого Design Update всегда брать из `docs/design/current.md`, а не из старых chat/prompt сообщений.

---

# 7. Общие архитектурные запреты

Без explicit design change запрещается:

- concrete peer dependency между независимыми cognitive modules;
- runtime Service Locator внутри cognition/runtime code;
- shared mutable globals как межмодульный state bus;
- hidden direct mutation чужого state;
- зависимость Agent от Training/Evaluation Runtime;
- скрытый evaluator/oracle input;
- hidden behavior-changing fallback;
- ad-hoc module ordering вместо declared scheduler semantics;
- partial commit causally relevant public/private state;
- silent stale-result rebase;
- смешивание natural/replayed/imagined/intervened/counterfactual provenance;
- реализация downstream-функциональности «заодно» до соответствующего DU.

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
Canonical Percept ≠ hidden world belief
External Task Specification ≠ Goal Proposal ≠ Committed Goal
Goal ≠ Reward ≠ Drive ≠ Utility/Value ≠ Policy
MINDRA Agent ≠ Cortex ≠ concrete LLM
MemoryRecord ≠ embedding/index entry
Memory ≠ trajectory/replay
Memory retrieval ≠ ambient Cortex context
Canonical Percept ≠ World Belief ≠ World Prediction
World Prediction ≠ observed fact
Imagined Transition ≠ Environment Transition
prediction error ≠ reward / intrinsic utility
predictive uncertainty ≠ risk / value
```

---

# 9. State/scheduler discipline

До изменения `DU-03…05` запрещается:

- мутировать committed `CognitiveState` inplace;
- писать в namespace без semantic ownership;
- использовать hidden `last-write-wins`;
- публиковать peer output до commit текущей wave;
- строить instantaneous dependency cycle;
- использовать physical completion order как causal semantics;
- оставлять causally relevant private state изменённым после rejected commit;
- менять `agent_revision` внутри in-flight wave;
- использовать wall-clock как неявное cognitive time.

---

# 10. Observability/intervention discipline

До изменения `DU-06` запрещается:

- давать passive observer mutation authority;
- превращать research probe в runtime dependency;
- выполнять intervention без target/base/provenance;
- скрывать intervention как natural output;
- выдавать partial restore за exact counterfactual;
- считать raw activation access обязательной capability всех backends;
- смешивать intervened experience с natural experience без provenance.

---

# 11. Environment/Perception discipline

До изменения `DU-07/08` запрещается:

- передавать Environment Research Ground Truth Agent как normal input;
- использовать evaluator metric как task feedback;
- считать seed полным world identity;
- считать `MicroWorld` universal internal representation;
- передавать raw Environment-specific schema независимым modules;
- делать один learned latent единственным canonical percept;
- использовать hidden persistent object ID как бесплатную percept identity;
- смешивать direct observation, perceptual inference, Memory и World Model prediction;
- молча смешивать несовместимые feature-space revisions.

---

# 12. Goal/Cortex discipline

До изменения `DU-09/10` запрещается:

- давать Cortex/Planner/Drives direct write authority Goal Graph;
- хранить authoritative Goal только в Policy/Cortex hidden state;
- превращать Goal в scalar reward/value;
- делать model-specific prompt/tokenizer/provider API частью cognitive consumer;
- давать Cortex Gateway ambient access ко всему Agent state;
- превращать Cortex output автоматически в Goal/Memory/Action/observed fact;
- требовать hidden states/CoT/gradients от любого Cortex backend;
- скрывать context truncation/model fallback/provider substitution;
- делать конкретную LLM частью canonical architecture.

---

# 13. Memory discipline

До изменения `DU-11/19/20` запрещается:

- считать vector database или embedding каноническим Memory Store;
- использовать index slot/row/object id как `memory_id`;
- молча переписывать source payload старого MemoryRecord;
- смешивать несовместимые representation revisions;
- давать consumer direct write authority Memory Store;
- выполнять hidden Memory retrieval внутри Cortex Gateway/другого consumer;
- считать retrieval score utility/salience/importance/truth probability;
- смешивать Agent Memory с trajectory log или training replay;
- добавлять salience/emotional forgetting до соответствующих DU;
- называть `NoMemory` implementation, возвращающую fake successful retrieval.

---

# 14. World Model discipline

До изменения `DU-12` запрещается:

- использовать Environment hidden ground truth как normal World Model belief/input;
- считать текущий `Canonical Percept` полным World Belief при partial observability без explicit baseline semantics;
- превращать backend latent в universal inter-module representation;
- считать action prediction фактом выбора/commit действия;
- записывать imagined rollout как observed Environment trajectory;
- делать imagined state natural MemoryRecord автоматически;
- позволять World Model выбирать preferred action вместо Policy/Planner;
- смешивать world dynamics с Goal/Valuation;
- считать prediction error reward/intrinsic utility автоматически;
- называть arbitrary variance `epistemic`/`aleatoric` без estimator/evaluation semantics;
- выполнять hidden Memory lookup или hidden Cortex call без declared causal operation;
- обучать baseline на evaluator-only oracle state и описывать это как agent-experience-only learning;
- использовать один `None`/zero-vector для разных failure/uncertainty states;
- фиксировать RSSM/Dreamer/Transformer/TorchRL обязательными из-за research evidence.

---

# 15. Research discipline

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

Не подбирать success criterion после просмотра результата без явной post-hoc маркировки.

---

# 16. Scope implementation

Пока `docs/design/current.md` не разрешает implementation/version work, подробный design **не является разрешением писать production architecture**.

До соответствующих Design Updates нельзя превращать обсуждавшиеся candidates в обязательные choices, включая:

- конкретный Cortex backend/model size;
- конкретный Memory backend/index/embedding model;
- RSSM/Dreamer/TD-MPC/Transformer world model;
- TensorDict/DI/config/scheduler framework;
- PPO/RND/ICM и другие learning algorithms;
- Colab/cloud runtime;
- конкретную структуру `src/`.

---

# 17. Поведение при неопределённости

Если документация не определяет существенное решение:

- не скрывать неопределённость;
- не создавать implicit contract;
- зафиксировать вопрос как design blocker/open question;
- предложить варианты/trade-offs, если это часть задачи;
- не реализовывать зависимую архитектуру до design decision.

Мелкие локальные implementation details могут выбираться самостоятельно только если они не меняют contracts, research validity и принятые boundaries.
