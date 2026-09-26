# Plan / Registro de ejecución — Capítulo 36: Integración: el Turno Durable Gobernado

**Fecha:** 2026-09-26
**Estado:** ✅ Completado (2026-09-26). Rama `cap-36-integracion-turno-durable` mergeada a `main`, sobre `35b3e9e`.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-36 (§6) y cierre de release (§9).
- `2026-09-18-capitulo-26-*.md` y `2026-09-18-capitulo-27-*.md`: patrón de capítulo de integración (sin componentes ni contratos; tabla de tipos heredados).
- `2026-09-14-capitulo-13-integracion-caminos-de-gobierno.md`: caminos DENY / REQUIRE_APPROVAL / reanudación, `resumeTurnWithObservation`.
- Los planes de CH-30..CH-35 y sus secciones "Deuda".

## 1. Objetivo

Último capítulo de v0.2. Cablear en un solo turno lo que CH-28..CH-35 dejaron "para la integración": admisión con `Principal` → continuación o activación → pasos con journal → espera estacionada y reanudación → código del modelo en el entorno aislado → recuperación tras una caída.

## 2. Alcance decidido

**0 componentes + 0 contratos + 0 contratos modificados.** Cinco funciones de integración y un tipo embebido:
1. `enterDurableTurn`: `admitWithVerifiedIdentity` (CH-31) → `routeAdmittedRequest` (CH-34) → `continuationAllowedForCaller` (CH-31) si continúa.
2. `runDurableGovernedStep`: `beginStep` / `recordModelResponse` (CH-32) → `invokeModelForTurn` (CH-03) → `resolveModelProposedToolCall` (CH-08) → `evaluatePolicyForToolCall` (CH-05) →
   - `DENY`: compromete el paso sin tool call;
   - `REQUIRE_APPROVAL`: `createHumanInteractionRequest` (CH-06) → `parkRun` / `linkRequestToWait` / `parkedAgentState` (CH-33) → checkpoint (CH-10);
   - `ALLOW`: `recordToolCallBeforeExecution` → `executeToolCallIsolated` (CH-35) → `recordToolResult` → `commitStep`.
3. `resumeDurableApproval`: `acceptDelivery` (CH-33) → `resolveHumanInteractionRequest` (CH-06) → ejecución registrada (CH-32/CH-35) → `resumeTurnWithObservation` (CH-13).
4. `resolvePendingStepOnRecovery`: `decideUnknownOutcome` (CH-30, con `executionStillInFlight = FALSE`) → `executeToolCallIsolated` o `buildUnknownOutcomeResult` → `commitStep`.
5. `bindDurableCaller`: `buildCallerSnapshot` + `bindCallerToExecution` (CH-31).
6. **Embebido:** `STRUCT DurableStepOutcome` (step, state, wait?, request?).

## 3. Decisiones de diseño centrales

- **Hallazgo: `beginToolApprovalPause` y `resumeAfterHumanResolution` (CH-13) no se pueden envolver con el journal.** La primera no devuelve la `HumanInteractionRequest` que crea (hace falta su id para `parkRun`); la segunda ejecuta la tool y continúa el turno en una sola llamada sin exponer el `ToolResult` (hace falta para `recordToolResult` y el write-ahead). El turno durable **compone sus mismas piezas** (CH-06, CH-10, CH-13 `resumeTurnWithObservation`) en vez de invocarlas. `resumeToolApprovalWait` (CH-33) sigue siendo el camino no durable. Se documenta en §9 y §18.
- **El paso estacionado queda `STARTED` sin tool call.** Nada se ejecutó; al reanudar, la tool call se registra antes de ejecutar. Un run estacionado no se "recupera": la recuperación es para runs interrumpidos, no para runs que esperan.
- **La aprobación no cambia el llamante.** Quien aprueba queda como `resolvedBy`; la acción sigue ejecutándose en nombre de `caller.current` (quien pidió).
- **Continuar sin permiso es un error sin evento,** igual que un rechazo de admisión: todavía no hay run cargado.
- **CH-28 (steering) y CH-29 (compactación) no se cablean aquí:** actúan dentro del ciclo de `AgentLoop` / `ContextEngine` entre pasos; el turno durable los atraviesa sin cambiarlos. Se declara en §18.

## 4. Archivos creados

- `book/chapters/36-integracion-turno-durable/chapter.md` (secciones 0–21, 6 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-36-integracion-turno-durable.md`
- `diagrams/archify/capitulo-36-integracion-turno-durable.json` + `rendered/…html`; `diagrams/mindmap/chapter-36.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/glossary.yaml`: Durable Governed Turn (componentes y contratos sin cambios: 26 / 48)
- `book/book.yaml`; CH-35 `next_chapter: CH-36`
- KB: índice de capítulos, glosario, navegación de CH-35

## 6. Resultado real del pipeline

- **Rojo:** 19 errores con solo el frontmatter.
- **Verde, tras dos correcciones:**
  - `validate-chapter` exigía que §13 nombre `HarnessError` / `ErrorCategory`;
  - `validate-retrieval-set` no aceptó "seguir" como verbo de capacidad; pasó a "explicar".
  - Resultado: `validate-chapter` OK (22 secciones, 6 bloques); `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **Error de diseño corregido antes del build:** `resolvePendingStepOnRecovery` llamaba a `buildUnknownOutcomeResult` antes del `IF`, pero esa función (CH-30) lanza `NOT_A_REPORT_UNKNOWN_DECISION` si la decisión es `REEXECUTE`. Quedó como `IF REEXECUTE … ELSE buildUnknownOutcomeResult`.
- **Glifo:** `✗` en §10 se reemplazó por texto, para no sumar avisos de fuente en el PDF.
- **`build-all` exit 0 con 37/37 capítulos y 37/37 retrieval sets.** `dist/book.pdf` 5,3 MB; 0 `Could not fetch`; `Missing character` se mantiene en 6 (los de CH-10).
- **Archify:** showcase 9/9, 0/0; spec `a203928cf100…`; visual-check pass (claro y oscuro); revisado a 1440×900. Cinco participantes (modelo, política, capability, entorno y HumanInteractionService solo en notas); la etiqueta del tercer segmento se acortó a "Recuperar" para no chocar con el mensaje de la caída.

## 7. Definition of Done

- [x] Validadores de CH-36 en verde; registro sin cambios salvo el glosario.
- [x] 37/37 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-35 `next_chapter` = CH-36.
- [x] Tests §16 que recorren los caminos de punta a punta (16 tests, incluido `CrashDuringApprovedExecutionIsResolvedOnRecovery`).

## 8. Deuda (entra al cierre de v0.2 o a v0.3)

- Revisar CH-13 para que `beginToolApprovalPause` devuelva su solicitud y `resumeAfterHumanResolution` exponga el `ToolResult`; así se invocarían en vez de componerse. No se hizo para no reabrir pseudocódigo publicado.
- `PendingInput` (CH-28) durable entre pasos.
- Reanudación durable de preguntas, autorizaciones y límites de presupuesto (mismo patrón que `resumeDurableApproval`).
- Liberar la dirección de continuación y responder por el canal (CH-34).
- Vencimiento activo de esperas con un schedule interno.
- Detección de la credencial faltante que abre un `AuthorizationChallenge` (CH-33).
- Routing (Preview).
