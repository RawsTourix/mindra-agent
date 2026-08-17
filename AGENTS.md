# AGENTS.md — правила работы с MINDRA

## Назначение

Этот файл — **карта обязательного контекста** для Codex, ChatGPT и других coding agents.

Он не дублирует canonical design. Source of truth находится в `docs/`.

---

# 1. Язык

- документация и комментарии в коде — на русском;
- technical identifiers, API/package/class/function/type names — на английском;
- общепринятый технический термин можно оставить на английском, если перевод ухудшает точность.

---

# 2. Перед любой работой

Обязательно:

1. проверить фактический repository status/HEAD;
2. прочитать [`docs/README.md`](docs/README.md);
3. прочитать [`docs/design/current.md`](docs/design/current.md);
4. определить scope: documentation/design/implementation/research;
5. прочитать релевантный canonical design owner;
6. прочитать действующие ADR;
7. прочитать candidate/exact contracts;
8. не выходить за разрешённый DU/version scope.

Краткий task prompt не заменяет repository context.

---

# 3. Source of truth

```text
accepted non-superseded ADR + canonical design
→ candidate/exact contracts
→ version specification
→ implementation sequence
→ implementation
→ engineering/research evidence
```

Research result меняет architecture только через interpretation/design review/ADR.

---

# 4. Фундамент

Перед subsystem changes обязательны:

- `docs/design/system-context.md`;
- `docs/design/dependency-rules.md`;
- `docs/design/execution-model.md`;
- `docs/design/cognitive-state.md`;
- `docs/design/module-lifecycle.md`;
- `docs/design/observability-and-intervention.md`.

Foundation ADR: `ADR-0001 … ADR-0006`.

---

# 5. Принятые subsystem boundaries

| Область | Design | Contract | ADR |
|---|---|---|---|
| Environment | `docs/design/modules/environment.md` | `docs/design/contracts/environment.md` | `ADR-0007` |
| Perception | `docs/design/modules/perception.md` | `docs/design/contracts/perception.md` | `ADR-0008` |
| Goals | `docs/design/modules/goals.md` | `docs/design/contracts/goals.md` | `ADR-0009` |
| Cortex | `docs/design/modules/cortex.md` | `docs/design/contracts/cortex.md` | `ADR-0010` |
| Memory Core | `docs/design/modules/memory.md` | `docs/design/contracts/memory.md` | `ADR-0011` |
| World Model | `docs/design/modules/world-model.md` | `docs/design/contracts/world-model.md` | `ADR-0012` |
| Self Model | `docs/design/modules/self-model.md` | `docs/design/contracts/self-model.md` | `ADR-0013` |
| Intrinsic Signals | `docs/design/modules/intrinsic-signals.md` | `docs/design/contracts/intrinsic-signals.md` | `ADR-0014` |
| Drives | `docs/design/modules/drives.md` | `docs/design/contracts/drives.md` | `ADR-0015` |
| Appraisal | `docs/design/modules/appraisal.md` | `docs/design/contracts/appraisal.md` | `ADR-0016` |
| Affect | `docs/design/modules/affect.md` | `docs/design/contracts/affect.md` | `ADR-0017` |
| Valuation | `docs/design/modules/valuation.md` | `docs/design/contracts/valuation.md` | `ADR-0018` |
| Salience | `docs/design/modules/salience.md` | `docs/design/contracts/salience.md` | `ADR-0019` |

Текущий разрешённый следующий DU всегда брать только из `docs/design/current.md`.

---

# 6. Общие архитектурные запреты

Без explicit design change запрещается:

- concrete peer dependency между независимыми cognitive modules;
- runtime Service Locator;
- shared mutable global state bus;
- hidden mutation чужого state;
- dependency Agent → Training/Evaluation Runtime;
- hidden evaluator/oracle input;
- hidden behavior-changing fallback;
- ad-hoc module ordering вместо declared scheduler;
- partial commit causally relevant state;
- silent stale-result rebase;
- смешение actual/replayed/imagined/intervened/counterfactual provenance;
- реализация downstream responsibility до соответствующего DU.

---

# 7. Действующие semantic distinctions

```text
Cognitive Cycle ≠ Environment Transition
CognitiveState ≠ full Agent Snapshot
Observability ≠ Intervention
Raw Observation ≠ Canonical Percept
Goal Proposal ≠ Committed Goal
Goal ≠ Reward ≠ Drive ≠ Value ≠ Policy
MINDRA Agent ≠ Cortex ≠ concrete LLM
MemoryRecord ≠ embedding/index
Memory ≠ trajectory/training replay
Canonical Percept ≠ World Belief ≠ World Prediction
World Prediction ≠ observed fact
Intrinsic Signal ≠ Reward/Drive/Value
Drive State ≠ Drive Pressure ≠ Value
Appraisal ≠ Affect ≠ Valuation
Appraisal relevance ≠ Salience
Affect State ≠ Drive State ≠ Value
ValueProfile ≠ ScalarizedValue ≠ Training Reward ≠ Critic Value ≠ Policy Decision
predictive uncertainty ≠ risk
SalienceProfile ≠ AttentionAllocation
AttentionAllocation ≠ Workspace admission
AttentionAllocation ≠ Executive compute decision
AttentionAllocation ≠ Policy decision
Cortex attention weight ≠ MINDRA Salience
Memory retrieval score ≠ Salience
```

