---
id: "CH-09"
tipo: capitulo
titulo: "\"EventBus y la Distribución Desacoplada de un Evento Ya Producido\""
tags: [capitulo, ch09]
introduces_components: ["CMP-009"]
introduces_contracts: ["C-019"]
articulos_constitucionales: ["P-04", "P-11", "P-12", "P-25", "INV-18", "INV-19", "INV-20"]
---

# CH-09 — "EventBus y la Distribución Desacoplada de un Evento Ya Producido"

## Navegación

⬅ [[ch-08-capability-registry|CH-08]] · **CH-09** · [[ch-10-session-manager|CH-10]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-009-eventbus|CMP-009]] — Distribuir cada AgentEvent ya producido por cualquier otro componente del runtime hacia los consumidores desacoplados que se hayan suscrito — registrando cada suscripción activa y entregando (fan-out) el evento a las que hagan match por filtro — sin decidir qué información contiene ese evento, sin interpretar ni actuar sobre él, sin persistir historial de sesión de forma durable y sin decidir continuación de turno ni ninguna otra decisión arquitectónica.

### Contratos

- [[C-019-eventsubscription|C-019]] — EventSubscription (impacto: P-04, P-12, INV-18, INV-19)


## Artículos constitucionales relevantes

P-04, P-11, P-12, P-25, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/09-event-bus/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
