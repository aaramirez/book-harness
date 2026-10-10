---
id: "CH-42"
tipo: capitulo
titulo: "Fuentes de Datos Gobernadas: Recuperar sin Tirarlo Todo al Contexto"
tags: [capitulo, ch42, v0-3]
introduces_components: ["CMP-029"]
introduces_contracts: ["C-055", "C-056"]
modifies_contracts: []
articulos_constitucionales: ["P-01", "P-14", "P-22", "P-31", "P-38", "INV-E07", "INV-E11", "INV-E26"]
---

# CH-42 — Fuentes de Datos Gobernadas: Recuperar sin Tirarlo Todo al Contexto

## Navegación

⬅ [[ch-41-conexiones|CH-41]] · **CH-42**

## Resultado esperado

Al terminar este capítulo podrás decidir de qué fuentes puede el agente recuperar datos, qué parte de cada fuente le corresponde a quien llama, y cuáles de los datos recuperados entran al contexto. También podrás explicar cómo la clasificación de un dato lo acompaña hasta un resumen hecho con él.

## Qué introduce este capítulo

### Componentes

- [[CMP-029-retrievalengine|CMP-029 RetrievalEngine]]: qué puede recuperarse de cada fuente para el llamante.
- [[CMP-004-contextengine|ContextEngine]] gana `selectRetrievedCandidates` y `summaryContextBlock`; [[CMP-018-datagovernanceengine|DataGovernanceEngine]] gana `moreRestrictive` y `classifyDerivedData`.

### Contratos

- [[C-055-datasourcedescriptor|C-055 DataSourceDescriptor]]
- [[C-056-retrievedcandidate|C-056 RetrievedCandidate]]

### Deuda

Resuelve D-015, D-016, D-019, D-024 y D-047.

## Artículos constitucionales relevantes

P-01, P-14, P-22, P-31, P-38, INV-E07, INV-E11, INV-E26 (y EVO-09)

## Localización en el repo

`book/chapters/42-fuentes-de-datos/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
