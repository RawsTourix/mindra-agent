# Research pass — Affect Dynamics / persistent affective state

## Статус

**Связанный Design Update:** `DU-17 — Affect Dynamics`  
**Дата среза:** 2026-08-17  
**Статус:** non-canonical research evidence

Этот документ фиксирует внешний исследовательский контекст, использованный при проектировании `DU-17`.

Он не объявляет человеческую emotion theory канонической архитектурой MINDRA и не доказывает субъективный опыт искусственного агента.

---

# 1. Исследовательские вопросы

Проверялись вопросы:

1. Имеет ли смысл отдельный persistent Affect layer поверх Appraisal?
2. Достаточны ли valence/arousal/PAD dimensions как universal state?
3. Есть ли evidence, что affect/mood зависит от накопленной истории событий, а не только текущего event?
4. Может ли persistent affect обратно влиять на дальнейшую оценку/решения?
5. Какие computational agent systems разделяют appraisal и dynamic emotion state?
6. Как predicted/imagined events должны соотноситься с current Affect?
7. Какие controls нужны, чтобы не спутать Affect с дополнительной recurrent memory capacity?

---

# 2. Russell — circumplex valence/arousal

James A. Russell.  
**A Circumplex Model of Affect.**  
Journal of Personality and Social Psychology, 1980.  
DOI: `10.1037/h0077714`.

Работа показывает, что human affective self-reports можно организовать в систематическое пространство, связанное с pleasure/displeasure и arousal.

Вывод для MINDRA:

- low-dimensional affective state является реалистичным computational representation candidate;
- однако модель описывает структуру human affect concepts/self-report и не является доказательством того, что искусственный Agent должен иметь именно такие coordinates;
- valence/arousal разумно оставить implementation/view/control, а не universal contract.

---

# 3. Mehrabian/Russell — pleasure/arousal/dominance

Albert Mehrabian, James A. Russell.  
**The Basic Emotional Impact of Environments.**  
Perceptual and Motor Skills, 1974.  
DOI: `10.2466/pms.1974.38.1.283`.

James A. Russell, Albert Mehrabian.  
**Evidence for a three-factor theory of emotions.**  
Journal of Research in Personality, 1977.  
DOI: `10.1016/0092-6566(77)90037-X`.

Авторы исследовали pleasure/arousal/dominance как compact dimensions human affective judgments.

Вывод для MINDRA:

- PAD пригоден как candidate baseline/view;
- `dominance` нельзя автоматически переносить в core, потому что MINDRA уже отдельно различает World-side controllability и Self-side coping/competence;
- прямое копирование PAD создало бы semantic overlap.

---

# 4. Rutledge et al. — affect как интеграция недавней истории

Robb B. Rutledge, Nikolina Skandali, Peter Dayan, Raymond J. Dolan.  
**A computational and neural model of momentary subjective well-being.**  
PNAS, 2014.  
DOI: `10.1073/pnas.1407535111`.

В probabilistic reward task momentary happiness лучше объяснялась не текущим earnings, а накопленным влиянием недавних expectations и reward prediction errors с temporal weighting.

Для MINDRA важна не человеческая «счастливость» сама по себе, а computational pattern:

```text
current affective state
=
function(recent event history, expectations, errors, temporal decay)
```

Это поддерживает гипотезу persistent integrator state поверх отдельных event evaluations.

---

# 5. Mood fluctuations и history-dependent dynamics

Исследования computational mood models показывают, что текущий mood level можно описывать через историю expected values/outcomes/prediction errors с decaying influence во времени, а не только через последний event.

Отдельные модели также исследуют обратную связь:

```text
outcomes/prediction errors
→ mood
→ perceived reward / future learning
```

Вывод для MINDRA:

- temporal inertia и history dependence имеют computational precedent;
- feedback Affect → future cognition допустим как исследовательская гипотеза;
- для MINDRA такой feedback должен идти только через explicit previous committed Affect revision, а не recursive same-step loop.

---

# 6. Emotion/mood и learning feedback

Работы по interaction between mood and learning показывают возможность bidirectional computational loop, где affective state зависит от outcomes, а затем влияет на perception/valuation следующих outcomes.

Для MINDRA это поддерживает отдельную проверяемую hypothesis:

```text
Affect_t
→ bias/modulation future Appraisal/Valuation
→ new Appraisal
→ Affect_(t+1)
```

Но design не принимает конкретный human reward-bias equation.

---

# 7. Appraisal trajectories

Johannes Schäfer, Janne Wagner, Roman Klinger.  
**Appraisal Trajectories in Narratives Reveal Distinct Patterns of Emotion Evocation.**  
WASSA 2026.  
DOI: `10.18653/v1/2026.wassa-1.7`.

Работа показывает, что последовательность appraisal dimensions во времени содержит структуру, не видимую в одном snapshot.

Вывод:

