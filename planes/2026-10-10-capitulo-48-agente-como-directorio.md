# Plan / Registro de ejecución — Capítulo 48: El Agente como Directorio: Autoría por Convención

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `cap-48-agente-como-directorio` mergeada a `main`, sobre `0a07f58`.
**Release:** v0.3. Sin deudas con destino CH-48. Decisión T0.6 (2): CH-48 es un capítulo de v0.3.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-48 (§6), con el mapa ranura → contrato.
- Diseño de referencia en `arnes-ai`: `docs/propuestas/arnes0.1/Arnes-Filesystem-First.md` (ranuras, reglas R1–R11, descubrimiento).
- CH-11 (`AgentCore`, validar el `AgentConfig` antes de arrancar), y los contratos que cada ranura produce: C-002, C-012, C-018, C-022, C-035, C-051, C-054, C-055.
- Constitución: P-06 (los agentes son configuración sobre un runtime compartido), P-39 (el agente se escribe como archivos inspeccionables en ubicaciones convencionales), INV-09, INV-E27 (un diagnóstico ERROR impide activar el agente); EVO-10 se cita en el cuerpo (el validador no admite artículos EVO en el frontmatter).

## 1. Objetivo

Que un agente se escriba como un directorio convencional donde la ruta es la identidad, que un adaptador de autoría lo descubra y produzca un manifiesto inspeccionable con diagnósticos, y que un diagnóstico de nivel ERROR impida activarlo.

## 2. Alcance decidido

**0 componentes + 2 contratos:**
1. **C-065 `AgentManifest`:** agentRoot, sources, diagnostics, trusted, discoveredAt.
2. **C-066 `AuthoringDiagnostic`:** level, code, path, message.
3. **Embebidos:** `ENUM AuthoringSlot`, `ENUM SourceOrigin` (PROJECT, DEFAULT), `ENUM DiagnosticLevel` (ERROR, WARNING, INFO), `STRUCT ManifestSource`, `STRUCT SlotRule`, `STRUCT AuthoredFile`.
4. **Funciones:**
   - adaptador de autoría (sin componente, EVO-01): `slotOf`, `validSlotName`, `findSource`, `diagnosticsForFile`, `discoverAgent`, `closedChannelDiagnostics`, `hasErrors`;
   - AgentCore (CMP-011), dentro de "validar un AgentConfig antes de que arranque cualquier ejecución": `requireActivatableManifest`.

## 3. Decisiones de diseño centrales

- **Es un adaptador de autoría, no un componente** (EVO-01): produce los mismos contratos que ya existen (AgentConfig, CapabilityDescriptor, ConnectionDescriptor…).
- **La ruta es la identidad:** el nombre de cada fuente sale de su ruta; dos fuentes con el mismo nombre en la misma ranura son un error.
- **Los defaults ocupan las mismas ranuras:** un archivo propio con el mismo nombre los reemplaza.
- **El markdown es dato; el código necesita confianza:** sin confianza, un archivo de código es un diagnóstico ERROR.
- **Las entradas no se abren solas:** un canal sin regla de admisión se descubre, pero no escucha (WARNING).
- **Nada se infiere:** lo que no está en el manifiesto no existe para el runtime, y el manifiesto se expone (P-39).
- **INV-E27 lo hace cumplir AgentCore**, que ya valida la configuración antes de activar.

## 4. Archivos creados

- `book/chapters/48-agente-como-directorio/chapter.md` (secciones 0–21, 16 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-48-agente-como-directorio.md`, `kb/03-Contratos/C-065-agentmanifest.md`, `C-066-authoringdiagnostic.md`
- `diagrams/archify/capitulo-48-agente-como-directorio.json` + `rendered/…html`; `diagrams/mindmap/chapter-48.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/contracts.yaml`: C-065, C-066
- `registry/glossary.yaml`: Filesystem-First Authoring, AgentManifest, AuthoringDiagnostic
- `book/book.yaml`; CH-47 `next_chapter: CH-48`
- KB: índices de contratos y capítulos; glosario; navegación de CH-47

## 6. Resultado real del pipeline

- **Rojo:** 22 errores de capítulo con solo el frontmatter; sin deudas con destino CH-48.
- **Registro:** `validate-contracts` OK (66), `validate-components` OK (29), `validate-debt` OK.
- **Verde:** `validate-chapter` falló primero porque el frontmatter citaba EVO-10 (el validador solo admite P-, INV- e INV-E- allí; ningún capítulo cita EVO en el frontmatter). Quitado del frontmatter y citado en el cuerpo: OK (22 secciones, 16 bloques, 2 contratos, 0 componentes). `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **`build-all` exit 0 con 49/49 capítulos y 49/49 retrieval sets.** `dist/book.pdf` 7,1 MB; `Missing character` en 6.
- **Archify:** showcase 9/9, 0/0; `check` 9/9; visual-check pass, revisado a 1440×900 (claro y oscuro); 11 mensajes, 5 participantes.

## 7. Definition of Done

- [x] Validadores de CH-48 en verde; C-065, C-066 registrados.
- [x] 49/49 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-47 `next_chapter` = CH-48.

## 8. Deuda

- Sin deuda nueva. Lo de §18 del capítulo se declaró explícitamente:
  - un ámbito global agrega un origen más con la misma estructura: no es deuda;
  - el lenguaje de los archivos de código lo elige cada despliegue: no es deuda;
  - registrar la confianza es del adaptador de autoría: no es deuda;
  - recargar en caliente es una versión nueva, cubierta por CH-45: no es deuda.
