---
id: "C-020"
tipo: contrato
nombre: "SessionState"
version: "v2"
capitulo: "CH-10"
tags: [contrato, c-020]
used_by: ["CMP-010"]
modified_by: ["CH-29"]
articulos_constitucionales: ["P-08", "P-23", "INV-12", "INV-13"]
---

# SessionState (C-020)

> Contrato **v2** — introducido en [[ch-10-session-manager|CH-10]], modificado en [[ch-29-compactacion-sesiones-arbol|CH-29]] (ADR-003, parte v2).

## Definición canónica

```text
STRUCT SessionState
    sessionId: SessionId
    runIds: List<RunId>
    latestCheckpoint: SessionCheckpoint
    parentCheckpointId: Optional<SessionCheckpointId>
    activeCheckpointId: Optional<SessionCheckpointId>
    branchSummaries: List<BranchSummary>
    createdAt: Timestamp
    updatedAt: Timestamp
END
```

## Usado por

[[CMP-010-sessionmanager|CMP-010]]

## Modificado por

[[ch-29-compactacion-sesiones-arbol|CH-29]]: agrega `activeCheckpointId` y `branchSummaries` (ver [[C-038-branchsummary|BranchSummary]])

## Impacto constitucional

P-08, P-23, INV-12, INV-13

## Contexto del libro

- Introducido en: [[ch-10-session-manager|CH-10]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
