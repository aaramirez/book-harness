# Plan / Registro de ejecución — Cierre de release v0.2

**Fecha:** 2026-09-26
**Estado:** ✅ Completado (2026-09-26). Rama `release-v0.2` mergeada a `main`, sobre `3bcceb5`; tag `v0.2`.
**Aprobación humana:** ✅ el autor aprobó el cierre y el tag `v0.2` el 2026-09-26 ("aprobado").

**Depende de:** `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md` §9 (cierre de cada release) y T0.6 (versión 0.2 y luego 0.3; nombres de los tramos al cerrar v0.2).

## 1. Qué incluye v0.2

- 9 capítulos: CH-28..CH-36 (Tramo 4 — Operación durable, Amendment v1.2).
- 4 componentes nuevos: CMP-023 ExecutionJournal, CMP-024 ResumptionCoordinator, CMP-025 ContinuationRegistry, CMP-026 IsolatedExecutionEnvironment.
- 13 contratos nuevos (C-036..C-048) y 8 modificaciones de contrato: C-020, C-018, C-009, C-004, C-023, C-015, C-022 → v2.
- ADR-001, ADR-002 y ADR-003 (parte v2) Accepted.
- Totales: 26 componentes, 48 contratos, 37 capítulos, 165 términos.

## 2. Pasos del cierre (§9 del plan maestro)

1. **CH-25 (epílogo):** se agregan notas "Actualización (cierre de v0.2)" en §1 (tramos nuevos), §10 (secuencia), §17 (conteos y cobertura de v1.2) y §19 (deja de ser el último capítulo). El texto original se conserva como registro de la versión 0.1. `next_chapter: CH-26` ya era correcto; lo desactualizado era la prosa de §19.
2. **Diagramas generales:** `nucleo-del-arnes` y `capa-enterprise` suman CMP-023..026; se diagnostica el FAIL de `archify-check`.
3. **KB:** `kb/Index.md`, `kb/00-Inicio/El-Libro.md` e índices de componentes, contratos y capítulos pasan a 26 / 48 / 37 / 165 y versión 0.2.
4. **`book/book.yaml`:** `version: "0.2"`.
5. `build-all` → exit 0 → tag `v0.2` → push.

**Nombres de los tramos (T0.6):** "Tramo 3 (cierre) — Integración enterprise" para CH-26..CH-27 (en la KB, "Enterprise II"), y "Tramo 4 — Operación durable" para CH-28..CH-36, el nombre que ya usaban los capítulos.

## 3. Decisiones del autor sobre la deuda (2026-09-26)

Inventario: 35 puntos en las secciones "Deuda" de los planes de CH-28..CH-36.
- **9 sin dueño**: prometidos "en CH-36" y no resueltos, más la revisión de CH-13.
- **9 con capítulo de v0.3** asignado.
- **5 fuera de alcance o Preview.**

| Pregunta | Decisión |
|---|---|
| ¿Cuándo? | **Tag v0.2 ahora; la deuda sin dueño se resuelve en v0.2.1, antes de CH-37** |
| ¿Dónde? | **Capítulos nuevos de integración antes de v0.3**; los capítulos de v0.3 se renumeran |
| ¿Registro? | **Sí, verificable**: `registry/debt.yaml` más un validador en `build-all` (con plan de tooling propio, regla 5) |
| ¿CH-13? | **Revisar CH-13**: `beginToolApprovalPause` devuelve la solicitud y `resumeAfterHumanResolution` expone el `ToolResult`; se ajustan CH-13, CH-33 y CH-36 |

Orden de v0.2.1:
1. plan de tooling y `registry/debt.yaml` con su validador;
2. revisión de CH-13;
3. capítulos de integración nuevos;
4. renumeración de v0.3 en el plan maestro;
5. tag `v0.2.1`.

## 4. Resultado real

- `build-all` exit 0: 37/37 capítulos y 37/37 retrieval sets; `dist/book.pdf` 5,3 MB; 0 `Could not fetch`; `Missing character` en 6 (los de CH-10).
- **Diagramas generales:**
  - **Causa del FAIL:** no era un error de los JSON. Los dos diagramas declaran `meta.repository` y rutas `sources`, y archify exige `--repo-root` para verificar esa evidencia. Con `archify-check.js diagrams/archify --repo-root .` pasan **42/42**.
  - **`capa-enterprise`:** suma CMP-023..026 en una fila nueva, con su plano en cada nodo, y tres aristas reales: `routeAdmittedRequest`, `resolveEgressCredential` y `decideUnknownOutcome`. También una vista "Operación durable (v1.2)" y las tarjetas actualizadas (15 componentes, 4 aristas; versión 0.2: 26 / 48). La línea de la tarjeta cian sobre PolicyEngine → HandoffCoordinator quedó reducida a un puntero, para no desbordar el viewport.
  - **`nucleo-del-arnes`:** los once componentes de Article III no cambian; se agrega un ítem que remite a `capa-enterprise` para los quince restantes.
  - **Ambos:** `meta.repository.revision` pasa a `3bcceb5`. Validación showcase 9/9, 0/0; visual-check pass.
- Tag `v0.2` sobre el merge de esta rama.
