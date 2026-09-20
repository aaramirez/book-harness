---
id: "C-019"
tipo: contrato
nombre: "EventSubscription"
version: "v1"
capitulo: "CH-09"
tags: [contrato, c-019]
used_by: ["CMP-009"]
modified_by: []
articulos_constitucionales: ["P-04", "P-12", "INV-18", "INV-19"]
---

# EventSubscription (C-019)

> Contrato v1 — introducido en [[ch-09-event-bus|CH-09]].

## Definición canónica

```text
STRUCT EventSubscription
    id: EventSubscriptionId
    subscriberRef: Text
    filter: Optional<EventFilter>
    status: EventSubscriptionStatus
    subscribedAt: Timestamp
END
```

## Usado por

[[CMP-009-eventbus|CMP-009]]

## Modificado por

Ninguno

## Impacto constitucional

P-04, P-12, INV-18, INV-19

## Contexto del libro

- Introducido en: [[ch-09-event-bus|CH-09]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
