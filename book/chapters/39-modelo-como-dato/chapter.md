---
id: CH-39
title: "El Modelo como Dato: Catálogo, Costo y Cache"
starting_version: "0.2.1"
ending_version: "0.3"
introduces_components: []
introduces_contracts: [C-049, C-050]
modifies_contracts: [C-006, C-007]
constitutional_articles: [P-02, P-29, INV-09, INV-E10]
previous_chapter: CH-38
next_chapter: CH-40
retrieval_set:
  expected_outcome:
    id: EO-CH39
    text: |
      Al terminar este capítulo podrás decidir qué modelo usa un turno a partir de un catálogo, si
      la conversación cabe en su ventana, cuánto costó cada llamada y cuánto cuesta un resultado de
      negocio, y explicar por qué el costo lo calcula el arnés y no el proveedor.
  skeleton:
    id: SK-CH39
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
    contracts_to_be_introduced: [C-049, C-050]
  guiding_questions:
    - id: GQ-CH39-01
      text: |
        Si mañana cambias de proveedor de modelo, ¿qué debería cambiar en el código del agente, y qué
        debería cambiar solo en un registro de datos?
      answered_by: RQ-CH39-01
    - id: GQ-CH39-02
      text: |
        ¿Cómo sabe el arnés que una conversación ya no cabe en el modelo antes de enviarla, y no
        después de que el proveedor la rechace?
      answered_by: RQ-CH39-02
    - id: GQ-CH39-03
      text: |
        Si dos proveedores informan su costo de formas distintas, ¿cómo comparas cuánto costó cada
        llamada? ¿Y cuánto costó, en total, resolver el caso de un cliente?
      answered_by: RQ-CH39-03
    - id: GQ-CH39-04
      text: |
        Si el modelo pide ejecutar tres herramientas en una sola respuesta, ¿debería el arnés quedarse
        solo con la primera?
      answered_by: RQ-CH39-04
  systems_lens:
    iceberg_visible_fact: |
      ModelGateway invoca "el modelo" sin saber cuál es: no conoce su ventana de contexto, su precio
      ni sus capacidades; el costo de cada llamada no se registra, la cache no se puede pedir, y una
      respuesta con varias tool calls se reduce a una (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que P-02 hace reemplazable al proveedor, pero sin un contrato para el
      modelo cada reemplazo se hace a mano, el presupuesto (maxCost) no tiene de dónde sacar el costo y
      INV-E10 exige registrar una "configuración del modelo" que nadie definió (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce ModelDescriptor (C-049) y UsageRecord (C-050), lleva ModelRequest (C-006)
      y ModelResponse (C-007) a v2, y amplía ModelGateway dentro de su owns: selección desde el
      catálogo, cache efectiva, costo calculado y normalización de varias propuestas (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-02 (el modelo es reemplazable: cambiar de modelo es cambiar un dato),
      INV-E10 (cada run registra la versión exacta del modelo), INV-09 (el costo cuenta contra el
      presupuesto) y P-29 (el costo se correlaciona con el resultado de negocio) (ver sección 4).
    reinforcing_loop: |
      Sin costo por llamada, el presupuesto maxCost nunca se alcanza, los runs largos no se detienen,
      y el gasto real solo aparece en la factura del proveedor. Con UsageRecord, cada llamada suma al
      presupuesto y el run se detiene a tiempo.
    balancing_loop: |
      El catálogo es el mecanismo de equilibrio: por mucho que cambien los proveedores, solo se usa un
      modelo registrado, con su ventana y su precio, y lo que no cabe se detecta antes de enviarlo.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que el costo lo calcule ModelGateway con el
      precio del ModelDescriptor (C-049) y lo deje en un UsageRecord (C-050): así el presupuesto, la
      auditoría de versiones y el costo por resultado usan el mismo número.
  recall_questions:
    - id: RQ-CH39-01
      text: |
        ¿Qué campos tiene un ModelDescriptor, qué hace selectModelDescriptor con un modelo fuera del
        catálogo o sin la capacidad pedida, y qué evento emite al seleccionar?
    - id: RQ-CH39-02
      text: |
        ¿Qué compara fitsContextWindow, y qué devuelve effectiveCacheRetention cuando el modelo no tiene
        la capacidad PROMPT_CACHE?
    - id: RQ-CH39-03
      text: |
        ¿Con qué fórmula calcula calculateUsageCost el costo de una llamada, qué suma accumulateUsage al
        uso acumulado del run, y qué exige costForOutcome sobre la moneda?
    - id: RQ-CH39-04
      text: |
        ¿Qué devuelve effectiveToolCallProposals para una respuesta v1 y para una v2, y qué deuda quedó
        registrada para el journal?
  explain_prompts:
    - id: EP-CH39-01
      text: |
        ModelGateway ya "seleccionaba el provider". Explica, como si hablaras con alguien sin contexto
        técnico, por qué seleccionar desde un catálogo de ModelDescriptor sigue siendo esa misma
        decisión, y por qué P-02 se cumple mejor con el modelo como dato.
      target_entity: CMP-003
    - id: EP-CH39-02
      text: |
        Explica por qué UsageRecord guarda la versión del descriptor y el costo calculado, y qué
        perderían el presupuesto y la auditoría si solo guardara los tokens.
      target_entity: C-050
  interleaved_questions:
    - id: IQ-CH39-01
      text: |
        En CH-07, ExecutionController detenía un run con STOP cuando ExecutionUsage superaba algún
        límite de ExecutionBudget, incluido maxCost. ¿De dónde sale ahora costUsed, qué función lo
        actualiza, y por qué ExecutionController no necesita cambiar para usarlo?
      current_chapter_entities: [C-050]
      prior_chapter_entities: [C-012, CMP-007]
      prior_chapter: CH-07
  flashcards:
    - id: FC-CH39-01
      front: |
        ¿Qué es un ModelDescriptor (C-049)?
      back: |
        El modelo como dato del catálogo: modelId, provider, descriptorVersion, contextWindow,
        maxOutputTokens, pricing (por millón de tokens) y capabilities. ModelGateway solo usa modelos
        del catálogo (P-02, INV-E10).
      source_entity: C-049
      chapter_introduced_in: CH-39
      review_stage: DAY_1
    - id: FC-CH39-02
      front: |
        ¿Qué es un UsageRecord (C-050) y a dónde va?
      back: |
        Uso y costo de una llamada: tokens de entrada, salida, lectura y escritura de cache, costo y
        moneda, con la versión del descriptor. Suma a ExecutionUsage (presupuesto, INV-09) y al costo
        por resultado de negocio (P-29).
      source_entity: C-050
      chapter_introduced_in: CH-39
      review_stage: DAY_1
    - id: FC-CH39-03
      front: |
        ¿Qué agrega ModelResponse v2 (C-007) y cómo se leen las propuestas?
      back: |
        proposedToolCalls (todas las propuestas) y usage. proposedToolCall se conserva como la primera.
        effectiveToolCallProposals devuelve la lista, o [proposedToolCall] para una respuesta v1.
      source_entity: C-007
      chapter_introduced_in: CH-39
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH39-01
      recall_question: RQ-CH39-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH39-02
      recall_question: RQ-CH39-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH39-03
      recall_question: RQ-CH39-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH39-04
      recall_question: RQ-CH39-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 39 — El Modelo como Dato: Catálogo, Costo y Cache

> **Regla constitucional (P-02):** el modelo es reemplazable. Reemplazarlo debería ser cambiar un
> dato, no cambiar código.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir qué modelo usa un turno a partir de
un catálogo, si la conversación cabe en su ventana, cuánto costó cada llamada y cuánto cuesta un
resultado de negocio. También podrás explicar por qué el costo lo calcula el arnés y no el proveedor.

**Esqueleto.** Primer capítulo de la versión 0.3. No introduce componentes: amplía `ModelGateway`,
introduce dos contratos y lleva `ModelRequest` y `ModelResponse` a v2.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si mañana cambias de proveedor de modelo, ¿qué debería cambiar en el código del agente, y qué
   debería cambiar solo en un registro de datos?
2. ¿Cómo sabe el arnés que una conversación ya no cabe en el modelo antes de enviarla, y no después de
   que el proveedor la rechace?
3. Si dos proveedores informan su costo de formas distintas, ¿cómo comparas cuánto costó cada llamada?
   ¿Y cuánto costó, en total, resolver el caso de un cliente?
4. Si el modelo pide ejecutar tres herramientas en una sola respuesta, ¿debería el arnés quedarse solo
   con la primera?

## 1. Arquitectura Actual (Current Architecture)

- **`ModelGateway` (CMP-003, CH-03)** selecciona el provider, adapta los mensajes a un `ModelRequest`
  (C-006), invoca al modelo y normaliza la respuesta en un `ModelResponse` (C-007), con a lo sumo una
  `proposedToolCall`.
- **`ExecutionBudget` (C-012)** tiene `maxCost`, y `ExecutionUsage` (CH-07) tiene `costUsed`, pero
  ningún componente produce el costo de una llamada.
- **INV-E10** exige registrar la "configuración del modelo" exacta de cada run, sin decir qué es.
- **`BusinessOutcomeCorrelation` (C-033, CH-22)** une un run con un resultado de negocio, sin costo.
- **CH-32** dejó registrada la deuda D-021: una respuesta del modelo puede proponer varias tool calls,
  y el contrato solo lleva una.

## 2. El Problema (Problem)

El arnés invoca "el modelo" sin saber cuál es:
- **no conoce su ventana de contexto.** Una conversación demasiado larga se descubre cuando el
  proveedor la rechaza, después de pagar el intento;
- **no conoce su precio.** `maxCost` existe en el presupuesto, pero nunca se alcanza, porque nadie
  calcula el costo;
- **no conoce sus capacidades:** si soporta tool calls, varias en paralelo, cache o imágenes;
- **no puede pedir cache**, aunque el modelo la ofrezca y abarate un contexto repetido;
- **no puede registrar** qué versión exacta del modelo usó cada run (INV-E10);
- **se queda con la primera tool call** cuando el modelo propone varias.

Cambiar de proveedor obliga a tocar código en varios lugares, que es exactamente lo que P-02 quería
evitar.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **"Seleccionar el provider" sin un contrato para el modelo** deja la decisión implícita en el código
  del adapter.
- **El costo informado por cada proveedor no es comparable.** Unos cuentan los tokens de cache aparte,
  otros los incluyen, otros no informan costo. Si el presupuesto depende de lo que diga cada uno, la
  misma conversación cuesta distinto según el proveedor.
- **`ModelRequest` no tiene dónde pedir cache**, y `ModelResponse` no tiene dónde llevar el uso.
- **`proposedToolCall` es una sola.** Elegir la primera y descartar las demás cambia lo que el modelo
  pidió sin decírselo.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-02   The model is replaceable.
           Cambiar de modelo es cambiar el modelId pedido; el catálogo trae todo lo demás.
    P-29   Business outcomes are first-class observability.
           costForOutcome une el costo de las llamadas con un BusinessOutcomeCorrelation.

Invariants preserved
    INV-09   Todo AgentRun tiene límites explícitos.
             accumulateUsage alimenta costUsed, que ExecutionController compara con maxCost.
    INV-E10  Every production run records exact versions of … model configuration.
             Cada UsageRecord lleva modelId y descriptorVersion; MODEL_SELECTED lleva el descriptor.

Component ownership changes
    Ninguno nuevo. ModelGateway gana funciones dentro de "selección de provider" y
    "normalización de respuestas".

Contract changes
    Nuevos: C-049 ModelDescriptor, C-050 UsageRecord.
    C-006 ModelRequest v1 → v2 (+ cacheRetention, Optional).
    C-007 ModelResponse v1 → v2 (+ proposedToolCalls, + usage).

Security implications
    Un modelo fuera del catálogo nunca se invoca (ver sección 15).

Observability implications
    Nuevo AgentEventType: MODEL_SELECTED.

Deterministic vs agentic boundary
    Sin cambios: el modelo propone; la selección, el costo y la cache son determinísticos.
```

## 5. Conceptos Nuevos (New Concepts)

- **Catálogo de modelos:** la lista de `ModelDescriptor` que el arnés puede usar. Cada uno dice quién
  lo provee, cuánto texto acepta (ventana de contexto), cuánto puede responder, cuánto cuesta y qué
  sabe hacer. Su `descriptorVersion` cambia cada vez que cambia algo de eso.
- **Capacidad:** algo que el modelo sabe hacer y que un turno puede exigir. Por ejemplo:
  - `TOOL_CALLS` y `PARALLEL_TOOL_CALLS`;
  - `PROMPT_CACHE`;
  - `VISION`;
  - `REASONING`.

  Un turno que necesita tools no puede usar un modelo sin `TOOL_CALLS`.
- **Costo calculado por el arnés:** el proveedor informa tokens; el arnés multiplica por el precio del
  catálogo. Así dos proveedores se comparan con la misma regla.
- **Retención de cache:** cuánto tiempo pide el turno que el proveedor guarde el contexto repetido
  (`NONE`, `SHORT`, `LONG`). Es un pedido: si el modelo no tiene cache, se reduce a `NONE`.
- **Costo por resultado:** la suma del costo de las llamadas de un run, puesta al lado del resultado
  de negocio que ese run logró (P-29).

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `ModelRequest` (C-006, que pasa a v2), `ModelResponse` (C-007, que pasa a v2),
  `AgentMessage` (C-001), `ExecutionBudget` (C-012), `BusinessOutcomeCorrelation` (C-033),
  `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `RunId`, `AgentId`, `Timestamp`.

| Identificador (heredado, sin `C-XXX` propio) | Introducido en | Rol en este capítulo |
|---|---|---|
| `RawToolCallProposal` | CH-03 §6 | una propuesta de tool call del modelo |
| `ExecutionUsage` | CH-07 §6 | el uso acumulado del run, con `costUsed` |
| `AgentEventType` | CH-00 | se agrega `MODEL_SELECTED` |
| `ErrorCategory` | CH-00 | reutiliza `MODEL` y `VALIDATION` |

### `ModelCapability` y `ModelPricing` — partes del descriptor (embebidos)

```pseudocode
ENUM ModelCapability
    TOOL_CALLS
    PARALLEL_TOOL_CALLS
    PROMPT_CACHE
    VISION
    REASONING
END
```

```pseudocode
STRUCT ModelPricing
    inputPerMillion: Number
    outputPerMillion: Number
    cacheReadPerMillion: Number
    cacheWritePerMillion: Number
    currency: Text
END
```

### `ModelDescriptor` — el modelo como dato (C-049)

```pseudocode
STRUCT ModelDescriptor
    modelId: Text
    provider: Text
    descriptorVersion: Text
    contextWindow: Integer
    maxOutputTokens: Integer
    pricing: ModelPricing
    capabilities: List<ModelCapability>
END
```

`provider` es una referencia al adapter que ModelGateway usa. El nombre de un proveedor concreto es un
dato de configuración, nunca una dependencia del núcleo (P-27).

### `UsageRecord` — uso y costo de una llamada (C-050)

```pseudocode
STRUCT UsageRecord
    modelId: Text
    descriptorVersion: Text
    inputTokens: Integer
    outputTokens: Integer
    cacheReadTokens: Integer
    cacheWriteTokens: Integer
    cost: Number
    currency: Text
    recordedAt: Timestamp
END
```

`inputTokens` cuenta solo los tokens de entrada que **no** salieron de cache. Los leídos de cache van
en `cacheReadTokens`, que tienen su propio precio.

### `CacheRetention` y `ModelRequest` — versión 2 (C-006)

```pseudocode
ENUM CacheRetention
    NONE
    SHORT
    LONG
END
```

```pseudocode
STRUCT ModelRequest
    messages: List<AgentMessage>
    budget: ExecutionBudget
    cacheRetention: Optional<CacheRetention>
    requestedAt: Timestamp
END
```

### `ModelResponse` — versión 2 (C-007)

```pseudocode
STRUCT ModelResponse
    finished: Boolean
    content: Optional<Value>
    proposedToolCall: Optional<RawToolCallProposal>
    proposedToolCalls: List<RawToolCallProposal>
    usage: Optional<UsageRecord>
    producedAt: Timestamp
END
```

**Compatibilidad hacia atrás:**
- `cacheRetention = NULL` es una petición sin cache, como en v1;
- en una respuesta v1, `proposedToolCalls` está vacía y `usage` es `NULL`;
- `proposedToolCall` se conserva y es la primera propuesta de la lista.

Ningún pseudocódigo anterior cambia de significado.

### `OutcomeCost` — el costo de un resultado de negocio (embebido)

```pseudocode
STRUCT OutcomeCost
    runId: RunId
    measuredOutcome: Text
    totalCost: Number
    currency: Text
    callCount: Integer
END
```

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-049
Name:                   ModelDescriptor
Version:                v1
Introduced In:          CH-39
Used By:                [CMP-003]
Constitutional Impact:  [P-02, INV-E10]
```

```text
ID:                     C-050
Name:                   UsageRecord
Version:                v1
Introduced In:          CH-39
Used By:                [CMP-003, CMP-020]
Constitutional Impact:  [P-29, INV-09, INV-E10]
```

```text
C-006 ModelRequest   v1 → v2   Modified By: [CH-39]   + cacheRetention: Optional<CacheRetention>
C-007 ModelResponse  v1 → v2   Modified By: [CH-39]   + proposedToolCalls: List<RawToolCallProposal>
                                                       + usage: Optional<UsageRecord>
```

`ModelCapability`, `ModelPricing`, `CacheRetention` y `OutcomeCost` quedan embebidos.
`EvaluationHarness` (CMP-020, CH-22) aparece en `used_by` de `UsageRecord`, porque el costo por
resultado se calcula junto al `BusinessOutcomeCorrelation` que ese componente produce.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce componentes.** `ModelGateway` gana funciones dentro de su `owns`
literal:

```text
ModelGateway (CMP-003)
    owns: "selección de provider", "adaptación de mensajes", "invocación del modelo",
          "streaming", "normalización de respuestas"
    nuevas, dentro de "selección de provider":
        hasCapability, selectModelDescriptor, fitsContextWindow, effectiveCacheRetention
    nuevas, dentro de "normalización de respuestas":
        calculateUsageCost, attachUsage, effectiveToolCallProposals
    no posee:
        decidir si el run puede seguir con ese costo (ExecutionController, CH-07)
        decidir cuántas de las propuestas se ejecutan ni en qué orden (la integración y
        PolicyEngine, propuesta por propuesta)
        medir el resultado de negocio (EvaluationHarness, CH-22)
```

`accumulateUsage` y `costForOutcome` son funciones de integración: suman datos que ya producen
componentes registrados, y no deciden nada nuevo.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
Antes de invocar:  selectModelDescriptor (catálogo, capacidades exigidas) → fitsContextWindow
                   → effectiveCacheRetention → ModelRequest v2
Al recibir:        tokens del proveedor → calculateUsageCost → attachUsage → ModelResponse v2
                   → effectiveToolCallProposals (todas las propuestas, para la integración)
Después:           accumulateUsage → ExecutionUsage → evaluateExecutionContinuation (CH-07, maxCost)
Al cerrar el run:  costForOutcome(BusinessOutcomeCorrelation (CH-22), UsageRecord del run)
```

**Las varias propuestas en el turno durable.** `effectiveToolCallProposals` entrega todas, pero el
journal (`StepRecord`, C-042) registra una tool call por paso. Registrar las demás sin volver a llamar
al modelo es la deuda D-044, con destino en la integración de la versión 0.3 (CH-49). Hasta entonces,
la integración ejecuta las propuestas de una respuesta en pasos sucesivos.

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Catálogo (datos) → ModelGateway (seleccionar, ajustar cache) → proveedor (adapter)
proveedor → ModelGateway (costo, propuestas) → ExecutionController (presupuesto) → EvaluationHarness (resultado)
```

**Vista 2 — Sequence: una llamada con costo**

```text
Integración
   │ selectModelDescriptor(catálogo, "modelo-a", [TOOL_CALLS])  → ModelDescriptor + MODEL_SELECTED
   │ fitsContextWindow(descriptor, 180 000, 4 000)              → TRUE
   │ effectiveCacheRetention(request SHORT, descriptor)         → SHORT
   │ invokeModelForTurn (CH-03)                                 → ModelResponse
   │ calculateUsageCost(descriptor, 12 000, 800, 150 000, 0)    → UsageRecord(cost)
   │ attachUsage(response, usage)                               → ModelResponse v2
   │ accumulateUsage(usage del run, record)                     → ExecutionUsage.costUsed
   │ evaluateExecutionContinuation (CH-07)                      → CONTINUE | STOP (maxCost)
```

**Vista 2b — Sequence: un modelo que no sirve para el turno**

```text
selectModelDescriptor(catálogo, "modelo-b", [TOOL_CALLS])
   → MODEL_LACKS_CAPABILITY (el modelo existe, pero no soporta tool calls)
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

### ModelGateway: seleccionar desde el catálogo

```pseudocode
FUNCTION hasCapability(
    descriptor: ModelDescriptor,
    capability: ModelCapability
) -> Boolean

    FOR EACH available IN descriptor.capabilities
        IF available == capability
            RETURN TRUE
        END
    END

    RETURN FALSE
END
```

```pseudocode
FUNCTION selectModelDescriptor(
    catalog: List<ModelDescriptor>,
    modelId: Text,
    required: List<ModelCapability>,
    execution: ExecutionContext,
    agentId: AgentId
) -> ModelDescriptor

    FOR EACH descriptor IN catalog
        IF descriptor.modelId == modelId
            FOR EACH capability IN required
                IF NOT hasCapability(descriptor, capability)
                    THROW HarnessError(
                        category = MODEL,
                        code = "MODEL_LACKS_CAPABILITY",
                        message = "El modelo está en el catálogo, pero no tiene una capacidad que el turno exige",
                        recoverable = FALSE,
                        retryable = FALSE,
                        metadata = {}
                    )
                END
            END

            EMIT AgentEvent(
                eventId = newEventId(),
                eventType = MODEL_SELECTED,
                timestamp = now(),
                runId = execution.runId,
                sessionId = execution.sessionId,
                agentId = agentId,
                traceId = execution.traceId,
                payload = descriptor
            )

            RETURN descriptor
        END
    END

    THROW HarnessError(
        category = MODEL,
        code = "MODEL_NOT_IN_CATALOG",
        message = "El modelo pedido no está en el catálogo; el arnés nunca invoca un modelo que no conoce",
        recoverable = FALSE,
        retryable = FALSE,
        metadata = {}
    )
END
```

```pseudocode
FUNCTION fitsContextWindow(
    descriptor: ModelDescriptor,
    estimatedInputTokens: Integer,
    requestedOutputTokens: Integer
) -> Boolean

    RETURN requestedOutputTokens <= descriptor.maxOutputTokens
        AND estimatedInputTokens + requestedOutputTokens <= descriptor.contextWindow
END
```

```pseudocode
FUNCTION effectiveCacheRetention(
    request: ModelRequest,
    descriptor: ModelDescriptor
) -> CacheRetention

    IF request.cacheRetention == NULL OR NOT hasCapability(descriptor, PROMPT_CACHE)
        RETURN NONE
    END

    RETURN request.cacheRetention
END
```

### ModelGateway: costo y normalización

```pseudocode
FUNCTION calculateUsageCost(
    descriptor: ModelDescriptor,
    inputTokens: Integer,
    outputTokens: Integer,
    cacheReadTokens: Integer,
    cacheWriteTokens: Integer
) -> UsageRecord

    price: ModelPricing = descriptor.pricing

    cost: Number = (
        inputTokens * price.inputPerMillion
        + outputTokens * price.outputPerMillion
        + cacheReadTokens * price.cacheReadPerMillion
        + cacheWriteTokens * price.cacheWritePerMillion
    ) / 1000000

    RETURN UsageRecord(
        modelId = descriptor.modelId,
        descriptorVersion = descriptor.descriptorVersion,
        inputTokens = inputTokens,
        outputTokens = outputTokens,
        cacheReadTokens = cacheReadTokens,
        cacheWriteTokens = cacheWriteTokens,
        cost = cost,
        currency = price.currency,
        recordedAt = now()
    )
END
```

```pseudocode
FUNCTION attachUsage(
    response: ModelResponse,
    usage: UsageRecord
) -> ModelResponse

    RETURN ModelResponse(
        finished = response.finished,
        content = response.content,
        proposedToolCall = response.proposedToolCall,
        proposedToolCalls = response.proposedToolCalls,
        usage = usage,
        producedAt = response.producedAt
    )
END
```

```pseudocode
FUNCTION effectiveToolCallProposals(
    response: ModelResponse
) -> List<RawToolCallProposal>

    IF length(response.proposedToolCalls) > 0
        RETURN response.proposedToolCalls
    END

    IF response.proposedToolCall != NULL
        RETURN [response.proposedToolCall]
    END

    RETURN []
END
```

### Integración: presupuesto y costo por resultado

```pseudocode
FUNCTION accumulateUsage(
    usage: ExecutionUsage,
    record: UsageRecord
) -> ExecutionUsage

    RETURN ExecutionUsage(
        toolCallsUsed = usage.toolCallsUsed,
        inputTokensUsed = usage.inputTokensUsed + record.inputTokens + record.cacheReadTokens,
        outputTokensUsed = usage.outputTokensUsed + record.outputTokens,
        costUsed = usage.costUsed + record.cost,
        runtimeMsElapsed = usage.runtimeMsElapsed,
        concurrentToolsInFlight = usage.concurrentToolsInFlight
    )
END
```

```pseudocode
FUNCTION costForOutcome(
    correlation: BusinessOutcomeCorrelation,
    records: List<UsageRecord>,
    currency: Text
) -> OutcomeCost

    total: Number = 0

    FOR EACH record IN records
        IF record.currency != currency
            THROW HarnessError(
                category = VALIDATION,
                code = "MIXED_CURRENCY",
                message = "El costo de un resultado solo suma llamadas de una misma moneda; el arnés no convierte monedas",
                recoverable = FALSE,
                retryable = FALSE,
                metadata = {}
            )
        END
        total = total + record.cost
    END

    RETURN OutcomeCost(
        runId = correlation.runId,
        measuredOutcome = correlation.measuredOutcome,
        totalCost = total,
        currency = currency,
        callCount = length(records)
    )
END
```

`newEventId`, `now` y `length` son utilidades primitivas. Los tokens de cache leídos cuentan contra
`maxInputTokens`, porque ocupan la ventana igual que los demás, aunque su precio sea menor.

Nótese lo que estas funciones **no** hacen:
- ninguna decide si el run puede seguir con ese costo: lo decide `ExecutionController`;
- ninguna confía en el costo que informa el proveedor: el costo sale del catálogo;
- ninguna descarta propuestas: `effectiveToolCallProposals` las entrega todas.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no cambia `AgentRunStatus`. La selección de un modelo:

```text
modelId fuera del catálogo                 → MODEL_NOT_IN_CATALOG
en el catálogo, sin una capacidad exigida  → MODEL_LACKS_CAPABILITY
en el catálogo, con las capacidades        → ModelDescriptor + MODEL_SELECTED
```

Y la cache efectiva:

```text
cacheRetention NULL                     → NONE
modelo sin PROMPT_CACHE                 → NONE
modelo con PROMPT_CACHE                 → la pedida (SHORT | LONG | NONE)
```

## 13. Semántica de Fallos (Failure Semantics)

Códigos nuevos de `HarnessError`, con `ErrorCategory` ya existentes:

```text
MODEL       MODEL_NOT_IN_CATALOG     recoverable: FALSE, retryable: FALSE
MODEL       MODEL_LACKS_CAPABILITY   recoverable: FALSE, retryable: FALSE
VALIDATION  MIXED_CURRENCY           recoverable: FALSE, retryable: FALSE
```

`fitsContextWindow = FALSE` no es un error: es la señal para compactar (CH-29) antes de invocar.

## 14. Eventos Producidos (Events Produced)

```text
MODEL_SELECTED — ModelGateway eligió un modelo del catálogo (payload: ModelDescriptor, con su versión)
```

El uso de cada llamada viaja en el `ModelResponse` v2 (`usage`) y en el `ExecutionUsage`, no en un
evento propio.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Ningún modelo desconocido.** Un `modelId` que no está en el catálogo nunca se invoca, aunque un
  adapter sepa llamarlo. Agregar un modelo es una decisión registrada, no un cambio de código.
- **El costo no lo decide el proveedor.** Un proveedor que informe un costo menor al real no puede
  hacer que el run supere `maxCost` sin que el arnés lo note.
- **La versión exacta queda registrada** (INV-E10). Si el precio o la ventana de un modelo cambian,
  cambia `descriptorVersion`, y cada `UsageRecord` dice con qué versión se calculó.
- **El catálogo no contiene credenciales.** `provider` es una referencia al adapter; la credencial del
  proveedor la resuelve `CredentialBroker` (INV-E08).
- **Las propuestas no se pierden en silencio.** Si el modelo propuso tres tool calls, la integración
  ve las tres, y cada una pasa por `PolicyEngine`.

## 16. Tests (Tests)

```text
TEST ModelOutsideTheCatalogIsNeverInvoked
TEST ModelWithoutARequiredCapabilityIsRejected
TEST SelectingAModelEmitsModelSelectedWithItsVersion
TEST ConversationThatDoesNotFitIsDetectedBeforeInvoking
TEST CacheIsReducedToNoneWhenTheModelHasNoPromptCache
TEST CostIsComputedFromTheCatalogPriceNotFromTheProvider
TEST CacheReadTokensAreChargedAtTheirOwnPrice
TEST UsageAccumulatesIntoCostUsed
TEST MaxCostStopsTheRunThroughExecutionController
TEST OutcomeCostRejectsMixedCurrencies
TEST EffectiveProposalsReturnsTheWholeList
TEST EffectiveProposalsWrapsAV1SingleProposal
TEST V1ResponseHasNoUsageAndAnEmptyProposalList
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.3 en curso, después de CH-39) — 26 componentes, 50 contratos, 40 capítulos

Components — 26, sin cambios
 └── CMP-003 ModelGateway   (+ catálogo, cache efectiva, costo, propuestas)

Contracts — 50
 ├── C-006 ModelRequest v2   (CH-03 → modificado en CH-39: cacheRetention)
 ├── C-007 ModelResponse v2  (CH-03 → modificado en CH-39: proposedToolCalls, usage)
 ├── C-049 ModelDescriptor   (CH-39, nuevo)
 └── C-050 UsageRecord       (CH-39, nuevo)

Deuda: D-021 resuelta (contrato); D-044 nueva (journal de varias propuestas) → CH-49.
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Los adapters de cada proveedor:** el libro enseña la costura (P-02), no la lista de proveedores.
- **Cambiar de modelo a mitad de un run.** El modelo puede elegirse turno a turno con
  `selectModelDescriptor`, pero registrar ese cambio en la sesión como una entrada propia es parte de
  la evolución del runtime (CH-45, `RuntimeVersionSnapshot`).
- **Registrar varias propuestas en el journal** sin volver a llamar al modelo: D-044, con destino
  CH-49.
- **Conversión de monedas:** fuera de alcance; el costo por resultado exige una sola moneda.
- **Presupuestos que se heredan entre runs:** CH-43.

## 19. Siguiente Incremento (Next Increment)

Ahora el modelo es un dato: se elige de un catálogo, se sabe cuánto cuesta y se registra su versión.
Pero el arnés todavía no tiene una forma segura de que **otros** agreguen comportamiento: un hook
que audite, una extensión que agregue una tool, un plugin del equipo. Hoy, agregar algo así exige
tocar el núcleo, o abre una puerta para saltarse la constitución.

El siguiente capítulo introduce **ExtensionHost**:
- registro de extensiones con su nivel de confianza;
- puntos de hook declarados;
- la regla de que ningún hook puede devolver una decisión de autorización (INV-E24).

Será CH-40 ("Extensiones que No Pueden Saltarse la Constitución"). `next_chapter` queda en `null`
porque CH-40 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): ModelGateway invoca un modelo sin conocer su ventana, precio ni
   capacidades; el costo no se registra y las propuestas se reducen a una.
2. **Patrones** (= §3): sin contrato para el modelo, cada reemplazo es código, el presupuesto no tiene
   costo y INV-E10 no dice qué registrar.
3. **Estructuras** (= §8): `ModelDescriptor` (C-049), `UsageRecord` (C-050), `ModelRequest` y
   `ModelResponse` v2, y funciones nuevas en `ModelGateway`.
4. **Modelos mentales** (= §4): P-02, INV-E10, INV-09 y P-29.

**Bucles de retroalimentación**

- **Refuerzo:** sin costo, `maxCost` nunca detiene un run. Con `UsageRecord`, cada llamada suma.
- **Equilibrio:** el catálogo. Solo se usa un modelo registrado, y lo que no cabe se detecta antes.

**Punto de apalancamiento**

La decisión con mayor efecto es que el costo lo calcule `ModelGateway` con el precio del
`ModelDescriptor` (C-049) y lo deje en un `UsageRecord` (C-050), para que el presupuesto, la
auditoría de versiones y el costo por resultado usen el mismo número.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué campos tiene un `ModelDescriptor`, qué hace `selectModelDescriptor` con un modelo fuera del
   catálogo o sin la capacidad pedida, y qué evento emite al seleccionar? *(pregunta guía 1)*
2. ¿Qué compara `fitsContextWindow`, y qué devuelve `effectiveCacheRetention` cuando el modelo no
   tiene la capacidad `PROMPT_CACHE`? *(pregunta guía 2)*
3. ¿Con qué fórmula calcula `calculateUsageCost` el costo de una llamada, qué suma `accumulateUsage`
   al uso acumulado del run, y qué exige `costForOutcome` sobre la moneda? *(pregunta guía 3)*
4. ¿Qué devuelve `effectiveToolCallProposals` para una respuesta v1 y para una v2, y qué deuda quedó
   registrada para el journal? *(pregunta guía 4)*

### Explicar

1. `ModelGateway` ya "seleccionaba el provider". Explica por qué seleccionar desde un catálogo de
   `ModelDescriptor` sigue siendo esa misma decisión, y por qué P-02 se cumple mejor con el modelo
   como dato.
2. Explica por qué `UsageRecord` guarda la versión del descriptor y el costo calculado, y qué
   perderían el presupuesto y la auditoría si solo guardara los tokens.

### Conectar

1. En CH-07, `ExecutionController` detenía un run con `STOP` cuando `ExecutionUsage` superaba algún
   límite de `ExecutionBudget`, incluido `maxCost`. ¿De dónde sale ahora `costUsed`, qué función lo
   actualiza, y por qué `ExecutionController` no necesita cambiar para usarlo?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
