---
id: CH-45
title: "Evolución del Runtime con Sesiones Abiertas"
starting_version: "0.2.1"
ending_version: "0.3"
introduces_components: []
introduces_contracts: [C-060]
modifies_contracts: [C-020]
constitutional_articles: [P-08, P-23, P-36, INV-12, INV-13, INV-E10, INV-E22]
previous_chapter: CH-44
next_chapter: CH-46
retrieval_set:
  expected_outcome:
    id: EO-CH45
    text: |
      Al terminar este capítulo podrás decidir cuándo una sesión abierta puede pasar a una versión nueva
      del agente, la política, el modelo, las conexiones o el formato de sesión, y explicar qué trabajo
      vivo lo impide y qué se registra cuando cambia.
  skeleton:
    id: SK-CH45
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
    contracts_to_be_introduced: [C-060]
  guiding_questions:
    - id: GQ-CH45-01
      text: |
        Si despliegas una versión nueva del agente mientras un usuario tiene abierta una conversación de
        varios días, ¿cuándo debería esa conversación pasar a la versión nueva?
      answered_by: RQ-CH45-01
    - id: GQ-CH45-02
      text: |
        ¿Y una conversación que empezó antes de que el sistema registrara versiones? ¿Deberías suponer
        que está en la primera versión?
      answered_by: RQ-CH45-02
    - id: GQ-CH45-03
      text: |
        Si un servidor externo publica una versión nueva de sus herramientas, ¿qué versión debería ver
        una conversación que ya estaba usando las viejas?
      answered_by: RQ-CH45-03
    - id: GQ-CH45-04
      text: |
        Si el agente cambia de modelo a mitad de una tarea, ¿es eso un cambio de versión? ¿Cómo debería
        quedar registrado?
      answered_by: RQ-CH45-04
  systems_lens:
    iceberg_visible_fact: |
      SessionState no dice con qué versiones corre una sesión: un despliegue nuevo cambia el agente, la
      política o las tools de una conversación a mitad de una espera, y nadie puede decir después con
      qué versión se tomó cada decisión (ver sección 2, El Problema).
    iceberg_patterns: |
      El patrón que se repite es que INV-E10 registra versiones por run, pero una sesión atraviesa
      muchos runs y varios despliegues; sin la versión en la sesión, migrar es algo que pasa sin que
      nadie lo decida, incluso con trabajo vivo en curso (ver sección 3).
    iceberg_structures: |
      Este capítulo introduce RuntimeVersionSnapshot (C-060), lleva SessionState (C-020) a v3 con
      runtimeVersion (ADR-003 parte v3), y le da a SessionManager la decisión de migrar y a
      ConnectionManager la versión fijada de cada conexión (ver sección 8).
    iceberg_mental_models: |
      Los modelos mentales son P-36 (el runtime evoluciona bajo sesiones abiertas solo en fronteras
      inactivas), INV-E22 (el trabajo vivo nunca migra), INV-E10 (versiones exactas) e INV-13 (una
      ejecución durable se reconstruye desde lo persistido) (ver sección 4).
    reinforcing_loop: |
      Si una sesión migra con trabajo vivo, una espera estacionada se retoma con otra política o un paso
      sin confirmar se recupera con otro formato; cada inconsistencia obliga a corregir a mano, y cada
      corrección es otra intervención sin versión registrada.
    balancing_loop: |
      sessionMayMigrate es el equilibrio: mientras haya trabajo vivo, la sesión se queda en su versión;
      cuando el trabajo vivo termina, migra. La versión nueva se adopta sola, a medida que cada sesión
      llega a su frontera inactiva.
    leverage_point: |
      La decisión con mayor efecto de este capítulo es que RuntimeVersionSnapshot (C-060) viva en la
      sesión y solo cambie en una frontera inactiva: con eso un despliegue nunca toca trabajo vivo, y
      cada decisión puede atribuirse a la versión exacta que la tomó.
  recall_questions:
    - id: RQ-CH45-01
      text: |
        ¿Qué tres tipos de trabajo vivo cuenta liveWorkOf, y qué decide sessionMayMigrate si hay alguno?
    - id: RQ-CH45-02
      text: |
        ¿Cómo trata el arnés una sesión sin runtimeVersion, y qué necesita para migrarla?
    - id: RQ-CH45-03
      text: |
        ¿Qué devuelve connectionVersionFor para una sesión con una versión fijada de la conexión, y para
        qué sirve connectionVersionInUse?
    - id: RQ-CH45-04
      text: |
        ¿Por qué cambiar de modelo entre turnos no es una migración, y qué hace recordModelSwitch?
  explain_prompts:
    - id: EP-CH45-01
      text: |
        SessionManager ya persistía y reconstruía sesiones. Explica, como si hablaras con alguien sin
        contexto técnico, por qué también le pertenece decidir cuándo una sesión pasa a una versión
        nueva, y por qué no hace falta un componente nuevo.
      target_entity: CMP-010
    - id: EP-CH45-02
      text: |
        Explica por qué la versión del runtime tiene que vivir en la sesión y no solo en cada run, y qué
        se perdería si se registrara solo por run.
      target_entity: C-060
  interleaved_questions:
    - id: IQ-CH45-01
      text: |
        En CH-10, reconstructSessionState armaba un SessionState a partir de un checkpoint. ¿Con qué
        runtimeVersion quedaría una sesión reconstruida así, qué haría eso con su próxima migración, y
        qué función de este capítulo lo evita?
      current_chapter_entities: [C-060]
      prior_chapter_entities: [C-020, CMP-010]
      prior_chapter: CH-10
  flashcards:
    - id: FC-CH45-01
      front: |
        ¿Qué es RuntimeVersionSnapshot (C-060)?
      back: |
        Las versiones con que corre una sesión: VersionSnapshot (agente, skill, política, configuración de
        modelo, capabilities), el modelo elegido, la versión traducida de cada conexión y el formato de
        sesión. Solo cambia en una frontera inactiva.
      source_entity: C-060
      chapter_introduced_in: CH-45
      review_stage: DAY_1
    - id: FC-CH45-02
      front: |
        ¿Qué agrega SessionState v3 (C-020) y qué significa que falte?
      back: |
        runtimeVersion, opcional. Si falta, la versión es desconocida (no la inicial): la sesión funciona
        como antes, pero solo migra con un migrador de formato explícito desde "desconocido".
      source_entity: C-020
      chapter_introduced_in: CH-45
      review_stage: DAY_1
    - id: FC-CH45-03
      front: |
        ¿Qué es trabajo vivo según INV-E22?
      back: |
        Esperas estacionadas (PARKED), pasos sin confirmar (STARTED) e invocaciones de agente no
        terminales. Con cualquiera de los tres, la sesión no migra.
      source_entity: C-060
      chapter_introduced_in: CH-45
      review_stage: DAY_1
  calibration_pairs:
    - id: CP-CH45-01
      recall_question: RQ-CH45-01
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH45-02
      recall_question: RQ-CH45-02
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH45-03
      recall_question: RQ-CH45-03
      confidence_levels: [Alta, Media, Baja]
    - id: CP-CH45-04
      recall_question: RQ-CH45-04
      confidence_levels: [Alta, Media, Baja]
