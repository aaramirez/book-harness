# Plan / Registro de ejecución — Capítulo 42: Fuentes de Datos Gobernadas

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `cap-42-fuentes-de-datos` mergeada a `main`, sobre `acc774a`.
**Release:** v0.3. Deudas con destino CH-42: D-015, D-016, D-019, D-024, D-047.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-42 (§6).
- CH-04 (`assembleContextSnapshot` recibe candidatos "ya dados, sin retrieval"; `ContextBlock` con `provenance`), CH-20 (`classifyData`, `DataGovernanceLabel`, `DataClassificationLevel`), CH-29 (`CompactionSummary.provenance`), CH-31 (`requireTenantCaller`), CH-34 (`sourceKind = STREAM_EVENT`), CH-41 (`ConnectionDescriptor`).
- Constitución: P-01, P-14 (seleccionar, no volcar), P-22, EVO-09 (procedencia y frescura), INV-E11 (la política del dato lo acompaña), INV-E26 (una fuente sin clasificación es RESTRICTED).

## 1. Objetivo

Cerrar el hueco de CH-04: que los datos lleguen al contexto desde **fuentes declaradas**, recuperados para el llamante, con procedencia, clasificación y frescura, y que ContextEngine decida qué entra.

## 2. Alcance decidido

**1 componente + 2 contratos:**
1. **CMP-029 `RetrievalEngine`.**
2. **C-055 `DataSourceDescriptor`:** sourceId, kind, endpointRef, classification?, access, scopeRule, connectionId?, credentialName?, freshnessSeconds?.
3. **C-056 `RetrievedCandidate`:** candidateId, sourceId, content, provenance, classification, score, observedAt, label?.
4. **Embebidos:** `DataSourceKind` (SQL, FILES, HTTP, STREAM, CONNECTION_RESOURCE), `DataAccessMode` (READ_ONLY), `DataScopeRule` (SHARED, PER_TENANT, PER_PRINCIPAL), `DataScope`, `SourceRecord`.
5. **Funciones:**
   - RetrievalEngine: `effectiveSourceClassification`, `validateDataSource`, `scopeFor`, `retrieveCandidates`;
   - DataGovernanceEngine: `moreRestrictive`, `classifyDerivedData` (D-016);
   - ContextEngine: `selectRetrievedCandidates`, `summaryContextBlock` (D-015);
   - integración: `governRetrievedCandidate`.

| Deuda | Cómo se resuelve |
|---|---|
| D-015 | `summaryContextBlock`: el bloque del resumen usa `CompactionSummary.provenance`, no `"conversation_history"` |
| D-016 | `classifyDerivedData`: el resumen hereda la clasificación más restrictiva, la preservación legal y la retención más corta de sus fuentes |
| D-019 | `scopeFor`: alcance `PER_TENANT` / `PER_PRINCIPAL` sobre `execution.caller.current` |
| D-024 | `DataSourceKind.STREAM` con `freshnessSeconds` obligatoria: se lee una ventana reciente; activar desde un stream sigue siendo CH-34 |
| D-047 | `DataSourceKind.CONNECTION_RESOURCE`: los recursos de un servidor MCP entran por una conexión declarada (CH-41) |

## 3. Decisiones de diseño centrales

- **Recuperar no es seleccionar:** RetrievalEngine decide qué **puede** recuperarse (fuente, alcance, clasificación, frescura); ContextEngine decide qué **entra** (ranking bajo presupuesto, techo de clasificación).
- **La clasificación más restrictiva gana.** Entre la que declara la fuente y la que asigna DataGovernanceEngine, vale la más restrictiva; sin declaración, RESTRICTED.
- **Una fuente es de solo lectura:** escribir es una tool, con su política y su journal.
- **El techo de clasificación del contexto lo fija la política** (PolicyEngine); ContextEngine solo lo aplica. Los techos por audiencia llegan en CH-46.

## 4. Archivos creados

- `book/chapters/42-fuentes-de-datos/chapter.md` (secciones 0–21, 17 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-42-fuentes-de-datos.md`, `kb/02-Componentes/CMP-029-retrievalengine.md`, `kb/03-Contratos/C-055-datasourcedescriptor.md`, `C-056-retrievedcandidate.md`
- `diagrams/archify/capitulo-42-fuentes-de-datos.json` + `rendered/…html`; `diagrams/mindmap/chapter-42.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/components.yaml`: CMP-029
- `registry/contracts.yaml`: C-055, C-056
- `registry/glossary.yaml`: Governed Retrieval, Derived Data Label, DataSourceDescriptor, RetrievedCandidate
- `registry/debt.yaml`: D-015, D-016, D-019, D-024, D-047 → `resolved` (CH-42)
- `book/book.yaml`; CH-41 `next_chapter: CH-42`
- KB: índices de componentes, contratos y capítulos; glosario; navegación de CH-41

## 6. Resultado real del pipeline

- **Rojo:** 22 errores de capítulo y 5 de `validate-debt` (las cinco deudas de CH-42, vencidas al entrar el capítulo).
- **Registro:** `validate-contracts` OK (56), `validate-components` OK (29), `validate-debt` OK (11 open, 31 resolved, 6 out_of_scope), ya con la verificación de los planes.
- **Verde:** `validate-chapter` OK (22 secciones, 17 bloques, 2 contratos, 1 componente); `validate-retrieval-set` OK (4/4/2/1/3/4), sin ajustes. Grep de plataformas vacío.
- **`build-all` exit 0 con 43/43 capítulos y 43/43 retrieval sets.** `dist/book.pdf` 6,2 MB; `Missing character` en 6; 0 `Could not fetch`.
- **Archify:** showcase 9/9, 0/0; spec `805df6bdf3ec`; visual-check pass; revisado a 1440×900 (claro y oscuro). La selección es un solo mensaje, sin flecha de retorno, para no pasar de 11.

## 7. Definition of Done

- [x] Validadores de CH-42 en verde; CMP-029, C-055, C-056 registrados; D-015, D-016, D-019, D-024, D-047 resolved.
- [x] 43/43 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-41 `next_chapter` = CH-42.

## 8. Deuda

- Sin deuda nueva. Lo de §18 del capítulo se declaró explícitamente:
  - búsqueda semántica e índices son del adaptador de cada fuente: no es deuda;
  - la memoria de largo plazo es una fuente más: no es deuda;
  - los techos por audiencia ya están planeados con `SessionAudience` en CH-46: no es deuda;
  - activar desde un stream sigue en el Ingress Adapter de CH-34: no es deuda.
