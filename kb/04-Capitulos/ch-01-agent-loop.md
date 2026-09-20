---
id: "CH-01"
tipo: capitulo
titulo: "El Agent Loop y el Ciclo de Ejecución Cognitiva"
tags: [capitulo, ch01]
introduces_components: ["CMP-001"]
introduces_contracts: ["C-013"]
articulos_constitucionales: ["P-10", "P-12", "P-13", "INV-08", "INV-09", "INV-16", "INV-17", "INV-18"]
---

# CH-01 — El Agent Loop y el Ciclo de Ejecución Cognitiva

## Navegación

⬅ [[ch-00-constitucion|CH-00]] · **CH-01** · [[ch-02-tool-runtime|CH-02]] ➡

## Resultado esperado

Al terminar este capítulo podrás distinguir, dentro de la decisión "¿debe ocurrir otro turno de razonamiento?", qué parte le pertenece en exclusiva a AgentLoop y qué parte pertenece a un dominio distinto (autorización, presupuesto operacional, ejecución de una tool call) que todavía no tiene componente propio — y podrás diagnosticar, para cualquier AgentRunStatus dado, si la transición que propones respeta el lifecycle formal de Article V o si en realidad está inventando un estado que el contrato no reconoce.

## Qué introduce este capítulo

### Componentes

- [[CMP-001-agentloop|CMP-001]] — Coordinar el turn lifecycle de una ejecución cognitiva (el ciclo model → action → observation), decidir si otro turno de razonamiento debe ocurrir y producir la transición de AgentRunStatus y el AgentEvent correspondientes — sin ejecutar directamente ningún side effect.

### Contratos

- [[C-013-agentrunstatus|C-013]] — AgentRunStatus (impacto: P-10, INV-08, INV-09)


## Artículos constitucionales relevantes

P-10, P-12, P-13, INV-08, INV-09, INV-16, INV-17, INV-18

## Localización en el repo

`book/chapters/01-agent-loop/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
