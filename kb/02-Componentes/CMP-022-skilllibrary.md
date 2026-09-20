---
id: "CMP-022"
tipo: componente
nombre: "SkillLibrary"
capitulo: "CH-24"
tags: [componente, cmp-022]
consumes: ["C-004"]
produces: ["C-010", "C-011", "C-035"]
articulos_constitucionales: ["P-07", "P-13", "INV-18", "INV-19", "INV-20"]
---

# SkillLibrary (CMP-022)

> Componente introducido en [[ch-24-skill-library|CH-24]] — parte del runtime del arnés.

## Responsabilidad

Registrar el descriptor de una skill — conocimiento procedural reusable, nombre canónico, versión y una referencia opaca al procedimiento/guía real — como una capa separada del core del agente, de las tools/capabilities y de la identidad del agente, y resolver qué SkillDescriptor aplica a una situación nombrada — sin resolver qué implementación concreta satisface una capability solicitada, sin representar la identidad/configuración de un agente, sin ejecutar ningún side effect y sin decidir autorización sobre ninguna acción.

## Decisiones que posee (owns)

- Skills encode reusable procedural knowledge (cita literal, título P-07) — El conocimiento procedural reusable debe estar separado del core, las tools y la identidad del agente (cita literal, texto P-07) — registrar, en exclusiva, el descriptor de una skill como conocimiento procedural reusable, como una capa separada de AgentCore (identidad del agente, CMP-011, CH-11), de CapabilityRegistry/ToolRuntime (tools/capabilities, CMP-008/CMP-002, CH-08/CH-02) y de PolicyEngine (autorización, CMP-005, CH-05)
- resolver, contra ese registro, qué SkillDescriptor aplica a una situación nombrada — produciendo una referencia consultable a un procedimiento reusable, nunca una acción ejecutable ni una implementación de capability
- rechazar por defecto (fail-closed) una resolución de skill invocada sin un situationName real, o cuyo situationName no corresponde a ningún SkillDescriptor registrado

## Decisiones que NO posee (does_not_own)

- resolver qué implementación concreta satisface una capability solicitada (CapabilityRegistry, CMP-008, ya introducido en CH-08 — la frontera más importante de este capítulo: CapabilityRegistry resuelve QUÉ CÓDIGO/API concreto ejecuta una acción; SkillLibrary resuelve QUÉ PROCEDIMIENTO/GUÍA reusable aplica a una situación — dos preguntas ortogonales, aun cuando ambas comparan un nombre de texto libre contra un registro propio)
- representar la identidad/configuración de un agente (AgentCore, CMP-011, ya introducido en CH-11 — AgentConfig, C-002, CH-00, ya representa qué es un agente independiente de cualquier run; ningún SkillDescriptor resuelto se embebe jamás dentro de AgentConfig ni de AgentState)
- ejecutar el side effect en sí de ninguna acción (ToolRuntime, CMP-002, ya introducido en CH-02)
- decidir autorización sobre ninguna acción, incluida la lectura de una skill (PolicyEngine, CMP-005, ya introducido en CH-05)
- certificar un candidato de skill antes de su promoción a producción (EvaluationHarness, CMP-020, ya introducido en CH-22 — EvaluationHarness ya declara evaluable, entre otros candidatos, a una skill antes de su promoción controlada; SkillLibrary registra y resuelve una skill YA registrada, nunca decide si debe promoverse)
- generar por sí mismo el contenido procedural real detrás de procedureRef (Preview, infraestructura de borde — referencia opaca, mismo patrón que implementationRef en CapabilityDescriptor, CH-08)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-035-skilldescriptor|C-035]] |

## Artículos constitucionales

P-07, P-13, INV-18, INV-19, INV-20

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-24-skill-library|CH-24]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
