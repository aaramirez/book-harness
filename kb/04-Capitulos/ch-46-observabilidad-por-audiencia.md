---
id: "CH-46"
tipo: capitulo
titulo: "Observabilidad Acotada por Audiencia"
tags: [capitulo, ch46, v0-3]
introduces_components: []
introduces_contracts: ["C-061", "C-062", "C-063"]
modifies_contracts: []
articulos_constitucionales: ["P-04", "P-22", "P-25", "P-37", "INV-E11", "INV-E23"]
---

# CH-46 — Observabilidad Acotada por Audiencia

## Navegación

⬅ [[ch-45-evolucion-del-runtime|CH-45]] · **CH-46** · [[ch-47-evaluacion-con-lift|CH-47]] ➡

## Resultado esperado

Al terminar este capítulo podrás decidir qué contenido de una sesión puede llegar a cada destino de telemetría y qué datos pueden entrar al contexto según quién ve la sesión, y explicar en qué se diferencian un evento, una entrada de auditoría y un span.

## Qué introduce este capítulo

### Componentes

- Ninguno nuevo. [[CMP-018-datagovernanceengine|DataGovernanceEngine]] gana la audiencia de la sesión y los techos de captura y de contexto; [[CMP-009-eventbus|EventBus]] gana `fanOutSpan`.

### Contratos

- [[C-061-sessionaudience|C-061 SessionAudience]]
- [[C-062-tracecapturepolicy|C-062 TraceCapturePolicy]]
- [[C-063-telemetryspan|C-063 TelemetrySpan]]

### Deuda

Sin deudas con destino CH-46.

## Artículos constitucionales relevantes

P-04, P-22, P-25, P-37, INV-E11, INV-E23

## Localización en el repo

`book/chapters/46-observabilidad-por-audiencia/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
