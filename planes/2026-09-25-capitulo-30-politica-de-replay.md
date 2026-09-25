# Plan / Registro de ejecución — Capítulo 30: Cuando No se Sabe si Ocurrió: Política de Replay

**Fecha:** 2026-09-25
**Estado:** ✅ Completado (2026-09-25). Rama `cap-30-politica-de-replay` mergeada a `main`, sobre `7943ac0`.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-30 (§6).
- `2026-09-17-capitulo-17-idempotency-guard.md`: `IdempotencyGuard` (CMP-015), `IdempotencyRecord` (C-027, PENDING / COMPLETED), `checkIdempotency`, `recordIdempotentExecution`.
- `2026-09-14-capitulo-08-capability-registry.md`: `CapabilityDescriptor` (C-018).
- `2026-09-13-capitulo-02-tool-runtime.md`: `ToolResult` (C-009).
- `docs/adr/ADR-002-replay-policy-en-capability.md`: **Accepted** (2026-09-25).
- Amendment v1.2: **INV-E17** ("An effect whose outcome is unknown is re-executed only if its capability declares replayPolicy = SAFE").

## 1. Objetivo

Tercer capítulo del Tramo 4. Hace que cada capability **declare** qué hacer si no se sabe si su efecto ocurrió (`NEVER` / `SAFE`), y que el resultado desconocido llegue al modelo como **observación explícita** (INV-07), nunca como éxito ni como fallo inventados.

## 2. Alcance decidido

**0 componentes + 1 contrato + 2 contratos modificados:**
1. **C-039 `ReplayPolicy`** (ENUM `NEVER` / `SAFE`).
2. **C-018 `CapabilityDescriptor` v2:** `replayPolicy: Optional<ReplayPolicy>`. `NULL` equivale a `NEVER` mediante `effectiveReplayPolicy`.
3. **C-009 `ToolResult` v2:** `outcome: Optional<ToolOutcome>`. `NULL` se deriva de `succeeded`, como en v1.
4. **Embebidos:** `ENUM ToolOutcome` (SUCCEEDED / FAILED / UNKNOWN), `ENUM UnknownOutcomeAction` (WAIT / REEXECUTE / REPORT_UNKNOWN) y `STRUCT UnknownOutcomeDecision`.
5. **`IdempotencyGuard` (CMP-015)** se amplía dentro de su `owns` ("decidir si una ejecución repetida debe reusar el ToolResult ya conocido en vez de que el side effect real vuelva a ejecutarse"). Funciones nuevas: `effectiveReplayPolicy`, `decideUnknownOutcome`, `buildUnknownOutcomeResult`.
6. **`CapabilityRegistry` (CMP-008)** solo **registra** la política dentro del descriptor. No decide nada nuevo.

## 3. Decisiones de diseño centrales

- **Un resultado desconocido es un `PENDING` huérfano:** un `IdempotencyRecord` en `PENDING` cuya ejecución ya no está en curso (`executionStillInFlight = FALSE`, una señal de entrada asumida). Mientras la ejecución siga en curso, vale la semántica de CH-17 (`WAIT`).
- **`NEVER` por defecto.** Un descriptor sin política no se re-ejecuta. Es conservador, pero nunca duplica un efecto.
- **`REPORT_UNKNOWN` no es un error del run.** Es una observación que el modelo recibe, con un `HarnessError` de categoría `IDEMPOTENCY` y el mensaje "el resultado externo es desconocido". El modelo decide qué proponer después (por ejemplo, consultar el estado). El arnés nunca asume que el efecto ocurrió.
- **La detección durante una recuperación real** (tras un crash) es de `ExecutionJournal` (CH-32). CH-30 fija la **regla**; CH-32 fija **cuándo** se invoca.

## 4. Archivos creados

- `book/chapters/30-politica-de-replay/chapter.md` (secciones 0–21, 10 bloques)
- `kb/04-Capitulos/ch-30-politica-de-replay.md`, `kb/03-Contratos/C-039-replaypolicy.md`
- `diagrams/archify/capitulo-30-politica-de-replay.json` + `rendered/…html`; `diagrams/mindmap/chapter-30.diagram`

## 5. Archivos modificados

- `registry/contracts.yaml`: C-009 **v1 → v2** (`outcome`), C-018 **v1 → v2** (`replayPolicy`), C-039
- `registry/glossary.yaml`: Unknown Outcome, ReplayPolicy
- `docs/adr/ADR-002-…md`: **Accepted** (2026-09-25), con las decisiones Optional/NULL y la definición de resultado desconocido
- `book/book.yaml`; CH-29 `next_chapter: CH-30`
- KB: C-009 y C-018 (v2), índices, glosario, navegación de CH-29

## 6. Resultado real del pipeline

- **Rojo:** 22 errores, incluidos los dos `modified_by` faltantes (C-018, C-009).
- **Registro:** 39 contratos / 22 componentes OK.
- **Verde:** `validate-chapter` OK (22 secciones, 10 bloques); `validate-retrieval-set` OK (4/4/2/1/3/4).
- **`build-all` exit 0 con 31/31 capítulos** en verde tras modificar **dos** contratos a la vez. El mapa mental dibuja `CH-30 → C-018` y `CH-30 → C-009 [MODIFIES]`.
- 0 `Could not fetch`; `Missing character` se mantiene en 6 (los de CH-10).
- **Archify:** showcase 9/9, 0/0; spec `56893161…`; visual-check pass; revisado a 1440×900.

## 7. Definition of Done

- [x] Validadores de CH-30 en verde; C-018 y C-009 en v2 con `modified_by: [CH-30]`.
- [x] 31/31 capítulos en verde.
- [x] `build-all` exit 0.
- [x] Archify `capitulo-30-politica-de-replay` validado.
- [x] KB y glosario; `next_chapter` de CH-29 = CH-30; ADR-002 Accepted.

## 8. Deuda

- Detectar el corte de verdad (`executionStillInFlight` es una señal asumida): CH-32.
- Cableado en la recuperación (CH-32) y en el turno completo (CH-36).
- Consultar el estado del efecto externo para salir del "no se sabe": es una capability más, no modelada.
- Auditoría de las capabilities marcadas `SAFE` (CH-19): recomendación sin mecanismo.
- CH-31 hereda: sin identidad del llamante no hay credenciales por usuario ni aprobadores verificables.
