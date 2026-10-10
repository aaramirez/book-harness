# Plan / Registro de ejecución — Capítulo 46: Observabilidad Acotada por Audiencia

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `cap-46-observabilidad-por-audiencia` mergeada a `main`, sobre `8e27f22`.
**Release:** v0.3. Sin deudas con destino CH-46. Retoma lo que CH-35 (telemetría del proxy) y CH-42 (techos por audiencia) declararon "no es deuda, planeado en CH-46".

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-46 (§6).
- CH-09 (`EventBus`, fan-out), CH-19 (`AuditLedger`, auditoría distinta de la telemetría), CH-20 (`DataGovernanceEngine`, `DataClassificationLevel`), CH-42 (`moreRestrictive`, `selectRetrievedCandidates` con techo).
- Constitución: P-04 (toda acción produce eventos observables), P-22, P-25 (la evidencia de auditoría es distinta de la telemetría operativa), P-37 (la captura de observabilidad está acotada por la audiencia), INV-E11, INV-E23 (ningún destino de trazas captura por encima del techo de la sesión).

## 1. Objetivo

Que cada sesión tenga una audiencia (PUBLIC, PRIVATE, UNKNOWN) asignada al crearla, que esa audiencia fije un techo de captura que ningún destino de telemetría pueda superar ni restaurar, y que una sesión pública no ponga en el contexto datos que su audiencia no debe ver.

## 2. Alcance decidido

**0 componentes + 3 contratos:**
1. **C-061 `SessionAudience`:** sessionId, kind, decidedBy, decidedAt.
2. **C-062 `TraceCapturePolicy`:** audience, ceiling, captureBodies.
3. **C-063 `TelemetrySpan`:** spanId, traceId, parentSpanId?, sessionId, name, startedAt, endedAt?, attributes, body?, classification, redacted.
4. **Embebidos:** `ENUM AudienceKind` (PUBLIC, PRIVATE, UNKNOWN), `STRUCT TraceDestination`, `STRUCT SpanDelivery`.
5. **Funciones:**
   - DataGovernanceEngine (CMP-018): `classifySessionAudience`, `reclassifySessionAudience`, `lowerCeiling`, `findCapturePolicy`, `captureCeilingFor`, `contextCeilingForAudience`, `governSpanForDestination`;
   - EventBus (CMP-009): `fanOutSpan`.

## 3. Decisiones de diseño centrales

- **Tres señales, tres propósitos** (P-25): el evento observa, la auditoría prueba, el span diagnostica. El techo de captura recorta solo los spans; la auditoría tiene su propia retención y clasificación (CH-19, CH-38).
- **La audiencia acota en dos direcciones:**
  - una sesión PUBLIC (o UNKNOWN) baja el techo del **contexto**: lo que el agente responde lo ve su audiencia;
  - una sesión PRIVATE (o UNKNOWN) baja el techo de la **telemetría**: los operadores no ven lo privado.
- **UNKNOWN es lo más restrictivo de ambos lados** (fail-closed).
- **Dentro de una sesión, la audiencia solo se vuelve más restrictiva.**
- **El destino recibe lo ya recortado:** ningún destino puede restaurar lo que el techo excluyó, porque nunca le llegó.
- **Sin componente nuevo:** clasificar y fijar techos es de DataGovernanceEngine; distribuir, de EventBus.

## 4. Archivos creados

- `book/chapters/46-observabilidad-por-audiencia/chapter.md` (secciones 0–21, 14 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-46-observabilidad-por-audiencia.md`, `kb/03-Contratos/C-061-sessionaudience.md`, `C-062-tracecapturepolicy.md`, `C-063-telemetryspan.md`
- `diagrams/archify/capitulo-46-observabilidad-por-audiencia.json` + `rendered/…html`; `diagrams/mindmap/chapter-46.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/contracts.yaml`: C-061, C-062, C-063
- `registry/glossary.yaml`: Capture Ceiling, SessionAudience, TraceCapturePolicy, TelemetrySpan
- `book/book.yaml`; CH-45 `next_chapter: CH-46`
- KB: índices de contratos y capítulos; glosario; navegación de CH-45

## 6. Resultado real del pipeline

- **Rojo:** 22 errores de capítulo con solo el frontmatter; `validate-debt` sin deudas con destino CH-46.
- **Registro:** `validate-contracts` OK (63), `validate-components` OK (29), `validate-debt` OK.
- **Verde:** `validate-chapter` OK al primer intento (22 secciones, 14 bloques, 3 contratos, 0 componentes); `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **`build-all` exit 0 con 47/47 capítulos y 47/47 retrieval sets.** `dist/book.pdf` 6,8 MB; `Missing character` en 6.
- **Archify:** showcase 9/9, 0/0; `check` 9/9; visual-check pass, revisado a 1440×900 (claro y oscuro); 11 mensajes, 5 participantes.

## 7. Definition of Done

- [x] Validadores de CH-46 en verde; C-061, C-062, C-063 registrados.
- [x] 47/47 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-45 `next_chapter` = CH-46.

## 8. Deuda

- Sin deuda nueva. Lo de §18 del capítulo se declaró explícitamente:
  - el formato de exportación es del adaptador de cada destino: no es deuda;
  - el muestreo de spans es configuración del adaptador: no es deuda;
  - la clasificación del cuerpo la asigna quien produce el span (CH-20): no es deuda;
  - quién lee la auditoría es autorización sobre AuditLedger: no es deuda.
