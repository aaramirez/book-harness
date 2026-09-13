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
retrieval_set:
  expected_outcome:
    id: EO-CH00
    text: |
      Al terminar este capítulo podrás diagnosticar si una decisión arquitectónica de un
      arnés de agentes está gobernada de forma determinística y verificable, o si en
      realidad sigue implícita en el buen juicio del modelo, y podrás señalar, para
      cualquier propuesta de diseño futura, qué contrato de datos fundamental falta para
      hacer esa decisión auditable.
  skeleton:
    id: SK-CH00
    section_titles:
      - "1. Arquitectura Actual (Current Architecture)"
      - "2. El Problema (Problem)"
      - "3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)"
      - "4. Impacto Constitucional (Constitutional Impact)"
      - "5. Conceptos Nuevos (New Concepts)"
      - "6. Nuevas Estructuras de Datos (New Data Structures)"
      - "7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)"
      - "8. Responsabilidades de Componentes (Component Responsibilities)"
      - "9. Relaciones de Dependencia (Dependency Relationships)"
      - "10. Diagrama de Secuencia (Sequence Diagram)"
      - "11. Pseudocódigo (Pseudocode)"
      - "12. Transiciones de Estado (State Transitions)"
      - "13. Semántica de Fallos (Failure Semantics)"
      - "14. Eventos Producidos (Events Produced)"
      - "15. Implicaciones de Seguridad / Política (Security / Policy Implications)"
      - "16. Tests (Tests)"
      - "17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)"
      - "18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)"
      - "19. Siguiente Incremento (Next Increment)"
    components_to_be_introduced: []
    contracts_to_be_introduced: [C-001, C-002, C-003, C-004, C-010, C-011, C-012]
  guiding_questions:
    - id: GQ-CH00-01
      text: |
        Si un agente puede llegar a ejecutar acciones con efectos reales, ¿quién decide si
        una de esas acciones es segura, y cómo se hace esa decisión verificable en vez de
        dejarla implícita en el criterio del modelo?
      answered_by: RQ-CH00-01
    - id: GQ-CH00-02
      text: |
        ¿Cómo evitamos que cada mensaje que produce un modelo dentro del ciclo cognitivo
        tenga una forma distinta según quién lo generó, de modo que nada más adelante en
        el sistema pueda depender de una forma estable?
      answered_by: RQ-CH00-02
    - id: GQ-CH00-03
      text: |
        Si la ejecución de un agente se detiene a la mitad de una tarea, ¿cómo sabemos en
        qué punto exacto del proceso quedó, sin tener que preguntarle al propio modelo?
      answered_by: RQ-CH00-03
    - id: GQ-CH00-04
      text: |
        ¿Qué impide que un agente siga ejecutando turnos indefinidamente, gastando tiempo
        y dinero, si nadie, ni siquiera el modelo, recuerda imponerle un límite?
      answered_by: RQ-CH00-04
    - id: GQ-CH00-05
      text: |
        Cuando algo falla a mitad de una ejecución, ¿cómo distinguimos un fallo que
        conviene reintentar de uno que exige detener todo, sin que la respuesta dependa de
        quién escribió ese manejo de errores en particular?
      answered_by: RQ-CH00-05
  systems_lens:
    iceberg_visible_fact: |
      Construir un arnés de agentes puede degenerar en una colección cada vez más larga de
      instrucciones de prompt que le piden al modelo, con más y más énfasis, que "por favor"
      no haga cosas peligrosas, no invente funciones que no existen, y no olvide los límites
      de presupuesto (ver seccion 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que un prompt no puede garantizar que una acción con
      efectos secundarios pase por autorización, que un error se clasifique siempre igual,
      que un límite de ejecución se respete aunque el modelo lo olvide, ni impedir que un
      capítulo futuro use una entidad que este libro todavía no ha definido (ver seccion 3,
      Por Qué la Arquitectura Actual No Basta).
    iceberg_structures: |
      Todavía no existe ningún componente de runtime (ver seccion 8): lo que este capítulo
      instala son los contratos de datos (secciones 6 y 7) y dos políticas concretas, P-05
      (toda acción con efectos secundarios pasa por política) y P-13 (la autorización es
      determinística y externa al modelo), que cualquier componente futuro deberá cumplir
      por diseño, no por buena voluntad.
    iceberg_mental_models: |
      El modelo mental que sostiene todo lo anterior es el límite Probabilístico y
      Determinístico del Article XII (ver seccion 4, Impacto Constitucional): el modelo
      propone intención; el arnés gobierna identidad, autorización, límites, estado y
      ejecución. Nunca al revés.
    reinforcing_loop: |
      Cada vez que una decisión de autorización se deja implícita en el prompt en lugar de
      en un contrato explícito, aumenta la probabilidad de que el próximo capítulo repita
      el mismo atajo por si acaso, apilando más prosa persuasiva en vez de más estructura.
      Este capítulo corta esa espiral de raíz al declarar P-05 y P-13 antes de que exista
      código que pueda violarlas.
    balancing_loop: |
      governTurnContinuation (seccion 11) es el mecanismo de equilibrio: cada vez que
      state.currentTurn se acerca a budget.maxTurns, la función determinística detiene la
      ejecución con un HarnessError en lugar de dejar que la espiral de turnos continúe
      indefinidamente.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que ExecutionBudget (C-012) y
      AgentState (C-003) existan como contratos de datos ANTES que cualquier componente que
      los use. Si esta frontera de datos antes que comportamiento no se fija aquí, ningún
      límite de ejecución futuro será verificable, solo prometido en prosa.
  recall_questions:
    - id: RQ-CH00-01
      text: |
        ¿Qué principio y qué invariante de la Constitution establecen que la autorización
        de una acción es una decisión determinística y externa al modelo, y qué política
        concreta lo enuncia en este capítulo?
    - id: RQ-CH00-02
      text: |
        ¿Qué contrato define la forma estable de todo mensaje del ciclo cognitivo, y qué
        cuatro campos garantiza siempre, sin importar qué componente lo produzca?
    - id: RQ-CH00-03
      text: |
        ¿Qué contrato representa el punto exacto de ejecución de un agente, y qué enum
        define los estados posibles por los que puede pasar esa ejecución?
    - id: RQ-CH00-04
      text: |
        ¿Qué contrato agrupa todos los límites de ejecución de un agente, y qué función de
        este capítulo es la primera en verificar uno de esos límites?
    - id: RQ-CH00-05
      text: |
        ¿Qué contrato clasifica todo fallo operacional, y qué dos campos booleanos
        determinan si conviene reintentar la operación o detener todo?
  explain_prompts:
    - id: EP-CH00-01
      text: |
        Explica en voz alta, como si hablaras con alguien sin ningún contexto técnico, qué
        SÍ decide el modelo de lenguaje en este capítulo y qué NUNCA decide, aunque lo
        proponga. ¿Por qué la Constitution se lo prohíbe explícitamente en el texto, en vez
        de simplemente confiar en que el modelo coopere?
      target_entity: "Model vs. Harness Runtime (Article XII, limite Probabilistico/Determinístico)"
    - id: EP-CH00-02
      text: |
        HarnessError posee la responsabilidad de clasificar un fallo (category, recoverable,
        retryable). Explica qué NO posee HarnessError: quién decide, entonces, si realmente
        se reintenta la operación, y por qué esa decisión no le pertenece al propio error?
      target_entity: C-011
  interleaved_questions: []
  flashcards:
    - id: FC-CH00-01
      front: |
        ¿Qué garantiza siempre un AgentMessage, sin importar qué componente lo produzca?
      back: |
        Un id (MessageId), un role (MessageRole: SYSTEM/USER/ASSISTANT/TOOL), un content
        (Value) y un timestamp: la forma estable de todo mensaje del ciclo cognitivo.
      source_entity: C-001
      chapter_introduced_in: CH-00
      review_stage: DAY_1
    - id: FC-CH00-02
      front: |
        ¿Qué campos agrupa un AgentConfig?
      back: |
        agentId, name y budget (ExecutionBudget): la configuración mínima necesaria para
        instanciar un agente.
      source_entity: C-002
      chapter_introduced_in: CH-00
      review_stage: DAY_1
    - id: FC-CH00-03
      front: |
        ¿Qué representa AgentState, y qué es lo que este capítulo deliberadamente NO
        resuelve todavía sobre él?
      back: |
        runId, sessionId, agentId, status (AgentRunStatus) y currentTurn: el progreso de
        una ejecución. Su persistencia real queda para SessionManager (preview, fuera de
        alcance de este capítulo).
      source_entity: C-003
      chapter_introduced_in: CH-00
      review_stage: DAY_1
    - id: FC-CH00-04
      front: |
        ¿Qué agrupa ExecutionContext, y por qué existe separado de AgentState?
      back: |
        runId, sessionId, traceId y budget: el contexto que acompaña cada decisión de
        ejecución, separado del estado del agente para poder auditarse de forma
        independiente.
      source_entity: C-004
      chapter_introduced_in: CH-00
      review_stage: DAY_1
    - id: FC-CH00-05
      front: |
        ¿Qué campos son obligatorios en todo AgentEvent, y qué principios constitucionales
        existen gracias a ese envelope común?
      back: |
        eventId, eventType, timestamp, runId, sessionId, agentId, traceId y payload: hacen
        posibles P-04, INV-18 e INV-19 (observabilidad y trazabilidad de punta a punta).
      source_entity: C-010
      chapter_introduced_in: CH-00
      review_stage: DAY_1
    - id: FC-CH00-06
      front: |
        ¿Qué dos campos booleanos de HarnessError determinan cómo debe reaccionar el
        sistema ante un fallo?
      back: |
        recoverable y retryable: nunca se infieren del texto del mensaje de error, siempre
        se declaran explícitamente junto con category.
      source_entity: C-011
      chapter_introduced_in: CH-00
      review_stage: DAY_1
    - id: FC-CH00-07
      front: |
        ¿Qué siete límites agrupa ExecutionBudget?
      back: |
        maxTurns, maxToolCalls, maxInputTokens, maxOutputTokens, maxCost, maxRuntimeMs y
        maxConcurrentTools.
      source_entity: C-012
      chapter_introduced_in: CH-00
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH00-01
      recall_question: RQ-CH00-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH00-02
      recall_question: RQ-CH00-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH00-03
      recall_question: RQ-CH00-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH00-04
      recall_question: RQ-CH00-04
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH00-05
      recall_question: RQ-CH00-05
      confidence_levels: [Alta, Media, Baja]
  interleaving_exception: |
    CH-00 es el primer capítulo del libro (previous_chapter es null en este mismo
    frontmatter): no existe un capítulo anterior con el cual conectar todavía. El
    movimiento Conectar (interleavedQuestions) queda vacío en este RetrievalSet, no porque
    se haya omitido, sino porque no hay con qué construirlo sin inventar un capítulo que no
    existe. validate-retrieval-set exime explícitamente a CH-00 de la regla de al menos una
    interleavedQuestion por esta razón. A partir de CH-01, que sí podrá mezclar entidades
    propias con las de CH-00, este movimiento se retoma con normalidad.
---

# Capítulo 0 — La Constitución Arquitectónica de un Arnés

> **Regla constitucional:** los sistemas probabilísticos pueden proponer decisiones. Los sistemas
> determinísticos deben gobernar sus consecuencias.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral, no un paso más de la secuencia arquitectónica (§4 del plan
> `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES de la sección 1 y ANTES de
> saber cómo se llaman los contratos de este capítulo. El detalle estructurado de esta
> sección vive en `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set`
> valida automáticamente.

**Resultado esperado.** Al terminar este capítulo podrás diagnosticar si una decisión
arquitectónica de un arnés de agentes está gobernada de forma determinística y verificable, o
si en realidad sigue implícita en el buen juicio del modelo — y podrás señalar, para cualquier
propuesta de diseño futura, qué contrato de datos fundamental falta para hacer esa decisión
auditable.

**Esqueleto.** Este capítulo recorre 19 secciones (Arquitectura Actual → Next Increment, ver
tabla de contenidos) e introduce siete contratos de datos fundamentales (`AgentMessage`,
`AgentConfig`, `AgentState`, `ExecutionContext`, `AgentEvent`, `HarnessError`,
`ExecutionBudget`) — todavía sin explicarlos, solo como mapa. No introduce ningún componente
de runtime.

**Preguntas guía** (respóndelas de memoria en la sección 21 — "Recordar" — sin volver a mirar
atrás; están formuladas en lenguaje de problema, sin usar todavía los nombres canónicos que
este capítulo va a definir):

1. Si un agente puede llegar a ejecutar acciones con efectos reales, ¿quién decide si una de
   esas acciones es segura, y cómo se hace esa decisión verificable en vez de dejarla
   implícita en el criterio del modelo?
2. ¿Cómo evitamos que cada mensaje que produce un modelo dentro del ciclo cognitivo tenga una
   forma distinta según quién lo generó, de modo que nada más adelante en el sistema pueda
   depender de una forma estable?
3. Si la ejecución de un agente se detiene a la mitad de una tarea, ¿cómo sabemos en qué
   punto exacto del proceso quedó, sin tener que preguntarle al propio modelo?
4. ¿Qué impide que un agente siga ejecutando turnos indefinidamente, gastando tiempo y
   dinero, si nadie — ni siquiera el modelo — recuerda imponerle un límite?
5. Cuando algo falla a mitad de una ejecución, ¿cómo distinguimos un fallo que conviene
   reintentar de uno que exige detener todo, sin que la respuesta dependa de quién escribió
   ese manejo de errores en particular?

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

## 20. Lente de Sistemas (Systems Lens)

> Sección de cierre del cuerpo del capítulo (§4 del plan de método activo), no un paso más de
> la secuencia arquitectónica. No introduce contenido nuevo: reetiqueta, bajo el marco
> Iceberg / Bucles de retroalimentación / Punto de apalancamiento (Dinámica de Sistemas,
> Forrester/Meadows), secciones que este mismo capítulo ya estaba obligado a tener.

**El Iceberg**

1. **Hecho visible** (= §2, El Problema): construir un arnés de agentes puede degenerar en una
   colección cada vez más larga de instrucciones de prompt que le piden al modelo, con más y
   más énfasis, que "por favor" no haga cosas peligrosas, no invente funciones que no existen,
   y no olvide los límites de presupuesto.
2. **Patrones que se repiten** (= §3, Por Qué la Arquitectura Actual No Basta): un prompt no
   puede garantizar que una acción con efectos secundarios pase por autorización, que un error
   se clasifique siempre igual, que un límite de ejecución se respete aunque el modelo lo
   olvide, ni impedir que un capítulo futuro use una entidad que este libro todavía no ha
   definido.
3. **Estructuras / reglas / incentivos** (= §8, Component Responsibilities + Security/Policy):
   todavía no existe ningún componente de runtime; lo que este capítulo instala son los
   contratos de datos (§6/§7) y dos políticas concretas — P-05 (toda acción con efectos
   secundarios pasa por política) y P-13 (la autorización es determinística y externa al
   modelo) — que cualquier componente futuro deberá cumplir por diseño, no por buena voluntad.
4. **Modelos mentales** (= §4, Constitutional Impact): el límite Probabilístico y
   Determinístico del Article XII — el modelo propone intención; el arnés gobierna identidad,
   autorización, límites, estado y ejecución. Nunca al revés.

**Bucles de retroalimentación**

- **Bucle de refuerzo (espiral):** cada vez que una decisión de autorización se deja implícita
  en el prompt en lugar de en un contrato explícito, aumenta la probabilidad de que el próximo
  capítulo repita el mismo atajo "por si acaso", apilando más prosa persuasiva en vez de más
  estructura. Este capítulo corta esa espiral de raíz al declarar P-05/P-13 antes de que exista
  código que pueda violarlas.
- **Bucle de equilibrio (estabiliza):** `governTurnContinuation` (§11) es el mecanismo de
  equilibrio — cada vez que `state.currentTurn` se acerca a `budget.maxTurns`, la función
  determinística detiene la ejecución con un `HarnessError` en lugar de dejar que la espiral de
  turnos continúe indefinidamente.

**Punto de apalancamiento**

La decisión con mayor efecto de este capítulo es que `ExecutionBudget` (C-012) y `AgentState`
(C-003) existan como contratos de datos **antes** que cualquier componente que los use. Si esta
frontera de "datos antes que comportamiento" no se fija aquí, ningún límite de ejecución futuro
será verificable — solo prometido en prosa.

## 21. Practica lo que Aprendiste (Practice What You Learned)

> Sección de cierre del capítulo (§4 del plan de método activo). El detalle estructurado
> completo de esta sección (con ids estables para cada pregunta/tarjeta) vive en
> `retrieval_set` (frontmatter) y es lo que `scripts/validate-retrieval-set` valida. Aquí se
> presenta en prosa, para lectura directa del capítulo.

### Recordar

Vuelve a la sección 0 y responde de memoria, sin mirar atrás, antes de seguir leyendo:

1. ¿Qué principio y qué invariante de la Constitution establecen que la autorización de una
   acción es una decisión determinística y externa al modelo, y qué política concreta lo
   enuncia en este capítulo? *(cierra la pregunta guía 1)*
2. ¿Qué contrato define la forma estable de todo mensaje del ciclo cognitivo, y qué cuatro
   campos garantiza siempre, sin importar qué componente lo produzca? *(cierra la pregunta
   guía 2)*
3. ¿Qué contrato representa el punto exacto de ejecución de un agente, y qué enum define los
   estados posibles por los que puede pasar esa ejecución? *(cierra la pregunta guía 3)*
4. ¿Qué contrato agrupa todos los límites de ejecución de un agente, y qué función de este
   capítulo es la primera en verificar uno de esos límites? *(cierra la pregunta guía 4)*
5. ¿Qué contrato clasifica todo fallo operacional, y qué dos campos booleanos determinan si
   conviene reintentar la operación o detener todo? *(cierra la pregunta guía 5)*

### Explicar

1. Explica en voz alta, como si hablaras con alguien sin ningún contexto técnico, qué SÍ
   decide el modelo de lenguaje en este capítulo y qué NUNCA decide, aunque lo proponga. ¿Por
   qué la Constitution se lo prohíbe explícitamente en el texto, en vez de simplemente confiar
   en que el modelo coopere? *(límite Model vs. Harness Runtime, Article XII)*
2. `HarnessError` posee la responsabilidad de clasificar un fallo (`category`, `recoverable`,
   `retryable`). Explica qué **NO** posee `HarnessError`: ¿quién decide, entonces, si realmente
   se reintenta la operación, y por qué esa decisión no le pertenece al propio error?

### Conectar

Este capítulo es el primero del libro (`previous_chapter: null`): no existe todavía un capítulo
anterior con el cual mezclar preguntas de interleaving. Esta excepción se documenta aquí en vez
de inventar un capítulo previo que no existe — `scripts/validate-retrieval-set` exime
explícitamente a `CH-00` de la regla "≥ 1 interleavedQuestion" por esta misma razón. El
movimiento "Conectar" se retoma con normalidad a partir de `CH-01`, que sí podrá mezclar
entidades propias con las de este capítulo (`AgentMessage`, `AgentState`, `ExecutionBudget`,
`HarnessError`, ...).

### Espaciar

Las siete tarjetas de repaso de este capítulo (una por contrato introducido: `AgentMessage`,
`AgentConfig`, `AgentState`, `ExecutionContext`, `AgentEvent`, `HarnessError`,
`ExecutionBudget`) entran hoy en `reviewStage = DAY_1`. Repásalas de nuevo al día 3, al día 7 y
al día 21 (curva de Ebbinghaus) — ver el apéndice de tarjetas al final del libro (edición PDF) o
`retrieval_set.flashcards` en `dist/book-ir.json` (edición Web; la vista `/repaso` con
calendario interactivo por lector es explícitamente v0.2+, no v0.1).

### Calibrar

*(Adición propia de este método, no citada de las fuentes de §0 del plan — práctica de
metacognición complementaria.)* Antes de revisar tus respuestas de "Recordar", califica tu
confianza en cada una — Alta / Media / Baja — y solo entonces compára la con el texto del
capítulo. Si calificaste "Alta" y te equivocaste, ese es precisamente el punto ciego que este
método existe para revelar.
