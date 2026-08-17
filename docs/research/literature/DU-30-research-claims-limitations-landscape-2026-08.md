# Research pass — Research Claims / Limitations / scientific reporting

## Статус

**Связанный Design Update:** `DU-30 — Research Claims / Limitations`  
**Дата среза:** 2026-08-17  
**Статус:** non-canonical research evidence

Этот документ фиксирует исследовательский контекст, использованный при проектировании claim/limitation discipline MINDRA.

Он не задаёт publication venue, statistical doctrine или философскую теорию сознания.

---

# 1. Исследовательские вопросы

Проверялись:

1. как отделять observation, interpretation и claim;
2. как ограничивать strength/scope claim experimental evidence;
3. как документировать negative/null/inconclusive results;
4. как хранить limitations и known unknowns не только prose-абзацем;
5. как различать reproducibility/replicability/generalization;
6. как не приписывать architecture effect concrete implementation/Cortex/compute confound;
7. какие правила нужны для causal wording;
8. какие ограничения особенно важны для claims о consciousness/subjective experience у AI;
9. как сохранять superseded/challenged claims без history rewrite.

---

# 2. NASEM — reproducibility и replicability как разные scientific concerns

National Academies of Sciences, Engineering, and Medicine.  
**Reproducibility and Replicability in Science.**  
National Academies Press, 2019. DOI: `10.17226/25303`.

Отчёт подчёркивает необходимость различать reproducibility/replicability, прозрачность методов, uncertainty и условия, при которых результат можно повторить или независимо подтвердить.

Для MINDRA:

- `DU-27 ReproducibilityClaim` не должен автоматически превращаться в claim о independent replication;
- restoration одного run и повторяемость scientific effect — разные axes;
- claim обязан ссылаться на конкретный scope software/hardware/data/replicates.

---

# 3. TOP Guidelines — прозрачность research lifecycle

Brian A. Nosek et al.  
**Promoting an open research culture.**  
Science, 2015. DOI: `10.1126/science.aab2374`.

TOP Guidelines формализовали уровни прозрачности data/materials/code/design/preregistration/replication.

Вывод для MINDRA:

- confirmatory/exploratory distinction разумно делать first-class;
- future report должен быть traceable до conditions, data, code/checkpoint и analysis plan;
- один prose statement недостаточен как source of truth scientific claim.

MINDRA не принимает конкретную TOP level taxonomy как contract.

---

# 4. Open Science Collaboration — independent replication может существенно отличаться от исходной литературы

Open Science Collaboration.  
**Estimating the reproducibility of psychological science.**  
Science, 2015. DOI: `10.1126/science.aac4716`.

Работа показала, что наличие опубликованного эффекта и независимое воспроизведение эффекта — разные вопросы, а uncertainty/heterogeneity требуют явного анализа.

Для MINDRA:

- успешный initial experiment не становится permanent architecture truth;
- claim lifecycle должен поддерживать challenging evidence и supersession;
- independent replicates особенно важны для широких claims.

---

# 5. ASA statement — p-value не является полным смыслом evidence

Ronald L. Wasserstein, Nicole A. Lazar.  
**The ASA's Statement on p-Values: Context, Process, and Purpose.**  
The American Statistician, 2016. DOI: `10.1080/00031305.2016.1154108`.

Основная полезная для MINDRA идея: один threshold/p-value не должен заменять effect magnitude, uncertainty, study design и substantive interpretation.

Вывод:

```text
statistically detectable
≠
practically meaningful
≠
causal
≠
general
```

Поэтому `ResearchClaim` не получает canonical `p < 0.05 → supported` rule.

---

# 6. RL/ML variability — claims требуют condition/replicate scope

Henderson et al.  
**Deep Reinforcement Learning that Matters.**  
AAAI 2018 / arXiv:`1709.06560`.

Работа показывает чувствительность RL conclusions к seeds, hyperparameters, implementations и reporting choices.

Agarwal et al.  
**Deep Reinforcement Learning at the Edge of the Statistical Precipice.**  
NeurIPS 2021.

Работа подчёркивает неопределённость aggregate RL results при малом числе runs и необходимость interval/distribution-aware reporting.

Для MINDRA:

- claim обязан pin'ить replicate/analysis context;
- point estimate без uncertainty недостаточен для stochastic general claim;
- tuning/compute/implementation differences являются limitations/confounders, а не мелкими деталями.

Детальная evaluation semantics уже принята `DU-28`.

---

# 7. Causal language требует causal design

Современная causal-inference традиция различает наблюдательные ассоциации и эффекты вмешательств.

Для MINDRA достаточный инженерный вывод:

```text
correlation(state, behavior)
≠
causal contribution
```

Сильный claim о causal role должен ссылаться на `DU-28` intervention/control evidence, base-state validity и off-target assessment.

MINDRA не выбирает одну causal inference library или одну formal causal model.

---

# 8. Butlin et al. — AI consciousness требует theory-derived indicators, а не поведенческого leap

Patrick Butlin et al.  
**Consciousness in Artificial Intelligence: Insights from the Science of Consciousness.**  
arXiv:`2308.08708`, 2023.

Работа обсуждает теоретически мотивированные indicator properties из нескольких scientific theories сознания и подчёркивает необходимость аккуратной, theory-specific оценки AI systems.

Для MINDRA особенно важен отрицательный вывод:

