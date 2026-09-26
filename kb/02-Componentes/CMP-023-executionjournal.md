---
id: "CMP-023"
tipo: componente
nombre: "ExecutionJournal"
capitulo: "CH-32"
tags: [componente, cmp-023]
consumes: ["C-004", "C-007", "C-008", "C-009"]
produces: ["C-010", "C-011", "C-042", "C-043"]
articulos_constitucionales: ["P-23", "P-32", "INV-13", "INV-E16", "INV-E17", "INV-18", "INV-19", "INV-20"]
---

# ExecutionJournal (CMP-023)

> Componente introducido en [[ch-32-pasos-durables|CH-32]] — parte del runtime del arnés (plano Reliability).

## Responsabilidad

Registrar, paso por paso, el progreso durable de un turno — una llamada al modelo y la tool call que su respuesta propuso — escribiendo cada hecho antes del efecto siguiente, declarar un paso COMMITTED solo cuando todo su resultado está persistido, y decidir, al recuperar un run interrumpido, qué hacer con cada paso del journal — sin ejecutar tools, sin invocar al modelo, sin decidir por sí mismo si un efecto cuyo resultado se desconoce puede repetirse, sin guardar la historia de la sesión y sin decidir si el run puede continuar contra su presupuesto.

## Decisiones que posee (owns)

- A turn MUST be decomposed into steps (one model call and its inline tool calls). Each step MUST be recorded as committed before its effects are considered durable, and recovery MUST reason per step, not per turn (cita literal, P-32)
- Process memory MUST NOT be the source of truth for durable runs (cita literal, P-23) — el journal, no el proceso, es la fuente de verdad del progreso de un turno
- Una ejecución durable debe poder reconstruirse desde estado persistido suficiente (cita literal, INV-13) — decidir qué es "suficiente" a nivel de paso
- declarar un paso COMMITTED solo cuando su respuesta y su resultado están persistidos, y rechazar (fail-closed) cualquier escritura sobre un paso ya COMMITTED
- A committed step is never re-executed during recovery (cita literal, INV-E16) — decidir, por paso, la RecoveryAction

## Decisiones que NO posee (does_not_own)

- decidir si un efecto cuyo resultado se desconoce puede re-ejecutarse ([[CMP-015-idempotencyguard|IdempotencyGuard]], CH-17/CH-30 — la frontera más importante: el journal detecta QUÉ paso quedó pendiente; IdempotencyGuard decide SI el efecto se repite, INV-E17)
- persistir la historia y los checkpoints de la sesión ([[CMP-010-sessionmanager|SessionManager]], CH-10)
- decidir si el run puede seguir contra su ExecutionBudget ([[CMP-007-executioncontroller|ExecutionController]], CH-07)
- ejecutar la tool call ([[CMP-002-toolruntime|ToolRuntime]]) ni invocar al modelo ([[CMP-003-modelgateway|ModelGateway]])
- el mecanismo físico de escritura durable y atómica (infraestructura de borde, Preview)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-007-modelresponse|C-007]], [[C-008-toolcall|C-008]], [[C-009-toolresult|C-009]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-042-steprecord|C-042]], [[C-043-recoverydecision|C-043]] |

## Artículos constitucionales

P-23, P-32, INV-13, INV-E16, INV-E17, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-32-pasos-durables|CH-32]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
