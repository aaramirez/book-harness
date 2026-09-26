# Plan / Registro de ejecución — Capítulo 31: La Identidad del Llamante y el Arranque que No Admite Nada

**Fecha:** 2026-09-25
**Estado:** ✅ Completado (2026-09-25). Rama `cap-31-identidad-del-llamante` mergeada a `main`, sobre `f28725c`.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-31.
- `2026-09-14-capitulo-14-admission-controller.md`: `AdmissionController` (CMP-012), `ActivationRequest` (C-022, con `externalIdentityRef` sin verificar), `AdmissionDecision` (C-023), `evaluateAdmissionForActivationRequest` y su default REJECT.
- `book/chapters/00-arquitectura-constitucion/chapter.md` (CH-00, sin plan propio; lo cubre `2026-08-23-book-harness-como-construir-un-arnes.md`): `ExecutionContext` (C-004), usado por 11 componentes.
- `docs/adr/ADR-001-principal-en-execution-context.md`: **Accepted** (2026-09-25).
- Amendment v1.2: **P-31** (la identidad viaja con cada turno) e **INV-E15** (un arnés sin configurar no admite nada; la admisión de desarrollo depende del modo de proceso, nunca del request).

## 1. Objetivo

Cuarto capítulo del Tramo 4. Que la identidad verificada del llamante:
1. salga de la admisión como un **principal** explícito;
2. viaje con cada turno en `ExecutionContext` (`initiator` fijo, `current` renovado);
3. sea la única fuente del tenant.

Y que un arnés sin reglas de admisión configuradas no admita nada, en ningún entorno.

## 2. Alcance decidido

**0 componentes + 2 contratos + 2 contratos modificados:**
1. **C-040 `Principal`:** principalId, principalType (`PrincipalType`: USER / SERVICE / RUNTIME), issuer, tenantId?, attributes.
2. **C-041 `CallerSnapshot`:** initiator, current.
3. **C-004 `ExecutionContext` v2:** `caller: Optional<CallerSnapshot>`. Es el contrato más usado del libro (11 `used_by`), y ADR-001 lo justifica.
4. **C-023 `AdmissionDecision` v2:** `principal: Optional<Principal>`.
5. **Embebidos:** `ENUM PrincipalType`, `ENUM ProcessMode` (DEVELOPMENT / PRODUCTION) y `ENUM SessionOwnershipRule` (SAME_PRINCIPAL / SAME_TENANT).
6. **`AdmissionController` (CMP-012)** se amplía dentro de su `owns` literal ("apply identity, authorization, tenant… decisions"). Funciones:
   - `admitWithVerifiedIdentity`: INV-E15 y principal;
   - `buildCallerSnapshot`;
   - `bindCallerToExecution`;
   - `requireTenantCaller`;
   - `continuationAllowedForCaller`: responde "la admisión no es propiedad de sesión" con una regla explícita;
   - `acceptDeliveryForSession`: aplica la regla a una entrega nueva y emite `SESSION_CONTINUATION_REJECTED` si la rechaza.

## 3. Decisiones de diseño centrales

- **La verificación criptográfica de la identidad** (OIDC, JWT, API key) es un **adaptador**, como el Ingress Adapter. Entra como `verifiedPrincipal: Optional<Principal>`, una señal de entrada asumida. El libro modela **qué hace el arnés con un principal ya verificado**, no el protocolo.
- **INV-E15:** `admissionConfigured = FALSE` implica REJECT en PRODUCTION. En DEVELOPMENT se admite solo con un principal RUNTIME sintético. `processMode` es un dato del **proceso**, nunca del request.
- **`initiator` no cambia nunca; `current` se renueva en cada entrega.** El tenant solo sale de `caller.current`.
- **Propiedad de sesión:** `continuationAllowedForCaller` exige una `SessionOwnershipRule` explícita. No hay un default permisivo.

## 4. Archivos creados

- `book/chapters/31-identidad-del-llamante/chapter.md` (secciones 0–21, 13 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-31-identidad-del-llamante.md`, `kb/03-Contratos/C-040-principal.md`, `kb/03-Contratos/C-041-callersnapshot.md`
- `diagrams/archify/capitulo-31-identidad-del-llamante.json` + `rendered/…html`; `diagrams/mindmap/chapter-31.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/contracts.yaml`: C-004 **v1 → v2** (`caller`; `used_by` suma CMP-012), C-023 **v1 → v2** (`principal`), C-040, C-041
- `registry/glossary.yaml`: Verified Principal, Fail-Closed Bootstrap, Principal, CallerSnapshot
- `docs/adr/ADR-001-…md`: **Accepted** (2026-09-25). El punto 3 deja de nombrar `verifyExternalIdentity`, porque la verificación es un adaptador fuera del registro; se agregan los puntos 6 (arranque cerrado) y 7 (propiedad de sesión).
- `book/book.yaml`; CH-30 `next_chapter: CH-31`
- KB: C-004 y C-023 (v2), índices de capítulos y contratos, glosario, navegación de CH-30

## 6. Resultado real del pipeline

- **Rojo:** 23 errores con solo el frontmatter, incluidos los `modified_by` faltantes de C-004 y C-023.
- **Registro:** `validate-contracts` OK (41), `validate-components` OK (22).
- **Verde:** `validate-chapter` OK (22 secciones, 13 bloques, 2 contratos); `validate-retrieval-set` OK (4/4/2/1/3/4).
- **`build-all` exit 0 con 32/32 capítulos y 32/32 retrieval sets** tras modificar `ExecutionContext`, el contrato más usado del libro. El mapa mental dibuja `CH-31 → C-004` y `CH-31 → C-023 [MODIFIES]`.
- `dist/book.pdf` 4,61 MB; 0 `Could not fetch`; `Missing character` se mantiene en 6 (los de CH-10).
- **Archify:** showcase 9/9, 0/0; spec `880d071d…`; visual-check pass; revisado a 1440×900 (se ajustaron los límites de los segmentos para que la etiqueta del tercero no subiera). La tarjeta "Evidencia" de CH-29/30 se sustituye por la de INV-E15, que cita `chapter.md §11–§13`.
- **Entorno:** el PATH del shell Bash no tenía Graphviz ni pandoc (`spawnSync dot ENOENT`). `build-all` se corrió desde PowerShell con el PATH refrescado del registro; no es un cambio del repo.
- **Ajuste de diseño:** se agregó `acceptDeliveryForSession`, que separa la regla pura (`continuationAllowedForCaller`) de su aplicación con evento, igual que `decideUnknownOutcome` en CH-30.

## 7. Definition of Done

- [x] Validadores de CH-31 en verde; C-004 y C-023 en v2 con `modified_by: [CH-31]`.
- [x] 32/32 capítulos en verde; en particular, los 11 capítulos cuyos componentes usan C-004.
- [x] `build-all` exit 0; Archify validado; KB y glosario; CH-30 `next_chapter` = CH-31.

## 8. Deuda

- Reglas de admisión que usen el principal (tipo, tenant): la firma de `evaluateAdmissionForActivationRequest` (CH-14) no cambia; se cablea en la integración (CH-36).
- `CredentialBroker`, `PolicyEngine` y memoria leyendo `caller.current`: CH-36, CH-39 (conexiones) y CH-40 (datos).
- Reenvío de identidad entre agentes (`forwardPrincipal`): CH-42.
- Auditoría de quién continuó cada sesión (CH-19): el mecanismo existe, falta conectarlo.
- CH-32 hereda: la identidad ya viaja, pero la recuperación a mitad de turno no tiene una unidad más fina que el turno.
