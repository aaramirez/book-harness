---
id: "CH-41"
tipo: capitulo
titulo: "Conexiones: MCP y OpenAPI como Fuentes de Capabilities"
tags: [capitulo, ch41, v0-3]
introduces_components: ["CMP-028"]
introduces_contracts: ["C-054"]
modifies_contracts: ["C-018"]
articulos_constitucionales: ["P-03", "P-27", "P-38", "INV-04", "INV-05", "INV-06", "INV-E08", "INV-E25"]
---

# CH-41 — Conexiones: MCP y OpenAPI como Fuentes de Capabilities

## Navegación

⬅ [[ch-40-extension-host|CH-40]] · **CH-41**

## Resultado esperado

Al terminar este capítulo podrás decidir cómo entra al arnés una herramienta que vive en un servidor MCP o en una API OpenAPI, qué ve el modelo de ella y qué no. También podrás explicar por qué recorre el mismo camino de resolución, política y ejecución que una herramienta propia.

## Qué introduce este capítulo

### Componentes

- [[CMP-028-connectionmanager|CMP-028 ConnectionManager]]: traduce las tools de una conexión declarada en capabilities `<conexión>__<tool>`, con filtro y argumentos provistos.

### Contratos

- [[C-054-connectiondescriptor|C-054 ConnectionDescriptor]]
- **Modifica** [[C-018-capabilitydescriptor|C-018 CapabilityDescriptor]] → v3 (`sourceConnectionId`, `executionKind`; ADR-005 Accepted).

### Deuda

Resuelve D-018 (credencial de la conexión por llamante) y D-025 (tipo de ejecución en el descriptor).

## Artículos constitucionales relevantes

P-03, P-27, P-38, INV-04, INV-05, INV-06, INV-E08, INV-E25

## Localización en el repo

`book/chapters/41-conexiones/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
