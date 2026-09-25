---
id: CH-29
title: "Compactar sin Perder el Hilo: Resúmenes Estructurados y Sesiones en Árbol"
starting_version: "0.1"
ending_version: "0.2"
introduces_components: []
introduces_contracts: [C-037, C-038]
modifies_contracts: [C-020]
constitutional_articles: [P-01, P-02, P-08, P-14, INV-07, INV-12, INV-13, INV-18, INV-19]
previous_chapter: CH-28
next_chapter: CH-30
retrieval_set:
  expected_outcome:
    id: EO-CH29
    text: |
      Al terminar este capítulo podrás decidir cuándo un historial necesita compactarse, dónde
      cortarlo sin separar nunca una tool call de su resultado y qué parte del trabajo le toca al
      modelo (proponer el resumen) y cuál al arnés (validar su forma y el punto de corte) — y podrás
      distinguir navegar hacia atrás dentro de una sesión, que no borra nada, de ramificar en una
      sesión nueva.
  skeleton:
    id: SK-CH29
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
    contracts_to_be_introduced: [C-037, C-038]
  guiding_questions:
    - id: GQ-CH29-01
      text: |
        Cuando una conversación ya no cabe en lo que el modelo puede leer, ¿conviene primero pedirle
        al modelo que la resuma, o hay un paso más barato que muchas veces alcanza sin llamarlo?
      answered_by: RQ-CH29-01
    - id: GQ-CH29-02
      text: |
        Si hay que cortar la conversación en "lo viejo que se resume" y "lo reciente que se conserva
        tal cual", ¿qué dos mensajes nunca deberían quedar a lados distintos del corte, y por qué?
      answered_by: RQ-CH29-02
    - id: GQ-CH29-03
      text: |
        Si el modelo escribe el resumen de lo viejo, ¿quién decide desde qué mensaje empieza lo que
        se conserva literal — y qué pasa si el resumen dice otra cosa?
      answered_by: RQ-CH29-03
    - id: GQ-CH29-04
      text: |
        Si el usuario quiere volver a un punto anterior de la conversación para probar otra
        alternativa, ¿hay que borrar lo que se hizo después, o crear una conversación nueva, o hay
        una tercera opción?
      answered_by: RQ-CH29-04
  systems_lens:
    iceberg_visible_fact: |
      Las conversaciones largas dejan de caber en lo que el modelo puede leer, y cada implementación
      reacciona distinto: trunca por el principio, pierde decisiones tomadas, corta en medio de una
      llamada a una herramienta dejando su resultado huérfano, o borra lo que el usuario hizo al
      volver atrás (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que, sin reglas declaradas, la compactación se decide en el lugar
      donde el presupuesto se agota — y ese lugar no conoce ni la estructura del turno (tool call y
      resultado van juntos) ni qué información es crítica. CH-04 compactaba candidato por
      candidato; nada cubría el historial completo ni la navegación dentro de una sesión (ver
      sección 3).
    iceberg_structures: |
      Este capítulo introduce CompactionSummary (C-037) y BranchSummary (C-038), y lleva
      SessionState (C-020) a v2 con activeCheckpointId y branchSummaries — dentro del owns ya
      existente de ContextEngine (compaction, context budgets, provenance) y de SessionManager
      (branching, checkpoints, reconstruction). El modelo propone el resumen; el arnés valida su
      forma y el punto de corte (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-14 (el contexto se selecciona, no se vuelca), P-01 (el contexto es
      un componente de primera clase) y P-08 (el estado del agente y el de la sesión son cosas
      distintas): la sesión conserva todo lo que pasó; el contexto elige qué ve el modelo (ver
      sección 4).
    reinforcing_loop: |
      Truncar sin estructura hace que el modelo olvide decisiones ya tomadas, las vuelva a discutir,
      y eso genera todavía más historial que truncar. Un resumen con campos fijos (decisions,
      constraints, nextSteps) corta esa espiral: lo decidido sobrevive a la compactación.
    balancing_loop: |
      La fase 1 (recortar sin modelo los resultados de tools demasiado grandes) es el mecanismo de
      equilibrio: resuelve la mayoría de los desbordes sin gastar una llamada al modelo, y solo si no
      alcanza se pasa a la fase 2.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que el punto de corte lo fije ContextEngine y
      no el modelo: CompactionSummary (C-037) solo es válido si su firstKeptMessageId coincide con
      el corte seguro que el arnés calculó. Así ningún resumen puede desplazar el corte ni dejar una
      tool call separada de su resultado.
  recall_questions:
    - id: RQ-CH29-01
      text: |
        ¿Qué hace trimOversizedToolResults (fase 1) y en qué caso planHistoryCompaction marca
        needsSummary = FALSE sin necesitar ningún CompactionSummary del modelo?
    - id: RQ-CH29-02
      text: |
        ¿Qué hace findSafeCutIndex si el índice de corte cae sobre un mensaje con rol TOOL, y qué
        invariante (INV-07) protege con eso?
    - id: RQ-CH29-03
      text: |
        ¿Qué error lanza applyHistoryCompaction si el firstKeptMessageId del CompactionSummary
        propuesto no coincide con el primer mensaje de la región reciente, y por qué el modelo no
        puede mover el corte?
    - id: RQ-CH29-04
      text: |
        ¿En qué se diferencia navigateToCheckpoint (CH-29) de branchSessionFromCheckpoint (CH-10), y
        qué guarda el BranchSummary que navigateToCheckpoint agrega a la sesión?
  explain_prompts:
    - id: EP-CH29-01
      text: |
        ContextEngine posee la compactación (Article III), pero no invoca al modelo. Explica, como si
        hablaras con alguien sin contexto técnico, por qué el resumen lo propone el modelo y lo valida
        ContextEngine — ¿qué se rompería si ContextEngine llamara directamente al modelo, o si el
        modelo decidiera dónde cortar?
      target_entity: CMP-004
    - id: EP-CH29-02
      text: |
        SessionManager posee branching y reconstruction. Explica por qué navegar hacia atrás no borra
        la rama abandonada, y por qué SessionManager NO posee decidir qué parte de esa rama ve el
        modelo en el próximo turno (P-08).
      target_entity: CMP-010
  interleaved_questions:
    - id: IQ-CH29-01
      text: |
        reconstructSessionState (CH-10) reconstruía una sesión desde latestCheckpoint. Con
        SessionState v2, ¿qué campo nuevo debe consultar primero para saber desde dónde continúa el
        próximo turno, y por qué latestCheckpoint sigue siendo necesario después de navegar?
      current_chapter_entities: [C-038, C-037]
      prior_chapter_entities: [C-020, CMP-010]
      prior_chapter: CH-10
  flashcards:
    - id: FC-CH29-01
      front: |
        ¿Qué es un CompactionSummary (C-037) y qué campo valida el arnés antes de aceptarlo?
      back: |
        La forma estructurada del resumen de la región antigua: goal, constraints, progress,
        decisions, nextSteps, criticalContext, touchedFiles, firstKeptMessageId y provenance. El
        arnés exige que firstKeptMessageId coincida con el corte seguro que calculó; si no, lanza
        COMPACTION_SUMMARY_CUT_MISMATCH.
      source_entity: C-037
      chapter_introduced_in: CH-29
      review_stage: DAY_1
    - id: FC-CH29-02
      front: |
        ¿Qué es un BranchSummary (C-038) y cuándo se crea?
      back: |
        El resumen de la rama que se abandona al navegar dentro de una sesión hacia un checkpoint
        anterior: abandonedTipId (sigue direccionable), resumedFromId, summary (CompactionSummary) y
        createdAt. Lo crea navigateToCheckpoint; navegar no borra nada.
      source_entity: C-038
      chapter_introduced_in: CH-29
      review_stage: DAY_1
    - id: FC-CH29-03
      front: |
        ¿Qué agrega SessionState v2 (C-020) respecto a v1?
      back: |
        activeCheckpointId (desde dónde continúa el próximo turno; NULL = latestCheckpoint) y
        branchSummaries (los resúmenes de ramas abandonadas). Es la primera modificación real de un
        contrato en el libro (ADR-003, parte v2).
      source_entity: C-020
      chapter_introduced_in: CH-29
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH29-01
      recall_question: RQ-CH29-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH29-02
      recall_question: RQ-CH29-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH29-03
      recall_question: RQ-CH29-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH29-04
      recall_question: RQ-CH29-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 29 — Compactar sin Perder el Hilo: Resúmenes Estructurados y Sesiones en Árbol

> **Regla constitucional (P-14):** el contexto se selecciona, no se vuelca.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir cuándo un historial necesita
compactarse, dónde cortarlo sin separar nunca una tool call de su resultado, y qué parte del trabajo
le toca al modelo (proponer el resumen) y cuál al arnés (validar su forma y el punto de corte).
También podrás distinguir navegar hacia atrás dentro de una sesión, que no borra nada, de ramificar
en una sesión nueva.

**Esqueleto.** Segundo capítulo del Tramo 4. Recorre 19 secciones, introduce dos contratos y lleva
un contrato existente a su versión 2: es la **primera modificación real de un contrato** en el
libro.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Cuando una conversación ya no cabe en lo que el modelo puede leer, ¿conviene primero pedirle al
   modelo que la resuma, o hay un paso más barato que muchas veces alcanza sin llamarlo?
2. Si hay que cortar la conversación en "lo viejo que se resume" y "lo reciente que se conserva tal
   cual", ¿qué dos mensajes nunca deberían quedar a lados distintos del corte, y por qué?
3. Si el modelo escribe el resumen de lo viejo, ¿quién decide desde qué mensaje empieza lo que se
   conserva literal? ¿Y qué pasa si el resumen dice otra cosa?
4. Si el usuario quiere volver a un punto anterior de la conversación para probar otra alternativa,
   ¿hay que borrar lo que se hizo después, o crear una conversación nueva, o hay una tercera opción?

## 1. Arquitectura Actual (Current Architecture)

**`ContextEngine` (CMP-004, CH-04)** arma el `ContextSnapshot` (C-005) de cada turno con
`assembleContextSnapshot`:
- recorre los candidatos en orden;
- si uno no cabe en `budget.maxInputTokens`, lo compacta con la primitiva `compact(...)`;
- si ni compactado cabe, lo deja fuera, de forma explícita.

CH-04 decidió deliberadamente que **no existe un componente `Compactor` o `Summarizer`**: la compactación es de `ContextEngine` (Article III: "selection, ranking, composition, compaction, context budgets, provenance").

**`SessionManager` (CMP-010, CH-10)** persiste la sesión (`SessionState`, C-020) con su `latestCheckpoint`, la reconstruye (`reconstructSessionState`, INV-13) y ramifica (`branchSessionFromCheckpoint`). Ramificar crea una **sesión nueva** que desciende de un checkpoint, vía `parentCheckpointId`.

CH-28 dejó una deuda: el steering y el follow-up hacen crecer el historial de un run.

## 2. El Problema (Problem)

Las conversaciones largas dejan de caber en lo que el modelo puede leer. Cuando eso pasa, las
implementaciones reaccionan de maneras que rompen cosas:
- truncan por el principio y pierden las decisiones ya tomadas;
- cortan en medio de una llamada a una herramienta y dejan su resultado huérfano;
- resumen sin estructura, y lo importante se diluye en un párrafo.

Y cuando el usuario quiere **volver a un punto anterior** para probar otra alternativa, borran lo que
vino después, o lo obligan a empezar una conversación nueva desde cero.

Necesitamos compactar el **historial completo** de un run con reglas declaradas, y poder navegar
hacia atrás dentro de una sesión sin perder nada.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- `assembleContextSnapshot` compacta **candidato por candidato**. No tiene noción de "región
  antigua" y "región reciente", ni de dónde cortar el historial.
- Nada impide que un corte deje un mensaje `TOOL` (el resultado) de un lado y la tool call que lo
  originó del otro. Eso viola INV-07: el resultado debe volver al ciclo como observación explícita,
  y un resultado sin su llamada ya no se entiende.
- `compact(...)` es una caja negra: no dice qué debe sobrevivir a la compactación. Las decisiones
  y las restricciones pueden perderse.
- Si el resumen lo escribe el modelo, nada impide que el mismo modelo decida también **dónde
  cortar**. Eso mezcla lo agéntico (redactar un resumen) con lo determinístico (qué parte del
  historial se conserva literal), y Article XII los separa.
- `SessionState` (C-020 v1) solo conoce `latestCheckpoint`. Volver a un checkpoint anterior dentro
  de la misma sesión no tiene representación, y la única opción es ramificar en una sesión nueva
  (CH-10).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-01   Context is a first-class architectural component.
           La compactación del historial es una decisión de ContextEngine, con contratos
           propios, no un efecto lateral del lugar donde se agota el presupuesto.
    P-02   The model is replaceable.
           ContextEngine no invoca al modelo: recibe una propuesta de resumen que la
           integración obtiene de ModelGateway. Cambiar de modelo no cambia estas reglas.
    P-08   Agent state and session state are different concerns.
           SessionState v2 conserva todo lo que pasó (latestCheckpoint + ramas abandonadas);
           el contexto elige qué ve el modelo. Navegar cambia desde dónde sigue la sesión,
           no el AgentState de ningún run.
    P-14   Context should be selected, not dumped.
           Fase 1 recorta sin modelo; fase 2 resume solo la región antigua; la región
           reciente se conserva literal.

Invariants preserved
    INV-07   El ToolResult vuelve al loop como observación explícita.
             findSafeCutIndex nunca deja un mensaje TOOL separado de su tool call.
    INV-12   AgentState y SessionState permanecen independientes.
             navigateToCheckpoint modifica solo SessionState.
    INV-13   Una ejecución durable puede reconstruirse desde estado persistido.
             resolveResumeCheckpoint usa activeCheckpointId o, si falta, latestCheckpoint.
    INV-18   Toda acción significativa produce un evento observable.
             CONTEXT_HISTORY_COMPACTED, CONTEXT_COMPACTION_FAILED, SESSION_BRANCH_NAVIGATED.
    INV-19   Toda decisión crítica es trazable.
             Cada CompactionSummary lleva provenance y el id del primer mensaje conservado.

Component ownership changes
    Ninguno en registry/components.yaml. ContextEngine (CMP-004) ya posee "compaction,
    context budgets, provenance"; SessionManager (CMP-010) ya posee "branching, checkpoints,
    reconstruction" (Article III).

Contract changes
    C-020 SessionState pasa a v2 (ADR-003, parte v2, Accepted): agrega activeCheckpointId y
    branchSummaries. Compatible hacia atrás: CH-10..CH-28 siguen válidos sin tocarlos.

Security implications
    Un resumen propuesto por el modelo no puede mover el punto de corte ni omitir campos
    obligatorios: si lo intenta, applyHistoryCompaction lo rechaza (ver sección 15).

Observability implications
    Tres valores nuevos de AgentEventType (ver sección 14).

Deterministic vs agentic boundary
    Agéntico: el texto de cada campo del resumen. Determinístico: cuándo compactar, dónde
    cortar, qué se recorta sin modelo y si el resumen propuesto es válido (Article XII).
```

## 5. Conceptos Nuevos (New Concepts)

- **Compactación del historial** (*history compaction*): compactar el historial completo de un run en dos fases.
  1. **Recorte sin modelo:** los resultados de tools demasiado grandes se truncan con una marca.
  2. **Resumen:** solo si el recorte no alcanza, la región antigua se reemplaza por un resumen estructurado.
- **Región antigua y región reciente**: el historial se divide en un punto de corte. Lo anterior puede recortarse o resumirse; lo posterior se conserva **literal**.
- **Punto de corte seguro** (*safe cut point*): el índice donde empieza la región reciente. Nunca cae en un mensaje `TOOL`, porque separaría un resultado de su llamada.
- **Resumen estructurado**: un resumen con campos fijos (objetivo, restricciones, progreso, decisiones, próximos pasos, contexto crítico, archivos tocados). Así lo decidido sobrevive a la compactación. El texto lo propone el modelo; la forma la fija el contrato.
- **Navegación dentro de una sesión**: volver a un checkpoint anterior de la **misma** sesión para continuar desde ahí. No borra la rama que se deja; la resume.
- **Rama abandonada**: el tramo de la sesión entre el checkpoint al que se vuelve y la punta que se deja. Sigue siendo direccionable, porque la sesión no borra nada.

Navegar **dentro** de una sesión es distinto de **ramificar** en una sesión nueva:
- `branchSessionFromCheckpoint` (CH-10) sigue existiendo y crea un linaje independiente;
- `navigateToCheckpoint` (este capítulo) cambia desde dónde continúa la **misma** sesión.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato** (`registry/contracts.yaml`): `AgentMessage` (C-001), `ExecutionBudget` (C-012), `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError` (C-011), `SessionState` (C-020, que este capítulo lleva a v2);
- **identificadores primitivos:** `AgentId`, `SessionId`, `RunId`, `Timestamp`.

Se usan también, sin contrato propio:

| Identificador | Rol en este capítulo |
|---|---|
| `MessageId` | identificador de un `AgentMessage` (heredado de CH-00) |
| `MessageRole` | rol de un mensaje; este capítulo depende de `TOOL` y `SYSTEM` (heredado de CH-00) |
| `SessionCheckpoint` | checkpoint embebido de CH-10 (`id`, `runId`, `agentState`, `createdAt`) |
| `SessionCheckpointId` | identificador de un `SessionCheckpoint` (heredado de CH-10) |
| `AgentEventType` | se agregan `CONTEXT_HISTORY_COMPACTED`, `CONTEXT_COMPACTION_FAILED` y `SESSION_BRANCH_NAVIGATED` |
| `ErrorCategory` | reutiliza `CONTEXT`, `VALIDATION` y `PERSISTENCE`, sin valores nuevos |

### `CompactionPolicy` — los umbrales de compactación (embebida)

```pseudocode
STRUCT CompactionPolicy
    reserveTokens: Integer
    keepRecentTokens: Integer
    maxToolResultChars: Integer
END
```

- `reserveTokens`: margen que se deja libre por debajo de `budget.maxInputTokens` para la respuesta del modelo. La compactación se dispara cuando el historial lo invade.
- `keepRecentTokens`: cuánto historial reciente se conserva literal.
- `maxToolResultChars`: el tamaño a partir del cual la fase 1 recorta un resultado de tool.

Son parámetros del arnés, no del modelo.

### `CompactionSummary` — el contrato del resumen estructurado (C-037)

```pseudocode
STRUCT CompactionSummary
    goal: Text
    constraints: List<Text>
    progress: List<Text>
    decisions: List<Text>
    nextSteps: List<Text>
    criticalContext: List<Text>
    touchedFiles: List<Text>
    firstKeptMessageId: MessageId
    provenance: Text
END
```

`firstKeptMessageId` ata el resumen al corte: indica desde qué mensaje el historial se conserva
literal. `provenance` cumple EVO-09 ("context has provenance") y registra de dónde vino este bloque
(p.ej. `"history_compaction"`).

### `CompactionPlan` — la decisión de ContextEngine antes de pedir el resumen (embebida)

```pseudocode
STRUCT CompactionPlan
    cutIndex: Integer
    olderRegion: List<AgentMessage>
    recentRegion: List<AgentMessage>
    needsSummary: Boolean
END
```

### `BranchSummary` — el resumen de una rama abandonada (C-038)

```pseudocode
STRUCT BranchSummary
    abandonedTipId: SessionCheckpointId
    resumedFromId: SessionCheckpointId
    summary: CompactionSummary
    createdAt: Timestamp
END
```

### `SessionState` — versión 2 (C-020, ADR-003 parte v2)

```pseudocode
STRUCT SessionState
    sessionId: SessionId
    runIds: List<RunId>
    latestCheckpoint: SessionCheckpoint
    parentCheckpointId: Optional<SessionCheckpointId>
    activeCheckpointId: Optional<SessionCheckpointId>
    branchSummaries: List<BranchSummary>
    createdAt: Timestamp
    updatedAt: Timestamp
END
```

Los dos campos nuevos son compatibles hacia atrás:
- `activeCheckpointId = NULL` significa "continuar desde `latestCheckpoint`", igual que en v1;
- `branchSummaries` vacío significa que nunca se navegó.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-037
Name:                   CompactionSummary
Version:                v1
Introduced In:          CH-29
Current Definition:     STRUCT CompactionSummary (ver seccion 6)
Used By:                [CMP-004, CMP-010]
Modified By:            []
Constitutional Impact:  [P-01, P-14, INV-07]
```

```text
ID:                     C-038
Name:                   BranchSummary
Version:                v1
Introduced In:          CH-29
Current Definition:     STRUCT BranchSummary (ver seccion 6)
Used By:                [CMP-010, CMP-004]
Modified By:            []
Constitutional Impact:  [P-08, INV-12, INV-13]
```

```text
ID:                     C-020
Name:                   SessionState
Version:                v2   (antes v1, CH-10)
Introduced In:          CH-10
Current Definition:     STRUCT SessionState v2 (ver seccion 6)
Used By:                [CMP-010]
Modified By:            [CH-29]
Constitutional Impact:  [P-08, P-23, INV-12, INV-13]
ADR:                    ADR-003 (parte v2, Accepted 2026-09-25)
```

`CompactionPolicy` y `CompactionPlan` quedan embebidos: solo cruzan la frontera de `ContextEngine`
dentro de sus propias funciones.

## 8. Responsabilidades de Componentes (Component Responsibilities)

Este capítulo **no introduce componentes**. Amplía dos componentes existentes dentro de su `owns` literal (Article III), así que no hace falta tocar sus fichas en `registry/components.yaml`.

```text
COMPONENT: ContextEngine (CMP-004, CH-04 — ficha sin cambios)

Owns (Article III) — lo que este capítulo usa: compaction, context budgets, provenance.
Decisiones nuevas, dentro de ese owns:
    - cuándo el historial necesita compactarse (shouldCompactHistory)
    - dónde cortar sin separar una tool call de su resultado (findSafeCutIndex)
    - qué recortar sin modelo (trimOversizedToolResults)
    - si un resumen propuesto es válido y coincide con el corte (applyHistoryCompaction)
Does NOT own (se preserva):
    - invocar al modelo para obtener el resumen (ModelGateway, CH-03 — lo hace la integración)
    - redactar el resumen (el modelo lo propone — Article XII)
    - persistir la sesión (SessionManager, CH-10)
```

```text
COMPONENT: SessionManager (CMP-010, CH-10 — ficha sin cambios)

Owns (Article III) — lo que este capítulo usa: branching, checkpoints, reconstruction.
Decisiones nuevas, dentro de ese owns:
    - desde qué checkpoint continúa el próximo turno (resolveResumeCheckpoint)
    - navegar dentro de la sesión sin borrar la rama abandonada (navigateToCheckpoint)
Does NOT own (se preserva):
    - qué parte de la rama abandonada ve el modelo (ContextEngine)
    - el AgentState de un run (AgentLoop, CH-01 — P-08/INV-12)
```

Por qué no hay un componente nuevo (EVO-01): un `Summarizer` separado duplicaría la decisión de
compactación que CH-04 ya le asignó a `ContextEngine`, y un `BranchNavigator` duplicaría el
branching que Article III ya le asigna a `SessionManager`.

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
ContextEngine (ampliado en CH-29)
    consumes → AgentMessage, ExecutionBudget, CompactionSummary (propuesto)
    produces → CompactionPlan (embebido), AgentMessage (historial compactado),
               AgentEvent, HarnessError

SessionManager (ampliado en CH-29)
    consumes → SessionState v2, SessionCheckpoint, CompactionSummary (de la rama abandonada)
    produces → SessionState v2, BranchSummary, AgentEvent, HarnessError
```

La integración (Preview, CH-36) encadena:
1. `planHistoryCompaction`;
2. si `needsSummary`, una llamada a `invokeModelForTurn` (ModelGateway, CH-03) para obtener la propuesta de `CompactionSummary` con el `firstKeptMessageId` del plan;
3. `applyHistoryCompaction`;
4. el resultado pasa como `candidates` a `assembleContextSnapshot` (CH-04), que no cambia.

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Integración → ContextEngine (plan) → [ModelGateway: propuesta de resumen] → ContextEngine (aplicar)
Integración → SessionManager (navegar) → [ContextEngine/ModelGateway: resumen de la rama]
```

**Vista 2 — Sequence: compactar un historial que no cabe**

```text
Integración
   │ planHistoryCompaction(history, estimatedTokens, budget, policy)
   ▼
ContextEngine
   │ shouldCompactHistory → TRUE (el historial invade reserveTokens)
   │ findSafeCutIndex → cut (nunca sobre un mensaje TOOL)
   │ trimOversizedToolResults(región antigua)  — fase 1, sin modelo
   │ ¿cabe ya? → NO → needsSummary = TRUE
   ▼
Integración
   │ invokeModelForTurn (ModelGateway, CH-03): "resume la región antigua"
   │ → propuesta CompactionSummary (firstKeptMessageId = id del primer mensaje reciente)
   ▼
ContextEngine
   │ applyHistoryCompaction(plan, propuesta)
   │ valida: goal no vacío; firstKeptMessageId == primer mensaje de la región reciente
   │ → [mensaje SYSTEM con el resumen] + región reciente literal
   │ emite CONTEXT_HISTORY_COMPACTED
   ▼
assembleContextSnapshot (CH-04, sin cambios) recibe el historial compactado como candidatos
```

**Vista 2b — Sequence: volver a un punto anterior**

```text
Usuario: "volvamos al checkpoint de antes de migrar la base"
   ▼
Integración → (resumen de la rama que se deja: ContextEngine + ModelGateway)
   ▼
SessionManager
   │ navigateToCheckpoint(session, target, resumenDeLaRama)
   │ valida: target pertenece a esta sesión
   │ activeCheckpointId = target.id ; branchSummaries += BranchSummary
   │ latestCheckpoint NO cambia — la rama abandonada sigue direccionable
   │ emite SESSION_BRANCH_NAVIGATED
   ▼
próximo turno: resolveResumeCheckpoint(session) → target.id
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

Usa exclusivamente entidades definidas en la sección 6 o registradas en capítulos anteriores.

```pseudocode
FUNCTION shouldCompactHistory(
    estimatedTokens: Integer,
    budget: ExecutionBudget,
    policy: CompactionPolicy
) -> Boolean

    RETURN estimatedTokens > budget.maxInputTokens - policy.reserveTokens
END
```

```pseudocode
FUNCTION findSafeCutIndex(
    history: List<AgentMessage>,
    policy: CompactionPolicy
) -> Integer

    cut: Integer = length(history)
    keptTokens: Integer = 0
    stillFits: Boolean = TRUE

    WHILE cut > 0 AND stillFits
        messageTokens: Integer = estimateTokens(history[cut - 1].content)
        IF keptTokens + messageTokens > policy.keepRecentTokens
            stillFits = FALSE
        ELSE
            keptTokens = keptTokens + messageTokens
            cut = cut - 1
        END
    END

    IF cut == length(history) AND length(history) > 0
        cut = length(history) - 1
    END

    WHILE cut > 0 AND history[cut].role == TOOL
        cut = cut - 1
    END

    RETURN cut
END
```

El primer `WHILE` retrocede mientras la región reciente cabe en `keepRecentTokens`. El ajuste
siguiente garantiza que al menos el último mensaje se conserve literal. El segundo `WHILE` es la
regla de seguridad: si la región reciente empezaría con un resultado de tool (`TOOL`), el corte
retrocede hasta incluir la tool call que lo originó (INV-07).

```pseudocode
FUNCTION trimOversizedToolResults(
    messages: List<AgentMessage>,
    policy: CompactionPolicy
) -> List<AgentMessage>

    trimmed: List<AgentMessage> = []

    FOR EACH message IN messages
        IF message.role == TOOL AND length(message.content) > policy.maxToolResultChars
            trimmed = append(trimmed, AgentMessage(
                id = message.id,
                role = TOOL,
                content = truncateWithMarker(message.content, policy.maxToolResultChars),
                timestamp = message.timestamp
            ))
        ELSE
            trimmed = append(trimmed, message)
        END
    END

    RETURN trimmed
END
```

```pseudocode
FUNCTION planHistoryCompaction(
    history: List<AgentMessage>,
    estimatedTokens: Integer,
    budget: ExecutionBudget,
    policy: CompactionPolicy
) -> CompactionPlan

    IF NOT shouldCompactHistory(estimatedTokens, budget, policy)
        RETURN CompactionPlan(
            cutIndex = 0,
            olderRegion = [],
            recentRegion = history,
            needsSummary = FALSE
        )
    END

    cut: Integer = findSafeCutIndex(history, policy)
    olderRegion: List<AgentMessage> = trimOversizedToolResults(slice(history, 0, cut), policy)
    recentRegion: List<AgentMessage> = slice(history, cut, length(history))

    fitsWithoutSummary: Boolean =
        estimateHistoryTokens(olderRegion) + estimateHistoryTokens(recentRegion)
            <= budget.maxInputTokens - policy.reserveTokens

    RETURN CompactionPlan(
        cutIndex = cut,
        olderRegion = olderRegion,
        recentRegion = recentRegion,
        needsSummary = NOT fitsWithoutSummary
    )
END
```

```pseudocode
FUNCTION applyHistoryCompaction(
    plan: CompactionPlan,
    proposal: Optional<CompactionSummary>,
    execution: ExecutionContext,
    agentId: AgentId
) -> List<AgentMessage>

    IF NOT plan.needsSummary
        RETURN concat(plan.olderRegion, plan.recentRegion)
    END

    IF proposal == NULL OR proposal.goal == ""
        failure: HarnessError = HarnessError(
            category = CONTEXT,
            code = "COMPACTION_SUMMARY_MISSING",
            message = "El plan exige un resumen de la región antigua y no llegó una propuesta válida",
            recoverable = TRUE,
            retryable = TRUE,
            metadata = {}
        )
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = CONTEXT_COMPACTION_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )
        THROW failure
    END

    IF proposal.firstKeptMessageId != first(plan.recentRegion).id
        failure: HarnessError = HarnessError(
            category = CONTEXT,
            code = "COMPACTION_SUMMARY_CUT_MISMATCH",
            message = "El resumen propuesto no coincide con el corte seguro calculado por el arnés",
            recoverable = TRUE,
            retryable = TRUE,
            metadata = {}
        )
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = CONTEXT_COMPACTION_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )
        THROW failure
    END

    summaryMessage: AgentMessage = AgentMessage(
        id = newMessageId(),
        role = SYSTEM,
        content = proposal,
        timestamp = now()
    )

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = CONTEXT_HISTORY_COMPACTED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = proposal
    )

    RETURN concat([summaryMessage], plan.recentRegion)
