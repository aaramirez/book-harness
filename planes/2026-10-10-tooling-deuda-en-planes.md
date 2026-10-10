# Plan / Registro de ejecución — Tooling: la deuda de los planes también se verifica

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `tooling-deuda-en-planes` mergeada a `main`, sobre `540597e`.
**Decisión del autor:** "ajusta el validador y luego sigue" (2026-10-10).

**Depende de:** `2026-09-26-tooling-registro-de-deuda.md` (`registry/debt.yaml` y `validate-debt`). Regla 5 del plan maestro: un cambio de tooling lleva plan propio y nunca desactiva un validador.

## 1. Problema

`validate-debt` revisa `registry/debt.yaml`, pero no los planes. En CH-40 y en CH-41 quedaron pendientes con destino futuro escritos solo en la sección "Deuda" del plan, sin entrada en el registro. Se detectaron a mano antes del commit (D-045, D-046, D-047). Un pendiente que vive solo en la prosa puede vencer sin que el build lo note.

## 2. Cambio

`scripts/validate-debt` gana `checkPlanDebtSections`:
- recorre `planes/*-capitulo-NN-*.md`;
- dentro de una sección `## N. Deuda…`, toda línea que nombre un capítulo que **no existe** en `book/book.yaml` debe:
  - citar al menos un `D-NNN`, y cada id citado tiene que existir en `registry/debt.yaml`; o
  - declarar explícitamente "no es deuda".

Las líneas que nombran capítulos ya escritos no se revisan: son historia, y el registro ya cubre su vencimiento.

## 3. Lo que encontró al activarse

12 líneas, en los planes de CH-29, CH-31..CH-35 y CH-37..CH-39:
- **11 ya tenían su deuda registrada** y solo les faltaba la cita. Se anotaron con "(registrada: D-NNN)": D-015, D-016, D-017, D-006/D-018/D-019, D-020, D-022, D-023, D-024, D-026, D-041 y D-042. La línea de CH-37 decía "candidata para CH-46", pero D-042 se había registrado con destino CH-49 al cerrar v0.2.1; se corrigió el texto.
- **1 era un pendiente nunca registrado:** en CH-39, "registrar el cambio de modelo a mitad de un run … no se registra deuda aparte". Ahora es **D-048** → CH-45.

## 4. Verificación

- **Prueba negativa** (sobre una copia del plan de CH-41, restaurada byte a byte):
  - una línea con destino CH-47 sin id → falla;
  - una con un id inexistente `D-999` → falla;
  - una marcada "no es deuda" → pasa.
- `validate-debt`: OK, 48 deudas (16 open, 26 resolved, 6 out_of_scope).
- `build-all`: exit 0 con 42/42 capítulos; `validate-debt` en la etapa de validación, en verde.

## 5. Efecto en el procedimiento

El paso REGISTRO del §8 del plan maestro ya pedía actualizar `registry/debt.yaml`. Ahora el build lo exige también para la sección "Deuda" del plan de cada capítulo.
