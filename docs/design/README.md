# Design-документация MINDRA

## Назначение

`docs/design/` — каноническое место архитектурной документации MINDRA.

Здесь должны фиксироваться принятые семантики, invariants, границы модулей, internal contracts, архитектурные решения и будущие version plans.

На текущем этапе каталог содержит только documentation foundation. Детальные subsystem design будут добавляться последовательно после отдельного исследования вариантов.

---

# 1. Иерархия

```text
Concept
→ Design semantics / invariants
→ ADR
→ Exact internal contracts
→ Version specification
→ Implementation sequence
→ Engineering/research acceptance evidence
```

Research evidence не переписывает design напрямую: противоречащий результат инициирует design review.

---

# 2. Текущая навигация

## Foundation

- [`principles.md`](principles.md) — устойчивые инженерные и исследовательские принципы;
- [`glossary.md`](glossary.md) — канонические значения терминов;
- [`documentation-plan.md`](documentation-plan.md) — порядок дальнейшего проектирования;
- [`current.md`](current.md) — factual status и следующий допустимый шаг.

## Decision records

- [`decisions/README.md`](decisions/README.md).

## Exact internal contracts

- [`contracts/README.md`](contracts/README.md).

## Versions

- [`versions/README.md`](versions/README.md).

---

# 3. Canonical owner

У значимой архитектурной темы в будущем должен быть один основной canonical owner.

Общий документ может ссылаться на тему, но не должен независимо определять вторую конкурирующую семантику.

Если ADR меняет принятое решение:

1. обновляется ADR registry;
2. обновляется canonical design owner;
3. обновляются exact contracts;
4. обновляются затронутые version plans/status;
5. только затем implementation следует новому решению.

---

# 4. Design для coding agents

Implementation-ready design должен минимизировать архитектурные догадки.

Для каждой будущей подсистемы желательно определить:

- назначение;
- responsibilities;
- non-goals;
- inputs/outputs;
- owned state;
- dependencies;
- lifecycle/update semantics;
- training signals;
- persistence/checkpoint semantics;
- observability;
- failure/degradation behavior;
- ablation/control strategy;
- evaluation metrics;
- open questions.

Если существенное решение ещё не принято, оно должно быть обозначено как open question/blocker, а не оставлено на усмотрение Codex.

---

# 5. Текущая граница

Пока не существует accepted module design, exact module contract или version roadmap.

Обсуждавшиеся ранее Qwen, TensorDict, PPO, Dreamer, RND, ICM, FAISS, PEFT/LoRA, Colab и другие технологии являются кандидатами для будущего анализа, но не каноническими требованиями.

Фактический статус: [`current.md`](current.md).
