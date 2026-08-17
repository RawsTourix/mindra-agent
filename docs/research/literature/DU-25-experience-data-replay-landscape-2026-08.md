# DU-25 — Experience / Data / Replay: research pass 2026-08

## Статус

**Дата:** 2026-08-17  
**Тип:** non-canonical research evidence  
**Связанный Design Update:** `DU-25 — Experience / Data / Replay`

Этот документ фиксирует ориентиры, использованные при проектировании data plane MINDRA.

Он **не выбирает** RLDS, Minari, Reverb, Arrow, HDF5, TFRecord или конкретный replay-buffer backend.

---

# 1. Исследовательский вопрос

Нужен data design, который одновременно поддерживает:

```text
rich causal MINDRA history
+
обычные episode/transition datasets
+
sequence training
+
replay
+
relabeling/hindsight
+
research annotations
```

при этом не смешивает:

```text
Agent Memory
Research Evidence
Training Dataset
Training Replay
```

и не теряет failure cases `DU-24`.

---

# 2. RLDS

## Google Research — RLDS

- repository: https://github.com/google-research/rlds

RLDS позиционируется как ecosystem для хранения, чтения и преобразования episodic sequential-decision datasets.

Базовая структура:

```text
Dataset
→ Episodes
→ Steps
```

Episode имеет metadata, а Step может содержать:

```text
observation
action
reward
is_first
is_last
is_terminal
discount
custom metadata
```

RLDS также подчёркивает уникальные episode IDs и возможность хранить agent/environment/experiment metadata.

Для MINDRA это сильный precedent двух вещей:

1. episode/step projection является практически полезным interoperability format;
2. metadata/version/identity вокруг trajectory необходимы, а не являются «лишними логами».

Но standard step semantics недостаточна как source of truth MINDRA, потому что не обязана выражать:

```text
multiple Cognitive Cycles
Executive decisions
Policy candidate set
SelectedActionIntent vs ActionCommit
execution_unknown
partial execution
intervention lineage
```

Следствие для `DU-25`:

> RLDS-подобный episode/step view полезен как derived/export projection, но не как полный canonical Experience Journal.

---

# 3. Minari

## Farama Foundation — Minari

- docs: https://minari.farama.org/
- dataset standards: https://minari.farama.org/content/dataset_standards/

Minari предоставляет dataset tooling для offline RL и сохраняет episode-level data с:

```text
observations
actions
rewards
terminations
truncations
infos
```

Текущая документация также предусматривает dataset/episode metadata и storage в Arrow/HDF5 в зависимости от версии/tooling.

Особенно полезен принцип:

```text
observations count = steps + 1
```

что делает transition extraction явным.

Для MINDRA Minari показывает, что practical offline RL stack выигрывает от удобного episode-level materialized representation.

Но `infos` не должен использоваться MINDRA как бесформенный контейнер, где одновременно лежат:

```text
agent-visible data
hidden evaluator labels
transport diagnostics
internal cognition
```

Именно поэтому `DU-25` вводит отдельные primary Experience Events и Research Annotation Records.

---

# 4. Reverb

## Cassirer et al. — Reverb: A Framework For Experience Replay

- arXiv: `2102.04736`
- repository: https://github.com/google-deepmind/reverb

Reverb — специализированная infrastructure для experience replay.

Она поддерживает configurable tables и разные sampler/remover strategies:

```text
uniform
prioritized
FIFO / queue
rate limiting
```

Для MINDRA это важный precedent:

> replay storage/sampling policy является отдельной runtime/training infrastructure responsibility.

Следовательно:

```text
Experience Journal
≠
Replay Table
```

Replay table может менять priorities, sampling frequency и eviction независимо от долговременного source dataset.

Удаление replay item не должно означать удаление historical experience.

MINDRA не принимает Reverb/gRPC/TensorFlow как обязательную implementation.

---

# 5. Hindsight Experience Replay

## Andrychowicz et al. — Hindsight Experience Replay

- arXiv: `1707.01495`
- https://arxiv.org/abs/1707.01495

HER переиспользует experience, рассматривая достигнутый outcome как альтернативную goal condition для обучения.

Для data architecture это особенно важный пример:

```text
что Agent реально хотел в source trajectory
≠
какой goal используется в derived training sample
```

Поэтому `DU-25` не разрешает hindsight transform переписывать original Goal/trajectory.

Правильный pattern:

```text
source trajectory
+
relabel transform
→ new TrainingSample
```

с explicit source/relabel provenance.

Это правило обобщается на reward relabeling, feature re-encoding и post-hoc targets.

---

# 6. W3C PROV

## W3C — PROV Data Model

- Recommendation family: https://www.w3.org/TR/prov-dm/

PROV-DM рассматривает provenance через entities, activities, agents и derivation relations.

Для MINDRA полезны не конкретные RDF/XML formats, а general design principles:

```text
derived entity
→ имеет связь с source entities/activities

responsibility/source identity
→ часть provenance

provenance itself
→ может иметь собственную структуру
```

Это хорошо поддерживает наше решение:

```text
source ExperienceEvent
→ transformation activity
→ derived TrainingSample
```

и отдельное хранение source/trust boundary.

MINDRA не принимает W3C PROV schema как внутренний wire format.

---

# 7. Почему простой `(s,a,r,s')` недостаточен

Классический RL sample предполагает, что существует понятная связь:

```text
state/action
→ next state/reward
```

После `DU-24` возможна ситуация:

```text
Action Commit
→ DispatchAttempt
→ execution_unknown
```

без достоверного next observation.

Также внутри одного Decision Window могут быть несколько Cognitive Cycle и Policy deferral/planning events.

Следовательно transition tuple должен быть **projection**, а не archival truth.

---

