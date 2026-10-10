# Plan / Registro de ejecución — Capítulo 45: Evolución del Runtime con Sesiones Abiertas

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `cap-45-evolucion-del-runtime` mergeada a `main`, sobre `29ba532`.
**Release:** v0.3. Deudas con destino CH-45: D-017, D-022, D-046, D-048.
**ADR:** ADR-003 parte v3 **Accepted** (2026-10-10, aprobada por el autor) con un ajuste: una sesión sin `runtimeVersion` es de versión **desconocida**, no de la inicial.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-45 (§6).
- CH-10 (`SessionManager`, `SessionState`), CH-19 (`VersionSnapshot` embebido, INV-E10), CH-29 (C-020 v2), CH-32 (`StepRecord`, `StepStatus`), CH-33 (`ParkedWait`, `WaitStatus`), CH-39 (`ModelDescriptor`, `selectModelDescriptor`), CH-41 (`translateConnectionTools` con `connectionVersion`), CH-44 (`AgentInvocation`, `isTerminalInvocationStatus`).
- Constitución: P-08, P-23, P-36 (el runtime evoluciona bajo sesiones abiertas solo en fronteras inactivas), INV-12, INV-13, INV-E10, INV-E22 (el trabajo vivo nunca migra).

## 1. Objetivo

Que una sesión registre con qué versiones corre, y que pase a una versión nueva del agente, la política, el modelo, las conexiones o el formato de sesión solo cuando no tiene trabajo vivo.

## 2. Alcance decidido

**0 componentes + 1 contrato + 1 contrato modificado:**
1. **C-060 `RuntimeVersionSnapshot`:** versions (`VersionSnapshot`, CH-19), modelId, connectionVersions, sessionFormatVersion, adoptedAt.
2. **C-020 `SessionState` v3:** `runtimeVersion?` (ADR-003 parte v3).
3. **Embebidos:** `STRUCT LiveWork` (pendingWaits, uncommittedSteps, activeChildInvocations) y `STRUCT SessionFormatMigrator` (fromFormatVersion?, toFormatVersion, migratorRef).
4. **Funciones:**
   - SessionManager (CMP-010): `liveWorkOf`, `hasLiveWork`, `findFormatMigrator`, `formatMigrationAvailable`, `sessionMayMigrate`, `withRuntimeVersion`, `migrateSessionRuntime`, `recordModelSwitch`;
   - ConnectionManager (CMP-028): `connectionVersionFor`, `connectionVersionInUse`.

| Deuda | Cómo se resuelve |
|---|---|
| D-017 | `SessionState.runtimeVersion` (C-020 v3) con `RuntimeVersionSnapshot` (C-060) |
| D-022 | `liveWorkOf` cuenta los pasos `STARTED`; `sessionMayMigrate` niega la migración si hay alguno |
| D-046 | `connectionVersionFor`: una sesión usa la versión traducida que tiene fijada; `connectionVersionInUse`: la versión vieja se conserva mientras alguna sesión la tenga fijada |
| D-048 | `recordModelSwitch`: el cambio de modelo entre turnos actualiza `runtimeVersion.modelId` y emite `MODEL_SWITCH_RECORDED` |

## 3. Decisiones de diseño centrales

- **El trabajo vivo son tres cosas** (INV-E22): esperas `PARKED`, pasos `STARTED` e invocaciones no terminales. Con cualquiera, la sesión no migra.
- **Versión desconocida, no inicial** (ajuste aprobado): una sesión sin `runtimeVersion` sigue funcionando como hasta CH-44, pero solo migra con un migrador de formato explícito desde "desconocido".
- **Cambiar de modelo entre turnos no es migrar:** la configuración de modelo (`modelConfigVersion`) no cambia; el modelo elegido sí, y queda registrado.
- **Una conexión retraducida no rompe sesiones abiertas:** cada sesión ve la versión que tiene fijada hasta su próxima frontera inactiva.
- **Sin componente nuevo:** la sesión es de SessionManager; la traducción de conexiones, de ConnectionManager.

## 4. Archivos creados

- `book/chapters/45-evolucion-del-runtime/chapter.md` (secciones 0–21, 15 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-45-evolucion-del-runtime.md`, `kb/03-Contratos/C-060-runtimeversionsnapshot.md`
- `diagrams/archify/capitulo-45-evolucion-del-runtime.json` + `rendered/…html`; `diagrams/mindmap/chapter-45.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/contracts.yaml`: C-020 v3, C-060
- `registry/glossary.yaml`: Idle Boundary, RuntimeVersionSnapshot
- `registry/debt.yaml`: D-017, D-022, D-046, D-048 → `resolved` (CH-45)
- `docs/adr/ADR-003-sesion-en-arbol-y-version-de-runtime.md`: Accepted completo, con el ajuste "versión desconocida"
- `book/book.yaml`; CH-44 `next_chapter: CH-45`
- KB: C-020 a v3; índices de contratos y capítulos; glosario; navegación de CH-44

## 6. Resultado real del pipeline

- **Rojo:** 20 errores de capítulo con solo el frontmatter.
- **Registro:** `validate-contracts` OK (60), `validate-components` OK (29), `validate-debt` OK (4 open, 38 resolved, 6 out_of_scope; solo quedan las de CH-49).
- **Verde:** `validate-chapter` OK al primer intento (22 secciones, 15 bloques, 1 contrato, 0 componentes); `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **`build-all` exit 0 con 46/46 capítulos y 46/46 retrieval sets.** `dist/book.pdf` 6,6 MB; `Missing character` en 6.
- **Archify:** showcase 9/9, 0/0; `check` 9/9; visual-check pass, revisado a 1440×900 (claro y oscuro); 11 mensajes, 4 participantes.

## 7. Definition of Done

- [x] Validadores de CH-45 en verde; C-060 registrado; C-020 en v3 con `modified_by: [CH-29, CH-45]`; ADR-003 Accepted completo; D-017, D-022, D-046, D-048 resolved.
- [x] 46/46 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-44 `next_chapter` = CH-45.

## 8. Deuda

- Sin deuda nueva. Lo de §18 del capítulo se declaró explícitamente:
  - cómo se despliega una versión es del proceso de despliegue y de CH-18: no es deuda;
  - escribir un migrador de formato es del adaptador de persistencia: no es deuda;
  - forzar la migración exige cancelar trabajo vivo con un comando operacional explícito: no es deuda;
  - una sesión de versión desconocida no se fija sin migrar: no es deuda.
