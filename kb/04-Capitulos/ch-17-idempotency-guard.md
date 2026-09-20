---
id: "CH-17"
tipo: capitulo
titulo: "\"IdempotencyGuard y la Deduplicación de un Side Effect Crítico\""
tags: [capitulo, ch17]
introduces_components: ["CMP-015"]
introduces_contracts: ["C-027"]
articulos_constitucionales: ["P-13", "P-24", "INV-11", "INV-E09", "INV-18", "INV-19", "INV-20"]
---

# CH-17 — "IdempotencyGuard y la Deduplicación de un Side Effect Crítico"

## Navegación

⬅ [[ch-16-credential-broker|CH-16]] · **CH-17** · [[ch-18-operational-controller|CH-18]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-015-idempotencyguard|CMP-015]] — Rastrear, para un ToolCall con side effects (C-008, CH-02) identificado por una clave de idempotencia ya asumida como dada, si esa ejecución ya ocurrió antes bajo esa misma clave — permitiendo, cuando corresponda, reusar el ToolResult (C-009, CH-02) ya producido en vez de duplicar el side effect real — y registrar, una vez que una ejecución nueva concluye, el IdempotencyRecord terminal correspondiente, sin sobrescribir jamás uno ya producido — sin ejecutar el side effect en sí, sin decidir autorización, sin resolver qué implementación satisface la capability y sin decidir si un run puede reintentar contra su presupuesto.

### Contratos

- [[C-027-idempotencyrecord|C-027]] — IdempotencyRecord (impacto: INV-11, P-24, INV-E09)


## Artículos constitucionales relevantes

P-13, P-24, INV-11, INV-E09, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/17-idempotency-guard/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
