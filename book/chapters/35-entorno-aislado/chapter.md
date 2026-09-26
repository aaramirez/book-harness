---
id: CH-35
title: "El Entorno Aislado y las Credenciales que Solo Existen en el Egress"
starting_version: "0.1"
ending_version: "0.2"
introduces_components: [CMP-026]
introduces_contracts: [C-047, C-048]
modifies_contracts: []
constitutional_articles: [P-27, P-35, INV-05, INV-E07, INV-E08, INV-E20]
previous_chapter: CH-34
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH35
    text: |
      Al terminar este capítulo podrás decidir dónde corre el código que el modelo pide ejecutar,
      qué puede alcanzar por la red, y cómo ese código usa un servicio autenticado sin que ninguna
      credencial llegue nunca a estar dentro de su entorno.
  skeleton:
    id: SK-CH35
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
    components_to_be_introduced: [CMP-026]
    contracts_to_be_introduced: [C-047, C-048]
  guiding_questions:
    - id: GQ-CH35-01
      text: |
        Si el agente puede ejecutar comandos de shell y el proceso que lo corre tiene las claves de
        acceso a la base de datos, ¿qué impide que un comando las lea y las imprima?
      answered_by: RQ-CH35-01
    - id: GQ-CH35-02
      text: |
        Si el código que corre el agente necesita llamar a una API que exige una clave, ¿cómo puede
        hacerlo sin tener la clave?
      answered_by: RQ-CH35-02
    - id: GQ-CH35-03
      text: |
        ¿Debería el código que pide el modelo poder conectarse a cualquier dirección de internet?
        ¿Qué debería pasar con una dirección que nadie autorizó?
      answered_by: RQ-CH35-03
    - id: GQ-CH35-04
      text: |
        Decidir "en qué máquina corre" y decidir "qué puede hacer lo que corre ahí", ¿son la misma
        decisión?
      answered_by: RQ-CH35-04
  systems_lens:
    iceberg_visible_fact: |
      El código que el modelo pide ejecutar corre en el mismo proceso que guarda los secretos del
      arnés, y puede alcanzar cualquier dirección de red: un prompt manipulado basta para leer una
      clave y enviarla afuera (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que INV-E08 saca las credenciales del contexto del modelo, pero no
      del cómputo que el modelo controla; Article XII declara "sandboxing" como decisión
      determinística, y ningún componente es su dueño (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce IsolatedExecutionEnvironment (CMP-026), SandboxSession (C-047) y
      NetworkPolicy (C-048), y le da a CredentialBroker la resolución en el egress: un entorno por
      sesión sin secretos, una política de red explícita y credenciales que el borde agrega por nombre
      (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-35 (los secretos nunca entran al cómputo que controla el modelo),
      INV-E20 (las credenciales nunca se materializan dentro del entorno aislado) e INV-E08 (las
      credenciales las resuelve CredentialBroker) (ver sección 4).
    reinforcing_loop: |
      Si el código del agente puede leer secretos, cada tool nueva que ejecuta código amplía la
      superficie de fuga, y cada fuga se parcha filtrando la salida de esa tool concreta. Sacar los
      secretos del entorno corta la espiral: no hay nada que filtrar.
    balancing_loop: |
      La NetworkPolicy es el mecanismo de equilibrio: aunque el código intente salir a cualquier
      dirección, una ALLOW_LIST deniega todo lo que no nombra.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que una EgressRule de la NetworkPolicy (C-048)
      pida la credencial por nombre y el borde la inyecte con la CredentialReference que resuelve
      CredentialBroker, para que el valor del secreto nunca esté en la SandboxSession (C-047).
  recall_questions:
    - id: RQ-CH35-01
      text: |
        ¿Qué rechaza buildSandboxEnvironment y con qué error, y por qué el entorno aislado tiene un
        ciclo de vida separado del runtime que guarda los secretos?
    - id: RQ-CH35-02
      text: |
        ¿Qué decide decideEgress cuando la regla que coincide tiene credentialName, qué función de
        CredentialBroker actúa después, y qué recibe el proxy del borde?
    - id: RQ-CH35-03
      text: |
        ¿Qué decide decideEgress para un dominio que no aparece en las reglas, según el NetworkMode
        (DENY_ALL, ALLOW_ALL, ALLOW_LIST), y qué evento emite al denegar?
    - id: RQ-CH35-04
      text: |
        ¿Qué campo de SandboxSession enlaza con ExecutionPlacement (CH-21), y qué decide cada uno de
        los dos componentes?
  explain_prompts:
    - id: EP-CH35-01
      text: |
        ExecutionFabricAdapter e IsolatedExecutionEnvironment tratan ambos con "dónde corre el
        cómputo". Explica, como si hablaras con alguien sin contexto técnico, qué pregunta responde
        cada uno, y por qué un entorno aislado sigue haciendo falta aunque el run corra en una máquina
        dedicada.
      target_entity: CMP-026
    - id: EP-CH35-02
      text: |
        Explica por qué una EgressRule nombra la credencial en vez de contenerla, y qué se rompería si
        la NetworkPolicy guardara el valor del secreto.
      target_entity: C-048
  interleaved_questions:
    - id: IQ-CH35-01
      text: |
        En CH-16, resolveCredentialReference producía una CredentialReference opaca que nunca contiene
        el valor del secreto. ¿Qué agrega resolveEgressCredential, qué exige de la EgressDecision, y
        por qué no hace falta una función nueva para validar la credencial?
      current_chapter_entities: [C-047, C-048, CMP-026]
      prior_chapter_entities: [C-026, CMP-014]
      prior_chapter: CH-16
  flashcards:
    - id: FC-CH35-01
      front: |
        ¿Qué es una SandboxSession (C-047)?
      back: |
        El entorno aislado de una sesión, donde corre el código que el modelo pide. Tiene política de
        red, estado (OPEN / CLOSED), una referencia al entorno real y, opcionalmente, a su
        ExecutionPlacement. Nunca contiene credenciales (INV-E20).
      source_entity: C-047
      chapter_introduced_in: CH-35
      review_stage: DAY_1
    - id: FC-CH35-02
      front: |
        ¿Qué es una NetworkPolicy (C-048) y qué decide sobre un dominio no nombrado?
      back: |
        Qué puede alcanzar la red del entorno: DENY_ALL, ALLOW_ALL o ALLOW_LIST, con reglas por dominio
        que pueden pedir una credencial por nombre. Un dominio no nombrado se deniega con ALLOW_LIST y
        DENY_ALL, y se permite solo con ALLOW_ALL.
      source_entity: C-048
      chapter_introduced_in: CH-35
      review_stage: DAY_1
    - id: FC-CH35-03
      front: |
        ¿Qué posee IsolatedExecutionEnvironment (CMP-026) y qué no?
      back: |
        Posee el entorno aislado por sesión, la garantía de que no contiene credenciales y la decisión
        de egress. No posee dónde corre el cómputo (ExecutionFabricAdapter), resolver la credencial
        (CredentialBroker), autorizar (PolicyEngine) ni ejecutar la tool (ToolRuntime).
      source_entity: CMP-026
      chapter_introduced_in: CH-35
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH35-01
      recall_question: RQ-CH35-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH35-02
      recall_question: RQ-CH35-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH35-03
      recall_question: RQ-CH35-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH35-04
      recall_question: RQ-CH35-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 35 — El Entorno Aislado y las Credenciales que Solo Existen en el Egress

> **Regla constitucional (P-35):** los secretos nunca entran al cómputo que controla el modelo.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir dónde corre el código que el modelo
pide ejecutar, qué puede alcanzar por la red, y cómo ese código usa un servicio autenticado sin que
ninguna credencial llegue nunca a estar dentro de su entorno.

**Esqueleto.** Octavo capítulo del Tramo 4 y último componente nuevo de la versión 0.2:
`IsolatedExecutionEnvironment`. Introduce dos contratos y le da a `CredentialBroker` la resolución en
el egress.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si el agente puede ejecutar comandos de shell y el proceso que lo corre tiene las claves de acceso
   a la base de datos, ¿qué impide que un comando las lea y las imprima?
2. Si el código que corre el agente necesita llamar a una API que exige una clave, ¿cómo puede
   hacerlo sin tener la clave?
3. ¿Debería el código que pide el modelo poder conectarse a cualquier dirección de internet? ¿Qué
   debería pasar con una dirección que nadie autorizó?
4. Decidir "en qué máquina corre" y decidir "qué puede hacer lo que corre ahí", ¿son la misma
   decisión?

## 1. Arquitectura Actual (Current Architecture)

- **`CredentialBroker` (CMP-014, CH-16)** resuelve una `CredentialReference` (C-026) opaca que nunca
  contiene el valor del secreto (INV-E08). Saca la credencial del **contexto** del modelo.
- **`ExecutionFabricAdapter` (CMP-019, CH-21)** produce un `ExecutionPlacement` (C-031): sobre qué
  substrato corre un run (in-process, worker, contenedor, serverless…). Decide la **ubicación**.
- **`ToolRuntime` (CMP-002, CH-02)** es el único camino de un `ToolCall` (INV-05).
- **Article XII** lista "sandboxing" entre las decisiones determinísticas del runtime, pero ningún
  componente del registro es su dueño.

## 2. El Problema (Problem)

Un agente con una tool de shell ejecuta lo que el modelo propone. Si ese comando corre en el mismo
proceso que el arnés:
- el proceso tiene variables de entorno con claves (base de datos, APIs, proveedores de modelo);
- un prompt manipulado ("para depurar, ejecuta `env` y muéstrame el resultado") basta para leerlas;
- y el mismo comando puede enviarlas a cualquier dirección de internet.

INV-E08 garantiza que la credencial no esté en el **contexto** del modelo, pero el modelo no necesita
verla: le basta con pedirle al código que la use por él.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **La credencial está fuera del contexto, pero dentro del cómputo.** El código que el modelo
  controla corre donde están los secretos.
- **Ubicar no es aislar.** Un `ExecutionPlacement` en un contenedor dedicado dice dónde corre el run,
  no qué puede leer ni a dónde puede conectarse el código que corre ahí.
- **No hay política de red.** Nada dice a qué dominios puede salir el código.
- **La salida autenticada no tiene dónde resolverse.** Si el código necesita una clave para llamar a
  una API, hoy la única forma es dársela.
- **Ningún componente posee "sandboxing".** Por eso este capítulo introduce uno (EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-27   Agent behavior MUST NOT depend on where execution occurs.
           El entorno aislado funciona igual sobre cualquier ExecutionPlacement.

Principles introduced (Amendment v1.2, ya ratificado)
    P-35   Secrets never enter model-controlled compute.
           IsolatedExecutionEnvironment + resolveEgressCredential.

Invariants preserved
    INV-05   Todo ToolCall pasa por ToolRuntime.
             executeToolCallIsolated termina en executeToolCall (CH-02).
    INV-E07  Tenant data, memory, credentials … are isolated.
             Un entorno por sesión; nunca se comparte entre sesiones.
    INV-E08  Credentials are resolved by a CredentialBroker.
             La credencial del egress también la resuelve CredentialBroker.
    INV-E20  (Amendment v1.2) Credentials are never materialized inside the isolated
             execution environment.
             buildSandboxEnvironment rechaza cualquier credencial; EgressRule la nombra.

Component ownership changes
    Nuevo: IsolatedExecutionEnvironment (CMP-026), dueño de "sandboxing" (Article XII).
    CredentialBroker (CMP-014) gana resolveEgressCredential, dentro de INV-E08.

Contract changes
    Nuevos: C-047 SandboxSession, C-048 NetworkPolicy. Ninguno modificado.

Security implications
    El código que pide el modelo no puede leer secretos ni salir a dominios no autorizados
    (ver sección 15).

Observability implications
    Nuevos AgentEventType: SANDBOX_OPENED, SANDBOX_CLOSED y EGRESS_DENIED.

Deterministic vs agentic boundary
    El modelo propone qué ejecutar; el entorno, la red y las credenciales son determinísticos.
```

## 5. Conceptos Nuevos (New Concepts)

- **Entorno aislado** (*sandbox*): el lugar donde corre el código que el modelo pide (shell,
  archivos). Tiene un ciclo de vida **separado** del runtime del arnés: se abre para una sesión, se
  reusa en sus turnos y se cierra. El runtime tiene secretos; el entorno no.
- **Política de red**: qué puede alcanzar el entorno.
  - `DENY_ALL`: nada;
  - `ALLOW_ALL`: todo (para desarrollo o tareas sin riesgo);
  - `ALLOW_LIST`: solo los dominios que nombran las reglas.
- **Egress con credencial en el borde** (*brokered egress*): el código pide un dominio sin clave; la
  regla de ese dominio nombra una credencial; `CredentialBroker` la resuelve y el **proxy del borde**
  (fuera del entorno) la agrega a la petición. El código nunca ve el secreto.
- **Capability aislada**: una capability que debe ejecutarse dentro del entorno (típicamente shell y
  archivos). Cuáles lo son es configuración del agente.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `ToolCall` (C-008), `ToolResult` (C-009), `CapabilityDescriptor` (C-018),
  `CredentialReference` (C-026), `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError`
  (C-011);
- **primitivos:** `SessionId`, `AgentId`, `CapabilityId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `SandboxId` | identificador nuevo de un entorno aislado |
| `ExecutionPlacementId` | identificador de un `ExecutionPlacement` (heredado de CH-21) |
| `CredentialClassification` | `CONFIDENTIAL` / `RESTRICTED` (heredado de CH-16) |
| `AgentEventType` | se agregan `SANDBOX_OPENED`, `SANDBOX_CLOSED` y `EGRESS_DENIED` |
| `ErrorCategory` | reutiliza `EXECUTION_FABRIC` y `CREDENTIAL`, sin valores nuevos |

### `NetworkMode` y `EgressRule` — la forma de una política de red (embebidos)

```pseudocode
ENUM NetworkMode
    DENY_ALL
    ALLOW_ALL
    ALLOW_LIST
END
```

```pseudocode
STRUCT EgressRule
    domain: Text
    credentialName: Optional<Text>
    capability: Optional<CapabilityId>
END
```

`credentialName` es un **nombre**, nunca un valor. `capability` dice a qué capability pertenece esa
credencial, para que `CredentialBroker` la valide como en CH-16.

### `NetworkPolicy` — qué puede alcanzar el entorno (C-048)

```pseudocode
STRUCT NetworkPolicy
    mode: NetworkMode
    rules: List<EgressRule>
END
```

### `SandboxStatus` y `SandboxSession` — el entorno de una sesión (C-047)

```pseudocode
ENUM SandboxStatus
    OPEN
    CLOSED
END
```

```pseudocode
STRUCT SandboxSession
    sandboxId: SandboxId
    sessionId: SessionId
    networkPolicy: NetworkPolicy
    status: SandboxStatus
    environmentRef: Text
    placementRef: Optional<ExecutionPlacementId>
    openedAt: Timestamp
    closedAt: Optional<Timestamp>
END
```

`environmentRef` es una referencia opaca al entorno real (una máquina virtual, un contenedor), con el
mismo patrón que `computeResourceRef` en CH-21.

### `EgressRequest`, `EgressOutcome` y `EgressDecision` — una salida de red (embebidos)

```pseudocode
STRUCT EgressRequest
    sandboxId: SandboxId
    domain: Text
    requestedAt: Timestamp
END
```

```pseudocode
ENUM EgressOutcome
    ALLOW
    ALLOW_WITH_CREDENTIAL
    DENY
END
```

```pseudocode
STRUCT EgressDecision
    sandboxId: SandboxId
    domain: Text
    outcome: EgressOutcome
    credentialName: Optional<Text>
    capability: Optional<CapabilityId>
    decidedAt: Timestamp
END
```

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-047
Name:                   SandboxSession
Version:                v1
Introduced In:          CH-35
Used By:                [CMP-026]
Constitutional Impact:  [P-35, INV-E20]
```

```text
ID:                     C-048
Name:                   NetworkPolicy
Version:                v1
Introduced In:          CH-35
Used By:                [CMP-026]
Constitutional Impact:  [P-35, INV-E08, INV-E20]
```

`NetworkMode`, `EgressRule`, `SandboxStatus`, `EgressRequest`, `EgressOutcome` y `EgressDecision`
quedan embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

```pseudocode
COMPONENT IsolatedExecutionEnvironment
    consumes: ExecutionContext, ToolCall
    produces: SandboxSession, NetworkPolicy, AgentEvent, HarnessError
END
```

```text
COMPONENT: IsolatedExecutionEnvironment (CMP-026)

Responsibility:
    Abrir, reusar y cerrar, por sesión, el entorno aislado donde corre el código que el modelo
    pide; garantizar que ninguna credencial se materialice dentro de él; y decidir cada salida de
    red del entorno según su NetworkPolicy.

Owns:
    - "sandboxing" (Article XII — Deterministic Decisions)
    - "Credentials MUST remain outside both model context and the isolated environment where
      model-requested code executes" (P-35)
    - "Credentials are never materialized inside the isolated execution environment" (INV-E20)
    - aplicar la NetworkPolicy: DENY, ALLOW o ALLOW_WITH_CREDENTIAL, denegando por defecto
    - decidir si una capability se ejecuta dentro del entorno (lista configurada)

Does NOT own:
    - sobre qué substrato corre el cómputo (ExecutionFabricAdapter, CMP-019, CH-21). Es la frontera
      más importante del capítulo: ExecutionFabricAdapter decide DÓNDE corre un run;
      IsolatedExecutionEnvironment decide QUÉ PUEDE HACER y QUÉ PUEDE ALCANZAR el código que el
      modelo pide, dondequiera que corra.
    - resolver la credencial del egress (CredentialBroker, CMP-014, CH-16)
    - autorizar la tool call (PolicyEngine, CMP-005)
    - ejecutar la tool call (ToolRuntime, CMP-002; INV-05)
    - límites de recursos o presupuesto (ExecutionController, CMP-007)
    - el mecanismo real de aislamiento ni el proxy que inyecta la credencial (infraestructura)
```

**CredentialBroker (CMP-014)** gana `resolveEgressCredential`, dentro de su `owns` literal
"Credentials are resolved by a CredentialBroker" (INV-E08) y "garantizar … que el valor real del
secreto nunca aparezca en ningún dato que este componente produce". No valida nada nuevo: reusa
`resolveCredentialReference` (CH-16).

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
IsolatedExecutionEnvironment
    consumes → ExecutionContext, ToolCall
    produces → SandboxSession, NetworkPolicy, AgentEvent, HarnessError
    depends on (componentes) → (ninguno)
```

La integración (CH-36) encadena:
1. al empezar a usar capabilities aisladas en una sesión: `resolveExecutionPlacement` (CH-21) →
   `buildSandboxEnvironment` → `openSandboxSession` (reusa el de la sesión si ya está abierto);
2. para cada tool call: `mustRunIsolated` → `executeToolCallIsolated` → `executeToolCall` (CH-02);
3. para cada salida de red del entorno, el **proxy del borde** pregunta `decideEgress`:
   - `ALLOW`: deja pasar la petición tal cual;
   - `ALLOW_WITH_CREDENTIAL`: `resolveEgressCredential` → `CredentialReference` → el proxy agrega la
     credencial a la petición, **fuera** del entorno;
   - `DENY`: corta la conexión;
4. al terminar la sesión: `closeSandboxSession`.

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Integración → IsolatedExecutionEnvironment (abrir) → ToolRuntime (ejecutar dentro)
Código en el entorno → proxy del borde → IsolatedExecutionEnvironment (decideEgress) → CredentialBroker
```

**Vista 2 — Sequence: un comando que llama a una API con clave**

```text
Integración
   │ buildSandboxEnvironment(config, secretNames)          → entorno sin secretos
   │ openSandboxSession(sessionId, policy ALLOW_LIST, …)  → SandboxSession OPEN + SANDBOX_OPENED
   │ executeToolCallIsolated(call "shell", sandbox, …)     → executeToolCall (CH-02) dentro del entorno
   ▼
Código en el entorno: GET api.facturas.example            (sin clave)
Proxy del borde: decideEgress(sandbox, request)            → ALLOW_WITH_CREDENTIAL ("facturas-api")
CredentialBroker: resolveEgressCredential(decision, …)     → CredentialReference
Proxy del borde: agrega la credencial y sale                (el entorno nunca la vio)
```

**Vista 2b — Sequence: una salida no autorizada**

```text
Código en el entorno: POST exfiltra.example
Proxy del borde: decideEgress → DENY + EGRESS_DENIED        (ALLOW_LIST no nombra el dominio)
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION validateNetworkPolicy(
    policy: NetworkPolicy
) -> NetworkPolicy

    IF (policy.mode == ALLOW_LIST AND length(policy.rules) == 0)
        OR (policy.mode == DENY_ALL AND length(policy.rules) > 0)

        THROW HarnessError(
            category = EXECUTION_FABRIC,
            code = "INVALID_NETWORK_POLICY",
            message = "Una ALLOW_LIST necesita al menos una regla y una DENY_ALL no admite reglas",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN policy
END
```

```pseudocode
FUNCTION buildSandboxEnvironment(
    config: Map<Text, Value>,
    secretNames: List<Text>
) -> Map<Text, Value>

    FOR EACH name IN secretNames
        IF hasKey(config, name)
            THROW HarnessError(
                category = EXECUTION_FABRIC,
                code = "SECRET_IN_SANDBOX_ENVIRONMENT",
                message = "La configuración del entorno aislado nombra una credencial; las credenciales solo existen en el borde",
                recoverable = FALSE,
                retryable = FALSE,
                metadata = {}
            )
        END
    END

    RETURN config
END
```

```pseudocode
FUNCTION openSandboxSession(
    sessionId: SessionId,
    policy: NetworkPolicy,
    existing: Optional<SandboxSession>,
    environmentRef: Text,
    placementRef: Optional<ExecutionPlacementId>,
    execution: ExecutionContext,
    agentId: AgentId
) -> SandboxSession

    IF existing != NULL AND existing.status == OPEN AND existing.sessionId == sessionId
        RETURN existing
    END

    validated: NetworkPolicy = validateNetworkPolicy(policy)

    sandbox: SandboxSession = SandboxSession(
        sandboxId = newSandboxId(),
        sessionId = sessionId,
        networkPolicy = validated,
        status = OPEN,
        environmentRef = environmentRef,
        placementRef = placementRef,
        openedAt = now(),
        closedAt = NULL
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = SANDBOX_OPENED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = sandbox
    )

    RETURN sandbox
END
```

```pseudocode
FUNCTION matchEgressRule(
    policy: NetworkPolicy,
    domain: Text
) -> Optional<EgressRule>

    FOR EACH rule IN policy.rules
        IF rule.domain == domain
            RETURN rule
        END
    END

    RETURN NULL
END
```

```pseudocode
FUNCTION decideEgress(
    sandbox: SandboxSession,
    request: EgressRequest,
    execution: ExecutionContext,
    agentId: AgentId
) -> EgressDecision

    outcome: EgressOutcome = DENY
    credentialName: Optional<Text> = NULL
    capability: Optional<CapabilityId> = NULL

    IF sandbox.status == OPEN AND request.sandboxId == sandbox.sandboxId
        AND sandbox.networkPolicy.mode != DENY_ALL

        rule: Optional<EgressRule> = matchEgressRule(sandbox.networkPolicy, request.domain)

        IF rule != NULL AND rule.credentialName != NULL
            outcome = ALLOW_WITH_CREDENTIAL
            credentialName = rule.credentialName
            capability = rule.capability
        ELSE
            IF rule != NULL OR sandbox.networkPolicy.mode == ALLOW_ALL
                outcome = ALLOW
            END
        END
    END

    decision: EgressDecision = EgressDecision(
        sandboxId = request.sandboxId,
        domain = request.domain,
        outcome = outcome,
        credentialName = credentialName,
        capability = capability,
        decidedAt = now()
    )

    IF outcome == DENY
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = EGRESS_DENIED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = decision
        )
    END

    RETURN decision
END
```

```pseudocode
FUNCTION resolveEgressCredential(
    decision: EgressDecision,
    descriptor: CapabilityDescriptor,
    classification: CredentialClassification,
    credentialBelongsToCapability: Boolean,
    secretExists: Boolean,
    expiresAt: Optional<Timestamp>,
    execution: ExecutionContext,
    agentId: AgentId
) -> CredentialReference

    IF decision.outcome != ALLOW_WITH_CREDENTIAL OR decision.capability != descriptor.capability
        THROW HarnessError(
            category = CREDENTIAL,
            code = "EGRESS_DOES_NOT_REQUIRE_THIS_CREDENTIAL",
            message = "Solo se resuelve una credencial de egress para una decisión ALLOW_WITH_CREDENTIAL de la misma capability",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN resolveCredentialReference(
        descriptor, decision.credentialName, classification,
        credentialBelongsToCapability, secretExists, expiresAt, execution, agentId
    )
END
```

```pseudocode
FUNCTION mustRunIsolated(
    call: ToolCall,
    isolatedCapabilities: List<CapabilityId>
) -> Boolean

    FOR EACH capability IN isolatedCapabilities
        IF call.capability == capability
            RETURN TRUE
        END
    END

    RETURN FALSE
END
```

```pseudocode
FUNCTION closeSandboxSession(
    sandbox: SandboxSession,
    execution: ExecutionContext,
    agentId: AgentId
) -> SandboxSession

    IF sandbox.status == CLOSED
        RETURN sandbox
    END

    closed: SandboxSession = SandboxSession(
        sandboxId = sandbox.sandboxId,
        sessionId = sandbox.sessionId,
        networkPolicy = sandbox.networkPolicy,
        status = CLOSED,
        environmentRef = sandbox.environmentRef,
        placementRef = sandbox.placementRef,
        openedAt = sandbox.openedAt,
        closedAt = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = SANDBOX_CLOSED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = closed
    )

    RETURN closed
END
```

La función de integración que conecta el entorno con `ToolRuntime`:

```pseudocode
FUNCTION executeToolCallIsolated(
    call: ToolCall,
    sandbox: Optional<SandboxSession>,
    isolatedCapabilities: List<CapabilityId>,
    execution: ExecutionContext,
    agentId: AgentId,
    capabilityResolved: Boolean,
    inputValid: Boolean,
    executionSucceeded: Boolean,
    executionOutput: Value
) -> ToolResult

    IF mustRunIsolated(call, isolatedCapabilities)
        AND (sandbox == NULL OR sandbox.status != OPEN OR sandbox.sessionId != execution.sessionId)

        THROW HarnessError(
            category = EXECUTION_FABRIC,
            code = "ISOLATED_ENVIRONMENT_REQUIRED",
            message = "Esta capability solo se ejecuta dentro del entorno aislado abierto de su propia sesión",
            recoverable = TRUE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN executeToolCall(
        call, execution, agentId, capabilityResolved, inputValid, executionSucceeded, executionOutput
    )
END
```

`newSandboxId`, `newEventId`, `now`, `length` y `hasKey` son utilidades primitivas. En
`executeToolCallIsolated`, que la ejecución ocurra físicamente dentro del entorno (`environmentRef`)
es infraestructura: la función garantiza que no ocurra **sin** él.

Nótese lo que estas funciones **no** hacen:
- ninguna guarda ni devuelve el valor de un secreto: la regla nombra, `CredentialBroker` referencia
  y el proxy inyecta;
- ninguna decide en qué máquina corre el entorno: `placementRef` apunta a la decisión de CH-21;
- ninguna autoriza la tool: `PolicyEngine` ya decidió antes de `executeToolCallIsolated`.

## 12. Transiciones de Estado (State Transitions)

El ciclo de vida de una `SandboxSession`:

```text
openSandboxSession (sin entorno abierto)  → OPEN    (SANDBOX_OPENED)
openSandboxSession (ya abierto)           → OPEN    (se reusa, sin evento)
closeSandboxSession                       → CLOSED  (SANDBOX_CLOSED)
closeSandboxSession (ya cerrado)          → CLOSED  (idempotente)
```

Y la tabla de `decideEgress`:

```text
entorno cerrado u otro entorno                 → DENY
DENY_ALL                                       → DENY
regla del dominio con credentialName           → ALLOW_WITH_CREDENTIAL
regla del dominio sin credentialName           → ALLOW
sin regla, ALLOW_ALL                           → ALLOW
sin regla, ALLOW_LIST                          → DENY
```

## 13. Semántica de Fallos (Failure Semantics)

```text
EXECUTION_FABRIC  INVALID_NETWORK_POLICY                   recoverable: FALSE, retryable: FALSE
EXECUTION_FABRIC  SECRET_IN_SANDBOX_ENVIRONMENT            recoverable: FALSE, retryable: FALSE
EXECUTION_FABRIC  ISOLATED_ENVIRONMENT_REQUIRED            recoverable: TRUE,  retryable: FALSE
                  (se recupera abriendo el entorno de la sesión)
CREDENTIAL        EGRESS_DOES_NOT_REQUIRE_THIS_CREDENTIAL  recoverable: FALSE, retryable: FALSE
```

`resolveEgressCredential` hereda, además, los fallos de `resolveCredentialReference` (CH-16):
credencial que no corresponde a la capability, inexistente o vencida.

Un egress denegado **no** es un `HarnessError` del run: la conexión se corta y la tool recibe un
fallo de red, que vuelve al modelo como cualquier `ToolResult` fallido (INV-07).

## 14. Eventos Producidos (Events Produced)

```text
SANDBOX_OPENED  — se abrió el entorno aislado de una sesión (payload: SandboxSession)
SANDBOX_CLOSED  — se cerró (payload: SandboxSession)
EGRESS_DENIED   — una salida de red del entorno fue denegada (payload: EgressDecision)
```

Las salidas permitidas no emiten eventos: serían demasiadas y no son decisiones de riesgo. Quedan en
la telemetría del proxy (CH-44).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **No hay nada que leer.** El entorno no tiene variables con secretos: `buildSandboxEnvironment`
  rechaza la configuración que nombre una credencial. Un `env` dentro del entorno no revela nada.
- **La credencial se usa sin verse.** El proxy del borde la agrega a la petición que sale; el código
  del entorno solo ve la respuesta.
- **La credencial solo va a su dominio.** Una regla une un dominio con una credencial: la clave de la
  API de facturas nunca se agrega a una petición a otro dominio.
- **Denegar por defecto.** Con `ALLOW_LIST`, lo que no está nombrado no sale. `ALLOW_ALL` existe, pero
  es una decisión explícita, no un olvido.
- **Un entorno por sesión.** Dos sesiones, aunque sean del mismo agente, nunca comparten entorno
  (INV-E07): los archivos de una no son visibles para la otra.
- **Aislar no reemplaza autorizar.** Que un comando corra en un entorno aislado no lo vuelve
  permitido: `PolicyEngine` decide antes.

## 16. Tests (Tests)

```text
TEST AllowListWithoutRulesIsInvalid
TEST DenyAllWithRulesIsInvalid
TEST SandboxEnvironmentNamingASecretIsRejected
TEST OpenSandboxIsReusedForTheSameSession
TEST SandboxIsNeverSharedBetweenSessions
TEST DenyAllDeniesEveryDomain
TEST AllowListDeniesUnnamedDomains
TEST AllowAllAllowsUnnamedDomains
TEST RuleWithCredentialNameAllowsWithCredential
TEST ClosedSandboxDeniesEveryEgress
TEST EgressDenialEmitsEgressDenied
TEST EgressCredentialIsResolvedOnlyForItsOwnCapability
TEST EgressCredentialReusesCredentialBrokerValidation
TEST IsolatedCapabilityWithoutOpenSandboxIsRejected
TEST NonIsolatedCapabilityRunsWithoutSandbox
TEST NoDataProducedContainsASecretValue
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.2 en curso, después de CH-35)

Components — 26
 ├── CMP-014 CredentialBroker              (+ resolveEgressCredential)
 └── CMP-026 IsolatedExecutionEnvironment  (CH-35, nuevo — plano Execution Fabric)

Contracts — 48
 ├── C-047 SandboxSession                  (CH-35, nuevo)
 └── C-048 NetworkPolicy                   (CH-35, nuevo)

Los cuatro componentes nuevos de v0.2 están completos: ExecutionJournal (CH-32),
ResumptionCoordinator (CH-33), ContinuationRegistry (CH-34), IsolatedExecutionEnvironment (CH-35).
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **El mecanismo real de aislamiento** (máquina virtual ligera, contenedor, proceso restringido) y el
  proxy que inyecta la credencial: infraestructura de borde.
- **Un tipo de capability en el descriptor.** Hoy las capabilities aisladas son una lista
  configurada; un campo en `CapabilityDescriptor` sería otra versión de C-018, que CH-39 ya lleva a
  v3.
- **Transformaciones más ricas en el egress** (reescribir rutas, limitar métodos): la regla solo
  une dominio y credencial.
- **Límites de CPU, memoria y disco del entorno:** son presupuesto (ExecutionController, CH-41).
- **Aislamiento de las corridas de evaluación:** CH-45 reusa este entorno.

## 19. Siguiente Incremento (Next Increment)

La versión 0.2 ya tiene todas sus piezas: pasos durables, esperas estacionadas, direcciones de
continuación, identidad en cada turno y un entorno sin secretos. Pero ninguna función las usa juntas
todavía: cada capítulo dejó su cableado para "la integración".

El siguiente capítulo es esa integración, **`runDurableGovernedTurn`**: un turno que entra por un
canal con dirección, se admite con identidad verificada, se registra paso a paso, se estaciona sin
cómputo cuando espera, ejecuta el código del modelo en el entorno aislado y se recupera de una caída
sin repetir lo comprometido.

Será CH-36 ("Integración: el Turno Durable Gobernado"). `next_chapter` queda en `null` porque CH-36
todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): el código que pide el modelo corre donde están los secretos y puede
   salir a cualquier dirección.
2. **Patrones** (= §3): INV-E08 saca las credenciales del contexto pero no del cómputo; "sandboxing"
   no tiene dueño.
3. **Estructuras** (= §8): `IsolatedExecutionEnvironment` (CMP-026), `SandboxSession` (C-047),
   `NetworkPolicy` (C-048) y `resolveEgressCredential`.
4. **Modelos mentales** (= §4): P-35, INV-E20 e INV-E08.

**Bucles de retroalimentación**

- **Refuerzo:** cada tool que ejecuta código amplía la superficie de fuga. Sin secretos en el
  entorno, no hay nada que filtrar.
- **Equilibrio:** la `NetworkPolicy`. Una `ALLOW_LIST` deniega todo lo que no nombra.

**Punto de apalancamiento**

La decisión con mayor efecto es que una `EgressRule` (C-048) pida la credencial por nombre y el
borde la inyecte con la `CredentialReference` de `CredentialBroker`, para que el secreto nunca esté
en la `SandboxSession` (C-047).

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué rechaza `buildSandboxEnvironment` y con qué error, y por qué el entorno aislado tiene un
   ciclo de vida separado del runtime que guarda los secretos? *(pregunta guía 1)*
2. ¿Qué decide `decideEgress` cuando la regla que coincide tiene `credentialName`, qué función de
   `CredentialBroker` actúa después, y qué recibe el proxy del borde? *(pregunta guía 2)*
3. ¿Qué decide `decideEgress` para un dominio que no aparece en las reglas, según el `NetworkMode`, y
   qué evento emite al denegar? *(pregunta guía 3)*
4. ¿Qué campo de `SandboxSession` enlaza con `ExecutionPlacement` (CH-21), y qué decide cada uno de
   los dos componentes? *(pregunta guía 4)*

### Explicar

1. `ExecutionFabricAdapter` e `IsolatedExecutionEnvironment` tratan ambos con "dónde corre el
   cómputo". Explica qué pregunta responde cada uno, y por qué un entorno aislado sigue haciendo
   falta aunque el run corra en una máquina dedicada.
2. Explica por qué una `EgressRule` nombra la credencial en vez de contenerla, y qué se rompería si la
   `NetworkPolicy` guardara el valor del secreto.

### Conectar

1. En CH-16, `resolveCredentialReference` producía una `CredentialReference` opaca que nunca contiene
   el valor del secreto. ¿Qué agrega `resolveEgressCredential`, qué exige de la `EgressDecision`, y
   por qué no hace falta una función nueva para validar la credencial?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