END
```

```pseudocode
FUNCTION resolveResumeCheckpoint(
    session: SessionState
) -> SessionCheckpointId

    IF session.activeCheckpointId != NULL
        RETURN session.activeCheckpointId
    END

    RETURN session.latestCheckpoint.id
END
```

```pseudocode
FUNCTION navigateToCheckpoint(
    session: SessionState,
    target: SessionCheckpoint,
    abandonedSummary: CompactionSummary,
    execution: ExecutionContext,
    agentId: AgentId
) -> SessionState

    IF target == NULL
        THROW HarnessError(
            category = VALIDATION,
            code = "NAVIGATION_TARGET_REQUIRED",
            message = "navigateToCheckpoint fue invocada sin un checkpoint destino",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    IF target.agentState.sessionId != session.sessionId
        THROW HarnessError(
            category = VALIDATION,
            code = "CHECKPOINT_NOT_IN_SESSION",
            message = "El checkpoint destino pertenece a otra sesión; para eso existe branchSessionFromCheckpoint",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    currentTipId: SessionCheckpointId = resolveResumeCheckpoint(session)

    IF currentTipId == target.id
        RETURN session
    END

    branch: BranchSummary = BranchSummary(
        abandonedTipId = currentTipId,
        resumedFromId = target.id,
        summary = abandonedSummary,
        createdAt = now()
    )

    navigated: SessionState = SessionState(
        sessionId = session.sessionId,
        runIds = session.runIds,
        latestCheckpoint = session.latestCheckpoint,
        parentCheckpointId = session.parentCheckpointId,
        activeCheckpointId = target.id,
        branchSummaries = append(session.branchSummaries, branch),
        createdAt = session.createdAt,
        updatedAt = now()
    )

    persisted: Boolean = persistSessionState(navigated)

    IF NOT persisted
        failure: HarnessError = HarnessError(
            category = PERSISTENCE,
            code = "SESSION_PERSISTENCE_FAILED",
            message = "SessionManager no pudo persistir la sesión después de navegar",
            recoverable = TRUE,
            retryable = TRUE,
            metadata = {}
        )
        EMIT AgentEvent(
            eventId = newEventId(),
            eventType = SESSION_PERSISTENCE_FAILED,
            timestamp = now(),
            runId = execution.runId,
            sessionId = execution.sessionId,
            agentId = agentId,
            traceId = execution.traceId,
            payload = failure
        )
        THROW failure
    END

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = SESSION_BRANCH_NAVIGATED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = execution.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = branch
    )

    RETURN navigated
END
```

`length`, `slice`, `concat`, `append`, `first`, `estimateTokens`, `estimateHistoryTokens`,
`truncateWithMarker`, `newMessageId`, `newEventId`, `now` y `persistSessionState` son utilidades
primitivas. Las dos últimas ya venían de CH-04 y CH-10. Ninguna es una entidad arquitectónica.

Nótese lo que estas funciones **no** hacen:
- `applyHistoryCompaction` no redacta el resumen; lo valida.
- Ninguna función de `ContextEngine` invoca al modelo (P-02).
- `navigateToCheckpoint` no borra ni la rama abandonada ni `latestCheckpoint`.
- Nada toca el `AgentState` de un run (INV-12).

## 12. Transiciones de Estado (State Transitions)

Este capítulo no cambia `AgentRunStatus`. Introduce la evolución de una sesión navegable:

```text
SessionState v2
   activeCheckpointId = NULL           → el próximo turno continúa desde latestCheckpoint
   navigateToCheckpoint(target)        → activeCheckpointId = target.id
                                          branchSummaries += BranchSummary(abandonedTip → target)
                                          latestCheckpoint sin cambios
   navigateToCheckpoint(mismo punto)   → sin cambios, sin resumen
```

Y la del historial dentro de un turno:

```text
historial
   → no invade reserveTokens            → sin compactar
   → invade, y basta la fase 1           → región antigua recortada + región reciente literal
   → invade, y hace falta la fase 2      → [resumen SYSTEM] + región reciente literal
                                            (o COMPACTION_SUMMARY_MISSING / _CUT_MISMATCH)
```

## 13. Semántica de Fallos (Failure Semantics)

Cada fallo nuevo es un `HarnessError` con su `ErrorCategory`:

```text
CONTEXT
    applyHistoryCompaction sin propuesta válida cuando needsSummary = TRUE
    → recoverable: TRUE, retryable: TRUE (se puede pedir otra propuesta)
    → código: COMPACTION_SUMMARY_MISSING

CONTEXT
    la propuesta no coincide con el corte (firstKeptMessageId distinto)
    → recoverable: TRUE, retryable: TRUE
    → código: COMPACTION_SUMMARY_CUT_MISMATCH

VALIDATION
    navigateToCheckpoint sin checkpoint destino
    → recoverable: FALSE, retryable: FALSE → código: NAVIGATION_TARGET_REQUIRED

VALIDATION
    el checkpoint destino es de otra sesión
    → recoverable: FALSE, retryable: FALSE → código: CHECKPOINT_NOT_IN_SESSION

PERSISTENCE
    no se pudo persistir la sesión navegada
    → recoverable: TRUE, retryable: TRUE → código: SESSION_PERSISTENCE_FAILED (el de CH-10)
```

Si la fase 2 falla dos veces, la integración todavía puede caer en el comportamiento de CH-04
(candidato por candidato, con exclusiones explícitas). La compactación del historial es una mejora
sobre esa base, no un reemplazo.

## 14. Eventos Producidos (Events Produced)

Tres valores nuevos de `AgentEventType`:

```text
CONTEXT_HISTORY_COMPACTED   — ContextEngine aplicó un resumen válido (payload: CompactionSummary)
CONTEXT_COMPACTION_FAILED   — la propuesta faltó o no coincidía con el corte (payload: HarnessError)
SESSION_BRANCH_NAVIGATED    — SessionManager navegó dentro de la sesión (payload: BranchSummary)
```

`SESSION_PERSISTENCE_FAILED` se reutiliza de CH-10 sin cambios.

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **El modelo no decide qué se conserva literal.** Un resumen que intente mover el corte, por
  ejemplo para "olvidar" una instrucción reciente del usuario o una denegación de política, se
  rechaza con `COMPACTION_SUMMARY_CUT_MISMATCH`. La región reciente siempre llega literal.
- **Los resultados de tools recortados llevan una marca.** El modelo sabe que están truncados y no
  los toma por completos.
- **Una rama abandonada no se borra.** Si algo se hizo en esa rama (un side effect), su evidencia
  sigue en la sesión y, cuando corresponde, en el `AuditLedger` (CH-19). Navegar no es deshacer:
  un efecto ya ocurrido en el mundo real no se revierte por volver a un checkpoint.
- **Clasificación de datos en el resumen:** si la región antigua contenía datos sensibles, su
  resumen también puede contenerlos. Aplicar la etiqueta de gobierno del dato (CH-20) al resumen
  queda para la integración (CH-36) y para las fuentes gobernadas (CH-40).

## 16. Tests (Tests)

```text
TEST ShouldCompactHistoryOnlyWhenHistoryInvadesReserveTokens
TEST SafeCutIndexNeverStartsTheRecentRegionWithAToolMessage
TEST SafeCutIndexAlwaysKeepsAtLeastTheLastMessageLiteral
TEST PhaseOneTrimsOnlyToolResultsLargerThanMaxToolResultChars
TEST PlanDoesNotRequireSummaryWhenPhaseOneIsEnough
TEST ApplyRejectsMissingSummaryWhenPlanRequiresIt
TEST ApplyRejectsSummaryWhoseFirstKeptMessageIdDiffersFromTheCut
TEST ApplyKeepsTheRecentRegionLiteral
TEST ContextEngineNeverInvokesTheModelDirectly
TEST NavigateToCheckpointNeverChangesLatestCheckpoint
TEST NavigateToCheckpointRejectsCheckpointsFromAnotherSession
TEST NavigateToTheCurrentTipIsANoOpWithoutSummary
TEST ResolveResumeCheckpointFallsBackToLatestCheckpoint
TEST SessionStateV2IsBackwardCompatibleWithChaptersTenToTwentyEight
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (BH-v0.2 en curso, después de CH-29)

Contracts (registry/contracts.yaml) — 38
 ├── C-001 .. C-036                (sin cambios, salvo C-020)
 ├── C-020 SessionState v2         (CH-10 → modificado en CH-29, ADR-003 parte v2)
 ├── C-037 CompactionSummary       (CH-29, nuevo)
 └── C-038 BranchSummary           (CH-29, nuevo)

Components (registry/components.yaml) — 22, sin cambios
 ├── CMP-004 ContextEngine    (decisiones nuevas dentro de "compaction, context budgets, provenance")
 └── CMP-010 SessionManager   (decisiones nuevas dentro de "branching, checkpoints, reconstruction")
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Cablearlo en la integración.** Ninguna función de integración invoca todavía `planHistoryCompaction` ni `navigateToCheckpoint`. El primer cableado será CH-36.
- **Provenance del bloque del resumen.** `assembleContextSnapshot` (CH-04) sigue etiquetando todo candidato como `"conversation_history"`. El `CompactionSummary` ya lleva su propia `provenance`, pero el `ContextBlock` resultante no la distingue todavía. Generalizar la procedencia por fuente es parte de las fuentes de datos gobernadas (CH-40).
- **Etiqueta de gobierno del dato para el resumen** (CH-20 / CH-40).
- **Recuperar un turno interrumpido a mitad de la compactación** (CH-32, pasos durables).
- **La versión del runtime en la sesión** (`runtimeVersion`, ADR-003 parte v3, CH-43).

## 19. Siguiente Incremento (Next Increment)

Hasta aquí, todo lo que el arnés hace dentro de un turno se puede reconstruir y compactar, pero hay
algo que no se puede "volver a pedir" sin riesgo: **un efecto en el mundo real cuyo resultado no se
sabe**. Si el proceso muere justo después de llamar a una API de pagos y antes de registrar la
respuesta, ¿se vuelve a llamar?

El siguiente capítulo introduce la **política de replay** que cada capability declara (`NEVER` o `SAFE`) y el resultado "desconocido" como observación explícita. Será CH-30 ("Cuando No se Sabe si Ocurrió: Política de Replay"). `next_chapter` queda en `null` porque CH-30 todavía no existe como archivo.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): las conversaciones largas dejan de caber. Las implementaciones
   truncan, pierden decisiones, dejan resultados huérfanos o borran lo que el usuario hizo al volver
   atrás.