- appraisal-history имеет temporal information;
- отдельный persistent Affect может исследоваться как online compressed state этой history;
- нельзя просто переписывать прошлые AppraisalRecord текущим значением.

---

# 8. Affect flow в последовательных взаимодействиях

Alok Debnath, Yvette Graham, Owen Conlan.  
**An Appraisal Theoretic Approach to Modelling Affect Flow in Conversation Corpora.**  
CoNLL 2025.  
DOI: `10.18653/v1/2025.conll-1.16`.

Работа рассматривает affect flow — изменение affect/emotion по ходу последовательности — через multidimensional appraisal representation.

Для MINDRA:

- transition/trajectory semantics полезнее статического label;
- Appraisal и temporal affect evolution разумно держать связанными, но не обязательно одной сущностью.

---

# 9. Dynamic affective state в современных LLM-agent systems

Jingyao Cai et al.  
**From Triggers to Emotions: A CPM-Grounded Appraisal Multi-Agent for Dynamic Emotional Evolution in Persona-Based Dialogue.**  
`arXiv:2607.07824`, 2026.

Framework разделяет:

```text
trigger extraction
→ multidimensional appraisal
→ integration with previous emotional state
→ updated latent emotion state
```

Авторы показывают, что previous emotional state + current appraisal могут использоваться для последовательного обновления состояния в multi-turn agent simulation.

Для MINDRA это является evidence практической реализуемости разделения:

```text
Appraisal
≠
persistent Affect update
```

Но:

- работа ориентирована на persona/dialogue simulation;
- использует emotion taxonomy и LLM multi-agent orchestration;
- эти choices не переносятся в MINDRA canonical core.

---

# 10. Valence/arousal dynamics в 2026

Darya Hryhoryeva, Amaia Zurinaga, Hamidreza Jamalabadi, Iryna Gurevych.  
**UKP_Psycontrol at SemEval-2026 Task 2: Modeling Valence and Arousal Dynamics from Text.**  
`arXiv:2604.21534`.

В задаче моделировались current affect и short-term affective change в chronologically ordered texts.

В reported experiments recent numeric affect trajectories оказались важным источником для prediction изменения состояния.

Вывод для MINDRA:

- previous affective state может содержать predictive information сверх текущего semantic input;
- это поддерживает необходимость temporal controls (`ResetEveryEvent`, shuffled history, matched recurrent control).

---

# 11. Circumplex через Active Inference

Candice Pattisapu et al.  
**Free Energy in a Circumplex Model of Emotion.**  
`arXiv:2407.02474`, 2024.

Работа выводит valence/arousal-like signals из quantities Active Inference и демонстрирует artificial-agent simulations.

Вывод:

- low-dimensional affective views можно получить из совершенно разных computational theories;
- одинаковый label `valence` не гарантирует одинаковую causal semantics;
- MINDRA поэтому не фиксирует universal valence source/formula до Valuation/Training design.

---

# 12. RL + emotion literature

Работы по emotions in RL agents показывают большое разнообразие формализаций:

- appraisal-derived states;
- homeostatic/internal variables;
- prediction-error-based quantities;
- emotion-conditioned action/learning modulation.

Это поддерживает осторожный design:

> архитектурно фиксировать temporal/causal boundary, а не конкретную emotion theory.

---

# 13. Design conclusions, поддержанные research evidence

Research pass поддерживает следующие решения `DU-17`:

1. persistent history-dependent state является обоснованной исследовательской гипотезой;
2. Appraisal и Affect полезно разделять по event-level vs persistent temporal role;
3. Affect dynamics должна учитывать previous state и temporal decay/inertia;
4. low-dimensional valence/arousal/PAD — candidate, но не universal core;
5. предыдущий Affect может влиять на дальнейшую cognition только через explicit causal feedback;
6. temporal history controls обязательны для доказательства самостоятельной роли Affect;
7. emotion labels не нужны как canonical state;
8. branch-local simulated Affect полезнее, чем автоматическое изменение real Affect от любого imagined event.

---

# 14. Что evidence НЕ доказывает

Из рассмотренных работ не следует, что:

- искусственный Agent с persistent affective state что-либо субъективно чувствует;
- valence/arousal являются единственно правильным artificial affect space;
- human emotion categories должны быть внутренними переменными MINDRA;
- reward prediction error автоматически является Affect;
- Affect обязательно улучшит MINDRA;
- concrete LLM emotion simulation эквивалентна внутренней функциональной affect dynamics автономного агента.

---

# 15. Что нужно перепроверить перед implementation/version selection

Перед выбором implementation нужно заново проверить:

- актуальные lightweight affect-state/recurrent approaches;
- методы learned state-space dynamics;
- способы matched recurrent controls;
- calibration/normalization low-dimensional affect views;
- новые исследования appraisal → affect → decision causal chains;
- совместимость candidate implementation с выбранными `DU-18…23` boundaries.
