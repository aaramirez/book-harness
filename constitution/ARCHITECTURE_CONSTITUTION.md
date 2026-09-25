# Agent Harness Architecture Constitution
## Version 1.0 — Foundational Architecture Rules

> **Constitutional rule:** Probabilistic systems may propose decisions. Deterministic systems must govern consequences.

---

# Nota de adopción — Book Production Harness ("arnés")

Este documento es la semilla constitucional adoptada por el **Book Production Harness** de este
repositorio (`book-harness`), tal como exige la Fase 0 del plan de ejecución
(`planes/2026-08-23-book-harness-como-construir-un-arnes.md`).

Se conserva íntegro y sin traducir el contenido original de `ARCHITECTURE_CONSTITUTION(1).md`
(Principios P-01..P-30, Invariantes INV-01..INV-20 más INV-E01..INV-E14, Component Sovereignty,
Decision Ownership, Lifecycle, Execution, Failure, Human Interaction, Resources, Observability,
Evolution y Deterministic vs Agentic Boundary). Es la misma constitución que:

1. gobierna el diseño del propio Book Production Harness (agentes, skills, validadores, policies
   de `book-harness`), y
2. es la constitución **que el libro "¿Cómo construir un arnés?" enseña a construir**, empezando
   por el capítulo piloto (`book/chapters/00-arquitectura-constitucion/chapter.md`), que introduce
   su vocabulario (`AgentMessage`, `AgentConfig`, `AgentState`, `ExecutionContext`, `AgentEvent`,
   `HarnessError`, `ExecutionBudget`) como los primeros contratos canónicos del libro.

"Agent Harness" en este documento se traduce conceptualmente como "arnés de agentes" o simplemente
"arnés" en la prosa del libro; los identificadores técnicos (`AgentLoop`, `ToolRuntime`, `PolicyEngine`,
etc.) permanecen en inglés por decisión editorial (ver §8 del plan de ejecución).

---

# Preámbulo

Esta Architecture Constitution define las reglas fundamentales que gobiernan el diseño, implementación, evolución y operación de un Agent Harness.

El harness existe para proporcionar una infraestructura segura, observable, extensible, durable y agnóstica al modelo, donde sistemas probabilísticos puedan interpretar objetivos, razonar y proponer acciones, mientras mecanismos determinísticos gobiernan su ejecución y sus consecuencias.

```text
Probabilistic Intelligence
        │
        │ proposes
        ▼
Deterministic Runtime
        │
        │ governs
        ▼
External World
```

El modelo puede decidir **qué intentar**.

El harness decide **qué puede ocurrir, cómo puede ocurrir, bajo qué límites y con qué trazabilidad**.

Esta constitución debe utilizarse como criterio para:

- diseño de componentes;
- architecture reviews;
- pull requests;
- incorporación de nuevas capacidades;
- definición de extensiones;
- integraciones;
- seguridad;
- gobierno;
- evaluación de trade-offs;
- breaking changes;
- evolución del runtime.

La Constitution se organiza en los siguientes artículos:

```text
Architecture Constitution
│
├── Article I   — Fundamental Principles
├── Article II  — Invariants
├── Article III — Component Sovereignty
├── Article IV  — Decision Ownership
├── Article V   — Lifecycle
├── Article VI  — Execution
├── Article VII — Failure Semantics
├── Article VIII — Human Interaction
├── Article IX  — Resources and Budgets
├── Article X   — Observability
├── Article XI  — Evolution
└── Article XII — Deterministic vs Agentic Boundary
```

---

# Article I — Fundamental Principles

## P-01 — Context is a first-class architectural component

El contexto no es simplemente historial de conversación. Debe ser construido, seleccionado, priorizado, resumido, limitado y controlado por el harness.

## P-02 — The model is replaceable

El runtime nunca debe depender estructuralmente de un proveedor específico. Los modelos se integran mediante contratos y adapters.

## P-03 — Tools are explicit capabilities, not prompt tricks

