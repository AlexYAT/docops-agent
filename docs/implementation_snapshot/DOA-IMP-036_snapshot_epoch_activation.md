# DOA-IMP-036 — Snapshot epoch activation

## Metadata

- Project: docops-agent
- Doc type: implementation_snapshot
- ID: DOA-IMP-036
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-OP-037

---

## Summary

Зафиксирована активация новой controlled эпохи после создания fixed snapshot DOA-FSN-002.

Система переведена в snapshot-driven режим, где:

- legacy слой заморожен
- controlled зона является единственным источником operational truth
- все новые документы создаются только post-snapshot

---

## Implementation

Выполнено:

- создан DOA-FSN-002 как boundary snapshot
- зафиксирован scope snapshot
- зафиксированы validator/gate состояния "as is"
- определена новая epoch (controlled post-snapshot)
- установлены правила linking и usage

---

## Operational Mode

Система переведена в режим:

- epoch-based execution
- dual-mode semantics:
  - legacy = read-only historical layer
  - controlled = active execution layer

---

## Rules Activated

После snapshot активированы следующие правила:

- новые документы создаются только после DOA-FSN-002
- ссылки на legacy допускаются только через snapshot semantics
- legacy findings не используются как блокер execution
- controlled зона — единственный источник принятия решений

---

## Validation

Подтверждено:

- snapshot создан и принят
- boundary определён
- controlled epoch активирована
- правила использования задокументированы

---

## Notes

Это первый момент, когда система DocOps Agent полностью перешла в snapshot-driven режим.

---

## Consequences

- вся дальнейшая разработка ведётся только в controlled зоне
- новые проекты DocOps должны стартовать после DOA-FSN-002
- legacy больше не участвует в operational принятии решений
