# План проектирования документации MINDRA

## Статус документа

Этот документ задаёт порядок дальнейшего проектирования MINDRA.

Он не является version roadmap и не определяет implementation milestones. Его задача — указать, какие design topics должны быть последовательно проработаны до начала серьёзной реализации.

Главный принцип:

```text
общие invariants
→ system/state boundaries
→ module semantics
→ training/data lifecycle
→ evaluation/reproducibility
→ exact internal contracts
→ unresolved ADR
→ version roadmap
→ implementation sequences
```

Version roadmap должен выводиться из уже достаточно сформированной архитектуры, а не использоваться для преждевременного разбиения неизвестной системы.

---

# 1. Foundation — выполнено частично

Базовый documentation foundation включает:

- `project-concept.md`;
- `architecture-concept.md`;
- `research-methodology.md`;
- `design/principles.md`;
- `design/glossary.md`;
- `design/current.md`;
- registry для ADR/contracts/versions;
- repository `AGENTS.md`.

Этот этап фиксирует язык и правила работы, но не определяет точную реализацию.

---

# 2. System context

Следующий design topic должен определить MINDRA как систему в окружении внешних компонентов.

Необходимо описать:

- Environment;
- Agent boundary;
- Cortex boundary;
- training/evaluation runtime;
- artifact/checkpoint storage;
- experiment runner;
- границу между online execution и offline training/consolidation;
- роль локальной машины, Colab/remote compute и external model storage без преждевременного выбора одного обязательного провайдера.

Результат: `system-context.md`.

---

# 3. Dependency rules

После system context необходимо определить допустимые зависимости между основными слоями и модулями.

Вопросы:

- могут ли modules напрямую импортировать друг друга;
- как выглядит composition root;
- где живут shared contracts;
- как изолируется Cortex-specific code;
- как evaluation получает observability без проникновения в private implementation;
- как training code взаимодействует с runtime modules.

Результат: `dependency-rules.md`.

---

# 4. Canonical cognitive state

Один из центральных design topics.

Необходимо определить semantic model внутреннего состояния:

- какие категории state существуют;
- что является persistent/ephemeral;
- кто владеет каждым фрагментом;
- кто может читать/писать;
- как выражается absence/unknown/stale;
- как state сериализуется для experiment replay/checkpoint;
- какие данные запрещено протаскивать напрямую из конкретного Cortex backend.

На этом этапе нужно сначала определить семантику, а затем рассмотреть candidate frameworks.

Результаты могут включать:

- `cognitive-state.md`;
- ADR по representation/framework;
- позднее exact contract в `contracts/`.

---

# 5. Module lifecycle и scheduling

Нужно определить общий жизненный цикл когнитивного модуля.

Как минимум рассмотреть:

```text
initialize
reset episode
read state
compute/update state
observe outcome
learn/update weights
checkpoint
restore
shutdown
```

Нужно решить:

- синхронный или graph/scheduler-based execution;
- порядок зависимостей;
- как предотвращать cyclic hidden coupling;
- какие шаги выполняются каждый environment tick;
- какие — только при training/consolidation;
- как работает disabled/no-op module.

Результат: `module-lifecycle.md` + при необходимости ADR.

---

# 6. Cortex design

Только после state/lifecycle boundary стоит проектировать Cortex integration.

Нужно отдельно исследовать:

- open-weight model candidates;
- hidden-state access;
- multilingual quality;
- resource requirements;
- frozen vs adapter tuning;
- soft/latent bridge;
- text-only fallback;
- dummy/no-Cortex modes;
- transfer между backbone;
- canonical representation adapter.

Не фиксировать конкретную Qwen/Gemma/Llama только из предыдущего обсуждения без свежего сравнения.

Результат: `modules/cortex.md`, ADR и exact Cortex contract.

---

# 7. Environment / MicroWorld design

До сложного обучения необходимо спроектировать контролируемую среду, позволяющую проверять причинные гипотезы.

Нужно определить:

- observation/action spaces;
- deterministic replay;
- procedural generation;
- hidden rules;
- train/test world split;
- task families;
- controlled interventions;
- counterfactual cloning;
- environment versioning.

Результат: `modules/environment.md` + exact environment contract.

---

# 8. World Model

Исследовать candidate architectures и выбрать минимально достаточную baseline-реализацию.

Design должен определить:

- prediction target;
- uncertainty semantics;
- multi-step rollout;
- interaction with state/policy;
- training data;
- losses;
- evaluation;
- no-op/control implementation.

Результат: `modules/world-model.md`.

---

# 9. Self Model

Определить, что именно система должна моделировать о себе и как проверить calibration.

Не превращать Self Model в текстовый personality profile.

Результат: `modules/self-model.md`.

---

# 10. Drives / intrinsic signals