Toda acción sobre el mundo externo debe representarse mediante contratos explícitos, validables y observables.

## P-04 — Every action produces observable events

Las operaciones relevantes deben generar eventos que permitan UI, logging, tracing, persistence, analytics y audit.

## P-05 — Side effects pass through policy

Toda acción con efectos secundarios debe atravesar una capa determinística de validación, autorización y políticas.

## P-06 — Agents are configuration over a shared runtime

Los agentes deben configurarse sobre un runtime común en lugar de convertirse en aplicaciones independientes que reimplementan infraestructura.

## P-07 — Skills encode reusable procedural knowledge

El conocimiento procedural reusable debe estar separado del core, las tools y la identidad del agente.

## P-08 — Agent state and session state are different concerns

El estado operativo de una ejecución y la historia persistente de una sesión son responsabilidades diferentes.

## P-09 — Single-agent reliability precedes multi-agent complexity

No se debe introducir multi-agent como sustituto de resolver correctamente context, tools, state, reliability y governance.

## P-10 — The harness owns execution state—not the model

El modelo propone decisiones semánticas. El harness controla continuidad, ejecución, estado, límites y lifecycle.

## P-11 — UI is an adapter, not part of the core

TUI, Web, API, IDE, Slack, Teams u otras interfaces son adapters alrededor del mismo runtime.

## P-12 — Events observe; hooks intervene

Los eventos comunican hechos ocurridos. Los hooks permiten intervenir en puntos controlados del lifecycle.

## P-13 — Authorization is deterministic and external to the LLM

El modelo nunca constituye una fuente de verdad para identidad, permisos o autorización.

## P-14 — Context should be selected, not dumped

Más contexto no implica mejor razonamiento. El harness debe seleccionar información relevante dentro de presupuestos explícitos.

## P-15 — Automation and agents should share the same execution substrate

Automatizaciones, agentes interactivos y agentes autónomos deben compartir infraestructura de estado, tools, políticas, eventos, observabilidad y durable execution.

---

# Article II — Invariants

Los invariants son reglas verificables que nunca deben violarse.

## Model Invariants

### INV-01
`AgentCore` no depende directamente de APIs específicas de OpenAI, Anthropic, Google u otro proveedor.

### INV-02
Toda comunicación interna del runtime utiliza contratos propios, incluyendo `AgentMessage`.

### INV-03
El modelo nunca constituye una fuente de autorización.

## Tool Invariants

### INV-04
Todo `ToolCall` debe validarse antes de ejecutarse.

### INV-05
Todo `ToolCall` pasa por `ToolRuntime`.

### INV-06
Todo side effect pasa por `PolicyEngine`.

### INV-07
Todo `ToolResult` vuelve al ciclo del agente como observación explícita cuando el lifecycle continúa.

## Execution Invariants

### INV-08
El harness es propietario del execution state.

### INV-09
Todo `AgentRun` tiene límites explícitos.

### INV-10
Todo `AgentRun` debe poder cancelarse.

### INV-11
Side effects críticos deben soportar idempotencia, deduplicación o una protección equivalente.

## State Invariants

### INV-12
`AgentState` y `SessionState` permanecen conceptualmente independientes.

### INV-13
Una ejecución durable debe poder reconstruirse desde estado persistido suficiente.

## Human Interaction Invariants

### INV-14
Human Interaction nunca depende de una interfaz particular.

### INV-15
Una acción que requiere aprobación no puede ejecutarse antes de una resolución válida.

## UI Invariants

### INV-16
`AgentCore` puede ejecutarse sin UI.

### INV-17
La UI observa y presenta el runtime mediante contratos; no contiene la lógica soberana del AgentLoop.

## Observability Invariants

### INV-18
Toda acción significativa produce un evento observable.

### INV-19
Toda decisión crítica debe poder trazarse hasta su actor, contexto y policy relevante.

### INV-20
Todo error operacional pertenece a una categoría conocida.

---

# Article III — Component Sovereignty

El runtime se compone de dominios con responsabilidades explícitas.

