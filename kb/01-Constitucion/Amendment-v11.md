---
id: amendment-v11
tipo: constitucion
tags: [constitucion, enmienda, enterprise]
---

# Enmienda v1.1 — Enterprise Activation, Interoperability and Operations

Extiende la constitución para el plano **enterprise**: activación, interoperabilidad entre agentes y operaciones. Introduce **P-16..P-30**, **INV-E01..INV-E14** y los **8 planos canónicos**.

## Nuevos principios (P-16..P-30)

| Principio | Tema |
|-----------|------|
| P-16 | La activación es independiente de la ejecución |
| P-17 | La admisión precede a la ejecución |
| P-18 | La semántica de comunicación es independiente de protocolo/transporte |
| P-19 | La interoperabilidad externa es basada en adapters |
| P-20 | Delegación interna y federación externa son preocupaciones distintas |
| P-21 | La autoridad delegada es explícita y de menor privilegio |
| P-22 | Los datos empresariales se gobiernan durante todo su ciclo de vida |
| P-23 | La ejecución durable es una propiedad del core del runtime |
| P-24 | Los side effects requieren semánticas de idempotencia |
| P-25 | La evidencia de auditoría es distinta de la telemetría operacional |
| P-26 | Las capabilities tienen ciclos de vida gobernados |
| P-27 | La topología de despliegue es independiente de la semántica del agente |
| P-28 | Producción y evaluación son preocupaciones de ejecución separadas |
| P-29 | Los outcomes de negocio son observabilidad de primera clase |
| P-30 | El control operacional puede anular la autonomía |

## Planos canónicos (8)

1. Ingress & Activation Plane
2. Execution Plane
3. Agent Interoperability Plane
4. Capability & Integration Plane
5. Data & Context Plane
6. Control Plane
7. Reliability Plane
8. Observability & Governance Plane

## Componentes que la materializan

[[CMP-012-admissioncontroller|AdmissionController]] (CH-14) · [[CMP-013-agentcommunicationgateway|AgentCommunicationGateway]] (CH-15) · [[CMP-014-credentialbroker|CredentialBroker]] (CH-16) · [[CMP-015-idempotencyguard|IdempotencyGuard]] (CH-17) · [[CMP-016-operationalcontroller|OperationalController]] (CH-18) · [[CMP-017-auditledger|AuditLedger]] (CH-19) · [[CMP-018-datagovernanceengine|DataGovernanceEngine]] (CH-20) · [[CMP-019-executionfabricadapter|ExecutionFabricAdapter]] (CH-21) · [[CMP-020-evaluationharness|EvaluationHarness]] (CH-22) · [[CMP-021-handoffcoordinator|HandoffCoordinator]] (CH-23) · [[CMP-022-skilllibrary|SkillLibrary]] (CH-24)

Ver también: [[Architecture-Constitution|Constitución]] · [[Index|Mapa del libro]]
