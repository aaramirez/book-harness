---
id: "CMP-009"
tipo: componente
nombre: "EventBus"
capitulo: "CH-09"
tags: [componente, cmp-009]
consumes: ["C-010"]
produces: ["C-011", "C-019"]
articulos_constitucionales: ["P-04", "P-11", "P-12", "P-25", "INV-18", "INV-19", "INV-20"]
---

# EventBus (CMP-009)

> Componente introducido en [[ch-09-event-bus|CH-09]] — parte del runtime del arnés.

## Responsabilidad

Distribuir cada AgentEvent ya producido por cualquier otro componente del runtime hacia los consumidores desacoplados que se hayan suscrito — registrando cada suscripción activa y entregando (fan-out) el evento a las que hagan match por filtro — sin decidir qué información contiene ese evento, sin interpretar ni actuar sobre él, sin persistir historial de sesión de forma durable y sin decidir continuación de turno ni ninguna otra decisión arquitectónica.

## Decisiones que posee (owns)

- registrar una suscripción de un consumidor desacoplado (subscriberRef opaco y un filtro opcional)
- cancelar una suscripción ya registrada
- distribuir (fan-out) cada AgentEvent ya producido por cualquier componente hacia las suscripciones activas que hagan match por filtro
- desacoplar al productor de un AgentEvent de sus consumidores (cita literal de Article III)

## Decisiones que NO posee (does_not_own)

- decidir qué información va dentro de un AgentEvent (cada componente productor ya lo decide al construir su propio AgentEvent — CMP-001..CMP-008, ya introducidos)
- interpretar o actuar sobre un AgentEvent distribuido (Logs/Tracing/Audit/Replay/Analytics/Evals/Cost Analysis/Debugging/UI, Article X — ninguno es un componente propio de este registry todavía)
- persistir historial de sesión de forma durable para reconstrucción posterior (SessionManager, Article III — no introducido, preview)
- decidir continuación de turno o cualquier otra decisión arquitectónica (AgentLoop/PolicyEngine/ExecutionController, ya introducidos)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-010-agentevent|C-010]] |
| 🡐 Produce | [[C-011-harnesserror|C-011]], [[C-019-eventsubscription|C-019]] |

## Artículos constitucionales

P-04, P-11, P-12, P-25, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-09-event-bus|CH-09]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
