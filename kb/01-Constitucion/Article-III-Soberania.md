---
id: article-iii
tipo: constitucion
tags: [constitucion, articulo]
---

# Artículo III — Soberanía de Componentes


Define los **11 componentes canónicos** del runtime y su responsabilidad exclusiva — el mapa de quién posee qué dentro del arnés:

| Componente | Responsabilidad |
|------------|-----------------|
| AgentCore | Identidad del agente, validación de config, nacimiento del AgentState |
| AgentLoop | Ciclo cognitivo model → action → observation |
| ModelGateway | Selección e invocación del provider de modelo |
| ContextEngine | Selección, ranking, composición y compactación de contexto |
| ToolRuntime | Ejecución controlada de una tool call aprobada |
| PolicyEngine | Evaluación determinística allow/deny/require_approval |
| SessionManager | Persistencia durable de la sesión (checkpoints) |
| HumanInteractionService | Solicitudes de aprobación humana y reanudación |
| EventBus | Distribución desacoplada (fan-out) de eventos |
| ExecutionController | Presupuestos, cancelación y límites operacionales |
| CapabilityRegistry | Registro y resolución de capabilities |

Cada uno tiene una nota propia en [[02-Componentes/00-Índice|Componentes]] con sus `owns` / `does_not_own` detallados.


Ver también: [[Architecture-Constitution|Constitución]] · [[Index|Mapa del libro]]
