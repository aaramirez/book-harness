# Plan — Extensión del libro v0.2 y v0.3: lecciones de eve, aportes de pi y conexión del arnés con el mundo

**Fecha:** 2026-09-24
**Estado:** 🚧 En ejecución. Fase 0 completa (T0.1–T0.6); CH-28 ✅; siguiente: CH-29. Se ejecuta sobre `d16e2c7` (CH-00..CH-27, 22 componentes, 35 contratos).

**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md`: plan base (pipeline, registries, scripts, DoD).
- `2026-08-23-metodo-aprendizaje-activo-lector.md`: `RetrievalSet`.
- `2026-08-24-mapa-mental-progresivo.md`: `BookMindMap`.
- `2026-09-18-capitulo-25-epilogo-secuenciacion.md`: P-09 y el orden.
- `2026-09-18-capitulo-26-*.md`, `2026-09-18-capitulo-27-*.md`: patrón de capítulo de integración.
- `2026-09-18-diagramas-interactivos-archify.md`: convención Archify.
- `constitution/ARCHITECTURE_CONSTITUTION.md`: Articles I–XII, EVO-01..10, Amendment v1.1.

**Fuentes de diseño externas:** vault de estudio `arnes-ai`, en `C:\Users\Home\Documents\P\arnes-ai`, commit `b9f9e43`. Este plan **transcribe lo necesario** para ejecutarse sin abrirlas.
- `docs/propuestas/book-harness/BH-Propuestas.md`: índice y hoja de ruta.
- `docs/propuestas/book-harness/BH-Propuesta-Lecciones-eve.md`: 9 lecciones de eve, con bocetos.
- `docs/propuestas/book-harness/BH-Propuesta-Aportes-pi.md`: 11 aportes de pi.
- `docs/propuestas/arnes0.1/Arnes-Filesystem-First.md`: estructura `agent/`, con MCP/OpenAPI/A2A, datos, canales, WebSocket y triggers.
- `docs/comparativas/Eve-vs-BookHarness-vs-Pi.md`: por qué cada cosa.
- `plans/005-book-harness-actualizacion-2026-09-24.md`: primera versión de este plan. **Este archivo la reemplaza** y agrega los capítulos de conexiones, datos, A2A y autoría.

---

## 0. Cómo ejecutar este plan (protocolo)

1. **Un incremento es un capítulo.** Cada incremento vive en su propia rama `cap-NN-<slug>` sobre `main`, con PR y merge a `main` antes de empezar el siguiente. Las Fases 0 y de cierre de release son incrementos sin capítulo.
2. **Antes de escribir cada capítulo** se crea su plan propio `planes/AAAA-MM-DD-capitulo-NN-<slug>.md`, con el formato de los existentes (p.ej. `2026-09-17-capitulo-17-idempotency-guard.md`). Allí se cierra el alcance usando la ficha de §6.
3. **Orden estricto** según §3. Un incremento no empieza si el anterior no terminó `build-all` en verde.
4. **Commits** en el estilo del repo: `Escribir CH-NN: <título>`, `Agregar ADR-00N: …`, `Ratificar Amendment v1.2`, `Corregir …`.
5. **Condición de parada:** si un validador exige algo que este plan no previó (p.ej. el spike T0.2 falla), se detiene el incremento y se abre un plan propio para el cambio de tooling. Nunca se desactiva un validador.
6. **Aprobación humana obligatoria** para: el Amendment v1.2 (T0.4), cada ADR que pase a `Accepted`, y el cierre de cada release. El agente `book-architect` propone, pero no aprueba (`agents/book-architect.md:16-30`).

---

## 1. Objetivo

Extender *"¿Cómo construir un arnés?"* con **20 capítulos nuevos (CH-28..CH-47)** en dos releases.

- **v0.2 — Núcleo robusto y operación durable.** Cierra huecos que el libro declara y no resuelve:
  - P-23 (ejecución durable) no tiene mecanismo;
  - `resumeAfterHumanResolution` no está cableada (`book/chapters/13-integracion-caminos-de-gobierno/chapter.md:643-646`);
  - `PAUSED` nunca se produce (`book/chapters/00-arquitectura-constitucion/chapter.md:451`);
  - la identidad no tiene contrato;
  - no hay steering, compactación estructurada ni política de replay.
- **v0.3 — Conectar, escalar y evolucionar.** El arnés se conecta con el mundo:
  - catálogo de modelos;
  - ExtensionHost;
  - **conexiones MCP y OpenAPI**;
  - **fuentes de datos gobernadas con recuperación**: el ContextEngine hoy "no hace retrieval" (`book/chapters/04-context-engine/chapter.md:776-779`);
  - presupuesto jerárquico;
  - **invocación durable entre agentes y A2A**;
  - evolución del runtime;
  - observabilidad por audiencia;
  - evaluación con lift;
  - **el agente como directorio** (autoría filesystem-first, P-06).

Todo sigue siendo pseudocódigo **independiente de la plataforma** (P-27): nada de Vercel, pi-ai ni SDKs. MCP, OpenAPI, A2A, WebSocket, SQL y los canales son **adaptadores**, o tipos de un contrato, nunca dependencias del núcleo.

---

## 2. Línea base verificada (2026-09-24)

| Verificación | Resultado |
| --- | --- |
| Commit | `d16e2c7`, `main` limpio, remoto `aaramirez/book-harness` |
| `node scripts/validate-contracts` | OK: 35 contratos |
| `node scripts/validate-components` | OK: 22 componentes |
| `validate-chapter` + `validate-retrieval-set` (28 capítulos, vía `build-all`) | OK |
| `node scripts/build-all` | **OK (exit 0)**: BookIR, mapa mental, web y `dist/book.pdf` (2,2 MB) |
| Warnings | 29 `Could not fetch resource …\dist.build\mindmap\*.pdf`: **bug T0.1**. El PDF sale sin mapas mentales en Windows |

**Entorno instalado para esta línea base (Windows):**

| Herramienta | Versión | Ubicación | Cómo se instaló |
| --- | --- | --- | --- |
| Graphviz (`dot`) | 16.1.0 | `C:\Program Files\Graphviz\bin` | `winget install Graphviz.Graphviz` |
| pandoc | 3.11 | `%LOCALAPPDATA%\Pandoc` | `winget install JohnMacFarlane.Pandoc` |
| XeTeX (TinyTeX, TeX Live 2026) | — | `%LOCALAPPDATA%\Programs\TinyTeX\bin\windows` | `gh release download v2026.09 -R rstudio/tinytex-releases -p "TinyTeX-1-windows-v2026.09.exe"` + autoextracción (el servidor de MiKTeX no respondía) |
| Paquete LaTeX `caption` | — | TinyTeX | `tlmgr install caption` |
| Ghostscript (`gs`) | 10.07.1 | `%USERPROFILE%\bin\gs.exe` | copia de `TinyTeX\tlpkg\tlgs\bin\gswin64c.exe` + `gsdll64.dll`, porque `render-diagram.js:49` invoca `gs` |

Las tres primeras rutas se agregaron al `Path` del usuario. **En una terminal abierta antes de la instalación**, anteponerlas manualmente:

```powershell
$env:Path = "C:\Program Files\Graphviz\bin;$env:LOCALAPPDATA\Pandoc;$env:LOCALAPPDATA\Programs\TinyTeX\bin\windows;$env:USERPROFILE\bin;" + $env:Path
```

Si un capítulo nuevo usa otro paquete LaTeX, `build-pdf` falla con `File 'x.sty' not found`. Se resuelve con `tlmgr install <paquete>`, y se anota en el registro de ejecución (§11).

---

## 3. Alcance: releases, capítulos y asignación de IDs

IDs correlativos por orden de introducción (regla de `registry/*.yaml`: nunca se reutiliza un id).

### Release v0.2 — Núcleo robusto y operación durable

| Cap. | Título | Origen | Componente | Contratos nuevos | Contratos modificados | Artículos |
| --- | --- | --- | --- | --- | --- | --- |
| CH-28 | Entradas que llegan durante el turno: steering y follow-up | pi | AgentLoop | C-036 PendingInput | — | P-10, INV-08, INV-10 |
| CH-29 | Compactar sin perder el hilo: resúmenes estructurados y sesiones en árbol | pi (+eve) | ContextEngine, SessionManager | C-037 CompactionSummary, C-038 BranchSummary | C-020 SessionState **v2** | P-01, P-08, P-14, EVO-09, INV-07 |
| CH-30 | Cuando no se sabe si ocurrió: política de replay | pi | CapabilityRegistry, IdempotencyGuard | C-039 ReplayPolicy | C-018 CapabilityDescriptor **v2**, C-009 ToolResult **v2** | P-24, INV-11, INV-E09, INV-E17 |
| CH-31 | La identidad del llamante y el arranque que no admite nada | eve | AdmissionController | C-040 Principal, C-041 CallerSnapshot | C-004 ExecutionContext **v2**, C-023 AdmissionDecision **v2** | P-17, P-31, INV-E15, INV-19 |
| CH-32 | Pasos durables y la recuperación a mitad de turno | eve + pi | **CMP-023 ExecutionJournal** | C-042 StepRecord, C-043 RecoveryDecision | — | P-23, P-32, INV-13, INV-E16, INV-E17 |
| CH-33 | Esperas durables y la reanudación desde cualquier canal | eve + pi | **CMP-024 ResumptionCoordinator** | C-044 ParkedWait, C-045 AuthorizationChallenge | C-015 HumanInteractionRequest **v2**, C-013 AgentRunStatus (se da uso a `PAUSED`) | P-33, INV-14, INV-15, INV-E18 |
| CH-34 | Canales y direcciones de continuación: HTTP, WebSocket, webhooks y schedules | eve | **CMP-025 ContinuationRegistry** | C-046 ContinuationAddress | C-022 ActivationRequest **v2** (+ `sourceKind`: CHANNEL, WEBSOCKET, WEBHOOK, SCHEDULE, STREAM_EVENT; + `continuationAddress`) | P-16, P-34, INV-E01, INV-E19 |
| CH-35 | El entorno aislado y las credenciales que solo existen en el egress | eve | **CMP-026 IsolatedExecutionEnvironment**, CredentialBroker | C-047 SandboxSession, C-048 NetworkPolicy | — | P-35, INV-E08, INV-E20, Article XII |
| CH-36 | Integración: el turno durable gobernado (`runDurableGovernedTurn`) | — | función de integración | — | — | todos los anteriores |

### Release v0.3 — Conectar, escalar y evolucionar

| Cap. | Título | Origen | Componente | Contratos nuevos | Contratos modificados | Artículos |
| --- | --- | --- | --- | --- | --- | --- |
| CH-37 | El modelo como dato: catálogo, costo y cache | pi | ModelGateway | C-049 ModelDescriptor, C-050 UsageRecord | C-006 ModelRequest **v2**, C-007 ModelResponse **v2** | P-02, P-29, INV-E10 |
| CH-38 | Extensiones que no pueden saltarse la constitución | pi | **CMP-027 ExtensionHost** | C-051 ExtensionRegistration, C-052 HookPoint, C-053 ResourceTrustDecision | — | P-07, P-12, EVO-10, INV-E24 |
| CH-39 | Conexiones: MCP y OpenAPI como fuentes de capabilities | eve | **CMP-028 ConnectionManager** | C-054 ConnectionDescriptor | C-018 CapabilityDescriptor **v3** (+ `sourceConnectionId`) | P-03, P-19, P-38, INV-04, INV-05, INV-E08, INV-E25 |
| CH-40 | Fuentes de datos gobernadas: recuperar sin tirarlo todo al contexto | eve (hueco) + libro | **CMP-029 RetrievalEngine** | C-055 DataSourceDescriptor, C-056 RetrievedCandidate | — | P-01, P-14, P-22, EVO-09, INV-E11, INV-E26 |
| CH-41 | Presupuestos que se heredan | eve | ExecutionController | C-057 ExecutionUsage (se promueve) | C-012 ExecutionBudget **v2** | INV-09, INV-E06, INV-E21 |
| CH-42 | Invocación durable entre agentes y A2A (único capítulo multi-agente) | eve (+A2A) | AgentCommunicationGateway | C-058 AgentInvocation, C-059 AgentCard | C-024 AgentCommunicationMessage **v2** | P-18..P-21, INV-E03..E06 |
| CH-43 | Evolucionar el runtime sin romper sesiones abiertas | eve + pi | SessionManager, ExecutionFabricAdapter | C-060 RuntimeVersionSnapshot | C-020 SessionState **v3** | P-27, P-36, INV-E10, INV-E22 |
| CH-44 | Observabilidad acotada por audiencia | eve + pi | DataGovernanceEngine, EventBus | C-061 SessionAudience, C-062 TraceCapturePolicy, C-063 TelemetrySpan | — | P-04, P-25, P-37, INV-E23 |
| CH-45 | Medir el aporte de un cambio: evaluación con lift | pi | EvaluationHarness | C-064 LiftReport | C-032 EvaluationReport **v2** | P-28, INV-E13 |
| CH-46 | El agente como directorio: autoría por convención | eve + pi | — (adaptador de autoría) | C-065 AgentManifest, C-066 AuthoringDiagnostic | — | P-06, P-39, EVO-10, INV-E27 |
| CH-47 | Integración: el arnés conectado (`runConnectedGovernedTurn`) | — | función de integración | — | — | todos |

**Totales:**

| | Cantidad | Rango |
| --- | --- | --- |
| Capítulos | 20 | CH-28..CH-47 |
| Componentes | 7 | CMP-023..CMP-029 |
| Contratos nuevos | 31 | C-036..C-066 |
| Modificaciones de contrato | 15 | sobre 13 contratos: C-018 ×2, C-020 ×2 |

**Dependencias que fijan el orden:**
- CH-30 → CH-32: `ReplayPolicy`.
- CH-31 → CH-33, CH-35, CH-42, CH-44: `Principal`.
- CH-32 + CH-33 → CH-34: la entrega por dirección puede reanudar una espera.
- CH-29 → CH-43: `SessionState` v2 → v3.
- CH-35 → CH-45: aislamiento de las corridas de eval.
- CH-39 + CH-40 + CH-34 → CH-46: el directorio declara conexiones, datos y canales.
- CH-41 → CH-42: presupuesto antes de multi-agente (P-09, EVO-02).

---

## 4. Amendment v1.2 — texto propuesto (T0.4, requiere aprobación humana)

Se agrega al final de `constitution/ARCHITECTURE_CONSTITUTION.md`, después de "Canonical Enterprise Planes" (`:991-1000`), **sin tocar P-01..P-30**.

Se ratifica completo al inicio, igual que el Amendment v1.1 existía antes de CH-14. Así los P e INV no se renumeran aunque cambie el orden de los capítulos.

```text
# Amendment v1.2 — Durable Operation, Identity, Connectivity and Authoring

## P-31 — Identity travels with every turn
## P-32 — A step is the unit of durability and recovery
## P-33 — Waiting is durable and consumes no compute
## P-34 — External conversations are addressed, not inferred
## P-35 — Secrets never enter model-controlled compute
## P-36 — The runtime may evolve under open sessions only at idle boundaries
## P-37 — Observability capture is bounded by audience
## P-38 — External capabilities enter only through declared connections
## P-39 — An agent is authored as inspectable, conventionally located files

## Additional Enterprise Invariants (v1.2)
INV-E15  An unconfigured harness admits nothing, in any environment; development admission depends on process mode, never on the request.
INV-E16  A committed step is never re-executed during recovery.
INV-E17  An effect whose outcome is unknown is re-executed only if its capability declares replayPolicy = SAFE.
INV-E18  A delivery resumes only the wait it addresses, and only if its responder is authorized for it.
INV-E19  A continuation address has at most one owning session at a time.
INV-E20  Credentials are never materialized inside the isolated execution environment.
INV-E21  A child budget never exceeds its parent's remaining budget.
INV-E22  Live work (pending waits, uncommitted steps, active child runs) never migrates between runtime versions.
INV-E23  No trace destination may capture content above the session's capture ceiling.
INV-E24  No hook point may return an authorization outcome.
INV-E25  No external tool reaches the model except as a CapabilityDescriptor resolved by CapabilityRegistry and evaluated by PolicyEngine.
INV-E26  Every data source declares a classification; an undeclared source is RESTRICTED.
INV-E27  An authoring diagnostic of level ERROR prevents any activation of that agent.
```

Cada principio lleva un párrafo en el mismo estilo de v1.1 (`:926-973`). El texto de cada uno sale de la sección "Lección" de la propuesta de eve o de pi.

---

## 5. ADRs (T0.3; `docs/adr/` hoy está vacío)

Formato mínimo del libro (`constitution/ARCHITECTURE_CONSTITUTION.md:867-884`): ADR-ID, Title, Status, Context, Decision, Alternatives, Consequences, Constitutional Articles Affected, Migration Strategy.

| ADR | Decisión | Contratos | Estrategia de migración | Capítulo que lo acepta |
| --- | --- | --- | --- | --- |
| ADR-001 | El principal verificado viaja en `ExecutionContext` | C-004 v2, C-023 v2 | `caller: Optional<CallerSnapshot>`: CH-00..CH-30 siguen válidos | CH-31 |
| ADR-002 | La capability declara su política de replay | C-018 v2, C-009 v2 | Default `NEVER` (fail-closed) | CH-30 |
| ADR-003 | La sesión es un árbol navegable con versión de runtime | C-020 v2 → v3 | `activeCheckpointId` y `runtimeVersion` opcionales | CH-29 (v2), CH-43 (v3) |
| ADR-004 | El presupuesto es jerárquico | C-012 v2 | `parentRunId` opcional | CH-41 |
| ADR-005 | Una capability puede venir de una conexión externa | C-018 v3 | `sourceConnectionId` opcional; las capabilities locales no cambian | CH-39 |

---

## 6. Fichas por capítulo (alcance cerrado de cada incremento)

Cada ficha es el **Paso 2 ("Alcance decidido")** del plan propio del capítulo. Los bocetos de pseudocódigo están en las propuestas de `arnes-ai` citadas en el encabezado, y se reescriben con la gramática de `skills/write-pseudocode/SKILL.md`.

### CH-28 — Steering y follow-up
- **Se amplía AgentLoop:** decide cuándo se aplica una entrada pendiente.
- **Contrato C-036 `PendingInput`:** `kind` (STEER / FOLLOW_UP), `mode` (ONE_AT_A_TIME / ALL), `message: AgentMessage` y `receivedAt`.
- **Reglas:**
  - un STEER se aplica solo "después de las tools, antes del modelo";
  - un FOLLOW_UP solo cuando `runTurn` daría COMPLETED;
  - nunca se cancela una tool en ejecución.
- **Tests §16:** steer entre batches; follow-up solo al final; ninguna tool se salta.

### CH-29 — Compactación estructurada y sesiones en árbol
- **ContextEngine:** `CompactionSummary` (goal, constraints, progress, decisions, nextSteps, criticalContext, touchedFiles, firstKeptMessageId, provenance).
- **Corte:** nunca separa una tool call de su resultado (INV-07). Primero se recorta sin modelo y luego se resume.
- **SessionManager:** `BranchSummary`, navegación entre ramas, y `SessionState` v2 con `activeCheckpointId`.
- **ADR-003** (parte v2).

### CH-30 — Política de replay
- **C-039 `ReplayPolicy`** (ENUM NEVER / SAFE).
- **C-018 v2:** `replayPolicy` con default NEVER.
- **C-009 v2:** agrega el resultado OUTCOME_UNKNOWN.
- **IdempotencyGuard** decide ante un resultado desconocido.
- **ADR-002.**

### CH-31 — Identidad del llamante y arranque seguro
- **Contratos:** C-040 `Principal` (principalId, principalType USER / SERVICE / RUNTIME, issuer, tenantId?, attributes) y C-041 `CallerSnapshot` (initiator, current).
- **AdmissionController:** `verifyExternalIdentity` como punto de extensión declarado.
- **C-004 v2 y C-023 v2.**
- **INV-E15.**
- **Advertencia explícita:** la admisión no es propiedad de sesión.
- **ADR-001.**

### CH-32 — Pasos durables (CMP-023 ExecutionJournal)
- **Ficha:**
  - `owns`:
    - "declarar un paso COMMITTED solo cuando su resultado está persistido";
    - "decidir REPLAY_RECORDED / REEXECUTE / REPORT_OUTCOME_UNKNOWN por paso".
  - `does_not_own`: dedup por clave (IdempotencyGuard), historia de sesión (SessionManager) y continuación (ExecutionController).
- **Contratos:** C-042 `StepRecord` (incluye la respuesta parcial ya comprometida, aporte de pi) y C-043 `RecoveryDecision`.
- **Funciones:** `beginStep`, `commitStep`, `recoverRun`, `decideStepRecovery`.

### CH-33 — Esperas durables (CMP-024 ResumptionCoordinator)
- **C-044 `ParkedWait`:** `kind` puede ser TOOL_APPROVAL, QUESTION, AUTHORIZATION o BUDGET_LIMIT.
- **C-045 `AuthorizationChallenge`:** OAuth por usuario.
- **Cablea `resumeAfterHumanResolution`** de CH-13.
- **Da uso a `PAUSED`** para esperas no humanas.
- **Anexo:** protocolo de UI remota (solicitud y respuesta de diálogo, de pi) como adaptador de HumanInteractionService (INV-14, INV-16).

### CH-34 — Canales y direcciones de continuación (CMP-025 ContinuationRegistry)
- **C-046 `ContinuationAddress`** (channelRef, conversationRef) con propiedad exclusiva (INV-E19).
- **C-022 v2**, con `sourceKind` y `continuationAddress`.
- **Canales como Ingress Adapters,** fuera del registro, cada uno con su sección: HTTP (API de sesiones), **WebSocket de entrada** (conexión persistente, un turno por mensaje), webhooks (firma verificada en tiempo constante), y **schedules** (cron) y **eventos de stream** como fuentes de `ActivationRequest` (P-16).
- **Regla de estructura:** un canal sin regla de admisión no escucha (se relaciona con INV-E15).

### CH-35 — Entorno aislado (CMP-026 IsolatedExecutionEnvironment)
- **Contratos:** C-047 `SandboxSession` y C-048 `NetworkPolicy` (DENY_ALL, ALLOW_ALL, o allow-list con transformaciones que referencian `CredentialReference`).
- **CredentialBroker** resuelve en el egress.
- **ToolRuntime** delega las capabilities SHELL y FILESYSTEM.
- **INV-E20.**

### CH-36 — Integración v0.2
- **`runDurableGovernedTurn`:** admisión con Principal → continuación o activación → pasos con journal → espera aparcada y reanudación → recuperación tras un crash.
- **Es la primera integración que sí cablea los caminos de CH-13,** y lo dice explícitamente.

### CH-37 — El modelo como dato
- **Contratos:** C-049 `ModelDescriptor` (modelId, provider, contextWindow, maxOutputTokens, pricing, capabilities) y C-050 `UsageRecord` (input, output, cacheRead, cacheWrite, cost).
- **C-006 v2** (`cacheRetention`) y **C-007 v2** (`usage`).
- **Vínculo:** `BusinessOutcomeCorrelation` (CH-22) puede medir el costo por resultado.

### CH-38 — ExtensionHost (CMP-027)
- **Contratos:** C-051 `ExtensionRegistration`, C-052 `HookPoint` (ENUM: BEFORE_RUN, TRANSFORM_CONTEXT, BEFORE_REQUEST, AFTER_RESPONSE, BEFORE_TOOL, AFTER_TOOL, BEFORE_COMPACTION, BEFORE_NAVIGATION) y C-053 `ResourceTrustDecision`.
- **INV-E24:** ningún hook devuelve "autorizado".
- **Hace cumplir EVO-10.**
- **Separación P-12:** los hooks intervienen, los observers observan.

### CH-39 — Conexiones MCP y OpenAPI (CMP-028 ConnectionManager)
- **Ficha:**
  - `responsibility`: gestionar el ciclo de vida de proveedores externos de capabilities (servidores **MCP** por **stdio** o **HTTP/SSE**, y especificaciones **OpenAPI**), y traducir sus tools u operaciones en `CapabilityDescriptor` con espacio de nombres `<conexión>__<tool>`, filtro allow/block y argumentos provistos (ocultos al modelo).
  - `does_not_own`: tokens (CredentialBroker), autorización (PolicyEngine), ejecución (ToolRuntime) y resolución (CapabilityRegistry).
- **C-054 `ConnectionDescriptor`:** id, kind MCP / OPENAPI, transport STDIO / HTTP, endpointRef, toolFilter, providedArguments, credentialName?, approvalDefault.
- **C-018 v3** (`sourceConnectionId`, **ADR-005**).
- **P-38 e INV-E25.**
- **Sección:** el arnés como **servidor** MCP es un canal (CH-34), no una conexión.

### CH-40 — Fuentes de datos gobernadas (CMP-029 RetrievalEngine)
- **Cierra el hueco declarado en CH-04:** `candidates` llegan "ya dados, sin retrieval".
- **C-055 `DataSourceDescriptor`:** id, kind (SQL, FILES, HTTP, STREAM), transport?, classification, access READ_ONLY, scopeRule.
- **C-056 `RetrievedCandidate`:** sourceId, content, provenance y label (`DataGovernanceLabel`, C-030).
- **Streams (WebSocket o SSE de salida):** una fuente STREAM puede emitir `ActivationRequest` con `sourceKind = STREAM_EVENT` (vínculo con CH-34).
- **INV-E26:** sin clasificación, la fuente es RESTRICTED.
- **Ficha:** `does_not_own` incluye clasificar (DataGovernanceEngine), ensamblar el snapshot (ContextEngine) y resolver credenciales (CredentialBroker).

### CH-41 — Presupuestos que se heredan
- **C-057 `ExecutionUsage`:** se promueve desde la estructura embebida de `book/chapters/07-execution-controller/chapter.md:588`.
- **C-012 v2** (`parentRunId`, `consumed`).
- **`allocateChildBudget`.**
- **INV-E21.**
- **ADR-004.**

### CH-42 — Invocación durable entre agentes y A2A
- **C-058 `AgentInvocation`:** invocationId, owner: Principal, childRunId, status (WORKING, INPUT_REQUIRED, AUTHORIZATION_REQUIRED, COMPLETED, FAILED, CANCELLED), result?, expiresAt?.
- **C-059 `AgentCard`:** anuncio de capacidades: agentRef, skills, endpointRef, authScheme.
- **C-024 v2** (`invocationId`).
- **A2A es un adaptador de protocolo** del Gateway (P-19, INV-E04/E05). Nunca es una dependencia del núcleo.

### CH-43 — Evolución del runtime
- **C-060 `RuntimeVersionSnapshot`:** versión de agente, política, modelo y **formato de sesión** (aporte de pi).
- **C-020 v3.**
- **`sessionMayMigrate`.**
- **INV-E22.**
- **ADR-003** (parte v3).

### CH-44 — Observabilidad por audiencia
- **Contratos:** C-061 `SessionAudience` (PUBLIC / PRIVATE / UNKNOWN), C-062 `TraceCapturePolicy` y C-063 `TelemetrySpan` ("diagnostic data, not business state").
- **Tabla de tres columnas:** evento (observa), auditoría (prueba) y span (diagnostica).
- **INV-E23.**

### CH-45 — Evaluación con lift
- **C-064 `LiftReport`:** baselineRef, treatmentRef, metric, scores, lift, isolationRef.
- **C-032 v2** (`evidence`).
- **Cada corrida** se hace en su propio entorno aislado (CH-35).

### CH-46 — El agente como directorio
- **Contratos:** C-065 `AgentManifest` (fuentes con origen y ruta) y C-066 `AuthoringDiagnostic` (level, code, path).
- **Mapa ranura → contrato:**
  - `agent.ts` → `AgentConfig` (C-002) + `ExecutionBudget` (C-012);
  - `tools/` → `CapabilityDescriptor`;
  - `connections/` → `ConnectionDescriptor`;
  - `data/` → `DataSourceDescriptor`;
  - `channels/` y `schedules/` → Ingress Adapters;
  - `policies/` → reglas de PolicyEngine;
  - `skills/` → `SkillDescriptor`;
  - `hooks/` → `ExtensionRegistration`.
- **Reglas:** la ruta es la identidad; los defaults ocupan las mismas ranuras; el markdown es dato; hace falta confianza antes de ejecutar código.
- **INV-E27** y **P-39.**
- **Es un adaptador de autoría, sin componente** (EVO-01). El propio arnés de producción del libro es el ejemplo: `registry/`, `book/`, `planes/` son autoría filesystem-first.

### CH-47 — Integración v0.3
- **`runConnectedGovernedTurn`:** manifiesto sin errores → admisión → recuperación de datos gobernados → capabilities de conexión autorizadas → invocación A2A con presupuesto heredado → trazas acotadas por audiencia.

---

## 7. Fase 0 — Preparación (antes de CH-28)

| Tarea | Qué | Cómo se verifica |
| --- | --- | --- |
| **T0.1** | Corregir el bug de rutas en Windows: normalizar a `/` las rutas de imagen que `scripts/build-pdf` escribe en el Markdown (`:123` y `:182`, p.ej. `pdfPath.split(path.sep).join('/')`) | `build-all` sin ningún `Could not fetch resource`; el PDF incluye los mapas mentales. Commit: `Corregir rutas de mapas mentales en build-pdf para Windows` |
| **T0.2** | **Spike de validadores** en la rama desechable `spike/contract-v2`: poner C-004 en v2 con un campo `Optional<CallerSnapshot>` (tipo inexistente todavía), declarar un capítulo ficticio CH-28 que lo modifique, y correr `build-all` | Confirmar tres cosas: (a) `validate-chapter` acepta `modifies_contracts` (`scripts/validate-chapter:151-178`); (b) `validate-contracts` acepta `version: v2` + `modified_by` (`scripts/validate-contracts:11-52`); (c) **CH-00..CH-27 no fallan** aunque la `current_definition` de C-004 mencione un tipo de un capítulo posterior. Si (c) falla, se abre un plan de tooling para versionar definiciones **antes** de CH-28. La rama no se mergea. |
| **T0.3** | Borradores de ADR-001..005 en `docs/adr/`, con `Status: Proposed` | Cinco archivos con las 9 secciones del formato |
| **T0.4** | Amendment v1.2 (§4) en la constitución, más el plan `planes/2026-MM-DD-amendment-v1-2.md` con la aprobación humana registrada | Diff solo después de `:1000`; `build-all` en verde |
| **T0.5** | ~~Glosario en Fase 0~~ **Corregido (2026-09-24):** cada término de `registry/glossary.yaml` exige `introduced_in` con un capítulo existente, así que los términos nuevos entran **en el paso 3 del incremento que los introduce**, no en la Fase 0 | — |
| **T0.6** | Decidir y anotar en §10: **versión del libro** (0.2 / 0.3, o mantener 0.1) y **nombres finales de los tramos** en CH-25 | Anotado en el registro (§11) |

---

## 8. Procedimiento por incremento (CH-28 … CH-47)

```text
0. git checkout main && git pull && git checkout -b cap-NN-<slug>
1. Plan propio en planes/AAAA-MM-DD-capitulo-NN-<slug>.md (alcance = ficha §6). book-architect produce el Chapter Brief.
2. ROJO:   agregar { id: CH-NN, file: chapters/NN-<slug>/chapter.md } a book/book.yaml
           + chapter.md con solo el frontmatter (id, title, starting_version, ending_version,
             introduces_components, introduces_contracts, modifies_contracts, constitutional_articles,
             previous_chapter, next_chapter, retrieval_set)
           node scripts/validate-chapter book/chapters/NN-<slug>/chapter.md   → debe FALLAR
3. REGISTRO:
           registry/components.yaml  (ficha de 10 campos; does_not_own citando componentes ya registrados)
           registry/contracts.yaml   (nuevos con introduced_in: CH-NN; modificados: version++, current_definition, modified_by += CH-NN)
           registry/glossary.yaml
           node scripts/validate-components && node scripts/validate-contracts   → OK
4. CAPÍTULO: secciones 0–21 con las skills write-technical-chapter, define-component, define-contract,
           write-pseudocode (sin entidades mágicas), analyze-constitutional-impact (§4 y §17),
           design-retrieval-practice (retrieval_set)
5. VERDE:  node scripts/validate-chapter book/chapters/NN-<slug>/chapter.md
           node scripts/validate-retrieval-set book/chapters/NN-<slug>/chapter.md   → OK
6. ENCADENAR: el next_chapter del capítulo anterior pasa a CH-NN (para CH-28: el de CH-27, hoy null)
7. PIPELINE: node scripts/build-all → exit 0, sin warnings nuevos
8. DIAGRAMA: diagrams/archify/capitulo-NN-<slug>.json → archify validate --quality showcase (9/9, 0/0)
           → archify deliver → archify visual-check (convención de 2026-09-18-diagramas-interactivos-archify.md)
9. KB:     kb/04-Capitulos/CH-NN.md, kb/02-Componentes/CMP-0xx.md, kb/03-Contratos/C-0xx.md
10. ADR:   si el capítulo modifica un contrato con ADR, pasar el ADR a Accepted (con aprobación humana)
11. Registro de ejecución en el plan del capítulo (archivos creados/modificados, resultado del pipeline, DoD, deuda)
12. commit "Escribir CH-NN: <título>" → push → PR → merge a main
```

**Definition of Done por capítulo:**
- `build-all` termina en 0.
- Ninguna entidad sin registro previo.
- Ningún nombre de plataforma o SDK en el pseudocódigo: `grep -niE "vercel|openai|anthropic|pi-ai|langchain" book/chapters/NN-*/chapter.md` vacío, salvo en prosa histórica justificada.
- Cada invariante nueva que el capítulo introduce tiene al menos un test en la sección 16.
- El diagrama Archify está validado.

---

## 9. Cierre de cada release (tras CH-36 y tras CH-47)

1. `book/chapters/25-epilogo-secuenciacion/chapter.md`:
   - agregar los tramos nuevos al orden y a la verificación de P-09;
   - corregir la inconsistencia `next_chapter: CH-26` (frontmatter) frente a §19 ("el último").
2. `diagrams/archify/nucleo-del-arnes.json` y `capa-enterprise.json`: los componentes nuevos. Opcional: un diagrama nuevo `capa-conectividad` en v0.3.
3. `kb/Index.md`: conteos (componentes, contratos, capítulos, términos).
4. `book/book.yaml`: `version` según T0.6.
5. `node scripts/build-all` completo → exit 0 → tag `v0.2` / `v0.3` → aprobación humana del release.
6. Opcional en `arnes-ai`: marcar `docs/propuestas/book-harness/BH-Propuestas.md` como "aplicado en vX", y un estudio visual con el skill `estudio-visual`.

---

## 10. Riesgos y decisiones pendientes

- **Validadores sin historia de versiones:** hay una sola `current_definition` por contrato, y en 35 contratos `modified_by` siempre ha estado vacío. T0.2 es obligatorio y puede requerir un plan de tooling previo.
- **Escala:** 20 capítulos casi duplican el libro. v0.2 es autosuficiente, y v0.3 puede publicarse más tarde como "Parte III".
- **Copiar plataformas:** en cada Brief, verificar que el capítulo enseña un contrato o principio y no el producto de eve o pi (P-27, EVO-01).
- **Protocolos reales (MCP, A2A):** el libro modela contratos y adaptadores, no la especificación del protocolo. Cada capítulo cita la especificación como adaptador y no la reproduce.
- **Pendiente de decidir (T0.6):**
  - (1) la versión del libro;
  - (2) si CH-46 (el agente como directorio) va en v0.3 o como apéndice;
  - (3) los nombres de los tramos en CH-25.

---

## 11. Registro de ejecución

*(Vacío. Cada incremento anota aquí fecha, rama, commit, resultado de `build-all`, paquetes LaTeX que agregó y deuda.)*

| Incremento | Fecha | Commit | build-all | Notas |
| --- | --- | --- | --- | --- |
| Línea base | 2026-09-24 | `d16e2c7` | ✅ exit 0 (29 warnings, T0.1) | Entorno: Graphviz 16.1, pandoc 3.11, TinyTeX 2026 + `caption`, gs 10.07 |
| T0.1 | 2026-09-24 | `a572e44` | ✅ exit 0, 0 warnings | `markdownImagePath()` en `scripts/build-pdf` normaliza a `/` las rutas de los mapas mentales; `dist/book.pdf` pasa de 2,2 MB a 4,0 MB (ahora incluye los 29 mapas) |
| T0.2 | 2026-09-24 | rama `spike/contract-v2` (descartada, no mergeada) | ✅ exit 0, 0 warnings | Con C-004 en `v2` (con `caller: Optional<CallerSnapshot>`, tipo aún inexistente), `modified_by: [CH-27]` y `modifies_contracts: [C-004]` en CH-27: (a) ✅ `validate-chapter` acepta `modifies_contracts`; (b) ✅ `validate-contracts` acepta `v2` + `modified_by`; (c) ✅ **CH-00..CH-27 siguen en verde**. `build-mind-map` dibuja la arista `CH-27 → C-004 [MODIFIES]`. **Hallazgo:** ningún validador revisa los tipos dentro de `current_definition` (se aceptó `CallerSnapshot` sin definir). No bloquea: el capítulo que modifica el contrato define el tipo en su propio pseudocódigo, que sí se valida. Mejora opcional de tooling: que `validate-contracts` verifique los tipos de `current_definition` contra los contratos introducidos hasta el último capítulo de `modified_by` |
| T0.3 | 2026-09-24 | `7497ad7` | — | `docs/adr/ADR-001..005` en estado `Proposed`, con las 9 secciones del formato de la constitución (`:867-884`) |
| T0.4 | 2026-09-25 | `Ratificar Amendment v1.2` | ✅ exit 0, 0 warnings | Aprobado tal cual por el autor. P-31..P-39 e INV-E15..E27 en la constitución (`:1002`) y en `kb/01-Constitucion/Amendment-v12.md`. Desbloquea CH-30+ |
| T0.6 | 2026-09-25 | — | — | ✅ Decisiones del autor: (1) **versión** 0.2 y luego 0.3: CH-28..CH-36 con `starting_version: "0.1"`, `ending_version: "0.2"`; CH-37..CH-47 con `"0.2"` → `"0.3"`; `book.yaml` sube al cerrar cada release. (2) **CH-46 es un capítulo** en v0.3. (3) Los nombres de los tramos en CH-25 se fijan al cerrar v0.2 |
| CH-28 | 2026-09-25 | rama `cap-28-steering-follow-up` → `main` | ✅ exit 0, 0 fetch warnings | C-036 `PendingInput`; 0 componentes (amplía AgentLoop dentro de su owns); `runTurn` sin cambios. Plan: `planes/2026-09-25-capitulo-28-steering-follow-up.md` |
| T0.7 (propuesta) | 2026-09-25 | — | — | **Hallazgo preexistente:** el PDF emite `[WARNING] Missing character` por los glifos de dibujo de cajas (`─ │ ├ └ ▼`) de los diagramas de texto: 1733 en `main` antes de CH-28 y 1768 después (+35 del §10 de CH-28, mismo patrón que todos los capítulos). La fuente monoespaciada por defecto no los trae. Propuesta de tooling: `-V monofont="Consolas"` (o DejaVu Sans Mono) en `scripts/build-pdf`. Pendiente de aprobación |
