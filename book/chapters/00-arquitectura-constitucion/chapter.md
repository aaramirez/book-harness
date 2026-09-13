---
id: CH-00
title: "La Constitución Arquitectónica de un Arnés"
starting_version: "0.1"
ending_version: "0.1"
introduces_components: []
introduces_contracts: [C-001, C-002, C-003, C-004, C-010, C-011, C-012]
modifies_contracts: []
constitutional_articles: [P-01, P-02, P-03, P-04, P-05, P-06, P-07, P-08, P-09, P-10, P-11, P-12, P-13, P-14, P-15, INV-01, INV-02, INV-03, INV-04, INV-05, INV-06, INV-07, INV-08, INV-09, INV-10, INV-11, INV-12, INV-13, INV-14, INV-15, INV-16, INV-17, INV-18, INV-19, INV-20]
previous_chapter: null
next_chapter: null
---

# Capítulo 0 — La Constitución Arquitectónica de un Arnés

> **Regla constitucional:** los sistemas probabilísticos pueden proponer decisiones. Los sistemas
> determinísticos deben gobernar sus consecuencias.

## 1. Arquitectura Actual (Current Architecture)

No existe arquitectura previa. Este es el capítulo fundacional del libro: antes de escribir una
sola línea de `AgentLoop`, `ModelGateway` o `ToolRuntime`, necesitamos el documento que va a
gobernar cómo se diseñan, revisan y evolucionan esos componentes.

Lo único que existe antes de este capítulo es la intención: construir un **arnés de agentes**
(*Agent Harness*) — un runtime donde un modelo de lenguaje puede razonar y proponer acciones,
mientras un sistema determinístico decide qué puede realmente ocurrir.

## 2. El Problema (Problem)

¿Cómo evitamos que "construir un arnés" se convierta en una colección de prompts cada vez más
largos que le piden al modelo, con más y más énfasis, que "por favor no haga cosas peligrosas",
"por favor no invente nombres de funciones que no existen", "por favor recuerde los límites de
presupuesto"?

Necesitamos que ciertas propiedades sean **verdaderas por construcción**, no verdaderas porque el
modelo decidió cooperar esa vez.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

Como no hay arquitectura todavía, la "arquitectura actual" es, literalmente, un prompt. Y un
prompt no puede:

- garantizar que una acción con efectos secundarios pase por una capa de autorización antes de
  ejecutarse;
- garantizar que un error se clasifique siempre de la misma manera;
- garantizar que un límite de ejecución (turnos, costo, tiempo) se respete aunque el modelo
  "olvide" mencionarlo;
- impedir que un capítulo posterior de este mismo libro use una entidad (`ToolRuntime`,
  `PolicyEngine`, ...) que todavía no ha sido definida.

> **Regla editorial fundamental:** todo concepto debe atravesar siempre la secuencia
> `Concept → Contract → Pseudocode → Interaction`. Ningún pseudocódigo puede usar una entidad
> que no haya sido definida antes mediante `STRUCT`, `ENUM`, `INTERFACE` o un `COMPONENT`
> registrado — **no magic entities**.

Este capítulo existe para fijar, antes de cualquier otra cosa, las reglas que hacen posible
cumplir esa regla editorial durante el resto del libro.

## 4. Impacto Constitucional (Constitutional Impact)

Este capítulo es un caso especial: **introduce** la Constitution en lugar de modificarla o
preservarla (no existe una Constitution previa que preservar).

```text
Constitutional Impact

Principles introduced
    P-01 .. P-15   (Article I completo — ver constitution/ARCHITECTURE_CONSTITUTION.md)

Invariants introduced
    INV-01 .. INV-20   (Article II completo)

Component ownership changes
    None — Article III (Component Sovereignty) se documenta como marco de referencia, pero
    ningún componente de runtime se instancia todavía en este capítulo (ver §8, Preview).

Lifecycle changes
    Introduce AgentRunStatus (Article V) y sus transiciones válidas. Ningún AgentRun real existe
    todavía — el lifecycle se define como contrato, no como implementación.

Security implications
    Establece P-05 (side effects pass through policy) y P-13 (authorization is deterministic and
    external to the LLM) como reglas que todo componente futuro deberá cumplir. No hay
    PolicyEngine todavía; la regla se declara antes de que exista quien la haga cumplir.

Observability implications
    Establece AgentEvent (C-010) como envelope obligatorio de todo evento observable (P-04,
    INV-18) y exige que toda decisión crítica sea trazable (INV-19).

Deterministic vs agentic boundary
    Este capítulo introduce la frontera misma (Article XII): el modelo propone intención: el
    harness gobierna identidad, autorización, límites, estado y ejecución.
```

