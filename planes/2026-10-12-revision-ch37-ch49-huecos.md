# Plan / Registro de ejecución — Revisión de CH-37 y CH-49: dos huecos del pseudocódigo

**Fecha:** 2026-10-12
**Estado:** ✅ Completado (2026-10-12). Rama `rev-ch37-ch49-huecos` mergeada a `main`, sobre `59288a1`.
**Origen:** la regeneración del set visual de book-harness v0.3 en el vault `arnes-ai` (`docs/diagramas/book-harness/`). Sus agentes de exploración encontraron los dos huecos y se verificaron contra el texto.
**Decisión del autor:** "hazlo y también el patch" (2026-10-12). Es una corrección de pseudocódigo: no cambia contratos, componentes ni ADRs, y no abre release.

## 1. Problema

- **CH-49:** `openConnectedGovernedTurn` produce `ConnectedTurnStart.contextBlocks`: los candidatos recuperados, gobernados y recortados con el techo de la audiencia (`ch49:557-563`). Pero `runConnectedGovernedStep` invoca al modelo solo con `selection.messages` (`ch49:792-795`). Ninguna función une los bloques gobernados con la llamada, así que el paso 4 del turno conectado no tenía efecto.
- **CH-37:** `parkForMissingCredential` llama a `parkRun` pero no a `parkedAgentState` (`ch37:749-771`). Mientras esperaba la autorización por la credencial faltante, el run seguía RUNNING, aunque `runStatusForWait(AUTHORIZATION)` dice `PAUSED` (CH-33).

## 2. Cambio

**CH-49 (`book/chapters/49-integracion-conectada/chapter.md`):**
- **§6:** `AgentMessage` (C-001) en la lista de tipos heredados.
- **§11, nota de revisión y una función nueva:** `connectedModelMessages(contextBlocks, selection) -> List<AgentMessage>`. Produce un `AgentMessage` USER por bloque, con la convención de CH-12 y CH-26, y después agrega las entradas pendientes.
- **§11, en `runConnectedGovernedStep`:**
  - nuevo parámetro `contextBlocks: List<ContextBlock>`;
  - la llamada al modelo usa `connectedModelMessages(contextBlocks, selection)`;
  - un paso que toma su propuesta del journal no llama al modelo.
- **§16:** dos tests nuevos, `GovernedContextBlocksReachTheModelCall` y `ContextBlocksPrecedeThePendingInputsInTheModelCall`.

**CH-37 (`book/chapters/37-esperas-credenciales-canales/chapter.md`):**
- **§6:** `AuthorizationParking` suma `pausedState: AgentState`. Es un tipo embebido y no hay contrato que cambie.
- **§11:** nota de revisión. `parkForMissingCredential` aplica `parkedAgentState(state, wait)` (CH-33) y devuelve el estado PAUSED.
- **§12:** transición `RUNNING → PAUSED`.
- **§16:** test `MissingCredentialParksTheRunAsPaused`.

**Sin cambios:**
- CH-33: `parkedAgentState` y `runStatusForWait` ya existían.
- CH-41: describe el flujo en prosa.
- Retrieval sets.
- Registros: el cambio no introduce entidades nuevas ni cambia contratos.

## 3. Resultado real

- `validate-chapter` / `validate-retrieval-set` OK para CH-37 (16 bloques de pseudocódigo) y CH-49 (15).
- **`build-all` exit 0 con 50/50 capítulos y 50/50 retrieval sets.** `dist/book.pdf` 7,2 MB; `Missing character` en 6 (la línea base de CH-10).

## 4. Deuda

- Sin deuda nueva. La inconsistencia de plano de CredentialBroker (`ch25:334` dice "Data & Context"; `registry/components.yaml:101` dice "Capability & Integration") queda fuera de esta revisión. Se anota para una próxima.