---

# Capítulo 45 — Evolución del Runtime con Sesiones Abiertas

> **Regla constitucional (INV-E22):** el trabajo vivo (esperas pendientes, pasos sin confirmar, runs
> hijos activos) nunca migra entre versiones del runtime.

## 0. Preguntas Guía (Guiding Questions)

> Sección de umbral (§4 del plan `2026-08-23-metodo-aprendizaje-activo-lector.md`). Léela ANTES
> de la sección 1. El detalle estructurado vive en `retrieval_set` (frontmatter).

**Resultado esperado.** Al terminar este capítulo podrás decidir cuándo una sesión abierta puede pasar
a una versión nueva del agente, la política, el modelo, las conexiones o el formato de sesión. También
podrás explicar qué trabajo vivo lo impide y qué se registra cuando cambia.

**Esqueleto.** Séptimo capítulo de la versión 0.3. No introduce componentes: agrega
`RuntimeVersionSnapshot`, lleva `SessionState` a v3 (ADR-003 parte v3) y amplía `SessionManager` y
`ConnectionManager`.

**Preguntas guía** (respóndelas de memoria en la sección 21):

1. Si despliegas una versión nueva del agente mientras un usuario tiene abierta una conversación de
   varios días, ¿cuándo debería esa conversación pasar a la versión nueva?
2. ¿Y una conversación que empezó antes de que el sistema registrara versiones? ¿Deberías suponer que
   está en la primera versión?
3. Si un servidor externo publica una versión nueva de sus herramientas, ¿qué versión debería ver una
   conversación que ya estaba usando las viejas?
4. Si el agente cambia de modelo a mitad de una tarea, ¿es eso un cambio de versión? ¿Cómo debería
   quedar registrado?

## 1. Arquitectura Actual (Current Architecture)

- **`SessionManager` (CMP-010, CH-10)** persiste, reconstruye y ramifica sesiones. `SessionState`
  (C-020) va en v2 desde CH-29, con rama activa y resúmenes de ramas.
- **`VersionSnapshot` (CH-19)** registra, por decisión auditada, las versiones de agente, skill,
  política, configuración de modelo y capabilities (INV-E10). Vive en el run, no en la sesión.
- **Trabajo vivo**, de tres capítulos distintos:
  - esperas estacionadas: `ParkedWait` (C-044) en `PARKED` (CH-33);
  - pasos sin confirmar: `StepRecord` (C-042) en `STARTED` (CH-32);
  - invocaciones de agente no terminales: `AgentInvocation` (C-058, CH-44).
