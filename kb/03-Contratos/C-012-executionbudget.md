---
id: "C-012"
tipo: contrato
nombre: "ExecutionBudget"
version: "v1"
capitulo: "CH-00"
tags: [contrato, c-012]
used_by: ["CMP-007", "CMP-011"]
modified_by: []
articulos_constitucionales: ["P-10", "INV-09"]
---

# ExecutionBudget (C-012)

> Contrato v1 — introducido en [[ch-00-constitucion|CH-00]].

## Definición canónica

```text
STRUCT ExecutionBudget
    maxTurns: Integer
    maxToolCalls: Integer
    maxInputTokens: Integer
    maxOutputTokens: Integer
    maxCost: Number
    maxRuntimeMs: Integer
    maxConcurrentTools: Integer
END
```

## Usado por

[[CMP-007-executioncontroller|CMP-007]], [[CMP-011-agentcore|CMP-011]]

## Modificado por

Ninguno

## Impacto constitucional

P-10, INV-09

## Contexto del libro

- Introducido en: [[ch-00-constitucion|CH-00]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
