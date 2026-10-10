---
id: "C-062"
tipo: contrato
nombre: "TraceCapturePolicy"
version: "v1"
capitulo: "CH-46"
tags: [contrato, c-062]
used_by: ["CMP-018", "CMP-009"]
modified_by: []
articulos_constitucionales: ["P-37", "INV-E23"]
---

# TraceCapturePolicy (C-062)

> Contrato v1 — introducido en [[ch-46-observabilidad-por-audiencia|CH-46]].

## Definición canónica

```text
STRUCT TraceCapturePolicy
    audience: AudienceKind
    ceiling: DataClassificationLevel
    captureBodies: Boolean
END
```

## Usado por

[[CMP-018-datagovernanceengine|CMP-018]], [[CMP-009-eventbus|CMP-009]]

## Modificado por

Ninguno

## Impacto constitucional

P-37, INV-E23

## Contexto del libro

- Introducido en: [[ch-46-observabilidad-por-audiencia|CH-46]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
