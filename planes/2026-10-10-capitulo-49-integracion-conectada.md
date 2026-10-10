# Plan / Registro de ejecución — Capítulo 49: Integración: el Arnés Conectado

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `cap-49-integracion-conectada` mergeada a `main`, sobre `f9035af`.
**Release:** v0.3 (último capítulo). Deudas con destino CH-49: D-041, D-042, D-044, D-045. Al cerrarlas, `registry/debt.yaml` queda sin deudas abiertas.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-49 (§6).
- CH-36 (`enterDurableTurn`, `runDurableGovernedStep`, `bindDurableCaller`), CH-37 (`detectMissingCallerCredential`, `parkForMissingCredential`, `OutboundMessage`), CH-38 (`admitWithPrincipalRules`, `evaluatePolicyForCaller`, `takePendingInputsForStep`, `confirmPendingInputsAfterCommit`, `resolveCallerCredentialReference`), CH-39 (`effectiveToolCallProposals`), CH-40 (`hooksFor`, `runBeforeToolHooks`, `ExtensionStatus.DISABLED`), CH-42 (`governRetrievedCandidate`, `selectRetrievedCandidates`), CH-44 (`invokeAgentDurably`), CH-46 (`contextCeilingForAudience`, `captureCeilingFor`, `fanOutSpan`), CH-48 (`requireActivatableManifest`).

## 1. Objetivo

Ver la versión 0.3 funcionar junta en un turno conectado, y cerrar las cuatro deudas que quedan: reescribir la entrada y el paso durables con las funciones de CH-37/CH-38 (D-041), avisar a un aprobador por otro canal (D-042), registrar varias tool calls de una respuesta sin volver a llamar al modelo (D-044) y correr extensiones PROJECT en el entorno aislado con apagado por comando operacional (D-045).

## 2. Alcance decidido

**0 componentes, 0 contratos.** Funciones de integración:
- `enterConnectedTurn` (D-041: CH-36 + `admitWithPrincipalRules` + `requireActivatableManifest`);
- `governedContextBlocks` (CH-42 + techo por audiencia de CH-46);
- `nextProposalFromJournal` (D-044);
- `requireExtensionPlacement`, `beforeToolHooksForStep`, `disableExtension` (D-045);
- `approverNoticeFor` (D-042);
- `credentialForConnectedCall` (CH-37 + CH-38);
- `runConnectedGovernedStep` (D-041: el paso de CH-36 con entradas pendientes, política por llamante, journal, aviso al aprobador y hooks);
- `traceConnectedStep` (CH-46);
- `openConnectedGovernedTurn`.

**Embebidos nuevos:** `STRUCT ConnectedStepOutcome`, `STRUCT ConnectedCredential`, `STRUCT ConnectedTurnStart`.

**Nombre:** el `runConnectedGovernedTurn` de la ficha se reparte en `openConnectedGovernedTurn` (entrada, llamante y contexto) y `runConnectedGovernedStep` (cada paso). El bucle de pasos sigue siendo de AgentLoop (CH-01), como en CH-36.

## 3. Decisiones de diseño centrales

- **El journal manda sobre el modelo:** si la respuesta registrada del turno todavía tiene propuestas sin ejecutar, el paso siguiente toma la próxima del journal y no llama al modelo (D-044).
- **Las entradas pendientes se aplican solo antes de una llamada al modelo** (CH-28, CH-38), nunca entre propuestas de una misma respuesta.
- **El aviso al aprobador es un `WAIT_NOTICE` a su dirección,** no a la de la sesión; la respuesta vuelve a la espera por su `waitId` y la regla de quien responde no cambia (D-042).
- **Una extensión PROJECT corre en el entorno aislado o no corre;** una apagada (`DISABLED`) no se selecciona (D-045).
- **Apagar una extensión es un comando operacional** (`DISABLE_CAPABILITY` con `targetRef` = la extensión, CH-18).
- **El orden del turno:** manifiesto → admisión → llamante → contexto con techo de audiencia → modelo o journal → política por llamante → aprobación → hooks → credencial → ejecución aislada → commit → trazas.

## 4. Archivos creados

- `book/chapters/49-integracion-conectada/chapter.md` (secciones 0–21, 14 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-49-integracion-conectada.md`
- `diagrams/archify/capitulo-49-integracion-conectada.json` + `rendered/…html`; `diagrams/mindmap/chapter-49.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/debt.yaml`: D-041, D-042, D-044, D-045 → `resolved` (CH-49); **0 deudas abiertas**
- `registry/glossary.yaml`: Connected Governed Turn
- `book/book.yaml`; CH-48 `next_chapter: CH-49`
- KB: índice de capítulos; glosario; navegación de CH-48

## 6. Resultado real del pipeline

- **Rojo:** 19 errores de capítulo con solo el frontmatter.
- **Registro:** `validate-debt` OK (48: 0 open, 42 resolved, 6 out_of_scope).
- **Verde:** `validate-chapter` OK (22 secciones, 14 bloques, 0 contratos, 0 componentes); `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **Revisión de lógica antes del commit:** la primera versión de `runConnectedGovernedStep` confirmaba un paso DENY sin registrar la tool call; `nextProposalFromJournal` no lo habría contado y habría vuelto a ofrecer la misma propuesta en cada paso. Corregido: una tool call denegada (`POLICY_DENIED`) o bloqueada por un hook se registra como fallida antes del commit.
- **`build-all` exit 0 con 50/50 capítulos y 50/50 retrieval sets.** `dist/book.pdf` 7,2 MB; `Missing character` en 6.
- **Archify:** showcase 9/9, 0/0; `check` 9/9; visual-check pass, revisado a 1440×900 (claro y oscuro); 11 mensajes, 5 participantes.

## 7. Definition of Done

- [x] Validadores de CH-49 en verde; D-041, D-042, D-044, D-045 resolved; `validate-debt` con 0 abiertas.
- [x] 50/50 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-48 `next_chapter` = CH-49.

## 8. Deuda

- Sin deuda nueva. Lo de §18 del capítulo se declaró explícitamente:
  - el bucle de pasos sigue siendo de AgentLoop (CH-01): no es deuda;
  - ejecutar propuestas en paralelo exigiría otro contrato de paso: no es deuda;
  - el directorio de direcciones de aprobadores es configuración del despliegue: no es deuda;
  - lo que viene después de v0.3 se planea en un plan maestro nuevo: no es deuda.
