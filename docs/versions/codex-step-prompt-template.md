# Canonical Codex Step Prompt Template

## Статус

**Статус:** `accepted`  
**Назначение:** единый source of truth для задания Codex на один implementation step  
**Текущая revision шаблона:** `CSPT-01`

Этот файл задаёт обязательную структуру prompt для implementation-задач MINDRA.

Если version-specific `implementation-sequence.md`, старый чат или другой документ содержит встроенный пример prompt, **этот файл имеет приоритет как актуальный operational template**, если только accepted version documentation явно не задаёт более строгие дополнительные требования.

Шаблон не переопределяет `F31`, version design или implementation sequence. Он только гарантирует, что Codex получает их как обязательный контекст и выполняет implementation + verification единым шагом.

---

# 1. Принцип использования

Один prompt = один разрешённый `Vx.y-IS-XX`.

```text
version design
      ↓
implementation sequence
      ↓
canonical Codex prompt
      ↓
implementation
      ↓
targeted verification
      ↓
full current regression gate
      ↓
CI evidence, если доступно
      ↓
Codex report
      ↓
ChatGPT audit
```

Завершение Codex task не открывает следующий implementation step автоматически.

---

# 2. Обязательная verification-семантика

## 2.1. Targeted verification

Codex обязан выполнить все проверки, явно указанные у текущего implementation step.

Например:

```text
FAST
ARCH
targeted pytest paths
state-machine tests
version-specific smoke
```

Нельзя заменять более строгую указанную проверку более слабой.

## 2.2. Full local regression gate

Если текущая версия уже определяет полный локальный verification profile, Codex обязан выполнить его **после targeted verification и перед итоговым отчётом**.

Для `v0.1` после создания toolchain в `V0.1-IS-01` полный профиль:

```text
FULL-C0
```

то есть:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked lint-imports
uv run --locked pytest
uv build
```

Даже если конкретный step указывает `FAST + ARCH`, это означает targeted profile, а не разрешение пропустить уже существующий `FULL-C0` regression gate перед завершением Codex task.

Если full profile ещё не существует по accepted sequence, Codex выполняет всю уже доступную применимую часть и явно сообщает отсутствующий gate.

## 2.3. CI verification

Если изменения текущего task уже доступны как remote commit и Codex имеет доступ к GitHub Actions, он обязан проверить CI для этого commit.

Нужно различать минимум:

```text
CI PASS
CI FAIL
CI RUNNING
CI PENDING — изменения ещё не находятся на remote commit
CI NOT AVAILABLE — среда не имеет доступа к Actions
```

`PENDING` и `NOT AVAILABLE` **не являются `PASS`**.

Если CI падает:

1. изучить доступные logs;
2. определить причину;
3. исправлять только defect внутри scope текущего implementation step;
4. повторить применимые проверки;
5. не ослаблять CI/tests/contracts ради green.

Если текущая рабочая среда не создаёт/не отправляет commit, Codex не должен делать вид, что GitHub Actions проверил незапушенные изменения. В отчёте CI остаётся `PENDING` до появления remote commit и отдельного evidence.

## 2.4. Verification evidence

Итоговый отчёт обязан различать:

- команда была запущена и прошла;
- команда была запущена и упала;
- команда не применима;
- команда не запускалась/недоступна.

Запрещено выводить `PASS` только из того, что конфигурационный файл выглядит корректно.

---

# 3. Canonical prompt

Перед отправкой заменить placeholders:

```text
{STEP_ID}
{VERSION}
{STEP_TITLE}
```

При необходимости version documentation может добавить дополнительные обязательные файлы/commands, но не ослабить этот шаблон без accepted documentation update.

```text
Реализуй только этап {STEP_ID} — {STEP_TITLE} из docs/versions/{VERSION}/implementation-sequence.md.

Перед изменениями обязательно прочитай:
- AGENTS.md;
- docs/design/current.md;
- docs/design/contract-adr-consistency-freeze.md;
- docs/design/contracts/semantic-freeze-manifest.md;
- docs/design/version-roadmap.md;
- docs/versions/codex-step-prompt-template.md;
- docs/versions/{VERSION}/README.md;
- соответствующий раздел docs/versions/{VERSION}/implementation-sequence.md;
- все canonical design / ADR / contracts, перечисленные для текущего этапа.

