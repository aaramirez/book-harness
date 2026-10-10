---
id: CH-41
title: "Conexiones: MCP y OpenAPI como Fuentes de Capabilities"
starting_version: "0.2.1"
ending_version: "0.3"
introduces_components: [CMP-028]
introduces_contracts: [C-054]
modifies_contracts: [C-018]
constitutional_articles: [P-03, P-27, P-38, INV-04, INV-05, INV-06, INV-E08, INV-E25]
previous_chapter: CH-40
next_chapter: CH-42
retrieval_set:
  expected_outcome:
    id: EO-CH41
    text: |
      Al terminar este capítulo podrás decidir cómo entra al arnés una herramienta que vive en un
      servidor MCP o en una API OpenAPI, qué ve el modelo de ella y qué no, y explicar por qué recorre
      el mismo camino de resolución, política y ejecución que una herramienta propia.
  skeleton:
    id: SK-CH41
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
    components_to_be_introduced: [CMP-028]
    contracts_to_be_introduced: [C-054]
  guiding_questions:
    - id: GQ-CH41-01
      text: |
        Si un servidor externo publica veinte herramientas, ¿debería el modelo verlas todas? ¿Y si dos
        servidores tienen una herramienta con el mismo nombre?
      answered_by: RQ-CH41-01
    - id: GQ-CH41-02
      text: |
        Una API necesita un identificador de cuenta que el modelo no debería poder cambiar. ¿Dónde vive
        ese dato, y qué pasa si el modelo intenta enviarlo igual?
      answered_by: RQ-CH41-02
    - id: GQ-CH41-03
      text: |
        Si una conexión usa la cuenta de cada usuario y no una cuenta compartida, ¿de dónde sale la
        credencial, y qué pasa si el usuario todavía no la conectó?
      answered_by: RQ-CH41-03
    - id: GQ-CH41-04
      text: |
        ¿Debería una herramienta externa poder saltarse la política porque "el servidor ya la
        controla"? ¿Y repetirse automáticamente si no se sabe si se ejecutó?
      answered_by: RQ-CH41-04
  systems_lens:
    iceberg_visible_fact: |
      Las herramientas de servidores MCP y de APIs OpenAPI no tienen cómo entrar al arnés: o se
      escriben a mano como capabilities locales, o se le dan al modelo por fuera de CapabilityRegistry
      y PolicyEngine (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que P-38 exige que las capabilities externas entren por conexiones
      declaradas, pero CapabilityDescriptor no sabe de dónde viene una capability, ni si se ejecuta
      local, aislada o en una conexión; y la lista de capabilities aisladas de CH-35 es configuración
      suelta (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce ConnectionManager (CMP-028) y ConnectionDescriptor (C-054), y lleva
      CapabilityDescriptor (C-018) a v3 con sourceConnectionId y executionKind (ADR-005): cada tool
      externa se traduce a un descriptor con espacio de nombres y recorre el camino de siempre (ver
      sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-38 (las capabilities externas entran solo por conexiones declaradas),
      INV-E25 (ninguna tool externa llega al modelo sin CapabilityRegistry y PolicyEngine), INV-E08 (la
      credencial la resuelve CredentialBroker) y P-27 (el protocolo es un adaptador) (ver sección 4).
    reinforcing_loop: |
      Si cada servidor externo se conecta a su manera, cada integración nueva agrega un camino con sus
      propias reglas de permisos y credenciales, y el modelo termina viendo herramientas que nadie
      autorizó. Un solo camino — conexión declarada, descriptor, registro, política — corta la espiral.
    balancing_loop: |
      El filtro de tools de la conexión es el mecanismo de equilibrio: por muchas herramientas que
      publique un servidor, el modelo solo ve las que la conexión permite.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que ConnectionManager (CMP-028) solo produzca
      CapabilityDescriptor: así una tool externa no tiene un camino propio, y la resolución, la política,
      la credencial, el aislamiento y el replay se aplican igual que a una tool local.
  recall_questions:
    - id: RQ-CH41-01
      text: |
        ¿Qué hace translateConnectionTools con una tool fuera del filtro y con una cuyo nombre colisiona
        con una capability local, y qué forma tiene el identificador de una capability traducida?
    - id: RQ-CH41-02
      text: |
        ¿Qué hace translateConnectionTools con los argumentos provistos al armar el schema, qué hace
        prepareConnectionCall con ellos, y qué error lanza si el modelo intenta fijarlos?
    - id: RQ-CH41-03
      text: |
        ¿Qué función usa resolveConnectionCredential según el credentialScope, y qué capítulo maneja el
        caso en que la credencial del usuario todavía no existe?
    - id: RQ-CH41-04
      text: |
        ¿Qué hace applyConnectionApprovalDefault con un ALLOW, qué replayPolicy tiene una tool traducida,
        y qué devuelve effectiveExecutionKind para un descriptor con sourceConnectionId y executionKind
        NULL?
  explain_prompts:
    - id: EP-CH41-01
      text: |
        CapabilityRegistry ya registraba y resolvía capabilities. Explica, como si hablaras con alguien
        sin contexto técnico, por qué traducir las tools de una conexión es una decisión distinta que
        merece un componente, y por qué ese componente no resuelve ni autoriza nada.
      target_entity: CMP-028
    - id: EP-CH41-02
      text: |
        Explica por qué un ConnectionDescriptor separa los argumentos provistos del schema que ve el
        modelo, y qué ataque permitiría dejarlos en el schema.
      target_entity: C-054
  interleaved_questions:
    - id: IQ-CH41-01
      text: |
        En CH-35, mustRunIsolated decidía con una lista configurada qué capabilities corrían en el
        entorno aislado. ¿Qué la reemplaza con CapabilityDescriptor v3, cómo se deriva el valor cuando
        el descriptor no lo declara, y por qué una tool de conexión no corre en el entorno aislado?
      current_chapter_entities: [C-054, CMP-028]
      prior_chapter_entities: [C-047, CMP-026]
      prior_chapter: CH-35
  flashcards:
    - id: FC-CH41-01
      front: |
        ¿Qué es un ConnectionDescriptor (C-054)?
      back: |
        Una conexión declarada a un servidor MCP o una API OpenAPI: transporte, filtro de tools,
        argumentos provistos (ocultos al modelo), credencial compartida o por llamante, y aprobación
        por defecto. Solo por una conexión declarada entra una capability externa (P-38).
      source_entity: C-054
      chapter_introduced_in: CH-41
      review_stage: DAY_1
    - id: FC-CH41-02
      front: |
        ¿Qué posee ConnectionManager (CMP-028) y qué no?
      back: |
        Posee traducir las tools permitidas de una conexión en CapabilityDescriptor <conexión>__<tool>,
        el filtro y los argumentos provistos. No resuelve (CapabilityRegistry), no autoriza
        (PolicyEngine), no ejecuta (ToolRuntime), no resuelve credenciales (CredentialBroker) ni habla
        el protocolo (adaptador).
      source_entity: CMP-028
      chapter_introduced_in: CH-41
      review_stage: DAY_1
    - id: FC-CH41-03
      front: |
        ¿Qué agrega CapabilityDescriptor v3 (C-018)?
      back: |
        sourceConnectionId (de qué conexión viene; NULL = local) y executionKind (LOCAL, ISOLATED,
        CONNECTION), que reemplaza la lista isolatedCapabilities de CH-35. Si executionKind es NULL, se
        deriva CONNECTION o LOCAL.
      source_entity: C-018
      chapter_introduced_in: CH-41
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH41-01
      recall_question: RQ-CH41-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH41-02
      recall_question: RQ-CH41-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH41-03
      recall_question: RQ-CH41-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH41-04
      recall_question: RQ-CH41-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 41 — Conexiones: MCP y OpenAPI como Fuentes de Capabilities

> **Regla constitucional (P-38):** las capabilities de sistemas externos entran solo por conexiones
> declaradas, y se resuelven como cualquier capability.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir cómo entra al arnés una herramienta
que vive en un servidor MCP o en una API OpenAPI, qué ve el modelo de ella y qué no. También podrás
explicar por qué recorre el mismo camino de resolución, política y ejecución que una herramienta
propia.

**Esqueleto.** Tercer capítulo de la versión 0.3. Introduce el componente `ConnectionManager` y un
contrato, y lleva `CapabilityDescriptor` a v3 (ADR-005).

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si un servidor externo publica veinte herramientas, ¿debería el modelo verlas todas? ¿Y si dos
   servidores tienen una herramienta con el mismo nombre?
2. Una API necesita un identificador de cuenta que el modelo no debería poder cambiar. ¿Dónde vive ese
   dato, y qué pasa si el modelo intenta enviarlo igual?
3. Si una conexión usa la cuenta de cada usuario y no una cuenta compartida, ¿de dónde sale la
   credencial, y qué pasa si el usuario todavía no la conectó?
4. ¿Debería una herramienta externa poder saltarse la política porque "el servidor ya la controla"?
   ¿Y repetirse automáticamente si no se sabe si se ejecutó?

## 1. Arquitectura Actual (Current Architecture)

- **`CapabilityRegistry` (CMP-008, CH-08)** registra y resuelve capabilities descritas por un
  `CapabilityDescriptor` (C-018, v2 desde CH-30), todas implementadas localmente
  (`implementationRef`).
- **`PolicyEngine` (CH-05)** autoriza cada tool call; **`ToolRuntime` (CH-02)** la ejecuta
  (INV-05, INV-06).
- **`CredentialBroker` (CH-16, CH-35, CH-37, CH-38)** resuelve la credencial, compartida o del usuario
  que llama, y abre una autorización interactiva si falta.
- **`IsolatedExecutionEnvironment` (CH-35)** decide con una **lista configurada**
  (`isolatedCapabilities`) qué capabilities corren aisladas; la deuda D-025 pedía reemplazarla por un
  dato del descriptor.
- **P-38** exige conexiones declaradas, y **INV-E25** que ninguna tool externa llegue al modelo sin
  pasar por `CapabilityRegistry` y `PolicyEngine`. Ningún componente las hace cumplir todavía.

## 2. El Problema (Problem)

Las herramientas útiles de un agente real viven afuera: un servidor que expone el sistema de tickets,
una API de facturación descrita en OpenAPI, un servidor de búsqueda. Hoy hay dos opciones, y las dos
son malas:
- **escribir cada herramienta a mano** como capability local, y mantenerla sincronizada con el
  servidor;
- **darle al modelo las herramientas del servidor directamente**, por fuera de `CapabilityRegistry`
  y `PolicyEngine`.

Además:
- un servidor publica veinte herramientas y el agente necesita tres;
- dos servidores tienen una herramienta `search`;
- una API exige un identificador de cuenta que el modelo no debería poder cambiar;
- la credencial puede ser la de la empresa o la de cada usuario.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **`CapabilityDescriptor` no sabe de dónde viene una capability.** Sin eso, ni la política, ni la
  credencial, ni la auditoría pueden distinguir una herramienta propia de una externa (INV-E10).
- **No sabe cómo se ejecuta.** Local, en el entorno aislado o en una conexión: hoy la diferencia es
  una lista suelta (CH-35) o código del adapter.
- **No hay dónde declarar una conexión:** su transporte, su filtro, sus argumentos fijos, su
  credencial.
- **Ningún componente posee la decisión** "¿qué herramientas de este servidor entran, con qué nombre
  y con qué schema?". No es de `CapabilityRegistry` (resuelve lo registrado), ni de `ToolRuntime`
  (ejecuta), ni de `CredentialBroker` (credenciales). Por eso este capítulo introduce un componente
  (EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-03   Tools are explicit capabilities, not prompt tricks.
           Una tool externa es un CapabilityDescriptor explícito, con schema validable.
    P-27   El comportamiento no depende de dónde se ejecuta.
           MCP y OpenAPI son adaptadores; el núcleo no depende de ningún SDK.

Principles introduced (Amendment v1.2, ya ratificado)
    P-38   External capabilities enter only through declared connections.
           ConnectionDescriptor + translateConnectionTools.

Invariants preserved
    INV-04   Todo ToolCall se valida antes de ejecutarse.
             CapabilityRegistry valida contra el schema traducido.
    INV-05   Todo ToolCall pasa por ToolRuntime.
             La tool de conexión se ejecuta por ToolRuntime con una ConnectionInvocation.
    INV-06   Todo side effect pasa por PolicyEngine.
             La aprobación por defecto de la conexión solo restringe la decisión de PolicyEngine.
    INV-E08  Credentials are resolved by a CredentialBroker.
             La credencial de la conexión, compartida o del llamante, la resuelve CredentialBroker.
    INV-E25  (Amendment v1.2) No external tool reaches the model except as a CapabilityDescriptor
             resolved by CapabilityRegistry and evaluated by PolicyEngine.
             ConnectionManager solo produce descriptores.

Component ownership changes
    Nuevo: ConnectionManager (CMP-028).
    CapabilityRegistry gana effectiveExecutionKind; IsolatedExecutionEnvironment, requiresIsolation;
    PolicyEngine, applyConnectionApprovalDefault.

Contract changes
    Nuevo: C-054 ConnectionDescriptor.
    C-018 CapabilityDescriptor v2 → v3 (+ sourceConnectionId, + executionKind; ADR-005 Accepted).

Security implications
    El modelo nunca ve una tool fuera del filtro ni un argumento provisto (ver sección 15).

Deterministic vs agentic boundary
    Sin cambios: el modelo propone usar una capability; la traducción, el filtro y la política
    son determinísticos.
```

## 5. Conceptos Nuevos (New Concepts)

- **Conexión declarada:** un proveedor externo de herramientas registrado con un
  `ConnectionDescriptor`. Puede ser un servidor **MCP** (por `STDIO` o `HTTP`) o una especificación
  **OpenAPI**.
- **Traducción a capability:** cada herramienta permitida de la conexión se vuelve un
  `CapabilityDescriptor` con espacio de nombres `<conexión>__<tool>` (por ejemplo, `tickets__search` y
  `docs__search` no chocan).
- **Filtro de tools:** una lista de herramientas permitidas (`ALLOW_LIST`) o bloqueadas
  (`BLOCK_LIST`). El modelo solo ve lo que el filtro deja pasar.
- **Argumento provisto:** un valor que la conexión fija (un identificador de cuenta, una región) y que
  el modelo nunca ve. Se quita del schema y se agrega al preparar la invocación.
- **Alcance de la credencial:** `SHARED` (una cuenta de la empresa) o `PER_CALLER` (la cuenta de cada
  usuario, que se resuelve para `caller.current`).
- **Tipo de ejecución:** `LOCAL`, `ISOLATED` (en el entorno aislado, CH-35) o `CONNECTION` (en el
  proveedor externo). Lo declara el descriptor; si no, se deriva.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `CapabilityDescriptor` (C-018, que pasa a v3), `ToolCall` (C-008), `PolicyDecision`
  (C-014), `CredentialReference` (C-026), `ExecutionContext` (C-004), `HarnessError` (C-011);
- **primitivos:** `CapabilityId`, `ToolCallId`, `AgentId`, `Timestamp`.

| Identificador (heredado o nuevo, sin `C-XXX` propio) | Rol en este capítulo |
|---|---|
| `ConnectionId` | identificador nuevo de una conexión |
| `ReplayPolicy` | `NEVER` / `SAFE` (C-039, CH-30) |
| `CredentialClassification` | clasificación de la credencial (CH-16) |
| `ErrorCategory` | reutiliza `VALIDATION` y `POLICY` |

### Partes de una conexión (embebidas)

```pseudocode
ENUM ConnectionKind
    MCP
    OPENAPI
END
```

```pseudocode
ENUM ConnectionTransport
    STDIO
    HTTP
END
```

```pseudocode
ENUM FilterMode
    ALLOW_LIST
    BLOCK_LIST
END
```

```pseudocode
STRUCT ToolFilter
    mode: FilterMode
    names: List<Text>
END
```

```pseudocode
ENUM CredentialScope
    SHARED
    PER_CALLER
END
```

### `ConnectionDescriptor` — una conexión declarada (C-054)

```pseudocode
STRUCT ConnectionDescriptor
    connectionId: ConnectionId
    kind: ConnectionKind
    transport: ConnectionTransport
    endpointRef: Text
    toolFilter: ToolFilter
    providedArguments: Map<Text, Value>
    credentialName: Optional<Text>
    credentialScope: CredentialScope
    requiresApprovalByDefault: Boolean
END
```

`endpointRef` es una referencia opaca (un comando para `STDIO`, una URL para `HTTP`, la ubicación de la
especificación para `OPENAPI`), con el mismo patrón que `implementationRef` en CH-08.

### `ExecutionKind` y `CapabilityDescriptor` — versión 3 (C-018)

```pseudocode
ENUM ExecutionKind
    LOCAL
    ISOLATED
    CONNECTION
END
```

```pseudocode
STRUCT CapabilityDescriptor
    capability: CapabilityId
    name: Text
    version: Text
    inputSchema: Value
    implementationRef: Text
    replayPolicy: Optional<ReplayPolicy>
    sourceConnectionId: Optional<ConnectionId>
    executionKind: Optional<ExecutionKind>
END
```

**Compatibilidad hacia atrás:** con `sourceConnectionId = NULL` y `executionKind = NULL`, un descriptor
es una capability local, como en v1 y v2. La lista `isolatedCapabilities` de CH-35 sigue funcionando.
El descriptor v3 la reemplaza para quien lo declare.

### `ExternalToolSpec` y `ConnectionInvocation` — lo que publica el servidor y lo que se le envía (embebidos)

```pseudocode
STRUCT ExternalToolSpec
    name: Text
    description: Text
    inputSchema: Value
END
```

```pseudocode
STRUCT ConnectionInvocation
    callId: ToolCallId
    connectionId: ConnectionId
    toolName: Text
    arguments: Map<Text, Value>
END
```

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-054
Name:                   ConnectionDescriptor
Version:                v1
Introduced In:          CH-41
Used By:                [CMP-028]
Constitutional Impact:  [P-38, INV-E08, INV-E25]
```

```text
C-018 CapabilityDescriptor  v2 → v3   Modified By: [CH-30, CH-41]
                            + sourceConnectionId: Optional<ConnectionId>
                            + executionKind: Optional<ExecutionKind>
Used By:                    [CMP-008, CMP-015, CMP-026, CMP-028]
ADR:                        ADR-005 (Accepted 2026-10-10)
```

## 8. Responsabilidades de Componentes (Component Responsibilities)

```pseudocode
COMPONENT ConnectionManager
    consumes: ExecutionContext, ToolCall, CapabilityDescriptor
    produces: CapabilityDescriptor, ConnectionDescriptor, HarnessError
END
```

```text
COMPONENT: ConnectionManager (CMP-028)

Responsibility:
    Gestionar las conexiones declaradas a servidores MCP y especificaciones OpenAPI, traducir sus
    tools en CapabilityDescriptor con espacio de nombres propio, filtro y argumentos provistos, y
    preparar cada invocación hacia el adaptador del protocolo.

Owns:
    - "Capabilities provided by external systems … MUST enter through declared connections and be
      resolved as capability descriptors" (P-38)
    - aplicar el filtro de tools y rechazar (fail-closed) una tool fuera del filtro o un nombre que
      colisiona con una capability local
    - ocultar al modelo los argumentos provistos, y rechazar una tool call que intenta fijarlos

Does NOT own:
    - resolver capabilities y validar argumentos (CapabilityRegistry, CH-08). Es la frontera más
      importante del capítulo: ConnectionManager produce descriptores; CapabilityRegistry los
      resuelve como a cualquier otro (INV-E25).
    - autorizar (PolicyEngine) · ejecutar (ToolRuntime) · resolver credenciales (CredentialBroker)
    - hablar el protocolo (adaptador, P-38) · exponer el arnés como servidor MCP (canal, CH-34)
```

**Otros componentes ganan una función cada uno, dentro de su `owns`:**
- `CapabilityRegistry`: `effectiveExecutionKind`, dentro de "registrar el descriptor de una
  capability";
- `IsolatedExecutionEnvironment`: `requiresIsolation`, dentro de "decidir si una capability debe
  ejecutarse dentro del entorno aislado";
- `PolicyEngine`: `applyConnectionApprovalDefault`, que solo restringe.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
ConnectionManager
    consumes → ExecutionContext, ToolCall, CapabilityDescriptor
    produces → CapabilityDescriptor, ConnectionDescriptor, HarnessError
    depends on (componentes) → (ninguno)
```

**Al conectar:**
1. el adaptador del protocolo lista las tools del servidor (`ExternalToolSpec`);
2. `translateConnectionTools` → `CapabilityDescriptor` v3;
3. los descriptores se agregan a `registeredCapabilities`, la lista que `CapabilityRegistry` resuelve
   desde CH-08.

**En cada tool call:**
1. `resolveModelProposedToolCall` (CH-08) resuelve `tickets__search` y valida los argumentos contra el
   schema traducido;
2. `evaluatePolicyForToolCall` (CH-05), con las reglas por llamante de CH-38 si las hay →
   `applyConnectionApprovalDefault`;
3. `resolveConnectionCredential`: compartida, o del llamante (CH-38); si al usuario le falta,
   `detectMissingCallerCredential` + `parkForMissingCredential` (CH-37);
4. `prepareConnectionCall` → `ConnectionInvocation` con los argumentos provistos;
5. `ToolRuntime` la ejecuta con el adaptador del protocolo (`effectiveExecutionKind = CONNECTION`).

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Servidor externo → [adaptador] → ConnectionManager (traducir) → CapabilityRegistry
Modelo → CapabilityRegistry → PolicyEngine (+ aprobación por defecto) → CredentialBroker
       → ConnectionManager (preparar) → ToolRuntime → [adaptador] → servidor
```

**Vista 2 — Sequence: conectar y usar una tool de un servidor de tickets**

```text
Integración
   │ adaptador lista 20 tools → translateConnectionTools(conexión "tickets", ALLOW_LIST [search, create])
   │   → [tickets__search, tickets__create]  (schema sin "accountId", provisto por la conexión)
Modelo propone tickets__search(query = "factura 42")
   │ resolveModelProposedToolCall (CH-08)                → ToolCall
   │ evaluatePolicyForToolCall (CH-05)                   → ALLOW
   │ applyConnectionApprovalDefault (requiere aprobación) → REQUIRE_APPROVAL
   │ … aprobación (CH-36) …
   │ resolveConnectionCredential(PER_CALLER)             → CredentialReference del usuario
   │ prepareConnectionCall                               → ConnectionInvocation(query, accountId)
   │ ToolRuntime → adaptador → servidor
```

**Vista 2b — Sequence: el modelo intenta fijar un argumento provisto**

```text
tickets__search(query = "…", accountId = "otra-cuenta")
   │ prepareConnectionCall → PROVIDED_ARGUMENT_FROM_MODEL   (la tool no se invoca)
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

### ConnectionManager: traducir y preparar

```pseudocode
FUNCTION toolAllowed(
    filter: ToolFilter,
    toolName: Text
) -> Boolean

    listed: Boolean = FALSE

    FOR EACH name IN filter.names
        IF name == toolName
            listed = TRUE
        END
    END

    IF filter.mode == ALLOW_LIST
        RETURN listed
    END

    RETURN NOT listed
END
```

```pseudocode
FUNCTION translateConnectionTools(
    connection: ConnectionDescriptor,
    specs: List<ExternalToolSpec>,
    localCapabilities: List<CapabilityDescriptor>,
    connectionVersion: Text
) -> List<CapabilityDescriptor>

    translated: List<CapabilityDescriptor> = []

    FOR EACH spec IN specs
        IF toolAllowed(connection.toolFilter, spec.name)
            capability: CapabilityId = namespacedCapabilityId(connection.connectionId, spec.name)

            FOR EACH local IN localCapabilities
                IF local.capability == capability
                    THROW HarnessError(
                        category = VALIDATION,
                        code = "CAPABILITY_NAME_COLLISION",
                        message = "Una tool de la conexión produce un identificador que ya usa una capability local",
                        recoverable = FALSE,
                        retryable = FALSE,
                        metadata = {}
                    )
                END
            END

            translated = append(translated, CapabilityDescriptor(
                capability = capability,
                name = spec.name,
                version = connectionVersion,
                inputSchema = schemaWithout(spec.inputSchema, keysOf(connection.providedArguments)),
                implementationRef = connection.endpointRef,
                replayPolicy = NULL,
                sourceConnectionId = connection.connectionId,
                executionKind = CONNECTION
            ))
        END
    END

    RETURN translated
END
```

```pseudocode
FUNCTION prepareConnectionCall(
    call: ToolCall,
    descriptor: CapabilityDescriptor,
    connection: ConnectionDescriptor
) -> ConnectionInvocation

    IF descriptor.capability != call.capability OR descriptor.sourceConnectionId != connection.connectionId
        THROW HarnessError(
            category = VALIDATION,
            code = "CALL_NOT_FROM_THIS_CONNECTION",
            message = "La tool call no corresponde a una capability de esta conexión",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    FOR EACH key IN keysOf(connection.providedArguments)
        IF hasKey(call.arguments, key)
            THROW HarnessError(
                category = VALIDATION,
                code = "PROVIDED_ARGUMENT_FROM_MODEL",
                message = "El modelo intentó fijar un argumento que la conexión provee y que el modelo nunca ve",
                recoverable = FALSE,
                retryable = FALSE,
                metadata = {}
            )
        END
    END

    RETURN ConnectionInvocation(
        callId = call.id,
        connectionId = connection.connectionId,
        toolName = descriptor.name,
        arguments = mergeArguments(call.arguments, connection.providedArguments)
    )
END
```

### CapabilityRegistry e IsolatedExecutionEnvironment: el tipo de ejecución (D-025)

```pseudocode
FUNCTION effectiveExecutionKind(
    descriptor: CapabilityDescriptor
) -> ExecutionKind

    IF descriptor.executionKind != NULL
        RETURN descriptor.executionKind
    END

    IF descriptor.sourceConnectionId != NULL
        RETURN CONNECTION
    END

    RETURN LOCAL
END
```

```pseudocode
FUNCTION requiresIsolation(
    descriptor: CapabilityDescriptor
) -> Boolean

    RETURN effectiveExecutionKind(descriptor) == ISOLATED
END
```

### PolicyEngine: la aprobación por defecto solo restringe

```pseudocode
FUNCTION applyConnectionApprovalDefault(
    decision: PolicyDecision,
    descriptor: CapabilityDescriptor,
    connection: ConnectionDescriptor
) -> PolicyDecision

    IF decision.outcome != ALLOW
        OR descriptor.sourceConnectionId != connection.connectionId
        OR NOT connection.requiresApprovalByDefault

        RETURN decision
    END

    RETURN PolicyDecision(
        callId = decision.callId,
        outcome = REQUIRE_APPROVAL,
        policyRuleId = decision.policyRuleId,
        reason = NULL,
        decidedAt = now()
    )
END
```

### Integración: la credencial de la conexión (D-018)

```pseudocode
FUNCTION resolveConnectionCredential(
    connection: ConnectionDescriptor,
    descriptor: CapabilityDescriptor,
    classification: CredentialClassification,
    credentialBelongsToCapability: Boolean,
    secretExists: Boolean,
    expiresAt: Optional<Timestamp>,
    execution: ExecutionContext,
    agentId: AgentId
) -> Optional<CredentialReference>

    IF connection.credentialName == NULL
        RETURN NULL
    END

    IF connection.credentialScope == PER_CALLER
        RETURN resolveCallerCredentialReference(
            descriptor, connection.credentialName, classification, credentialBelongsToCapability,
            secretExists, expiresAt, execution, agentId
        )
    END

    RETURN resolveCredentialReference(
        descriptor, connection.credentialName, classification, credentialBelongsToCapability,
        secretExists, expiresAt, execution, agentId
    )
END
```

`namespacedCapabilityId`, `schemaWithout`, `keysOf`, `hasKey`, `mergeArguments`, `append` y `now` son
utilidades primitivas. `namespacedCapabilityId` produce `<conexión>__<tool>`. Con `PER_CALLER`, antes de
llamar a `resolveConnectionCredential`, la integración usa `detectMissingCallerCredential` (CH-37); si
falta la cuenta del usuario, estaciona el run con `parkForMissingCredential` en lugar de resolver.

Nótese lo que estas funciones **no** hacen:
- ninguna habla MCP ni OpenAPI: el adaptador lista las tools y ejecuta la invocación;
- ninguna autoriza: la aprobación por defecto solo convierte un `ALLOW` en `REQUIRE_APPROVAL`;
- ninguna declara `SAFE` una tool externa: `replayPolicy = NULL` equivale a `NEVER` (CH-30).

## 12. Transiciones de Estado (State Transitions)

```text
Tool publicada por el servidor
    fuera del filtro                   → no se traduce (el modelo nunca la ve)
    nombre que colisiona con una local → CAPABILITY_NAME_COLLISION
    permitida                          → CapabilityDescriptor <conexión>__<tool>, CONNECTION, replay NEVER

Tool call sobre una capability de conexión
    argumento provisto fijado por el modelo        → PROVIDED_ARGUMENT_FROM_MODEL
    ALLOW + requiresApprovalByDefault              → REQUIRE_APPROVAL
    PER_CALLER sin credencial del usuario          → AuthorizationChallenge (CH-37)
    en regla                                       → ConnectionInvocation → ToolRuntime → adaptador
```

## 13. Semántica de Fallos (Failure Semantics)

Códigos nuevos de `HarnessError`, con `ErrorCategory` ya existentes:

```text
VALIDATION  CAPABILITY_NAME_COLLISION      recoverable: FALSE, retryable: FALSE
VALIDATION  CALL_NOT_FROM_THIS_CONNECTION  recoverable: FALSE, retryable: FALSE
VALIDATION  PROVIDED_ARGUMENT_FROM_MODEL   recoverable: FALSE, retryable: FALSE
```

Un fallo del servidor externo durante la ejecución es un `ToolResult` fallido, que vuelve al modelo
como observación (INV-07). Una caída en medio de la invocación es un resultado desconocido, y con
`NEVER` no se repite (CH-30, CH-36).

## 14. Eventos Producidos (Events Produced)

Ningún `AgentEventType` nuevo: traducir ocurre al conectar, antes de cualquier run, y cada tool call de
conexión produce los eventos de siempre (`POLICY_EVALUATED`, `TOOL_CALL_COMPLETED`,
`TOOL_CALL_FAILED`, `STEP_COMMITTED`). El `sourceConnectionId` del descriptor queda en la auditoría
(INV-E10).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **El modelo ve solo lo que la conexión permite.** Una herramienta peligrosa del servidor que no está
  en la lista permitida no existe para el agente.
- **Un argumento provisto no se negocia.** El modelo no lo ve en el schema y no puede enviarlo; un
  prompt manipulado no puede cambiar la cuenta contra la que trabaja la herramienta.
- **El servidor no reemplaza a la política.** Que el servidor tenga sus propios permisos no exime a
  la tool de `PolicyEngine` (INV-E25), y la aprobación por defecto de la conexión solo agrega
  restricción.
- **La credencial nunca está en la conexión.** `credentialName` es un nombre; el valor lo resuelve
  `CredentialBroker`. Con `PER_CALLER`, cada usuario usa su propia cuenta (INV-E07).
- **Nada externo se repite a ciegas.** Una tool traducida es `NEVER` hasta que alguien la declare
  `SAFE`, y esa declaración queda auditada (CH-38).
- **Nombres sin ambigüedad.** El espacio de nombres impide que un servidor nuevo "tape" una
  herramienta local o de otro servidor.

## 16. Tests (Tests)

```text
TEST ToolOutsideTheAllowListIsNeverTranslated
TEST BlockListExcludesItsTools
TEST TranslatedCapabilityIsNamespacedByConnection
TEST NameCollisionWithALocalCapabilityIsRejected
TEST ProvidedArgumentsAreRemovedFromTheModelSchema
TEST ProvidedArgumentsAreAddedToTheInvocation
TEST ModelSettingAProvidedArgumentIsRejected
TEST TranslatedCapabilityDefaultsToReplayNever
TEST ApprovalDefaultTurnsAllowIntoRequireApproval
TEST ApprovalDefaultNeverTurnsDenyIntoAnything
TEST PerCallerConnectionUsesTheCallersCredential
TEST SharedConnectionUsesTheSharedCredential
TEST ExecutionKindIsDerivedFromSourceConnection
TEST RequiresIsolationReadsTheDescriptor
TEST LocalDescriptorV2BehavesAsBefore
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.3 en curso, después de CH-41) — 28 componentes, 54 contratos, 42 capítulos

Components — 28
 └── CMP-028 ConnectionManager         (CH-41, nuevo — Capability & Integration Plane)

Contracts — 54
 ├── C-018 CapabilityDescriptor v3     (CH-08 → CH-30 → CH-41: sourceConnectionId, executionKind)
 └── C-054 ConnectionDescriptor        (CH-41, nuevo)

Deuda: D-018 y D-025 resueltas.
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Los protocolos:** el libro modela la conexión y la traducción; MCP y OpenAPI son adaptadores
  (P-38).
- **Actualizar las tools cuando el servidor cambia:** se vuelve a traducir con otra
  `connectionVersion`. Decidir cuándo, y qué pasa con una sesión abierta, es evolución del runtime
  (CH-45).
- **Recursos y prompts que publican algunos servidores** (además de tools): son datos para el
  contexto, y entran por las fuentes de datos gobernadas (CH-42).
- **El arnés como servidor MCP:** es un canal de entrada (CH-34).

## 19. Siguiente Incremento (Next Increment)

Ahora las herramientas externas entran por un solo camino. Pero un agente también necesita **datos**
que no son herramientas: documentos, tablas, registros que hoy llegan al contexto "ya dados", sin que
nadie decida qué se recupera ni con qué clasificación (CH-04 lo dejó declarado).

El siguiente capítulo introduce las **fuentes de datos gobernadas** (P-38 aplicado a datos, INV-E26):
- un `DataSourceDescriptor` por fuente, con clasificación obligatoria;
- un `RetrievalEngine` que recupera candidatos con procedencia y etiqueta de gobierno;
- datos y memoria que se recuperan para el llamante (deuda D-019).

Será CH-42 ("Fuentes de Datos Gobernadas: Recuperar sin Tirarlo Todo al Contexto"). `next_chapter`
queda en `null` porque CH-42 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): las tools externas se escriben a mano o se le dan al modelo por fuera de
   la política.
2. **Patrones** (= §3): el descriptor no sabe de dónde viene ni cómo se ejecuta una capability; la
   lista de aislamiento es configuración suelta.
3. **Estructuras** (= §8): `ConnectionManager` (CMP-028), `ConnectionDescriptor` (C-054) y
   `CapabilityDescriptor` v3.
4. **Modelos mentales** (= §4): P-38, INV-E25, INV-E08 y P-27.

**Bucles de retroalimentación**

- **Refuerzo:** cada servidor conectado a su manera agrega un camino con sus propias reglas. Un solo
  camino corta la espiral.
- **Equilibrio:** el filtro de tools. El modelo ve solo lo que la conexión permite.

**Punto de apalancamiento**

La decisión con mayor efecto es que `ConnectionManager` (CMP-028) solo produzca `CapabilityDescriptor`:
una tool externa no tiene un camino propio, y la resolución, la política, la credencial, el
aislamiento y el replay se aplican igual que a una tool local.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué hace `translateConnectionTools` con una tool fuera del filtro y con una cuyo nombre colisiona
   con una capability local, y qué forma tiene el identificador de una capability traducida?
   *(pregunta guía 1)*
2. ¿Qué hace `translateConnectionTools` con los argumentos provistos al armar el schema, qué hace
   `prepareConnectionCall` con ellos, y qué error lanza si el modelo intenta fijarlos?
   *(pregunta guía 2)*
3. ¿Qué función usa `resolveConnectionCredential` según el `credentialScope`, y qué capítulo maneja el
   caso en que la credencial del usuario todavía no existe? *(pregunta guía 3)*
4. ¿Qué hace `applyConnectionApprovalDefault` con un `ALLOW`, qué `replayPolicy` tiene una tool
   traducida, y qué devuelve `effectiveExecutionKind` para un descriptor con `sourceConnectionId` y
   `executionKind = NULL`? *(pregunta guía 4)*

### Explicar

1. `CapabilityRegistry` ya registraba y resolvía capabilities. Explica por qué traducir las tools de
   una conexión es una decisión distinta que merece un componente, y por qué ese componente no resuelve
   ni autoriza nada.
2. Explica por qué un `ConnectionDescriptor` separa los argumentos provistos del schema que ve el
   modelo, y qué ataque permitiría dejarlos en el schema.

### Conectar

1. En CH-35, `mustRunIsolated` decidía con una lista configurada qué capabilities corrían en el entorno
   aislado. ¿Qué la reemplaza con `CapabilityDescriptor` v3, cómo se deriva el valor cuando el
   descriptor no lo declara, y por qué una tool de conexión no corre en el entorno aislado?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
