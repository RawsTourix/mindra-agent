# Research pass — Appraisal / cognitive appraisal landscape

## Статус

**Связанный Design Update:** `DU-16 — Appraisal`  
**Дата среза:** 2026-08-17  
**Статус:** non-canonical research evidence

Этот документ фиксирует внешний исследовательский контекст, использованный при проектировании `DU-16`.

Он не выбирает конкретную психологическую appraisal theory как обязательную архитектуру MINDRA и не переопределяет `docs/design/`.

---

# 1. Исследовательские вопросы

Проверялись следующие вопросы:

1. Должен ли Appraisal быть scalar, emotion label или multidimensional profile?
2. Какие appraisal dimensions устойчиво встречаются в разных теориях/данных?
3. Чем expectedness/novelty отличается от prediction error/surprisal?
4. Как разделить controllability и coping potential?
5. Следует ли Appraisal быть event-level или persistent state?
6. Нужно ли копировать human emotion taxonomy в MINDRA?
7. Может ли LLM/Cortex сам выступать Appraisal System?
8. Как моделировать appraisal dynamics и reappraisal?
9. Какие современные работы показывают полезность structured appraisal reasoning?

---

# 2. Component Process Model / dimensional appraisal

## Scherer / Component Process tradition

Appraisal theory рассматривает эмоционально значимое событие не через один label, а через набор evaluative checks относительно experiencer.

В литературе CPM часто выделяются группы checks вроде:

- relevance;
- implication/goal consequences;
- coping potential;
- normative significance;
- novelty/expectedness;
- controllability/power.

Для MINDRA важно:

- event significance зависит от целей/мотивации/контекста;
- multidimensional representation лучше сохраняет causal structure, чем emotion label;
- конкретные human check sets нельзя автоматически объявлять универсальным API искусственного агента.

---

# 3. Troiano, Oberländer, Klinger — appraisal dimensions в вычислительной форме

## Dimensional Modeling of Emotions in Text with Appraisal Theories

Enrica Troiano, Laura Oberländer, Roman Klinger.  
Computational Linguistics, 2023.  
DOI: `10.1162/coli_a_00461`.

Работа формализует appraisal variables как dimensions оценки событий и рассматривает 21 dimension на основе Component Process tradition.

Важные для MINDRA примеры:

- relevance;
- goal compatibility;
- expectedness;
- control;
- coping-related checks;
- agency;
- norm compatibility.

Вывод:

- appraisal dimensions могут быть machine-predictable intermediate representation;
- dimension profile даёт более структурированное описание event meaning, чем один emotion label;
- число и exact набор human dimensions не являются фиксированной истиной для MINDRA.

---

# 4. Эмпирическая интеграция appraisal dimensions

Работы по сравнению Scherer, Roseman, Smith/Ellsworth и других frameworks показывали частичное совпадение, но не полную идентичность dimension taxonomies.

В эмпирической интеграции выделялись factors вроде:

- pleasantness;
- control;
- certainty;
- effort/attention;
- novelty;
- motivational state;
- coping potential.

Вывод для design:

> наличие нескольких частично совпадающих human taxonomies — аргумент за extensible typed schema, а не за жёсткое копирование одной теории.

---

# 5. EMA — appraisal как процесс над интерпретацией ситуации

## EMA: A process model of appraisal dynamics

Stacy Marsella, Jonathan Gratch.  
Cognitive Systems Research, 2009, 10(1):70–90.  
DOI: `10.1016/j.cogsys.2008.03.005`.

EMA моделирует appraisal/coping как динамический вычислительный процесс и подчёркивает, что appraisal применяется к текущей интерпретации agent-environment relation, а динамика возникает по мере изменения этой интерпретации.

Вывод для MINDRA:

- Appraisal должен быть привязан к текущему internal context, а не быть immutable property события;
- reappraisal естественно представлять новым evaluation над новым context;
- persistence emotion/affect state не нужно прятать внутрь самого event-level Appraisal.

---

# 6. Appraisal и coping/controllability

Психологические и computational appraisal traditions регулярно отделяют assessment ситуации от последующего coping response.

Empirical work по controllability показывает, что appraisal control связан с выбором coping strategy, но высокий perceived control сам по себе не гарантирует лучший outcome.

Вывод:

```text
controllability
≠
coping strategy
≠
competence
```

Для MINDRA это поддерживает разделение:

- World-side action sensitivity → `controllability`;
- Self-side ability to cope → `coping potential`;
- actual response selection → future Executive Control/Policy.