# 8. Event sourcing как data pattern, но не Agent runtime

Append-only events естественно сохраняют:

- failures;
- reconciliation;
- late/out-of-order writes;
- interventions;
- derived-data lineage.

Но полное runtime event sourcing MINDRA уже не требуется и даже конфликтовало бы с ранее принятыми current-state semantics.

Поэтому `DU-25` использует pattern только в data plane:

```text
runtime state
→ обычный MINDRA committed state

historical experience
→ causal event journal
```

---

# 9. Late/out-of-order data

В асинхронной infrastructure physical record order может отличаться от causal order.

Например:

```text
worker A event logically earlier
worker B event physically arrives first
```

Поэтому stable IDs + causal parent refs + logical scopes сильнее, чем один timestamp/file offset.

Wall-clock полезен диагностически, но не должен быть единственным causal ordering key.

---

# 10. Dataset projections как materialized views

Практическая архитектура training data выигрывает, если сложная reconstruction из journal выполняется один раз на dataset-build этапе, а не на каждом minibatch.

Поэтому MINDRA вводит:

```text
Experience Journal
→ ProjectionSpec
→ Episode/Decision/Transition/Sequence projection
→ DatasetManifest
```

Так standard RL/sequence tooling остаётся простым, а source causal history не теряется.

---

# 11. Privileged annotations

Многие benchmark environments имеют information, полезную evaluator'у:

```text
true world state
oracle action
shortest path
success condition
hidden rules
```

Запись такой информации полезна для analysis.

Но если поместить её в обычный per-step `info` и затем автоматически export'ить в training data, возникает leakage.

Поэтому `DU-25` принимает отдельный:

```text
ResearchAnnotationRecord
```

и explicit visibility policy.

Это особенно важно для заявлений о self-supervised/agent-visible learning.

---

# 12. Replay sampling — тоже provenance

Prioritized replay и другие sampling policies меняют effective training distribution.

Поэтому воспроизводимость training experiment требует знать не только dataset, но и:

```text
sampler
priority revision
population/buffer revision
selected samples
RNG semantics
```

Reverb является практическим precedent, где sampler/remover/rate limiter являются first-class configuration.

`DU-25` фиксирует только data provenance; exact learning consequences проектируются в `DU-26`.

---

# 13. Replay priority не является cognitive value

Training algorithms могут определять priority через:

```text
TD error
loss
age
novelty for training
```

Но это training-side importance.

Она не должна автоматически становиться:

```text
Memory retention importance
Salience
Drive
Valuation
```

Иначе Training Runtime начнёт скрыто менять cognition Agent.

---

# 14. Sequence data и modern agents

MINDRA не ограничена one-step RL.

World Model, Policy, Executive Control, Memory и Cortex training потенциально могут требовать:

```text
history windows
Decision Window sequences
full episodes
n-step targets
paired/counterfactual samples
```

Поэтому canonical data layer должен поддерживать произвольные derived windows над source events, а не только transitions.

---

# 15. Schema/versioning

RLDS/Minari показывают важность dataset/environment metadata, но MINDRA дополнительно должна связывать behavior с внутренними revision:

```text
agent_revision
policy_revision
world-model revision
self-model revision
Memory revision
representation revision
```

Это особенно важно при online learning, когда outcome может быть обработан уже другой revision, чем та, которая выбрала action.

---

# 16. Changing behavior policies

Offline datasets часто объединяют experience разных policies/quality levels.

Для MINDRA mixed revisions допустимы, но должны быть observable.

Нельзя dataset, собранный под:

```text
A1, A2, A3
```

назвать просто:

```text
Agent A3 data
```

если action attribution реально относится к старым revisions.

---

# 17. `terminated` и `truncated`

RLDS и Minari оба сохраняют semantics окончания episode/trajectory, хотя конкретные representations различаются.

Это поддерживает решение `DU-07/25` не сворачивать external truncation в natural task terminal.

Training extractor должен сохранять это различие до тех пор, пока конкретный algorithm явно не задаст собственную target semantics.

---

# 18. Storage backend

Практические systems используют разные formats:

```text
RLDS/TFDS
HDF5
Arrow
in-memory replay tables
```

Это подтверждает, что semantic schema и physical storage не стоит склеивать.

Первая MINDRA implementation может использовать максимально простой локальный backend, если сохраняет IDs/provenance/revisions.

---

# 19. Data completeness

RLDS предусматривает invalid/incomplete episode metadata для случаев неполной записи.

Для MINDRA требуется более granular distinction, потому что отсутствие:

```text
Cortex activation artifact
```

и отсутствие:

```text
Action Commit
```

имеют совершенно разное влияние на пригодность trajectory.

Поэтому completeness/integrity становится structured property.

---

# 20. Research implications

Будущая evaluation/data testing должна сравнить как минимум:

```text
full causal projection
vs transition-only projection
```

и отдельно проверять:

- leakage privileged annotations;
- source/derived lineage;
- replay selection reproducibility;
- mixed agent revisions;
- unresolved execution handling;
- sequence ordering;
- split leakage;
- schema migration.

---

# 21. Вывод для DU-25

Research landscape поддерживает следующие решения:

1. episode/step formats полезны, но недостаточны как полный source MINDRA;
2. replay infrastructure должна быть отделена от archival source experience;
3. hindsight/relabeling логичнее оформлять как derived transformation;
4. provenance/derivation — first-class часть data quality;
5. evaluator-only data должно иметь отдельную visibility boundary;
6. `terminated/truncated` и incomplete data нельзя смешивать;
7. changing actor/model revisions должны сохраняться в metadata;
8. physical storage/backend можно выбирать позже;
9. canonical event journal + derived projections даёт баланс causal fidelity и practical training usability.
