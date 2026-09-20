---
id: "CMP-012"
tipo: componente
nombre: "AdmissionController"
capitulo: "CH-14"
tags: [componente, cmp-012]
consumes: ["C-022"]
produces: ["C-011", "C-023"]
articulos_constitucionales: ["P-16", "P-17", "P-25", "INV-E01", "INV-E02", "INV-18", "INV-19", "INV-20"]
---

# AdmissionController (CMP-012)

> Componente introducido en [[ch-14-admission-controller|CH-14]] — parte del runtime del arnés.

## Responsabilidad

Aplicar identity, authorization, tenant, capacity, rate, budget, deduplication y policy decisions sobre un ActivationRequest ya normalizado, antes de que cualquier ruteo hacia un agente concreto sea siquiera posible — produciendo un AdmissionDecision determinístico de dos resultados posibles (ADMIT/REJECT, nunca un Boolean) — sin decidir a qué agente concreto corresponde la activación, sin construir ningún AgentState y sin evaluar policy sobre ninguna acción ya resuelta.

## Decisiones que posee (owns)

- apply identity, authorization, tenant, capacity, rate, budget, deduplication and policy decisions before routing (cita literal, Amendment v1.1, P-17)
- decidir, con un outcome de dos valores (ADMIT/REJECT), si un ActivationRequest ya normalizado puede proceder
- rechazar por defecto (fail-closed) cuando ninguna regla de admisión concede acceso (Default Reject)
- correlacionar cada AdmissionDecision de vuelta con el ActivationRequest que la motivó (requestId)

## Decisiones que NO posee (does_not_own)

- normalizar el estímulo externo crudo en un ActivationRequest (Ingress Adapter — infraestructura de borde, Amendment v1.1 P-16, no un componente propio de este registry)
- resolver o rutear una activación admitida hacia un AgentId/AgentConfig concreto (Routing, Amendment v1.1 — P-17 la coloca explícitamente "before routing"; sin componente propio todavía en este registry)
- construir el AgentState/AgentActivationRequest real de un agente concreto (AgentCore, CMP-011, ya introducido en CH-11 — AdmissionController decide SI se puede proceder, AgentCore decide CÓMO nace el run)
- evaluar policy sobre una ToolCall ya en curso (PolicyEngine, CMP-005, ya introducido en CH-05 — distinto momento, distinta pregunta: "¿puede esta activación empezar?" vs. "¿puede esta acción ejecutarse?")

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-022-activationrequest|C-022]] |
| 🡐 Produce | [[C-011-harnesserror|C-011]], [[C-023-admissiondecision|C-023]] |

## Artículos constitucionales

P-16, P-17, P-25, INV-E01, INV-E02, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-14-admission-controller|CH-14]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
