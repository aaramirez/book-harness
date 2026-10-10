---
id: "C-055"
tipo: contrato
nombre: "DataSourceDescriptor"
version: "v1"
capitulo: "CH-42"
tags: [contrato, c-055]
used_by: ["CMP-029"]
modified_by: []
articulos_constitucionales: ["P-22", "P-38", "INV-E07", "INV-E26"]
---

# DataSourceDescriptor (C-055)

> Contrato v1 — introducido en [[ch-42-fuentes-de-datos|CH-42]].

## Definición canónica

```text
STRUCT DataSourceDescriptor
    sourceId: DataSourceId
    kind: DataSourceKind
    endpointRef: Text
    classification: Optional<DataClassificationLevel>
    access: DataAccessMode
    scopeRule: DataScopeRule
    connectionId: Optional<ConnectionId>
    credentialName: Optional<Text>
    freshnessSeconds: Optional<Integer>
END
```

## Usado por

[[CMP-029-retrievalengine|CMP-029]]

## Modificado por

Ninguno

## Impacto constitucional

P-22, P-38, INV-E07, INV-E26

## Contexto del libro

- Introducido en: [[ch-42-fuentes-de-datos|CH-42]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