```text
Agent Runtime
│
├── AgentCore
├── AgentLoop
├── ModelGateway
├── ContextEngine
├── ToolRuntime
├── PolicyEngine
├── SessionManager
├── HumanInteractionService
├── EventBus
├── ExecutionController
└── CapabilityRegistry
```

## AgentCore

Responsable de representar y coordinar las primitives fundamentales del agente.

No debe absorber responsabilidades de UI, persistencia específica, proveedores o business integrations.

## AgentLoop

Responsable de:

- turn lifecycle;
- model → action → observation cycle;
- continuation;
- completion;
- coordinación de la ejecución cognitiva.

No responsable de:

- autorización;
- rendering;
- almacenamiento concreto;
- APIs específicas de proveedores.

## ModelGateway

Responsable de:

- selección de provider;
- adaptación de mensajes;
- invocación del modelo;
- streaming;
- normalización de respuestas.

## ContextEngine

Responsable de:

- selección;
- ranking;
- composición;
- compaction;
- context budgets;
- provenance.

## ToolRuntime

Responsable de:

- resolver tools/capabilities;
- validar llamadas;
- ejecutar hooks;
- coordinar ejecución;
- devolver resultados normalizados.

## PolicyEngine

Responsable de:

- allow;
- deny;
- constraints;
- approval requirements;
- policy evaluation.

## SessionManager

Responsable de:

- persistencia;
- recuperación;
- branching;
- checkpoints;
- reconstrucción.

## HumanInteractionService

Responsable de:

- representar solicitudes humanas;
- persistir interacciones pendientes;
- recibir resoluciones;
- permitir reanudación.

## EventBus

Responsable de distribuir eventos del runtime a consumidores desacoplados.

## ExecutionController

Responsable de:

- budgets;
- cancellation;
- deadlines;
- runtime limits;
- operational continuation.

## CapabilityRegistry

Responsable de desacoplar la intención de una capacidad de su implementación concreta.

---

# Article IV — Decision Ownership

Cada decisión arquitectónica debe tener un owner definido.

```text
LLM
→ What should I try?

AgentLoop
→ Should another reasoning turn occur?

ContextEngine
→ What should the model know?

ModelGateway
→ How should the selected model be invoked?

ToolRuntime
→ How should an approved action be executed?

PolicyEngine
→ May this action occur?

HumanInteractionService
→ How is required human intervention represented and resolved?

SessionManager
→ What execution history and checkpoints persist?

ExecutionController
→ May the run continue operationally?

CapabilityRegistry
→ What implementation satisfies a requested capability?

UI
→ How is runtime state presented and human input transported?
```

## Ownership Rule

> Ningún componente debe absorber silenciosamente decisiones que pertenecen a otro dominio.

Cuando una decisión no tiene owner claro, debe resolverse arquitectónicamente antes de implementar la feature.

---

# Article V — Lifecycle

El Agent Harness debe utilizar un lifecycle explícito.

```text
CREATED
   ↓
INITIALIZING
   ↓
RUNNING
   ↓
┌────────────────────────┐
│ WAITING_FOR_MODEL      │
│ WAITING_FOR_TOOL       │
│ WAITING_FOR_HUMAN      │
└────────────────────────┘
   ↓
RUNNING
   ↓
COMPLETED
```

Estados alternativos:

```text
PAUSED
FAILED
CANCELLED
EXPIRED
```

Contrato sugerido:

```ts
type AgentRunStatus =
  | "created"
  | "initializing"
  | "running"
  | "waiting_for_model"
  | "waiting_for_tool"
  | "waiting_for_human"
  | "paused"
  | "completed"
  | "failed"
  | "cancelled"
  | "expired";
```

## Lifecycle Rule

El LLM no controla directamente la máquina de estados operacional.

Ejemplo:

```text
WAITING_FOR_HUMAN
        │
        ├── approved  → RUNNING
        ├── rejected  → RUNNING / FAILED
        ├── expired   → FAILED / EXPIRED
        └── cancelled → CANCELLED
```

