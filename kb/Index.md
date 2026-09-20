---
id: index
tipo: moc
tags: [moc, indice, libro]
---

# ¿Cómo construir un arnés? — Knowledge Base

> **Mapa de conocimiento** del libro *¿Cómo construir un arnés?* y su harness de producción (`book-harness`).
> Constitución v1.0 + Enmienda v1.1 · 22 componentes · 35 contratos · 28 capítulos.

## 🗺️ Rutas de entrada

| Ruta | Qué encontrarás | Entrada |
|------|----------------|---------|
| **Cimientos** | Constitución, artículos, enmienda | [[Architecture-Constitution]] |
| **El libro** | 28 capítulos en orden, con resultado esperado | [[04-Capitulos/00-Índice|Índice de capítulos]] |
| **Runtime** | Los 22 componentes del arnés | [[02-Componentes/00-Índice|Índice de componentes]] |
| **Contratos** | Las 35 estructuras de datos canónicas | [[03-Contratos/00-Índice|Índice de contratos]] |
| **Vocabulario** | Los 134 términos canónicos | [[05-Glosario/Glosario]] |
| **Harness** | Agents, skills y planes del proyecto | [[06-Harness/00-Índice]] |

## 🏛️ Constitución (los cimientos)

**Regla suprema:** *Los sistemas probabilísticos pueden proponer decisiones. Los sistemas determinísticos deben gobernar las consecuencias.*

- [[Article-I-Principios|Artículo I — Principios fundamentales (P-01..P-15)]]
- [[Article-II-Invariantes|Artículo II — Invariantes (INV-01..INV-20)]]
- [[Article-III-Soberania|Artículo III — Soberanía de componentes]]
- [[Article-IV-Decision-Ownership|Artículo IV — Titularidad de decisiones]]
- [[Article-V-Lifecycle|Artículo V — Ciclo de vida]]
- [[Article-VI-Execution|Artículo VI — Ejecución]]
- [[Article-VII-Failure|Artículo VII — Semántica de fallos]]
- [[Article-VIII-Human-Interaction|Artículo VIII — Interacción humana]]
- [[Article-IX-Resources|Artículo IX — Recursos y presupuestos]]
- [[Article-X-Observability|Artículo X — Observabilidad]]
- [[Article-XI-Evolution|Artículo XI — Evolución]]
- [[Article-XII-Boundary|Artículo XII — Frontera determinística vs. agéntica]]
- [[Amendment-v11|Enmienda v1.1 — Enterprise (P-16..P-30, INV-E01..INV-E14)]]

## 🧩 Componentes del runtime (resumen)

| ID | Componente | Rol |
|----|-----------|-----|
| [[CMP-001-agentloop|CMP-001]] | AgentLoop | Ciclo cognitivo model → action → observation |
| [[CMP-002-toolruntime|CMP-002]] | ToolRuntime | Ejecución controlada de tool calls |
| [[CMP-003-modelgateway|CMP-003]] | ModelGateway | Invocación del modelo vía providers |
| [[CMP-004-contextengine|CMP-004]] | ContextEngine | Selección/composición de contexto |
| [[CMP-005-policyengine|CMP-005]] | PolicyEngine | Autorización determinística de acciones |
| [[CMP-006-humaninteractionservice|CMP-006]] | HumanInteractionService | Aprobaciones humanas |
| [[CMP-007-executioncontroller|CMP-007]] | ExecutionController | Presupuestos y límites operacionales |
| [[CMP-008-capabilityregistry|CMP-008]] | CapabilityRegistry | Registro y resolución de capabilities |
| [[CMP-009-eventbus|CMP-009]] | EventBus | Distribución desacoplada de eventos |
| [[CMP-010-sessionmanager|CMP-010]] | SessionManager | Persistencia durable de sesiones |
| [[CMP-011-agentcore|CMP-011]] | AgentCore | Identidad y nacimiento de un AgentState |
| ... | (CH-14..CH-24: componentes enterprise) | [[02-Componentes/00-Índice|Ver los 22]] |

[^1]: La lista completa con los 22 componentes está en [[02-Componentes/00-Índice|Índice de componentes]].

## 📚 Los 28 capítulos de un vistazo

| Tramo | Capítulos | Tema |
|-------|-----------|------|
| **Cimientos** | CH-00 | La constitución y los contratos canónicos |
| **Core** | CH-01..CH-11 | Los 11 componentes del Article III (uno por capítulo) |
| **Integración** | CH-12..CH-13 | Camino feliz y caminos de gobierno de un AgentRun |
| **Enterprise** | CH-14..CH-24 | Enmienda v1.1: ingreso, interoperabilidad, credenciales, confiabilidad, control, auditoría, gobierno de datos, despliegue, evaluación, handoff, skills |
| **Cierre** | CH-25 | Epílogo: el orden que nunca se declaró en prosa |
| **Enterprise II** | CH-26..CH-27 | Integración enterprise: camino feliz y control/traspaso |

Ver [[04-Capitulos/00-Índice|índice completo de capítulos]].

## 🔧 El harness (proyecto)

- [[06-Harness/00-Índice|Índice del harness]] — agents, skills, planes, estructura del repo
- [[00-Inicio/Como-Usar-la-KB|Cómo usar esta KB]]

---
*Generado desde `registry/components.yaml`, `registry/contracts.yaml`, `registry/glossary.yaml`, `book/book.yaml` y `constitution/ARCHITECTURE_CONSTITUTION.md`.*