## 5. Conceptos Nuevos (New Concepts)

- **Probabilistic vs Deterministic Boundary**: la separación entre lo que un modelo de lenguaje
  puede decidir (interpretar intención, proponer una acción) y lo que el runtime determinístico
  controla (autorización, límites, transiciones de estado, auditoría). Es la regla suprema de la
  Constitution (Article XII).
- **Component Sovereignty** *(preview — se instancia a partir del próximo capítulo)*: cada
  componente del runtime tendrá una responsabilidad exclusiva y fronteras explícitas de lo que
  NO posee.
- **Decision Ownership**: cada decisión arquitectónica (¿debo seguir ejecutando otro turno?,
  ¿puede ocurrir esta acción?, ¿qué debería saber el modelo?) tiene, desde este capítulo en
  adelante, un dueño único y nombrado — nunca "el prompt en general".
- **Execution Budget**: todo `AgentRun` está acotado por límites explícitos (turnos, tool calls,
  tokens, costo, tiempo, concurrencia) — el modelo nunca es la única autoridad para decidir
  cuándo detenerse.
- **Observability as a first-class property**: toda acción significativa produce un evento con
  un envelope común, para que logging, tracing, auditoría y replay puedan reconstruirse.
- **Human-in-the-loop como capacidad del runtime** *(preview)*: la interacción humana se
  representará como estado persistido, no como una particularidad de una interfaz (TUI, Web,
  Slack, ...).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores fundamentales

Estos identificadores son tipos opacos (sin campos propios): identifican entidades sin exponer su
representación interna. Se usan como tipo de campo en los `STRUCT` de esta sección.

| Identificador | Identifica |
|---|---|
| `AgentId` | un agente configurado sobre el runtime |
| `SessionId` | una sesión persistente |
| `RunId` | una ejecución (`AgentRun`) concreta |
| `MessageId` | un mensaje dentro del ciclo cognitivo |
| `EventId` | un evento observable |
| `TraceId` | una traza de ejecución de punta a punta |
| `Timestamp` | un instante en el tiempo |

A partir de estos identificadores, definimos los primeros contratos de datos del libro:

```pseudocode
ENUM MessageRole
    SYSTEM
    USER
    ASSISTANT
    TOOL
END
```

```pseudocode
STRUCT AgentMessage
    id: MessageId
    role: MessageRole
    content: Value
    timestamp: Timestamp
END
```

```pseudocode
STRUCT ExecutionBudget
    maxTurns: Integer
    maxToolCalls: Integer
    maxInputTokens: Integer
    maxOutputTokens: Integer
    maxCost: Number
    maxRuntimeMs: Integer
    maxConcurrentTools: Integer
END
```

```pseudocode
STRUCT AgentConfig
    agentId: AgentId
    name: Text
    budget: ExecutionBudget
END
```

```pseudocode
ENUM AgentRunStatus
    CREATED
    INITIALIZING
    RUNNING
    WAITING_FOR_MODEL
    WAITING_FOR_TOOL
    WAITING_FOR_HUMAN
    PAUSED
    COMPLETED
    FAILED
    CANCELLED
END
```

```pseudocode
STRUCT AgentState
    runId: RunId
    sessionId: SessionId
    agentId: AgentId
    status: AgentRunStatus
    currentTurn: Integer
END
```

```pseudocode
STRUCT ExecutionContext
    runId: RunId
    sessionId: SessionId
    traceId: TraceId
    budget: ExecutionBudget
END
```

```pseudocode
ENUM ErrorCategory
    VALIDATION
    POLICY
    TOOL
    MODEL
    CONTEXT
    PERSISTENCE
    INFRASTRUCTURE
    BUDGET
    CANCELLATION
    FATAL
END
```

