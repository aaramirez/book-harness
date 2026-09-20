---
id: "C-030"
tipo: contrato
nombre: "DataGovernanceLabel"
version: "v1"
capitulo: "CH-20"
tags: [contrato, c-030]
used_by: ["CMP-018"]
modified_by: []
articulos_constitucionales: ["P-22", "INV-E11", "INV-19"]
---

# DataGovernanceLabel (C-030)

> Contrato v1 — introducido en [[ch-20-data-governance|CH-20]].

## Definición canónica

```text
STRUCT DataGovernanceLabel
    id: DataGovernanceLabelId
    subjectRef: Text
    classification: DataClassificationLevel
    residencyRequirement: Optional<Text>
    retentionDeadline: Optional<Timestamp>
    legalHold: Boolean
    lineageRef: Optional<Text>
    classifiedAt: Timestamp
END
```

## Usado por

[[CMP-018-datagovernanceengine|CMP-018]]

## Modificado por

Ninguno

## Impacto constitucional

P-22, INV-E11, INV-19

## Contexto del libro

- Introducido en: [[ch-20-data-governance|CH-20]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
