---
id: CH-31
title: "La Identidad del Llamante y el Arranque que No Admite Nada"
starting_version: "0.1"
ending_version: "0.2"
introduces_components: []
introduces_contracts: [C-040, C-041]
modifies_contracts: [C-004, C-023]
constitutional_articles: [P-13, P-17, P-31, INV-19, INV-E02, INV-E07, INV-E15]
previous_chapter: CH-30
next_chapter: CH-32
retrieval_set:
  expected_outcome:
    id: EO-CH31
    text: |
      Al terminar este capítulo podrás decidir de dónde sale la identidad de quien llama al agente y
      cómo viaja con cada turno, distinguir a quien inició una sesión de quien envía la entrega
      actual, y justificar por qué un arnés recién instalado no debe admitir a nadie hasta que alguien
      configure quién puede entrar.
  skeleton:
    id: SK-CH31
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
    contracts_to_be_introduced: [C-040, C-041]
  guiding_questions:
    - id: GQ-CH31-01
      text: |
        Si una herramienta necesita saber para qué empresa (tenant) está trabajando, ¿de dónde
        debería sacar ese dato: del mensaje del usuario, de un argumento que proponga el modelo, o de
        otra parte?
      answered_by: RQ-CH31-01
    - id: GQ-CH31-02
      text: |
        Si una persona empieza una conversación con el agente y más tarde otra persona escribe en
        esa misma conversación, ¿con los permisos de quién debería actuar el agente en ese momento?
      answered_by: RQ-CH31-02
    - id: GQ-CH31-03
      text: |
        Si instalas el arnés y todavía nadie configuró quién puede usarlo, ¿debería aceptar a
        cualquiera "mientras tanto"? ¿Y cómo se distingue un entorno de desarrollo sin que lo decida
        quien hace la petición?
      answered_by: RQ-CH31-03
    - id: GQ-CH31-04
      text: |
        Que alguien haya sido admitido para usar el agente, ¿significa que puede continuar cualquier
        conversación existente?
      answered_by: RQ-CH31-04
  systems_lens:
    iceberg_visible_fact: |
      La identidad del llamante se pierde después de la admisión: las herramientas no saben para
      qué usuario ni para qué empresa trabajan, así que toman ese dato de donde pueden — el texto
      del mensaje o un argumento del modelo — y un arnés recién instalado, sin configurar, acepta a
      cualquiera (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que P-17 asigna la identidad a AdmissionController, pero ningún
      contrato la lleva más allá de la admisión: ExecutionContext no la tiene y ActivationRequest
      solo trae una referencia sin verificar. La identidad se reconstruye en cada lugar que la
      necesita, cada vez con menos garantías (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce Principal (C-040) y CallerSnapshot (C-041), lleva ExecutionContext
      (C-004) y AdmissionDecision (C-023) a v2, y amplía AdmissionController dentro de su owns
      literal ("apply identity, authorization, tenant"), con una regla explícita de propiedad de
      sesión (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-31 (la identidad viaja con cada turno), P-13 (la identidad no es
      autorización: autorizar sigue siendo de PolicyEngine) e INV-E15 (un arnés sin configurar no
      admite nada) (ver sección 4).
    reinforcing_loop: |
      Cada herramienta que toma el tenant de un argumento del modelo abre una puerta para que un
      prompt manipulado actúe sobre otra empresa, y cada incidente así lleva a agregar validaciones
      ad hoc en más herramientas. Llevar el tenant verificado en el contexto corta la espiral: una
      sola fuente, validada una vez.
    balancing_loop: |
      INV-E15 es el mecanismo de equilibrio: un arnés sin reglas de admisión rechaza todo en
      producción, así que la configuración mínima de seguridad no puede olvidarse — el sistema
      no arranca abierto.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que Principal (C-040) llegue a cada turno
      dentro de CallerSnapshot (C-041), con initiator fijo y current renovado, y que requireTenantCaller
      sea la única forma de obtener el tenant. Así ninguna herramienta necesita confiar en el texto.
  recall_questions:
    - id: RQ-CH31-01
      text: |
        ¿Qué devuelve requireTenantCaller, de qué campo del ExecutionContext v2 lo toma, y en qué
        casos lanza TENANT_CALLER_REQUIRED?
    - id: RQ-CH31-02
      text: |
        En un CallerSnapshot, ¿qué campo no cambia nunca y cuál se renueva en cada entrega, y qué
        hace buildCallerSnapshot cuando recibe un snapshot existente?
    - id: RQ-CH31-03
      text: |
        ¿Qué decide admitWithVerifiedIdentity cuando admissionConfigured = FALSE, según processMode
        (DEVELOPMENT o PRODUCTION), y por qué processMode no puede venir del ActivationRequest?
    - id: RQ-CH31-04
      text: |
        ¿Qué regla exige continuationAllowedForCaller para aceptar a un Principal en una sesión
        existente, y qué dos valores tiene SessionOwnershipRule?
  explain_prompts:
    - id: EP-CH31-01
      text: |
        AdmissionController posee "apply identity, authorization, tenant… decisions" (P-17).
        Explica, como si hablaras con alguien sin contexto técnico, por qué convertir una identidad
        ya verificada en un Principal le pertenece — y por qué NO le pertenece verificar la firma de
        un token (un adaptador) ni autorizar una acción concreta (PolicyEngine, P-13).
      target_entity: CMP-012
    - id: EP-CH31-02
      text: |
        Explica por qué CallerSnapshot distingue initiator de current, y qué se rompería si el agente
        siguiera actuando con los permisos del iniciador cuando otra persona escribe en la misma
        sesión.
      target_entity: C-041
  interleaved_questions:
    - id: IQ-CH31-01
      text: |
        resolveCredentialReference (CredentialBroker, CH-16) recibía un agentId, no un usuario. Con
        ExecutionContext v2, ¿qué campo usaría la integración para elegir la credencial del usuario
        o del tenant correctos, y por qué la credencial nunca debería elegirse a partir de un
        argumento del modelo?
      current_chapter_entities: [C-040, C-041]
      prior_chapter_entities: [C-026, CMP-014]
      prior_chapter: CH-16
  flashcards:
    - id: FC-CH31-01
      front: |
        ¿Qué es un Principal (C-040) y cuál es la única fuente válida del tenant de una tool?
      back: |
        La identidad ya verificada de un llamante: principalId, principalType (USER / SERVICE /
        RUNTIME), issuer, tenantId opcional y attributes. El tenant solo sale de
        execution.caller.current vía requireTenantCaller — nunca del prompt ni de un argumento.
      source_entity: C-040
      chapter_introduced_in: CH-31
      review_stage: DAY_1
    - id: FC-CH31-02
      front: |
        ¿Qué es CallerSnapshot (C-041)?
      back: |
        El par initiator (quien creó el run, nunca cambia) y current (quien envió la entrega actual,
        renovado en cada una), que viaja en ExecutionContext v2.
      source_entity: C-041
      chapter_introduced_in: CH-31
      review_stage: DAY_1
    - id: FC-CH31-03
      front: |
        ¿Qué dice INV-E15 y cómo lo aplica admitWithVerifiedIdentity?
      back: |
        Un arnés sin configurar no admite nada, en ningún entorno. Con admissionConfigured = FALSE:
        en PRODUCTION rechaza con HARNESS_ADMISSION_NOT_CONFIGURED; en DEVELOPMENT admite solo con
        un Principal RUNTIME sintético. processMode es un dato del proceso, nunca del request.
      source_entity: C-040
      chapter_introduced_in: CH-31
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH31-01
      recall_question: RQ-CH31-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH31-02
      recall_question: RQ-CH31-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH31-03
      recall_question: RQ-CH31-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH31-04
      recall_question: RQ-CH31-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 31 — La Identidad del Llamante y el Arranque que No Admite Nada

> **Regla constitucional (P-31):** la identidad verificada acompaña cada turno.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir de dónde sale la identidad de quien
llama al agente y cómo viaja con cada turno, y podrás distinguir a quien inició una sesión de quien
envía la entrega actual. También podrás justificar por qué un arnés recién instalado no debe admitir
a nadie hasta que alguien configure quién puede entrar.

**Esqueleto.** Cuarto capítulo del Tramo 4. Introduce dos contratos y lleva a v2 el contrato más
usado del libro (`ExecutionContext`, 11 componentes) junto con la decisión de admisión.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si una herramienta necesita saber para qué empresa (tenant) está trabajando, ¿de dónde debería
   sacar ese dato: del mensaje del usuario, de un argumento que proponga el modelo, o de otra parte?
2. Si una persona empieza una conversación con el agente y más tarde otra persona escribe en esa
   misma conversación, ¿con los permisos de quién debería actuar el agente en ese momento?
3. Si instalas el arnés y todavía nadie configuró quién puede usarlo, ¿debería aceptar a cualquiera
   "mientras tanto"? ¿Y cómo se distingue un entorno de desarrollo sin que lo decida quien hace la
   petición?
4. Que alguien haya sido admitido para usar el agente, ¿significa que puede continuar cualquier
   conversación existente?

## 1. Arquitectura Actual (Current Architecture)

**`AdmissionController` (CMP-012, CH-14)** decide si un `ActivationRequest` (C-022) puede proceder:
- produce un `AdmissionDecision` (C-023) con `ADMIT` o `REJECT`, y rechaza por defecto;
- su ficha le asigna literalmente, por P-17, "apply identity, authorization, tenant, capacity, rate, budget, deduplication and policy decisions before routing".

Pero `ActivationRequest` solo trae un `externalIdentityRef: Text` **sin verificar**, y `AdmissionDecision` no lleva ninguna identidad.

**`ExecutionContext` (C-004, CH-00)** acompaña cada operación del run con `runId`, `sessionId`, `traceId` y `budget`. No hay identidad. **`CredentialBroker` (CH-16)** resuelve credenciales con un `agentId`, no con un usuario.

## 2. El Problema (Problem)

Después de la admisión, la identidad de quien llama **se pierde**:
- las herramientas no saben para qué usuario ni para qué empresa trabajan;
- el dato se toma de donde se puede, a veces del **texto del mensaje** o de un **argumento que propone el modelo**, que es exactamente lo que un prompt manipulado puede falsificar;
- si en una sesión escribe una segunda persona, no hay forma de saber si el agente debe actuar con los permisos de quien la inició o con los de quien escribe ahora.

Y hay un problema de arranque: un arnés recién instalado, sin reglas de admisión configuradas, **acepta a cualquiera**, porque "todavía nadie configuró nada". Muchas instalaciones llegan así a producción.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- P-17 asigna la identidad a `AdmissionController`, pero **ningún contrato la lleva** más allá de la
  admisión. `ExecutionContext` no la tiene, así que ningún componente posterior la puede leer.
- `externalIdentityRef` es texto sin verificar. Tratarlo como identidad es confiar en lo que el
  request dice de sí mismo.
- No existe la distinción entre quien **inició** un run y quien envía la entrega **actual**.
- Nada impide que un arnés sin configurar admita todo. El default REJECT de CH-14 solo aplica cuando
  hay reglas; si no hay ninguna configurada, la implementación decide.
- Nada dice quién puede **continuar** una sesión existente. Que alguien haya sido admitido no
  significa que pueda operar la sesión de otra persona.

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-13   Authorization is deterministic and external to the LLM.
           Un Principal identifica, no autoriza: toda acción sigue pasando por PolicyEngine.
           La identidad deja además de depender de texto que el modelo pueda producir.
    P-17   Admission precedes execution.
           AdmissionController ahora produce, además del ADMIT, el Principal verificado.

Principles introduced (Amendment v1.2, ya ratificado)
    P-31   Identity travels with every turn.
           ExecutionContext v2 lleva CallerSnapshot; initiator fijo, current renovado.

Invariants preserved
    INV-19   Toda decisión crítica es trazable hasta su actor.
             El actor ahora es un Principal con issuer, no un texto libre.
    INV-E02  Ninguna activación se ejecuta sin AdmissionDecision.
             Sin cambios: el principal viaja dentro de esa misma decisión.
    INV-E07  Datos, memoria, credenciales y auditoría aislados por tenant.
             requireTenantCaller es la única fuente del tenant.
    INV-E15  (Amendment v1.2) Un arnés sin configurar no admite nada; la admisión de
             desarrollo depende del modo de proceso, nunca del request.
             admitWithVerifiedIdentity es su materialización directa.

Component ownership changes
    Ninguno en registry/components.yaml. AdmissionController (CMP-012) ya posee
    "apply identity, authorization, tenant… decisions" (P-17).

Contract changes
    C-004 ExecutionContext v2 (caller) y C-023 AdmissionDecision v2 (principal), ambos
    compatibles hacia atrás (ADR-001, Accepted 2026-09-25).

Security implications
    El tenant ya no se toma del texto; un arnés sin configurar no abre producción; la
    continuación de una sesión exige una regla explícita (ver sección 15).

Observability implications
    Un valor nuevo de AgentEventType: SESSION_CONTINUATION_REJECTED.

Deterministic vs agentic boundary
    La identidad es enteramente determinística: el modelo no la propone, no la ve como
    dato editable y no puede cambiarla.
```

## 5. Conceptos Nuevos (New Concepts)

- **Principal verificado**: la identidad de quien llama, ya verificada por un adaptador de identidad (OIDC, JWT, API key) y convertida por `AdmissionController` en un dato del arnés. Tiene un **tipo**:
  - **USER:** una persona;
  - **SERVICE:** un sistema que llama al agente;
  - **RUNTIME:** el propio arnés, por ejemplo en desarrollo o en llamadas internas.
- **Iniciador y actual**: quien **creó** el run (iniciador, fijo) y quien envió la entrega **actual** (actual, renovado en cada una). Las decisiones del turno usan al actual. El iniciador queda para la trazabilidad y para decidir quién puede continuar.
- **Tenant verificado**: la empresa o unidad a la que pertenece el principal. Solo se obtiene del principal actual, nunca del prompt ni de un argumento.
- **Arranque cerrado** (*fail-closed bootstrap*): un arnés sin reglas de admisión configuradas no admite nada. La única excepción es el desarrollo local, y la decide el **modo del proceso** (un dato con el que arrancó el proceso), nunca un campo del request.
- **Regla de propiedad de sesión**: que alguien esté admitido no le da derecho a continuar cualquier sesión. Hace falta una regla explícita:
  - **mismo principal**, o
  - **mismo tenant**.

  No hay un default permisivo.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `ActivationRequest` (C-022), `AdmissionDecision` (C-023, que pasa a v2), `ExecutionContext` (C-004, que pasa a v2), `ExecutionBudget` (C-012), `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `RunId`, `SessionId`, `TraceId`, `AgentId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `ActivationRequestId` | identificador de un `ActivationRequest` (heredado de CH-14) |
| `AdmissionOutcome` | `ADMIT` / `REJECT` (heredado de CH-14) |
| `AgentEventType` | se agrega `SESSION_CONTINUATION_REJECTED` |
| `ErrorCategory` | reutiliza `ADMISSION`, sin valores nuevos |

### `PrincipalType` — el tipo de llamante (embebido)

```pseudocode
ENUM PrincipalType
    USER
    SERVICE
    RUNTIME
END
```

### `Principal` — la identidad verificada (C-040)

```pseudocode
STRUCT Principal
    principalId: Text
    principalType: PrincipalType
    issuer: Text
    tenantId: Optional<Text>
    attributes: Map<Text, Value>
END
```

`issuer` distingue dos identidades con el mismo `principalId` que vienen de proveedores distintos:
el mismo "ana" en dos directorios no es la misma persona.

### `CallerSnapshot` — iniciador y actual (C-041)

```pseudocode
STRUCT CallerSnapshot
    initiator: Principal
    current: Principal
END
```

### `ProcessMode` — el modo con que arrancó el proceso (embebido)

```pseudocode
ENUM ProcessMode
    DEVELOPMENT
    PRODUCTION
END
```

### `SessionOwnershipRule` — quién puede continuar una sesión (embebido)

```pseudocode
ENUM SessionOwnershipRule
    SAME_PRINCIPAL
    SAME_TENANT
END
```

### `ExecutionContext` — versión 2 (C-004)

```pseudocode
STRUCT ExecutionContext
    runId: RunId
    sessionId: SessionId
    traceId: TraceId
    budget: ExecutionBudget
    caller: Optional<CallerSnapshot>
END
```

### `AdmissionDecision` — versión 2 (C-023)

```pseudocode
STRUCT AdmissionDecision
    requestId: ActivationRequestId
    outcome: AdmissionOutcome
    reason: Optional<HarnessError>
    principal: Optional<Principal>
    decidedAt: Timestamp
END
```

**Compatibilidad hacia atrás** (ADR-001):
- `caller = NULL` es un contexto sin identidad, como en v1;
- `principal = NULL` es lo que tienen todo `REJECT` y todas las decisiones de CH-14..CH-30.

Ningún pseudocódigo anterior cambia de significado.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-040
Name:                   Principal
Version:                v1
Introduced In:          CH-31
Used By:                [CMP-012]
Constitutional Impact:  [P-17, P-31, INV-19, INV-E07]
```

```text
ID:                     C-041
Name:                   CallerSnapshot
Version:                v1
Introduced In:          CH-31
Used By:                [CMP-012]
Constitutional Impact:  [P-31, INV-19]
```

```text
C-004 ExecutionContext   v1 → v2   Modified By: [CH-31]   + caller: Optional<CallerSnapshot>
C-023 AdmissionDecision  v1 → v2   Modified By: [CH-31]   + principal: Optional<Principal>
ADR:                     ADR-001 (Accepted 2026-09-25)
```

`PrincipalType`, `ProcessMode` y `SessionOwnershipRule` quedan embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo **no introduce componentes**.

```text
COMPONENT: AdmissionController (CMP-012, CH-14 — ficha sin cambios)

Owns (registry/components.yaml, cita literal de P-17):
    "apply identity, authorization, tenant, capacity, rate, budget, deduplication and
     policy decisions before routing"
Decisiones nuevas, dentro de ese owns:
    - convertir una identidad ya verificada en el Principal de la decisión (admitWithVerifiedIdentity)
    - no admitir nada si no hay reglas configuradas (INV-E15)
    - construir el CallerSnapshot y ligarlo al ExecutionContext
    - decidir si un Principal puede continuar una sesión existente (continuationAllowedForCaller)
Does NOT own (se preserva o se declara explícitamente):
    - verificar la firma de un token (adaptador de identidad, fuera del registro, como el
      Ingress Adapter de CH-14)
    - autorizar una acción concreta (PolicyEngine, CH-05 — P-13)
    - elegir la credencial de un servicio externo (CredentialBroker, CH-16), que desde ahora
      puede leer execution.caller
```

`requireTenantCaller` es una utilidad que cualquier componente que necesite el tenant (credenciales, memoria, datos) invoca sobre el `ExecutionContext`. No es una decisión nueva de nadie, sino la **única lectura válida** del tenant.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
AdmissionController (ampliado en CH-31)
    consumes → ActivationRequest, Principal (verificado por un adaptador), ExecutionContext
    produces → AdmissionDecision v2, CallerSnapshot, ExecutionContext v2, AgentEvent, HarnessError
```

La integración (Preview, CH-36) encadena:
1. el adaptador de identidad verifica el token → `Principal`;
2. `admitWithVerifiedIdentity` → `AdmissionDecision` v2 con `principal`;
3. `buildCallerSnapshot(NULL, principal)` al crear el run, o `acceptDeliveryForSession(...)` en una entrega posterior;
4. `bindCallerToExecution` → `ExecutionContext` v2, que acompaña el resto del turno.

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Llamante → [Adaptador de identidad] → AdmissionController → (ExecutionContext v2) → resto del turno
```

**Vista 2 — Sequence: primera entrega**

```text
Llamante (token)
   ▼
Adaptador de identidad (fuera del registro): verifica firma/emisor → Principal
   ▼
AdmissionController
   │ admitWithVerifiedIdentity(request, principal, admissionConfigured, processMode)
   │   sin reglas configuradas y PRODUCTION → REJECT HARNESS_ADMISSION_NOT_CONFIGURED
   │   sin principal verificado             → REJECT UNVERIFIED_CALLER
   │   reglas de CH-14 conceden acceso      → ADMIT con principal
   │ buildCallerSnapshot(NULL, principal) → initiator = current = principal
   │ bindCallerToExecution(execution, snapshot) → ExecutionContext v2
   ▼
Tools / CredentialBroker / memoria: requireTenantCaller(execution) → tenant verificado
```

**Vista 2b — Sequence: entrega de otra persona en la misma sesión**

```text
Otro llamante (token) → Adaptador → Principal
   ▼
AdmissionController
   │ acceptDeliveryForSession(snapshot, candidato, SAME_TENANT, execution, agentId)
   │   mismo tenant → CallerSnapshot(initiator = original, current = candidato)
   │   otro tenant  → SESSION_CONTINUATION_REJECTED + SESSION_CONTINUATION_NOT_ALLOWED
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION admitWithVerifiedIdentity(
    request: ActivationRequest,
    verifiedPrincipal: Optional<Principal>,
    admissionConfigured: Boolean,
    processMode: ProcessMode
) -> AdmissionDecision

    IF NOT admissionConfigured
        IF processMode == DEVELOPMENT
            RETURN AdmissionDecision(
                requestId = request.id,
                outcome = ADMIT,
                reason = NULL,
                principal = Principal(
                    principalId = "local-development",
                    principalType = RUNTIME,
                    issuer = "harness-process",
                    tenantId = NULL,
                    attributes = {}
                ),
                decidedAt = now()
            )
        END

        RETURN AdmissionDecision(
            requestId = request.id,
            outcome = REJECT,
            reason = HarnessError(
                category = ADMISSION,
                code = "HARNESS_ADMISSION_NOT_CONFIGURED",
                message = "No hay reglas de admisión configuradas: el arnés no admite ninguna activación fuera de desarrollo",
                recoverable = FALSE,
                retryable = FALSE,
                metadata = {}
            ),
            principal = NULL,
            decidedAt = now()
        )
    END

    IF verifiedPrincipal == NULL
        RETURN AdmissionDecision(
            requestId = request.id,
            outcome = REJECT,
            reason = HarnessError(
                category = ADMISSION,
                code = "UNVERIFIED_CALLER",
                message = "La activación no trae una identidad verificada por un adaptador de identidad",
                recoverable = TRUE,
                retryable = FALSE,
                metadata = {}
            ),
            principal = NULL,
            decidedAt = now()
        )
    END

    ruleDecision: AdmissionDecision = evaluateAdmissionForActivationRequest(request)

    IF ruleDecision.outcome != ADMIT
        RETURN ruleDecision
    END

    RETURN AdmissionDecision(
        requestId = request.id,
        outcome = ADMIT,
        reason = NULL,
        principal = verifiedPrincipal,
        decidedAt = ruleDecision.decidedAt
    )
END
```

```pseudocode
FUNCTION buildCallerSnapshot(
    existing: Optional<CallerSnapshot>,
    principal: Principal
) -> CallerSnapshot

    IF existing == NULL
        RETURN CallerSnapshot(initiator = principal, current = principal)
    END

    RETURN CallerSnapshot(initiator = existing.initiator, current = principal)
END
```

```pseudocode
FUNCTION bindCallerToExecution(
    execution: ExecutionContext,
    snapshot: CallerSnapshot
) -> ExecutionContext

    RETURN ExecutionContext(
        runId = execution.runId,
        sessionId = execution.sessionId,
        traceId = execution.traceId,
        budget = execution.budget,
        caller = snapshot
    )
END
```

```pseudocode
FUNCTION continuationAllowedForCaller(
    snapshot: CallerSnapshot,
    candidate: Principal,
    rule: SessionOwnershipRule
) -> Boolean

    IF rule == SAME_PRINCIPAL
        RETURN candidate.issuer == snapshot.initiator.issuer
            AND candidate.principalId == snapshot.initiator.principalId
    END

    RETURN candidate.tenantId != NULL
        AND candidate.tenantId == snapshot.initiator.tenantId
END
```

```pseudocode
FUNCTION acceptDeliveryForSession(
    snapshot: CallerSnapshot,
    candidate: Principal,
    rule: SessionOwnershipRule,
    execution: ExecutionContext,
    agentId: AgentId
) -> CallerSnapshot

    IF NOT continuationAllowedForCaller(snapshot, candidate, rule)
        failure: HarnessError = HarnessError(
            category = ADMISSION,
            code = "SESSION_CONTINUATION_NOT_ALLOWED",
            message = "El llamante fue admitido, pero la regla de propiedad de esta sesión no le permite continuarla",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = SESSION_CONTINUATION_REJECTED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )
        THROW failure
    END

    RETURN buildCallerSnapshot(snapshot, candidate)
END
```

```pseudocode
FUNCTION requireTenantCaller(
    execution: ExecutionContext
) -> Principal

    IF execution.caller == NULL
        OR execution.caller.current.principalType != USER
        OR execution.caller.current.tenantId == NULL

        THROW HarnessError(
            category = ADMISSION,
            code = "TENANT_CALLER_REQUIRED",
            message = "Esta operación exige un usuario verificado con tenant; el tenant nunca se toma del prompt ni de un argumento",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN execution.caller.current
END
```

`evaluateAdmissionForActivationRequest` es la función de CH-14 y no se modifica. `newEventId` y `now` son utilidades primitivas.

Nótese lo que estas funciones **no** hacen:
- ninguna verifica la firma de un token;
- ninguna autoriza una acción;
- ninguna lee el tenant del `ActivationRequest.payload` ni de un argumento del modelo.

## 12. Transiciones de Estado (State Transitions)

Este capítulo no cambia `AgentRunStatus`. Introduce la evolución del `CallerSnapshot` de un run:

```text
creación del run        → CallerSnapshot(initiator = P1, current = P1)
entrega de P1           → (initiator = P1, current = P1)
entrega de P2, permitida → (initiator = P1, current = P2)   — initiator nunca cambia
entrega de P3, no permitida → SESSION_CONTINUATION_REJECTED; el snapshot no cambia
```

Y la tabla de admisión:

```text
admissionConfigured = FALSE, DEVELOPMENT → ADMIT (principal RUNTIME sintético)
admissionConfigured = FALSE, PRODUCTION  → REJECT HARNESS_ADMISSION_NOT_CONFIGURED
configurado, sin principal verificado    → REJECT UNVERIFIED_CALLER
configurado, reglas de CH-14 rechazan    → REJECT (la decisión de CH-14)
configurado, reglas de CH-14 admiten     → ADMIT con principal verificado
```

## 13. Semántica de Fallos (Failure Semantics)

Cada fallo nuevo es un `HarnessError` de categoría `ADMISSION`:

```text
ADMISSION  HARNESS_ADMISSION_NOT_CONFIGURED   recoverable: FALSE, retryable: FALSE
           (arnés sin reglas, fuera de desarrollo — INV-E15)
ADMISSION  UNVERIFIED_CALLER                  recoverable: TRUE,  retryable: FALSE
           (sin identidad verificada; se recupera presentando una)
ADMISSION  SESSION_CONTINUATION_NOT_ALLOWED   recoverable: FALSE, retryable: FALSE
ADMISSION  TENANT_CALLER_REQUIRED             recoverable: FALSE, retryable: FALSE
```

Los dos primeros viajan como `reason` de un `AdmissionDecision` de `REJECT`, sin `AgentEvent`. Es el
mismo criterio de CH-14: antes de admitir no existe run al cual atribuir un evento.

## 14. Eventos Producidos (Events Produced)

```text
SESSION_CONTINUATION_REJECTED — un Principal admitido intentó continuar una sesión cuya regla
                                de propiedad no lo permite (payload: HarnessError)
```

La admisión en sí no emite eventos, igual que en CH-14: no hay run todavía. Su trazabilidad es la
auditoría de la decisión, que ya existe desde CH-26.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **El tenant nunca sale del texto.** `requireTenantCaller` es la única lectura válida. Una tool que
  toma el tenant de un argumento del modelo abre la puerta a que un prompt manipulado actúe sobre otra
  empresa (INV-E07).
- **Identidad no es autorización (P-13).** Un `Principal` dice quién es alguien, no qué puede
  hacer. Cada acción sigue pasando por `PolicyEngine`, que ahora puede usar `caller.current` en sus
  reglas.
- **Un arnés sin configurar no abre producción (INV-E15).** El modo `DEVELOPMENT` es un dato del
  proceso, fijado al arrancar. Ningún header ni campo del request puede activarlo.
- **La admisión no es propiedad de sesión.** Ser admitido no da derecho a continuar la sesión de
  otro. La regla es explícita (`SAME_PRINCIPAL` / `SAME_TENANT`) y no hay default permisivo.
- **El iniciador no hereda sus permisos a otros.** Las decisiones del turno usan `current`. Si una
  segunda persona escribe, el agente actúa con los permisos de esa segunda persona.
- **Los tokens nunca se guardan en el `Principal`.** Solo su resultado verificado. Las credenciales
  siguen siendo de `CredentialBroker` (INV-E08).

## 16. Tests (Tests)

```text
TEST UnconfiguredHarnessRejectsEveryActivationInProduction
TEST UnconfiguredHarnessAdmitsOnlyARuntimePrincipalInDevelopment
TEST ProcessModeNeverComesFromTheActivationRequest
TEST AdmissionWithoutVerifiedPrincipalIsRejectedAsUnverifiedCaller
TEST AdmitCarriesTheVerifiedPrincipalAndRejectCarriesNone
TEST InitiatorNeverChangesAcrossDeliveries
TEST CurrentIsRenewedOnEveryAcceptedDelivery
TEST SamePrincipalRuleRequiresSameIssuerAndPrincipalId
TEST SameTenantRuleRejectsCallersWithoutTenant
TEST RejectedContinuationEmitsSessionContinuationRejected
TEST RequireTenantCallerNeverReadsTheTenantFromThePrompt
TEST RequireTenantCallerRejectsServiceAndRuntimePrincipals
TEST PrincipalNeverStoresTheRawToken
TEST ExecutionContextV2IsBackwardCompatibleWithChaptersZeroToThirty
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.2 en curso, después de CH-31)

Contracts — 41
 ├── C-004 ExecutionContext v2     (CH-00 → modificado en CH-31: caller)
 ├── C-023 AdmissionDecision v2    (CH-14 → modificado en CH-31: principal)
 ├── C-040 Principal               (CH-31, nuevo)
 └── C-041 CallerSnapshot          (CH-31, nuevo)

Components — 22, sin cambios
 └── CMP-012 AdmissionController   (decisiones nuevas dentro de "identity, tenant")
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El protocolo de verificación** (OIDC, JWT, API key). Es un adaptador fuera del registro; el libro modela qué hace el arnés con el resultado.
- **Reglas de admisión que usen el principal.** `evaluateAdmissionForActivationRequest` (CH-14) sigue recibiendo solo el `ActivationRequest`. Que las reglas miren el tipo o el tenant del principal queda para la integración (CH-36), sin cambiar la firma de CH-14 en este capítulo.
- **Que `CredentialBroker`, `PolicyEngine` y la memoria usen `caller.current`.** El dato ya viaja; cablearlo es de la integración (CH-36) y de los capítulos de conexiones (CH-39) y datos (CH-40).
- **Reenviar la identidad a otro agente** (`forwardPrincipal`, con remitentes de confianza). Es de la invocación entre agentes (CH-42).
- **Auditar quién continuó cada sesión** (CH-19 ya tiene el mecanismo; falta conectarlo).

## 19. Siguiente Incremento (Next Increment)

Ahora el arnés sabe **quién** pide el trabajo. Lo que todavía no sabe es **qué parte del trabajo ya
está hecha** si el proceso se cae a mitad de un turno. P-23 exige ejecución durable, pero el libro no
tiene una unidad de recuperación más fina que el turno.

El siguiente capítulo introduce el **paso** como unidad de durabilidad (P-32):
- un registro por paso;
- la regla de que un paso comprometido nunca se re-ejecuta (INV-E16);
- la política de replay de CH-30 aplicada a los pasos interrumpidos.

Será CH-32 ("Pasos Durables y la Recuperación a Mitad de Turno"), el primer componente nuevo del Tramo 4. `next_chapter` queda en `null` porque CH-32 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): la identidad se pierde después de la admisión, las herramientas toman
   el tenant del texto, y un arnés sin configurar acepta a cualquiera.
2. **Patrones** (= §3): P-17 asigna la identidad, pero ningún contrato la lleva. Se reconstruye en
   cada lugar, con menos garantías cada vez.
3. **Estructuras** (= §8): `Principal` (C-040), `CallerSnapshot` (C-041) y `ExecutionContext` /
   `AdmissionDecision` v2, dentro del `owns` de `AdmissionController`, más una regla explícita de
   propiedad de sesión.
4. **Modelos mentales** (= §4): P-31, P-13 e INV-E15.

**Bucles de retroalimentación**

- **Refuerzo:** tomar el tenant de un argumento abre puertas, y cada incidente agrega validaciones
  ad hoc. Una sola fuente verificada corta la espiral.
- **Equilibrio:** INV-E15. Un arnés sin reglas no arranca abierto.

**Punto de apalancamiento**

La decisión con mayor efecto es que `Principal` (C-040) llegue a cada turno dentro de
`CallerSnapshot` (C-041), con `initiator` fijo y `current` renovado, y que `requireTenantCaller` sea
la única forma de obtener el tenant.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué devuelve `requireTenantCaller`, de qué campo del `ExecutionContext` v2 lo toma, y en qué
   casos lanza `TENANT_CALLER_REQUIRED`? *(pregunta guía 1)*
2. En un `CallerSnapshot`, ¿qué campo no cambia nunca y cuál se renueva en cada entrega, y qué hace
   `buildCallerSnapshot` cuando recibe un snapshot existente? *(pregunta guía 2)*
3. ¿Qué decide `admitWithVerifiedIdentity` cuando `admissionConfigured = FALSE`, según `processMode`,
   y por qué `processMode` no puede venir del `ActivationRequest`? *(pregunta guía 3)*
4. ¿Qué regla exige `continuationAllowedForCaller` para aceptar a un `Principal` en una sesión
   existente, y qué dos valores tiene `SessionOwnershipRule`? *(pregunta guía 4)*

### Explicar

1. `AdmissionController` posee "apply identity, authorization, tenant… decisions" (P-17). Explica
   por qué convertir una identidad ya verificada en un `Principal` le pertenece, y por qué NO le
   pertenece verificar la firma de un token ni autorizar una acción concreta.
2. Explica por qué `CallerSnapshot` distingue `initiator` de `current`, y qué se rompería si el agente
   siguiera actuando con los permisos del iniciador cuando otra persona escribe en la misma sesión.

### Conectar

1. `resolveCredentialReference` (CH-16) recibía un `agentId`, no un usuario. Con `ExecutionContext`
   v2, ¿qué campo usaría la integración para elegir la credencial correcta, y por qué nunca debería
   elegirse a partir de un argumento del modelo?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7 y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
