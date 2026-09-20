---
id: "CH-14"
tipo: capitulo
titulo: "\"AdmissionController y la Admisión de una Activación Cruda\""
tags: [capitulo, ch14]
introduces_components: ["CMP-012"]
introduces_contracts: ["C-022", "C-023"]
articulos_constitucionales: ["P-16", "P-17", "P-25", "INV-E01", "INV-E02", "INV-18", "INV-19", "INV-20"]
---

# CH-14 — "AdmissionController y la Admisión de una Activación Cruda"

## Navegación

⬅ [[ch-13-caminos-gobierno|CH-13]] · **CH-14** · [[ch-15-agent-communication-gateway|CH-15]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-012-admissioncontroller|CMP-012]] — Aplicar identity, authorization, tenant, capacity, rate, budget, deduplication y policy decisions sobre un ActivationRequest ya normalizado, antes de que cualquier ruteo hacia un agente concreto sea siquiera posible — produciendo un AdmissionDecision determinístico de dos resultados posibles (ADMIT/REJECT, nunca un Boolean) — sin decidir a qué agente concreto corresponde la activación, sin construir ningún AgentState y sin evaluar policy sobre ninguna acción ya resuelta.

### Contratos

- [[C-022-activationrequest|C-022]] — ActivationRequest (impacto: P-16, INV-E01)
- [[C-023-admissiondecision|C-023]] — AdmissionDecision (impacto: P-17, INV-E02, INV-19, INV-20)


## Artículos constitucionales relevantes

P-16, P-17, P-25, INV-E01, INV-E02, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/14-admission-controller/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
