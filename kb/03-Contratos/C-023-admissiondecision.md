---
id: "C-023"
tipo: contrato
nombre: "AdmissionDecision"
version: "v2"
capitulo: "CH-14"
tags: [contrato, c-023]
used_by: ["CMP-012"]
modified_by: ["CH-31"]
articulos_constitucionales: ["P-17", "INV-E02", "INV-19", "INV-20"]
---

# AdmissionDecision (C-023)

> Contrato **v2** — introducido en [[ch-14-admission-controller|CH-14]], modificado en [[ch-31-identidad-del-llamante|CH-31]] (ADR-001).

## Definición canónica

```text
STRUCT AdmissionDecision
    requestId: ActivationRequestId
    outcome: AdmissionOutcome
    reason: Optional<HarnessError>
    principal: Optional<Principal>
    decidedAt: Timestamp
END
```

## Usado por

[[CMP-012-admissioncontroller|CMP-012]]

## Modificado por

[[ch-31-identidad-del-llamante|CH-31]]: agrega `principal` (el Principal verificado de un ADMIT; NULL en todo REJECT y en las decisiones previas)

## Impacto constitucional

P-17, INV-E02, INV-19, INV-20

## Contexto del libro

- Introducido en: [[ch-14-admission-controller|CH-14]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