Сначала проверь текущий repository HEAD/status и сверь:
- разрешён ли именно {STEP_ID} в docs/design/current.md;
- prerequisites этапа;
- scope и forbidden scope;
- acceptance criteria;
- VerificationObligations;
- уже существующие implementation/results предыдущих шагов.

Если prerequisite отсутствует, документация противоречива, требуется semantic/F31 change, либо возникает архитектурное решение, которое accepted documentation не разрешает принимать самостоятельно, остановись и выдай blocker report. Не выбирай новую архитектуру самостоятельно.

Реализуй только scope {STEP_ID}. Не реализуй следующий implementation step заранее и не добавляй abstractions/features «на будущее» вне текущего scope.

Не изменяй F31, accepted ADR, canonical design, accepted version design или implementation sequence, если текущий этап прямо этого не требует.

Не упрощай architecture/contracts ради прохождения тестов. Не ослабляй tests/type/import contracts, не скрывай failures через skip/xfail/quarantine, broad noqa/type: ignore или test-only production bypass.

После implementation выполни verification в таком порядке:

1. Все targeted checks/tests, явно требуемые текущим этапом.
2. Полный уже существующий local regression profile текущей версии. Для v0.1 после IS-01 это FULL-C0:
   uv sync --locked
   uv run --locked ruff check .
   uv run --locked ruff format --check .
   uv run --locked mypy src tests
   uv run --locked lint-imports
   uv run --locked pytest
   uv build
3. Если изменения доступны как remote commit и есть доступ к GitHub Actions — проверь CI этого commit на всех declared OS/jobs.
   - Если CI ещё выполняется: укажи RUNNING.
   - Если изменения ещё не на remote commit: укажи PENDING.
   - Если доступ к Actions отсутствует: укажи NOT AVAILABLE.
   - Не выдавай PENDING/NOT AVAILABLE за PASS.
4. Если проверка падает из-за defect текущего этапа, исправь defect только внутри scope этапа и повтори затронутые targeted + full regression checks.

В итоговом отчёте укажи:

1. Что реализовано.
2. Какие файлы изменены.
3. Были ли отклонения от implementation sequence; если нет — явно укажи «нет».
4. Какие VerificationObligations затронуты/закрыты и на каком уровне.
5. Таблицу verification evidence:
   - command/check;
   - PASS / FAIL / NOT APPLICABLE / NOT AVAILABLE / PENDING / RUNNING;
   - существенный вывод.
6. Отдельно:
   - targeted verification: PASS/FAIL;
   - full local regression profile: PASS/FAIL/NOT AVAILABLE;
   - GitHub Actions по каждому declared job/OS: PASS/FAIL/PENDING/RUNNING/NOT AVAILABLE.
7. Остались ли blockers, риски или незакрытые вопросы.
8. Можно ли считать implementation текущего step завершённой со стороны Codex.

Не обновляй самостоятельно docs/design/current.md, milestone status и не открывай следующий implementation step, если это не является прямым scope текущего этапа. Следующий step открывается только после отдельного ChatGPT audit.
```

---

# 4. Правила актуализации шаблона

Актуальность этого файла — обязательная часть version/implementation governance.

Проверка шаблона обязательна:

1. при принятии нового `docs/versions/vX.Y/README.md`;
2. при создании или изменении `docs/versions/vX.Y/implementation-sequence.md`;
3. при открытии каждого следующего implementation step после ChatGPT audit;
4. при изменении verification profiles, CI provider/jobs, обязательных commands, reporting/evidence semantics или source-of-truth paths;
5. при появлении нового класса обязательного verification evidence.

Если перечисленные изменения требуют поправки prompt, шаблон обновляется **тем же документационным патчем**.

Если изменений не требуется, файл не переписывается ради формальной активности; достаточно подтвердить, что `CSPT` остаётся применимым.

Нельзя хранить обязательное новое правило prompt только в истории чата.

---

# 5. Version-specific additions

Version-specific implementation sequence может добавлять требования поверх `CSPT`, например:

- accelerator profile;
- local model smoke;
- migration tests;
- dataset/checkpoint verification;
- remote-provider CI;
- additional evidence artifacts.

Такие требования должны быть записаны в version documentation и при необходимости отражены в новой revision этого шаблона.

Version-specific документ не должен молча ослаблять обязательные stop conditions, reporting truthfulness или verification evidence semantics этого файла.