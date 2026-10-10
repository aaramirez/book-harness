# Plan / Registro de ejecución — Capítulo 41: Conexiones: MCP y OpenAPI como Fuentes de Capabilities

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `cap-41-conexiones` mergeada a `main`, sobre `4c14ccf`.
**Release:** v0.3. Deudas con destino CH-41: D-018, D-025.
**ADR:** ADR-005 **Accepted** (2026-10-10, aprobado por el autor), con la ampliación de `executionKind` (D-025), también aprobada.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-41 (§6).
- CH-08 (`CapabilityRegistry`, `resolveToolCall`), CH-05 (`PolicyEngine`), CH-16 / CH-38 (`resolveCredentialReference`, `resolveCallerCredentialReference`), CH-37 (autorización interactiva), CH-35 (`mustRunIsolated` con lista configurada), CH-30 (`ReplayPolicy`).
- Constitución: P-03, P-38 (las capabilities externas entran solo por conexiones declaradas), INV-E25 (ninguna tool externa llega al modelo sin CapabilityRegistry y PolicyEngine).

## 1. Objetivo

Que las tools de servidores MCP y de APIs OpenAPI entren al arnés **como capabilities**, por una conexión declarada, con espacio de nombres, filtro y argumentos que el modelo nunca ve, y que sigan el mismo camino que cualquier otra: CapabilityRegistry, PolicyEngine, ToolRuntime. El protocolo queda como adaptador.

## 2. Alcance decidido

**1 componente + 1 contrato + 1 contrato modificado:**
1. **CMP-028 `ConnectionManager`.**
2. **C-054 `ConnectionDescriptor`:** connectionId, kind, transport, endpointRef, toolFilter, providedArguments, credentialName?, credentialScope, requiresApprovalByDefault.
3. **C-018 `CapabilityDescriptor` v3:** `sourceConnectionId` (ADR-005) y `executionKind` (D-025).
4. **Embebidos:** `ConnectionKind`, `ConnectionTransport`, `FilterMode`, `ToolFilter`, `CredentialScope`, `ExecutionKind`, `ExternalToolSpec`, `ConnectionInvocation`.
5. **Funciones:**
   - ConnectionManager: `toolAllowed`, `translateConnectionTools`, `prepareConnectionCall`;
   - CapabilityRegistry: `effectiveExecutionKind`;
   - IsolatedExecutionEnvironment: `requiresIsolation`, que resuelve D-025;
   - PolicyEngine: `applyConnectionApprovalDefault`;
   - integración: `resolveConnectionCredential`, que resuelve D-018.

## 3. Decisiones de diseño centrales

- **Una tool externa es una capability más** (INV-E25). ConnectionManager produce descriptores; CapabilityRegistry los resuelve y valida como a cualquier otro.
- **Espacio de nombres `<conexión>__<tool>`:** dos servidores pueden tener una tool `search` sin chocar. Un nombre que colisiona con una capability local se rechaza.
- **Argumentos provistos:** se quitan del schema que ve el modelo y se agregan al preparar la invocación. Si el modelo intenta fijarlos, la tool call se rechaza.
- **Replay `NEVER` por defecto:** una tool externa traducida no declara `replayPolicy`, así que su efecto desconocido nunca se repite (CH-30). Declararla `SAFE` es una decisión auditada (CH-38).
- **La aprobación por defecto solo restringe:** convierte un `ALLOW` en `REQUIRE_APPROVAL`, nunca concede.
- **El arnés como servidor MCP es un canal** (CH-34), no una conexión.

## 4. Archivos creados

- `book/chapters/41-conexiones/chapter.md` (secciones 0–21, 18 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-41-conexiones.md`, `kb/02-Componentes/CMP-028-connectionmanager.md`, `kb/03-Contratos/C-054-connectiondescriptor.md`
- `diagrams/archify/capitulo-41-conexiones.json` + `rendered/…html`; `diagrams/mindmap/chapter-41.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/components.yaml`: CMP-028
- `registry/contracts.yaml`: C-018 **v2 → v3** (`sourceConnectionId`, `executionKind`; `used_by` suma CMP-026 y CMP-028), C-054
- `registry/glossary.yaml`: Declared Connection, Provided Argument, ConnectionDescriptor
- `registry/debt.yaml`: D-018 y D-025 → `resolved` (CH-41)
- `docs/adr/ADR-005-…md`: **Accepted** (2026-10-10), con los puntos 4 (`executionKind`, D-025), 5 (`credentialScope`, D-018) y 6 (la aprobación por defecto solo restringe)
- `book/book.yaml`; CH-40 `next_chapter: CH-41`
- KB: C-018 (v3), índices de componentes, contratos y capítulos; glosario; navegación de CH-40

## 6. Resultado real del pipeline

- **Rojo:** 22 errores de capítulo y 2 de `validate-debt` (D-018 y D-025, vencidas al entrar CH-41).
- **Registro:** `validate-contracts` OK (54), `validate-components` OK (28), `validate-debt` OK (13 open, 26 resolved, 6 out_of_scope).
- **Verde:** `validate-chapter` OK (22 secciones, 18 bloques, 1 contrato, 1 componente); `validate-retrieval-set` OK (4/4/2/1/3/4), sin ajustes. Grep de plataformas vacío.
- **`build-all` exit 0 con 42/42 capítulos y 42/42 retrieval sets.** El mapa mental dibuja `CH-41 → C-018 [MODIFIES]`. `dist/book.pdf` 6,0 MB; `Missing character` en 6; 0 `Could not fetch`.
- **Archify:** showcase 9/9, 0/0; spec `ef5bb1c57a86`; visual-check pass; revisado a 1440×900. Sin participante "modelo" (la propuesta va en la nota de `resolveModelProposedToolCall`); `resolveConnectionCredential` y `prepareConnectionCall` comparten un mensaje.

## 7. Definition of Done

- [x] Validadores de CH-41 en verde; CMP-028 y C-054 registrados; C-018 en v3 con `modified_by: [CH-30, CH-41]`; ADR-005 Accepted; D-018 y D-025 resolved.
- [x] 42/42 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-40 `next_chapter` = CH-41.

## 8. Deuda

- **D-046** (registrada): volver a traducir las tools cuando el servidor cambia, sin romper sesiones abiertas → CH-45.
- **D-047** (registrada): recursos y prompts de servidores MCP como fuente de datos gobernada → CH-42.
- El arnés como servidor MCP es un canal (CH-34): no es deuda.
