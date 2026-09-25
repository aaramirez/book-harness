# Plan / Registro de ejecución — Capítulo 29: Compactar sin Perder el Hilo: Resúmenes Estructurados y Sesiones en Árbol

**Fecha:** 2026-09-25
**Estado:** ✅ Completado (2026-09-25). Rama `cap-29-compactacion-sesiones-arbol` mergeada a `main`, sobre `846f347`.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-29 (§6) y procedimiento (§8).
- `2026-09-13-capitulo-04-context-engine.md`: `ContextEngine` (CMP-004), `assembleContextSnapshot`, `ContextBlock`, y la decisión de CH-04 de **no** crear un componente `Compactor`/`Summarizer`, porque ContextEngine posee la compactación.
- `2026-09-14-capitulo-10-session-manager.md`: `SessionManager` (CMP-010), `SessionState` (C-020), `SessionCheckpoint` y `branchSessionFromCheckpoint` (la rama como sesión nueva).
- `2026-09-25-capitulo-28-steering-follow-up.md`: su deuda. El steering y el follow-up hacen crecer el historial.
- `docs/adr/ADR-003-sesion-en-arbol-y-version-de-runtime.md`: **Accepted, parte v2** (2026-09-25).

---

## 1. Objetivo

Segundo capítulo del Tramo 4.
- **ContextEngine:** compactar el **historial** de un run, no solo candidato por candidato como en CH-04, en dos fases:
  1. recortar sin modelo los resultados de tools demasiado grandes;
  2. resumir con el modelo la región antigua en un resumen **estructurado**.

  El punto de corte nunca separa una tool call de su resultado (INV-07).
- **SessionManager:** navegar dentro de una sesión hacia un checkpoint anterior **sin borrar** la rama abandonada, dejando un resumen de lo que se abandonó.

## 2. Alcance decidido

**0 componentes + 2 contratos + 1 contrato modificado:**
1. **C-037 `CompactionSummary`:** goal, constraints, progress, decisions, nextSteps, criticalContext, touchedFiles, firstKeptMessageId, provenance.
2. **C-038 `BranchSummary`:** abandonedTipId, resumedFromId, summary: CompactionSummary, createdAt.
3. **C-020 `SessionState` v2:** agrega `activeCheckpointId: Optional<SessionCheckpointId>` y `branchSummaries: List<BranchSummary>` (ADR-003 v2).
4. **Embebidos:**
   - `CompactionPolicy` (reserveTokens, keepRecentTokens, maxToolResultChars);
   - `CompactionPlan` (cutIndex, olderRegion, recentRegion, needsSummary).
5. **ContextEngine (CMP-004) se amplía dentro de su `owns` literal** ("compaction, context budgets, provenance"):
   - `shouldCompactHistory`
   - `findSafeCutIndex`
   - `trimOversizedToolResults`
   - `planHistoryCompaction`
   - `applyHistoryCompaction`: valida la propuesta de resumen del modelo.
6. **SessionManager (CMP-010) se amplía dentro de su `owns` literal** ("branching, checkpoints, reconstruction"):
   - `navigateToCheckpoint`
   - `resolveResumeCheckpoint`: `activeCheckpointId` o, si falta, `latestCheckpoint`.

## 3. Decisiones de diseño centrales

- **El modelo propone el resumen; ContextEngine decide.** Resumir es agéntico (Article XII); dónde cortar, qué conservar literal y si el resumen es válido es determinístico. ContextEngine nunca invoca al modelo: la propuesta llega desde la integración, que llama a ModelGateway (CH-03). Esto preserva P-02.
- **Recortar antes de resumir:** la fase 1 no usa el modelo y muchas veces basta.
- **Corte seguro:** si el índice de corte cae en un mensaje `TOOL`, retrocede hasta incluir la tool call que lo originó.
- **Navegar no borra:** `latestCheckpoint` queda intacto; `activeCheckpointId` indica desde dónde continúa el próximo turno.
- **La rama en CH-10 es una sesión nueva** (`branchSessionFromCheckpoint`), y se conserva. CH-29 agrega la navegación **dentro** de una sesión, que es otra operación.
- **EVO-09** ("context has provenance") se cita en prosa, no en el frontmatter: el validador solo reconoce P-xx / INV-xx.

