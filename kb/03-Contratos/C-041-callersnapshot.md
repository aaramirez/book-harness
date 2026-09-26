---
id: "C-041"
tipo: contrato
nombre: "CallerSnapshot"
version: "v1"
capitulo: "CH-31"
tags: [contrato, c-041]
used_by: ["CMP-012"]
modified_by: []
articulos_constitucionales: ["P-31", "INV-19"]
---

# CallerSnapshot (C-041)

> Contrato v1 — introducido en [[ch-31-identidad-del-llamante|CH-31]].

## Definición canónica

```text
STRUCT CallerSnapshot
    initiator: Principal
    current: Principal
END
```

## Usado por

[[CMP-012-admissioncontroller|CMP-012]]

## Modificado por

Ninguno

## Impacto constitucional

P-31, INV-19

## Contexto del libro

- Introducido en: [[ch-31-identidad-del-llamante|CH-31]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
