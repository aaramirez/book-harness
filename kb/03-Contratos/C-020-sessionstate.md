---
id: "C-020"
tipo: contrato
nombre: "SessionState"
version: "v1"
capitulo: "CH-10"
tags: [contrato, c-020]
used_by: ["CMP-010"]
modified_by: []
articulos_constitucionales: ["P-08", "P-23", "INV-12", "INV-13"]
---

# SessionState (C-020)

> Contrato v1 — introducido en [[ch-10-session-manager|CH-10]].

## Definición canónica

```text
STRUCT SessionState
    sessionId: SessionId
    runIds: List<RunId>
    latestCheckpoint: SessionCheckpoint
    parentCheckpointId: Optional<SessionCheckpointId>
    createdAt: Timestamp
    updatedAt: Timestamp
END
```

## Usado por

[[CMP-010-sessionmanager|CMP-010]]

## Modificado por

Ninguno

## Impacto constitucional

P-08, P-23, INV-12, INV-13

## Contexto del libro

- Introducido en: [[ch-10-session-manager|CH-10]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
