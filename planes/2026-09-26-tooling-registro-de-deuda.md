# Plan / Registro de ejecución — Tooling: registro de deuda verificable

**Fecha:** 2026-09-26
**Estado:** ✅ Completado (2026-09-26). Rama `tooling-registro-deuda` mergeada a `main`, sobre `82832ab` (tag `v0.2`).

**Depende de:**
- `2026-09-26-cierre-release-v0-2.md` §3: decisión del autor ("Sí, verificable").
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md` §0, regla 5: un cambio de tooling lleva plan propio y nunca desactiva un validador.

## 1. Problema

Cada plan de capítulo termina con una sección "Deuda", y cada capítulo con un §18 que dice a qué capítulo futuro pasa cada punto. Ningún validador lo revisa. Así, siete capítulos (CH-28, CH-29, CH-31..CH-35) asignaron trabajo a "CH-36", CH-36 se escribió sin hacerlo, y el build siguió en verde.

## 2. Diseño

**`registry/debt.yaml`**, un cuarto registro junto a contracts, components y glossary:

```yaml
debts:
  - id: D-001                  # D-NNN, correlativo, nunca se reutiliza
    title: "…"                 # una frase
    origin: CH-33              # capítulo que la declaró (debe existir en book/book.yaml)
    status: open               # open | resolved | out_of_scope
    target: v0.2.1             # open: capítulo planeado (CH-NN) o release (vX.Y.Z)
    retargeted_from: [CH-36]   # opcional: destinos anteriores que no la resolvieron
    resolved_in: CH-36         # resolved: capítulo existente que la resolvió
    rationale: "…"             # out_of_scope: por qué no se resuelve (obligatorio)
```

**`scripts/validate-debt`**, que corre en la etapa de validación de `build-all`, antes de los capítulos:
1. Campos obligatorios; `id` con formato `D-NNN` y único; `status` válido.
2. `origin` existe en `book/book.yaml`.
3. **`open` con destino `CH-NN`:** si ese capítulo ya existe en `book/book.yaml`, **falla** ("deuda vencida: el capítulo destino ya se escribió"). El destino debe ser posterior al origen.
4. **`open` con destino de release (`vX.Y.Z`):** si `book.version` ya es igual o mayor, **falla** ("deuda vencida: la release destino ya se cerró").
5. **`resolved`:** `resolved_in` existe en `book/book.yaml` y no es anterior al origen.
6. **`out_of_scope`:** `rationale` no vacío.
7. Imprime un resumen por estado y por destino.

**Regla 3** es la que habría detenido CH-36: el capítulo destino se escribió y la deuda seguía abierta.

**Para cerrar una deuda** hay que hacer una de tres cosas en el mismo incremento:
- marcarla `resolved` con `resolved_in`;
- moverla a otro destino, dejando el anterior en `retargeted_from`;
- declararla `out_of_scope` con su justificación.

Cualquiera de las tres queda en el diff y en la revisión humana.

**No se cambia ningún validador existente.** `registries.js` gana `loadDebts()`; `build-all`, una línea.

## 3. Carga inicial

Los 35 puntos de las secciones "Deuda" de CH-28..CH-36, deduplicados y separados en unidades atómicas. Resultan 40 entradas:
- **14 `open` → `v0.2.1`:** los 9 grupos "sin dueño" del cierre de v0.2, separados en unidades atómicas. Cada una lleva en `retargeted_from` el capítulo escrito que no la resolvió.
- **12 `open` → capítulo de v0.3** (CH-37..CH-43, numeración actual del plan maestro; se actualizan cuando se renumere v0.3).
- **9 `resolved`** por un capítulo posterior de v0.2.
- **5 `out_of_scope`**, con justificación.

## 4. Verificación

- `validate-debt` en verde con la carga inicial.
- **Prueba negativa (sin commit):** mover una deuda de `v0.2.1` a `CH-36` debe hacer fallar `build-all` en la etapa de validación.
- `build-all` exit 0.

## 5. Resultado real

- **Archivos nuevos:** `registry/debt.yaml` (40 deudas) y `scripts/validate-debt`.
- **Archivos modificados:**
  - `scripts/lib/registries.js` (`loadDebts`) y `scripts/build-all` (`validate-debt` después de `validate-components`);
  - `scripts/README.md`, `agents/book-architect.md` (el Brief debe incluir la deuda con destino en el capítulo, y el agente corre `validate-debt`) y `kb/00-Inicio/Como-Usar-la-KB.md`;
  - §8 del plan maestro: el paso REGISTRO actualiza `registry/debt.yaml` y corre `validate-debt`.
- **`validate-debt`:** OK (26 open, 9 resolved, 5 out_of_scope). Destinos abiertos: `v0.2.1` 14, CH-40 4, CH-39 2, CH-42 2, CH-43 2, CH-37 1, CH-41 1.
- **Pruebas negativas** (sobre copias; los archivos se restauraron y se compararon byte a byte):
  1. D-001 con destino CH-36 → `VENCIDA: su destino CH-36 ya existe`, exit 1;
  2. `book.version` en 0.2.1 → 14 deudas `VENCIDA`, exit 1;
  3. `resolved` sin `resolved_in`, `out_of_scope` sin `rationale` y destino anterior al origen → 4 errores, exit 1;
  4. `build-all` con el caso 1 → "FALLÓ en la etapa de validación … build detenido".
- **`build-all` exit 0** con 37/37 capítulos; `Missing character` en 6.
- **Consecuencia para v0.2.1:** subir `book.version` a `0.2.1` sin cerrar las 14 deudas hace fallar el build. El tag `v0.2.1` no puede crearse con deuda abierta.
