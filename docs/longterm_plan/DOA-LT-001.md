## Metadata

- Project: DOA
- Doc type: longterm_plan
- ID: DOA-LT-001
- Status: draft
- Date: 2026-04-08
- Parent: DOA-IDEA-001

---

## Summary

Долгосрочный план **DocOps foundation** для DocOps Agent: от документной базы и workflow к устойчивой поддержке внедрения.

## Strategic Goal

Построить **doc-first foundation**: воспроизводимая структура артефактов, правила и трассируемость так, чтобы разработка не опиралась на неявный контекст.

## Time Horizon

**12–24 месяца** с момента bootstrap (оценочно; пересматривается новым `DOA-LT-<NNN>` при смене стратегии).

## Milestones

- **Documentation foundation** — стабильные `docs/` + `templates/`, согласованные metadata и naming
- **Workflow validation** — примеры документов, аудиты, первые accepted operational_plan циклы
- **Implementation support** — регулярные `implementation_snapshot` и решения в `decision_log`, связанные с реальной поставкой

## Risks

- **Рассинхрон** между публикацией (Notion) и Git — митигация: Git как source of truth
- **Накопление legacy** без явной политики — митигация: фиксировать в audit, не править задним числом без нового артефакта

## Expected Result

Рабочая модель DocOps Agent, в которой любой значимый сдвиг можно проследить по цепочке Parent и типам документов.
