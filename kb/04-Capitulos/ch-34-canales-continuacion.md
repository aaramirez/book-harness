---
id: "CH-34"
tipo: capitulo
titulo: "Canales y Direcciones de Continuación: HTTP, WebSocket, Webhooks y Schedules"
tags: [capitulo, ch34, tramo-4]
introduces_components: ["CMP-025"]
introduces_contracts: ["C-046"]
modifies_contracts: ["C-022"]
articulos_constitucionales: ["P-16", "P-17", "P-34", "INV-E01", "INV-E02", "INV-E15", "INV-E19"]
---

# CH-34 — Canales y Direcciones de Continuación: HTTP, WebSocket, Webhooks y Schedules

## Navegación

⬅ [[ch-33-esperas-durables|CH-33]] · **CH-34**

## Resultado esperado

Al terminar este capítulo podrás decidir, para cualquier mensaje que llegue al agente por un canal (una API, un chat, un WebSocket, un webhook o un schedule), si continúa una conversación que ya existe o empieza una nueva, sin adivinarlo. También podrás explicar por qué una conversación externa solo puede pertenecer a una sesión a la vez.

## Qué introduce este capítulo

### Componentes

- [[CMP-025-continuationregistry|CMP-025 ContinuationRegistry]], entre [[CMP-012-admissioncontroller|AdmissionController]] y el Routing (Preview).

### Contratos

- [[C-046-continuationaddress|C-046 ContinuationAddress]]
- **Modifica** [[C-022-activationrequest|C-022 ActivationRequest]] → v2 (`sourceKind`, `continuationAddress`).

### Canales (Ingress Adapters, sin componente)

API HTTP de sesiones, chat, WebSocket de entrada, webhooks (firma en tiempo constante), schedules y eventos de stream.

## Artículos constitucionales relevantes

P-16, P-17, P-34, INV-E01, INV-E02, INV-E15, INV-E19

## Localización en el repo

`book/chapters/34-canales-continuacion/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
