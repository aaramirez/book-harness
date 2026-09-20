---
id: "CMP-016"
tipo: componente
nombre: "OperationalController"
capitulo: "CH-18"
tags: [componente, cmp-016]
consumes: ["C-003", "C-004"]
produces: ["C-010", "C-011", "C-028"]
articulos_constitucionales: ["P-13", "P-30", "INV-08", "INV-18", "INV-19", "INV-20", "INV-E14"]
---

# OperationalController (CMP-016)

> Componente introducido en [[ch-18-operational-controller|CH-18]] — parte del runtime del arnés.

## Responsabilidad

Emitir y aplicar un comando operacional (ControlDirective) que deshabilita una capability, aísla los runs de un tenant, revierte un rollout o fuerza, mediante un kill switch, la terminación inmediata de un AgentRun — actuando siempre desde AFUERA del ciclo de cualquier run particular y sin depender de la cooperación del modelo ni de AgentLoop — sin decidir si UN run específico puede seguir contra su propio presupuesto operacional, sin autorizar ninguna acción ya resuelta, sin resolver qué implementación satisface una capability y sin ejecutar el side effect en sí.

## Decisiones que posee (owns)

- The platform MUST support cancellation, capability disablement, tenant isolation, rollout rollback and kill switches without relying on model cooperation (cita literal, P-30 — "cancellation" se provee aquí exclusivamente como KILL_SWITCH, la mitad externa; la mitad interna, evaluada desde dentro del ciclo de un run, sigue siendo de ExecutionController)
- Kill switches operate independently of AgentLoop (cita literal, INV-E14)
- emitir un ControlDirective (ISSUED) para cualquiera de los cuatro tipos, rechazando por defecto (fail-closed) uno sin referencia de alcance (targetRef)
- forzar, para un ControlDirective de tipo KILL_SWITCH, la transición inmediata de un AgentState en un AgentRunStatus no terminal hacia CANCELLED, sin invocar evaluateExecutionContinuation (ExecutionController, CH-07) ni ningún turno de AgentLoop (CH-01)
- registrar, de forma terminal y write-once, cuándo un ControlDirective ya se aplicó (APPLIED), rechazando reaplicar uno ya APPLIED
- rechazar por defecto (fail-closed) un kill switch cuyo AgentRun objetivo ya alcanzó un AgentRunStatus terminal por cualquier otra vía — la regla explícita que resuelve el "empate" con ExecutionController

## Decisiones que NO posee (does_not_own)

- decidir si UN AgentRun específico puede seguir operacionalmente contra su ExecutionBudget, evaluado desde DENTRO del propio ciclo de esa ejecución (ExecutionController, CMP-007, ya introducido en CH-07 — distinción central de este capítulo: "¿puedo seguir intentando, evaluado desde dentro de mi propio ciclo?" nunca es "¿debe el control externo forzar mi fin, desde afuera, sin pedir cooperación?"; la mitad de "cancellation" evaluada por presupuesto sigue siendo, sin excepción, de ExecutionController)
- decidir si una acción/ToolCall ya resuelta está autorizada (PolicyEngine, CMP-005, ya introducido en CH-05 — distinta pregunta, distinto momento: "¿debe detenerse/deshabilitarse esto por control operacional?" nunca es "¿está permitido hacerlo?")
- resolver qué implementación satisface una capability solicitada (CapabilityRegistry, CMP-008, ya introducido en CH-08 — este componente decide SI una capability está deshabilitada, nunca CUÁL implementación la satisface)
- ejecutar el side effect en sí (ToolRuntime, CMP-002, ya introducido en CH-02)
- generar el targetRef mismo, ni decidir a qué capability/tenant/rollout/run corresponde en el mundo real más allá de la referencia opaca ya provista (asumida como una señal de entrada dada)
- el mecanismo real y distribuido que efectivamente impide invocar una capability deshabilitada, bloquea físicamente los runs de un tenant aislado, o redespliega una versión anterior de un rollout (Preview, infraestructura de borde, no un componente propio de este registry)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-003-agentstate|C-003]], [[C-004-executioncontext|C-004]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-028-controldirective|C-028]] |

## Artículos constitucionales

P-13, P-30, INV-08, INV-18, INV-19, INV-20, INV-E14

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-18-operational-controller|CH-18]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
