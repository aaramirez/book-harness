---
id: "C-056"
tipo: contrato
nombre: "RetrievedCandidate"
version: "v1"
capitulo: "CH-42"
tags: [contrato, c-056]
used_by: ["CMP-029", "CMP-004"]
modified_by: []
articulos_constitucionales: ["P-14", "INV-E11", "INV-E26"]
---

# RetrievedCandidate (C-056)

> Contrato v1 — introducido en [[ch-42-fuentes-de-datos|CH-42]].

## Definición canónica

```text
STRUCT RetrievedCandidate
    candidateId: RetrievedCandidateId
    sourceId: DataSourceId
    content: Value
    provenance: Text
    classification: DataClassificationLevel
    score: Number
    observedAt: Timestamp
    label: Optional<DataGovernanceLabel>
END
```

## Usado por

[[CMP-029-retrievalengine|CMP-029]], [[CMP-004-contextengine|CMP-004]]

## Modificado por

Ninguno

## Impacto constitucional

P-14, INV-E11, INV-E26

## Contexto del libro

- Introducido en: [[ch-42-fuentes-de-datos|CH-42]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