```pseudocode
STRUCT HarnessError
    category: ErrorCategory
    code: Text
    message: Text
    recoverable: Boolean
    retryable: Boolean
    metadata: Map<Text, Value>
END
```

```pseudocode
ENUM AgentEventType
    RUN_STARTED
    TURN_CONTINUED
    RUN_COMPLETED
    RUN_FAILED
END
```

```pseudocode
STRUCT AgentEvent
    eventId: EventId
    eventType: AgentEventType
    timestamp: Timestamp
    runId: RunId
    sessionId: SessionId
    agentId: AgentId
    traceId: TraceId
    payload: Value
END
```

**Unchanged / Not yet introduced**: no hay todavía `ToolCall`, `ToolResult`, `ModelRequest`,
`ModelResponse` ni `ContextSnapshot` — llegan junto con `ModelGateway`, `ContextEngine` y
`ToolRuntime` en capítulos posteriores (fuera del alcance de esta ejecución BH-v0.1).

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

Este capítulo no introduce ninguna `INTERFACE` (contrato de comportamiento) todavía — las
interfaces (`ModelGateway`, `ToolRuntime`, `PolicyEngine`, ...) requieren componentes que aún no
existen. Introduce siete contratos de datos, registrados en `registry/contracts.yaml`:

```text
ID:                     C-001
Name:                   AgentMessage
Version:                v1
Introduced In:          CH-00
Current Definition:     STRUCT AgentMessage (ver §6)
Used By:                []
Modified By:            []
Constitutional Impact:  [P-02, INV-02]
```

```text
ID:                     C-002
Name:                   AgentConfig
Version:                v1
Introduced In:          CH-00
Current Definition:     STRUCT AgentConfig (ver §6)
Used By:                []
Modified By:            []
Constitutional Impact:  [P-06]
```

```text
ID:                     C-003
Name:                   AgentState
Version:                v1
Introduced In:          CH-00
Current Definition:     STRUCT AgentState (ver §6)
Used By:                []
Modified By:            []
Constitutional Impact:  [P-08, P-10, INV-12]
```

```text
ID:                     C-004
Name:                   ExecutionContext
Version:                v1
Introduced In:          CH-00
Current Definition:     STRUCT ExecutionContext (ver §6)
Used By:                []
Modified By:            []
Constitutional Impact:  [P-01, P-14]
```

```text
ID:                     C-010
Name:                   AgentEvent
Version:                v1
Introduced In:          CH-00
Current Definition:     STRUCT AgentEvent (ver §6)
Used By:                []
Modified By:            []
Constitutional Impact:  [P-04, INV-18, INV-19]
```

```text
ID:                     C-011
Name:                   HarnessError
Version:                v1
Introduced In:          CH-00
Current Definition:     STRUCT HarnessError (ver §6)
Used By:                []
Modified By:            []
Constitutional Impact:  [INV-20]
```

```text
ID:                     C-012
Name:                   ExecutionBudget
Version:                v1
Introduced In:          CH-00
Current Definition:     STRUCT ExecutionBudget (ver §6)
Used By:                []
Modified By:            []
Constitutional Impact:  [P-10, INV-09]
```

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce ningún componente de runtime.** `registry/components.yaml`
permanece vacío después de este capítulo.

Los componentes de Article III (Component Sovereignty) se listan aquí únicamente como **Preview
— no introducidos en este capítulo** (permitido explícitamente por
`BOOK_HARNESS_BUILD_INSTRUCTIONS(1).md` §22 regla 8). Ninguno de estos nombres aparece dentro de
un bloque de pseudocódigo de este capítulo:

| Nombre (preview) | Dominio (Article III) |
|---|---|
| `AgentCore` | primitives fundamentales del agente |
| `AgentLoop` | ciclo de ejecución cognitiva |
| `ModelGateway` | invocación del modelo, independiente de proveedor |
| `ContextEngine` | selección y composición de contexto |
| `ToolRuntime` | ejecución de tools/capacidades |
| `PolicyEngine` | autorización y políticas |
| `SessionManager` | persistencia y recuperación de sesión |
| `HumanInteractionService` | interacción humana durable |
| `EventBus` | distribución de eventos |
| `ExecutionController` | budgets, cancelación, límites |
| `CapabilityRegistry` | desacoplar intención de implementación |

