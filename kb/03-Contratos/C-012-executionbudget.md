---
id: "C-012"
tipo: contrato
nombre: "ExecutionBudget"
version: "v2"
capitulo: "CH-00"
tags: [contrato, c-012]
used_by: ["CMP-007", "CMP-011"]
modified_by: ["CH-43"]
articulos_constitucionales: ["P-10", "INV-09"]
---

# ExecutionBudget (C-012)

> Contrato **v2** — introducido en [[ch-00-constitucion|CH-00]], modificado en [[ch-43-presupuestos-heredados|CH-43]].

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
    parentRunId: Optional<RunId>
    consumed: Optional<ExecutionUsage>
    sandboxLimits: Optional<SandboxLimits>
END
```

## Usado por

[[CMP-007-executioncontroller|CMP-007]], [[CMP-011-agentcore|CMP-011]]

## Modificado por

[[ch-43-presupuestos-heredados|CH-43]]: agrega `parentRunId`, `consumed` ([[C-057-executionusage|C-057]]) y `sandboxLimits` (los tres opcionales; NULL = run raíz sin límites de entorno, como en v1). ADR-004.

## Impacto constitucional

P-10, INV-09

## Contexto del libro

- Introducido en: [[ch-00-constitucion|CH-00]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
