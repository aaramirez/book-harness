---
id: "C-065"
tipo: contrato
nombre: "AgentManifest"
version: "v1"
capitulo: "CH-48"
tags: [contrato, c-065]
used_by: ["CMP-011"]
modified_by: []
articulos_constitucionales: ["P-06", "P-39", "INV-E27"]
---

# AgentManifest (C-065)

> Contrato v1 — introducido en [[ch-48-agente-como-directorio|CH-48]].

## Definición canónica

```text
STRUCT AgentManifest
    agentRoot: Text
    sources: List<ManifestSource>
    diagnostics: List<AuthoringDiagnostic>
    trusted: Boolean
    discoveredAt: Timestamp
END
```

## Usado por

[[CMP-011-agentcore|CMP-011]]

## Modificado por

Ninguno

## Impacto constitucional

P-06, P-39, INV-E27

## Contexto del libro

- Introducido en: [[ch-48-agente-como-directorio|CH-48]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
