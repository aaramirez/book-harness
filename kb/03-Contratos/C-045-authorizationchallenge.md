---
id: "C-045"
tipo: contrato
nombre: "AuthorizationChallenge"
version: "v1"
capitulo: "CH-33"
tags: [contrato, c-045]
used_by: ["CMP-024"]
modified_by: []
articulos_constitucionales: ["P-31", "P-33", "INV-E08", "INV-E18"]
---

# AuthorizationChallenge (C-045)

> Contrato v1 — introducido en [[ch-33-esperas-durables|CH-33]].

## Definición canónica

```text
STRUCT AuthorizationChallenge
    challengeId: AuthorizationChallengeId
    principal: Principal
    connectionRef: Text
    callbackRef: Text
    createdAt: Timestamp
    expiresAt: Timestamp
END
```

## Usado por

[[CMP-024-resumptioncoordinator|CMP-024]]

## Modificado por

Ninguno

## Impacto constitucional

P-31, P-33, INV-E08, INV-E18

## Contexto del libro

- Introducido en: [[ch-33-esperas-durables|CH-33]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
