---
id: diagramas
tipo: referencia
tags: [diagramas, archify]
---

# Diagramas del Harness

Los diagramas viven en el repositorio en `diagrams/` — no se copian a la KB para evitar duplicados; esta nota los referencia.

## Qué hay en `diagrams/`

| Ruta | Descripción |
|------|-------------|
| `diagrams/archify/<slug>.json` | Fuente Archify (especificación JSON validada con `archify validate --quality showcase`) |
| `diagrams/archify/rendered/<slug>.html` | HTML autocontenido: pan/zoom, búsqueda, vistas guiadas, tema claro/oscuro |
| `diagrams/mindmap/chapter-NN.diagram` | Mapa mental progresivo de cada capítulo (generado por `build-mind-map`, embebido en el PDF) |

55 diagramas Archify: 5 transversales y 50 de capítulo (CH-00..CH-49).

## Diagramas transversales

| Slug | Título |
|------|--------|
| `capa-enterprise` | La Capa de Gobierno Enterprise |
| `estados-de-un-run` | Los 11 Estados de un AgentRun |
| `nucleo-del-arnes` | El Núcleo del Arnés |
| `turno-gobernado` | El Turno Gobernado de Punta a Punta |
| `un-agentrun-real` | Un AgentRun de Punta a Punta |

## Diagramas por capítulo

| Slug | Título |
|------|--------|
| `capitulo-00-constitucion` | CH-00 — La Constitución Arquitectónica de un Arnés |
| `capitulo-01-agent-loop` | CH-01 — El Agent Loop y el Ciclo de Ejecución Cognitiva |
| `capitulo-02-tool-runtime` | CH-02 — ToolRuntime y la Ejecución Controlada de una Tool Call |
| `capitulo-03-model-gateway` | CH-03 — ModelGateway y la Invocación Real del Modelo |
| `capitulo-04-context-engine` | CH-04 — ContextEngine y Qué Ve Realmente el Modelo |
| `capitulo-05-policy-engine` | CH-05 — PolicyEngine y la Frontera de Autorización |
| `capitulo-06-human-interaction-service` | CH-06 — HumanInteractionService y la Reanudación de una Ejecución Pausada |
| `capitulo-07-execution-controller` | Capítulo 7 — ExecutionController y los Límites Operacionales de una Ejecución |
| `capitulo-08-capability-registry` | Capítulo 8 — CapabilityRegistry y la Resolución Real de una Tool Call |
| `capitulo-09-event-bus` | Capítulo 9 — EventBus y la Distribución Desacoplada de un Evento Ya Producido |
| `capitulo-10-session-manager` | Capítulo 10 — SessionManager y la Persistencia Durable de una Sesión |
| `capitulo-11-agent-core` | Capítulo 11 — AgentCore y el Nacimiento de un AgentState |
| `capitulo-12-integracion-camino-feliz` | Capítulo 12 — Integración: el Camino Feliz de un AgentRun Completo |
| `capitulo-13-integracion-caminos-de-gobierno` | CH-13 — Integración, los Caminos de Gobierno de un AgentRun |
| `capitulo-14-admission-controller` | Capítulo 14 — AdmissionController y la Admisión de una Activación Cruda |
| `capitulo-15-agent-communication-gateway` | Capítulo 15 — AgentCommunicationGateway y la Frontera Explícita entre Agentes |
| `capitulo-16-credential-broker` | Capítulo 16 — CredentialBroker y la Resolución Segura de una Credencial |
| `capitulo-17-idempotency-guard` | Capítulo 17 — IdempotencyGuard y la Deduplicación de un Side Effect Crítico |
| `capitulo-18-operational-controller` | Capítulo 18 — OperationalController y los Kill Switches Independientes de AgentLoop |
| `capitulo-19-audit-ledger` | Capítulo 19 — AuditLedger y la Evidencia de Auditoría Estructuralmente Inmutable |
| `capitulo-20-data-governance-engine` | Capítulo 20 — DataGovernanceEngine y la Etiqueta de Gobernanza que Viaja con el Dato |
| `capitulo-21-execution-fabric-adapter` | Capítulo 21 — ExecutionFabricAdapter y la Topología de Despliegue que el Comportamiento del Agente Nunca Debe Conocer |
| `capitulo-22-evaluation-harness` | Capítulo 22 — EvaluationHarness y la Certificación de un Candidato Antes de que Exista Ningún Run |
| `capitulo-23-handoff-coordinator` | Capítulo 23 — HandoffCoordinator y el Paquete Estructurado que Nunca Es Solo Prosa |
| `capitulo-24-skill-library` | Capítulo 24 — SkillLibrary y el Conocimiento Procedural que Nunca Fue una Capability |
| `capitulo-25-epilogo` | Capítulo 25 — Epílogo: El Orden que Nunca se Declaró en Prosa |
| `capitulo-26-integracion-enterprise-camino-feliz` | Capítulo 26 — Integración Enterprise: el Camino Feliz de una Activación Admitida y Gobernada |
| `capitulo-27-integracion-enterprise-caminos-de-control` | CH-27 — Integración Enterprise, los Caminos de Control y Traspaso |
| `capitulo-28-steering-follow-up` | Capítulo 28 — Steering y Follow-up |
| `capitulo-29-compactacion-sesiones-arbol` | Capítulo 29 — Compactación y Sesiones en Árbol |
| `capitulo-30-politica-de-replay` | Capítulo 30 — Política de Replay |
| `capitulo-31-identidad-del-llamante` | Capítulo 31 — La Identidad del Llamante |
| `capitulo-32-pasos-durables` | Capítulo 32 — Pasos Durables |
| `capitulo-33-esperas-durables` | Capítulo 33 — Esperas Durables |
| `capitulo-34-canales-continuacion` | Capítulo 34 — Canales y Continuación |
| `capitulo-35-entorno-aislado` | Capítulo 35 — Entorno Aislado |
| `capitulo-36-integracion-turno-durable` | Capítulo 36 — Turno Durable |
| `capitulo-37-esperas-credenciales-canales` | Capítulo 37 — Esperas y Canales |
| `capitulo-38-identidad-auditoria-retencion` | Capítulo 38 — Identidad y Retención |
| `capitulo-39-modelo-como-dato` | Capítulo 39 — El Modelo como Dato |
| `capitulo-40-extension-host` | Capítulo 40 — Extensiones |
| `capitulo-41-conexiones` | Capítulo 41 — Conexiones |
| `capitulo-42-fuentes-de-datos` | Capítulo 42 — Fuentes de Datos |
| `capitulo-43-presupuestos-heredados` | Capítulo 43 — Presupuestos Heredados |
| `capitulo-44-invocacion-entre-agentes` | Capítulo 44 — Invocación entre Agentes |
| `capitulo-45-evolucion-del-runtime` | Capítulo 45 — Evolución del Runtime |
| `capitulo-46-observabilidad-por-audiencia` | Capítulo 46 — Observabilidad por Audiencia |
| `capitulo-47-evaluacion-con-lift` | Capítulo 47 — Evaluación con Lift |
| `capitulo-48-agente-como-directorio` | Capítulo 48 — El Agente como Directorio |
| `capitulo-49-integracion-conectada` | Capítulo 49 — El Arnés Conectado |

## Cómo verlos

1. Abre el repo `book-harness` → carpeta `diagrams/archify/rendered/`
2. Abre el `.html` en cualquier navegador
3. Para editarlos, cambia el `.json` y vuelve a validar y entregar con Archify (ver `planes/2026-09-18-diagramas-interactivos-archify.md`)

Ver también: [[Index|Mapa del libro]]
