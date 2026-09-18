# Plan / Registro de ejecución — Capítulo 27: Integración Enterprise, los Caminos de Control y Traspaso de un Turno Gobernado

**Fecha:** 2026-09-18
**Estado:** ✅ Completado, sobre el estado dejado por CH-26 (`planes/2026-09-18-capitulo-26-integracion-enterprise-camino-feliz.md`) — el camino feliz de un turno enterprise (`runGovernedEnterpriseTurn`) ya conectaba `AdmissionController`/`DataGovernanceEngine`/`SkillLibrary`/`CredentialBroker`/`IdempotencyGuard`/`AuditLedger` de punta a punta.
**Depende de:**
- `2026-09-14-capitulo-13-integracion-caminos-de-gobierno.md` (plantilla estructural exacta: segundo capítulo de una pareja de integración, caminos NO felices)
- `2026-09-18-capitulo-26-integracion-enterprise-camino-feliz.md` (deja documentados, en su propia sección 18, los dos componentes del Amendment todavía sin una sola invocación real: `OperationalController` y `HandoffCoordinator`)
- `2026-09-17-capitulo-18-operational-controller.md`, `2026-09-18-capitulo-23-handoff-coordinator.md`
- `2026-09-14-capitulo-05-policy-engine.md` (el camino de denegación severa parte de `PolicyDecision.outcome = DENY`, CH-05)

**Nota de proceso**: el subagente escribió CH-26 y CH-27 en la misma sesión (decidió honestamente que 8 componentes no cabían en un solo capítulo disciplinado, mismo criterio que ya separó CH-12/CH-13), pero esa sesión se cortó por límite de uso antes de comitear — ambos capítulos y los registries quedaron completos y bien formados en disco. Esta sesión verificó el contenido sin reescribirlo, corrió el build limpio de los 28 capítulos, confirmó la cobertura total de los 64 principios/invariantes, escribió este documento (el de CH-26 ya existía) y completa el commit/push de ambos capítulos juntos.

---

## 1. Objetivo

Escribir el segundo y último capítulo de integración de Amendment v1.1, cerrando los 2 componentes que CH-26 dejó explícitamente pendientes: `OperationalController` (CH-18, kill switch que interrumpe un run desde afuera, sin cooperación del ciclo cognitivo — `INV-E14`) y `HandoffCoordinator` (CH-23, traspaso estructurado hacia un humano — `INV-E12`). Con este capítulo, los 8 componentes del Amendment v1.1 planeados para integración (de los 9 totales — `AgentCommunicationGateway`, CH-15, queda fuera con justificación explícita, ver §2) quedan conectados con pseudocódigo real al runtime de Article III y entre sí.

## 2. Alcance: dos caminos, ninguno el "camino feliz"

Mismo criterio que separó CH-12 de CH-13: mezclar el camino feliz (CH-26) con los caminos de interrupción/escalación en una sola función habría mezclado dos familias de decisión distintas. CH-27 escribe **dos funciones nuevas**, ninguna de las cuales modifica el pseudocódigo ya publicado de `runGovernedEnterpriseTurn` (CH-26), `runAgentTurnEndToEnd` (CH-12) ni de ningún componente:

1. **`interruptGovernedEnterpriseRunWithKillSwitch(...)`** — un `ControlDirective` de tipo `KILL_SWITCH` (`OperationalController`, CH-18: `issueControlDirective` → `applyControlDirective`, forzando `AgentRunStatus.CANCELLED` sin invocar `AgentLoop.runTurn` ni `ExecutionController.evaluateExecutionContinuation` — primera cita con ejecución real de `INV-E14`) interrumpe un run enterprise ya en curso, y el resultado siempre se empaqueta hacia un humano vía `createHandoffPackage` (CH-23, `reason = KILL_SWITCH`) — un run detenido a la fuerza no queda `CANCELLED` sin que nadie continúe lo pendiente.
2. **`escalateGovernedEnterpriseRunAfterSevereDenial(...)`** — una `PolicyDecision` con `outcome = DENY` (`PolicyEngine`, CH-05) que se considera "severa" (señal asumida como dada, no modelada en este capítulo) no sigue el camino normal de `runAgentTurnWithPolicyDenial` (CH-13, que construye una observación de vuelta al modelo) sino que se empaqueta vía `createHandoffPackage` (CH-23, `reason = EXPLICIT_ESCALATION`) — transfiriendo la decisión a un humano en vez de dejar que el modelo lo intente de nuevo.

Ambas funciones invocan `AuditLedger.recordAuditEntry` (CH-19) ADEMÁS de `emitAndDistribute`/`EventBus.distributeEvent` (CH-12/CH-09) — un `ControlDirective` aplicado y un `HandoffPackage` creado son, ambos, decisiones críticas que `P-25` exige preservar como evidencia inmutable, no solo telemetría.

**Explícitamente fuera de alcance de CH-26/CH-27 (documentado con justificación honesta, no omitido)**: `AgentCommunicationGateway` (CH-15) — no aplica a la escala de un turno individual, es interoperabilidad entre agentes; `EvaluationHarness` (CH-22) — opera antes de que exista ningún run, no dentro de uno; `ExecutionFabricAdapter` (CH-21) — describe topología de despliegue, ortogonal a la lógica de un turno.

## 3. Verificación (ejecutada por esta sesión tras encontrar el trabajo completo sin comitear)

```
rm -rf dist && ./scripts/build-all
```
Exit 0. 28 capítulos válidos (`validate-chapter`/`validate-retrieval-set`), 35 contratos, 22 componentes (sin cambios respecto a CH-25 — ni CH-26 ni CH-27 introducen nada nuevo al registry). `chapter-27.diagram`: 162 nodos/245 aristas (mismo conteo de aristas que CH-25/CH-26 — esperado, ningún capítulo de integración pura agrega aristas al `BookMindMap`, limitación de tooling ya documentada desde CH-12). `dist/book.pdf`: 719 páginas.

`pypdf`: el texto extraído contiene `runGovernedEnterpriseTurn`, `interruptGovernedEnterpriseRunWithKillSwitch`, `escalateGovernedEnterpriseRunAfterSevereDenial`, y los 8 nombres de componente cableados (`AdmissionController`, `CredentialBroker`, `IdempotencyGuard`, `AuditLedger`, `DataGovernanceEngine`, `OperationalController`, `HandoffCoordinator`, `SkillLibrary`). Web: las 28 páginas tienen exactamente 1 SVG inline cada una; navegación CH-25↔CH-26↔CH-27 verificada (`next_chapter`/`previous_chapter` consistentes en los tres frontmatters).

**Cobertura total de principios/invariantes** (verificado con `scripts/lib/registries.js#loadConstitutionArticleIds` contra `frontmatter.constitutional_articles` de los 28 capítulos, no por grep de texto libre): **64/64** definidos, **64/64** citados, 0 sin citar.

## 4. Deuda intencional remanente (documentada, no oculta)

- `runGovernedEnterpriseTurn` (CH-26) y `runAgentTurnEndToEnd` (CH-12) siguen sin invocar, dentro de su propio cuerpo, ninguna de las funciones de CH-27 — son invocaciones alternativas, nunca ramas agregadas al pseudocódigo ya publicado.
- Quién decide que una `PolicyDecision` es "severa": señal asumida como dada, no modelada.
- Las transiciones `PENDING → ACCEPTED → COMPLETED` de `HandoffPackage.status`: deuda ya heredada de CH-23 §18, no resuelta aquí.
- `AgentCommunicationGateway` (CH-15) permanece sin integrar a ningún flujo de turno — decisión explícita, no un olvido.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
