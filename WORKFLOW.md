# DocOps Agent — базовый поток

## Порядок типов документов

1. **idea_to_mvp**
2. **architecture_draft**
3. **midterm_plan**
4. **operational_plan**
5. **decision_log**
6. **implementation_snapshot**
7. **audit_check**

## Правила

- Работа **вне `operational_plan` запрещена**, кроме стартового этапа **до первого accepted `operational_plan`**.
- Значимые решения фиксируются в **`decision_log`**.
- Содержательные изменения делаются **create-only** (новые версии/артефакты, без переписывания утверждённой истории).
