# ADR-0002 — Явная композиция и запрет runtime Service Locator

## Статус

`accepted`

## Связанный Design Update

`DU-02 — Dependency & Composition Rules`

## Канонический документ-владелец

[`../dependency-rules.md`](../dependency-rules.md)

---

# 1. Контекст

MINDRA проектируется как модульная исследовательская когнитивная архитектура, в которой:

- concrete Cortex backend должен быть заменяем;
- cognitive modules должны поддерживать ablation/control implementations;
- Training/Evaluation Runtime находятся вне логической границы Agent;
- future runtime может работать в одном процессе или быть распределённым;
- исследовательская валидность требует явного происхождения конфигурации и зависимостей;
- скрытые cross-module dependencies недопустимы.

После `DU-01` необходимо определить, кто знает о concrete implementations и как они попадают в работающую композицию.

---

# 2. Проблема

Нужно выбрать canonical composition model, который одновременно:

1. позволяет заменять concrete implementations;
2. не заставляет cognitive modules импортировать peers;
3. не превращает registry/container в скрытое глобальное состояние;
4. позволяет собирать разные experiment profiles;
5. поддерживает `NoOp`/`Dummy`/`Control` implementations;
6. не привязывает проект к конкретному DI framework;
7. допускает будущий plugin discovery;
8. остаётся понятным для Codex и architecture review.

---

# 3. Рассмотренные варианты

## Вариант A — direct concrete wiring в потребителях

Примерно:

```text
Policy создаёт конкретный Memory
Memory импортирует concrete storage
Agent сам создаёт Qwen backend
```

### Плюсы

- минимальный initial boilerplate;
- быстро для маленького прототипа.

### Минусы

- concrete dependencies протекают по архитектуре;
- подмена требует изменения потребителей;
- ablation становится специальной веткой кода;
- сложно отделить research effect от wiring;
- высок риск циклических импортов;
- смена Cortex/Memory backend затрагивает независимые модули.

**Решение:** отклонён как canonical model.

---

## Вариант B — global Service Locator / runtime container

Примерно:

```text
module → services.get("memory")
module → registry.resolve("cortex")
```

### Плюсы

- легко добавлять новые implementations;
- мало constructor parameters;
- центральное место регистрации.

### Минусы

- dependency не видна в contract модуля;
- runtime behavior зависит от global state;
- unit/ablation tests требуют манипуляции контейнером;
- повышается риск circular resolution;
- становится трудно понять provenance выбранного backend;
- скрытая подмена сервиса способна менять experiment semantics;
- service discovery проникает внутрь cognition.

**Решение:** отклонён как runtime dependency model.

Registry не запрещается полностью; запрещается его использование cognitive/runtime consumers как Service Locator.

---

## Вариант C — explicit Composition Root + dependency inversion

Семантика:

```text
configuration
     ↓
Composition Root
     ↓
resolve factories/providers
     ↓
construct concrete implementations
     ↓
inject contracts / assemble Agent
```

Registry при необходимости используется только внутри composition/discovery boundary.

### Плюсы

- dependencies явны;
- concrete knowledge централизовано;
- легко подменять implementations;
- удобно строить baseline/ablation profiles;
- Agent не зависит от experiment infrastructure;
- проще проверять import rules;
- не требует конкретного DI framework;
- совместимо с будущим plugin discovery.

### Минусы

- больше явного assembly-кода;
- необходимо дисциплинированно поддерживать composition boundary;
- без хорошей документации root может со временем превратиться в крупный bootstrap-компонент;
- required capabilities/compatibility придётся явно валидировать.

**Решение:** принят.

---

## Вариант D — обязательный внешний DI-container/framework

### Плюсы

- готовые lifecycle/scopes/registration возможности;
- меньше собственного wiring-кода при большом проекте.

### Минусы

- преждевременная framework dependency;
- DI-container semantics могут начать определять архитектуру;
- сложнее исследовать систему без знания framework;
- текущие exact contracts и lifecycle ещё не спроектированы.

**Решение:** не принимается и не запрещается как будущая implementation detail. Если позднее будет доказана необходимость конкретного container framework как архитектурного решения, требуется отдельный ADR.

---

# 4. Evidence

## Python structural contracts

Официальный `typing.Protocol` позволяет описывать structural interfaces без обязательного inheritance от concrete implementation.

Источник:

- https://docs.python.org/3/library/typing.html#typing.Protocol

Это показывает, что contract-first replaceability можно реализовать стандартными средствами Python без обязательного DI framework.

## Python plugin discovery

PyPA документирует plugin discovery по naming conventions, namespace packages и package metadata `entry points`.

Источники:

- https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/
- https://packaging.python.org/en/latest/specifications/entry-points/

Это подтверждает возможность позднее расширить composition discovery без превращения cognitive modules в самостоятельных загрузчиков plugins.

Эти механизмы являются evidence, а не обязательными implementation choices MINDRA.

---

# 5. Принятое решение

MINDRA принимает:

1. **явный Composition Root** как logical owner concrete assembly;
2. **dependency inversion** для заменяемых capabilities;
3. **explicit dependency passing** вместо runtime Service Locator;
4. optional registry/factory catalogue только на composition/discovery boundary;
5. возможность будущего plugin discovery только как responsibility composition layer;
6. запрет cognitive modules самостоятельно разрешать concrete dependencies из global container/registry;
7. запрет scattered backend construction внутри независимых потребителей.

---

# 6. Дополнительные invariants

## ADR2-01

Знание о concrete implementation должно быть максимально сосредоточено в composition/adapters layer.

## ADR2-02

Registry не является Agent state и не является runtime cognitive service bus.

## ADR2-03

Конфигурация сообщает Composition Root, **что собрать**, но cognitive module не использует глобальную конфигурацию для поиска peers.

## ADR2-04

`NoOp`/`Dummy`/`Control` implementations подключаются тем же composition mechanism, что и обычные implementations.

## ADR2-05

Временные feedback loops должны реализовываться будущей runtime/state semantics, а не взаимными concrete object dependencies.

---

# 7. Последствия

## Положительные

- заменяемость становится архитектурным свойством;
- Cortex backend можно изолировать;
- ablation/control configurations собираются системно;
- появляется естественная точка для validation/provenance;
- architecture tests смогут проверять import directions;
- future external plugins остаются возможными;
- local single-process и distributed deployment используют одну логическую composition semantics.

## Отрицательные / стоимость

- потребуется явный bootstrap/composition code;
- потребуется определить совместимость capabilities;
- нужно не допустить роста Composition Root в бизнес-/когнитивную логику;
- конфигурация и factories должны иметь строгую provenance;
- module contracts должны быть достаточно точными для реальной подмены.

---

# 8. Что решение намеренно не определяет

ADR не выбирает:

- Python `Protocol` как обязательный interface mechanism;
- конкретный DI-container;
- конкретную registry library;
- `entry points` как обязательный plugin mechanism;
- config library;
- окончательную структуру `src/`;
- exact constructor/factory signatures;
- module lifecycle;
- scheduler;
- `CognitiveState` implementation.

---

# 9. Обязательные consistency updates

После принятия ADR должны быть согласованы:

- `docs/design/dependency-rules.md`;
- `docs/design/decisions/README.md`;
- `docs/design/README.md`;
- `docs/design/current.md`;
- `AGENTS.md` в части обязательных dependency rules.

Exact contracts пока не создаются: соответствующие semantics будут определены в следующих `DU`.
