# Plan / Registro de ejecución — Capítulo 28: Entradas que Llegan Durante el Turno: Steering y Follow-up

**Fecha:** 2026-09-25
**Estado:** ✅ Completado (2026-09-25). Rama `cap-28-steering-follow-up` mergeada a `main`, sobre `b182422` (Fase 0 completa, Amendment v1.2 ratificado).

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: plan de extensión; ficha CH-28 en §6 y procedimiento en §8.
- `2026-09-13-capitulo-01-agent-loop.md`: origen de `AgentLoop` (CMP-001) y de `runTurn`, que este capítulo **no modifica**.
- `2026-09-14-capitulo-13-integracion-caminos-de-gobierno.md`: `resumeTurnWithObservation`, el punto donde, en una integración futura (CH-36), se aplican las entradas pendientes.
- `2026-09-14-capitulo-06-human-interaction-service.md`: frontera que este capítulo debe distinguir con más cuidado. Un mensaje de steering **no** es una resolución humana.

---

## 1. Objetivo

Primer capítulo del Tramo 4 ("enriquecer el núcleo de agente único"). Modelar qué pasa con un mensaje del usuario que **llega mientras el turno todavía corre**:
- **steering** (corrección), que se aplica antes de la próxima llamada al modelo;
- **follow-up**, que se aplica solo cuando el agente iba a terminar.

No se cancela ninguna tool en ejecución, y `runTurn` (CH-01) queda intacto.

## 2. Alcance decidido

Exactamente **0 componentes + 1 contrato**:

1. **Contrato nuevo `PendingInput` (C-036).** Una entrada del usuario que llegó durante un turno en curso: `id`, `runId`, `kind` (`PendingInputKind`: STEER / FOLLOW_UP), `message: AgentMessage` y `receivedAt`.
2. **Estructuras embebidas, sin contrato propio** (mismo patrón que `ExecutionUsage` o `ContextBlock`):
   - `ENUM PendingInputKind`, `ENUM PendingInputMode` (ONE_AT_A_TIME / ALL), `ENUM TurnBoundary` (BEFORE_MODEL_CALL / WOULD_COMPLETE);
   - `STRUCT PendingInputQueue` (dos listas, con un modo por lista);
   - `STRUCT PendingInputSelection`.
3. **`AgentLoop` (CMP-001) se amplía en prosa y en pseudocódigo.** La decisión "¿en qué frontera del turno se aplica una entrada pendiente?" es **continuación del turno**, que ya está en su `owns` literal (Article III: "turn lifecycle", "continuation"). Por eso **no hace falta cambiar su ficha** en `registry/components.yaml`.
4. **Funciones nuevas:**
   - `enqueuePendingInput`
   - `takeByMode`
   - `selectPendingInputsAtBoundary`
   - `resolveCompletionWithPendingInput`: convierte el `modelFinished` del modelo en una **propuesta** que el arnés anula si queda un follow-up o un steering pendiente (P-10).
5. **Eventos nuevos en `AgentEventType`:** `PENDING_INPUT_QUEUED`, `PENDING_INPUT_APPLIED`.
6. **Errores nuevos** (`VALIDATION`): `PENDING_INPUT_ON_TERMINAL_RUN`, `PENDING_INPUT_RUN_MISMATCH`.

**Desvío de la ficha §6 del plan de extensión:** el modo (ONE_AT_A_TIME / ALL) vive en la **cola**, no en cada `PendingInput`, como en pi (`steeringMode` / `followUpMode` son propiedades de la cola). Un mensaje no elige su propio modo de entrega.

## 3. Decisiones de diseño centrales

- **`runTurn` no se toca.** El follow-up se resuelve **antes** de llamar a `runTurn`, pasando un `modelFinished` efectivo. Así CH-01..CH-27 no cambian, y la decisión sigue siendo determinística.
- **El steering nunca interrumpe una tool en ejecución** (INV-07: el `ToolResult` vuelve siempre como observación). Solo se aplica en la frontera `BEFORE_MODEL_CALL`.
- **La prioridad del steering sobre el follow-up** en `WOULD_COMPLETE`: una corrección pendiente se aplica antes que un mensaje "para después".
- **Una entrada pendiente no es autorización:** un steering que diga "aprobado" no resuelve una `HumanInteractionRequest` (INV-15, P-13). Tampoco es cancelación (INV-10): cancelar sigue siendo de ExecutionController / OperationalController.

