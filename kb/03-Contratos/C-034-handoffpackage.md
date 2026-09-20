---
id: "C-034"
tipo: contrato
nombre: "HandoffPackage"
version: "v1"
capitulo: "CH-23"
tags: [contrato, c-034]
used_by: ["CMP-021"]
modified_by: []
articulos_constitucionales: ["INV-E12", "INV-19"]
---

# HandoffPackage (C-034)

> Contrato v1 — introducido en [[ch-23-handoff-coordinator|CH-23]].

## Definición canónica

```text
STRUCT HandoffPackage
    id: HandoffPackageId
    runId: RunId
    sessionId: SessionId
    reason: HandoffReason
    contextRef: Text
    transferTo: ActorId
    humanInteractionRef: Optional<HumanInteractionRequestId>
    status: HandoffStatus
    createdAt: Timestamp
END
```

## Usado por

[[CMP-021-handoffcoordinator|CMP-021]]

## Modificado por

Ninguno

## Impacto constitucional

INV-E12, INV-19

## Contexto del libro

- Introducido en: [[ch-23-handoff-coordinator|CH-23]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
