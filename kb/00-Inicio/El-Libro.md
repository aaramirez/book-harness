---
id: el-libro
tipo: concepto
tags: [libro, inicio]
---

# El Libro: ¿Cómo construir un arnés?

Libro que enseña a construir, capítulo a capítulo, un **Agent Harness** ("arnés de agentes"): una infraestructura segura, observable, extensible y agnóstica al modelo donde los sistemas probabilísticos (LLMs) **proponen** decisiones y los mecanismos determinísticos **gobiernan** su ejecución y consecuencias.

## Datos

- **Versión**: 0.3
- **Idioma**: español (identificadores técnicos en inglés)
- **Estructura**: 50 capítulos (CH-00..CH-49)
- **Regla suprema**: *Probabilistic systems may propose decisions. Deterministic systems must govern consequences.*

## Cómo se construye

Cada capítulo introduce, en orden estricto, **contratos** (C-XXX, estructuras de datos canónicas) y **componentes** (CMP-XXX, unidades del runtime con responsabilidad exclusiva), validados contra la [[Architecture-Constitution|Constitución]]. Un capítulo nunca puede usar una entidad que todavía no ha sido definida ("no magic entities").

## Qué contiene

- **CH-00** — la constitución y los 7 contratos canónicos (AgentMessage, AgentConfig, AgentState, ExecutionContext, AgentEvent, HarnessError, ExecutionBudget)
- **CH-01..CH-11** — los 11 componentes del runtime (AgentLoop, ToolRuntime, ModelGateway, ContextEngine, PolicyEngine, HumanInteractionService, ExecutionController, CapabilityRegistry, EventBus, SessionManager, AgentCore)
- **CH-12..CH-13** — integración: camino feliz y caminos de gobierno
- **CH-14..CH-24** — la Enmienda v1.1 (enterprise): AdmissionController, AgentCommunicationGateway, CredentialBroker, IdempotencyGuard, OperationalController, AuditLedger, DataGovernanceEngine, ExecutionFabricAdapter, EvaluationHarness, HandoffCoordinator, SkillLibrary
- **CH-25..CH-27** — epílogo y cierre enterprise
- **CH-28..CH-36** — la Enmienda v1.2, operación durable (v0.2): ExecutionJournal, ResumptionCoordinator, ContinuationRegistry, IsolatedExecutionEnvironment
- **CH-37..CH-38** — cierre de la deuda de v0.2 (v0.2.1)
- **CH-39..CH-49** — conectividad (v0.3): ExtensionHost, ConnectionManager, RetrievalEngine, presupuestos heredados, invocación entre agentes, evolución del runtime, observabilidad por audiencia, evaluación con lift, el agente como directorio y la integración conectada

## Ver también

- [[Index|Mapa del libro]]
- [[Architecture-Constitution|La Constitución]]
