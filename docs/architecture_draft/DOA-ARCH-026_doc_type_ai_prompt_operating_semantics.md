# architecture_draft — DOA-ARCH-026

## Metadata

- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-026
- Status: accepted
- Date: 2026-04-18
- Parent: DOA-DEC-060

_Create-only: новые версии — только новым ID; не переписывать принятые артефакты._

---

## Title

Операционная семантика `doc_type` для AI / prompt workflow (после DOA-DEC-060)

---

## Context

Решение **DOA-DEC-060** разводит `doc_type` (класс артефакта) и `status` (ось зрелости). Без явных правил интерпретации LLM и шаблоны prompt могут ошибочно трактовать подстроку `draft` в имени типа как статус документа или инициировать «исправление» типов вне lifecycle.

Данный документ задаёт **нормы чтения и генерации** для ChatGPT, Cursor и прочих AI-исполнителей в контуре DocOps.

---

## Rule

1. **`doc_type`** — имя **класса артефакта** (стабильный идентификатор типа в metadata и путях).
2. **`status`** — **состояние зрелости** конкретного экземпляра документа.
3. **Канонический путь** под `docs/` — **производный** от `doc_type`: `docs/<doc_type>/` (см. DOA-ARCH-025, Derive/Define).
4. В текущем **hardening cycle** **запрещены** semantic cleanup, переименование типов и миграции каталогов без отдельного lifecycle и DEC.

---

## Interpretation Rules

- Зрелость документа определяется **только** полем **`status`**, не подстроками внутри `doc_type`.
- Слова вроде `draft` в **`architecture_draft`** — часть **имени класса**, не обязательный намёк на `draft` в **`status`**.
- Сочетание **`architecture_draft` + `Status: accepted`** **допустимо** и не является противоречием.
- Запрещено выводить «этот документ черновик» **только** из наличия `draft` в `doc_type`.
- Любое предложение «переименовать тип / почистить семантику» в рамках текущего hardening без нового lifecycle — **вне scope** (см. DOA-DEC-060 Non-goals).

---

## Allowed Examples

- `Doc type: architecture_draft`, `Status: accepted` — валидная пара осей.
- `Doc type: decision_log`, `Status: draft` — зрелость черновая; класс артефакта при этом `decision_log`.
- Новый файл в `docs/architecture_draft/` с `doc_type: architecture_draft` — согласованное размещение.

---

## Forbidden Misinterpretations

- «`architecture_draft` значит документ обязан быть в статусе draft».
- «Нужно переименовать тип в `architecture`, потому что документ accepted».
- «Канонический путь можно выбрать по смыслу слова в типе, игнорируя `doc_type`».
- «Текущий hardening — хороший момент для массового переименования типов/папок».

---

## Consequences for Prompting

- System / Cursor rules и пользовательские prompt **должны** ссылаться на **DOA-DEC-060** и **настоящий документ** при описании метаданных.
- При создании документов AI **обязан** копировать `doc_type` **как есть** из политики репозитория; не «улучшать» имена типов.
- Валидационные и аудиторские prompt: проверять **`status`** и **`doc_type`** раздельно.

---

## Non-goals

- Изменение существующих accepted-документов.
- Переименование `doc_type`, каталогов, миграции.
- Semantic cleanup модели типов в этом цикле.

---

## Next Steps

- Встроить краткую отсылку в system prompt и `.cursor/rules` (отдельными изменениями, не подменяя DEC/ARCH).
- При необходимости — отдельный lifecycle и DEC на будущий semantic cleanup модели типов.
