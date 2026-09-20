---
id: "C-031"
tipo: contrato
nombre: "ExecutionPlacement"
version: "v1"
capitulo: "CH-21"
tags: [contrato, c-031]
used_by: ["CMP-019"]
modified_by: []
articulos_constitucionales: ["P-27", "INV-19"]
---

# ExecutionPlacement (C-031)

> Contrato v1 — introducido en [[ch-21-execution-fabric|CH-21]].

## Definición canónica

```text
STRUCT ExecutionPlacement
    id: ExecutionPlacementId
    runId: RunId
    topology: DeploymentTopology
    computeResourceRef: Optional<Text>
    residencyConstraint: Optional<Text>
    resolvedAt: Timestamp
END
```

## Usado por

[[CMP-019-executionfabricadapter|CMP-019]]

## Modificado por

Ninguno

## Impacto constitucional

P-27, INV-19

## Contexto del libro

- Introducido en: [[ch-21-execution-fabric|CH-21]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
