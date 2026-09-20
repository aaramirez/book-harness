---
id: "CMP-013"
tipo: componente
nombre: "AgentCommunicationGateway"
capitulo: "CH-15"
tags: [componente, cmp-013]
consumes: ["C-024", "C-025"]
produces: ["C-011", "C-024"]
articulos_constitucionales: ["P-18", "P-19", "P-20", "P-21", "P-25", "INV-E03", "INV-E04", "INV-E05", "INV-E06", "INV-18", "INV-19", "INV-20"]
---

# AgentCommunicationGateway (CMP-013)

> Componente introducido en [[ch-15-agent-communication-gateway|CH-15]] — parte del runtime del arnés.

## Responsabilidad

Adaptar mensajes semánticos hacia/desde protocolos de interoperabilidad externos (A2A u otros) exclusivamente a través de adapters, desacoplando el core de cualquier SDK, protocolo o transporte concreto — y verificar, sin redefinirlo, que una comunicación respaldada por un DelegationGrant respete el scope, el vencimiento y el ExecutionBudget acotado que ese grant ya declara — sin decidir si el estímulo que originó cualquiera de los dos runs comunicándose tenía derecho a arrancar, sin autorizar ninguna acción ya resuelta y sin decidir continuación de turno.

## Decisiones que posee (owns)

- Agent communication MUST use explicit semantic contracts. Protocols define interoperability; transports define delivery. Neither belongs inside Agent Core (cita literal, P-18)
- A2A or future interoperability standards MUST be integrated through AgentCommunicationGateway adapters. The core MUST NOT depend directly on an A2A SDK or a particular wire protocol (cita literal, P-19)
- distinguir siempre delegación interna de federación externa (boundary, P-20)
- verificar — nunca redefinir — que un DelegationGrant que respalda un mensaje siga vigente, cubra lo que el mensaje pide (scope) y respete el ExecutionBudget acotado que declara (INV-E06)
- rechazar por defecto (fail-closed) cuando un DelegationGrant declarado no se encuentra, no corresponde, expiró o no cubre el mensaje

## Decisiones que NO posee (does_not_own)

- decidir si el estímulo externo crudo que originó cualquiera de los dos runs comunicándose tenía siquiera derecho a arrancar (AdmissionController, CMP-012, ya introducido en CH-14 — pregunta anterior, sobre un ActivationRequest todavía sin agentId resuelto)
- autorizar una acción/tool call ya resuelta dentro de un run (PolicyEngine, CMP-005, ya introducido en CH-05 — distinto momento, distinta pregunta: "¿puede este mensaje cruzar hacia otro agente?" vs. "¿puede esta acción ejecutarse dentro de este run?")
- decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en CH-01)
- el protocolo de wire o el transporte concreto en sí — HTTP, gRPC, WebSocket, un SDK de A2A (Protocol Adapter / Transport Adapter, INV-E04, no un componente propio de este registry)
- revalidar la coherencia interna del ExecutionBudget embebido en un DelegationGrant (AgentCore, CMP-011, ya introducido en CH-11 — isExecutionBudgetCoherent ya existe ahí)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-024-agentcommunicationmessage|C-024]], [[C-025-delegationgrant|C-025]] |
| 🡐 Produce | [[C-011-harnesserror|C-011]], [[C-024-agentcommunicationmessage|C-024]] |

## Artículos constitucionales

P-18, P-19, P-20, P-21, P-25, INV-E03, INV-E04, INV-E05, INV-E06, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-15-agent-communication-gateway|CH-15]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
