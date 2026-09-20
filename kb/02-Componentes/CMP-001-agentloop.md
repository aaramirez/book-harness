---
id: "CMP-001"
tipo: componente
nombre: "AgentLoop"
capitulo: "CH-01"
tags: [componente, cmp-001]
consumes: ["C-002", "C-003", "C-004", "C-013"]
produces: ["C-003", "C-010", "C-011", "C-013"]
articulos_constitucionales: ["P-10", "P-12", "P-13", "INV-08", "INV-09", "INV-16", "INV-17", "INV-18", "INV-19"]
---

# AgentLoop (CMP-001)

> Componente introducido en [[ch-01-agent-loop|CH-01]] — parte del runtime del arnés.

## Responsabilidad

Coordinar el turn lifecycle de una ejecución cognitiva (el ciclo model → action → observation), decidir si otro turno de razonamiento debe ocurrir y producir la transición de AgentRunStatus y el AgentEvent correspondientes — sin ejecutar directamente ningún side effect.

## Decisiones que posee (owns)

- turn lifecycle
- model → action → observation cycle (la decisión de continuar el ciclo, no su ejecución)
- continuation
- completion
- coordinación de la ejecución cognitiva

## Decisiones que NO posee (does_not_own)

- autorización
- rendering
- almacenamiento concreto
- APIs específicas de proveedores
- operational continuation (budgets / cancelación / deadlines — Article IV asigna esta decisión a ExecutionController, preview, no introducido en este capítulo)
- ejecución de una tool call aprobada (ToolRuntime, preview, no introducido en este capítulo)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-002-agentconfig|C-002]], [[C-003-agentstate|C-003]], [[C-004-executioncontext|C-004]], [[C-013-agentrunstatus|C-013]] |
| 🡐 Produce | [[C-003-agentstate|C-003]], [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-013-agentrunstatus|C-013]] |

## Artículos constitucionales

P-10, P-12, P-13, INV-08, INV-09, INV-16, INV-17, INV-18, INV-19

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-01-agent-loop|CH-01]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