---

# Article VI — Execution Constitution

Toda acción ejecutable debe atravesar un camino controlado.

```text
Tool Intent
     ↓
Resolve Capability
     ↓
Validate Schema
     ↓
beforeToolCall
     ↓
Policy Evaluation
     ↓
Authorization
     ↓
Human Approval?
     ↓
Execution Budget
     ↓
Sandbox
     ↓
Execute
     ↓
afterToolCall
     ↓
ToolResult
     ↓
Observation
```

## Execution Rules

1. `AgentLoop` no ejecuta directamente side effects.
2. Las tools se ejecutan exclusivamente mediante `ToolRuntime`.
3. Las policies se evalúan antes del side effect.
4. Los hooks pueden intervenir en puntos definidos.
5. Las tool calls independientes pueden paralelizarse.
6. Las operaciones dependientes o con shared mutable state deben respetar secuencialidad.
7. Toda ejecución debe aceptar cancellation cuando técnicamente sea posible.
8. Las operaciones críticas deben ser auditables.

---

# Article VII — Failure Constitution

Todo fallo debe clasificarse.

```text
ValidationError
PolicyError
ToolError
ModelError
ContextError
HumanInteractionError
PersistenceError
InfrastructureError
BudgetExceeded
Cancellation
FatalError
```

Contrato conceptual:

```ts
interface HarnessError {
  category: ErrorCategory;
  recoverable: boolean;
  retryable: boolean;
  retryAfter?: number;
  cause?: Error;
  metadata?: unknown;
}
```

## Failure Examples

```text
HTTP 503
→ transient / retryable

Invalid tool arguments
→ validation / recoverable

Policy denied
→ policy / non-retryable

Tool timeout
→ tool / potentially retryable

Model unavailable
→ model / potentially provider fallback

Budget exceeded
→ stop execution

User cancellation
→ graceful cancellation

Corrupt session
→ infrastructure/fatal
```

## Failure Rule

Retries, fallbacks y recovery deben obedecer políticas determinísticas; no deben depender exclusivamente del modelo.

---

# Article VIII — Human Interaction Constitution

Human-in-the-loop es una capacidad del runtime, no de la TUI.

Tipos mínimos:

```text
Approval
Input
Review
Decision
```

Flujo:

```text
HumanInteractionRequest
        ↓
Persist
        ↓
WAITING_FOR_HUMAN
        ↓
Channel Adapter
        ↓
Human
        ↓
Resolution
        ↓
Resume
```

Canales posibles:

```text
TUI
Web
Slack
Teams
Mobile
Email
API
```

## Human Interaction Rule

> Las interfaces transportan la interacción; el runtime define y persiste su significado.

Una ejecución durable no debe mantener necesariamente un proceso abierto mientras espera intervención humana.

---

# Article IX — Resource and Budget Constitution

Todo run debe tener un `ExecutionBudget`.

```ts
interface ExecutionBudget {
  maxTurns: number;
  maxToolCalls: number;
  maxInputTokens: number;
  maxOutputTokens: number;
  maxCost: number;
  maxRuntimeMs: number;
  maxConcurrentTools: number;
}
```

El `ExecutionController` aplica estos límites.

```text
AgentLoop
   │
   ▼
ExecutionController
   │
   ├── turns?
   ├── tool calls?
   ├── tokens?
   ├── cost?
   ├── runtime?
   └── concurrency?
```

## Budget Rule

El modelo nunca es la única autoridad para determinar cuándo debe detenerse una ejecución.

---

# Article X — Observability Constitution

Todo `AgentRun` debe producir una historia reconstruible.

```text
AgentRun
│
├── run_started
├── context_built
├── model_requested
├── model_response
├── tool_requested
├── policy_evaluated
├── tool_started
├── tool_completed
├── human_requested
├── human_resolved
├── turn_completed
└── run_completed
```

Cada evento debería incluir como mínimo:

```text
eventId
timestamp
runId
sessionId
agentId
traceId
eventType
payload
```

