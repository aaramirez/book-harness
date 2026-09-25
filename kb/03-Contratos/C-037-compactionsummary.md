---
id: "C-037"
tipo: contrato
nombre: "CompactionSummary"
version: "v1"
capitulo: "CH-29"
tags: [contrato, c-037]
used_by: ["CMP-004", "CMP-010"]
modified_by: []
articulos_constitucionales: ["P-01", "P-14", "INV-07"]
---

# CompactionSummary (C-037)

> Contrato v1 — introducido en [[ch-29-compactacion-sesiones-arbol|CH-29]].

## Definición canónica

```text
STRUCT CompactionSummary
    goal: Text
    constraints: List<Text>
    progress: List<Text>
    decisions: List<Text>
    nextSteps: List<Text>
    criticalContext: List<Text>
    touchedFiles: List<Text>
    firstKeptMessageId: MessageId
    provenance: Text
END
```

## Usado por

[[CMP-004-contextengine|CMP-004]] · [[CMP-010-sessionmanager|CMP-010]]

## Modificado por

Ninguno

## Impacto constitucional

P-01, P-14, INV-07

## Contexto del libro

- Introducido en: [[ch-29-compactacion-sesiones-arbol|CH-29]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
