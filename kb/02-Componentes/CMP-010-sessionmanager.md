---
id: "CMP-010"
tipo: componente
nombre: "SessionManager"
capitulo: "CH-10"
tags: [componente, cmp-010]
consumes: ["C-003", "C-004"]
produces: ["C-010", "C-011", "C-020"]
articulos_constitucionales: ["P-04", "P-08", "P-23", "INV-12", "INV-13", "INV-18", "INV-19", "INV-20"]
---

# SessionManager (CMP-010)

> Componente introducido en [[ch-10-session-manager|CH-10]] — parte del runtime del arnés.

## Responsabilidad

Persistir y actualizar la historia de una sesión mediante checkpoints construidos a partir de un AgentState ya producido por una ejecución existente, reconstruir un SessionState completo desde un checkpoint ya persistido, y crear una rama nueva de sesión a partir de un checkpoint existente — sin poseer el estado operativo de la ejecución en curso, sin persistir las solicitudes de interacción humana que HumanInteractionService ya persiste por su cuenta, sin decidir continuación de turno y sin distribuir eventos.

## Decisiones que posee (owns)

- persistencia
- recuperación
- branching
- checkpoints
- reconstrucción

## Decisiones que NO posee (does_not_own)

- el estado operativo de una ejecución en curso (AgentState, C-003, ya existente — producido y poseído en exclusiva por AgentLoop, CMP-001, ya introducido en CH-01; P-08/INV-12 exigen que ambos permanezcan conceptualmente independientes: SessionManager solo persiste una COPIA inmutable de un AgentState ya producido, nunca lo posee ni lo trata como fuente de verdad de la ejecución activa)
- persistir sus propias solicitudes de interacción humana pendientes (HumanInteractionService, CMP-006, ya introducido en CH-06 — ya tiene esa responsabilidad acotada y propia; SessionManager no la absorbe ni la duplica)
- decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en CH-01)
- distribuir eventos del runtime a consumidores desacoplados (EventBus, CMP-009, ya introducido en CH-09 — aunque SessionManager podría, en un capítulo futuro, suscribirse como un consumidor más de EventBus para reconstruir historial a partir de eventos ya distribuidos)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-003-agentstate|C-003]], [[C-004-executioncontext|C-004]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-020-sessionstate|C-020]] |

## Artículos constitucionales

P-04, P-08, P-23, INV-12, INV-13, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-10-session-manager|CH-10]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
