---
id: "CMP-008"
tipo: componente
nombre: "CapabilityRegistry"
capitulo: "CH-08"
tags: [componente, cmp-008]
consumes: ["C-004", "C-007"]
produces: ["C-008", "C-010", "C-011", "C-018"]
articulos_constitucionales: ["P-03", "P-13", "P-26", "INV-03", "INV-04", "INV-05", "INV-18", "INV-19", "INV-20"]
---

# CapabilityRegistry (CMP-008)

> Componente introducido en [[ch-08-capability-registry|CH-08]] — parte del runtime del arnés.

## Responsabilidad

Registrar las capabilities disponibles junto con su descriptor (nombre canónico, versión, schema de entrada esperado y una referencia opaca a su implementación concreta), resolver el capabilityName de una RawToolCallProposal contra ese registro, validar sus rawArguments contra el schema declarado y producir un ToolCall resuelto — sin ejecutar la capability, sin invocar al modelo ni interpretar su propuesta cruda, sin evaluar policy/autorización y sin decidir continuación de turno.

## Decisiones que posee (owns)

- registrar el descriptor de una capability disponible (nombre, versión, schema de entrada, referencia de implementación)
- resolver qué implementación satisface una capability solicitada
- validar los argumentos crudos de una propuesta contra el schema declarado por la capability resuelta
- desacoplar la intención de una capacidad de su implementación concreta

## Decisiones que NO posee (does_not_own)

- ejecutar la capability ya resuelta (ToolRuntime, CMP-002, ya introducido en CH-02 — Article IV: "ToolRuntime → How should an approved action be executed?")
- invocar al modelo seleccionado o interpretar su propuesta cruda antes de que llegue como ModelResponse (ModelGateway, CMP-003, ya introducido en CH-03 — Article IV: "ModelGateway → How should the selected model be invoked?")
- evaluar policy/autorización sobre si la acción ya resuelta debe ejecutarse (PolicyEngine, CMP-005, ya introducido en CH-05 — distinción cuidadosa: "¿existe e implementa correctamente esta capability?" es de CapabilityRegistry, "¿está permitido usarla ahora?" es de PolicyEngine)
- decidir si otro turno de razonamiento debe ocurrir (AgentLoop, CMP-001, ya introducido en CH-01)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]], [[C-007-modelresponse|C-007]] |
| 🡐 Produce | [[C-008-toolcall|C-008]], [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-018-capabilitydescriptor|C-018]] |

## Artículos constitucionales

P-03, P-13, P-26, INV-03, INV-04, INV-05, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-08-capability-registry|CH-08]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
