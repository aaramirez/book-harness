---
id: "C-018"
tipo: contrato
nombre: "CapabilityDescriptor"
version: "v1"
capitulo: "CH-08"
tags: [contrato, c-018]
used_by: ["CMP-008"]
modified_by: []
articulos_constitucionales: ["P-03", "P-26", "INV-04", "INV-20"]
---

# CapabilityDescriptor (C-018)

> Contrato v1 — introducido en [[ch-08-capability-registry|CH-08]].

## Definición canónica

```text
STRUCT CapabilityDescriptor
    capability: CapabilityId
    name: Text
    version: Text
    inputSchema: Value
    implementationRef: Text
END
```

## Usado por

[[CMP-008-capabilityregistry|CMP-008]]

## Modificado por

Ninguno

## Impacto constitucional

P-03, P-26, INV-04, INV-20

## Contexto del libro

- Introducido en: [[ch-08-capability-registry|CH-08]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