---

# 7. CPM-RL — формализация appraisal через RL quantities

## Modeling Cognitive-Affective Processes with Appraisal and Reinforcement Learning

Jiayi Zhang, Joost Broekens, Jussi Jokinen, 2023.  
`arXiv:2309.06367`.

Работа формализует ряд CPM checks через quantities reinforcement learning:

- novelty;
- goal relevance;
- goal conduciveness;
- power.

Вывод для MINDRA:

- appraisal dimensions могут иметь operational computational definitions;
- один и тот же dimension не обязан требовать LLM;
- RL quantities — один возможный estimator family, но не architectural definition dimension;
- MINDRA не должна преждевременно смешивать Appraisal с reward/value только потому, что конкретный computational model использует RL formalization.

---

# 8. LLM как appraisal reasoner: возможности и ограничения

## Is GPT a Computational Model of Emotion? Detailed Analysis

Ala N. Tak, Jonathan Gratch, 2023.  
`arXiv:2307.13779`.

Исследование показывает, что GPT-family модели способны давать appraisal/emotion predictions, но имеют сложности с intensity и coping responses и чувствительны к постановке задачи.

## Investigating Large Language Models' Perception of Emotion Using Appraisal Theory

Nutchanon Yongsatianchot, Parisa Ghanad Torshizi, Stacy Marsella, 2023.  
`arXiv:2310.04450`.

LLM responses демонстрировали часть human-like appraisal dynamics, но не всегда различали ключевые appraisal dimensions так, как предсказывают theory/human data; ответы чувствительны к формулировкам.

Вывод для MINDRA:

- Cortex может быть полезным appraisal estimator/helper;
- textual self-report LLM не является автоматически canonical Appraisal;
- model/prompt/backend revision должны быть частью provenance;
- NoCortex/rule-based baseline необходим для оценки реального вклада Cortex.

---

# 9. Mechanistic appraisal representations в LLM

## Mechanistic Interpretability of Emotion Inference in Large Language Models

Ala N. Tak, Amin Banayeeanzade, Anahita Bolourani, Mina Kian, Robin Jia, Jonathan Gratch.  
Findings of ACL 2025.  
DOI: `10.18653/v1/2025.findings-acl.679`.

Авторы идентифицируют internal representations, связанные с appraisal concepts, и демонстрируют causal steering emotion inference через interventions на этих representations.

Вывод:

- appraisal-like dimensions могут иметь causal computational role внутри neural models;
- это поддерживает intervention-oriented evaluation MINDRA;
- raw latent intervention требует safeguards `DU-06` и не доказывает наличие subjective emotion.

---

# 10. Third-Person Appraisal Agent

## Third-Person Appraisal Agent: Simulating Human Emotional Reasoning in Text with Large Language Models

Simin Hong, Jun Sun, Hongyang Chen.  
Findings of EMNLP 2025.  
DOI: `10.18653/v1/2025.findings-emnlp.1288`.

Framework использует primary appraisal, secondary appraisal и reappraisal для structured emotional reasoning поверх LLM.

Вывод для MINDRA:

- appraisal/reappraisal decomposition остаётся актуальной в современных LLM systems;
- однако эта работа моделирует human emotional reasoning в тексте и не является готовой архитектурой внутренней оценки собственного autonomous Agent;
- evaluator feedback/reinforced tuning из таких systems нельзя переносить в natural Appraisal MINDRA как privileged runtime input.

---

# 11. Appraisal trajectories

## Appraisal Trajectories in Narratives Reveal Distinct Patterns of Emotion Evocation

Johannes Schäfer, Janne Wagner, Roman Klinger.  
WASSA 2026.  
DOI: `10.18653/v1/2026.wassa-1.7`.

Работа анализирует appraisal не как snapshot, а как trajectory по последовательности событий и показывает различимые временные patterns.

Вывод для MINDRA:

- appraisal records должны иметь temporal identity;
- повторные appraisals одного/связанных events полезно хранить как trajectory, а не переписывать старое значение;
- persistent Affect при этом остаётся отдельной возможной responsibility.

---

# 12. CAREBench 2026

## CAREBench: Evaluating LLMs' Emotion Understanding by Assessing Cognitive Appraisal Reasoning

Zhaoyue Sun, Hainiu Xu, Andero Uusberg, James J. Gross, Petr Slovak, Yulan He.  
`arXiv:2605.17176`.