- **El modelo se elige turno a turno** con `selectModelDescriptor` (CH-39), y el cambio no se registra
  en la sesión (D-048).
- **Las tools de una conexión se traducen con una `connectionVersion`** (CH-41), pero nada dice qué
  versión ve una sesión abierta cuando el servidor cambia (D-046).

## 2. El Problema (Problem)

Un agente de soporte atiende un caso que dura una semana. El martes queda estacionado esperando la
aprobación de un supervisor. El miércoles se despliega una versión nueva del agente, con otra
política y un formato de sesión nuevo. Hoy:
- **la sesión no sabe en qué versión está:** cuando la aprobación llega, se retoma con la política
  nueva una espera que se estacionó con la vieja;
- **un paso que quedó sin confirmar** se recupera con un formato que no es el suyo (D-022);
- **la conexión al sistema de tickets publicó tools nuevas:** el caso abierto empieza a ver otro
  schema en mitad de una tool call (D-046);
- **el agente cambió de modelo el lunes para un razonamiento largo,** y la sesión no lo registra
  (D-048);
- **la auditoría no puede responder** con qué versión se tomó cada decisión de esa semana.

## 3. Por Qué la Arquitectura Actual No Basta (Why the Current Architecture Is Insufficient)

- **INV-E10 versiona el run, no la sesión.** Una sesión atraviesa muchos runs y varios despliegues; sin
  su versión, migrar es algo que pasa solo, sin que nadie lo decida (D-017).
- **Nadie junta el trabajo vivo.** Está repartido en tres registros de tres capítulos, y ninguna
  función pregunta por los tres a la vez.
- **Una conexión retraducida reemplaza la anterior para todos,** incluso para quien estaba a mitad de
  usarla.
- **Suponer que una sesión sin versión está en la primera** es optimista: si el formato ya cambió una
  vez, migrarla con el migrador equivocado corrompe su historia.
- **No hace falta un componente nuevo:** la sesión es de `SessionManager` y la traducción de
  conexiones es de `ConnectionManager` (EVO-01).

## 4. Impacto Constitucional (Constitutional Impact)

```text
Constitutional Impact

Principles preserved
    P-08   Agent state y session state son distintos: la versión vive en la sesión, no en AgentState.
    P-23   La ejecución durable es una propiedad del núcleo: lo durable no migra a mitad.
    P-36   (Amendment v1.2) The runtime may evolve under open sessions only at idle boundaries.
           sessionMayMigrate lo decide; migrateSessionRuntime lo registra.

Invariants preserved
    INV-12   AgentState y SessionState siguen independientes.
    INV-13   Reconstruir una sesión conserva su runtimeVersion (reconstructWithRuntimeVersion).
    INV-E10  Las versiones exactas ahora también viven en la sesión.
    INV-E22  (Amendment v1.2) Live work never migrates between runtime versions.
             liveWorkOf lo cuenta; sessionMayMigrate lo hace cumplir.

Component ownership changes
    Ninguno nuevo. SessionManager gana la decisión de migrar ("persistencia", "reconstrucción");
    ConnectionManager, la versión de conexión que ve cada sesión (traducir, P-38).

Contract changes
    Nuevo: C-060 RuntimeVersionSnapshot.
    C-020 SessionState v2 → v3 (+ runtimeVersion; ADR-003 parte v3 Accepted).

Observability implications
    Nuevos AgentEventType: SESSION_RUNTIME_MIGRATED, MODEL_SWITCH_RECORDED.
```

## 5. Conceptos Nuevos (New Concepts)

- **Versión del runtime de una sesión:** el conjunto de versiones con que corre una sesión: las de
  INV-E10, el modelo elegido, la versión traducida de cada conexión y el formato de sesión.
- **Trabajo vivo:** esperas `PARKED`, pasos `STARTED` e invocaciones no terminales de la sesión.
- **Frontera inactiva:** el momento en que la sesión no tiene trabajo vivo. Es el único momento en
  que migra.
- **Migrador de formato:** una referencia a la transformación que lleva la historia de una sesión de
  un formato a otro. Desde "desconocido" hace falta uno explícito.
- **Versión desconocida:** la de una sesión sin `runtimeVersion` (anterior a este capítulo). Sigue
  funcionando como antes; no se supone que sea la primera.
- **Versión fijada de una conexión:** la versión traducida que ve una sesión hasta su próxima frontera
  inactiva.
- **Cambio de modelo:** elegir otro modelo entre turnos, dentro de la misma configuración de modelo. No
  es una migración; se registra.

## 6. Nuevas Estructuras de Datos (New Data Structures)

### Identificadores y tipos heredados

Estos tipos ya existen y este capítulo solo los referencia por nombre:
- **por contrato:** `SessionState` (C-020, que pasa a v3), `BranchSummary` (C-038), `StepRecord`
  (C-042), `ParkedWait` (C-044), `ModelDescriptor` (C-049), `AgentInvocation` (C-058),
  `ExecutionContext` (C-004), `AgentEvent` (C-010), `HarnessError` (C-011);
