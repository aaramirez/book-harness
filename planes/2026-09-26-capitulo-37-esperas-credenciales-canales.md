# Plan / Registro de ejecución — Capítulo 37: Esperas, Credenciales y Canales Completos

**Fecha:** 2026-09-26
**Estado:** ✅ Completado (2026-09-26). Rama `cap-37-esperas-credenciales-canales` mergeada a `main`, sobre `46ba1d8`.
**Release:** v0.2.1 (cierre de deuda de v0.2). Deudas de `registry/debt.yaml` con destino CH-37: D-009, D-010, D-011, D-012, D-013.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-37 (§6), release v0.2.1 (§3).
- CH-33 (`ResumptionCoordinator`, `ParkedWait`, `AuthorizationChallenge`, `acceptDelivery`), CH-34 (`ContinuationRegistry`, `releaseContinuationAddress`), CH-16/CH-35 (`CredentialBroker`), CH-36 (`resumeDurableApproval`) y la revisión v0.2.1 de CH-13 (`resolveApprovalForResume`).

## 1. Objetivo

Completar los cuatro tipos de espera de CH-33 y la mitad de salida de los canales de CH-34:
- que una espera sin respuesta **venza sola**;
- que preguntas, autorizaciones y límites de presupuesto se **reanuden de forma durable**, como la aprobación en CH-36;
- que una autorización interactiva empiece cuando **falta la credencial del usuario** y termine con el **token en CredentialBroker**, sin pasar por la espera;
- que una dirección de continuación se **libere** al terminar la sesión;
- que el arnés **responda** por el canal de esa dirección.

## 2. Alcance decidido

**0 componentes + 0 contratos + 0 contratos modificados**: la restricción de v0.2.1 para no correr los ids de v0.3. Tipos embebidos: `ENUM SessionEndReason`, `ENUM OutboundKind`, `STRUCT OutboundMessage`, `STRUCT AuthorizationParking`.

| Deuda | Componente (dentro de su `owns`) | Funciones |
|---|---|---|
| D-009 vencimiento activo | ResumptionCoordinator | `dueParkedWaits`, `expireParkedWait`, `expiryObservation` |
| D-011 credencial faltante y callback | CredentialBroker | `detectMissingCallerCredential`, `acceptAuthorizationCallback` |
| D-012 liberar la dirección | ContinuationRegistry | `releaseAddressesForSession` |
| D-013 responder por el canal | ContinuationRegistry | `outboundAddressFor`, `buildOutboundMessage` |
| D-010 reanudación durable | (integración) | `parkForMissingCredential`, `resumeDurableQuestion`, `resumeDurableAuthorization`, `resumeDurableBudgetLimit` |

## 3. Decisiones de diseño centrales

- **El vencimiento entra por un schedule** (`sourceKind = SCHEDULE`, CH-34, P-16), admitido con un `Principal` `RUNTIME`. Vencer es otra forma de rechazar: aprobación y autorización continúan con la observación `WAIT_EXPIRED`, y un límite de presupuesto termina el run.
- **El token nunca pasa por la espera.** `acceptAuthorizationCallback` recibe solo `tokenStored` (la señal del Secret Store) y produce una `WaitDelivery` sin credenciales. Quien responde debe ser el mismo `Principal` del desafío.
- **Un límite de presupuesto aprobado no decide el presupuesto:** el operador propone un `ExecutionBudget` extendido y `ExecutionController` (`evaluateExecutionContinuation`) decide si el run continúa. Un rechazo termina con `terminateAgentRunOperationally` (CH-13).
- **La pregunta ya está comprometida** cuando se estaciona: fue la respuesta del modelo. La contestación entra como un mensaje nuevo, y el paso siguiente empieza limpio.
- **Handoff no libera la dirección:** la sesión la conserva, para que las respuestas del humano sigan llegando a ella.
- **Solo se responde a la dirección que la sesión posee.** Un aviso de espera lleva su `waitId`, para que la respuesta sea una entrega dirigida (INV-E18).

## 4. Archivos creados

- `book/chapters/37-esperas-credenciales-canales/chapter.md` (secciones 0–21, 16 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-37-esperas-credenciales-canales.md`
- `diagrams/archify/capitulo-37-esperas-credenciales-canales.json` + `rendered/…html`; `diagrams/mindmap/chapter-37.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/debt.yaml`: D-009..D-013 → `resolved`, `resolved_in: CH-37`
- `registry/glossary.yaml`: Active Wait Expiry, Outbound Reply
- `book/book.yaml`; CH-36 `next_chapter: CH-37`
- KB: índice de capítulos, glosario, navegación de CH-36

## 6. Resultado real del pipeline

- **Rojo:** 19 errores con solo el frontmatter. En el mismo paso, **`validate-debt` falló con las cinco deudas de CH-37 como VENCIDAS**: el registro de deuda funcionó como se diseñó y obligó a resolverlas antes del build.
- **Verde:** `validate-chapter` OK (22 secciones, 16 bloques), tras agregar `HumanInteractionOutcome` a la tabla de tipos heredados; `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **`validate-debt`:** 20 open, 15 resolved, 5 out_of_scope; quedan 8 con destino CH-38.
- **`build-all` exit 0 con 38/38 capítulos y 38/38 retrieval sets.** `dist/book.pdf` 5,5 MB; `Missing character` en 6; 0 `Could not fetch`.
- **Archify:** showcase 9/9, 0/0; spec `7c4286d0e8e0`; visual-check pass (claro y oscuro); revisado a 1440×900. Segmentos con los límites de CH-36; la etiqueta del tercero quedó en "Vencer, liberar", y dos mensajes se acortaron para no chocar con la barra de CredentialBroker. Secret Store y adaptador de callback aparecen en notas, no como participantes.
- **Incidente de tooling:** la nota de KB de CH-37 se generó con un `node -e` dentro de Bash, y los backticks la dejaron sin los nombres de funciones. Se reescribió con Write. En adelante, el contenido con backticks va en un archivo, nunca en `node -e`.

## 7. Definition of Done

- [x] Validadores de CH-37 en verde; D-009..D-013 `resolved` con `resolved_in: CH-37` y `validate-debt` en verde.
- [x] 38/38 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-36 `next_chapter` = CH-37.

## 8. Deuda nueva (registrada al cerrar v0.2.1 si no la resuelve CH-38)

- Avisar a un aprobador por un canal distinto del de la sesión: requiere una dirección propia del aprobador. Fuera de v0.2.1; candidata para CH-46 (observabilidad por audiencia) o una versión posterior.
- El protocolo OAuth y el adaptador de callback: infraestructura, fuera de alcance, igual que D-039.
