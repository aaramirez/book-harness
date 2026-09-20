---
id: "CMP-021"
tipo: componente
nombre: "HandoffCoordinator"
capitulo: "CH-23"
tags: [componente, cmp-021]
consumes: ["C-004"]
produces: ["C-010", "C-011", "C-034"]
articulos_constitucionales: ["P-13", "INV-E12", "INV-18", "INV-19", "INV-20"]
---

# HandoffCoordinator (CMP-021)

> Componente introducido en [[ch-23-handoff-coordinator|CH-23]] — parte del runtime del arnés.

## Responsabilidad

Empaquetar un HandoffPackage estructurado cuando la decisión de transferir el control COMPLETO de un run/sesión a un humano ya se tomó — con campos estructurados que nunca colapsan a un resumen de prosa libre — sin decidir CUÁNDO debe ocurrir ese handoff, sin pedir o persistir una decisión puntual dentro de un turno en curso, y sin ejecutar ninguna acción una vez que el humano toma control.

## Decisiones que posee (owns)

- A human handoff transfers a structured HandoffPackage rather than only prose (cita literal, INV-E12) — construir, en exclusiva, el paquete estructurado que representa la transferencia COMPLETA de control de un run/sesión a un humano, nunca solo un bloque de texto libre resumiendo la situación
- correlacionar, opcionalmente, un HandoffPackage con una HumanInteractionRequest ya existente (CMP-006, CH-06) vía una referencia reusada, sin modificar ese contrato
- rechazar por defecto (fail-closed) un HandoffPackage sin referencia al run/sesión que se transfiere

## Decisiones que NO posee (does_not_own)

- pedir o persistir una decisión puntual dentro de un turno en curso (HumanInteractionService, CMP-006, ya introducido en CH-06 — la frontera más importante de este capítulo: HumanInteractionService representa y resuelve UNA decisión puntual dentro de un turno que sigue en marcha; HandoffCoordinator empaqueta la transferencia del CONTROL COMPLETO de un run/sesión, nunca una decisión aislada dentro de él)
- decidir CUÁNDO debe ocurrir un handoff (OperationalController, CMP-016, ya introducido en CH-18, vía un kill switch; ExecutionController, CMP-007, ya introducido en CH-07, vía terminación; o PolicyEngine, CMP-005, ya introducido en CH-05 — HandoffCoordinator construye el paquete UNA VEZ que esa decisión ya se tomó, nunca antes)
- ejecutar cualquier acción una vez que el humano toma control del run/sesión transferido (Preview, infraestructura de borde — fuera de alcance de este capítulo)
- transportar el HandoffPackage a través de ningún canal concreto (Channel Adapter, concepto de infraestructura de borde ya declarado por HumanInteractionService, CH-06 — no un componente propio de Article III / del registry)
- generar por sí mismo el runId, el sessionId, la reason, el contextRef o el transferTo — todas llegan como señales de entrada ya resueltas (mismo patrón que subjectRef en CH-19/CH-20/CH-22, o runId/topology en CH-21)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-034-handoffpackage|C-034]] |

## Artículos constitucionales

P-13, INV-E12, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-23-handoff-coordinator|CH-23]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
