# Plan / Registro de ejecución — Capítulo 26: Integración Enterprise, el Camino Feliz de una Activación Admitida y Gobernada

**Fecha:** 2026-09-18
**Estado:** ✅ Completado, sobre el estado dejado por `13b816d` (CH-00..CH-25 como los veintiséis
únicos capítulos reales antes de este: los once componentes de Article III + dos capítulos de
integración (CH-00..CH-13), los nueve planos del Amendment v1.1 (CH-14..CH-22), `HandoffCoordinator`
(CH-23), `SkillLibrary` (CH-24) y el epílogo de cierre (CH-25) — 64/64 principios/invariantes ya
citados por al menos un capítulo real).
**Depende de:**
- `2026-08-23-book-harness-como-construir-un-arnes.md` (plan base — pipeline, registries, scripts)
- `2026-08-23-metodo-aprendizaje-activo-lector.md` (Ciclo de Dominio Activo / `RetrievalSet`)
- `2026-08-24-mapa-mental-progresivo.md` (`BookMindMap`, snapshots acumulativos por capítulo)
- `2026-09-14-capitulo-12-integracion-camino-feliz.md` / `2026-09-14-capitulo-13-integracion-caminos-de-gobierno.md`
  (plantilla estructural exacta: capítulo de integración pura, `introduces_components: []`/
  `introduces_contracts: []`, función nueva que invoca por nombre exacto funciones ya publicadas)
- `2026-09-14-capitulo-14-admission-controller.md`, `2026-09-14-capitulo-16-credential-broker.md`,
  `2026-09-17-capitulo-17-idempotency-guard.md`, `2026-09-17-capitulo-19-audit-ledger.md`,
  `2026-09-18-capitulo-20-data-governance-engine.md`, `2026-09-18-capitulo-24-skill-library.md`
  (cada uno documenta, en su propia sección 18, exactamente qué llamada real hacia el runtime de
  Article III dejó pendiente — la lista consolidada que este capítulo cierra)

---

## 1. Objetivo

Escribir el primero de dos capítulos de integración de Amendment v1.1 (CH-26/CH-27), cableando con
pseudocódigo real 6 de los 9 componentes del Amendment v1.1 —`AdmissionController` (CH-14),
`CredentialBroker` (CH-16), `IdempotencyGuard` (CH-17), `AuditLedger` (CH-19),
`DataGovernanceEngine` (CH-20) y `SkillLibrary` (CH-24)— entre sí y con el runtime de Article III
que CH-12/CH-13 ya cablearon, sin modificar el pseudocódigo ya publicado de ninguno de los
diecisiete componentes/funciones de integración involucrados. Los 3 componentes restantes del
Amendment (`OperationalController`, CH-18; `HandoffCoordinator`, CH-23) se cablean en CH-27;
`AgentCommunicationGateway` (CH-15) se decide, con justificación explícita, fuera de alcance de
ambos capítulos.

## 2. Decisión de alcance: 2 capítulos, no 1

Se evaluó honestamente si los 8 componentes cabían en un solo capítulo disciplinado (siguiendo el
mismo criterio que separó CH-12 de CH-13: camino feliz vs. caminos de gobierno). Igual que CH-13
documentó respecto a CH-12, mezclar en una sola función el camino feliz enterprise (admisión →
clasificación → skill → credencial → idempotencia → auditoría) con los caminos de control/traspaso
(`OperationalController` interrumpiendo el run desde afuera; `HandoffCoordinator` empaquetando una
denegación severa) habría producido una única función gigantesca que mezcla dos familias de
decisión completamente distintas — exactamente el acoplamiento que Article IV, aplicado a la
integración misma, existe para evitar. Se decidió, por lo tanto, la misma partición dos-capítulos:

- **CH-26 (este capítulo)**: camino feliz enterprise — Admission → DataGovernance → SkillLibrary →
  (turno normal) → CredentialBroker → IdempotencyGuard → AuditLedger.
- **CH-27**: caminos de control/traspaso enterprise — OperationalController (kill switch) →
  HandoffCoordinator, y PolicyDecision severa → HandoffCoordinator.

## 3. Componentes cableados en este capítulo, con nombres de función exactos

1. **`AdmissionController.evaluateAdmissionForActivationRequest(request: ActivationRequest) ->
   AdmissionDecision`** (CH-14) — invocada antes de que exista cualquier `AgentActivationRequest`
   (CH-11). Cierra CH-14 §18 ("El cableado real `AdmissionController → Routing → AgentCore`").
