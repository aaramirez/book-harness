---
id: "C-048"
tipo: contrato
nombre: "NetworkPolicy"
version: "v1"
capitulo: "CH-35"
tags: [contrato, c-048]
used_by: ["CMP-026"]
modified_by: []
articulos_constitucionales: ["P-35", "INV-E08", "INV-E20"]
---

# NetworkPolicy (C-048)

> Contrato v1 — introducido en [[ch-35-entorno-aislado|CH-35]].

## Definición canónica

```text
STRUCT NetworkPolicy
    mode: NetworkMode
    rules: List<EgressRule>
END
```

## Usado por

[[CMP-026-isolatedexecutionenvironment|CMP-026]]

## Modificado por

Ninguno

## Impacto constitucional

P-35, INV-E08, INV-E20

## Contexto del libro

- Introducido en: [[ch-35-entorno-aislado|CH-35]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
