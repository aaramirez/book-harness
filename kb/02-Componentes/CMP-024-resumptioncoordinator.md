---
id: "CMP-024"
tipo: componente
nombre: "ResumptionCoordinator"
capitulo: "CH-33"
tags: [componente, cmp-024]
consumes: ["C-003", "C-004", "C-015", "C-040"]
produces: ["C-010", "C-011", "C-044", "C-045"]
articulos_constitucionales: ["P-23", "P-33", "INV-14", "INV-15", "INV-E18", "INV-18", "INV-19", "INV-20"]
---

# ResumptionCoordinator (CMP-024)

> Componente introducido en [[ch-33-esperas-durables|CH-33]] — parte del runtime del arnés (plano Execution).

## Responsabilidad

Estacionar durablemente un run que espera — una aprobación, una respuesta, una autorización interactiva o una decisión sobre un límite de presupuesto — sin retener cómputo, y decidir, cuando llega una entrega por cualquier canal, qué espera estacionada reanuda y si quien responde está autorizado para ella — sin representar ni resolver la solicitud humana, sin decidir si una acción requiere aprobación, sin ejecutar la acción, sin transportar la entrega por un canal concreto y sin tocar jamás un token.

## Decisiones que posee (owns)

- Approvals, questions, interactive authorizations and budget limits MUST park the run durably. A parked run MUST NOT hold compute, and MUST be resumable by a delivery arriving through any authorized channel (cita literal, P-33)
- A delivery resumes only the wait it addresses, and only if its responder is authorized for it (cita literal, INV-E18) — encontrar la espera por su waitId explícito, nunca inferirla, y validar al que responde contra la regla de la espera
- decidir el AgentRunStatus de un run estacionado: WAITING_FOR_HUMAN para aprobaciones y preguntas, PAUSED para autorizaciones y límites de presupuesto (primer uso real de PAUSED)
- representar la espera de una autorización interactiva (AuthorizationChallenge) sin contener credenciales
- rechazar por defecto (fail-closed) una entrega a una espera ya reanudada, vencida o no dirigida, y una autorización que pueda responder alguien distinto del usuario que debe autorizar

## Decisiones que NO posee (does_not_own)

- representar la solicitud humana, persistirla y recibir su resolución ([[CMP-006-humaninteractionservice|HumanInteractionService]], CH-06 — la frontera más importante: la SOLICITUD y su RESOLUCIÓN son de HumanInteractionService; la ESPERA es de ResumptionCoordinator)
- decidir SI una acción requiere aprobación ([[CMP-005-policyengine|PolicyEngine]], CH-05)
- ejecutar la acción aprobada ([[CMP-002-toolruntime|ToolRuntime]]) ni decidir si el turno continúa ([[CMP-001-agentloop|AgentLoop]])
- detectar que falta una credencial ni guardar el token ([[CMP-014-credentialbroker|CredentialBroker]], CH-16 — INV-E08)
- decidir o ampliar el presupuesto ([[CMP-007-executioncontroller|ExecutionController]], CH-07)
- transportar la entrega por un canal concreto (Channel Adapter, P-11 — infraestructura de borde)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-003-agentstate|C-003]], [[C-004-executioncontext|C-004]], [[C-015-humaninteractionrequest|C-015]], [[C-040-principal|C-040]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-044-parkedwait|C-044]], [[C-045-authorizationchallenge|C-045]] |

## Artículos constitucionales

P-23, P-33, INV-14, INV-15, INV-E18, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-33-esperas-durables|CH-33]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
