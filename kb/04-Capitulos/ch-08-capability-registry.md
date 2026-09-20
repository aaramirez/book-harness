---
id: "CH-08"
tipo: capitulo
titulo: "\"CapabilityRegistry y la Resolución Real de una Tool Call\""
tags: [capitulo, ch08]
introduces_components: ["CMP-008"]
introduces_contracts: ["C-018"]
articulos_constitucionales: ["P-03", "P-13", "P-26", "INV-03", "INV-04", "INV-05", "INV-18", "INV-19", "INV-20"]
---

# CH-08 — "CapabilityRegistry y la Resolución Real de una Tool Call"

## Navegación

⬅ [[ch-07-execution-controller|CH-07]] · **CH-08** · [[ch-09-event-bus|CH-09]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-008-capabilityregistry|CMP-008]] — Registrar las capabilities disponibles junto con su descriptor (nombre canónico, versión, schema de entrada esperado y una referencia opaca a su implementación concreta), resolver el capabilityName de una RawToolCallProposal contra ese registro, validar sus rawArguments contra el schema declarado y producir un ToolCall resuelto — sin ejecutar la capability, sin invocar al modelo ni interpretar su propuesta cruda, sin evaluar policy/autorización y sin decidir continuación de turno.

### Contratos

- [[C-018-capabilitydescriptor|C-018]] — CapabilityDescriptor (impacto: P-03, P-26, INV-04, INV-20)


## Artículos constitucionales relevantes

P-03, P-13, P-26, INV-03, INV-04, INV-05, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/08-capability-registry/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
