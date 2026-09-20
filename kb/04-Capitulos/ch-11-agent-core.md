---
id: "CH-11"
tipo: capitulo
titulo: "\"AgentCore y el Nacimiento de un AgentState\""
tags: [capitulo, ch11]
introduces_components: ["CMP-011"]
introduces_contracts: ["C-021"]
articulos_constitucionales: ["P-06", "P-10", "P-12", "INV-01", "INV-08", "INV-09", "INV-16", "INV-18", "INV-19", "INV-20"]
---

# CH-11 — "AgentCore y el Nacimiento de un AgentState"

## Navegación

⬅ [[ch-10-session-manager|CH-10]] · **CH-11** · [[ch-12-camino-feliz|CH-12]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-011-agentcore|CMP-011]] — Representar la identidad de un agente — independiente de cualquier run o sesión particular —, validar su AgentConfig antes de que arranque cualquier ejecución, e instanciar el AgentState inicial de un nuevo run: asignar su runId, decidir su sessionId y producir la primera transición formal de Article V (CREATED → INITIALIZING) — sin decidir nada de lo que ocurre una vez que ese run ya está RUNNING.

### Contratos

- [[C-021-agentactivationrequest|C-021]] — AgentActivationRequest (impacto: P-06, P-10, INV-08, INV-09)


## Artículos constitucionales relevantes

P-06, P-10, P-12, INV-01, INV-08, INV-09, INV-16, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/11-agent-core/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
