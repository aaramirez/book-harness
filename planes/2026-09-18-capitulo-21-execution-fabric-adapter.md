# Plan / Registro de ejecución — Capítulo 21: ExecutionFabricAdapter y la Topología de Despliegue que el Comportamiento del Agente Nunca Debe Conocer

**Fecha:** 2026-09-18
**Estado:** ✅ Completado, sobre el estado dejado por `8d75e1a` (CH-00..CH-20 como los veintiún únicos
capítulos reales; siete componentes del Amendment v1.1 ya instanciados: `AdmissionController` CH-14,
`AgentCommunicationGateway` CH-15, `CredentialBroker` CH-16, `IdempotencyGuard` CH-17,
`OperationalController` CH-18, `AuditLedger` CH-19, `DataGovernanceEngine` CH-20).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-18-capitulo-20-data-governance-engine.md` (precedente inmediato: mismo tipo de capítulo
  del Amendment v1.1, sin nombre literal en la Constitution — mismo tratamiento aplicado aquí; y el
  capítulo cuya sección 19 ya identificaba el Execution Fabric como uno de los dos planos restantes)
- `2026-09-14-capitulo-07-execution-controller.md` (la frontera más importante a trazar:
  `ExecutionController` ya posee "cuánto puede consumir un run"; este capítulo agrega "sobre qué
  substrato corre", una pregunta ortogonal)
- `2026-09-14-capitulo-11-agent-core.md` (la frontera más precisa: `AgentCore` ya posee instanciar el
  `AgentState`/`ExecutionContext` inicial de un run; este capítulo describe el substrato de un run YA
  instanciado, nunca lo crea)
- `2026-09-13-capitulo-03-model-gateway.md` (contraste de dirección de adaptación: `ModelGateway`
  adapta HACIA AFUERA, hacia un proveedor de modelo; este capítulo adapta HACIA ABAJO, hacia el
  substrato de cómputo del propio harness)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Amendment v1.1 — `P-27`, línea 963; "Canonical
  Enterprise Planes", línea 991+)

---

## 1. Objetivo

Escribir el vigesimosegundo capítulo real de contenido del libro, CH-21 — el octavo componente del
Amendment v1.1, cubriendo el **Execution Fabric** (noveno y último de los 9 "Canonical Enterprise
Planes"). Materializa, por primera vez con código real, `P-27` ("Deployment topology is independent
from agent semantics") — un principio que, a diferencia de `P-22` (citado en prosa desde CH-10/CH-11
antes de resolverse) o `P-25` (citado en prosa desde CH-09), nunca había sido citado con código real
por ningún capítulo anterior; solo existía como el nombre de un plano en la lista de "Canonical
Enterprise Planes" transcrita en CH-00 §5. Igual que `IdempotencyGuard` (CH-17), `OperationalController`
(CH-18), `AuditLedger` (CH-19) y `DataGovernanceEngine` (CH-20), **ningún texto constitucional nombra
un componente específico** para esto. Con este capítulo, los nueve planos canónicos de Amendment v1.1
quedan, todos, cubiertos por al menos un capítulo real de este libro.

## 2. Alcance (decisión ya tomada antes de escribir, confirmada en el resultado)

Exactamente **1 componente + 1 contrato**:

1. **`ExecutionFabricAdapter`** (`CMP-019`) — nombre sintetizado por este libro (no una cita literal),
   evaluado contra alternativas (`DeploymentTopologyAdapter`, descartado porque "Deployment" evoca con
   demasiada fuerza el proceso de release/CI-CD de una versión de software, un dominio ya cercano al
   de `OperationalController`/`ROLLOUT_ROLLBACK`, CH-18; `ExecutionSubstrate`, descartado porque nombra
   correctamente el contrato de datos resultante, pero no transmite que existe un componente activo
   que produce y empaqueta esa descripción de forma uniforme — un `STRUCT` puede llamarse
   `ExecutionSubstrate`, un `COMPONENT` necesita un nombre que comunique una acción). `owns`: abstraer
   el substrato de cómputo concreto sobre el que corre un run ya existente (in-process, worker,
   Kubernetes, serverless, cloud, edge, on-premise) detrás de una interfaz uniforme (`P-27` literal);
   producir una referencia opaca al recurso de cómputo concreto; registrar, cuando aplica, una
   restricción de residencia sobre el CÓMPUTO. `does_not_own` (frontera trazada contra cinco
   componentes ya existentes): decidir límites de recursos/presupuesto de un run
   (`ExecutionController`, CMP-007, CH-07 — la frontera más importante: `ExecutionController` decide
   CUÁNTO puede consumir un run; `ExecutionFabricAdapter` decide DÓNDE/EN QUÉ TIPO DE INFRAESTRUCTURA
   corre ese mismo run); invocar proveedores de modelo (`ModelGateway`, CMP-003, CH-03 — adapta hacia
   afuera, no hacia abajo); adaptar protocolos de comunicación entre agentes externos
   (`AgentCommunicationGateway`, CMP-013, CH-15); **instanciar el `AgentState` inicial de un run**
   (`AgentCore`, CMP-011, CH-11 — la frontera más precisa: `ExecutionFabricAdapter` describe sobre qué
   corre un run YA instanciado, nunca lo crea); clasificar requisitos de gobernanza de un dato
   (`DataGovernanceEngine`, CMP-018, CH-20 — residencia del DATO vs. residencia del CÓMPUTO); ejecutar
   el aprovisionamiento/scheduling real (Preview, infraestructura de borde).
2. **`ExecutionPlacement`** (`C-031`) — `id`, `runId: RunId` (el identificador YA EXISTENTE desde
   CH-00 — decisión evaluada explícitamente contra el patrón `subjectRef: Text` opaco de
   `AuditRecord`/`DataGovernanceLabel`, y descartado porque el universo que este contrato describe es
   siempre exactamente un run, nunca un tipo heterogéneo de dato), `topology: DeploymentTopology`
   (`ENUM` de siete valores citados literalmente de `P-27`:
   `IN_PROCESS`/`WORKER`/`KUBERNETES`/`SERVERLESS`/`CLOUD`/`EDGE`/`ON_PREMISE`), `computeResourceRef:
   Optional<Text>`, `residencyConstraint: Optional<Text>` (evaluado explícitamente contra reusar
   `DataGovernanceLabel.residencyRequirement`, CH-20, y descartado: describen sujetos distintos —
   dónde debe residir el CÓMPUTO vs. dónde debe residir el DATO — relacionados en la práctica pero no
   intercambiables por diseño), `resolvedAt: Timestamp`.
3. **Pseudocódigo**: `resolveExecutionPlacement(runId, topology, computeResourceRef,
   residencyConstraint, execution, agentId) -> ExecutionPlacement` (fail-closed hacia un
   `HarnessError` cuando `runId` está ausente — único código de fallo real, a diferencia de los dos de
   `classifyData` en CH-20, porque `topology` llega tipada como un `ENUM` cerrado sin valor "vacío"
   posible, y `computeResourceRef`/`residencyConstraint` son `Optional` por diseño) más una
   demostración (`demonstrateAssociatingAnExecutionContextWithItsPlacement`) que asocia un
   `ExecutionContext` real de CH-00/CH-11 con un `ExecutionPlacement` — sin invocar ni modificar
   `AgentLoop.runTurn` (CH-01) ni `AgentCore.instantiateAgentState` (CH-11). Se documenta en prosa
   (seccion 9/18) que ningún componente anterior invoca todavía `resolveExecutionPlacement` de
   verdad — deuda de integración explícita, patrón ya establecido por CH-09..CH-20.
4. `consumes: [C-004]`, `produces: [C-010, C-011, C-031]` — ningún componente previo editado
   (`CMP-001`..`CMP-018` intactos, incluidos `CMP-007 ExecutionController` y `CMP-011 AgentCore`);
   `registry/contracts.yaml` no modifica ningún `STRUCT`/`ENUM` existente (`C-012 ExecutionBudget` y
   `C-030 DataGovernanceLabel` quedan intactos); `book/chapters/20-data-governance-engine/chapter.md`
   solo recibió `next_chapter: CH-21`.
5. `ExecutionFabricAdapter` emite `AgentEvent` desde una única función
   (`EXECUTION_PLACEMENT_RESOLVED`), condicionalmente: solo cuando `execution`/`agentId` llegan ambos
   resueltos — y se documenta explícitamente (seccion 14) que ese evento nunca es evidencia de
   auditoría inmutable (frontera con `AuditLedger`, CH-19).

## 3. Corrección editorial explícita sobre CH-20

CH-20 §0/§19 contó, entre los planos "sin cubrir por este libro", tanto el **Execution Plane**
(segundo canónico) como el **Execution Fabric** (noveno canónico) — conflacionando, sin proponérselo,
dos planos distintos. Este capítulo corrige esa cuenta explícitamente en su propia apertura: el
Execution Plane (continuación de turno, ejecución de tool calls, invocación de modelo, autorización,
presupuesto de ejecución) ya estaba cubierto, con código real, desde el propio núcleo de BH-v0.1
(`AgentLoop` CH-01, `ToolRuntime` CH-02, `ModelGateway` CH-03, `PolicyEngine` CH-05,
`ExecutionController` CH-07) — mucho antes de que Amendment v1.1 nombrara ese plano. Lo único que
realmente permanecía sin cubrir, hasta este capítulo, era el Execution Fabric — el plano que protege
`P-27`, nunca antes citado con código real por ningún capítulo de este libro.

## 4. Verificación ejecutada (evidencia concreta)

```
./scripts/validate-chapter book/chapters/21-execution-fabric-adapter      → OK a la primera
    (22/19 secciones, 7 bloques pseudocode, 1 contrato introducido, 1 componente introducido)
