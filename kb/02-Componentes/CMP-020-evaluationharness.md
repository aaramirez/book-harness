---
id: "CMP-020"
tipo: componente
nombre: "EvaluationHarness"
capitulo: "CH-22"
tags: [componente, cmp-020]
consumes: ["C-004"]
produces: ["C-010", "C-011", "C-032", "C-033"]
articulos_constitucionales: ["P-13", "P-28", "P-29", "INV-E13", "INV-18", "INV-19", "INV-20"]
---

# EvaluationHarness (CMP-020)

> Componente introducido en [[ch-22-evaluation-harness|CH-22]] — parte del runtime del arnés.

## Responsabilidad

Evaluar cualquier candidato (un agente, un prompt, una skill, un modelo, una policy o una capability) ANTES de su promoción controlada a producción, aplicando o verificando la policy de certificación que su clase de riesgo exige y produciendo un resultado de tres estados que nunca se reduce a aprobado/rechazado cuando la decisión no puede tomarse todavía — y correlacionar la ejecución de un run ya existente con un outcome de negocio medible, un SLA/SLO aplicable y una posible escalación humana — sin evaluar ni autorizar ninguna acción dentro de un run en curso, sin producir evidencia de auditoría inmutable, sin registrar versiones de capability y sin decidir si un run puede continuar operacionalmente.

## Decisiones que posee (owns)

- Candidate agents, prompts, skills, models, policies and capabilities MUST be evaluable in an Evaluation Harness before controlled promotion to production (cita literal, P-28) — evaluar, en exclusiva, cualquier candidato completo antes de su promoción controlada a producción, completamente separado de evaluar una acción dentro de un run ya existente
- Production promotion requires certification policy where risk class requires it (cita literal, INV-E13) — aplicar o verificar, según la RiskClass de un candidato, si una policy de certificación aplica, produciendo NEEDS_REVIEW en vez de fabricar CERTIFIED/REJECTED cuando esa certificación no puede resolverse todavía
- Technical success does not imply business success. Enterprise runs SHOULD correlate execution with measurable outcomes, value, SLA/SLO and human escalation (cita literal, P-29) — correlacionar, en exclusiva, la ejecución de un run ya existente con un outcome de negocio medible, una referencia opaca a un SLA/SLO aplicable, y una posible escalación humana
- rechazar por defecto (fail-closed) un EvaluationReport sin referencia al candidato que evalúa, o un BusinessOutcomeCorrelation sin referencia al run que correlaciona

## Decisiones que NO posee (does_not_own)

- evaluar o autorizar una acción concreta dentro de un run ya en curso (PolicyEngine, CMP-005, ya introducido en CH-05 — la frontera más importante de este capítulo: PolicyEngine decide si UNA ACCIÓN puede ocurrir DENTRO de un run que ya existe; EvaluationHarness decide si UN CANDIDATO debe promoverse a producción ANTES de que exista ningún run que lo use)
- producir evidencia de auditoría estructuralmente inmutable sobre la decisión de certificación (AuditLedger, CMP-017, ya introducido en CH-19 — EvaluationHarness produce el resultado de evaluación; auditarlo de forma inmutable, si alguien lo necesita, es responsabilidad de AuditLedger)
- registrar versiones de capability o gestionar su lifecycle de rollout/deprecation/retirement (CapabilityRegistry, CMP-008, ya introducido en CH-08 — CapabilityRegistry declara qué CapabilityDescriptor existen y cuál es su version; EvaluationHarness evalúa, mediante subjectRef, si una versión concreta YA REGISTRADA debe certificarse)
- decidir si un run puede continuar operacionalmente contra su ExecutionBudget (ExecutionController, CMP-007, ya introducido en CH-07)
- representar, persistir o resolver la intervención humana que NEEDS_REVIEW exige (HumanInteractionService, CMP-006, ya introducido en CH-06 — EvaluationHarness produce el estado que exige esa intervención; HumanInteractionService es quien la representa, persiste y resuelve)
- aplicar kill switches, aislamiento de tenant, o cualquier otro control operacional (OperationalController, CMP-016, ya introducido en CH-18)
- ejecutar el mecanismo real de evaluación — correr el candidato contra un dataset de test real, calcular métricas reales de calidad o seguridad, o medir en la práctica un outcome de negocio (Preview, infraestructura de borde)
- generar por sí mismo el subjectRef, la riskClass, la señal de si la certificación ya se satisfizo, el runId o el measuredOutcome — todas llegan como señales de entrada ya resueltas (mismo patrón que subjectRef en CH-19/CH-20, o runId/topology en CH-21)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-032-evaluationreport|C-032]], [[C-033-businessoutcomecorrelation|C-033]] |

## Artículos constitucionales

P-13, P-28, P-29, INV-E13, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-22-evaluation-harness|CH-22]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
