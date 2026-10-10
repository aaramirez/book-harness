---
id: "CH-48"
tipo: capitulo
titulo: "El Agente como Directorio: Autoría por Convención"
tags: [capitulo, ch48, v0-3]
introduces_components: []
introduces_contracts: ["C-065", "C-066"]
modifies_contracts: []
articulos_constitucionales: ["P-06", "P-39", "INV-09", "INV-E27"]
---

# CH-48 — El Agente como Directorio: Autoría por Convención

## Navegación

⬅ [[ch-47-evaluacion-con-lift|CH-47]] · **CH-48** · [[ch-49-integracion-conectada|CH-49]] ➡

## Resultado esperado

Al terminar este capítulo podrás decidir dónde va cada parte de un agente escrito como directorio y qué contrato produce cada ubicación, y explicar qué diagnósticos impiden activarlo y por qué el runtime no infiere nada que no esté declarado.

## Qué introduce este capítulo

### Componentes

- Ninguno nuevo. Un **adaptador de autoría** (sin componente) descubre el directorio; [[CMP-011-agentcore|AgentCore]] gana `requireActivatableManifest` (INV-E27).

### Contratos

- [[C-065-agentmanifest|C-065 AgentManifest]]
- [[C-066-authoringdiagnostic|C-066 AuthoringDiagnostic]]

### Deuda

Sin deudas con destino CH-48.

## Artículos constitucionales relevantes

P-06, P-39, INV-09, INV-E27 (y EVO-10)

## Localización en el repo

`book/chapters/48-agente-como-directorio/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