- **primitivos:** `SessionId`, `RunId`, `AgentId`, `Timestamp`.

| Identificador | Rol en este capítulo |
|---|---|
| `VersionSnapshot` | CH-19 §6: las versiones de INV-E10 |
| `SessionCheckpoint` | CH-10 §6: el checkpoint embebido en `SessionState` |
| `SessionCheckpointId` | CH-10 §6: id de un checkpoint |
| `ConnectionId` | CH-41 §6: id de una conexión |
| `WaitStatus` | CH-33 §6: se cuenta `PARKED` |
| `StepStatus` | CH-32 §6: se cuenta `STARTED` |
| `AgentEventType` | se agregan `SESSION_RUNTIME_MIGRATED` y `MODEL_SWITCH_RECORDED` |
| `ErrorCategory` | reutiliza `PERSISTENCE` |

### `RuntimeVersionSnapshot` — con qué versiones corre una sesión (C-060)

```pseudocode
STRUCT RuntimeVersionSnapshot
    versions: VersionSnapshot
    modelId: Text
    connectionVersions: Map<ConnectionId, Text>
    sessionFormatVersion: Integer
    adoptedAt: Timestamp
END
```

- `versions` reutiliza el `VersionSnapshot` de CH-19: las mismas cinco versiones de INV-E10.
- `modelId` es el modelo elegido; `versions.modelConfigVersion` es la configuración que lo permite.
- `connectionVersions` fija la versión traducida de cada conexión (D-046).
- `sessionFormatVersion` es la versión del formato con que se persiste la historia.
- `adoptedAt` es cuándo la sesión adoptó este conjunto de versiones.

### `SessionState` — versión 3 (C-020)

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
    runtimeVersion: Optional<RuntimeVersionSnapshot>
END
```

**Compatibilidad hacia atrás:** una sesión sin `runtimeVersion` es de versión **desconocida**
(ajuste aprobado de ADR-003). Funciona como en CH-10..CH-44; lo único que no puede hacer es migrar sin
un migrador explícito desde "desconocido".

### `LiveWork` y `SessionFormatMigrator` (embebidos)

```pseudocode
STRUCT LiveWork
    pendingWaits: Integer
    uncommittedSteps: Integer
    activeChildInvocations: Integer
END
```

```pseudocode
STRUCT SessionFormatMigrator
    fromFormatVersion: Optional<Integer>
    toFormatVersion: Integer
    migratorRef: Text
END
```

`fromFormatVersion` en `NULL` es un migrador desde un formato desconocido. `migratorRef` es una
referencia: la transformación la aplica el adaptador de persistencia.

## 7. Nuevos Contratos / Interfaces (New Contracts / Interfaces)

```text
ID:                     C-060
Name:                   RuntimeVersionSnapshot
Version:                v1
Introduced In:          CH-45
Used By:                [CMP-010, CMP-028]
Constitutional Impact:  [P-36, INV-13, INV-E10, INV-E22]
```

```text
C-020 SessionState  v2 → v3   Modified By: [CH-29, CH-45]
                    + runtimeVersion: Optional<RuntimeVersionSnapshot>
ADR:                ADR-003 parte v3 (Accepted 2026-10-10, con el ajuste "versión desconocida")
```

`LiveWork` y `SessionFormatMigrator` quedan embebidos.

## 8. Responsabilidades de Componentes (Component Responsibilities)

**Este capítulo no introduce componentes.** Dos componentes ganan funciones dentro de su `owns`
literal:

```text
SessionManager (CMP-010)
    owns: "persistencia", "recuperación", "branching", "checkpoints", "reconstrucción"
    nuevas:
        liveWorkOf, hasLiveWork, findFormatMigrator, formatMigrationAvailable, sessionMayMigrate,
        withRuntimeVersion, migrateSessionRuntime, recordModelSwitch, reconstructWithRuntimeVersion
    no posee:
        decidir qué versión desplegar (el proceso de despliegue y OperationalController, CH-18)
        aplicar la transformación de formato (el adaptador de persistencia, vía migratorRef)
        elegir el modelo (ModelGateway, selectModelDescriptor, CH-39)

ConnectionManager (CMP-028)
    owns: traducir las tools de una conexión declarada en CapabilityDescriptor (P-38)
    nuevas:
        connectionVersionFor, connectionVersionInUse
    no posee:
        resolver la capability (CapabilityRegistry, CH-08)
```

## 9. Relaciones de Dependencia (Dependency Relationships)

```text
Despliegue de una versión nueva (target: RuntimeVersionSnapshot)
    por cada sesión abierta:
        liveWorkOf(sesión, esperas, pasos, invocaciones) → LiveWork
        sessionMayMigrate → sí: migrateSessionRuntime → SESSION_RUNTIME_MIGRATED
                          → no: la sesión sigue en su versión; se reintenta en su frontera inactiva
