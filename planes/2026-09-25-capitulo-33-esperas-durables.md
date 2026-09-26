# Plan / Registro de ejecución — Capítulo 33: Esperas Durables y la Reanudación desde Cualquier Canal

**Fecha:** 2026-09-25
**Estado:** ✅ Completado (2026-09-25). Rama `cap-33-esperas-durables` mergeada a `main`, sobre `34fcc89`.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-33 (§6).
- `2026-09-14-capitulo-06-human-interaction-service.md`: `HumanInteractionService` (CMP-006), `HumanInteractionRequest` (C-015), `HumanInteractionResolution` (C-016), `createHumanInteractionRequest` / `resolveHumanInteractionRequest`.
- `2026-09-14-capitulo-13-integracion-caminos-de-gobierno.md`: `beginToolApprovalPause` (persiste y retorna) y `resumeAfterHumanResolution`, que existe pero nadie invoca.
- `2026-09-25-capitulo-31-identidad-del-llamante.md`: `Principal` (C-040) y `caller.current`, para saber quién pidió la espera y quién responde.
- Amendment v1.2: **P-33** (esperar es durable y no consume cómputo) e **INV-E18** (una entrega reanuda solo la espera a la que se dirige, y solo si quien responde está autorizado).

## 1. Objetivo

Sexto capítulo del Tramo 4. Cierra la otra mitad de CH-13: `beginToolApprovalPause` estaciona el run y retorna, pero nadie decide **qué entrega** lo reanuda, **quién** puede responder, ni **qué pasa** con las esperas que no son humanas. Además da el primer uso real a `PAUSED` (C-013), que nunca se producía.

## 2. Alcance decidido

**1 componente + 2 contratos + 1 contrato modificado:**
1. **CMP-024 `ResumptionCoordinator`.** HumanInteractionService sigue siendo dueño de la solicitud y su resolución (INV-14); el coordinador es dueño de la **espera**.
2. **C-044 `ParkedWait`:** waitId, runId, sessionId, kind, requestId?, challengeId?, requestedBy, responderRule, designatedResponder?, status, parkedAt, expiresAt?, resumedAt?.
3. **C-045 `AuthorizationChallenge`:** challengeId, principal, connectionRef, callbackRef, createdAt, expiresAt. Nunca contiene un token.
4. **C-015 `HumanInteractionRequest` v2:** `waitId: Optional<WaitId>`. Sin ADR: el plan maestro solo exige ADR para las cinco decisiones de §5, y esta es un vínculo opcional.
5. **C-013 `AgentRunStatus`:** sin cambios en el registro; `PAUSED` se usa por primera vez (autorización y límite de presupuesto).
6. **Embebidos:** `ENUM WaitKind` (TOOL_APPROVAL, QUESTION, AUTHORIZATION, BUDGET_LIMIT), `ENUM WaitStatus` (PARKED, RESUMED, EXPIRED), `ENUM ResponderRule` (SAME_PRINCIPAL, SAME_TENANT, DESIGNATED_PRINCIPAL), `STRUCT WaitDelivery`.
7. **Funciones de ResumptionCoordinator:** `runStatusForWait`, `samePrincipal`, `parkRun`, `parkedAgentState`, `createAuthorizationChallenge`, `findAddressedWait`, `responderMayResolve`, `rejectDelivery`, `acceptDelivery`.
8. **HumanInteractionService (CMP-006)**, dentro de su `owns` ("persistir interacciones pendientes"): `linkRequestToWait`.
9. **Integración:** `resumeToolApprovalWait` cablea por fin `resumeAfterHumanResolution` (CH-13).

## 3. Decisiones de diseño centrales

