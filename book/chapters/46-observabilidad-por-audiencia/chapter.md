---
id: CH-46
title: "Observabilidad Acotada por Audiencia"
starting_version: "0.2.1"
ending_version: "0.3"
introduces_components: []
introduces_contracts: [C-061, C-062, C-063]
modifies_contracts: []
constitutional_articles: [P-04, P-22, P-25, P-37, INV-E11, INV-E23]
previous_chapter: CH-45
next_chapter: CH-47
retrieval_set:
  expected_outcome:
    id: EO-CH46
    text: |
      Al terminar este capítulo podrás decidir qué contenido de una sesión puede llegar a cada destino
      de telemetría y qué datos pueden entrar al contexto según quién ve la sesión, y explicar en qué se
      diferencian un evento, una entrada de auditoría y un span.
  skeleton:
    id: SK-CH46
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
    contracts_to_be_introduced: [C-061, C-062, C-063]
  guiding_questions:
    - id: GQ-CH46-01
      text: |
        Si un agente responde en un canal que ve toda la empresa, ¿qué datos debería poder usar para
        responder? ¿Los mismos que en una conversación privada?
      answered_by: RQ-CH46-01
    - id: GQ-CH46-02
      text: |
        Si la conversación es privada, ¿debería el equipo que opera el sistema poder leer en las trazas
        lo que el usuario escribió?
      answered_by: RQ-CH46-02
    - id: GQ-CH46-03
      text: |
        Si el sistema no sabe si una conversación es pública o privada, ¿qué debería suponer?
      answered_by: RQ-CH46-03
    - id: GQ-CH46-04
      text: |
        ¿En qué se diferencian un evento, una entrada de auditoría y una traza? ¿Deberían recortarse
        las tres por igual?
      answered_by: RQ-CH46-04
  systems_lens:
    iceberg_visible_fact: |
      Toda la telemetría se captura igual para todas las sesiones: un destino de trazas recibe los
      prompts de una conversación privada, y una sesión en un canal público puede poner en el contexto
      datos confidenciales que toda su audiencia verá en la respuesta (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que la clasificación del dato (CH-20) y su techo en el contexto (CH-42)
      no conocen a quién ve la sesión: el mismo dato es apropiado en una conversación privada e
      inapropiado en un canal público, y nada distingue los dos casos (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce SessionAudience (C-061), TraceCapturePolicy (C-062) y TelemetrySpan
      (C-063), y le da a DataGovernanceEngine los techos por audiencia y a EventBus la distribución de
      spans ya recortados (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-37 (la captura está acotada por la audiencia), INV-E23 (ningún destino
      captura por encima del techo), P-25 (auditoría y telemetría son distintas) y P-22 (la gobernanza
      se hace cumplir fuera del modelo) (ver sección 4).
    reinforcing_loop: |
      Si la telemetría captura todo, cada destino nuevo es una copia más de contenido privado; cuantas
      más copias, más difícil retirarlas, y más destinos se suman porque "ya está todo ahí".
    balancing_loop: |
      El techo de captura es el equilibrio: agregar un destino no agrega contenido, porque cada destino
      recibe a lo sumo lo que el techo de la sesión permite.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que TraceCapturePolicy (C-062) se derive de la
      audiencia de la sesión y se aplique antes de distribuir: ningún destino recibe lo que el techo
      excluye, así que ninguno puede restaurarlo.
  recall_questions:
    - id: RQ-CH46-01
      text: |
        ¿Qué techo de contexto devuelve contextCeilingForAudience para una sesión PRIVATE y para una
        PUBLIC o UNKNOWN, y a qué función de CH-42 se le pasa?
    - id: RQ-CH46-02
      text: |
        ¿Qué hace governSpanForDestination con un span por encima del techo, y con uno dentro del techo
        cuyo cuerpo la política no permite capturar?
    - id: RQ-CH46-03
      text: |
        ¿Qué techo de captura usa captureCeilingFor para una sesión UNKNOWN, qué pasa si no hay política,
        y qué cambios de audiencia permite reclassifySessionAudience?
    - id: RQ-CH46-04
      text: |
        ¿Qué hace cada una de las tres señales (evento, auditoría, span), y por qué el techo de captura se
        aplica a los spans y no a la auditoría?
  explain_prompts:
    - id: EP-CH46-01
      text: |
        DataGovernanceEngine ya clasificaba datos. Explica, como si hablaras con alguien sin contexto
        técnico, por qué también le pertenece decidir los techos por audiencia, y qué le queda a EventBus.
      target_entity: CMP-018
    - id: EP-CH46-02
      text: |
        Explica por qué el techo de captura se aplica antes de distribuir el span y no en cada destino, y
        qué no se podría garantizar si cada destino recortara por su cuenta.
      target_entity: C-062
  interleaved_questions:
    - id: IQ-CH46-01
      text: |
        En CH-42, selectRetrievedCandidates recibía un techo de clasificación fijado por la política.
        ¿Qué techo recibe ahora en una sesión PUBLIC, qué función lo calcula, y por qué ese cálculo nunca
        puede subir el techo de la política?
      current_chapter_entities: [C-061]
      prior_chapter_entities: [C-056, CMP-004]
      prior_chapter: CH-42
  flashcards:
    - id: FC-CH46-01
      front: |
        ¿Qué es SessionAudience (C-061)?
      back: |
        Quién puede ver una sesión: PUBLIC, PRIVATE o UNKNOWN. Se asigna al crearla; dentro de la sesión
        solo se vuelve más restrictiva.
      source_entity: C-061
      chapter_introduced_in: CH-46
      review_stage: DAY_1
    - id: FC-CH46-02
      front: |
        ¿Qué es TraceCapturePolicy (C-062) y qué pasa si falta?
      back: |
        El techo de captura de una audiencia: clasificación máxima y si se capturan cuerpos. Si falta, el
        techo más restrictivo: PUBLIC y sin cuerpos.
      source_entity: C-062
      chapter_introduced_in: CH-46
      review_stage: DAY_1
    - id: FC-CH46-03
      front: |
        ¿Qué es TelemetrySpan (C-063) y en qué se diferencia de un evento y de una entrada de auditoría?
      back: |
        Un tramo de diagnóstico ("diagnostic data, not business state"). El evento observa, la auditoría
        prueba, el span diagnostica; el techo de captura recorta solo el span.
      source_entity: C-063
      chapter_introduced_in: CH-46
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH46-01
      recall_question: RQ-CH46-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH46-02
      recall_question: RQ-CH46-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH46-03
      recall_question: RQ-CH46-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH46-04
      recall_question: RQ-CH46-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 46 — Observabilidad Acotada por Audiencia

> **Regla constitucional (INV-E23):** ningún destino de trazas puede capturar contenido por encima del
> techo de captura de la sesión.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir qué contenido de una sesión puede
llegar a cada destino de telemetría, y qué datos pueden entrar al contexto según quién ve la sesión.
También podrás explicar en qué se diferencian un evento, una entrada de auditoría y un span.

**Esqueleto.** Octavo capítulo de la versión 0.3. No introduce componentes: agrega `SessionAudience`,
`TraceCapturePolicy` y `TelemetrySpan`, y amplía `DataGovernanceEngine` y `EventBus`.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si un agente responde en un canal que ve toda la empresa, ¿qué datos debería poder usar para
   responder? ¿Los mismos que en una conversación privada?
2. Si la conversación es privada, ¿debería el equipo que opera el sistema poder leer en las trazas lo
   que el usuario escribió?
3. Si el sistema no sabe si una conversación es pública o privada, ¿qué debería suponer?
4. ¿En qué se diferencian un evento, una entrada de auditoría y una traza? ¿Deberían recortarse las
   tres por igual?

## 1. Arquitectura Actual (Current Architecture)

- **`EventBus` (CMP-009, CH-09)** distribuye cada `AgentEvent` a las suscripciones activas. Los eventos
  observan lo que pasa (P-04).
- **`AuditLedger` (CMP-017, CH-19)** registra evidencia inmutable, separada de la telemetría (P-25),
  con su propia clasificación y retención (CH-38).
- **`DataGovernanceEngine` (CMP-018, CH-20)** clasifica datos (`DataClassificationLevel`: PUBLIC,
  INTERNAL, CONFIDENTIAL, RESTRICTED). En CH-42 ganó `moreRestrictive` y `classifyDerivedData`.
- **`ContextEngine` (CH-42)** filtra los candidatos recuperados con un techo de clasificación que fija
  la política (`selectRetrievedCandidates`).
- **No hay trazas como dato propio:** CH-35 dejó la telemetría del proxy para este capítulo, y CH-42,
  los techos por audiencia.

## 2. El Problema (Problem)

Un agente de recursos humanos atiende dos sesiones a la vez: una conversación privada con un empleado
sobre su salario, y un hilo en un canal que ve toda la empresa, donde alguien pregunta por la política
de vacaciones. Hoy:
- **el destino de trazas recibe todo:** los prompts de la conversación privada, con el salario,
  quedan en una herramienta que lee todo el equipo de operaciones;
- **el hilo público puede recuperar datos confidenciales:** el techo de contexto es el de la política,
  igual para las dos sesiones, y la respuesta la lee toda la empresa;
- **agregar un destino de trazas** (otro proveedor, un entorno de pruebas) es copiar todo una vez más;
- **cuando el canal de una sesión no dice si es público o privado,** nada decide qué suponer.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **La clasificación es del dato, no de la sesión.** El mismo salario es apropiado en la conversación
  privada e inapropiado en el canal público.
- **El techo de contexto no conoce la audiencia:** lo fija la política, que es la misma para las dos
  sesiones.
- **Las trazas no tienen techo:** lo que no está acotado antes de distribuir ya se copió; un destino
  no puede "des-capturar".
- **Mezclar las tres señales** haría que recortar trazas recorte también la auditoría, y P-25 exige
  que sean distintas.
- **No hace falta un componente nuevo:** clasificar y fijar techos es de `DataGovernanceEngine` (P-22);
  distribuir es de `EventBus` (EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-04   Toda acción produce eventos observables: los eventos no se recortan por audiencia.
    P-22   La gobernanza se hace cumplir fuera del modelo: los techos los calcula DataGovernanceEngine.
    P-25   Audit evidence is distinct from operational telemetry.
           El techo de captura recorta spans; la auditoría sigue su propia clasificación.
    P-37   (Amendment v1.2) Observability capture is bounded by audience.
           SessionAudience al crear la sesión; TraceCapturePolicy deriva el techo.

Invariants preserved
    INV-E11  La política del dato lo acompaña: la clasificación del span viaja con él.
    INV-E23  (Amendment v1.2) No trace destination may capture content above the session's capture
             ceiling. governSpanForDestination recorta antes de distribuir.

Component ownership changes
    Ninguno nuevo. DataGovernanceEngine gana los techos por audiencia; EventBus, el fan-out de spans.

Contract changes
    Nuevos: C-061 SessionAudience, C-062 TraceCapturePolicy, C-063 TelemetrySpan.

Observability implications
    Nuevo AgentEventType: SESSION_AUDIENCE_CLASSIFIED.
```

## 5. Conceptos Nuevos (New Concepts)

- **Audiencia de la sesión:** quién puede ver lo que pasa en ella. `PUBLIC` (un canal abierto),
  `PRIVATE` (una conversación con una persona o un grupo cerrado) o `UNKNOWN` (el canal no lo dice).
- **Techo de captura:** la clasificación máxima de contenido que puede llegar a un destino de
  telemetría desde una sesión, y si se capturan cuerpos (prompts, salidas, argumentos).
- **Techo de contexto por audiencia:** lo que el agente responde lo ve su audiencia, así que una
  sesión pública baja el techo de lo que puede entrar al contexto.
- **La audiencia acota en dos direcciones:**
  - PUBLIC baja el techo del **contexto** (lo que se responde);
  - PRIVATE baja el techo de la **telemetría** (lo que ven los operadores);
  - UNKNOWN baja los dos.
- **Recortar antes de distribuir:** cada destino recibe un span ya recortado. Lo que el techo excluyó
  nunca le llegó, así que no puede restaurarlo.
- **Tres señales, tres propósitos:**

| Señal | Propósito | Quién la consume | ¿La recorta la audiencia? |
|---|---|---|---|
| `AgentEvent` | observa: qué pasó | UI, integraciones, suscriptores | no: su payload lo decide cada productor |
| Entrada de auditoría | prueba: qué se decidió y con qué versión | auditoría, cumplimiento | no: tiene su propia clasificación y retención (CH-19, CH-38) |
| `TelemetrySpan` | diagnostica: cuánto tardó, dónde falló | operadores, destinos de trazas | sí: el techo de captura |

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `SessionId`, `SpanId`, `TraceId`, `AgentId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `DataClassificationLevel` | CH-20 §6: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED |
| `SpanId` | id de un span; nuevo primitivo |
| `AgentEventType` | se agrega `SESSION_AUDIENCE_CLASSIFIED` |
| `ErrorCategory` | reutiliza `VALIDATION` |

### `AudienceKind` (embebido)

```pseudocode
ENUM AudienceKind
    PUBLIC
    PRIVATE
    UNKNOWN
END
```

### `SessionAudience` — quién ve la sesión (C-061)

```pseudocode
STRUCT SessionAudience
    sessionId: SessionId
    kind: AudienceKind
    decidedBy: Text
    decidedAt: Timestamp
END
```

`decidedBy` dice de dónde salió la audiencia: el adaptador del canal (CH-34) o una regla del
despliegue. `SessionState` no cambia: la audiencia es un registro de gobierno, como un
`DataGovernanceLabel`.

### `TraceCapturePolicy` — el techo de una audiencia (C-062)

```pseudocode
STRUCT TraceCapturePolicy
    audience: AudienceKind
    ceiling: DataClassificationLevel
    captureBodies: Boolean
END
```

### `TelemetrySpan` — un tramo de diagnóstico (C-063)

```pseudocode
STRUCT TelemetrySpan
    spanId: SpanId
    traceId: TraceId
    parentSpanId: Optional<SpanId>
    sessionId: SessionId
    name: Text
    startedAt: Timestamp
    endedAt: Optional<Timestamp>
    attributes: Map<Text, Value>
    body: Optional<Value>
    classification: DataClassificationLevel
    redacted: Boolean
END
```

- `attributes` son datos de diagnóstico (duración, códigos, ids); `body` es el contenido (prompt,
  salida, argumentos).
- `classification` es la del contenido más sensible del span, asignada por quien lo produce.
- `redacted` dice si el span llegó recortado.

### `TraceDestination` y `SpanDelivery` (embebidos)

```pseudocode
STRUCT TraceDestination
    destinationRef: Text
    ceiling: DataClassificationLevel
END
```

```pseudocode
STRUCT SpanDelivery
    destinationRef: Text
    span: TelemetrySpan
END
```

Un destino puede declarar un techo propio, más bajo que el de la sesión; nunca uno que lo suba.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-061
Name:                   SessionAudience
Version:                v1
Introduced In:          CH-46
Used By:                [CMP-018]
Constitutional Impact:  [P-37, INV-E23]
```

```text
ID:                     C-062
Name:                   TraceCapturePolicy
Version:                v1
Introduced In:          CH-46
Used By:                [CMP-018, CMP-009]
Constitutional Impact:  [P-37, INV-E23]
```

```text
ID:                     C-063
Name:                   TelemetrySpan
Version:                v1
Introduced In:          CH-46
Used By:                [CMP-009, CMP-018]
Constitutional Impact:  [P-04, P-25, INV-E23]
```

`AudienceKind`, `TraceDestination` y `SpanDelivery` quedan embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce componentes.** Dos componentes ganan funciones dentro de su `owns`
literal:

```text
DataGovernanceEngine (CMP-018)
    owns: clasificar cualquier dato fuera del razonamiento del modelo (P-22); la política del dato lo
          acompaña (INV-E11); fail-closed hacia lo más restrictivo
    nuevas:
        classifySessionAudience, reclassifySessionAudience, lowerCeiling, findCapturePolicy,
        captureCeilingFor, contextCeilingForAudience, governSpanForDestination
    no posee:
        fijar el techo de contexto de la política (PolicyEngine, CH-05; este capítulo solo lo baja)
        seleccionar qué entra al contexto (ContextEngine, CH-42)
        la clasificación y retención de la auditoría (AuditLedger, CH-19, CH-38)

EventBus (CMP-009)
    owns: distribuir (fan-out) a las suscripciones activas
    nueva:
        fanOutSpan
    no posee:
        decidir qué contenido puede capturarse (DataGovernanceEngine)
        exportar al formato de cada destino (el adaptador del destino)
```

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
Crear sesión:   adaptador del canal → classifySessionAudience → SessionAudience
                (UNKNOWN si el canal no lo dice)          → SESSION_AUDIENCE_CLASSIFIED
Durante:        el canal cambia (un hilo se vuelve privado) → reclassifySessionAudience (solo restringe)
Contexto:       PolicyEngine fija el techo → contextCeilingForAudience → selectRetrievedCandidates (CH-42)
Telemetría:     un componente produce un TelemetrySpan
                captureCeilingFor(audiencia, políticas) → TraceCapturePolicy
                EventBus.fanOutSpan → governSpanForDestination por destino → SpanDelivery
Auditoría:      recordAuditEntry (CH-19) sin cambios: no pasa por el techo de captura
```

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
canal → DataGovernanceEngine.classifySessionAudience → SessionAudience
span → EventBus.fanOutSpan → DataGovernanceEngine.governSpanForDestination → destinos (recortado)
PolicyEngine (techo) → DataGovernanceEngine.contextCeilingForAudience → ContextEngine
```

**Vista 2 — Sequence: la conversación privada**

```text
sesión s-8, canal directo → classifySessionAudience = PRIVATE
captureCeilingFor(PRIVATE) = techo INTERNAL, sin cuerpos
span "model.call" (CONFIDENTIAL: el prompt con el salario)
   │ fanOutSpan(span, política, [trazas-ops (techo CONFIDENTIAL), pruebas (techo PUBLIC)])
   │   trazas-ops: techo efectivo INTERNAL → por encima → solo metadatos, body NULL, redacted
   │   pruebas:    techo efectivo PUBLIC   → por encima → solo metadatos, body NULL, redacted
   ▼ ninguno de los dos destinos recibió el salario
```

**Vista 2b — Sequence: el hilo público**

```text
sesión s-9, canal de toda la empresa → PUBLIC
PolicyEngine fija techo de contexto CONFIDENTIAL; techo público del despliegue INTERNAL
contextCeilingForAudience(PUBLIC, CONFIDENTIAL, INTERNAL) = INTERNAL
selectRetrievedCandidates(…, INTERNAL, …) → la planilla de salarios (CONFIDENTIAL) no entra
```

**Vista 2c — Sequence: canal que no dice**

```text
classifySessionAudience(…, NULL) = UNKNOWN
contexto: como PUBLIC (techo bajado)   telemetría: como PRIVATE (o más estricto)
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION classifySessionAudience(
    sessionId: SessionId,
    declared: Optional<AudienceKind>,
    decidedBy: Text,
    execution: ExecutionContext,
    agentId: AgentId
) -> SessionAudience

    kind: AudienceKind = UNKNOWN
    IF declared != NULL
        kind = declared
    END

    audience: SessionAudience = SessionAudience(
        sessionId = sessionId,
        kind = kind,
        decidedBy = decidedBy,
        decidedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = SESSION_AUDIENCE_CLASSIFIED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = audience
    )

    RETURN audience
END
```

```pseudocode
FUNCTION reclassifySessionAudience(
    current: SessionAudience,
    declared: AudienceKind,
    decidedBy: Text,
    execution: ExecutionContext,
    agentId: AgentId
) -> SessionAudience

    IF current.kind == declared
        RETURN current
    END

    IF current.kind != PUBLIC AND declared != PRIVATE
        THROW HarnessError(
            category = VALIDATION,
            code = "AUDIENCE_RELAXATION_NOT_ALLOWED",
            message = "Dentro de una sesión, la audiencia solo se vuelve más restrictiva",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN classifySessionAudience(current.sessionId, declared, decidedBy, execution, agentId)
END
```

```pseudocode
FUNCTION lowerCeiling(
    a: DataClassificationLevel,
    b: DataClassificationLevel
) -> DataClassificationLevel

    IF moreRestrictive(a, b) == a
        RETURN b
    END

    RETURN a
END
```

```pseudocode
FUNCTION findCapturePolicy(
    policies: List<TraceCapturePolicy>,
    kind: AudienceKind
) -> Optional<TraceCapturePolicy>

    FOR EACH policy IN policies
        IF policy.audience == kind
            RETURN policy
        END
    END

    RETURN NULL
END
```

```pseudocode
FUNCTION captureCeilingFor(
    audience: SessionAudience,
    policies: List<TraceCapturePolicy>
) -> TraceCapturePolicy

    found: Optional<TraceCapturePolicy> = findCapturePolicy(policies, audience.kind)

    IF found == NULL
        RETURN TraceCapturePolicy(audience = audience.kind, ceiling = PUBLIC, captureBodies = FALSE)
    END

    IF audience.kind == UNKNOWN
        private: Optional<TraceCapturePolicy> = findCapturePolicy(policies, PRIVATE)
        IF private == NULL
            RETURN TraceCapturePolicy(audience = UNKNOWN, ceiling = PUBLIC, captureBodies = FALSE)
        END

        RETURN TraceCapturePolicy(
            audience = UNKNOWN,
            ceiling = lowerCeiling(found.ceiling, private.ceiling),
            captureBodies = found.captureBodies AND private.captureBodies
        )
    END

    RETURN found
END
```

```pseudocode
FUNCTION contextCeilingForAudience(
    audience: SessionAudience,
    policyCeiling: DataClassificationLevel,
    publicCeiling: DataClassificationLevel
) -> DataClassificationLevel

    IF audience.kind == PRIVATE
        RETURN policyCeiling
    END

    RETURN lowerCeiling(policyCeiling, publicCeiling)
END
```

```pseudocode
FUNCTION governSpanForDestination(
    span: TelemetrySpan,
    policy: TraceCapturePolicy,
    destination: TraceDestination
) -> TelemetrySpan

    ceiling: DataClassificationLevel = lowerCeiling(policy.ceiling, destination.ceiling)
    withinCeiling: Boolean = moreRestrictive(span.classification, ceiling) == ceiling

    IF NOT withinCeiling
        RETURN TelemetrySpan(
            spanId = span.spanId,
            traceId = span.traceId,
            parentSpanId = span.parentSpanId,
            sessionId = span.sessionId,
            name = span.name,
            startedAt = span.startedAt,
            endedAt = span.endedAt,
            attributes = metadataAttributes(span.attributes),
            body = NULL,
            classification = ceiling,
            redacted = TRUE
        )
    END

    IF span.body != NULL AND NOT policy.captureBodies
        RETURN TelemetrySpan(
            spanId = span.spanId,
            traceId = span.traceId,
            parentSpanId = span.parentSpanId,
            sessionId = span.sessionId,
            name = span.name,
            startedAt = span.startedAt,
            endedAt = span.endedAt,
            attributes = span.attributes,
            body = NULL,
            classification = span.classification,
            redacted = TRUE
        )
    END

    RETURN span
END
```

```pseudocode
FUNCTION fanOutSpan(
    span: TelemetrySpan,
    policy: TraceCapturePolicy,
    destinations: List<TraceDestination>
) -> List<SpanDelivery>

    deliveries: List<SpanDelivery> = []

    FOR EACH destination IN destinations
        deliveries = append(deliveries, SpanDelivery(
            destinationRef = destination.destinationRef,
            span = governSpanForDestination(span, policy, destination)
        ))
    END

    RETURN deliveries
END
```

Utilidades primitivas:
- `metadataAttributes` conserva solo los atributos de diagnóstico declarados como metadatos
  (duraciones, códigos, ids) y descarta el resto;
- `append`, `newEventId` y `now` son las de siempre.

`moreRestrictive` (CH-42) y `selectRetrievedCandidates` (CH-42) no cambian: el techo que recibe
`selectRetrievedCandidates` ahora sale de `contextCeilingForAudience`.

**Por qué un span por encima del techo conserva sus metadatos:** el operador necesita saber que hubo
una llamada al modelo, cuánto tardó y si falló, aunque no pueda leer qué se dijo. Sin metadatos no
habría diagnóstico; con el cuerpo no habría privacidad.

Nótese lo que estas funciones **no** hacen:
- ninguna toca la auditoría: `recordAuditEntry` (CH-19) sigue igual;
- ninguna recorta un `AgentEvent`: su payload lo decide cada productor, y los eventos que van a un
  destino de trazas se convierten primero en spans;
- `contextCeilingForAudience` nunca sube el techo de la política, solo lo baja.

## 12. Transiciones de Estado (State Transitions)

`AgentRunStatus` no cambia. La audiencia de una sesión:

```text
(crear) → PUBLIC | PRIVATE | UNKNOWN (UNKNOWN si el canal no lo dice)
PUBLIC  → PRIVATE | UNKNOWN          (más restrictiva: permitido)
UNKNOWN → PRIVATE                    (permitido)
UNKNOWN → PUBLIC, PRIVATE → otra     (AUDIENCE_RELAXATION_NOT_ALLOWED)

Un span hacia un destino
    dentro del techo, con cuerpo permitido o sin cuerpo → llega tal cual
    dentro del techo, cuerpo no permitido               → sin body, redacted
    por encima del techo                                → solo metadatos, redacted
```

## 13. Semántica de Fallos (Failure Semantics)

Código nuevo de `HarnessError`, con una `ErrorCategory` ya existente:

```text
VALIDATION  AUDIENCE_RELAXATION_NOT_ALLOWED  recoverable: FALSE, retryable: FALSE
```

- Una sesión que necesita una audiencia menos restrictiva se abre como sesión nueva.
- **Sin política para una audiencia,** el techo es el más restrictivo (PUBLIC, sin cuerpos), no un
  error: la telemetría sigue funcionando, con menos contenido.
- **Un destino que no responde** es un problema del adaptador del destino; los spans recortados no se
  reintentan con más contenido.

## 14. Eventos Producidos (Events Produced)

```text
SESSION_AUDIENCE_CLASSIFIED — se asignó o restringió la audiencia de una sesión (payload: SessionAudience)
```

Recortar un span no emite un evento: pasaría en casi todos los spans de una sesión privada. El span
mismo lo dice (`redacted = TRUE`).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Los operadores no leen conversaciones privadas en las trazas:** el techo de una sesión PRIVATE
  deja solo metadatos por encima de su nivel.
- **Un canal público no filtra datos confidenciales en las respuestas:** el techo de contexto baja.
- **No saber es lo más restrictivo de los dos lados.**
- **Agregar un destino no agrega exposición:** cada destino recibe a lo sumo el techo de la sesión, y
  puede declarar uno más bajo.
- **Ningún destino puede restaurar lo recortado:** el recorte ocurre antes de distribuir.
- **La auditoría sigue completa** para quien está autorizado a leerla (P-25).

## 16. Tests (Tests)

```text
TEST AudienceDefaultsToUnknownWhenTheChannelDoesNotSay
TEST ClassifyingAudienceEmitsEvent
TEST AudienceMayOnlyBecomeMoreRestrictive
TEST UnknownMayBecomePrivateButNotPublic
TEST MissingCapturePolicyFallsBackToTheMostRestrictive
TEST UnknownCaptureIsAtLeastAsStrictAsPrivate
TEST PrivateSessionKeepsThePolicyContextCeiling
TEST PublicAndUnknownSessionsLowerTheContextCeiling
TEST ContextCeilingIsNeverRaised
TEST SpanAboveCeilingKeepsOnlyMetadata
TEST BodyIsDroppedWhenCaptureBodiesIsFalse
TEST DestinationCeilingLowersButNeverRaises
TEST FanOutGovernsEachDestinationSeparately
TEST AuditEntriesAreNotCappedByAudience
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.3 en curso, después de CH-46) — 29 componentes, 63 contratos, 47 capítulos

Components — 29, sin cambios
 ├── CMP-018 DataGovernanceEngine  (+ audiencia de la sesión, techos de captura y de contexto)
 └── CMP-009 EventBus              (+ fan-out de spans ya recortados)

Contracts — 63
 ├── C-061 SessionAudience         (CH-46)
 ├── C-062 TraceCapturePolicy      (CH-46)
 └── C-063 TelemetrySpan           (CH-46)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El formato de exportación de cada destino** (protocolos de trazas, proveedores): es del adaptador
  de cada destino. No es deuda.
- **Muestreo de spans** (capturar uno de cada cien): reduce volumen, no exposición; es configuración
  del adaptador. No es deuda.
- **Detectar contenido sensible dentro de un cuerpo** sin clasificación previa: la clasificación la
  asigna quien produce el span, con las reglas de CH-20. No es deuda.
- **Quién puede leer la auditoría:** es autorización (PolicyEngine) sobre `AuditLedger`, no captura. No
  es deuda.

## 19. Siguiente Incremento (Next Increment)

Ahora el arnés observa cada sesión sin exponer lo que su audiencia no debe ver. Pero cuando se cambia
algo —un prompt, una política, un modelo— todavía no hay una forma gobernada de medir si el cambio
**mejora** al agente frente a la versión anterior.

El siguiente capítulo introduce la **evaluación con lift**:
- un `LiftReport` que compara una línea base y un tratamiento sobre la misma métrica;
- `EvaluationResult` v2 con su evidencia;
- cada corrida en su propio entorno aislado (CH-35), para que una no contamine a la otra.

Será CH-47 ("Evaluación con Lift"). `next_chapter` queda en `null` porque CH-47 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): las trazas capturan todo, y una sesión pública puede responder con datos
   confidenciales.
2. **Patrones** (= §3): la clasificación es del dato y el techo de contexto de la política; ninguno
   conoce a quién ve la sesión.
3. **Estructuras** (= §8): `SessionAudience` (C-061), `TraceCapturePolicy` (C-062), `TelemetrySpan`
   (C-063) y funciones nuevas en `DataGovernanceEngine` y `EventBus`.
4. **Modelos mentales** (= §4): P-37, INV-E23, P-25 y P-22.

**Bucles de retroalimentación**

- **Refuerzo:** cada destino nuevo es otra copia de contenido privado.
- **Equilibrio:** el techo de captura. Agregar un destino no agrega contenido.

**Punto de apalancamiento**

La decisión con mayor efecto es que `TraceCapturePolicy` (C-062) se derive de la audiencia y se
aplique antes de distribuir: ningún destino recibe lo que el techo excluye.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué techo de contexto devuelve `contextCeilingForAudience` para una sesión PRIVATE y para una
   PUBLIC o UNKNOWN, y a qué función de CH-42 se le pasa? *(pregunta guía 1)*
2. ¿Qué hace `governSpanForDestination` con un span por encima del techo, y con uno dentro del techo
   cuyo cuerpo la política no permite capturar? *(pregunta guía 2)*
3. ¿Qué techo de captura usa `captureCeilingFor` para una sesión UNKNOWN, qué pasa si no hay política,
   y qué cambios de audiencia permite `reclassifySessionAudience`? *(pregunta guía 3)*
4. ¿Qué hace cada una de las tres señales (evento, auditoría, span), y por qué el techo de captura se
   aplica a los spans y no a la auditoría? *(pregunta guía 4)*

### Explicar

1. `DataGovernanceEngine` ya clasificaba datos. Explica por qué también le pertenece decidir los techos
   por audiencia, y qué le queda a `EventBus`.
2. Explica por qué el techo de captura se aplica antes de distribuir el span y no en cada destino, y
   qué no se podría garantizar si cada destino recortara por su cuenta.

### Conectar

1. En CH-42, `selectRetrievedCandidates` recibía un techo de clasificación fijado por la política. ¿Qué
   techo recibe ahora en una sesión PUBLIC, qué función lo calcula, y por qué ese cálculo nunca puede
   subir el techo de la política?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
