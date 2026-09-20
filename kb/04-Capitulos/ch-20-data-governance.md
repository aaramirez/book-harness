---
id: "CH-20"
tipo: capitulo
titulo: "\"DataGovernanceEngine y la Etiqueta de Gobernanza que Viaja con el Dato\""
tags: [capitulo, ch20]
introduces_components: ["CMP-018"]
introduces_contracts: ["C-030"]
articulos_constitucionales: ["P-13", "P-22", "INV-18", "INV-19", "INV-20", "INV-E11"]
---

# CH-20 — "DataGovernanceEngine y la Etiqueta de Gobernanza que Viaja con el Dato"

## Navegación

⬅ [[ch-19-audit-ledger|CH-19]] · **CH-20** · [[ch-21-execution-fabric|CH-21]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-018-datagovernanceengine|CMP-018]] — Clasificar cualquier dato que fluye por el sistema (un ContextBlock ya seleccionado, un ToolResult ya producido, o cualquier otro dato futuro) con un nivel de sensibilidad, un requisito de residencia, una fecha límite de retención, una bandera de legal-hold y una referencia de lineage — produciendo una etiqueta de gobernanza portátil que viaja junto con el dato a través de fronteras de componentes, de forma completamente independiente de si el modelo entiende o acepta esos requisitos — sin decidir si ese dato es relevante para el turno actual, sin decidir si puede verse en absoluto, sin reclasificar un secreto ya clasificado por CredentialBroker y sin producir evidencia de auditoría inmutable.

### Contratos

- [[C-030-datagovernancelabel|C-030]] — DataGovernanceLabel (impacto: P-22, INV-E11, INV-19)


## Artículos constitucionales relevantes

P-13, P-22, INV-18, INV-19, INV-20, INV-E11

## Localización en el repo

`book/chapters/20-data-governance-engine/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
