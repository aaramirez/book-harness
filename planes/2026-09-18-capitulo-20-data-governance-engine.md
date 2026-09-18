# Plan / Registro de ejecución — Capítulo 20: DataGovernanceEngine y la Etiqueta de Gobernanza que Viaja con el Dato

**Fecha:** 2026-09-18
**Estado:** ✅ Completado, sobre el estado dejado por `e1da467` (CH-00..CH-19 como los veinte únicos
capítulos reales; seis componentes del Amendment v1.1 ya instanciados: `AdmissionController` CH-14,
`AgentCommunicationGateway` CH-15, `CredentialBroker` CH-16, `IdempotencyGuard` CH-17,
`OperationalController` CH-18, `AuditLedger` CH-19).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-17-capitulo-19-audit-ledger.md` (precedente inmediato: mismo tipo de capítulo del
  Amendment v1.1, sin nombre literal en la Constitution — mismo tratamiento aplicado aquí)
- `2026-09-13-capitulo-04-context-engine.md` (la frontera más importante que trazar: `ContextEngine`
  ya separó "relevante" de "autorizado a verse"; este capítulo agrega la tercera pregunta,
  "¿qué requisitos de gobierno aplican?")
- `2026-09-14-capitulo-16-credential-broker.md` (el precedente narrow que generalizar: CH-16 ya
  materializó `P-22` para un secreto y dejó, en su propia sección 18, la generalización a "cualquier
  dato empresarial gobernado" como trabajo explícito de un capítulo futuro del Data & Context Plane)
- `constitution/ARCHITECTURE_CONSTITUTION.md` (Amendment v1.1 — `P-22`, `INV-E11`, línea 926+)

---

## 1. Objetivo

Escribir el vigesimoprimer capítulo real de contenido del libro, CH-20 — el séptimo componente del
Amendment v1.1, cubriendo el **Data & Context Plane** (quinto de los 9 "Canonical Enterprise Planes",
séptimo que este libro cubre — el mismo tipo de salto no-canónico que ya hicieron `IdempotencyGuard`,
`OperationalController` y `AuditLedger`). Generaliza `P-22` ("Enterprise data is governed throughout
its lifecycle") e `INV-E11` ("Data governance policy follows context and artifacts across component
boundaries") más allá del único mecanismo previo (`CredentialClassification`, CH-16, exclusivo de un
secreto) hacia cualquier dato que fluya por el sistema. Igual que `IdempotencyGuard` (CH-17),
`OperationalController` (CH-18) y `AuditLedger` (CH-19), **ningún texto constitucional nombra un
componente específico** para esto.

## 2. Alcance (decisión ya tomada antes de escribir, confirmada en el resultado)

Exactamente **1 componente + 1 contrato**:

1. **`DataGovernanceEngine`** (`CMP-018`) — nombre sintetizado por este libro (no una cita literal),
   evaluado contra alternativas (`DataClassifier`, descartado porque "Classifier" sugiere solo
   clasificación, sin transmitir residencia/retención/legal-hold/lineage — la mitad restante de
   `P-22`; `ComplianceEngine`, descartado porque implica juzgar cumplimiento regulatorio activo, un
   dominio distinto, y porque "Engine" junto a "Compliance" invita a confundirlo con `PolicyEngine`).
   `owns`: clasificar cualquier dato que fluya por el sistema (un `ContextBlock` de CH-04, un
   `ToolResult` de CH-02) con clasificación/residencia/retención/legal-hold/lineage, de forma
   independiente del razonamiento del modelo (`P-22` literal, mismo espíritu que `P-13` aplicado a
   datos en vez de a acciones); producir una etiqueta portátil (`INV-E11` literal); decidir si un
   borrado programado ya es exigible, sin ejecutar el borrado real. `does_not_own` (frontera trazada
   contra cinco componentes ya existentes): seleccionar/rankear/componer qué contexto es relevante
   (`ContextEngine`, CMP-004, CH-04 — la frontera más importante: `ContextEngine` decide QUÉ entra;
   `DataGovernanceEngine` decide QUÉ REQUISITOS aplican a lo que ya se decidió incluir); autorizar
   visibilidad (`PolicyEngine`, CMP-005, CH-05); **reclasificar un secreto ya clasificado por
   `CredentialBroker`** (CMP-014, CH-16 — la frontera más precisa: `CredentialClassification`,
   `ENUM` de dos valores exclusivo de secretos, sigue intacta y sin tocar; `DataGovernanceEngine`
   generaliza `P-22` al resto del universo de datos, nunca reclasifica una credencial); producir
   evidencia de auditoría inmutable (`AuditLedger`, CMP-017, CH-19); aislar tenants
   (`OperationalController`, CMP-016, CH-18); ejecutar el borrado/cifrado/residencia física reales
   (Preview, infraestructura de borde).
2. **`DataGovernanceLabel`** (`C-030`) — `id`, `subjectRef: Text` (referencia opaca al dato
   gobernado, mismo patrón que `AuditRecord.subjectRef`/`ControlDirective.targetRef`),
   `classification: DataClassificationLevel` (`ENUM` de cuatro valores, `PUBLIC`/`INTERNAL`/
   `CONFIDENTIAL`/`RESTRICTED` — nunca un `Boolean`, y deliberadamente distinto del `ENUM` de dos
   valores de `CredentialClassification`, CH-16, evaluado y descartado explícitamente como reuso),
   `residencyRequirement: Optional<Text>`, `retentionDeadline: Optional<Timestamp>`,
   `legalHold: Boolean`, `lineageRef: Optional<Text>`, `classifiedAt: Timestamp`. Evaluado contra
   alternativas de nombre (`DataClassification`, descartado por subestimar el alcance — solo
   clasificación, sin residencia/retención/legal-hold/lineage; `GovernanceTag`, descartado porque
   "tag" connota algo ligero e informal, subestimando que este contrato encapsula obligaciones
   exigibles). Deliberadamente sin campo `actor` (a diferencia de `AuditRecord`, CH-19): describe una
   propiedad del dato, no evidencia de quién decidió qué — documentado explícitamente en la seccion 6
   del capítulo. Sin ningún campo de estado/lifecycle — pero por una razón distinta a la de
   `AuditRecord` (CH-19): el cambio se modela por reemplazo (una invocación nueva de `classifyData`
   produce una etiqueta nueva), no porque una segunda escritura sea estructuralmente imposible.
3. **Pseudocódigo**: `classifyData(subjectRef, provenance, legalHold, execution, agentId) ->
   DataGovernanceLabel` (fail-closed hacia `RESTRICTED` cuando ninguna regla de gobernanza aplica,
   mismo principio que `evaluatePolicyForToolCall`, CH-05) y `enforceRetention(label, evaluatedAt,
   execution, agentId) -> RetentionEnforcementResult` (evalúa `legalHold` ANTES de comparar
   `retentionDeadline`, y nunca borra ni reemplaza ese plazo original — la interacción legal-
   hold/retención documentada con cuidado, seccion 11), más una demostración
   (`demonstrateClassifyingAContextBlock`) que clasifica un `ContextBlock` real de CH-04 usando su
   `provenance` — sin invocar ni modificar `ContextEngine.assembleContextSnapshot`. Se documenta en
   prosa (seccion 9/18) que ningún componente anterior invoca todavía `classifyData`/
   `enforceRetention` de verdad — deuda de integración explícita, patrón ya establecido por
   CH-09..CH-19.
4. `consumes: [C-004]`, `produces: [C-010, C-011, C-030]` — ningún componente previo editado
   (`CMP-001`..`CMP-017` intactos, incluido `CMP-014 CredentialBroker`); `registry/contracts.yaml`
   no modifica ningún `STRUCT`/`ENUM` existente (`C-026 CredentialReference` y
   `CredentialClassification`, CH-16, quedan intactos); `book/chapters/19-audit-ledger/chapter.md`
   solo recibió `next_chapter: CH-20`.
5. `DataGovernanceEngine` emite `AgentEvent` desde DOS funciones distintas
   (`DATA_CLASSIFIED`/`RETENTION_ENFORCEMENT_EVALUATED`), ambas **condicionalmente**: solo cuando
   `execution`/`agentId` llegan ambos resueltos — y se documenta explícitamente (seccion 14) que
   ninguno de los dos eventos es, jamás, evidencia de auditoría inmutable (frontera con `AuditLedger`,
   CH-19).

## 3. Verificación ejecutada (evidencia concreta)

```
./scripts/validate-chapter book/chapters/20-data-governance-engine      → OK (tras agregar
    ContextBlock a la tabla de tipos reusados de la seccion 6 — primer intento falló con
    "Entidad no definida (no magic entities): ContextBlock", corregido registrando el tipo
    reusado explícitamente, mismo mecanismo que ActorId en CH-19 §6)
