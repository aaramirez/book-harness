---
id: "C-028"
tipo: contrato
nombre: "ControlDirective"
version: "v1"
capitulo: "CH-18"
tags: [contrato, c-028]
used_by: ["CMP-016"]
modified_by: []
articulos_constitucionales: ["P-30", "INV-E14", "INV-19"]
---

# ControlDirective (C-028)

> Contrato v1 — introducido en [[ch-18-operational-controller|CH-18]].

## Definición canónica

```text
STRUCT ControlDirective
    id: ControlDirectiveId
    type: ControlDirectiveType
    targetRef: Text
    issuedBy: ActorId
    status: ControlDirectiveStatus
    issuedAt: Timestamp
    appliedAt: Optional<Timestamp>
END
```

## Usado por

[[CMP-016-operationalcontroller|CMP-016]]

## Modificado por

Ninguno

## Impacto constitucional

P-30, INV-E14, INV-19

## Contexto del libro

- Introducido en: [[ch-18-operational-controller|CH-18]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
