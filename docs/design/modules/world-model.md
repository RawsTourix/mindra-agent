# World Model MINDRA

## Статус документа

**Design Update:** `DU-12 — World Model`  
**Статус:** accepted  
**Канонический владелец темы:** этот документ

Этот документ определяет предсказательную модель внешнего мира MINDRA при частичной наблюдаемости.

Документ определяет:

- responsibility и ownership `World Model`;
- `World Belief` как состояние оценки внешнего мира при partial observability;
- различие assimilation/posterior update и action-conditioned prior/prediction;
- one-step prediction и multi-step imagination;
- structured и learned prediction views;
- observed/predicted/imagined provenance;
- stochastic dynamics и uncertainty semantics;
- prediction error/surprise boundary;
- использование Memory без ambient retrieval;
- связь с Cortex без превращения Cortex в source of truth;
- model/belief revisioning;
- snapshot/restore/counterfactual requirements;
- `NoWorldModel`/Dummy/Control configurations;
- observability/intervention/failure semantics.

Документ опирается на:

- [`../execution-model.md`](../execution-model.md) — observed/replayed/imagined transitions и causal time различаются;
- [`../cognitive-state.md`](../cognitive-state.md) — committed state/provenance/private-state semantics;
- [`../module-lifecycle.md`](../module-lifecycle.md) — staged public/private effects и wave commit;
- [`../observability-and-intervention.md`](../observability-and-intervention.md) — passive evidence и explicit interventions;
- [`environment.md`](environment.md) — hidden world state не является normal Agent input;
- [`perception.md`](perception.md) — `Canonical Percept` описывает текущее observation, а не belief/prediction;
- [`goals.md`](goals.md) — Goal state не является world dynamics;
- [`cortex.md`](cortex.md) — Cortex является optional semantic capability, а не authoritative world model;
- [`memory.md`](memory.md) — Memory retrieval является explicit causal operation и не равна текущему world belief.

Документ намеренно **не** определяет:

- конкретную neural architecture: RSSM, GRU/LSTM, Transformer, SSM, diffusion или другую;
- Dreamer/PlaNet/TD-MPC/IRIS как обязательный algorithm;
- exact latent size/distribution;
- exact training losses — `DU-26`;
- intrinsic reward/curiosity — `DU-14`;
- Self Model — `DU-13`;
- Valuation/Policy/Planner — `DU-18/23`;
- concrete action schema — `DU-24`;
- exact trajectory/replay contract — `DU-25`;
- exact Python API/checkpoint format — `DU-27`.

---

# 1. Цель DU-12

MINDRA должна уметь отвечать не только на вопрос:

> «Что я наблюдаю сейчас?»

но и на вопросы:

> «Каково наиболее правдоподобное состояние внешнего мира с учётом прошлых наблюдений?»

> «Что, вероятно, произойдёт после действия X?»

> «Какие несколько вариантов будущего возможны?»

> «Насколько мой прогноз надёжен?»

При этом World Model не должна становиться:

- скрытой копией `Environment Research Ground Truth`;
- Memory;
- Policy/Planner;
- Utility/Reward Model;
- Self Model;
- Cortex prompt с красивым названием;
- источником observed facts без реального Outcome Commit.

Канонические отношения:

```text
Canonical Percept
≠
World Belief
≠
World Prediction
≠
Imagined Trajectory
≠
Hidden World State
```

и:

```text
prediction quality
≠
desirability / value
```

---

# 2. Главное архитектурное решение

MINDRA принимает **belief-state World Model с раздельными assimilation, prediction и imagination semantics и гибридной prediction surface**.

Conceptually:

```text
previous World Belief
       +
actual Canonical Percept / Outcome
       ↓
Assimilation / Posterior Update
       ↓
Committed World Belief B_t
       │
       ├── + candidate action a_t
       │          ↓
       │    Transition / Prior
       │          ↓
       │    World Prediction P_{t+1}
       │
       └── + action sequence / branching query
                  ↓
             Imagination Rollout
                  ↓
          Predicted Belief B'_{t+k}
          + predicted outcomes
```

`World Belief` не обязан быть полностью интерпретируемым symbolic map. Реализация может иметь causally relevant private latent/recurrent state.

Но backend-specific latent **не становится универсальным межмодульным representation contract**.

