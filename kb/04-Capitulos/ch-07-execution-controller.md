---
id: "CH-07"
tipo: capitulo
titulo: "ExecutionController y los Límites Operacionales de una Ejecución"
tags: [capitulo, ch07]
introduces_components: ["CMP-007"]
introduces_contracts: ["C-017"]
articulos_constitucionales: ["P-10", "INV-08", "INV-09", "INV-10", "INV-18", "INV-19", "INV-20"]
---

# CH-07 — ExecutionController y los Límites Operacionales de una Ejecución

## Navegación

⬅ [[ch-06-human-interaction|CH-06]] · **CH-07** · [[ch-08-capability-registry|CH-08]] ➡

## Resultado esperado

Al terminar este capítulo podrás distinguir, dentro de la pregunta "¿puede esta ejecución seguir?", qué tramo le pertenece en exclusiva al componente que aplica los límites operacionales de un `AgentRun` y qué tramo le pertenece a un dominio distinto (la continuación cognitiva de un ciclo de razonamiento, la ejecución de una tool call, la autorización de una acción, la invocación del modelo) — y podrás diseñar, para cualquier evaluación de continuación operacional, un resultado de tres estados que distinga detenerse por presupuesto agotado de detenerse por cancelación explícita, en vez de colapsar ambos casos en un simple booleano "sí, puede seguir" / "no, no puede seguir".

## Qué introduce este capítulo

### Componentes

- [[CMP-007-executioncontroller|CMP-007]] — Evaluar si un AgentRun puede continuar operacionalmente contra su ExecutionBudget — turnos, tool calls, tokens, costo, runtime y concurrencia — o si fue cancelado explícitamente, produciendo una ExecutionDecision determinística de tres resultados posibles (continue/stop/cancelled) con el uso actual siempre trazable — sin decidir si otro turno de razonamiento cognitivo debe ocurrir, sin ejecutar tools/side effects, sin evaluar policy/autorización y sin invocar al modelo.

### Contratos

- [[C-017-executiondecision|C-017]] — ExecutionDecision (impacto: P-10, INV-08, INV-09, INV-10, INV-18, INV-19, INV-20)


## Artículos constitucionales relevantes

P-10, INV-08, INV-09, INV-10, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/07-execution-controller/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
