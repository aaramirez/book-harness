---
id: "CH-38"
tipo: capitulo
titulo: "Identidad, Auditoría y Retención en Todo el Turno"
tags: [capitulo, ch38, v0-2-1, deuda]
introduces_components: []
introduces_contracts: []
modifies_contracts: []
articulos_constitucionales: ["P-13", "P-17", "P-22", "P-25", "P-31", "P-32", "INV-07", "INV-13", "INV-19", "INV-E07", "INV-E10", "INV-E17"]
---

# CH-38 — Identidad, Auditoría y Retención en Todo el Turno

## Navegación

⬅ [[ch-37-esperas-credenciales-canales|CH-37]] · **CH-38**

## Resultado esperado

Al terminar este capítulo podrás decidir cómo la identidad de quien llama restringe la admisión, la política y las credenciales sin concederle nunca más de lo que la regla base permite. También podrás explicar cómo las entradas pendientes, la compactación, la auditoría y la retención se sostienen dentro del turno durable, también después de una caída.

## Qué introduce este capítulo

Segundo y último capítulo de v0.2.1. Resuelve las deudas D-001..D-008 (`registry/debt.yaml`) sin componentes ni contratos nuevos:

- [[CMP-012-admissioncontroller|AdmissionController]]: `principalRulesGrantAccess`, `admitWithPrincipalRules`
- [[CMP-005-policyengine|PolicyEngine]]: `evaluatePolicyForCaller` (la identidad solo restringe)
- [[CMP-014-credentialbroker|CredentialBroker]]: `resolveCallerCredentialReference`
- [[CMP-018-datagovernanceengine|DataGovernanceEngine]]: `evaluateJournalRetention`
- Integración: `takePendingInputsForStep`, `confirmPendingInputsAfterCommit`, `compactHistoryInDurableTurn` (la compactación es un paso del journal), `auditSafeReplayDeclaration`, `auditSessionContinuation`

## Artículos constitucionales relevantes

P-13, P-17, P-22, P-25, P-31, P-32, INV-07, INV-13, INV-19, INV-E07, INV-E10, INV-E17

## Localización en el repo

`book/chapters/38-identidad-auditoria-retencion/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
