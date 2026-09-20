---
id: "CMP-017"
tipo: componente
nombre: "AuditLedger"
capitulo: "CH-19"
tags: [componente, cmp-017]
consumes: ["C-004"]
produces: ["C-010", "C-011", "C-029"]
articulos_constitucionales: ["P-13", "P-25", "INV-18", "INV-19", "INV-20", "INV-E10"]
---

# AuditLedger (CMP-017)

> Componente introducido en [[ch-19-audit-ledger|CH-19]] — parte del runtime del arnés.

## Responsabilidad

Producir y preservar, de forma estructuralmente inmutable (append-only, nunca editada ni borrada una vez escrita), evidencia de auditoría para una decisión crítica ya tomada por otro componente — capturando una referencia opaca a esa decisión, el snapshot exacto de versiones de agente/skill/policy/configuración de modelo/capability vigente en ese instante (INV-E10) y el actor/contexto que INV-19 exige — sin tomar ni modificar la decisión que audita, sin distribuir el flujo general de eventos operacionales del harness y sin autorizar el acceso de lectura al propio ledger.

## Decisiones que posee (owns)

- Logs, traces, execution ledger and immutable audit evidence have different purposes and MUST NOT be conflated (cita literal, P-25) — producir, en exclusiva, el subconjunto de evidencia estructuralmente inmutable que ese principio distingue de la telemetría operacional
- Every production run records exact versions of agent, skill, policy, model configuration and capability contracts (cita literal, INV-E10) — capturar el VersionSnapshot exacto vigente en el momento de la decisión auditada
- correlacionar cada AuditRecord con el actor (ActorId) y, cuando existe, el contexto (traceId) de la decisión auditada (INV-19)
- garantizar, por ausencia estructural de cualquier función de actualización o borrado, que un AuditRecord ya escrito nunca se edite ni se elimine (write-once por diseño, no por convención)
- producir una garantía de integridad verificable (contentHash) sobre el contenido de cada AuditRecord
- rechazar por defecto (fail-closed) un AuditRecord sin referencia de sujeto, sin actor, o con un VersionSnapshot incompleto

## Decisiones que NO posee (does_not_own)

- distribuir el flujo general de eventos operacionales del harness hacia consumidores desacoplados (EventBus, CMP-009, ya introducido en CH-09 — la frontera más importante de este capítulo: EventBus mueve un AgentEvent mutable, de alto volumen, para logs/tracing/debugging; AuditLedger produce un subconjunto específico, estructuralmente inmutable, de evidencia — nunca el flujo general)
- tomar la decisión que audita — evaluar policy (PolicyEngine, CMP-005, ya introducido en CH-05), aplicar control operacional (OperationalController, CMP-016, ya introducido en CH-18), decidir admisión (AdmissionController, CMP-012, ya introducido en CH-14), o cualquier otra decisión crítica ya tomada por su dueño correspondiente — AuditLedger registra una decisión YA TOMADA, nunca la toma ni la modifica
- autorizar el acceso de lectura al propio ledger (Preview, fuera de alcance de este capítulo)
- el mecanismo real y durable de almacenamiento append-only/WORM que preserva un AuditRecord más allá de la vida del proceso, y el algoritmo criptográfico real detrás de contentHash (Preview, infraestructura de borde)
- generar por sí mismo el subjectRef o el VersionSnapshot — ambos llegan como señales de entrada ya resueltas (mismo patrón que targetRef en CH-18)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-029-auditrecord|C-029]] |

## Artículos constitucionales

P-13, P-25, INV-18, INV-19, INV-20, INV-E10

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-19-audit-ledger|CH-19]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