- наличие отдельного functional mechanism само по себе не является достаточным consciousness proof;
- human-like language/self-report не решает вопрос автоматически;
- разные theories дают разные indicators и assumptions;
- architecture должна отделять functional evidence от phenomenological claim.

MINDRA не принимает indicator list этой работы как собственный consciousness benchmark.

---

# 9. Cogitate Consortium 2025 — теории сознания сами требуют adversarial testing

Cogitate Consortium et al.  
**Adversarial testing of global neuronal workspace and integrated information theories of consciousness.**  
Nature 642, 133–142 (2025). DOI: `10.1038/s41586-025-08888-1`.

Preregistered adversarial collaboration проверяла differential predictions GNWT и IIT и получила результаты, которые частично поддерживали, а частично существенно оспаривали ключевые predictions обеих теорий.

Для MINDRA:

- нельзя описывать одну human consciousness theory как установленный software criterion;
- наличие Workspace не является доказательством consciousness;
- сильные theory claims должны сохранять failed/partial predictions;
- adversarial/negative evidence должно иметь равный статус в ClaimRegistry.

---

# 10. Functional analogy ≠ biological identity

Human-inspired computational terminology полезна для формирования hypotheses:

```text
memory
appraisal
affect
workspace
self model
```

Но одинаковое имя может скрывать разные causal mechanisms.

Для MINDRA canonical rule:

> сравнивать operational properties и causal roles, а не выводить biological/phenomenological identity из названия или поверхностного поведения.

---

# 11. Negative results и publication bias

Research ecosystems склонны сильнее распространять положительные результаты, чем null/negative evidence.

Для long-lived архитектурного проекта это особенно опасно: условный модуль может сохраняться годами только потому, что неудобные matched-control результаты потерялись.

Поэтому DU-30 требует:

```text
negative/null/inconclusive evidence
→ persistent record
→ claim/module-gate review
```

а не только публикацию «успешных» experiments.

---

# 12. Null result не всегда evidence отсутствия

Нулевой/неубедительный результат может возникнуть из-за:

- высокой variance;
- малого числа independent replicates;
- слабой manipulation;
- insensitive metric;
- ceiling/floor effect;
- implementation defect;
- broad heterogeneous task distribution.

Поэтому нужны разные result classes:

```text
negative evidence
null estimate
inconclusive
invalid
not measured
```

Это продолжает `DU-28` validity/statistical semantics.

---

# 13. Claim scope и external validity

Результат одной condition family не должен автоматически распространяться на:

- другой Cortex;
- более длинный horizon;
- physical/embodied environment;
- другую data regime;
- другую compute scale;
- другую implementation boundary.

Scope extension является отдельной empirical hypothesis.

---

# 14. Architecture vs implementation attribution

Если одна конкретная implementation `WorkspaceV1` выигрывает, возможны по меньшей мере два объяснения:

```text
семантика Workspace полезна
```

или:

```text
именно implementation V1 имеет удачный inductive bias/capacity
```

Architecture-level claim требует более широких controls/transfer evidence.

Это особенно важно для MINDRA, где module boundaries намеренно заменяемы.

---

# 15. Claim lifecycle как средство scientific self-correction

Research project длится дольше отдельной статьи.

Поэтому полезна модель:

```text
Claim rev1
→ new evidence
→ ClaimReview
→ rev2 / weaken / narrow / supersede
```

вместо редактирования старой фразы без history.

Такой lifecycle хорошо согласуется с общей MINDRA discipline immutable source evidence + derived versioned interpretations.

---

# 16. Known unknowns как нормальный результат

Некоторые вопросы могут быть principially unresolved текущим design:

- есть ли phenomenological experience;
- переносится ли mechanism на qualitatively другой Cortex;
- какой latent variable соответствует human concept;
- является ли effect architecture-general или implementation-specific.

Попытка заменить `unknown` красивой гипотезой увеличивает риск overclaim.

Поэтому `KnownUnknownRecord` принят как first-class entity.

---

# 17. Design conclusions

Research pass поддерживает решения `DU-30`:

1. Observation/Interpretation/Claim должны быть разными artifacts;
2. ClaimScope обязателен;
3. claim strength ограничен design/evidence strength;
4. causal/generalization/architecture claims требуют отдельных support semantics;
5. negative/null/inconclusive/invalid различаются;
6. limitations и known unknowns должны иметь stable identity/lifecycle;
7. old claims нужно supersede/weaken, а не rewrite;
8. functional cognitive mechanisms не являются sufficient evidence phenomenology;
9. Workspace/Affect/Self Model не дают consciousness proof автоматически;
10. publication/report prose должно быть traceable до canonical claim revision.

---

# 18. Что evidence НЕ доказывает

Из рассмотренного research landscape не следует, что:

- существует одна универсальная шкала evidence strength;
- один statistical method подходит всем MINDRA studies;
- отсутствие significant effect доказывает отсутствие mechanism;
- reproducible run гарантирует replicated scientific effect;
- human-inspired architecture является biologically equivalent;
- наличие functional consciousness-theory indicator достаточно для утверждения subjective experience;
- AGI можно определить одним benchmark score.

---

# 19. Что перепроверить перед реальными публикациями

Перед первой external research publication нужно заново проверить:

- актуальные reporting/reproducibility guidelines выбранного venue;
- актуальное состояние AI-consciousness research и terminology;
- требования к disclosure models/data/compute;
- актуальные statistical recommendations для конкретного experiment design;
- подходящие preregistration/registered-report options;
- policy выбранного venue по negative results/artifacts.
