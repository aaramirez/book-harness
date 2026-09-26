---
id: "C-022"
tipo: contrato
nombre: "ActivationRequest"
version: "v2"
capitulo: "CH-14"
tags: [contrato, c-022]
used_by: ["CMP-012", "CMP-025"]
modified_by: ["CH-34"]
articulos_constitucionales: ["P-16", "INV-E01"]
---

# ActivationRequest (C-022)

> Contrato **v2** — introducido en [[ch-14-admission-controller|CH-14]], modificado en [[ch-34-canales-continuacion|CH-34]].

## Definición canónica

```text
STRUCT ActivationRequest
    id: ActivationRequestId
    sourceRef: Text
    sourceKind: Optional<SourceKind>
    externalIdentityRef: Text
    continuationAddress: Optional<ContinuationAddress>
    payload: Value
    receivedAt: Timestamp
END
```

## Usado por

[[CMP-012-admissioncontroller|CMP-012]], [[CMP-025-continuationregistry|CMP-025]]

## Modificado por

[[ch-34-canales-continuacion|CH-34]]: agrega `sourceKind` (API, CHANNEL, WEBSOCKET, WEBHOOK, SCHEDULE, STREAM_EVENT) y `continuationAddress` (NULL = activa una sesión nueva, como en v1)

## Impacto constitucional

P-16, INV-E01

## Contexto del libro

- Introducido en: [[ch-14-admission-controller|CH-14]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
