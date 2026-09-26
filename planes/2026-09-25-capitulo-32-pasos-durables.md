# Plan / Registro de ejecución — Capítulo 32: Pasos Durables y la Recuperación a Mitad de Turno

**Fecha:** 2026-09-25
**Estado:** ✅ Completado (2026-09-25). Rama `cap-32-pasos-durables` mergeada a `main`, sobre `0d670bb`.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-32 (§6).
- `2026-09-25-capitulo-30-politica-de-replay.md`: `ReplayPolicy` (C-039), `decideUnknownOutcome` de IdempotencyGuard (CMP-015) y su deuda: "detectar el corte de verdad (`executionStillInFlight` es una señal asumida): CH-32".
- `2026-09-14-capitulo-10-session-manager.md`: `SessionManager` (CMP-010) y el checkpoint al final de fases, que **no** es un registro por paso.
- `2026-09-13-capitulo-03-model-gateway.md`: `ModelResponse` (C-007), con **una** `proposedToolCall` opcional por respuesta.
- Amendment v1.2: **P-32** (el paso es la unidad de durabilidad y recuperación), **INV-E16** (un paso comprometido nunca se re-ejecuta) e **INV-E17** (un efecto de resultado desconocido se re-ejecuta solo si su capability es `SAFE`).

## 1. Objetivo

Quinto capítulo del Tramo 4 y **primer componente nuevo** de v0.2. P-23 exige ejecución durable, pero el libro no tiene una unidad de recuperación más fina que el turno. Este capítulo:
1. descompone el turno en **pasos** (una llamada al modelo y la tool call que su respuesta propuso);
2. registra cada hecho del paso **antes** del efecto siguiente (*write-ahead*);
3. decide, al recuperar un run interrumpido, qué hacer con cada paso sin re-ejecutar nunca uno comprometido.

## 2. Alcance decidido

**1 componente + 2 contratos:**
1. **CMP-023 `ExecutionJournal`.** Justificación EVO-01/EVO-07: ni SessionManager (historia de la sesión, checkpoint por fase) ni IdempotencyGuard (dedup por clave y política de replay por efecto) poseen la decisión "¿este paso ya se comprometió y qué hago con él al recuperar?".
2. **C-042 `StepRecord`:** stepId, runId, turn, index, status, partialOutput?, modelResponse?, toolCall?, toolResult?, startedAt, committedAt?.
3. **C-043 `RecoveryDecision`:** runId, stepId, action, pendingToolCall?, decidedAt.
4. **Embebidos:** `ENUM StepStatus` (STARTED / COMMITTED) y `ENUM RecoveryAction` (REPLAY_RECORDED, COMMIT_RECORDED, CLOSE_WITH_PARTIAL, REEXECUTE_MODEL_CALL, RESUME_FROM_RESPONSE, RESOLVE_PENDING_TOOL).
5. **Funciones:** `beginStep`, `requireOpenStep`, `recordPartialOutput`, `recordModelResponse`, `recordToolCallBeforeExecution`, `recordToolResult`, `commitStep`, `decideStepRecovery`, `recoverRun`.

## 3. Decisiones de diseño centrales

- **Un paso tiene a lo sumo una tool call.** `ModelResponse` (C-007) propone una sola `proposedToolCall`. P-32 habla de "inline tool calls" en plural; el libro no inventa una lista que ningún contrato produce.
- **Write-ahead:** la tool call se registra **antes** de que ToolRuntime la ejecute. De ahí sale la distinción que hace segura la recuperación:
  - respuesta sin tool call registrada → ningún efecto empezó → `RESUME_FROM_RESPONSE` (se vuelve a gobernar la propuesta);
  - tool call sin resultado → el efecto pudo haber empezado → `RESOLVE_PENDING_TOOL`.
