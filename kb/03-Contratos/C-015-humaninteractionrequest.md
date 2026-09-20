---
id: "C-015"
tipo: contrato
nombre: "HumanInteractionRequest"
version: "v1"
capitulo: "CH-06"
tags: [contrato, c-015]
used_by: ["CMP-006"]
modified_by: []
articulos_constitucionales: ["INV-14", "INV-15", "INV-18", "INV-19"]
---

# HumanInteractionRequest (C-015)

> Contrato v1 — introducido en [[ch-06-human-interaction|CH-06]].

## Definición canónica

```text
STRUCT HumanInteractionRequest
    id: HumanInteractionRequestId
    type: HumanInteractionType
    callId: ToolCallId
    status: HumanInteractionStatus
    requestedAt: Timestamp
END
```

## Usado por

[[CMP-006-humaninteractionservice|CMP-006]]

## Modificado por

Ninguno

## Impacto constitucional

INV-14, INV-15, INV-18, INV-19

## Contexto del libro

- Introducido en: [[ch-06-human-interaction|CH-06]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
