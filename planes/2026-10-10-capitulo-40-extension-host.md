# Plan / Registro de ejecución — Capítulo 40: Extensiones que No Pueden Saltarse la Constitución

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `cap-40-extension-host` mergeada a `main`, sobre `25cdd82`.
**Release:** v0.3. Sin deuda con destino CH-40.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-40 (§6).
- `2026-09-13-capitulo-02-tool-runtime.md`: `beforeToolCall` / `afterToolCall`, los dos únicos puntos de extensión del libro; ToolRuntime posee "ejecutar hooks".
- Constitución: P-12 ("events observe; hooks intervene"), EVO-10 (extensiones sin bypass), INV-E24 (ningún hook devuelve una autorización), P-13 e INV-06 (la autorización es de PolicyEngine).
- Propuesta de pi P-A6 (`arnes-ai/docs/propuestas/book-harness/BH-Propuesta-Aportes-pi.md`): hooks del runtime durable y confianza de proyecto atada a un archivo de confianza.

## 1. Objetivo

Hacer verificable EVO-10. Que una extensión solo pueda intervenir en un punto declarado, con un resultado que ese punto admite, nunca con una autorización. Y que el código de un proyecto solo se cargue con una decisión de confianza explícita, atada a su contenido.

## 2. Alcance decidido

**1 componente + 3 contratos:**
1. **CMP-027 `ExtensionHost`.** Justificación EVO-07: ni CapabilityRegistry (resolver capabilities) ni ToolRuntime (ejecutarlas y correr sus hooks) deciden qué código de terceros puede intervenir, en qué punto y con qué resultado.
2. **C-051 `ExtensionRegistration`:** extensionId, version, source, sourceRef, contentHash, hookPoints, capabilities, trustDecisionId?, status, registeredAt.
3. **C-052 `HookPoint`** (ENUM de 8 puntos).
4. **C-053 `ResourceTrustDecision`:** decisionId, sourceRef, contentHash, outcome, decidedBy (`Principal`), decidedAt.
5. **Embebidos:** `ENUM ExtensionSource`, `ENUM ExtensionStatus`, `ENUM TrustOutcome`, `ENUM HookOutcomeKind` (CONTINUE, BLOCK, TRANSFORM), `STRUCT HookOutcome`.
6. **Funciones:** `trustCovers`, `registerExtension`, `allowedOutcomes`, `hooksFor`, `validateHookOutcome`, `firstBlockingOutcome`; integración: `runBeforeToolHooks`.

## 3. Decisiones de diseño centrales

- **INV-E24 es estructural:** `HookOutcomeKind` no tiene ningún valor de autorización. Un hook puede seguir (`CONTINUE`), restringir (`BLOCK`) o transformar dentro de su punto (`TRANSFORM`), nunca conceder.
- **`BEFORE_TOOL` no admite `TRANSFORM`:** los argumentos ya pasaron por el schema de CapabilityRegistry y por PolicyEngine; transformarlos después sería un bypass (EVO-10). Los hooks de `BEFORE_TOOL` corren **después** de un `ALLOW`, y solo pueden bloquear.
- **El dueño del punto ejecuta el hook.** ToolRuntime conserva "ejecutar hooks" (CH-02); ExtensionHost solo dice qué hooks corren y valida lo que devuelven.
- **La confianza se ata al hash.** Si el código de la extensión cambia, la decisión deja de cubrirla y el registro queda `REJECTED`. Una extensión incorporada (`BUILT_IN`) no necesita decisión: es parte del arnés.
- **Registrar no emite eventos:** ocurre antes de cualquier run, con el mismo criterio que la admisión (CH-14). Validar un resultado de hook sí los emite, porque ocurre dentro de un run.

## 4. Archivos creados

- `book/chapters/40-extension-host/chapter.md` (secciones 0–21, 16 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-40-extension-host.md`, `kb/02-Componentes/CMP-027-extensionhost.md`, `kb/03-Contratos/C-051-extensionregistration.md`, `C-052-hookpoint.md`, `C-053-resourcetrustdecision.md`
- `diagrams/archify/capitulo-40-extension-host.json` + `rendered/…html`; `diagrams/mindmap/chapter-40.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/components.yaml`: CMP-027
- `registry/contracts.yaml`: C-051, C-052, C-053
- `registry/glossary.yaml`: Extension, Hook Outcome, ExtensionRegistration, HookPoint, ResourceTrustDecision
- `book/book.yaml`; CH-39 `next_chapter: CH-40`
- KB: índices de componentes, contratos y capítulos; glosario; navegación de CH-39

## 6. Resultado real del pipeline

- **Rojo:** 23 errores con solo el frontmatter. Sin deuda con destino CH-40.
- **Registro:** `validate-contracts` OK (53), `validate-components` OK (27).
- **Verde, tras dos ajustes del retrieval set:**
  - el punto de apalancamiento tenía que nombrar un contrato del capítulo; ahora nombra `HookPoint` (C-052);
  - faltaba una tarjeta con `source_entity: C-051`; se agregó una cuarta.

  Resultado: `validate-chapter` OK (22 secciones, 16 bloques, 3 contratos, 1 componente); `validate-retrieval-set` OK (4/4/2/1/4/4).
- **`build-all` exit 0 con 41/41 capítulos y 41/41 retrieval sets.** `dist/book.pdf` 5,9 MB; `Missing character` en 6; 0 `Could not fetch`.
- **Archify:** showcase 9/9, 0/0; spec `f354ed111604`; visual-check pass; revisado a 1440×900. `registerExtension` se dibuja desde "Persona", por el límite de cinco participantes.

## 7. Definition of Done

- [x] Validadores de CH-40 en verde; CMP-027, C-051, C-052, C-053 registrados.
- [x] 41/41 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-39 `next_chapter` = CH-40.
- [x] Tests §16 para INV-E24 (`HookOutcomeKindHasNoAuthorizationValue`, `NoHookCanTurnADenyIntoAnAllow`) y EVO-10 (`BeforeToolRejectsTransform`, `ExtensionCapabilityGoesThroughCapabilityRegistryAndPolicyEngine`).

## 8. Deuda

Lo de §18 no se registra como deuda: instalar paquetes es infraestructura, y las contribuciones de interfaz son adaptadores (P-11). Lo que sí tiene destino:
- **D-045** (registrada): correr extensiones `PROJECT` en el entorno aislado y apagar una extensión (`DISABLED`) por comando operacional → CH-49, junto a D-041.
