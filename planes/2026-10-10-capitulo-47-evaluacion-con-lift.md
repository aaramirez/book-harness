# Plan / Registro de ejecución — Capítulo 47: Medir el Aporte de un Cambio: Evaluación con Lift

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `cap-47-evaluacion-con-lift` mergeada a `main`, sobre `d47857a`.
**Release:** v0.3. Sin deudas con destino CH-47.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-47 (§6).
- CH-22 (`EvaluationHarness`, `EvaluationReport`, `evaluateCandidateForPromotion`, `RiskClass`, `EvaluationOutcome`), CH-35 (`openSandboxSession`, `SandboxSession`).
- Constitución: P-28 (producción y evaluación son asuntos separados), P-29, INV-19 (toda decisión crítica se puede trazar), INV-E07 (aislamiento), INV-E13 (la promoción exige certificación según la clase de riesgo).

## 1. Objetivo

Que un cambio (un prompt, una política, un modelo, una skill) se pueda comparar contra la versión anterior en la misma métrica y los mismos casos, con cada corrida aislada, y que esa comparación sea la evidencia con la que `EvaluationHarness` decide si certifica.

## 2. Alcance decidido

**0 componentes + 1 contrato + 1 contrato modificado:**
1. **C-064 `LiftReport`:** reportId, baselineRef, treatmentRef, metric, scores, lift, minimumLift, verdict, isolationRef, producedAt.
2. **C-032 `EvaluationReport` v2:** `evidence: List<LiftReportId>` (vacía si falta).
3. **Embebidos:** `STRUCT CaseScore` (caseId, baselineScore, treatmentScore, baselineSandboxId, treatmentSandboxId), `ENUM LiftVerdict` (IMPROVED, INCONCLUSIVE, REGRESSED).
4. **Funciones (EvaluationHarness, CMP-020):** `requireIsolatedCase`, `computeLift`, `liftVerdict`, `certificationSignalFromLift`, `evaluateCandidateWithLift`.

## 3. Decisiones de diseño centrales

- **Lift pareado:** la misma métrica sobre los mismos casos, línea base contra tratamiento; el lift es la diferencia de medias.
- **Cada corrida en su propio entorno aislado:** dos corridas que comparten entorno se rechazan, porque una puede contaminar a la otra (CH-35, INV-E07).
- **Tres veredictos, no dos:** sin casos suficientes o con un lift dentro del umbral, el veredicto es INCONCLUSIVE, nunca "mejoró".
- **El lift alimenta la certificación de CH-22 sin reemplazarla:** una regresión rechaza, todo IMPROVED certifica, lo demás queda en NEEDS_REVIEW.
- **Sin componente nuevo:** evaluar candidatos antes de producción ya es de EvaluationHarness (P-28).

## 4. Archivos creados

- `book/chapters/47-evaluacion-con-lift/chapter.md` (secciones 0–21, 9 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-47-evaluacion-con-lift.md`, `kb/03-Contratos/C-064-liftreport.md`
- `diagrams/archify/capitulo-47-evaluacion-con-lift.json` + `rendered/…html`; `diagrams/mindmap/chapter-47.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/contracts.yaml`: C-032 v2, C-064
- `registry/glossary.yaml`: Lift, LiftReport
- `book/book.yaml`; CH-46 `next_chapter: CH-47`
- KB: C-032 a v2; índices de contratos y capítulos; glosario; navegación de CH-46

## 6. Resultado real del pipeline

- **Rojo:** 20 errores de capítulo con solo el frontmatter; sin deudas con destino CH-47.
- **Registro:** `validate-contracts` OK (64), `validate-components` OK (29), `validate-debt` OK.
- **Verde:** `validate-chapter` OK al primer intento (22 secciones, 9 bloques, 1 contrato, 0 componentes); `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **`build-all` exit 0 con 48/48 capítulos y 48/48 retrieval sets.** `dist/book.pdf` 6,9 MB; `Missing character` en 6.
- **Archify:** showcase 9/9, 0/0; `check` 9/9; visual-check pass, revisado a 1440×900 (claro y oscuro); 11 mensajes, 5 participantes.

## 7. Definition of Done

- [x] Validadores de CH-47 en verde; C-064 registrado; C-032 en v2 con `modified_by: [CH-47]`.
- [x] 48/48 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-46 `next_chapter` = CH-47.

## 8. Deuda

- Sin deuda nueva. Lo de §18 del capítulo se declaró explícitamente:
  - las pruebas estadísticas son otra forma de calcular el veredicto con la misma estructura: no es deuda;
  - cómo se puntúa un caso es del ejecutor de evaluaciones: no es deuda;
  - evaluar con tráfico real es despliegue, separado por P-28: no es deuda;
  - elegir y versionar los casos es un dato del equipo: no es deuda.
