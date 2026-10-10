# Plan / Registro de ejecución — Capítulo 43: Presupuestos que se Heredan

**Fecha:** 2026-10-10
**Estado:** ✅ Completado (2026-10-10). Rama `cap-43-presupuestos-heredados` mergeada a `main`, sobre `780b861`.
**Release:** v0.3. Deuda con destino CH-43: D-026.
**ADR:** ADR-004 **Accepted** (2026-10-10, aprobado por el autor) con dos ajustes aprobados: `consumed` opcional y `sandboxLimits` (D-026).

**Depende de:**
- `2026-09-24-extension-v0-2-v0-3-eve-pi-conexiones.md`: ficha CH-43 (§6).
- CH-07 (`ExecutionController`, `ExecutionBudget`, `ExecutionUsage` embebida, `evaluateExecutionContinuation`), CH-35 (entorno aislado), CH-39 (`accumulateUsage`).
- Propuesta de eve E6: los hijos de un lote se reparten el saldo del padre, y el lote siguiente ve el saldo menos lo que consumieron.
- Constitución: P-09 (la confiabilidad single-agent antes que la complejidad multi-agente: el presupuesto jerárquico va antes de CH-44), INV-09, INV-E06, INV-E21 (un hijo nunca excede el saldo del padre).

## 1. Objetivo

Que un run pueda delegar trabajo en hijos con una **parte** de su presupuesto, nunca más de lo que le queda, y que lo que gastan los hijos se descuente del padre. Además, darle al entorno aislado límites de CPU, memoria y disco (D-026).

## 2. Alcance decidido

**0 componentes + 1 contrato + 1 contrato modificado:**
1. **C-057 `ExecutionUsage`:** se promueve desde la estructura embebida de CH-07, sin cambiar sus campos.
2. **C-012 `ExecutionBudget` v2:** `parentRunId?`, `consumed?` (`ExecutionUsage`) y `sandboxLimits?`.
3. **Embebidos:** `STRUCT SandboxLimits` (maxCpuMillis, maxMemoryMb, maxDiskMb) y `STRUCT SandboxUsage`.
4. **ExecutionController (CMP-007)**, dentro de su `owns` ("budgets", "runtime limits"): `allocateChildBudget`, `childBudgetWithinParent`, `requireChildWithinParent`, `rollUpChildUsage` y `sandboxLimitsExceeded`.

## 3. Decisiones de diseño centrales

- **Se reparte lo compartible y se acota lo demás.**
  - Tool calls, tokens y costo se dividen entre los hijos del lote.
  - El tiempo restante no se divide: los hijos de un lote corren en paralelo, y cada uno tiene a lo sumo lo que le queda al padre.
  - Turnos, concurrencia y límites del entorno se copian del padre como techo.
- **Si el saldo no alcanza para todos, no se asigna a nadie:** un reparto que deja a algún hijo con cero en una dimensión falla, en vez de crear hijos que no pueden hacer nada.
- **Lo que consume un hijo se suma al padre** (`rollUpChildUsage`): el lote siguiente ve el saldo menos lo gastado, como en eve.
- **Un hijo no amplía nada.** Si el padre tiene límites de entorno, un hijo sin límites no está dentro del presupuesto del padre.
- **Superar los límites del entorno aislado no detiene el run:** la tool call que los superó falla, y el modelo recibe la observación, igual que con un timeout.
- **Sin componente nuevo:** los límites ya son de ExecutionController (ADR-004, EVO-01).

## 4. Archivos creados

- `book/chapters/43-presupuestos-heredados/chapter.md` (secciones 0–21, 9 bloques de pseudocódigo)
- `kb/04-Capitulos/ch-43-presupuestos-heredados.md`, `kb/03-Contratos/C-057-executionusage.md`
- `diagrams/archify/capitulo-43-presupuestos-heredados.json` + `rendered/…html`; `diagrams/mindmap/chapter-43.diagram` (generado)
- este plan

## 5. Archivos modificados

- `registry/contracts.yaml`: C-012 v2, C-057
- `registry/glossary.yaml`: Inherited Budget, ExecutionUsage
- `registry/debt.yaml`: D-026 → `resolved` (CH-43)
- `docs/adr/ADR-004-presupuesto-jerarquico.md`: Accepted, con los ajustes 4 (`consumed` opcional) y 5 (`sandboxLimits`)
- `book/book.yaml`; CH-42 `next_chapter: CH-43`
- **CH-39:** RQ-CH39-03 y su pregunta de §21 dicen "uso acumulado del run" en vez de `ExecutionUsage`: al volverse contrato en CH-43, `validate-retrieval-set` rechaza nombrarlo antes (entidad no introducida todavía)
- KB: C-012 a v2; índices de contratos y capítulos; glosario; navegación de CH-42

## 6. Resultado real del pipeline

- **Rojo:** `validate-chapter` falló con solo el frontmatter; `validate-debt` marcó D-026 vencida.
- **Registro:** `validate-contracts` OK (57), `validate-components` OK (29), `validate-debt` OK.
- **Verde:** `validate-chapter` OK (22 secciones, 9 bloques, 1 contrato, 0 componentes); `validate-retrieval-set` OK (4/4/2/1/3/4), sin ajustes. Grep de plataformas vacío.
- **Primer `build-all`: FALLÓ** en RQ-CH39-03 (nombraba `ExecutionUsage`, ahora introducido en CH-43). Corregida la redacción, **`build-all` exit 0 con 44/44 capítulos y 44/44 retrieval sets.** `dist/book.pdf` 6,3 MB; `Missing character` en 6; 0 `Could not fetch`.
- **Archify:** showcase 9/9, 0/0; `check` 9/9; visual-check pass, revisado a 1440×900 (claro y oscuro); 11 mensajes, 4 participantes.

## 7. Definition of Done

- [x] Validadores de CH-43 en verde; C-057 registrado; C-012 en v2 con `modified_by: [CH-43]`; ADR-004 Accepted; D-026 resolved.
- [x] 44/44 capítulos en verde; `build-all` exit 0.
- [x] Archify validado; KB; CH-42 `next_chapter` = CH-43.

## 8. Deuda

- Sin deuda nueva. Lo de §18 del capítulo se declaró explícitamente:
  - los repartos desiguales serían otra función con la misma verificación: no es deuda;
  - la profundidad máxima de delegación ya está planeada dentro de INV-E06 en CH-44: no es deuda;
  - cancelar a los hijos se cablea con la invocación entre agentes en CH-44: no es deuda;
  - hacer cumplir físicamente los límites del entorno es infraestructura del aislamiento: no es deuda.
