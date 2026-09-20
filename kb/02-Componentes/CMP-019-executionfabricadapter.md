---
id: "CMP-019"
tipo: componente
nombre: "ExecutionFabricAdapter"
capitulo: "CH-21"
tags: [componente, cmp-019]
consumes: ["C-004"]
produces: ["C-010", "C-011", "C-031"]
articulos_constitucionales: ["P-13", "P-27", "INV-18", "INV-19", "INV-20"]
---

# ExecutionFabricAdapter (CMP-019)

> Componente introducido en [[ch-21-execution-fabric|CH-21]] — parte del runtime del arnés.

## Responsabilidad

Abstraer, detrás de una interfaz uniforme, el substrato de cómputo concreto sobre el que se materializa la ejecución de un run ya existente (in-process, worker, Kubernetes, serverless, cloud, edge, on-premise) — produciendo un ExecutionPlacement opaco y portátil que describe esa topología sin exponer el detalle real de cada substrato, y registrando, cuando aplica, una restricción de residencia sobre DÓNDE se ejecuta ese cómputo — sin decidir límites de recursos o presupuesto de un run, sin invocar proveedores de modelo, sin adaptar protocolos de comunicación entre agentes externos y sin instanciar el AgentState inicial de un run.

## Decisiones que posee (owns)

- Agent behavior MUST NOT depend on whether execution occurs in-process, on a worker, Kubernetes, serverless, cloud, edge or on-premise (cita literal, P-27) — abstraer, en exclusiva, el substrato de cómputo concreto sobre el que corre la ejecución de un run detrás de una interfaz uniforme
- producir, para un run ya existente (runId), una referencia opaca y uniforme al substrato de cómputo (topology + computeResourceRef) — nunca el detalle real de cada substrato concreto
- registrar, cuando aplica, una restricción de residencia geográfica sobre DÓNDE se ejecuta el cómputo de un run — distinta de dónde debe residir el DATO que ese run procesa
- rechazar por defecto (fail-closed) un ExecutionPlacement sin referencia al run que representa

## Decisiones que NO posee (does_not_own)

- decidir límites de recursos o presupuesto de un run — cuánto tiempo puede correr, cuántas tool calls concurrentes, cuánto cuesta (ExecutionController, CMP-007, ya introducido en CH-07 — la frontera más importante de este capítulo: ExecutionController decide CUÁNTO puede consumir un run ya en marcha, en cualquier substrato; ExecutionFabricAdapter describe DÓNDE/EN QUÉ TIPO DE INFRAESTRUCTURA corre ese mismo run — dos preguntas ortogonales sobre el mismo run)
- invocar proveedores de modelo concretos (ModelGateway, CMP-003, ya introducido en CH-03 — ModelGateway adapta HACIA AFUERA, hacia qué proveedor de modelo; ExecutionFabricAdapter adapta HACIA ABAJO, hacia qué substrato de cómputo corre el propio harness)
- adaptar protocolos de comunicación entre agentes externos (AgentCommunicationGateway, CMP-013, ya introducido en CH-15 — adapta hacia protocolos de interoperabilidad entre agentes, no hacia el substrato de cómputo del propio harness)
- instanciar el AgentState inicial de un run (AgentCore, CMP-011, ya introducido en CH-11 — ExecutionFabricAdapter describe sobre qué substrato corre un run YA instanciado, nunca lo crea)
- clasificar los requisitos de gobernanza de un dato, incluida su residencia (DataGovernanceEngine, CMP-018, ya introducido en CH-20 — residencyRequirement ahí describe dónde debe residir el DATO; residencyConstraint aquí describe dónde se ejecuta el CÓMPUTO del run — conceptos relacionados pero distintos)
- ejecutar el aprovisionamiento real, el scheduling real, o el mecanismo real que efectivamente coloca un proceso dentro de un pod de Kubernetes, una función serverless o un nodo edge (Preview, infraestructura de borde)
- generar por sí mismo el runId, la topología o el computeResourceRef — todas llegan como señales de entrada ya resueltas (mismo patrón que subjectRef en CH-19/CH-20)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-031-executionplacement|C-031]] |

## Artículos constitucionales

P-13, P-27, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-21-execution-fabric|CH-21]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
