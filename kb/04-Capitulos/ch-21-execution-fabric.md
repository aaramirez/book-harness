---
id: "CH-21"
tipo: capitulo
titulo: "\"ExecutionFabricAdapter y la Topología de Despliegue que el Comportamiento del Agente Nunca Debe Conocer\""
tags: [capitulo, ch21]
introduces_components: ["CMP-019"]
introduces_contracts: ["C-031"]
articulos_constitucionales: ["P-13", "P-27", "INV-18", "INV-19", "INV-20"]
---

# CH-21 — "ExecutionFabricAdapter y la Topología de Despliegue que el Comportamiento del Agente Nunca Debe Conocer"

## Navegación

⬅ [[ch-20-data-governance|CH-20]] · **CH-21** · [[ch-22-evaluation-harness|CH-22]] ➡

## Resultado esperado

—

## Qué introduce este capítulo

### Componentes

- [[CMP-019-executionfabricadapter|CMP-019]] — Abstraer, detrás de una interfaz uniforme, el substrato de cómputo concreto sobre el que se materializa la ejecución de un run ya existente (in-process, worker, Kubernetes, serverless, cloud, edge, on-premise) — produciendo un ExecutionPlacement opaco y portátil que describe esa topología sin exponer el detalle real de cada substrato, y registrando, cuando aplica, una restricción de residencia sobre DÓNDE se ejecuta ese cómputo — sin decidir límites de recursos o presupuesto de un run, sin invocar proveedores de modelo, sin adaptar protocolos de comunicación entre agentes externos y sin instanciar el AgentState inicial de un run.

### Contratos

- [[C-031-executionplacement|C-031]] — ExecutionPlacement (impacto: P-27, INV-19)


## Artículos constitucionales relevantes

P-13, P-27, INV-18, INV-19, INV-20

## Localización en el repo

`book/chapters/21-execution-fabric-adapter/chapter.md`

Ver también: [[Index|Mapa del libro]] · [[04-Capitulos/00-Índice|Índice de capítulos]]
