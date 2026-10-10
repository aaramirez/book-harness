---
id: "CH-44"
tipo: capitulo
titulo: "Invocación Durable entre Agentes y A2A"
tags: [capitulo, ch44, v0-3]
introduces_components: []
introduces_contracts: ["C-058", "C-059"]
modifies_contracts: ["C-024"]
articulos_constitucionales: ["P-18", "P-19", "P-20", "P-21", "INV-E03", "INV-E04", "INV-E05", "INV-E06", "INV-E21"]
---

# CH-44 — Invocación Durable entre Agentes y A2A

## Navegación

⬅ [[ch-43-presupuestos-heredados|CH-43]] · **CH-44**

## Resultado esperado

Al terminar este capítulo podrás decidir cómo un agente invoca a otro, dentro del arnés o afuera, sin repetir la invocación después de un reinicio, y explicar qué identidad, qué presupuesto y qué esperas cruzan la frontera entre los dos.

## Qué introduce este capítulo

### Componentes

- Ninguno nuevo. [[CMP-013-agentcommunicationgateway|AgentCommunicationGateway]] gana `invocationIdForStep`, `requireAdvertisedSkill`, `forwardedCallerFor`, `openAgentInvocation`, `applyInvocationUpdate`, `invocationStatusForWait` y `surfaceChildWait`.

### Contratos

- [[C-058-agentinvocation|C-058 AgentInvocation]]
- [[C-059-agentcard|C-059 AgentCard]]
- [[C-024-agentcommunicationmessage|C-024 AgentCommunicationMessage]] v1 → v2

### Deuda

Resuelve D-020 y D-023.

## Artículos constitucionales relevantes

P-18, P-19, P-20, P-21, INV-E03, INV-E04, INV-E05, INV-E06, INV-E21

## Localización en el repo

`book/chapters/44-invocacion-entre-agentes/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