- **Frontera con IdempotencyGuard:** `RESOLVE_PENDING_TOOL` **no** decide si repetir el efecto. Entrega la tool call a `decideUnknownOutcome` (CH-30), que aplica INV-E17. Se ajusta así la ficha del plan maestro, que ponía `REEXECUTE / REPORT_OUTCOME_UNKNOWN` en ExecutionJournal: esa decisión ya es de CMP-015 desde CH-30.
- **Salida parcial (pi):** una llamada al modelo interrumpida con salida parcial ya persistida se cierra con esa salida (`CLOSE_WITH_PARTIAL`), sin volver a llamar al proveedor. Sin salida parcial, se repite la llamada (`REEXECUTE_MODEL_CALL`): llamar al modelo no tiene efectos visibles fuera del arnés (P-24 aplica a capabilities).
- **Commit fail-closed:** `commitStep` exige respuesta, resultado si hubo tool call, y la confirmación de persistencia (`resultPersisted`, señal de entrada asumida del almacenamiento).
- **Journal coherente:** a lo sumo un paso `STARTED`, y debe ser el último; si no, `JOURNAL_INCONSISTENT`.

## 4. Archivos creados

- `book/chapters/32-pasos-durables/chapter.md` (secciones 0–21, 14 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-32-pasos-durables.md`, `kb/02-Componentes/CMP-023-executionjournal.md`, `kb/03-Contratos/C-042-steprecord.md`, `kb/03-Contratos/C-043-recoverydecision.md`
- `diagrams/archify/capitulo-32-pasos-durables.json` + `rendered/…html`; `diagrams/mindmap/chapter-32.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/components.yaml`: CMP-023 (primer componente de v0.2)
- `registry/contracts.yaml`: C-042, C-043
- `registry/glossary.yaml`: Durable Step, Write-Ahead Step, StepRecord, RecoveryDecision
- `book/book.yaml`; CH-31 `next_chapter: CH-32`
- KB: índices de componentes, contratos y capítulos; glosario; navegación de CH-31

## 6. Resultado real del pipeline

- **Rojo:** 22 errores con solo el frontmatter.
- **Registro:** `validate-contracts` OK (43), `validate-components` OK (23).
- **Verde:** `validate-chapter` OK (22 secciones, 14 bloques, 2 contratos, 1 componente); `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **`build-all` exit 0 con 33/33 capítulos y 33/33 retrieval sets.**
- 0 `Could not fetch`. El primer build dio 7 `Missing character`: el nuevo era `▶` (U+25B6) en §17, que Consolas no tiene; se reemplazó por `→` y vuelve a 6 (los de CH-10).
- **Archify:** showcase 9/9, 0/0; spec `d67c2a6e…`; visual-check pass (claro y oscuro); revisado a 1440×900. Título corto ("Capítulo 32 — Pasos Durables", como CH-28..31) para no desbordar el alto; etiquetas de segmento y de `beginStep`/`recoverRun` acortadas, con el detalle en sus notas.
- **Ajuste de diseño frente a la ficha del plan maestro:** `REEXECUTE / REPORT_OUTCOME_UNKNOWN` por efecto ya es de IdempotencyGuard desde CH-30. ExecutionJournal lo **delega** con `RESOLVE_PENDING_TOOL` en vez de duplicarlo (Article IV). Se agregaron `COMMIT_RECORDED`, `CLOSE_WITH_PARTIAL` (pi), `REEXECUTE_MODEL_CALL` y `RESUME_FROM_RESPONSE`, que salen de la regla write-ahead.

## 7. Definition of Done

- [x] Validadores de CH-32 en verde; CMP-023, C-042, C-043 registrados.
- [x] 33/33 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB (capítulo, componente, contratos), glosario; CH-31 `next_chapter` = CH-32.
- [x] Tests §16 para INV-E16 (`CommittedStepIsReplayedNeverReexecuted`) e INV-E17 (`NeverPolicyPendingToolIsReportedUnknownNotReexecuted`).

## 8. Deuda

- Cableado de `beginStep … commitStep` y `recoverRun` en el turno completo: CH-36 (`runDurableGovernedTurn`).
- Un paso que espera una aprobación no debe retener el proceso: CH-33 (esperas durables).
- Varias tool calls por respuesta: `ModelResponse` v1 propone una; se modela si un capítulo futuro lo amplía (candidato: CH-37, catálogo de modelos).
- Retención y archivo del journal de runs terminados: gobierno del dato (CH-20), sin mecanismo.
- `sessionMayMigrate` (CH-43) debe leer los pasos sin comprometer (INV-E22).