## 4. Archivos creados

- `book/chapters/29-compactacion-sesiones-arbol/chapter.md` (secciones 0–21, 12 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-29-compactacion-sesiones-arbol.md`, `kb/03-Contratos/C-037-compactionsummary.md`, `kb/03-Contratos/C-038-branchsummary.md`
- `diagrams/archify/capitulo-29-compactacion-sesiones-arbol.json` + `rendered/…html`
- `diagrams/mindmap/chapter-29.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/contracts.yaml`: C-020 **v1 → v2** (`modified_by: [CH-29]`), C-037, C-038
- `registry/glossary.yaml`: History Compaction, Safe Cut Point, Branch Navigation, CompactionSummary, BranchSummary
- `docs/adr/ADR-003-…md`: **Accepted, parte v2**, con el ajuste `branchSummaries`
- `book/book.yaml` (CH-29); CH-28 `next_chapter: CH-29`
- KB: `C-020-sessionstate.md` (v2), índices de capítulos y contratos, glosario, navegación de CH-28
- `diagrams/mindmap/full-book.diagram` (regenerado, con la arista `CH-29 → C-020 [MODIFIES]`)

## 6. Resultado real del pipeline

- **Rojo:** 22 errores, incluido "registry/contracts.yaml para C-020 no incluye CH-29 en modified_by".
- **Registro:** `validate-contracts` OK (38), `validate-components` OK (22).
- **Verde:** `validate-chapter` OK (22 secciones, 12 bloques, 2 contratos); `validate-retrieval-set` OK (4/4/2/1/3/4).
- **Primera modificación real de un contrato:** `build-all` exit 0 con **30/30 capítulos** y **30/30 retrieval sets** en verde, es decir, CH-00..CH-28 no se rompieron con C-020 v2. `build-mind-map` dibuja `CH-29 → C-020 [MODIFIES]`.
- `dist/book.pdf` 4,37 MB; 0 `Could not fetch`; `Missing character` se mantiene en 6 (los de CH-10, T0.7).
- **Archify:** showcase 9/9, 0/0; spec `63eb3ec3…`; visual-check pass; publicado en `dist/web/diagramas/`.
- **Ajuste de diseño en el pseudocódigo:** `findSafeCutIndex` usa una bandera `stillFits` en vez de `BREAK`, que no está en la gramática canónica (`skills/write-pseudocode`).

## 7. Definition of Done

- [x] `validate-chapter` / `validate-retrieval-set` de CH-29 en verde.
- [x] `validate-contracts` (38) y `validate-components` (22) en verde; C-020 en `v2` con `modified_by: [CH-29]`.
- [x] CH-00..CH-28 siguen en verde (primera modificación real de un contrato en el libro).
- [x] `build-all` exit 0, sin warnings nuevos de `Could not fetch`.
- [x] Archify `capitulo-29-compactacion-sesiones-arbol` validado.
- [x] KB: capítulo, C-037, C-038, C-020 actualizado, índices y glosario.
- [x] `next_chapter` de CH-28 = CH-29.

## 8. Deuda intencional

- Cableado en la integración (CH-36).
- Provenance del bloque del resumen en `assembleContextSnapshot`, que sigue etiquetando `"conversation_history"` (CH-40).
- Etiqueta de gobierno del dato para el resumen (CH-20 / CH-40).
- Recuperación a mitad de la compactación (CH-32).
- `runtimeVersion` en la sesión (ADR-003 v3, CH-43).
- CH-30 hereda: un efecto cuyo resultado se desconoce no puede "volver a pedirse" sin política de replay.
