---
id: "C-038"
tipo: contrato
nombre: "BranchSummary"
version: "v1"
capitulo: "CH-29"
tags: [contrato, c-038]
used_by: ["CMP-010", "CMP-004"]
modified_by: []
articulos_constitucionales: ["P-08", "INV-12", "INV-13"]
---

# BranchSummary (C-038)

> Contrato v1 — introducido en [[ch-29-compactacion-sesiones-arbol|CH-29]].

## Definición canónica

```text
STRUCT BranchSummary
    abandonedTipId: SessionCheckpointId
    resumedFromId: SessionCheckpointId
    summary: CompactionSummary
    createdAt: Timestamp
END
```

## Usado por

[[CMP-010-sessionmanager|CMP-010]] · [[CMP-004-contextengine|CMP-004]]

## Modificado por

Ninguno

## Impacto constitucional

P-08, INV-12, INV-13

## Contexto del libro

- Introducido en: [[ch-29-compactacion-sesiones-arbol|CH-29]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