## 9. Relaciones de Dependencia (Dependency Relationships)

No hay Dependency Map de componentes todavía (no existen componentes — ver §8). Lo que este
capítulo sí establece es la relación conceptual de más alto nivel, de la que todo Dependency Map
posterior heredará su dirección:

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

Toda nueva dependencia que se introduzca en capítulos futuros deberá apuntar hacia contratos
estables (interfaces), nunca hacia implementaciones concretas — regla que se fija aquí y se
aplica desde el primer componente real que se introduzca.

## 10. Diagrama de Secuencia (Sequence Diagram)

Tres vistas obligatorias de la misma interacción (REGLAS_LIBRO_AGENT_HARNESS(1).md §14), a nivel
constitucional (roles genéricos, no componentes concretos todavía):

**Vista 1 — Componentes**

```text
Model → Harness Runtime → External World
```

**Vista 2 — Sequence**

```text
Model
   │ proposes(intent)
   ▼
Harness Runtime
   │ governs(intent, budget)
   ▼
External World
```

**Vista 3 — Pseudocódigo**

Ver §11: `governTurnContinuation` es la primera formalización ejecutable de "Harness Runtime
governs".

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades ya definidas en §6 de este mismo capítulo.

```pseudocode
FUNCTION governTurnContinuation(
    state: AgentState,
    execution: ExecutionContext,
    budget: ExecutionBudget
) -> AgentEvent

    IF state.currentTurn >= budget.maxTurns
        error: HarnessError = HarnessError(
            category = BUDGET,
            code = "MAX_TURNS_EXCEEDED",
            message = "Execution budget exhausted: maxTurns reached",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )

        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = RUN_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = state.agentId,
            traceId = execution.traceId,
            payload = error
        )

        THROW error
    END

    RETURN AgentEvent(
        eventId = newEventId(),
        eventType = TURN_CONTINUED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = state.agentId,
        traceId = execution.traceId,
        payload = state
    )
END
```

`newEventId()` y `now()` son utilidades primitivas de generación de identificador/timestamp (no
son entidades arquitectónicas ni componentes — no requieren ficha ni registro).

Nótese la regla en acción: el modelo (`Model`) puede haber propuesto "sigamos con otro turno",
pero `governTurnContinuation` — determinístico, sin invocar ningún modelo — es quien decide si
eso puede realmente ocurrir, basándose únicamente en `state` y `budget`.

## 12. Transiciones de Estado (State Transitions)

`AgentRunStatus` (§6) define el lifecycle completo (Article V de la Constitution):

```text
CREATED
   → INITIALIZING

INITIALIZING
   → RUNNING
   → FAILED

RUNNING
   → WAITING_FOR_MODEL
   → WAITING_FOR_TOOL
   → WAITING_FOR_HUMAN
   → COMPLETED
   → FAILED
   → CANCELLED

WAITING_FOR_HUMAN
   → approved  → RUNNING
   → rejected  → RUNNING / FAILED
   → expired   → FAILED
   → cancelled → CANCELLED
```

El LLM no controla directamente esta máquina de estados (P-10): `governTurnContinuation` (§11)
es un ejemplo mínimo de una decisión de continuación que el harness — no el modelo — resuelve.

## 13. Semántica de Fallos (Failure Semantics)