Sesión nueva:          withRuntimeVersion(sesión, versión vigente)
Entre turnos:          selectModelDescriptor (CH-39) → recordModelSwitch → MODEL_SWITCH_RECORDED
Conexión retraducida:  translateConnectionTools (CH-41) con la connectionVersion nueva
                       connectionVersionFor(sesión) → la versión fijada o la última
                       connectionVersionInUse → conservar la versión vieja mientras alguien la use
Reconstrucción:        reconstructSessionState (CH-10) → reconstructWithRuntimeVersion
```

## 10. Diagrama de Secuencia (Sequence Diagram)

**Vista 1 — Componentes**

```text
Despliegue → SessionManager.liveWorkOf → sessionMayMigrate → migrateSessionRuntime
ModelGateway.selectModelDescriptor → SessionManager.recordModelSwitch
ConnectionManager.connectionVersionFor ← SessionState.runtimeVersion.connectionVersions
```

**Vista 2 — Sequence: el caso de soporte**

```text
Martes:    sesión s-1 en versión A (formato 3); ParkedWait w-4 PARKED (aprobación)
Miércoles: despliegue de la versión B (formato 4)
   │ liveWorkOf(s-1) = 1 espera, 0 pasos, 0 invocaciones
   │ sessionMayMigrate = FALSE → s-1 sigue en A
Jueves:    llega la aprobación; w-4 se retoma con la política de A; el run termina
   │ liveWorkOf(s-1) = 0, 0, 0
   │ sessionMayMigrate: migrador 3 → 4 existe = TRUE
   │ migrateSessionRuntime → s-1 en B           → SESSION_RUNTIME_MIGRATED
```

**Vista 2b — Sequence: una sesión anterior a este capítulo**

```text
sesión s-0 sin runtimeVersion (versión desconocida), sin trabajo vivo
   → formatMigrationAvailable busca un migrador desde NULL hacia el formato 4
   → no existe → SESSION_FORMAT_MIGRATOR_MISSING: s-0 sigue funcionando como antes, sin migrar
```

**Vista 2c — Sequence: cambio de modelo y conexión retraducida**

```text
Lunes: selectModelDescriptor elige "razonador-largo" → recordModelSwitch → modelId actualizado
Miércoles: el sistema de tickets publica v7 de sus tools; s-1 tiene fijada v6
   → connectionVersionFor(s-1, tickets, "v7") = "v6"
   → connectionVersionInUse(sesiones, tickets, "v6") = TRUE: v6 se conserva
```

**Vista 3 — Pseudocódigo:** ver la sección 11.

## 11. Pseudocódigo (Pseudocode)

```pseudocode
FUNCTION liveWorkOf(
    session: SessionState,
    waits: List<ParkedWait>,
    steps: List<StepRecord>,
    invocations: List<AgentInvocation>
) -> LiveWork

    pendingWaits: Integer = 0
    uncommittedSteps: Integer = 0
    activeChildInvocations: Integer = 0

    FOR EACH wait IN waits
        IF wait.sessionId == session.sessionId AND wait.status == PARKED
            pendingWaits = pendingWaits + 1
        END
    END

    FOR EACH step IN steps
        IF contains(session.runIds, step.runId) AND step.status == STARTED
            uncommittedSteps = uncommittedSteps + 1
        END
    END

    FOR EACH invocation IN invocations
        IF contains(session.runIds, invocation.parentRunId)
            AND NOT isTerminalInvocationStatus(invocation.status)
            activeChildInvocations = activeChildInvocations + 1
        END
    END

    RETURN LiveWork(
        pendingWaits = pendingWaits,
        uncommittedSteps = uncommittedSteps,
        activeChildInvocations = activeChildInvocations
    )
END
```

```pseudocode
FUNCTION hasLiveWork(
    live: LiveWork
) -> Boolean

    RETURN live.pendingWaits > 0 OR live.uncommittedSteps > 0 OR live.activeChildInvocations > 0
END
```

```pseudocode
FUNCTION findFormatMigrator(
    migrators: List<SessionFormatMigrator>,
    fromFormatVersion: Optional<Integer>,
    toFormatVersion: Integer
) -> Optional<SessionFormatMigrator>

    FOR EACH migrator IN migrators
        IF migrator.fromFormatVersion == fromFormatVersion AND migrator.toFormatVersion == toFormatVersion
            RETURN migrator
        END
    END

    RETURN NULL
END
```

```pseudocode
FUNCTION formatMigrationAvailable(
    session: SessionState,
    target: RuntimeVersionSnapshot,
    migrators: List<SessionFormatMigrator>
) -> Boolean

    IF session.runtimeVersion == NULL
        RETURN findFormatMigrator(migrators, NULL, target.sessionFormatVersion) != NULL
    END

    IF session.runtimeVersion.sessionFormatVersion == target.sessionFormatVersion
        RETURN TRUE
    END

    RETURN findFormatMigrator(
        migrators, session.runtimeVersion.sessionFormatVersion, target.sessionFormatVersion
    ) != NULL
