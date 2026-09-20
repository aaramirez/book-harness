---
id: "C-026"
tipo: contrato
nombre: "CredentialReference"
version: "v1"
capitulo: "CH-16"
tags: [contrato, c-026]
used_by: ["CMP-014"]
modified_by: []
articulos_constitucionales: ["P-22", "INV-E07", "INV-E08"]
---

# CredentialReference (C-026)

> Contrato v1 — introducido en [[ch-16-credential-broker|CH-16]].

## Definición canónica

```text
STRUCT CredentialReference
    id: CredentialReferenceId
    capability: CapabilityId
    credentialName: Text
    classification: CredentialClassification
    resolvedAt: Timestamp
    expiresAt: Optional<Timestamp>
END
```

## Usado por

[[CMP-014-credentialbroker|CMP-014]]

## Modificado por

Ninguno

## Impacto constitucional

P-22, INV-E07, INV-E08

## Contexto del libro

- Introducido en: [[ch-16-credential-broker|CH-16]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