`ErrorCategory` (§6) clasifica todo fallo operacional (Article VII, INV-20: "todo error
operacional pertenece a una categoría conocida"). Ejemplos relevantes para este capítulo:

```text
BUDGET
    maxTurns / maxToolCalls / maxCost / maxRuntimeMs excedido
    → recoverable: FALSE, retryable: FALSE
    → detiene la ejecución (ver §11)

VALIDATION
    un AgentConfig o ExecutionContext malformado
    → recoverable: TRUE (puede corregirse y reintentarse)

FATAL
    corrupción de estado irrecuperable
    → recoverable: FALSE
```

`governTurnContinuation` (§11) nunca lanza un error genérico: siempre construye un `HarnessError`
con `category`, `recoverable` y `retryable` explícitos.

## 14. Eventos Producidos (Events Produced)

`AgentEventType` (§6) introduce el vocabulario mínimo de eventos de este capítulo:

```text
RUN_STARTED       — un AgentRun inicia (aún no implementado; declarado para uso futuro)
TURN_CONTINUED    — el harness autorizó continuar con otro turno (ver §11)
RUN_COMPLETED     — un AgentRun terminó exitosamente (aún no implementado)
RUN_FAILED        — un AgentRun terminó por un HarnessError (ver §11)
```

Capítulos posteriores extenderán este vocabulario (`ToolExecutionStarted`, `PolicyEvaluated`,
`HumanInteractionRequested`, ...) sin redefinir el envelope común `AgentEvent` (C-010).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

Este capítulo no implementa autorización todavía (no existe `PolicyEngine` — ver §8), pero fija
las reglas que todo componente futuro deberá cumplir:

- **P-05 — Side effects pass through policy**: ninguna acción con efectos secundarios podrá
  ejecutarse sin atravesar una capa determinística de validación y autorización.
- **P-13 — Authorization is deterministic and external to the LLM**: el modelo nunca será, en
  ningún capítulo posterior, la fuente de verdad para identidad, permisos o autorización.

`governTurnContinuation` (§11) ya demuestra el patrón: la decisión de continuar o detener la
ejecución depende de `state`/`budget`, nunca de lo que el modelo "cree" que debería pasar.

## 16. Tests (Tests)

Tests arquitectónicos declarados en este capítulo (REGLAS_LIBRO_AGENT_HARNESS(1).md §28) — se
implementarán como pruebas ejecutables reales una vez exista el componente correspondiente:

```text
TEST HarnessErrorAlwaysDeclaresCategoryRecoverableAndRetryable
TEST AgentRunStatusNeverSkipsAnUndeclaredTransition
TEST ExecutionBudgetIsMandatoryOnEveryExecutionContext
TEST GovernTurnContinuationNeverConsultsTheModel
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.1, después de CH-00)

Constitution
 ├── Article I    — Principles (P-01 .. P-15)
 ├── Article II   — Invariants (INV-01 .. INV-20)
 └── Article III  — Component Sovereignty (referencia; sin instanciar)

Contracts (registry/contracts.yaml)
 ├── C-001 AgentMessage
 ├── C-002 AgentConfig
 ├── C-003 AgentState
 ├── C-004 ExecutionContext
 ├── C-010 AgentEvent
 ├── C-011 HarnessError
 └── C-012 ExecutionBudget

Components (registry/components.yaml)
 └── (vacío)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- Ningún componente de runtime (`AgentCore`, `AgentLoop`, `ModelGateway`, `ContextEngine`,
  `ToolRuntime`, `PolicyEngine`, `SessionManager`, `HumanInteractionService`, `EventBus`,
  `ExecutionController`, `CapabilityRegistry`) — llegan en capítulos posteriores, fuera del
  alcance de esta ejecución BH-v0.1.
- Ninguna `INTERFACE` de comportamiento (`ModelGateway`, `ToolRuntime`, ...).
- Enforcement real de `PolicyEngine` — la regla P-05/P-13 está declarada, no implementada.
- Persistencia real de `AgentState`/`SessionState` — los contratos existen, `SessionManager` no.
- Human-in-the-loop implementado — solo mencionado como preview conceptual.
- Reviewers plurales (técnico/pedagógico/consistencia), evals, orquestación multi-agente y
  aprobación humana persistente del propio Book Harness — explícitamente fuera de alcance de
  BH-v0.1 (ver plan de ejecución §7).

## 19. Siguiente Incremento (Next Increment)

El problema natural del próximo capítulo: ¿cómo ejecuta el harness un turno real del ciclo
cognitivo (`Model → Harness → External World` de §10, pero con un componente real en el medio)?
Eso requiere introducir `AgentCore`/`AgentLoop` — el primer componente de Article III que deja de
ser preview (§8) para tener ficha arquitectónica, `INTERFACE` y pseudocódigo propios.

Ese capítulo (`CH-01`, fuera del alcance de esta ejecución BH-v0.1) es el primer lugar donde
`registry/components.yaml` deja de estar vacío. `next_chapter` queda en `null` en el frontmatter
de este capítulo porque, en este momento del libro, `CH-01` todavía no existe como archivo — solo
como el problema que motivará su escritura.
