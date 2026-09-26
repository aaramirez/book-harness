---
id: "CMP-025"
tipo: componente
nombre: "ContinuationRegistry"
capitulo: "CH-34"
tags: [componente, cmp-025]
consumes: ["C-004", "C-022", "C-023"]
produces: ["C-010", "C-011", "C-046"]
articulos_constitucionales: ["P-16", "P-34", "INV-E01", "INV-E19", "INV-18", "INV-19", "INV-20"]
---

# ContinuationRegistry (CMP-025)

> Componente introducido en [[ch-34-canales-continuacion|CH-34]] — parte del runtime del arnés (plano Ingress & Activation).

## Responsabilidad

Mantener qué sesión es dueña de cada dirección de continuación — un hilo, un issue, una sesión de socket, un schedule — y decidir, para un ActivationRequest ya admitido, si continúa la sesión dueña de su dirección o activa una sesión nueva, sin inferir nunca qué run continúa un estímulo — sin admitir ni rechazar la activación, sin elegir qué agente atiende una activación nueva, sin decidir si el llamante puede operar la sesión, sin reanudar una espera y sin normalizar ni transportar el estímulo de ningún canal.

## Decisiones que posee (owns)

- Every external conversation (a thread, an issue, a socket session, a schedule) MUST map to a durable session through an explicit continuation address with exclusive ownership. The runtime MUST NOT guess which run a stimulus continues (cita literal, P-34)
- A continuation address has at most one owning session at a time (cita literal, INV-E19) — reclamar, liberar y rechazar (fail-closed) el reclamo de una dirección que ya tiene otra sesión dueña
- decidir, para un ActivationRequest ya admitido, CONTINUE_SESSION, ACTIVATE_NEW o ACTIVATE_UNADDRESSED

## Decisiones que NO posee (does_not_own)

- admitir o rechazar la activación ([[CMP-012-admissioncontroller|AdmissionController]], CH-14 — la frontera más importante: AdmissionController decide SI un estímulo entra; ContinuationRegistry decide A QUÉ SESIÓN va)
- decidir si el llamante puede continuar la sesión dueña (AdmissionController, `continuationAllowedForCaller`, CH-31)
- reanudar una espera estacionada ([[CMP-024-resumptioncoordinator|ResumptionCoordinator]], CH-33)
- elegir qué agente atiende una activación nueva (Routing, Preview)
- crear la sesión ni guardar su historia ([[CMP-010-sessionmanager|SessionManager]], CH-10)
- normalizar el estímulo, verificar firmas, mantener sockets o disparar schedules (Ingress Adapter, INV-E01)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-022-activationrequest|C-022]], [[C-023-admissiondecision|C-023]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-046-continuationaddress|C-046]] |

## Artículos constitucionales

P-16, P-34, INV-E01, INV-E19, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-34-canales-continuacion|CH-34]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
