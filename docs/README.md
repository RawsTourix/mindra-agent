# Документация MINDRA

## Назначение

Этот каталог — каноническая база знаний исследовательского проекта MINDRA.

Документация должна позволять человеку, ChatGPT, Codex или другому coding agent восстановить актуальный контекст **без истории чатов**.

Краткое задание не заменяет repository documentation.

---

# Быстрый порядок чтения

## Для общего понимания

1. [`project-concept.md`](project-concept.md)
2. [`architecture-concept.md`](architecture-concept.md)
3. [`research-methodology.md`](research-methodology.md)
4. [`design/README.md`](design/README.md)
5. [`design/current.md`](design/current.md)
6. [`design/contract-adr-consistency-freeze.md`](design/contract-adr-consistency-freeze.md)
7. [`design/version-roadmap.md`](design/version-roadmap.md)

## Для восстановления development workflow / нового чата

1. [`../AGENTS.md`](../AGENTS.md)
2. [`process/README.md`](process/README.md) — durable operational handoff;
3. mode-specific документ:
   - audit/correction → [`process/independent-audit.md`](process/independent-audit.md);
   - opening next step / Codex instruction → [`process/codex-instruction-authoring.md`](process/codex-instruction-authoring.md);
4. [`design/current.md`](design/current.md) — единственный live status;
5. current version docs и перечисленные в `current.md` clarification files.

## Перед version design / implementation

1. [`../AGENTS.md`](../AGENTS.md)
2. [`process/README.md`](process/README.md)
3. mode-specific process document;
4. [`design/current.md`](design/current.md)
5. [`design/contract-adr-consistency-freeze.md`](design/contract-adr-consistency-freeze.md)
6. [`design/contracts/semantic-freeze-manifest.md`](design/contracts/semantic-freeze-manifest.md)
7. [`design/version-roadmap.md`](design/version-roadmap.md)
8. [`versions/README.md`](versions/README.md)
9. релевантные canonical design owners;
10. релевантные accepted/non-superseded ADR;
11. релевантные semantic contracts;
12. version-specific `README.md`;
13. version-specific `implementation-sequence.md`;
14. section только текущего разрешённого `Vx.y-IS-XX` перед coding;
15. accepted step-specific clarification/correction docs;
16. датированный research/tool pass, если current tooling/model/compute materially влияет на решение.

Один Codex task реализует только один разрешённый implementation step; следующий открывается после verification + independent ChatGPT audit.

---

# Уровни истины

```text
Concept
→ Canonical Design + ADR
→ Semantic Freeze Baseline F31
→ semantic-frozen contracts
→ DU-32 Version Roadmap
→ Version design / exact contracts
→ Implementation sequence
→ Step-specific clarification
→ docs/design/current.md
→ Current implementation step
→ Implementation
→ Verification evidence
→ Independent audit
→ Engineering / Research evidence
→ Versioned Research Claims
```

```text
Design
≠ Implementation
≠ Engineering Testing
≠ Research Evidence
≠ Research Claim
```

Research/engineering evidence инициирует claim/design review при необходимости, но не переписывает architecture автоматически.

---

# Язык

Документация и комментарии в коде — на русском языке. Technical identifiers/API/package/class/function/type names остаются на английском.

---

# Operational workflow

Canonical process documentation:

- [`process/README.md`](process/README.md) — роли, modes, lifecycle, acceptance gates и recovery protocol;
- [`process/independent-audit.md`](process/independent-audit.md) — independent implementation/correction audit;
- [`process/codex-instruction-authoring.md`](process/codex-instruction-authoring.md) — transition/opening step и authoring copy-ready Codex instructions;
- [`versions/codex-step-prompt-template.md`](versions/codex-step-prompt-template.md) — canonical content template самого Codex task.

Новые обязательные workflow rules нельзя оставлять только в чате.

---

# Semantic Freeze F31

Canonical owner:

- [`design/contract-adr-consistency-freeze.md`](design/contract-adr-consistency-freeze.md)

Machine-facing manifest:

- [`design/contracts/semantic-freeze-manifest.md`](design/contracts/semantic-freeze-manifest.md)

Accepted decision:

- [`design/decisions/ADR-0031-semantic-contract-consistency-freeze.md`](design/decisions/ADR-0031-semantic-contract-consistency-freeze.md)

Freeze означает semantic ownership/lifecycle/source/provenance/causal boundaries, а не exact Python API.

---

# Version Roadmap

Canonical roadmap:

- [`design/version-roadmap.md`](design/version-roadmap.md)

Accepted decision:

- [`design/decisions/ADR-0032-vertical-capability-version-roadmap.md`](design/decisions/ADR-0032-vertical-capability-version-roadmap.md)

Version index:

- [`versions/README.md`](versions/README.md)

Roadmap строится вертикальными runnable slices и доводит проект от `v0.1 Core Kernel` до `v1.0 MINDRA Research Baseline`.

---

# Исследовательский журнал

Датированные literature/research/tool pass хранятся в [`research/`](research/). Hypotheses/experiments/results/claim evidence хранятся отдельно от canonical design.

---

# Внешние planes

- [`design/experience-data-replay.md`](design/experience-data-replay.md) — Experience/Data, `DU-25`;
- [`design/training-lifecycle.md`](design/training-lifecycle.md) — Training, `DU-26`;
- [`design/checkpoint-reproducibility-compute.md`](design/checkpoint-reproducibility-compute.md) — Checkpoint/Reproducibility/Compute, `DU-27`;
- [`design/mindra-eval.md`](design/mindra-eval.md) — Evaluation, `DU-28`;
- [`design/engineering-testing.md`](design/engineering-testing.md) — Engineering Verification, `DU-29`;
- [`design/research-claims-limitations.md`](design/research-claims-limitations.md) — Research Claims/Limitations, `DU-30`.

---

# Текущий статус

Общий архитектурный цикл:

```text
DU-00 … DU-32 complete
```

Semantic baseline `F31` и software roadmap приняты.

Для текущей version используются accepted version README, implementation sequence и step-specific clarifications.

**Фактический текущий implementation step и его OPEN/CLOSED/accepted status всегда определяются только:**

- [`design/current.md`](design/current.md)

Этот README намеренно не дублирует номер текущего `IS`, чтобы не становиться stale после каждого transition.