---
id: CH-43
title: "Presupuestos que se Heredan"
starting_version: "0.2.1"
ending_version: "0.3"
introduces_components: []
introduces_contracts: [C-057]
modifies_contracts: [C-012]
constitutional_articles: [P-09, P-35, INV-09, INV-E06, INV-E21]
previous_chapter: CH-42
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH43
    text: |
      Al terminar este capítulo podrás decidir cuánto presupuesto recibe cada run hijo a partir de lo
      que le queda a su padre, explicar por qué un hijo nunca puede recibir más, y calcular cuánto le
      queda al padre después de que sus hijos terminan.
  skeleton:
    id: SK-CH43
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
    contracts_to_be_introduced: [C-057]
  guiding_questions:
    - id: GQ-CH43-01
      text: |
        Si un agente con un presupuesto de 10 dólares lanza tres tareas en paralelo, ¿cuánto debería
        poder gastar cada una? ¿Y si ya había gastado 4?
      answered_by: RQ-CH43-01
    - id: GQ-CH43-02
      text: |
        Si una tarea delegada gasta más de lo previsto, ¿cómo se entera el agente que la lanzó, y qué
        le queda para lo que sigue?
      answered_by: RQ-CH43-02
    - id: GQ-CH43-03
      text: |
        ¿Debería una tarea delegada poder tener más tiempo, más turnos o más memoria que el agente que
        la lanzó?
      answered_by: RQ-CH43-03
    - id: GQ-CH43-04
      text: |
        Si el código que corre en el entorno aislado se queda sin memoria, ¿debería detenerse todo el
        run o solo esa herramienta?
      answered_by: RQ-CH43-04
  systems_lens:
    iceberg_visible_fact: |
      Cada run tiene un ExecutionBudget plano: no sabe si es hijo de otro, no lleva lo que ya consumió
      y no tiene límites para el entorno aislado; delegar trabajo equivale a darle al hijo un
      presupuesto nuevo, completo, que nadie descuenta del padre (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que INV-E06 exige que la delegación quede acotada por el presupuesto,
      pero ExecutionUsage era una estructura interna de ExecutionController y no cruzaba de un run a
      otro, así que el saldo del padre no podía limitar al hijo (ver sección 3).
    iceberg_structures: |
      Este capítulo promueve ExecutionUsage a contrato (C-057), lleva ExecutionBudget (C-012) a v2 con
      parentRunId, consumed y sandboxLimits (ADR-004), y le da a ExecutionController el reparto, la
      verificación y la suma del uso de los hijos (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son INV-E21 (un hijo nunca excede el saldo del padre), INV-E06 (la
      delegación queda acotada por el presupuesto), INV-09 (todo run tiene límites explícitos) y P-09
      (el presupuesto jerárquico va antes que la complejidad multi-agente) (ver sección 4).
    reinforcing_loop: |
      Si cada hijo recibe un presupuesto completo, delegar se vuelve la forma de saltarse el límite: un
      run que se queda sin saldo lanza hijos, que lanzan nietos, y el gasto total crece sin techo. El
      reparto desde el saldo corta la espiral.
    balancing_loop: |
      rollUpChildUsage es el mecanismo de equilibrio: lo que gasta cada hijo se descuenta del padre, así
      que cada lote nuevo de hijos se reparte un saldo más chico.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que ExecutionUsage (C-057) cruce la frontera
      padre-hijo: con el uso del padre como dato, allocateChildBudget reparte solo el saldo y
      rollUpChildUsage devuelve lo gastado, así que la delegación nunca agranda el presupuesto total.
  recall_questions:
    - id: RQ-CH43-01
      text: |
        ¿Qué dimensiones reparte allocateChildBudget entre los hijos de un lote, cuáles copia del padre
        como techo, y qué pasa si el reparto deja a algún hijo con cero?
    - id: RQ-CH43-02
      text: |
        ¿Qué suma rollUpChildUsage al uso del padre, qué no suma, y por qué?
    - id: RQ-CH43-03
      text: |
        ¿Qué verifica childBudgetWithinParent, y qué devuelve para un hijo sin límites de entorno si el
        padre sí los tiene?
    - id: RQ-CH43-04
      text: |
        ¿Qué compara sandboxLimitsExceeded, qué devuelve, y qué le pasa a la tool call y al run cuando un
        límite se supera?
  explain_prompts:
    - id: EP-CH43-01
      text: |
        ExecutionController ya decidía si un run puede seguir contra su presupuesto. Explica, como si
        hablaras con alguien sin contexto técnico, por qué repartir el presupuesto entre hijos también
        le pertenece, y por qué no hace falta un componente nuevo.
      target_entity: CMP-007
    - id: EP-CH43-02
      text: |
        Explica por qué ExecutionUsage pasó de estructura interna a contrato, y qué no se podría
        verificar si el uso del padre siguiera siendo un detalle de ExecutionController.
      target_entity: C-057
  interleaved_questions:
    - id: IQ-CH43-01
      text: |
        En CH-39, accumulateUsage sumaba el costo de cada llamada al modelo al ExecutionUsage del run.
        ¿Cómo se combina con rollUpChildUsage para que el costo de un hijo cuente contra el maxCost del
        padre, y qué función de CH-07 lo hace cumplir sin cambiar?
      current_chapter_entities: [C-057]
      prior_chapter_entities: [C-012, CMP-007]
      prior_chapter: CH-07
  flashcards:
    - id: FC-CH43-01
      front: |
        ¿Qué es ExecutionUsage (C-057) y por qué es un contrato desde CH-43?
      back: |
        El uso acumulado de un run: tool calls, tokens, costo, tiempo y concurrencia. Era interno de
        ExecutionController (CH-07); es contrato porque ahora cruza la frontera padre-hijo.
      source_entity: C-057
      chapter_introduced_in: CH-43
      review_stage: DAY_1
    - id: FC-CH43-02
      front: |
        ¿Qué agrega ExecutionBudget v2 (C-012)?
      back: |
        parentRunId (de qué run es hijo), consumed (ExecutionUsage) y sandboxLimits (CPU, memoria y
        disco del entorno aislado). Los tres son opcionales: un run raíz se comporta como en v1.
      source_entity: C-012
      chapter_introduced_in: CH-43
      review_stage: DAY_1
    - id: FC-CH43-03
      front: |
        ¿Qué dice INV-E21 y qué función lo verifica?
      back: |
        Un presupuesto hijo nunca excede el saldo de su padre. childBudgetWithinParent lo verifica
        dimensión por dimensión, y requireChildWithinParent rechaza el hijo que no cumple.
      source_entity: C-057
      chapter_introduced_in: CH-43
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH43-01
      recall_question: RQ-CH43-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH43-02
      recall_question: RQ-CH43-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH43-03
      recall_question: RQ-CH43-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH43-04
      recall_question: RQ-CH43-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 43 — Presupuestos que se Heredan

> **Regla constitucional (INV-E21):** un presupuesto hijo nunca excede el saldo de su padre.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir cuánto presupuesto recibe cada run
hijo a partir de lo que le queda a su padre, y explicar por qué un hijo nunca puede recibir más.
También podrás calcular cuánto le queda al padre después de que sus hijos terminan.

**Esqueleto.** Quinto capítulo de la versión 0.3. No introduce componentes: promueve `ExecutionUsage`
a contrato, lleva `ExecutionBudget` a v2 (ADR-004) y amplía `ExecutionController`.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si un agente con un presupuesto de 10 dólares lanza tres tareas en paralelo, ¿cuánto debería
   poder gastar cada una? ¿Y si ya había gastado 4?
2. Si una tarea delegada gasta más de lo previsto, ¿cómo se entera el agente que la lanzó, y qué le
   queda para lo que sigue?
3. ¿Debería una tarea delegada poder tener más tiempo, más turnos o más memoria que el agente que la
   lanzó?
4. Si el código que corre en el entorno aislado se queda sin memoria, ¿debería detenerse todo el run o
   solo esa herramienta?

## 1. Arquitectura Actual (Current Architecture)

- **`ExecutionController` (CMP-007, CH-07)** compara el `ExecutionUsage` de un run con su
  `ExecutionBudget` (C-012) en `evaluateExecutionContinuation`, y decide `CONTINUE`, `STOP` o
  `CANCELLED`.
- **`ExecutionBudget`** es plano: turnos, tool calls, tokens, costo, tiempo y concurrencia. No sabe si
  el run es hijo de otro, ni cuánto lleva consumido.
- **`ExecutionUsage`** es una estructura embebida de CH-07, sin contrato propio. Desde CH-39,
  `accumulateUsage` le suma el costo de cada llamada al modelo.
- **`IsolatedExecutionEnvironment` (CH-35)** abre el entorno aislado sin límites de CPU, memoria ni
  disco (deuda D-026).
- **INV-E06** exige que la delegación quede acotada por el presupuesto. La invocación entre agentes
  llega en CH-44, y P-09 pide resolver el presupuesto antes.

## 2. El Problema (Problem)

Un agente analiza un contrato y decide delegar tres revisiones en paralelo: legal, financiera y de
riesgo. Hoy:
- **cada revisión recibe un presupuesto completo**, igual al del padre, porque no hay otro;
- **lo que gastan no se descuenta del padre:** después de las tres, el padre cree que le queda lo
  mismo que antes;
- **delegar es la forma de saltarse el límite.** Un run que se queda sin saldo puede lanzar hijos, que
  lanzan nietos, y el gasto total no tiene techo;
- **el entorno aislado no tiene límites:** un comando que consume toda la memoria afecta al resto.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **`ExecutionUsage` no cruza la frontera entre runs.** Si es un detalle interno de
  `ExecutionController`, el saldo del padre no puede limitar al hijo, y lo que gasta el hijo no puede
  volver al padre.
- **`ExecutionBudget` no tiene dónde decir "soy hijo de este run"** ni "llevo esto consumido".
- **No hay regla de reparto.** Sin ella, cada integración decidiría cuánto darle a un hijo.
- **Los límites del entorno aislado no tienen dueño:** son límites de recursos, y los límites ya son
  de `ExecutionController` ("runtime limits"). Por eso no hace falta un componente nuevo (EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-09   Single-agent reliability precedes multi-agent complexity.
           El presupuesto jerárquico existe antes de la invocación entre agentes (CH-44).
    P-35   Secrets never enter model-controlled compute.
           El entorno aislado gana límites de recursos; sigue sin credenciales.

Invariants preserved
    INV-09   Todo AgentRun tiene límites explícitos. También un hijo, y desde el saldo del padre.
    INV-E06  Delegation depth, child runs and delegated cost are bounded by ExecutionBudget.
             allocateChildBudget y rollUpChildUsage lo mecanizan.
    INV-E21  (Amendment v1.2) A child budget never exceeds its parent's remaining budget.
             childBudgetWithinParent lo verifica.

Component ownership changes
    Ninguno nuevo. ExecutionController gana funciones dentro de "budgets" y "runtime limits".

Contract changes
    Nuevo: C-057 ExecutionUsage (promovido desde la estructura embebida de CH-07).
    C-012 ExecutionBudget v1 → v2 (+ parentRunId, + consumed, + sandboxLimits; ADR-004 Accepted).

Observability implications
    Nuevo AgentEventType: CHILD_BUDGET_ALLOCATED.
```

## 5. Conceptos Nuevos (New Concepts)

- **Saldo:** lo que le queda a un run en cada dimensión (presupuesto menos uso).
- **Lote de hijos:** los runs hijos que un padre lanza a la vez. Se reparten el saldo del padre.
- **Reparto por dimensión:**
  - **se dividen** las dimensiones que los hijos consumen del mismo saldo: tool calls, tokens de
    entrada y de salida, costo;
  - **se acota sin dividir** el tiempo restante: los hijos de un lote corren en paralelo, y cada uno
    puede usar a lo sumo lo que le queda al padre;
  - **se copian como techo** los turnos, la concurrencia y los límites del entorno aislado.
- **Devolver el gasto:** cuando un hijo termina, lo que consumió se suma al uso del padre. El lote
  siguiente se reparte un saldo más chico.
- **Límites del entorno aislado:** CPU, memoria y disco que puede usar el código del entorno de una
  sesión. Si una tool los supera, esa tool falla; el run sigue.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `ExecutionBudget` (C-012, que pasa a v2), `ExecutionContext` (C-004),
  `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `RunId`, `AgentId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `AgentEventType` | se agrega `CHILD_BUDGET_ALLOCATED` |
| `ErrorCategory` | reutiliza `BUDGET` y `VALIDATION` |

### `ExecutionUsage` — el uso de un run, ahora contrato (C-057)

```pseudocode
STRUCT ExecutionUsage
    toolCallsUsed: Integer
    inputTokensUsed: Integer
    outputTokensUsed: Integer
    costUsed: Number
    runtimeMsElapsed: Integer
    concurrentToolsInFlight: Integer
END
```

Los campos son los mismos que en CH-07: promoverlo a contrato no cambia su forma, solo lo vuelve un
dato que cruza de un run a otro.

### `SandboxLimits` y `SandboxUsage` — límites del entorno aislado (embebidos)

```pseudocode
STRUCT SandboxLimits
    maxCpuMillis: Integer
    maxMemoryMb: Integer
    maxDiskMb: Integer
END
```

```pseudocode
STRUCT SandboxUsage
    cpuMillis: Integer
    memoryMb: Integer
    diskMb: Integer
END
```

### `ExecutionBudget` — versión 2 (C-012)

```pseudocode
STRUCT ExecutionBudget
    maxTurns: Integer
    maxToolCalls: Integer
    maxInputTokens: Integer
    maxOutputTokens: Integer
    maxCost: Number
    maxRuntimeMs: Integer
    maxConcurrentTools: Integer
    parentRunId: Optional<RunId>
    consumed: Optional<ExecutionUsage>
    sandboxLimits: Optional<SandboxLimits>
END
```

**Compatibilidad hacia atrás:** con los tres campos nuevos en `NULL`, un presupuesto es el de un run
raíz, sin límites de entorno, como en CH-00..CH-42. `consumed` es opcional por decisión del autor al
aprobar ADR-004.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-057
Name:                   ExecutionUsage
Version:                v1
Introduced In:          CH-43
Used By:                [CMP-007]
Constitutional Impact:  [INV-09, INV-E06, INV-E21]
```

```text
C-012 ExecutionBudget  v1 → v2   Modified By: [CH-43]
                       + parentRunId: Optional<RunId>
                       + consumed: Optional<ExecutionUsage>
                       + sandboxLimits: Optional<SandboxLimits>
ADR:                   ADR-004 (Accepted 2026-10-10)
```

`SandboxLimits` y `SandboxUsage` quedan embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce componentes.** `ExecutionController` gana funciones dentro de su `owns`
literal:

```text
ExecutionController (CMP-007)
    owns: "budgets", "cancellation", "deadlines", "runtime limits", "operational continuation"
    nuevas, dentro de "budgets":
        allocateChildBudget, childBudgetWithinParent, requireChildWithinParent, rollUpChildUsage
    nueva, dentro de "runtime limits":
        sandboxLimitsExceeded
    no posee:
        decidir SI delegar ni en qué agente (la integración y AgentCommunicationGateway, CH-44)
        hacer cumplir físicamente los límites del entorno (la infraestructura del aislamiento, CH-35)
        cancelar al hijo (OperationalController, CH-18, o la integración)
```

Un componente `BudgetAllocator` aparte violaría EVO-01: los límites ya son de `ExecutionController`
(ADR-004, alternativas).

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
Antes de lanzar un lote:  allocateChildBudget(presupuesto del padre, uso del padre, tamaño del lote)
Al recibir un presupuesto: requireChildWithinParent (también lo usa la invocación entre agentes, CH-44)
Durante el hijo:          evaluateExecutionContinuation (CH-07) con su propio presupuesto, sin cambios
En cada tool aislada:     sandboxLimitsExceeded → la tool falla si se superó un límite
Al terminar cada hijo:    rollUpChildUsage → uso del padre → evaluateExecutionContinuation del padre
```

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Padre (ExecutionController) → allocateChildBudget → hijos (cada uno con su ExecutionBudget v2)
hijos → rollUpChildUsage → uso del padre → evaluateExecutionContinuation (CH-07)
```

**Vista 2 — Sequence: tres revisiones en paralelo**

```text
Padre: maxCost 10, costUsed 4; maxToolCalls 30, toolCallsUsed 12
   │ allocateChildBudget(…, lote de 3)
   │   → cada hijo: maxCost 2, maxToolCalls 6, tiempo = el restante del padre, techo de turnos y entorno
   │   → CHILD_BUDGET_ALLOCATED
   ▼ hijos corren (cada uno se detiene con STOP si agota lo suyo, CH-07)
   │ rollUpChildUsage × 3 (costos 1,5 · 2 · 0,8)
Padre: costUsed 8,3 → le quedan 1,7 para lo que sigue
```

**Vista 2b — Sequence: un lote demasiado grande**

```text
allocateChildBudget(…, lote de 20) con 18 tool calls restantes
   → FANOUT_EXCEEDS_REMAINING_BUDGET   (un reparto de 0 tool calls por hijo no crea hijos)
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION allocateChildBudget(
    parent: ExecutionBudget,
    parentRunId: RunId,
    parentUsage: ExecutionUsage,
    fanout: Integer,
    execution: ExecutionContext,
    agentId: AgentId
) -> ExecutionBudget

    IF fanout < 1
        THROW HarnessError(
            category = VALIDATION,
            code = "INVALID_FANOUT",
            message = "Un lote de hijos tiene al menos un hijo",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    remainingToolCalls: Integer = parent.maxToolCalls - parentUsage.toolCallsUsed
    remainingInput: Integer = parent.maxInputTokens - parentUsage.inputTokensUsed
    remainingOutput: Integer = parent.maxOutputTokens - parentUsage.outputTokensUsed
    remainingCost: Number = parent.maxCost - parentUsage.costUsed
    remainingRuntime: Integer = parent.maxRuntimeMs - parentUsage.runtimeMsElapsed

    childToolCalls: Integer = floorDiv(remainingToolCalls, fanout)
    childInput: Integer = floorDiv(remainingInput, fanout)
    childOutput: Integer = floorDiv(remainingOutput, fanout)
    childCost: Number = remainingCost / fanout

    IF childToolCalls < 1 OR childInput < 1 OR childOutput < 1 OR childCost <= 0 OR remainingRuntime <= 0
        THROW HarnessError(
            category = BUDGET,
            code = "FANOUT_EXCEEDS_REMAINING_BUDGET",
            message = "El saldo del padre no alcanza para darle a cada hijo del lote algo en cada dimensión",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    child: ExecutionBudget = ExecutionBudget(
        maxTurns = parent.maxTurns,
        maxToolCalls = childToolCalls,
        maxInputTokens = childInput,
        maxOutputTokens = childOutput,
        maxCost = childCost,
        maxRuntimeMs = remainingRuntime,
        maxConcurrentTools = parent.maxConcurrentTools,
        parentRunId = parentRunId,
        consumed = NULL,
        sandboxLimits = parent.sandboxLimits
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = CHILD_BUDGET_ALLOCATED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = child
    )

    RETURN child
END
```

```pseudocode
FUNCTION childBudgetWithinParent(
    child: ExecutionBudget,
    parent: ExecutionBudget,
    parentUsage: ExecutionUsage
) -> Boolean

    sandboxWithin: Boolean = parent.sandboxLimits == NULL
        OR (child.sandboxLimits != NULL
            AND child.sandboxLimits.maxCpuMillis <= parent.sandboxLimits.maxCpuMillis
            AND child.sandboxLimits.maxMemoryMb <= parent.sandboxLimits.maxMemoryMb
            AND child.sandboxLimits.maxDiskMb <= parent.sandboxLimits.maxDiskMb)

    RETURN child.maxTurns <= parent.maxTurns
        AND child.maxToolCalls <= parent.maxToolCalls - parentUsage.toolCallsUsed
        AND child.maxInputTokens <= parent.maxInputTokens - parentUsage.inputTokensUsed
        AND child.maxOutputTokens <= parent.maxOutputTokens - parentUsage.outputTokensUsed
        AND child.maxCost <= parent.maxCost - parentUsage.costUsed
        AND child.maxRuntimeMs <= parent.maxRuntimeMs - parentUsage.runtimeMsElapsed
        AND child.maxConcurrentTools <= parent.maxConcurrentTools
        AND sandboxWithin
END
```

```pseudocode
FUNCTION requireChildWithinParent(
    child: ExecutionBudget,
    parent: ExecutionBudget,
    parentUsage: ExecutionUsage
) -> ExecutionBudget

    IF NOT childBudgetWithinParent(child, parent, parentUsage)
        THROW HarnessError(
            category = BUDGET,
            code = "CHILD_BUDGET_EXCEEDS_PARENT",
            message = "El presupuesto del hijo excede el saldo del padre en alguna dimensión (INV-E21)",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN child
END
```

```pseudocode
FUNCTION rollUpChildUsage(
    parentUsage: ExecutionUsage,
    childUsage: ExecutionUsage
) -> ExecutionUsage

    RETURN ExecutionUsage(
        toolCallsUsed = parentUsage.toolCallsUsed + childUsage.toolCallsUsed,
        inputTokensUsed = parentUsage.inputTokensUsed + childUsage.inputTokensUsed,
        outputTokensUsed = parentUsage.outputTokensUsed + childUsage.outputTokensUsed,
        costUsed = parentUsage.costUsed + childUsage.costUsed,
        runtimeMsElapsed = parentUsage.runtimeMsElapsed,
        concurrentToolsInFlight = parentUsage.concurrentToolsInFlight
    )
END
```

```pseudocode
FUNCTION sandboxLimitsExceeded(
    budget: ExecutionBudget,
    usage: SandboxUsage
) -> Optional<HarnessError>

    IF budget.sandboxLimits == NULL
        RETURN NULL
    END

    IF usage.cpuMillis > budget.sandboxLimits.maxCpuMillis
        OR usage.memoryMb > budget.sandboxLimits.maxMemoryMb
        OR usage.diskMb > budget.sandboxLimits.maxDiskMb

        RETURN HarnessError(
            category = BUDGET,
            code = "SANDBOX_LIMIT_EXCEEDED",
            message = "La tool superó un límite de CPU, memoria o disco del entorno aislado",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN NULL
END
```

`floorDiv` (división entera hacia abajo), `newEventId` y `now` son utilidades primitivas.

**Por qué `rollUpChildUsage` no suma el tiempo ni la concurrencia:**
- el tiempo del padre es su reloj, y los hijos corren en paralelo dentro de él;
- la concurrencia es un valor del momento, no un acumulado.

El tiempo del padre sigue corriendo mientras espera a sus hijos, y `evaluateExecutionContinuation`
(CH-07) lo compara con `maxRuntimeMs` como siempre.

Nótese lo que estas funciones **no** hacen:
- ninguna decide si delegar: lo decide la integración, y la invocación entre agentes llega en CH-44;
- `allocateChildBudget` nunca crea saldo: todo lo que da sale de lo que le queda al padre;
- `sandboxLimitsExceeded` no detiene el run: devuelve el error para que la tool falle.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no cambia `AgentRunStatus`. El saldo del padre a lo largo de un lote:

```text
antes del lote     → saldo S
allocateChildBudget → cada hijo recibe S / n en tool calls, tokens y costo (o falla si alguno queda en 0)
cada hijo termina  → rollUpChildUsage: el uso del padre crece en lo que gastó el hijo
después del lote   → saldo S − (gasto de los hijos); el lote siguiente se reparte eso

Tool en el entorno aislado
    dentro de los límites → resultado normal
    supera un límite      → ToolResult fallido con SANDBOX_LIMIT_EXCEEDED; el run sigue
```

## 13. Semántica de Fallos (Failure Semantics)

Códigos nuevos de `HarnessError`, con `ErrorCategory` ya existentes:

```text
VALIDATION  INVALID_FANOUT                   recoverable: FALSE, retryable: FALSE
BUDGET      FANOUT_EXCEEDS_REMAINING_BUDGET  recoverable: FALSE, retryable: FALSE
BUDGET      CHILD_BUDGET_EXCEEDS_PARENT      recoverable: FALSE, retryable: FALSE
BUDGET      SANDBOX_LIMIT_EXCEEDED           recoverable: TRUE,  retryable: FALSE
```

`SANDBOX_LIMIT_EXCEEDED` vuelve al modelo como observación de una tool fallida (INV-07); el modelo
puede intentar algo más chico. Un hijo que agota su presupuesto se detiene con `STOP` (CH-07), y su uso
igual se suma al padre.

## 14. Eventos Producidos (Events Produced)

```text
CHILD_BUDGET_ALLOCATED — el padre asignó el presupuesto de un hijo (payload: ExecutionBudget)
```

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Delegar no es una forma de gastar más.** Todo lo que recibe un hijo sale del saldo del padre, y
  todo lo que gasta vuelve al padre.
- **Un presupuesto ajeno se verifica.** Un presupuesto que llega con una invocación (CH-44) pasa por
  `requireChildWithinParent` antes de usarse.
- **Un hijo no se libera de los límites del entorno.** Si el padre tiene límites, un hijo sin límites
  queda fuera de su presupuesto.
- **Un comando que consume toda la memoria falla solo:** la tool supera el límite y vuelve al modelo
  como observación, sin afectar a otras sesiones (CH-35, INV-E07).

## 16. Tests (Tests)

```text
TEST ChildBudgetSplitsTheRemainingNotTheTotal
TEST ChildRuntimeIsTheRemainingRuntimeNotDivided
TEST ChildCopiesTurnsConcurrencyAndSandboxLimitsAsCeiling
TEST FanoutThatLeavesAChildWithZeroIsRejected
TEST InvalidFanoutIsRejected
TEST AllocationEmitsChildBudgetAllocated
TEST ChildBudgetAboveTheParentRemainingIsRejected
TEST ChildWithoutSandboxLimitsIsNotWithinAParentWithLimits
TEST ChildUsageRollsUpIntoTheParent
TEST RollUpDoesNotAddRuntimeOrConcurrency
TEST NextBatchSplitsTheReducedRemaining
TEST SandboxLimitExceededFailsOnlyTheTool
TEST RootBudgetWithoutNewFieldsBehavesAsV1
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.3 en curso, después de CH-43) — 29 componentes, 57 contratos, 44 capítulos

Components — 29, sin cambios
 └── CMP-007 ExecutionController   (+ reparto, verificación, suma del uso de hijos, límites del entorno)

Contracts — 57
 ├── C-012 ExecutionBudget v2      (CH-00 → modificado en CH-43: parentRunId, consumed, sandboxLimits)
 └── C-057 ExecutionUsage          (CH-43, promovido desde CH-07)

Deuda: D-026 resuelta.
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Repartos desiguales** (darle más a un hijo que a otro): la regla del capítulo es pareja dentro de
  un lote; un reparto ponderado sería otra función con la misma verificación. No es deuda.
- **Profundidad máxima de delegación:** el saldo la acota en la práctica, porque cada nivel recibe
  menos; un límite explícito de profundidad llega con la invocación entre agentes (CH-44), que ya lo
  planea dentro de INV-E06. No es deuda.
- **Cancelar a los hijos cuando el padre se cancela:** es un comando operacional (CH-18) que se cablea
  en la invocación entre agentes (CH-44). No es deuda.
- **Hacer cumplir físicamente los límites del entorno** (cgroups, cuotas): infraestructura del
  aislamiento. No es deuda.

## 19. Siguiente Incremento (Next Increment)

Ahora un run puede repartir su presupuesto entre hijos sin agrandarlo. Pero todavía no hay una forma
gobernada de **invocar a otro agente**: ni a uno del mismo arnés con un run hijo durable, ni a uno
externo que hable A2A.

El siguiente capítulo introduce la **invocación durable entre agentes**, el único capítulo
multi-agente de la versión 0.3:
- una `AgentInvocation` con dueño, estado y presupuesto heredado;
- una `AgentCard` que anuncia capacidades;
- A2A como un adaptador del `AgentCommunicationGateway`, nunca como dependencia del núcleo.

Será CH-44 ("Invocación Durable entre Agentes y A2A"). `next_chapter` queda en `null` porque CH-44
todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): cada hijo recibe un presupuesto completo, su gasto no vuelve al padre y
   el entorno aislado no tiene límites.
2. **Patrones** (= §3): `ExecutionUsage` no cruzaba de un run a otro, así que el saldo del padre no
   limitaba al hijo.
3. **Estructuras** (= §8): `ExecutionUsage` (C-057), `ExecutionBudget` v2 y funciones nuevas en
   `ExecutionController`.
4. **Modelos mentales** (= §4): INV-E21, INV-E06, INV-09 y P-09.

**Bucles de retroalimentación**

- **Refuerzo:** delegar para saltarse el límite hace crecer el gasto sin techo. Repartir desde el saldo
  corta la espiral.
- **Equilibrio:** `rollUpChildUsage`. Cada lote nuevo se reparte un saldo más chico.

**Punto de apalancamiento**

La decisión con mayor efecto es que `ExecutionUsage` (C-057) cruce la frontera padre-hijo, para que la
delegación nunca agrande el presupuesto total.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué dimensiones reparte `allocateChildBudget` entre los hijos de un lote, cuáles copia del padre
   como techo, y qué pasa si el reparto deja a algún hijo con cero? *(pregunta guía 1)*
2. ¿Qué suma `rollUpChildUsage` al uso del padre, qué no suma, y por qué? *(pregunta guía 2)*
3. ¿Qué verifica `childBudgetWithinParent`, y qué devuelve para un hijo sin límites de entorno si el
   padre sí los tiene? *(pregunta guía 3)*
4. ¿Qué compara `sandboxLimitsExceeded`, qué devuelve, y qué le pasa a la tool call y al run cuando un
   límite se supera? *(pregunta guía 4)*

### Explicar

1. `ExecutionController` ya decidía si un run puede seguir contra su presupuesto. Explica por qué
   repartir el presupuesto entre hijos también le pertenece, y por qué no hace falta un componente
   nuevo.
2. Explica por qué `ExecutionUsage` pasó de estructura interna a contrato, y qué no se podría verificar
   si el uso del padre siguiera siendo un detalle de `ExecutionController`.

### Conectar

1. En CH-39, `accumulateUsage` sumaba el costo de cada llamada al modelo al `ExecutionUsage` del run.
   ¿Cómo se combina con `rollUpChildUsage` para que el costo de un hijo cuente contra el `maxCost` del
   padre, y qué función de CH-07 lo hace cumplir sin cambiar?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