Наружу World Model публикует stable semantic prediction/result surfaces с revision/provenance, а raw latent доступен только через declared feature/research capability.

Решение дополнительно фиксируется в `ADR-0012`.

---

# 3. Responsibility и ownership

## 3.1. World Model является agent-owned cognitive subsystem

World Model логически принадлежит Agent.

Он владеет:

- текущим `World Belief`/belief revision;
- causally relevant private recurrent/latent state, если implementation его использует;
- собственными model parameters/adapters;
- prediction heads/representations;
- model-specific uncertainty state;
- world-model-specific research probes.

## 3.2. World Model отвечает за

- assimilation фактически полученного percept/outcome;
- temporal integration наблюдений при partial observability;
- action-conditioned prediction внешней динамики;
- multi-step imagined rollout;
- prediction provenance;
- explicit uncertainty output, если capability поддерживается;
- post-outcome prediction error/surprise evidence;
- world-model-specific snapshot/restore state.

## 3.3. World Model не отвечает за

- выбор действия;
- выбор цели;
- оценку желательности состояния;
- определение internal reward/utility;
- Memory retention;
- оценку собственной компетентности Agent;
- hidden access к evaluator/Environment oracle;
- объявление prediction observed fact до реального outcome.

---

# 4. World Belief

## 4.1. Зачем нужен belief

При partial observability текущий `Canonical Percept` не содержит полного состояния внешнего мира.

Поэтому World Model поддерживает **belief** — внутреннюю оценку внешней ситуации, построенную из причинно доступной информации.

Conceptually:

```text
B_t = update(B_{t-1}, a_{t-1}, percept_t, allowed context)
```

Это не утверждение о конкретной Bayesian implementation.

## 4.2. World Belief не является Hidden World State

Даже если в MicroWorld evaluator знает точную скрытую карту:

```text
Environment Hidden World State
≠
World Belief
```

Belief может:

- быть неполным;
- быть неопределённым;
- содержать ошибочные гипотезы;
- расходиться с ground truth;
- исправляться после новых наблюдений.

Именно это является исследовательски полезным.

## 4.3. Public и private части belief

Implementation может содержать private representation, например:

```text
recurrent hidden state
stochastic latent state
transformer history/cache
particle set
ensemble state
```

Но независимые modules не получают право читать её напрямую.

Canonical boundary должна позволять публиковать lightweight `WorldBeliefSummary`/descriptor, например:

- `belief_revision`;
- source causal identities;
- model revision;
- availability/status;
- optional structured hypotheses;
- optional versioned feature view;
- uncertainty summary, если поддерживается.

Exact поля не frozen.

## 4.4. Belief revision

`belief_revision` отличается от:

```text
state_revision
agent_revision
memory_revision
world_model_revision
feature_space_revision
```

Новый фактический percept/outcome, изменивший belief, создаёт новую committed belief revision.

Чистый query к уже committed belief не обязан менять belief revision.

---

# 5. Assimilation / Posterior Update

World Model обязана различать обновление по **реально полученному** evidence и предсказание без него.

Conceptually:

```text
prior belief B^-_t
+
actual Canonical Percept O_t
+
actual agent-visible outcome signals
↓
posterior / assimilated belief B_t
```

Термины `prior/posterior` здесь описывают causal semantics и не требуют конкретного variational/Bayesian algorithm.

Assimilation должна сохранять provenance:

```text
observed evidence
≠
Memory-retrieved context
≠
Cortex interpretation
≠
research intervention
```

---

# 6. Action-conditioned Transition / Prior

World Model предоставляет prediction capability вида:

```text
World Belief B_t
+
Candidate Action A
↓
World Prediction
```

`Candidate Action` пока является semantic placeholder до `DU-24`.

Ключевой invariant:

> Запрос прогноза действия не означает выбор или commit этого действия.

Можно запросить несколько альтернатив:

```text
B_t
├── action A → prediction P_A
├── action B → prediction P_B
└── action C → prediction P_C
```

World Model не решает, какой branch предпочтительнее.

---

# 7. Hybrid Prediction Surface

MINDRA не требует, чтобы World Model всегда реконструировала весь следующий Raw Observation/пиксели.

Также не принимается один opaque latent как единственная externally meaningful prediction surface.

