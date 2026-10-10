---
id: "C-057"
tipo: contrato
nombre: "ExecutionUsage"
version: "v1"
capitulo: "CH-43"
tags: [contrato, c-057]
used_by: ["CMP-007"]
modified_by: []
articulos_constitucionales: ["INV-09", "INV-E06", "INV-E21"]
---

# ExecutionUsage (C-057)

> Contrato v1 — introducido en [[ch-43-presupuestos-heredados|CH-43]] (era una estructura embebida desde CH-07).

## Definición canónica

```text
STRUCT ExecutionUsage
    toolCallsUsed: Integer
    inputTokensUsed: Integer
    outputTokensUsed: Integer
    costUsed: Number
    runtimeMsElapsed: Integer
    concurrentToolsInFlight: Integer
END
```

## Usado por

[[CMP-007-executioncontroller|CMP-007]]

## Modificado por

Ninguno

## Impacto constitucional

INV-09, INV-E06, INV-E21

## Contexto del libro

- Introducido en: [[ch-43-presupuestos-heredados|CH-43]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
