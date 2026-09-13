# Introducción

## Qué vas a construir

A lo largo de este libro construimos, capítulo a capítulo, un arnés de agentes completo: desde el
ciclo cognitivo mínimo (`AgentLoop`) hasta la ejecución de herramientas gobernada por políticas
(`ToolRuntime` + `PolicyEngine`), la interacción humana durable (`HumanInteractionService`), la
observabilidad basada en eventos (`EventBus`) y, eventualmente, la integración con estándares de
interoperabilidad entre agentes.

Cada capítulo sigue la misma secuencia fija:

```text
Current Architecture
   ↓
Problem
   ↓
Why the Current Architecture Is Insufficient
   ↓
Constitutional Impact
   ↓
New Concepts → New Data Structures → New Contracts/Interfaces → Component Responsibilities
   ↓
Dependency Relationships → Sequence Diagram → Pseudocode
   ↓
State Transitions → Failure Semantics → Events Produced → Security/Policy Implications
   ↓
Tests
   ↓
Architecture After This Chapter
   ↓
What We Deliberately Do Not Solve Yet
   ↓
Next Increment
```

## Por qué esta estructura y no prosa libre

Porque la meta de este libro no es que puedas repetir ejemplos de código sueltos, sino que puedas
razonar la arquitectura de un arnés de principio a fin: qué componente posee cada decisión, qué
contrato conecta a dos componentes, qué invariante de la Constitution se preserva o se introduce
en cada paso, y qué queda deliberadamente sin resolver hasta el capítulo siguiente.

## Cómo leer el pseudocódigo

Este libro usa una gramática de pseudocódigo propia, independiente de cualquier lenguaje de
programación real (`STRUCT`, `ENUM`, `INTERFACE`, `FUNCTION`, ...). Ninguna entidad aparece en un
bloque de pseudocódigo sin haber sido definida antes — esta regla ("no magic entities") se aplica
y se valida automáticamente sobre el propio texto del libro; ver `scripts/validate-chapter`.

## El capítulo 0

El Capítulo 0, "La Constitución Arquitectónica de un Arnés", es el único punto de partida posible:
antes de escribir `AgentLoop`, hace falta el documento que define qué principios e invariantes
debe respetar. Ese capítulo introduce el vocabulario base (`AgentMessage`, `AgentState`,
`ExecutionContext`, `AgentEvent`, `HarnessError`, `ExecutionBudget`, `AgentConfig`) que el resto
del libro reutiliza sin redefinir.