./scripts/validate-retrieval-set book/chapters/21-execution-fabric-adapter → OK a la primera
    (guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2, interleavedQuestions: 3
    — CH-07/CH-11/CH-03 — flashcards: 5, calibrationPairs: 4)
./scripts/validate-components / validate-contracts                        → OK
    (19 componentes, 31 contratos)
./scripts/validate-chapter book/chapters/20-data-governance-engine        → OK (revalidado tras
    el único cambio de navegación permitido, next_chapter: CH-21)
rm -rf dist && ./scripts/build-all                                        → exit 0
```

22 capítulos reales, todos pasando `validate-chapter`/`validate-retrieval-set`. `build-mind-map`:
`chapter-21.diagram` con 141 nodos/217 aristas — más que `chapter-20.diagram` (135 nodos/208 aristas),
como exige la verificación. Se leyó `scripts/lib/render-diagram.js` (fix de Ghostscript, CH-16) antes
de empezar y no se encontró ningún problema real que justificara modificarlo.

**Web**: `dist/web/chapters/CH-21.html` con SVG inline (`grep -c '<svg'` = 1 en las 22 páginas,
verificado una por una), anchors `id="CMP-019"`/`id="C-031"` presentes, navegación CH-20↔CH-21
verificada en ambos sentidos (`href="CH-21.html"` desde CH-20, `href="CH-20.html"` desde CH-21).
Anchors clave de capítulos anteriores (`CMP-001` en CH-01, `CMP-007` en CH-07, `CMP-011` en CH-11,
`CMP-018` en CH-20) intactos.

**PDF**: con `pypdf`, más páginas que el build de 21 capítulos (529 páginas). Texto extraído contiene,
verificado programáticamente, "ExecutionFabricAdapter" y "ExecutionPlacement".

**Prueba negativa real**: se renombró el campo obligatorio `does_not_own` de `CMP-019` a
`does_not_own_BROKEN` en `registry/components.yaml` (edición dirigida solo a la ficha de `CMP-019`,
sin tocar los otros dieciocho componentes). `./scripts/validate-components` falló con `exit 1` y el
mensaje exacto `Componente CMP-019: falta el campo obligatorio "does_not_own"`;
`./scripts/build-all` se detuvo en la etapa de validación con `exit 1` real (confirmado con `$?`, no
inferido de un pipe) y `policies/publishing.yaml: unresolved_validation_errors = deny → build
detenido.`, sin construir `dist/`. Se restauró el campo desde una copia de respaldo, se confirmó
`validate-components: OK (19 componente(s))`, y se reconstruyó todo desde cero: mismos 22 capítulos,
31 contratos, 19 componentes, mismos nodos/aristas por capítulo (141/217 en CH-21), mismo número de
páginas de PDF — conteos idénticos al build previo a la prueba negativa.

## 5. Decisiones de diseño no cubiertas en el encargo original

- **`ExecutionPlacement.runId` como `RunId` tipado, no `subjectRef: Text` opaco**: se evaluó
  explícitamente seguir el patrón de `AuditRecord`/`DataGovernanceLabel` (una referencia opaca
  genérica, porque el universo referenciado es heterogéneo) y se descartó porque, para este contrato,
  el universo referenciado es homogéneo — siempre exactamente un run — así que usar `Text` opaco
  habría renunciado, sin necesidad, a la verificación de tipos que `RunId` ya provee.
- **Un único código de fallo real** (`EXECUTION_FABRIC_PLACEMENT_MISSING_RUN_ID`), a diferencia de los
  dos de `classifyData` (CH-20): documentado explícitamente en la seccion 11 como una diferencia
  legítima, no una inconsistencia — `topology` es un `ENUM` cerrado sin estado "vacío" posible, y
  `computeResourceRef`/`residencyConstraint` son `Optional` por diseño, así que su ausencia nunca es
  un error.
- **Frontera `residencyConstraint` vs. `DataGovernanceLabel.residencyRequirement`**: se convirtió en
  el hilo narrativo secundario del capítulo (seccion 2/5/6/8/15) y en un `explainPrompt` completo
  (`EP-CH21-02`) — un run puede tener una restricción de residencia sobre su cómputo sin que ningún
  dato específico que procese la tenga, y viceversa; los dos campos nunca se colapsan en uno solo.
- **Corrección explícita sobre CH-20 §0/§19** respecto de qué planos quedaban "sin cubrir" (ver
  seccion 3 de este documento y la apertura del propio capítulo): decisión no anticipada por el
  encargo original, mencionada como interpretación explícita en el Paso 5 del encargo, y adoptada
  como marco narrativo consistente con el resto del capítulo.
- **`DeploymentTopology` con los siete valores literales de `P-27`** (incluyendo `CLOUD`, que el
  encargo original mencionaba solo como ejemplo abreviado): se incluyeron los siete para no perder,
  sin justificación, ninguna distinción que la propia enmienda ya nombra por su nombre exacto.

## 6. Deuda intencional hacia el próximo capítulo

- **El cableado real hacia `resolveExecutionPlacement`**: `AgentCore` (CH-11) no invoca todavía, de
  verdad, esta función tras crear cada run nuevo.
- **Cuál `ExecutionPlacement` es "el vigente"** para un `runId` dado cuando existen varios producidos
  en momentos distintos (p. ej. tras un rebalanceo de infraestructura): no modelado, Preview — mismo
  límite abierto que "cuál `DataGovernanceLabel` es el vigente" (CH-20 §18).
- **El motor real de asignación de topología**: quién decide, en la práctica, a qué substrato debe
  asignarse un run nuevo — asumido, no modelado.
- **El mecanismo real de aprovisionamiento/scheduling**: Preview, infraestructura de borde.
- **Autorización de lectura/escritura sobre las propias descripciones de topología**, e `INV-E07`: no
  resuelto — mismo límite abierto que `AuditLedger` (CH-19) y `DataGovernanceEngine` (CH-20) dejaron
  para sus propios registros.
- **Auditar una resolución de topología con `AuditLedger`**: ningún cableado real conecta todavía
  `ExecutionFabricAdapter` con `recordAuditEntry`.
- **La interacción con `OperationalController`** sobre aislamiento de tenant por substrato: señalado
  en prosa, no construido.

## 7. Nota de cierre — los nueve planos canónicos de Amendment v1.1, completos

Con CH-21, los 9 "Canonical Enterprise Planes" de Amendment v1.1 quedan todos cubiertos por al menos
un capítulo real de este libro:

1. **Ingress & Activation Plane** → CH-14 (`AdmissionController`, CMP-012)
2. **Execution Plane** → cubierto por el core BH-v0.1 (CH-01 `AgentLoop`, CH-02 `ToolRuntime`, CH-03
   `ModelGateway`, CH-05 `PolicyEngine`, CH-07 `ExecutionController`) — ver seccion 3 de este
   documento para la corrección explícita sobre lo que CH-20 §0/§19 había contado como "sin cubrir"
3. **Agent Interoperability Plane** → CH-15 (`AgentCommunicationGateway`, CMP-013)
4. **Capability & Integration Plane** → CH-16 (`CredentialBroker`, CMP-014)
5. **Data & Context Plane** → CH-20 (`DataGovernanceEngine`, CMP-018)
6. **Control Plane** → CH-18 (`OperationalController`, CMP-016)
7. **Reliability Plane** → CH-17 (`IdempotencyGuard`, CMP-015)
8. **Observability & Governance Plane** → CH-19 (`AuditLedger`, CMP-017)
9. **Execution Fabric** → CH-21 (`ExecutionFabricAdapter`, CMP-019)

Ningún plano está construido de punta a punta (el cableado real de integración entre los componentes
de cada plano y el núcleo de BH-v0.1 sigue siendo, en su gran mayoría, deuda explícita para capítulos
futuros — ver seccion 6), pero los nueve tienen, cada uno, al menos un componente real con código,
contrato, pseudocódigo y ficha de `owns`/`does_not_own` propia.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
