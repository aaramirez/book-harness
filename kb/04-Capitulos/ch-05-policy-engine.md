---
id: "CH-05"
tipo: capitulo
titulo: "PolicyEngine y la Frontera de Autorización"
tags: [capitulo, ch05]
introduces_components: ["CMP-005"]
introduces_contracts: ["C-014"]
articulos_constitucionales: ["P-05", "P-13", "INV-04", "INV-06", "INV-15", "INV-18", "INV-19", "INV-20"]
---

# CH-05 — PolicyEngine y la Frontera de Autorización

## Navegación

⬅ [[ch-04-context-engine|CH-04]] · **CH-05** · [[ch-06-human-interaction|CH-06]] ➡

## Resultado esperado

Al terminar este capítulo podrás distinguir, dentro de la pregunta "¿puede ocurrir esta acción?", qué tramo le pertenece en exclusiva al componente que evalúa autorización y qué tramos pertenecen a dominios distintos (ejecución de la acción ya aprobada, resolución de una aprobación humana pendiente, enforcement de presupuesto) que ya tienen o todavía no tienen componente propio — y podrás diseñar, para cualquier evaluación de autorización, un resultado de tres estados que nunca colapse en un simple sí/no y que deniegue por defecto cuando ningún criterio conocido aplica, en vez de permitir por accidente.

## Qué introduce este capítulo

### Componentes

- [[CMP-005-policyengine|CMP-005]] — Evaluar si una acción ya resuelta (ToolCall) puede ocurrir, produciendo una PolicyDecision determinística de tres resultados posibles (allow, deny, require_approval) — con la regla aplicable y el ToolCall evaluado siempre trazables — sin ejecutar la acción, sin invocar al modelo, sin seleccionar contexto, sin decidir continuación del turno y sin resolver ella misma la aprobación humana cuando la exige.

### Contratos

- [[C-014-policydecision|C-014]] — PolicyDecision (impacto: P-05, P-13, INV-06, INV-15, INV-19)


## Artículos constitucionales relevantes

P-05, P-13, INV-04, INV-06, INV-15, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/05-policy-engine/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
