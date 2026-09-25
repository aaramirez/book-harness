---
id: CH-30
title: "Cuando No se Sabe si Ocurrió: Política de Replay"
starting_version: "0.1"
ending_version: "0.2"
introduces_components: []
introduces_contracts: [C-039]
modifies_contracts: [C-018, C-009]
constitutional_articles: [P-24, INV-07, INV-11, INV-20, INV-E09, INV-E17]
previous_chapter: CH-29
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH30
    text: |
      Al terminar este capítulo podrás decidir, para cualquier efecto externo que empezó pero cuyo
      resultado nunca se registró, si el arnés debe esperar, volver a ejecutarlo o reportar al
      modelo que el resultado es desconocido — y podrás justificar por qué esa decisión la declara
      cada capability y no la toma el modelo ni se deja a la buena voluntad de cada herramienta.
  skeleton:
    id: SK-CH30
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
    contracts_to_be_introduced: [C-039]
  guiding_questions:
    - id: GQ-CH30-01
      text: |
        Si el proceso se cae justo después de pedirle a una API de pagos que cobre, y antes de guardar
        su respuesta, ¿el arnés sabe si el cobro ocurrió? ¿Qué sería peor: volver a cobrar o no hacer
        nada?
      answered_by: RQ-CH30-01
    - id: GQ-CH30-02
      text: |
        ¿Hay herramientas que sí se pueden repetir sin riesgo aunque no se sepa si la primera vez
        funcionó? ¿Quién debería decir cuáles son: el modelo, el arnés o la propia herramienta?
      answered_by: RQ-CH30-02
    - id: GQ-CH30-03
      text: |
        Si una herramienta no dice nada sobre si es seguro repetirla, ¿qué debería asumir el arnés
        por defecto, y por qué?
      answered_by: RQ-CH30-03
    - id: GQ-CH30-04
      text: |
        Si el arnés decide no repetir, ¿qué le cuenta al modelo sobre lo que pasó: que funcionó, que
        falló, o algo distinto?
      answered_by: RQ-CH30-04
  systems_lens:
    iceberg_visible_fact: |
      Tras un corte, un efecto externo queda en el limbo: empezó, pero su resultado nunca se
      registró. Las implementaciones lo resuelven al azar — lo repiten (y cobran dos veces), lo dan
      por hecho (y el modelo cree que funcionó) o lo dan por fallido (y el modelo lo reintenta por su
      cuenta) (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que "¿se puede repetir?" queda sin dueño: ni la capability lo
      declara, ni el arnés tiene una regla, así que lo decide quien esté más cerca del error.
      IdempotencyGuard (CH-17) resuelve duplicados con clave, pero no el caso en que no se sabe si
      el efecto ocurrió (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce ReplayPolicy (C-039) como declaración de cada capability en
      CapabilityDescriptor v2 (C-018), y ToolResult v2 (C-009) con outcome = UNKNOWN como
      observación explícita. IdempotencyGuard decide WAIT / REEXECUTE / REPORT_UNKNOWN dentro de su
      owns ya existente (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-24 (todo side effect declara su semántica de idempotencia y retry)
      e INV-E17 (un efecto de resultado desconocido solo se re-ejecuta si su capability es SAFE):
      la seguridad de repetir es una propiedad declarada, no una suposición (ver sección 4).
    reinforcing_loop: |
      Cada efecto duplicado por un reintento a ciegas empuja a las implementaciones a desactivar
      los reintentos en general, y entonces se pierden también los que eran seguros (lecturas), lo
      que obliga al usuario a repetir a mano. Declarar la política por capability corta esa espiral:
      se repite solo lo que es seguro repetir.
    balancing_loop: |
      El default NEVER es el mecanismo de equilibrio: una capability que no declaró nada nunca se
      re-ejecuta tras un resultado desconocido. El costo es conservador (se reporta en vez de
      repetir), pero nunca se duplica un efecto.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que ReplayPolicy (C-039) viva en el
      CapabilityDescriptor y valga NEVER cuando no se declara. Así la seguridad de repetir se decide
      una vez, al registrar la capability, y no en el momento del corte.
  recall_questions:
    - id: RQ-CH30-01
      text: |
        ¿Qué condición exacta hace que decideUnknownOutcome trate un efecto como de resultado
        desconocido, usando el IdempotencyRecord de CH-17 y la señal executionStillInFlight?
    - id: RQ-CH30-02
      text: |
        ¿Dónde se declara la ReplayPolicy de una capability, y qué acción decide
        decideUnknownOutcome cuando esa política es SAFE?
    - id: RQ-CH30-03
      text: |
        ¿Qué devuelve effectiveReplayPolicy cuando el CapabilityDescriptor no declara ninguna
        política, y qué invariante de Amendment v1.2 protege ese default?
    - id: RQ-CH30-04
      text: |
        ¿Qué ToolResult construye buildUnknownOutcomeResult (valores de succeeded, outcome y error),
        y por qué no es ni un éxito ni un fallo común?
  explain_prompts:
    - id: EP-CH30-01
      text: |
        IdempotencyGuard ya decidía si una ejecución repetida debía reusar un resultado conocido.
        Explica, como si hablaras con alguien sin contexto técnico, por qué decidir qué hacer ante un
        resultado DESCONOCIDO también le pertenece — y por qué NO le pertenece ejecutar el efecto de
        nuevo (ToolRuntime) ni autorizarlo (PolicyEngine).
      target_entity: CMP-015
    - id: EP-CH30-02
      text: |
        Explica por qué la política de replay se declara en el CapabilityDescriptor que registra
        CapabilityRegistry y no se decide en el momento del corte, y por qué el modelo nunca puede
        cambiarla aunque proponga "vuelve a intentarlo".
      target_entity: C-039
  interleaved_questions:
    - id: IQ-CH30-01
      text: |
        En CH-17, un IdempotencyRecord en PENDING significaba "hay una ejecución en curso: espera".
        ¿Qué cambia en ese mismo estado cuando la ejecución ya no está en curso, y qué función de
        CH-17 se invoca después si decideUnknownOutcome devuelve REEXECUTE?
      current_chapter_entities: [C-039]
      prior_chapter_entities: [C-027, CMP-015]
      prior_chapter: CH-17
  flashcards:
    - id: FC-CH30-01
      front: |
        ¿Qué es ReplayPolicy (C-039) y cuál es su valor efectivo si no se declara?
      back: |
        Lo que una capability declara que el arnés debe hacer si no se sabe si su efecto ocurrió:
        NEVER (reportar el resultado desconocido, nunca re-ejecutar) o SAFE (re-ejecutar es seguro).
        Si no se declara, effectiveReplayPolicy devuelve NEVER (INV-E17, fail-closed).
      source_entity: C-039
      chapter_introduced_in: CH-30
      review_stage: DAY_1
    - id: FC-CH30-02
      front: |
        ¿Cuáles son las tres acciones de decideUnknownOutcome y cuándo aplica cada una?
      back: |
        WAIT: la ejecución sigue en curso (semántica de CH-17). REEXECUTE: ya no está en curso y la
        política es SAFE. REPORT_UNKNOWN: ya no está en curso y la política es NEVER (o no declarada).
      source_entity: C-039
      chapter_introduced_in: CH-30
      review_stage: DAY_1
    - id: FC-CH30-03
      front: |
        ¿Qué agregan CapabilityDescriptor v2 (C-018) y ToolResult v2 (C-009)?
      back: |
        CapabilityDescriptor v2: replayPolicy (Optional<ReplayPolicy>, NULL = NEVER). ToolResult v2:
        outcome (Optional<ToolOutcome>: SUCCEEDED / FAILED / UNKNOWN; NULL se deriva de succeeded).
        Ambos compatibles hacia atrás (ADR-002).
      source_entity: C-018
      chapter_introduced_in: CH-30
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH30-01
      recall_question: RQ-CH30-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH30-02
      recall_question: RQ-CH30-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH30-03
      recall_question: RQ-CH30-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH30-04
      recall_question: RQ-CH30-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 30 — Cuando No se Sabe si Ocurrió: Política de Replay

> **Regla constitucional (INV-E17):** un efecto cuyo resultado es desconocido solo se re-ejecuta
> si su capability declara `replayPolicy = SAFE`.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir, para cualquier efecto externo que
empezó pero cuyo resultado nunca se registró, si el arnés debe esperar, volver a ejecutarlo o
reportar al modelo que el resultado es desconocido. También podrás justificar por qué esa decisión
la declara cada capability, y no la toma el modelo ni se deja a la buena voluntad de cada
herramienta.

**Esqueleto.** Tercer capítulo del Tramo 4. Introduce un contrato y lleva dos contratos existentes a
su versión 2.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si el proceso se cae justo después de pedirle a una API de pagos que cobre, y antes de guardar su
   respuesta, ¿el arnés sabe si el cobro ocurrió? ¿Qué sería peor: volver a cobrar o no hacer nada?
2. ¿Hay herramientas que sí se pueden repetir sin riesgo aunque no se sepa si la primera vez
   funcionó? ¿Quién debería decir cuáles son: el modelo, el arnés o la propia herramienta?
3. Si una herramienta no dice nada sobre si es seguro repetirla, ¿qué debería asumir el arnés por
   defecto, y por qué?
4. Si el arnés decide no repetir, ¿qué le cuenta al modelo sobre lo que pasó: que funcionó, que
   falló, o algo distinto?

## 1. Arquitectura Actual (Current Architecture)

**`IdempotencyGuard` (CMP-015, CH-17)** protege los side effects críticos con un `IdempotencyRecord` (C-027) por clave, que tiene dos estados:
- **`PENDING`:** hay una ejecución en curso, así que hay que esperar;
- **`COMPLETED`:** el resultado ya se conoce y se reutiliza.

`checkIdempotency` consulta el registro antes de ejecutar, y `recordIdempotentExecution` lo cierra en `COMPLETED` al terminar. Si antes había un `PENDING`, conserva su `id` y su `createdAt`.

**`CapabilityRegistry` (CMP-008, CH-08)** registra cada capability en un `CapabilityDescriptor` (C-018): `capability`, `name`, `version`, `inputSchema` e `implementationRef`.

**`ToolRuntime` (CMP-002, CH-02)** devuelve un `ToolResult` (C-009) con `succeeded`, `output`, `error` y `completedAt`. Siempre vuelve al ciclo como observación explícita (INV-07).

## 2. El Problema (Problem)

Hay un momento en que el arnés **no sabe** qué pasó:
1. el efecto externo se pidió (se llamó a la API de pagos, se envió el correo, se creó el recurso);
2. el proceso se cayó antes de registrar la respuesta;
3. al reanudar, el `IdempotencyRecord` sigue en `PENDING`, pero la ejecución que lo abrió ya no existe.

Las implementaciones resuelven ese limbo al azar:
- **lo repiten**, y cobran dos veces;
- **lo dan por hecho**, y el modelo cree que funcionó;
- **lo dan por fallido**, y el modelo lo reintenta por su cuenta.

Ninguna de las tres es honesta con lo que el arnés realmente sabe.

Necesitamos que cada capability **declare** si es seguro repetirla, y que, cuando no lo sea, el
modelo reciba la verdad: "el resultado externo es desconocido".

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- `PENDING` (CH-17) solo significa "espera". No distingue una ejecución que sigue viva de una que
  murió con el proceso. En el segundo caso, esperar es esperar para siempre.
- `CapabilityDescriptor` (C-018 v1) no tiene dónde declarar si repetir es seguro. P-24 e INV-E09
  exigen que todo side effect declare su semántica de idempotencia y retry, pero el contrato no
  tiene ese campo.
- `ToolResult` (C-009 v1) solo tiene `succeeded: Boolean`. No hay forma de decir "no sé": un
  `FALSE` le dice al modelo que falló, lo cual es falso si el efecto en realidad ocurrió.
- Sin regla declarada, la decisión queda a quien esté más cerca del error, a veces el propio
  modelo, que propone "vuelve a intentarlo" sin saber si el primer intento funcionó.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-24   Side effects require idempotency semantics.
           Cada capability declara ahora, además de su clave de idempotencia (CH-17), si es
           seguro re-ejecutarla ante un resultado desconocido (replayPolicy).

Invariants preserved
    INV-07   El ToolResult vuelve al loop como observación explícita.
             Un resultado desconocido vuelve como ToolResult con outcome = UNKNOWN: una
             observación, no un silencio ni un éxito inventado.
    INV-11   Los side effects críticos requieren idempotencia o deduplicación.
             Se completa el caso que CH-17 dejaba abierto: el PENDING huérfano.
    INV-20   Todo error operacional tiene una categoría conocida.
             TOOL_OUTCOME_UNKNOWN y UNKNOWN_OUTCOME_REQUIRES_PENDING_RECORD usan IDEMPOTENCY.
    INV-E09  Todo side effect declara idempotencia y retry.
             replayPolicy es esa declaración, con default NEVER.
    INV-E17  (Amendment v1.2) Un efecto de resultado desconocido solo se re-ejecuta si su
             capability declara replayPolicy = SAFE.
             decideUnknownOutcome es su materialización directa.

Component ownership changes
    Ninguno en registry/components.yaml. IdempotencyGuard (CMP-015) ya posee "decidir si
    una ejecución repetida debe reusar el ToolResult ya conocido en vez de que el side
    effect real vuelva a ejecutarse"; decidir qué hacer ante un resultado desconocido es el
    mismo tipo de decisión. CapabilityRegistry (CMP-008) solo registra la política en el
    descriptor.

Contract changes
    C-018 CapabilityDescriptor v2 (replayPolicy) y C-009 ToolResult v2 (outcome), ambos
    compatibles hacia atrás (ADR-002, Accepted 2026-09-25).

Security implications
    El modelo no puede cambiar la política ni forzar un reintento (ver sección 15).

Observability implications
    Dos valores nuevos de AgentEventType (ver sección 14).

Deterministic vs agentic boundary
    Qué hacer ante un resultado desconocido es determinístico y declarado por la
    capability; el modelo solo recibe la observación y propone el paso siguiente.
```

## 5. Conceptos Nuevos (New Concepts)

- **Resultado desconocido** (*unknown outcome*): un efecto externo que empezó pero cuyo resultado nunca se registró. En este libro se reconoce por un `IdempotencyRecord` en `PENDING` cuya ejecución **ya no está en curso**.
- **Política de replay**: lo que cada capability declara que el arnés debe hacer ante un resultado desconocido.
  - **`NEVER`:** nunca re-ejecutar; reportar al modelo que no se sabe.
  - **`SAFE`:** re-ejecutar es seguro; por ejemplo, una lectura, o una operación que el sistema externo ya deduplica.
- **Default conservador**: una capability que no declara política vale `NEVER`. Es conservador (a veces se reporta lo que se podría haber repetido), pero **nunca** duplica un efecto.
- **Tres acciones**:
  - **`WAIT`:** la ejecución sigue en curso; es la semántica original de CH-17.
  - **`REEXECUTE`:** ya no está en curso y la política es `SAFE`.
  - **`REPORT_UNKNOWN`:** ya no está en curso y la política es `NEVER`.

Re-ejecutable (este capítulo) y deduplicable por clave (CH-17) son **dos preguntas distintas**:
- una capability puede tener clave de idempotencia y aun así ser `NEVER`, porque el sistema externo no garantiza nada;
- otra puede ser `SAFE` sin clave, como una lectura.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `ToolCall` (C-008), `ToolResult` (C-009, que pasa a v2), `CapabilityDescriptor` (C-018, que pasa a v2), `IdempotencyRecord` (C-027), `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `ToolCallId`, `CapabilityId`, `AgentId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `IdempotencyRecordStatus` | `PENDING` / `COMPLETED` (heredado de CH-17) |
| `AgentEventType` | se agregan `TOOL_OUTCOME_UNKNOWN_DETECTED` y `TOOL_REPLAY_DECIDED` |
| `ErrorCategory` | reutiliza `IDEMPOTENCY` y `VALIDATION`, sin valores nuevos |

### `ReplayPolicy` — el contrato de este capítulo (C-039)

```pseudocode
ENUM ReplayPolicy
    NEVER
    SAFE
END
```

### `ToolOutcome` — el resultado de una tool, con un tercer valor (embebido)

```pseudocode
ENUM ToolOutcome
    SUCCEEDED
    FAILED
    UNKNOWN
END
```

### `UnknownOutcomeAction` — qué hace el arnés ante un resultado desconocido (embebido)

```pseudocode
ENUM UnknownOutcomeAction
    WAIT
    REEXECUTE
    REPORT_UNKNOWN
END
```

### `UnknownOutcomeDecision` — la decisión, trazable (embebida)

```pseudocode
STRUCT UnknownOutcomeDecision
    callId: ToolCallId
    capability: CapabilityId
    policy: ReplayPolicy
    action: UnknownOutcomeAction
    decidedAt: Timestamp
END
```

### `CapabilityDescriptor` — versión 2 (C-018)

```pseudocode
STRUCT CapabilityDescriptor
    capability: CapabilityId
    name: Text
    version: Text
    inputSchema: Value
    implementationRef: Text
    replayPolicy: Optional<ReplayPolicy>
END
```

### `ToolResult` — versión 2 (C-009)

```pseudocode
STRUCT ToolResult
    callId: ToolCallId
    succeeded: Boolean
    outcome: Optional<ToolOutcome>
    output: Optional<Value>
    error: Optional<HarnessError>
    completedAt: Timestamp
END
```

**Compatibilidad hacia atrás** (ADR-002):
- `replayPolicy = NULL` equivale a `NEVER`;
- `outcome = NULL` se deriva de `succeeded` (`TRUE` → `SUCCEEDED`, `FALSE` → `FAILED`), exactamente como en v1.

Ningún descriptor ni resultado construido en CH-02..CH-29 cambia de significado.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-039
Name:                   ReplayPolicy
Version:                v1
Introduced In:          CH-30
Current Definition:     ENUM ReplayPolicy (ver seccion 6)
Used By:                [CMP-008, CMP-015]
Modified By:            []
Constitutional Impact:  [P-24, INV-E09, INV-E17]
```

```text
ID:                     C-018
Name:                   CapabilityDescriptor
Version:                v2   (antes v1, CH-08)
Modified By:            [CH-30]
Cambio:                 + replayPolicy: Optional<ReplayPolicy>  (ADR-002)
```

```text
ID:                     C-009
Name:                   ToolResult
Version:                v2   (antes v1, CH-02)
Modified By:            [CH-30]
Cambio:                 + outcome: Optional<ToolOutcome>  (ADR-002)
```

`ToolOutcome`, `UnknownOutcomeAction` y `UnknownOutcomeDecision` quedan embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo **no introduce componentes**.

```text
COMPONENT: IdempotencyGuard (CMP-015, CH-17 — ficha sin cambios)

Owns (registry/components.yaml, CH-17) — lo que este capítulo usa:
    "decidir si una ejecución repetida debe reusar el ToolResult ya conocido en vez de que el
     side effect real vuelva a ejecutarse"
Decisión nueva, del mismo tipo:
    ante un PENDING cuya ejecución ya no está en curso: ¿WAIT, REEXECUTE o REPORT_UNKNOWN?
Does NOT own (se preserva):
    - ejecutar el efecto de nuevo (ToolRuntime, CH-02)
    - autorizarlo (PolicyEngine, CH-05)
    - declarar la política (la declara la capability; CapabilityRegistry la registra, CH-08)
    - detectar el corte durante una recuperación real (ExecutionJournal, CH-32 — Preview)
```

```text
COMPONENT: CapabilityRegistry (CMP-008, CH-08 — ficha sin cambios)

Lo que cambia: el CapabilityDescriptor que registra lleva ahora replayPolicy.
No decide nada nuevo: registrar una política no es aplicarla.
```

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
IdempotencyGuard (ampliado en CH-30)
    consumes → ToolCall, CapabilityDescriptor v2, IdempotencyRecord (PENDING)
    produces → UnknownOutcomeDecision (embebido), ToolResult v2 (outcome = UNKNOWN),
               AgentEvent, HarnessError
```

La integración, primero en CH-32 (Preview), usa la decisión así:

| Acción | Qué hace la integración después |
|---|---|
| `WAIT` | nada nuevo: la semántica de CH-17 |
| `REEXECUTE` | `executeToolCall` (CH-02) y luego `recordIdempotentExecution` (CH-17) con el mismo `PENDING`, que conserva su `id` y su `createdAt` |
| `REPORT_UNKNOWN` | `buildUnknownOutcomeResult` → el `ToolResult` vuelve al ciclo como observación (INV-07) |

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Integración (recuperación, CH-32 Preview) → IdempotencyGuard → [ToolRuntime | AgentLoop]
```

**Vista 2 — Sequence**

```text
Integración
   │ encuentra un IdempotencyRecord en PENDING y la ejecución que lo abrió ya no existe
   │ decideUnknownOutcome(toolCall, descriptor, pendingRecord, executionStillInFlight = FALSE)
   ▼
IdempotencyGuard
   │ valida: record PENDING; misma capability en record, descriptor y toolCall
   │ emite TOOL_OUTCOME_UNKNOWN_DETECTED
   │ effectiveReplayPolicy(descriptor)
   │   SAFE  → action = REEXECUTE
   │   NEVER (o no declarada) → action = REPORT_UNKNOWN
   │ emite TOOL_REPLAY_DECIDED
   ▼
Integración
   ├─ REEXECUTE      → ToolRuntime.executeToolCall → recordIdempotentExecution (CH-17)
   └─ REPORT_UNKNOWN → buildUnknownOutcomeResult → ToolResult(outcome = UNKNOWN)
                        → vuelve al ciclo como observación → el modelo decide el paso siguiente
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION effectiveReplayPolicy(
    descriptor: CapabilityDescriptor
) -> ReplayPolicy

    IF descriptor.replayPolicy == NULL
        RETURN NEVER
    END

    RETURN descriptor.replayPolicy
END
```

```pseudocode
FUNCTION resolveToolOutcome(
    result: ToolResult
) -> ToolOutcome

    IF result.outcome != NULL
        RETURN result.outcome
    END

    IF result.succeeded
        RETURN SUCCEEDED
    END

    RETURN FAILED
END
```

```pseudocode
FUNCTION decideUnknownOutcome(
    toolCall: ToolCall,
    descriptor: CapabilityDescriptor,
    pendingRecord: IdempotencyRecord,
    executionStillInFlight: Boolean,
    execution: ExecutionContext,
    agentId: AgentId
) -> UnknownOutcomeDecision

    IF pendingRecord == NULL OR pendingRecord.status != PENDING
        THROW HarnessError(
            category = IDEMPOTENCY,
            code = "UNKNOWN_OUTCOME_REQUIRES_PENDING_RECORD",
            message = "Solo un IdempotencyRecord en PENDING puede representar un resultado desconocido",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    IF pendingRecord.capability != toolCall.capability
        OR descriptor.capability != toolCall.capability

        THROW HarnessError(
            category = IDEMPOTENCY,
            code = "IDEMPOTENCY_KEY_CAPABILITY_MISMATCH",
            message = "El registro, el descriptor y la tool call no se refieren a la misma capability",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    policy: ReplayPolicy = effectiveReplayPolicy(descriptor)
    action: UnknownOutcomeAction = WAIT

    IF NOT executionStillInFlight
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = TOOL_OUTCOME_UNKNOWN_DETECTED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = pendingRecord
        )

        IF policy == SAFE
            action = REEXECUTE
        ELSE
            action = REPORT_UNKNOWN
        END
    END

    decision: UnknownOutcomeDecision = UnknownOutcomeDecision(
        callId = toolCall.id,
        capability = toolCall.capability,
        policy = policy,
        action = action,
        decidedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = TOOL_REPLAY_DECIDED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = decision
    )

    RETURN decision
END
```

```pseudocode
FUNCTION buildUnknownOutcomeResult(
    toolCall: ToolCall,
    decision: UnknownOutcomeDecision
) -> ToolResult

    IF decision.action != REPORT_UNKNOWN
        THROW HarnessError(
            category = VALIDATION,
            code = "NOT_A_REPORT_UNKNOWN_DECISION",
            message = "buildUnknownOutcomeResult solo aplica cuando la decisión es REPORT_UNKNOWN",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN ToolResult(
        callId = toolCall.id,
        succeeded = FALSE,
        outcome = UNKNOWN,
        output = NULL,
        error = HarnessError(
            category = IDEMPOTENCY,
            code = "TOOL_OUTCOME_UNKNOWN",
            message = "La ejecución se interrumpió y el resultado externo es desconocido: no asumas que ocurrió ni que falló",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        ),
        completedAt = now()
    )
END
```

`newEventId` y `now` son utilidades primitivas.

Nótese lo que estas funciones **no** hacen:
- ninguna ejecuta el efecto de nuevo;
- ninguna autoriza nada;
- ninguna permite que el modelo cambie la política.

El `ToolResult` de `REPORT_UNKNOWN` tiene `succeeded = FALSE` para no romper a los consumidores de v1, pero `outcome = UNKNOWN` es lo que dice la verdad.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no cambia `AgentRunStatus`. Completa el ciclo de un `IdempotencyRecord` (CH-17):

```text
PENDING (ejecución en curso)        → WAIT (sin cambios, CH-17)
PENDING (ejecución ya no en curso)  → SAFE:  REEXECUTE → COMPLETED (recordIdempotentExecution)
                                    → NEVER: REPORT_UNKNOWN → el registro queda PENDING;
                                             el modelo recibe ToolResult(outcome = UNKNOWN)
COMPLETED                           → reutilizar el resultado (sin cambios, CH-17)
```

Con `REPORT_UNKNOWN` el registro **no** pasa a `COMPLETED`, porque el arnés no sabe si el efecto
ocurrió. Cerrarlo sería afirmar algo que no sabe.

## 13. Semántica de Fallos (Failure Semantics)

Cada fallo nuevo es un `HarnessError` con su `ErrorCategory`:

```text
IDEMPOTENCY
    decideUnknownOutcome sin un registro en PENDING
    → recoverable: FALSE, retryable: FALSE → UNKNOWN_OUTCOME_REQUIRES_PENDING_RECORD

IDEMPOTENCY
    registro, descriptor y tool call con capabilities distintas
    → recoverable: FALSE, retryable: FALSE → IDEMPOTENCY_KEY_CAPABILITY_MISMATCH (el de CH-17)

VALIDATION
    buildUnknownOutcomeResult con una decisión que no es REPORT_UNKNOWN
    → recoverable: FALSE, retryable: FALSE → NOT_A_REPORT_UNKNOWN_DECISION

IDEMPOTENCY (como observación, no como fallo del run)
    el ToolResult de un resultado desconocido
    → recoverable: TRUE, retryable: FALSE → TOOL_OUTCOME_UNKNOWN
```

`TOOL_OUTCOME_UNKNOWN` es `retryable = FALSE` a propósito: el arnés no debe reintentar solo. Si el
modelo propone consultar el estado del efecto (una lectura, que probablemente es `SAFE`), esa es
otra tool call, con su propia autorización.

## 14. Eventos Producidos (Events Produced)

```text
TOOL_OUTCOME_UNKNOWN_DETECTED — un PENDING cuya ejecución ya no está en curso
                                (payload: IdempotencyRecord)
TOOL_REPLAY_DECIDED           — la decisión WAIT / REEXECUTE / REPORT_UNKNOWN
                                (payload: UnknownOutcomeDecision)
```

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **El modelo no puede cambiar la política.** `replayPolicy` vive en el descriptor que registra
  `CapabilityRegistry`. Un "vuelve a intentarlo" del modelo es una tool call nueva, con su propia
  autorización (`PolicyEngine`, CH-05), no un reintento del efecto desconocido.
- **`REEXECUTE` no evita la política.** Re-ejecutar una capability `SAFE` vuelve a pasar por
  `PolicyEngine` como cualquier ejecución. La política de replay decide **si** se puede repetir,
  no **si** está autorizado.
- **Declarar `SAFE` es una afirmación de quien registra la capability.** Marcar `SAFE` algo que no
  lo es (por ejemplo, un cobro sin deduplicación externa) reintroduce el problema. Por eso el
  default es `NEVER`, y conviene auditar las capabilities marcadas `SAFE` (CH-19).
- **Honestidad del resultado:** nunca se reporta como exitoso algo que no se sabe si ocurrió. Esto
  importa para la auditoría (CH-19) y para el traspaso a humanos (CH-23): el humano recibe "no se
  sabe", no una falsa certeza.

## 16. Tests (Tests)

```text
TEST EffectiveReplayPolicyIsNeverWhenTheDescriptorDeclaresNone
TEST PendingRecordWithExecutionInFlightAlwaysWaits
TEST OrphanPendingWithSafePolicyIsReexecuted
TEST OrphanPendingWithNeverPolicyIsReportedAsUnknown
TEST UnknownOutcomeIsNeverReportedAsSucceeded
TEST ReportUnknownLeavesTheIdempotencyRecordPending
TEST DecideUnknownOutcomeRejectsACompletedRecord
TEST DecideUnknownOutcomeRejectsMismatchedCapabilities
TEST BuildUnknownOutcomeResultRejectsNonReportDecisions
TEST ResolveToolOutcomeDerivesFromSucceededWhenOutcomeIsNull
TEST ReexecutionStillPassesThroughPolicyEngine
TEST ModelCannotChangeTheReplayPolicyOfACapability
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.2 en curso, después de CH-30)

Contracts — 39
 ├── C-009 ToolResult v2            (CH-02 → modificado en CH-30: outcome)
 ├── C-018 CapabilityDescriptor v2  (CH-08 → modificado en CH-30: replayPolicy)
 └── C-039 ReplayPolicy             (CH-30, nuevo)

Components — 22, sin cambios
 ├── CMP-015 IdempotencyGuard   (decisión nueva dentro de su owns: resultado desconocido)
 └── CMP-008 CapabilityRegistry (registra la política; no decide nada nuevo)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Detectar el corte.** Saber que una ejecución "ya no está en curso" (`executionStillInFlight = FALSE`) es hoy una señal de entrada asumida. Detectarla de verdad, tras un crash y paso por paso, es de `ExecutionJournal` (CH-32).
- **Cablearlo en la integración** (CH-32 para la recuperación, CH-36 para el turno completo).
- **Consultar el estado del efecto externo** para salir del "no se sabe", por ejemplo preguntarle a la API de pagos si el cobro existe. Es una capability más, que el modelo puede proponer. Este capítulo no la modela.
- **Auditar las capabilities marcadas `SAFE`** (CH-19): queda como recomendación, sin mecanismo nuevo.

## 19. Siguiente Incremento (Next Increment)

La política de replay responde "¿se puede repetir este efecto?". Pero antes de repetir o reportar hay
otra pregunta que el libro todavía no modela: **¿quién pidió este trabajo?** Sin la identidad del
llamante:
- ninguna credencial puede elegirse por usuario;
- ninguna aprobación puede validar quién responde;
- ningún tenant puede aislarse.

El siguiente capítulo introduce el **principal verificado** que viaja con cada turno (P-31), y el arranque que no admite nada sin configuración (INV-E15). Será CH-31 ("La Identidad del Llamante y el Arranque que No Admite Nada"). `next_chapter` queda en `null` porque CH-31 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): tras un corte, un efecto queda en el limbo, y se repite, se da por
   hecho o se da por fallido al azar.
2. **Patrones** (= §3): "¿se puede repetir?" no tiene dueño. CH-17 resolvía los duplicados con
   clave, no el resultado desconocido.
3. **Estructuras** (= §8): `ReplayPolicy` (C-039) declarada en `CapabilityDescriptor` v2,
   `ToolResult` v2 con `outcome = UNKNOWN`, y la decisión de `IdempotencyGuard` dentro de su `owns`.
4. **Modelos mentales** (= §4): P-24 e INV-E17. La seguridad de repetir se declara, no se supone.

**Bucles de retroalimentación**

- **Refuerzo:** cada efecto duplicado lleva a desactivar reintentos en general, y se pierden los que
  eran seguros. Declarar por capability corta la espiral.
- **Equilibrio:** el default `NEVER` nunca duplica un efecto.

**Punto de apalancamiento**

La decisión con mayor efecto es que `ReplayPolicy` (C-039) viva en el `CapabilityDescriptor` y
valga `NEVER` cuando no se declara. La seguridad de repetir se decide una vez, al registrar la
capability, no en el momento del corte.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué condición exacta hace que `decideUnknownOutcome` trate un efecto como de resultado
   desconocido, usando el `IdempotencyRecord` de CH-17 y la señal `executionStillInFlight`?
   *(pregunta guía 1)*
2. ¿Dónde se declara la `ReplayPolicy` de una capability, y qué acción decide
   `decideUnknownOutcome` cuando esa política es `SAFE`? *(pregunta guía 2)*
3. ¿Qué devuelve `effectiveReplayPolicy` cuando el `CapabilityDescriptor` no declara ninguna
   política, y qué invariante de Amendment v1.2 protege ese default? *(pregunta guía 3)*
4. ¿Qué `ToolResult` construye `buildUnknownOutcomeResult` (valores de `succeeded`, `outcome` y
   `error`), y por qué no es ni un éxito ni un fallo común? *(pregunta guía 4)*

### Explicar

1. `IdempotencyGuard` ya decidía si una ejecución repetida debía reusar un resultado conocido.
   Explica por qué decidir qué hacer ante un resultado DESCONOCIDO también le pertenece, y por qué
   NO le pertenece ejecutar el efecto de nuevo (`ToolRuntime`) ni autorizarlo (`PolicyEngine`).
2. Explica por qué la política de replay se declara en el `CapabilityDescriptor` y no se decide en
   el momento del corte, y por qué el modelo nunca puede cambiarla.

### Conectar

1. En CH-17, un `IdempotencyRecord` en `PENDING` significaba "hay una ejecución en curso: espera".
   ¿Qué cambia en ese mismo estado cuando la ejecución ya no está en curso, y qué función de CH-17
   se invoca después si `decideUnknownOutcome` devuelve `REEXECUTE`?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`: dos sobre `ReplayPolicy` y una sobre los contratos v2. Repásalas al día 3, al día 7 y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