- **Una abstracción para cuatro esperas** (lección de eve), en vez de cuatro mecanismos.
- **La entrega nombra su espera.** `findAddressedWait` busca por `waitId` explícito; nunca "la última espera de la sesión" (INV-E18).
- **Quién responde se valida con `Principal`** (CH-31). Una autorización OAuth solo la puede responder el mismo principal que debe autorizar.
- **El canal no importa para decidir.** `channelRef` queda para trazabilidad; la validez depende de la espera y del principal, no del canal (P-33: "any authorized channel").
- **El token nunca pasa por la espera.** El callback entrega la credencial a CredentialBroker; a la espera solo le llega "autorizado o no" (INV-E08).
- **Anexo pi:** el protocolo de UI remota (solicitud y respuesta de diálogo) se describe como un adaptador de canal (P-11, INV-14), no como un componente.

## 4. Archivos creados

- `book/chapters/33-esperas-durables/chapter.md` (secciones 0–21, 19 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-33-esperas-durables.md`, `kb/02-Componentes/CMP-024-resumptioncoordinator.md`, `kb/03-Contratos/C-044-parkedwait.md`, `kb/03-Contratos/C-045-authorizationchallenge.md`
- `diagrams/archify/capitulo-33-esperas-durables.json` + `rendered/…html`; `diagrams/mindmap/chapter-33.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/components.yaml`: CMP-024
- `registry/contracts.yaml`: C-015 **v1 → v2** (`waitId`; `used_by` suma CMP-024), C-044, C-045
- `registry/glossary.yaml`: Parked Wait, Addressed Delivery, ParkedWait, AuthorizationChallenge
- `book/book.yaml`; CH-32 `next_chapter: CH-33`
- KB: C-015 (v2), índices de componentes, contratos y capítulos; glosario; navegación de CH-32

## 6. Resultado real del pipeline

- **Rojo:** 23 errores con solo el frontmatter, incluido el `modified_by` faltante de C-015.
- **Registro:** `validate-contracts` OK (45), `validate-components` OK (24).
- **Verde:** `validate-chapter` OK (22 secciones, 19 bloques, 2 contratos, 1 componente); `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **`build-all` exit 0 con 34/34 capítulos y 34/34 retrieval sets.** El mapa mental dibuja `CH-33 → C-015 [MODIFIES]`.
- `dist/book.pdf` 4,9 MB; 0 `Could not fetch`; `Missing character` se mantiene en 6 (los de CH-10).
- **Archify:** showcase 9/9, 0/0; spec `df6210df…`; visual-check pass en los cuatro viewports; revisado a 1440×900. Título corto ("Capítulo 33 — Esperas Durables"); la etiqueta de `beginToolApprovalPause` se acortó para no empujar la del segmento.
- **Ajuste de diseño:** `linkRequestToWait` queda en HumanInteractionService (su `owns` "persistir interacciones pendientes"), no en el coordinador, para que la solicitud siga siendo solo de CMP-006. `resumeToolApprovalWait` es una función de integración, no del componente: el coordinador decide la espera, nunca ejecuta.

## 7. Definition of Done

- [x] Validadores de CH-33 en verde; CMP-024, C-044, C-045 registrados; C-015 en v2 con `modified_by: [CH-33]`.
- [x] 34/34 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB y glosario; CH-32 `next_chapter` = CH-33.
- [x] Tests §16 para INV-E18 (`ResponderOutsideTheRuleIsRejectedAndWaitStaysParked`, `DeliveryWithoutMatchingWaitIdIsNeverInferred`) y P-33 (`ParkRunReturnsWithoutHoldingAProcess`).

## 8. Deuda

- Vencimiento activo (`EXPIRED` sin respuesta): necesita un disparador de tiempo, que llega con los schedules (CH-34).
- Reanudar preguntas, autorizaciones y límites de presupuesto: mismo patrón que `resumeToolApprovalWait`, se integra en CH-36.
- A qué canal avisar que hay una espera: dirección de continuación (CH-34).
- Esperas de un run hijo hacia el padre: CH-42.
- `CredentialBroker` todavía no tiene la función que detecta la credencial faltante del `caller.current` ni la que recibe el token del callback: CH-35 (credenciales solo en el egress) o CH-36.
