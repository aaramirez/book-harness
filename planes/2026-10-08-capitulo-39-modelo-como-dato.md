# Plan / Registro de ejecución — Capítulo 39: El Modelo como Dato: Catálogo, Costo y Cache

**Fecha:** 2026-10-08
**Estado:** ✅ Completado (2026-10-08). Rama `cap-39-modelo-como-dato` mergeada a `main`, sobre `9961a18` (tag `v0.2.1`).
**Release:** v0.3, primer capítulo. Deuda con destino CH-39: D-021.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-39 (§6).
- `2026-09-13-capitulo-03-model-gateway.md`: `ModelGateway` (CMP-003), `ModelRequest` (C-006), `ModelResponse` (C-007), `RawToolCallProposal`.
- `2026-09-14-capitulo-07-execution-controller.md`: `ExecutionBudget.maxCost` y `ExecutionUsage.costUsed`.
- CH-22: `BusinessOutcomeCorrelation` (C-033).
- Propuesta de pi P-A4 (`arnes-ai/docs/propuestas/book-harness/BH-Propuesta-Aportes-pi.md`): catálogo, `calculateCost`, `cacheRetention`. Se toma el **contrato**, no los adaptadores (P-27).

## 1. Objetivo

Que el modelo sea un **dato** que ModelGateway selecciona de un catálogo (ventana, precios, capacidades, versión exacta para INV-E10), que cada llamada produzca su **uso y costo**, que la **política de cache** se pida y se reduzca a lo que el modelo soporta, y que una respuesta con **varias tool calls** se normalice (D-021).

## 2. Alcance decidido

**0 componentes + 2 contratos + 2 contratos modificados**, sin ADR:
1. **C-049 `ModelDescriptor`:** modelId, provider, descriptorVersion, contextWindow, maxOutputTokens, pricing, capabilities.
2. **C-050 `UsageRecord`:** modelId, descriptorVersion, inputTokens, outputTokens, cacheReadTokens, cacheWriteTokens, cost, currency, recordedAt.
3. **C-006 `ModelRequest` v2:** `cacheRetention: Optional<CacheRetention>`.
4. **C-007 `ModelResponse` v2:** `proposedToolCalls: List<RawToolCallProposal>` (resuelve D-021) y `usage: Optional<UsageRecord>`.
5. **Embebidos:** `ENUM CacheRetention`, `STRUCT ModelPricing`, `ENUM ModelCapability`, `STRUCT OutcomeCost`.
6. **ModelGateway (CMP-003)**, dentro de su `owns` ("selección de provider", "normalización de respuestas"): `hasCapability`, `selectModelDescriptor`, `fitsContextWindow`, `effectiveCacheRetention`, `calculateUsageCost`, `effectiveToolCallProposals`, `attachUsage`.
7. **Integración:** `accumulateUsage` (UsageRecord → ExecutionUsage, para el presupuesto) y `costForOutcome` (costo por resultado de negocio, P-29).

## 3. Decisiones de diseño centrales

- **Fuera del catálogo no hay modelo:** `selectModelDescriptor` es fail-closed, ante un modelo que no está o que no tiene la capacidad pedida.
- **La cache se pide, no se impone:** si el modelo no soporta `PROMPT_CACHE`, `effectiveCacheRetention` devuelve `NONE`.
- **El costo lo calcula el arnés** con el precio del catálogo, no lo informa el proveedor, para que dos proveedores se comparen con la misma regla.
- **D-021 se resuelve en el contrato:** `proposedToolCalls` lleva todas las propuestas; `proposedToolCall` se conserva como la primera, por compatibilidad. Registrar varias en el journal (`StepRecord` tiene una sola tool call) es **D-044**, con destino CH-49. Se registró al empezar el capítulo.
- **Costo por resultado:** solo suma registros de una moneda; con monedas mezcladas falla, y no convierte.

## 4. Archivos creados

- `book/chapters/39-modelo-como-dato/chapter.md` (secciones 0–21, 17 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-39-modelo-como-dato.md`, `kb/03-Contratos/C-049-modeldescriptor.md`, `kb/03-Contratos/C-050-usagerecord.md`
- `diagrams/archify/capitulo-39-modelo-como-dato.json` + `rendered/…html`; `diagrams/mindmap/chapter-39.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/contracts.yaml`: C-006 **v1 → v2** (`cacheRetention`), C-007 **v1 → v2** (`proposedToolCalls`, `usage`), C-049, C-050
- `registry/glossary.yaml`: Model Catalog, ModelDescriptor, UsageRecord
- `registry/debt.yaml`: D-021 → `resolved` (CH-39, en el contrato); **D-044 nueva** (journal de varias propuestas) → CH-49
- `book/book.yaml`; CH-38 `next_chapter: CH-39`
- KB: C-006 y C-007 (v2), índices de capítulos y contratos, glosario, navegación de CH-38

## 6. Resultado real del pipeline

- **Rojo:** 23 errores de capítulo y 1 de `validate-debt` (D-021 vencida al entrar CH-39).
- **Registro:** `validate-contracts` OK (50), `validate-components` OK (26), `validate-debt` OK (14 open, 24 resolved, 6 out_of_scope).
- **Verde:** `validate-chapter` OK (22 secciones, 17 bloques, 2 contratos); `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas y de nombres de proveedores de modelos vacío.
- **`build-all` exit 0 con 40/40 capítulos y 40/40 retrieval sets.** El mapa mental dibuja `CH-39 → C-006` y `CH-39 → C-007 [MODIFIES]`. `dist/book.pdf` 5,7 MB; `Missing character` en 6; 0 `Could not fetch`.
- **Archify:** showcase 9/9, 0/0; spec `9a4caa5a6110`; visual-check pass; revisado a 1440×900 (claro y oscuro). Cinco participantes (EvaluationHarness queda en una nota); el tercer segmento tiene dos mensajes; etiquetas acortadas, con el detalle en las notas.

## 7. Definition of Done

- [x] Validadores de CH-39 en verde; C-049, C-050 registrados; C-006 y C-007 en v2 con `modified_by: [CH-39]`; D-021 resolved.
- [x] 40/40 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-38 `next_chapter` = CH-39.

## 8. Deuda

- **D-044** (registrada): registrar en el journal una respuesta con varias tool calls sin volver a llamar al modelo → CH-49.
- Registrar el cambio de modelo a mitad de un run como entrada de sesión: se cubre con `RuntimeVersionSnapshot` en CH-45 (ya planeado; no se registra deuda aparte).
