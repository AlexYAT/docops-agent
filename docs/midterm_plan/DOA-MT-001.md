## Metadata

- Project: DOA
- Doc type: midterm_plan
- ID: DOA-MT-001
- Status: draft
- Date: 2026-04-08
- Parent: DOA-LT-001

---

## Summary

Среднесрочный план на этап **MVP bootstrap DocOps Agent**: шаблоны, примеры документов и первый аудит согласованности.

## Goal

Довести до состояния «можно показать новому участнику полный сквозной пример и правила без устных пояснений».

## Milestones

### MT-01

- **ID**: MT-01
- **Title**: templates ready
- **Done when**: все doc_types имеют заполненный `*.template.md` в `templates/` и единый блок Metadata

### MT-02

- **ID**: MT-02
- **Title**: sample docs ready
- **Done when**: по одному примеру на doc_type в `docs/`, осмысленный контент, корректные Parent и ID

### MT-03

- **ID**: MT-03
- **Title**: audit completed
- **Done when**: выполнен `audit_check` по naming/metadata/Parent, зафиксированы findings и итоговый result

## Dependencies

- Принято решение `DOA-DEC-025` (шаблоны как основной механизм стандартизации)
- Наличие `WORKFLOW.md` и структуры каталогов из T01

## Risks

- Скрытые несоответствия между историческими и новыми ID — выявляется аудитом, не правкой истории в том же шаге

## Expected Result

Репозиторий содержит согласованную **цепочку примеров** от IDEA до AUD и готов к следующему operational циклу.