World Prediction должна поддерживать гибридную модель:

```text
WorldPrediction
├── envelope/provenance
├── predicted observable/semantic outcomes?
├── predicted task-visible external signals?
├── predicted termination semantics?
├── optional structured state hypotheses
├── optional feature/latent views
├── uncertainty
└── horizon/depth metadata
```

Exact components зависят от implementation/capability.

## 7.1. Structured prediction

Для MicroWorld полезно уметь предсказывать agent-relevant semantic outcomes, например:

- изменение наблюдаемого положения;
- открытие/закрытие двери;
- появление/исчезновение объекта из доступной observation;
- agent-visible effect действия;
- `terminated`, если termination является частью Environment dynamics/task semantics.

## 7.2. Learned prediction view

World Model может использовать или публиковать versioned latent/feature prediction.

Он обязан иметь:

```text
feature_space_id
feature_space_revision
world_model_revision
source belief/action identity
```

если representation пересекает module boundary.

## 7.3. Truncation не является обычной world-dynamics целью

`truncated` обычно возникает из внешнего horizon/runtime limit.

World Model не должна притворяться, что truncation является естественным состоянием мира, если Environment contract явно не делает time-limit agent-visible dynamics.

---

# 8. Multi-step Imagination

World Model поддерживает возможность прогнозирования нескольких шагов без реального Environment transition.

Conceptually:

```text
Base Belief B0
   ↓ action a0
Predicted Belief B1'
   ↓ action a1
Predicted Belief B2'
   ↓ action a2
Predicted Belief B3'
```

Каждый такой state имеет provenance:

```text
imagined
```

а не:

```text
observed
```

## 8.1. Imagination не коммитит reality

Imagined rollout:

- не увеличивает Environment transition counter;
- не меняет canonical observed history;
- не становится MemoryRecord автоматически;
- не становится natural trajectory автоматически;
- не изменяет committed World Belief, если query contract явно не предусматривает отдельный owner-authorized transition;
- не выбирает action за Planner/Policy.

## 8.2. Rollout identity

Rollout evidence должна различать минимум:

```text
rollout_id
base belief revision
world_model_revision
branch/action sequence
horizon/depth
stochastic sample/seed semantics
intervention provenance
```

## 8.3. Horizon ограничен

Нельзя считать arbitrarily long rollout достоверным по умолчанию.

Contract должен позволять:

- maximum supported horizon;
- truncation of imagination;
- uncertainty growth;
- accumulated model error/degradation;
- explicit status, если дальнейший rollout ненадёжен или не поддерживается.

---

# 9. Partial observability и Memory

World Model может использовать историю только через разрешённые causal boundaries.

Допустимо:

```text
current percept
+
previous World Belief
+
explicit RetrievalResult
→ belief update / query
```

Запрещено:

```text
World Model
→ hidden Memory scan
→ сама нашла прошлое
→ нигде не зафиксировала retrieval
```

Memory и World Belief различаются:

```text
Memory
→ отдельные прошлые records

World Belief
→ текущая интегрированная оценка внешнего мира
```

MemoryRecord не обязан автоматически обновлять belief только из-за существования в Store.

---

# 10. World Model и Cortex

Cortex может быть optional capability внутри конкретной World Model implementation или отдельного semantic reasoning step.

Например:

- interpretation сложного natural-language rule;
- semantic hypothesis generation;
- structured outcome candidate generation.

Но:

```text
Cortex statement
≠
observed world fact
```

и:

```text
Cortex
≠
World Model owner
```

Любой Cortex invocation остаётся explicit/traceable по `DU-10`.

`NoCortex` World Model должна оставаться допустимой configuration, если выбранная implementation не требует Cortex как explicit capability.

---

# 11. Goal neutrality

Базовая transition semantics World Model должна описывать:

> что произойдёт при action,

а не:

> насколько это полезно для текущей цели.

Поэтому Goal не является обязательным causal input world dynamics.

Goal может использоваться consumer'ом для:

- выбора action candidates;
- запроса конкретной projection prediction;
- фокусировки downstream Planner;

но изменение Goal при неизменных belief/action не должно скрыто менять физический prediction только потому, что состояние стало «желательнее».

Goal-conditioned model variants возможны как отдельные experiment/configurations, но не смешивают dynamics с Valuation.

