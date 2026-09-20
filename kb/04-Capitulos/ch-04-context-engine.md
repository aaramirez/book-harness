---
id: "CH-04"
tipo: capitulo
titulo: "ContextEngine y Qué Ve Realmente el Modelo"
tags: [capitulo, ch04]
introduces_components: ["CMP-004"]
introduces_contracts: ["C-005"]
articulos_constitucionales: ["P-01", "P-04", "P-12", "P-14", "INV-02", "INV-09", "INV-18", "INV-19"]
---

# CH-04 — ContextEngine y Qué Ve Realmente el Modelo

## Navegación

⬅ [[ch-03-model-gateway|CH-03]] · **CH-04** · [[ch-05-policy-engine|CH-05]] ➡

## Resultado esperado

Al terminar este capítulo podrás distinguir, dentro de la construcción del material que un turno le presenta al modelo, qué tramo le pertenece en exclusiva al componente que selecciona, rankea, compone y compacta ese material dentro de un presupuesto explícito, y qué tramo pertenece a dominios distintos (invocación real del modelo, continuación del turno, persistencia de historial, autorización sobre qué puede verse) que ya tienen o todavía no tienen componente propio — y podrás diseñar, para cualquier conjunto de candidatos de contexto, una representación normalizada que registre de dónde vino cada fragmento incluido y contra qué presupuesto se validó, sin necesitar resolver todavía cómo ese resultado llega al modelo.

## Qué introduce este capítulo

### Componentes

- [[CMP-004-contextengine|CMP-004]] — Seleccionar, rankear, componer y compactar el material candidato de un turno (AgentMessage, AgentState, ExecutionContext) dentro de un presupuesto de contexto explícito, devolviendo un ContextSnapshot que registra la procedencia (provenance) de cada bloque incluido — sin invocar al modelo, sin decidir si otro turno debe ocurrir, sin persistir historial de sesión y sin autorizar qué información puede verse.

### Contratos

- [[C-005-contextsnapshot|C-005]] — ContextSnapshot (impacto: P-01, P-14, INV-09)


## Artículos constitucionales relevantes

P-01, P-04, P-12, P-14, INV-02, INV-09, INV-18, INV-19

## Localización en el repo

`book/chapters/04-context-engine/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
