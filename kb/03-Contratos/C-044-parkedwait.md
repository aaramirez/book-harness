---
id: "C-044"
tipo: contrato
nombre: "ParkedWait"
version: "v1"
capitulo: "CH-33"
tags: [contrato, c-044]
used_by: ["CMP-024"]
modified_by: []
articulos_constitucionales: ["P-23", "P-33", "INV-E18", "INV-19"]
---

# ParkedWait (C-044)

> Contrato v1 — introducido en [[ch-33-esperas-durables|CH-33]].

## Definición canónica

```text
STRUCT ParkedWait
    waitId: WaitId
    runId: RunId
    sessionId: SessionId
    kind: WaitKind
    requestId: Optional<HumanInteractionRequestId>
    challengeId: Optional<AuthorizationChallengeId>
    requestedBy: Principal
    responderRule: ResponderRule
    designatedResponder: Optional<Principal>
    status: WaitStatus
    parkedAt: Timestamp
    expiresAt: Optional<Timestamp>
    resumedAt: Optional<Timestamp>
END
```

## Usado por

[[CMP-024-resumptioncoordinator|CMP-024]]

## Modificado por

Ninguno

## Impacto constitucional

P-23, P-33, INV-E18, INV-19

## Contexto del libro

- Introducido en: [[ch-33-esperas-durables|CH-33]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