2. **Patrones que se repiten** (= §3): la compactación se decide donde se agota el presupuesto, y
   ese lugar no conoce la estructura del turno ni qué es crítico.
3. **Estructuras / reglas / incentivos** (= §8): `CompactionSummary` (C-037), `BranchSummary`
   (C-038) y `SessionState` v2, dentro del `owns` de `ContextEngine` y de `SessionManager`. El
   modelo propone; el arnés valida.
4. **Modelos mentales** (= §4): P-14, P-01 y P-08. La sesión conserva todo; el contexto elige qué
   ve el modelo.

**Bucles de retroalimentación**

- **Bucle de refuerzo:** truncar sin estructura hace olvidar decisiones, el modelo las rediscute y
  genera más historial. Un resumen con campos fijos corta esa espiral.
- **Bucle de equilibrio:** la fase 1, sin modelo, resuelve la mayoría de los desbordes sin gastar
  una llamada.

**Punto de apalancamiento**

La decisión con mayor efecto es que el punto de corte lo fije `ContextEngine` y no el modelo:
`CompactionSummary` (C-037) solo es válido si su `firstKeptMessageId` coincide con el corte seguro
que el arnés calculó.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué hace `trimOversizedToolResults` (fase 1) y en qué caso `planHistoryCompaction` marca
   `needsSummary = FALSE` sin necesitar ningún `CompactionSummary` del modelo? *(pregunta guía 1)*
