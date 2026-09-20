---
id: "CH-02"
tipo: capitulo
titulo: "ToolRuntime y la Ejecución Controlada de una Tool Call"
tags: [capitulo, ch02]
introduces_components: ["CMP-002"]
introduces_contracts: ["C-008", "C-009"]
articulos_constitucionales: ["P-03", "P-04", "P-05", "P-12", "P-13", "INV-04", "INV-05", "INV-06"]
---

# CH-02 — ToolRuntime y la Ejecución Controlada de una Tool Call

## Navegación

⬅ [[ch-01-agent-loop|CH-01]] · **CH-02** · [[ch-03-model-gateway|CH-03]] ➡

## Resultado esperado

Al terminar este capítulo podrás distinguir, dentro del camino completo que atraviesa una acción con efectos reales, qué tramo le pertenece en exclusiva al componente que ejecuta esa acción y qué tramos pertenecen a dominios distintos (autorización, aprobación humana, presupuesto operacional, resolución de qué implementación satisface la capacidad pedida) que todavía no tienen componente propio — y podrás diseñar, para cualquier resultado de esa ejecución, una representación normalizada que no dependa de que cada implementación invente su propia forma de decir "esto falló" o "esto funcionó".

## Qué introduce este capítulo

### Componentes

- [[CMP-002-toolruntime|CMP-002]] — Resolver la capability solicitada por un ToolCall, validar su input contra el schema declarado, ejecutar los hooks de extensión (beforeToolCall/afterToolCall) y coordinar la ejecución de la acción aprobada, devolviendo un ToolResult normalizado — sin decidir autorización, aprobación humana, enforcement de presupuesto ni qué implementación concreta satisface la capability solicitada.

### Contratos

- [[C-008-toolcall|C-008]] — ToolCall (impacto: P-03, INV-04, INV-05)
- [[C-009-toolresult|C-009]] — ToolResult (impacto: INV-07, INV-20, P-04)


## Artículos constitucionales relevantes

P-03, P-04, P-05, P-12, P-13, INV-04, INV-05, INV-06

## Localización en el repo

`book/chapters/02-tool-runtime/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
