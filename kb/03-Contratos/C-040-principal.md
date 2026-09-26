---
id: "C-040"
tipo: contrato
nombre: "Principal"
version: "v1"
capitulo: "CH-31"
tags: [contrato, c-040]
used_by: ["CMP-012"]
modified_by: []
articulos_constitucionales: ["P-17", "P-31", "INV-19", "INV-E07"]
---

# Principal (C-040)

> Contrato v1 — introducido en [[ch-31-identidad-del-llamante|CH-31]].

## Definición canónica

```text
STRUCT Principal
    principalId: Text
    principalType: PrincipalType
    issuer: Text
    tenantId: Optional<Text>
    attributes: Map<Text, Value>
END
```

## Usado por

[[CMP-012-admissioncontroller|CMP-012]]

## Modificado por

Ninguno

## Impacto constitucional

P-17, P-31, INV-19, INV-E07

## Contexto del libro

- Introducido en: [[ch-31-identidad-del-llamante|CH-31]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