---

# 8. State / scheduler discipline

Запрещается:

- inplace mutation committed state;
- write без semantic ownership;
- hidden `last-write-wins`;
- publication до wave commit;
- instantaneous dependency cycles;
- physical completion order как causal order;
- private-state advancement после rejected commit;
- `agent_revision` change внутри in-flight wave;
- wall-clock как implicit cognitive time.

---

# 9. Observability / intervention

Запрещается:

- observer mutation authority;
- research probe как runtime dependency;
- intervention без target/base/provenance;
- скрывать intervention как natural output;
- выдавать partial restore за exact counterfactual;
- смешивать intervention data с natural experience без provenance.

---

# 10. Subsystem safeguards

## Environment / Perception / Goals / Cortex

Запрещается:

- Ground Truth → Agent normal input;
- evaluator metric как feedback;
- raw Environment-specific schema → independent cognitive modules;
- один latent как universal Canonical Percept;
- direct Goal Graph mutation от Cortex/Planner/Drives;
- model-specific tokenizer/prompt/provider logic в cognitive consumers;
- ambient Agent-state access Cortex;
- concrete LLM как canonical architecture.

## Memory / World / Self

Запрещается:

- vector DB/embedding как canonical Memory;
- hidden Memory retrieval;
- Memory = trajectory/replay;
- imagined rollout как observed trajectory;
- World Model action selection;
- prediction error как automatic reward;
- Cortex self-report как canonical Self Model;
- Self Model action/goal/compute authority.

## Intrinsic Signals / Drives

Запрещается:

- mandatory `intrinsic_reward`;
- высокий signal = автоматически desirable;
- novelty/surprisal/error/rarity как синонимы;
- replay = natural visitation;
- `DriveStateSet` = global motivation scalar;
- Drive Pressure = Utility;
- mandatory homeostatic set-point для каждого Drive;
- direct Drive → Goal/Policy mutation.

## Appraisal / Affect

Запрещается:

- Appraisal как emotion classifier/global utility;
- relevance = Salience;
- Appraisal action selection;
- Affect как mandatory human emotion labels/VA/PAD;
- same-wave recursive Appraisal ↔ Affect;
- real Affect update из imagination по умолчанию;
- Affect = Utility/Reward;
- объявлять Affect доказательством subjective experience.

## Valuation

Запрещается:

- mandatory universal scalar;
- hidden fixed weighted sum;
- потеря per-Goal/per-Drive conflicts до explicit comparison;
- hard constraint → arbitrary huge reward penalty без policy;
- novelty/feedback/Appraisal/Affect/Drive/Self confidence как automatic utility;
- uncertainty = risk;
- imagined value = experienced value;
- RL critic/reward = canonical Valuation автоматически;
- Valuation → final Action Commit;
- `incomparable` как technical error.

## Salience

До explicit пересмотра `DU-19` запрещается:

- global timeless `target.salience` как universal property;
- ambient scan всего Agent state/Memory;
- mandatory scalar salience;
- hidden weighted sum evidence без versioned policy;
- считать novelty/relevance/value/risk готовой Salience автоматически;
- сравнивать scores между разными purpose/policy revisions как одну валюту;
- Salience-owned global compute budget;
- hidden Memory retrieval/retention;
- Workspace admission внутри Salience;
- Cortex invocation/planning-depth/Cognitive-Cycle decisions внутри Salience;
- scheduler graph mutation из Salience;
- action selection через salience score;
- Transformer/Cortex attention weights как canonical Salience;
- failure/unavailable заменять `salience=0`;
- imagined allocation автоматически применять к real processing;
- считать логируемый score функциональной Salience без downstream allocation effect.

---

# 11. Research discipline

Для causal claims применять, где возможно:

- baseline / `No*`;
- Dummy/control;
- random/shuffled/constant;
- parameter/compute/state-matched controls;
- ablation;
- controlled intervention;
- multiple seeds;
- held-out distributions;
- заранее определённый success/falsification criterion.

Для Salience обязательно проверять:

```text
correct allocation
vs uniform/random/shuffled/source-only/matched control
```

и цепочку:

```text
intervention
→ changed allocation
→ changed actual processing
→ measurable effect
```

---

# 12. Scope implementation

Пока `docs/design/current.md` не разрешает version/implementation work, detailed design **не является разрешением писать production architecture**.

Не превращать research candidates в mandatory choices: concrete models, frameworks, neural routers, memory indexes, world-model families, intrinsic algorithms, drive equations, appraisal/affect taxonomies, valuation scalarization/risk policy, salience formula/top-K/router и т. п.

Если значимое решение не определено — зафиксировать uncertainty/design blocker, а не создавать implicit contract.
