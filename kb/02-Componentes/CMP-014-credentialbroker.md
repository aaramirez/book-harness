---
id: "CMP-014"
tipo: componente
nombre: "CredentialBroker"
capitulo: "CH-16"
tags: [componente, cmp-014]
consumes: ["C-004", "C-018"]
produces: ["C-010", "C-011", "C-026"]
articulos_constitucionales: ["P-13", "P-22", "INV-E07", "INV-E08", "INV-18", "INV-19", "INV-20"]
---

# CredentialBroker (CMP-014)

> Componente introducido en [[ch-16-credential-broker|CH-16]] — parte del runtime del arnés.

## Responsabilidad

Resolver, para una implementación de capability ya resuelta (CapabilityDescriptor, C-018, CH-08), la credencial que necesita para autenticarse contra el sistema externo real que envuelve — produciendo exclusivamente una CredentialReference opaca, nunca el valor real del secreto — y aplicar sobre ese secreto el gobierno de datos que P-22 exige (clasificación, rotación/expiración), sin decidir si la acción que esa implementación va a ejecutar está autorizada, sin decidir qué implementación satisface la capability solicitada y sin ejecutar el side effect en sí.

## Decisiones que posee (owns)

- Credentials are resolved by a CredentialBroker and SHOULD NOT enter model context (cita literal, INV-E08)
- Tenant data, memory, credentials, artifacts and audit records are isolated (cita literal, INV-E07, aplicada específicamente a credenciales)
- aplicar sobre un secreto el gobierno de datos que P-22 exige — clasificación explícita (CredentialReference.classification) y rotación/expiración explícitas (CredentialReference.expiresAt) — cuando ese secreto las declara
- verificar que el secreto solicitado corresponda a la capability ya resuelta, exista y no haya vencido, antes de producir cualquier CredentialReference
- rechazar por defecto (fail-closed) cuando el secreto no corresponde, no existe o ya venció
- garantizar, por construcción del propio contrato, que el valor real del secreto nunca aparezca en ningún dato que este componente produce

## Decisiones que NO posee (does_not_own)

- decidir si la acción/ToolCall ya resuelta que la implementación va a ejecutar está autorizada (PolicyEngine, CMP-005, ya introducido en CH-05 — distinta pregunta, distinto momento: "con qué se autentica" nunca es "si está permitido")
- resolver qué implementación satisface una capability solicitada (CapabilityRegistry, CMP-008, ya introducido en CH-08 — este componente actúa DESPUÉS, sobre un CapabilityDescriptor ya resuelto)
- ejecutar el side effect en sí, incluyendo la autenticación real contra el sistema externo con la credencial ya resuelta (ToolRuntime, CMP-002, ya introducido en CH-02 — el cableado real es trabajo de un capítulo de integración futuro)
- el mecanismo real de almacenamiento, cifrado o rotación física del secreto (Secret Store — infraestructura de borde, no un componente propio de este registry)
- decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en CH-01)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-018-capabilitydescriptor|C-018]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-026-credentialreference|C-026]] |

## Artículos constitucionales

P-13, P-22, INV-E07, INV-E08, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-16-credential-broker|CH-16]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
