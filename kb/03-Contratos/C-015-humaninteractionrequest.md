---
id: "C-015"
tipo: contrato
nombre: "HumanInteractionRequest"
version: "v2"
capitulo: "CH-06"
tags: [contrato, c-015]
used_by: ["CMP-006", "CMP-024"]
modified_by: ["CH-33"]
articulos_constitucionales: ["INV-14", "INV-15", "INV-18", "INV-19"]
---

# HumanInteractionRequest (C-015)

> Contrato **v2** — introducido en [[ch-06-human-interaction|CH-06]], modificado en [[ch-33-esperas-durables|CH-33]].

## Definición canónica

```text
STRUCT HumanInteractionRequest
    id: HumanInteractionRequestId
    type: HumanInteractionType
    callId: ToolCallId
    status: HumanInteractionStatus
    waitId: Optional<WaitId>
    requestedAt: Timestamp
END
```

## Usado por

[[CMP-006-humaninteractionservice|CMP-006]], [[CMP-024-resumptioncoordinator|CMP-024]]

## Modificado por

[[ch-33-esperas-durables|CH-33]]: agrega `waitId` (la espera estacionada que abrió esta solicitud; NULL = solicitud como en v1)

## Impacto constitucional

INV-14, INV-15, INV-18, INV-19

## Contexto del libro

- Introducido en: [[ch-06-human-interaction|CH-06]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
