---
id: "C-047"
tipo: contrato
nombre: "SandboxSession"
version: "v1"
capitulo: "CH-35"
tags: [contrato, c-047]
used_by: ["CMP-026"]
modified_by: []
articulos_constitucionales: ["P-35", "INV-E20"]
---

# SandboxSession (C-047)

> Contrato v1 — introducido en [[ch-35-entorno-aislado|CH-35]].

## Definición canónica

```text
STRUCT SandboxSession
    sandboxId: SandboxId
    sessionId: SessionId
    networkPolicy: NetworkPolicy
    status: SandboxStatus
    environmentRef: Text
    placementRef: Optional<ExecutionPlacementId>
    openedAt: Timestamp
    closedAt: Optional<Timestamp>
END
```

## Usado por

[[CMP-026-isolatedexecutionenvironment|CMP-026]]

## Modificado por

Ninguno

## Impacto constitucional

P-35, INV-E20

## Contexto del libro

- Introducido en: [[ch-35-entorno-aislado|CH-35]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