Benchmark оценивает appraisal reasoning, appraisal ratings и emotion annotation как раздельные стадии и показывает, что хороший конечный emotion prediction не гарантирует корректный appraisal reasoning.

Вывод:

```text
correct downstream label
≠
correct internal appraisal mechanism
```

Это прямо поддерживает process-level evaluation MINDRA и dimension-specific diagnostics.

---

# 13. Современные appraisal-guided LLM frameworks 2025–2026

Современные работы используют appraisal как structured intermediate reasoning representation для:

- emotional reasoning;
- conversation analysis;
- emotion-cause extraction;
- response generation;
- retrieval;
- persona dynamics.

Это подтверждает практическую полезность appraisal как intermediate structured layer.

Но для MINDRA ключевое отличие:

> Appraisal оценивает события **относительно собственного committed Agent state**, а не реконструирует эмоции человека из текста.

---

# 14. Почему не emotion label

Literature показывает, что appraisal profiles способны объяснять/различать emotion categories, однако MINDRA не проектируется как human emotion classifier.

Поэтому канонический direction:

```text
event + agent context
→ AppraisalProfile
```

а optional research mapping:

```text
AppraisalProfile
→ human-like emotion label
```

не является core architecture.

---

# 15. Почему не обязательный scalar valence

Один event может иметь mixed relations одновременно:

```text
Goal A: facilitating
Goal B: obstructing
Drive X: pressure reduced
Drive Y: pressure increased
```

Scalarization требует отдельной aggregation policy.

Вывод:

- Appraisal сохраняет vector/typed structure;
- future Valuation решает decision-facing aggregation;
- optional event polarity может существовать только как derived summary.

---

# 16. Design conclusions DU-16

Research evidence поддерживает следующие canonical conclusions:

1. Appraisal разумно моделировать event-centered и context-dependent.
2. Multidimensional profile лучше соответствует исследовательской задаче MINDRA, чем emotion label или one-scalar reward.
3. Goals/Drives должны быть explicit appraisal context.
4. Controllability и coping potential следует разделять.
5. Expectedness не следует автоматически отождествлять с novelty/prediction error.
6. Reappraisal должно создавать новый temporally identified evaluation.
7. Cortex является optional estimator, а не semantic owner Appraisal.
8. Human appraisal theories являются источником candidate dimensions, но не обязательным complete schema.
9. Dimension-level interventions и process-level evaluation важнее проверки только downstream emotion/behavior label.
10. Appraisal не является доказательством human-like emotion или subjective experience.

---

# 17. Что нужно перепроверить перед implementation

Перед выбором concrete Appraisal implementation нужно заново проверить:

- актуальные appraisal benchmarks/datasets;
- availability/licensing datasets;
- актуальные small-model/Cortex candidates;
- whether rule-based MicroWorld dimensions достаточны для first vertical slice;
- calibration methodology per dimension;
- стоимость Cortex-assisted Appraisal;
- необходимость learned vs deterministic estimators;
- minimal subset dimensions, необходимый для `DU-17/18` experiments.

---

# 18. References

Основные источники этого research pass:

- Marsella & Gratch, **EMA: A process model of appraisal dynamics**, 2009, DOI `10.1016/j.cogsys.2008.03.005`;
- Troiano, Oberländer, Klinger, **Dimensional Modeling of Emotions in Text with Appraisal Theories**, 2023, DOI `10.1162/coli_a_00461`;
- Zhang, Broekens, Jokinen, **Modeling Cognitive-Affective Processes with Appraisal and Reinforcement Learning**, `arXiv:2309.06367`;
- Tak & Gratch, **Is GPT a Computational Model of Emotion? Detailed Analysis**, `arXiv:2307.13779`;
- Yongsatianchot, Torshizi, Marsella, **Investigating Large Language Models' Perception of Emotion Using Appraisal Theory**, `arXiv:2310.04450`;
- Tak et al., **Mechanistic Interpretability of Emotion Inference in Large Language Models**, Findings ACL 2025, DOI `10.18653/v1/2025.findings-acl.679`;
- Hong, Sun, Chen, **Third-Person Appraisal Agent**, Findings EMNLP 2025, DOI `10.18653/v1/2025.findings-emnlp.1288`;
- Schäfer, Wagner, Klinger, **Appraisal Trajectories in Narratives Reveal Distinct Patterns of Emotion Evocation**, WASSA 2026, DOI `10.18653/v1/2026.wassa-1.7`;
- Sun et al., **CAREBench**, `arXiv:2605.17176`.