---

# 12. Self Model boundary

World Model моделирует **внешнюю динамику**, включая agent-visible embodiment/world-side consequences actions.

Будущий Self Model отвечает за функциональные свойства самого Agent, например:

- собственную компетентность;
- вероятность успешного выполнения внутренне сложного действия;
- resource/compute capability;
- calibration собственного знания.

Следовательно:

```text
World prediction of door physics
≠
Self prediction of "смогу ли я правильно выполнить сложную процедуру"
```

Граница уточняется в `DU-13`.

---

# 13. Stochastic Dynamics

World Model не обязана быть deterministic.

Contract должна допускать:

```text
point prediction
probabilistic prediction
sampled futures
ensemble predictions
mixture/multimodal outcomes
```

Если мир имеет несколько возможных исходов, forcing одного average outcome может быть неадекватным.

При stochastic rollout evidence должна сохранять sampling semantics настолько, насколько это нужно reproducibility.

---

# 14. Uncertainty Semantics

## 14.1. Predictive uncertainty

Базовый общий термин:

```text
predictive uncertainty
```

допустим, если конкретный estimator имеет определённую semantics.

## 14.2. Epistemic vs aleatoric

MINDRA не разрешает автоматически подписывать любое число как:

```text
epistemic uncertainty
```

или:

```text
aleatoric uncertainty
```

только потому, что implementation имеет variance/ensemble disagreement.

Разделение допускается только если:

- estimator design обосновывает интерпретацию;
- training data/assumptions совместимы;
- evaluation отдельно проверяет ожидаемые свойства.

Иначе capability публикует generic predictive uncertainty либо `unknown/unavailable` decomposition.

## 14.3. Uncertainty не равна risk/value

```text
uncertainty
≠
risk
≠
negative valence
≠
low utility
```

Оценка последствия появляется в downstream modules.

---

# 15. Prediction Error и Surprise

После фактического `Outcome Commit` World Model может сопоставить ранее зарегистрированный prediction с реальным agent-visible outcome.

Conceptually:

```text
Prediction P_t
+
actual Outcome O_t
↓
PredictionError / SurpriseEvidence
```

Важно:

- prediction должен быть идентифицируем;
- сравниваются совместимые semantic/feature revisions;
- error может быть многокомпонентным;
- probabilistic model может использовать likelihood/surprisal-like measures;
- deterministic model может использовать residual/distance;
- один universal scalar не обязателен.

Канонический invariant:

```text
prediction error
≠
reward
≠
intrinsic utility
```

`DU-14` решит, как такие signals могут превращаться в intrinsic motivation inputs.

---

# 16. Training Boundary

`DU-12` определяет необходимые learning targets концептуально, но не optimizer/loss schedule.

Natural baseline training evidence должна происходить из agent-available experience:

```text
belief/context at t
committed action at t
actual agent-visible outcome/percept at t+1
```

Environment Research Ground Truth может использоваться для:

- evaluation/probing;
- diagnostic labels;
- отдельного explicitly declared privileged-supervision experiment.

Но нельзя молча обучить baseline World Model на hidden oracle state и потом описать её как модель, научившуюся только из Agent experience.

Exact replay, target encoding, sequence length, loss composition и online/offline schedule относятся к `DU-25/26`.

---

# 17. Model Revision

Поведение World Model должно иметь воспроизводимую identity.

Conceptually различаются:

```text
world_model_revision
belief_revision
agent_revision
encoder/feature revision
```

Изменение trainable weights/adapters, влияющее на prediction behavior, создаёт новую model revision/соответствующую Agent revision по будущему training contract.

In-flight query/wave исполняется под фиксированной revision по `DU-05`.

---

# 18. Snapshot / Restore

Полный Agent Snapshot должен сохранять causally relevant World Model state.

Conceptually:

```text
WorldModelSnapshot
├── world_model_revision
├── committed belief/private recurrent state
├── belief_revision
├── feature/representation manifests
├── model configuration identity
├── causally relevant RNG state
└── intervention/degradation state
```

Trainable parameters могут храниться в общем Agent checkpoint, а не дублироваться в module snapshot; exact packaging определит `DU-27`.

Нельзя называть counterfactual fork exact, если recurrent belief/RNG/model revision не восстановлены.

