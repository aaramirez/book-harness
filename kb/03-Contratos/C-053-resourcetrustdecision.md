---
id: "C-053"
tipo: contrato
nombre: "ResourceTrustDecision"
version: "v1"
capitulo: "CH-40"
tags: [contrato, c-053]
used_by: ["CMP-027"]
modified_by: []
articulos_constitucionales: ["P-13", "INV-19"]
---

# ResourceTrustDecision (C-053)

> Contrato v1 — introducido en [[ch-40-extension-host|CH-40]].

## Definición canónica

```text
STRUCT ResourceTrustDecision
    decisionId: ResourceTrustDecisionId
    sourceRef: Text
    contentHash: Text
    outcome: TrustOutcome
    decidedBy: Principal
    decidedAt: Timestamp
END
```

## Usado por

[[CMP-027-extensionhost|CMP-027]]

## Modificado por

Ninguno

## Impacto constitucional

P-13, INV-19

## Contexto del libro

- Introducido en: [[ch-40-extension-host|CH-40]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
