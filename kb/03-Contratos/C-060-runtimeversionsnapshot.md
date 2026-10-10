---
id: "C-060"
tipo: contrato
nombre: "RuntimeVersionSnapshot"
version: "v1"
capitulo: "CH-45"
tags: [contrato, c-060]
used_by: ["CMP-010", "CMP-028"]
modified_by: []
articulos_constitucionales: ["P-36", "INV-13", "INV-E10", "INV-E22"]
---

# RuntimeVersionSnapshot (C-060)

> Contrato v1 — introducido en [[ch-45-evolucion-del-runtime|CH-45]].

## Definición canónica

```text
STRUCT RuntimeVersionSnapshot
    versions: VersionSnapshot
    modelId: Text
    connectionVersions: Map<ConnectionId, Text>
    sessionFormatVersion: Integer
    adoptedAt: Timestamp
END
```

## Usado por

[[CMP-010-sessionmanager|CMP-010]], [[CMP-028-connectionmanager|CMP-028]]

## Modificado por

Ninguno

## Impacto constitucional

P-36, INV-13, INV-E10, INV-E22

## Contexto del libro

- Introducido en: [[ch-45-evolucion-del-runtime|CH-45]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
