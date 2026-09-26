# Plan / Registro de ejecución — Capítulo 34: Canales y Direcciones de Continuación

**Fecha:** 2026-09-26
**Estado:** ✅ Completado (2026-09-26). Rama `cap-34-canales-continuacion` mergeada a `main`, sobre `e7c201a`.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-34 (§6).
- `2026-09-14-capitulo-14-admission-controller.md`: `ActivationRequest` (C-022), `AdmissionDecision` (C-023), el Ingress Adapter fuera del registro y el Routing como Preview ("before routing", P-17).
- `2026-09-25-capitulo-31-identidad-del-llamante.md`: `continuationAllowedForCaller` (propiedad de sesión) e INV-E15 (arranque cerrado).
- `2026-09-25-capitulo-33-esperas-durables.md`: `ResumptionCoordinator`, al que una entrega a una sesión estacionada se dirige.
- `2026-09-25-capitulo-28-steering-follow-up.md`: `PendingInput`, para un mensaje que llega a una sesión con un run en curso.
- Amendment v1.2: **P-34** (las conversaciones externas se direccionan, no se infieren) e **INV-E19** (una dirección tiene a lo sumo una sesión dueña a la vez).

## 1. Objetivo

Séptimo capítulo del Tramo 4. P-16 normaliza todo estímulo en un `ActivationRequest`, pero nadie responde "¿este estímulo **continúa** una sesión o **activa** una nueva?". El capítulo introduce la dirección de continuación con propiedad exclusiva, y describe los canales (HTTP, WebSocket de entrada, webhooks, schedules y eventos de stream) como Ingress Adapters que la producen.

## 2. Alcance decidido

**1 componente + 1 contrato + 1 contrato modificado:**
1. **CMP-025 `ContinuationRegistry`,** entre AdmissionController y el Routing (Preview).
2. **C-046 `ContinuationAddress`:** channelRef, conversationRef.
3. **C-022 `ActivationRequest` v2:** `sourceKind: Optional<SourceKind>` y `continuationAddress: Optional<ContinuationAddress>`. Sin ADR (no está entre las cinco decisiones de §5).
4. **Embebidos:** `ENUM SourceKind` (API, CHANNEL, WEBSOCKET, WEBHOOK, SCHEDULE, STREAM_EVENT), `ENUM ClaimStatus` (ACTIVE, RELEASED), `STRUCT ContinuationClaim`, `ENUM RouteAction` (CONTINUE_SESSION, ACTIVATE_NEW, ACTIVATE_UNADDRESSED), `STRUCT ContinuationRoute`.
5. **Funciones:** `sameAddress`, `findActiveClaim`, `routeAdmittedRequest`, `claimContinuationAddress`, `releaseContinuationAddress`.
6. **Canales** (sección propia en §9, sin componente): API HTTP de sesiones, WebSocket de entrada (conexión persistente, un turno por mensaje), webhooks (firma verificada en tiempo constante), schedules (cron) y eventos de stream.

## 3. Decisiones de diseño centrales

- **Admisión antes que continuación.** `routeAdmittedRequest` exige un `ADMIT` del mismo request (INV-E02). ContinuationRegistry nunca admite.
- **Continuar no es tener permiso.** Que la dirección tenga dueña dice **a qué sesión** va el estímulo; si el llamante puede operarla lo sigue decidiendo `continuationAllowedForCaller` (CH-31).
- **Enrutar no emite eventos,** igual que la admisión (CH-14): todavía no hay run. Reclamar y liberar sí, porque ocurren con una sesión ya existente.
- **Reclamar es idempotente para la dueña** y fail-closed para cualquier otra sesión.
- **`SourceKind` suma `API`** a los cinco valores de la ficha: la API HTTP de sesiones es un canal más y no debía quedar sin tipo.
- **Un canal sin regla de admisión no escucha:** se obtiene de INV-E15 (CH-31), no de una función nueva. Un arnés sin reglas rechaza todo, por cualquier canal.

## 4. Archivos creados

- `book/chapters/34-canales-continuacion/chapter.md` (secciones 0–21, 13 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-34-canales-continuacion.md`, `kb/02-Componentes/CMP-025-continuationregistry.md`, `kb/03-Contratos/C-046-continuationaddress.md`
- `diagrams/archify/capitulo-34-canales-continuacion.json` + `rendered/…html`; `diagrams/mindmap/chapter-34.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/components.yaml`: CMP-025
- `registry/contracts.yaml`: C-022 **v1 → v2** (`sourceKind`, `continuationAddress`; `used_by` suma CMP-025), C-046
- `registry/glossary.yaml`: Continuation Address, Exclusive Ownership, ContinuationAddress
- `book/book.yaml`; CH-33 `next_chapter: CH-34`
- KB: C-022 (v2), índices de componentes, contratos y capítulos; glosario; navegación de CH-33

## 6. Resultado real del pipeline

- **Rojo:** 22 errores con solo el frontmatter.
- **Registro:** `validate-contracts` OK (46), `validate-components` OK (25).
- **Verde:** `validate-chapter` OK (22 secciones, 13 bloques, 1 contrato, 1 componente); `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas (incluidos nombres de productos de chat y de repositorios) vacío.
- **`build-all` exit 0 con 35/35 capítulos y 35/35 retrieval sets.** El mapa mental dibuja `CH-34 → C-022 [MODIFIES]`.
- `dist/book.pdf` 5,0 MB; 0 `Could not fetch`; `Missing character` se mantiene en 6 (los de CH-10).
- **Archify:** showcase 9/9, 0/0; spec `ffbce9ac…`; visual-check pass en los cuatro viewports; revisado a 1440×900. La integración no tiene línea de vida propia: el Ingress Adapter conduce las llamadas al registro, como "Integración" en CH-32/CH-33.

## 7. Definition of Done

- [x] Validadores de CH-34 en verde; CMP-025 y C-046 registrados; C-022 en v2 con `modified_by: [CH-34]`.
- [x] 35/35 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB y glosario; CH-33 `next_chapter` = CH-34.
- [x] Tests §16 para P-34 (`AddressWithOwnerContinuesThatSession`, `RoutingNeverReadsThePayload`) e INV-E19 (`SecondSessionCannotClaimAnOwnedAddress`, `ConcurrentClaimsLeaveExactlyOneOwner`).

## 8. Deuda

- Cuándo se libera una dirección (fin de sesión, vencimiento, handoff con marcador): CH-36.
- Adaptador de salida para responder por el canal de la dirección: CH-36.
- Routing (qué agente atiende una activación nueva): sigue en Preview.
- Schedule interno que dispare el vencimiento de esperas (deuda de CH-33): CH-36.
- Lectura de eventos de stream como fuente de datos: CH-40.
