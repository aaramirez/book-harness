---
id: CH-40
title: "Extensiones que No Pueden Saltarse la Constitución"
starting_version: "0.2.1"
ending_version: "0.3"
introduces_components: [CMP-027]
introduces_contracts: [C-051, C-052, C-053]
modifies_contracts: []
constitutional_articles: [P-07, P-12, P-13, INV-05, INV-06, INV-E24]
previous_chapter: CH-39
next_chapter: CH-41
retrieval_set:
  expected_outcome:
    id: EO-CH40
    text: |
      Al terminar este capítulo podrás decidir si una extensión puede cargarse, en qué puntos del
      ciclo puede intervenir y qué puede devolver en cada uno, y explicar por qué ningún hook puede
      autorizar una acción aunque pueda bloquearla.
  skeleton:
    id: SK-CH40
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
    components_to_be_introduced: [CMP-027]
    contracts_to_be_introduced: [C-051, C-052, C-053]
  guiding_questions:
    - id: GQ-CH40-01
      text: |
        Si clonas un repositorio que trae su propia extensión para el agente, ¿debería el arnés
        cargarla automáticamente? ¿Qué debería pasar si el código de esa extensión cambia mañana?
      answered_by: RQ-CH40-01
    - id: GQ-CH40-02
      text: |
        Una extensión quiere revisar cada herramienta antes de que se ejecute. ¿Debería poder
        aprobar una acción que la política denegó? ¿Y bloquear una que la política permitió?
      answered_by: RQ-CH40-02
    - id: GQ-CH40-03
      text: |
        ¿Por qué una extensión podría cambiar el contexto que ve el modelo, pero no los argumentos de
        una herramienta que ya fue autorizada?
      answered_by: RQ-CH40-03
    - id: GQ-CH40-04
      text: |
        ¿Qué diferencia hay entre un componente que observa lo que pasó y uno que puede intervenir en
        lo que va a pasar?
      answered_by: RQ-CH40-04
  systems_lens:
    iceberg_visible_fact: |
      El libro tiene dos puntos de extensión, beforeToolCall y afterToolCall dentro de ToolRuntime,
      sin contrato; cualquier código que quiera intervenir en otro punto tiene que tocar el núcleo, y
      nada impide que una extensión cargada desde un proyecto haga lo que el núcleo prohibiría (ver
      sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que EVO-10 prohíbe que una extensión se salte ToolRuntime,
      PolicyEngine o el ciclo de vida, pero ningún componente lo hace cumplir, y P-12 separa hooks de
      eventos sin decir qué puede devolver un hook (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce ExtensionHost (CMP-027), ExtensionRegistration (C-051), HookPoint
      (C-052) y ResourceTrustDecision (C-053): un registro de extensiones con confianza atada al
      contenido y un catálogo cerrado de puntos, cada uno con los resultados que admite (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son EVO-10 (una extensión no se salta la constitución), INV-E24 (ningún
      hook devuelve una autorización), P-12 (los eventos observan, los hooks intervienen) y P-13 (la
      autorización es de PolicyEngine) (ver sección 4).
    reinforcing_loop: |
      Si cada extensión puede intervenir donde quiera y devolver lo que quiera, cada extensión nueva
      agrega un camino que nadie revisó, y cada incidente se parcha con otra excepción. Un catálogo
      cerrado de puntos y resultados corta la espiral: lo que no está en el catálogo no existe.
    balancing_loop: |
      La decisión de confianza atada al hash es el mecanismo de equilibrio: por mucho que cambie el
      código de una extensión de proyecto, cada cambio exige una decisión nueva antes de cargarse.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que cada HookPoint (C-052) admita solo
      resultados de un HookOutcomeKind sin ningún valor de autorización: así INV-E24 no depende de que
      cada extensión se porte bien, sino de que el tipo no permite expresarlo.
  recall_questions:
    - id: RQ-CH40-01
      text: |
        ¿Qué exige registerExtension a una extensión de proyecto u organización, qué cubre una
        ResourceTrustDecision, y qué pasa con la extensión si su contentHash cambia?
    - id: RQ-CH40-02
      text: |
        ¿Cuáles son los tres valores de HookOutcomeKind, en qué momento corren los hooks de BEFORE_TOOL
        respecto de PolicyEngine, y qué devuelve runBeforeToolHooks si uno bloquea?
    - id: RQ-CH40-03
      text: |
        ¿Qué resultados admite allowedOutcomes para TRANSFORM_CONTEXT y para BEFORE_TOOL, y por qué
        BEFORE_TOOL no admite TRANSFORM?
    - id: RQ-CH40-04
      text: |
        ¿Qué componente ejecuta los hooks de cada punto, qué hace ExtensionHost con el resultado, y en
        qué se diferencia un hook de un suscriptor del EventBus?
  explain_prompts:
    - id: EP-CH40-01
      text: |
        ToolRuntime ya "ejecutaba hooks" desde CH-02. Explica, como si hablaras con alguien sin
        contexto técnico, por qué hace falta un componente aparte que decida qué hooks pueden correr y
        qué pueden devolver, y por qué ese componente no los ejecuta él mismo.
      target_entity: CMP-027
    - id: EP-CH40-02
      text: |
        Explica por qué una ResourceTrustDecision se ata al hash del contenido y no solo al nombre del
        recurso, y qué ataque permitiría confiar por nombre.
      target_entity: C-053
  interleaved_questions:
    - id: IQ-CH40-01
      text: |
        En CH-38, evaluatePolicyForCaller partía de la decisión base de PolicyEngine y solo podía
        convertir un permiso en rechazo. ¿Qué tiene en común con un hook BLOCK de BEFORE_TOOL, y por
        qué ninguno de los dos puede convertir un rechazo en permiso?
      current_chapter_entities: [C-052, CMP-027]
      prior_chapter_entities: [C-014, CMP-005]
      prior_chapter: CH-05
  flashcards:
    - id: FC-CH40-01
      front: |
        ¿Qué puede devolver un hook (HookOutcomeKind) y qué no?
      back: |
        CONTINUE, BLOCK o TRANSFORM, según lo que admita su HookPoint. No existe ningún valor de
        autorización: un hook puede restringir o transformar, nunca conceder (INV-E24).
      source_entity: C-052
      chapter_introduced_in: CH-40
      review_stage: DAY_1
    - id: FC-CH40-02
      front: |
        ¿Qué es una ResourceTrustDecision (C-053)?
      back: |
        La decisión explícita de confiar o no en el código de un recurso, atada a su sourceRef y a su
        contentHash, tomada por un Principal verificado. Si el contenido cambia, ya no lo cubre.
      source_entity: C-053
      chapter_introduced_in: CH-40
      review_stage: DAY_1
    - id: FC-CH40-03
      front: |
        ¿Qué posee ExtensionHost (CMP-027) y qué no?
      back: |
        Posee registrar extensiones con su confianza, el catálogo de HookPoints con sus resultados
        admitidos y la validación de cada resultado. No ejecuta los hooks (lo hace el dueño de cada
        punto), no autoriza, no registra capabilities ni ejecuta tools.
      source_entity: CMP-027
      chapter_introduced_in: CH-40
      review_stage: DAY_1
    - id: FC-CH40-04
      front: |
        ¿Qué es una ExtensionRegistration (C-051) y cuándo queda REJECTED?
      back: |
        Una extensión registrada: origen (BUILT_IN, ORGANIZATION, PROJECT), sourceRef, contentHash,
        puntos de hook, capabilities, decisión de confianza y estado. Queda REJECTED si no es BUILT_IN
        y ninguna decisión TRUSTED cubre su sourceRef y su contentHash actuales.
      source_entity: C-051
      chapter_introduced_in: CH-40
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH40-01
      recall_question: RQ-CH40-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH40-02
      recall_question: RQ-CH40-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH40-03
      recall_question: RQ-CH40-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH40-04
      recall_question: RQ-CH40-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 40 — Extensiones que No Pueden Saltarse la Constitución

> **Regla constitucional (EVO-10):** una extensión no puede saltarse ToolRuntime, PolicyEngine, el
> ciclo de vida ni los controles de ejecución.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir si una extensión puede cargarse, en
qué puntos del ciclo puede intervenir y qué puede devolver en cada uno. También podrás explicar por
qué ningún hook puede autorizar una acción aunque pueda bloquearla.

**Esqueleto.** Segundo capítulo de la versión 0.3. Introduce el componente `ExtensionHost` y tres
contratos.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si clonas un repositorio que trae su propia extensión para el agente, ¿debería el arnés cargarla
   automáticamente? ¿Qué debería pasar si el código de esa extensión cambia mañana?
2. Una extensión quiere revisar cada herramienta antes de que se ejecute. ¿Debería poder aprobar una
   acción que la política denegó? ¿Y bloquear una que la política permitió?
3. ¿Por qué una extensión podría cambiar el contexto que ve el modelo, pero no los argumentos de una
   herramienta que ya fue autorizada?
4. ¿Qué diferencia hay entre un componente que observa lo que pasó y uno que puede intervenir en lo
   que va a pasar?

## 1. Arquitectura Actual (Current Architecture)

- **`ToolRuntime` (CMP-002, CH-02)** posee "ejecutar hooks". Llama a `beforeToolCall` y
  `afterToolCall`, los dos únicos puntos de extensión del libro, sin contrato ni registro.
- **`EventBus` (CMP-009, CH-09)** distribuye eventos a suscriptores que **observan**: no pueden
  cambiar lo que pasó.
- **`PolicyEngine` (CMP-005, CH-05)** es el único que autoriza (P-13, INV-06).
- **`CapabilityRegistry` (CMP-008, CH-08)** registra y resuelve capabilities.
- **EVO-10** prohíbe que una extensión se salte la constitución, y **P-12** dice que los hooks
  intervienen y los eventos observan. Ningún componente hace cumplir ninguno de los dos.

## 2. El Problema (Problem)

Un equipo quiere agregar comportamiento al agente sin tocar el núcleo:
- un hook que redacte datos personales del resultado de cada herramienta;
- una regla que agregue al contexto las convenciones del proyecto;
- una extensión del repositorio que bloquee comandos peligrosos en ese proyecto.

Hoy pasan tres cosas:
- **solo hay dos puntos**, y ambos dentro de `ToolRuntime`. Intervenir en el contexto, en la llamada
  al modelo o en la compactación exige tocar el núcleo;
- **nada limita qué devuelve un hook.** Un hook de "antes de la tool" podría devolver "aprobado" y
  saltarse a `PolicyEngine`, o cambiar los argumentos después de que la política los autorizó;
- **cualquier código del repositorio se carga.** Clonar un proyecto con una extensión maliciosa
  basta para que se ejecute dentro del arnés.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **EVO-10 es una frase, no un mecanismo.** Ningún componente revisa qué hace una extensión.
- **Un hook sin tipo de resultado puede expresar cualquier cosa**, incluida una autorización. Que no
  lo haga dependería de que cada extensión se porte bien.
- **No hay confianza.** El libro no distingue el código del propio arnés del que trae un repositorio
  clonado.
- **Ningún componente posee la decisión** "¿qué código de terceros puede intervenir, dónde y con qué
  resultado?". No es de `ToolRuntime` (ejecuta tools y sus hooks), ni de `CapabilityRegistry`
  (capabilities), ni de `EventBus` (observar). Por eso este capítulo introduce un componente (EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-07   Skills encode reusable procedural knowledge.
           Una extensión puede aportar capabilities y hooks; las skills siguen en SkillLibrary.
    P-12   Events observe; hooks intervene.
           Los hooks intervienen solo en un HookPoint declarado; los eventos siguen en EventBus.
    P-13   Authorization is deterministic and external to the LLM.
           Ningún hook autoriza; la autorización sigue siendo de PolicyEngine.

Evolution rule enforced
    EVO-10 Extensions cannot bypass constitutional boundaries.
           ExtensionHost lo vuelve verificable: registro con confianza y resultado de hook validado.

Invariants preserved
    INV-05   Todo ToolCall pasa por ToolRuntime.
             Una capability aportada por una extensión se ejecuta igual que cualquier otra.
    INV-06   Todo side effect pasa por PolicyEngine.
             Los hooks de BEFORE_TOOL corren después de un ALLOW, y solo pueden bloquear.
    INV-E24  (Amendment v1.2) No hook point may return an authorization outcome.
             HookOutcomeKind no tiene ningún valor de autorización.

Component ownership changes
    Nuevo: ExtensionHost (CMP-027). ToolRuntime conserva "ejecutar hooks".

Contract changes
    Nuevos: C-051 ExtensionRegistration, C-052 HookPoint, C-053 ResourceTrustDecision.

Security implications
    El código de un proyecto no se carga sin confianza explícita atada a su contenido
    (ver sección 15).

Observability implications
    Nuevo AgentEventType: HOOK_OUTCOME_REJECTED.

Deterministic vs agentic boundary
    Sin cambios: una extensión es código determinístico que interviene en puntos fijos.
```

## 5. Conceptos Nuevos (New Concepts)

- **Extensión:** código que no es del núcleo y que aporta hooks o capabilities. Tiene un origen:
  - `BUILT_IN`: parte del propio arnés;
  - `ORGANIZATION`: distribuida por la organización;
  - `PROJECT`: viene con el repositorio en el que trabaja el agente.
- **Punto de hook** (*hook point*): un lugar fijo del ciclo donde un hook puede intervenir. Hay ocho,
  y cada uno pertenece a un componente que lo ejecuta:

  | Punto | Dueño que lo ejecuta | Resultados admitidos |
  |---|---|---|
  | `BEFORE_RUN` | AgentCore / AgentLoop | `CONTINUE`, `BLOCK` |
  | `TRANSFORM_CONTEXT` | ContextEngine | `CONTINUE`, `TRANSFORM` |
  | `BEFORE_REQUEST` | ModelGateway | `CONTINUE`, `BLOCK`, `TRANSFORM` |
  | `AFTER_RESPONSE` | ModelGateway | `CONTINUE`, `TRANSFORM` |
  | `BEFORE_TOOL` | ToolRuntime | `CONTINUE`, `BLOCK` |
  | `AFTER_TOOL` | ToolRuntime | `CONTINUE`, `TRANSFORM` |
  | `BEFORE_COMPACTION` | ContextEngine | `CONTINUE`, `BLOCK` |
  | `BEFORE_NAVIGATION` | SessionManager | `CONTINUE`, `BLOCK` |

- **Resultado de hook:** lo que un hook devuelve. Seguir (`CONTINUE`), detener (`BLOCK`) o transformar
  el dato de su punto (`TRANSFORM`). **No existe "aprobado".**
- **Confianza de recurso:** la decisión explícita, de una persona verificada, de que el código de un
  recurso puede cargarse. Se ata al hash del contenido: si el código cambia, hace falta decidir otra
  vez.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `Principal` (C-040), `PolicyDecision` (C-014), `ToolCall` (C-008),
  `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `AgentId`, `CapabilityId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `ResourceTrustDecisionId` | identificador nuevo de una decisión de confianza |
| `AgentEventType` | se agrega `HOOK_OUTCOME_REJECTED` |
| `ErrorCategory` | reutiliza `POLICY` y `VALIDATION` |

### `HookPoint` — los puntos donde un hook puede intervenir (C-052)

```pseudocode
ENUM HookPoint
    BEFORE_RUN
    TRANSFORM_CONTEXT
    BEFORE_REQUEST
    AFTER_RESPONSE
    BEFORE_TOOL
    AFTER_TOOL
    BEFORE_COMPACTION
    BEFORE_NAVIGATION
END
```

### `ExtensionSource`, `ExtensionStatus` y `TrustOutcome` (embebidos)

```pseudocode
ENUM ExtensionSource
    BUILT_IN
    ORGANIZATION
    PROJECT
END
```

```pseudocode
ENUM ExtensionStatus
    ACTIVE
    REJECTED
    DISABLED
END
```

```pseudocode
ENUM TrustOutcome
    TRUSTED
    UNTRUSTED
END
```

### `ResourceTrustDecision` — confiar en un contenido concreto (C-053)

```pseudocode
STRUCT ResourceTrustDecision
    decisionId: ResourceTrustDecisionId
    sourceRef: Text
    contentHash: Text
    outcome: TrustOutcome
    decidedBy: Principal
    decidedAt: Timestamp
END
```

### `ExtensionRegistration` — una extensión registrada (C-051)

```pseudocode
STRUCT ExtensionRegistration
    extensionId: Text
    version: Text
    source: ExtensionSource
    sourceRef: Text
    contentHash: Text
    hookPoints: List<HookPoint>
    capabilities: List<CapabilityId>
    trustDecisionId: Optional<ResourceTrustDecisionId>
    status: ExtensionStatus
    registeredAt: Timestamp
END
```

### `HookOutcomeKind` y `HookOutcome` — lo que un hook devuelve (embebidos)

```pseudocode
ENUM HookOutcomeKind
    CONTINUE
    BLOCK
    TRANSFORM
END
```

```pseudocode
STRUCT HookOutcome
    extensionId: Text
    point: HookPoint
    kind: HookOutcomeKind
    transformed: Optional<Value>
    reason: Optional<HarnessError>
END
```

`transformed` solo tiene valor con `TRANSFORM`; `reason`, con `BLOCK`.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-051
Name:                   ExtensionRegistration
Version:                v1
Introduced In:          CH-40
Used By:                [CMP-027]
Constitutional Impact:  [P-12, INV-E24]
```

```text
ID:                     C-052
Name:                   HookPoint
Version:                v1
Introduced In:          CH-40
Used By:                [CMP-027]
Constitutional Impact:  [P-12, INV-E24]
```

```text
ID:                     C-053
Name:                   ResourceTrustDecision
Version:                v1
Introduced In:          CH-40
Used By:                [CMP-027]
Constitutional Impact:  [P-13, INV-19]
```

`ExtensionSource`, `ExtensionStatus`, `TrustOutcome`, `HookOutcomeKind` y `HookOutcome` quedan
embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

```pseudocode
COMPONENT ExtensionHost
    consumes: ExecutionContext, Principal
    produces: ExtensionRegistration, HookPoint, ResourceTrustDecision, AgentEvent, HarnessError
END
```

```text
COMPONENT: ExtensionHost (CMP-027)

Responsibility:
    Registrar las extensiones del arnés con su origen, su hash y la decisión de confianza que las
    cubre; mantener el catálogo cerrado de HookPoints con los resultados que admite cada uno; y
    validar el resultado de cada hook antes de que el dueño del punto lo aplique.

Owns:
    - "Una extensión no puede saltarse ToolRuntime, PolicyEngine, lifecycle o controles de
      ejecución …" (EVO-10), vuelto verificable
    - "No hook point may return an authorization outcome" (INV-E24)
    - "Los hooks permiten intervenir en puntos controlados del lifecycle" (P-12): el catálogo de
      puntos y resultados admitidos
    - rechazar (fail-closed) una extensión de proyecto u organización sin confianza vigente

Does NOT own:
    - ejecutar los hooks en cada punto (el dueño del punto: ToolRuntime, que posee "ejecutar hooks"
      desde CH-02; ModelGateway, ContextEngine, AgentLoop y SessionManager para los suyos). Es la
      frontera más importante del capítulo: ExtensionHost decide QUÉ hooks corren y QUÉ pueden
      devolver; el dueño del punto los invoca y aplica el resultado ya validado.
    - autorizar (PolicyEngine, CH-05)
    - registrar o resolver capabilities (CapabilityRegistry, CH-08)
    - ejecutar tools (ToolRuntime, INV-05)
    - observar y distribuir eventos (EventBus, CH-09)
    - descargar, instalar o aislar código (infraestructura y entorno aislado, CH-35)
```

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
ExtensionHost
    consumes → ExecutionContext, Principal
    produces → ExtensionRegistration, HookPoint, ResourceTrustDecision, AgentEvent, HarnessError
    depends on (componentes) → (ninguno)
```

**Carga de una extensión:**
1. una persona verificada decide confiar en un recurso de proyecto (`ResourceTrustDecision`);
2. `registerExtension` lo registra `ACTIVE` si la decisión cubre su `sourceRef` y su `contentHash`,
   o `REJECTED` si no;
3. las capabilities que aporta se registran en `CapabilityRegistry` como cualquier otra, y quedan
   sujetas a la misma política.

**Ejecución de un hook (en el punto `BEFORE_TOOL`):**
1. `PolicyEngine` decide sobre la tool call;
2. si decide `ALLOW`, `ToolRuntime` pide `hooksFor(…, BEFORE_TOOL)` e invoca cada hook;
3. `runBeforeToolHooks` valida cada resultado con `validateHookOutcome`;
4. si alguno es `BLOCK`, la tool no se ejecuta y el modelo recibe el motivo como observación.

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Persona verificada → ResourceTrustDecision → ExtensionHost (registrar)
PolicyEngine (ALLOW) → ToolRuntime (ejecutar hooks) → ExtensionHost (validar) → ejecutar | bloquear
```

**Vista 2 — Sequence: una extensión de proyecto bloquea un comando**

```text
Integración
   │ registerExtension(ext "guardas-del-proyecto", PROJECT, hash h1, [BEFORE_TOOL], trust(h1))  → ACTIVE
   │ evaluatePolicyForToolCall(call "shell: rm -rf build")                                       → ALLOW
   │ hooksFor(registros, BEFORE_TOOL)                                                            → [guardas-del-proyecto]
   │ ToolRuntime invoca el hook → HookOutcome(BLOCK, motivo)
   │ runBeforeToolHooks → validateHookOutcome (BLOCK admitido en BEFORE_TOOL)                     → error EXTENSION_BLOCKED_TOOL
   │ la tool no se ejecuta; el modelo recibe el motivo
```

**Vista 2b — Sequence: un hook intenta transformar argumentos ya autorizados**

```text
HookOutcome(BEFORE_TOOL, TRANSFORM, argumentos nuevos)
   │ validateHookOutcome → TRANSFORM no admitido en BEFORE_TOOL
   │ → HOOK_OUTCOME_REJECTED + HOOK_OUTCOME_NOT_ALLOWED
```

**Vista 2c — Sequence: el código de la extensión cambió**

```text
registerExtension(ext, PROJECT, hash h2, …, trust(h1)) → REJECTED (la confianza cubre h1, no h2)
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION trustCovers(
    decision: Optional<ResourceTrustDecision>,
    sourceRef: Text,
    contentHash: Text
) -> Boolean

    RETURN decision != NULL
        AND decision.outcome == TRUSTED
        AND decision.sourceRef == sourceRef
        AND decision.contentHash == contentHash
END
```

```pseudocode
FUNCTION registerExtension(
    extensionId: Text,
    version: Text,
    source: ExtensionSource,
    sourceRef: Text,
    contentHash: Text,
    hookPoints: List<HookPoint>,
    capabilities: List<CapabilityId>,
    trust: Optional<ResourceTrustDecision>
) -> ExtensionRegistration

    status: ExtensionStatus = ACTIVE
    trustId: Optional<ResourceTrustDecisionId> = NULL

    IF source != BUILT_IN
        IF trustCovers(trust, sourceRef, contentHash)
            trustId = trust.decisionId
        ELSE
            status = REJECTED
        END
    END

    RETURN ExtensionRegistration(
        extensionId = extensionId,
        version = version,
        source = source,
        sourceRef = sourceRef,
        contentHash = contentHash,
        hookPoints = hookPoints,
        capabilities = capabilities,
        trustDecisionId = trustId,
        status = status,
        registeredAt = now()
    )
END
```

```pseudocode
FUNCTION allowedOutcomes(
    point: HookPoint
) -> List<HookOutcomeKind>

    IF point == BEFORE_REQUEST
        RETURN [CONTINUE, BLOCK, TRANSFORM]
    END

    IF point == TRANSFORM_CONTEXT OR point == AFTER_RESPONSE OR point == AFTER_TOOL
        RETURN [CONTINUE, TRANSFORM]
    END

    RETURN [CONTINUE, BLOCK]
END
```

```pseudocode
FUNCTION hooksFor(
    registrations: List<ExtensionRegistration>,
    point: HookPoint
) -> List<ExtensionRegistration>

    selected: List<ExtensionRegistration> = []

    FOR EACH registration IN registrations
        IF registration.status == ACTIVE
            FOR EACH declared IN registration.hookPoints
                IF declared == point
                    selected = append(selected, registration)
                END
            END
        END
    END

    RETURN selected
END
```

```pseudocode
FUNCTION validateHookOutcome(
    outcome: HookOutcome,
    registration: ExtensionRegistration,
    execution: ExecutionContext,
    agentId: AgentId
) -> HookOutcome

    declared: Boolean = FALSE
    FOR EACH point IN registration.hookPoints
        IF point == outcome.point
            declared = TRUE
        END
    END

    admitted: Boolean = FALSE
    FOR EACH kind IN allowedOutcomes(outcome.point)
        IF kind == outcome.kind
            admitted = TRUE
        END
    END

    wellFormed: Boolean = (outcome.kind == TRANSFORM) == (outcome.transformed != NULL)

    IF registration.status != ACTIVE
        OR registration.extensionId != outcome.extensionId
        OR NOT declared
        OR NOT admitted
        OR NOT wellFormed

        failure: HarnessError = HarnessError(
            category = VALIDATION,
            code = "HOOK_OUTCOME_NOT_ALLOWED",
            message = "El hook no es de una extensión activa, no declaró este punto, o devolvió un resultado que este punto no admite",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = HOOK_OUTCOME_REJECTED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )
        THROW failure
    END

    RETURN outcome
END
```

```pseudocode
FUNCTION firstBlockingOutcome(
    outcomes: List<HookOutcome>
) -> Optional<HookOutcome>

    FOR EACH outcome IN outcomes
        IF outcome.kind == BLOCK
            RETURN outcome
        END
    END

    RETURN NULL
END
```

La función de integración que conecta los hooks de `BEFORE_TOOL` con la política:

```pseudocode
FUNCTION runBeforeToolHooks(
    call: ToolCall,
    decision: PolicyDecision,
    hooks: List<ExtensionRegistration>,
    outcomes: List<HookOutcome>,
    execution: ExecutionContext,
    agentId: AgentId
) -> Optional<HarnessError>

    IF decision.outcome != ALLOW OR decision.callId != call.id
        THROW HarnessError(
            category = POLICY,
            code = "HOOKS_REQUIRE_AN_ALLOW",
            message = "Los hooks de BEFORE_TOOL corren solo después de que PolicyEngine permitió esta tool call",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    validated: List<HookOutcome> = []

    FOR EACH outcome IN outcomes
        FOR EACH registration IN hooks
            IF registration.extensionId == outcome.extensionId
                validated = append(validated, validateHookOutcome(outcome, registration, execution, agentId))
            END
        END
    END

    blocking: Optional<HookOutcome> = firstBlockingOutcome(validated)

    IF blocking == NULL
        RETURN NULL
    END

    RETURN HarnessError(
        category = POLICY,
        code = "EXTENSION_BLOCKED_TOOL",
        message = "Una extensión bloqueó esta tool call después de que la política la permitiera",
        recoverable = FALSE,
        retryable = FALSE,
        metadata = {}
    )
END
```

`newEventId`, `now` y `append` son utilidades primitivas. `outcomes` son los resultados que
`ToolRuntime` obtuvo al invocar cada hook de `hooksFor(…, BEFORE_TOOL)`. El error que devuelve
`runBeforeToolHooks` vuelve al modelo como una observación de tool fallida (INV-07).

Nótese lo que estas funciones **no** hacen:
- ninguna ejecuta un hook: los ejecuta el dueño de cada punto;
- ninguna puede producir un permiso: no existe un resultado de hook que lo exprese;
- `runBeforeToolHooks` nunca corre antes de la política: exige un `ALLOW` de la misma tool call.

## 12. Transiciones de Estado (State Transitions)

```text
ExtensionRegistration
    BUILT_IN                                         → ACTIVE
    PROJECT | ORGANIZATION con confianza vigente      → ACTIVE
    PROJECT | ORGANIZATION sin confianza, o hash otro → REJECTED
    (DISABLED: apagada por un operador; Preview)

Hook en un punto
    CONTINUE                → el dueño sigue
    BLOCK (si el punto lo admite)     → el dueño detiene y produce la observación
    TRANSFORM (si el punto lo admite) → el dueño usa el dato transformado
    resultado no admitido   → HOOK_OUTCOME_REJECTED + HOOK_OUTCOME_NOT_ALLOWED
```

## 13. Semántica de Fallos (Failure Semantics)

Códigos nuevos de `HarnessError`, con `ErrorCategory` ya existentes:

```text
VALIDATION  HOOK_OUTCOME_NOT_ALLOWED  recoverable: FALSE, retryable: FALSE
POLICY      HOOKS_REQUIRE_AN_ALLOW    recoverable: FALSE, retryable: FALSE
POLICY      EXTENSION_BLOCKED_TOOL    (observación de tool fallida, no fallo del run)
```

Un resultado de hook rechazado **no** se aplica, y el run no falla por él: el dueño del punto sigue
como si el hook hubiera devuelto `CONTINUE`, y queda el evento `HOOK_OUTCOME_REJECTED` para
investigar la extensión. Una extensión que bloquea mucho puede apagarse (`DISABLED`).

## 14. Eventos Producidos (Events Produced)

```text
HOOK_OUTCOME_REJECTED — un hook devolvió un resultado que su punto no admite (payload: HarnessError)
```

Registrar una extensión no emite eventos (ocurre antes de cualquier run, como la admisión en CH-14).
Su trazabilidad es la `ResourceTrustDecision`, con el `Principal` que decidió.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Clonar no es confiar.** Una extensión de proyecto solo se carga con una decisión explícita de una
  persona verificada.
- **La confianza es sobre un contenido, no sobre un nombre.** Si alguien cambia el código de una
  extensión ya confiada (un commit nuevo, una dependencia actualizada), el hash cambia y la extensión
  queda `REJECTED` hasta que alguien vuelva a decidir.
- **Un hook no puede aprobar.** No existe un valor que lo exprese. Un hook de `BEFORE_TOOL` corre
  después de un `ALLOW` y solo puede detener.
- **Un hook no puede cambiar lo autorizado.** `BEFORE_TOOL` no admite `TRANSFORM`, porque los
  argumentos ya pasaron por el schema y por la política.
- **Lo que un hook transforma sigue gobernado.** Un contexto transformado sigue pasando por la
  procedencia y el gobierno del dato de `ContextEngine` (CH-04, CH-20); un resultado de tool
  transformado sigue volviendo al modelo como observación (INV-07).
- **Una capability de extensión no tiene atajos.** Se registra en `CapabilityRegistry`, la autoriza
  `PolicyEngine` y la ejecuta `ToolRuntime`, en el entorno aislado si corresponde (CH-35).

## 16. Tests (Tests)

```text
TEST HookOutcomeKindHasNoAuthorizationValue
TEST ProjectExtensionWithoutTrustIsRejected
TEST TrustForAnotherHashDoesNotCoverTheExtension
TEST BuiltInExtensionNeedsNoTrustDecision
TEST HooksForReturnsOnlyActiveExtensionsThatDeclaredThePoint
TEST BeforeToolRejectsTransform
TEST TransformWithoutTransformedValueIsMalformed
TEST HookFromAnUndeclaredPointIsRejected
TEST RejectedHookOutcomeEmitsHookOutcomeRejected
TEST BeforeToolHooksRequireAnAllowForTheSameCall
TEST BlockingHookPreventsTheToolAfterAnAllow
TEST NoHookCanTurnADenyIntoAnAllow
TEST ExtensionCapabilityGoesThroughCapabilityRegistryAndPolicyEngine
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.3 en curso, después de CH-40) — 27 componentes, 53 contratos, 41 capítulos

Components — 27
 └── CMP-027 ExtensionHost           (CH-40, nuevo — Capability & Integration Plane)

Contracts — 53
 ├── C-051 ExtensionRegistration     (CH-40, nuevo)
 ├── C-052 HookPoint                 (CH-40, nuevo)
 └── C-053 ResourceTrustDecision     (CH-40, nuevo)
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Instalar y actualizar paquetes de extensiones** (desde un registro, un repositorio o una ruta):
  infraestructura; el libro modela qué pasa con el código una vez que está.
- **Correr el código de una extensión en el entorno aislado:** posible con CH-35, pero no se cablea
  aquí. Una extensión `PROJECT` con hooks de código arbitrario debería correr aislada.
- **Apagar una extensión** (`DISABLED`) y quién puede hacerlo: un comando operacional (CH-18) que se
  conecta en la integración (CH-49).
- **Contribuciones de interfaz** (comandos, atajos, renderizadores): son adaptadores de UI (P-11).
- **Los hooks de los demás puntos** (`TRANSFORM_CONTEXT`, `BEFORE_REQUEST`, …) se validan con las
  mismas funciones; cada dueño los invoca. Este capítulo cablea solo `BEFORE_TOOL`, que es el que
  toca la autorización.

## 19. Siguiente Incremento (Next Increment)

Ahora el código de terceros entra por un registro y no puede saltarse la constitución. Pero la mayor
parte de las herramientas que un agente real usa no las escribe el equipo: vienen de servidores
externos que publican sus tools (MCP) o de APIs descritas con OpenAPI. Hoy no hay forma gobernada de
conectarlas.

El siguiente capítulo introduce las **conexiones** (P-38):
- un `ConnectionDescriptor` por servidor o API;
- las capabilities que traen pasan por `CapabilityRegistry` y `PolicyEngine` como cualquier otra
  (INV-E25);
- `CapabilityDescriptor` pasa a v3, con `sourceConnectionId` (ADR-005, que requiere tu aprobación).

Será CH-41 ("Conexiones: MCP y OpenAPI como Fuentes de Capabilities"). `next_chapter` queda en `null`
porque CH-41 todavía no existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): dos puntos de extensión sin contrato; un hook podría aprobar o cambiar lo
   autorizado; cualquier código del repositorio se carga.
2. **Patrones** (= §3): EVO-10 y P-12 existen, pero ningún componente los hace cumplir.
3. **Estructuras** (= §8): `ExtensionHost` (CMP-027), `ExtensionRegistration` (C-051), `HookPoint`
   (C-052) y `ResourceTrustDecision` (C-053).
4. **Modelos mentales** (= §4): EVO-10, INV-E24, P-12 y P-13.

**Bucles de retroalimentación**

- **Refuerzo:** cada extensión que interviene donde quiere agrega un camino no revisado. Un catálogo
  cerrado corta la espiral.
- **Equilibrio:** la confianza atada al hash. Cada cambio de código exige una decisión nueva.

**Punto de apalancamiento**

La decisión con mayor efecto es que cada `HookPoint` (C-052) admita solo un `HookOutcomeKind` sin valor de autorización: INV-E24
no depende de que cada extensión se porte bien, sino de que el tipo no permite expresarlo.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué exige `registerExtension` a una extensión de proyecto u organización, qué cubre una
   `ResourceTrustDecision`, y qué pasa con la extensión si su `contentHash` cambia?
   *(pregunta guía 1)*
2. ¿Cuáles son los tres valores de `HookOutcomeKind`, en qué momento corren los hooks de
   `BEFORE_TOOL` respecto de `PolicyEngine`, y qué devuelve `runBeforeToolHooks` si uno bloquea?
   *(pregunta guía 2)*
3. ¿Qué resultados admite `allowedOutcomes` para `TRANSFORM_CONTEXT` y para `BEFORE_TOOL`, y por qué
   `BEFORE_TOOL` no admite `TRANSFORM`? *(pregunta guía 3)*
4. ¿Qué componente ejecuta los hooks de cada punto, qué hace `ExtensionHost` con el resultado, y en
   qué se diferencia un hook de un suscriptor del `EventBus`? *(pregunta guía 4)*

### Explicar

1. `ToolRuntime` ya "ejecutaba hooks" desde CH-02. Explica por qué hace falta un componente aparte que
   decida qué hooks pueden correr y qué pueden devolver, y por qué ese componente no los ejecuta él
   mismo.
2. Explica por qué una `ResourceTrustDecision` se ata al hash del contenido y no solo al nombre del
   recurso, y qué ataque permitiría confiar por nombre.

### Conectar

1. En CH-38, `evaluatePolicyForCaller` partía de la decisión base de `PolicyEngine` y solo podía
   convertir un permiso en rechazo. ¿Qué tiene en común con un hook `BLOCK` de `BEFORE_TOOL`, y por
   qué ninguno de los dos puede convertir un rechazo en permiso?

### Espaciar

Las cuatro tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
