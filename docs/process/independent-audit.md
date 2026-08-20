# Independent Audit Mode

## Статус

**Статус:** `accepted operational governance`  
**Режимы:** `MODE-AUDIT`, `MODE-CORRECTION`  
**Назначение:** независимая проверка implementation/correction после push и принятие решения о необходимости correction

Этот документ описывает **не Codex self-check**, а отдельный audit ChatGPT после того, как implementation находится на remote commit.

---

# 1. Когда входить в MODE-AUDIT

Типичный вход:

```text
пользователь: «код запушен, проверь»
+
Codex implementation/verification report
```

Audit начинается только после определения фактического remote commit/HEAD.

Codex report используется как:

- карта заявленных изменений;
- список выполненных verification commands;
- список затронутых VerificationObligations;
- источник предложенного commit name;

но **не** как доказательство корректности code/design.

---

# 2. Обязательный входной контекст

До verdict ChatGPT должен прочитать/проверить минимум:

1. `AGENTS.md`;
2. [`README.md`](README.md);
3. `docs/design/current.md`;
4. current version `README.md`;
5. current version `implementation-sequence.md`, section проверяемого `IS`;
6. все step-specific accepted clarifications/corrections;
7. релевантные canonical design/ADR/contracts;
8. remote commit metadata/diff;
9. changed production files;
10. changed tests;
11. CI evidence/status, если доступно.

Нельзя выдавать итоговый `PASS` только по commit summary или Codex report.

---

# 3. Audit layers

Audit выполняется минимум по следующим слоям.

## 3.1. Repository/commit layer

Проверить:

- фактический HEAD/commit SHA;
- commit действительно содержит заявленный implementation;
- сравнение с предыдущим accepted baseline;
- changed files;
- нет ли посторонних changes;
- commit message соответствует фактическому scope, если это materially важно;
- документация/current status не были самовольно изменены Codex, если step этого не разрешал.

## 3.2. Scope layer

Проверить:

- реализован только текущий `IS`;
- prerequisites действительно уже accepted;
- forbidden scope следующего `IS` не протёк;
- нет premature abstractions/features «на будущее»;
- correction не превратилась в feature extension.

Verdict должен явно различать:

```text
scope PASS
scope leak
scope underimplementation
```

## 3.3. Exact design layer

Проверить implementation относительно:

```text
F31
+ canonical design/ADR/contract
+ accepted version design
+ implementation sequence
+ step-specific clarification
```

Особое внимание:

- ownership;
- read/write authority;
- source/provenance;
- temporal semantics;
- revision semantics;
- controlled construction;
- fail-closed validation;
- staged vs committed distinction;
- public vs internal API;
- transaction boundary;
- availability/missing semantics;
- deterministic/canonical representations.

Если implementation соответствует общему смыслу, но нарушает exact accepted shape текущего step, это считается defect или documentation mismatch — не «почти PASS».

## 3.4. Boundary/invariant layer

Нужно искать не только happy-path bugs, но и способы обойти boundary.

Примеры вопросов:

- можно ли сконструировать supposedly validated object в обход validator/compiler;
- может ли модуль получить ambient/full state;
- может ли mutable alias изменить старый snapshot;
- может ли partial mutation произойти после первой успешной операции batch;
- можно ли подделать provenance/revision;
- выполняется ли validation до allocation/commit/mutation;
- не появился ли Service Locator;
- не получила ли observability/evaluation plane causal influence;
- не превратился ли staged proposal в implicit commit.

Нужно мысленно проверять adversarial/negative cases, даже если tests их ещё не содержат.

## 3.5. Test quality layer

Проверить не только наличие tests, но и то, что они действительно доказывают нужные invariants.

Искать:

- только happy-path coverage;
- тест, который проверяет реализацию тем же ошибочным предположением, что и production code;
- отсутствующий regression test на найденный edge case;
- слишком слабую assertion;
- property test, который фактически не варьирует важный параметр;
- test-only bypass production boundary;
- skipped/xfail вместо исправления.

Если найден реальный defect, correction должна включать regression test.

## 3.6. Verification evidence layer

Codex report сверяется с accepted verification profile.

Минимально различать:

```text
PASS
FAIL
NOT APPLICABLE
NOT AVAILABLE
PENDING
RUNNING
```

Для `v0.1` после `IS-01` проверяется наличие:

- targeted verification;
- `FULL-C0`;
- build;
- `git diff --check`, если требовалось task;
- remote GitHub Actions Ubuntu/Windows evidence.

ChatGPT по возможности проверяет CI самостоятельно.

Если connector не видит push-triggered run, допустимо operator confirmation:

```text
post-push CI: operator-confirmed PASS
```

Но нельзя писать, что ChatGPT independently observed green run, если этого не было.

---

# 4. Audit verdicts

Допустимые основные verdicts:

## `AUDIT-PASS-PENDING-CI`

Использовать, если:

- code/design/scope audit прошёл;
- local verification прошла;
- обязательный post-push CI ещё не подтверждён.

Следующий `IS` **не открывается**.

## `AUDIT-PASS`

Использовать, если code/design/scope и все acceptance evidence достаточны.

После этого можно перейти в `MODE-TRANSITION`.

## `CORRECTION-REQUIRED`

Использовать, если найден implementation defect внутри accepted semantics.

Следующий `IS` остаётся CLOSED.

ChatGPT переходит в `MODE-CORRECTION`.

## `DOCUMENTATION-CLARIFICATION-REQUIRED`

Использовать, если defect нельзя однозначно исправить без нового exact version-level решения, но semantic F31 менять не нужно.

Сначала создаётся accepted clarification, затем correction prompt.

## `SEMANTIC-BLOCKER`

Использовать, если корректная реализация требует изменить F31/canonical semantics.

Coding останавливается:

```text
blocker
→ design review
→ ADR/canonical update
→ freeze/version impact
→ только потом implementation
```

---

# 5. MODE-CORRECTION

Correction prompt пишется только для найденного defect.

Обязательные свойства:

- назвать точную причину defect;
- объяснить violated invariant;
- ограничить correction текущим `IS`;
- явно запретить следующий `IS`;
- перечислить required regression tests;
- потребовать targeted verification + full regression gate;
- сохранить existing design semantics;
- не разрешать unrelated refactor;
- попросить Conventional Commit message;
- по умолчанию запретить commit/push.

Correction prompt может ссылаться на новый accepted clarification, если ChatGPT сначала зафиксировал его в repository docs.

После push correction выполняется **новый независимый audit correction diff**, а не автоматическое принятие исходного step.

---

# 6. Correction diff audit

Для correction проверяется минимум:

1. base = implementation commit до correction;
2. head = correction commit;
3. diff минимален и относится к найденному defect;
4. regression tests действительно reproduces/закрывают defect;
5. forbidden scope не расширился;
6. targeted verification прошла;
7. full regression прошёл;
8. post-push CI подтверждён;
9. исходный invariant теперь механически enforced.

Если correction audit PASS, исходный implementation step может быть принят.

---

# 7. Правило независимости

Независимость audit означает:

```text
Codex report
≠
ChatGPT audit
```

ChatGPT должен самостоятельно:

- открыть remote commit/diff;
- прочитать critical production code;
- прочитать tests;
- сопоставить с docs;
- подумать о negative/bypass cases;
- проверить evidence настолько, насколько позволяет tool access.

Нельзя ограничиваться перефразированием отчёта Codex.

---

# 8. Правило глубины audit

Глубина зависит от риска step.

Особенно глубокий audit требуется для:

- identity/revision primitives;
- immutable snapshot/state representations;
- controlled construction;
- provenance/source ownership;
- DAG/scheduling/temporal ordering;
- commit/transaction machinery;
- private-state isolation;
- persistence/checkpoint;
- training revision activation;
- evaluation isolation;
- security/capability boundaries.

Чем ниже-level primitive и чем больше следующих шагов на него опираются, тем выше цена пропущенного edge case.

---

# 9. Что не является defect само по себе

Не требовать correction только потому, что:

- implementation выбрала один эквивалентный physical file split, разрешённый design;
- internal helper можно намеренно импортировать по private Python path, если supported public API boundary корректен;
- runtime type distinction сознательно обеспечивается static typing согласно accepted design;
- следующий слой validation намеренно принадлежит будущему `IS`;
- implementation более fail-closed, не меняя accepted semantics/API contract.

Audit должен отличать настоящий broken invariant от вкусового предпочтения reviewer.

---

# 10. Формат ответа audit

Рекомендуемый порядок:

1. идентифицировать проверенный commit;
2. дать короткий verdict;
3. перечислить подтверждённые ключевые invariants;
4. описать найденный defect, если он есть;
5. отдельно дать verification/CI status;
6. сказать, нужен ли correction prompt;
7. явно указать, можно ли открывать следующий `IS`.

Если correction нужен, готовую correction-инструкцию следует выдавать по правилам [`codex-instruction-authoring.md`](codex-instruction-authoring.md): как отдельный copy-ready writing block.

---

# 11. Exit conditions MODE-AUDIT

`MODE-AUDIT` завершён только одним из переходов:

```text
AUDIT-PASS
→ MODE-TRANSITION
```

```text
CORRECTION-REQUIRED
→ MODE-CORRECTION
```

```text
DOCUMENTATION-CLARIFICATION-REQUIRED
→ MODE-DESIGN
→ MODE-CORRECTION
```

```text
SEMANTIC-BLOCKER
→ design/ADR review
```

Нельзя молча открыть следующий implementation step внутри незавершённого audit.