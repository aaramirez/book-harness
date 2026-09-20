---
id: "CMP-011"
tipo: componente
nombre: "AgentCore"
capitulo: "CH-11"
tags: [componente, cmp-011]
consumes: ["C-002", "C-012", "C-021"]
produces: ["C-003", "C-004", "C-010", "C-011"]
articulos_constitucionales: ["P-06", "P-10", "P-12", "INV-01", "INV-08", "INV-09", "INV-16", "INV-18", "INV-19", "INV-20"]
---

# AgentCore (CMP-011)

> Componente introducido en [[ch-11-agent-core|CH-11]] — parte del runtime del arnés.

## Responsabilidad

Representar la identidad de un agente — independiente de cualquier run o sesión particular —, validar su AgentConfig antes de que arranque cualquier ejecución, e instanciar el AgentState inicial de un nuevo run: asignar su runId, decidir su sessionId y producir la primera transición formal de Article V (CREATED → INITIALIZING) — sin decidir nada de lo que ocurre una vez que ese run ya está RUNNING.

## Decisiones que posee (owns)

- representar y coordinar las primitives fundamentales del agente
- representar la identidad/definición del agente, independiente de cualquier run o sesión particular
- validar un AgentConfig antes de que arranque cualquier ejecución
- instanciar el AgentState inicial de un nuevo run (asignar runId, decidir sessionId)
- la transición CREATED → INITIALIZING (Article V)

## Decisiones que NO posee (does_not_own)

- UI (cita literal Article III — INV-16)
- persistencia específica (cita literal Article III — SessionManager, CMP-010, ya introducido en CH-10, posee la persistencia durable de la historia de una sesión)
- proveedores (cita literal Article III — ModelGateway, CMP-003, ya introducido en CH-03, posee selección/invocación de provider — INV-01)
- business integrations (cita literal Article III — sin componente propio todavía en este registry; fuera de alcance genérico de BH-v0.1)
- decidir si otro turno de razonamiento debe ocurrir una vez que el run ya está RUNNING (AgentLoop, CMP-001, ya introducido en CH-01 — AgentCore entrega el testigo a AgentLoop después de INITIALIZING, nunca compite con él)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-002-agentconfig|C-002]], [[C-012-executionbudget|C-012]], [[C-021-agentactivationrequest|C-021]] |
| 🡐 Produce | [[C-003-agentstate|C-003]], [[C-004-executioncontext|C-004]], [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]] |

## Artículos constitucionales

P-06, P-10, P-12, INV-01, INV-08, INV-09, INV-16, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-11-agent-core|CH-11]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