---

# 19. Observability

Минимальная evidence surface должна позволять восстановить:

```text
belief update attempt
source percept/outcome identities
belief revision before/after
prediction query id
base belief revision
candidate action identity
world_model_revision
prediction result
uncertainty status
rollout id/branch/depth
prediction error evidence
failure/degradation
intervention id
```

Private learned state может иметь research probes, но probe access не становится runtime dependency.

---

# 20. Interventions

Допустимые research targets концептуально включают:

- structured belief field/projection;
- belief feature/latent через declared research capability;
- transition prediction;
- uncertainty output;
- model parameters/adapters через отдельную research/training boundary;
- rollout branch inputs.

Intervention обязана сохранять provenance и natural/treatment lineage distinction.

Latent intervention подпадает под OOD/off-target safeguards `DU-06`.

---

# 21. Failure / Degradation

World Model должна различать причинно значимые состояния, например:

```text
world model unavailable
belief uninitialized
incompatible belief/model revision
unsupported action representation
unsupported horizon
prediction unavailable
uncertainty unavailable
rollout truncated
numerical/invalid prediction
feature-space mismatch
snapshot incompatible
Cortex sub-capability unavailable
```

Нельзя использовать один `None`, zero-vector или empty prediction для всех случаев.

Fallback должен быть explicit и observable.

---

# 22. Configurations и controls

Должны быть различимы:

```text
NoWorldModel
DummyWorldModel
ControlWorldModel
real WorldModel
```

## 22.1. NoWorldModel

Prediction capability отсутствует.

## 22.2. DummyWorldModel

Deterministic engineering implementation для contract/integration tests.

## 22.3. ControlWorldModel

Research controls могут включать:

```text
last-observation persistence baseline
simple tabular/known-rule baseline
random/shuffled prediction
capacity/parameter-matched predictor
oracle/ground-truth research control
```

Oracle control допустим только через explicit research configuration и не является normal Agent-access baseline.

---

# 23. Evaluation implications

Будущий MINDRA-Eval должен отдельно измерять как минимум:

## Prediction quality

- one-step semantic prediction accuracy/error;
- probabilistic likelihood/calibration, если применимо;
- multi-step rollout degradation;
- event/termination prediction quality.

## Belief quality

В MicroWorld evaluator может сравнивать probe/public hypothesis с hidden ground truth, **не отдавая ground truth Agent**.

## Generalization

Проверять unseen:

- world instances;
- rule mappings;
- compositions;
- stochastic regimes;
- horizons.

## Causal usefulness

Важно не только:

> «World Model хорошо предсказывает»

но и:

> «корректный World Model улучшает downstream behavior относительно No/Control model».

Нужны controls класса:

```text
correct World Model
shuffled/degraded World Model
NoWorldModel
```

И parameter/compute-matched baseline, когда применимо.

---

# 24. Open implementation questions

До version design остаются открыты:

- RSSM/GRU/Transformer/SSM/другая architecture;
- stochastic latent family;
- reconstruction-based vs decoder-free training;
- structured prediction heads;
- representation dimension;
- ensemble count/uncertainty estimator;
- exact rollout interface;
- World Model size относительно Cortex;
- sequence batching/training schedule;
- use of TorchRL/Dreamer components;
- privileged auxiliary supervision experiments;
- exact compute budget.

Эти вопросы должны решаться позже в контексте конкретной версии и hardware budget, а не молча закрепляться implementation.

---

# 25. Completion gate DU-12

`DU-12` считается завершённым, когда:

- World Model имеет самостоятельную responsibility;
- `Canonical Percept`, `World Belief`, `World Prediction`, imagination и Hidden World State разведены;
- assimilation и action-conditioned prior/prediction разделены;
- partial observability имеет явную belief semantics;
- backend latent не превращён в universal representation;
- one-step и multi-step prediction имеют provenance;
- observed и imagined transitions не смешиваются;
- uncertainty имеет осторожную интерпретацию;
- prediction error не превращён в reward;
- Memory/Cortex/Goal/Self/Policy boundaries определены;
- snapshot/revision/failure semantics заданы;
- controls/ablation/evaluation implications заданы;
- concrete RSSM/Transformer/другой backend не принят преждевременно.