Esta fuente de eventos debe poder alimentar:

```text
Logs
Tracing
Audit
Replay
Analytics
Evals
Cost Analysis
Debugging
UI
```

## Observability Rule

La observabilidad debe surgir de primitives del runtime, no de instrumentación ad hoc dispersa por las aplicaciones.

---

# Article XI — Evolution Constitution

## EVO-01 — Keep the core small

Una nueva capacidad debe intentar implementarse primero mediante:

```text
Extension
Hook
ContextProvider
Tool
Policy
Event Consumer
Adapter
```

antes de modificar `AgentCore`.

## EVO-02 — Multi-agent is not the default solution

No introducir multi-agent para resolver problemas que puedan resolverse mejor mediante tools, context, workflows o una mejor arquitectura single-agent.

## EVO-03 — Deterministic controls do not belong in prompts

Nunca utilizar una instrucción como único mecanismo para seguridad, autorización, budgets o compliance.

## EVO-04 — Declare side effects

Toda integración nueva debe declarar sus side effects y características operacionales.

## EVO-05 — Define failure semantics

Todo componente nuevo debe definir cómo falla, si puede recuperarse y si puede reintentarse.

## EVO-06 — Everything important is observable

Toda capacidad nueva debe definir sus eventos y trazabilidad.

## EVO-07 — Core dependencies require justification

Toda nueva dependencia dentro del core requiere justificación arquitectónica.

## EVO-08 — Breaking contracts require an ADR

Breaking changes sobre contratos fundamentales requieren un Architecture Decision Record.

## EVO-09 — Context has provenance

Nuevas fuentes de contexto deben identificar origen, freshness y reglas de acceso cuando corresponda.

## EVO-10 — Extensions cannot bypass constitutional boundaries

Una extensión no puede saltarse ToolRuntime, PolicyEngine, lifecycle o controles de ejecución para realizar acciones que el core prohibiría.

---

# Article XII — Deterministic vs Agentic Boundary

Esta frontera constituye una de las reglas fundamentales del sistema.

## Agentic Decisions

El LLM puede:

```text
interpret intent
form hypotheses
identify missing information
select an appropriate capability
analyze observations
propose a semantic next action
evaluate whether the semantic objective appears satisfied
```

## Deterministic Decisions

El runtime controla:

```text
identity
authorization
schema validation
permissions
budgets
timeouts
retries
idempotency
sandboxing
rate limits
approval requirements
state transitions
audit requirements
resource limits
```

Arquitectura:

```text
                PROBABILISTIC

                    LLM
                     │
               proposes intent
                     │
                     ▼
════════════════════════════════════
        DETERMINISTIC BOUNDARY
════════════════════════════════════
                     │
                     ▼
              Harness Runtime
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      Policy       State       Execution
        │            │            │
        └────────────┼────────────┘
                     ▼
                Real World
```

## Supreme Constitutional Rule

> **Probabilistic systems may propose decisions. Deterministic systems must govern consequences.**

---

# Constitutional Compliance

Toda nueva feature significativa debe responder:

```text
1. Which principles does this affect?
2. Which invariants must remain true?
3. Which component owns the decision?
4. Which contracts change?
5. How does the lifecycle change?
6. What are the failure semantics?
7. What are the security implications?
8. What events are produced?
9. What budgets apply?
10. Does this change the deterministic/agentic boundary?
```

---

# Architecture Decision Records

Cambios significativos deben documentarse mediante ADRs.

Formato mínimo:

```text
ADR-ID
Title
Status
Context
Decision
Alternatives
Consequences
Constitutional Articles Affected
Migration Strategy
```

---

# Final Architecture Doctrine

```text
Model
    proposes

Harness
    governs

Context
    informs

Tools
    act

Policies
    constrain

State
    tracks

Sessions
    persist

Events
    expose

Humans
    intervene

Interfaces
    present

ExecutionController
    limits
```

La Constitution existe para asegurar que, a medida que el harness evoluciona desde un Agent Loop mínimo hacia una plataforma empresarial de agentes, **la inteligencia probabilística permanezca desacoplada del control operacional determinístico**.

