# Glosario

Vocabulario técnico canónico del libro. Esta página es la versión legible para humanos de
`registry/glossary.yaml` (fuente de verdad; en una versión posterior del harness se generará
automáticamente desde ese registry — ver deuda intencional en el Registro de ejecución del plan).

## Conceptos

- **Harness** — Runtime gobernado que permite a sistemas probabilísticos (modelos) proponer
  decisiones mientras mecanismos determinísticos controlan su ejecución, límites y consecuencias.
- **Architecture Constitution** — Documento rector que define los principios (`P-xx`), invariantes
  (`INV-xx`) y fronteras de propiedad de componentes que gobiernan la evolución del arnés.
- **Deterministic Boundary** — Frontera explícita que separa lo que un modelo puede proponer de lo
  que el runtime determinístico decide y ejecuta.
- **Component Sovereignty** — Principio por el cual cada componente del runtime tiene una
  responsabilidad exclusiva y fronteras explícitas de lo que NO posee.
- **Probabilistic System** — Componente cuya salida (típicamente un modelo de lenguaje) es una
  propuesta razonada, no una decisión operacional vinculante.

## Contratos (introducidos en el Capítulo 0)

- **`AgentMessage`** (`C-001`) — Contrato canónico e independiente de proveedor para representar
  un mensaje dentro del ciclo cognitivo del agente.
- **`AgentConfig`** (`C-002`) — Configuración declarativa de un agente sobre el runtime compartido.
- **`AgentState`** (`C-003`) — Estado operativo de una ejecución (run) del agente, conceptualmente
  independiente del estado persistente de la sesión.
- **`ExecutionContext`** (`C-004`) — Contexto de ejecución que acompaña cada operación dentro de
  un run.
- **`AgentEvent`** (`C-010`) — Envelope canónico de evento observable producido por cualquier
  acción significativa del runtime.
- **`HarnessError`** (`C-011`) — Contrato de error clasificado (categoría, recuperabilidad,
  reintentabilidad).
- **`ExecutionBudget`** (`C-012`) — Conjunto explícito de límites operacionales que acota toda
  ejecución de un agente.

Ver `registry/contracts.yaml` para la ficha completa de cada contrato y `registry/components.yaml`
para los componentes de runtime (vacío hasta el capítulo que introduzca el primero, fuera del
alcance de esta ejecución BH-v0.1).
