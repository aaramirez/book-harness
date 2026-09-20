---
id: "CH-15"
tipo: capitulo
titulo: "\"AgentCommunicationGateway y la Frontera Explícita entre Agentes\""
tags: [capitulo, ch15]
introduces_components: ["CMP-013"]
introduces_contracts: ["C-024", "C-025"]
articulos_constitucionales: ["P-18", "P-19", "P-20", "P-21", "P-25", "INV-E03", "INV-E04", "INV-E05", "INV-E06", "INV-18", "INV-19", "INV-20"]
---

# CH-15 — "AgentCommunicationGateway y la Frontera Explícita entre Agentes"

## Navegación

⬅ [[ch-14-admission-controller|CH-14]] · **CH-15** · [[ch-16-credential-broker|CH-16]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-013-agentcommunicationgateway|CMP-013]] — Adaptar mensajes semánticos hacia/desde protocolos de interoperabilidad externos (A2A u otros) exclusivamente a través de adapters, desacoplando el core de cualquier SDK, protocolo o transporte concreto — y verificar, sin redefinirlo, que una comunicación respaldada por un DelegationGrant respete el scope, el vencimiento y el ExecutionBudget acotado que ese grant ya declara — sin decidir si el estímulo que originó cualquiera de los dos runs comunicándose tenía derecho a arrancar, sin autorizar ninguna acción ya resuelta y sin decidir continuación de turno.

### Contratos

- [[C-024-agentcommunicationmessage|C-024]] — AgentCommunicationMessage (impacto: P-18, P-20, INV-E03, INV-E04)
- [[C-025-delegationgrant|C-025]] — DelegationGrant (impacto: P-21, INV-E06, INV-19)


## Artículos constitucionales relevantes

P-18, P-19, P-20, P-21, P-25, INV-E03, INV-E04, INV-E05, INV-E06, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/15-agent-communication-gateway/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