# Amendment v1.1 — Enterprise Activation, Interoperability and Operations

This amendment is normative and extends the original Constitution without invalidating P-01 through P-15.

## P-16 — Activation is independent from execution
External stimuli MUST be normalized into an `ActivationRequest` before entering the execution core. User prompts, APIs, webhooks, queues, schedules, events, files, databases, systems and other agents are ingress mechanisms—not AgentLoop concerns.

## P-17 — Admission precedes execution
No activation has an inherent right to execute. `AdmissionController` MUST apply identity, authorization, tenant, capacity, rate, budget, deduplication and policy decisions before routing.

## P-18 — Communication semantics are independent from protocol and transport
Agent communication MUST use explicit semantic contracts. Protocols define interoperability; transports define delivery. Neither belongs inside Agent Core.

## P-19 — External agent interoperability is adapter-based
A2A or future interoperability standards MUST be integrated through `AgentCommunicationGateway` adapters. The core MUST NOT depend directly on an A2A SDK or a particular wire protocol.

## P-20 — Internal delegation and external federation are different concerns
Managed sub-agent delegation MAY use an internal protocol. Communication with independently operated agents SHOULD use a standards-based federation boundary such as A2A where appropriate.

## P-21 — Delegated authority is explicit and least-privileged
A child or remote agent MUST NOT automatically inherit the caller's authority. Delegation MUST be scoped, time-bounded, auditable and represented by an explicit delegation contract/token.

## P-22 — Enterprise data is governed throughout its lifecycle
Classification, residency, retention, lineage, encryption, deletion and legal-hold requirements MUST be enforceable independently of model reasoning.

## P-23 — Durable execution is a core runtime property
Long-running work MUST support persistence, checkpoint, pause, crash recovery and resume. Process memory MUST NOT be the source of truth for durable runs.

## P-24 — Side effects require idempotency semantics
Capabilities with externally visible side effects MUST declare idempotency, retry and duplicate-delivery behavior.

## P-25 — Audit evidence is distinct from operational telemetry
Logs, traces, execution ledger and immutable audit evidence have different purposes and MUST NOT be conflated.

## P-26 — Capabilities have governed lifecycles
Tools/capabilities MUST support explicit versions, compatibility policy, rollout, deprecation and retirement.

## P-27 — Deployment topology is independent from agent semantics
Agent behavior MUST NOT depend on whether execution occurs in-process, on a worker, Kubernetes, serverless, cloud, edge or on-premise.

## P-28 — Production and evaluation are separate execution concerns
Candidate agents, prompts, skills, models, policies and capabilities MUST be evaluable in an Evaluation Harness before controlled promotion to production.

## P-29 — Business outcomes are first-class observability
Technical success does not imply business success. Enterprise runs SHOULD correlate execution with measurable outcomes, value, SLA/SLO and human escalation.

## P-30 — Operational control can override autonomy
The platform MUST support cancellation, capability disablement, tenant isolation, rollout rollback and kill switches without relying on model cooperation.

## Additional Enterprise Invariants
- INV-E01: No ingress adapter calls AgentLoop directly; it produces an ActivationRequest.
- INV-E02: No ActivationRequest executes without an AdmissionDecision.
- INV-E03: Agent-to-agent messages cross an explicit AgentCommunication boundary.
- INV-E04: Protocol adapters and transport adapters are replaceable independently.
- INV-E05: A2A is an external interoperability option, not an Agent Core dependency.
- INV-E06: Delegation depth, child runs and delegated cost are bounded by ExecutionBudget.
- INV-E07: Tenant data, memory, credentials, artifacts and audit records are isolated.
- INV-E08: Credentials are resolved by a CredentialBroker and SHOULD NOT enter model context.
- INV-E09: Every side-effecting capability declares idempotency and retry semantics.
- INV-E10: Every production run records exact versions of agent, skill, policy, model configuration and capability contracts.
- INV-E11: Data governance policy follows context and artifacts across component boundaries.
- INV-E12: A human handoff transfers a structured HandoffPackage rather than only prose.
- INV-E13: Production promotion requires certification policy where risk class requires it.
- INV-E14: Kill switches operate independently of AgentLoop.

