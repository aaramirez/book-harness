---
id: "CH-24"
tipo: capitulo
titulo: "\"SkillLibrary y el Conocimiento Procedural que Nunca Fue una Capability\""
tags: [capitulo, ch24]
introduces_components: ["CMP-022"]
introduces_contracts: ["C-035"]
articulos_constitucionales: ["P-07", "P-13", "INV-18", "INV-19", "INV-20"]
---

# CH-24 — "SkillLibrary y el Conocimiento Procedural que Nunca Fue una Capability"

## Navegación

⬅ [[ch-23-handoff-coordinator|CH-23]] · **CH-24** · [[ch-25-epilogo|CH-25]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-022-skilllibrary|CMP-022]] — Registrar el descriptor de una skill — conocimiento procedural reusable, nombre canónico, versión y una referencia opaca al procedimiento/guía real — como una capa separada del core del agente, de las tools/capabilities y de la identidad del agente, y resolver qué SkillDescriptor aplica a una situación nombrada — sin resolver qué implementación concreta satisface una capability solicitada, sin representar la identidad/configuración de un agente, sin ejecutar ningún side effect y sin decidir autorización sobre ninguna acción.

### Contratos

- [[C-035-skilldescriptor|C-035]] — SkillDescriptor (impacto: P-07, INV-19)


## Artículos constitucionales relevantes

P-07, P-13, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/24-skill-library/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
