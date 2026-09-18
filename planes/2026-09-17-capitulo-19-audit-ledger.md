# Plan / Registro de ejecución — Capítulo 19: AuditLedger y la Evidencia de Auditoría Estructuralmente Inmutable

**Fecha:** 2026-09-17
**Estado:** ✅ Completado, sobre el estado dejado por `703a5fd` (CH-00..CH-18 como los diecinueve
únicos capítulos reales; cinco componentes del Amendment v1.1 ya instanciados: `AdmissionController`
CH-14, `AgentCommunicationGateway` CH-15, `CredentialBroker` CH-16, `IdempotencyGuard` CH-17,
`OperationalController` CH-18).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-17-capitulo-18-operational-controller.md` (precedente inmediato: mismo tipo de capítulo
  del Amendment v1.1, sin nombre literal en la Constitution — mismo tratamiento aplicado aquí)
- `2026-09-13-capitulo-09-event-bus.md` (la frontera más importante que trazar: `EventBus` ya cita
  "Audit" entre sus consumidores desacoplados, Article X, sin resolver jamás el mecanismo)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Amendment v1.1 — `P-25`, `INV-E10`, `INV-19`)

---

## 1. Objetivo

Escribir el vigésimo capítulo real de contenido del libro, CH-19 — el sexto componente del Amendment
v1.1 (`constitution/ARCHITECTURE_CONSTITUTION.md`, línea 926+), cubriendo el **Observability &
Governance Plane** (octavo de los 9 "Canonical Enterprise Planes", sexto que este libro cubre — el
mismo tipo de salto no-canónico que ya hicieron `IdempotencyGuard` con el Reliability Plane y
`OperationalController` con el Control Plane). Cierra `P-25` ("Logs, traces, execution ledger and
immutable audit evidence have different purposes and MUST NOT be conflated"), citado sin resolverse
desde `EventBus` (CH-09) y repetido, sin resolverse, en la sección 14 de CH-14, CH-15, CH-16, CH-17 y
CH-18 — CH-18 §19 llegó a nombrar explícitamente este plano como el que "por fin resolvería" esa
deuda. Igual que `IdempotencyGuard` (CH-17) y `OperationalController` (CH-18), **ningún texto
constitucional nombra un componente específico** para esto.

## 2. Alcance (decisión ya tomada antes de escribir, confirmada en el resultado)

Exactamente **1 componente + 1 contrato**:

1. **`AuditLedger`** (`CMP-017`) — nombre sintetizado por este libro (no una cita literal),
   documentado explícitamente como tal en el comentario de `registry/components.yaml` junto a su
   ficha. Evaluado contra alternativas (`AuditTrail`, descartado porque "trail" no compromete
   inmutabilidad estructural; `ComplianceRecorder`, descartado porque implica juzgar cumplimiento,
   algo que este componente nunca hace; `EvidenceStore`, descartado porque subestima que el
   componente produce activamente cada registro, incluido su `contentHash`, no solo lo almacena).
   `owns`: producir y preservar evidencia de auditoría ESTRUCTURALMENTE inmutable (append-only por
   diseño, no por convención — "por ausencia estructural de cualquier función de actualización o
   borrado") para una decisión crítica ya tomada por otro componente, capturando el `VersionSnapshot`
   exacto (`INV-E10`) y el actor/contexto (`INV-19`) del momento de esa decisión, con una garantía de
   integridad verificable (`contentHash`). `does_not_own` (frontera trazada con cuidado contra cinco
   componentes ya existentes, la primera y más importante contra `EventBus`): distribuir el flujo
   general de eventos operacionales (`EventBus`, CMP-009, CH-09 — la distinción central: `EventBus`
   mueve un `AgentEvent` mutable de alto volumen para logs/tracing/debugging/replay/analytics/evals/
   cost analysis/UI; `AuditLedger` produce un subconjunto específico, estructuralmente inmutable, de
   evidencia — nunca el flujo general), tomar la decisión que audita (`PolicyEngine`/
   `OperationalController`/`AdmissionController`/`CredentialBroker` — `AuditLedger` REGISTRA una
   decisión YA TOMADA, nunca la toma ni la modifica), autorizar el acceso de lectura del propio
   ledger (Preview), el mecanismo de almacenamiento WORM real y el algoritmo criptográfico detrás de
   `contentHash` (Preview, infraestructura de borde), y generar `subjectRef`/`versionSnapshot` por sí
   mismo (señales de entrada ya resueltas, mismo patrón que `targetRef` en CH-18).
2. **`AuditRecord`** (`C-029`) — `id: AuditRecordId`, `subjectRef: Text` (referencia opaca a la
   decisión original ya auditada — `PolicyDecision`/`ControlDirective`/`AdmissionDecision`/etc.,
   nunca un campo por tipo posible, mismo argumento que `ControlDirective.targetRef` de CH-18),
   `versionSnapshot: VersionSnapshot` (struct embebida, sin `C-XXX` propio — mismo patrón que
   `ExecutionUsage`/`ControlDirectiveApplication` — con `agentVersion`/`skillVersion: Optional`/
   `policyVersion`/`modelConfigVersion`/`capabilityVersion: Optional`, las cinco versiones exactas
   que `INV-E10` exige por nombre), `actor: ActorId` (reusado de CH-06/CH-18), `context:
   Optional<TraceId>`, `recordedAt: Timestamp`, `contentHash: Text` (garantía de integridad
   verificable). **Primer contrato del libro sin ningún campo de estado/lifecycle y sin ninguna
   función de actualización o borrado** — inmutabilidad estructural, decisión de diseño deliberada y
   documentada explícitamente en el propio capítulo (seccion 3/6/12), no una omisión: introducir un
   `ENUM AuditRecordStatus` habría abierto, por la sola forma del `STRUCT`, la posibilidad conceptual
   de una segunda escritura sobre el mismo registro — exactamente lo que `P-25` prohíbe.
3. **Pseudocódigo**: `recordAuditEntry(subjectRef, versionSnapshot, actor, execution, agentId) ->
   AuditRecord`, autónomo, con una demostración (`demonstrateAuditingADeniedPolicyDecision`) que
   audita una `PolicyDecision` de CH-05 con `outcome = DENY` — mostrando deliberadamente que
   `recordAuditEntry` nunca recibe ni inspecciona la decisión auditada en sí, solo su `subjectRef`
   opaco, para probar que el mecanismo es genérico frente a cualquier tipo de decisión. Se documenta
   en prosa (seccion 9/18) que ningún componente anterior invoca todavía `recordAuditEntry` de
   verdad — deuda de integración explícita, patrón ya establecido por CH-09..CH-18.
4. `consumes: [C-004]`, `produces: [C-010, C-011, C-029]` — ningún componente previo editado
   (`CMP-001`..`CMP-016` intactos); `registry/contracts.yaml` no modifica ningún `STRUCT`/`ENUM`
   existente; `book/chapters/18-operational-controller/chapter.md` solo recibió
   `next_chapter: CH-19`.
5. `AuditLedger` emite `AgentEvent` (`AUDIT_RECORD_CREATED`) **condicionalmente**: solo cuando
   `execution`/`agentId` llegan ambos resueltos a `recordAuditEntry` — y se documenta explícitamente
   (seccion 14) que ese evento, incluso cuando se emite, NUNCA es la evidencia de auditoría misma:
   la evidencia ya quedó escrita en el `AuditRecord` que la función devuelve directamente a quien la
   invoca; el evento es, apenas, una notificación tan mutable y distribuible como cualquier otra.

## 3. Verificación ejecutada (evidencia concreta)

```
./scripts/validate-chapter book/chapters/19-audit-ledger      → OK a la primera
./scripts/validate-retrieval-set book/chapters/19-audit-ledger → OK a la primera
./scripts/validate-contracts / validate-components             → OK (29 contratos, 17 componentes)
rm -rf dist && ./scripts/build-all                              → exit 0
```

20 capítulos reales, todos pasando `validate-chapter`/`validate-retrieval-set` (CH-18 también se
revalidó tras el único cambio de navegación permitido, `next_chapter: CH-19`). `build-mind-map`:
`chapter-19.diagram` con 129 nodos/199 aristas — más que `chapter-18.diagram` (124 nodos/191
aristas), como exige la verificación. Se leyó `scripts/lib/render-diagram.js` (fix de Ghostscript,
CH-16) antes de empezar y no se encontró ningún problema real que justificara modificarlo.

**Web**: `dist/web/chapters/CH-19.html` con SVG inline (`grep -c '<svg'` = 1 en las 20 páginas,
verificado una por una), anchors `id="CMP-017"`/`id="C-029"` presentes, navegación CH-18↔CH-19
verificada en ambos sentidos (`CH-19.html` enlazado desde CH-18 con `href="CH-19.html"`, `CH-18.html`
enlazado desde CH-19 con `href="CH-18.html"`/`href="CH-18.html#CMP-016"`/`href="CH-18.html#C-028"`).
Anchors clave de capítulos anteriores (`CMP-001` en CH-01, `CMP-007` en CH-07, `CMP-008` en CH-08,
`CMP-016` en CH-18) intactos.

**PDF**: con `pypdf`, 495 páginas — más que el build de 19 capítulos (465 páginas, confirmado antes
de escribir este capítulo). Texto extraído contiene, verificado programáticamente, "AuditLedger" y
"AuditRecord".

**Prueba negativa real**: se renombró el campo obligatorio `does_not_own` de `CMP-017` a
`does_not_own_BROKEN` en `registry/components.yaml` (edición dirigida solo a la línea de `CMP-017`,
sin tocar los otros dieciséis componentes). `./scripts/validate-components` falló con `exit 1` y el
mensaje exacto `Componente CMP-017: falta el campo obligatorio "does_not_own"`; `./scripts/build-all`
se detuvo en la etapa de validación con `exit 1` y
`policies/publishing.yaml: unresolved_validation_errors = deny → build detenido.`, sin construir
`dist/`. Se restauró el campo, se confirmó `validate-components: OK (17 componente(s))`, y se
reconstruyó todo desde cero.

**Nota de proceso — una falla real y no relacionada, encontrada y no oculta**: el primer intento de
reconstrucción tras restaurar `registry/components.yaml` falló con `exit 1` en la etapa de
`build-web` (`Error: Could not open ".../dist/.build/mindmap/chapter-13.svg" for writing: No such
file or directory` — una condición de carrera de creación de directorio, sobre un capítulo,
`chapter-13`, que este trabajo nunca tocó). Un segundo intento inmediato, sin cambiar nada, completó
con `exit 0` y conteos idénticos (20 capítulos, 29 contratos, 17 componentes, mismos nodos/aristas
por capítulo, 495 páginas de PDF) — consistente con una falla transitoria de E/S del entorno, no con
un defecto de `scripts/lib/render-diagram.js` ni de ningún archivo de este capítulo. Documentado aquí
explícitamente, sin ocultarlo, y sin modificar `render-diagram.js` sin una causa real que lo
justificara.

## 4. Deuda intencional hacia el próximo capítulo

- **El cableado real hacia `recordAuditEntry`**: `PolicyEngine` (CH-05), `OperationalController`
  (CH-18), `AdmissionController` (CH-14), `CredentialBroker` (CH-16), `IdempotencyGuard` (CH-17) y
  `AgentCommunicationGateway` (CH-15) no invocan todavía, de verdad, `recordAuditEntry` sobre sus
  propias decisiones.
- **El mecanismo real y durable de almacenamiento append-only/WORM**: no modelado, Preview.
- **El algoritmo criptográfico real detrás de `contentHash`, y su verificación posterior**
  (`verifyAuditRecord` o equivalente): no construido.
- **La generación real de `subjectRef` y `VersionSnapshot`**: asumidas como señales de entrada ya
  resueltas, no modeladas.
- **El concepto de "skill" como entidad propia**: `INV-E10` lo nombra literalmente, pero ningún
  contrato de este libro lo modela todavía — `VersionSnapshot.skillVersion` queda `Optional<Text>`
  opaco.
- **Autorización de lectura sobre el propio ledger**: señalado explícitamente, no resuelto.
- **Los tres planos restantes** del Amendment v1.1 (Execution Plane, Data & Context Plane, Execution
  Fabric): candidatos para los próximos incrementos.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
