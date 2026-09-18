# Plan / Registro de ejecución — Capítulo 18: OperationalController y los Kill Switches Independientes de AgentLoop

**Fecha:** 2026-09-17
**Estado:** ✅ Completado, sobre el estado dejado por `cfe5a1c` (CH-00..CH-17 como los dieciocho
únicos capítulos reales; cuatro componentes del Amendment v1.1 ya instanciados:
`AdmissionController` CH-14, `AgentCommunicationGateway` CH-15, `CredentialBroker` CH-16,
`IdempotencyGuard` CH-17).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-17-capitulo-17-idempotency-guard.md` (precedente inmediato: mismo tipo de capítulo del
  Amendment v1.1, sin nombre literal en la Constitution — mismo tratamiento aplicado aquí)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Amendment v1.1 — `P-30`, `INV-E14`, "Canonical
  Enterprise Planes")

---

## 1. Objetivo

Escribir el decimonoveno capítulo real de contenido del libro, CH-18 — el quinto componente del
Amendment v1.1 (`constitution/ARCHITECTURE_CONSTITUTION.md`, línea 926+), cubriendo el **Control
Plane** (sexto de los 9 "Canonical Enterprise Planes", quinto que este libro cubre — el mismo tipo
de salto no-canónico que ya hizo `IdempotencyGuard` con el Reliability Plane, séptimo en la
enumeración pero cuarto que el libro cubrió). Igual que `IdempotencyGuard` (CH-17), **ningún texto
constitucional nombra un componente específico** para esto — `P-30`/`INV-E14` exigen la propiedad
(cancelación, deshabilitación de capabilities, aislamiento de tenant, rollback de rollout y kill
switches, todos "sin depender de la cooperación del modelo", y los kill switches en particular
"independientemente de `AgentLoop`") sin asignarle un dueño con nombre propio.

## 2. Alcance (decisión ya tomada antes de escribir, confirmada en el resultado)

Exactamente **1 componente + 1 contrato**:

1. **`OperationalController`** (`CMP-016`) — nombre sintetizado por este libro (no una cita
   literal), documentado explícitamente como tal en el comentario de `registry/components.yaml`
   junto a su ficha. Evaluado contra alternativas (`KillSwitchController`, que solo habría cubierto
   una de las cuatro capacidades de `P-30`; `ControlPlaneGateway`, que habría sugerido
   incorrectamente un rol de adaptador de protocolo como `AgentCommunicationGateway`). `owns`: las
   cuatro capacidades de `P-30` que no le pertenecen ya a `ExecutionController` — deshabilitar una
   capability (a nivel de `CapabilityDescriptor`, `C-018`), aislar todos los runs de un tenant,
   revertir un rollout (reusando `CapabilityDescriptor.version`, sin sistema de versiones nuevo), y
   forzar un kill switch (cita literal `INV-E14`) — más el fail-closed de rechazar reaplicar un
   `ControlDirective` ya `APPLIED` y de rechazar un kill switch sobre un `AgentRun` ya terminal.
   `does_not_own` (cinco fronteras, la primera y más importante contra `ExecutionController`):
   decidir si UN `AgentRun` específico puede seguir contra su `ExecutionBudget` evaluado desde
   DENTRO de su propio ciclo (`ExecutionController`, CH-07 — la distinción central del capítulo:
   "¿puedo seguir intentando, evaluado desde dentro?" nunca es "¿debe el control externo forzar el
   fin, desde afuera, sin pedir cooperación?"), autorizar una acción (`PolicyEngine`, CH-05),
   resolver una implementación (`CapabilityRegistry`, CH-08), ejecutar el side effect
   (`ToolRuntime`, CH-02), y el mecanismo real y distribuido de enforcement (Preview,
   infraestructura de borde).
2. **`ControlDirective`** (`C-028`) — `id`, `type: ControlDirectiveType` (ENUM
   `DISABLE_CAPABILITY`/`ISOLATE_TENANT`/`ROLLBACK`/`KILL_SWITCH`, cita literal de `P-30` —
   deliberadamente sin un quinto valor `CANCELLATION`, porque esa palabra de `P-30` ya tiene dueño
   en `ExecutionController`, y `KILL_SWITCH` es, precisamente, la forma en que este componente
   provee la mitad externa de "cancellation"), `targetRef: Text` (referencia opaca única —
   capabilityId/tenantId/versión de rollout/runId según `type`, evaluado explícitamente contra
   cuatro campos `Optional` separados y descartado por la misma razón que ya usó
   `IdempotencyRecord.result` en CH-17), `issuedBy: ActorId` (reusado de CH-06 §6, no un tipo
   nuevo), `status: ControlDirectiveStatus` (ENUM `ISSUED`/`APPLIED` — **nunca un Boolean**: la
   ventana entre "comando emitido" y "comando con efecto real" es información real que un booleano
   colapsaría), `issuedAt`, `appliedAt: Optional<Timestamp>`.
3. **El caso límite del "empate" con `ExecutionController`, resuelto explícitamente (no dejado
   ambiguo)**: `AgentRunStatus` es terminal-una-vez (Article V); la regla es "quien escribe primero
   sobre un `AgentState` todavía no terminal, gana", y `applyControlDirective` la hace cumplir
   rechazando (fail-closed, `KILL_SWITCH_ON_TERMINAL_AGENT_STATE`) forzar un kill switch sobre un
   run que ya alcanzó un estado terminal por cualquier otra vía. En la práctica, a través de los
   dieciocho capítulos reales de este libro, el kill switch SIEMPRE gana hoy — no por una prioridad
   abstracta, sino porque `OperationalController` es la única de las dos vías que este libro ha
   cableado hasta escribir `AgentState.status` de verdad (`ExecutionController`, CH-07 §18, sigue
   dejando esa escritura como Preview).
4. **Primer componente distinto de `AgentLoop` que escribe, con pseudocódigo real, una transición
   de `AgentRunStatus`**: `applyControlDirective`, para `KILL_SWITCH`, construye directamente un
   `AgentState` nuevo con `status = CANCELLED`, sin invocar `evaluateExecutionContinuation` (CH-07)
   ni ningún turno de `AgentLoop` (CH-01) — la materialización literal de `INV-E14`. Se documenta en
   el propio capítulo (seccion 3/12) que esto matiza, sin contradecir, la afirmación de CH-07 §12
   ("AgentRunStatus es propiedad exclusiva de AgentLoop") — el camino cooperativo del lifecycle
   sigue siendo exclusivo de `AgentLoop`; la Constitution exige, por diseño, una segunda vía no
   cooperativa hacia el mismo destino terminal, disparada únicamente por un `KILL_SWITCH`.
5. `consumes: [C-003, C-004]`, `produces: [C-010, C-011, C-028]` — ningún componente previo
   editado (`CMP-001`..`CMP-015` intactos); `registry/contracts.yaml` de `C-003`/`C-004`/`C-013`
   solo actualiza su lista `used_by` para incluir `CMP-016` (sin cambiar ningún `STRUCT`/`ENUM`);
   `book/chapters/17-idempotency-guard/chapter.md` solo recibió `next_chapter: CH-18`.
6. `OperationalController` emite `AgentEvent` (`CONTROL_DIRECTIVE_APPLIED`) **condicionalmente**:
   solo para `KILL_SWITCH` aplicado con éxito (el único de los cuatro tipos cuyo alcance es un
   único `AgentRun` con `ExecutionContext` genuino) — nunca para `DISABLE_CAPABILITY`/
   `ISOLATE_TENANT`/`ROLLBACK`, cuyo alcance es más amplio que un run y para los cuales no existe un
   `runId`/`sessionId`/`traceId` honesto que emitir. Limitación hacia `INV-18` señalada
   explícitamente en la seccion 14/18, no silenciada.

## 3. Verificación ejecutada (evidencia concreta)

```
./scripts/validate-chapter book/chapters/18-operational-controller      → OK a la primera
./scripts/validate-retrieval-set book/chapters/18-operational-controller → OK a la primera
./scripts/validate-contracts / validate-components                      → OK (28 contratos, 16 componentes)
rm -rf dist && ./scripts/build-all                                      → exit 0
```

19 capítulos reales, todos pasando `validate-chapter`/`validate-retrieval-set`. `build-mind-map`:
`chapter-18.diagram` con 124 nodos/191 aristas — más que `chapter-17.diagram` (116 nodos/179
aristas), como exige la verificación. `dist/book.pdf` se generó con el fix de
`scripts/lib/render-diagram.js` (normalización con Ghostscript, CH-16) sin necesidad de tocarlo de
nuevo — se leyó el script antes de empezar y no se encontró ningún problema real que justificara
modificarlo.

**Web**: `dist/web/chapters/CH-18.html` con SVG inline (`grep -c '<svg'` = 1, igual que las otras 18
páginas, verificado una por una), anchors `id="CMP-016"`/`id="C-028"` presentes, navegación
CH-17↔CH-18 verificada en ambos sentidos (`CH-18.html` enlazado desde CH-17, `CH-17.html` enlazado
desde CH-18). Anchors clave de capítulos anteriores (`CMP-001` en CH-01, `CMP-007` en CH-07,
`CMP-008` en CH-08) intactos.

**PDF**: con `pypdf`, 465 páginas — más que el build de 18 capítulos (433 páginas, confirmado antes
de escribir este capítulo). Texto extraído contiene "OperationalController" y "ControlDirective"
(verificado programáticamente, no solo visualmente).

**Prueba negativa real**: se renombró el campo obligatorio `does_not_own` de `CMP-016` a
`does_not_own_BROKEN` en `registry/components.yaml`. `./scripts/validate-components` falló con
`exit 1` y el mensaje exacto `Componente CMP-016: falta el campo obligatorio "does_not_own"`;
`./scripts/build-all` se detuvo en la etapa de validación con `exit 1` y
`policies/publishing.yaml: unresolved_validation_errors = deny → build detenido.`, sin construir
`dist/`. Se restauró el archivo desde una copia de respaldo, se confirmó `validate-components: OK
(16 componente(s))`, y se reconstruyó todo desde cero: `build-all` con `exit 0` y conteos idénticos
al build limpio original (19 capítulos, 28 contratos, 16 componentes, mismos nodos/aristas por
capítulo en el mapa mental, 465 páginas de PDF).

## 4. Deuda intencional hacia el próximo capítulo

- **El cableado real `CapabilityRegistry ↔ OperationalController`**: `resolveToolCall` (CH-08) no
  consulta todavía si una capability tiene un `ControlDirective` `APPLIED` de tipo
  `DISABLE_CAPABILITY` antes de resolverla.
- **El mecanismo real y distribuido de aislamiento de tenant y de rollback de rollout**: ningún
  pseudocódigo de este libro bloquea, todavía, ningún `AgentRun` en curso de un tenant aislado, ni
  redespliega realmente una versión anterior de una capability.
- **Quién está autorizado a emitir un `ControlDirective`**: `issueControlDirective` recibe
  `issuedBy: ActorId` ya resuelto, sin verificar si ese actor tiene autoridad real — señalado
  explícitamente como fuera de alcance (suena a `PolicyEngine`, pero cablearlo queda para después).
- **La observabilidad completa de `DISABLE_CAPABILITY`/`ISOLATE_TENANT`/`ROLLBACK`**: sin
  `AgentEvent` real, limitación hacia `INV-18` documentada explícitamente, no resuelta.
- **Ausencia de evidencia de auditoría real** (`P-25`): igual que en CH-14..CH-17, señalada, no
  resuelta.
- **Los cuatro planos restantes** del Amendment v1.1 (Execution, Data & Context, Observability &
  Governance, Execution Fabric): candidatos para los próximos incrementos.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