2. ¿Qué hace `findSafeCutIndex` si el índice de corte cae sobre un mensaje con rol `TOOL`, y qué
   invariante (INV-07) protege con eso? *(pregunta guía 2)*
3. ¿Qué error lanza `applyHistoryCompaction` si el `firstKeptMessageId` del `CompactionSummary`
   propuesto no coincide con el primer mensaje de la región reciente, y por qué el modelo no puede
   mover el corte? *(pregunta guía 3)*
4. ¿En qué se diferencia `navigateToCheckpoint` (CH-29) de `branchSessionFromCheckpoint` (CH-10), y
   qué guarda el `BranchSummary` que `navigateToCheckpoint` agrega a la sesión? *(pregunta guía 4)*

### Explicar

1. `ContextEngine` posee la compactación, pero no invoca al modelo. Explica por qué el resumen lo
   propone el modelo y lo valida `ContextEngine`. ¿Qué se rompería si `ContextEngine` llamara
   directamente al modelo, o si el modelo decidiera dónde cortar?
2. `SessionManager` posee branching y reconstruction. Explica por qué navegar hacia atrás no borra la
   rama abandonada, y por qué `SessionManager` NO posee decidir qué parte de esa rama ve el modelo en
   el próximo turno (P-08).

### Conectar

1. `reconstructSessionState` (CH-10) reconstruía una sesión desde `latestCheckpoint`. Con
   `SessionState` v2, ¿qué campo nuevo debe consultar primero para saber desde dónde continúa el
   próximo turno, y por qué `latestCheckpoint` sigue siendo necesario después de navegar?

### Espaciar

Las tres tarjetas de repaso de este capítulo entran hoy en `reviewStage = DAY_1`: dos sobre los contratos nuevos y una sobre `SessionState` v2. Repásalas al día 3, al día 7 y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
