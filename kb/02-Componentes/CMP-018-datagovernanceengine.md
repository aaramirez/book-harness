---
id: "CMP-018"
tipo: componente
nombre: "DataGovernanceEngine"
capitulo: "CH-20"
tags: [componente, cmp-018]
consumes: ["C-004"]
produces: ["C-010", "C-011", "C-030"]
articulos_constitucionales: ["P-13", "P-22", "INV-18", "INV-19", "INV-20", "INV-E11"]
---

# DataGovernanceEngine (CMP-018)

> Componente introducido en [[ch-20-data-governance|CH-20]] — parte del runtime del arnés.

## Responsabilidad

Clasificar cualquier dato que fluye por el sistema (un ContextBlock ya seleccionado, un ToolResult ya producido, o cualquier otro dato futuro) con un nivel de sensibilidad, un requisito de residencia, una fecha límite de retención, una bandera de legal-hold y una referencia de lineage — produciendo una etiqueta de gobernanza portátil que viaja junto con el dato a través de fronteras de componentes, de forma completamente independiente de si el modelo entiende o acepta esos requisitos — sin decidir si ese dato es relevante para el turno actual, sin decidir si puede verse en absoluto, sin reclasificar un secreto ya clasificado por CredentialBroker y sin producir evidencia de auditoría inmutable.

## Decisiones que posee (owns)

- Classification, residency, retention, lineage, encryption, deletion and legal-hold requirements MUST be enforceable independently of model reasoning (cita literal, P-22) — clasificar, en exclusiva, cualquier dato que fluya por el sistema con esos requisitos, resuelta por completo fuera del razonamiento del modelo
- Data governance policy follows context and artifacts across component boundaries (cita literal, INV-E11) — producir una etiqueta portátil (DataGovernanceLabel), referenciada por subjectRef, consultable desde cualquier componente sin reabrir el dato original
- decidir, para un plazo de retención dado, si el borrado ya es exigible, sigue sin serlo, o está suspendido por una preservación legal — sin borrar ni reemplazar nunca la fecha de retención original al aplicar esa suspensión
- rechazar por defecto (fail-closed), hacia el nivel de clasificación más conservador (RESTRICTED), cualquier dato sin regla de gobernanza conocida
- rechazar por defecto un DataGovernanceLabel sin referencia de sujeto o sin procedencia

## Decisiones que NO posee (does_not_own)

- seleccionar, rankear o componer qué contexto es relevante para que el modelo razone sobre un turno (ContextEngine, CMP-004, ya introducido en CH-04 — la frontera más importante de este capítulo: ContextEngine decide QUÉ material entra dentro de un presupuesto; DataGovernanceEngine decide QUÉ REQUISITOS de gobierno aplican a lo que ya se decidió incluir)
- autorizar si un dato puede verse en absoluto (PolicyEngine, CMP-005, ya introducido en CH-05 — distinta pregunta, distinto dominio: "¿cuán sensible es esto?" nunca es "¿puede verse esto en absoluto?")
- reclasificar un secreto que CredentialBroker ya clasificó con CredentialClassification (CredentialBroker, CMP-014, ya introducido en CH-16 — esquema narrow de dos valores, exclusivo de credenciales; DataGovernanceEngine generaliza P-22 a cualquier OTRO dato, sin tocar el contrato de CH-16)
- producir evidencia de auditoría estructuralmente inmutable sobre una clasificación ya producida (AuditLedger, CMP-017, ya introducido en CH-19 — un DataGovernanceLabel describe la clasificación vigente hoy, no evidencia permanente de que ocurrió)
- aislar operacionalmente los runs de un tenant (OperationalController, CMP-016, ya introducido en CH-18 — aislamiento operacional es una decisión distinta de clasificar un dato, aunque ambas toquen, en espíritu, "quién puede ver qué")
- ejecutar el borrado real, el cifrado real, o el mecanismo real que mueve o almacena un dato físicamente dentro de una región concreta (Preview, infraestructura de borde)
- generar por sí mismo el subjectRef, la procedencia o la bandera de legal-hold — todas llegan como señales de entrada ya resueltas (mismo patrón que targetRef en CH-18 o subjectRef en CH-19)

## Contratos

| Dirección | Contratos |
|-----------|-----------|
| 🡒 Consume | [[C-004-executioncontext|C-004]] |
| 🡐 Produce | [[C-010-agentevent|C-010]], [[C-011-harnesserror|C-011]], [[C-030-datagovernancelabel|C-030]] |

## Artículos constitucionales

P-13, P-22, INV-18, INV-19, INV-20, INV-E11

## Dependencias

Ninguna (componente autocontenido)

## Contexto del libro

- Introducido en: [[ch-20-data-governance|CH-20]]
- Ver: [[Index|Mapa del libro]] · [[Architecture-Constitution|Constitución]]
