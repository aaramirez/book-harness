# Plan / Registro de ejecución — Cierre de release v0.3

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `release-v0.3` mergeada a `main`, sobre `c566d39`; tag `v0.3`.
**Aprobación humana:** ✅ el autor aprobó el cierre y el tag `v0.3` el 2026-10-10 ("Aprobar el cierre").

**Depende de:** `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md` (release v0.3, CH-39..CH-49) y `2026-09-26-cierre-release-v0-2-1.md` (mismos pasos de cierre).

## 1. Qué incluye v0.3

- **CH-39..CH-49** (once capítulos): el modelo como dato, ExtensionHost, ConnectionManager, RetrievalEngine, presupuestos heredados, invocación durable entre agentes, evolución del runtime, observabilidad por audiencia, evaluación con lift, el agente como directorio y el arnés conectado.
- **ADRs aceptados en v0.3:** ADR-004 (presupuesto jerárquico, con `consumed` opcional y `sandboxLimits`), ADR-005 (capability desde conexión, con `executionKind`) y ADR-003 parte v3 (versión del runtime en la sesión, con "versión desconocida").
- **Tooling:** `validate-debt` verifica también las secciones de deuda de los planes de capítulo (`2026-10-10-tooling-deuda-en-planes.md`).
- **Totales:** 29 componentes (CMP-027..029 nuevos), 66 contratos (C-049..C-066 nuevos), 50 capítulos, 201 términos.

## 2. Pasos del cierre

1. **CH-25:** notas "Actualización (cierre de v0.3)" en §1 (Tramo 5) y §17 (totales).
2. **KB:** `kb/Index.md` (versión 0.3, 29 componentes, 66 contratos, 50 capítulos, 201 términos, fila "Conectividad"), `kb/00-Inicio/El-Libro.md`.
3. **`book/book.yaml`:** `version: "0.3"`.
4. `build-all` → merge → tag `v0.3` → push.

## 3. Resultado real

- **`validate-debt` con `book.version = 0.3`:** OK. 48 deudas: **0 open**, 42 resolved, 6 out_of_scope.
- **`build-all`:** exit 0 con 50/50 capítulos y 50/50 retrieval sets; `Missing character` en 6 (los subíndices de CH-10, línea base).

## 4. Balance de la deuda

| Estado | Cantidad |
|---|---|
| Resueltas en v0.2 (CH-29..CH-36) | 9 |
| Resueltas en v0.2.1 (CH-13 revisado, CH-37, CH-38) | 14 |
| Resueltas en v0.3 (CH-39..CH-49) | 19 |
| Fuera de alcance, con justificación | 6 |
| Abiertas | 0 |

## 5. Lo que sigue

Lo que venga después de v0.3 se planea en un plan maestro nuevo.
