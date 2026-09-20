---
id: "CH-22"
tipo: capitulo
titulo: "\"EvaluationHarness y la Certificación de un Candidato Antes de que Exista Ningún Run\""
tags: [capitulo, ch22]
introduces_components: ["CMP-020"]
introduces_contracts: ["C-032", "C-033"]
articulos_constitucionales: ["P-13", "P-28", "P-29", "INV-E13", "INV-18", "INV-19", "INV-20"]
---

# CH-22 — "EvaluationHarness y la Certificación de un Candidato Antes de que Exista Ningún Run"

## Navegación

⬅ [[ch-21-execution-fabric|CH-21]] · **CH-22** · [[ch-23-handoff-coordinator|CH-23]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-020-evaluationharness|CMP-020]] — Evaluar cualquier candidato (un agente, un prompt, una skill, un modelo, una policy o una capability) ANTES de su promoción controlada a producción, aplicando o verificando la policy de certificación que su clase de riesgo exige y produciendo un resultado de tres estados que nunca se reduce a aprobado/rechazado cuando la decisión no puede tomarse todavía — y correlacionar la ejecución de un run ya existente con un outcome de negocio medible, un SLA/SLO aplicable y una posible escalación humana — sin evaluar ni autorizar ninguna acción dentro de un run en curso, sin producir evidencia de auditoría inmutable, sin registrar versiones de capability y sin decidir si un run puede continuar operacionalmente.

### Contratos

- [[C-032-evaluationreport|C-032]] — EvaluationReport (impacto: P-28, INV-E13, INV-19)
- [[C-033-businessoutcomecorrelation|C-033]] — BusinessOutcomeCorrelation (impacto: P-29, INV-19)


## Artículos constitucionales relevantes

P-13, P-28, P-29, INV-E13, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/22-evaluation-harness/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
