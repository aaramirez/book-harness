# Plan / Registro de ejecución — Capítulo 38: Identidad, Auditoría y Retención en Todo el Turno

**Fecha:** 2026-09-26
**Estado:** ✅ Completado (2026-09-26). Rama `cap-38-identidad-auditoria-retencion` mergeada a `main`, sobre `4c0a0c7`.
**Release:** v0.2.1, último capítulo. Deudas con destino CH-38: D-001..D-008.

**Depende de:** CH-28 (`PendingInputQueue`, `selectPendingInputsAtBoundary`), CH-29 (`planHistoryCompaction`, `applyHistoryCompaction`), CH-32 (journal y `decideStepRecovery`), CH-14 / CH-31 (`admitWithVerifiedIdentity`), CH-05 (`evaluatePolicyForToolCall`), CH-16 (`resolveCredentialReference`), CH-19 (`recordAuditEntry`), CH-20 (`classifyData`, `enforceRetention`), CH-30 (`effectiveReplayPolicy`) y CH-36 (`enterDurableTurn`).

## 1. Objetivo

Completar la otra mitad de la deuda de v0.2:
- que las entradas pendientes y la compactación sean **durables** dentro del turno;
- que la **identidad** del llamante llegue a las decisiones de admisión, política y credenciales;
- que queden **auditadas** las capabilities `SAFE` y las continuaciones de sesión;
- que el **journal** tenga retención.

## 2. Alcance decidido

**0 componentes + 0 contratos + 0 contratos modificados.** Tipos embebidos: `STRUCT PrincipalAdmissionRule`, `STRUCT CallerPolicyRule`, `STRUCT CompactionStepOutcome`.

| Deuda | Dónde | Funciones |
|---|---|---|
| D-001 PendingInput durable | integración | `takePendingInputsForStep`, `confirmPendingInputsAfterCommit` |
| D-002 y D-003 compactación cableada y recuperable | integración | `compactHistoryInDurableTurn` (la compactación es un paso del journal) |
| D-004 auditoría de SAFE | integración, sobre AuditLedger | `auditSafeReplayDeclaration` |
| D-005 admisión con Principal | AdmissionController | `principalRulesGrantAccess`, `admitWithPrincipalRules` |
| D-006 PolicyEngine / CredentialBroker con caller | PolicyEngine, CredentialBroker | `evaluatePolicyForCaller`, `resolveCallerCredentialReference` |
| D-007 auditoría de continuaciones | integración, sobre AuditLedger | `auditSessionContinuation` |
| D-008 retención del journal | DataGovernanceEngine | `evaluateJournalRetention` |

## 3. Decisiones de diseño centrales

- **La identidad solo restringe** (P-13). `admitWithPrincipalRules` y `evaluatePolicyForCaller` parten de la decisión base (CH-14 / CH-31, CH-05) y solo pueden convertir un permiso en rechazo, nunca al revés. Un conjunto de reglas vacío no concede nada (fail-closed).
- **Una entrada pendiente sale de la cola solo cuando su paso se compromete.** Si el proceso se cae antes, la recuperación la vuelve a aplicar; nunca se pierde ni se aplica dos veces un paso comprometido.
- **La compactación es un paso del journal** (sin tool call). La propuesta de resumen del modelo queda en `modelResponse`. Al recuperar valen las acciones de CH-32 sin cambios:
  - `REEXECUTE_MODEL_CALL` si el corte fue antes de la propuesta;
  - `COMMIT_RECORDED`, que reaplica de forma determinística la propuesta registrada;
  - `REPLAY_RECORDED`.

  El recorte sin modelo (fase 1 de CH-29) no necesita journal, porque es recomputable.
- **Auditar no es emitir un evento** (P-25). Las declaraciones `SAFE` y las continuaciones se registran con `recordAuditEntry` (CH-19, write-once).
- **La retención del journal nunca borra un run vivo:** solo evalúa runs terminados sin pasos `STARTED`, y la preservación legal suspende el borrado (CH-20).

## 4. Archivos creados

- `book/chapters/38-identidad-auditoria-retencion/chapter.md` (secciones 0–21, 13 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-38-identidad-auditoria-retencion.md`
- `diagrams/archify/capitulo-38-identidad-auditoria-retencion.json` + `rendered/…html`; `diagrams/mindmap/chapter-38.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/debt.yaml`: D-001..D-008 → `resolved`, `resolved_in: CH-38`
- `registry/glossary.yaml`: Identity Narrows Never Widens, Commit-Acknowledged Input
- `book/book.yaml`; CH-37 `next_chapter: CH-38`
- KB: índice de capítulos, glosario, navegación de CH-37 (generados desde un script en archivo, sin `node -e`)

## 6. Resultado real del pipeline

- **Rojo:** 19 errores de capítulo y 8 de `validate-debt` (las deudas de CH-38, vencidas al entrar el capítulo en `book.yaml`).
- **Verde:** `validate-chapter` OK (22 secciones, 13 bloques); `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **`validate-debt`:** 12 open (todas en v0.3: CH-39..CH-45), 23 resolved, 5 out_of_scope. **No queda ninguna deuda con destino CH-37, CH-38 ni v0.2.1.**
- **`build-all` exit 0 con 39/39 capítulos y 39/39 retrieval sets.** `dist/book.pdf` 5,6 MB; `Missing character` en 6; 0 `Could not fetch`.
- **Archify:** showcase 9/9, 0/0; spec `52d39dafd412`; visual-check pass; revisado a 1440×900. Segmentos con los límites de CH-36/37; etiquetas cortas ("La identidad restringe", "Compactar, cola", "Evidencia") y participantes "Admisión + Política" y "DataGovernance" para que quepan.

## 7. Definition of Done

- [x] Validadores de CH-38 en verde; D-001..D-008 `resolved` (`resolved_in: CH-38`); `validate-debt` sin deudas con destino CH-37, CH-38 ni v0.2.1.
- [x] 39/39 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-37 `next_chapter` = CH-38.

## 8. Deuda

- Sin deuda nueva con destino en v0.2.1.
- **Reescribir `enterDurableTurn` y `runDurableGovernedStep` (CH-36) con las funciones de CH-37 y CH-38:** CH-38 §9 dice dónde entra cada una. Lo toma el turno conectado de v0.3 (CH-49), porque volver a abrir CH-36 no agrega un comportamiento nuevo.
- Candidatas a registrar al abrir v0.3:
  - avisar a un aprobador por otro canal (de CH-37 §18);
  - reglas de política más ricas por Principal (de CH-38 §18).