./scripts/validate-retrieval-set book/chapters/20-data-governance-engine → OK a la primera
    (guidingQuestions: 4, recallQuestions: 4, explainPrompts: 2, interleavedQuestions: 3 —
    CH-04/CH-16/CH-19 — flashcards: 5, calibrationPairs: 4)
./scripts/validate-contracts / validate-components                       → OK (30 contratos,
    18 componentes)
./scripts/validate-chapter book/chapters/19-audit-ledger                 → OK (revalidado tras
    el único cambio de navegación permitido, next_chapter: CH-20)
rm -rf dist && ./scripts/build-all                                        → exit 0
```

21 capítulos reales, todos pasando `validate-chapter`/`validate-retrieval-set`. `build-mind-map`:
`chapter-20.diagram` con 135 nodos/208 aristas — más que `chapter-19.diagram` (129 nodos/199
aristas), como exige la verificación. Se leyó `scripts/lib/render-diagram.js` (fix de Ghostscript,
CH-16) antes de empezar y no se encontró ningún problema real que justificara modificarlo.

**Web**: `dist/web/chapters/CH-20.html` con SVG inline (`grep -c '<svg'` = 1 en las 21 páginas,
verificado una por una), anchors `id="CMP-018"`/`id="C-030"` presentes, navegación CH-19↔CH-20
verificada en ambos sentidos (`href="CH-20.html"` desde CH-19, `href="CH-19.html"` desde CH-20).
Anchors clave de capítulos anteriores (`CMP-001` en CH-01, `CMP-004` en CH-04, `CMP-014` en CH-16,
`CMP-017` en CH-19) intactos.

**PDF**: con `pypdf`, 529 páginas — más que el build de 20 capítulos (495 páginas, confirmado antes
de escribir este capítulo). Texto extraído contiene, verificado programáticamente,
"DataGovernanceEngine" y "DataGovernanceLabel".

**Prueba negativa real**: se renombró el campo obligatorio `does_not_own` de `CMP-018` a
`does_not_own_BROKEN` en `registry/components.yaml` (edición dirigida solo a la ficha de `CMP-018`,
sin tocar los otros diecisiete componentes). `./scripts/validate-components` falló con `exit 1` y el
mensaje exacto `Componente CMP-018: falta el campo obligatorio "does_not_own"`; `./scripts/build-all`
se detuvo en la etapa de validación con `exit 1` real (confirmado con `$?`, no inferido de un pipe) y
`policies/publishing.yaml: unresolved_validation_errors = deny → build detenido.`, sin construir
`dist/`. Se restauró el campo desde una copia de respaldo, se confirmó
`validate-components: OK (18 componente(s))`, y se reconstruyó todo desde cero: mismos 21 capítulos,
30 contratos, 18 componentes, mismos nodos/aristas por capítulo (135/208 en CH-20), 529 páginas de
PDF — conteos idénticos al build previo a la prueba negativa.

## 4. Decisiones de diseño no cubiertas en el encargo original

- **Frontera con `CredentialBroker` (CH-16), más precisa que la enumerada en el encargo original**:
  se descubrió, leyendo CH-16 completo antes de escribir, que ese capítulo ya materializó `P-22` con
  código real (`CredentialClassification`, `ENUM` de dos valores) exclusivamente para un secreto — y
  que CH-16 §18 documentó, explícitamente, la generalización a "cualquier dato empresarial gobernado"
  como trabajo de un capítulo futuro del Data & Context Plane. Esto se convirtió en el hilo narrativo
  central del capítulo (seccion 1/2/3/8/15) y en una `interleaved_question` completa (`IQ-CH20-02`),
  además de la frontera con `ContextEngine` que el encargo ya pedía explícitamente.
- **`DataGovernanceLabel` sin campo `actor`**: evaluado explícitamente y descartado — a diferencia de
  `AuditRecord` (CH-19), que existe para probar QUIÉN decidió QUÉ, `DataGovernanceLabel` describe una
  propiedad del dato mismo. La trazabilidad de `INV-19` se resuelve, en cambio, a través del
  `traceId`/`agentId` que el `AgentEvent` condicional ya transporta — mismo tratamiento que
  `ContextEngine` (CH-04) ya aplicó.
- **`RetentionEnforcementOutcome` como `ENUM` de tres valores, no un `Boolean`**: para poder
  distinguir "todavía no es exigible" de "es exigible pero suspendido por legal-hold" — ambos
  colapsarían al mismo valor `FALSE` bajo un `Boolean`, perdiendo precisamente la distinción que el
  encargo pidió documentar con cuidado.
- **Por qué `legalHold` se evalúa ANTES de `retentionDeadline` en `enforceRetention`, y por qué la
  función nunca borra ni reemplaza `retentionDeadline`**: documentado extensamente en la seccion 11
  del capítulo — es, además, el `leverage_point` del `systems_lens` (frontmatter) y el punto de mayor
  cuidado editorial de todo el capítulo, por instrucción explícita del encargo.
- **`ErrorCategory.GOVERNANCE`** (nuevo, noveno valor agregado desde CH-00) y dos valores nuevos de
  `AgentEventType` (`DATA_CLASSIFIED`, `RETENTION_ENFORCEMENT_EVALUATED`) — el primer capítulo desde
  `IdempotencyGuard` (CH-17) en agregar más de un valor de evento, porque introduce dos funciones
  reales en vez de una sola.

## 5. Deuda intencional hacia el próximo capítulo

- **El cableado real hacia `classifyData`/`enforceRetention`**: `ContextEngine` (CH-04) y
  `ToolRuntime` (CH-02) no invocan todavía, de verdad, estas funciones sobre su propio material
  producido.
- **Cuál `DataGovernanceLabel` es "el vigente"** para un `subjectRef` dado cuando existen varios
  producidos en momentos distintos: no modelado, Preview.
- **El motor real de reglas de gobernanza** detrás de `dataGovernanceRuleFound`/
  `matchDataGovernanceRule`/etc.: asumido, no modelado (mismo tratamiento que
  `policyRuleFound`/`matchPolicyRule` en CH-05).
- **El mecanismo real que ejecuta un borrado, un cifrado, o el movimiento físico de un dato entre
  regiones**: Preview, infraestructura de borde.
- **El grafo completo de lineage**: `lineageRef` queda opaco.
- **Autorización de lectura/escritura sobre las propias etiquetas de gobernanza, e `INV-E07`**: no
  resuelto — mismo límite abierto que `AuditLedger` (CH-19) dejó para su propio ledger.
- **Auditar una clasificación con `AuditLedger`**: ningún cableado real conecta todavía
  `DataGovernanceEngine` con `recordAuditEntry`.
- **Los dos planos restantes** del Amendment v1.1 (Execution Plane, Execution Fabric): candidatos
  para los próximos incrementos — con este capítulo, siete de nueve planos canónicos quedan
  cubiertos por este libro.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