## 4. Archivos creados

- `book/chapters/28-steering-follow-up/chapter.md` (secciones 0–21, 10 bloques de pseudocódigo, `retrieval_set` completo)
- `kb/04-Capitulos/ch-28-steering-follow-up.md`, `kb/03-Contratos/C-036-pendinginput.md`
- `diagrams/archify/capitulo-28-steering-follow-up.json` + `rendered/capitulo-28-steering-follow-up.html`
- `diagrams/mindmap/chapter-28.diagram` (generado por `build-mind-map`)
- este plan

## 5. Archivos modificados

- `book/book.yaml`: entrada CH-28
- `book/chapters/27-integracion-enterprise-caminos-de-control/chapter.md`: `next_chapter: CH-28`
- `registry/contracts.yaml`: C-036 `PendingInput`
- `registry/glossary.yaml`: Steering, Follow-up, Turn Boundary, PendingInput
- `kb/04-Capitulos/00-Índice.md`, `kb/03-Contratos/00-Índice.md`, `kb/05-Glosario/Glosario.md`, `kb/04-Capitulos/ch-27-enterprise-control.md` (navegación)
- `diagrams/mindmap/full-book.diagram` (regenerado)

## 6. Resultado real del pipeline

- **Rojo** (paso 2): `validate-chapter` sobre el frontmatter solo → exit 1, 20 errores (secciones faltantes + C-036 sin registrar).
- **Registro** (paso 3): `validate-contracts` OK (36), `validate-components` OK (22).
- **Verde** (paso 5): `validate-chapter` OK (22 secciones, 10 bloques pseudocode, 1 contrato); `validate-retrieval-set` OK (4 guías, 4 recall, 2 explain, 1 interleaved con CH-06, 2 flashcards, 4 calibración).
- **Pipeline** (paso 7): `build-all` exit 0; `dist/book.pdf` 4,16 MB; `chapter-28.diagram` generado.
- **Hallazgo (preexistente, no causado por este capítulo):** el PDF emite advertencias `[WARNING] Missing character` por los caracteres de dibujo de cajas (`─ │ ├ └ ▼`) de los diagramas de texto: **1733 en `main`** (medido en un worktree limpio de `b182422`) y 1768 con CH-28 (+35 del diagrama de texto de su §10). Causa: la fuente monoespaciada por defecto de pandoc/xelatex no trae esos glifos, así que se ven como ausentes en el PDF. Propuesta de tooling (fuera de este incremento): pasar `-V monofont="Consolas"` (o DejaVu Sans Mono) en `scripts/build-pdf`.

## 7. Definition of Done

- [x] `validate-chapter` y `validate-retrieval-set` de CH-28 en verde.
- [x] `validate-contracts` (36) y `validate-components` (22) en verde.
- [x] `build-all` exit 0, sin warnings nuevos.
- [x] Diagrama Archify `capitulo-28-steering-follow-up` validado: showcase 9/9, 0/0; deliver con spec `14cf0662…`; visual-check pass; publicado en `dist/web/diagramas/`.
- [x] KB: `kb/04-Capitulos/ch-28-steering-follow-up.md`, `kb/03-Contratos/C-036-pendinginput.md`, índices y glosario.
- [x] `next_chapter` de CH-27 = CH-28.

## 8. Deuda intencional hacia el próximo capítulo

- La cola de entradas pendientes no es durable (CH-32/CH-33).
- Ninguna función de integración aplica todavía la cola (primer cableado: CH-36).
- No se interrumpe la generación del modelo en curso (requiere llamadas recuperables, CH-32).
- Canales e identidad del remitente: CH-34 y CH-31.
- CH-29 hereda el crecimiento del historial que el steering y el follow-up producen.
