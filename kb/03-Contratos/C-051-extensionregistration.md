---
id: "C-051"
tipo: contrato
nombre: "ExtensionRegistration"
version: "v1"
capitulo: "CH-40"
tags: [contrato, c-051]
used_by: ["CMP-027"]
modified_by: []
articulos_constitucionales: ["P-12", "INV-E24"]
---

# ExtensionRegistration (C-051)

> Contrato v1 — introducido en [[ch-40-extension-host|CH-40]].

## Definición canónica

```text
STRUCT ExtensionRegistration
    extensionId: Text
    version: Text
    source: ExtensionSource
    sourceRef: Text
    contentHash: Text
    hookPoints: List<HookPoint>
    capabilities: List<CapabilityId>
    trustDecisionId: Optional<ResourceTrustDecisionId>
    status: ExtensionStatus
    registeredAt: Timestamp
END
```

## Usado por

[[CMP-027-extensionhost|CMP-027]]

## Modificado por

Ninguno

## Impacto constitucional

P-12, INV-E24

## Contexto del libro

- Introducido en: [[ch-40-extension-host|CH-40]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
