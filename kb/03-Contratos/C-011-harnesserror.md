---
id: "C-011"
tipo: contrato
nombre: "HarnessError"
version: "v1"
capitulo: "CH-00"
tags: [contrato, c-011]
used_by: ["CMP-001", "CMP-002", "CMP-003", "CMP-004", "CMP-005", "CMP-006", "CMP-007", "CMP-008", "CMP-012"]
modified_by: []
articulos_constitucionales: ["INV-20"]
---

# HarnessError (C-011)

> Contrato v1 — introducido en [[ch-00-constitucion|CH-00]].

## Definición canónica

```text
STRUCT HarnessError
    category: ErrorCategory
    code: Text
    message: Text
    recoverable: Boolean
    retryable: Boolean
    metadata: Map<Text, Value>
END
```

## Usado por

[[CMP-001-agentloop|CMP-001]], [[CMP-002-toolruntime|CMP-002]], [[CMP-003-modelgateway|CMP-003]], [[CMP-004-contextengine|CMP-004]], [[CMP-005-policyengine|CMP-005]], [[CMP-006-humaninteractionservice|CMP-006]], [[CMP-007-executioncontroller|CMP-007]], [[CMP-008-capabilityregistry|CMP-008]], [[CMP-012-admissioncontroller|CMP-012]]

## Modificado por

Ninguno

## Impacto constitucional

INV-20

## Contexto del libro

- Introducido en: [[ch-00-constitucion|CH-00]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
