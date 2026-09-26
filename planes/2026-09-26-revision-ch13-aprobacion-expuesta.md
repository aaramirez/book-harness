# Plan / Registro de ejecución — Revisión de CH-13: exponer la solicitud y el punto de ejecución de una aprobación

**Fecha:** 2026-09-26
**Estado:** ✅ Completado (2026-09-26). Rama `rev-ch13-aprobacion-expuesta` mergeada a `main`, sobre `b6c2d1d`.
**Deuda:** D-014 (`registry/debt.yaml`), paso 2 de v0.2.1 (`2026-09-26-cierre-release-v0-2.md` §3).
**Decisión del autor:** "Revisar CH-13" (2026-09-26), sin cambiar firmas publicadas.

## 1. Problema

CH-36 encontró dos funciones de CH-13 que no se podían envolver con el journal:
- `beginToolApprovalPause` crea la `HumanInteractionRequest` pero no la devuelve, y `parkRun` (CH-33) necesita su id;
- `resumeAfterHumanResolution` resuelve, ejecuta la tool y continúa el turno en una sola llamada, sin un punto entre resolver y ejecutar donde el journal registre la tool call antes y el resultado después.

CH-36 las rearmaba con `createHumanInteractionRequest`, `createOrUpdateSessionCheckpoint` y `resolveHumanInteractionRequest`.

## 2. Cambio

**CH-13 (`book/chapters/13-integracion-caminos-de-gobierno/chapter.md`):**
- **§6:** dos tipos embebidos, `ApprovalPause` (pausedState, request) y `ApprovalResume` (resumedState, resolution).
- **§11:** nota de revisión y tres funciones nuevas.
  - `beginToolApprovalPauseForDecision(turnState, execution, decision, session, subs) -> ApprovalPause`: el cuerpo anterior de `beginToolApprovalPause`, a partir de la `PolicyDecision` ya evaluada.
  - `resolveApprovalForResume(...) -> ApprovalResume`: resuelve y construye el estado RUNNING; no ejecuta.
  - `observationForApproval(resolution, result?) -> AgentMessage`: TOOL con el `ToolResult`, o el rechazo `HUMAN_APPROVAL_REJECTED` (mismo mensaje que antes). Lanza `APPROVED_WITHOUT_TOOL_RESULT` si se aprobó y no hay resultado.
  - **`beginToolApprovalPause` y `resumeAfterHumanResolution` conservan firma y comportamiento:**
    - la primera evalúa la política y llama a `beginToolApprovalPauseForDecision`;
    - la segunda llama a `resolveApprovalForResume`, luego `executeToolCall` si se aprobó, luego `observationForApproval` y `resumeTurnWithObservation`.
- **§16:** cinco tests nuevos, dos de ellos de equivalencia con el comportamiento anterior.

**CH-36:**
- `runDurableGovernedStep` (REQUIRE_APPROVAL) invoca `beginToolApprovalPauseForDecision`, y deja de llamar a `createHumanInteractionRequest`, `createOrUpdateSessionCheckpoint` y `parkedAgentState`.
- `resumeDurableApproval` invoca `resolveApprovalForResume` y `observationForApproval`, y registra la tool call y su resultado entre ambas.
- §3, §5, §9, §10, §14 (orden de eventos: el checkpoint ahora precede a `RUN_PARKED`), §16, §18, §20, §21 y el retrieval set (`RQ-CH36-04`, `iceberg_patterns`, `leverage_point`) pasan de "componer en vez de invocar" a "CH-13 revisado expone lo necesario".

**CH-33:** sin cambios. `resumeToolApprovalWait` sigue invocando `resumeAfterHumanResolution`, cuya firma y comportamiento no cambiaron.

**Otros:** la tarjeta "Hallazgo" del Archify `capitulo-36` pasó a "CH-13 revisado en v0.2.1 (D-014)"; se actualizaron la nota de KB de CH-36 y la deuda D-014 (`resolved`, `resolved_in: CH-36`).

## 3. Resultado real

- `validate-chapter` / `validate-retrieval-set` OK para CH-13 (10 bloques de pseudocódigo) y CH-36.
- `validate-debt`: 25 open, 10 resolved, 5 out_of_scope; quedan 13 → `v0.2.1`.
- Archify `capitulo-36`: showcase 9/9, 0/0; spec `9cc5db3a6349`; visual-check pass; revisado a 1440×900.
- `build-all`: el primer intento falló en `build-pdf` con ``File `soul.sty' not found``, porque pandoc lo requiere para el tachado `~~…~~` de CH-36 §18. Se instaló con `tlmgr install soul` (§2 del plan maestro). Con eso, **exit 0**: 37/37 capítulos, `Missing character` en 6, 0 `Could not fetch`.
- **Hallazgo de entorno, preexistente y no bloqueante:** la copia `%USERPROFILE%\bin\gs.exe` no encuentra `gs_init.ps`, así que `render-diagram` no normaliza los PDF de los mapas mentales y conserva los de `dot -Tpdf` (76 avisos, ya presentes en los builds anteriores). No afecta al libro; se corrige apuntando `gs` al Ghostscript de TinyTeX con su `GS_LIB`.