Требуется отдельное исследование биологических аналогий и существующих ML-подходов, но canonical design должен оставаться функциональным.

Нужно развести:

- drives;
- intrinsic signals;
- reward;
- utility;
- goals.

Результат: `modules/drives.md` и, возможно, ADR по value representation.

---

# 11. Appraisal

Определить semantic inputs/outputs, способ обучения и causal evaluation.

Особенно важно избежать ситуации, когда Appraisal является просто вторым именем для reward model.

Результат: `modules/appraisal.md`.

---

# 12. Salience

Определить, какие downstream-механизмы Salience реально регулирует и как измеряется её future utility.

Результат: `modules/salience.md`.

---

# 13. Memory / consolidation

Нужно отдельно спроектировать:

- working state;
- episodic storage;
- retrieval;
- retention/forgetting;
- replay;
- consolidation;
- provenance;
- capacity limits;
- shuffled/no-memory controls.

Выбор FAISS/vector DB/другого backend должен следовать semantic requirements.

Результат: `modules/memory.md` + data/replay design.

---

# 14. Workspace / integration

Определить:

- зачем нужен отдельный Workspace сверх общего state bus;
- limited capacity;
- competition/gating;
- consumers;
- intervention strategy;
- no-workspace baseline.

Если отдельный Workspace не добавляет функционально различимую роль, он не должен сохраняться только из-за когнитивной аналогии.

Результат: `modules/workspace.md`.

---

# 15. Policy / Planner

Определить action-selection boundary и взаимодействие с Cortex/World Model/Drives/Appraisal.

Необходимо сравнить candidate RL/planning approaches после фиксации environment и signal semantics.

Результат: `modules/policy.md`.

---

# 16. Training lifecycle

После module semantics проектируется общая training architecture.

Нужно определить:

- какие модули frozen/trainable;
- pretraining отдельных компонентов;
- online learning;
- replay;
- joint training;
- consolidation;
- optimizer/checkpoint boundaries;
- Cortex adaptation;
- catastrophic forgetting controls;
- stopping/resume semantics.

Результат: `training.md`.

---

# 17. Data and replay

Отдельный документ должен определить:

- trajectory schema;
- generated experience;
- human/synthetic annotations, если они нужны;
- leakage prevention;
- replay sampling;
- dataset versioning;
- storage/retention;
- train/eval split.

Результат: `data-and-replay.md`.

---

# 18. Checkpointing / reproducibility

Нужно определить versioned checkpoint composition и experiment identity.

Результаты:

- `checkpointing.md`;
- `reproducibility.md`;
- exact contracts для checkpoint/experiment record.

---

# 19. Evaluation design

После появления module semantics нужно превратить `research-methodology.md` в точный evaluation harness.

Нужно определить:

- baseline matrix;
- ablation matrix;
- causal intervention metrics;
- transfer tests;
- generalization tests;
- module-specific metrics;
- statistical policy;
- compute-aware minimum evidence;
- acceptance of negative result.

Результат: `evaluation.md`.

---

# 20. Testing

Engineering testing проектируется отдельно от research evaluation.

Нужно определить:

- unit;
- contract;
- architecture/dependency;
- integration;
- deterministic replay;
- checkpoint roundtrip;
- CPU/GPU compatibility;
- failure recovery;
- smoke/full experiment profiles.

Результат: `testing.md`.

---

# 21. Research claims / limitations

До публикации серьёзных результатов нужно создать документы, ограничивающие допустимую интерпретацию.

Результаты:

- `research-claims.md`;
- `limitations.md`.

---

# 22. Exact internal contracts

После semantic design соответствующих областей создаются machine-facing contracts.

Нельзя проектировать exact interface раньше, чем понятна его семантика, если только ранний prototype contract явно не помечен experimental/non-canonical.

---

# 23. ADR consistency pass

Перед roadmap необходимо проверить unresolved major choices и оформить значимые решения через ADR.

---

# 24. Version roadmap

Только после предыдущих этапов архитектура разбивается на implementation milestones.

Roadmap должен учитывать:

- dependency graph;
- минимально проверяемые вертикальные slices;
- compute constraints;
- необходимость baseline до сложных модулей;
- acceptance/evaluation gates;
- отсутствие заведомого rewrite shortcut.

---

# 25. Version implementation sequences

Для каждой версии создаётся patch-oriented последовательность, пригодная как прямой источник задач Codex.

Каждый patch должен содержать как минимум:

- цель;
- prerequisites;
- canonical docs;
- scope;
- forbidden scope;
- implementation requirements;
- required tests/evaluation;
- acceptance criteria;
- documentation updates.

---

# 26. Текущий следующий шаг

После принятия documentation foundation следует начинать с **system context**, затем dependency rules и canonical cognitive state.

Это не означает автоматического начала реализации.
