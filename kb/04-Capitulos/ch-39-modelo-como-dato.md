---
id: "CH-39"
tipo: capitulo
titulo: "El Modelo como Dato: Catálogo, Costo y Cache"
tags: [capitulo, ch39, v0-3]
introduces_components: []
introduces_contracts: ["C-049", "C-050"]
modifies_contracts: ["C-006", "C-007"]
articulos_constitucionales: ["P-02", "P-29", "INV-09", "INV-E10"]
---

# CH-39 — El Modelo como Dato: Catálogo, Costo y Cache

## Navegación

⬅ [[ch-38-identidad-auditoria-retencion|CH-38]] · **CH-39** · [[ch-40-extension-host|CH-40]] ➡

## Resultado esperado

Al terminar este capítulo podrás decidir qué modelo usa un turno a partir de un catálogo, si la conversación cabe en su ventana, cuánto costó cada llamada y cuánto cuesta un resultado de negocio. También podrás explicar por qué el costo lo calcula el arnés y no el proveedor.

## Qué introduce este capítulo

Primer capítulo de v0.3.

### Componentes

- Ninguno. [[CMP-003-modelgateway|ModelGateway]] gana el catálogo, la cache efectiva, el costo calculado y la normalización de varias propuestas.

### Contratos

- [[C-049-modeldescriptor|C-049 ModelDescriptor]]
- [[C-050-usagerecord|C-050 UsageRecord]]
- **Modifica** [[C-006-modelrequest|C-006 ModelRequest]] → v2 (`cacheRetention`) y [[C-007-modelresponse|C-007 ModelResponse]] → v2 (`proposedToolCalls`, `usage`).

### Deuda

Resuelve D-021 (varias tool calls por respuesta, en el contrato). Registra D-044 (el journal de varias propuestas) con destino CH-49.

## Artículos constitucionales relevantes

P-02, P-29, INV-09, INV-E10

## Localización en el repo

`book/chapters/39-modelo-como-dato/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
