# Plan / Registro de ejecución — Cierre de release v0.2.1

**Fecha:** 2026-09-26
**Estado:** ✅ Completado (2026-09-26). Rama `release-v0.2.1` mergeada a `main`, sobre `6af01b6`; tag `v0.2.1`.
**Aprobación humana:** ✅ el autor aprobó el cierre y el tag `v0.2.1` el 2026-09-26 ("aprobado").

**Depende de:** `2026-09-26-cierre-release-v0-2.md` §3 (decisiones sobre la deuda) y la release v0.2.1 del plan maestro (§3).

## 1. Qué incluye v0.2.1

- **Tooling:** `registry/debt.yaml` y `scripts/validate-debt` en `build-all` (`2026-09-26-tooling-registro-de-deuda.md`).
- **Revisión de CH-13:** `beginToolApprovalPauseForDecision`, `resolveApprovalForResume` y `observationForApproval`, con las firmas publicadas intactas; CH-36 las invoca (`2026-09-26-revision-ch13-aprobacion-expuesta.md`).
- **Renumeración de v0.3:** CH-37..CH-47 pasan a CH-39..CH-49.
- **CH-37**, esperas, credenciales y canales completos: D-009..D-013.
- **CH-38**, identidad, auditoría y retención en todo el turno: D-001..D-008.
- **Totales:** 26 componentes, 48 contratos (sin cambios), 39 capítulos, 169 términos.

## 2. Pasos del cierre

1. **`registry/debt.yaml`:** tres deudas nuevas.
   - D-041: reescribir `enterDurableTurn` y `runDurableGovernedStep` con las funciones de CH-37 y CH-38. Destino CH-49.
   - D-042: avisar a un aprobador por un canal distinto del de la sesión. Destino CH-49.
   - D-043: reglas de política más ricas por Principal. `out_of_scope`, con su justificación.
2. **CH-25:** nota "Actualización (cierre de v0.2.1)" en §1.
3. **KB:** `kb/Index.md` (versión 0.2.1, 39 capítulos, 169 términos, fila "Cierre de deuda"), `kb/00-Inicio/El-Libro.md` e índice de capítulos.
4. **`book/book.yaml`:** `version: "0.2.1"`.
5. `build-all` → tag `v0.2.1` → push.

## 3. Resultado real

- **`validate-debt` con `book.version = 0.2.1`:** OK. 43 deudas: 14 open, todas en v0.3 (CH-39..CH-49); 23 resolved; 6 out_of_scope. Ninguna vencida.
- **`build-all`:** exit 0 con 39/39 capítulos y 39/39 retrieval sets; `dist/book.pdf` 5,6 MB; `Missing character` en 6; 0 `Could not fetch`.

## 4. Balance de la deuda de v0.2

| Estado | Cantidad |
|---|---|
| Resueltas en v0.2 (CH-29..CH-36) | 9 |
| Resueltas en v0.2.1 (CH-13 revisado, CH-37, CH-38) | 14 |
| Fuera de alcance, con justificación | 6 |
| Abiertas, con capítulo de v0.3 asignado | 14 |
