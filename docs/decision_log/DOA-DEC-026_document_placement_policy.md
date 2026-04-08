# Decision: DOA-DEC-026
Date: 2026-04-08
Status: accepted

## Title
Использовать docs/<doc_type>/ как каноническое размещение документов проекта

## Context
На текущем этапе часть документов находится вне канонической структуры проекта,
в отдельном каталоге `tz/`. Это создаёт риск путаницы, дублирования и потери
traceability при дальнейшем выполнении operational_plan.

## Options considered
1. Оставить документы в `tz/` как рабочее место по умолчанию
2. Перенести канонические документы в `docs/<doc_type>/`, а `tz/` считать временной staging/import зоной
3. Хранить документы параллельно и в `tz/`, и в `docs/`

## Chosen solution
Каноническим размещением документов проекта считать только структуру:

- docs/idea_to_mvp/
- docs/architecture_draft/
- docs/decision_log/
- docs/implementation_snapshot/
- docs/audit_check/
- docs/longterm_plan/
- docs/midterm_plan/
- docs/operational_plan/

Каталог `tz/` считать временной staging/import зоной для входящих или промежуточных файлов,
но не источником истины.

## Why
- соответствует утверждённой doc_types model
- упрощает navigation и audit_check
- сохраняет единый source of truth
- снижает риск работы "мимо структуры"
- поддерживает planning-first и traceability

## Trade-offs
- потребуется отдельный план раскладки/миграции документов
- возможны дубли между `tz/` и `docs/` до завершения раскладки
- потребуется audit_check для фиксации legacy и конфликтов версий

## Placement rules
- Канонические документы хранятся только в `docs/<doc_type>/`
- Новые документы создаются сразу в каноническом каталоге
- `tz/` используется только как входящий буфер / staging area
- Документы из `tz/` не считаются активными, пока не разложены по `docs/`
- При конфликте версий активной считается версия, явно зафиксированная в `docs/`

## Follow-ups
- создать operational_plan на раскладку документов из `tz/`
- провести audit_check после раскладки
- зафиксировать legacy/double files отдельным implementation_snapshot
