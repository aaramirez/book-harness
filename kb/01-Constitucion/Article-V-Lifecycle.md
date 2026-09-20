---
id: article-v
tipo: constitucion
tags: [constitucion, articulo]
---

# Artículo V — Ciclo de Vida (Lifecycle)

Define el **diagrama de estados formal** de un AgentRun: CREATED → INITIALIZING → RUNNING → (WAITING_FOR_MODEL / WAITING_FOR_TOOL / WAITING_FOR_HUMAN / PAUSED) → COMPLETED / FAILED / CANCELLED / EXPIRED. Ningún componente puede inventar transiciones que el contrato [[C-013-agentrunstatus|AgentRunStatus (C-013)]] no reconoce. AgentCore materializa la primera transición (CREATED → INITIALIZING) en CH-11.

Ver también: [[Architecture-Constitution|Constitución]] · [[Index|Mapa del libro]]