## Canonical Enterprise Planes
1. Ingress & Activation Plane
2. Execution Plane
3. Agent Interoperability Plane
4. Capability & Integration Plane
5. Data & Context Plane
6. Control Plane
7. Reliability Plane
8. Observability & Governance Plane
9. Execution Fabric

# Amendment v1.2 — Durable Operation, Identity, Connectivity and Authoring

This amendment is normative and extends the Constitution and Amendment v1.1 without invalidating P-01 through P-30.

## P-31 — Identity travels with every turn
The verified principal that admission produced MUST accompany every turn of a run as an explicit caller snapshot (initiator and current). Tenant, user-scoped credentials, policy and memory MUST derive from that snapshot, never from prompts, tool arguments or external responses.

## P-32 — A step is the unit of durability and recovery
A turn MUST be decomposed into steps (one model call and its inline tool calls). Each step MUST be recorded as committed before its effects are considered durable, and recovery MUST reason per step, not per turn.

## P-33 — Waiting is durable and consumes no compute
Approvals, questions, interactive authorizations and budget limits MUST park the run durably. A parked run MUST NOT hold compute, and MUST be resumable by a delivery arriving through any authorized channel.

## P-34 — External conversations are addressed, not inferred
Every external conversation (a thread, an issue, a socket session, a schedule) MUST map to a durable session through an explicit continuation address with exclusive ownership. The runtime MUST NOT guess which run a stimulus continues.

## P-35 — Secrets never enter model-controlled compute
Credentials MUST remain outside both model context and the isolated environment where model-requested code executes. Authenticated egress MUST be brokered at the boundary.

## P-36 — The runtime may evolve under open sessions only at idle boundaries
A session MAY move to a new runtime version (agent, policy, model configuration, capability contracts, session format) only when it holds no live work. The version in effect MUST be recorded with the session.

## P-37 — Observability capture is bounded by audience
Every session MUST be classified by audience at creation. A trace capture ceiling derived from that audience MUST bound every telemetry destination; no destination may restore content the ceiling excludes.

## P-38 — External capabilities enter only through declared connections
Capabilities provided by external systems (for example MCP servers or OpenAPI services) MUST enter through declared connections and be resolved as capability descriptors. Protocols remain adapters; the core MUST NOT depend on a protocol SDK.

## P-39 — An agent is authored as inspectable, conventionally located files
An agent's configuration, capabilities, connections, data sources, entry channels and policies SHOULD be authored as files in conventional locations whose path determines identity. The runtime MUST NOT infer configuration that the authored files do not declare, and MUST expose what it discovered.

## Additional Enterprise Invariants (v1.2)
- INV-E15: An unconfigured harness admits nothing, in any environment; development admission depends on process mode, never on the request.
- INV-E16: A committed step is never re-executed during recovery.
- INV-E17: An effect whose outcome is unknown is re-executed only if its capability declares replayPolicy = SAFE.
- INV-E18: A delivery resumes only the wait it addresses, and only if its responder is authorized for it.
- INV-E19: A continuation address has at most one owning session at a time.
- INV-E20: Credentials are never materialized inside the isolated execution environment.
- INV-E21: A child budget never exceeds its parent's remaining budget.
- INV-E22: Live work (pending waits, uncommitted steps, active child runs) never migrates between runtime versions.
- INV-E23: No trace destination may capture content above the session's capture ceiling.
- INV-E24: No hook point may return an authorization outcome.
- INV-E25: No external tool reaches the model except as a CapabilityDescriptor resolved by CapabilityRegistry and evaluated by PolicyEngine.
- INV-E26: Every data source declares a classification; an undeclared source is RESTRICTED.
- INV-E27: An authoring diagnostic of level ERROR prevents any activation of that agent.
