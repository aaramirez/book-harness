---
id: "CH-37"
tipo: capitulo
titulo: "Esperas, Credenciales y Canales Completos"
tags: [capitulo, ch37, v0-2-1, deuda]
introduces_components: []
introduces_contracts: []
modifies_contracts: []
articulos_constitucionales: ["P-11", "P-16", "P-31", "P-33", "P-34", "INV-14", "INV-15", "INV-E08", "INV-E18", "INV-E19"]
---

# CH-37 — Esperas, Credenciales y Canales Completos

## Navegación

⬅ [[ch-36-integracion-turno-durable|CH-36]] · **CH-37** · [[ch-38-identidad-auditoria-retencion|CH-38]] ➡

## Resultado esperado

Al terminar este capítulo podrás decidir qué pasa con cada tipo de espera cuando llega su respuesta y cuando no llega nunca. También podrás explicar cómo un usuario autoriza el acceso a un servicio sin que su credencial pase por el run, y decidir cuándo una conversación externa deja de pertenecer a una sesión y por dónde el arnés le contesta.

## Qué introduce este capítulo

Primer capítulo de v0.2.1. Resuelve las deudas D-009..D-013 (`registry/debt.yaml`) sin componentes ni contratos nuevos:

- [[CMP-024-resumptioncoordinator|ResumptionCoordinator]]: vencimiento activo (`dueParkedWaits`, `expireParkedWait`, `expiryObservation`)
- [[CMP-014-credentialbroker|CredentialBroker]]: credencial faltante del llamante y callback sin token (`detectMissingCallerCredential`, `acceptAuthorizationCallback`)
- [[CMP-025-continuationregistry|ContinuationRegistry]]: liberar direcciones y responder por el canal (`releaseAddressesForSession`, `outboundAddressFor`, `buildOutboundMessage`)
- Integración: `parkForMissingCredential`, `resumeDurableQuestion`, `resumeDurableAuthorization`, `resumeDurableBudgetLimit`

## Artículos constitucionales relevantes

P-11, P-16, P-31, P-33, P-34, INV-14, INV-15, INV-E08, INV-E18, INV-E19

## Localización en el repo

`book/chapters/37-esperas-credenciales-canales/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