2. **`AuditLedger.recordAuditEntry(subjectRef, versionSnapshot, actor, execution, agentId) ->
   AuditRecord`** (CH-19) — invocada con `execution = NULL`/`agentId = NULL` sobre la
   `AdmissionDecision` (resolviendo el hallazgo honesto de CH-14 §14: "el primer componente real
   del libro cuya función principal nunca construye un `AgentEvent`"), y de nuevo con `execution`
   real sobre la ejecución de la tool call. Cierra CH-19 §18 ("el cableado real de cada componente
   que decide hacia `recordAuditEntry`... no fueron modificados para invocar de verdad
   `recordAuditEntry`").
3. **`DataGovernanceEngine.classifyData(subjectRef, provenance, legalHold, execution, agentId) ->
   DataGovernanceLabel`** (CH-20) — invocada sobre `block.provenance` de cada `ContextBlock` que
   `ContextEngine.assembleContextSnapshot` (CH-04) ya produjo, antes de convertirlo en
   `AgentMessage`. Cierra CH-20 §9/§18 ("el cableado exacto que este capítulo deja explícitamente
   para un capítulo de integración futuro, sin tocar una sola línea de CH-04").
4. **`SkillLibrary.resolveSkillForSituation(situationName, registeredSkills, execution, agentId) ->
   SkillDescriptor`** (CH-24) — invocada junto al `ContextSnapshot` ya ensamblado, antes de invocar
   al modelo, distinta de `CapabilityRegistry.resolveModelProposedToolCall` (CH-08), que resuelve
   "qué tool ejecutar" solo después de que el modelo propone algo. Cierra CH-24 §18.
5. **`CredentialBroker.resolveCredentialReference(descriptor, credentialName, classification,
   credentialBelongsToCapability, secretExists, expiresAt, execution, agentId) ->
   CredentialReference`** (CH-16) — invocada después de `PolicyEngine.evaluatePolicyForToolCall`
   (ALLOW) y antes de `ToolRuntime.executeToolCall`. Cierra CH-16 §18.
6. **`IdempotencyGuard.checkIdempotency(toolCall, idempotencyKey, existingRecordForKey, execution,
   agentId) -> Optional<IdempotencyRecord>`** y **`recordIdempotentExecution(toolCall, toolResult,
   idempotencyKey, existingRecordForKey, execution, agentId) -> IdempotencyRecord`** (CH-17) —
   invocadas alrededor de `executeToolCall`; si ya existe un registro `COMPLETED`, `executeToolCall`
   nunca se invoca de nuevo. Cierra CH-17 §18.

Todas conviven, en `runGovernedEnterpriseTurn` (CH-26 §11), con las funciones ya publicadas de
Article III que CH-12 ya cableó (`activateAgent`, `beginAgentInitialization`,
`evaluateExecutionContinuation`, `assembleContextSnapshot`, `invokeModelForTurn`, `runTurn`,
`resolveModelProposedToolCall`, `evaluatePolicyForToolCall`, `executeToolCall`, `emitAndDistribute`,
`createOrUpdateSessionCheckpoint`) — sin modificar ni una línea de ninguna de las diecisiete.

## 4. Verificación ejecutada

- `node scripts/validate-chapter book/chapters/26-integracion-enterprise-camino-feliz/chapter.md` → OK
  (22/19 secciones, 1 bloque pseudocódigo, 0 contratos/componentes introducidos).
- `node scripts/validate-retrieval-set book/chapters/26-integracion-enterprise-camino-feliz/chapter.md` → OK
  (4 guiding questions, 4 recall questions, 2 explain prompts, 5 interleaved questions, 5
  flashcards, 4 calibration pairs).
- `rm -rf dist && ./scripts/build-all` → ejecutado junto con CH-27 (ver
  `planes/2026-09-18-capitulo-27-integracion-enterprise-caminos-de-control.md` §4 para el resultado
  consolidado de la corrida completa de 28 capítulos).
- Verificación de los 64 principios/invariantes: script Python ad-hoc sobre
  `frontmatter.constitutional_articles` de los 28 `chapter.md` (excluyendo CH-00, que transcribe la
  Constitution completa) confirma 64/64 citados por al menos un capítulo real, sin regresión.

## 5. Lo que este capítulo no resuelve (honesto, ver también CH-26 §18)

- `OperationalController`/`HandoffCoordinator` (CH-27).
- `AgentCommunicationGateway` (CH-15) — frontera entre agentes/runs distintos, no dentro de un
  turno individual (INV-E03/E06 exigen un segundo run y un `DelegationGrant` ya emitido).
- `EvaluationHarness` (CH-22, certificación pre-producción de un candidato) y
  `ExecutionFabricAdapter` (CH-21, topología de despliegue) — ninguno opera en la escala de un
  turno individual, confirmado al releer ambos capítulos completos.
- `enforceRetention` (CH-20): se invoca `classifyData`, no `enforceRetention`.
- Auditoría exhaustiva de cada paso: solo 2 puntos de auditoría (admisión, ejecución real),
  decisión de alcance documentada explícitamente, no un intento de auditar los 17 pasos.
