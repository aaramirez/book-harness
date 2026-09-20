---
id: "C-023"
tipo: contrato
nombre: "AdmissionDecision"
version: "v1"
capitulo: "CH-14"
tags: [contrato, c-023]
used_by: ["CMP-012"]
modified_by: []
articulos_constitucionales: ["P-17", "INV-E02", "INV-19", "INV-20"]
---

# AdmissionDecision (C-023)

> Contrato v1 — introducido en [[ch-14-admission-controller|CH-14]].

## Definición canónica

```text
STRUCT AdmissionDecision
    requestId: ActivationRequestId
    outcome: AdmissionOutcome
    reason: Optional<HarnessError>
    decidedAt: Timestamp
END
```

## Usado por

[[CMP-012-admissioncontroller|CMP-012]]

## Modificado por

Ninguno

## Impacto constitucional

P-17, INV-E02, INV-19, INV-20

## Contexto del libro

- Introducido en: [[ch-14-admission-controller|CH-14]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
