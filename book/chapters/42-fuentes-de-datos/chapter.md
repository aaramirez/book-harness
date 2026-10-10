---
id: CH-42
title: "Fuentes de Datos Gobernadas: Recuperar sin Tirarlo Todo al Contexto"
starting_version: "0.2.1"
ending_version: "0.3"
introduces_components: [CMP-029]
introduces_contracts: [C-055, C-056]
modifies_contracts: []
constitutional_articles: [P-01, P-14, P-22, P-31, P-38, INV-E07, INV-E11, INV-E26]
previous_chapter: CH-41
next_chapter: null
retrieval_set:
  expected_outcome:
    id: EO-CH42
    text: |
      Al terminar este capítulo podrás decidir de qué fuentes puede el agente recuperar datos, qué
      parte de cada fuente le corresponde a quien llama, y cuáles de los datos recuperados entran al
      contexto, y explicar cómo la clasificación de un dato lo acompaña hasta un resumen hecho con él.
  skeleton:
    id: SK-CH42
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
    components_to_be_introduced: [CMP-029]
    contracts_to_be_introduced: [C-055, C-056]
  guiding_questions:
    - id: GQ-CH42-01
      text: |
        Si el agente tiene acceso a la base de datos de clientes de toda la empresa, ¿debería ver los
        clientes de todas las empresas que atiende cuando le pregunta un usuario de una sola?
      answered_by: RQ-CH42-01
    - id: GQ-CH42-02
      text: |
        Si una fuente de datos nunca declaró qué tan sensibles son sus datos, ¿cómo debería tratarlos
        el arnés: como públicos o como restringidos?
      answered_by: RQ-CH42-02
    - id: GQ-CH42-03
      text: |
        Si una búsqueda devuelve cien documentos y solo caben diez en el contexto, ¿quién decide cuáles
        entran: la fuente que los encontró o el arnés que arma el contexto?
      answered_by: RQ-CH42-03
    - id: GQ-CH42-04
      text: |
        Si el agente resume una conversación que incluyó un dato confidencial, ¿puede el resumen
        tratarse como un dato público?
      answered_by: RQ-CH42-04
  systems_lens:
    iceberg_visible_fact: |
      Los datos llegan al contexto "ya dados": ContextEngine compone candidatos que nadie recuperó de
      ninguna fuente declarada, sin alcance por usuario, sin clasificación de origen ni frescura, y el
      resumen de una compactación se etiqueta como "conversation_history" aunque resuma datos
      confidenciales (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que P-14 y EVO-09 exigen seleccionar con procedencia y frescura, e
      INV-E11 que la política del dato lo acompañe, pero ningún componente decide qué puede recuperarse
      de una fuente ni cómo hereda la clasificación un dato derivado (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce RetrievalEngine (CMP-029), DataSourceDescriptor (C-055) y
      RetrievedCandidate (C-056); ContextEngine gana la selección de candidatos recuperados y el bloque
      del resumen con su procedencia, y DataGovernanceEngine la clasificación de datos derivados (ver
      sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-14 (seleccionar, no volcar), INV-E26 (una fuente sin clasificación es
      RESTRICTED), INV-E11 (la política del dato lo acompaña, también en un resumen) e INV-E07 (los
      datos de un tenant no se cruzan) (ver sección 4).
    reinforcing_loop: |
      Si los datos se vuelcan al contexto sin selección, cada fuente nueva agrega ruido, el modelo
      razona peor, y la tentación es agregar todavía más contexto "por las dudas". Recuperar con alcance
      y seleccionar bajo presupuesto corta la espiral.
    balancing_loop: |
      El techo de clasificación es el mecanismo de equilibrio: por mucho que se recupere, ningún
      candidato más sensible que el techo entra al contexto.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es separar a RetrievalEngine (CMP-029), que decide
      qué puede recuperarse de cada fuente para el llamante, de ContextEngine, que decide qué entra al
      contexto: así una fuente nunca impone su contenido, y el contexto nunca ve lo que el llamante no
      podía recuperar.
  recall_questions:
    - id: RQ-CH42-01
      text: |
        ¿Qué devuelve scopeFor para una fuente PER_TENANT y para una PER_PRINCIPAL, y qué pasa si no hay
        un llamante que satisfaga la regla?
    - id: RQ-CH42-02
      text: |
        ¿Qué devuelve effectiveSourceClassification para una fuente sin clasificación, y cómo combina
        governRetrievedCandidate la clasificación de la fuente con la de la etiqueta?
    - id: RQ-CH42-03
      text: |
        ¿Qué decide retrieveCandidates sobre un registro más viejo que la frescura de su fuente, y qué
        decide selectRetrievedCandidates con el techo de clasificación y el presupuesto de tokens?
    - id: RQ-CH42-04
      text: |
        ¿Qué hereda classifyDerivedData de las etiquetas de sus fuentes, qué devuelve sin fuentes, y qué
        procedencia usa summaryContextBlock?
  explain_prompts:
    - id: EP-CH42-01
      text: |
        ContextEngine ya seleccionaba y rankeaba contexto. Explica, como si hablaras con alguien sin
        contexto técnico, por qué recuperar de una fuente es una decisión distinta que merece su propio
        componente, y por qué RetrievalEngine no decide qué entra al contexto.
      target_entity: CMP-029
    - id: EP-CH42-02
      text: |
        Explica por qué un DataSourceDescriptor declara una regla de alcance por llamante, y qué se
        rompería en un arnés que atiende a varias empresas si la fuente se consultara siempre entera.
      target_entity: C-055
  interleaved_questions:
    - id: IQ-CH42-01
      text: |
        En CH-20, classifyData producía una DataGovernanceLabel y rechazaba hacia RESTRICTED un dato sin
        regla conocida. ¿Qué agrega classifyDerivedData para un dato hecho con otros, y por qué un
        resumen no puede quedar menos restringido que sus fuentes?
      current_chapter_entities: [C-056, CMP-029]
      prior_chapter_entities: [C-030, CMP-018]
      prior_chapter: CH-20
  flashcards:
    - id: FC-CH42-01
      front: |
        ¿Qué es un DataSourceDescriptor (C-055)?
      back: |
        Una fuente declarada y de solo lectura: tipo (SQL, FILES, HTTP, STREAM, CONNECTION_RESOURCE),
        clasificación (RESTRICTED si falta), regla de alcance (SHARED, PER_TENANT, PER_PRINCIPAL),
        conexión si son recursos MCP, y frescura.
      source_entity: C-055
      chapter_introduced_in: CH-42
      review_stage: DAY_1
    - id: FC-CH42-02
      front: |
        ¿Qué es un RetrievedCandidate (C-056)?
      back: |
        Un candidato recuperado: contenido, procedencia, clasificación de la fuente, puntaje,
        observedAt y la DataGovernanceLabel que lo acompaña. ContextEngine decide si entra al contexto.
      source_entity: C-056
      chapter_introduced_in: CH-42
      review_stage: DAY_1
    - id: FC-CH42-03
      front: |
        ¿Qué posee RetrievalEngine (CMP-029) y qué no?
      back: |
        Posee recuperar de fuentes declaradas con alcance por llamante, clasificación (INV-E26) y
        frescura. No selecciona el contexto (ContextEngine), no clasifica con reglas de gobierno
        (DataGovernanceEngine), no autoriza, no resuelve credenciales ni escribe.
      source_entity: CMP-029
      chapter_introduced_in: CH-42
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH42-01
      recall_question: RQ-CH42-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH42-02
      recall_question: RQ-CH42-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH42-03
      recall_question: RQ-CH42-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH42-04
      recall_question: RQ-CH42-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 42 — Fuentes de Datos Gobernadas: Recuperar sin Tirarlo Todo al Contexto

> **Regla constitucional (P-14):** el contexto se selecciona, no se vuelca.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir de qué fuentes puede el agente
recuperar datos, qué parte de cada fuente le corresponde a quien llama, y cuáles de los datos
recuperados entran al contexto. También podrás explicar cómo la clasificación de un dato lo acompaña
hasta un resumen hecho con él.

**Esqueleto.** Cuarto capítulo de la versión 0.3. Introduce el componente `RetrievalEngine` y dos
contratos, y amplía `ContextEngine` y `DataGovernanceEngine`.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si el agente tiene acceso a la base de datos de clientes de toda la empresa, ¿debería ver los
   clientes de todas las empresas que atiende cuando le pregunta un usuario de una sola?
2. Si una fuente de datos nunca declaró qué tan sensibles son sus datos, ¿cómo debería tratarlos el
   arnés: como públicos o como restringidos?
3. Si una búsqueda devuelve cien documentos y solo caben diez en el contexto, ¿quién decide cuáles
   entran: la fuente que los encontró o el arnés que arma el contexto?
4. Si el agente resume una conversación que incluyó un dato confidencial, ¿puede el resumen tratarse
   como un dato público?

## 1. Arquitectura Actual (Current Architecture)

- **`ContextEngine` (CMP-004, CH-04)** selecciona, rankea, compone y compacta candidatos bajo
  presupuesto. Pero sus candidatos llegan **"ya dados, sin retrieval"**, y cada bloque se etiqueta
  con una procedencia fija, `"conversation_history"`.
- **`DataGovernanceEngine` (CMP-018, CH-20)** clasifica un dato (`classifyData`) y produce una
  `DataGovernanceLabel` (C-030) consultable por su `subjectRef`. Un dato sin regla conocida queda
  `RESTRICTED`.
- **CH-29** produce un `CompactionSummary` con su propia `provenance`, pero el bloque del resumen
  sigue entrando como `"conversation_history"` (deuda D-015) y sin etiqueta de gobierno (D-016).
- **CH-31** hace viajar el `Principal` en cada turno; datos y memoria todavía no lo usan (D-019).
- **CH-34** activa runs desde un stream; nadie lo lee como fuente de datos (D-024).
- **CH-41** conecta servidores MCP, que además de tools publican recursos; nadie los trata como
  datos (D-047).

## 2. El Problema (Problem)

Un agente de soporte necesita, para responder, los tickets del cliente, el contrato vigente y los
últimos eventos de su cuenta. Hoy:
- **no hay fuentes:** alguien tiene que poner esos datos en los candidatos antes del turno, y nadie
  registra de dónde salieron;
- **no hay alcance:** la base de tickets tiene los de todas las empresas que atiende el arnés, y nada
  impide recuperar los de otra;
- **no hay clasificación de origen:** un documento confidencial y una página pública llegan iguales;
- **no hay frescura:** el estado de la cuenta de hace tres días llega como si fuera actual;
- **el resumen "lava" la clasificación:** si el agente resume una conversación con datos
  confidenciales, el resumen entra como historial común.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **ContextEngine selecciona entre lo que recibe, pero no decide qué se puede recuperar.** Si
  recuperara, mezclaría dos preguntas: "¿qué puede ver este llamante?" y "¿qué conviene que vea el
  modelo?".
- **`classifyData` clasifica un dato, no un dato derivado.** Un resumen no tiene una regla propia;
  su clasificación sale de lo que resume (INV-E11).
- **Sin descriptor de fuente no hay dónde declarar la clasificación**, y INV-E26 exige que toda
  fuente la declare.
- **Ningún componente posee la decisión** "¿qué puede recuperarse de esta fuente para este llamante,
  con qué procedencia y frescura?". No es de `ContextEngine` (selección), ni de `DataGovernanceEngine`
  (clasificación), ni de `PolicyEngine` (autorización). Por eso este capítulo introduce un componente
  (EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-01   Context is a first-class architectural component.
           El contexto se arma con candidatos recuperados y seleccionados, no con datos sueltos.
    P-14   Context should be selected, not dumped.
           RetrievalEngine recupera lo acotado; ContextEngine selecciona bajo presupuesto.
    P-22   Enterprise data is governed throughout its lifecycle.
           Cada candidato y cada resumen llevan su etiqueta de gobierno.
    P-31   Identity travels with every turn.
           El alcance de una fuente se aplica sobre caller.current.
    P-38   External capabilities enter only through declared connections.
           Los recursos de un servidor MCP entran por la conexión declarada (CH-41).

Evolution rule applied
    EVO-09 Context has provenance. Procedencia por candidato, frescura por fuente.

Invariants preserved
    INV-E07  Los datos de un tenant están aislados. PER_TENANT y PER_PRINCIPAL los separan.
    INV-E11  La política del dato lo acompaña. classifyDerivedData hace que un resumen herede.
    INV-E26  (Amendment v1.2) Una fuente sin clasificación es RESTRICTED.

Component ownership changes
    Nuevo: RetrievalEngine (CMP-029).
    ContextEngine gana selectRetrievedCandidates y summaryContextBlock (dentro de "selección",
    "ranking" y "provenance").
    DataGovernanceEngine gana moreRestrictive y classifyDerivedData (dentro de INV-E11).

Contract changes
    Nuevos: C-055 DataSourceDescriptor, C-056 RetrievedCandidate.

Security implications
    El contexto nunca ve lo que el llamante no podía recuperar ni lo que excede el techo de
    clasificación (ver sección 15).

Observability implications
    Nuevo AgentEventType: DATA_RETRIEVED.
```

## 5. Conceptos Nuevos (New Concepts)

- **Fuente de datos declarada:** un lugar del que el agente puede leer, registrado con un
  `DataSourceDescriptor`. Puede ser una base SQL, un repositorio de archivos, una API HTTP, un stream de
  eventos o los recursos que publica un servidor MCP. Siempre de solo lectura: escribir es una tool.
- **Regla de alcance:** qué parte de la fuente le corresponde al llamante.
  - `SHARED`: toda la fuente (por ejemplo, la documentación pública);
  - `PER_TENANT`: solo lo de la empresa del llamante;
  - `PER_PRINCIPAL`: solo lo del propio llamante (por ejemplo, su correo).
- **Recuperar y seleccionar son dos pasos.** Recuperar trae lo que el llamante **puede** ver de una
  fuente; seleccionar decide qué **conviene** que vea el modelo, dentro del presupuesto y por debajo del
  techo de clasificación.
- **Frescura:** cuánto puede tener de antigüedad un dato de esa fuente para seguir siendo útil. Un
  registro más viejo se descarta. En un stream es obligatoria: se lee una ventana reciente.
- **Dato derivado:** un dato producido a partir de otros, como un resumen. Su etiqueta hereda la
  clasificación más restrictiva, la preservación legal y el plazo de retención más corto de sus
  fuentes.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `DataGovernanceLabel` (C-030), `ConnectionDescriptor` (C-054), `CompactionSummary`
  (C-037), `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `AgentId`, `Timestamp`.

| Identificador (heredado o nuevo, sin `C-XXX` propio) | Rol en este capítulo |
|---|---|
| `DataSourceId` | identificador nuevo de una fuente |
| `RetrievedCandidateId` | identificador nuevo de un candidato recuperado |
| `ConnectionId` | identificador de una conexión (CH-41) |
| `DataClassificationLevel` | `PUBLIC` / `INTERNAL` / `CONFIDENTIAL` / `RESTRICTED` (CH-20) |
| `DataGovernanceLabelId` | identificador de una etiqueta de gobierno (CH-20) |
| `ContextBlock` | bloque de un `ContextSnapshot` (CH-04) |
| `AgentEventType` | se agrega `DATA_RETRIEVED` |
| `ErrorCategory` | reutiliza `CONTEXT` y `VALIDATION` |

### Partes de una fuente (embebidas)

```pseudocode
ENUM DataSourceKind
    SQL
    FILES
    HTTP
    STREAM
    CONNECTION_RESOURCE
END
```

```pseudocode
ENUM DataAccessMode
    READ_ONLY
END
```

```pseudocode
ENUM DataScopeRule
    SHARED
    PER_TENANT
    PER_PRINCIPAL
END
```

### `DataSourceDescriptor` — una fuente declarada (C-055)

```pseudocode
STRUCT DataSourceDescriptor
    sourceId: DataSourceId
    kind: DataSourceKind
    endpointRef: Text
    classification: Optional<DataClassificationLevel>
    access: DataAccessMode
    scopeRule: DataScopeRule
    connectionId: Optional<ConnectionId>
    credentialName: Optional<Text>
    freshnessSeconds: Optional<Integer>
END
```

`DataAccessMode` tiene un solo valor a propósito: declarar `READ_ONLY` deja escrito que una fuente
nunca es un canal de escritura.

### `DataScope` y `SourceRecord` — lo que se consulta y lo que vuelve (embebidos)

```pseudocode
STRUCT DataScope
    tenantId: Optional<Text>
    principalId: Optional<Text>
END
```

```pseudocode
STRUCT SourceRecord
    ref: Text
    content: Value
    score: Number
    observedAt: Timestamp
END
```

`SourceRecord` es lo que el adaptador de la fuente devolvió para la consulta, ya acotada por el
`DataScope`.

### `RetrievedCandidate` — un candidato recuperado (C-056)

```pseudocode
STRUCT RetrievedCandidate
    candidateId: RetrievedCandidateId
    sourceId: DataSourceId
    content: Value
    provenance: Text
    classification: DataClassificationLevel
    score: Number
    observedAt: Timestamp
    label: Optional<DataGovernanceLabel>
END
```

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-055
Name:                   DataSourceDescriptor
Version:                v1
Introduced In:          CH-42
Used By:                [CMP-029]
Constitutional Impact:  [P-22, P-38, INV-E07, INV-E26]
```

```text
ID:                     C-056
Name:                   RetrievedCandidate
Version:                v1
Introduced In:          CH-42
Used By:                [CMP-029, CMP-004]
Constitutional Impact:  [P-14, INV-E11, INV-E26]
```

## 8. Responsabilidades de Componentes (Component Responsibilities)

```pseudocode
COMPONENT RetrievalEngine
    consumes: ExecutionContext, ConnectionDescriptor, DataSourceDescriptor
    produces: RetrievedCandidate, AgentEvent, HarnessError
END
```

```text
COMPONENT: RetrievalEngine (CMP-029)

Responsibility:
    Recuperar, de las fuentes declaradas, los candidatos que una consulta puede ver — con la regla de
    alcance de cada fuente sobre el llamante, su clasificación (o RESTRICTED) y su frescura —, con
    procedencia, para que ContextEngine decida cuáles entran al contexto.

Owns:
    - "Context should be selected, not dumped" (P-14): recuperar solo lo acotado
    - "Every data source declares a classification; an undeclared source is RESTRICTED" (INV-E26)
    - "Nuevas fuentes de contexto deben identificar origen, freshness y reglas de acceso" (EVO-09)
    - aplicar la regla de alcance sobre caller.current, fail-closed sin llamante que la satisfaga
    - rechazar una fuente que no sea de solo lectura, o de recursos sin conexión declarada

Does NOT own:
    - seleccionar y componer el contexto (ContextEngine, CH-04). Es la frontera más importante del
      capítulo: RetrievalEngine decide QUÉ PUEDE recuperarse; ContextEngine decide QUÉ ENTRA.
    - clasificar con reglas de gobierno (DataGovernanceEngine, CH-20)
    - autorizar (PolicyEngine) · resolver credenciales (CredentialBroker) · escribir en una fuente
    - hablar el protocolo de cada fuente (adaptador)
```

**Otros componentes ganan funciones dentro de su `owns`:**
- `ContextEngine` ("selección", "ranking", "provenance"): `selectRetrievedCandidates` y
  `summaryContextBlock`;
- `DataGovernanceEngine` (INV-E11, "la política del dato lo acompaña"): `moreRestrictive` y
  `classifyDerivedData`.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
RetrievalEngine
    consumes → ExecutionContext, ConnectionDescriptor, DataSourceDescriptor
    produces → RetrievedCandidate, AgentEvent, HarnessError
    depends on (componentes) → (ninguno)
```

**En un turno:**
1. al registrar una fuente: `validateDataSource`;
2. antes de armar el contexto: `scopeFor` → el adaptador consulta la fuente con ese alcance →
   `retrieveCandidates`;
3. `governRetrievedCandidate` (integración): `classifyData` (CH-20) por candidato;
4. `selectRetrievedCandidates` (ContextEngine): techo y presupuesto → `ContextBlock`;
5. los bloques se suman a los del historial en el `ContextSnapshot` (CH-04).

**Al compactar (CH-29, CH-38):**
1. `classifyDerivedData` → etiqueta del resumen, a partir de las etiquetas de lo resumido;
2. `summaryContextBlock` → el bloque del resumen con su propia procedencia.

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Fuente (adaptador) → RetrievalEngine (alcance, clasificación, frescura) → DataGovernanceEngine (etiqueta)
                   → ContextEngine (techo, presupuesto) → ContextSnapshot
```

**Vista 2 — Sequence: el contexto de un turno de soporte**

```text
Integración
   │ scopeFor(fuente "tickets" PER_TENANT, execution)      → DataScope(tenantId = "acme")
   │ adaptador consulta tickets de "acme"                  → 40 SourceRecord
   │ retrieveCandidates(…)                                 → 37 candidatos (3 viejos, fuera) + DATA_RETRIEVED
   │ governRetrievedCandidate × 37 (classifyData, CH-20)   → etiqueta y clasificación efectiva
   │ selectRetrievedCandidates(…, techo CONFIDENTIAL, 6000) → 9 ContextBlock (los RESTRICTED quedan fuera)
```

**Vista 2b — Sequence: un resumen que no lava la clasificación**

```text
classifyDerivedData("resumen-7", …, [INTERNAL, CONFIDENTIAL, PUBLIC]) → etiqueta CONFIDENTIAL
summaryContextBlock(resumen) → ContextBlock(provenance = "compaction:run-12:7")
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

### RetrievalEngine: fuente, alcance y recuperación

```pseudocode
FUNCTION effectiveSourceClassification(
    source: DataSourceDescriptor
) -> DataClassificationLevel

    IF source.classification == NULL
        RETURN RESTRICTED
    END

    RETURN source.classification
END
```

```pseudocode
FUNCTION validateDataSource(
    source: DataSourceDescriptor,
    connections: List<ConnectionDescriptor>
) -> DataSourceDescriptor

    connectionDeclared: Boolean = FALSE
    FOR EACH connection IN connections
        IF source.connectionId != NULL AND connection.connectionId == source.connectionId
            connectionDeclared = TRUE
        END
    END

    IF source.access != READ_ONLY
        OR (source.kind == CONNECTION_RESOURCE AND NOT connectionDeclared)
        OR (source.kind == STREAM AND source.freshnessSeconds == NULL)

        THROW HarnessError(
            category = VALIDATION,
            code = "INVALID_DATA_SOURCE",
            message = "Una fuente debe ser de solo lectura; los recursos de conexión necesitan una conexión declarada y un stream necesita frescura",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN source
END
```

```pseudocode
FUNCTION scopeFor(
    source: DataSourceDescriptor,
    execution: ExecutionContext
) -> DataScope

    IF source.scopeRule == SHARED
        RETURN DataScope(tenantId = NULL, principalId = NULL)
    END

    IF source.scopeRule == PER_TENANT
        caller: Principal = requireTenantCaller(execution)
        RETURN DataScope(tenantId = caller.tenantId, principalId = NULL)
    END

    IF execution.caller == NULL
        THROW HarnessError(
            category = CONTEXT,
            code = "CALLER_REQUIRED_FOR_SOURCE",
            message = "Esta fuente se recupera por llamante y el turno no tiene un llamante verificado",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    RETURN DataScope(
        tenantId = execution.caller.current.tenantId,
        principalId = execution.caller.current.principalId
    )
END
```

```pseudocode
FUNCTION retrieveCandidates(
    source: DataSourceDescriptor,
    records: List<SourceRecord>,
    now: Timestamp,
    execution: ExecutionContext,
    agentId: AgentId
) -> List<RetrievedCandidate>

    candidates: List<RetrievedCandidate> = []
    classification: DataClassificationLevel = effectiveSourceClassification(source)

    FOR EACH record IN records
        fresh: Boolean = source.freshnessSeconds == NULL
            OR secondsBetween(record.observedAt, now) <= source.freshnessSeconds

        IF fresh
            candidates = append(candidates, RetrievedCandidate(
                candidateId = newRetrievedCandidateId(),
                sourceId = source.sourceId,
                content = record.content,
                provenance = sourceProvenance(source.sourceId, record.ref),
                classification = classification,
                score = record.score,
                observedAt = record.observedAt,
                label = NULL
            ))
        END
    END

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = DATA_RETRIEVED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = candidates
    )

    RETURN candidates
END
```

### DataGovernanceEngine: la clasificación más restrictiva y los datos derivados

```pseudocode
FUNCTION moreRestrictive(
    a: DataClassificationLevel,
    b: DataClassificationLevel
) -> DataClassificationLevel

    IF a == RESTRICTED OR b == RESTRICTED
        RETURN RESTRICTED
    END

    IF a == CONFIDENTIAL OR b == CONFIDENTIAL
        RETURN CONFIDENTIAL
    END

    IF a == INTERNAL OR b == INTERNAL
        RETURN INTERNAL
    END

    RETURN PUBLIC
END
```

```pseudocode
FUNCTION classifyDerivedData(
    subjectRef: Text,
    provenance: Text,
    sources: List<DataGovernanceLabel>,
    legalHold: Boolean
) -> DataGovernanceLabel

    classification: DataClassificationLevel = PUBLIC
    hold: Boolean = legalHold
    deadline: Optional<Timestamp> = NULL
    residency: Optional<Text> = NULL

    IF length(sources) == 0
        classification = RESTRICTED
    END

    FOR EACH label IN sources
        classification = moreRestrictive(classification, label.classification)
        hold = hold OR label.legalHold

        IF label.retentionDeadline != NULL AND (deadline == NULL OR label.retentionDeadline < deadline)
            deadline = label.retentionDeadline
        END

        IF residency == NULL
            residency = label.residencyRequirement
        END
    END

    RETURN DataGovernanceLabel(
        id = newDataGovernanceLabelId(),
        subjectRef = subjectRef,
        classification = classification,
        residencyRequirement = residency,
        retentionDeadline = deadline,
        legalHold = hold,
        lineageRef = provenance,
        classifiedAt = now()
    )
END
```

### ContextEngine: seleccionar lo recuperado y el bloque del resumen

```pseudocode
FUNCTION selectRetrievedCandidates(
    candidates: List<RetrievedCandidate>,
    ceiling: DataClassificationLevel,
    tokenBudget: Integer
) -> List<ContextBlock>

    blocks: List<ContextBlock> = []
    usedTokens: Integer = 0

    FOR EACH candidate IN sortByScoreDescending(candidates)
        withinCeiling: Boolean = moreRestrictive(candidate.classification, ceiling) == ceiling
        tokens: Integer = estimateTokens(candidate.content)

        IF withinCeiling AND usedTokens + tokens <= tokenBudget
            blocks = append(blocks, ContextBlock(
                provenance = candidate.provenance,
                content = candidate.content,
                compacted = FALSE
            ))
            usedTokens = usedTokens + tokens
        END
    END

    RETURN blocks
END
```

```pseudocode
FUNCTION summaryContextBlock(
    summary: CompactionSummary
) -> ContextBlock

    RETURN ContextBlock(
        provenance = summary.provenance,
        content = summary,
        compacted = TRUE
    )
END
```

### Integración: gobernar cada candidato

```pseudocode
FUNCTION governRetrievedCandidate(
    candidate: RetrievedCandidate,
    legalHold: Boolean,
    execution: ExecutionContext,
    agentId: AgentId
) -> RetrievedCandidate

    label: DataGovernanceLabel = classifyData(
        candidate.provenance, candidate.provenance, legalHold, execution, agentId
    )

    RETURN RetrievedCandidate(
        candidateId = candidate.candidateId,
        sourceId = candidate.sourceId,
        content = candidate.content,
        provenance = candidate.provenance,
        classification = moreRestrictive(candidate.classification, label.classification),
        score = candidate.score,
        observedAt = candidate.observedAt,
        label = label
    )
END
```

Utilidades primitivas:
- `secondsBetween`, `sourceProvenance` (produce `"<fuente>:<ref>"`), `sortByScoreDescending`,
  `estimateTokens` (CH-04), `length` y `append`;
- `newRetrievedCandidateId`, `newDataGovernanceLabelId`, `newEventId` y `now`.

La etiqueta del candidato se consulta por su `subjectRef`, que es la procedencia del bloque: así la
política del dato lo acompaña dentro del `ContextSnapshot` sin cambiar `ContextBlock` (INV-E11).

Nótese lo que estas funciones **no** hacen:
- `retrieveCandidates` no consulta la fuente: recibe lo que el adaptador devolvió para el alcance de
  `scopeFor`;
- ninguna escribe en una fuente;
- `selectRetrievedCandidates` nunca deja entrar un candidato por encima del techo, aunque tenga el
  mejor puntaje.

## 12. Transiciones de Estado (State Transitions)

```text
Fuente
    sin clasificación                         → RESTRICTED (INV-E26)
    no READ_ONLY | recursos sin conexión | stream sin frescura → INVALID_DATA_SOURCE

Alcance
    SHARED        → toda la fuente
    PER_TENANT    → tenant del llamante (TENANT_CALLER_REQUIRED si no lo hay, CH-31)
    PER_PRINCIPAL → el llamante (CALLER_REQUIRED_FOR_SOURCE si no lo hay)

Registro → candidato → bloque
    más viejo que la frescura   → descartado
    por encima del techo        → fuera del contexto
    no cabe en el presupuesto   → fuera del contexto
    en regla                    → ContextBlock con su procedencia

Dato derivado
    sin fuentes → RESTRICTED; con fuentes → la más restrictiva, hold si alguna, retención más corta
```

## 13. Semántica de Fallos (Failure Semantics)

Códigos nuevos de `HarnessError`, con `ErrorCategory` ya existentes:

```text
VALIDATION  INVALID_DATA_SOURCE         recoverable: FALSE, retryable: FALSE
CONTEXT     CALLER_REQUIRED_FOR_SOURCE  recoverable: FALSE, retryable: FALSE
```

`scopeFor` hereda `TENANT_CALLER_REQUIRED` (CH-31). Una fuente que no responde es un fallo del
adaptador: el turno sigue con los candidatos de las demás fuentes, y ContextEngine arma el contexto con
lo que hay (CH-04).

## 14. Eventos Producidos (Events Produced)

```text
DATA_RETRIEVED — candidatos recuperados de una fuente (payload: List<RetrievedCandidate>)
```

Se reutilizan `DATA_CLASSIFIED` (CH-20) y `CONTEXT_SNAPSHOT_ASSEMBLED` (CH-04).

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Un llamante solo recupera lo suyo.** Con `PER_TENANT`, la consulta nunca sale del tenant del
  llamante verificado; el tenant no sale del prompt (INV-E07).
- **Lo que nadie clasificó es lo más sensible.** Una fuente sin clasificación cuenta como
  `RESTRICTED`, y la clasificación más restrictiva entre la de la fuente y la de la etiqueta gana.
- **El techo protege al modelo.** Un candidato `RESTRICTED` no entra a un contexto con techo
  `CONFIDENTIAL`, por mucho que la fuente lo considere el más relevante.
- **Un resumen no lava datos.** Hereda la clasificación más restrictiva, la preservación legal y la
  retención más corta de lo que resume.
- **Recuperar no autoriza.** Si un dato puede verse en absoluto lo sigue decidiendo `PolicyEngine`, que
  también fija el techo.
- **Una fuente no se escribe.** Escribir es una tool, con su política, su journal y su replay.

## 16. Tests (Tests)

```text
TEST UndeclaredSourceClassificationIsRestricted
TEST SourceThatIsNotReadOnlyIsInvalid
TEST ConnectionResourceWithoutDeclaredConnectionIsInvalid
TEST StreamSourceWithoutFreshnessIsInvalid
TEST PerTenantScopeUsesTheCallersTenant
TEST PerTenantScopeWithoutTenantCallerIsRejected
TEST PerPrincipalScopeWithoutCallerIsRejected
TEST StaleRecordsAreDropped
TEST RetrievalEmitsDataRetrieved
TEST GovernedCandidateKeepsTheMoreRestrictiveClassification
TEST CandidateAboveTheCeilingNeverEntersTheContext
TEST SelectionRespectsTheTokenBudget
TEST DerivedDataInheritsTheMostRestrictiveClassification
TEST DerivedDataInheritsLegalHoldAndTheEarliestRetention
TEST DerivedDataWithoutSourcesIsRestricted
TEST SummaryBlockUsesTheSummaryProvenance
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.3 en curso, después de CH-42) — 29 componentes, 56 contratos, 43 capítulos

Components — 29
 ├── CMP-029 RetrievalEngine         (CH-42, nuevo — Data & Context Plane)
 ├── CMP-004 ContextEngine           (+ selectRetrievedCandidates, summaryContextBlock)
 └── CMP-018 DataGovernanceEngine    (+ moreRestrictive, classifyDerivedData)

Contracts — 56
 ├── C-055 DataSourceDescriptor      (CH-42, nuevo)
 └── C-056 RetrievedCandidate        (CH-42, nuevo)

Deuda: D-015, D-016, D-019, D-024 y D-047 resueltas.
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Búsqueda semántica, índices y embeddings:** son parte del adaptador de cada fuente; el arnés
  recibe registros con puntaje. No es deuda.
- **Memoria de largo plazo del agente** como fuente propia: es una fuente más, con
  `PER_PRINCIPAL` o `PER_TENANT`. Escribir en ella es una tool. No es deuda.
- **Techos de clasificación por audiencia de la sesión** (pública, privada): llegan con la
  observabilidad por audiencia, en CH-46, que ya planea el `SessionAudience`. No es deuda.
- **Activar un run desde un stream** sigue siendo el Ingress Adapter de CH-34. No es deuda.

## 19. Siguiente Incremento (Next Increment)

Ahora el agente lee de fuentes declaradas, solo lo que le corresponde al llamante, y el contexto se
arma con lo seleccionado. Pero el agente todavía no sabe repartir su **presupuesto**: un run que delega
trabajo en otro no tiene forma de darle una parte de su presupuesto sin regalarle todo.

El siguiente capítulo introduce los **presupuestos que se heredan**:
- `ExecutionUsage` pasa a ser un contrato;
- `ExecutionBudget` pasa a v2, con el presupuesto del padre (ADR-004, que requiere tu aprobación);
- la regla de que un hijo nunca recibe más de lo que le queda al padre (INV-E21).

Será CH-43 ("Presupuestos que se Heredan"). `next_chapter` queda en `null` porque CH-43 todavía no
existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): los datos llegan "ya dados", sin fuente, alcance, clasificación ni
   frescura, y un resumen lava la clasificación.
2. **Patrones** (= §3): P-14, EVO-09 e INV-E11 existen, pero nadie decide qué puede recuperarse ni
   cómo hereda un dato derivado.
3. **Estructuras** (= §8): `RetrievalEngine` (CMP-029), `DataSourceDescriptor` (C-055),
   `RetrievedCandidate` (C-056), y funciones nuevas en `ContextEngine` y `DataGovernanceEngine`.
4. **Modelos mentales** (= §4): P-14, INV-E26, INV-E11 e INV-E07.

**Bucles de retroalimentación**

- **Refuerzo:** más contexto "por las dudas" empeora el razonamiento y pide todavía más. Recuperar
  con alcance y seleccionar corta la espiral.
- **Equilibrio:** el techo de clasificación. Nada más sensible que el techo entra al contexto.

**Punto de apalancamiento**

La decisión con mayor efecto es separar a `RetrievalEngine` (CMP-029), que decide qué puede
recuperarse de cada fuente para el llamante, de `ContextEngine`, que decide qué entra al contexto.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué devuelve `scopeFor` para una fuente `PER_TENANT` y para una `PER_PRINCIPAL`, y qué pasa si no
   hay un llamante que satisfaga la regla? *(pregunta guía 1)*
2. ¿Qué devuelve `effectiveSourceClassification` para una fuente sin clasificación, y cómo combina
   `governRetrievedCandidate` la clasificación de la fuente con la de la etiqueta? *(pregunta guía 2)*
3. ¿Qué decide `retrieveCandidates` sobre un registro más viejo que la frescura de su fuente, y qué
   decide `selectRetrievedCandidates` con el techo de clasificación y el presupuesto de tokens?
   *(pregunta guía 3)*
4. ¿Qué hereda `classifyDerivedData` de las etiquetas de sus fuentes, qué devuelve sin fuentes, y qué
   procedencia usa `summaryContextBlock`? *(pregunta guía 4)*

### Explicar

1. `ContextEngine` ya seleccionaba y rankeaba contexto. Explica por qué recuperar de una fuente es una
   decisión distinta que merece su propio componente, y por qué `RetrievalEngine` no decide qué entra
   al contexto.
2. Explica por qué un `DataSourceDescriptor` declara una regla de alcance por llamante, y qué se
   rompería en un arnés que atiende a varias empresas si la fuente se consultara siempre entera.

### Conectar

1. En CH-20, `classifyData` producía una `DataGovernanceLabel` y rechazaba hacia `RESTRICTED` un dato
   sin regla conocida. ¿Qué agrega `classifyDerivedData` para un dato hecho con otros, y por qué un
   resumen no puede quedar menos restringido que sus fuentes?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
