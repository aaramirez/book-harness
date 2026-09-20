---
id: "CH-16"
tipo: capitulo
titulo: "\"CredentialBroker y la Resolución Segura de una Credencial\""
tags: [capitulo, ch16]
introduces_components: ["CMP-014"]
introduces_contracts: ["C-026"]
articulos_constitucionales: ["P-13", "P-22", "INV-E07", "INV-E08", "INV-18", "INV-19", "INV-20"]
---

# CH-16 — "CredentialBroker y la Resolución Segura de una Credencial"

## Navegación

⬅ [[ch-15-agent-communication-gateway|CH-15]] · **CH-16** · [[ch-17-idempotency-guard|CH-17]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-014-credentialbroker|CMP-014]] — Resolver, para una implementación de capability ya resuelta (CapabilityDescriptor, C-018, CH-08), la credencial que necesita para autenticarse contra el sistema externo real que envuelve — produciendo exclusivamente una CredentialReference opaca, nunca el valor real del secreto — y aplicar sobre ese secreto el gobierno de datos que P-22 exige (clasificación, rotación/expiración), sin decidir si la acción que esa implementación va a ejecutar está autorizada, sin decidir qué implementación satisface la capability solicitada y sin ejecutar el side effect en sí.

### Contratos

- [[C-026-credentialreference|C-026]] — CredentialReference (impacto: P-22, INV-E07, INV-E08)


## Artículos constitucionales relevantes

P-13, P-22, INV-E07, INV-E08, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/16-credential-broker/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
