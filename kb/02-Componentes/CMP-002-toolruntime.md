---
id: "CMP-002"
tipo: componente
nombre: "ToolRuntime"
capitulo: "CH-02"
tags: [componente, cmp-002]
consumes: ["C-004", "C-008"]
produces: ["C-009", "C-010", "C-011"]
articulos_constitucionales: ["P-03", "P-04", "P-05", "P-12", "P-13", "INV-04", "INV-05", "INV-06", "INV-07", "INV-18", "INV-19", "INV-20"]
---

# ToolRuntime (CMP-002)

> Componente introducido en [[ch-02-tool-runtime|CH-02]] — parte del runtime del arnés.

## Responsabilidad

Resolver la capability solicitada por un ToolCall, validar su input contra el schema declarado, ejecutar los hooks de extensión (beforeToolCall/afterToolCall) y coordinar la ejecución de la acción aprobada, devolviendo un ToolResult normalizado — sin decidir autorización, aprobación humana, enforcement de presupuesto ni qué implementación concreta satisface la capability solicitada.

## Decisiones que posee (owns)

- resolver tools/capabilities
- validar llamadas
- ejecutar hooks
- coordinar ejecución
- devolver resultados normalizados

## Decisiones que NO posee (does_not_own)

- policy evaluation y autorización de la acción (PolicyEngine, Article IV — no introducido en este capítulo)
- aprobación humana (HumanInteractionService — no introducido en este capítulo)
- enforcement de ExecutionBudget (ExecutionController — no introducido en este capítulo, mismo patrón ya establecido por AgentLoop en CH-01)
- registro y resolución de qué implementación satisface una capability solicitada (CapabilityRegistry, Article III — no introducido en este capítulo, es un componente distinto)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-008-toolcall|C-008]] |
| 🡐 Produce | [[C-009-toolresult|C-009]], [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]] |

## Artículos constitucionales

P-03, P-04, P-05, P-12, P-13, INV-04, INV-05, INV-06, INV-07, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-02-tool-runtime|CH-02]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