END
```

```pseudocode
FUNCTION sessionMayMigrate(
    session: SessionState,
    live: LiveWork,
    target: RuntimeVersionSnapshot,
    migrators: List<SessionFormatMigrator>
) -> Boolean

    RETURN NOT hasLiveWork(live) AND formatMigrationAvailable(session, target, migrators)
END
```

```pseudocode
FUNCTION withRuntimeVersion(
    session: SessionState,
    snapshot: RuntimeVersionSnapshot
) -> SessionState

    RETURN SessionState(
        sessionId = session.sessionId,
        runIds = session.runIds,
        latestCheckpoint = session.latestCheckpoint,
        parentCheckpointId = session.parentCheckpointId,
        activeCheckpointId = session.activeCheckpointId,
        branchSummaries = session.branchSummaries,
        createdAt = session.createdAt,
        updatedAt = now(),
        runtimeVersion = snapshot
    )
END
```

```pseudocode
FUNCTION migrateSessionRuntime(
    session: SessionState,
    live: LiveWork,
    target: RuntimeVersionSnapshot,
    migrators: List<SessionFormatMigrator>,
    execution: ExecutionContext,
    agentId: AgentId
) -> SessionState

    IF hasLiveWork(live)
        THROW HarnessError(
            category = PERSISTENCE,
            code = "LIVE_WORK_BLOCKS_MIGRATION",
            message = "La sesión tiene esperas, pasos sin confirmar o invocaciones activas; migra en su próxima frontera inactiva",
            recoverable = TRUE,
            retryable = TRUE,
            metadata = {}
        )
    END

    IF NOT formatMigrationAvailable(session, target, migrators)
        THROW HarnessError(
            category = PERSISTENCE,
            code = "SESSION_FORMAT_MIGRATOR_MISSING",
            message = "No hay un migrador explícito desde el formato de la sesión (o desde un formato desconocido) hacia el nuevo",
            recoverable = FALSE,
            retryable = FALSE,
            metadata = {}
        )
    END

    migrated: SessionState = withRuntimeVersion(session, target)

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = SESSION_RUNTIME_MIGRATED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = session.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = target
    )

    RETURN migrated
END
```

```pseudocode
FUNCTION recordModelSwitch(
    session: SessionState,
    descriptor: ModelDescriptor,
    execution: ExecutionContext,
    agentId: AgentId
) -> SessionState

    IF session.runtimeVersion != NULL AND session.runtimeVersion.modelId == descriptor.modelId
        RETURN session
    END

    EMIT AgentEvent(
        eventId = newEventId(),
        eventType = MODEL_SWITCH_RECORDED,
        timestamp = now(),
        runId = execution.runId,
        sessionId = session.sessionId,
        agentId = agentId,
        traceId = execution.traceId,
        payload = descriptor
    )

    IF session.runtimeVersion == NULL
        RETURN session
    END

    RETURN withRuntimeVersion(session, RuntimeVersionSnapshot(
        versions = session.runtimeVersion.versions,
        modelId = descriptor.modelId,
        connectionVersions = session.runtimeVersion.connectionVersions,
        sessionFormatVersion = session.runtimeVersion.sessionFormatVersion,
        adoptedAt = session.runtimeVersion.adoptedAt
    ))
END
```

```pseudocode
FUNCTION reconstructWithRuntimeVersion(
    checkpoint: SessionCheckpoint,
    runIds: List<RunId>,
    persisted: Optional<RuntimeVersionSnapshot>,
    execution: ExecutionContext,
    agentId: AgentId
) -> SessionState

    reconstructed: SessionState = reconstructSessionState(checkpoint, runIds, execution, agentId)

    IF persisted == NULL
        RETURN reconstructed
    END

    RETURN withRuntimeVersion(reconstructed, persisted)
END
```

```pseudocode
FUNCTION connectionVersionFor(
    session: SessionState,
    connectionId: ConnectionId,
    latest: Text
) -> Text

    IF session.runtimeVersion == NULL
        RETURN latest
    END

    pinned: Optional<Text> = valueOf(session.runtimeVersion.connectionVersions, connectionId)

    IF pinned == NULL
        RETURN latest
    END

    RETURN pinned
END
```

```pseudocode
FUNCTION connectionVersionInUse(
    sessions: List<SessionState>,
    connectionId: ConnectionId,
    version: Text
) -> Boolean

    FOR EACH session IN sessions
        IF session.runtimeVersion != NULL
            AND valueOf(session.runtimeVersion.connectionVersions, connectionId) == version
            RETURN TRUE
        END
    END

    RETURN FALSE
