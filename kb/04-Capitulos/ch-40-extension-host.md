---
id: "CH-40"
tipo: capitulo
titulo: "Extensiones que No Pueden Saltarse la Constitución"
tags: [capitulo, ch40, v0-3]
introduces_components: ["CMP-027"]
introduces_contracts: ["C-051", "C-052", "C-053"]
modifies_contracts: []
articulos_constitucionales: ["P-07", "P-12", "P-13", "INV-05", "INV-06", "INV-E24"]
---

# CH-40 — Extensiones que No Pueden Saltarse la Constitución

## Navegación

⬅ [[ch-39-modelo-como-dato|CH-39]] · **CH-40**

## Resultado esperado

Al terminar este capítulo podrás decidir si una extensión puede cargarse, en qué puntos del ciclo puede intervenir y qué puede devolver en cada uno. También podrás explicar por qué ningún hook puede autorizar una acción aunque pueda bloquearla.

## Qué introduce este capítulo

### Componentes

- [[CMP-027-extensionhost|CMP-027 ExtensionHost]]: hace verificable EVO-10. [[CMP-002-toolruntime|ToolRuntime]] conserva "ejecutar hooks".

### Contratos

- [[C-051-extensionregistration|C-051 ExtensionRegistration]]
- [[C-052-hookpoint|C-052 HookPoint]]
- [[C-053-resourcetrustdecision|C-053 ResourceTrustDecision]]

## Artículos constitucionales relevantes

P-07, P-12, P-13, INV-05, INV-06, INV-E24 (y EVO-10)

## Localización en el repo

`book/chapters/40-extension-host/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
