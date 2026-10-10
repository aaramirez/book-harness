# Plan / Registro de ejecución — Capítulo 44: Invocación Durable entre Agentes y A2A

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `cap-44-invocacion-entre-agentes` mergeada a `main`, sobre `43245b8`.
**Release:** v0.3. Deudas con destino CH-44: D-020, D-023.

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-44 (§6).
- CH-15 (`AgentCommunicationGateway`, `AgentCommunicationMessage`, `DelegationGrant`, `authorizeAgentCommunicationMessage`), CH-18 (`issueControlDirective`, `KILL_SWITCH`), CH-31 (`CallerSnapshot`, `buildCallerSnapshot`), CH-32 (`StepRecord`, recuperación de pasos), CH-33 (`ParkedWait`, `WaitKind`), CH-34/CH-37 (dirección de salida del canal), CH-43 (`requireChildWithinParent`, `rollUpChildUsage`).
- Constitución: P-18 (semántica independiente del protocolo), P-19 (interoperabilidad por adaptador), P-20 (delegación interna ≠ federación externa), P-21 (autoridad delegada explícita y mínima), INV-E03..E06, INV-E21.

## 1. Objetivo

Que un agente pueda invocar a otro, dentro del arnés o afuera, como un **registro durable** con dueño, estado, profundidad y presupuesto heredado: que sobreviva a un reinicio sin repetirse, que las esperas del hijo lleguen al canal del padre (D-023), que la identidad del llamante cruce solo hacia adentro (D-020) y que A2A sea un adaptador, nunca una dependencia del núcleo.

## 2. Alcance decidido

**0 componentes + 2 contratos + 1 contrato modificado:**
1. **C-058 `AgentInvocation`:** invocationId, boundary, parentRunId, targetAgentRef, skill, owner, depth, childRunId?, remoteTaskRef?, status, budget, pendingWaitId?, result?, error?, openedAt, expiresAt?.
2. **C-059 `AgentCard`:** agentRef, description, skills, boundary, endpointRef?, authScheme?.
3. **C-024 v2:** `invocationId?`.
4. **Embebidos:** `ENUM AgentInvocationStatus` (WORKING, INPUT_REQUIRED, AUTHORIZATION_REQUIRED, COMPLETED, FAILED, CANCELLED), `STRUCT InvocationUpdate`.
5. **Funciones:**
   - AgentCommunicationGateway (CMP-013): `invocationIdForStep`, `requireAdvertisedSkill`, `forwardedCallerFor` (D-020), `openAgentInvocation`, `applyInvocationUpdate`, `invocationStatusForWait` y `surfaceChildWait` (D-023);
   - integración: `invokeAgentDurably`, `completeAgentInvocation`, `cancelChildInvocation`.

| Deuda | Cómo se resuelve |
|---|---|
| D-020 | `forwardedCallerFor`: hacia un agente interno el hijo recibe el mismo `CallerSnapshot` (la autoridad la acota el `DelegationGrant`); hacia uno externo el `Principal` no cruza nunca |
| D-023 | `surfaceChildWait`: la espera de un hijo interno pone la invocación en `INPUT_REQUIRED` / `AUTHORIZATION_REQUIRED` con su `waitId`; el padre la publica en su canal y la respuesta se entrega a la espera del hijo |

## 3. Decisiones de diseño centrales

- **Sin componente nuevo:** el Gateway ya es la frontera entre agentes (P-18..P-21); la invocación es la forma durable de un mensaje que la cruza.
- **El id de la invocación se deriva del paso que la abrió.** Recuperar el paso después de un reinicio encuentra la invocación ya abierta; nunca lanza un segundo hijo.
- **Para el padre, invocar es una tool call larga:** el run queda en `WAITING_FOR_TOOL` y el resultado vuelve como `ToolResult`.
- **La identidad cruza hacia adentro, no hacia afuera.** Un agente externo autentica al arnés con su `authScheme` (credencial del broker, CH-16), nunca al usuario.
- **El presupuesto del hijo sale del saldo del padre** (`requireChildWithinParent`, CH-43) y su gasto vuelve (`rollUpChildUsage`).
- **La profundidad se acota explícitamente** (`maxDepth` de la política del despliegue), además de lo que ya acota el saldo.
- **Los estados tienen la forma de una tarea A2A, pero el contrato es del arnés:** el adaptador A2A traduce en ambas direcciones (INV-E04, INV-E05).

## 4. Archivos creados

- `book/chapters/44-invocacion-entre-agentes/chapter.md` (secciones 0–21, 17 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-44-invocacion-entre-agentes.md`, `kb/03-Contratos/C-058-agentinvocation.md`, `C-059-agentcard.md`
- `diagrams/archify/capitulo-44-invocacion-entre-agentes.json` + `rendered/…html`; `diagrams/mindmap/chapter-44.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/contracts.yaml`: C-024 v2, C-058, C-059
- `registry/glossary.yaml`: Durable Agent Invocation, AgentInvocation, AgentCard
- `registry/debt.yaml`: D-020, D-023 → `resolved` (CH-44)
- `book/book.yaml`; CH-43 `next_chapter: CH-44`
- KB: C-024 a v2; índices de contratos y capítulos; glosario; navegación de CH-43

## 6. Resultado real del pipeline

- **Rojo:** 22 errores de capítulo con solo el frontmatter; `validate-debt` marcó D-020 y D-023 vencidas.
- **Registro:** `validate-contracts` OK (59), `validate-components` OK (29), `validate-debt` OK (8 open, 34 resolved, 6 out_of_scope).
- **Verde:** `validate-chapter` falló primero por 6 identificadores sin declarar (`AgentInvocationId`, `WaitId`, `StepId`, `ActorId`, `AgentCommunicationMessageId`, `DelegationGrantId`); agregados a la tabla de §6, OK (22 secciones, 17 bloques, 2 contratos, 0 componentes). `validate-retrieval-set` OK (4/4/2/1/3/4). Grep de plataformas vacío.
- **`build-all` exit 0 con 45/45 capítulos y 45/45 retrieval sets.** `dist/book.pdf` 6,5 MB; `Missing character` en 6.
- **Archify:** showcase 9/9, 0/0; `check` 9/9; visual-check pass, revisado a 1440×900 (claro y oscuro); 11 mensajes, 4 participantes.

## 7. Definition of Done

- [x] Validadores de CH-44 en verde; C-058, C-059 registrados; C-024 en v2 con `modified_by: [CH-44]`; D-020, D-023 resolved.
- [x] 45/45 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-43 `next_chapter` = CH-44.

## 8. Deuda

- Sin deuda nueva. Lo de §18 del capítulo se declaró explícitamente:
  - descubrir agentes: las tarjetas se declaran en la configuración del despliegue: no es deuda;
  - recibir invocaciones externas entra por la admisión existente con un principal SERVICE: no es deuda;
  - los resultados parciales en streaming los acumula el adaptador: no es deuda;
  - qué pasa con un hijo activo al cambiar de versión ya está planeado como INV-E22 en CH-45: no es deuda.