END
```

Utilidades primitivas: `contains` (¿la lista tiene el elemento?), `valueOf` (el valor de una clave
en un mapa, o `NULL`), `newEventId` y `now`.

`reconstructSessionState` (CH-10), `selectModelDescriptor` (CH-39), `translateConnectionTools`
(CH-41) e `isTerminalInvocationStatus` (CH-44) no cambian.

**Por qué `recordModelSwitch` no exige una frontera inactiva:** la configuración de modelo
(`versions.modelConfigVersion`) no cambia; el modelo se elige entre los que esa configuración
permite, como ya hacía CH-39. Registrar el cambio sirve para auditar, no para migrar.

**Por qué una sesión de versión desconocida sigue usando la última versión de cada conexión:** es lo
que hacía antes de este capítulo, y no hay una versión fijada que respetar. Al pasar por su primera
migración queda fijada como cualquier otra.

Nótese lo que estas funciones **no** hacen:
- ninguna transforma la historia: eso lo hace el adaptador de persistencia con `migratorRef`;
- ninguna espera a que el trabajo vivo termine: `sessionMayMigrate` dice "todavía no", y la migración
  se reintenta;
- ninguna decide qué versión desplegar.

## 12. Transiciones de Estado (State Transitions)

`AgentRunStatus` no cambia. La versión de una sesión:

```text
(sesión nueva)       → runtimeVersion = versión vigente
(sesión anterior)    → runtimeVersion = NULL (desconocida)
versión A, con trabajo vivo       → sigue en A (LIVE_WORK_BLOCKS_MIGRATION, reintentable)
versión A, sin trabajo vivo       → versión B (si hay migrador de formato o el formato no cambia)
desconocida, sin trabajo vivo     → versión B solo con un migrador desde NULL
cambio de modelo entre turnos     → misma versión, otro modelId (MODEL_SWITCH_RECORDED)
```

## 13. Semántica de Fallos (Failure Semantics)

Códigos nuevos de `HarnessError`, con una `ErrorCategory` ya existente:

```text
PERSISTENCE  LIVE_WORK_BLOCKS_MIGRATION       recoverable: TRUE,  retryable: TRUE
PERSISTENCE  SESSION_FORMAT_MIGRATOR_MISSING  recoverable: FALSE, retryable: FALSE
```

- `LIVE_WORK_BLOCKS_MIGRATION` no es una falla de la sesión: la sesión sigue en su versión y la
  migración se reintenta cuando llegue a su frontera inactiva.
- `SESSION_FORMAT_MIGRATOR_MISSING` deja la sesión en su versión, funcionando. Para migrarla hay que
  publicar el migrador que falta.
- Si la transformación de formato falla en el adaptador, la sesión no se persiste con la versión
  nueva: `migrateSessionRuntime` solo produce el estado, y persistirlo sigue siendo un paso aparte
  (CH-10).

## 14. Eventos Producidos (Events Produced)

```text
SESSION_RUNTIME_MIGRATED — la sesión pasó a otra versión (payload: RuntimeVersionSnapshot)
MODEL_SWITCH_RECORDED    — el run eligió otro modelo entre turnos (payload: ModelDescriptor)
```

## 15. Implicaciones de Seguridad / Política (Security / Policy Implications)

- **Una aprobación se resuelve con la política con la que se pidió.** Una espera estacionada es
  trabajo vivo: la sesión no cambia de política hasta que se resuelve.
- **La auditoría puede atribuir cada decisión a su versión:** la sesión registra su versión y cada
  cambio emite un evento (INV-E10).
- **Una versión sin migrador no corrompe historias:** una sesión de formato desconocido no se migra
  por suposición.
- **Una tool no cambia de schema a mitad de su uso:** la versión fijada de la conexión se respeta
  hasta la próxima frontera inactiva.
- **Retirar una versión de conexión es seguro solo cuando nadie la usa** (`connectionVersionInUse`).

## 16. Tests (Tests)

```text
TEST LiveWorkCountsParkedWaitsStartedStepsAndActiveInvocations
TEST LiveWorkIgnoresOtherSessions
TEST SessionWithLiveWorkMayNotMigrate
TEST SessionWithoutLiveWorkAndSameFormatMayMigrate
TEST FormatChangeRequiresAMigrator
TEST UnknownVersionRequiresAMigratorFromNull
TEST MigrationEmitsSessionRuntimeMigrated
TEST BlockedMigrationIsRetryable
TEST ModelSwitchUpdatesModelIdAndEmitsEvent
TEST SameModelDoesNotRecordASwitch
TEST ReconstructionKeepsThePersistedRuntimeVersion
TEST PinnedConnectionVersionWinsOverLatest
TEST UnpinnedConnectionUsesLatest
TEST OldConnectionVersionIsInUseWhileAnySessionPinsIt
TEST SessionWithoutRuntimeVersionBehavesAsV2
```

## 17. Arquitectura Después de Este Capítulo (Architecture After This Chapter)

```text
book-harness (v0.3 en curso, después de CH-45) — 29 componentes, 60 contratos, 46 capítulos

