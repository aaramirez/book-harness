---
id: "C-016"
tipo: contrato
nombre: "HumanInteractionResolution"
version: "v1"
capitulo: "CH-06"
tags: [contrato, c-016]
used_by: ["CMP-006"]
modified_by: []
articulos_constitucionales: ["INV-14", "INV-15", "INV-18", "INV-19"]
---

# HumanInteractionResolution (C-016)

> Contrato v1 — introducido en [[ch-06-human-interaction|CH-06]].

## Definición canónica

```text
STRUCT HumanInteractionResolution
    requestId: HumanInteractionRequestId
    outcome: HumanInteractionOutcome
    value: Optional<Value>
    resolvedBy: ActorId
    resolvedAt: Timestamp
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
