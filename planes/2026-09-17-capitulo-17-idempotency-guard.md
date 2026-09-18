# Plan / Registro de ejecución — Capítulo 17: IdempotencyGuard y la Deduplicación de un Side Effect Crítico

**Fecha:** 2026-09-17
**Estado:** ✅ Completado, sobre el estado dejado por `0755573` (CH-00..CH-16 como los diecisiete
únicos capítulos reales; tres componentes del Amendment v1.1 ya instanciados: `AdmissionController`
CH-14, `AgentCommunicationGateway` CH-15, `CredentialBroker` CH-16).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-14-capitulo-16-credential-broker.md` (precedente inmediato: mismo tipo de capítulo del
  Amendment v1.1, y origen del fix de `scripts/lib/render-diagram.js` que este capítulo también usa)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Article II — Invariantes originales, `INV-11`;
  Amendment v1.1 — `P-24`, `INV-E09`)

**Nota de proceso**: este documento lo escribe la sesión principal, no el subagente que escribió el
capítulo — el subagente terminó su turno esperando la notificación de un `build-all` en background
que lanzó él mismo, sin llegar a comitear (mismo patrón recurrente ya visto en CH-14/CH-15). El
contenido de `book/chapters/17-idempotency-guard/chapter.md` y de los registries ya estaba completo
y bien formado en disco — se verificó de nuevo aquí, sin reescribirlo, y se completó el resto del
ciclo (build limpio, verificación, este documento, commit, push).

---

## 1. Objetivo

Escribir el decimoctavo capítulo real de contenido del libro, CH-17 — el cuarto componente del
Amendment v1.1 (`constitution/ARCHITECTURE_CONSTITUTION.md`, línea 926+), cubriendo el **Reliability
Plane** (séptimo de los 9 "Canonical Enterprise Planes", cuarto que este libro cubre). A diferencia
de `AdmissionController`/`AgentCommunicationGateway`/`CredentialBroker` (los tres nombrados
literalmente en el texto de la Constitution), **ningún texto constitucional nombra un componente
específico** para la idempotencia de side effects — `P-24`/`INV-E09` solo exigen la propiedad, sin
asignarle un dueño. Este capítulo también cierra `INV-11` (Article II, **original**, no Amendment),
declarado desde CH-00 y nunca antes resuelto por ningún componente en dieciséis capítulos reales.

## 2. Alcance (decisión ya tomada antes de escribir, confirmada en el resultado)

Exactamente **1 componente + 1 contrato**:

1. **`IdempotencyGuard`** (`CMP-015`) — nombre sintetizado por este libro (no una cita literal),
   documentado explícitamente como tal en el comentario de `registry/components.yaml` junto a su
   ficha. `owns`: detectar si un `ToolCall` (`C-008`, CH-02) con side effects ya se ejecutó antes
   bajo la misma clave de idempotencia (asumida como señal de entrada dada — este capítulo no
   decide cómo se genera esa clave), decidir si una ejecución repetida debe reusar el `ToolResult`
   (`C-009`) ya producido en vez de duplicar el side effect real, y registrar de forma terminal y
   *write-once* el `IdempotencyRecord` resultante de una ejecución nueva ya concluida — nunca
   sobrescribiendo uno ya `COMPLETED`. `does_not_own` (cinco fronteras trazadas con precisión,
   cuatro contra componentes ya existentes y una contra infraestructura de borde): ejecutar el side
   effect en sí (`ToolRuntime`, CH-02), decidir autorización (`PolicyEngine`, CH-05), resolver qué
   implementación satisface la capability (`CapabilityRegistry`, CH-08), decidir si un `AgentRun`
   puede reintentar contra su `ExecutionBudget` (`ExecutionController`, CH-07 — la distinción
   central del capítulo: "¿ya se hizo con éxito?" y "¿puedo seguir intentando?" son preguntas
   ortogonales sobre materiales distintos), y el mecanismo real de persistencia atómica que evita
   una condición de carrera entre dos ejecuciones concurrentes con la misma clave (Preview,
   infraestructura de borde).
2. **`IdempotencyRecord`** (`C-027`) — `id`, `idempotencyKey: Text`, `capability: CapabilityId`,
   `originalToolCallId: ToolCallId`, `status: IdempotencyRecordStatus` (ENUM `PENDING`/`COMPLETED`
   — **nunca un Boolean**: la ausencia total de un registro, no un tercer valor del enum, es lo que
   representa "nunca visto antes"; `PENDING` existe específicamente para que una segunda llamada
   concurrente con la misma clave pueda distinguir "ya se hizo" de "se está haciendo ahora mismo" y
   decida esperar en vez de duplicar el side effect), `result: Optional<ToolResult>` (poblado solo
   en `COMPLETED`), `createdAt`, `completedAt: Optional<Timestamp>`.
3. `consumes: [C-004, C-008, C-009]`, `produces: [C-010, C-011, C-027]` — ningún componente previo
   editado; `book/chapters/16-credential-broker/chapter.md` solo recibió `next_chapter: CH-17`.

## 3. Verificación (ejecutada por esta sesión tras encontrar el trabajo completo sin comitear)

```
rm -rf dist && ./scripts/build-all
```
Exit 0. 18 capítulos válidos (`validate-chapter`/`validate-retrieval-set`), 27 contratos, 15
componentes. `chapter-17.diagram` creció respecto a `chapter-16.diagram` (109 nodos/167 aristas).
`dist/book.pdf` se generó sin errores usando el fix de `scripts/lib/render-diagram.js` (normalización
con Ghostscript) introducido en CH-16 — sin necesidad de tocarlo de nuevo.

`pypdf`: el texto extraído contiene "IdempotencyGuard", "IdempotencyRecord", "CMP-015", "C-027".
Web: `dist/web/chapters/CH-17.html` con SVG inline, anchors `id="CMP-015"`/`id="C-027"`, navegación
CH-16↔CH-17 verificada en ambos sentidos; CH-00..CH-16 con su SVG y anchors clave intactos.

## 4. Deuda intencional hacia el próximo capítulo

- **La integración real `ToolRuntime ↔ IdempotencyGuard`**: `executeToolCall` (CH-02) no consulta
  `checkIdempotency` antes de ejecutar ni invoca `recordIdempotentExecution` después — mismo patrón
  de deuda que domina el libro desde CH-03, resuelto explícitamente por capítulos de integración
  (CH-12/CH-13) cuando llegue el momento, no aquí.
- **La ruta de "protección equivalente"** que `INV-11` deja abierta como alternativa a la
  idempotencia estricta (compensación/reversión tras el hecho): no modelada, señalada en el propio
  capítulo (§18).
- **Generación de la `idempotencyKey`**: asumida como señal de entrada dada, no diseñada aquí.
- **Persistencia atómica real** contra condiciones de carrera: Preview, infraestructura de borde.
- **Los 5 planos restantes** del Amendment v1.1 (Data & Context, Control, Observability &
  Governance, Execution Fabric, y la porción de Execution Plane no ya cubierta por el core):
  candidatos para los próximos incrementos.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