Components — 29, sin cambios
 ├── CMP-010 SessionManager      (+ trabajo vivo, migración en frontera inactiva, cambio de modelo)
 └── CMP-028 ConnectionManager   (+ versión fijada de cada conexión por sesión)

Contracts — 60
 ├── C-020 SessionState v3       (CH-10 → CH-29 → modificado en CH-45: runtimeVersion)
 └── C-060 RuntimeVersionSnapshot (CH-45)

Deuda: D-017, D-022, D-046 y D-048 resueltas. ADR-003 Accepted completo.
```

## 18. Lo Que Deliberadamente No Resolvemos Todavía (What We Deliberately Do Not Solve Yet)

- **Cómo se despliega una versión** (canarios, porcentajes, rollback): es del proceso de despliegue y
  de los comandos operacionales de CH-18. No es deuda.
- **Cómo se escribe un migrador de formato:** el libro modela la referencia y la regla de cuándo se
  aplica; la transformación es del adaptador de persistencia. No es deuda.
- **Forzar la migración de una sesión que nunca queda inactiva:** cancelar su trabajo vivo es un
  comando operacional explícito (CH-18), nunca algo que la migración haga sola. No es deuda.
- **Fijar las versiones de una sesión de versión desconocida sin migrarla:** fijarlas sería suponer
  qué versiones usó; queda desconocida hasta su primera migración. No es deuda.

## 19. Siguiente Incremento (Next Increment)

Ahora cada sesión sabe con qué versión corre, y cambiarla queda registrado. Pero lo que el arnés
**observa** de cada sesión —eventos, auditoría, trazas— todavía se captura igual para todas, sin
importar quién puede verla.

El siguiente capítulo introduce la **observabilidad por audiencia**:
- una `SessionAudience` (PUBLIC, PRIVATE, UNKNOWN) asignada al crear la sesión;
- una `TraceCapturePolicy` que fija el techo de lo que puede capturarse;
- `TelemetrySpan` como dato de diagnóstico, distinto de un evento y de una entrada de auditoría.

Será CH-46 ("Observabilidad por Audiencia"). `next_chapter` queda en `null` porque CH-46 todavía no
existe.

## 20. Lente de Sistemas (Systems Lens)

**El Iceberg**

1. **Hecho visible** (= §2): un despliegue cambia la política, el formato o las tools de una sesión
   a mitad de una espera, y nadie puede decir con qué versión se decidió cada cosa.
2. **Patrones** (= §3): INV-E10 versiona el run, no la sesión; migrar pasa solo.
3. **Estructuras** (= §8): `RuntimeVersionSnapshot` (C-060), `SessionState` v3 y funciones nuevas en
   `SessionManager` y `ConnectionManager`.
4. **Modelos mentales** (= §4): P-36, INV-E22, INV-E10 e INV-13.

**Bucles de retroalimentación**

- **Refuerzo:** migrar con trabajo vivo produce inconsistencias que se corrigen a mano, sin versión
  registrada.
- **Equilibrio:** `sessionMayMigrate`. Cada sesión adopta la versión nueva cuando llega a su frontera
  inactiva.

**Punto de apalancamiento**

La decisión con mayor efecto es que `RuntimeVersionSnapshot` (C-060) viva en la sesión y solo cambie
en una frontera inactiva: un despliegue nunca toca trabajo vivo.

## 21. Practica lo que Aprendiste (Practice What You Learned)

### Recordar

1. ¿Qué tres tipos de trabajo vivo cuenta `liveWorkOf`, y qué decide `sessionMayMigrate` si hay
   alguno? *(pregunta guía 1)*
2. ¿Cómo trata el arnés una sesión sin `runtimeVersion`, y qué necesita para migrarla?
   *(pregunta guía 2)*
3. ¿Qué devuelve `connectionVersionFor` para una sesión con una versión fijada de la conexión, y para
   qué sirve `connectionVersionInUse`? *(pregunta guía 3)*
4. ¿Por qué cambiar de modelo entre turnos no es una migración, y qué hace `recordModelSwitch`?
   *(pregunta guía 4)*

### Explicar

1. `SessionManager` ya persistía y reconstruía sesiones. Explica por qué también le pertenece decidir
   cuándo una sesión pasa a una versión nueva, y por qué no hace falta un componente nuevo.
2. Explica por qué la versión del runtime tiene que vivir en la sesión y no solo en cada run, y qué se
   perdería si se registrara solo por run.

### Conectar

1. En CH-10, `reconstructSessionState` armaba un `SessionState` a partir de un checkpoint. ¿Con qué
   `runtimeVersion` quedaría una sesión reconstruida así, qué haría eso con su próxima migración, y qué
   función de este capítulo lo evita?

### Espaciar

Las tres tarjetas de este capítulo entran hoy en `reviewStage = DAY_1`. Repásalas al día 3, al día 7
y al día 21.

### Calibrar

Antes de revisar tus respuestas, califica tu confianza en cada una (Alta / Media / Baja).
