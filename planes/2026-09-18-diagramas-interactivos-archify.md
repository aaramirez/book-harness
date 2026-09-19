# 2026-09-18 — Diagramas Interactivos con Archify

## Por qué

El usuario se quejó explícitamente: "los gráficos, flujos, no se ven bien, necesito poderlos
navegar". Los mapas mentales Graphviz existentes (`diagrams/mindmap/*.diagram` → SVG embebido por
capítulo, uno por cada `chapter.md`) son estáticos: no tienen búsqueda, no trazan rutas entre
nodos, no ofrecen vistas guiadas ni tema oscuro, y su geometría automática de Graphviz no está
pensada para lectura exploratoria. Esta queja pide un apartado SEPARADO — nunca un reemplazo — con
diagramas navegables, curados a mano, sobre el contenido real ya publicado del libro.

## Qué es Archify

[Archify](https://github.com/tt-a1i/archify) es un skill/CLI (`~/.agents/skills/archify`) que
genera HTML autocontenido con SVG inline a partir de una especificación JSON tipada
(`architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`). El HTML resultante incluye:
pan/zoom, búsqueda, trazado de relaciones ("route/reach"), vistas guiadas (`meta.views`), tema
claro/oscuro, y exportación a imagen. El flujo de autoría es: escribir el JSON candidato → validar
con `archify validate --quality showcase` hasta 0 errores/warnings → congelar con `archify deliver`
(que además verifica hashes SHA-256 de especificación y artefacto) → `archify visual-check` para
evidencia de navegador real (contención en 1440×900 / 1600×1000 / 1920×1080 / 2048×1320, ambos
temas).

## Los 5 diagramas

Fuente en `diagrams/archify/<slug>.json`, entregado en `diagrams/archify/rendered/<slug>.html`.

1. **`nucleo-del-arnes`** (architecture) — "El Núcleo del Arnés". Los 11 componentes de Article
   III con las 12 conexiones reales que `runAgentTurnEndToEnd` (CH-12) ejercita, en el orden real
   de invocación. `sources` en cada nodo apunta al capítulo que lo introdujo (CH-01..CH-11). 3
   vistas guiadas: ciclo cognitivo, gobierno de una tool call, persistencia y eventos.

2. **`capa-enterprise`** (architecture) — "La Capa de Gobierno Enterprise". Los 11 componentes de
   Amendment v1.1 (CMP-012..CMP-022, verificados contra `registry/components.yaml`), no solo 8:
   se decidió mostrar los 11 para que el diagrama sea la referencia completa de esa capa, usando
   el campo `tag` de cada nodo para indicar qué gobierna (p.ej. "antecede a AgentCore") y las
   `cards` para documentar en prosa honesta que **solo una arista componente-a-componente es real**
   en todo el libro: `OperationalController → HandoffCoordinator` (CH-27, kill switch). El resto
   de relaciones de gobierno (AdmissionController sobre AgentCore, CredentialBroker/IdempotencyGuard
   sobre ToolRuntime, DataGovernanceEngine sobre ContextEngine, etc.) se documentan como prosa —
   nunca como flechas inventadas — porque CH-26/CH-27 nunca las cablean como llamadas directas
   entre esas dos fichas: pasan siempre a través de `runGovernedEnterpriseTurn`. Las tres
   exclusiones deliberadas (`AgentCommunicationGateway`, `EvaluationHarness`,
   `ExecutionFabricAdapter` — otra escala, no un turno individual) también se documentan en las
   `cards`, citando CH-26 §18/CH-27 §19 con honestidad.

   **Decisión de diseño explícita**: no se fusionó este diagrama con el 3 (`turno-gobernado`) a
   pesar de la escasez de aristas reales, porque la vista arquitectónica (qué existe y qué
   gobierna a qué, sin tiempo) y la vista de flujo (en qué orden se invoca dentro de un turno) responden
   preguntas distintas del lector, y el propio libro las trata como capítulos distintos (CH-14..24
   vs. CH-26/27). Las 5 fuentes del encargo original se mantuvieron intactas.

3. **`turno-gobernado`** (workflow, schema v2) — "El Turno Gobernado de Punta a Punta". La traza
   completa de `runGovernedEnterpriseTurn` (CH-26, camino feliz de 17 pasos) más los dos caminos de
   excepción de CH-27 (`interruptGovernedEnterpriseRunWithKillSwitch`,
   `escalateGovernedEnterpriseRunAfterSevereDenial`), convergiendo ambos en el mismo
   `HandoffCoordinator.createHandoffPackage`. 4 lanes (Ingreso / Núcleo Cognitivo / Gobierno
   Enterprise / Control y Traspaso) × 6 columnas. Para caber en 6 columnas sin perder ningún
   componente real, se combinó `CredentialBroker` + `IdempotencyGuard` en un único nodo ("Credential
   + Idempotency", con `tag` citando ambos CH) y se anotó `AuditLedger`/`EventBus` como `tag` del
   nodo `ToolRuntime` en vez de darles nodo propio — una simplificación de presentación, no de
   contenido: las funciones reales siguen citadas por su nombre exacto en `sublabel`/`tag`/`cards`.

4. **`un-agentrun-real`** (sequence) — "Un AgentRun de Punta a Punta". 8 participantes (AgentCore,
   AgentLoop, ContextEngine, ModelGateway, CapabilityRegistry, PolicyEngine, ToolRuntime, EventBus)
   con los nombres de función reales de CH-12 como labels de mensaje
   (`activateAgent`/`beginAgentInitialization`, `assembleContextSnapshot`, `invokeModelForTurn`,
   `resolveModelProposedToolCall`, `evaluatePolicyForToolCall`, `executeToolCall`,
   `emitAndDistribute`). 3 `segments` (Activación / Razonamiento / Ejecución). Comprimido a 12
   mensajes (de los 15 pasos reales de CH-12) fusionando las dos emisiones intermedias de EventBus
   en `note`s de los mensajes vecinos, para que el diagrama quepa sin overflow a 1440×900.

5. **`estados-de-un-run`** (lifecycle) — "Los 11 Estados de un AgentRun". Los 11 valores reales de
   `AgentRunStatus` (C-013). 3 lanes geométricas (el renderer de lifecycle solo permite 3 bandas
   visuales reales — `main`, un band intermedio compartido, y `terminal` — sin importar cuántos
   `lanes.id` se declaren; ver hallazgo técnico abajo). Transiciones citadas contra su capítulo
   real: `CREATED→INITIALIZING` y `INITIALIZING→RUNNING` (AgentCore, CH-11);
   `RUNNING→WAITING_FOR_MODEL`/`WAITING_FOR_TOOL` (AgentLoop.runTurn, CH-01);
   `RUNNING→WAITING_FOR_HUMAN` (HumanInteractionService, CH-06/13);
   `RUNNING→COMPLETED` (AgentLoop, camino feliz); `RUNNING→FAILED`/`EXPIRED`
   (ExecutionController.terminateAgentRunOperationally, CH-07/13); y, como ruta explícitamente
   INDEPENDIENTE del ciclo normal (INV-E14), `RUNNING→CANCELLED` vía
   `OperationalController.applyControlDirective` (kill switch, CH-18/27).

   **Hallazgo honesto que cambia una premisa del encargo original**: se verificó con `grep` sobre
   los 28 capítulos que `AgentRunStatus.PAUSED` **nunca** es producido por ningún pseudocódigo real
   del libro — solo aparece declarado en el `ENUM` de CH-00/CH-01. La cita "todos los 11 estados ya
   fueron ejercitados" que motivó una instrucción original del encargo proviene de una frase de
   CH-13 §17 que, verificada literal por literal contra el propio pseudocódigo de ese y otros
   capítulos, no cuadra aritméticamente (afirma que CH-12 "cerró siete" estados, pero una cuenta
   exhaustiva por grep de las asignaciones reales de cada uno de los 11 valores en CH-12 no lo
   sostiene). En vez de repetir una cifra que no pude verificar, el diagrama documenta el hallazgo
   real y defendible: PAUSED es el único valor sin una sola transición ejercitada por código, y esto
   se cita en una card ("Un hallazgo honesto") en vez de forzar el conteo original.

## Decisiones de mapeo — tipos y geometría

- **Tipos de componente** (`architecture`/`sequence`): siguiendo el vocabulario cerrado de Archify
  (`frontend|backend|database|cloud|security|messagebus|external`) — `AgentLoop`/`AgentCore` =
  `backend` (con `tag: "el corazón del turno"` en vez de un tipo `emphasis` inexistente para
  componentes, ya que `variant: emphasis` es de conexiones, no de nodos); `ModelGateway` = `cloud`
  (proveedor externo de inferencia); `PolicyEngine`/`AdmissionController`/`CredentialBroker`/
  `IdempotencyGuard`/`OperationalController`/`DataGovernanceEngine` = `security`; `EventBus` =
  `messagebus`; `SessionManager`/`AuditLedger` = `database`; `HumanInteractionService`/
  `HandoffCoordinator` = `external`.
- **Geometría de arquitectura**: Archify exige rutas puramente ortogonales (horizontal/vertical) y
  penaliza automáticamente el cruce de una relación sobre un nodo no relacionado. La iteración real
  de `nucleo-del-arnes` requirió mover manualmente 6 `labelAt` y reducir el ancho total del
  `viewBox` (de 1450 a 1350) recortando subtítulos largos, para satisfacer el check
  `composition/desktop-readability` (mínimo 6px de fuente proyectada a 1440px de viewport).
- **Geometría de lifecycle — hallazgo técnico documentado para el futuro**: el renderer de
  lifecycle colapsa CUALQUIER lane que no se llame literalmente `"main"` o `"terminal"` en una
  única banda intermedia compartida (columnas 0..2), sin importar cuántos `lanes.id` distintos se
  declaren en el JSON — un lane con id `"esperas"` y otro con id `"control"` terminan en la MISMA
  fila visual. Esto no está en la referencia rápida del `SKILL.md` (sí insinuado en su nota sobre
  "event/terminal column N alineado bajo main column N+2") y solo se descubrió iterando contra los
  mensajes de error de `validate`. `estados-de-un-run.json` usa 3 `lanes` (`main`, `esperas`,
  `terminal`) en vez de los 4 sugeridos originalmente, y compensa la pérdida de separación visual
  con routing explícito (`via` de 3-4 puntos, siempre ortogonal) para que las 6 transiciones que
  salen de `RUNNING` hacia bandas inferiores no se crucen entre sí ni atraviesen nodos ajenos.
- **`schema_version: 2`** se usó para `turno-gobernado` (todo workflow nuevo debería usarlo, per
  SKILL.md).

## Cómo se integró al build (copia, no regeneración)

`scripts/build-web` gana una función nueva, `buildArchifyDiagramsSection()`, invocada al final de
`main()` — **no toca** ninguna lógica existente de capítulos/mapa mental. El paso:

1. Si `diagrams/archify/rendered/` no existe (o existe vacío), se salta limpiamente con un mensaje
   informativo y `build-web` sigue teniendo exit 0 — el pipeline zero-dependencias del proyecto
   sigue funcionando igual para cualquiera que clone el repo sin haber corrido el paso de autoría
   de Archify (que si depende de Node + Chrome para `visual-check`, no del resto del proyecto).
2. Si existe, copia cada `.html` (excluyendo los sidecars `*.visual-check.html/.png/.json` que dej
   a `archify visual-check` junto al artefacto real) **byte a byte, sin modificar su contenido**
   hacia `dist/web/diagramas/<mismo-nombre>.html` — nunca se re-renderiza ni se reprocesa: son
   artefactos ya firmados (SHA-256 verificado) por el propio `archify deliver`.
3. Genera `dist/web/diagramas.html`, una página hub con el mismo `BASE_CSS` del resto de la Web,
   una explicación de en qué difieren estos diagramas de los mapas mentales por capítulo, y una
   tarjeta por diagrama (título + descripción + link).
4. Añade un link nuevo (`Diagramas Interactivos (Archify)`) debajo del link a `mapa.html` en
   `dist/web/index.html`, vía un `replace` de string sobre el HTML ya generado — no se modificó
   `renderIndexPage` directamente para mantener el diff mínimo y localizado.

**Por qué copia y no regeneración**: Archify no es una dependencia del proyecto (no está en
`package.json`, no se invoca desde ningún `scripts/build-*` existente) y depende de Node CLI +
Chrome headless para `visual-check` — cablearlo directamente al pipeline zero-dependencias de
`build-all` habría violado esa propiedad para cualquiera que solo quiera compilar el libro. Los 5
HTML de `diagrams/archify/rendered/` se tratan como artefactos versionados en git (igual que
`diagrams/mindmap/*.diagram` se versionan como fuente), listos para copiar.

## Verificación real ejecutada

- Los 5 `validate --quality showcase` terminaron en `"ok": true`, `"errors": 0`, `"warnings": 0`
  (evidencia JSON completa en la sesión de trabajo; resumen: `nucleo-del-arnes` y `capa-enterprise`
  con 9/9 checks + evidencia de repositorio verificada contra el commit `44a70a2`;
  `un-agentrun-real` con `column_fit: spread`; `turno-gobernado` con `schema_version: 2`;
  `estados-de-un-run` fue el más costoso de iterar — múltiples rondas de `edge-through-node`,
  `orthogonal-arrows` y `composition/desktop-readability` hasta 0/0).
- Los 5 `deliver` terminaron en `"ok": true` con SHA-256 y byte count de especificación y artefacto
  reportados.
- Los 5 `visual-check` terminaron en `"status": "pass"` con `containment.status: "pass"` en
  1440×900 y 1600×1000 (además de 1920×1080/2048×1320 donde aplicó ajuste de `viewBox`) — dos
  diagramas (`un-agentrun-real`, `estados-de-un-run`) requirieron reducir `viewBox` height
  iterativamente (800→650→610→650 con cards más cortas) hasta que `scrollHeight <= innerHeight`
  en el viewport más pequeño.
- `rm -rf dist && ./scripts/build-all`: exit 0, dos corridas limpias completas. `dist/book.pdf` con
  **719 páginas** (idéntico al conteo previo a este cambio). `dist/web/chapters/` con 28 archivos,
  `dist/web/frontmatter/` con 2, `dist/web/mapa.html` presente y sin cambios.
- `dist/web/diagramas.html` existe y enlaza a los 5 `dist/web/diagramas/*.html`; se comparó tamaño
  en bytes de cada copia contra su original en `diagrams/archify/rendered/*.html` — coinciden
  exactamente (819418/813583/819947/814687/819253 bytes respectivamente).
- `dist/web/index.html` contiene el link `<a href="diagramas.html">Diagramas Interactivos
  (Archify)</a>` y el archivo de destino existe.
- Se detectó y corrigió un bug real durante la verificación: el filtro inicial de
  `buildArchifyDiagramsSection()` copiaba también los sidecars `*.visual-check.html` que
  `archify visual-check` deja junto a cada artefacto (10 archivos copiados en vez de 5) — corregido
  excluyendo cualquier nombre que contenga `.visual-check.`.

## Decisiones no cubiertas explícitamente por el encargo original

- Se usaron los 11 componentes de Amendment v1.1 en `capa-enterprise` (no solo 8), documentando en
  `cards` cuáles 8 están cableados dentro de un turno y cuáles 3 operan a otra escala — más
  completo y más honesto que recortar la ficha a los 8 "activos".
- Se corrigió, con evidencia de grep, la premisa de que "los 11 estados ya fueron ejercitados" —
  PAUSED no lo fue nunca — y se documentó el hallazgo real en vez de forzar la cifra original.
- Se combinaron `CredentialBroker`+`IdempotencyGuard` (y se anotó `AuditLedger`/`EventBus` como
  `tag`) en `turno-gobernado` para caber en las 6 columnas que permite `schema_version: 2` sin
  perder ningún nombre real de función.
