---
id: "C-014"
tipo: contrato
nombre: "PolicyDecision"
version: "v1"
capitulo: "CH-05"
tags: [contrato, c-014]
used_by: ["CMP-005", "CMP-006"]
modified_by: []
articulos_constitucionales: ["P-05", "P-13", "INV-06", "INV-15", "INV-19"]
---

# PolicyDecision (C-014)

> Contrato v1 — introducido en [[ch-05-policy-engine|CH-05]].

## Definición canónica

```text
STRUCT PolicyDecision
    callId: ToolCallId
    outcome: PolicyOutcome
    policyRuleId: Text
    reason: Optional<HarnessError>
    decidedAt: Timestamp
END
```

## Usado por

[[CMP-005-policyengine|CMP-005]], [[CMP-006-humaninteractionservice|CMP-006]]

## Modificado por

Ninguno

## Impacto constitucional

P-05, P-13, INV-06, INV-15, INV-19

## Contexto del libro

- Introducido en: [[ch-05-policy-engine|CH-05]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
