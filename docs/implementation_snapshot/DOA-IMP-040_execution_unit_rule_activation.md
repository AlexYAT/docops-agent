# Metadata
Project: docops-agent  
Doc type: implementation_snapshot  
ID: DOA-IMP-040  
Status: accepted  
Date: 2026-04-25  
Parent: DOA-DEC-069  

---

# Title
Execution unit rule activation (one chat = one lifecycle)

---

# Summary
Зафиксировано внедрение операционного правила execution unit:

👉 1 chat = 1 IDEA lifecycle

---

# What changed

- введено ограничение на один lifecycle в рамках одного чата
- запрещено смешивание нескольких IDEA в одном чате
- введено правило закрытия чата после IMP/AUD

---

# System impact

- уменьшение размера контекста
- улучшение traceability
- повышение воспроизводимости циклов

---

# Evidence

- DOA-DEC-069 создан и принят
- правило применяется в текущем workflow

---

# Notes

- правило не требует изменений в коде или tooling
- применяется как операционная дисциплина
